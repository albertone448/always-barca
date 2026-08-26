# Notas metodológicas — always-barca

Este documento explica las decisiones técnicas y metodológicas detrás del proyecto: qué herramienta o técnica se usó en cada punto, qué problema resolvía, y por qué se eligió ese enfoque en particular. No es documentación de código línea por línea (para eso están los notebooks), es un registro de razonamiento: el "por qué" detrás de cada decisión, pensado tanto para repasar el proyecto en el futuro como para que cualquiera que revise el repositorio entienda el criterio aplicado.

Se actualiza al cierre de cada fase del proyecto.

---

## Fase 1: rendimiento, entrenador y gasto en fichajes

### Control de versiones y estructura del proyecto

El repositorio separa `data/raw/` (datos crudos, nunca modificados) de `data/processed/` (resultados de limpieza y transformación). Esto garantiza que cualquier error en el procesamiento se pueda corregir reconstruyendo desde la fuente original, sin depender de que el dato crudo siga disponible externamente. `data/raw/transfermarkt/` está excluido del control de versiones (`.gitignore`) porque el dataset de Kaggle es demasiado grande para un repositorio de GitHub y su licencia desaconseja la redistribución directa; en su lugar, el proyecto documenta cómo regenerarlo con la API de Kaggle (`kagglehub`).

### Tipos de dato al leer CSV: el problema del cero inicial

Códigos de temporada como `'0102'` o `'0203'` se guardan correctamente en CSV, pero al releerlos con `pandas.read_csv()` sin especificar tipo, se interpretan como enteros y pierden el cero inicial (`'0102'` se convierte en `102`). La solución aplicada en todo el proyecto es cargar estas columnas de forma explícita:

```python
df = pd.read_csv('archivo.csv', dtype={'temporada': str})
```

Este es un error silencioso particularmente peligroso: no lanza ninguna excepción, simplemente hace que los `merge()` y las comparaciones por temporada fallen sin encontrar coincidencias, sin ningún aviso.

### `pd.merge()`: unir tablas manteniendo el rango completo

El dataset maestro (`df_maestro`) se construye uniendo rendimiento, entrenador y gasto con `merge(..., how='left')`, siempre partiendo de la tabla que cubre las 33 temporadas completas (`rendimiento_barca`). Con `how='left'`, cualquier temporada sin dato disponible en una de las otras tablas queda marcada con `NaN` en vez de desaparecer silenciosamente, que es lo que ocurriría con un `how='inner'`.

Un hallazgo relevante durante este proceso: en el dataset de Transfermarkt, el identificador de club (`club_id`) usado en la tabla de clubes no coincidía con el identificador usado como llave foránea en la tabla de transferencias (`to_club_id`/`from_club_id`). La llave correcta resultó ser una columna distinta (`club_code`). La lección aplicada de aquí en adelante: nunca asumir que dos columnas con nombres parecidos en tablas distintas son la misma llave sin verificarlo primero con un filtro de prueba.

### `groupby()` y el patrón de "doble perspectiva" para tablas de posiciones

Cada partido de fútbol aporta información sobre dos equipos (local y visitante), pero el objetivo era una fila por equipo. La solución fue duplicar cada partido en dos filas —una desde la perspectiva del equipo local, otra desde la del visitante— y apilarlas antes de agrupar:

```python
local = df[['HomeTeam', 'FTHG', 'FTAG']].copy()
local.columns = ['equipo', 'goles_favor', 'goles_contra']
visitante = df[['AwayTeam', 'FTAG', 'FTHG']].copy()
visitante.columns = ['equipo', 'goles_favor', 'goles_contra']
partidos = pd.concat([local, visitante], ignore_index=True)
```

Este patrón evita escribir un bucle manual por equipo y es el enfoque estándar para reconstruir tablas de posiciones desde resultados partido a partido.

### Decisiones de normalización: comparar datos que pertenecen a contextos distintos

**Cambio en el sistema de puntos.** La Liga otorgaba 2 puntos por victoria hasta 1994/95 y 3 puntos desde 1995/96. En vez de normalizar los puntos en el dato base, se optó por mantener la cifra histórica real y aplicar cualquier ajuste solo en el momento puntual de una comparación entre eras. Esto preserva la fidelidad a la clasificación real de cada temporada.

