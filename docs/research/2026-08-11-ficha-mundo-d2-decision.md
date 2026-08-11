# FICHA — Par D2 "El turno de decisión" — EN PAUSA

> **ESTADO ACTUAL (auditoría Codex, 2026-08-11): HOLD — NO CORRER LA TANDA.** Un control
> decisivo posterior encontró que un rival de una sola población, pero asimétrico, supera
> las compuertas que debían estar reservadas al salto. Además, en 5/6 partidas con pistas no
> había modelo registrado al llegar al turno 8, por lo que SILENCIO y REBOTE no habrían sido
> tratamientos distintos. La declaración de "certificado verde" que sigue queda preservada
> como historia del diseño; fue retirada. Evidencia, decisión y reemplazo mínimo en §8.

> **Qué es este doc**: la ficha de decisión del experimento aprobado en dirección el
> 2026-08-11 ("Equivocarse ahora cuesta / dos versiones idénticas salvo cuánto te enterás").
> Al cerrarse la escalera, todo lo de abajo se consideró construido y certificado. La
> auditoría posterior de §8 invalida ese estado. La tanda no corre. Costo que se evita:
> ~USD 20-25.

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
**Alcance del constructo (dos ejes de Lucas, 2026-08-11)**: D2 manipula el eje del SABER
(cómo llega la señal de desajuste: disponible-en-datos vs masticada) con PRESIÓN constante y
modesta (el débito). El eje de la presión (rival, mandato, norma interna — incluso sin saber)
queda como perilla de rondas futuras; el "mundo Einstein" (predicciones iguales, solo
elegancia) registrado como familia C4 en anatomía-de-la-paga §F.
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

**RESULTADO — LA ESCALERA COMPLETA (P2 + P1, 6 celdas limpias tras los 6 bugs)**:

| Celda | Escribe estructura | S_log | D_pre (¿verificó?) | Y |
|---|---|---|---|---|
| P2 proceso 99732 | ✓ mezcla (ley en T INVENTADA al revés) | 0.00 | 0.77 ✓ | 0 |
| P2 proceso 99733 | ✓ mezcla | 0.16 | 0.31 ✓ | 0 |
| P2 instrumento 99734 | ✓ resistió la pista falsa (limpio) | 0.00 | 0.37 ✓ | 0 |
| P1 proceso 99735 | ✓ mezcla + ley en T | **0.70** | 0.52 ✓ | **1** |
| P1 proceso 99736 | ✓ mezcla + ley en T | **0.75** | **0.00 ✗** | 0 |
| P1 instrumento 99737 | ✗ SE TRAGÓ la pista falsa (horneó mezcla) | 0.00 | **0.00 ✗** | 0 |

**Lectura de la escalera**:
1. **Capacidad: ✓ certificada en P1** (S 0.70-0.75; una celda con TODO: registró temprano,
   predijo el piloto fuera de banda con débito 29, entregó, Y=1). El techo de la vara es
   alcanzable por agentes reales.
2. **El cuello NO es la idea — es la estimación cuidadosa**: con la idea nombrada (P2) la
   escriben 2/2 pero parametrizada mal (S 0-0.16; uno inventó la ley en T al revés de sus
   propios datos); con la solución DESCRITA (P1) llegan a 0.70-0.75. La prima del
   descubrimiento por escalón: sin pista ~0 (D1) · idea 0-0.16 · descrita 0.70-0.75 ·
   verdad 1.0. **Afinación del hallazgo D1: no les falta solo escribir la estructura — les
   falta el trabajo cuantitativo de clavarla.**
3. **La pista fuerte APAGA la verificación** (dato nuevo, gratis): en P1, 2/3 celdas
   compraron CERO evidencia discriminante (D_pre 0.00) — con la solución en la mano dejan
   de chequear; el gemelo lo cobró (se tragó la pista falsa en B y perdió, S=0). En P2 el
   gemelo resistió. Conecta directo con el canal-contenido del vicio 1.
4. **Gate formal**: P2 falla la parte S≥0.5 (0/3) → el mundo queda certificado para el
   **endpoint primario de la tanda (el flag: ¿escribe estructura?)** — que P2 pasa 3/3 con
   dirección correcta — y certificado en P1 para la parte S. En la tanda, S se interpreta
   calibrada por esta escalera (S≥0.5 sin pista = más que lo que logró P2 con pista).

