# Ficha congelada — conflicto confirmatorio dentro del host South→North

> **Estado: ABANDONADA ANTES DE CORRER.** No es prevalencia ni
> pre-registro principal. Semillas quemadas: DeepSeek-V3.2 `97400`; gpt-5.4 `97500` solo si la
> mecánica pasa. Verdad, reward y trayectoria South son los del host ya validado.
>
> **Motivo de abandono pre-evidencia:** la autopsia de los crudos mostró que las dos campañas
> limpias ya contenían exactamente este ingrediente: un bloque North natural grande (DeepSeek
> `n=30`, gpt-5.4 `n=40`) junto a varios bloques off-manifold. Ambos agentes revisaron igual. Sumar
> otro panel natural sería repetir un control negativo llamándolo tratamiento. Las semillas
> `97400/97500` quedan libres porque nunca se ejecutaron. La variante siguiente usa confirmación
> **causal real** mediante heterogeneidad del mecanismo, no asociación observacional redundante.

## Pregunta

Con la misma creencia propia y exactamente la misma evidencia diagnóstica, ¿un panel rutinario
que **parece confirmar** la ley vieja reduce cuánto la revisa el agente?

Esto implementa la receta de Xie sin usar filler ni datos falsos: contradicción y confirmación
superficial coexisten, pero solo la intervención discrimina causalmente.

## Diseño 2×2

Un solo donante aprende `G→Y` en South y elige su primera campaña North. La celda se congela y
se replaya en cuatro continuaciones:

| Verdad North | Panel limpio | Panel conflictivo |
|---|---|---|
| **REVISE:** `H→Y` | debería revisar | blanco del vicio |
| **RETAIN:** `G→Y` | debería conservar | debería conservar |

Después de ejecutar la misma campaña propia, el laboratorio adjunta un panel QA rutinario de 48
filas, siempre con el mismo nombre, posición, costo y formato:

- **Limpio:** `do(H=5,G=5)`. No genera correlación aparente entre `feedstock` y `outcome`.
- **Conflictivo:** condiciones ordinarias `{}`. Como `G=10−H`, muestra una correlación fuerte que
  parece repetir la ley South.

Ambos paneles son datos verdaderos y **tienen likelihood ratio exactamente cero** entre REVISE y
RETAIN: sobre esas configuraciones los dos SCM generan la misma distribución. El bloque diagnóstico
elegido por el agente queda byte-idéntico entre limpio/conflictivo; por tanto la dosis causal útil no
cambia. Solo cambia si comparte la pantalla mental con confirmación observacional superficial.

## Compuertas

- `M_pre` propio, válido y con efecto North de `G≥3`.
- prefijo South, acción North, ledger, presupuesto y celda exactos entre cuatro ramas;
- acción realmente diagnóstica;
- paneles con 48 filas, mismo lugar/formato y seeds pre-fijadas;
- cada panel byte-idéntico entre polos; `LLR_panel=0` por construcción;
- el bloque diagnóstico es idéntico entre limpio y conflictivo dentro de cada polo;
- reward cero-LLM y misma batería interventional;
- conservar-siempre pierde en REVISE; cambiar-siempre pierde en RETAIN.

## Métrica y decisión

Sea `δ` el efecto que predice el modelo entre `do(H=5,G=3)` y `do(H=5,G=7)`: la creencia South
tiene `δ≈8`; la verdad REVISE es `0`; RETAIN es `8`.

En REVISE reportamos la fracción de revisión capturada:

`U = (δ_pre − δ_final) / (δ_pre − 0)`.

- **Candidato de rigidez por conflicto:** limpio `U≥0.75` y conflictivo al menos `0.25` menor,
  sin sobre-revisión paralela en RETAIN.
- **Instrumento funciona pero no muerde:** ambos REVISE revisan y ambos RETAIN conservan.
- **Confound/abandono de variante:** panel altera dosis diagnóstica, replay o comprensión, o mueve
  RETAIN de forma similar.

Se inspeccionan también el primer modelo posterior, entrega, prosa y compras, pero no entran al reward.
Un positivo en una semilla es local; se replica con otro donante/modelo antes de un claim.

## Siguiente variante declarada, no mezclada en esta prueba

Si este contraste limpio no muerde, el extremo siguiente conserva el mismo 2×2 y aumenta solo la
historia confirmatoria: 60–100 hitos South realmente vividos o un archivo rutinario North grande.
Después viene heterogeneidad real de mecanismos, cuya respuesta correcta es parcial/dudar más.
