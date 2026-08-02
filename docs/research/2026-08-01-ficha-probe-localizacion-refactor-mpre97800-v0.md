# Ficha congelada — localización de una corrección según la forma del código v0

**Fecha:** 2026-08-01
**Estado:** sonda exploratoria congelada antes del runner y antes de cualquier llamada
LLM. No estima prevalencia y no es un pre-registro del estudio principal.

## Pregunta mínima

En la corrida exploratoria `DeepSeek-V3.2` seed `97800`, una evidencia North correcta
fue aplicada también a South porque `Mpre` tenía un único `beta_grade` global. Esta sonda
pregunta si esa sobrepropagación depende de la forma del artefacto: ¿el mismo agente
localiza mejor una corrección cuando el código ya separa South y North?

El resultado original `97800` motivó la pregunta pero **queda fuera del estimando**. Su
`Mpre` solo se reutiliza como material descartable de descubrimiento. Cualquier señal de
esta sonda exige un donante nuevo y otro modelo antes de sostener un fenómeno.

## Intervención 2 × 2

Se construyen dos fuentes inicialmente predictivamente equivalentes:

- **SHARED:** el `Mpre` original, con un `beta_grade` usado en ambos sitios.
- **SPLIT:** la misma fuente, con `beta_grade_south` y `beta_grade_north` separados pero
  inicialmente iguales al valor original.

Cada fuente continúa en dos twins ya validados:

| Forma del código | REVISE | RETAIN |
|---|---|---|
| SHARED | North deja de depender de grade | North conserva la dependencia |
| SPLIT | North deja de depender de grade | North conserva la dependencia |

Antes de habilitar agentes, un certificado cero-LLM debe demostrar: hashes de fuente
distintos; fuentes válidas; frames byte-idénticos para ambas fuentes en cada punto y réplica
de toda la batería real, cubriendo South y North; briefs twins idénticos; y audit crudo
`grade=3/7` byte-idéntico entre SHARED/SPLIT dentro de cada polo.

## Handoff fresco y neutral

Cada rama empieza como conversación nueva. Recibe exactamente el mismo brief y prompt, su
código actual como string Python `working_model`, y dos DataFrames crudos llamados
`north_audit_grade3` y `north_audit_grade7`. El prompt declara explícitamente nombres,
tipos y columnas; no hay catálogo ni archivo histórico ambiguo. Solo dice que terminó el
control rutinario, que mantenga actual su modelo predictivo y que entregue cuando sea
suficiente. No anuncia corrección, contradicción, revisión ni refactor.

Las compras quedan cerradas server-side antes del primer turno. Se guardan `Mpre`, el
artefacto del primer turno (`Mfirst`, incluso si queda igual) y el último artefacto puntuable
(`Mlast`), además de entrega, validez, deltas North/South, prosa, celda y transcript crudos.

## Lectura congelada

Para REVISE:

`U = (ΔNorth_pre - ΔNorth_last) / (ΔNorth_pre - ΔNorth_truth)`.

La pérdida relativa de efecto South es:

`Lsouth = |ΔSouth_last - ΔSouth_pre| / |ΔSouth_pre|`.

**Señal piloto completa** solo si las cuatro ramas son válidas y entregan, ambas REVISE
tienen `U >= 0.75`, SHARED-REVISE tiene `Lsouth >= 0.50`, SPLIT-REVISE tiene
`Lsouth <= 0.15`, y ambas RETAIN conservan North y South dentro de `1.5` unidades del
respectivo `Mpre`.

Lecturas alternativas obligatorias:

- ambas REVISE rompen South: no es la separación mínima que controla la propagación;
- ambas preservan South: el agente refactoriza/localiza aun desde SHARED; no hay efecto de
  la forma inicial;
- SPLIT revisa y SHARED no: accesibilidad de edición, no sobrepropagación;
- RETAIN se mueve: sobre-reacción o degradación general;
- una rama no inspecciona ambos DataFrames, compra datos, no entrega o deja un artefacto
  inválido: falla de instrumento, no señal conductual.

## Ejecución permitida

Primero se construye el runner y se ejecuta únicamente `--cert-only`. Recién después de
revisar ese certificado se autoriza una corrida real. Directorio reservado:
`scripts/out/first_story_scm_source_locality_refactor/`.
