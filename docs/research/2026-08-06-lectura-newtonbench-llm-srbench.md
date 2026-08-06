# Lectura a texto completo — NewtonBench y LLM-SRBench (paso 1 del slice de saltos)

> **Fecha:** 2026-08-06 · **Método:** extracción dirigida en dos pasadas sobre el HTML completo de
> arXiv por paper (generación/construcción + evaluación/hallazgos), con verbatims. Alimenta la
> ficha del [slice mezcla](2026-08-05-plan-slice-salto-mezcla-v0.md) y el diseño de la
> [máquina](2026-08-05-menu-estrategico-y-maquina-de-saltos.md).

## NewtonBench (arXiv 2510.07172; Zheng et al.)

**Generación.** "Counterfactual law shifts" = **mutaciones sobre el árbol de expresión** de leyes
canónicas: cambian operadores (suma→producto) o constantes (exponente 2→3). Dificultad por
acumulación: Easy = 1–2 mutaciones · Medium = +1–2 · Hard = +1–2. **Complejidad de sistema** en
tres niveles: ecuación sola / sistema simple (1–2 ecuaciones auxiliares) / sistema complejo
(varias auxiliares = confusores). 108 leyes × 3 = 324 tareas, 12 dominios de física.

**Interacción.** `<run_experiment>`: el agente asigna valores a las variables de entrada y recibe
las salidas del modelo completo — un do() sobre perillas, como el nuestro. **Sin presupuesto duro
declarado** (miden tokens, no cobran experimentos). Intérprete Python opcional. Entrega = ecuación
simbólica.

**Scoring.** Primario: exactitud simbólica binaria vía **LLM-as-judge** (98.3% acuerdo con
expertos; Appendix A.4.1). Secundario: RMSLE. **No es cero-LLM.**

**Solvabilidad.** Prueba FORMAL genérica (Appendix E.2: reducción a oráculo directo +
identificabilidad de muestra finita). No corren un testigo mecánico por instancia.

**Controles negativos / gemelos: NO EXISTEN.** Las 324 tareas tienen ley mutada; no hay tarea
donde "la ley no cambió" sea la respuesta correcta.

**Hallazgos con números.**
- Degradación por complejidad: GPT-5 92.4% (easy/vanilla) → 29.9% (hard/complex);
  Gemini-2.5-pro → 13.9%; el resto de los razonadores <5% en lo más difícil. No-razonadores <10%
  en todo (GPT-4.1 5.3%).
- **Sensibilidad extrema al ruido:** ruido 0.0001 → −13–15% de exactitud vs sin ruido.
- **Tool paradox** (verbatim): *"stronger LLMs… tend to leverage code for tasks like
  function-fitting. This can accelerate convergence to a 'good enough' solution, causing the
  model to prematurely settle in a local optimum."* Números: GPT-5 72.9→69.6 · Gemini-2.5-pro
  65.0→62.0 · GPT-5-mini 51.5→44.7 con code; los débiles MEJORAN (GPT-4.1-mini 4.6→13.0).
- Limitaciones declaradas: leyes mutadas dimensionalmente coherentes pero quizá físicamente
  implausibles; tool-paradox correlacional, no causal; sin baseline humano.

## LLM-SRBench (arXiv 2504.10415; ICML 2025 oral)

**LSR-Transform (111 problemas desde 100 ecuaciones de Feynman).** Receta: elegir una variable de
entrada como nuevo target → **resolver la ecuación para esa variable con SymPy** → conservar solo
las analíticamente resolubles → filtrar datos al dominio válido de la forma nueva → LLM redacta el
enunciado nuevo. Complejidad controlada (nodos del árbol) al rango de la distribución original.

**LSR-Synth (128: química 36 · biología 24 · física 43 · materiales 25).** Términos conocidos
(lista generada por GPT-4o) + **términos sintéticos novedosos** (LLM) → combinar → verificar
solvabilidad con solvers numéricos (`solve_ivp`) → chequeo de novedad (LLM) → generar datos →
**validación por dos expertos humanos**. Ej.: cinética con término `kA²/(1+βA⁴)`.

**Verificación de identificabilidad: NO formal** — solo "el solver corre". Sin testigo por
instancia.

**Memorización rota, demostrada por brecha:** a igual complejidad, Feynman ~50%+ vs
LSR-Transform ~31% (verbatim: *"substantially more challenging… despite identical equation
structure but alternative mathematical forms"*); baseline **DataBlind** (sin datos) falla →
el conocimiento previo solo no alcanza; la firma "caída abrupta del error" delata recall.

**Scoring.** Exactitud simbólica vía **GPT-4o como evaluador** (94.6% acuerdo con humanos) +
Acc_τ y NMSE numéricos + **test sets OOD** para LSR-Synth. **Tampoco es cero-LLM.**

**Resultados.** Mejor sistema (LLM-SR + GPT-4o-mini): **31.5%** en LSR-Transform, 28.1% en
LSR-Synth. Backbones chicos (Llama-3.1-8B, GPT-3.5, GPT-4o-mini) — ojo generacional.

## Qué ROBAMOS y qué queda confirmado (implicancias directas para la ficha)

1. **Confirmado el hueco:** ambos vecinos puntúan con juez-LLM y NINGUNO tiene gemelos/controles
   negativos ni presupuesto de evidencia. Cero-LLM + gemelos + economía + testigo por instancia
   siguen siendo nuestra combinación exclusiva — ahora verificado a texto completo.
2. **Robamos de LSR-Transform:** el truco "resolver para otra variable" como transformación
   anti-memorización (aplicable a nuestras pieles); y el control de complejidad apareada al
   comparar (nodos del árbol) — usarlo si comparamos niveles de la escalera.
3. **Robamos de LSR-Synth:** el patrón proponedor-LLM + verificador-mecánico + validación humana
   para la fábrica (= nuestro writer ciego + certificados, convergencia independiente); y los
   test sets OOD como estándar (ya lo tenemos como batería held-out).
4. **Robamos de NewtonBench:** mutación-sobre-árbol como dial de dificultad discreto (contar
   mutaciones); niveles de sistema (vanilla/simple/complex = nuestra escalera de composición,
   validada afuera); y la advertencia del RUIDO: con 1e-4 ya duele — **nuestra perilla de
   solapamiento/ruido se calibra con el testigo BAJO el ruido real del mundo**, no en abstracto.
5. **Tool paradox = nuestra candidata de cierre, medida afuera:** el kernel puede inducir
   ajustar-y-cerrar prematuro en modelos fuertes. Para el slice: el kernel es parte de la
   ecología; registrar qué ajusta y qué chequea (conecta con el brazo B instrumentado gratis).
6. **Su solvabilidad es genérica (prueba formal) o débil ("el solver corre"); la nuestra es por
   instancia y mecánica (testigo).** Punto de venta del paper de la máquina.

## Registro

Filas actualizadas en `lectura-de-fuentes.md` (NewtonBench → LEÍDO; LLM-SRBench → fila nueva
LEÍDO). Etiqueta NewtonBench en `vicios/vicio-2` → VERIFICADO con números.