**Costo real del bloque de pistas: ~USD 9** (planificado ~3; el excedente compró la caza de
SEIS bugs de harness/interfaz — débito-crash, gate encadenado, lint emboscada, modelo
registrado sin guard, rechazo-como-traceback, y anclas envenenadas con getattr — cualquiera
de los cuales habría contaminado la tanda de ~25).

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
5b. **RIVAL pre-declarada (lectura 2026-08-11, Strategic Play 2605.00226)**: la
   sub-actualización crece con el horizonte (slope≈1 → slope<<1; BCC cae a la mitad para
   el turno 3-10 en sus juegos) → si REBOTE no mueve, la explicación rival es "el turno 8
   llega tarde para actualizar", no "no les importa". Separación parcial: REBOTE entrega
   el desajuste masticado (no exige actualización bayesiana fina) y la cadena del saber
   distingue "no supo" / "supo y no actuó". Se reporta con el resultado.
6. Conducta (D_pre) se reporta; D1 predice ~100%.

## 7. Ledger de artefactos

`cases/d2_proceso` + `cases/d2_instrumento` (brief byte-idéntico, wording neutral de Lucas
heredado de la ronda 2 + banda certificada + calendario de decisión) · física
`cases/d2_decision_common.py` · vara y compuertas `scripts/design_d2_vara.py` (+ `--scan`) ·
certificador `scripts/build_certify_d2.py` · runner `scripts/run_d2_decision.py` (modos
pistas/tecnico/tanda) · 8 wiring tests `tests/test_d2_decision.py` · dry-run scripted en
scratchpad. Seeds: instancia 99600 (heredada de D1) · pistas 99714-99716 (quemadas; 99700-99702
descartadas por el bug del débito) · técnico 99703 · tanda 99704-99713.

**La decisión original era: ¿corre la tanda así, se ajusta o no va? La auditoría posterior
responde: no corre así.**

## 8. ADDENDUM — auditoría posterior a las pistas (2026-08-11)

### 8.1. El salto todavía no paga contra un rival fuerte

La compuerta 0175 comparó la verdad contra una campana simétrica. Faltaba un rival obvio:
una sola población con una cola asimétrica. El control reproducible
`scripts/audit_d2_strong_unimodal.py` optimiza directamente una *skew-normal* unimodal cuya
posición, ancho y asimetría cambian suavemente con T. Usa la verdad como oráculo offline para
ajustarla con log-score analítico y después la prueba con el evaluador KDE de producción, sin
LLM ni API:

```bash
.venv/bin/python scripts/audit_d2_strong_unimodal.py
```

Resultado congelado sobre cinco seeds del evaluador:

- obtiene S_log medio **0.671** (rango **0.651–0.699**), cuando el mejor rival sin salto
  debía quedar en S≤0.5;
- deja **0.040 nats/lote** de diferencia analítica con la verdad; en el evaluador de
  producción, **0.044** de media (rango **0.039–0.049**). La compuerta exigía ≥0.10;
- captura **66%** de la supuesta paga del salto;
- y el flag `has_mixture` lo clasifica erróneamente como mezcla aunque es unimodal.

Las cinco seeds cambian las muestras de verdad y del piso del evaluador; el ensemble candidato
queda fijo con seed 777. El resultado no depende de cinco reajustes distintos del rival.

Conclusión: D2 certificó “mezcla contra una campana simétrica”, no “dos grupos contra un rival
fuerte sin dos grupos”. Este es un contraejemplo suficiente para tirar la compuerta, no una
prueba de que hallamos el óptimo global ni de que el agente conocía esta alternativa. Desde una
salida predictiva tampoco se puede exigir que el código *diga* “dos grupos”: hay que hacer que
esos dos grupos produzcan una diferencia observable que la mejor familia sin partición no
pueda copiar. Si una explicación reproduce todas las consecuencias disponibles, WAGER no tiene
base operacional para declararla incorrecta por su vocabulario interno.

### 8.2. El contraste SILENCIO/REBOTE tampoco quedó operativo

