# Re-evaluación del proyecto — posición de Claude/orquesta (2026-07-31)

> Producida con orquesta propia: 4 auditorías del repo (activos, resultados, proceso, posición
> competitiva) → 4 estrategias independientes (paper-first, ciencia-first, abogado-del-diablo,
> realista-de-recursos) → 3 verificadores adversariales atacando las propuestas (2 de 4 NO
> sobrevivieron enteras). Crudo en el journal del workflow (11 agentes). INDEPENDIENTE: escrita
> sin leer `2026-07-31-reassessment-claude.md` (otra sesión Claude) ni
> `2026-07-31-reassessment-pivote-codex.md`; el cruce viene después.

## 1. Diagnóstico (dónde estamos de verdad)

**El proyecto convergió, no derrapó.** Cinco pivotes en ~52 días, cada uno achicando el alcance,
terminaron en una pregunta medible, un instrumento validado (fork apareado + replay determinístico
+ freno de calibración que PASÓ) y una pasada metodológicamente madura (252/252, pre-registrada,
~US$27). Eso es un activo raro: casi ningún vecino de la literatura tiene esta disciplina.

**Pero el estado honesto del inventario tiene grietas que las auditorías destaparon:**

1. **El hallazgo estrella está confundido POR CONSTRUCCIÓN.** En la pasada 1, la evidencia
   "mezclada" traía la MITAD de las observaciones diagnósticas que la limpia (el gate exigía
   dosis 2×) y el oráculo de F se construyó con el bundle limpio para TODOS los brazos. "La
   evidencia sucia domina" mezcla tres cosas: menos contenido + dilución + denominador. El
   número F 0.97-vs-0.14 NO sobrevive a un revisor hostil tal como está.
2. **La consecuencia global casi no cobra** (ΔR≈0 en casi todas las celdas): todo el efecto vive
   en el score local congelado. El claim "con consecuencias" necesita o re-pesar la batería o
   decirse honesto ("proper score local sobre la región relevante").
3. **Las 28 no-entregas (11%) están sin clasificar y se concentran en celdas informativas** —
   censura potencialmente informativa que contamina cualquier lectura.
4. **Inventario engañoso**: los mundos de la nota llevan check.json byte-idéntico heredado del
   esqueleto (certifica la física, no el par); el e0_summary del decoy dice "NO EMERGE" porque
   corre el detector del pozo, no el de mezcla-de-compromiso; hay una carpeta basura
   (logistic_growth_v0) y dos mundos muertos que cuentan como hechos.
5. **La pasada 2 "vivida vs atribuida", tal como está la maquinaria, es IRREALIZABLE**: el fork
   actual convierte TODA trayectoria en log neutral ("jamás mensajes con rol assistant") — el
   brazo "vivido" no existe todavía. Y aunque exista, vivida = contexto más largo → cualquier
   positivo se explica por Context Rot sin un control de longitud igualada.
6. **El gate del segundo modelo probablemente falla**: DeepSeek tuvo 4/10 fallas de entrega en
   esta clase de mundo y el pre-registro exige 9/10 válidas. No hay plan B presupuestado.
7. **Del lado bueno**: el kit reutilizable es real y verificado (fork resumible, analizador
   pre-registrado, red-team del score con piso 0.25σ, sondas maduras, reward cero-LLM con ~153
   tests verdes), el pool de donantes existe (14 elegibles + lab largo con obra registrada,
   ~9 elegibles), y la ventana competitiva sigue abierta pero es estrecha.

**Sobre el pivote radical** (abandonar ya el eje carga/autoría): el abogado del diablo lo argumentó
con "8 nulos consecutivos", pero el ataque de coherencia lo refutó — esa cuenta infla mezclando
nulos de OTROS fenómenos (el pozo es otro vicio, cerrado por su propia regla de muerte; las pistas
eran elicitación por instrucción). Los nulos LIMPIOS sobre carga son dos (etiquetas de autoría y
compromiso), ambos de carga *atribuida*. El eje carga merece exactamente UN test más — el vivido —
bien hecho y barato, no el abandono ni la fe.

## 2. La decisión estratégica (mi postura)

**Ni pivote radical ni continuación inercial: blindar-y-decidir.** El proyecto tiene UN hallazgo
candidato (la calidad probatoria domina la actualización aplicada) y UNA hipótesis viva (la carga
vivida frena donde la atribuida no). Los próximos 90 días se dedican a (a) volver inatacable el
hallazgo, (b) darle al eje carga su test definitivo con instrumento capaz de medirlo, (c) replicar
lo que sobreviva en segunda física y segundo modelo, (d) escribir. **Nada nuevo se construye salvo
lo que estos cuatro puntos exijan.**

## 3. El plan (con las correcciones de los ataques integradas)

**Fase A — Higiene bloqueante (semana 1, ~US$0):**
commitear la evidencia suelta · clasificar las 28 no-entregas con reglas escritas ANTES de mirar
(técnica vs conductual; modelo barato) · arreglar el inventario engañoso (acta de congelamiento de
overgen; check heredado marcado como tal en los mundos nota; borrar la carpeta basura; anotar el
e0_summary del decoy) · re-análisis GRATIS de la pasada 1: estratificar por régimen basal del
donante (lección BASIL) y medir la brecha declara-vs-entrega en las replies ya guardadas.

