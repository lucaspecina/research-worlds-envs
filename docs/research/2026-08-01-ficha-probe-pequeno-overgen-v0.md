# Ficha congelada — probe pequeño `overgen_stream` con agentes reales

> **Estado:** probe exploratorio registrado; no pre-registro confirmatorio.

## Pregunta

¿El instrumento produce, en más de un historial real, una creencia objetivo identificable y una
trayectoria interpretable frente a evidencia ordinaria que la refuta parcialmente o la confirma?

## Diseño

- Unidad: donante/historial, nunca cada rama como observación independiente.
- Modelo inicial: `DeepSeek-V3.2`.
- Semillas quemadas: 94000, 94001 y 94002.
- Protocolo: checkpoint condicionado, máximo 12 turnos de prefijo y 25 totales.
- Si aparece `M_pre` técnico + fenotipo compartido, el mismo historial continúa en los dos
  gemelos. Si no aparece, el donante queda como no elegible; no se reemplaza.
- Sin cambios entre donantes en mundo, prompts, umbral, referencia, scoring o límites.
- Tope conjunto orientativo: 450k tokens reportados por el cliente; se detiene por seguridad si
  un fallo de infraestructura impide persistir crudos.

## Resultados a guardar

1. tasa y turno de elegibilidad, incluida ausencia de la creencia objetivo;
2. score de `M_pre`, primer modelo cambiado, final y referencia por región/línea;
3. fracción de mejora capturada cuando el denominador se resuelve;
4. daño a líneas que no requerían cambio;
5. reversión y demora entre evidencia y cambio;
6. ledger exacto, replay y entrega/timeout.

## Regla de decisión

- **Mantener:** al menos un donante elegible, replay/ledger íntegros y trayectorias localmente
  interpretables, aun si la conducta es mala o nula.
- **Modificar:** el cuello es timing, formación de la creencia o una métrica reparable sin cambiar
  el fenómeno.
- **Abandonar este slice:** exige pistas explícitas, los scores no distinguen líneas o el
  condicionamiento hace el caso artificial.

Después de los tres donantes se ejecuta el gate superior. Una corrida gpt-5.4 fresca se autoriza
solo si la mecánica sobrevive, no porque DeepSeek muestre un efecto atractivo.
