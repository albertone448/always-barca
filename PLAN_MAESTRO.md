# Plan maestro — always-barca

Documento de seguimiento secuencial. Se trabaja de arriba hacia abajo, un paso a la vez, marcando `[x]` conforme se completa. No saltar pasos: si algo no aplica o se decide dejar para después, se anota explícitamente en vez de simplemente omitirlo, para no perder el rastro entre conversaciones.

---

## PARTE 1 — Completar lo pendiente de Fase 1

### 1.1 Ataque vs defensa: ¿qué pesa más en el rendimiento? — COMPLETO
- [x] Calcular correlación de Pearson: `goles_favor` vs `rendimiento_relativo` (r=0.787, p<0.001)
- [x] Calcular correlación de Pearson: `goles_contra` vs `rendimiento_relativo` (r=-0.660, p<0.001)
- [x] Comparar la fuerza de ambas correlaciones (ataque pesa más que defensa en el dataset completo)
- [x] Visualización: scatter comparando ambas relaciones lado a lado
- [x] Revisar si el patrón cambia por era/entrenador (inestable por muestra chica, documentado con cautela)
- [x] Markdown de hallazgo en el notebook
- [x] Actualizar README con el hallazgo

### 1.2 Rendimiento local vs visitante por temporada — COMPLETO
- [x] Cargar `partidos_barca_completo.csv` en el notebook de trabajo
- [x] Agregar por temporada y condición (local/visitante): puntos por partido, goles a favor/contra
- [x] Calcular brecha local-visitante y revisar top temporadas de fortaleza de visitante
- [x] Visualización: líneas de local/visitante en el tiempo + marcas de temporadas de Título
- [x] Identificar y documentar temporadas con contexto atípico (más de la mitad del calendario afectado): 2020/21 (pandemia, sin público toda la temporada), 2023/24 y 2024/25 (local en Montjuïc por remodelación del Camp Nou)
- [x] Markdown de hallazgo en el notebook
- [x] Actualizar README con el hallazgo

### 1.3 Cierre de Fase 1 — COMPLETO
- [x] Confirmar que no queda ningún punto del planteamiento original de Fase 1 sin abordar
- [x] Markdown de cierre del notebook 02 actualizado con los 4 análisis (gasto, entrenador, ataque/defensa, local/visitante)
- [ ] Commit final de Fase 1 (ya con 1.1 y 1.2 incluidos)

---

## PARTE 2 — Fase 2: Uso de canteranos

- [x] Recolectar lista de canteranos históricos (tabla "Jugadores formados en La Masía" de Wikipedia, 103 nombres, parseada con BeautifulSoup)
- [x] Explorar `appearances.csv` y `games.csv` de Transfermarkt (estructura, columnas, cobertura por temporada)
- [x] Detectar y documentar limitación de cobertura: appearances/games solo cubre La Liga desde 2012/13 (14 de 33 temporadas). Decisión tomada: acotar el análisis cuantitativo a ese rango, sin proxy de menor calidad para el resto.
- [x] Definir estrategia de cruce de nombres entre fuentes (normalización con `unidecode` para tildes)
- [x] Ejecutar el cruce y validar contra la realidad (casos resueltos: Gavi con nombre corto, Araújo/tildes, Onana/Grimaldo/Cucurella/Miranda/Gabarrón sin minutos de Liga en el rango, corrección de error propio en la tabla de Wikipedia)
- [x] Validación adicional: top 20 canteranos con más minutos, contrastado contra jugadores conocidos
- [x] Documentar nota metodológica sobre la definición ambigua de "canterano" (criterio amplio usado, incluye filial)
- [ ] Resolver fecha de salida de cada canterano en `barca_promociones_cantera.csv` (hoy solo tiene fecha de entrada) — pendiente, no bloqueante para el análisis actual
- [x] Definir la métrica de "uso de cantera" por temporada (% de minutos jugados en Liga)
- [x] Calcular la métrica para las 14 temporadas con cobertura de datos (2012/13-2025/26)
- [x] Detectar y documentar limitación adicional: cobertura reducida de apariciones en 2020/21 (menos registros que el resto, sin explicación de valores nulos)
- [x] Visualización: uso de cantera por temporada, con estrellas de Título y formato de temporada `2020/21`
- [x] Aplicar el mismo formato de eje (`2020/21` en vez de `2020`) a los gráficos de `02_analisis_rendimiento.ipynb` (commit `dc4f5d4`, checkbox desactualizado, ya resuelto en su momento)
- [x] Analizar relación entre uso de cantera y rendimiento (Pearson r=0.274, p=0.344, no significativa)
- [x] Analizar uso de cantera y títulos por entrenador (2+ temporadas), con visualización
- [x] Markdown de hallazgos finales de Fase 2 en el notebook
- [x] Reflexión personal documentada por separado (hipótesis sobre el peso de "las personas al mando", marcada explícitamente como no demostrada, con propuesta de Fase 4 en README)
- [x] Actualizar README con el cierre de Fase 2 (commit `72ace49`, checkbox desactualizado, ya resuelto en su momento)
- [x] Actualizar NOTAS_METODOLOGICAS.md con las técnicas de Fase 2 (commit `72ace49`, checkbox desactualizado, ya resuelto en su momento)
- [x] Commit de Fase 2 (`72ace49`, checkbox desactualizado, ya resuelto en su momento)
- [x] Exportar `top_canteranos_minutos.csv` a `data/processed/`, pendiente desde el notebook 03 (la tabla nunca se había persistido, solo existía como Series de pandas usada para el gráfico de Matplotlib), necesario para conectarlo como fuente de datos nueva en la Hoja 3 del Dashboard 2 de Tableau

