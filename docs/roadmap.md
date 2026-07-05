# Roadmap y estado — WAGER

> **Dónde estamos, la cartera de mundos, y el plan de validación E1→E4.** La sección
> *Estado actual* se mantiene al día cada sesión; el resto es el plan estable. Los
> resultados detallados de cada hito están en `docs/adr/`; lo sin decidir en
> `docs/open-questions.md`.

## Estado actual `[VOLÁTIL — mantener al día]`

**Verde**: reward path (Slice 1) + harness (C1+C2+C3) + factory de derivación completos;
`pytest` ~125 verdes. Infra de mundos-trayectoria lista (ADR 0068). Docs reestructurados
(ADR 0070) + re-skin a "línea de proceso" (ADR 0071).

**Hitos**: **v2 (trofeo)** — tríptico confirmado con solver real; en 10 episodios / 2
familias nadie infiere composición por-lote, máx R=0.666 (falta juicio, no ejecución).
**#6** — el presupuesto discrimina estilos. Detalle en ADRs 0064-0068.

**Próximo**: **#11 — primer mundo ODE** (logístico saturante, Horizon): valida el 2º
formalismo. Spec en `docs/archived/MUNDOS_DINAMICOS_CONTEXT.md`. Orden: contrato de fuentes
→ world+meta → brief ciego → derivación → certificados → E0-probe. Vara: 1-2 sesiones.

