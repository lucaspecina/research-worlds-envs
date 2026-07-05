# E1 — Matriz de celdas (BORRADOR v0.61; ~20 mundos, ARCHITECTURE §12)

> Borrador de cartera, NO constitucional. Principios que la ordenan: 2 formalismos
> (SCM + ODE), ≥5 suites, carga diferencial ≥2 coordenadas por mundo trampa,
> **la dificultad viene de COMPOSICIÓN (2–4 operadores) y PRESUPUESTO ajustado**,
> no de trampas sueltas (lección v0.60: una trampa de manual = mundo de control).
> Buckets: **[C]ontrol** (frontier debe aprobar — separa ejecución de juicio,
> E1-4) / **[T]rampa** (headroom buscado). La vara de rivales: escalera-de-6 +
> twins por capa. Presupuesto: holgado en [C], AJUSTADO en [T] (el dial central).

| # | Slot | Suite | Formalismo | Operadores (composición) | Bucket | Estado |
|---|------|-------|-----------|--------------------------|--------|--------|
| 1 | dummy_dose_v0 | causal-cliente | SCM | confounding (1) | C | **HECHO** (control) |
| 2 | latent_mix_v0 | Latent | SCM | hetero+confounding, proxy limpio | C | **HECHO** (control negativo) |
| 3 | latent_mix_v1 | Latent | SCM | ídem, dial declarado | C | **HECHO** (control; reclasificado v0.46) |
| 4 | selection_bias_v0 | sampling | SCM | collider+medición (2, fuentes) | C | **HECHO** (saturado v0.60) |
| 5 | latent_mix_v2 | Latent | SCM | hetero+confounding+**estado oculto por lote** (ventana n_cal) | T | **HECHO** (v0.64: tríptico confirmado; mejor solver 0.096 vs techo 1.0) |
| 6 | selection_bias_scarce_v0 | sampling | SCM | #4 recompuesto: mismo mundo, presupuesto ÷4 y réplicas ×3 precio | T | **HECHO** (v0.65: escasez muerde — R 0.00/0.84 vs 0.97/0.99) |
| 7 | survivorship+censura | sampling | SCM | survivorship + censura informativa (2) | T | por autorar |
| 8 | immortal-time | sampling | SCM longitudinal | immortal_time + selección (2) | T | por autorar |
| 9 | batch-effect confundido | canal | SCM | batch_effect + confounding (2) | T | por autorar |
| 10 | missingness informativo | canal | SCM | MNAR + error medición (2) | T | por autorar |
| 11 | logístico saturante | Horizon | **ODE** (crecimiento) | umbral_no_lineal + medición; forecasting held-out | C→T | 1º ODE (valida formalismo 2) |
| 12 | compartimental 2-tanques | Horizon | ODE | regime_shift + proxy (2) | T | por autorar |
| 13 | colas M/M/k | diagnóstico | eventos discretos | contaminación + selección (2) | T | por autorar (3º formalismo, opcional §12) |
| 14 | anomalía plantada | Anomaly | SCM | contaminacion_anomala + medición (2) | T | por autorar |
| 15 | anomalía temporal | Anomaly | ODE | contaminación + regime_shift (2) | T | por autorar |
| 16 | prior confiable | Prior | SCM | cualquiera, prior_reliability ALTA | C | por autorar (ancla anti-contrarian) |
| 17 | prior traicionero (move-37) | Prior | SCM | hetero + piel engañosa, prior_reliability baja | T | por autorar (requiere panel (c) re-elicitado) |
| 18 | identificabilidad | identificabilidad | SCM | acceso restringido; gana el ensemble ancho | T | por autorar (ejercita abstención) |
| 19 | triangulación | Horizon | SCM/ODE | 2 fuentes con sesgos complementarios | T | por autorar (§10 patrón) |
| 20 | revelación secuencial | causal-cliente | SCM | revelacion_secuencial + confounding (2) | T | por autorar (brecha de adaptividad) |

**Reglas de cartera**: (i) ningún [T] se certifica sin visibilidad de TODOS sus
operadores + E0-probe con headroom pre-registrado; (ii) cada [T] declara qué
coordenadas carga (≥2); (iii) los [C] son ~25% de la cartera (4–5) y ya están;
(iv) #6 es el test barato de la hipótesis "la dificultad está en el presupuesto"
sobre un mundo ya saturado — si sigue fácil con presupuesto ÷4, la dificultad
tiene que venir de composición, no de escasez; (v) pipeline: v2 (gate) → #6 →
#11 (formalismo 2) → resto por pares suite/formalismo.
