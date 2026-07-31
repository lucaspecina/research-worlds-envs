# Arquitecturas experimentales candidatas — Claude (2026-07-31)

> Ejercicio independiente (espejo del que hará Codex; se cruzan después). Etapa: razonamiento,
> sin contrato ni implementación. Marco: la pregunta oficial (ADR 0156) — asimilación /
> decisión / propagación, M0 → Mbelief → Mdeliver, dos varas + contrafactual C_B(Mbelief).

## 0. Posiciones sobre los cinco puntos abiertos de Codex

1. **El resultado interesante**: acuerdo con su formulación, y la afilaría así: el titular es
   el TRIÁNGULO — *el agente registró la creencia correcta, la reparación era alcanzable con su
   presupuesto, y la dejó sin hacer* — cuantificado como "correcciones dejadas sobre la mesa"
   (regret contra C_B(Mbelief)). **Guardia anti-trivialidad pre-registrada**: el claim solo
   cuenta si el control mecánico repara ≥X% en las mismas condiciones (si nadie puede reparar,
   no hay fenómeno, hay dificultad).
2. **Cómo observar Mbelief**: acuerdo con registro obligatorio idéntico entre brazos +
   declararlo como protocolo (medimos agentes-bajo-registro). La ablación sin-registro queda
   para después, anotada en el contrato como límite de alcance conocido.
3. **Qué mundo**: mi candidata converge con la suya (híbrido derivado de 5 líneas) — abajo la
   concretizo turno a turno, que es donde se decide si aguanta.
4. **Fricción**: acuerdo con inesperada-primero (propagación pura). Agrego: la fricción se
   dosifica en unidades calibradas por el control mecánico (costo como % del presupuesto
   restante), DOS niveles + control — no un continuo (potencia).
5. **Trayectoria**: acuerdo en que entra después; la manipulación válida dentro del mismo mundo
   es el diseño acoplado (yoked): constructor-activo vs observador-acoplado (recibe el MISMO
   log turno a turno, formato idéntico, sin elegir nada) vs adoptante-por-snapshot. El desafío
   es igualar el formato del contexto entre "yo hice X" y "el log dice que se hizo X" — se
   diseña en papel desde ya, se corre después del primer instrumento.

## 1. Arquitectura A — "El tablero con dependientes" (derivado 5-líneas; MI RECOMENDADA)

**Mundo**: las 5 líneas de siempre, con un cambio estructural: el brief declara que cada línea
sigue UNA de K=3 familias de forma conocidas (saturante / pico / lineal-con-meseta) con
parámetros en bandas declaradas. El espacio de hipótesis es explícito → M*belief es un
posterior EXACTO computable server-side.

**Turno a turno (≈14 turnos):**
- T1-5 (construcción): el agente compra datos (overview + pilotos + 1-2 campañas), forma su
  modelo. **T5 = REGISTRO OBLIGATORIO de M0**: formulario estructurado por línea — pesos sobre
  las 3 familias + parámetros puntuales + incertidumbre (el server lo convierte en mezcla
  ejecutable).
- T6-8 (dependientes): con helpers del server (que cuestan acciones), el agente construye 3
  artefactos DERIVADOS de su M0: (a) tabla de umbrales de alarma por línea, (b) política de
  asignación de slots del trimestre, (c) presupuesto de control de calidad. Cada uno queda
  asentado y es puntuable contra su versión-desde-la-verdad. → El artefacto final es MODULAR:
  5 modelos + 3 dependientes.
- T9 (evidencia, randomizada): tanda de filas nuevas sobre una línea, con dosis graduada
  server-side (LLR entre familias): refutatoria / confirmatoria / placebo / intermedia —
  formato y longitud idénticos.
- T10 = **CAPTURA OBLIGATORIA de Mbelief** (mismo formulario que T5, antes de cualquier
  acción). Recién acá se cierra la compra de datos.