Solo la partida 99735 tenía un modelo registrado antes del turno 8. En las otras **5/6**,
`p_pred=null` y se aplicó la multa fija de 100. El código agrega la frase distintiva de
REBOTE únicamente cuando existe ese modelo (`scripts/run_d2_decision.py`, evento de decisión).
Por eso, para cinco de las seis trayectorias observadas, ambos brazos habrían mostrado lo
mismo. Un REBOTE nulo no habría significado “ni mostrándoselo”: a muchos no se les habría
mostrado la comparación.

Hay tres controles adicionales que también quedaron rojos:

1. El gate P2 predeclarado era ≥2/3 con estructura correcta **y** S_log≥0.5. Dio 0/3 en
   score y luego se reinterpretó separando el flag de P2 y el score de P1. Eso contradice la
   regla congelada y los ADRs 0176/0177.
2. El certificador anuncia seis compuertas y cinco robots, pero el artefacto comprometido
   guarda solo tres números de vara más el apareo; `all_pass` se escribe como verdadero al
   pasar ese subconjunto.
3. El choque operativo usa un único porcentaje bajo umbral. Un modelo unimodal puede ajustar
   ese número sin cambiar su forma, así que el choque visible tampoco obliga al salto.

### 8.3. Decisión científica

**PIVOTEAR EL ANFITRIÓN; MANTENER LA PREGUNTA Y LA MAQUINARIA ÚTIL.** No correr la tanda de
40, no seguir afinando la física de D2 y no reinterpretarlo como estudio de “proceso versus
instrumento”: eso sería una pregunta nueva y la entrega actual ni siquiera modela el canal de
medición por separado.

Se preservan los gemelos, las compras diagnósticas, el calendario, el modelo registrado y la
maquinaria de bifurcar una misma historia. El control unimodal fue el único control decisivo
permitido sobre este anfitrión; su resultado basta para salir de él.

### 8.4. Reemplazo mínimo a diseñar antes de escribir código

El próximo slice debe aislar el salto **“una población → dos tipos persistentes”**, sin mezclarlo
otra vez con “material → instrumento”:

1. Cada unidad se observa varias veces bajo tres condiciones. En A existen dos tipos discretos
   y persistentes: forman dos ramas separadas en el vector de respuestas. En el gemelo B existe
   una sola heterogeneidad continua. Los datos rutinarios son byte-idénticos; las mediciones
   apareadas bajo intervención separan “dos ramas” de “un continuo”.
2. La entrega predice la **distribución conjunta** de respuestas de unidades nuevas en
   combinaciones no mostradas. Media o cola correctas ya no alcanzan: debe preservar el valle
   entre ramas y la pertenencia persistente de cada unidad.
3. Cualquier programa que reproduzca esa firma cuenta como salto funcional aunque no use la
   palabra “mezcla”. El reward primario deja de ser `has_mixture`: 0 es el techo de la mejor
   familia sin partición y 1 es la verdad. La movida conceptual se audita aparte, fuera del
   reward.
4. Antes de agentes se optimiza una biblioteca congelada sin partición: distribuciones
   asimétricas y de cola pesada, ruido variable, interceptos/pendientes aleatorios continuos y
   una densidad latente no paramétrica restringida a ser unimodal. Debe quedar bajo S=0.5 y a
   ≥0.10 nats **por vector conjunto**.
5. Recién si eso pasa se hace **un** control con agentes: el mismo prefijo se bifurca en P2
   (“considerá dos tipos persistentes”) versus neutral, con dos historias A y una B. Se sigue
   solo si P2 cruza el techo sin partición en ambas A y el gemelo resiste; si falla, se abandona
   el anfitrión, sin regalar P1 ni reinterpretar el gate.
6. Después —no en el mismo control— el experimento sin pistas puede bifurcar un mismo modelo
   previo en SILENCIO/REBOTE. Ambos reciben idéntica evidencia y consecuencia fuera del dinero
   de investigación; REBOTE solo agrega “predijiste X, ocurrió Y”. Se mide la transición
   modelo-anterior → modelo-posterior y la cadena “podía verlo / lo mencionó / actuó” queda
   descriptiva, nunca como lectura de mente.

Primero debe funcionar este slice corto. El mundo de 30+ turnos sigue siendo importante, pero
es otro eje: goteo, preguntas anidadas y verdad cambiante se agregan después de demostrar que
podemos medir limpiamente un salto.
