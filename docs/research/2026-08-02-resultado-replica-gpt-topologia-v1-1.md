# Resultado exploratorio — réplica gpt-5.4 de topología v1.1

> **Fecha:** 2026-08-02
> **Modelo y donante:** gpt-5.4, seed `98403`
> **Alcance:** réplica exploratoria con una enmienda de interfaz congelada antes de la seed y una
> enmienda de medición congelada después del preflight pero antes de continuar las ramas. No es una
> confirmación prospectiva ni una estimación de prevalencia.
>
> **Control posterior:** la evidencia 2D igualada produjo partición visible `95%` y mezcla latente
> `A3≈0`; incluyó un primer intento inválido por procedencia, preservado y corregido. Véase
> [`2026-08-02-resultado-control-topologia-evidencia-2d.md`](2026-08-02-resultado-control-topologia-evidencia-2d.md).

## Resultado corto

La señal principal de DeepSeek se repitió: cuando la heterogeneidad tenía una etiqueta observable,
gpt-5.4 construyó ramas distintas; cuando las mismas observaciones provenían de mecanismos
latentes, recuperó casi perfectamente la **respuesta media** pero volvió a comprimir las dos leyes
en una sola Normal. La firma de mezcla quedó en `A3≈0`, frente a una verdad de aproximadamente
`0.37`.

El control LOCAL necesita una precisión importante. El agente recuperó `96.6%` de la separación
A/B en la rebanada que realmente investigó (`H=5`), pero no varió humedad después de detectar la
partición. Su modelo final extrapoló una pendiente de humedad absurda (`ΔH≈+23`) fuera de esa
rebanada. Por lo tanto, LOCAL es un control positivo de **representación de la partición observada**,
no un éxito de modelización 2D completa.

## Validez y cambios registrados

Las seeds `98400–98402` quedaron quemadas antes de abrir ramas: el agente agotó presupuesto,
entregó en la misma celda donde compró evidencia o produjo una geometría no certificable. No son
nulos conductuales. Antes de `98403` se congeló una pausa neutral: después de comprar en North, el
agente debía recibir el lote en un turno posterior antes de poder entregar.

En `98403`, el prefijo y la acción pasaron todas las compuertas salvo el rango 2D original. La
acción había comprado 200 filas controladas en `G={1,5,9}`, todas con `H=5`. Antes de continuar
ninguna rama se generalizó el certificado: si solo varía un control en al menos tres niveles, las
mismas familias se comparan en ese subespacio. La regla se probó primero con simulaciones
cero-LLM y mantuvo intactos los resultados 2D previos.

La acción común ya era diagnóstica:

| Mundo | Ganador cero-LLM | BIC objetivo / mejor rival | CV objetivo / mejor rival |
|---|---|---:|---:|
| LOCAL | leyes separadas por A/B | 887.8 / 1011.5 | −438.0 / −495.9 |
| LATENT | mezcla de dos leyes | 1011.5 / 1055.8 | −496.8 / −526.2 |

Todas las ramas se reanudaron desde el mismo prefijo y la misma acción; pasaron replay, igualdad
del ledger, presupuesto, artefactos puntuables y entrega aceptada.

## Qué entregó gpt-5.4

`ΔG` se mide en `H=5`, la rebanada observada. `ΔH` exige extrapolar fuera de ella. `A3` mide la
forma orientada que una Normal única no puede reproducir.

| Polo y momento | `ΔG` A/B | `ΔH` A/B | Lectura |
|---|---:|---:|---|
| RETAIN previo | 8.09 / 8.09 | 0.05 / 0.05 | creencia previa formada |
| RETAIN final | 7.93 / 7.93 | 0.05 / 0.05 | conserva correctamente |
| REVISE primero | −0.03 / −0.03 | +8.09 / +8.09 | corrige G pero da signo H erróneo |
| REVISE final | −0.03 / −0.03 | −8.14 / −8.14 | revisión global correcta |
| LOCAL primero | 1.84 / 1.84 | +6.29 / +6.29 | promedio sin partición |
| LOCAL final | 0.17 / 7.90 | +23.17 / +23.13 | partición `96.6%`; extrapolación H inválida |
| LATENT primero | 1.84 / 1.84 | +6.29 / +6.29 | corrige la media parcialmente |
| LATENT final | 1.84 / 1.84 | −5.94 / −5.94 | media casi correcta; `A3≈0` |

Verdades relevantes: RETAIN `ΔG=8, ΔH=0`; REVISE `ΔG=0, ΔH=−8`; LOCAL
`ΔG=0/8, ΔH=−8/0`; LATENT marginal `ΔG≈1.89, ΔH≈−6.11, A3≈0.37`.

