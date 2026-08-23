## Estado actual del proyecto

La Fase 1 está completa: rendimiento deportivo, entrenador y gasto neto en fichajes, unidos en un solo dataset por temporada (1993/94-2025/26). Sobre esa base, ya se hizo un primer análisis exploratorio con hallazgos concretos.

### Metodología: cómo se mide una "temporada buena"

Se definieron dos métricas complementarias: una escala continua (`rendimiento_relativo`, puntos obtenidos sobre el máximo posible esa temporada específica, normalizado para ser comparable entre eras con distintas reglas de puntos y calendarios) y una categórica basada en posición final, ajustada al contexto de un club de la escala del Barça, donde no clasificar a Champions League ya representa una temporada fallida: Título, Top 4, Mala (5°-8°), Catastrófico (9° en adelante, categoría que resultó vacía en todo el rango).

### Hallazgos del análisis exploratorio

- **El gasto neto en fichajes no predice el rendimiento de forma significativa.** Correlación de Pearson de 0.207 (débil) con un valor p de 0.520, muy por encima del umbral de significancia estadística, sobre las 12 temporadas con datos de gasto confiables (2014/15-2025/26).
- **El entrenador se asocia con más variación en el rendimiento que el gasto.** Guardiola lidera el rendimiento promedio (0.818, 3 títulos en 4 temporadas), seguido de cerca por Luis Enrique y Hansi Flick. Van Gaal, pese a dirigir 4 temporadas en dos etapas distintas, tiene el promedio más bajo del grupo con muestra representativa.
- **Tres eras bien diferenciadas en el rendimiento histórico:** inestabilidad en el banquillo (1994-2003, valle mínimo bajo Rexach), la era dorada de Guardiola-Vilanova (2008-2013, pico absoluto en la temporada del récord de 100 puntos), y recuperación reciente tras la crisis institucional de la etapa Koeman.

**Limitación honesta:** con solo 12 temporadas de gasto disponible y varios entrenadores representados por 1-2 temporadas, estos son hallazgos descriptivos sólidos, no pruebas causales. Se documentan como tal en el notebook correspondiente.

### Lo que sigue pendiente

- Extender el gasto neto hacia atrás (1993/94-2013/14) vía investigación manual, para robustecer el análisis de correlación
- Uso de canteranos por temporada (Fase 2), con `barca_promociones_cantera.csv` ya generado como insumo
- Valor de mercado de la plantilla (Fase 3, opcional)
- Dashboard final en Tableau Public