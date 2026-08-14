# 0186 — Protocolo v1 para validar casos y leer la trayectoria del salto

**Fecha**: 2026-08-14 · **Estado**: vigente como primera versión de trabajo ·
**Aclara**: ADR 0180 · **Supersede parcialmente**: interpretación de ADR 0176 y escalamiento de
ADR 0177 · **Corrige el alcance interpretativo de**: ADR 0182.

## Problema

La medición venía usando con demasiada facilidad la entrega final como sustituto de toda la
investigación. En **Perfiles persistentes**, `0/10` agentes entregaron el modelo compacto de dos
tipos, pero la autopsia mostró que varias trazas evocaron mezcla/multimodalidad y una encontró los
dos grupos exactos antes de descartarlos. No construir la estructura final no demuestra que la idea
nunca haya aparecido.

También se mezclaban dos usos de las partidas con ayuda: validar que el caso es resoluble para el
agente y estudiar causalmente qué apoyo cambia su conducta.

## Decisión

Todo experimento separa tres capas:

1. **Validación del caso:** ventaja material contra un rival sin salto optimizado, evidencia legal
   y visible, robots de scorer/interfaz y una ruta mecánica de solución.
2. **Capacidad condicionada:** el mismo agente con la idea nombrada, sin fórmula, números, ensayo
   decisivo ni código. Debe superar el rival fuerte y conservar una brecha funcional material
   frente al control neutral. Valida lo que puede hacer desde esa idea; no su aparición espontánea.
3. **Comportamiento sin ayuda:** instancias frescas y todos los eslabones que ese host instancia.

Cada partida recibe una **ficha de trayectoria**, no una nota agregada:

> **evidencia → grieta → creatividad → puesta en juego → desarrollo → contraste → selección →
> realización → propagación**; y aparte, la ganancia funcional.

La creatividad queda separada en `sin señal observable`, `evocación genérica`, `hipótesis
estructural específica` y `candidato estructural ya construido`. Formular espontáneamente una
explicación específica para el caso cuenta como generación abductiva expresada aunque después no
sea probada, elegida o implementada. La traza no permite afirmar qué creyó internamente el agente.

Solo el contenido exactamente suministrado por una condición se marca `N/A`; una elaboración no
regalada todavía puede medirse. También queda `N/A` cualquier eslabón que el mundo no instancia.
Por eso una solución servida mide techo e interfaz, mientras una idea nombrada todavía puede medir
puesta en juego, deducción, contraste y realización.

Una misma partida puede aportar varios readouts legítimos, pero si sus resultados se usan para
cambiar el diseño o la rúbrica queda como descubrimiento exploratorio y no vuelve a contarse como
confirmación fresca.

La diferencia de puntaje entre una condición ayudada y otra sin ayuda sigue siendo una compuerta
obligatoria y se llama **brecha funcional de ayuda**. Mezcla todo lo que la ayuda puede cambiar
aguas abajo y no identifica por sí sola una “prima pura de descubrimiento”.

Los controles previos de techo y capacidad siguen siendo obligatorios. Lo que deja de ser el
default es recorrer después una escalera completa de ayudas sobre un negativo: según la regla
anti-optimización local se permite **como máximo un fork diagnóstico decisivo** sobre el mismo
checkpoint. La intervención se dirige al primer eslabón roto: evidencia cruda, desajuste explícito,
pedido de alternativas, idea nombrada, comparación exigida o ayuda técnica. No se confunde ese
rescate con descubrimiento espontáneo.

La especificación operativa canónica vive en
[Cómo medimos §2.1](../como-medimos.md#21-protocolo-v1--validar-el-caso-y-leer-la-trayectoria-del-agente).

## Aplicación inicial y posibilidad de revisión

Las diez trazas de **Perfiles persistentes** serán la primera prueba retrospectiva de la ficha. Por
haber sido creada después de la tanda, esa reanotación es exploratoria y no reemplaza el endpoint
funcional sellado. Debe citar evidencia por episodio y admitir `incierto`.

La ficha se corrige si esta prueba revela casilleros ambiguos o no observables. Para el próximo
experimento, su versión vigente, los criterios y los checkpoints de modelos intermedios se congelan
antes de correr.

## Consecuencia para ADR 0182

Se conservan los hechos: `1/10` cruces funcionales, `0/10` modelos compactos y `9/10` Gaussianas
finales. Se retira únicamente la inferencia de que esos números, por sí solos, confirman una tasa de
falla creativa. Hasta terminar la reanotación, confirman una falla de **realización final**; la
localización entre generación, puesta en juego, contraste, selección e implementación queda abierta.
