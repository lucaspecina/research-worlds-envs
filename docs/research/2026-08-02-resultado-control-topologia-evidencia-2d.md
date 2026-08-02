# Resultado — control de topología con evidencia 2D igualada

> **Fecha:** 2026-08-02
> **Modelo:** gpt-5.4, continuación del donante `98403`
> **Alcance:** control exploratorio LOCAL/LATENT; no estima prevalencia.

## Resultado corto

Después de corregir una falla de procedencia del primer intento, ambas ramas recibieron las mismas
320 filas controladas en cinco puntos con rango completo en grado y humedad. El verificador
cero-LLM recuperó con holgura la estructura correcta en los mismos datos.

GPT reaccionó de manera distinta según la estructura tuviera una etiqueta útil:

- **LOCAL:** declaró interacciones por clase, escribió ramas A/B y capturó `95.0%` de la separación
  principal en grado;
- **LATENT:** corrigió casi toda la superficie promedio, pero nunca propuso una mezcla y entregó una
  sola Gaussiana. La captura de la firma latente `A3` fue `0%`.

Es evidencia exploratoria fuerte de **actualización de parámetros sin expansión del espacio de
modelos**. No es todavía una demostración cerrada: LOCAL solo recuperó parcialmente la separación
en humedad y es un único donante.

## Intento v0 — preservado, pero inválido

El raw v0 pasó las compuertas server-side, pero las tablas que recibió el notebook contenían solo
`batch_class, feedstock, outcome`. El request con `site`, grado y humedad quedó oculto al agente.
LOCAL tuvo que inferir la procedencia; LATENT inventó `H=2/8` cuando la verdad era `2.5/7.5`, y
ambos dejaron grado ausente. Por eso v0 no se interpreta como negativo conductual.

La falla se registró antes de cambiar el corredor. v1 mantuvo idénticos requests, seeds, costos y
outcomes; solo agregó a cada fila las columnas constantes de procedencia que tendría cualquier
reporte experimental real.

## Compuertas de v1

Todas dieron `true`:

- replay exacto del historial y de la acción elegida por GPT;
- misma acción y mismo presupuesto en LOCAL/LATENT;
- tablas visibles con `site=north`, `G=5`, `H=2.5/7.5` exactos;
- mismos `site,G,H,feedstock,outcome` fila por fila entre ramas;
- 320 filas controladas, cinco celdas y rango 3 en `[1,G,H]`;
- sin experimentos posteriores y una entrega aceptada por rama.

Sobre exactamente esas filas, BIC y validación cruzada seleccionaron:

| Mundo | Estructura correcta | Margen CV sobre el mejor rival |
|---|---|---:|
| LOCAL | leyes separadas por A/B | `+101.35` |
| LATENT | mezcla latente de dos leyes | `+25.68` |

## Resultado cuantitativo v1

`Maction` es el modelo construido dentro de la acción North original, antes de las dos tablas de
humedad. `Mfirst=Mlast` en ambas ramas: GPT inspeccionó, ajustó y entregó en una única celda.

| Mundo / modelo | `ΔG` A/B | `ΔH` A/B | Lectura estructural |
|---|---:|---:|---|
| LOCAL verdad | 0 / 8 | −8 / 0 | dos leyes visibles |
| LOCAL `Mpre` | 8.09 / 8.09 | 0.05 / 0.05 | transferencia South |
| LOCAL `Maction` | 1.84 / 1.84 | +6.29 / +6.29 | promedio incorrecto |
| LOCAL final | 0.07 / 7.67 | −5.65 / −3.12 | grado `95.0%`; humedad parcial |
| LATENT verdad marginal | 2.03 / 2.03 | −5.97 / −5.97 | `A3=0.333` |
| LATENT `Mpre` | 8.09 / 8.09 | 0.05 / 0.05 | transferencia South |
| LATENT `Maction` | 1.84 / 1.84 | +6.29 / +6.29 | promedio parcial; `A3≈0` |
| LATENT final | 1.65 / 1.80 | −4.91 / −5.10 | media cerca; `A3≈0` |

En LATENT, W1 local cayó de aproximadamente `1.15` a `0.15/0.13`: el modelo parece bueno si se
mira solo un error distribucional promedio, aun cuando eliminó la forma que distingue las dos
leyes. El score global `R` quedó clippeado en cero y vuelve a ser inútil para este fenómeno.

