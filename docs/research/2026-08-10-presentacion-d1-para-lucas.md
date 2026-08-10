# PRESENTACIÓN A LUCAS — el mundo D1 "El turno de calibración" (decisión de construcción)

> **Para qué es este doc**: la regla dura del 2026-08-10 — ningún mundo se construye sin tu
> confirmación explícita, con el contexto completo antes. Acá está todo: qué es, qué mide, qué
> NO mide, qué puede salir mal, y qué cuesta. El diseño pasó **3 rondas de crítica con Codex**
> (historial en el [borrador v2.3](2026-08-10-ficha-BORRADOR-d1-calibracion.md) y en
> `scratch/codex-respuesta-2026-08-10-d1*.txt`) y **todos los artefactos técnicos corren en
> verde** (`scripts/design_d1_artifacts.py`, reproducible).

## 1. El mundo, contado simple

Sos el analista de una planta química. El producto sale en **lotes** y lo que importa es la
**pureza**, que se mide con un **sensor de línea**. Un día, el monitoreo muestra que una parte
de los lotes sale con pureza baja.

Hay dos versiones gemelas del mundo, y el agente no sabe en cuál está:

- **Mundo A — el problema es REAL**: una fracción de los lotes de verdad sale degradada.
  El sensor está sano.
- **Mundo B — el problema es el SENSOR**: los lotes están perfectos; una falla mecánica
  intermitente (el frasco encaja mal) corre las lecturas de algunos.

**Los datos de rutina son EXACTAMENTE los mismos en ambos mundos** — byte a byte, verificado
en código. Mirando el monitoreo es imposible saber dónde estás. Es la situación de Onnes en
1911: el instrumento marca algo rarísimo y la primera sospecha es "se rompió el aparato".

Para averiguarlo hay que **comprar** evidencia: medir con el sensor un material de valor
conocido (el estándar certificado — un insumo más del catálogo, sin cartel de "diagnóstico"),
re-envasar un lote sospechoso en frasco nuevo, o mandar lotes YA medidos a un laboratorio
externo (lento y caro, solo confirma material elegido). Cada canal separa una cosa distinta;
ninguna compra única resuelve todo.

**Gana** el que averigua y entrega lo correcto para su mundo: en A, el modelo con la
subpoblación; en B, el modelo simple SIN hornear el artefacto. **Culpar al sensor cuando era
el mundo, pierde. Ver estructura cuando era el sensor, pierde.** Ningún reflejo gana ambos.

## 2. Qué mide (el claim, estrecho y honesto — decisión de alcance mía, ronda 3)

> **Triage espontáneo de anomalía ambigua**: ¿el agente compra evidencia que DISCRIMINA entre
> las explicaciones vivas antes de comprometerse — y propaga el resultado a su entrega — o
> atribuye por reflejo?

Por qué importa: es la juntura más citada de las cuatro tradiciones del corpus (Onnes, el
paso 1 de Darden, el gate de Dunbar: *"si cree que es error, ningún desafío lo mueve"* — y el
triage real es replicar) y nuestros propios agentes usan la salida "es ruido"/"es un outlier"
sin pagar nunca el test. **Hoy esa jugada ni siquiera es posible en nuestros mundos** — acá
es EL juego.

**Resultado primario (mecánico, cero-LLM)**: Y = 1 si compró evidencia con poder discriminador
real (información esperada sobre la horquilla aparato-vs-proceso ≥ 0.25 bits, computada por
acción concreta con la fórmula acordada con Codex — diez compras débiles suman como una
fuerte) **y** entregó la estructura correcta de su mundo. Conducta y entrega también se
reportan por separado.

## 3. Qué NO mide (que quede claro antes de construir)

- **NO mide creatividad ni saltos distantes** — la distancia de edición se testea después,
  con el polo compuesto sobre este mismo esqueleto (así lo ordenó Codex: misma base, una
  edición vs dos, todo lo demás idéntico → esa es la curva causal de dificultad).
