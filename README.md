# Always Barça

Análisis histórico del FC Barcelona: qué relación existe entre el gasto neto en fichajes, el entrenador a cargo y el rendimiento deportivo del equipo, temporada a temporada, desde 1993/94 hasta hoy.

## Por qué este proyecto

Soy ingeniero en sistemas recién graduado, buscando trabajo como Data Analyst, y decidí construir mi portafolio con un tema que realmente me interesa en vez de un dataset genérico de Kaggle sin ninguna conexión personal. Soy aficionado del Barça, y llevaba tiempo con la curiosidad de responder algo con datos reales en vez de opinión de bar: ¿el dinero invertido en fichajes de verdad predice el éxito deportivo del equipo, o hay otros factores (como el entrenador) que pesan más?

## La pregunta que busco responder

¿Qué relación existe entre el gasto neto en fichajes, el entrenador a cargo, el uso de cantera, el valor de la plantilla y la presidencia del club, y el rendimiento deportivo del Barça por temporada? ¿El dinero predice el éxito mejor que quién toma las decisiones?

Decidí no limitar el análisis a una sola era (por ejemplo, solo la época Guardiola), porque eso reduce demasiado el número de temporadas y le quita fuerza estadística a cualquier patrón. En su lugar, trato al entrenador y al presidente como variables más dentro de todo el rango temporal, para poder ver tanto el patrón general como comparar entre eras.

## Alcance y consideraciones clave del análisis

Antes de entrar a los hallazgos, esto es lo que hay que tener presente para interpretarlos bien:

- **No todas las variables cubren las mismas 33 temporadas.** Rendimiento, gasto neto, entrenador y presidente están completos para 1993/94-2025/26. Uso de cantera y valor de mercado de plantilla solo cubren 2012/13-2025/26 (14 de 33 temporadas), porque los datos de apariciones y valoraciones de Transfermarkt no tienen cobertura confiable antes de esa fecha. No se aproximó el resto del rango con un proxy de menor calidad, se documentó la limitación y se acotó el análisis.
- **Tres temporadas tienen contexto atípico documentado explícitamente**, no tratado como dato normal: 2020/21 (pandemia, sin público en ningún partido), 2023/24 y 2024/25 (local en el Montjuïc por la remodelación del Camp Nou).
- **Una corrección manual sobre los datos crudos:** la tabla de posiciones de 2006/07 se reconstruyó con un criterio de puntos simplificado que da empate técnico entre Barça y Real Madrid, pero el título real se decidió por el criterio de desempate oficial (resultados entre ambos), que favoreció al Madrid. Se corrigió a mano para reflejar el resultado real.
- **"Canterano" no tiene una definición única en el fútbol.** Este proyecto usa un criterio amplio (cualquier jugador en la tabla de Wikipedia "Jugadores formados en La Masía", incluyendo quienes pasaron por el filial), no solo quienes llegaron desde las categorías más jóvenes. Con otro criterio, los números de uso de cantera podrían variar.
- **Correlación no es causalidad.** Esto aplica sobre todo a los hallazgos de Fase 4: que el gasto promedio de un presidente no se asocie con mejor rendimiento no significa que gastar menos sea buena gestión, hay contexto financiero heredado de por medio (ver hallazgos de esa fase más abajo).
- El razonamiento detallado detrás de cada una de estas decisiones está en [NOTAS_METODOLOGICAS.md](./NOTAS_METODOLOGICAS.md).

## Estado del proyecto

Las 4 fases de análisis están completas: rendimiento y gasto (Fase 1), uso de canteranos (Fase 2), valor de mercado de plantilla (Fase 3), y presidentes/directiva (Fase 4), unificadas en un dataset final y una comparación conjunta de todas las variables.

## Metodología: cómo se mide una "temporada buena"

Se definieron dos métricas complementarias: una escala continua (`rendimiento_relativo`, puntos obtenidos sobre el máximo posible esa temporada específica, normalizado para ser comparable entre eras con distintas reglas de puntos y calendarios) y una categórica basada en posición final, ajustada al contexto de un club de la escala del Barça, donde no clasificar a Champions League ya representa una temporada fallida: Título, Top 4, Mala (5°-8°), Catastrófico (9° en adelante, categoría que resultó vacía en todo el rango).

## Metodología: cómo se mide el gasto de forma comparable entre eras

El gasto neto absoluto no es comparable entre 1996 y 2020, el mercado de fichajes se ha inflado mucho más rápido que la economía general. En vez de usar un índice de precios genérico, se calculó `proporcion_mercado_barca`: el gasto neto del Barça como porcentaje del gasto total de todos los clubes de La Liga esa misma temporada. Este enfoque sigue el mismo principio metodológico que usa el CIES Football Observatory (centro de investigación del fútbol) para medir la inflación del mercado de fichajes: usar el propio volumen del mercado como referencia, no la inflación de la economía general. La misma lógica se aplicó al valor de mercado de la plantilla (Fase 3).

