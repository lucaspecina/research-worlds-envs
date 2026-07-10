# Codex ronda 3 — diseño del canónico legal (GPT-5.6 Sol, max) — 2026-07-10 (madrugada, turno autónomo)

> Consulta de DISEÑO previa a implementar D1 (ADR 0120). Veredicto: diseño válido como "techo predictivo legal"; cambios exigidos: gate do() explícito, allowlist positiva identitaria, unsupported≠irrecuperable, legal_plan_v0 versionado. Crudo:

codex
Veredicto: el diseño sirve como **techo predictivo legal**, no como modelo causal unificado. El mayor cambio necesario es agregar gate explícito sobre la sub-batería `do()` y distinguir “no soportado por este canónico” de “mundo no recuperable”.

## (a) Factorización por régimen

Es semánticamente válida porque el submission ve si `decision ∈ regime.config`; puede distinguir observación de intervención. El mundo mismo cambia de régimen bajo `do()`, así que ramificar no es trampa.

Pero la conclusión permitida es estrecha:

> “Existe un predictor conductual alcanzable con acceso legal.”

No:

> “El mecanismo causal completo es recuperable.”

La mitad observacional memorizada no es degenerada si el pool es una muestra legal y la evaluación usa seeds nuevos. El riesgo es que un mundo con observacional fácil y `do()` malo pase por ponderación agregada.

Cambio imprescindible:

- `R_full ≥ .95`
- `R_obs ≥ .95`
- **`R_do ≥ .95`**

Full+obs no garantiza do.

También haría la activación por allowlist positiva de fuente realmente identitaria: sin channel, selección, censura, hidden columns, transformaciones ni eventos que alteren la vista. “No channel y no selection” puede quedarse corto.

## (b) Injerto de contexto

Es un corte razonable como **clase tipada y declarada**, con estos supuestos explícitos:

- efecto aditivo en las medias;
- sin interacción `decision × context`;
- distribución observacional de decisión y marcadores invariante;
- covarianza/residuos invariantes;
- misma semántica de contexto en obs y do.

Cuando se viola, no diría “el mundo no es recuperable”. Diría:

> `unsupported_by_canonical: context invariance violated`

El fallo del estimador no demuestra imposibilidad informacional. Si la plantilla prometía esa invariancia y el mundo generado la viola, entonces sí: mundo inválido para esa plantilla y rechazo inmediato.

Conviene verificar la invariancia desde la declaración/composición del mundo, no esperar que el R agregado la descubra accidentalmente.

## (c) Plan de compras

Es legal y suficientemente razonable para v0, pero todavía es heurístico: `5×3×400` y `pool=2000` son números mágicos aunque el costo se derive de meta.

La versión principista sería:

1. Cantidad mínima de niveles según rango del diseño:

   - grado 2 → al menos 3 niveles de decisión;
   - contexto lineal → al menos 2 niveles.

2. Agregar niveles extra como chequeo de falta de ajuste, no necesariamente para fit.

3. Reservar pool según dimensionalidad/covarianza a estimar.

4. Distribuir el presupuesto restante con diseño balanceado o D-optimal, contabilizando costos fijos.

Para esta noche no lo sobreoptimizaría. Implementaría el plan actual como política explícita y versionada `legal_plan_v0`, sin llamarla genérica.

Una mejora conceptual: usar `3×2` para fit y los niveles/celdas restantes como validación interna. Si las 15 celdas entran todas al fit, solo compraron más precisión; si algunas quedan held-out, también verifican el supuesto cuadrático-aditivo.

## (d) Tests

### Imprescindibles esta noche

1. **Presupuesto inviable falla cerrado**, con costo exacto en ledger.

2. **Gate por partición:**

   - obs perfecto + do roto debe fallar;
   - do perfecto + obs roto debe fallar.

3. **Fuente no-identitaria no activa la ruta nueva.** Probar explícitamente channel/selection/hidden column; el reskin solo no alcanza.

4. **Invariancia de contexto violada → `unsupported`, nunca certificado.** Es central porque el injerto depende enteramente de ella.

5. **Seed robustness:** un seed alto y otro bajo → el mínimo gobierna.

6. **Regresión de mundos existentes**, incluyendo al menos uno source-layer real, además de `reskin_pilot_v0`.

7. **Roles/columnas permutados**, si es barato; evita otra dependencia silenciosa de orden/nombres.

### Deuda razonable

- Par formal no-identificable.
- Dos latentes.
- Proxy postratamiento.
- Clipping fuerte.
- Correlated errors.
- GMM/factor estructural.

Esos últimos pertenecen principalmente al futuro estimador latente; el canónico factorizado actual casi no usa esa semántica.

Última guardia: `confounded_gen_v0` solo puede ser fixture positivo. Después de congelar código, plan, thresholds y tests, el primer mundo fresco decide el yield.
tokens used
