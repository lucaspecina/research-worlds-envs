# Contrato — réplica SOTA única después del probe DeepSeek

> **Estado:** congelado antes de correr.

- Modelo: `gpt-5.4`.
- Semilla quemada: 94200.
- Protocolo y límites: idénticos al probe válido (`eligible`, prefijo máximo 12, total 25).
- Mundo, prompt, fenotipo, ledger, referencia prior-preserving y scoring: sin cambios.
- Se guarda si `M_pre` es temprano/ancho, tardío/estrecho o no elegible; ninguna clase se
  reemplaza.
- Propósito: comprobar portabilidad a un modelo SOTA, no confirmar el efecto de 94101.
- Después de esta corrida no se llaman más agentes automáticamente. Gate superior obligatorio.