**Criterio de desempate simplificado, y su costo real.** La reconstrucción de la tabla de posiciones usa diferencia de gol como único criterio de desempate, una simplificación frente al reglamento oficial de La Liga (que prioriza los enfrentamientos directos). Este atajo tuvo una consecuencia concreta: la temporada 2006/07 se calculó inicialmente con el Barça en primer lugar, cuando el título real correspondió a Real Madrid por enfrentamientos directos, ambos empatados en puntos. El error se detectó al contrastar el conteo total de títulos del dataset contra el número real conocido, y se corrigió puntualmente con la fuente documentada. La lección: una simplificación metodológica declarada explícitamente igual necesita validarse contra la realidad en los casos donde el resultado importa (títulos, posiciones límite).

**Ajuste del gasto por inflación del mercado.** Comparar gasto neto absoluto entre 1996 y 2020 es engañoso, porque el mercado de fichajes se ha inflado a un ritmo muy distinto al de la economía general. En vez de aplicar un índice de precios genérico, se calculó el gasto del Barça como proporción del gasto total de todos los clubes de La Liga esa misma temporada:

```python
proporcion_mercado_barca = gasto_neto_barca / gasto_total_liga_esa_temporada
```

Este enfoque replica, con datos propios, el mismo principio metodológico que usa el CIES Football Observatory para medir la inflación del mercado de fichajes: usar el propio volumen del mercado como referencia, no un índice de precios externo.

**Filtrado de movimientos no comerciales.** Al calcular gasto neto desde `transfers.csv`, se excluyeron las promociones desde equipos filiales y las salidas sin club de destino, por no representar operaciones reales de mercado. Esas filas no se descartaron, se conservaron aparte como un dataset propio (`barca_promociones_cantera.csv`), útil para el análisis de canteranos en la siguiente fase del proyecto.

### Estadística aplicada

**Correlación de Pearson.** Se usó para medir la fuerza y dirección de la relación lineal entre pares de variables continuas (gasto y rendimiento, goles a favor/en contra y rendimiento). Es importante tener presente su limitación: solo detecta relaciones lineales, así que puede arrojar un coeficiente bajo incluso si existe un patrón real que depende de una tercera variable o que no es lineal.

**Interpretación del valor p.** Se aplicó el umbral convencional de 0.05 para considerar un resultado estadísticamente significativo. El tamaño de la muestra demostró tener un efecto directo: la misma relación gasto-rendimiento pasó de un valor p de 0.520 (con 12 temporadas de gasto automatizado) a 0.204 (con las 33 temporadas completas), sin dejar de ser no significativa, pero mostrando cómo una muestra más grande cambia la confianza en el resultado.

**Separar variables compuestas antes de interpretarlas.** En vez de asumir que la diferencia de gol capturaba de forma equilibrada el ataque y la defensa, se calculó la correlación de cada componente por separado con el rendimiento. El resultado mostró que ambos son significativos, pero de magnitud distinta, el ataque explica más varianza que la defensa en este dataset, algo que la variable compuesta por sí sola no habría revelado.

**Precaución con muestras pequeñas.** Al desagregar la correlación ataque/defensa por entrenador (3 a 5 temporadas cada uno), varios coeficientes resultaron inestables, incluyendo un caso donde el signo se invirtió respecto al patrón general del dataset completo. Estos resultados se documentaron explícitamente como referencia exploratoria, no como evidencia estadística concluyente.

### Visualización con Matplotlib

**Formateo de ejes.** Los valores grandes (millones de euros) o las proporciones se formatearon con `FuncFormatter` para mostrarse en unidades legibles (`150M`, `20%`) en vez de notación científica. El eje de temporadas también se formateó con una función personalizada para mostrar `2020/21` en vez del año simple `2020` usado internamente para ordenar.

**Doble eje Y (`twinx()`).** Usado para graficar rendimiento y gasto en la misma figura pese a tener escalas muy distintas, cada serie con su propio eje.

**Fondo coloreado por tramos (`axvspan`).** Usado para mostrar el entrenador a cargo como una tercera dimensión en un gráfico de series de tiempo, sin necesitar un eje adicional. El mismo recurso sirvió para marcar temporadas con limitaciones de cobertura de datos (por ejemplo, la pandemia).

**Boxplots para comparar distribuciones.** Usados para comparar la dispersión del gasto entre categorías de temporada (Título, Top 4, Mala), más informativo que comparar solo promedios.

**Guardado reproducible de figuras.** Todas las visualizaciones se exportan con `fig.savefig(...)` dentro del propio código, en vez de guardarse manualmente desde la interfaz, para que se regeneren automáticamente si los datos cambian.

### Recolección y validación de datos

