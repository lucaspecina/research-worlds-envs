# Codex ronda 6 — las propuestas de Lucas sobre pistas (variantes + negación del vicio + controles + multi-modelo) — 2026-07-10

> Se le pasaron las propuestas de Lucas casi textuales. Veredicto: ambas ideas validadas con refinamientos — negación literal induce el vicio OPUESTO (usar principio BALANCEADO); variantes con proceso 8-12→filtro semántico→4 congeladas→claim=promedio+leave-one-out; ambos controles necesarios ("el mismo hint en otro mundo controla al hint; otro hint en el mismo mundo controla al mundo"); diseño mínimo honesto 480 episodios (240+240 secuencial); 2 familias de modelos con reglas de lectura; autopsia enriquecida (banco de variantes pre-generado + experimento FORK). Crudo:

codex
## (a) Pista = negación del vicio

Sí, tiene valor sistematizarla, pero la negación literal puede inducir el vicio opuesto:

- “No confirmes” → refutación compulsiva.
- “No te cases” → escepticismo permanente.
- “No ignores evidencia” → sobre-incorporación.

Conviene derivar un **principio balanceado**, no una prohibición:

> “Tratala como provisional y actualizá según cuán discriminante sea la evidencia.”

El test de altura actual no alcanza. Hay que agregar un test de maniobra:

- No revela mecanismo, variable, fuente, herramienta ni experimento específico.
- No prescribe directamente la jugada ganadora.
- Sigue siendo razonable en varias estructuras y en el polo espejo.
- Se deriva viendo solo el catálogo, nunca el mundo concreto.

Lo incorporaría al catálogo como biblioteca de manipulaciones:

- principio balanceado;
- variantes permitidas;
- acciones/palabras prohibidas;
- tier “principio” vs. “acción prescriptiva”;
- auditoría de leak;
- mundos usados para desarrollo y mundos held-out.

Las action-hints pueden existir como upper bound diagnóstico, pero no como evidencia principal de constructo.

## (b) K variantes

No usaría el mínimo: al crecer K, una paráfrasis tóxica terminaría matando cualquier efecto.

Proceso:

1. Generar 8–12 variantes en desarrollo.
2. Filtrarlas por criterios semánticos/leak, no por cuál mejora más R.
3. Congelar 4 variantes confirmatorias lingüísticamente diversas.
4. Claim primario: efecto promedio sobre las cuatro.
5. Robustez: análisis leave-one-variant-out; ninguna variante individual debe explicar todo el efecto.
6. Reportar heterogeneidad y cambios de signo.

Con K=4 no hablaría formalmente de “efecto aleatorio de la población de paráfrasis”; es un conjunto fijo. Para esa generalización necesitarían K≈8 o más.

Mínimo práctico:

- K=4.
- 10 episodios por variante por mundo/modelo.
- 40 episodios agregados por principio en cada mundo/modelo.

Eso alcanza para detectar efectos grandes del orden de 30 puntos porcentuales, no diferencias chicas.

## (c) Ambos controles

Sí. La frase para Lucas:

> **El mismo hint en otro mundo controla al hint; otro hint en el mismo mundo controla al mundo. Sin ambos no sabés cuál de los dos produjo el efecto.**

El diseño ideal es simétrico:

| | Mundo A: vicio A | Mundo B: vicio B |
|---|---:|---:|
| Libre | baseline | baseline |
| Pista A | debería ayudar | control off-diagonal |
| Pista B | control off-diagonal | debería ayudar |

Así ambas diagonales son predicciones y ambos off-diagonales controlan mejora general.

### Mínimo honesto con números

- 2 mundos.
- 2 modelos.
- 3 brazos conceptuales: libre, principio A, principio B.
- K=4 variantes por principio.
- 10 episodios por variante.
- Libre: 40 episodios para igualar precisión.

Conteo:

- 32 celdas de variante ×10 = 320 episodios.
- 4 celdas libres ×40 = 160.
- **Total: 480 episodios.**

Puede hacerse secuencialmente:

- Modelo primario: 240.
- Solo después de cerrar y analizar ese bloque, réplica exacta: otros 240.

Menos que eso vuelve a dejar intervalos demasiado anchos para un fenómeno bimodal. Randomizar e intercalar mundos, brazos y variantes; no correr por bloques secuenciales.

## (d) Multi-modelo

Mínimo: dos familias distintas.

- **Modelo 1:** confirmatorio primario; debe exhibir el vicio y tener headroom basal.
- **Modelo 2:** réplica de transporte; también elegido por baseline/headroom, nunca por respuesta a la pista.
- **Modelo 3 opcional:** perfil exploratorio, no necesario para el claim inicial.

Lectura:

- El vicio no aparece basalmente en un modelo → ausencia de efecto es perfil/ceiling, no refutación del mundo.
- Ambos exhiben el vicio, pero la pista solo cambia conducta en uno → la manipulación es model-specific.
- Cambia conducta en ambos, pero mejora outcome en uno solo → interacción mundo/modelo; debilita generalidad.
- Cambia conducta y mejora selectivamente en ambos → evidencia fuerte.

No promediar modelos ciegamente. El efecto debe condicionarse a que el vicio estuviera vivo antes del tratamiento.

## (e) Autopsia útil para desarrollar variantes

Agregaría hoy:

1. Guardar versión exacta del modelo, temperatura, timestamps, prompt completo, traza, compras, código y score por ítem/partición.

2. Taxonomía ciega de fallos:

   - correlación trasladada a `do()`;
   - sobre-incorporación;
   - reescritura final;
   - defaults/rama incorrecta;
   - proceso vs. medición;
   - ejecución válida pero concepto equivocado.

3. Banco de 8–12 variantes generado antes de mirar sus efectos. Guardar todas, incluidas las tóxicas.

4. Anotar por variante:

   - activó la conducta buscada;
   - reveló una jugada;
   - indujo el vicio opuesto;
   - cambió compras;
   - cambió solo finalización/código;
   - cambió la tasa catastrófica.

5. Hacer un experimento exploratorio de fork: dar a varias muestras exactamente el mismo paquete de evidencia y variar solo la pista al momento de construir la entrega. Eso separa efecto sobre integración final de efecto sobre adquisición.

6. Usar la autopsia para estimar tasas y potencia, pero jamás para contar validación.

La idea de Lucas mejora mucho si la unidad deja de ser “esta frase funcionó” y pasa a ser “este principio, distribuido sobre varias realizaciones lingüísticas, cambia la conducta y el outcome donde corresponde”.
