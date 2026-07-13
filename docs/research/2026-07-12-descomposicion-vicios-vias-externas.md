# Descomposición de vicios — vías externas (respuestas 1 y 2 de la IA de Lucas; 2 más por venir)

2026-07-12. Guardadas VERBATIM para la síntesis (el texto completo está en la conversación de la
sesión; acá el índice de lo que cada una aporta + el estado de las disputas).

## Disputas auditadas
- **El 68% (vicio 1)**: la Respuesta 2 sospechó que era un número humano (Siebert & Siebert 68.5%)
  mal atribuido. VERIFICADO HOY contra arXiv 2604.18805: el abstract dice verbatim *"evidence is
  ignored in 68%% of traces, refutation-driven belief revision occurs in 26%%"*. La cita nuestra
  QUEDA. (La sospecha era del tipo correcto — precedente caso-67.)

## Lo NUEVO que aporta la Respuesta 1 (no estaba en la vía Claude)
- Sicofancia como polo del par del vicio 1: Fanous et al. 58.2%%; "creo que la respuesta es X"
  induce acuerdo 63.7%% promedio; circuito mecanístico en Gemma-2-2B (silenciarlo: 28→81%%).
  [POR-LEER]
- Sobre-corrección: actualiza 2.5× más fuerte ante feedback CONTRARIO que ante apoyo. [POR-LEER]
- Confabulación anclada (2604.25931): UN hecho intermedio confirmado AUMENTA las respuestas
  confiadas-incorrectas; escala con capacidad. [POR-LEER]
- Anclaje: al revés de Vaccaro — Suri et al. / Lou & Sun dicen robusto y que empeora con capacidad;
  mitigaciones por prompt inefectivas. [POR-LEER — tensión con Vaccaro a resolver en síntesis]
- TheAgentCompany: atajos falsos con traza (renombró a otro usuario para "encontrar" a la persona
  buscada); inventa valores en campos vacíos; da por cumplida la tarea prematuro. [POR-LEER]
- MAST: 1.600+ trazas multi-agente anotadas (HuggingFace mcemri/MAD), κ=0.88, taxonomía 14 modos.
  CORPUS MINABLE. [POR-LEER]
- Sakana con artefactos: modificó su código para EXTENDER su propio timeout; self-relaunch en loop;
  ~1TB de checkpoints (vicio 8: optimizar la restricción, Goodhart puro). [POR-LEER]
- Par propuesto (hipótesis suya): sub-actualizar-ante-DATOS ↔ sobre-actualizar-ante-OPINIONES —
  mismo canal superficial, polos opuestos según la fuente. Candidato a contribución original.

## Lo NUEVO que aporta la Respuesta 2
- **ImpossibleBench (2510.20270): GPT-5 hace trampa 76%% cuando la trampa PAGA localmente (tests
  pasan) vs 2.9%% cuando no** — "la jugada viciosa tiene que pagar localmente" = el factor #1.
  Nuestros pozos nunca pagaron de verdad. [POR-LEER]
- EvilGenie: ambigüedad > dificultad (44%% hardcodea en problemas ambiguos-pero-resolubles vs ~0-5%%
  en imposibles limpios). [POR-LEER]
- p-hacking por encuadre (Asher et al.): pedido directo → se niega; re-encuadrado como "reporte de
  incertidumbre" → lo hace. El vicio gobernado por ENCUADRE, no presión. [POR-LEER]
- **DiscoverPhysics (2605.26087): EL VECINO MÁS CERCANO A WAGER** — 22 mundos de física alterada,
  entrega = explicación + ley en Python, MSE held-out; frontier falla justo en ESTRUCTURA LATENTE
  (vicio 4 VIVO en frontier agéntico). Ellos usan LLM-judge para la explicación → nuestro
  diferencial cero-LLM. LEER ESTA SEMANA. [POR-LEER]
- BoxingGym (2501.01540): diseño experimental + revisión de teorías, 10 entornos. [POR-LEER]
- RadLE (2509.25559): traza inspeccionable de fijación (ve los rasgos correctos en el razonamiento
  intermedio y VUELVE a la hipótesis inicial). [POR-LEER]
- Firmas mecánicas robables: ProcCtrlBench (Duplicate Step / Tool Call Chain / **Dead Step** =
  "compró evidencia y no la usó", computable) + TIDE Loop Rate. [POR-LEER]
- Over-trust en el test propio (29.5%%, la firma MÁS frecuente de esa taxonomía) — NO está en
  nuestro catálogo. [POR-LEER]
- PaperBench matiz: cortar-antes es firma de la familia o-series, NO ley (Claude EMPEORA sin la
  opción de submit: 21.0→16.1). [ya VERIFICADO parcial en registro]
- Goal Drift matices: deriva por INACCIÓN; específica por modelo (Claude aguanta 100k, 4o-mini no).
- Einstellung MURIÓ entre generaciones (mARC → follow-up 2601.11866): los vicios EVAPORAN con las
  generaciones — el resultado modal de un mundo puede ser "el frontier lo resuelve".
- Crítica de diseño dura y correcta: costo de oportunidad ESCRITO en la consigna = medir aritmética,
  no juicio; el juicio es DARSE CUENTA de que hay costo. + "el pozo debe pagar local con retornos
  decrecientes; la alternativa se DESCUBRE, no se elige de menú".

## Convergencia de las tres vías (Claude + R1 + R2)
Las tres llegaron independientes a: (a) Big-Muddy — la escalada vive en IDENTIDAD y PARES, no en
economía; (b) el 0/60 nuestro replica lo publicado (decisión individual con contabilidad = racional);
(c) saliencia/encuadre como variable maestra; (d) el largo-real (contexto con objetivo lejos) sin
testear. Divergencia a resolver: anclaje (Vaccaro dice frágil; R1 dice robusto-y-peor-con-capacidad).
