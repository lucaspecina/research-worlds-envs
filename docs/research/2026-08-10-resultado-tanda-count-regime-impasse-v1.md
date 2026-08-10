# Resultado — tanda count_regime_v1 (el episodio del impasse): la reestructuración es UNIVERSAL en la entrega, y el resumen del fallo NO acelera la postulación — la INVIERTE

> **Alcance del titular** (ADR 0152): 1 modelo (gpt-5.4) × 1 mundo (quiebre de pendiente fuera
> del envolvente histórico) × n=10 por brazo × 1 dosis (2 pilotos) × sin ayuda. Ficha congelada
> + 3 addenda ANTES de correr: [ficha](2026-08-09-ficha-mundo-count-regime-v1-impasse.md).
> Corridas: técnico 99556 + tanda 30 brk (99521-99550, 3 brazos apareados) + 4 smooth
> (99551-99554). Costo ≈ USD 14. Crudos en `scripts/out/count_regime_impasse_v1/`.
> Análisis pre-registrado: `scripts/analyze_count_regime_impasse_v1.py` (cero-LLM).

## Los números

| Brazo (qué recibe con el piloto) | Expansión generativa* | S entrega (media) | Familia régimen en entrega |
|---|---|---|---|
| **RAW** (filas crudas, sin reporte) | **5/10** | **0.670** | 10/10 |
| **VISIBLE_GLOBAL** (+ desajuste global del modelo registrado) | 2/10 | 0.582 | 10/10 |
| **VISIBLE_ESTRUCTURADO** (+ tabla de residuos por velocidad) | 3/10 | 0.631 | 10/10 |
| Gemelo (sin régimen; RAW y ESTRUCTURADO) | — | S_clean 0.90-0.93 | **espurio 0/4** |

\* pre-registrada: candidata de familia régimen registrada ANTES de que la evidencia dicte
(ΔBIC ≥ 6 con lo que el agente tenía en ese momento). Validación por lectura de código: 24/30
primeros eventos "régimen" son DOS LEYES genuinas (bisagra/umbral explícito), y 9/10 de las
expansiones son postulaciones reales (la excepción: GLOBAL 99534, polinomio flexible → con el
criterio estricto GLOBAL queda 1/10; no cambia ninguna conclusión).

## Hallazgo 1 — El episodio del impasse produce reestructuración en TODOS (30/30)

Contra el 0/9 de count_mix (generación espontánea sin fallo) y el 2/5 de la v0 (aceptación con
evidencia dictante), el protocolo completo — M0 propio registrado → piloto rutinario que lo
falla a la vista → autorización de zoom → segundo piloto contra el remiendo — llevó a **los 30
episodios a entregar la familia de dos leyes** (S̄ 0.58-0.67; el mejor 0.82), y el gemelo quedó
limpio 4/4 (ni la tabla de residuos indujo fantasmas — el miedo bilateral de la compuerta C,
despejado). La cadena diseñada funcionó entera: 30/30 registraron M0 antes del piloto
(el aviso de calendario alcanza), hubo re-registro tras los golpes, y **7 episodios intentaron
cerrar ANTES del segundo piloto** (rebotaron por la compuerta y quedaron en la cadena — cierre
prematuro elicitado y observable, de regalo).

## Hallazgo 2 — H-V1 INVERTIDA: el resumen mecánico del fallo NO adelanta la postulación estructural

La regla firmada era *"señal si VISIBLE − RAW ≥ 2 en expansión generativa"*. Dio **−3 (GLOBAL)
y −2 (ESTRUCTURADO)**: los brazos con reporte postularon las dos leyes MÁS TARDE (relativo a su
propia evidencia) que el brazo de filas crudas. Tres episodios de reporte registraron el régimen
con gap NEGATIVO o casi cero (la evidencia todavía favorecía la suave: conjetura pura), pero en
conjunto el patrón de cadenas muestra el mecanismo: **los de reporte compran el zoom autorizado
PRIMERO y registran después** (para cuando registran, su propia evidencia ya dicta → cuenta como
aceptación); **los de crudo conjeturan primero y verifican después**.

⚠️ **Esa lectura mecanística es POST-HOC** (no estaba pre-registrada): queda como hipótesis
rival a testear, no como conclusión. Lo pre-registrado y firme es el signo: **negativo**.

**Qué mata y qué no** (per addendum ratificado): muere *"la transparencia de la ESTRUCTURA del
fallo acelera la postulación estructural"* — para este sustrato, este modelo y esta dosis. NO
muere la teoría del impasse en general: **los tres brazos tenían el fallo a la vista en las
filas** (el piloto con media ~11 contra predicción ~7.5 lo ve cualquiera que compare), y bajo
ese fallo compartido la reestructuración fue universal — lo cual es CONSISTENTE con
fallo→reestructuración. Lo que los brazos manipulaban era el RESUMEN, y el resumen no aceleró:
reorientó (verificar-antes-de-comprometer).

