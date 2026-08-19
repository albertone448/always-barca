# always-barca

Análisis histórico del FC Barcelona: qué relación existe entre el gasto neto en fichajes, el entrenador a cargo y el rendimiento deportivo del equipo, temporada a temporada, desde 1993/94 hasta hoy.

## Por qué este proyecto

Soy ingeniero en sistemas recién graduado, buscando trabajo como Data Analyst, y decidí construir mi portafolio con un tema que realmente me interesa en vez de un dataset genérico de Kaggle sin ninguna conexión personal. Soy aficionado del Barça, y llevaba tiempo con la curiosidad de responder algo con datos reales en vez de opinión de bar: ¿el dinero invertido en fichajes de verdad predice el éxito deportivo del equipo, o hay otros factores (como el entrenador) que pesan más?

## La pregunta que busco responder

¿Qué relación existe entre el gasto neto en fichajes (compras menos ventas), el entrenador a cargo, y el rendimiento deportivo del Barça por temporada? ¿El gasto predice el éxito mejor que otros factores?

Decidí no limitar el análisis a una sola era (por ejemplo, solo la época Guardiola), porque eso reduce demasiado el número de temporadas y le quita fuerza estadística a cualquier patrón. En su lugar, trato al entrenador como una variable más dentro de todo el rango temporal, para poder ver tanto el patrón general como comparar entre eras.

## Estado actual del proyecto

Este proyecto está en construcción activa. Por ahora está resuelta la parte de **rendimiento deportivo por temporada**: reconstruí la tabla de posiciones completa de La Liga para cada una de las 33 temporadas (1993/94 a 2025/26) directamente desde resultados partido a partido, y con eso tengo, temporada por temporada, la posición final del Barça, puntos, victorias, empates, derrotas y diferencia de gol.

Lo que sigue pendiente:
- Tabla de entrenadores por temporada
- Gasto neto en fichajes (cruzando datos de Transfermarkt)
- Unir las tres piezas y analizar la relación entre ellas
- Uso de canteranos por temporada (Fase 2)
- Valor de mercado de la plantilla (Fase 3, si el tiempo alcanza)
- Dashboard final en Tableau Public

Voy a ir actualizando este README con hallazgos reales a medida que avance, no solo al final.

## Algunos hallazgos hasta ahora

- Las estadísticas de juego (tiros, córners, tarjetas) solo están disponibles en los datos desde la temporada 2005/06 en adelante. Antes de eso, solo hay goles y resultado, lo cual definió que mi métrica principal de rendimiento se basara en puntos, posición y diferencia de gol, que sí cubren todo el rango.
- Las temporadas 1995/96 y 1996/97 se jugaron con 22 equipos en vez de 20 (la llamada "liga de los 22"), un formato transitorio antes de volver a 20 equipos en 1997/98.
- La regla de puntos por victoria cambió de 2 a 3 a partir de la temporada 1995/96. Los puntos en este proyecto respetan la regla vigente en cada temporada, no están normalizados, para ser fieles a la clasificación real de cada año.
- Validé el pipeline de reconstrucción de tabla contra hechos históricos reales: por ejemplo, la temporada 2009/10 del Barça (récord de 99 puntos bajo Guardiola, 31 victorias, 6 empates, 1 derrota) sale exacta en los datos procesados.

## Fuentes de datos

- **Resultados de partidos**: [datahub.io / football-data.co.uk](https://datahub.io/football/spanish-la-liga), licencia Open Data Commons Public Domain Dedication.
- **Fichajes y apariciones**: dataset "Football Data from Transfermarkt" en Kaggle (pendiente de integrar).
- **Entrenadores por temporada**: tabla propia, construida a mano con fuentes públicas (pendiente).

## Stack

Python, pandas y Jupyter Notebook para limpieza y análisis. Matplotlib para exploración. Tableau Public para el dashboard final.
