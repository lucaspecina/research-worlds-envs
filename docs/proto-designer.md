# Proto-designer — spec de trabajo (la fábrica automática de mundos)

> **Estado: BORRADOR DE DISEÑO (ADR 0093).** El multiplicador FUNDAMENTAL (Lucas): sin
> generación automática el proyecto no escala. La mitad VERIFICADORA ya existe (certificación
> cero-LLM); falta la mitad GENERADORA. Formato #11/Mundo-A: diseño completo, decisiones
> abiertas marcadas **[A]/[B]/[C]/[D]**, pre-registros firmables. LLM permitido acá (lado
> fábrica; el reward path sigue cero-LLM). Ante conflicto con el repo, manda el repo.

## 1. La idea en una frase

Un proceso (LLM lado-fábrica) recibe una **consigna** — "un mundo que castigue tal vicio,
tal dificultad, tal formalismo" — y produce `world.py` + `meta.json` + `brief.md`; la
**certificación cero-LLM que ya existe** lo acepta o lo rechaza SIN humano. La métrica es
el **yield**: qué fracción de lo generado certifica sin cirugía humana, por nivel de
consigna.

## 2. Lo que YA existe (la mitad difícil, verificadora)

Todo esto es cero-LLM y ya corre — es lo que hace SEGURA la generación por LLM (el
generador puede ser mediocre; el filtro es duro):
- Derivación mecánica de rivales, batería y certificados desde `meta` (`derive_rivals`,
  `build_battery`, el patrón `build_and_certify`).
- Gates: escalera L1 (sin inversiones), visibilidad por operador ≥ piso, recuperabilidad,
  naive-far, null-floor, carga diferencial ≥2 coordenadas.
- Certificado de trampa necesaria (robots vicioso/cuidadoso, ADR 0082) para anti-vicio.
- Test de contaminación (semillas famosas), pin no-op, sanidad de escala.
- **Un mundo generado que pasa la certificación completa es usable, lo haya escrito quien
  lo haya escrito.** Ese es el teorema que habilita todo.

## 3. Lo que FALTA (la mitad generadora) + lo que NO cambia

**Falta**: `world.py` + `meta.json` + `brief.md` desde la consigna. **No cambia** (doctrina):
- **La librería de operadores crece a demanda de semillas reales, no por imaginación suelta**
  (CLAUDE.md). El generador **COMPONE desde la librería de mecanismos vetados** (SCM lineal,
  confounding, selección/collider, canal/ruido, censura-archivo, batch/deriva, latent-mix,
  logístico-ODE), **no inventa mecanismos libres**. Esto lo mantiene verificable y
  doctrina-compliant. **[A: cuánta libertad dentro de la composición.]**
- **Brief ciego** (anti-leak): lo escribe un proceso ciego a batería y rivales; ve solo
  stakes/columnas/superficie de control. Doctrina existente.
- **Cero-LLM en el reward**: el `world.py` generado se verifica por la certificación
  cero-LLM; el LLM nunca toca el cómputo del reward. Frontera intacta.
- **El solver jamás ve la taxonomía de operadores** ni la consigna.

## 4. La arquitectura (consigna → generador → certificación → yield)

```
consigna ──▶ [GENERADOR LLM]  (compone mecanismo desde la librería,
   │            declara operadores+stakes+functional en meta,
   │            escribe world.py parametrizado)
   │                        │
   │                        ▼
   │            [WRITER CIEGO LLM]  (brief desde stakes/columnas, ciego a batería/rivales)
   │                        │
   ▼                        ▼
[CERTIFICACIÓN CERO-LLM]  build_and_certify + gates + contaminación + pin no-op
   │
   ├── PASA sin humano ──▶ yield++ (mundo entra a la cartera candidata)
   └── FALLA ───────────▶ yield-- (se registra POR QUÉ falló; no se retoca a mano)
```

- El generador puede correr la certificación y **auto-ajustar acotado** (la línea brillante
  pre-certificación, ADR 0056/0077 — declarado/registrado, jamás post-firma) dentro de un
  **presupuesto de intento declarado**. "Sin cirugía humana" = alcanza certificación dentro
  de ese presupuesto sin que un humano lo toque. **[B: el intento incluye auto-ajuste
  acotado, o es one-shot puro?]**

## 5. La escalera de encargos (ADR 0084/0086)

- **FÁCIL — re-skin**: re-skinear un mundo certificado (vocabulario/dominio nuevo, math
  IDÉNTICA). Verificación durísima: certificados **byte-idénticos** al original (el re-skin
  es no-op sobre la math). Testea el PLUMBING del generador (¿produce world.py+meta+brief
  válidos que cargan y certifican?), no la creatividad de diseño. **Yield esperado: alto.**
  → **este es el primer build.**
