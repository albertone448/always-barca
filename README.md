## Estado actual del proyecto

La Fase 1 está completa: rendimiento deportivo, entrenador y gasto neto en fichajes, unidos en un solo dataset de 33 temporadas (1993/94-2025/26). Sobre esa base, ya se hizo un análisis exploratorio completo con hallazgos concretos.

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
- **Tres eras bien diferenciadas en el rendimiento histórico:** inestabilidad en el banquillo (1994-2003, valle mínimo bajo Rexach), la era dorada de Guardiola-Vilanova (2008-2013, pico absoluto en la temporada del récord de 100 puntos), y recuperación reciente tras la crisis institucional de la etapa Koeman.
- **2003/04 y 2004/05 muestran la mayor proporción de mercado del rango** (~25% del gasto total de La Liga), coincidiendo con la reconstrucción del equipo tras la crisis de Van Gaal/Antić, con los fichajes de Ronaldinho y Deco.

**Limitación honesta:** son hallazgos descriptivos sólidos, respaldados por validación cruzada y contraste con hechos históricos reales, pero no pruebas causales. Se documentan como tal en los notebooks correspondientes.

### Lo que sigue pendiente

- Uso de canteranos por temporada (Fase 2), con `barca_promociones_cantera.csv` ya generado como insumo (46 ascensos de cantera identificados)
- Valor de mercado de la plantilla (Fase 3, opcional)
- Dashboard final en Tableau Public