**Decisión pendiente de Lucas**: re-orientar los slots 7-20 de la cartera a cobertura de
failure modes (`docs/open-questions.md` #16); prioridad del proto-designer (#14).

## Cartera E1 (20 slots; 6 hechos)

> El mundo = **composición de operadores** con dificultad declarada, no trampas sueltas.
> Buckets: **[C]ontrol** (frontier debe aprobar) / **[T]rampa** (headroom buscado).
> Presupuesto holgado en [C], ajustado en [T] (el dial central).

| # | Slot | Suite | Formalismo | Bucket | Estado |
|---|------|-------|-----------|--------|--------|
| 1 | dummy_dose_v0 | causal-cliente | SCM | C | HECHO |
| 2 | latent_mix_v0 | Latent | SCM | C | HECHO (control negativo) |
| 3 | latent_mix_v1 | Latent | SCM | C | HECHO |
| 4 | selection_bias_v0 | sampling | SCM | C | HECHO (saturado) |
| 5 | latent_mix_v2 | Latent | SCM | T | HECHO (tríptico confirmado) |
| 6 | selection_bias_scarce_v0 | sampling | SCM | T | HECHO (presupuesto discrimina) |
| 7 | survivorship+censura | sampling | SCM | T | por autorar |
| 8 | immortal-time | sampling | SCM longitudinal | T | por autorar |
| 9 | batch-effect confundido | canal | SCM | T | por autorar |
| 10 | missingness informativo | canal | SCM | T | por autorar |
| 11 | **logístico saturante** | Horizon | **ODE** | C→T | **PRÓXIMO** (1er ODE) |
| 12 | compartimental 2-tanques | Horizon | ODE | T | por autorar |
| 13 | colas M/M/k | diagnóstico | eventos discretos | T | por autorar (3er formalismo) |
| 14 | anomalía plantada | Anomaly | SCM | T | por autorar |
| 15 | anomalía temporal | Anomaly | ODE | T | por autorar |
| 16 | prior confiable | Prior | SCM | C | por autorar |
| 17 | prior traicionero (move-37) | Prior | SCM | T | por autorar |
| 18 | identificabilidad | identificabilidad | SCM | T | por autorar |
| 19 | triangulación | Horizon | SCM/ODE | T | por autorar |
| 20 | revelación secuencial | causal-cliente | SCM | T | por autorar |

Reglas: ningún [T] se certifica sin visibilidad de TODOS sus operadores + E0-probe con
headroom pre-registrado; cada [T] carga ≥2 coordenadas; los [C] son ~25% y ya están.

**Deudas registradas sin gatillar**: barrido c_F suite sampling; κ (4 divergencias R vs
|ΔP|); re-elicitación rival (c); derivación automática para mundos-ventana.

---

# Programa experimental — la escalera E1→E4 `[ESTABLE]`

> El plan de validación del proyecto (ex NORTH_STAR §6). De barato a caro; cada escalón con
> criterio de muerte explícito.

Principio rector: **no se testea la droga sin validar el ensayo.** Orden de barato a caro; cada pelfalla con criterio de muerte explícito; cada pelfalla publicable por sí solo. E2 y E3 son, además, **el sensor del loop maestro**: sus firmas dicen dónde parchear el juego.

La validación es una **pirámide**: los niveles L0–L2 (tests de contrato + sandbox red-team, escalera de verdades degradadas, protocolo de varianza del reward) validan la *maquinaria* y viven en `docs/reference/certificates.md` §13; la escalera E1→E4 de abajo valida el *constructo* (L3) y la *hipótesis* (L4–L5).

### E1 — Validez del instrumento (sin entrenar nada)

Decenas de mundos hechos a mano (dos formalismos) **+ mundos de control sin trampas** (para aislar el confound juicio-vs-ejecución); pasar por ellos modelos frontier existentes. Predicciones y chequeos que deben cumplirse:

1. El spread entre modelos respeta el orden conocido de capacidad de research.
2. **Manipulación de constructo**: el mismo modelo prompteado descuidado/overclaimer se desploma; prompteado metodológicamente prolijo, sube.
3. El score correlaciona con las firmas del trace (información por unidad de presupuesto, vía oráculo de valor).
4. **Mundos de control**: sin trampas, los modelos con buena ejecución convergen; el spread de juicio aparece solo con trampas. El perfil de juicio se reporta *condicional a la ejecución*, y la ejecución por separado (réplica interna del contraste ScienceWorld/DiscoveryWorld).
5. **Baseline humano**: 3–5 personas con formación en causal/estadística juegan ~10 mundos en el mismo REPL. Si los humanos competentes no superan a los frontier, el constructo está en duda.
6. **Validez convergente y discriminante**: los mismos modelos corridos en BoxingGym/DiscoveryBench/QRData — la correlación valida, la divergencia es hallazgo. Discriminante: el perfil debe agregar varianza más allá de un score de capacidad general (correlación parcial).
7. **Auditoría humana de baterías** (obligatoria): por cada mundo, leer los ~10 regímenes de mayor peso y verificar que son científicamente significativos — el único detector confiable de corrupción silenciosa de la relevancia a esta escala.

**Muerte**: si el eval no separa a un agente deliberadamente chapucero de uno cuidadoso, se frena todo — no hay instrumento.

### E2 — ¿Juicio o template?

RL con un modelo abierto mediano. La mirada NO va al score (sube seguro) sino a las **firmas**: ¿sube la información por experimento? ¿mejora la calibración (descomposición del proper score)? ¿aprende a abstenerse en lo no-identificable? ¿pesa priors adaptativamente al mover la perilla? ¿aparecen hipotetizar-discriminar-actualizar en los traces (backtracking, testeo de implicancias, pivoteo ante anomalías)? Diagnóstico de template: secuencias ritualizadas idénticas entre mundos, ganancia concentrada en motivos vistos.

**Muerte (parcial)**: score sube + firmas planas = máquina de templates; el loop maestro parchea curriculum/diversidad/brechas antes de seguir.

### E3 — Abstracción (decisivo y 100% interno — no necesita datos reales)

Entrenar reteniendo **familias enteras de operadores** y hasta **formalismos enteros** (entrenar en SCMs, testear en ODEs/colas). Lo convincente no es el efecto principal sino las dos **interacciones que nuestra propia teoría predice**:

1. El transfer escala con la **diversidad** de operadores de entrenamiento, no con la cantidad de mundos (la memorización predice lo contrario).
2. Las firmas de juicio emergen solo cuando presupuesto/complejidad es ajustado.

**Muerte**: sin transfer entre familias retenidas tras esfuerzo honesto en diversidad → la hipótesis de habilidad abstracta está muerta; queda un benchmark, no un método de entrenamiento. Se dice sin vergüenza.

### E4 — Sim2real (el titular)

- **Eval primario**: pares **observacional→experimento** — datasets observacionales reales cuya verdad la zanjó después un experimento aleatorizado (canónico: un análisis observacional revertido por un experimento posterior; curar casos oscuros y experimentos posteriores al cutoff, renovables en el tiempo). Secundario: predicción de replicación (SCORE / Replication Markets).
- **Anti-memorización**: delta **con-datos vs sin-datos** — si predice el experimento aleatorizado sin mirar el dataset, es memoria; importa cuánto gana por analizar.
- **Controles (cómputo igualado)**: (a) modelo base; (b) RL sobre math/código — el contrafáctico honesto de qué haría un lab con esas GPUs; (c) **ablación del ingrediente activo**: los mismos mundos con reward naive de preguntas fijas estilo v1.5.
- **Puente sin costura**: el agente investiga el dataset observacional real *en el mismo harness* (una fuente, presupuesto) y entrega su maqueta como siempre; predecir el experimento aleatorizado = **consultar la maqueta en el régimen del ensayo**. Cero mismatch de formato entre entrenamiento y demo.

**El número que decide todo**: el delta en obs→experimento contra el control de cómputo igualado.

### Notas de honestidad sobre la prueba misma

- Un nulo a escala chica (ej. 8B) es evidencia débil: el juicio podría "prender" a cierta escala. Mitigación: E1 ya da señal con frontiers sin entrenar; versión intermedia barata: experiencia in-context sobre mundos (sin tocar pesos) como sonda de transfer.
- Un positivo a escala chica con los controles bien hechos ya es enorme.
- Precedente a favor de E2: el RL de matemática con reward de outcome puro hizo emerger verificación y backtracking sin pedirlos; nuestro reward es más denso que un binario.
