# Re-assessment del proyecto — Claude (2026-07-31)

> Escrito SIN leer el re-assessment de la otra sesión (independencia; se cruzan después).
> Insumos: todo el arco del proyecto (155+ decisiones), la pasada 1 (ADRs 0154/0155), la campaña
> de lectura completa (16 papers + 4 repasos), y las notas de posicionamiento de Lucas.

## 1. Qué es el proyecto HOY, dicho sin piedad

**Lo que somos:** un instrumento causal funcionando (fork apareado + snapshot canónico + dosis
server-side + bases dobles + freno de calibración, validado en la pasada 1), dos familias de
mundo aptas (esqueleto 5-líneas; lab largo con registro de obra propia), una disciplina que la
industria acaba de validar (cero-LLM en el cobro; pre-registro; certificados), una pregunta
afilada que cuatro barridos independientes confirman VACANTE, y UN resultado medido (con su
confound señalado y su alcance declarado).

**Lo que también somos:** un proyecto que serpenteó durante semanas (el propio registro lo
documenta: pivotes semanales, aperturas sin cierre, y el episodio de habernos cazado el vicio 1
a nosotros mismos), con un problema de elicitación de fondo (a carga fabricable-en-episodio,
los frontier casi no fallan), mundos de juguete expuestos a la objeción ecológica, y una
ventana de novedad que se está cerrando (dos grupos a un paso de cruzar sus piezas con las
nuestras).

**El balance neto:** los activos son reales y el hueco es real; el riesgo dominante ya no es
"¿existe el fenómeno?" sino "¿lo medimos nosotros primero y con los controles correctos?".

## 2. Qué VALE de lo construido (los activos, en orden de valor)

1. **El instrumento de fork apareado** — la pieza que nadie más tiene apuntada a creencias.
   Costo marginal por experimento ridículo (~US$30/pasada en mundos cortos).
2. **El lab largo con REGISTER** — la única forma que tenemos de fabricar "obra propia
   construida de verdad" (la condición que TODA la literatura señala como la no-medida).
3. **La dosis server-side** (KL/logLR por bundle) — la diferencia entre "le mostramos algo" y
   "le mostramos exactamente X bits de evidencia"; nadie más la tiene en agéntico.
4. **La disciplina** (pre-registro con freno de calibración, cero-LLM, certificados, bases
   dobles) — pasó de excentricidad a estándar-de-facto (GeneBench-Pro la valida).
5. **La evidencia acumulada** (anatomía del vicio 1, mapa de timing, 252 forks, sondas) — todo
   reusable como pilotos/calibración de la pasada 2.
6. **El posicionamiento** (6 dimensiones + mapa de competidores de Lucas) — la introducción y
   la related work del paper ya están en borrador conceptual.

## 3. Qué NO vale (matar o congelar, explícito)

- **El catálogo de 9 vicios como programa activo** → CONGELADO como cantera documental. Somos
  un proyecto de UNA pregunta. El catálogo fue el camino hasta la pregunta, no el destino.
- **La familia del pozo** (rabbit_hole v0-v2 y variantes) → ACTIVO CERRADO: cumplió (dio el
  esqueleto y los donantes); su fenómeno propio (cavar de más) no es la pregunta actual.
- **El mundo de la sobre-generalización (WIP)** → CONGELADO en su estado; su temática (celda de
  compromiso-auto-generado) se hereda a la pasada 2 vía lab largo; el build a medio calibrar
  no se termina salvo que el mapa lo pida.
- **La fábrica / proto-designer** → sigue PAUSADA. Industrializar antes de tener el fenómeno
  medido es construir la imprenta antes que el libro.
- **La resolubilidad / mundos de aha** → DIFERIDOS (ya estaban). No tocan la pregunta.
- **Los mundos nota-final** → cumplieron como sonda ecológica (1/10 nativo); quedan como celda
  medida, sin más inversión.

## 4. ¿El proyecto se sostiene? — mi veredicto