## Hallazgos 3 y 4 — las otras dos microhipótesis firmadas cayeron

- **H-V2** (*"en RAW la tasa de familia nueva ≈ 0, la continuación del 0/9"*): **REFUTADA** —
  RAW 5/10 en expansión y 10/10 en entrega. Con el fallo del modelo propio a la vista, el mismo
  modelo que daba 0/9 sin fallo postula estructura. (Ya estaba marcada exploratoria por el
  addendum anti-recencia: count_mix no estimaba RAW acá. Igual: el contraste con-fallo/sin-fallo
  entre mundos es el dato más fuerte de la corrida.)
- **H-V3** (*"las expansiones llegarán tras el SEGUNDO fallo — persistencia"*): **REFUTADA** —
  29/30 postularon el régimen ANTES del piloto 2. Un solo fallo + la autorización de zoom
  alcanzó; la persistencia no fue necesaria para gpt-5.4 en este mundo.

## Explicaciones rivales VIVAS (obligatorias antes del titular)

1. **Especificidad de modelo**: todo es gpt-5.4. DeepSeek mostró en v0 el descarte ("outlier");
   su curva puede ser otra. La réplica con segundo modelo estaba prevista para DESPUÉS de la
   señal — y señal hay.
2. **La métrica de expansión puede estar midiendo ESTILO** (conjetura-primero vs
   verificar-primero), no capacidad generativa — la inversión sería entonces un efecto del
   reporte sobre la POLÍTICA DE COMPRA, no sobre la generación. Testeable leyendo si la
   conjetura precede a la compra en las trazas (como en v0).
3. **Techo de dificultad**: con el zoom autorizado tras el piloto, la evidencia comprable
   discrimina rápido (por diseño: alcanzabilidad) — el mundo puede ser demasiado resoluble para
   separar los brazos en la entrega (todos llegan). La separación viviría solo en el timing, que
   es justo donde apareció.
4. **La cerca como co-tratamiento**: la autorización de zoom llega CON el piloto 1 — el evento
   "fallo" y el evento "se abre la ventana de compra" están confundidos por diseño (idéntico
   entre brazos, así que no toca el contraste primario, pero sí la lectura absoluta de "qué
   disparó la postulación").

## Nivel arriba

- **Aprendizaje real**: el mismo modelo que da 0/9 sin fallo reestructura 30/30 con el fallo
  del modelo PROPIO a la vista — el elicitor que faltaba era el impasse, no la capacidad. Y el
  detalle del resumen importa menos que el fallo mismo: darle al agente la tabla de residuos no
  lo hace postular antes; lo hace verificar antes.
- **Límite del claim**: un modelo, un mundo, una dosis, n=10/brazo; "expansión generativa" es
  timing mecánico (validado 24/30 por lectura de código, pero timing al fin); la lectura
  conjetura-vs-verificación es post-hoc.
- **Explicación rival preferida por ahora**: el reporte induce política de verificación, no
  inhibición generativa.
- **¿Siguiente dólar?** El dossier va a Codex para MANTENER/MODIFICAR/PIVOTEAR. Candidatos:
  réplica con DeepSeek (¿la inversión generaliza?) · leer las 30 trazas para la firma
  conjetura-precede-compra · el mundo realista D1 (Onnes) que ya tiene cola.

## Ledger

✓ tanda 34/34 completa y analizada contra reglas firmadas · ✓ técnicos 1-3 documentados (2
fallas de operabilidad + 1 de constructo, cazadas antes de la tanda) · ✓ gemelo bilateral limpio
· VIVO: dossier a Codex · VIVO: validación semántica fina de las 30 trazas (los códigos ya
leídos mecánicamente; falta la lectura de prosa) · VIVO: mundo realista esperando diseño con
contexto a Lucas.

---

## ADDENDUM — el TECHO (crítica de Lucas, 2026-08-10, misma tarde)

*"¿Entonces el salto es muy fácil, no? No estamos haciendo nada interesante — por lo menos con
este mundo de juguete."* — Correcto, y queda registrado como lectura oficial del 30/30: **una vez
disparado, este salto es fácil; un mundo donde todos llegan no discrimina capacidad**. Y no es
accidente: la compuerta de alcanzabilidad certifica mundos resolubles por construcción, y una
curva 1D donde los residuos apuntan al arreglo es el peldaño de distancia mínima. El valor de la
corrida queda acotado a: (1) cerrar la pregunta del DISPARADOR (0/9 sin fallo → 30/30 con fallo,
mismo modelo y misma estructura); (2) la inversión del reporte; (3) la maquinaria probada.
**La pregunta del programa pasa a ser: ¿el impasse alcanza cuando el candidato está LEJOS?**
(predicción de Ohlsson, Principle of Scope: la tasa cae con el alcance). Escalera: disparador
fijo, distancia creciente — firma ambigua (Onnes) · operadores compuestos (2-4) · candidato
fuera del menú nombrable · el salto que NO agrega (borrar/re-anclar, Thagard).