- **MEDIO — estático nuevo**: un mundo estático nuevo con un tipo de trampa CONOCIDO
  (nueva composición de operadores de la librería: p.ej. confounding+selección en un dominio
  nuevo). Testea que el generador compone y parametriza para certificar. **Yield esperado:
  medio.**
- **DIFÍCIL — Mundo B**: el mundo de dos-historias-gemelas con las tres decisiones de
  carpintería fina (ADR 0084) escritas en la consigna, sobre la degeneración certificada del
  logístico (ADR 0076). Incluye generar el par de robots. **Yield esperado: bajo (timebox +
  fallback a diseño manual).**

## 6. Las decisiones abiertas

### [A] — libertad del generador dentro de la composición
Espectro: (i) **template-fill puro** (elige operadores de un menú + rangos de parámetros;
el world.py sale de una plantilla) — máxima verificabilidad, mínima creatividad; (ii)
**composición libre** (escribe world.py componiendo primitivas con wiring propio) — más
expresivo, más riesgo. Recomiendo **(i) para fácil/medio, (ii) acotado para difícil** (Mundo
B necesita el wiring de las dos historias). **[A: firmar el nivel por peldaño.]**

### [B] — one-shot vs auto-ajuste acotado
"Yield sin-retoque por nivel" (Lucas): un intento por encargo, nada de retocar-hasta-pasar.
Pregunta: ¿el "intento" incluye el loop interno certify-y-ajustar-parámetros del generador
(acotado, como el humano hace pre-certificación) o es one-shot literal? Recomiendo:
**auto-ajuste acotado dentro de un presupuesto declarado** (p.ej. ≤3 re-parametrizaciones,
solo de rangos declarados, jamás cambio estructural), porque eso ES lo que automatiza al
humano; el yield mide "certifica dentro del presupuesto sin humano". El one-shot puro
mediría algo más frágil. **[B: firmar la definición de intento + el presupuesto.]**

### [C] — anti-contaminación y writer ciego, wiring concreto
Dos etapas separadas: (1) generador mecanismo+meta; (2) writer ciego del brief (ve solo
stakes/columnas/control surface). Más el test de contaminación como gate. Abierto: ¿el
generador de mecanismo también debe ser ciego a algo (p.ej. a la batería, que se deriva
DESPUÉS)? La batería se deriva de meta, así que el generador no la ve por construcción —
pero el generador SÍ conoce la trampa (la puso). El brief NO debe. El writer ciego lo
garantiza. **[C: firmar la separación de etapas + qué ve cada una.]**

### [D] — diseño del experimento de yield
N encargos por nivel, un intento cada uno, yield = fracción que certifica. Pre-registrar
N y los yields esperados por nivel ANTES de correr. Primera pasada = la mínima informativa
(costo de API estimado antes, regla CLAUDE.md). Abierto: N por nivel; y si el yield del
fácil debe ser ~100% (si no, hay bug de plumbing, no de diseño). **[D: firmar N + yields
esperados.]**

## 7. Pre-registros firmables

- **Fácil**: yield esperado ~100% (re-skin es no-op; un fallo ahí = bug de plumbing, no de
  diseño); verificación = certificados byte-idénticos + suite verde + brief sin flag-words.
- **Medio**: yield esperado a firmar antes (p.ej. ≥50% en la primera pasada); cada fallo se
  clasifica (¿operador mal parametrizado? ¿stakes sin trazabilidad? ¿trampa no-visible?).
- **Difícil**: timebox; yield esperado bajo; fallback a diseño manual de Mundo B con las
  tres decisiones de ADR 0084.
- **Auditoría humana antes de E1** (regla dura): todo mundo generado que certifique pasa la
  auditoría de batería humana (los ~10 regímenes de mayor peso) antes de entrar a E1 — el
  único detector confiable de corrupción silenciosa de relevancia a esta escala.

## 8. Secuencia (spec-first)

1. **Estresar este spec** — firmar A/B/C/D. (Ahora, en paralelo al primer build.)
2. **Build FÁCIL (re-skin)**: el generador re-skinea un mundo certificado; verificar
   certificados byte-idénticos. Primer punto de yield. (Arranca ya — no depende de A/B/C/D
   para el peldaño no-op; su math no cambia.)
3. **Build MEDIO**: recién con A/B firmadas.
4. **DIFÍCIL / Mundo B**: timebox, con la consigna de ADR 0084.

**Compuerta**: si el yield del fácil no es ~100%, es plumbing y se arregla antes de subir.
Si el medio da yield ~0 tras varios encargos, el generador no compone y se reporta (la
librería o la consigna necesitan trabajo) — dato, no fracaso.
