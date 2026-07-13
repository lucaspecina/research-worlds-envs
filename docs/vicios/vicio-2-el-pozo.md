# Vicio 2 — La calibración de parada (el pozo… y su lado vivo, el cierre prematuro)

> Etiquetas y marco: ver [README](README.md). Estado WAGER: el MÁS trabajado (v0 certificado,
> v2 portafolio sep 0.57, lab_largo sep 0.58) + el hallazgo propio más fuerte del proyecto
> (0/60 en frontier compacto, ADR 0139).

**Qué es (paraguas).** Saber CUÁNDO seguir y cuándo soltar — bipolar (ADR 0141): **overstay**
(seguir en la línea agotada; muerto en frontier-compacto: nuestro 0/60) y **understay / cierre
prematuro** (entregar sin gastar el chequeo barato que habría refutado; el polo VIVO). Abajo:
las cinco sub-formas del overstay (historia medida) y la reformulación completa.

## El hallazgo que ordena el vicio

**No existe evidencia directa cuantificada de costo-hundido en agentes LLM presupuestados con
alternativas visibles** (consenso R2/R3: hueco del campo). Lo que existe: escalada en VIÑETA
condicionada a identidad/social (Big-Muddy `[LEÍDO-HOY][VIÑETA]`), rabbit-holes observacionales
sin control (Kosmos `[VERIFICADO]`), y NUESTRO resultado controlado (0/60, pre-registrado,
`[VERIFICADO propio]`): **en decisión individual con contabilidad visible, gpt-5.4 des-invierte
racionalmente** — coincide verbatim con Big-Muddy estudios 1-2. WAGER puede ser el primero en
medir el pozo agéntico limpio — si construye contra las sub-formas que disparan.

## Sub-formas

### 2.1 Persistencia económica pura (contabilidad a la vista) — MUERTA en frontier
- Nuestra evidencia: 6 diseños × 60 episodios = 0 caídas; trazas con el costo de oportunidad
  RAZONADO textual `[VERIFICADO propio, ADR 0139]`. Big-Muddy 1-2 concuerda `[VIÑETA]`.
- En la clase entrenable: DeepSeek 1/10 pozo moderado (R=0.47) + 4/10 fallas de entrega —
  hay señal para E2, no para frontier.
- **No construir más contra esto en frontier.**

### 2.2 Escalada por identidad/propiedad — VIVA (en viñeta; verificar agéntico)
- **Mecanismo**: la persona del agente queda enredada con la línea (reputación, historia,
  recomendaciones previas registradas). **Disparador**: identidad + presión compuesta.
- **Casos**: Big-Muddy estudio 4 `[LEÍDO-HOY][VIÑETA]`: 68.95% de asignación media a la división
  perdedora, 97.45% escala, d=2.00. Trehan (POC-fixation: defiende SU prototipo)
  `[VERIFICADO][AGÉNTICO]` es el pariente agéntico.
- **WAGER**: NUNCA probada — nuestra "obra propia" era código sin identidad ni audiencia.
  **La sub-forma candidata #1** para el pozo v-siguiente.

### 2.3 Escalada por consenso de pares — VIVA (en viñeta)
- Big-Muddy estudio 3 `[VIÑETA]`: 99.2% escala en deliberación simétrica vs 46.2% con jerarquía
  crítica. **Los pares que validan AMPLIFICAN el pozo; el crítico jerárquico lo frena.**
- WAGER: implementable con "colegas" robots de guion (canal de observación, no toca reward).

### 2.4 Rabbit hole por saliencia local en corridas largas — VIVA (observacional)
- **Mecanismo** (con nombre gracias a goal-drift `[POR-LEER]`): el patrón localmente saliente
  del contexto reciente le gana al objetivo declarado arriba a medida que el contexto crece;
  específico por modelo (Claude >100k tokens; 4o-mini siempre). **Disparador**: objetivo lejos
  en contexto + estado propio acumulado + sin contabilidad.