**SÍ, con el claim estrechado y con velocidad.** La pregunta refinada (¿cómo interactúan valor
probatorio × trayectoria real × costo de reparación en la desviación entre actualización legal
y entrega?) está: (a) vacante — 4 barridos independientes; (b) instrumentada — todo lo
necesario existe en el repo; (c) blindable — los confounds conocidos (context rot, capacidad,
prior implícito, régimen basal) tienen control diseñado; (d) con demanda — labs pagando >US$1B/
año por ambientes y admitiendo que no saben medir juicio.

**Los riesgos que me quitan el sueño, con su mitigación:**
1. **Resultado nulo en trayectoria** (la etiqueta ya dio plano; Big-Muddy avisa que ni en
   viñetas la autoría sola muerde). Mitigación: el diseño bilateral hace el nulo PUBLICABLE
   (deflacionario: "toda la curva es señal + costo operativo") — pero SOLO si los controles
   están impecables. El nulo mal controlado no es nada.
2. **Scoop** — BeliefTrack (pares+cero-LLM+RL) y el grupo del replay causal están a UN paso.
   Mitigación: pasada 2 en semanas, no meses; preprint del instrumento apenas cierre, con
   cualquier resultado.
3. **Nuestro serpenteo** — el riesgo interno #1, histórico y documentado. Mitigación:
   gobernanza nueva (abajo, §6).
4. **Costo del lab largo** — forks con 100-200k tokens de contexto son ~10-30× más caros que
   los de la pasada 1. Mitigación: calibración triplete ANTES (gate barato), n por celda
   dimensionado por la varianza medida en pasada 1, y presupuesto techo pre-firmado.

## 5. LA PROPUESTA: pasada 2 como el experimento que decide el proyecto

**Mundo**: lab largo (14 rondas, registro de modelo provisional por línea, obra con
dependencias). Donantes nuevos corridos a propósito (los E0 existentes del lab largo son 0/10
en el vicio del pozo — sirven como semilla, pero la tanda de donantes se corre fresca con
REGISTER activo constante entre brazos).

**Diseño en dos etapas (gate en el medio):**

*Etapa A — calibración del triplete (el instrumento a prueba, barato):*
- En el checkpoint medio (ronda ~8: obra registrada + rondas por delante), tres inyecciones
  con formato/longitud/posición IGUALADOS: REVISE (evidencia que refuta una pieza del modelo
  registrado, dosis alta), RETAIN (confirmatoria/no-diagnóstica, misma forma), PARTIAL
  (dosis intermedia que amerita revisión parcial).
- Métrica primaria: **ΔRegret contra el oráculo legal** (bilateral; funciona en RETAIN);
  F secundaria donde la mejora legal ≥ ε; estratificación por régimen basal del donante;
  tres canales (declara/compra/entrega).
- **Gate pre-firmado**: el instrumento ordena REVISE > PARTIAL > RETAIN en |actualización
  justificada| y el RETAIN no induce movimiento > bases. Si falla → instrumento, no hipótesis;
  se arregla o se para.
- Costo estimado: ~10 donantes × 5 brazos (3 inyecciones + 2 bases) ≈ US$40-80 (contexto largo).

*Etapa B — los dos contrastes que deciden (solo si A pasa):*
1. **Trayectoria vivida**: continuación nativa de SU conversación (máxima trayectoria) vs
   snapshot canónico del mismo estado (la escalera completa nativa/snapshot/etiqueta si el
   presupuesto da). Cruzado con REVISE-diluida (contenido diagnóstico IGUALADO, relleno
   controlado por longitud y posición).
2. **Fricción material**: mismas inyecciones con 0 vs 3 aplicaciones downstream ya asentadas
   que la corrección invalida (rehacerlas cuesta presupuesto real) + el brazo gemelo de
   dificultad-de-edición-sin-dilema (para separar "no quiso" de "no pudo").
- Brazos comparadores: andamiaje estimar-verificar-actualizar (¿la ayuda de proceso recupera
  la actualización?) y el oráculo legal programático.
