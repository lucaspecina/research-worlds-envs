# Lectura completa — "When Should Models Change Their Minds? Contextual Belief Management in Large Language Models" (arXiv 2605.30219)

Autores: Haoming Xu, Weihong Xu, Zongrui Li, Mengru Wang, Yunzhi Yao, Chiyu Wu, Jin Shang, Yu Gong, Shumin Deng.

Fuente leída: `arxiv.org/html/2605.30219` (HTML completo vía ar5iv/arxiv-html), no solo abstract — extracción con secciones, ecuaciones y tablas citadas abajo.

## Qué es

- **Tarea**: los modelos mantienen un "belief state" S^t sobre un espacio finito de creencias ℬℰ a lo largo de una interacción multi-turno. En cada turno t reciben evidencia formal e_t y opcionalmente ruido n_t, y deben devolver el subconjunto de hipótesis candidatas alineado con la evidencia acumulada. Dos entornos: **Rule Discovery** (adivinar una regla oculta a partir de triples numéricos, p. ej. [3,8,1]) y **Circuit Diagnosis** (diagnosticar fallas de un circuito a partir de lecturas de instrumentos).
- **Turnos/duración**: interacción multi-turno T variable por trayectoria (no se reporta un T fijo único; se arman turnos de "stay", "update" (turno de corrección t_c) y "isolation" con ruido).
- **n**: Rule Discovery = 1.300 trayectorias (modelos instruct) / 1.503 (modelos "thinking"); Circuit Diagnosis = 1.049 (instruct) / 1.616 (thinking). Evaluación con k=3 muestras independientes por ejemplo.
- **Modelos evaluados**: Qwen2.5-7B-Instruct, Qwen3.5-9B (línea base + versión post-RL), y mención acotada de DeepSeek-V3.2 y GPT-5.2 (evaluación limitada, no el foco del paper).
- **Cómo puntúan** (con números): tres tasas de falla (más bajo = mejor), todas booleanas por muestra con agregación sobre k=3 réplicas:
  - **FSR (Failed Stay Rate)**, ecuación 8: `FSR = (1/|D_stay|) Σ_{x∈D_stay} F_stay^(k)(x)` — falla si el modelo cambia de creencia en turnos post-lock donde no había evidencia nueva.
  - **FUR (Failed Update Rate)**, ecuación 9: `FUR = (1/|D_update|) Σ_{x∈D_update} F_update^(k)(x)` — falla si el modelo NO actualiza en el turno de corrección t_c.
  - **FIR (Failed Isolation Rate)**, ecuación 10: `FIR = (1/|D_iso|) Σ_{x∈D_iso} F_iso^(k)(x)` — falla si el modelo tiene éxito en la trayectoria limpia pero falla en la trayectoria con ruido (mismo e_{1:t}, distinto n_{1:t}).
  - Falla a nivel de muestra: `F_m^(k)(x) = 𝕀[∃i∈{1,…,k}, E_m^(i)(x)=1]`.
  - **Reward de RL** (ecuación 6, similaridad de Jaccard entre conjuntos): `R_i(q_t) = |Ŝ_{i,t} ∩ S*_t| / |Ŝ_{i,t} ∪ S*_t|`.

## Citas verbatim clave

1. (§3.1, definición) "Contextual Belief Management (CBM): a model's ability to maintain an evidence-aligned belief state throughout a multi-turn interaction."
2. (§3.2, benchmark) "BeliefTrack formulates each task as evidence-conditioned belief-state tracking over a finite belief space ℬℰ."
3. (§3.1, taxonomía de fallas) "Failed Stay, Failed Update, and Failed Isolation. These diagnostics distinguish belief calibration failures from belief isolation failures."
4. (§3.3, diseño apareado) "Each template forms a clean–noised pair, o_{1:t}^clean=(e_{1:t},∅_{1:t}) and o_{1:t}^noise=(e_{1:t},n_{1:t}), that shares the same evidence history e_{1:t} but differs in the noise history."
5. (§4.2, método RL) "We optimize the model with GRPO using rewards computed by a symbolic verifier."
6. (§5.3, hallazgo principal) "Vanilla models consistently lack reliable CBM... BT-Prompt provides limited gains... RL with belief-state rewards consistently improves CBM."

## Números principales

- Tabla 1 (Core CBM Performance, RD y CD):
  - Qwen2.5-7B Vanilla: RD-FSR 99.0%, RD-FUR 98.0%, RD-FIR 97.0%; CD-FSR 99.0%, CD-FUR 98.0%, CD-FIR 97.0%.
  - Qwen2.5-7B RL-RD: RD-FSR 0.0%, RD-FUR 2.0%, RD-FIR 20.0%; CD-FSR 6.0%, CD-FUR 28.3%, CD-FIR 35.0%.
  - Qwen3.5-9B Vanilla: RD-FSR 47.0%, RD-FUR 60.0%, RD-FIR 83.7%; CD-FSR 43.2%, CD-FUR 62.7%, CD-FIR 95.4%.
  - Qwen3.5-9B RL-RD: RD-FSR 6.0%, RD-FUR 8.0%, RD-FIR 18.6%; CD-FSR 20.0%, CD-FUR 21.4%, CD-FIR 34.9%.
