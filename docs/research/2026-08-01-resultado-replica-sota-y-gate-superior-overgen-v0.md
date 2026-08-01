# Resultado — réplica SOTA y gate superior de `overgen_stream`

> **Estado:** evidencia exploratoria de instrumento; 4 donantes, 2 modelos, una familia de mundo.

## Réplica gpt-5.4 / 94200

Pasó todos los gates en turno 3 (`SD_pre=0.843`, forma compartida `ratio=0.035`), replay/ledger
exactos y entregas 2/2.

- **Alcance limitado:** `R_diag 0.213 → 0.832`; referencia `0.830`; `F=1.004`. La estructura
  cambió de compartida (`0.035`) a diferenciada (`2.014`) en el primer turno posterior.
- **Transferencia:** `R_diag 0.534 → 0.705`. La forma permaneció dentro de compartida
  (`ratio=0.489 < 1`), aunque refinó parámetros por línea. Por eso “cambió el código” no equivale
  a “abandonó la estructura”.

## Trayectoria estructural conjunta

`ratio` es dispersión de las formas entre líneas / incertidumbre predictiva. Menor que 1 indica
estructura compartida; mayor que 1, diferenciación material.

| Donante | Pre | Final limitado | Final transferencia | Lectura |
|---|---:|---:|---:|---|
| DeepSeek 94100 | 0.035 | 2.818 | 0.035 | diferenciación correcta |
| DeepSeek 94101 | 0.031 | 0.031 | 0.255 | **no hizo la revisión estructural** |
| DeepSeek 94102 | 0.035 | 2.744 | 0.035 | diferenciación correcta |
| gpt-5.4 94200 | 0.035 | 2.014 | 0.489 | diferenciación correcta |

El caso 94101 es especialmente informativo: el razonamiento reconoció peor ajuste en líneas 2–3
y mayor variación alta, pero la entrega conservó una forma compartida y empeoró contra la verdad.
Es una brecha dice-hace medida en el artefacto, no por un juez LLM.

## Qué aprendimos de verdad

1. El fork natural distingue evidencia que refuta parcialmente de evidencia compatible sin
   anunciar “ahora revisá tu creencia”.
2. El modelo ejecutable permite separar mejora numérica de cambio estructural.
3. La trayectoria importa: algunos `M_pre` eran todavía muy anchos y el episodio mezclaba
   formación con revisión; confianza/competencia previa debe reportarse como moderador.
4. Score global, score local, referencia legal y geometría estructural capturan fallas distintas.
5. El instrumento encuentra tanto éxito como una falla interpretable; no está construido para
   fabricar fracaso universal.

## Límites que impiden venderlo como resultado publicable todavía

- cuatro donantes, dos modelos y una sola estructura de mundo;
- checkpoint condicionado a que exista la creencia objetivo;
- actualizador de referencia congelado pero no posterior normativo único;
- el umbral estructural necesita análisis de sensibilidad;
- no probamos todavía evidencia mezclada, timing tardío, compromiso fuerte ni fricción de
  retrabajo real;
- ninguna estimación de prevalencia ni generalización fuera de esta familia.

## Veredicto y próximo paso

**GO fuerte al enfoque; STOP a más corridas exploratorias.** La dirección es publicable en
potencia porque identifica revisión estructural natural, bilateral y cobrada en un artefacto. Lo
que sigue no es acumular anécdotas: escribir el contrato del piloto, simular potencia a nivel
donante, congelar métricas y construir una réplica en una segunda estructura de mundo.

Crudos: `technical_gpt-5.4_seed94200_eligible.json`. Scores vigentes:
`probe_gpt-5.4_seed94200_scores_v4.json`. Trayectorias estructurales conjuntas:
`probe_structure_94100_94200_v1.json`.