**BeautifulSoup para extraer tablas de HTML.** Usado para parsear contenido copiado directamente de Wikipedia y convertirlo en un DataFrame estructurado, un enfoque más robusto que intentar extraer texto con expresiones regulares.

**Por qué no se automatizó la recolección de Transfermarkt.** Transfermarkt prohíbe explícitamente el scraping automatizado en sus términos de servicio. El proyecto optó por una alternativa legítima: navegación manual por el usuario, con el texto copiado estructurado luego mediante código. Es una distinción real entre un proceso automatizado de peticiones y una persona transcribiendo lo que ve en pantalla.

**Validación cruzada de datos recolectados a mano.** Los totales de gasto del Barça, recolectados en dos rondas distintas desde vistas diferentes de Transfermarkt (balance por club y balance por competición), coincidieron de forma exacta, sirviendo como verificación de que la transcripción manual no introdujo errores.

**Verificación de resultados contra fuentes externas.** De forma sistemática, los resultados calculados (posiciones finales, récords de puntos, montos de fichajes históricos) se contrastaron con fuentes externas mediante búsqueda web. Esta práctica permitió detectar el error de la temporada 2006/07, un caso que una simple inspección del DataFrame no habría revelado por sí sola.

---

## Fase 2: uso de canteranos

### Parseo de tablas HTML con BeautifulSoup (segundo uso)

La lista de canteranos se extrajo de la tabla "Jugadores formados en La Masía" de Wikipedia, copiando el HTML crudo y parseándolo con `BeautifulSoup`, igual que en Fase 1, esta vez para una tabla con más columnas (nombre, año de nacimiento, rango de carrera, partidos, goles, primer y último club).

### Normalización de texto para cruces por nombre (`unidecode`)

El cruce inicial por `isin()` exacto entre dos fuentes (Wikipedia y Transfermarkt) falló para varios nombres por diferencias de tildes (`Araújo` vs `Araujo`). La solución fue normalizar ambas columnas con `unidecode` antes de comparar, quitando acentos y pasando a minúsculas:

```python
from unidecode import unidecode
df['nombre_normalizado'] = df['nombre'].apply(lambda x: unidecode(str(x)).lower())
```

Esto resuelve de una sola vez la clase completa de problemas de tildes, en vez de perseguir cada caso individualmente.

### Verificación exhaustiva de "no encontrados" antes de asumir errores

De 103 nombres cruzados, 63 no encontraron coincidencia directa contra las apariciones registradas. En vez de asumir que todos eran errores de formato de nombre, se filtraron primero por año de inicio de carrera (¿deberían aparecer, por fecha, dentro del rango de datos disponible?), reduciendo la revisión real a solo 6 casos. De esos, solo uno (Gavi, registrado con nombre completo en Wikipedia pero como apodo en Transfermarkt) era un problema real de formato. El resto resultaron ser jugadores que pasaron por la cantera pero nunca sumaron minutos de Liga con el primer equipo, cada uno verificado individualmente con búsqueda externa, incluyendo la corrección de una hipótesis propia equivocada (se asumió erróneamente que un jugador no era canterano real, cuando sí lo era, solo que debutó profesionalmente en otro club tras formarse en el Barça).

### Documentar límites de cobertura sin forzar una solución

`appearances.csv`/`games.csv` solo cubre La Liga desde 2012/13, muy por debajo del rango de 33 temporadas del resto del proyecto. En vez de aproximar el resto con una métrica de menor calidad (por ejemplo, contar presencia en plantilla en vez de minutos jugados, lo cual habría requerido además reconstruir fechas de salida de cada jugador con trabajo adicional considerable), se decidió acotar el análisis al rango con datos reales y documentar la limitación explícitamente. Se aplicó el mismo criterio en un caso más chico: la temporada 2020/21 mostró un número de apariciones notablemente menor al resto sin explicación de datos nulos, documentado como limitación de cobertura puntual en vez de ignorarla o forzar un ajuste que simulara datos inexistentes.

### Declarar definiciones ambiguas explícitamente

"Canterano" no tiene una definición única y objetiva en el fútbol. Se documentó explícitamente qué criterio usa este proyecto (el de la fuente de Wikipedia, que incluye el filial como parte de la formación) y se ilustró con un caso concreto del propio dataset (Ronald Araújo, que llegó directamente al filial como fichaje externo), para que cualquier lectura del porcentaje de uso de cantera se entienda bajo esa definición específica, no como un estándar universal.

### Separar hallazgos de reflexión personal