- Modelos: gpt-5.4 + DeepSeek (si pasa el gate de ≥9/10 entregas válidas); tercero si el
  presupuesto da.
- Costo estimado etapa B: US$150-300. Total pasada 2 ≤ US$400, techo pre-firmado.

**Criterios de muerte pre-firmados (van al pre-registro, adoptando los de Codex + míos):**
- Si el efecto de dilución desaparece al igualar longitud/posición → era contexto, no
  creencias: se reporta como tal y la línea "señal" se cierra.
- Si trayectoria nativa ≈ snapshot ≈ etiqueta EN TODO → no hay efecto de trayectoria a esta
  escala: se publica el resultado deflacionario con los controles como protagonistas y el
  proyecto pivotea (a la línea de fricción si ELLA dio señal, o a cierre elegante).
- Si el andamiaje recupera todo → es capacidad: hallazgo útil (para labs), no disposición;
  reencuadre del paper, no muerte.
- Si los efectos cambian de signo sin estructura entre donantes → n insuficiente o mundo
  inadecuado: UNA iteración de arreglo permitida, después se para.

**Después de la pasada 2, sea cual sea el resultado**: preprint del instrumento + pasada 1 +
pasada 2 (el instrumento y el mapa parcial SON publicables con nulo bien controlado), y ahí
recién decidir E2/entrenamiento (BeliefTrack demostró que el RL sobre recompensas de creencia
funciona y no rompe capacidades — pero primero el fenómeno).

## 6. Mejoras estructurales (la gobernanza anti-serpenteo)

1. **Regla de una rama**: máximo UNA línea exploratoria viva además de la pasada en curso.
   Todo lo demás: cantera, con fecha de revisión.
2. **Toda tanda nace con pre-registro + criterio de muerte + techo de gasto** (ya es práctica;
   pasa a regla escrita).
3. **Cadencia de cierre**: cada 2 semanas, un "corte de caja" — qué cerró, qué murió, qué
   sigue; contra la tendencia documentada a abrir sin cerrar.
4. **El paper como forcing function**: desde ya, un esqueleto de paper vivo (intro = nota de
   dirección; related work = posicionamiento de Lucas; método = pre-registros; resultados =
   se llenan por pasada). Escribir contra el esqueleto evita experimentos que no llenan
   ninguna sección.
5. **Vigilancia mensual** (no más): re-chequear los 2 grupos calientes y GeneBench v2. Un
   recordatorio, no una campaña.

## 7. Pivotes considerados y RECHAZADOS (para que conste que se pensaron)

- **Pivotear a tareas reales (código/data science)**: NO — perdemos dosis cuantificada e
  identificación causal, que son las dos únicas cosas que nadie más tiene. Las tareas reales
  entran DESPUÉS como validación de transferencia.
- **Pivotear a benchmark de capacidad científica** (competir con GeneBench): NO — commodity en
  dos años, cero diferencial, y OpenAI tiene 100× el presupuesto.
- **Saltar directo a entrenar (E2)**: NO — sin fenómeno medido no hay señal que valga la pena
  entrenar; y BeliefTrack ya se llevó el "RL sobre creencias funciona" genérico. Nuestro RL
  tendrá valor solo si entrena LA interacción (dosis × trayectoria × fricción).
- **Abandonar**: NO — la próxima tirada es barata (≤US$400, semanas), decisiva en ambas
  direcciones, y los cuatro barridos confirman que el centro sigue libre. Abandonar HOY sería
  regalar el instrumento en su mejor momento.
- **El pivote que SÍ hicimos y se consolida**: de "catálogo de vicios del científico
  artificial" a "mecánica causal de la revisión aplicada". Queda como identidad del proyecto.

## 8. En una frase

**WAGER hoy es un instrumento único apuntado a una pregunta vacante con ventana de tiempo
corta: la pasada 2 —lab largo, triplete calibrado, trayectoria vivida y fricción material,
con criterios de muerte firmados— es el experimento que convierte el proyecto en paper o en
cierre honesto, en semanas y por menos de US$400.**
