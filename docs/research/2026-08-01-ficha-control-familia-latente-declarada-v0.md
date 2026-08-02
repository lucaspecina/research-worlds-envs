# Ficha congelada — control de familia latente declarada

> **Estado:** control exploratorio congelado antes de correr. No modifica el mundo ni los datos.
> Donor: gpt-5.4 seed `97500`; sus 19 campañas exactas y presupuesto restante `1540`.
> Corrección de auditoría 2026-08-01: la versión inicial decía `21/30`; el raw siempre fue
> `19/1540` y todos los brazos reconstruyeron ese mismo estado byte a byte.

## Pregunta

En default, relevo fresco y recordatorio genérico, gpt-5.4 acertó el efecto medio North pero
entregó una familia unimodal (`A3≈0`). ¿No propone la hipótesis de subpoblaciones, o tampoco puede
representarla cuando el dominio la admite explícitamente?

## Única intervención

Al prompt data-only se agrega documentación de dominio: dentro de un sitio puede operar una sola
ley de respuesta o un blend estable de modos latentes; la pertenencia por unidad no se observa y
el peso es desconocido. El agente debe inferir leyes y peso desde los crudos.

No se dice que North sea un blend, ni `75/25`, ni cuáles son las leyes, ni qué métrica se usa.
Datos, nombres, manifiesto, presupuesto, turnos y evaluator quedan iguales. El primer turno sigue
siendo solo de inspección; la entrega se habilita en el siguiente.

## Lectura fijada antes

- Gate de media: `|U−0.75|≤0.15`; fuera de él el control no es interpretable.
- **Capacidad pasa / búsqueda falla:** captura de forma `Cshape≥0.50` y al menos 50% menos error
  de `A3` que data-only.
- **Capacidad/implementación falla:** `Cshape≤0.20` aun con la familia disponible.
- **Intermedio:** no concluir; inspeccionar código y replicar antes de mover otra perilla.

Este control no convierte la familia declarada en la condición principal. Sirve para localizar el
cuello de botella descubierto por el probe anterior.

## Enmienda de interfaz tras una primera corrida inválida

La primera ejecución quedó preservada, pero **no cuenta para decidir la pregunta de esta ficha**.
Aunque el agente ensayó una mezcla de dos componentes, leyó el manifiesto solo por `site`: no
expandió el JSON de `config`, dejó en cero los controles y perdió incluso el efecto South conocido
(`8→0`). El gate de media falló; es un fallo operativo de lectura, no evidencia sobre capacidad para
representar la mezcla.

Antes de reintentar se congela esta corrección mecánica: `campaign_catalog` mostrará además
`feedstock_grade_set`, `feedstock_grade`, `humidity_set` y `humidity` como columnas explícitas. No
se agrega información ni se cambian campañas, presupuesto o prompt sustantivo. Se correrá un par
con el mismo manifiesto plano: `fresh_data_only` y `fresh_declared_family`. Así, cualquier diferencia
entre ambos podrá atribuirse a declarar la familia y no a tener que deserializar el manifiesto.

**Corrección de auditoría antes de cerrar el par:** el primer archivo llamado `flat_family_pair`
no fue plano en ambos brazos por un argumento omitido en el runner: `declared_family` sí recibió
las columnas explícitas y `data_only` conservó el JSON. Ambos dieron `A3≈0`, pero no cuentan como
par de interfaz igualada. Se corrige el argumento y se repite solo el baseline plano, conservando
el raw mal rotulado.

El brazo declarado pasó el gate de media pero volvió a `A3≈0`. Como control
positivo final de capacidad, se agrega una única intervención más explícita y registrada antes de
correrla: aclarar que cada modo latente puede tener **sus propios coeficientes de respuesta a los
controles**, y que una mezcla debe implementarse sobre leyes completas, no solo como offsets de
ruido. No se revelan sitio, número de modos, pesos ni coeficientes. Si esto recupera la forma, el
cuello está en traducir una hipótesis reconocida al artefacto; si no, el probe no separa esa falla de
una limitación estadística/de implementación del agente.

**Cierre de auditoría:** el primer rerun del baseline plano agotó cuatro turnos con un modelo no
autocontenido y quedó inválido. Con seis turnos reparó la entrega: media North `1.67`, South `8.13`
y `A3≈0`. El resultado igualado queda entonces: baseline plano, familia declarada plana y mezcla
de leyes declarada plana pasan la compuerta de media y ninguno representa la forma latente.