## Fuentes de datos por pieza

- **Rendimiento y gasto (2014/15-2025/26):** automatizado, vía football-data.co.uk y el dataset de Transfermarkt en Kaggle.
- **Gasto y gasto total de liga (1993/94-2013/14):** recolección manual desde Transfermarkt, validada cruzadamente contra dos vistas distintas del sitio, coincidiendo de forma exacta.
- **Entrenadores y presidentes:** tablas construidas a mano con fuentes públicas, incluyendo varios casos de cambio a mitad de temporada con fechas verificadas.
- **Canteranos:** lista de 103 jugadores formados en La Masía (tabla de Wikipedia), cruzada contra apariciones y minutos jugados de Transfermarkt (cobertura desde 2012/13).
- **Valor de mercado de plantilla:** Transfermarkt (cobertura confiable desde 2012/13).

## Fase 1: rendimiento, gasto y entrenador (1993/94-2025/26)

- El gasto no predice el rendimiento de forma estadísticamente significativa (r=0.227, p=0.204).
- El entrenador se asocia con más variación en el rendimiento que el gasto. Guardiola lidera el rendimiento promedio (0.818, 3 títulos en 4 temporadas).
- El ataque explica más varianza del rendimiento que la defensa (goles a favor r=0.787 vs goles en contra r=-0.660, ambos p<0.001).
- El Barça depende de jugar en casa en la mayoría de las temporadas, aunque la brecha se ha achicado con el tiempo. Tres temporadas (2020/21 por la pandemia, 2023/24 y 2024/25 por la remodelación del Camp Nou con sede en Montjuïc) tienen un contexto atípico documentado explícitamente.
- El gasto tiende a concentrarse al inicio de cada ciclo de entrenador, más como inversión de renovación que como predictor directo de éxito esa temporada. Las temporadas de Título se ganaron tanto con gasto prácticamente nulo (1997/98, 2025/26) como con inversión considerable.

## Fase 2: uso de canteranos (2012/13-2025/26)

- El uso de cantera tampoco predice el rendimiento de forma significativa (r=0.274, p=0.344).
- No hay relación simple entre uso de cantera y títulos: Koeman tuvo el segundo mayor uso de cantera del grupo sin ganar ningún título en sus 2 temporadas; Flick combinó el mayor uso con el mejor récord de títulos (2 de 2).
- En 2024/25 y 2025/26, el balance de fichajes cerró prácticamente en cero, y son las dos temporadas con mayor valor de plantilla del rango, generado por jugadores creados en casa sin coste de fichaje (Yamal, Gavi, Fermín López, Balde) y canteranos recuperados a bajo coste (Eric García, agente libre en 2021).

## Fase 3: valor de mercado de plantilla (2012/13-2025/26)

- A diferencia del gasto y la cantera, el **valor de mercado de la plantilla sí muestra una correlación fuerte y significativa con el rendimiento** (r=0.753, p=0.002), la relación más fuerte encontrada hasta esa fase. Valor de plantilla mide el activo acumulado (una variable de "stock"), mientras que gasto neto mide el movimiento de un solo verano (una variable de "flujo"), y el acumulado predice mejor.

## Fase 4: presidentes y directiva (1993/94-2025/26)

- **Corrección metodológica importante:** el gasto promedio por presidente no equivale a mejor o peor gestión. Joan Laporta asumió la presidencia dos veces en medio de crisis financieras heredadas de sus antecesores (180M€ gastados por Gaspart en 2000-01; deuda de 1.350M€ heredada de Bartomeu en 2021, que impidió renovar a Messi). Gaspart y Laporta tienen prácticamente el mismo gasto promedio (7.5%), pero resultados opuestos de rendimiento, evidencia de que el gasto promedio sin contexto puede llevar a conclusiones equivocadas.
- Sandro Rosell lidera rendimiento, gasto y valor de plantilla promedio, heredando una base ya sólida construida por el primer mandato de Laporta.

## Resumen consolidado: comparando las 5 variables en la misma unidad

Para comparar de forma justa variables numéricas (gasto, cantera, valor de plantilla) con variables categóricas (entrenador, presidente), se usó varianza explicada del rendimiento en todos los casos: r² para las continuas, η² (eta cuadrado, obtenido de un análisis de varianza) para las categóricas.

| Variable | Varianza explicada | Significativa (p<0.05) |
|---|---|---|
| Gasto neto (% del mercado) | 0.052 | No |
| Uso de cantera (% de minutos) | 0.075 | No |
| Valor de plantilla (% del mercado) | 0.567 | Sí |
| Presidente | 0.606 | Sí |
| Entrenador | 0.727 | Sí |

