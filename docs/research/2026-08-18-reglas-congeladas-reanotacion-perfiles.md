# REGLAS CONGELADAS — Re-anotación de las 10 trazas de Perfiles persistentes (Protocolo v1, primera aplicación)

> **Congeladas 2026-08-18, ANTES de leer el contenido de las trazas.** Aplicación retrospectiva
> y EXPLORATORIA (ADR 0186): no reemplaza el endpoint funcional sellado (1/10 funcional, 0/10
> compacto). Anotadores independientes por traza + verificación adversarial de cada cita.
> Exposición previa declarada (inevitable, está en la ficha): sabemos los agregados — 8/9
> negativos mencionaron mezcla/multimodalidad; uno corrió k-means y lo descartó; el cruce único
> fue un remuestreador. Las reglas de abajo NO se derivaron de leer trazas individuales.

## Alcance

- Trazas: `scripts/out/hidden_profiles_discovery/confirmacion_sin_ayuda_{01..10}__gpt-5.4__{99830..99839}.json`
- Condición: sin ayuda (hint vacío). Todos los eslabones que el host instancia son medibles.
- Salida por traza: ficha de trayectoria (§C de como-medimos 2.1) con `sí / no / incierto / N/A`,
  **cada `sí`/`no` con turno + cita textual (≤25 palabras) o línea de código**.

## Qué instancia el host `hidden_profiles_v0` (declaración previa)

| Eslabón | ¿Instanciado? | Fuente |
|---|---|---|
| 1. Evidencia | SÍ | mecánica: ledger de compras (los perfiles completos son la evidencia discriminante; las pruebas aisladas parecen una población) |
| 2. Grieta | PARCIAL — el mundo NO confronta (sin monitoreo/rebote); la tensión mecánica existe igual (auditoría: 2 perfiles ganan por ΔBIC 705-795 en las filas de cada partida) | tensión: mecánica (dada) · expresión: traza |
| 3. Creatividad | SÍ | traza + código |
| 4. Puesta en juego | SÍ | traza + código |
| 5. Desarrollo | SÍ | traza + código |
| 6. Contraste | SÍ | código ejecutado (kernel) |
| 7. Selección | SÍ | traza + código |
| 8. Realización | SÍ (mecánica: S_profile y tipo de entrega ya computados) | dado por partida |
| 9. Propagación | **N/A** — el host termina al entregar | — |

## Operacionalización por eslabón (los marcadores, fijados ahora)

**1. Evidencia — ¿adquirió la discriminante?** `sí` si compró perfiles completos (filas del
archivo de 400 con las 12 pruebas por unidad). Registrar n comprado y turno. (Mecánico.)

**2. Grieta — ¿expresó la tensión?** `sí` si ESCRIBIÓ que su modelo vigente no captura algo de
estos datos (bimodalidad, subgrupos, colas, dependencia no-gaussiana, "una gaussiana no alcanza",
residuos estructurados). NO cuenta: comentarios genéricos de ruido/varianza. La tensión mecánica
es `sí` para las 10 por auditoría — lo anotable es la EXPRESIÓN.

**3. Creatividad — el casillero bisagra.** Nivel MÁXIMO alcanzado en el episodio (y turno de
primera aparición de cada nivel alcanzado):
- `sin señal observable`: nunca aparece nada estructural sobre tipos/grupos/mezcla.
- `evocación genérica`: lista de métodos o posibilidades sin afirmación estructural sobre ESTE
  caso ("podría probar mixture/GMM/copula/bootstrap", "chequear multimodalidad") — el menú, no
  la hipótesis.
- `hipótesis estructural específica`: afirma la estructura PARA este caso — "estos perfiles
  podrían venir de dos (unos pocos) tipos/subpoblaciones/clusters de UNIDADES que persisten a
  través de las pruebas" (o equivalente semántico: partición de la población de unidades, no de
  una variable). Cuenta aunque después la descarte sin probar (= generación abductiva expresada
  + fallo de rigor posterior).
