# always-barca

Análisis histórico del FC Barcelona: qué relación existe entre el gasto neto en fichajes, el entrenador a cargo y el rendimiento deportivo del equipo, temporada a temporada, desde 1993/94 hasta hoy.

## Por qué este proyecto

Soy ingeniero en sistemas recién graduado, buscando trabajo como Data Analyst, y decidí construir mi portafolio con un tema que realmente me interesa en vez de un dataset genérico de Kaggle sin ninguna conexión personal. Soy aficionado del Barça, y llevaba tiempo con la curiosidad de responder algo con datos reales en vez de opinión de bar: ¿el dinero invertido en fichajes de verdad predice el éxito deportivo del equipo, o hay otros factores (como el entrenador) que pesan más?

## La pregunta que busco responder

¿Qué relación existe entre el gasto neto en fichajes (compras menos ventas), el entrenador a cargo, y el rendimiento deportivo del Barça por temporada? ¿El gasto predice el éxito mejor que otros factores?

Decidí no limitar el análisis a una sola era (por ejemplo, solo la época Guardiola), porque eso reduce demasiado el número de temporadas y le quita fuerza estadística a cualquier patrón. En su lugar, trato al entrenador como una variable más dentro de todo el rango temporal, para poder ver tanto el patrón general como comparar entre eras.

## Estado actual del proyecto

La Fase 1 está completa: rendimiento deportivo, entrenador y gasto neto en fichajes, unidos en un solo dataset de 33 temporadas (1993/94-2025/26), con un análisis exploratorio completo que además de la pregunta central (gasto vs entrenador) cubre ataque vs defensa y rendimiento local vs visitante.

### Metodología: cómo se mide una "temporada buena"

Se definieron dos métricas complementarias: una escala continua (`rendimiento_relativo`, puntos obtenidos sobre el máximo posible esa temporada específica, normalizado para ser comparable entre eras con distintas reglas de puntos y calendarios) y una categórica basada en posición final, ajustada al contexto de un club de la escala del Barça, donde no clasificar a Champions League ya representa una temporada fallida: Título, Top 4, Mala (5°-8°), Catastrófico (9° en adelante, categoría que resultó vacía en todo el rango).

### Metodología: cómo se mide el gasto de forma comparable entre eras

El gasto neto absoluto no es comparable entre 1996 y 2020, el mercado de fichajes se ha inflado mucho más rápido que la economía general. En vez de usar un índice de precios genérico, se calculó `proporcion_mercado_barca`: el gasto neto del Barça como porcentaje del gasto total de todos los clubes de La Liga esa misma temporada. Este enfoque sigue el mismo principio metodológico que usa el CIES Football Observatory (centro de investigación del fútbol afiliado a la Universidad de Neuchâtel) para medir la inflación del mercado de fichajes: usar el propio volumen del mercado como referencia, no la inflación de la economía general.

### Fuentes de datos por pieza

- **Rendimiento y gasto (2014/15-2025/26):** automatizado, vía football-data.co.uk y el dataset de Transfermarkt en Kaggle.
- **Gasto y gasto total de liga (1993/94-2013/14):** recolección manual desde Transfermarkt, validada cruzadamente contra dos vistas distintas del sitio (balance por club y balance por competición), coincidiendo de forma exacta.
- **Entrenadores:** tabla construida a mano con fuentes públicas, incluyendo 6 casos de cambio de entrenador a mitad de temporada con fechas verificadas.

### Hallazgos del análisis exploratorio

