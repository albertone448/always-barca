# always-barca

Análisis histórico del FC Barcelona: qué relación existe entre el gasto neto en fichajes, el entrenador a cargo y el rendimiento deportivo del equipo, temporada a temporada, desde 1993/94 hasta hoy.

## Por qué este proyecto

Soy ingeniero en sistemas recién graduado, buscando trabajo como Data Analyst, y decidí construir mi portafolio con un tema que realmente me interesa en vez de un dataset genérico de Kaggle sin ninguna conexión personal. Soy aficionado del Barça, y llevaba tiempo con la curiosidad de responder algo con datos reales en vez de opinión de bar: ¿el dinero invertido en fichajes de verdad predice el éxito deportivo del equipo, o hay otros factores (como el entrenador) que pesan más?

## La pregunta que busco responder

¿Qué relación existe entre el gasto neto en fichajes (compras menos ventas), el entrenador a cargo, y el rendimiento deportivo del Barça por temporada? ¿El gasto predice el éxito mejor que otros factores?

Decidí no limitar el análisis a una sola era (por ejemplo, solo la época Guardiola), porque eso reduce demasiado el número de temporadas y le quita fuerza estadística a cualquier patrón. En su lugar, trato al entrenador como una variable más dentro de todo el rango temporal, para poder ver tanto el patrón general como comparar entre eras.

## Estado actual del proyecto

Las Fases 1 y 2 están completas: rendimiento deportivo, entrenador, gasto neto en fichajes y uso de canteranos, todo unido y analizado sobre el rango 1993/94-2025/26 (con la limitación de cobertura de canteranos acotada a 2012/13-2025/26).

### Metodología: cómo se mide una "temporada buena"

Se definieron dos métricas complementarias: una escala continua (`rendimiento_relativo`, puntos obtenidos sobre el máximo posible esa temporada específica, normalizado para ser comparable entre eras con distintas reglas de puntos y calendarios) y una categórica basada en posición final, ajustada al contexto de un club de la escala del Barça, donde no clasificar a Champions League ya representa una temporada fallida: Título, Top 4, Mala (5°-8°), Catastrófico (9° en adelante, categoría que resultó vacía en todo el rango).

### Metodología: cómo se mide el gasto de forma comparable entre eras

El gasto neto absoluto no es comparable entre 1996 y 2020, el mercado de fichajes se ha inflado mucho más rápido que la economía general. En vez de usar un índice de precios genérico, se calculó `proporcion_mercado_barca`: el gasto neto del Barça como porcentaje del gasto total de todos los clubes de La Liga esa misma temporada. Este enfoque sigue el mismo principio metodológico que usa el CIES Football Observatory (centro de investigación del fútbol afiliado a la Universidad de Neuchâtel) para medir la inflación del mercado de fichajes: usar el propio volumen del mercado como referencia, no la inflación de la economía general.

### Fuentes de datos por pieza

- **Rendimiento y gasto (2014/15-2025/26):** automatizado, vía football-data.co.uk y el dataset de Transfermarkt en Kaggle.
- **Gasto y gasto total de liga (1993/94-2013/14):** recolección manual desde Transfermarkt, validada cruzadamente contra dos vistas distintas del sitio (balance por club y balance por competición), coincidiendo de forma exacta.
- **Entrenadores:** tabla construida a mano con fuentes públicas, incluyendo 6 casos de cambio de entrenador a mitad de temporada con fechas verificadas.
- **Canteranos:** lista de 103 jugadores formados en La Masía (tabla de Wikipedia), cruzada contra apariciones y minutos jugados de Transfermarkt (cobertura desde 2012/13).

## Fase 1: rendimiento, gasto y entrenador (1993/94-2025/26)

### Hallazgos del análisis exploratorio