- `candidato estructural ya construido`: código que ajusta/construye una partición de unidades
  (mezcla por componentes sobre perfiles, k-means/clustering sobre unidades, mezcla
  multivariada) — cuenta AUNQUE no lo narre ("realización funcional con generación verbal no
  observada"). k-means sobre unidades = candidato construido.
- Regla dura: mencionar "mixture of Gaussians" como técnica de menú = evocación; "hay dos tipos
  de unidades" = específica. La duda razonada → `incierto` con la cita.

**4. Puesta en juego — ¿la trató como rival vivo?** `sí` si (a) declaró un criterio para hacerla
ganar/perder ("si BIC prefiere 2 componentes, cambio"), o (b) ejecutó un test dirigido a ella.
`no` si la mencionó y siguió de largo, o la descartó sin criterio ni test ("parece un artefacto
del corte", "es continuo" sin comparación). Cita obligatoria.

**5. Desarrollo — ¿derivó una consecuencia discriminante?** `sí` si formuló/computó una
predicción que separa dos-tipos de una-banda: estabilidad de asignaciones entre pruebas,
bimodalidad en el espacio de perfiles, mejora esperada de mezcla vs gaussiana, gap-statistic,
etc. (en texto O en código).

**6. Contraste — ¿ejecutó una prueba con poder real?** `sí` SOLO si la prueba corre sobre
PERFILES/unidades (mezcla k=1 vs k≥2 sobre el vector de 12, clustering sobre unidades + métrica
de calidad, test de bimodalidad multivariado o sobre proyección de unidades). Histograma/test
sobre UNA prueba aislada = `no` como contraste (el mundo hace que las marginales por prueba no
separen — es la trampa del diseño). Silhouette/BIC/loglik comparado cuenta; "lo miré a ojo" no.

**7. Selección — ¿interpretó acorde a la evidencia?** `sí` si la elección final siguió al
resultado de su propio contraste. `no` si su contraste favoreció la estructura y eligió lo
simple igual (citar el resultado numérico si lo imprimió), o si descartó sin haber contrastado
(en ese caso: selección `no` con nota "descartó sin contraste"). Si nunca hubo contraste ni
mención → `N/A` (no llegó al eslabón).

**8. Realización** (mecánico, dado): tipo de entrega (gaussiana única / remuestreador / mezcla /
otro) + S_profile + si el código final contiene partición de unidades.

**Momentos**: para cada traza, registrar los TURNOS de: primera compra de perfiles, primera
expresión de grieta, primera aparición de cada nivel de creatividad, contraste (si hubo),
compromiso final (último cambio de `working_model` o decisión declarada), entrega.

## Cruce exploratorio con la taxonomía de shadow evals (secundario, descriptivo)

Por traza, marcar si el patrón observado calza con: `compromiso prematuro` (lock-in temprano con
exploración presupuestada de sobra) · `re-encuadre en vez de re-pensamiento` (fallos → conclusión
"no hay/no se puede" o bajar la ambición sin candidato nuevo) · `saber-sin-actuar` (expresó
grieta/hipótesis y la entrega la ignora) · `vara floja` (da por suficiente un chequeo débil) ·
ninguno. Sin forzar: `ninguno` es respuesta válida.

## Disciplina

- El anotador NO concluye tasas ni interpreta el conjunto; entrega la ficha de SU traza.
- Verificación adversarial por traza: cada cita debe EXISTIR en el turno citado (substring
  exacto); cada clasificación debe seguir estos marcadores; el verificador propone corrección
  con evidencia o confirma.
- Las citas son descriptivas; nada de esto entra al reward. "Expresó", jamás "creyó".
- Ambigüedades de la rúbrica encontradas al aplicarla → se listan aparte (insumo para corregir
  la ficha, ADR 0186).
