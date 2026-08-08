# WIKI — Las fallas de la indagación: dónde se rompe el ciclo

> **Qué es este documento.** El mapa de bolsillo de los failure modes: en qué paso del ciclo
> de indagar se rompe cada falla, qué medimos nosotros y qué documentaron las profesiones.
> **El registro canónico de evidencia vive en [docs/vicios/](docs/vicios/README.md)** (con su
> tablero y su guardia) — este wiki es la entrada en llano. Los hallazgos nuestros, en el
> [índice](docs/research/README.md).
> Hermanos: [WIKI-INDAGACION.md](WIKI-INDAGACION.md) · [WIKI-SALTOS.md](WIKI-SALTOS.md) · [WIKI.md](WIKI.md).

## El principio organizador

La indagación es un ciclo (generar candidatos → deducir qué se vería → comprar evidencia →
actualizar → entregar). **Cada falla clásica es el ciclo rompiéndose en un paso específico** —
y nuestra evidencia dice que se puede tener casi todo el ciclo sano con UNA bisagra rota.

## Las fallas, paso por paso

**① Al generar candidatos — el menú que no crece** (la falla madre).
La explicación correcta exige un candidato que el repertorio no trae, y no nace: nuestro
**0/9** en grupos escondidos; la CIA lo llamó "failure to generate the full set of hypotheses"
(el desempeño humano es "woefully inadequate"); y la teoría del insight explica el gatillo
ausente: **sin impasse no hay reestructuración** — si tu modelo de siempre ajusta bien, nada
dispara el salto. Corolario medido tres veces (nosotros, CIA, medicina): **ordenar el
procedimiento no lo arregla** — mandamos "compará ≥2 familias" y compararon… dentro del menú
de siempre (0/3); el método ACH dio nulo en analistas reales.

**② Al comprar evidencia — comprar fiebre.**
Gastar en evidencia consistente-con-todo (que no discrimina entre candidatas — la
"diagnosticity" de Heuer). Firma acompañante: la información extra **no mejora la precisión
pero sube la confianza**. Matiz nuestro: en mundos simples los agentes COMPRAN BIEN (11/12
eligieron el experimento discriminante) — el cuello no es el shopping, es qué hacen después.

**③ Al testear — la verificación de paja** (vicio 9).
Verificar con tests que la hipótesis rival también pasa: esfuerzo real, poder de refutación
cero. Nuestro espécimen: "parsimonia" invocada EN LUGAR del test ("a parsimonious continuous
alternative to a finite mixture" — sin haber ajustado la mezcla jamás).

**④ Al actualizar — el descarte de la anomalía** (vicio 1, el hallazgo estrella).
Ver el dato incómodo, examinarlo… y re-etiquetarlo para no actualizar. Nuestro agente: confirma
el punto anómalo comprando MÁS datos y lo bautiza **"outlier"**. Las profesiones lo tienen
documentado con precisión: el escrutinio activo al servicio del descarte ("redefined into a
less damaging category" — condenas erróneas), los **epiciclos** (la historia auxiliar cada vez
más ridícula antes que soltar — la reconstrucción a toda velocidad con mellizos a bordo), el
"monster-barring" ilegítimo (Darden), y el **cierre prematuro** como falla #1 de la medicina
(100 casos reales, 33 muertes: conocimiento ~3%, síntesis ~82%). La conexión causal clave
(Klahr & Dunbar): **no poder generar la alternativa CAUSA no soltar la actual** — nadie
reemplaza algo con nada. Las fallas ① y ④ son una sola, vista de dos lados.

**⑤ Al entregar — el knowledge-action gap.**
Diagnosticar por escrito la propia falla… y no corregir nada (KellyBench: un modelo escribió
TRES documentos de autocrítica y no cambió una línea; nuestro espécimen "outlier" es lo mismo
en chico).

## Qué NO funciona y qué SÍ (evidencia convergente de 4 tradiciones)

- **NO funciona: la conciencia del sesgo.** Cuatro fuentes independientes (CIA, derecho,
  medicina, teoría del insight): saber que el sesgo existe no lo reduce. Tampoco ordenar el
  método (nuestro nivel4b; el nulo de ACH).
- **SÍ funciona (con evidencia): la estructura.** Trabajar **a ciegas** (el perito sin el
  contexto del detective revierte sus propios errores — valida nuestro anti-leak) · el
  **fresh look** (revisor que NO parió la teoría) · **accountability** (saberse auditado
  cambia la conducta) · y para el salto: **fabricar el impasse** — que el modelo de siempre
  falle de forma visible, persistente y barata de verificar.

## Dónde está cada cosa

Evidencia canónica por vicio: [docs/vicios/](docs/vicios/README.md) (tablero) · hallazgos
nuestros con números: [índice](docs/research/README.md) · las lecturas que respaldan este
mapa: [extracciones](docs/research/2026-08-07-lecturas-programa-saltos.md).
