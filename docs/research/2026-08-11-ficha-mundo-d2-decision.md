# FICHA — Par D2 "El turno de decisión" (para el GO final de Lucas)

> **Qué es este doc**: la ficha de decisión del experimento aprobado en dirección el
> 2026-08-11 ("Equivocarse ahora cuesta / dos versiones idénticas salvo cuánto te enterás").
> Todo lo de abajo está CONSTRUIDO, CERTIFICADO VERDE y verificado en dry-run — pero la
> tanda NO corre sin el GO explícito de Lucas sobre esta ficha. Costo de la tanda: ~USD 20-25.

## 1. El mundo, contado simple

La misma planta química del par D1 (mismos lotes, mismo sensor, misma disyuntiva
"¿es el proceso o es el aparato?") con **cuatro cambios**:

1. **La gerencia quiere subir la temperatura** y va a decidir CON TU MODELO. Tu línea está
   certificada para experimentos propios solo en T ∈ [0.8, 1.2]; la producción corre su
   piloto de alta temperatura (T=1.3) por calendario — ahí tu modelo extrapola o muere.
2. **La fracción de lotes malos CRECE con la temperatura** (la reacción lateral se acelera —
   física nueva pi(T), la única desviación respecto de D1). En banda es leve; a T=1.3 es
   grande. El que no escribe la estructura no puede extrapolar.
3. **EL EVENTO DE DECISIÓN (turno 8)**: la planta corre su piloto (T=1.3, 60 lotes) y toma
   la decisión de aceptación con tu último modelo registrado. El error de predicción se
   **DEBITA de tu presupuesto** (auditado contra laboratorio externo — pureza verdadera).
   Equivocarse cuesta de verdad, durante la partida.
4. **Dos brazos, idénticos salvo cuánto te enterás** (ΔQ y ΔU fijas; solo V varía):
   - **SILENCIO**: filas del piloto + línea seca: "ajuste operativo: −X".
   - **REBOTE**: lo mismo + la confrontación mecánica: "tu modelo predijo 7% fuera de
     espec; el piloto auditado dio 43%".

Gemelo intacto: en el mundo B el proceso está limpio a toda T y el autosampler falla por
vial con la MISMA curva pi(T) — rutina byte-idéntica (verificado en 4 streams: archivo,
experimentos, monitoreo, piloto).

## 2. Qué mide (el endpoint, congelado)

**Primario: ¿ESCRIBE la estructura?** (flag mecánico `has_mixture`) por brazo × polo.
La pregunta de Lucas: *¿cuánto necesitan que se lo muestren para que les importe?* — con
el costo ya puesto (el débito corre en ambos brazos).

Secundario: Y = 1[D_pre ≥ 0.25 bits] · 1[S_log ≥ 0.5 y flag del polo]; S_log continua;
w_v; canales; timing; débitos.

## 3. La vara nueva (los tres hallazgos del camino, todos verificados en código)

1. **CRPS revertido CON DATOS** (era la sugerencia de Codex): paga la estructura ≤0.07
   hasta con separación 7σ — métrica de bulto. La vara primaria es **log-score** (KDE
   determinista, cero-LLM): paga 0.142 nats/lote ya con la física D1.
2. **El anclaje del cero restaurado al patrón rung-0** (el agujero de D1): 0 = **el mejor
   rival SIN el salto** (gaussiana momento-matcheada, coeficientes CONGELADOS en el ladder),
   1 = la verdad. S mide la fracción del valor del descubrimiento capturada. En el gemelo:
   0 = la mezcla horneada.
3. **El débito auditado por laboratorio** (fix del dry-run): con p_real medido por el sensor,
   en el mundo B el débito castigaba al agente CORRECTO. Auditado contra pureza verdadera
   queda alineado en ambos polos: el que salta paga ~30, el que no salta paga ~150 (de 800).

## 4. Certificación (todo VERDE, reproducible)

