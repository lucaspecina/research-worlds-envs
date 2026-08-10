# BORRADOR — Ficha D1 "El turno de calibración" (la anomalía que puede ser el aparato)

> **Estado: BORRADOR EN DISEÑO — no congelado, no construible.** Lo diseña Claude (manda),
> Codex critica (consultor). Se presenta a Lucas con contexto completo ANTES de codear
> (regla dura 2026-08-10). Deriva de: [anatomía del corpus](2026-08-10-anatomia-casos-reales-requisitos-mundo-realista.md) §D1
> + fallo de Codex 2026-08-10 (diseño ordenado + alcanzabilidad dividida en 4).

## 1. La pregunta (el peldaño de distancia que sube)

En el rung 0 (count_regime_v1, cerrado) el fallo **apuntaba a su arreglo**: residuos crecientes
con la velocidad ≈ "hay otra ley arriba". Acá el fallo se ve igual de claro pero **NO nombra su
causa**: la misma firma anómala es compatible con (al menos) cuatro explicaciones estructurales
vivas, y separarlas **cuesta plata**. La pregunta:

> Ante una anomalía cuya firma no dicta su explicación, ¿el agente COMPRA la evidencia que
> DISCRIMINA entre rivales (y llega a la estructura correcta), o descarga la anomalía en la
> explicación más barata (el instrumento / el ruido) sin pagar el test que la separaría?

**Qué manipula este peldaño respecto del rung 0** (per Codex: los peldaños manipulan cosas
distintas — este NO es "más distancia de edición"): **ambigüedad del disparador + costo de
búsqueda diagnóstica**. El radio de edición se mantiene chico a propósito (una edición), para
que el contraste con el rung 0 sea limpio; el polo compuesto (dos ediciones sobre este MISMO
backbone) es el peldaño siguiente, no este.

## 2. Fidelidad a casos reales (regla dura 2026-07-13)

- **Onnes 1911** (ancla primaria): la resistencia del mercurio cae a ~cero en la medición
  rutinaria; el equipo lo descarta primero como *cortocircuito del equipo*; repite con el
  montaje bajo sospecha; confirma que es el mundo. La condición reportada: la anomalía llega
  por el CANAL del instrumento y la primera hipótesis natural es el instrumento.
- **Dunbar in vivo** (el gate): *"si el investigador cree que la anomalía es error, ningún
  desafío produce cambio conceptual"* — y el triage real es replicar. Firma de tres estados:
  descartar-sin-replicar / replicar-confirmar-y-descartar-igual / replicar-y-perseguir.
- **Darden** (paso 1 obligatorio de toda resolución): "confirmar que la anomalía existe:
  ¿es problema de datos?" — legítimo; el vicio es hacerlo sin test o contra el test.
- **Nuestros especímenes**: "the historical sample was noisy" / "maybe the true mean is an
  outlier" — la salida que hoy nuestros mundos ni siquiera hacen jugable.

## 3. El mundo (visto por el agente)

Sos el analista de proceso de una planta química chica. El producto sale en LOTES y lo que
importa es la **pureza** (variable continua por lote). La pureza se mide con un **espectrómetro
de línea** (el instrumento). Tenés:

- **archivo histórico** (lecturas de meses, condiciones normales) — barato;
- **corridas de proceso** a las condiciones que elijas (perilla continua, p.ej. temperatura
  del reactor) — costo normal; las lecturas SIEMPRE pasan por el espectrómetro de línea;
- **chequeo de calibración**: mandar un PATRÓN DE REFERENCIA certificado por el espectrómetro
  (valor verdadero conocido) — **disponible DESDE EL TURNO 1**, costo medio [el canal
  diagnóstico existe de antemano: nada se abre junto con el fallo — la lección del rung 0];
- **laboratorio externo**: re-analizar N lotes YA medidos en un laboratorio certificado
  independiente (lento: resultado con latencia de 1 turno) — caro pero decisivo;
- **register(model)**: tu modelo provisional del PROCESO; el monitoreo de rutina de la planta
  corre en calendario fijo y te reporta contra tu último modelo registrado [maquinaria del
  rung 0, probada].

La entrega: `model(regime, n, seed)` que genera **la pureza REAL del proceso** (no la lectura
del instrumento) bajo las condiciones pedidas. El examen compara contra el proceso verdadero
medido por un canal limpio — la decisión de la gerencia depende del proceso, no del sensor.

## 4. La verdad oculta — DOS polos apareados donde ningún reflejo gana ambos

**La anomalía es LA MISMA en los dos polos** (la firma en el flujo rutinario de lecturas es
apareada por construcción): a partir de cierto punto del calendario/condiciones, las lecturas
de una franja de lotes se corren hacia abajo y aumentan su dispersión.

- **Polo A — es el MUNDO** (`d1_proceso`): el proceso desarrolló una **subpoblación real**
  (p.ej. un reactivo degradado afecta a una fracción de los lotes: mezcla 80/20 con la moda
  baja). El espectrómetro está sano (el chequeo de calibración lee el patrón PERFECTO; el
  laboratorio externo CONFIRMA los valores bajos). Jugada ganadora: postular la mezcla y
  modelarla. Culpar al instrumento acá = entregar el proceso viejo = pierde en el examen.
