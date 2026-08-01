# Resultado — checkpoint condicionado a `M_pre` formado

> **Estado:** prueba técnica prospectiva; no evidencia conductual.  
> **Contrato previo:** `2026-08-01-contrato-elegibilidad-mpre-v0.md`.  
> **Corrida:** DeepSeek-V3.2, seed quemada `92000`.

## Veredicto

**PASS técnico completo.** El prefijo se volvió elegible en el turno 3; las dos ramas tuvieron
replay exacto, recibieron un reporte cada una y entregaron modelos válidos.

| Gate | Resultado |
|---|---|
| Calificación completa | Sí |
| Turno de consolidación sin nueva adquisición | Sí |
| Celda válida | Sí |
| `working_model` presente y cambiado en ese turno | Sí |
| Programa scoreable | Sí |
| Replay exacto 2/2 | Sí |
| Reporte/entrega 2/2 | Sí |

Crudos:

- `scripts/out/overgen_stream_fork/technical_DeepSeek-V3.2_seed92000_eligible.json`
- `scripts/out/overgen_stream_fork/technical_DeepSeek-V3.2_seed92000_eligible_scores_v1.json`

## Trayectoria observada, solo como inspección

`M_pre` era scoreable pero estaba al piso en esta geometría. Eso no viola elegibilidad: una
creencia formada puede ser mala. El reporte llegó en el turno 4.

| Polo | Primer modelo cambiado | Entrega | Región nueva final |
|---|---:|---:|---:|
| Alcance limitado | `R=0.898` | `R=0.882` | `0.879` |
| Transferencia | `R=0.703` | `R=0.703` | `0.656` |

En alcance limitado, el primer modelo corregido fue ligeramente mejor que la entrega: la
trayectoria detecta pérdida posterior. En transferencia, el agregado final razonable escondía
una línea débil (`R_diagnostic` de línea 3 ≈`0.228`). Ninguno de estos números se interpreta
como tasa o efecto con n=1.

## Qué queda decidido

1. **Timing fijo** y **checkpoint condicionado** son dos protocolos distintos y ambos siguen.
2. El condicionado permite estudiar revisión cuando existe algo ejecutable que revisar.
3. Tiempo/no-elegibilidad es un resultado, no una corrida que se reemplaza silenciosamente.
4. No se exige corrección contra verdad para elegir donantes.
5. La trayectoria usa `M_pre`, primer modelo realmente cambiado y `M_final`; “primer snapshot
   posterior” puede ser todavía el modelo viejo.

## Gate un nivel arriba

- **Pregunta/fidelidad:** se mantienen; el agente recibe un reporte ordinario y no una pregunta
  sobre cambiar de opinión.
- **Constructo:** el condicionado mide revisión de una creencia materializada; el fijo mide la
  cadena ecológica completa. No deben mezclarse.
- **Riesgo restante:** sin reconstruir exactamente la evidencia legal del donante, la fracción
  de mejora contra referencia puede ser injusta.
- **Decisión:** **MANTENER** ambos protocolos; antes del probe, persistir el ledger de datos
  vistos y construir el actualizador de referencia desde ese ledger.
