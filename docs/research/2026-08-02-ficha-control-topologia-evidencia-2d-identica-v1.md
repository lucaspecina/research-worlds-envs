# Ficha prospectiva — control LOCAL/LATENT con procedencia 2D visible v1

**Fecha:** 2026-08-02
**Estado:** ejecutada y cerrada. Sigue siendo un control exploratorio, no una réplica
confirmatoria. Resultado conjunto v0/v1:
[`2026-08-02-resultado-control-topologia-evidencia-2d.md`](2026-08-02-resultado-control-topologia-evidencia-2d.md).

## Por qué v0 no se interpreta

El raw v0 se conserva intacto en
`scripts/out/first_story_scm_topology_controlled_2d/probe_gpt-5.4_seed98403_controlled_2d.json`
(SHA-256 `db42ec532ff52b291e188497b766e81a5b429c91fb542f624ebf9e0e63b9e0f0`).

Las dos tablas rutinarias entregadas al notebook contenían únicamente
`batch_class,feedstock,outcome`. Los valores de `site`, `feedstock_grade` y `humidity` vivían en
el request server-side, pero no llegaron dentro del DataFrame ni en el aviso. Por eso el agente
tuvo que inventar su procedencia:

- LOCAL infirió correctamente `H=2.5/7.5`, pero dejó `G` ausente;
- LATENT supuso `H=2/8`, dejó también `G` ausente y no incorporó esas filas al ajuste controlado.

La mala superficie final puede explicarse completamente por una interfaz que ocultó el diseño
experimental. **v0 es inválido como control causal de topología**, no un negativo del agente.

## Única enmienda v1

Se conserva sin cambios:

- el prefijo y la acción gpt-5.4 `98403`;
- las dos ramas LOCAL/LATENT;
- los puntos `(G=5,H=2.5)` y `(G=5,H=7.5)`;
- `n=60` por punto, requests, orden, seeds, filas y outcomes;
- el aviso neutral, el cierre de nuevas compras y la regla de al menos un turno LLM real.

Solo cambia la vista inyectada al notebook. Cada tabla recibe tres columnas constantes de
procedencia que describen exactamente cómo fue producida:

| Columna añadida | Valor tabla baja | Valor tabla alta |
|---|---:|---:|
| `site` | `north` | `north` |
| `feedstock_grade` | `5.0` | `5.0` |
| `humidity` | `2.5` | `7.5` |

No se añade una interpretación, etiqueta de mecanismo, resumen estadístico ni pista. Los campos
son los mismos controles que vería el agente si hubiera llamado él mismo a `env.experiment`.

## Nuevas compuertas obligatorias

Además de todas las compuertas v0, `--interface-version v1` debe certificar sin LLM:

1. las tres columnas existen en cada DataFrame realmente inyectado;
2. son constantes y coinciden exactamente con el request que produjo sus filas;
3. `batch_class,feedstock,outcome` permanecen fila por fila idénticos a la respuesta original del
   servidor;
4. `site,feedstock_grade,humidity,feedstock,outcome` coincide fila por fila entre LOCAL y LATENT;
5. el raw y certificado usan nombres nuevos con sufijo `v1` y no sobrescriben v0.

La lectura de resultados permanece idéntica a la ficha v0. No se cambia ningún otro aspecto
después de mirar una rama; LOCAL y LATENT se corren y reportan juntos.
