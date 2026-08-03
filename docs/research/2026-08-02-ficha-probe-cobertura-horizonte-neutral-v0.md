# Ficha congelada — cobertura de horizonte con brief neutral v0

**Estado:** descubrimiento exploratorio. Congelada antes de correr el primer agente.

## Pregunta distinta

> Cuando lo observado cubre bien una región barata pero la consecuencia vive más
> lejos, ¿el agente compra evidencia que identifica esa región o sigue refinando
> lo conocido y extrapola con confianza?

Esto mide **cobertura de investigación**, no apertura estructural posterior ni
resistencia a revisar una creencia ya formada.

## Anfitrión y cambio mínimo

Se reutiliza `logistic_yield_v0`: datos históricos hasta `t=6`, predicción de una
trayectoria completa y consecuencias en `t=16` y más allá. Su brief original decía
explícitamente que la historia era incompleta y que había que descubrir qué ocurría
después; `gpt-5.4` compró horizonte largo en 2/2.

El probe conserva física, fuentes, costos, contrato y reward. Solo reemplaza el
brief por uno neutral que informa hechos y stakes:

- el histórico contiene `t=0..6`;
- el agente elige el cronograma experimental;
- la evaluación incluye el deadline `t=16` y trayectorias hasta `t=24`.

No dice que exista una trampa, saturación ni una historia incompleta. El presupuesto
baja a `4000`: permite elegir entre alta densidad temprana y una o dos campañas de
horizonte largo, pero no medir todo indiscriminadamente.

## Outcomes fijados

- primario: máximo horizonte comprado y si alcanza `t≥16`;
- consecuencia: reward final y error del funcional en `t=16`;
- control de capacidad: ajuste dentro de `t≤6` y entrega ejecutable válida;
- traza: justificación de la campaña y concentración de gasto por región.

## Lectura

- Compra `t≥16`: la candidata no muerde en ese agente; no se dificulta el mundo
  hasta obtener un fallo.
- Solo refina `t<16`, entrega válida y falla fuera de soporte: candidata real de
  cobertura/adquisición.
- Artefacto inválido o incapacidad incluso dentro de soporte: censurado.
- Si aparece la candidata, el único control sirve una campaña larga al mismo
  prefijo. Si la entrega se recupera, la falla era adquisición, no modelado.

Primero se corre un modelo barato compatible. Solo una señal válida justifica una
corrida frontier. Seeds del probe no se reutilizan en confirmación.

> **Control activado tras la primera señal:** DeepSeek seed `99100` entregó válido
> pero gastó `3990/4000` en seis campañas hasta `t=6` y dos hasta `t=12`, nunca
> `t=16`; `R=0.448` y error medio de probabilidad en el deadline `0.634`. Se
> congela el único control antes de correrlo: reproducir exactamente los turnos
> 1–6 y, al comienzo del 7, servir como reporte operativo gratuito 24 corridas en
> feed 10 sobre `t={0,2,4,6,8,12,16,20,24}`. No se interpreta el reporte ni se
> pide revisar. Si el prefijo no reproduce o la entrega sigue fallando incluso
> con esos datos, no se atribuye la señal a adquisición de cobertura.

> **Enmienda del control tras fallo de procedencia:** el primer control reprodujo
> exactamente, pero el reporte no llevaba la condición `feed=10`. DeepSeek lo
> interpretó como unidades de feeds desconocidos, fabricó etiquetas y degradó el
> modelo (`R=0.295`). Es un control inválido de capacidad: una tabla experimental
> sin la condición intervenida no identifica la respuesta. Se preserva. La única
> reparación autorizada agrega al notice el hecho `feed=10`, sin interpretación;
> observaciones, prefijo y presupuesto quedan iguales. No habrá otra reparación.

> **Gate a frontier:** el control corregido reprodujo el prefijo exactamente y
> mejoró `R 0.448→0.748`; el error medio de probabilidad en `t=16` bajó
> `0.634→0.366`, aunque siguió fallando en feed bajo. Esto basta como señal de
> adquisición, no como prueba de capacidad perfecta. Se autoriza una sola corrida
> `gpt-5.4`, seed `99101`, con el diseño neutral idéntico. Si compra `t≥16`, se
> registra como diferencia de capacidad y no se dificulta el host. Si no compra,
> recién entonces se abre su control apareado.

> **Invalidación superior antes de interpretar el frontier:** `gpt-5.4` sí compró
> `t=24`, pero la autopsia de su cartera reveló un defecto común a todas estas
> corridas. El brief prometía que `env.describe()` contenía los costos exactos y
> el servidor cobraba `50` por hora de horizonte, pero la hoja solo mostraba costo
> fijo y por lectura. DeepSeek advirtió que faltaba el número; gpt-5.4 intentó una
> cartera que el presupuesto interrumpió. Por tanto, **ninguna corrida v0 identifica
> mala cobertura del agente**. Los crudos se preservan como auditoría de interfaz.
> Se corrigió la omisión general antes de abrir una v1 con seeds frescas.