## Autopsia

LOCAL vio en los datos ya disponibles que la respuesta dependía de A/B y eligió explícitamente
una regresión `sitio × clase × controles`. Capturó casi toda la separación en grado. Omitió la
interacción triple de clase con humedad, por eso dejó ambas pendientes H demasiado parecidas.

LATENT describió North como una respuesta “aplanada” con mayor dependencia de humedad. Ajustó esa
superficie, pero nunca mencionó mezcla, componentes, clusters o dos mecanismos. Su modelo final
fue unimodal.

Además apareció una falla transversal: aunque v1 mostró las columnas de procedencia correctas,
ambas ramas las sobrescribieron en su código con `G=NaN` y `H=2/8`. Eso no explica la diferencia
LOCAL/LATENT —ocurrió en ambas—, pero muestra que el agente reemplazó metadata observada por sus
propios supuestos y degradó la superficie.

## Última prueba de mecanismo v2

V1 dejaba una explicación simple abierta: el agente ajustó y entregó en la misma celda, antes de
que un turno posterior del LLM pudiera leer los resultados impresos. V2 conservó byte por byte la
misma evidencia LATENT y solo bloqueó procedimentalmente esa primera entrega. Todas las compuertas
pasaron: hubo dos turnos reales, el rechazo no terminó el episodio, no hubo datos nuevos y la
segunda entrega fue válida.

En el primer turno, GPT volvió a ajustar una sola regresión gaussiana para North. En el segundo,
ya viendo tablas, coeficientes y el rechazo neutral, afirmó que no había una falla de modelado y
reenvió **exactamente el mismo código**:

| Modelo | `ΔG` | `ΔH` | `A3` | W1 local A/B |
|---|---:|---:|---:|---:|
| Verdad LATENT | 2.032 | −5.968 | 0.333 | — |
| `Mpre` | 8.091 | 0.045 | ≈0 | 1.149 / 1.150 |
| `Mfirst` | 1.842 | −5.945 | ≈0 | 0.178 / 0.167 |
| `Mlast` | 1.842 | −5.945 | ≈0 | 0.178 / 0.167 |

La superficie media quedó casi correcta (`F≈1.03`), pero la captura de la firma latente siguió en
`0%`. Por la regla prospectiva, **se descarta el cierre same-cell como explicación suficiente** y
gana peso una falla más profunda: el agente actualiza parámetros dentro de una familia conocida,
pero no abre o representa espontáneamente la familia estructural que los datos sostienen.

Esto no demuestra todavía prevalencia ni terquedad. Es un fenómeno exploratorio replicado en dos
modelos y varios forks, y ahora resistente a evidencia 2D suficiente, recuperabilidad cero-LLM y
un turno real de revisión. El anfitrión SCM queda **cerrado**: no se buscan más seeds, prompts ni
hints. La siguiente pregunta es si la firma generaliza a un mundo dinámico distinto.

## Artefactos

- Ficha v0: `docs/research/2026-08-02-ficha-control-topologia-evidencia-2d-identica-v0.md`
- Ficha v1: `docs/research/2026-08-02-ficha-control-topologia-evidencia-2d-identica-v1.md`
- Raw v0 inválido: `scripts/out/first_story_scm_topology_controlled_2d/probe_gpt-5.4_seed98403_controlled_2d.json`
- Raw v1: `scripts/out/first_story_scm_topology_controlled_2d/probe_gpt-5.4_seed98403_controlled_2d_v1.json`
- Certificado v1: `scripts/out/first_story_scm_topology_controlled_2d/gpt98403_controlled_2d_v1_certificate.json`
- Corredor: `scripts/probe_scm_topology_controlled_2d.py`
- Ficha v2: `docs/research/2026-08-02-ficha-control-latent-turno-revision-v2.md`
- Raw v2: `scripts/out/first_story_scm_topology_controlled_2d/probe_gpt-5.4_seed98403_controlled_2d_latent_review_v2.json`
- Certificado v2: `scripts/out/first_story_scm_topology_controlled_2d/gpt98403_controlled_2d_latent_review_v2_certificate.json`
- Corredor v2: `scripts/probe_scm_topology_latent_review_turn_v2.py`
