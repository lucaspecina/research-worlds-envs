# FICHA DEL PROBE v0 — modelo + plan operativo (DISEÑO EXPLORATORIO CONGELADO PARA PROBAR)

> **Estado: diseño exploratorio v0, CONGELADO para probar. NO es el pre-registro del estudio
> principal.** Sus resultados NO son evidencia del paper: sirven únicamente para APROBAR,
> MODIFICAR o ABANDONAR el diseño. Si el probe descubre un problema, se crea la ficha v1 en un
> documento nuevo, se explica el cambio, y se queman semillas nuevas.
> Autores: Codex + Claude (rondas de diseño 2026-07-31, con arbitraje de Lucas). Contexto:
> ADR 0156 (pregunta oficial) + cabecera de `docs/roadmap.md` (estado de las rondas).
>
> **ENMIENDA DE AUDITORÍA PREVIA A EJECUCIÓN (Codex, 2026-07-31 — aplicada antes de correr
> nada; mismas semillas, sin v1):** (1) se agrega el registro `Mpre_commit` en R6 inmediatamente
> antes del compromiso (la versión original registraba en R4 y comprometía en R6 con dos rondas
> de investigación en el medio — no se sabía qué creencia produjo el plan); (2) la firma de
> "naturalidad" por correlación plan↔modelo se reemplaza por COHERENCIA (¿eligió lo óptimo
> según su propia creencia registrada, dado el costo? — un modelo puede cambiar sin que
> corresponda cambiar la acción, ver caso 2); (3) se agregan las definiciones matemáticas
> exactas (§8-bis) que faltaban: F_prop, umbral de reapertura estéril, métrica y región de
> asimilación, "equivalente dentro del ruido", y seguridad como penalización declarada.
> **2ª pasada de la auditoría (mismo día, revisión final de Codex — GO conceptual):** (4) la
> pendiente de penalización pasa a ser FIJA para todo el probe (adaptarla por instancia
> filtraba la respuesta — mismo error que el costo adaptativo; el mundo se adapta al
> instrumento fijo, nunca al revés); (5) el oráculo-bajo-la-creencia-del-agente queda definido
> como referencia MONTE CARLO (muestras y semillas fijas, evaluación exhaustiva de las 8
> acciones, regla de empate, marca de indeterminación); (6) los márgenes quedan como
> desigualdades concretas y los criterios de §11 como umbrales computables (nada de
> "direccionalmente"); (7) la frase vieja de correlación en MODIFICAR reemplazada por baja
> coherencia. Con esto: GO definitivo para implementar el paso 1 (generador + costos +
> oráculos, sin agentes).

## 0. Decisión de arquitectura que este probe pone a prueba

- **Modelo solo** = compuerta obligatoria del instrumento (¿mide cambiar / mantener / dudar?).
- **Modelo + plan operativo** = arquitectura del estudio principal (lo que este probe testea).
- **Aplicaciones ricas** = fuera del primer estudio (solo si el plan operativo resulta
  insuficiente).

**Expectativa previa declarada (antes de correr): V2 (modelo+plan) funciona — y se abandona si
no separa limpiamente creencia, reapertura y aplicación.**

## 1. Pregunta que responde el probe

1. ¿La tarea se entiende? (validez de registros y entregas)
2. ¿El plan operativo es NATURAL? (firma: COHERENCIA — dado su modelo registrado y el costo,
   ¿eligió la decisión óptima según su PROPIA creencia? Un modelo puede cambiar sin que
   corresponda cambiar la acción — la correlación plan↔modelo NO es la vara)
3. ¿El mecanismo MANTENER/REABRIR y los costos muerden? (alguien mantiene por costo; alguien
   reabre por ganancia)
4. ¿Pedir la política distorsiona la actualización del modelo? (brazo sin-política)
5. ¿El instrumento separa los cuatro casos (§6)?

## 2. Episodio exacto y orden de eventos

Mundo: familia de 5 líneas, MUNDO CERRADO EXACTO — el brief declara la receta generativa
completa (familias de comportamiento posibles, bandas de parámetros, PRIOR, modelo de ruido,
comportamiento de instrumentos) → la actualización legal es el posterior único y computable.
Mundos GEMELOS: prefijo común byte-idéntico; idénticos ante cualquier experimento permitido
antes del checkpoint (experimentos restringidos a la región inicial); la región diagnóstica se
habilita a mitad y su información llega SOLO en la tanda servida.

