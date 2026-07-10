# Codex ronda 4 — review de la desviación del gate por partición — 2026-07-10 (madrugada)

> Review de la regla del 10% que Claude tomó solo (auditoría del "una sola cabeza"): encontró acantilado explotable + bug de signo; propuso el gate por REGRET absoluto (adoptado, commit posterior a f08643c). También: 5 requisitos pre-caso-fresco y la prohibición "ningún caso legacy cuenta como yield". Crudo:

codex
## (a) Regla del 10%

Detecta un problema real, pero abre una discontinuidad explotable:

- Con `den_partición = 9.9%`, alcanza quedar cerca del ingenuo.
- Con `10.1%`, exige R≥0.95.

Un generador podría mover parámetros alrededor de esa frontera. No permite colar un canónico arbitrariamente malo —`R≥−0.05` todavía lo ata al ingenuo—, pero sí tolera casi 10% de la escala total justo debajo del corte.

Otro agujero: usan `abs(den_s)` para decidir la rama, pero R conserva el signo del denominador. Si un denominador minúsculo cambia de signo por ruido, la interpretación de R se invierte.

“No peor que el ingenuo” sostiene solamente ese claim de dominancia. No debería llamarse recuperación cercana a la verdad.

## (b) Alternativa principista

Eliminaría el umbral del 10% y usaría regret absoluto respecto de una escala estable:

```text
regret_p =
  max_seed(S_truth,p − S_canonical,p)
  / abs(S_truth,full − S_naive,full)

gate: regret_p ≤ 0.05
```

Con sus números:

- confounded nuevo: ≈0.94% → pasa;
- confounded viejo, R_obs≈−4: ≈6.7% → falla;
- reskin, R_obs≈−4: ≈4.05% → pasa por poco.

Obtienen exactamente la separación buscada sin dividir por un denominador pequeño ni introducir un cliff.

Si quieren mayor rigor futuro:

```text
regret permitido =
max(5% de escala estable, error de estimación q95 del plan legal)
```

Pero exige más de dos seeds para estimar ese error. Para v0, el regret global de 5% es suficiente y coherente con `FLOOR`.

## (c) D10

Puede quedar como deuda solo bajo una prohibición explícita:

> Ningún caso fresco que use la ruta legacy/`obs_half=false` cuenta como yield.

`R_obs≈−4` no es enorme en distancia absoluta, pero demuestra que `ALL-PASS` puede coexistir con un canónico mucho peor que el ingenuo en un régimen. Eso es peligroso para una fábrica.

Para mundos existentes, alcanza con registrar:

- `recoverability_obs: unsupported/not_gated`;
- `ALL-PASS` no implica cobertura observacional.

Si el peldaño MEDIO puede generar channel, selección u otra fuente no-identidad, D10 es bloqueante, no deuda.

## (d) Antes del caso fresco

Cinco requisitos:

1. **Resolver y congelar ahora la regla de partición.** Cambiarla después de ver el caso lo quema.

2. **Congelar el dominio admisible:** solo fuente identidad, `obs_half=true` y clase aditiva-invariante. Cualquier salida fuera de clase falla; no entra por legacy.

3. **Preregistrar el protocolo de yield:** N, prompt, modelo/version, seeds, número máximo de reparaciones, qué cuenta como fallo y cero retoque humano. Un único caso es un piloto `1/1`, no una estimación de yield.

4. **Congelar hashes:** generador, verificador `f08643c`, scorer, consigna y rangos de parámetros.

5. **Regla de quema:** si el caso exige modificar verificador, canónico o thresholds, pasa a fixture de desarrollo y jamás vuelve al numerador.

Además, guardar prompt, salida cruda y todos los intentos. El caso fresco solo es evidencia si puede fallar sin que el sistema se adapte después.