**El entrenador es la variable que más explica el rendimiento de todo el proyecto**, por encima incluso del valor acumulado de la plantilla. El presidente queda muy cerca en segundo lugar. Gasto y cantera, las dos variables de "cuánto se invierte", quedan muy por debajo de las tres restantes, todas relacionadas con "quién decide" o "qué talento ya se tiene acumulado".

Se descartó, con evidencia, la hipótesis de que la correlación débil de cantera se debiera simplemente a poca variación del dato entre temporadas: cantera y valor de plantilla tienen variabilidad relativa similar (coeficientes de variación de 0.162 y 0.132 respectivamente), así que la diferencia entre ambas no se explica por cuánto varían, sino probablemente porque el rendimiento depende más de la calidad específica de los jugadores de cantera que juegan que de solo cuántos minutos acumulan.

**Conclusión final del proyecto:** ni el gasto ni el uso de cantera predicen bien el rendimiento del Barça en 33 años de historia. El valor acumulado de la plantilla sí, y quién está al mando (entrenador, y en segundo lugar presidente) explica aún más. Esto es consistente con la hipótesis planteada como reflexión desde el cierre de Fase 2: la calidad de las decisiones de quienes están al mando parece pesar más que la disponibilidad de recursos. Confirmar esto con rigor causal requeriría datos comparables de otros clubes, fuera del alcance de este proyecto.

**Con esto se cierra el análisis completo del proyecto.**

## Dashboards en Tableau Public

- [Fase 1: Rendimiento, gasto y entrenador](https://public.tableau.com/views/AlwaysBara/Dashboard1?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- [Fase 2: Uso de canteranos](https://public.tableau.com/views/AlwaysBara/UsodecanteranosFase2?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- [Fase 3: Valor de plantilla](https://public.tableau.com/views/AlwaysBara/Fase3Valordeplantilla?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- [Fase 4: Presidentes y resumen final](https://public.tableau.com/views/AlwaysBara/Dashboard4?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## Stack

Python, pandas y Jupyter Notebook para limpieza y análisis. Matplotlib para exploración. BeautifulSoup para extracción de tablas HTML. SciPy para pruebas estadísticas (Pearson, ANOVA). Tableau Public para el dashboard final.

## Notas metodológicas

Para el razonamiento detallado detrás de cada decisión técnica y metodológica del proyecto, ver [NOTAS_METODOLOGICAS.md](./NOTAS_METODOLOGICAS.md).

## Estructura del repositorio

```
always-barca/
├── data/
│   ├── raw/            # Datos crudos (resultados de La Liga, Transfermarkt, canteranos, presidentes)
│   └── processed/      # Datos limpios, incluyendo dataset_final.csv (las 4 fases unidas)
├── notebooks/
│   ├── 01_exploracion_estructura.ipynb   # Construcción y limpieza de datos (Fase 1)
│   ├── 02_analisis_rendimiento.ipynb     # Análisis exploratorio (Fase 1)
│   ├── 03_analisis_cantera.ipynb         # Uso de canteranos (Fase 2)
│   ├── 04_valor_mercado.ipynb            # Valor de mercado de plantilla (Fase 3)
│   ├── 05_analisis_presidentes.ipynb     # Presidentes y directiva (Fase 4)
│   └── 06_dataset_final.ipynb            # Unificación y comparación final de las 5 variables
├── src/
│   └── descargar_temporadas.py           # Script de descarga automatizada
└── reports/
    └── figures/                          # Visualizaciones exportadas
```

## Nota personal

Este proyecto no nació de un dataset genérico elegido por conveniencia, nació de ser culé. Escribo esto en Alajuela, Costa Rica, a casi 8,970 kilómetros en línea recta de Barcelona, y esa distancia es justamente parte del punto: dentro de España, ser del Barça está muy ligado a Cataluña, con un peso identitario y político regional que no es comparable con simplemente preferir a un equipo sobre otro. Fuera de España, ese peso regional desaparece, y lo que queda es otra cosa. Estoy convencido, aunque esto no es algo que un dataset pueda demostrar, de que ningún otro club del mundo genera fuera de su país el nivel de pasión que genera el Barça en su afición extranjera, ni siquiera comparado con otros gigantes europeos con hinchada global.

Qué curioso, además, terminar este análisis justo en un momento donde la ilusión por el club vuelve a sentirse fuerte: una generación de La Masía otra vez cargando al equipo, con nombres que ya aparecen en los propios datos de este proyecto (Yamal, Cubarsí, Fermín López), y decisiones institucionales que, al menos por ahora, parecen ir en la dirección correcta. Si algo deja claro este proyecto, tanto en los números como en lo que no se puede medir, es que las épocas doradas del Barça siempre han combinado cantera propia con buenas decisiones de quienes están al mando. Ojalá esta sea una de esas épocas.