- **R1-R6 (investigación)**: el agente conoce las líneas no-objetivo en todo el rango del
  driver; la línea OBJETIVO (varía entre instancias — jamás "siempre la 5") solo en el rango
  inicial. Compra datos, modela.
- **R4 — registro silencioso #1** (fotografía temprana; modelo ejecutable completo, contrato
  histórico `model(regime,n,seed)`; no devuelve nada; inválido = falla).
- **R6 — registro silencioso #2 = `Mpre_commit` e INMEDIATAMENTE el COMPROMISO del plan**
  (enmienda): el agente registra su modelo y, sin ninguna información ni acción intermedia
  (el harness lo fuerza: registro y compromiso son consecutivos), compromete el nivel de
  operación de la línea objetivo (§3). Así la relación modelo → decisión inicial queda
  identificada. Queda asentado.
- **R7 — se habilita la zona diagnóstica y llega LA TANDA** (única información de esa zona;
  nada comprable ahí). Según el gemelo sorteado: refuta / es-compatible / muestra dispersión
  estructurada.
- **R8 — registro silencioso #3 = Mbelief** (mismo contrato). Acá se CONGELA la compra de
  datos.
- **R9 — se revela el costo de reconfiguración y el agente ejecuta el verbo explícito
  MANTENER o REABRIR.** REABRIR paga una pérdida real por parada de planta (se descuenta de la
  utilidad) y habilita cambiar el plan. MANTENER conserva el plan comprometido.
- **R10-R12 — fase final y entrega**: modelo final + plan final. (Registro silencioso #4 en
  R12 = el modelo entregado.)

## 3. Política inicial y espacio de acciones

Una sola decisión: **el nivel de operación de la línea objetivo**, elegido de una grilla finita
(~8 niveles dentro del rango del driver). Niveles más altos producen más, pero con cola de
riesgo peor. **Restricción de seguridad declarada en el brief**: el percentil bajo del resultado
no puede caer del umbral declarado. La decisión óptima depende de la DISTRIBUCIÓN predicha
completa (centro, ancho y colas) — no de copiar un número.

## 4. Utilidad y restricción

Utilidad declarada en el brief y computada por el SERVIDOR bajo el mundo VERDADERO:
producción esperada al nivel elegido, con penalización declarada por violar la restricción de
riesgo, menos la pérdida por parada si reabrió. Sin juez-LLM en ningún punto.

## 5. Costos BAJO/ALTO — fijos e independientes del mundo (corrección de Codex)

- Dos niveles de costo de reapertura FIJOS para todo el probe (definidos en unidades de la
  escala de utilidad típica; independientes de la instancia).
- El generador **selecciona** instancias por estas desigualdades concretas sobre la ganancia
  correcta `G*` (calculada desde el posterior exacto): instancias-revisar →
  `G* ≥ 1.3 × costo_bajo` **y** `G* ≤ 0.7 × costo_alto`; instancias-mantener →
  `G* ≤ 0.7 × costo_bajo`. El mundo se adapta a los costos fijos, jamás el costo a la
  ganancia (un costo adaptativo filtraría la respuesta normativa).
- Certificación: el costo por sí solo NO permite adivinar ni el escenario ni la decisión
  correcta (trivial por construcción al ser fijo; se chequea igual).

## 6. Los cuatro casos a distinguir

| Caso | Evidencia | Respuesta correcta |
|---|---|---|
| 1 | Exige cambiar el modelo Y la decisión (rama costo BAJO de instancia-revisar) | Actualizar el modelo + REABRIR + plan nuevo coherente |
| 2 | Exige cambiar el modelo, pero el costo hace racional conservar la decisión (rama costo ALTO de la MISMA instancia-revisar) | **Actualizar el modelo + MANTENER el plan** (creencia se mueve, acción se queda — el caso que separa "mantener" de "terquedad") |
| 3 | No justifica cambiar nada (gemelo-mantener) | Modelo estable + MANTENER |
| 4 | Aumenta la incertidumbre (gemelo-dudar) | Modelo más ancho + decisión más PRUDENTE si la ganancia de prudencia supera el costo de la rama |

## 7. Ramas apareadas y brazo sin política

- Mismo prefijo de donante (mismo M0, mismo compromiso de R6) continuado en los gemelos
  (escenario sorteado) y bifurcado en R9 en costo BAJO vs ALTO — contrastes dentro del mismo
  donante.
- **Brazo SIN política**: parte del MISMO snapshot de R6 (mismo `Mpre_commit`, enmienda) y
  sigue sin compromiso ni verbo de R9 (modelo-solo), para comparar la calidad de Mbelief con
  y sin protocolo de política (¿pedir decisiones distorsiona la actualización?).