Al notar un patrón interesante pero no demostrable con los datos disponibles (la posible influencia de "las personas al mando" más allá del entrenador, extendible a directiva y presidencia), se documentó en una sección explícitamente separada y marcada como reflexión, no como conclusión del análisis, para no mezclar evidencia con especulación razonada. La misma lógica se aplicó al incluir un ranking de canteranos con más minutos como reconocimiento visual, dejando claro que no tiene pretensión analítica.

---

## Fase 3: valor de mercado de plantilla

### Agregación de datos sin cadencia fija (fecha de corte por temporada)

`player_valuations.csv` registra el valor de mercado de cada jugador en fechas irregulares (cuando Transfermarkt actualiza su estimación), no en una cadencia fija por temporada. En vez de buscar una fecha exacta de corte (que habría fallado en años con pocas valoraciones), se tomó la última valoración disponible de cada jugador dentro de cada temporada, usando julio como mes de corte entre una temporada y la siguiente, coherente con el calendario real del mercado de fichajes europeo:

```python
def fecha_a_temporada(fecha):
    if fecha.month >= 7:
        inicio = fecha.year
    else:
        inicio = fecha.year - 1
    return f'{str(inicio)[2:]}{str(inicio+1)[2:]}'
```

### Validar un total con una métrica secundaria, no reemplazarlo

Para descartar que el valor total de plantilla por temporada estuviera distorsionado simplemente por cuántos jugadores tenían valoración registrada ese año (entre 19 y 37 según la temporada), se calculó también el valor promedio por jugador como verificación cruzada, no como métrica alternativa de igual peso analítico: el total sigue siendo la medida correcta para "cuánto vale el activo completo", y el promedio solo confirma que un patrón visto en el total no es un artefacto de conteo.

### Corregir un diagnóstico propio equivocado con búsqueda externa

Al ejemplificar con casos reales de jugadores revalorizados sin coste de fichaje reciente, se verificó cada caso con búsqueda externa antes de nombrarlo en el análisis. Esto evitó afirmar datos de memoria que podían ser imprecisos (por ejemplo, confirmar la fecha y condición exacta del regreso de un jugador al club antes de citarlo como ejemplo).

### Depurar errores de estado en el kernel, no solo de código

Un error de `KeyError` en una columna que debería existir no siempre significa que el código esté mal escrito: puede significar que una celda anterior falló silenciosamente o nunca se ejecutó en el orden esperado, dejando una variable en un estado incompleto. La forma más robusta de resolverlo no es parchear la celda que falla, sino reconstruir la variable completa en una sola celda autocontenida, sin depender de que varias celdas previas se hayan ejecutado en un orden específico.

### Ajuste manual de etiquetas superpuestas en gráficos de dispersión

Cuando dos o más puntos de un scatter caen muy cerca entre sí, sus etiquetas de texto (`ax.annotate`) se superponen y quedan ilegibles. La solución aplicada fue un diccionario de desplazamientos manuales solo para los casos identificados visualmente como problemáticos, dejando el resto con un offset por defecto. Cuando el desplazamiento aleja demasiado la etiqueta de su punto, se agregó una flecha fina (`arrowprops`) conectando texto y punto, para no perder la trazabilidad visual de a qué dato corresponde cada etiqueta.

---

## Fase 4: presidentes y directiva

### Replicar una metodología ya validada, en vez de inventar una nueva

La tabla de presidentes se construyó con exactamente el mismo patrón que `entrenadores_detalle.csv` (tabla detallada por tramos + tabla agregada por temporada), reutilizando una estructura ya probada en vez de diseñar algo nuevo. Esto ahorró tiempo y redujo el riesgo de errores, porque el patrón ya había sido validado en Fase 1.

### No todo hallazgo cuantitativo resiste una lectura ingenua

El gasto promedio por presidente, tomado de forma aislada, sugería una lectura simplista ("más gasto, mejor o peor gestión" según el caso). Al señalar el usuario que Joan Laporta asumió la presidencia en ambas ocasiones tras crisis financieras heredadas de sus antecesores, se verificó esta afirmación con búsqueda externa (confirmando cifras concretas: 180M€ gastados por Gaspart en 2000-01, deuda de 1.350M€ heredada de Bartomeu en 2021) y se reescribió la conclusión completa. El hallazgo visual que sostiene esta corrección es contundente: Gaspart y Laporta tienen el mismo gasto promedio (7.5%) pero resultados opuestos, evidencia de que una métrica de gasto promedio, sin el contexto de la situación financiera heredada, puede llevar a una conclusión equivocada sobre la calidad de gestión de un presidente.

### Verificar afirmaciones de terceros antes de incorporarlas, no solo las propias