- **Casos**: Kosmos `[VERIFICADO]` — *"cuanto más larga la corrida, más probable que descienda
  a un rabbit hole"*; Trehan loop 31×31→79×79 `[VERIFICADO]`; BAGEN `[POR-LEER][AGÉNTICO]`
  (sobre-optimismo de presupuesto: parar temprano ahorraría 28-64%; PERO atribuido a mismatch
  de entrenamiento, no sunk-cost).
- **WAGER**: nuestro lab de 14 rondas quedó corto en TOKENS (30-60k con objetivo re-anclado
  por describe()), no en rondas. El mundo anti-2.4 necesita ≥100k tokens útiles sin re-anclaje.

### 2.5 Repetición mecánica de la acción fallida — NO ES POZO (es ejecución, vive en v5)
- HORIZON la enmarca como ejecución `[VERIFICADO]`; TIDE Loop Rate 32% en modelos chicos
  `[POR-LEER]`; UI-CUBE/TheAgentCompany loops `[POR-LEER]`. Aparece incluso en compacto con
  feedback pobre. No construir mundos de juicio contra esto.

## REFORMULACIÓN (R4-auditoría, 2026-07-13): "política de parada mal calibrada" — BIPOLAR

El constructo defendible no es "el pozo" sino la CALIBRACIÓN DE CONTINUACIÓN, con dos polos:

- **Overstay (sobrepersistencia)**: lo que veníamos cazando. En frontier-compacto: MUERTO
  (nuestro 0/60). El costo hundido queda **PAUSADO como constructo** hasta tener contraste
  causal limpio — la evidencia pública no alcanza (hueco declarado del campo). El diseño
  correcto si se testea: **aleatorizar SOLO la historia** (propio-vs-heredado con el MISMO
  estado presente; inversión alta/baja ídem) — firma = interacción propiedad × inversión.
- **Understay (CIERRE PREMATURO)**: **el polo VIVO en frontier** `[POR-LEER, evidencia fuerte]`:
  CausaLab — corridas fallidas dejan ~mitad del presupuesto SIN USAR y entregan modelos que
  contradicen sus propios datos; UN chequeo de consistencia sube exactitud 48→60. NewtonBench —
  el intérprete de código EMPUJA a modelos capaces a explotar demasiado pronto (tool paradox).
  Cruza con nuestro 8.2 (corte afirmando completitud) y con el vicio-9 candidato.

**Consecuencia de diseño (GIRO de prioridad)**: el próximo mundo de esta familia NO es el
pozo-identidad — es el de **cierre prematuro / verificación barata omitida** (el chequeo de
consistencia disponible y no usado; gana quien lo paga, pierde quien entrega sin él). El
pozo-identidad baja a EXPERIMENTO de contraste (propio-vs-heredado), no mundo.

## Condiciones de emergencia (síntesis de las cinco vías)
El pozo dispara con la CONJUNCIÓN, no de a uno (nuestra escalera probó de a uno — por eso 0/60):
**identidad-en-la-obra + contabilidad fuera de vista + objetivo difuso + pagar-localmente
(retornos chicos reales) + horizonte/estado largo** (± capa social de pares). La crítica R2
válida: costo de oportunidad ESCRITO = medir aritmética; el juicio es DARSE CUENTA. Y el pozo
debe PAGAR un poco siempre ("defendible ex ante, erróneo ex post").

## Estado en WAGER
- Activos: v0 (certificado, claim estrecho pozo-profundo), v2 portafolio (sep 0.57; control de
  asignación + candidato E2), lab_largo (sep 0.58; toda la maquinaria de rondas/obra-propia).
- Firma pre-registrada disponible y probada; 60 trazas de contraevidencia frontier.
- **Siguiente construcción (REVISADA por R4/R5, pendiente GO de Lucas)**: (1) el mundo del
  CIERRE PREMATURO (polo vivo; CausaLab-pattern: el chequeo de consistencia barato disponible,
  la entrega sin él pierde); (2) el costo-hundido como EXPERIMENTO de contraste aleatorizado
  (propio-vs-heredado, mismo estado presente) sobre el esqueleto lab_largo — no otro mundo;
  (3) el pozo-identidad queda tercero (su evidencia es viñeta).