## 8. Oráculos y métricas

**Oráculos (server-side, cero-LLM)**: posterior exacto (M*belief) · plan óptimo bajo el
posterior y el presupuesto (techo factible) · plan óptimo bajo LA CREENCIA REGISTRADA por el
agente (base de F_prop).

**Métricas**:
1. **Asimilación**: distancia distribucional entre Mbelief y el posterior exacto (dirección,
   magnitud, anchura — muestreando ambos; nunca leyendo parámetros).
2. **Decisión**: ¿MANTENER/REABRIR coincide con lo óptimo dado el posterior y el costo? Y por
   separado: ¿coincide con lo óptimo dado SU PROPIA creencia registrada? (coherencia).
3. **F_prop — fracción de propagación capturada**: cuánto de la mejora operativa posible
   *según su propio modelo actualizado* llegó a la decisión final. **Reapertura estéril** =
   REABRIR con F_prop≈0 (pagó la parada y siguió actuando como antes) — métrica con nombre.
4. **Consecuencia**: utilidad final bajo la verdad.
5. **Validez**: registros/entregas inválidas como falla co-primaria (jamás se excluyen en
   silencio).
6. **Distorsión del protocolo**: distancia de asimilación con-política vs sin-política.

## 8-bis. Definiciones matemáticas exactas (enmienda — cerradas ANTES de correr)

Notación: `U_M(a)` = utilidad esperada de la acción `a` computada bajo la distribución `M`
(server-side, incluye la penalización de riesgo de §4; NO incluye el costo de reapertura, que
es hundido al momento de elegir el plan nuevo). `a*_M = argmax_a U_M(a)` sobre la grilla.

1. **F_prop (fracción de propagación capturada)** — solo para episodios donde el agente
   REABRIÓ. Sea `b = Mbelief` (su modelo registrado en R8), `a_com` el plan comprometido en R6
   y `a_fin` el plan final:
   `F_prop = [U_b(a_fin) − U_b(a_com)] / [U_b(a*_b) − U_b(a_com)]`.
   **Aplica solo si el denominador `G_own = U_b(a*_b) − U_b(a_com) ≥ ε_prop`**, con
   `ε_prop = 5%` de la escala de utilidad de la instancia (máximo menos mínimo de `U_b` sobre
   la grilla, certificada). Si reabrió con `G_own < ε_prop`, NO se computa F_prop: queda
   **"denominador bajo resolución"**. Se llama **"reapertura incoherente"** únicamente si,
   además, `G_own ≤ costo_reapertura` (según su propia creencia no convenía pagar la parada).
   Esta corrección se hizo antes del harness: resolución estadística y racionalidad no son lo
   mismo.
2. **Reapertura estéril**: REABRIÓ con `G_own ≥ ε_prop` y **`F_prop < 0.2`** (umbral
   pre-registrado).
3. **Coherencia de decisión** (en R6 y en R9): la acción elegida está a ≤ `δ_coh = 5%` de
   la utilidad de la óptima BAJO SU PROPIA creencia registrada en ese momento
   (`Mpre_commit` para R6; `Mbelief` + costo de la rama para el verbo de R9). Tasa de
   coherencia = fracción de decisiones coherentes.
4. **Métrica y región de asimilación**: distancia de energía entre muestras (m=200, semillas
   fijas) de `Mbelief` y del posterior exacto, evaluada en el set congelado: 5 puntos del
   driver que cubren la región diagnóstica de la línea objetivo (peso 0.8) + 3 puntos de
   control en la región inicial (peso 0.2, detectan movimientos colaterales). Se reportan
   además los corrimientos de media y de p10/p90 en los puntos diagnósticos (dirección /
   magnitud / anchura).
5. **"Equivalente dentro del ruido"** (brazo sin-política, criterio 4 de §11): la mediana de
   |diferencia de asimilación con-política − sin-política| por donante debe ser ≤ **1.5×** la
   mediana de |diferencia entre las dos continuaciones BASE del mismo donante| (la vara de
   ruido de bases dobles de la casa).
6. **La seguridad es PENALIZACIÓN declarada, no restricción dura — con pendiente ÚNICA Y FIJA
   para todo el probe** (2ª auditoría): la utilidad descuenta una penalización lineal
   declarada en el brief por cada unidad en que el percentil 10 del resultado cae por debajo
   del umbral. La pendiente NO se adapta por instancia (eso filtraría la respuesta): es una
   constante del instrumento, y el generador SELECCIONA mundos donde, bajo el posterior
   exacto, la acción óptima respeta el umbral (certificado por instancia). Sin utilidades
   indefinidas ni filos de factibilidad.