- **El gasto no predice el rendimiento de forma estadísticamente significativa.** Correlación de Pearson de 0.227 entre `proporcion_mercado_barca` y `rendimiento_relativo`, con un valor p de 0.204, sobre las 33 temporadas completas.
- **El entrenador se asocia con más variación en el rendimiento que el gasto.** Guardiola lidera el rendimiento promedio (0.818, 3 títulos en 4 temporadas), seguido de cerca por Luis Enrique y Hansi Flick. Van Gaal, pese a dirigir 4 temporadas, tiene el promedio más bajo del grupo con muestra representativa, y su temporada de mayor gasto relativo del rango completo produjo el peor rendimiento de todos los datos.
- **El ataque explica más varianza del rendimiento que la defensa.** Ambas correlaciones son altamente significativas (p<0.001), pero de distinta magnitud: goles a favor (r=0.787) pesa más que goles en contra (r=-0.660), coherente con la identidad ofensiva del club en la mayoría de las eras analizadas.
- **El Barça depende de jugar en casa en la mayoría de las temporadas, aunque la brecha se ha achicado con el tiempo.** Tres temporadas tienen un contexto atípico que altera el significado habitual de "local": 2020/21 (pandemia, toda la temporada sin público en ningún estadio de la liga), y 2023/24-2024/25 (el club jugó como local en el Estadio Olímpico de Montjuïc durante la remodelación del Camp Nou, sin la ventaja histórica ni el aforo del Camp Nou). Ninguna temporada de Título se concentra en los extremos de mayor o menor dependencia del local.
- **Tres eras bien diferenciadas en el rendimiento histórico:** inestabilidad en el banquillo (1994-2003, valle mínimo bajo Rexach), la era dorada de Guardiola-Vilanova (2008-2013, pico absoluto en la temporada del récord de 100 puntos), y recuperación reciente tras la crisis institucional de la etapa Koeman.
- **2003/04 y 2004/05 muestran la mayor proporción de mercado del rango** (~25% del gasto total de La Liga), coincidiendo con la reconstrucción del equipo tras la crisis de Van Gaal/Antić, con los fichajes de Ronaldinho y Deco.

### Análisis integrador: rendimiento, gasto y entrenador en el tiempo

Se construyó una visualización que combina las tres variables centrales en un solo gráfico (rendimiento como línea, gasto como barras, entrenador como fondo por tramos, estrellas marcando temporadas de Título), revelando un patrón que los gráficos individuales no mostraban: **el gasto tiende a concentrarse al inicio de cada ciclo de entrenador**, más como una inversión de renovación que como predictor directo de rendimiento esa misma temporada. La temporada de mayor gasto relativo de todo el rango (2003/04, inicio de Rijkaard) antecede a la recuperación del club, mientras que hacia el final de ese mismo ciclo (2006/07-2007/08) el gasto se sostiene pero el rendimiento cae, ilustrando el desgaste natural de una etapa. Las temporadas de Título, además, se reparten en un rango de gasto muy amplio, sin ningún piso mínimo visible: se ganó la liga tanto con gasto prácticamente nulo (1997/98, 2025/26) como con inversión considerable (era Rijkaard-Guardiola).

**Limitación honesta:** son hallazgos descriptivos sólidos, respaldados por validación cruzada y contraste con hechos históricos reales, pero no pruebas causales. Se documentan como tal en los notebooks correspondientes.

**Con esto, la Fase 1 del proyecto queda formalmente cerrada.**

## Lo que sigue pendiente

- Uso de canteranos por temporada (Fase 2), con `barca_promociones_cantera.csv` ya generado como insumo (46 ascensos de cantera identificados)
- Valor de mercado de la plantilla (Fase 3, opcional)
- Dashboard final en Tableau Public
- Sitio de portafolio en React, desplegado en Vercel

## Stack

Python, pandas y Jupyter Notebook para limpieza y análisis. Matplotlib para exploración. Tableau Public para el dashboard final.

## Estructura del repositorio

```
always-barca/
├── data/
│   ├── raw/            # Datos crudos (resultados de La Liga, Transfermarkt)
│   └── processed/      # Datos limpios y listos para análisis
├── notebooks/
│   ├── 01_exploracion_estructura.ipynb   # Construcción y limpieza de datos (Fase 1)
│   └── 02_analisis_rendimiento.ipynb     # Análisis exploratorio (Fase 1)
├── src/
│   └── descargar_temporadas.py           # Script de descarga automatizada
└── reports/
    └── figures/                          # Visualizaciones exportadas
```