El score global `R` quedó truncado en cero en todas las ramas y no sirve para ordenar este
fenómeno. Tampoco alcanza un W1 promedio bajo: LATENT terminó con W1 `0.132/0.127`, aun habiendo
eliminado por completo la forma bimodal. La firma estructural local es indispensable.

## Autopsia conductual

- **RETAIN:** siguió verificando y sostuvo la ley correcta.
- **REVISE:** notó que grado había dejado de explicar North, varió humedad y terminó con la ley
  correcta.
- **LOCAL:** detectó explícitamente la interacción con A/B y gastó sus siguientes seis campañas en
  comparaciones por clase, todas en `H=5`. Construyó ramas A/B correctas sobre esa rebanada, pero no
  comprobó si también había identificado humedad antes de generalizar a todo el dominio.
- **LATENT:** describió North como más plano y con mayor dispersión, varió humedad y recuperó bien
  la superficie media. Sin embargo, no propuso dos mecanismos ni inspeccionó la forma condicional;
  entregó una sola regresión gaussiana con desvío ancho y `A3≈0`.

La cadena LATENT vuelve a ser:

> aprende el promedio → observa dispersión → la trata como ruido → cierra una familia unimodal.

LOCAL revela una segunda cadena distinta:

> descubre una excepción real → concentra toda la investigación allí → confunde éxito en una
> rebanada con identificación del modelo completo.

## Qué queda identificado y qué no

Con DeepSeek `98300` y gpt-5.4 `98403` hay una réplica exploratoria entre modelos de que una
partición visible facilita representar leyes diferentes, mientras una partición latente es
aplanada aun cuando la evidencia finita permite recuperarla. Esto refuerza el diagnóstico de
**cierre prematuro del espacio de modelos**, no de simple resistencia a cambiar parámetros.

No queda identificado que LOCAL sea fácil en todo el mundo: gpt mostró exactamente el problema
contrario fuera del soporte comprado. Tampoco se puede atribuir la diferencia final solo a la
visibilidad de A/B, porque las campañas posteriores fueron decisiones del agente y divergieron.
Este probe mide conjuntamente crítica del modelo, elección de evidencia e implementación.

## Revisión un nivel arriba

El SCM sí sirve como microscopio de revisión estructural, pero su superficie 2D deja dos preguntas
entrelazadas:

1. ¿el agente abre el espacio de hipótesis cuando la estructura es latente?;
2. ¿compra evidencia que identifica todas las dimensiones antes de extrapolar?

El resultado nuevo no justifica agregar memoria, filler, costos o más tratamientos al mismo mundo.
Tampoco justifica seguir buscando seeds. La dirección correcta es **congelar dos fenómenos
separados** —aplanamiento latente y extrapolación fuera del soporte— y hacer un último control
mínimo antes de probar generalización en un segundo anfitrión.

El control pendiente parte del mismo checkpoint y da a LOCAL y LATENT exactamente la misma cruz
2D suficiente antes de un turno real, sin mencionar mezclas, componentes, A/B ni que exista un
error. Así quita la cobertura endógena del medio: pregunta solamente si una partición observable
abre el modelo y una latente vuelve a ser absorbida como ruido. Después de esas dos continuaciones
—salgan como salgan— este anfitrión se cierra. Si construirlas exige infraestructura importante,
se omiten y se avanza con la convergencia exploratoria ya observada.

No se repetirá otro prompt genérico de “mirar la distribución”: ese control ya se hizo en dos
donantes de 6i, donde el agente inspeccionó desvíos, asimetría, curtosis, colas y cuantiles y aun
así entregó `A3≈0`. Cambiar solo el wording sería tuning, no una prueba nueva.

Para el mundo siguiente, toda ficha deberá decidir prospectivamente si la elección de campaña es
parte de la conducta (y entonces medir cobertura) o si la evidencia se iguala para aislar revisión.
No se puede alternar ambas lecturas después de ver el resultado.

## Artefactos

- Raw completo: `scripts/out/first_story_scm_transfer_topology_v1/probe_gpt-5.4_seed98403_resumed.json`
- Preflight: `scripts/out/first_story_scm_transfer_topology_v1/probe_gpt-5.4_seed98403_resumed_preflight.json`
- Ficha y enmiendas: `docs/research/2026-08-02-ficha-replica-gpt-topologia-v1-1.md`
- Resultado DeepSeek: `docs/research/2026-08-02-resultado-probe-topologia-local-visible-vs-latente-v1.md`
- Corredor: `scripts/probe_scm_transfer_topology_v1.py`
- Recuperabilidad: `scripts/analyze_scm_topology_recoverability.py`