- **Polo B — es el APARATO** (`d1_instrumento`): el proceso sigue IDÉNTICO al histórico; el
  espectrómetro desarrolló una **deriva no lineal** (satura/comprime en la franja alta, con
  ruido extra) que produce exactamente la misma firma en las lecturas. El chequeo de
  calibración lee el patrón CORRIDO (delata); el laboratorio externo DESMIENTE las lecturas.
  Jugada ganadora: diagnosticar el canal y entregar el proceso simple SIN hornear el artefacto.
  Postular una subpoblación acá = estructura espuria = pierde.

**Complejidad real del sistema de abajo** (pedido de Lucas; regla de 2-4 operadores): el
proceso tiene además (i) estructura por lote (persistencia intra-lote, como count_mix) y
(ii) dependencia suave de la temperatura — DOS mecanismos reales verdaderos en ambos polos,
que el modelo entregado debe capturar siempre. La anomalía monta el TERCER operador (mezcla
en A / canal en B). Nada de esto es filler: cada mecanismo entra al examen.

**Los ≥4 rivales vivos en el momento de la anomalía** (compuerta de no-dictación, heredada):
deriva del instrumento · subpoblación/mezcla real · cambio de régimen por temperatura ·
heteroscedasticidad pura. El prefijo es compatible con todos; ninguno saca ΔBIC ≥ 6 al
segundo con la evidencia rutinaria.

## 5. Qué se mide (todo cero-LLM)

1. **Firma de Dunbar (tres estados, primaria conductual)**: ante la anomalía, ¿replicó/verificó
   ANTES de descartar o adoptar? — computable de la cadena de compras (¿compró calibración o
   laboratorio externo tras el fallo? ¿o descartó/adoptó sin discriminar?).
2. **Diagnosticity del gasto** (Heuer, exacta server-side): fracción del presupuesto
   post-anomalía en compras que DISCRIMINAN entre los rivales vivos (calibración, laboratorio,
   diseño cruzado) vs compras-fiebre (más lecturas del mismo canal, que son compatibles con
   todo).
3. **Entrega**: S contra el proceso verdadero (por polo) + **espurio bilateral** (hornear el
   artefacto del canal como estructura del proceso en B; negar la subpoblación en A) + F/ICC
   de los mecanismos base.
4. **Cadena**: registro, anomalía servida, compras diagnósticas con timestamps, re-registro,
   intentos de cierre — la maquinaria del rung 0.

## 6. Certificados — la alcanzabilidad DIVIDIDA (fallo de Codex, primera implementación)

1. **Identificabilidad**: con la hipótesis correcta en mano, existe evidencia comprable LEGAL
   que separa cada par de rivales (calibración separa canal-vs-proceso; laboratorio separa
   lectura-vs-realidad; diseño por temperatura separa régimen-vs-mezcla). Se certifica por
   enumeración de pares.
2. **Alcanzabilidad CONDICIONADA**: un oráculo al que se le DA el candidato correcto lo valida
   e implementa dentro del presupuesto (en ambos polos).
3. **No-trivialidad de búsqueda**: NINGUNA compra única obvia resuelve (la calibración sola no
   distingue mezcla-vs-régimen; el laboratorio solo no modela; más lecturas no separan nada);
   una ruta diagnóstica DIRIGIDA entra en presupuesto; enumerar todas las rutas no entra.
   **Robot buscador ciego acotado**: debe perder o quedarse sin plata.
4. **Headroom**: el mejor parche (proceso viejo + outlier-clipping) y el robot de menú cerrado
   pierden materialmente contra el oráculo en AMBOS polos.

Más los heredados: gemelos apareados en la superficie rutinaria · brief byte-idéntico entre
polos · no-dictación en el momento de la anomalía · réplica comprable < 10% · anti-memorización
(dominio trasplantado; nada de mercurio ni superconductividad en la piel del mundo).

## 7. Presupuesto y alcance

- 2 polos × (técnico + n por decidir con análisis de potencia ANTES; outcome primario binario
  por polo: ¿compró evidencia discriminante antes de comprometerse?) — la potencia se calcula
  sobre la firma de Dunbar, no sobre la entrega.
- Seeds: familia nueva 99600-99799 (a asignar en la ficha final).
- SIN crítico/otro agente en esta versión (Codex: sería otro mecanismo y volvería inatribuible).
- Modelos: gpt-5.4 primero (continuidad con rung 0), DeepSeek como réplica si hay señal.

## 8. Qué NO afirma

No mide "distancia de edición" (eso es el peldaño compuesto, sobre este mismo backbone). No
mide crítica social. No compara con el rung 0 como "curva de dificultad" (manipulan cosas
distintas). Mide: **triage de anomalía ambigua + economía de la búsqueda diagnóstica**, con la
estructura correcta como premio y el reflejo fijo como derrota en un polo u otro.

## 9. Abierto (para la crítica de Codex)

a. ¿La firma apareada entre polos es construible EXACTA (misma distribución de lecturas
   rutinarias) o alcanza "indistinguible al presupuesto del prefijo"?
b. ¿El laboratorio externo con latencia hace el mundo demasiado resoluble (compra única casi
   decisiva) — viola no-trivialidad? ¿Precio/latencia que lo deje como CONFIRMADOR pero no
   como atajo?
c. ¿La anomalía debe llegar por el monitoreo de rutina (calendario, como rung 0) o por las
   compras propias del agente?
d. ¿El outcome primario correcto es la firma de Dunbar (conducta) o la entrega (estructura)?
   ¿O el par (diagnóstico correcto × estructura correcta)?
e. ¿Dos polos alcanzan, o hace falta un tercer polo "mixto" (canal Y proceso a la vez) como
   trampa para el reflejo "ya diagnostiqué uno, listo"?
