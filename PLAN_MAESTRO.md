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
- [ ] **PRIMERO EN LA PRÓXIMA SESIÓN: aplicar el mismo formato de eje (`2020/21` en vez de `2020`) a los gráficos de `02_analisis_rendimiento.ipynb` que usan `anio_inicio` (rendimiento histórico, integrador, local vs visitante)**
- [x] Analizar relación entre uso de cantera y rendimiento (Pearson r=0.274, p=0.344, no significativa)
- [x] Analizar uso de cantera y títulos por entrenador (2+ temporadas), con visualización
- [x] Markdown de hallazgos finales de Fase 2 en el notebook
- [x] Reflexión personal documentada por separado (hipótesis sobre el peso de "las personas al mando", marcada explícitamente como no demostrada, con propuesta de Fase 4 en README)
- [ ] Actualizar README con el cierre de Fase 2
- [ ] Actualizar NOTAS_METODOLOGICAS.md con las técnicas de Fase 2 (BeautifulSoup aplicado, unidecode, validación de nombres, manejo de cobertura parcial)
- [ ] Commit de Fase 2

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

## PARTE 3.6 — Unificación final (antes de Tableau)

- [ ] Consolidar en un solo dataset (o conjunto mínimo de tablas relacionadas) todo lo construido: rendimiento, entrenador, gasto, proporción de mercado, uso de cantera, valor de plantilla, presidente
- [ ] Guardar ese dataset consolidado en `data/processed/`, listo para importar a Tableau sin transformaciones adicionales
- [ ] Escribir una narrativa consolidada de los hallazgos de las 4 fases en conjunto (documento o notebook de cierre), no solo cada fase por separado
- [ ] Revisar que README, PLAN_MAESTRO y NOTAS_METODOLOGICAS reflejen el proyecto completo de punta a punta
- [ ] Commit de cierre de la etapa de análisis completa

---

## PARTE 4 — Presentación final

### 4.1 Dashboard en Tableau Public
- [ ] Definir qué vistas/hojas va a tener el dashboard (basado en los hallazgos ya documentados)
- [ ] Preparar los CSVs finales que se van a importar a Tableau
- [ ] Construir las hojas en Tableau Desktop
- [ ] Armar el dashboard combinando las hojas
- [ ] Publicar en Tableau Public
- [ ] Confirmar que el link público funciona

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