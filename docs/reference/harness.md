# Episodio, harness y lo mínimo para E1

> Referencia técnica (ex ARCHITECTURE.md). Los números de sección (§N) se
> preservan; las citas '§N' de otros docs resuelven acá o en los hermanos de
> `docs/reference/`. El *por qué* llano está en `WIKI.md`.

## 8. Episodio — harness `[ESTABLE en protocolo]`

- **Runtime**: kernel Jupyter persistente (patrón ya probado en SREG); objeto `env` inyectado; Python libre entre llamadas.
- **Opacidad**: el mundo corre server-side (proceso/contenedor separado); `env` es un cliente RPC. El agente no puede leer `world.py` ni la batería. Requisito duro (ataque #7).
- **Verbos** (protocolo universal; argumentos declarados por mundo):
  - `env.describe()` — gratis: brief, schema, fuentes+costos, superficie de control, presupuesto restante.
  - `env.observe(source, n)` — debita según `sources.yaml`; devuelve vista corrompida por los operadores de esa fuente.
  - `env.experiment(design)` — caro; `design` = {población, regla de asignación (incl. condicional/estratificada), configuración de superficie, horizonte, qué medir}. **El experimento esquiva el proceso de muestreo de las fuentes históricas (eso es lo que compra la aleatorización) pero NUNCA el canal de medición** — el termómetro sigue siendo el mismo termómetro. Operadores opcionales de imperfección experimental (non-compliance, attrition, error del instrumento) con perilla habilitan el trade-off **barato-y-sucio vs caro-y-limpio**: auditar el propio experimento es parte del juicio; el experimento perfecto entrenaría el anti-skill "el experimento aleatorizado es palabra santa".
  - `env.submit(code)` — terminal tras validación de humo.
- **Criterio de admisibilidad de verbos nuevos**: ejecutable determinísticamente desde la declaración del mundo. Extensiones candidatas: `buy_instrument` (revela columnas ocultas), `consult` (NL generado DESDE el programa — dirección formal→NL, segura).
- **Mundos observacionales** (suite Horizon): `experiment` ausente del menú; la superficie es elección de población/época/instrumento.
- **Ledger**: episodio termina por submit o quiebra. Ratio presupuesto/complejidad: dial central del curriculum.

### Validación de humo en submit (no es scoring)
3 regímenes públicos triviales: columnas exactas, tipos, n, timeout, sin red, **lint de imports de la submission** (allowlist: stdlib seguro + numpy/pandas/scipy/sklearn; sin red/subprocess/filesystem). Falla → error devuelto, episodio sigue abierto. El mismo lint, aplicado por el validator de fábrica, rige para `world.py` (allowlist: numpy/scipy/stdlib; sin subprocess/os/red).

### Semántica de bordes
Key de régimen ignorada = claim implícito de no-efecto (la batería lo cotiza). **Crash/NaN en un ítem → se asigna `D_MAX_item = 1.5 × D(verdad, null_model)` en ese ítem** (NO un clamp universal sobre distancias legítimas — v0.12): crashear paga estrictamente peor que no saber nada, para que el crash deliberado no sea una abstención trucha. Una distancia legítima > D_MAX solo se clampea como **cota de robustez** (el modelo es peor que 1.5× el nulo). **El null de referencia es el null MODEL** (marginales del pool, el mismo que ancla S_null), no una permutación de columnas de la verdad: la permutación conserva las marginales correctas y subestima cuán malo es "no saber nada" off-support, dejando que el propio nulo supere su cap (v0.12). Seeds apareados + m repeticiones por ítem (semántica precisa en §9).

---

## 12. Lo mínimo para E1 `[ESTABLE]`

Contenedor de casos (§1) + harness (§8) + scorer (§9) + constructor de batería (§6, puede ser semiautomático al principio) + **~20 mundos hechos a mano** en 2 familias (SCM + un ODE), cubriendo ≥5 suites, con certificados computados. Sin designer automático, sin RL, sin operadores abiertos. Modelos frontier vía API + las 3 manipulaciones de constructo de `docs/archived/NORTH_STAR_full.md` §6-E1.

---

## 14. Open items técnicos

1. Sampler de regímenes candidatos por familia de superficie (hereda OQ#1 de `docs/open-questions.md` — punto de presión #1).
2. Arquitectura RPC del handle opaco sin matar latencia del REPL.
3. Gramática de `design` en `experiment` por familia (describe el experimento, no creencias).
4. n_mc, K, m y n de scoring para varianza de reward objetivo (<x% del rango).
5. Fit generativo del rival (a): elección de la familia condicional.
6. Re-ajuste de parámetros del gemelo inocente (b): procedimiento estándar.
7. Compilación del prior evocado (c): prompt del panel + agregación.
8. MDL: alternativas a zlib (AST, parámetros); sensibilidad de λ.
9. Prompts de manipulación de constructo para E1 (descuidado / prolijo / base) — necesarios para la predicción 2 de E1.
10. Oráculo de valor v0 (EIG greedy por Monte Carlo sobre los 20 mundos a mano) — necesario para la predicción 3 de E1; las predicciones 1–2 pueden correr antes.
11. Probe "aprendió al generador": clasificador que intente predecir el operador instalado desde el brief/datos superficiales — alarma complementaria a E3 contra tells del generador.
12. Pipeline de minado de semillas: formato de la cola (NTSB/investigaciones/obs→experimento), criterios de priorización, y el trigger "moraleja inexpresable → operador nuevo".
13. Diseñador greedy-EIG por formalismo: maquinaria compartida entre proxy de adaptividad (§7) y oráculo de valor v0 — definir alcance mínimo.
14. Márgenes de la escalera (L1) y CV objetivo (L2): valores iniciales fijados (5% del rango; CV < 5% sobre R — Decision Log v0.10); queda abierto el procedimiento de ajuste empírico.