---

## PARTE 3 — Fase 3: Valor de mercado de plantilla — COMPLETA

- [x] Decidir hacer la fase (confirmado)
- [x] Explorar `player_valuations.csv` (estructura, columnas, cobertura por temporada)
- [x] Verificar ID de club correcto (`current_club_id`, 131 confirmado, consistente con transfers/appearances)
- [x] Definir método de agregación (última valoración por jugador dentro de cada temporada, corte en julio)
- [x] Detectar y documentar limitación de cobertura: número de jugadores contados por temporada muy bajo antes de 2012/13 (8, 6, 8 jugadores). Decisión: acotar a 2012/13-2025/26 (13 temporadas)
- [x] Calcular valor total de plantilla y valor promedio por jugador (como verificación cruzada de confiabilidad, no como métrica alternativa de igual peso)
- [x] Calcular `valor_relativo_plantilla` (% del mercado total de La Liga), mismo principio metodológico que `proporcion_mercado_barca`
- [x] Correlación con rendimiento: r=0.753, p=0.002 — la única variable de recursos del proyecto con relación estadísticamente significativa
- [x] Visualización: valor de plantilla vs rendimiento, con estrellas de Título
- [x] Cruce adicional: valor de plantilla vs gasto reciente, para distinguir valor generado internamente (cantera, revalorización) de valor comprado
- [x] Visualización de ese cruce, con estrellas de Título y ajuste manual de etiquetas superpuestas (offsets + flechas)
- [x] Ejemplificar con casos reales verificados (Yamal, Gavi, Fermín López, Balde como cantera pura; Eric García como canterano recuperado gratis, verificado con búsqueda externa)
- [x] Markdown de conclusión combinada (rendimiento + gasto reciente) en el notebook
- [ ] Actualizar README con el cierre de Fase 3
- [ ] Commit de Fase 3

---

## PARTE 3.5 — Fase 4: Presidentes / directiva — COMPLETA

- [x] Recolectar tabla de presidentes del FC Barcelona por periodo (Wikipedia + fuentes oficiales, fechas verificadas)
- [x] Construir tabla detallada por tramos (`presidentes_detalle.csv`, 38 filas), incluyendo 2 casos de múltiples cambios a mitad de temporada (2002/03: Gaspart → Reyna → Comisión Gestora; 2020/21: Bartomeu → Tusquets → Laporta)
- [x] Derivar tabla agregada `presidentes_temporada.csv` (33 filas) para el merge
- [x] Unir con `df_maestro` por temporada (persistido de vuelta en `df_maestro.csv`)
- [x] Calcular rendimiento promedio por presidente (los 5 presidentes del rango tienen 2+ temporadas, ninguno cae en "caso aislado")
- [x] Calcular gasto y valor de plantilla promedio por presidente
- [x] 3 visualizaciones: gasto por presidente, rendimiento vs gasto lado a lado, valor de plantilla por presidente
- [x] Corrección metodológica importante detectada por el usuario: el gasto promedio no equivale a mejor/peor gestión sin considerar el contexto financiero heredado (Laporta asumió dos veces en medio de crisis heredadas de Gaspart y Bartomeu, verificado con fuentes externas: deuda de 180M€ gastados por Gaspart en 2000-01, deuda de 1.350M€ heredada de Bartomeu en 2021)
- [x] Markdown de hallazgos con esta corrección incorporada
- [ ] Actualizar README con el cierre de Fase 4
- [ ] Commit de Fase 4

