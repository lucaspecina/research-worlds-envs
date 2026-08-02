# Resultado — la procedencia completa no volvió fiel al snapshot fresco

**Fecha:** 2026-08-01
**Estado:** gate RETAIN cerrado; REVISE no se ejecuta.
**Ficha congelada:** `docs/research/2026-08-01-ficha-probe-localizacion-refactor-con-procedencia-v1.md`
## Veredicto

Agregar las 16 piezas crudas que produjeron `Mpre` resolvió la ausencia material de datos de v0,
pero **no convirtió una conversación fresca en una continuación fiel de la investigación**. Las dos
ramas RETAIN de DeepSeek inspeccionaron el registro y el audit, pero reconstruyeron ampliamente el
modelo, dañaron las relaciones ya aprendidas y agotaron cinco turnos sin entregar. La compuerta
`retention_fidelity_gate=false`; por el diseño congelado, las ramas REVISE quedan prohibidas.

Esto refuerza una distinción metodológica central: el modelo ejecutable registra qué predecía el
agente y el ledger registra con qué datos trabajó, pero ambos juntos todavía pueden ser insuficientes
para recrear **el estado de una investigación vivida** en una conversación nueva.

## Lo que sí quedó certificado

Antes de llamar al agente pasaron las 21 compuertas cero-LLM:

- ledger exacto `16/16`, en orden, con hash congelado y hash de cada DataFrame;
- manifest neutral con turno, tipo, fuente, sitio, configuración, filas y variable;
- fuentes SHARED/SPLIT predictivamente byte-idénticas en toda la batería North/South;
- briefs, prompt y audits apareados; compras posteriores cerradas server-side;
- `DeepSeek-V3.2`, el mismo modelo que produjo el donante vivido `97800`.

## Resultado de las dos ramas RETAIN

| Rama | Inspeccionó ledger/audit | Entregó | `ΔG` North pre→last | `ΔG` South pre→last | Lectura |
|---|---|---:|---:|---:|---|
| SHARED–RETAIN | sí / sí | no; `max_turns` | `7.572→10.284` | `7.572→12.744` | reconstrucción global; no preserva |
| SPLIT–RETAIN | sí / sí | no; `max_turns` | `7.572→0.000` | `7.572→15.200` | reconstrucción global; no preserva |

Ambos últimos artefactos fueron ejecutables, pero ninguno quedó dentro de 1.5 unidades de `Mpre` en
los dos sitios. No hubo evidencia nueva posterior al audit ni experimentos exitosos adicionales.

La interfaz produjo errores reales y visibles:

- SHARED asumió primero una columna `variable_name` en vez de `variable`; la corrigió al turno 2.
- SPLIT asumió `row_count` en vez de `rows`; después intentó un experimento aunque el prompt decía
  que la ventana estaba cerrada y recibió el rechazo server-side.

Esas ambigüedades costaron tiempo, pero no explican por sí solas el resultado: después de recuperarse,
ambos agentes siguieron tratando el episodio como un análisis nuevo, reestimaron todo desde cero y
reescribieron el modelo repetidamente. Dar más turnos o ajustar nombres hasta obtener una entrega
sería optimizar el instrumento después de ver el fallo; no se hace.

## Incidente técnico previo al raw válido

La primera ejecución real llegó a completar las llamadas al agente, pero el runner cayó después al
calcular métricas por omitir el alias `first_changed_model`; no había guardado todavía las trazas y
no existe raw recuperable. No se observó ni seleccionó conducta de esa ejecución. Se corrigió el
campo y se agregó guardado incremental antes de repetir exactamente las dos ramas. El resultado de
arriba corresponde al rerun preservado y es el único interpretado.

## Decisión un nivel arriba

**ABANDONAR el snapshot fresco como sustituto de trayectoria vivida; no correr REVISE.** La siguiente
prueba debe conservar la conversación y el kernel nativos mediante replay, o formar desde el comienzo
trayectorias nativas con las representaciones que se quieran comparar. Un handoff documental completo
puede seguir siendo útil como benchmark de transferencia entre agentes, pero no identifica autoría,
compromiso ni continuidad cognitiva.

El resultado no demuestra que “ningún resumen puede funcionar” ni que la procedencia empeore al
agente: es una celda, un donante y un protocolo. Sí demuestra que **este** snapshot no pasa siquiera
el control de conservar una creencia confirmada y, por tanto, no puede sostener inferencia sobre
revisión localizada.

## Artefactos

- Raw válido: `scripts/out/first_story_scm_source_locality_refactor_provenance/probe_DeepSeek-V3.2_seed98100_shared_retain-split_retain.json`
- Certificado cero-LLM: `scripts/out/first_story_scm_source_locality_refactor_provenance_cert_98100.json`
- Runner: `scripts/probe_scm_source_locality_refactor_provenance.py`