- **El gasto no predice el rendimiento de forma estadísticamente significativa.** Correlación de Pearson de 0.227 entre `proporcion_mercado_barca` y `rendimiento_relativo`, con un valor p de 0.204, sobre las 33 temporadas completas.
- **El entrenador se asocia con más variación en el rendimiento que el gasto.** Guardiola lidera el rendimiento promedio (0.818, 3 títulos en 4 temporadas), seguido de cerca por Luis Enrique y Hansi Flick. Van Gaal, pese a dirigir 4 temporadas, tiene el promedio más bajo del grupo con muestra representativa, y su temporada de mayor gasto relativo del rango completo produjo el peor rendimiento de todos los datos.
- **El ataque explica más varianza del rendimiento que la defensa.** Ambas correlaciones son altamente significativas (p<0.001), pero de distinta magnitud: goles a favor (r=0.787) pesa más que goles en contra (r=-0.660), coherente con la identidad ofensiva del club en la mayoría de las eras analizadas.
- **El Barça depende de jugar en casa en la mayoría de las temporadas, aunque la brecha se ha achicado con el tiempo.** Tres temporadas tienen un contexto atípico que altera el significado habitual de "local": 2020/21 (pandemia, toda la temporada sin público en ningún estadio de la liga), y 2023/24-2024/25 (el club jugó como local en el Estadio Olímpico de Montjuïc durante la remodelación del Camp Nou). Ninguna temporada de Título se concentra en los extremos de mayor o menor dependencia del local.
- **Tres eras bien diferenciadas en el rendimiento histórico:** inestabilidad en el banquillo (1994-2003, valle mínimo bajo Rexach), la era dorada de Guardiola-Vilanova (2008-2013, pico absoluto en la temporada del récord de 100 puntos), y recuperación reciente tras la crisis institucional de la etapa Koeman.
- **2003/04 y 2004/05 muestran la mayor proporción de mercado del rango** (~25% del gasto total de La Liga), coincidiendo con la reconstrucción del equipo tras la crisis de Van Gaal/Antić, con los fichajes de Ronaldinho y Deco.

### Análisis integrador: rendimiento, gasto y entrenador en el tiempo

Se construyó una visualización que combina las tres variables centrales en un solo gráfico (rendimiento como línea, gasto como barras, entrenador como fondo por tramos, estrellas marcando temporadas de Título), revelando un patrón que los gráficos individuales no mostraban: **el gasto tiende a concentrarse al inicio de cada ciclo de entrenador**, más como una inversión de renovación que como predictor directo de rendimiento esa misma temporada. Las temporadas de Título, además, se reparten en un rango de gasto muy amplio, sin ningún piso mínimo visible: se ganó la liga tanto con gasto prácticamente nulo (1997/98, 2025/26) como con inversión considerable (era Rijkaard-Guardiola).

**Limitación honesta:** son hallazgos descriptivos sólidos, respaldados por validación cruzada y contraste con hechos históricos reales, pero no pruebas causales.

## Fase 2: uso de canteranos por temporada (2012/13-2025/26)

**Limitación de cobertura:** los datos de partido a partido de Transfermarkt solo cubren La Liga desde 2012/13, así que este análisis se acota a 14 de las 33 temporadas del proyecto. No se aproximó el resto del rango con un proxy de menor calidad (como conteo de plantilla en vez de minutos).

**Hallazgos:**
- El uso de cantera tampoco predice el rendimiento de forma estadísticamente significativa (r=0.274, p=0.344), un patrón similar al del gasto neto en Fase 1.
- No hay una relación simple entre uso de cantera y títulos: Ronald Koeman tuvo el segundo mayor uso de cantera del grupo analizado (45.7%) sin ganar ningún título en sus 2 temporadas, mientras que Hansi Flick combinó el mayor uso de cantera (48.5%) con el mejor récord de títulos (2 de 2).
- El caso de Xavi Hernández (menor uso de cantera del grupo, 36%) se explica casi enteramente por la temporada 2023/24, la de menor uso de cantera de todo el rango, coincidiendo con la crisis financiera del club ya documentada en Fase 1.

**Reflexión (no un hallazgo demostrado):** el patrón repetido a lo largo del proyecto, donde ni gasto ni cantera predicen bien el rendimiento pero el entrenador sí muestra diferencias consistentes, sugiere una hipótesis: que la calidad de las decisiones de quienes están al mando pesa más que la disponibilidad de recursos, dado que el Barça cuenta de forma prácticamente constante con cantera de calidad y capacidad de fichaje. Esto no se puede confirmar con datos de un solo club, y queda como posible extensión futura (ver Fase 4 más abajo).

**Entregable adicional (sin pretensión analítica):** un top 15 de los canteranos con más minutos jugados en el rango, como reconocimiento visual al linaje de La Masía, desde Busquets y Messi hasta la generación actual (Yamal, Cubarsí, Fermín López).

## Fase 3: valor de mercado de plantilla (2012/13-2025/26)

**Limitación de cobertura:** el número de jugadores del Barça con valoración registrada por temporada es muy bajo antes de 2012/13 (8, 6 y 8 jugadores en las primeras temporadas del dataset, muy por debajo de una plantilla real), así que este análisis se acota a las 13 temporadas con cobertura confiable.

