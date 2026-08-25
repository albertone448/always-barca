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