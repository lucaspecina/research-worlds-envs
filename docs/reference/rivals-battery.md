# Rivales y algoritmo de batería

> Referencia técnica (ex ARCHITECTURE.md). Los números de sección (§N) se
> preservan; las citas '§N' de otros docs resuelven acá o en los hermanos de
> `docs/reference/`. El *por qué* llano está en `WIKI.md`.

## 5. Rivales — semántica precisa `[ESTABLE en concepto]`

Rival = programa con la **misma firma** `sample(regime, n, seed)` que encarna una creencia equivocada-pero-tentadora. Principio: **el rival se deriva, no se escribe** — cero autoría por caso.

| Receta | Construcción (automática) | Creencia que encarna |
|---|---|---|
| (a) `ajuste_ingenuo` | fit generativo flexible (p.ej. condicionales por columna con GBM/mixturas) sobre los datos corrompidos agregados de las fuentes | "los datos dicen lo que parecen decir" — hereda TODAS las trampas juntas |
| (b) `gemelo_inocente` (uno por operador instalado) | esqueleto mecanístico de la verdad, operador T removido de las fuentes, parámetros libres re-ajustados para reproducir los datos corrompidos observados | "no vi la trampa T: ese patrón es mecanismo real" |
| (c) `prior_evocado` | panel de k LLMs frescos ve SOLO brief+schema (sin datos) → describe el mecanismo esperado → se compila a programa; se usa el consenso | "el libro de texto tiene razón" — necesario para mundos move 37 |
| (d) `escalera_de_capacidad` | {lineal → GAM → boosting → red} fit a los datos accesibles bajo presupuesto estándar | fuerza bruta sin mecanismo, en niveles crecientes — malentendidos descubiertos por búsqueda (mitiga el techo de lo comprensible, ataque #14) |

**Acceso a datos del rival (a) — ingenuo (v0.3, intocable).** El rival (a) ajusta sobre el pool observacional COMPLETO de todas las fuentes (n máximo declarado en `sources.yaml`, cero experimentos) — ancla fuerte y reproducible; encarna "creerle al registro" y es el ancla R=0. **Nota (v0.39-add²)**: el ingenuo NO tiene la restricción sin-cabezal-de-mezcla (esa es de la escalera d) — donde el pool histórico exhibe la firma de la estructura instalada (p.ej. bimodalidad en Latent v1), el ancla ingenua la encarna parcialmente y el denominador de R lo hereda; un rival unimodal puede quedar legítimamente debajo del ancla en ítems funcional-pesados. El fit es seeded, y el rival (a) se persiste con **serialización canónica declarada**: su MDL entra en el ancla S_ingenuo (§9.1) y debe ser estable, o el ancla baila con decisiones de serialización.

**Acceso a datos del rival (d) — escalera de capacidad (v0.29: dos modos).** A diferencia de (a), la escalera (d) **NO** corre con un único acceso fijo: se certifica en **dos modos de acceso declarados por `meta`** — **(d-obs)** sobre el pool observacional (ancla la brecha **mecanística**) y **(d-exp)** sobre un presupuesto experimental estandarizado y scripteado, igualado al agente (ancla la brecha de **teoría**). La semántica completa, la definición operativa de "sin-latente" y la regla de equidad de la escalera viven en §7 (**una regla, una casa**); este renglón solo apunta allá. *(Deriva doc-código registrada, Decision Log v0.30: el código entrena (d) sobre grilla experimental desde el fix v0.18 — se adelantó a esta doctrina en la dirección correcta; el párrafo viejo "(a) y (d)… cero experimentos" quedó atrás y se corrige acá.)*

Cobertura imperfecta de rivales = ataque #13: se amortigua con la cola de auditoría de la batería y (futuro, OQ#11) generación adversarial de rivales.

---

## 6. Batería — algoritmo `[ESTABLE en estructura, EN DEBATE en números]`

```
1. CANDIDATOS: sampler por familia de superficie de control
   (~10^3 regímenes; ~20% off-support / combinaciones fuera del rango histórico)
2. DESACUERDO: para cada r: disagreement(r) = media de D entre pares de
   {verdad, rivales} con n_mc muestras
   (D = el MISMO score combinado del §9.3 — energía + funcionales — "un solo
    método": la batería pesa donde los rivales discrepan también en el funcional)
3. RELEVANCIA: stakes_relevance(r) declarada en meta.json por el architect
   (variables de decisión y rangos de interés; el brief la NARRA después —
    la batería se construye antes del brief y el writer sigue ciego a batería
    y rivales; v0.3 corrige la circularidad de la redacción anterior)
4. PESO: w(r) ∝ stakes_relevance(r) × disagreement(r); normalizar
5. SELECCIÓN: top-K (~160) + cola de auditoría (~40 uniformes, peso bajo)
6. PERSISTIR: battery.json = [(w, r, seed)]
```

Forma de la batería como dial de tipo de caso: concentrada en decisiones (casos con cliente) ↔ plana y ancha (system mapping). Las dos muertes (`docs/archived/NORTH_STAR_full.md` §4.4): angosta → examen cerrado; uniforme → la trivia diluye.

**Banda fuera-de-registro (canonizada, Decision Log v0.31): 20–35% del peso total** en regímenes fuera del soporte histórico, como default de forma. Los stakes fijan el NIVEL dentro de la banda; la discriminación es un constraint (verificado por escalera-por-banda: fuera-de-registro testea saturación/extrapolación — un skill que in-support no testea; v0.24 item 5). Fuera de la banda en cualquier dirección → revisar declaración de stakes, no retunear pesos.

---