**Hallazgo principal:** a diferencia del gasto neto y del uso de cantera, el **valor de mercado de la plantilla sí muestra una correlación fuerte y estadísticamente significativa con el rendimiento** (r=0.753, p=0.002), la relación más fuerte encontrada en todo el proyecto. La explicación conceptual: gasto neto mide el movimiento de un solo verano (una variable de flujo), mientras que valor de plantilla mide el activo acumulado completo en un momento dado (una variable de stock), y ese acumulado se traduce mejor en resultados que la inversión puntual de una temporada. Aun así, valor alto no garantiza el título: hay temporadas sin título con valores de plantilla similares o superiores a otras que sí lo ganaron, señal de que la fortaleza del rival también pesa.

**De dónde viene ese valor:** en 2024/25 y 2025/26, el balance de fichajes del Barça cerró prácticamente en cero, y sin embargo son las dos temporadas con mayor valor de plantilla de todo el rango. Ese valor no vino de inversión reciente, vino de jugadores creados en casa sin coste de fichaje (Lamine Yamal, Gavi, Fermín López, Alejandro Balde, formados en La Masía) y de canteranos que salieron y regresaron a bajo coste, revalorizándose después (Eric García, que volvió como agente libre en 2021 tras salir del club en 2017).

**Con esto se cierra la Fase 3 del proyecto.**

## Fase 4: presidentes y directiva

Continuación de la reflexión documentada al cierre de Fase 2: ¿la presidencia del club se asocia con la misma variación en el rendimiento que ya se vio con el entrenador?

**Corrección metodológica importante:** el gasto promedio por presidente no debe leerse como "más gasto es mejor gestión". Joan Laporta llegó a la presidencia dos veces en medio de crisis financieras heredadas de sus antecesores: en 2003, tras Joan Gaspart, quien había gastado 180 millones de euros en dos mercados y dejó al club en tal estado que tuvo que regalar a Rivaldo al Milan solo para no pagar su sueldo. En 2021, tras Josep Maria Bartomeu, quien dejó una deuda de 1.350 millones de euros, tan grave que el club no pudo ni renovar a Messi. La evidencia lo confirma: Gaspart y Laporta tienen prácticamente el mismo gasto promedio (7.5% del mercado), pero quedan en extremos opuestos de rendimiento (Gaspart el peor de los cinco presidentes del rango, Laporta el de más títulos en total), señal de que el gasto promedio por sí solo no cuenta la historia sin el contexto de qué estado encontró cada uno al asumir.

**Hallazgos:** Sandro Rosell lidera rendimiento (0.820), gasto (11.3%) y valor de plantilla (18.0%) promedio, heredando y continuando la era Guardiola sobre una base ya sólida. Joan Gaspart tiene el peor rendimiento (0.535, 0 títulos), la crisis institucional más profunda del rango.

**Limitación central:** con datos de un solo club, no se puede aislar el efecto de las decisiones de la presidencia de otros factores compartidos por toda una era. La hipótesis planteada en la reflexión de Fase 2 (que el factor humano en el mando pesa más que los recursos disponibles) sigue sin poder confirmarse ni descartarse con rigor estadístico, pero el patrón de Laporta limpiando dos crisis heredadas con gasto similar al de quien las generó es un matiz real que la enriquece.

**Con esto se cierra la Fase 4 del proyecto.**

## Próximos pasos

- Unificación final de las 4 fases en un dataset y narrativa consolidados.
- Dashboard final en Tableau Public.
- Sitio de portafolio en React, desplegado en Vercel.

## Stack

Python, pandas y Jupyter Notebook para limpieza y análisis. Matplotlib para exploración. BeautifulSoup para extracción de tablas HTML. Tableau Public para el dashboard final.

## Notas metodológicas

Para el razonamiento detallado detrás de cada decisión técnica y metodológica del proyecto, ver [NOTAS_METODOLOGICAS.md](./NOTAS_METODOLOGICAS.md).

## Estructura del repositorio

```
always-barca/
├── data/
│   ├── raw/            # Datos crudos (resultados de La Liga, Transfermarkt, canteranos)
│   └── processed/      # Datos limpios y listos para análisis
├── notebooks/
│   ├── 01_exploracion_estructura.ipynb   # Construcción y limpieza de datos (Fase 1)
│   ├── 02_analisis_rendimiento.ipynb     # Análisis exploratorio (Fase 1)
│   └── 03_analisis_cantera.ipynb         # Uso de canteranos (Fase 2)
├── src/
│   └── descargar_temporadas.py           # Script de descarga automatizada
└── reports/
    └── figures/                          # Visualizaciones exportadas
```