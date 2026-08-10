# 0175 — El headroom se mide contra el MEJOR rival sin el salto (optimizado), jamás contra un default fijo

**Fecha**: 2026-08-10 · **Estado**: vigente · **Supersede**: la especificación de C4 en la
certificación D1 (scripts/build_certify_d1.py) y el patrón de anclas fijas como baseline de headroom.

## Decisión

1. Ningún mundo certifica sin la compuerta **"rival vago óptimo"**: se OPTIMIZA (no se elige a
   mano) el mejor modelo SIN la estructura objetivo contra la vara real del mundo, y ese rival
   debe perder materialmente (S ≤ 0.5). Si casi empata, el mundo NO paga el salto y no se corre.
2. La vara continua por defecto es de **distribución completa** (CRPS u equivalente cero-LLM):
   una familia de k parámetros no puede clavar una vara de k estadísticos — eso es un teorema,
   no un descuido, y la vara p10+sd de D1 lo violó (2 params vs 2 estadísticos).
3. La guardia llega con su par should-pass/should-fail (ADR 0057): **D1 ES el caso should-fail**
   (mejor campana afinada: S=0.986 — descubierto por Lucas el 2026-08-10, DESPUÉS de dos tandas).

## Razón

Las dos tandas D1 midieron conducta bajo una vara donde el salto pagaba 0.014 e invisible: la
atribución ("lazy", "no escriben lo que creen") quedó confundida con indiferencia racional y
hubo que bajar los claims (dossier D1, addendum 3). El costo de la compuerta es minutos; el
costo de su ausencia fueron ~USD 30 y dos rondas de interpretación contaminada. Grep de la
regla vieja: solo build_certify_d1.py implementaba C4 (s_default_en_A/s_mezcla_en_B, anclas
fijas) — queda documentado acá como mal medido; el certificador se corrige cuando el mundo
re-varado se diseñe (hoy TODO nuevo mundo está frenado esperando ese rediseño, no hay ventana
abierta).
