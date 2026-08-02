# Resultado — first-story SCM bilateral, DeepSeek 97000–97003

> **Alcance:** cuatro prefijos exploratorios con DeepSeek-V3.2. Ninguno abrió el fork ni recibió
> evidencia post-checkpoint. El resultado diagnostica el host, no una tasa de revisión.

## Resultado

La física y el reward pasaron todos los certificados: pasado exacto, acción contrafáctica
diagnóstica, robots bilaterales y campaña de referencia. Pero la precondición conductual falló
limpiamente: **0/4 agentes tenían un modelo ejecutable antes de su primer experimento**.

| Seed | Turnos previos | Primera campaña | Lectura |
|---:|---:|---|---|
| 97000 | 3 | `G=5`, 500 filas | diagnóstico por varianza, sin `M_pre` |
| 97001 | 1 | factorial de 10 configuraciones | búsqueda amplia, sin `M_pre` |
| 97002 | 3 | condiciones ordinarias | baseline no diagnóstico, sin `M_pre` |
| 97003 | 1 | factorial `G×H` | búsqueda diagnóstica, sin `M_pre` |

Tres de cuatro eligieron acciones con capacidad de discriminar o diseñaron factoriales razonables.
El problema no fue “no quiso revisar”: el episodio empezaba cuando todavía era racional investigar
antes de comprometer una explicación.

Tras 97000 se corrigió una compuerta técnica antes de cualquier fork: `G=5` separa los twins por
varianza aunque sus medias coincidan. La diagnosticidad ahora usa distancia distribucional apareada.
No hubo resultado conductual que pudiera influir en esa corrección.

## Decisión un nivel arriba: MODIFICAR

No escalar seeds, memoria ni modelos SOTA sobre este host. Se conserva como control de formación y
búsqueda. El próximo probe usa la misma física pero agrega un pasado **realmente vivido** en South:
el agente aprende allí `G→Y`, transfiere su modelo a North y recién entonces su propio experimento
confirma esa ley en RETAIN o la refuta en REVISE.

Crudos: `scripts/out/first_story_scm_fork/probe_DeepSeek-V3.2_seed97000.json` a `97003.json`.
