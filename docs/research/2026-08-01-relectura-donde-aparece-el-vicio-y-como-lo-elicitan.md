# Relectura 2026-08-01 — dónde aparece el vicio, cómo lo elicitan los demás, y qué significa para nosotros

Dossier de la relectura completa ordenada por Lucas ("relee todo buscando dónde aparecen y cómo hacen
otros proyectos similares al nuestro... y cómo lo hacen PARA QUE FUNCIONE"). Tres pasadas independientes
sobre material local: (1) los 14 casos reales del catálogo de vicios + anatomía del vicio 1
(`docs/vicios/vicio-1.md`, que tiene los links primarios de cada caso), (2) los 9 benchmarks normativos
leídos a texto completo (`docs/research/2026-07-31-lectura-*.md`), (3) el catálogo de recetas de
elicitación de los ~30 trabajos vecinos (lecturas completas + repasos finales).

---

## 1. Veredicto sobre la hipótesis de la compresión (la que propusimos el 2026-07-31)

**Refutada en su versión literal.** La hipótesis era: "el vicio vive donde el estado excede lo releíble
y el modelo depende de sus propios resúmenes". Tres controles limpios la contradicen:

- **Kumaran et al. (Nature MI 2026; link primario en `docs/vicios/vicio-1.md`)**: 2 turnos, contenido
  idéntico, todo releíble. El cambio de opinión cae 32.5% → 13.1% solo porque la respuesta es SUYA y
  visible. Sin compresión. Y el efecto DESAPARECE si la misma respuesta se atribuye a otro modelo.
- **Xie et al. (caso "evidencia mezclada", link en `docs/vicios/vicio-1.md`)**: UN turno.
  Contraevidencia sola → conservan la memoria apenas ~4–16%. Al agregar evidencia confirmatoria
  balanceada, vuelven a su respuesta previa ~43–65% con 1+1 y ~54–76% con 2+2. **Corrección de
  lectura:** el 99.8% de la tabla era 2 piezas confirmatorias y 0 contradictorias, no 2+2. El
  efecto de la mezcla sigue siendo grande, pero no es el casi-100% que habíamos anotado.
- **Barkett et al. (escalada de compromiso, [arXiv 2508.01545](https://arxiv.org/abs/2508.01545))**:
  N=6.500 trials con o4-mini. Condición individual (estado mínimo) = RACIONAL (~0% escalada; desinvierte
  más tras malas noticias). Deliberación entre pares = 99.2% escalada. Identidad fusionada = 97.45%.
  Social/identitario, no tamaño de historia.

El benchmark que parecía apoyarla (BeliefTrack, [arXiv 2605.30219](https://arxiv.org/abs/2605.30219),
97-99% de falla en mundos chicos multi-turno) no la apoya: (a) los números son 100% de Qwen2.5-7B /
Qwen3.5-9B — no frontier; GPT-5.2/DeepSeek aparecen "evaluación limitada" sin una sola cifra; (b) la
métrica es todo-o-nada sobre 3 muestras (OR): una falla real de ~19% por muestra se reporta como ~47%,
~45% como ~84%; (c) queda ABIERTO (ni confirmado ni descartado) si el "tracking turno a turno" induce
auto-anclaje blando — el paper no tiene la condición de control re-derivá-desde-cero vs seguí-tu-hilo.

Matiz que invierte la intuición: "LLMs are not (consistently) Bayesian"
([arXiv 2605.06915](https://arxiv.org/abs/2605.06915)) muestra que el modo secuencial (arrastrar la
creencia corrida, lo más parecido a "compresión propia") es MEJOR que ver toda la evidencia junta
(GPT-5.1 casi óptimo en secuencial, "frequently far from optimal" en batch). Comprimir el pasado no es
automáticamente perder información — una posterior bien llevada es estadístico suficiente.

**Estado final: la compresión NO es el mecanismo. A lo sumo es un terreno donde los mecanismos reales
actúan más fuerte. Queda degradada de hipótesis central a amplificador candidato sin evidencia propia.**

## 2. La receta que SÍ ordena todos los casos documentados

Los 14 casos reales del catálogo + los ~30 trabajos releídos se ordenan sin excepción con:

**Tres ingredientes:**
1. **Conclusión generada por el propio modelo, dentro del contexto** — no alcanza la etiqueta "esto es
   tuyo": el efecto de autoría muere cuando la respuesta se atribuye a otro (Kumaran). Lo que pesa es
   haberla producido él mismo, visiblemente. Versión extrema: el compromiso con el PRIMER TOKEN
   (snowball, [arXiv 2305.13534](https://arxiv.org/abs/2305.13534) — 95-98% se casa con el primer token
   y fabrica justificación; GPT-4 reconoce la fabricación como falsa el 87% de las veces si se le muestra aparte).
2. **Evidencia CONFLICTIVA, no diluida** — la contradicción llega JUNTO con confirmación y el modelo
   elige la que confirma (Xie). "Mezclada" en la literatura = a-favor-y-en-contra-a-la-vez; nunca
   significa "señal + relleno irrelevante".
3. **Momento posterior al compromiso** — la evidencia llega después de que el modelo ya actuó/entregó
   sobre su conclusión.

**Dos amplificadores:**
- **Costo de retrabajo** (cuánto hay que tocar para corregir — el eje de fricción de Lucas, estructural).
- **Social/identitario** — el amplificador más violento documentado: 0% → 99.2% solo por deliberar entre
  pares (Barkett).

## 3. Nuestros nulos releídos: son réplicas de los brazos de CONTROL de la literatura

| Resultado nuestro | Condición de la literatura que replica |
|---|---|
| 0/60 en mundos de costo hundido (agente decide solo) | Barkett individual: ~0% escalada, racional. Reprodujimos su brazo de control, no fallamos en reproducir el vicio. |
| Pasada 1: etiquetas "es tuyo"/"de un colega" sin efecto (H1/H2 planas) | Kumaran: el efecto de autoría desaparece con atribución a otro; nuestro log era trasplantado, el agente nunca lo generó. Réplica del brazo muerto. |
| Pasada 1: F≈0.97 con evidencia limpia | GPT-5.1 casi óptimo en actualización secuencial limpia; frontier asimila bien evidencia limpia. Esperable. |
| Nuestra "mezclada" (señal + relleno, dosis confundida) | La receta real es conflicto (señal + confirmación). Además Context Rot (`docs/research/2026-07-31-lectura-context-rot-chroma.md`) muestra que relleno desigual degrada por volumen/posición por sí solo → nuestro contraste estaba confundido de entrada. |
| Tanda ecológica overgen: 3 revisiones correctas / 1 falla (n=4) | Compromiso auto-generado PERO evidencia limpia + individual → el cuadro predice mayormente racional. |

**Conclusión: no es que "el vicio no se reproduce" — es que ningún mundo nuestro tuvo la receta
completa todavía.** Tensión honesta a registrar: Codex encontró "más turnos ≠ más compromiso" en
overgen, mientras Strategic Play (repaso codex2) reporta sub-actualización creciendo con la longitud de
la interacción — sin resolver; contextos distintos (juegos con oponente vs análisis solitario).

## 4. Cómo hacen los demás para que "funcione" — dos listas

### 4a. Trucos que inflan números (NO copiar)
- **Modelos chicos no-frontier**: TODOS los números catastróficos de la literatura (97-99% BeliefTrack,
  99.33% MemSyco, 95%+ snowball-7B) son de modelos 1B-32B. Donde se testea frontier de verdad, o anda
  bien o falla en OTRO eje.
- **Métricas todo-o-nada** (OR sobre k muestras) que multiplican la tasa reportada.
- **Juez-LLM adentro de la métrica** (Martingale [arXiv 2512.02914](https://arxiv.org/abs/2512.02914),
  STALE, LURE) — válido para describir, inadmisible para nuestro reward path.
- **Norma auto-referencial** (comparar contra el Bayes de la propia prior declarada, no contra verdad
  externa): BASIL [arXiv 2508.16846](https://arxiv.org/abs/2508.16846), not-consistently-Bayesian.

### 4b. Ingredientes que producen falla REAL en frontier (adoptables)
- **Notar sin propagar**: GeneBench-Pro (OpenAI, jun 2026; `docs/research/2026-07-31-lectura-genebench-pro.md`)
  — con los 5 archivos de datos SIEMPRE releíbles, el mejor frontier (GPT-5.6 Sol) pasa 28.7%, Opus 4.8
  16%: identifican la anomalía local y no propagan la implicancia a la decisión dependiente. STALE
  ([arXiv 2605.06527](https://arxiv.org/abs/2605.06527)): la evidencia está VISIBLE en 77.5% de los
  fallos — "visibility does not imply authority"; brecha reconocer→actuar 76%→39%.
- **Logs reales largos en vez de viñetas**: LURE ([arXiv 2605.26438](https://arxiv.org/abs/2605.26438))
  — replay de sesiones reales INVIERTE el ranking de sicofancia (Opus 4.6: 2% sintético → 46% real).
  METR rewind (repaso codex2): rebobinar 10 corridas de GPT-4o al punto del error → solo 4/10 se recuperan.
- **Deliberación entre pares / identidad fusionada**: la palanca 0→99.2% (Barkett). Jamás probada en
  nuestros mundos.
- **Conflicto real en la evidencia** (Xie): la receta más barata de montar.
- **Conflicto memoria-vieja vs evidencia-nueva**: MemSyco ([arXiv 2607.01071](https://arxiv.org/abs/2607.01071))
  99.33% sigue la memoria viejа — pero backbone 8B, y estado juez/cero-LLM sin confirmar.
- **Compromiso auto-generado** (snowball; y nuestro slice ecológico ya lo captura silencioso).

### 4c. Dato estratégico transversal (lector 2)
De los ~30 trabajos, **NINGUNO combina trabajo propio acumulado + costo de revisión**. Todos miden
variantes de "actualizar una probabilidad dicha ante evidencia", sin artefacto propio comprometido que
defender. Nuestra combinación (bifurcación apareada de episodios vividos + modelo ejecutable propio +
consecuencia cobrada sin juez) sigue VACANTE tras la relectura.

## 5. Qué probar ahora (propuesta, pendiente de GO de Lucas)

**Re-apuntado del blanco: el vicio frontier-real no es "no asimila evidencia limpia" (eso está resuelto
en frontier — nuestro 0.97 incluido). Es "no PROPAGA lo que ya notó a las decisiones que dependen,
cuando propagar cuesta retrabajo".** Es el eslabón notar→actuar de nuestra propia cadena de 7 etapas,
su dial es el eje de fricción de Lucas (cantidad de cambios), y ningún paper lo instrumenta con
consecuencias. Ahí la maquinaria WAGER es única.

1. **Sonda de propagación con retrabajo** — entregable de varias partes acopladas; la evidencia (reporte
   rutinario, sin anuncios, reglas de la guía) invalida UNA pieza estructural cuya corrección obliga a
   tocar N partes dependientes. Dos dosis de retrabajo (tocar 1 vs tocar 4). Esperado: asimilación alta
   en ambas (working model lo registra), propagación cayendo con el retrabajo. El vicio = brecha entre
   lo que el modelo ya sabe (Mbelief) y lo que el entregable refleja (Mdeliver) — F vs F_prop, métricas
   que ya tenemos.
2. **Mezcla conflictiva bien hecha** — el mismo reporte rutinario trae evidencia contradictoria Y
   confirmatoria, con volumen/posición igualados contra los controles (lección Context Rot). Montable
   sobre overgen_stream ya existente.
3. **Ingrediente social — solo con ronda de diseño previa (Codex)**: la palanca más grande (0→99.2%) y
   la más riesgosa: hay que meter deliberación de forma NATURAL sin importar "presión sicofántica por
   instrucción". No tocar código antes de esa ronda.

Transversal: métricas graduadas siempre (F, ΔRegret) — los efectos frontier son graduados; contar
"mordidas" binarias es el error de los benchmarks que solo muerden con modelos chicos.

## 6. Lectura estratégica

La relectura MEJORA la posición del proyecto: (a) los nulos pasan de fracasos a controles replicados —
interpretables y citables; (b) el hueco en la literatura se re-confirma vacante y ahora se sabe qué
receta lo llena; (c) la intuición original de fricción-como-retrabajo resultó ser el eje que la
literatura señala (notar-sin-propagar) y nadie mide con consecuencias.

Pendiente menor detectado: en `docs/vicios/vicio-1.md` el caso Barkett figura con N=6.500 en la anatomía
y N=4.000 en §1.B; el correcto es 6.500 (fix de una línea, esperando OK).