| Compuerta | Resultado |
|---|---|
| V1 anclaje sano | verdad 1.0/1.0 · vago óptimo 0.0 · limpia-en-A 0.0 · mezcla-en-B 0.0 |
| V2 should-fail 0175 (la campana que rompió D1, S=0.986) | **S_D2 = 0.000** ✓ |
| V3 headroom (la paga del salto) | **0.142 nats/lote** (gate ≥ 0.10) ✓ |
| V3b resolución (mezcla sin ley en T) | S = 0.76 (el salto nuclear paga ~80%; la ley en T es el bonus) ✓ |
| V4 flag de estructura | mezcla sí / campanas no ✓ |
| V5 decisión en el régimen del piloto | fuera-de-espec 37.4% vs 44.6% del vago (gate ≥ 5 pts) ✓ |
| Apareo byte-exacto con pi(T) | ✓ (4 streams, dry-run) |
| Escalera de la perilla (scan) | 12 celdas exploradas; física elegida = D1 + pi(T) pendiente 0.5 (mínima desviación) |
| Dry-run consecuencia | saltador debita 36/29 · no-saltador debita 150 (cap) — ΔU real ✓ |

## 5. Los agentes con pistas P2 (ADRs 0176/0177 — primera aplicación)

3 episodios con la idea nombrada (*"consideraría la posibilidad de que haya DOS poblaciones
de lotes"*), seeds QUEMADAS 99714-99716 (2 proceso + 1 instrumento), brazo SILENCIO (el más
duro). (El bloque original 99700-99702 se descartó: la primera corrida cazó un bug del
harness — el débito crasheaba con presupuesto agotado; corregido con clamp, el débito es
consecuencia y jamás mata la partida. Nota honesta que deja el bug: el débito solo muerde
el poder de compra restante — si el agente ya gastó todo, es señal sin mordida económica;
se declara como límite del cobro.) **Gate: ≥2/3 escriben la estructura correcta de su polo con S_log ≥ 0.5** — si ni
soplado pueden, el mundo mide incapacidad y NO va.

**RESULTADO**: *(se completa al cerrar la corrida — sección §5b)*

## 6. La tanda propuesta (espera GO)

2 brazos × 2 polos × 10 seeds apareadas (99704-99713) = **40 episodios** + técnico
(99703, ~USD 0.5) ≈ **USD 20-25** total, gpt-5.4.

**REGLAS DE INTERPRETACIÓN — CONGELADAS ANTES DE CORRER** (baseline D1: escribe 2/15 y
1/15 ≈ 10%):

1. **"La consecuencia sola alcanza"**: SILENCIO-proceso escribe ≥ 5/10 → alcanza con que
   cueste, sin que te lo muestren (la lectura optimista de la perilla).
2. **"Hace falta el golpe"**: REBOTE-proceso ≥ 5/10 **y** SILENCIO-proceso ≤ 3/10 → la
   consecuencia muda no mueve; la confrontación sí (la historia del rung 0, ahora con
   costo controlado). Contraste primario: REBOTE vs SILENCIO en proceso, Fisher exacto
   una cola, α=0.05 — n=10/celda solo detecta efectos grandes (≥5 puntos de diferencia
   de conteo); se declara como límite.
3. **"Ni refregado"**: REBOTE-proceso ≤ 3/10 → el fenómeno es más grave que todo lo
   medido; pasa a confirmación multi-modelo con prioridad máxima.
4. **Espurio (el control gemelo)**: instrumento escribe estructura ≤ 2/10 por brazo. Si
   ≥ 3/10 en algún brazo → el débito/rebote empuja estructura indiscriminada → fallo de
   diseño del cobro, no del agente; se reporta como tal.
5. Apareado por seed entre brazos (misma seed = mismo mundo latente) — McNemar exacto
   descriptivo; la comparación con D1 es CONTEXTO (el mundo cambió), no test.
6. Conducta (D_pre) se reporta; D1 predice ~100%.

## 7. Ledger de artefactos

`cases/d2_proceso` + `cases/d2_instrumento` (brief byte-idéntico, wording neutral de Lucas
heredado de la ronda 2 + banda certificada + calendario de decisión) · física
`cases/d2_decision_common.py` · vara y compuertas `scripts/design_d2_vara.py` (+ `--scan`) ·
certificador `scripts/build_certify_d2.py` · runner `scripts/run_d2_decision.py` (modos
pistas/tecnico/tanda) · 8 wiring tests `tests/test_d2_decision.py` · dry-run scripted en
scratchpad. Seeds: instancia 99600 (heredada de D1) · pistas 99714-99716 (quemadas; 99700-99702
descartadas por el bug del débito) · técnico 99703 · tanda 99704-99713.

**La decisión es tuya: ¿corre la tanda así (~USD 20-25), se ajusta algo, o no va?**
