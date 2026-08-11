# Nota de dirección — La tesis de entrenamiento (E2): fabricar el gradiente del salto

> Registrada 2026-08-10 (Lucas, cierre de la era D1). **Para más adelante — E2/RL.** No cambia
> el trabajo de hoy (E1 sigue: re-vara → ronda del fallo). Origen: la síntesis de la era —
> **"sin cobro no tienen motivo — es difícil que dejen de ser lazy"** — + el freno de Lucas
> (la vara pagaba el salto 0.014) + ADRs 0175/0176/0177.

## 1. LA ESCALERA DEL COBRO ("del golpe al vacío" — nombre propuesto, Lucas puede renombrar)

Cuánto y cómo le cobra el mundo al agente NO saltar — cuatro pisos, tres ya medidos:

| Piso | Cobro | Evidencia |
|---|---|---|
| **C1 — el golpe** | el mundo te rebota el modelo en la cara (impasse) | rung 0: 0/9 sin golpe → **30/30** con golpe |
| **C2 — la cuenta visible** | la consecuencia está servida si la mirás (reporte, monitoreo) | rung 0 H-V1: más detalle NO suma (RAW ≥ estructurado) |
| **C3 — la paga muda** | la paga existe (verosimilitud, decisiones) pero nadie la muestra | D1 rondas 1-2: compran 60/60, escriben 2/15 y 1/15 — **el piso de la ciencia real (Rayleigh: 0.5%, paga práctica cero)** |
| **C4 — el vacío** | ninguna métrica la paga; solo la norma interna | el caso Einstein de "LLMs can't jump" (loss≈0 y reestructuró igual) — techo del programa |

En humanos, la capa SOCIAL (Dunbar: colegas/PI/réplica) convierte C3 en C1. Nuestros agentes
no tienen norma interna (a) ni colegas (b); los mundos actuales tampoco (b). Por eso C3 da lo
que da — y es diagnóstico, no excusa.

## 2. La apuesta: derribar "LLMs can't jump" fabricando el gradiente

El paper (klU4737opt, leído 2026-07-10): *"sin discrepancia significativa no hay gradiente que
empuje la reestructuración"* → estructuralmente incapaces del salto abductivo. La tesis de
Lucas: **fabricar el gradiente sintéticamente** — entrenar (RL, policy abierta 4-8B, GPU E2)
sobre mundos donde saltar ES la jugada ganadora, con reward cero-LLM (el cobro en training).
Si la disposición transfiere a mundos sin cobro, el argumento cae empíricamente: no con
argumentos — con un modelo entrenado.

## 3. El curriculum: cobros desvanecientes

Entrenar C1 → C2 → C3 (sacarle las rueditas): primero el golpe, después la cuenta que hay que
ir a mirar, después la paga muda. La escalera de cobros pasa de taxonomía descriptiva a
**schedule de entrenamiento**.

## 4. El test final: EL TEST RAYLEIGH

Policy entrenada, suelta en un mundo C3 held-out (tipo D1, sin cobro visible): ¿compra los
chequeos y ESCRIBE la estructura sin que nadie la golpee? Si sí → la norma quedó adentro (lo
único que separaba a Rayleigh del resto). Medible con nuestra vara, cero-LLM, gemelo incluido
(no vale ver estructura donde no la hay). C4 (señal cero) queda como techo declarado.

## 5. Precondiciones (todas nacidas del 2026-08-10)

1. **El reward PAGA el salto** (ADR 0175: rival vago óptimo pierde fuerte; vara de forma
   completa/CRPS). Existencial: contra la vara de D1, el RL habría aprendido la **vagancia
   óptima** (campana afinada = 0.986 gratis). El freno de Lucas salvó E2 antes de que exista.
2. **Resolubilidad con agente** (ADRs 0176/0177/0179/0180): con la idea nombrada, pero sin la
   solución, el agente debe poder investigar e implementar el salto. En esta etapa es una pregunta
   de diseño y un control previo, no el objetivo ni una subpregunta científica del experimento.
   Compararlo con la condición sin ayuda puede estudiar la dificultad de descubrirlo recién sobre
   un mundo ya validado. La solución servida queda solo como control de techo.
3. **Diversidad de mundos** (la fábrica, hoy pausada): sin ella, el RL memoriza los 11
   operadores y no generaliza al 12 — la fábrica vuelve a ser central en E2.
4. Test de contaminación constitutivo (Magnani: creatividad relativa al repertorio).

## 6. Riesgos honestos

(a) Reward hacking de la vara (por eso CRPS + 0175); (b) memorizar la taxonomía → no
generalizar (por eso diversidad + held-out por operador); (c) la disposición no transfiere —
posible: el negativo también es paper ("el gradiente sintético no alcanza para internalizar
la norma").
