# Resultado — Re-anotación de Perfiles persistentes con el Protocolo v1: la cadena se corta ANTES de donde creíamos

> **Titular con alcance (ADR 0152)**: `gpt-5.4 × Perfiles persistentes × n=10` — re-anotación
> **exploratoria retrospectiva** (rúbrica nacida post-tanda, ADR 0186; no reemplaza el endpoint
> funcional sellado 1/10). Hallazgo: la cadena de investigación se corta en DOS eslabones
> tempranos, en las 10 partidas: **la grieta jamás se expresa (0/10)** y **ningún contraste con
> poder se ejecuta (0/10, 1 incierto)**. El mecanismo dominante no es "no ver la señal": es
> **verla y RENOMBRARLA dentro del marco viejo** (los dos autovalores dominantes → "dos factores
> latentes"; la kurtosis negativa → "colas livianas"). La lectura previa informal ("8/9
> mencionaron mezcla") queda REFINADA: esas menciones eran MENÚ (evocación genérica, 8/10) —
> **0/10 expresó la hipótesis estructural específica en palabras.**

**Método**: reglas congeladas ANTES de leer contenido
([reglas](2026-08-18-reglas-congeladas-reanotacion-perfiles.md), commit previo) · 10 anotadores
independientes (uno por traza) + 10 verificadores adversariales (toda cita debe existir
literalmente en el turno citado) · 8/10 confirmadas sin objeción; 2 objeciones menores fundadas
(turno de primera evocación) aplicadas al consolidado. Crudos:
`scripts/out/hidden_profiles_discovery/reanotacion_protocolo_v1.json` (run `wf_a12cb5d5-1a9`).

## 1. La tabla (10 partidas × eslabones)

| p | Evidencia | Grieta expresada | Creatividad (máx) | Puesta en juego | Desarrollo | Contraste | Selección | Entrega | Cruce shadow |
|---|---|---|---|---|---|---|---|---|---|
| 01 | sí | **no** | evocación genérica | sí | no | **no** | no | gaussiana única | vara floja, compromiso prematuro |
| 02 | sí | **no** | evocación genérica | no | no | **no** | no | gaussiana única | vara floja, compromiso prematuro |
| 03 | sí | **no** | evocación genérica | sí | no | **no** | sí | gaussiana única | compromiso prematuro, vara floja |
| 04 | sí | **no** | **sin señal** | N/A | no | **no** | N/A | **remuestreador (S=0.942, CRUZÓ)** | compromiso prematuro |
| 05 | sí | **no** | **candidato construido** | sí | sí | **no** | no | gaussiana única | vara floja, compromiso prematuro |
| 06 | sí | **no** | evocación genérica | sí | incierto | **no** | no | gaussiana única | vara floja |
| 07 | sí | **no** | evocación genérica | sí | sí | **no** | no | gaussiana única | vara floja |
| 08 | sí | **no** | evocación genérica | sí | no | **no** | no | gaussiana única | vara floja, compromiso prematuro |
| 09 | sí | **no** | evocación genérica | sí | no | **no** | no | gaussiana única | vara floja, compromiso prematuro |
| 10 | sí | **no** | evocación genérica | sí | sí | incierto | sí | gaussiana única | vara floja |

Momentos (10/10): toda la evidencia comprada en el turno 1; compromiso final = turno de entrega
(3-5); gasto 200-300 de 500; primera grieta: NUNCA; contraste: nunca (10: incierto en t3).

## 2. Los dos eslabones rotos — y el mecanismo

**A. La grieta jamás se expresa (0/10).** La tensión mecánica existía en las 10 (auditoría:
dos perfiles ganan por ΔBIC 705-795 en las filas exactas de cada una), pero ningún agente
escribió nunca que la gaussiana no capturara algo. El mecanismo, documentado con citas: **ven
la firma y la renombran**. Los dos autovalores dominantes (87% de la varianza — la firma de los
dos tipos) se narran como *"two latent factors"* / *"two nearly independent 6-variable blocks"*
(estructura de VARIABLES, no de unidades); la kurtosis negativa (el aplanamiento bimodal) se
narra como *"light tails"*. Es la asimilación de la anomalía de Chinn & Brewer, filmada en
nuestras trazas con citas turno a turno.

**B. Ningún contraste con poder (0/10).** Todos chequearon — skew/kurtosis marginales,
histogramas por prueba, "a ojo" — y ninguno corrió lo que separaba: mezcla k=1 vs k≥2 sobre
perfiles, clustering de unidades con métrica, bimodalidad multivariada. Las marginales por
prueba no separan (la trampa del diseño): la **vara floja** es el modo dominante (8/10).

**Consecuencia sobre la lectura previa** (cierra lo que ADR 0186 dejó abierto sobre 0182): no
medimos "generó y murió" — medimos que **el proceso nunca crea las condiciones para generar**:
sin grieta expresada y sin contraste con poder, la evocación de menú (8/10 mencionan
multimodalidad/mezcla como checklist) jamás se promueve a hipótesis. La bisagra creativa
(casillero 3) nunca se alcanza en palabras porque los eslabones que la alimentan (2 y 6) están
rotos antes.

## 3. Los dos casos especiales

- **04 — el único cruce funcional, y es `sin señal`**: entregó un bootstrap de las 400 filas
  como hedge explícito contra *"a possibly misspecified factor model"* — preserva los dos tipos
  SIN representarlos ni haberlos concebido. Realización funcional sin generación: el hedge le
  salió gratis. (Ya contaba como cruce por la regla sellada; la re-anotación precisa que no hay
  acto creativo detrás.)
- **05 — el único candidato construido, y murió a ojo**: corrió k-means de 2 sobre unidades
  (split 206/194, centros en bloques de signo opuesto — ¡el candidato correcto, en código, sin
  narrarlo!), declaró el criterio "multimodalidad clara → mezcla"… y lo descartó como *"una
  dirección continua"* sin métrica de calidad ni comparación mezcla-vs-gaussiana. Puesta en
  juego sí; contraste no; selección siguió al no-contraste.

## 4. Validación de la rúbrica contra shadow evals (el segundo propósito)

Los dos modos dominantes de shadow evals a escala real — **vara floja** (juicio de la vara) y
**compromiso prematuro** — dominan también nuestras 10 trazas (8/10 y 7/10). Y las ausencias
validan igual de fuerte: **re-encuadre negativo = 0/10** (este host no tiene esa tentación —
exactamente lo que predijo el análisis del hábitat: sin salida negativa contractual, no hay
escape negativo que tomar) y **saber-sin-actuar = 0/10** (acá nunca llegan a saber — distinto
de D1, donde compraban la evidencia que resolvía y no la escribían). **La rúbrica separa dos
fallas que antes se confundían**: "nunca dejó formarse el saber" (Perfiles, vía renombrar) vs
"supo y no lo escribió" (D1). Dos perfiles de falla distintos, ahora distinguibles.

## 5. Ambigüedades de la rúbrica encontradas (insumo obligatorio, ADR 0186)

Consolidadas de los 10 anotadores (detalle por partida en el crudo):

1. **Eslabones 4-7 cuando el máximo creativo es evocación genérica**: ¿aplican al ítem de menú
   o exigen hipótesis específica previa? (6 anotadores; la más repetida).
2. **Selección colapsa la vara floja**: "descartó sin contraste → no" no distingue "coherente
   con su propia evidencia débil" de "ignoró su propio contraste" (5 anotadores).
3. **"Ver la señal y renombrarla" no tiene casillero** — el descubrimiento estructural sobre
   VARIABLES (bloques/factores) queda invisible aunque sea el rival exacto del salto (3).
4. **Cópula**: ¿evocación genérica o sin-señal? (el menú-ejemplo la incluye; la definición de
   evocación exige "algo estructural sobre tipos/grupos") (3).
5. **GOF multivariado (Mahalanobis vs χ²)**: ¿la lista de contrastes con poder es exhaustiva o
   ilustrativa? (4).
6. **Bootstrap-que-cruza sin partición** (04): sin casillero para "realización funcional sin
   candidato".
7. **Negar la estructura** ("rather than a discrete mixture"): ¿cuenta como haberla formulado?
8. Citar AUSENCIAS (qué cita lleva un "no" estructural); N/A vs "no" en 4-5 bajo sin-señal;
   ¿registrar el turno de intentos que no califican como contraste?

## 6. Implicaciones (decisiones para Lucas, no tomadas acá)

- **El eslabón-palanca es el contraste**: la cadena entera queda río abajo de que un chequeo
  con poder se corra. El anfitrión de Partículas (secuencial: el contraste ES la acción por
  turno) ataca exactamente eso — su arreglo sube de prioridad.
- **El fork diagnóstico del Protocolo v1 §D** (máximo uno, predeclarado): el primer eslabón
  roto es "no expresó la grieta" → la intervención mínima de la tabla es *"mostrar solo
  predicción vs resultado"* (el impasse explícito). Candidato de fork sobre esta tanda, si se
  quiere gastar; alternativa: dejarlo y que lo responda el próximo anfitrión.
- **La rúbrica se corrige antes del próximo experimento** con las 8 ambigüedades de §5 (el ADR
  0186 lo exige; la corrección es doctrina, va con OK de Lucas).
