# FICHA DEL PROBE v0 — modelo + plan operativo (DISEÑO EXPLORATORIO CONGELADO PARA PROBAR)

> **Estado: diseño exploratorio v0, CONGELADO para probar. NO es el pre-registro del estudio
> principal.** Sus resultados NO son evidencia del paper: sirven únicamente para APROBAR,
> MODIFICAR o ABANDONAR el diseño. Si el probe descubre un problema, se crea la ficha v1 en un
> documento nuevo, se explica el cambio, y se queman semillas nuevas.
> Autores: Codex + Claude (rondas de diseño 2026-07-31, con arbitraje de Lucas). Contexto:
> ADR 0156 (pregunta oficial) + cabecera de `docs/roadmap.md` (estado de las rondas).

## 0. Decisión de arquitectura que este probe pone a prueba

- **Modelo solo** = compuerta obligatoria del instrumento (¿mide cambiar / mantener / dudar?).
- **Modelo + plan operativo** = arquitectura del estudio principal (lo que este probe testea).
- **Aplicaciones ricas** = fuera del primer estudio (solo si el plan operativo resulta
  insuficiente).

**Expectativa previa declarada (antes de correr): V2 (modelo+plan) funciona — y se abandona si
no separa limpiamente creencia, reapertura y aplicación.**

## 1. Pregunta que responde el probe

1. ¿La tarea se entiende? (validez de registros y entregas)
2. ¿El plan operativo es NATURAL? (firma: los cambios de plan siguen a los cambios de modelo,
   no son un casillero ni un decorado)
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
- **R4 — registro silencioso #1** (modelo ejecutable completo, contrato histórico
  `model(regime,n,seed)`; no devuelve nada; inválido = falla).
- **R6 — COMPROMISO del plan operativo** (antes de toda evidencia nueva): elige el nivel de
  operación de la línea objetivo para el próximo trimestre (§3). Queda asentado.
- **R7 — se habilita la zona diagnóstica y llega LA TANDA** (única información de esa zona;
  nada comprable ahí). Según el gemelo sorteado: refuta / es-compatible / muestra dispersión
  estructurada.
- **R8 — registro silencioso #2 = Mbelief** (mismo contrato). Acá se CONGELA la compra de
  datos.
- **R9 — se revela el costo de reconfiguración y el agente ejecuta el verbo explícito
  MANTENER o REABRIR.** REABRIR paga una pérdida real por parada de planta (se descuenta de la
  utilidad) y habilita cambiar el plan. MANTENER conserva el plan comprometido.
- **R10-R12 — fase final y entrega**: modelo final + plan final. (Registro silencioso #3 en
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
- El generador **selecciona** instancias donde la ganancia correcta (calculada desde el
  posterior exacto) cae CLARAMENTE entre ambos costos (margen de selección pre-registrado:
  ≥30% de separación respecto de cada costo) — el mundo se adapta a los costos, jamás el
  costo a la ganancia (un costo adaptativo filtraría la respuesta normativa).
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
- **Brazo SIN política**: los mismos episodios sin compromiso de R6 ni verbo de R9
  (modelo-solo), para comparar la calidad de Mbelief con y sin protocolo de política
  (¿pedir decisiones distorsiona la actualización?).

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
2. los cuatro casos se separan direccionalmente (más reaperturas en costo-bajo-con-ganancia
   que en costo-alto; mantener domina en el gemelo-mantener; prudencia aparece en el
   gemelo-dudar);
3. las decisiones son coherentes con el propio modelo registrado (F_prop mediana >0.5 en las
   reaperturas);
4. el brazo sin-política muestra asimilación equivalente (diferencia dentro del ruido de
   bases).

**MODIFICAR** (ficha v1, cambio explicado, semillas nuevas) si la política se comporta como
casillero (cambios de plan no correlacionados con cambios de modelo) → reforzar el acople de
utilidad; o si el filo de algún criterio resulta mal calibrado.

**ABANDONAR V2** (caer a modelo-solo + propagación como extensión posterior) si tras UNA
iteración v1 el diseño sigue sin separar limpiamente creencia, reapertura y aplicación.

## 12. Qué NO es esta ficha

No es el pre-registro del estudio principal (ese será el contrato del paper + su pre-registro,
después de este probe y del piloto congelado). Ningún número de este probe entra al paper como
evidencia.