A lo largo del proyecto se verificaron tanto errores propios (la corrección de 2006/07 en Fase 1, la hipótesis equivocada sobre Onana en Fase 2) como correcciones sugeridas por el usuario (el matiz sobre el gasto de Laporta en esta fase). En ambos casos se aplicó el mismo estándar: ninguna afirmación, propia o ajena, se incorpora al análisis sin verificación externa cuando es posible verificarla.

---

## Consolidación final: comparando variables continuas y categóricas en la misma unidad

### El problema: Pearson no sirve para variables categóricas

Gasto, cantera y valor de plantilla son numéricas continuas, así que Pearson (r) las compara directamente. Entrenador y presidente son categóricos (nombres, no números). Para comparar los cinco en una sola tabla, se necesitaba una técnica que produjera un número en la misma escala interpretativa que r, aplicable a variables de grupo.

### ANOVA y eta cuadrado (η²)

Un ANOVA de un factor (`scipy.stats.f_oneway`) prueba si el promedio de una variable continua difiere significativamente entre los grupos de una variable categórica. De ahí se deriva **eta cuadrado (η²)**, que se interpreta igual que un R²: proporción de varianza total explicada por la pertenencia a un grupo.

```python
def eta_cuadrado(df, variable_categorica, variable_continua):
    grupos = [grupo[variable_continua].values for _, grupo in df.groupby(variable_categorica)]
    f_stat, p_valor = stats.f_oneway(*grupos)

    gran_media = df[variable_continua].mean()
    ss_total = ((df[variable_continua] - gran_media) ** 2).sum()
    ss_entre = sum(len(g) * (g.mean() - gran_media) ** 2 for g in grupos)
    eta2 = ss_entre / ss_total
    return eta2, p_valor
```

Para que la comparación entre las cinco variables fuera honesta, se usó **r² (no r)** para las tres continuas, ya que r² y η² representan la misma cantidad conceptual (proporción de varianza explicada), mientras que r y η² no son directamente comparables en magnitud.

### Corregir un sesgo real: grupos de tamaño 1 inflan η² artificialmente

Cuando un grupo (un entrenador con una sola temporada) tiene una única observación, su varianza interna es matemáticamente cero, así que toda su distancia respecto al promedio general se contabiliza como "explicada por la categoría", sin reflejar necesariamente un patrón real. Por eso, únicamente para este cálculo puntual, se filtraron los entrenadores con menos de 2 temporadas (mismo criterio de muestra mínima ya usado en el resto del proyecto para tablas y gráficos individuales, donde esos casos sí se muestran, con su nota de "no comparable"). El filtro afecta solo el cálculo de η², no ninguna otra parte del proyecto.

Presidente no necesitó este filtro: los 5 presidentes del rango tienen 2 o más temporadas cada uno.

### Distinguir tamaño del efecto (r²/η²) de confianza en el resultado (p)

Dos preguntas distintas, que conviene no confundir:
- **Varianza explicada (r² o η²):** de toda la variación del rendimiento entre temporadas, ¿qué proporción se puede atribuir a esta variable? Mide el **tamaño** del efecto.
- **Valor p:** ¿qué tan probable es que ese patrón observado sea producto del azar, si en la realidad no existiera ninguna relación? Mide la **confianza** en que el resultado no es casualidad.

Un valor de r²/η² pequeño (como el de gasto, 0.052) puede coexistir con "no significativo" (p alto): con pocas observaciones, un efecto chico fácilmente puede deberse al azar. Un valor grande (como el de entrenador, 0.727) típicamente produce un p muy bajo, porque un efecto de esa magnitud es mucho menos probable que ocurra por casualidad.

### Verificar una hipótesis alternativa antes de descartarla sin evidencia

Al notar que la correlación de cantera era débil, se planteó la hipótesis de que la variable simplemente variaba poco entre temporadas (poca "señal" estadística disponible). Se verificó calculando el coeficiente de variación (desviación estándar entre la media) de cantera y de valor de plantilla, la variable con la que se comparaba. El resultado descartó la hipótesis: ambas variables tienen variabilidad relativa similar (cantera incluso ligeramente mayor), así que la diferencia en la fuerza de la correlación no se explica por cuánto varía cada una, sino, más probablemente, porque el rendimiento depende más de la calidad específica de los jugadores de cantera en cancha que de la cantidad total de minutos acumulados. Documentar y descartar una hipótesis con evidencia es tan valioso como confirmar una, evita quedarse con la primera explicación intuitiva sin comprobarla.