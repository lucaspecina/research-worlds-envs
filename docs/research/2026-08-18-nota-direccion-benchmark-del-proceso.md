# NOTA DE DIRECCIÓN (ideas en discusión — NADA decidido) — "El benchmark del proceso de investigación"

> Conversaciones Lucas↔Claude 2026-08-16/18, tras leer Model Discovery Agent (Murphy,
> 2608.09696) y shadow evaluations (2607.27191). Se persiste para no perderla en compactación
> de memoria. **Estado: ideas; ningún doc constitucional cambiado; espera discusión/OK.**

## De dónde sale y qué se descartó

Murphy construye el descubridor (LLM solo propone; SMC/SBI/VoI hacen el resto) — la contracara
de WAGER (medimos el agente desnudo). Primera idea de Claude: "escalera de andamios" como
producto (correr agentes con andamios procedimentales graduales que espejan los módulos de
Murphy y medir dónde se recuperan). **Lucas la frenó con razón**: como producto es un benchmark
de harness — espacio saturado, y Lucas tiene otro proyecto propio ahí (harness-refinement).
Queda degradada a sonda diagnóstica ocasional (seeds quemadas), jamás titular.

## La síntesis de Lucas (la formulación buena)

**El producto es el benchmark/la evaluación del PROCESO de investigación.** Con ese instrumento
fijo, el harness pasa a ser UNA columna más de la matriz experimental:

> proceso evaluado (fijo, el producto) × {modelo × harness × mundo × condición × entrenamiento}

"¿Qué harness produce qué cambios en el proceso?" queda admitida como APLICACIÓN del
instrumento — foco en todo, no solo en harnesses. Relación con harness-refinement: cliente
natural, no competencia.

## Qué significaría "evaluar el proceso" (bocetos)

- Rúbrica en dos capas: eslabones GENERALES (grieta → generación → puesta en juego → contraste
  → selección → realización → propagación; = Protocolo v1) instanciados POR CASO.
- Lecturas MECÁNICAS por eslabón (varias ya existen): información esperada de cada compra ·
  auditoría "la señal estaba en SUS filas" (¿podía saberlo?) · posterior del servidor ·
  flag estructural · archivo de `working_model` por celda · regret vs política óptima de
  compra. Anotación con reglas congeladas solo para texto; JAMÁS en el reward.
- El gemelo como control de falso positivo POR ESLABÓN.
- Solo posible porque los mundos son programas (auditoría "podía saberlo" partida por partida
  — imposible sobre tareas reales).

## Guardarraíles

La celda primaria de toda matriz = **el agente desnudo y espontáneo** (lo que nadie mide; lo
que conecta con E2: la fila "después de entrenar"; test Rayleigh). Sin leaderboard de harnesses
como identidad.

## Qué se resignifica sin tirar nada

Re-anotación de las 10 trazas = piloto del producto · anfitrión de partículas = primer mundo
diseñado a propósito (secuencial) · Protocolo v1 = rúbrica v1. Préstamos de Murphy que valen
solos: examen intervencional (adoptado) · titular el "umbral de reestructuración" como número
por modelo (¿a qué desajuste visible reestructura solo? Rayleigh 0.5%, Priestley ∞) ·
corroboración de su ablación.

## Validación externa del reencuadre (shadow evals)

Sus 5 failure modes son observaciones DE PROCESO hechas a mano por expertos (caro, n=2, no
repetible, no entrenable); los revisores-IA disponibles no son confiables según ellos mismos.
El hueco exacto = la evaluación mecánica del proceso. Detalle en
[por qué emergen allá y no acá](2026-08-18-por-que-emergen-alla-y-no-aca.md) y en
lectura-de-fuentes.