- Titular del abstract: "RL reduces failure rates by 70.9% on average."
- Capacidad general preservada tras RL (§5.3): GSM8K Qwen2.5-7B pasa de 83.3±0.4 (Vanilla) a 84.8±0.5 (RL-RD); MMLU/GSM8K "remain largely stable after training, with only small fluctuations."

## Qué les falta respecto de WAGER

- **No hay agente que entrega un modelo ejecutable puntuado contra verdad oculta**: la salida es un subconjunto de hipótesis simbólicas sobre un espacio finito ℬℰ (una lista de candidatos), no un artefacto ejecutable ni un modelo con el que se pueda simular/predecir contra ground truth continuo.
- **Bifurcación apareada del mismo episodio congelado cambiando UNA condición**: SÍ tienen algo parecido — el par clean/noise de §3.3 comparte e_{1:t} y difiere solo en n_{1:t}, que es literalmente la lógica de bifurcación apareada de WAGER, aunque acotada a "ruido sí/no" y no a manipular la condición de autoría, compromiso o fricción de revisión.
- **Evidencia con valor probatorio cuantificado (KL/likelihood)**: NO. La evidencia es simbólica y binaria (una regla verdadera/falsa, una lectura de instrumento); no hay ninguna cuantificación de cuánta información aporta cada pieza de evidencia (no hay KL, no hay likelihood ratio).
- **Trabajo propio acumulado**: NO. No hay noción de que el modelo haya invertido esfuerzo propio en una hipótesis previa que compita con la actualización (el "Failed Stay" mide justo lo contrario — resistencia sin causa, no inversión previa).
- **Fricción de revisión**: hay un turno de corrección t_c explícito (Failed Update mide si el modelo actualiza ahí), pero es un costo de "detectar que hay que actualizar", no un costo estructural de reabrir/rehacer trabajo ya entregado.
- **Casos cambiar/conservar/parcial**: tienen la partición Stay/Update/Isolation que es un pariente cercano, pero es taxonomía de turnos-de-evaluación, no de casos de evidencia graduada (todo o nada: la regla cambió o no cambió, no hay "evidencia parcial que amerita cambio parcial").
- **Cero-LLM en el reward**: SÍ lo tienen — el reward de RL es un "symbolic verifier" (Jaccard sobre conjuntos), sin juez-LLM. Esto es un punto de validación cercano a la regla dura de WAGER.

## Lecciones de diseño para WAGER

- **Copiar**: el patrón clean/noise apareado que comparte el prefijo de evidencia y bifurca solo el ruido es exactamente la lógica de "cambiar UNA condición por brazo" que WAGER usa — vale la pena citarlo como precedente de diseño experimental apareado en literatura de creencias de LLM.
- **Copiar**: la partición en tres modos de falla ortogonales (quedarse sin razón / no moverse con razón / dejarse mover por ruido) es un armazón de taxonomía limpio; WAGER podría usarlo como chequeo de sanidad adicional sobre sus propios brazos (¿el modelo se mueve con placebo? ¿se queda quieto con evidencia legítima?).
- **Evitar**: el espacio de creencias discreto y finito (candidatos enumerables) es mucho más pobre que "modelo ejecutable puntuado contra verdad oculta continua" — no serviría de molde de scoring para WAGER, solo de molde de bifurcación.
- **Citar**: útil como antecedente directo de "belief update" medido por comportamiento (no por lo que el modelo DICE que cree) — alineado con la premisa de WAGER de puntuar lo que se ENTREGA. Pero ojo: aquí lo entregado sigue siendo una afirmación simbólica ("creo que la regla es X"), no un artefacto ejecutable — la distinción vale la pena remarcarla en cualquier cita.

## Veredicto

**NOS-VALIDA** (parcial) — confirma con metodología independiente que el patrón "medir revisión de creencias por comportamiento, con bifurcación apareada evidencia-limpia vs evidencia-con-ruido, reward cero-LLM" es un diseño legítimo y da resultados fuertes (99%→0-30% de fallas con RL dirigido). No compite con WAGER porque el espacio de salida (hipótesis simbólicas discretas) y la ausencia de evidencia cuantificada por KL/likelihood y de fricción de revisión estructural lo dejan muy por debajo del listón de "modelo ejecutable + evidencia probatoria cuantificada + trabajo propio acumulado" que define a WAGER.
