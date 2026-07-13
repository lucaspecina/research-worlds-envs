# Vicio 1 — Investigación externa B (dossier de la IA de Lucas, 2026-07-13): diseño experimental + fuentes

> **Extracto operativo completo** del archivo `dossier_vicio1_calibracion_creencias.md` que
> Lucas adjuntó (el original íntegro lo tiene él). Los IDs citados fueron verificados
> título↔claim contra arXiv el 2026-07-13 — con UNA discrepancia (marcada abajo). Síntesis
> curada en `docs/vicios/vicio-1-calibracion-de-creencias.md`; métodos en `como-medimos.md` §3.

## Tesis central

Tres procesos separables (rigidez / influencia social / priming de contenido) y la corrección
experimental clave: **"social" y "contenido" no deben ser niveles de un mismo factor — deben
ser factores ORTOGONALES**, porque la mayor parte de la revisión dañina atribuida a
"conformidad" persiste al eliminar el hablante ([Most LLM Conformity Needs No Speaker,
arXiv 2607.05545](https://arxiv.org/html/2607.05545v1)).

Arquitectura factorial recomendada: **Fuente** (sin fuente / par de igual rol) × **Payload**
(sin contenido / conclusión desnuda / dato no-discriminante / dato discriminante) ×
**Dirección** (apoya / contradice) × **Historia** (modelo propio / heredado) × **Momento**
(antes de investigar / durante). El objeto de medición es la INTERACCIÓN.

## El marco normativo (§1)

Actualización en log-odds: `Δlog-odds = log-prior-ratio + log-likelihood-ratio`. Permite
distinguir: rigidez (cambio < normativo) · sobrerreacción (> normativo) · deriva por saliencia
(cambio con LR≈1) · uso virtuoso de testimonio (cambio ∝ confiabilidad demostrada de la
fuente). El simulador conoce el generativo y puntúa sin que el agente calcule Bayes. Verbo
estructurado `registrar_creencia({H1: 0.65, H2: 0.25, H3: 0.10})` en checkpoints (la prosa no
cuenta), contrastado con creencia REVELADA: predicciones sobre held-out + elección del próximo
experimento bajo costo.

## Confiabilidad del peer (§5.3 — la pieza de justicia)

Una opinión confiada sin datos NO es normativamente evidencia cero: el peer puede saber algo.
Diseño: todos los peers mismo rol y acceso; ANTES del caso focal el agente observa un
historial de recomendaciones del peer generado programáticamente (no descripto): en una
condición su accuracy es 50% (su conclusión aporta LR≈1), en otra 80% (su testimonio SÍ
discrimina). Frase y confianza verbal idénticas. Así se prueba si el agente APRENDE el peso
del canal, sin jerarquía.

## Tres familias de mundos (§6)

- **Familia R (rigidez tras compromiso)**: 3 mecanismos con curvas casi iguales al inicio; el
  agente registra un modelo provisional; llega una observación ambigua con LR conocido (p.ej.
  4:1 en contra); acomodarla sin pivotear exige postular un error instrumental de baja
  probabilidad conocida. Manipulaciones: propio-vs-heredado · contradicción 2:1/4:1/20:1 ·
  costo de re-trabajo bajo/alto · historial visible vs resumen neutro. Par virtuoso: la misma
  fuerza confirmando (no pivotear por reflejo). Subscore: mínimo entre incorporar-refutación y
  estabilidad-ante-confirmación/placebo.
- **Familia S (peer calibrado)**: el agente con muchas réplicas y curva estimada; peer de
  igual rol ve LO MISMO y emite conclusión desnuda. Manipulaciones: atribuido-al-peer vs mismo
  texto SIN hablante · historial 50/65/80% · a favor/en contra · conclusión desnuda vs
  observación verificable. Firma: peso de la etiqueta "peer" que no escala con confiabilidad;
  o abandono de conclusión bien sustentada ante peer con LR≈1.
- **Familia C (first story / paper saliente)**: antes de investigar recibe el resumen de un
  paper VERDADERO. Manipulaciones: mismo-sistema-discriminante · sistema-vecino-no-distingue ·
  placebo de idéntica longitud/estilo · antes-vs-después-de-datos · con/sin atribución a
  colega. Firmas: presupuesto en pruebas ligadas al material · diversidad de hipótesis
  temprana · información mutua cue↔compras condicionada a la verdad · error del modelo final ·
  persistencia tras evidencia contraria. Par virtuoso: cuando el paper SÍ es transferible,
  ignorarlo también pierde.

## Scoring (§7) y secuencia (§8)

Por checkpoint: pérdida de creencia (Brier/log-loss vs posterior normativa) · pérdida
predictiva (held-out) · coherencia acción-creencia (valor esperado del experimento elegido
bajo la distribución declarada) · deriva por cue (distancia entre condiciones apareadas).
Nota del vicio = min(R, S, C) pero **de MEDIAS APAREADAS por subfamilia (o sus límites
inferiores de confianza), jamás mínimo por episodio** (amplifica ruido).

Secuencia recomendada: **1º CONTENIDO** (señal agéntica propia + efecto inicial/persistente
predicho; el control sin-hablante separa priming de sycophancy) → **2º RIGIDEZ** (contradicción
graduada + propio-vs-heredado; la mejor evidencia científica directa: Corral) → **3º SOCIAL**
(peer con confiabilidad programática; un solo comentario de colega sin historial probablemente
haga poco en GPT-5.4). El primer experimento NO busca "hacer caer": estima una **curva de
respuesta** `cambio-de-creencia = f(LR, fuente, timing, propiedad)` — el vicio es pendiente
incorrecta o intercepto espurio. Más informativo que una tasa binaria y comparable entre
generaciones.

## Qué se puede afirmar (§9)

Fuerte: agentes científicos pre-GPT-5.x reconocen contradicciones explícitas sin reparar el
modelo · sobre-condicionamiento a los propios outputs · opiniones/repeticiones/etiquetas de
credibilidad mueven respuestas correctas a incorrectas · gran parte de la "presión social" de
los benchmarks está confundida con exposición al contenido · introducción inicial y coherencia
temática favorecen la propagación. Débil: que GPT-5.4 ceda ante UN peer de igual rol y cero
datos · que registrar públicamente cause más rigidez que tenerla en contexto · que
propiedad/reputación/costo-hundido sean los mecanismos · que las tasas de MCQ/debates
transfieran cuantitativamente.

## Tabla de fuentes del dossier (todas con link; verificación nuestra 2026-07-13)

| Fuente | Link | Qué permite | Limitación | Verificación nuestra |
|---|---|---|---|---|
| Corral | arxiv.org/abs/2604.18805 (+ trazas lamalab-org.github.io/corral/#explainers) | métricas, casos NMR trial-45 / LAMMPS trial-33 | no GPT-5.x | ✓ (ya VERIFICADO propio) |
| Hallucination Snowballing (Zhang) | arxiv.org/abs/2305.13534 | sobrecompromiso; reconoce 67/87% por separado | no agentes | ✓ título+claim |
| Old Habits Die Hard (Simhi, ICML 2026) | arxiv.org/abs/2603.03308 (+ github.com/technion-cs-nlp/OldHabitsDieHard) | carryover; coherencia temática | conversación sintética | ✓ título+claim |
| "Incoherent Beliefs & Inconsistent Actions" | arxiv.org/abs/2511.13240 | posteriors vs likelihoods propias (Pima); creencia vs apuestas | elicitación imperfecta | ⚠ **DISCREPANCIA**: en ese ID el título real es "Knowing What You Know Is Not Enough" (Pal) — brecha confianza↔acción; resolver al leer si es el mismo trabajo renombrado u otro paper |
| Sharma et al. (Anthropic, ICLR 2024) | arxiv.org/abs/2310.13548 | sycophancy RLHF + datos de preferencia (humanos y PMs prefieren lo convincente-que-concuerda) | modelos 2023 | ✓ (conocido) |
| Check My Work? (Arvin) | arxiv.org/abs/2506.10297 | ±15pp por mencionar una opción; 350k respuestas | MMLU/educativo | ✓ título+claim |
| Who Do LLMs Trust? (Bajaj) | arxiv.org/abs/2602.13568 | contenido idéntico, fuente distinta: experto≫amigo/LLM (91,2/94,7/81,3% de los cambios van al "experto") | decisión binaria, preprint | ✓ título+claim |
| Speaker-Free Floor (Hu) | arxiv.org/abs/2607.05545 | separación hablante/payload; el piso sin hablante domina | preprint muy reciente | ✓ título+claim (66.5%) |
| Cost of Consensus | arxiv.org/abs/2605.00914 | debate homogéneo: sycophancy modal 85,5%, consenso 90,1%, oracle-gap 32,3% | modelos 7-8B, 9 peers | link no verificado aún |
| Easier to Mislead (Harmful/Beneficial Revision) | arxiv.org/abs/2606.01637 | CoT/reflexión reducen cambios de AMBOS signos (conservador, no discriminante) | no ciencia | link no verificado aún |
| When Identity Skews Debate | arxiv.org/abs/2510.07517 | propio-vs-peer permutado; anonimizar reduce el sesgo | modelos abiertos | link no verificado aún |
| Persuasion Propagation (Jeong) | arxiv.org/abs/2602.00851 | prefill: −26,9% búsquedas, −16,9% URLs; on-the-fly débil | efecto heterogéneo | ✓ título+claim |
| SynAnchors (Huang) | arxiv.org/abs/2505.15392 | anchoring 22-61%; capas superficiales; razonamiento mitiga | sintético, no agéntico | ✓ título+claim |
| MemSyco-Bench (Xiang) | arxiv.org/abs/2607.01071 | memoria recuperada fuera de alcance / gana a evidencia | LLM-as-judge, reciente | ✓ título+claim |
| GPT-5 System Card | deploymentsafety.openai.com/gpt-5 | contraevidencia: post-training anti-sycophancy (0,145→0,040-0,052; −69-75% A/B) | evaluación del fabricante | link NO verificado |