**Fase B — Blindar la celda firme (semanas 1-3, ~US$40-60):**
el experimento discriminante con el diseño corregido: (i) CLEAN vs MIXED con **contenido
diagnóstico IDÉNTICO** (misma evidencia, solo cambia el relleno), (ii) control de **longitud
igualada** (mismos tokens, distinta dosis), (iii) brazo **RETAIN** (evidencia confirmatoria donde
lo correcto es NO moverse) con **ΔRegret como métrica primaria** (funciona en las tres
direcciones; F pasa a secundaria, con oráculo POR BRAZO, no el del bundle limpio), (iv) posición
del relleno contrabalanceada. Responde a la vez la objeción por-construcción y la alternativa
Context-Rot, y vuelve bilateral la medición. Advertencia del ataque integrada: "mantener" es la
acción nula — el brazo RETAIN se lee junto con un chequeo de que el modelo procesó la evidencia
(¿la menciona? ¿compra el chequeo?), no solo por la entrega.

**Fase C — El test definitivo del eje carga (semanas 3-6, ~US$40-60):**
construir el **fork-continuación** (la variante que preserva la conversación original con roles
assistant — la maquinaria de las sondas viejas ya replayaba así; es adaptación, no construcción
nueva) · escalera de tres escalones: continuación nativa / snapshot del mismo contenido /
etiqueta · **control de longitud igualada entre escalones** (snapshot inflado con relleno neutro)
para separar contenido-de-trayectoria de largo-de-contexto · pool: engordar lab largo (+8-12
episodios, ~US$15) ANTES, con el filtro de elegibilidad medido · manipulation check fuera del
reward (¿las entregas difieren byte a byte entre brazos? si no difieren, la manipulación no llegó
y la celda no se lee) · criterio de muerte del eje FIRMADO antes de correr.

**Fase D — Réplica de lo que sobreviva (semanas 6-10, presupuesto REALISTA):**
segunda física con timebox duro y costo honesto (la base rate del propio repo es 2-3 rondas de
calibración por mundo — se presupuestan, no se niegan) · segundo modelo con plan B explícito
(si DeepSeek falla su gate de 9/10: canonicalizador determinístico y/o un segundo frontier;
decisión pre-firmada, no improvisada).

**Fase E — Escribir (semanas 8-12, US$0 API):**
workshop paper / informe técnico arXiv con los claims escoping-ados a lo que sobrevivió; la tabla
comparativa sale de docs/posicionamiento-revision-de-creencias.md; ambos resultados de la Fase C
son publicables (efecto de carga vivida = el resultado nuevo; nulo limpio = la nota deflacionaria
"la carga no frena, la señal manda" — también valiosa).

## 4. Qué se mata / congela (con acta, no en silencio)

overgen_v0 + gemelo (WIP fantasma: check en rojo, ni una ronda más) · fábrica y piloto Tubinga
(pausados siguen) · cartera E1 vieja y 8 slots por autorar · mundos de aha, resolubilidad,
Neptuno/Vulcano (diferidos post-paper) · E0 de final_note_true_v0 y variantes con-formas ·
adaptación del score martingala (cara, no núcleo) · dos titulares en su forma actual ("F≈0.97"
y "la evidencia sucia domina") hasta que la Fase B los re-escriba con el diseño corregido.

## 5. Criterio de abandono (pre-registrable hoy)

Se CIERRA la línea "mapa de carga" (y se escribe el negativo con el mismo rigor) si se cumplen
las tres a la vez al cierre de la Fase C/D: (1) el control de relleno explica ≥50% de la caída
clean→mixed (el fenómeno era contexto, no juicio), (2) la carga vivida da plana (mediana apareada
~0, ≥12 pares válidos POST-clasificación de censura, CON manipulation check positivo), (3) la
celda firme corregida no replica en la segunda física o el segundo modelo. Si (1) y (2) matan
pero (3) replica, el proyecto pivotea con honra a la nota corta "calidad probatoria domina, la
carga no frena" y la infraestructura queda disponible para otra pregunta.

## 6. Mejoras de proceso (lo que la auditoría de proceso dejó)

- **Lo que funcionó y se mantiene**: pre-registros firmados antes de mirar · pares/polos ·
  regla de muerte pre-firmada · Codex como crítico externo · titulares-con-alcance ·
  ledger de pendientes.
- **Lo nuevo**: (i) *acta de congelamiento* obligatoria al pausar un WIP (el inventario engañoso
  nació de pausas silenciosas); (ii) los artefactos heredados (check/e0_summary copiados) se
  marcan HEREDADO en el archivo mismo; (iii) presupuestar réplicas con la base rate propia
  (2-3 rondas), no con optimismo; (iv) máximo UN experimento en vuelo por vez — la cola única
  ya existe, respetarla.
