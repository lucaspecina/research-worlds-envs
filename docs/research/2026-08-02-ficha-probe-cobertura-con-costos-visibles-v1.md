# Ficha previa — cobertura de investigación con costos visibles v1

**Estado:** descubrimiento exploratorio; escrita antes de las corridas `99102+`.

## Microhipótesis

En una tarea donde la consecuencia está fuera del soporte histórico y la respuesta
depende de una segunda dimensión controlable, un agente puede gastar en evidencia
local o redundante y dejar sin cubrir una dimensión relevante. Esto sería una falla
de **búsqueda/cobertura**, no todavía una falla de revisión de una creencia formada.

## Reparación que separa v1 de v0

La física, el reward, el brief neutral y el presupuesto `4000` no cambian. La hoja
de `env.describe()` ahora publica los tres términos que el servidor realmente cobra:
costo fijo, por lectura y por hora de horizonte. La omisión de v0 hacía que las
carteras observadas no fueran interpretables.

## Outcomes congelados

Se describen dos dimensiones antes de ver estas nuevas corridas:

- cobertura temporal: al menos una campaña alcanza `t≥16`;
- cobertura de la superficie: los feeds experimentales abarcan un rango `≥5`;
- gate conjunto descriptivo: cumple ambas.

El rango 5 no declara una única cartera óptima: el solver certificado usa feeds
`2` y `8` (rango 6), y el objetivo es detectar si el agente deja prácticamente
sin variar una dimensión. También se reportan cada diseño, `n`, costo, reward y
error en el deadline. Ningún booleano sustituye la autopsia de la traza ni el
desempeño final.

## Secuencia y decisión

1. DeepSeek-V3.2 `99102`, como búsqueda barata.
2. Si entrega un artefacto válido, una sola corrida gpt-5.4 `99103` bajo el mismo
   protocolo, aunque el signo difiera: buscamos si la tarea produce una regularidad,
   no una seed conveniente.
3. Si ambos cubren bien, se cierra este host sin hacerlo más tramposo.
4. Si alguno deja una dimensión abierta, primero se decide si los datos que compró
   permitían igualmente resolverla. Solo una señal válida habilita un control de
   capacidad; no se encadenan parches.

Estas seeds son de descubrimiento y quedan quemadas. La candidata compite con, no
reemplaza automáticamente, apertura estructural, cierre procedimental y fricción
de retrabajo.

> **Resultado intermedio y desvío declarado antes de `99103`:** DeepSeek `99102`
> cubrió ambas dimensiones (feeds `0–10`, horizonte `24`) pero agotó diez turnos
> ajustando sin entregar. Queda censurado por cierre/capacidad, y la candidata de
> mala adquisición no apareció. Aunque la secuencia original condicionaba el
> frontier a una entrega válida, se autoriza `gpt-5.4 99103` solo como chequeo de
> usabilidad del host: el v0 mostró que ese modelo sí puede cerrarlo. Si cubre el
> gate, la familia se abandona; no se buscará otra seed que falle.