---

## PARTE 3.6 — Unificación final (antes de Tableau) — COMPLETA

- [x] Consolidar en un solo dataset (`dataset_final.csv`, 33 temporadas) todo lo construido: rendimiento, entrenador, gasto, proporción de mercado, uso de cantera, valor de plantilla, presidente
- [x] Guardar ese dataset consolidado en `data/processed/`, listo para importar a Tableau sin transformaciones adicionales
- [x] Extender la comparación a las 5 variables (no solo 3): usar r² para gasto/cantera/valor de plantilla y η² (ANOVA) para entrenador/presidente, en la misma unidad de "varianza explicada"
- [x] Corregir sesgo de grupos de tamaño 1 en el cálculo de η² (filtrar entrenadores con 1 sola temporada, solo para este cálculo puntual)
- [x] Resultado final: entrenador (η²=0.727) y presidente (η²=0.606) explican más varianza del rendimiento que valor de plantilla (r²=0.567), muy por encima de cantera (r²=0.075) y gasto (r²=0.052)
- [x] Verificar y descartar con evidencia la hipótesis de que la correlación débil de cantera se debiera a poca variabilidad del dato (coeficientes de variación similares entre cantera y valor de plantilla)
- [x] Visualización resumen final: comparación de las 5 variables en una sola escala
- [x] Escribir una narrativa consolidada de los hallazgos de las 4 fases en conjunto (notebook `06_dataset_final.ipynb`)
- [x] Revisar que README, PLAN_MAESTRO y NOTAS_METODOLOGICAS reflejen el proyecto completo de punta a punta
- [x] Commit de cierre de la etapa de análisis completa

---

## PARTE 4 — Presentación final

### 4.1 Dashboard en Tableau Public

**Herramienta:** Tableau Public vía creación web (no hay versión de escritorio para Linux/Ubuntu). Se guarda únicamente publicando (no hay "guardar borrador" privado).

**Fuente de datos:** `dataset_final.csv`, conectado una sola vez, `Temporada` corregida a tipo texto para no perder el cero inicial, y un campo calculado `Temporada Formato` (`STR([Anio Inicio]) + "/" + RIGHT(STR([Anio Inicio] + 1), 2)`) para mostrar `1993/94` en vez de `1993` en todos los ejes.

**Estructura: 4 dashboards temáticos (no 16 hojas sueltas), uno por fase, navegables por pestaña.** Prioriza narrativa sobre volcar todo lo hecho en Matplotlib.

#### Dashboard 1 — Rendimiento, gasto y entrenador (Fase 1) — COMPLETO Y PUBLICADO
- [x] Hoja 1: Gráfico integrador (barras de gasto + línea de rendimiento coloreada por entrenador)
- [x] Hoja 2: Rendimiento por entrenador (barras horizontales, distinción 2+/1 temporada, campo calculado `Grupo Muestra Entrenador` con LOD fijo)
- [x] Hoja 3: Rendimiento histórico simple (línea, 33 temporadas)
- [x] Campo calculado `Años de Temporada` para formato `1993/94` en todos los ejes
- [x] Ensamblar dashboard 1 (1 grande arriba + 2 lado a lado abajo, leyendas reubicadas debajo)
- [x] Título del dashboard puesto
- [x] Publicado en Tableau Public

#### Dashboard 2 — Cantera (Fase 2) — COMPLETO Y PUBLICADO
- [x] Hoja 1: Uso de cantera por temporada (línea con estrellas de título), filtrada a 2012/13-2025/26 con filtro de contexto sobre `Anio Inicio`, marcador de título vía campo calculado `Cantera en Titulo` combinado en eje doble
- [x] Hoja 2: Uso de cantera y títulos por entrenador, con campo calculado propio `Grupo Muestra Entrenador Cantera` (2+ temporadas dentro de la ventana de cantera, distinto del campo equivalente del Dashboard 1 que usa las 33 temporadas completas) y `Titulos Entrenador Cantera` como etiqueta
- [x] Hoja 3: Top canteranos con más minutos (mención honorífica), en fuente de datos nueva (`top_canteranos_minutos.csv`, exportada desde el notebook 03, no existía como archivo hasta esta sesión), filtro Top 15 por `minutos_jugados`
- [x] Ensamblar dashboard 2 (1 grande arriba + 2 lado a lado abajo, mismo patrón que Dashboard 1)
- [x] Publicado en Tableau Public