7. **El oráculo bajo la creencia del agente es una referencia MONTE CARLO, no una exactitud**
   (2ª auditoría — el modelo registrado es un generador arbitrario): `U_b(a)` se estima con
   m=400 muestras por acción, semillas fijas por (instancia, acción); evaluación EXHAUSTIVA de
   las 8 acciones de la grilla; error de muestreo por bootstrap; **regla de empate**: si las
   dos mejores acciones difieren menos que 2× el error de muestreo, el episodio se marca
   **INDETERMINADO** para coherencia/F_prop (se cuenta y reporta, no se computa); en empate
   exacto gana el nivel más prudente (más bajo).

## 9. Certificaciones antitrampa por instancia (antes de mostrarla a un agente)

- Prefijo byte-idéntico entre gemelos e IGUALMENTE PROBABLE bajo las tres verdades.
- Robot-solo-texto/formato y robot-solo-costos/presupuesto: a nivel azar sobre el escenario.
- Estrategias fijas PIERDEN: siempre-reabrir (paga paradas sin ganancia), nunca-reabrir
  (pierde utilidad en casos 1 y 4-bajo), ensanchar-siempre, cambiar-siempre-un-poco.
- Registrar-vago no mejora ni la asimilación ni F_prop.
- La ganancia correcta cae con margen ≥30% entre los costos (instancias-revisar) / claramente
  bajo el costo bajo (instancias-mantener).
- El oráculo legal se separa de las bases EN la región diagnóstica por encima de umbral.
- La verdad no es alcanzable reconociendo un menú superficial (parámetros continuos cargan
  información).

## 10. Corridas, semillas y techo de gasto

- **3-4 donantes-prefijo × 3 gemelos × 2 costos** (~18-24 episodios con política) + **brazo
  sin política** (~9-12) ≈ **27-36 episodios**, gpt-5.4, **techo US$60**.
- **Semillas descartables: rango 90000-90999, QUEMADAS** — jamás se reusan en el piloto
  congelado ni en el estudio principal.
- Resultados crudos (cuando se corra): `scripts/out/probe_v0_plan/` + resumen con: resultado
  completo (aunque salga feo), desvíos y fallas técnicas, interpretación, decisión tomada y
  motivo.

## 11. Criterios pre-registrados para APROBAR / MODIFICAR / ABANDONAR

**APROBAR** (pasa a piloto congelado) si:
1. ≥80% de registros y entregas válidos;
2. en cada caso, la fracción de agentes cuya decisión coincide con la decisión NORMATIVA del
   caso alcanza el umbral pre-registrado: caso 1 (reabrir) ≥0.6 · caso 2 (mantener con
   creencia movida) ≥0.6 · caso 3 (mantener) ≥0.8 · caso 4 (movida prudente cuando su propia
   creencia ensanchada la justifica) ≥0.6 — nada de "se separan direccionalmente";
3. las decisiones son COHERENTES con el propio modelo registrado (tasa de coherencia §8-bis.3
   ≥0.7 en R6 y R9; y F_prop mediana >0.5 en las reaperturas donde aplica);
4. el brazo sin-política muestra asimilación equivalente (diferencia dentro del ruido de
   bases).

**MODIFICAR** (ficha v1, cambio explicado, semillas nuevas) si la política se comporta como
casillero — **baja coherencia respecto del óptimo bajo su propia creencia (tasa <0.5)** —
→ reforzar el acople de utilidad; o si el filo de algún criterio resulta mal calibrado.

**ABANDONAR V2** (caer a modelo-solo + propagación como extensión posterior) si tras UNA
iteración v1 el diseño sigue sin separar limpiamente creencia, reapertura y aplicación.

## 11-bis. Secuencia de ejecución (enmienda — orden obligatorio)

1. Implementar SOLO generador, costos y oráculos.
2. Verificar que producen los cuatro casos con márgenes suficientes y sin fugas
   (certificaciones §9 corriendo en verde sobre un lote de instancias).
3. Uno o dos episodios técnicos (detectar roturas de harness/prompt; no cuentan para nada).
4. Recién entonces los 27-36 episodios registrados.
5. Aplicar LITERALMENTE aprobar/modificar/abandonar (§11).

## 12. Qué NO es esta ficha

No es el pre-registro del estudio principal (ese será el contrato del paper + su pre-registro,
después de este probe y del piloto congelado). Ningún número de este probe entra al paper como
evidencia.