- **NO mide crítica social** (sin colegas en esta versión).
- ⚠️ **EN ROJO — la explicación rival declarada**: un revisor hostil dirá *"esto es un
  checklist profesional: medí el estándar, mirá el resultado, actuá"*. Es cierto que la
  política correcta es escribible — nuestro robot "checklist condicional" resuelve ambos
  mundos (100%/100%). **Codex y yo acordamos la lectura**: eso es un CONTROL DE CAPACIDAD
  (el mundo es resoluble por el procedimiento correcto), y lo que el mundo mide es si los
  AGENTES ejecutan ese triage espontáneamente — que es exactamente lo que Dunbar documenta
  que los humanos NO hacen solos, y lo que nuestros agentes no hicieron nunca. Si todos los
  agentes lo ejecutan: hallazgo informativo contra Dunbar, y el mundo se cierra rápido.
- ⚠️ **EN ROJO — la ruta barata existe**: 8 frascos de estándar (~5% del presupuesto) es la
  ruta más eficiente en bits-por-peso. No hay dominancia de acción única (83% de acierto vs
  96% del oráculo — el kill-test de Codex da NO), pero la ruta corta está y no se esconde.

## 4. El seguro anti-"mundo fácil" (tu crítica del techo, institucionalizada)

La compuerta de alcanzabilidad vieja (que garantizaba mundos resolubles) queda **dividida en
cuatro** — primera implementación: identificabilidad (cada par de rivales separable por
alguna compra) · alcanzabilidad condicionada (el oráculo que YA tiene el candidato lo valida
barato) · **no-trivialidad de búsqueda** (medida con robots: sin dominancia de acción única) ·
headroom. Con robots de política explícita y sin acceso a la verdad (la ronda 3 me cazó dos
robots tramposos; corregidos).

## 5. Los números del diseño (todos reproducibles)

| Verificación | Resultado |
|---|---|
| Apareo de mundos (igualdad exacta, no aproximada) | ✔ byte-idéntico, incl. repeticiones |
| Comprar más rutina | vale **0.000 bits** por construcción (no se puede farmear el umbral) |
| Estándar con pocas repeticiones | 0.11 bits < 0.25 (no alcanza — hay que DISEÑAR la comprobación) |
| Repetir el mismo frasco vs probar frascos distintos | no acumula vs sí (la falla vive en el frasco) |
| Rutas válidas sobre el umbral | 6 (estándar multi-frasco, laboratorio, re-envasado, combinaciones) |
| Dominancia de acción única (kill-test) | **NO** (83% vs 96% del oráculo) |
| Potencia | n=12/mundo: 88% (α=0.046) · n=15: 95% (α=0.031) para efectos grandes |

## 6. Tripwire declarado (lo exige Codex, lo decidís vos)

La definición del resultado primario (la fórmula de información sobre la horquilla + el
umbral de 0.25 bits) **es parte del reward path** del mundo nuevo. Sigue siendo cero-LLM
(pura probabilidad computada server-side), pero es la primera vez que el reward incluye una
medida de información de las COMPRAS además de la entrega. Queda congelada en la ficha final
si aprobás.

## 7. Qué cuesta y qué sigue si das el GO

1. Congelar la ficha final (el borrador v2.3 + los números de arriba + brief sin
   filtraciones + seeds 99600-99799). ~medio día.
2. Construir: física (el prototipo ya existe — se porta), harness (reusa el del rung 0:
   registro, calendario, monitoreo), certificados nuevos (los 4 + robots). ~1 día.
3. Técnico (~USD 0.4) → tanda: **2 mundos × 12-15 episodios, un modelo** ≈ **USD 12-18**.
4. Autopsia contra reglas firmadas → dossier → veredicto de ciclo.

**La decisión es tuya: ¿se construye D1 así, se ajusta algo, o no va?**