- T11 (revelación de fricción, randomizada): brazo BAJO — una acción atómica `propagate()`
  reconstruye los 3 dependientes desde el modelo registrado (costo chico); brazo ALTO — cada
  dependiente debe reconstruirse por separado (3 acciones, costo material, presupuesto justo:
  alcanza pero duele); brazo CONTROL MECÁNICO — se le dicta el cambio exacto ("línea 3 pasa a
  familia pico con c=6.1; reconstruí los dependientes") con el mismo patrón de costos.
- T12-14 (reparación y entrega): decide qué repara; entrega Mdeliver (modelos + dependientes).

**Referencias**: M*belief = posterior exacto · M*deliver,B = programa dinámico chico sobre qué
reparar con el presupuesto restante · C_B(Mbelief) = mejor implementación de LA creencia que el
agente registró. **Métricas**: distancia de Mbelief al posterior (dirección/magnitud) ·
correcciones-dejadas-sobre-la-mesa (regret vs C_B) · score final contra la verdad ·
no-entregas/ inválidos como co-primaria.

**Por qué la recomiendo**: identificación máxima con costo mínimo — reusa física, scoring,
harness y donantes de calibración; el posterior exacto mata la objeción "oráculo heurístico";
los dependientes hacen la fricción MATERIAL sin inventar un universo nuevo. **Su riesgo** (el
que Codex nombró): "parece BayesBench con pasos extra". Defensa: BayesBench no tiene entrega
ejecutable, ni dependientes que reparar, ni costo, ni fork apareado — y nuestra figura central
(el triángulo creyó-bien / podía-reparar / no-reparó) no existe en su diseño. El riesgo real es
de RETÓRICA, no de sustancia — se administra en el paper, no en el diseño.

## 2. Arquitectura B — "La tubería" (artefacto = código modular con contratos)

El agente construye una tubería de procesamiento real (4 módulos: ingesta→limpieza→ajuste→
reporte) sobre los datos de las líneas; los módulos tienen contratos server-side. Fricción =
acoplamiento de código (brazo alto: cambiar el ajuste obliga a re-editar 3 módulos que se
re-validan con costo; brazo bajo: interfaces limpias). Evidencia y capturas como en A.

**A favor**: máxima validez ecológica (es trabajo de agente de verdad, habla el idioma del
notice-act de OpenAI). **En contra (decisivo hoy)**: mete la habilidad-de-editar-código como
confound gigante (la falla #1 que el propio corte del refoco quiere excluir), el oráculo de
"mejor reparación de código bajo presupuesto" es difícil de computar limpio, y exige construir
maquinaria nueva (contratos por módulo). **Veredicto**: NO para el estudio 1; es la réplica
ecológica natural DESPUÉS (y su miniatura ya está adentro de A: los 3 dependientes son la
versión chica y computable de sus módulos).

## 3. Arquitectura C — "La agenda" (creencia → decisiones irreversibles secuenciales)

T rondas donde el agente además de modelar COMPROMETE decisiones irreversibles (qué línea corre
en cada slot del trimestre) que consumen sus creencias; las decisiones pasadas restringen las
futuras (dependencias naturales); la evidencia llega a mitad; revisar = deshacer slots con
costo. Mide propagación hacia DECISIONES (pariente de KellyBench, en nuestro terreno).

**A favor**: la fricción emerge sola (no hay que fabricarla) y el canal decisión es el más
cercano a los despliegues reales. **En contra**: el óptimo bajo presupuesto es un programa
dinámico que crece feo, la calidad de PLANIFICACIÓN se mezcla con la revisión de creencias, y
el estimando se embarra justo donde el refoco lo quiere nítido. **Veredicto**: NO para el
estudio 1; es el candidato natural para el estudio POSTERIOR de fricción-anticipada (la
pregunta 4b de Codex — el costo conocido de antemano moldeando qué se registra).

## 4. Comparación y recomendación

| | A tablero+dependientes | B tubería | C agenda |
|---|---|---|---|
| M*belief exacto | SÍ (posterior) | con forma estructurada | difuso |
| Fricción material limpia | SÍ (calibrable) | sí pero confundida con código | emerge pero embarrada |
| Confound de habilidad | bajo | ALTO | medio |
| Costo de construcción | bajo (derivado) | alto | medio-alto |
| Distancia a BayesBench | retórica, no sustantiva | grande | grande |
| Sirve al claim central (triángulo) | directo | directo pero sucio | indirecto |

**Recomendación: A como anfitrión del instrumento y el estudio principal** (compuertas y
target×fricción+control-mecánico), con B como réplica ecológica posterior y C como el estudio
de fricción-anticipada futuro. Si el cruce con Codex converge en el híbrido, la discusión útil
que queda es sobre los DETALLES de A: el formulario exacto de registro, la escala de costos de
reparación, y cómo evitar que las 3 familias declaradas hagan el mundo adivinable.

## 5. Ataques que le hice a A (y quedan abiertos para Codex)

- ¿El registro de pesos-sobre-3-familias vuelve la asimilación demasiado fácil (multiple
  choice disfrazado)? Mitigación posible: parámetros continuos dentro de familia cargan la
  mitad de la dosis; el posterior es sobre familia×parámetros, no solo familia.
- ¿El agente puede ganar reparando TODO siempre (si el presupuesto alcanza, no hay decisión)?
  → calibrar para que reparar-todo cueste más de lo que rinde en el brazo alto (el programa
  dinámico lo verifica antes de correr).
- ¿`propagate()` atómico del brazo bajo es demasiado regalo (nadie falla)? — está bien QUE
  nadie falle ahí: es el techo del instrumento, no una celda de interés.
- ¿Tres dependientes alcanzan para "modularidad"? Para el estudio 1 sí (2 niveles de fricción);
  más granularidad = más potencia necesaria.