#### Dashboard 3 — Valor de plantilla (Fase 3, el hallazgo más fuerte)
- [ ] Hoja 1: Valor de plantilla vs rendimiento (scatter con estrellas, r=0.753) — la pieza central del proyecto
- [ ] Hoja 2: Valor vs gasto reciente (evidencia Yamal/Gavi/Eric García)
- [ ] Ensamblar dashboard 3

#### Dashboard 4 — Presidentes y resumen final (Fase 4 + unificación)
- [ ] Hoja 1: Rendimiento vs gasto por presidente (lado a lado, Gaspart vs Laporta)
- [ ] Hoja 2: Comparación final de las 5 variables (r²/η²) — cierre del proyecto
- [ ] Ensamblar dashboard 4

**Visualizaciones del notebook que quedan fuera de Tableau a propósito** (viven solo en los notebooks, como evidencia analítica de respaldo, no en la presentación): proporción de mercado vs rendimiento (scatter), boxplot de gasto por categoría, categorías por entrenador (apiladas), ataque vs defensa, local vs visitante, rendimiento histórico con estrellas (Fase 1 extendida). Redundantes con lo que ya cuentan las hojas seleccionadas.

- [ ] Publicar los 4 dashboards en Tableau Public
- [ ] Confirmar que los links públicos funcionan
- [ ] Agregar los links al README

### 4.2 Sitio de portafolio (React + Vercel)
- [ ] Confirmar si ya existe el sitio base o hay que crearlo desde cero
- [ ] Sección de proyectos: agregar always-barca
- [ ] Embeber el dashboard de Tableau Public vía iframe
- [ ] Desplegar en Vercel
- [ ] Confirmar que el link público funciona

---

## PARTE 5 — Deuda técnica / sueltos

- [x] Confirmar si se regeneró el token de Kaggle que quedó expuesto en pantalla hace varias sesiones — confirmado, regenerado
- [ ] Última pasada de revisión general del README, una vez cerradas todas las fases

---

## Referencia: dónde vive cada cosa (notebooks)

| Pieza | Notebook / lugar |
|---|---|
| Construcción y limpieza de datos crudos (Fase 1) | `01_exploracion_estructura.ipynb` |
| Análisis exploratorio de rendimiento/gasto/entrenador | `02_analisis_rendimiento.ipynb` |
| Ataque vs defensa (1.1) | Extensión de `02_analisis_rendimiento.ipynb` |
| Local vs visitante (1.2) | Extensión de `02_analisis_rendimiento.ipynb` |
| Fase 2 (canteranos) | `03_analisis_cantera.ipynb` (nuevo) |
| Fase 3 (valor de mercado) | `04_valor_mercado.ipynb` (nuevo, si se hace) |
| Tableau | Fuera del repo de notebooks, en Tableau Public |
| Sitio de portafolio | Repositorio separado (React/Vercel) |

---

## Ya completado (referencia, no se vuelve a tocar salvo error)

- [x] Rendimiento deportivo por temporada (33 temporadas, 1993/94-2025/26)
- [x] Reconstrucción de tabla de posiciones desde resultados crudos, validada contra hechos reales
- [x] Entrenador principal por temporada + tabla detallada de tramos (6 cambios a mitad de temporada)
- [x] Gasto neto en fichajes (33 temporadas: 12 automatizadas + 21 manuales, validadas cruzadamente)
- [x] `proporcion_mercado_barca`: métrica de gasto ajustada por inflación del mercado
- [x] `rendimiento_relativo` y `categoria_temporada` (Título/Top 4/Mala/Catastrófico)
- [x] `df_maestro.csv`: unión de rendimiento, entrenador y gasto
- [x] Correlación gasto-rendimiento (Pearson) y comparación por entrenador
- [x] 7 visualizaciones exploratorias de Fase 1