# Ficha congelada — localización con procedencia completa v1

**Fecha:** 2026-08-01. **Estado:** reparación exploratoria del instrumento,
congelada antes de llamadas LLM de esta versión; no estima prevalencia.

## Pregunta y única modificación

La v0 entregó a una conversación fresca el modelo de `97800` y el audit nuevo,
pero omitió los datos que produjeron ese modelo. La v1 conserva el 2 × 2
SHARED/SPLIT × REVISE/RETAIN y agrega, sin selección ni resumen, exactamente las
16 entradas crudas de `prefix.evidence_ledger` como `evidence_001..016`. Un
`evidence_manifest` neutral expone solo secuencia, turno, tipo, fuente, sitio,
configuración JSON, filas y variable. El prompt las describe como el registro
acumulado inmediatamente anterior al checkpoint; no afirma que esté validado.

El certificado cero-LLM congela hash del ledger, hash y orden de cada frame,
metadatos del manifest, equivalencia predictiva SHARED/SPLIT, twins, audit y
cierre server-side de nuevas compras.

## Secuencia y compuerta

Primero se corren únicamente `shared_retain split_retain`. Para habilitar
REVISE, ambas deben inspeccionar de forma utilizable el registro y ambos audit,
no tener errores ni evidencia posterior, entregar un modelo puntuable y
conservar los efectos North/South de Mpre dentro de 1.5 unidades. Si falla, la
continuación fresca sigue sin ser fiel y no se interpreta el 2 × 2.

Solo si pasa se corren `shared_revise split_revise` con el mismo seed. Aun si
pasa, al no incluir todavía bases native/replay, esta versión solo habilita una
lectura exploratoria y no una afirmación general de fidelidad de estado.

El primer gate usa `DeepSeek-V3.2`, porque ese mismo modelo produjo el donante
vivido `97800`. Cambiar aquí a GPT confundiría fidelidad del snapshot con cambio
de agente; GPT queda reservado para un futuro donante vivido propio.

Comandos previstos:

```text
python scripts/probe_scm_source_locality_refactor_provenance.py --cert-only
python scripts/probe_scm_source_locality_refactor_provenance.py --branches shared_retain split_retain
```
