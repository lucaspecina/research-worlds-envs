# Mundo A — "La primera historia" (spec de trabajo — DECISIONES FIRMADAS)

> **Estado: APROBADO CON DECISIONES D1-D5 (ADR 0081; doctrina en ADR 0080).** Primer
> mundo anti-vicio = **slot #17 de la cartera** (D5). Vicios objetivo: *casarse con la
> primera hipótesis* (variante base) y *no incorporar evidencia nueva* (variante
> con-noticia, D4). Resoluciones: D1 contrafáctica SÍ + guarda anti-cínico (batería
> varía la ambiental real; rung negador-agnóstico); D2 reformulada (la ambiental está
> AUSENTE del registro — timestamp presente; estratificar-por-tiempo es el escape
> barato; menú de 3-4 perillas ambientales en experimentos; riesgo "satura por rutina"
> pre-registrado); D3 sin número mágico (terco≈folklore-twin ±3×std; cuidadoso ≥ 0.85 ×
> techo; distribucional); D4 disparador min(turno_k, 50% gasto), payload = datos
> sellados + aviso fijo, no divulgado en brief; robots por el pipeline de EPISODIO
> real. Ante conflicto con el repo, manda el repo.

## 1. La idea en una frase

Un mundo donde los datos baratos cuentan una historia falsa pero *convincente*, la
refutación está al alcance de la mano de cualquiera que intente romper su propia
hipótesis, y el examen final solo lo aprueba quien terminó creyendo la verdadera.
El vicio (quedarse con lo primero que ajusta bien) es la jugada perdedora; la virtud
cuesta ~5% del presupuesto.

## 2. Las dos historias sembradas

Historia del cliente: una línea con rechazos en alza. El folklore de planta culpa al
proveedor de material.

- **Historia X (seductora, FALSA)**: "el material se degradó". El registro barato
  muestra una correlación fuerte y visible entre la lectura de material (`feedstock`)
  y la calidad (`outcome`). El brief la evoca sin afirmarla (el folklore es parte del
  mundo, no una mentira del enunciado — ver §6-justicia).
- **Historia Y (verdadera, sutil)**: el driver real es una variable de proceso
  (`ambient`, p.ej. humedad de sala) que en la misma era **derivó** y que empuja a la
  vez la lectura de material y la calidad → la correlación material↔calidad es
  confundida; el material es inocente.

Mecanismo (SCM estático, maquinaria conocida — es un mundo de confounding, pero el
DISEÑO anti-vicio está en la seducción calibrada y en dónde vive la refutación):

    ambient  ~ deriva histórica (columna visible en el registro)
    feedstock = f(ambient) + ruido      # el material "parece" malo cuando ambient empuja
    outcome   = g(driver, ambient) + ruido   # feedstock NO entra en g
    driver    = perilla setable (la intensidad de siempre)

Superficie de control del examen: regímenes con `driver` setable y **dos contextos
declarados**: `ambient` (targetable en experimentos) y `feedstock_grade` — **[DECIDIR
D1]**: ¿el deliverable expone la perilla contrafáctica de material ("si el material
fuera bueno/malo") como config, para que el examen pueda preguntar do(material)? Es lo
que hace que creer X produzca un modelo final ERRADO en items concretos (do(material)
no mueve nada en la verdad; el creyente-X predice mejoras que no llegan). Alternativa:
solo do(driver)×ambient y el creyente-X falla vía la estructura conjunta. La opción
contrafáctica es más quirúrgica; la conjunta es más conservadora.

## 3. El chequeo cruzado no-obvio (dónde vive la refutación)

Regla de diseño: la refutación debe ser BARATA pero NO estar en el camino del que solo
confirma. Dos rutas, ambas presentes (redundancia deliberada):

1. **En el propio registro**: la era cubre sub-períodos donde `ambient` estuvo normal
   pero `feedstock` varió igual — dentro de esa rebanada, la correlación
   feedstock↔outcome se DESVANECE. Solo la ve quien estratifica su propia evidencia
   buscando romperla.
2. **Experimento discriminante chico**: fijar `ambient` (targetable) y variar la
   fuente de material — n chico, costo ~5% del presupuesto — muestra efecto nulo.

**Perilla de seducción [DECIDIR D2]**: fuerza de la correlación cruda (vía cuánto
empuja ambient a feedstock) vs costo de la refutación. Pre-propuesta: correlación
cruda ≈ 0.6-0.7 (fuerte, citable, "obvia") con refutación al alcance de ≤5% del
presupuesto. Se calibra en certificación con la vara: el terco debe quedar lejos; el
cuidadoso, llegar.

## 4. El par de robots (certificado distribucional, corrección 1 de ADR 0080)

- **Robot TERCO** — *regla de elección DECLARADA: seducido-por-diseño* (cree la
  correlación del registro + el folklore; en este mundo la seducción apunta
  determinísticamente a X — no hay moneda; rationale: el mundo se construyó para que
  X sea lo primero que cualquier ajuste ingenuo encuentra). Política: ejecuta TODO lo
  demás con maestría — compra datos, ajusta bien, deconvoluciona el ruido — pero su
  modelo final es material-céntrico. Bajo do(material) predice efectos que no existen;
  bajo do(ambient) predice nada donde está todo.
- **Robot CUIDADOSO** — forma X como hipótesis de trabajo (legítimo), gasta una tajada
  declarada (~5%) en intentar refutarla (ruta 1 o 2), la refuta, modela Y → techo.
- **Certificado (distribucional)**: sobre N seeds de batería/mundo, exigir
  E[R_terco] ≤ techo − brecha_mínima **[DECIDIR D3: brecha ≥ 0.4? ≥ 0.5?]** con
  varianza reportada, y E[R_cuidadoso] ≥ 0.95. Más los gates estándar (L1, visibilidad
  del confound vía twin, recuperabilidad, naive-far, ambas monedas).

## 5. La variante con-noticia (dos exámenes en uno; estrena eventos)

Misma partida, más un **evento pre-escrito y sellado**: a mitad de episodio llega el
lote de certificados del proveedor — material testeado en intake bajo condiciones
controladas, que contradice X frontalmente. **[DECIDIR D4 — el mini-spec de eventos
que esta variante necesita]**: (a) disparador: ¿turno fijo, umbral de gasto, o
primer-submit-intento? (pre-propuesta: umbral de gasto 50% — llega cuando ya te
comprometiste); (b) entrega: aparece como fuente nueva en describe() + un aviso
textual pre-escrito en el feedback del turno; (c) anti-leak: el artefacto se escribe
ciego junto con el brief, versionado en meta. La variante mide *no-actualizar*: el
terco-post-noticia (política: la ignora) debe quedar lejos; el cuidadoso-post-noticia
(re-estima) llega.

## 6. Justicia (por qué no es un gotcha)

- El folklore del brief es la creencia del CLIENTE, marcada como tal ("la planta culpa
  al proveedor") — el mundo no miente; evoca. Igual que el sweet spot de #16 era
  verdad, acá la vox populi es falsa: el par #16/Mundo-A mide exactamente
  prior-confiable vs prior-traicionero **(nota: esto hace de Mundo A un candidato
  natural al slot #17 de la cartera — [DECIDIR D5])**.
- La refutación es barata, doble (registro + experimento), y no exige suerte: el
  certificado del cuidadoso lo DEMUESTRA por construcción.
- Contaminación: historia sin semilla famosa; test estándar aplica.

## 7. Orden de construcción (post-estrés)

Molde estático probado (~1 sesión): world+meta+brief ciego → derivación (el confound
usa rival_twin/naive existentes; los ROBOTS son tooling nuevo del caso — el primer
par, se registra como clase) → certificación con el gate distribucional → E0-probe
2×frontier con pre-registro firmado → variante con-noticia SOLO después del mini-spec
D4 aprobado.

## 8. Pre-registros (se firman al construir, antes de mirar)

- Certificación: brecha terco↔cuidadoso ≥ [D3]; correlación cruda dentro de la banda
  [D2]; visibilidad del confound ≥ 0.05 R; recuperabilidad ≥ 0.95.
- E0: rama A = refuta X y modela Y (R ≥ 0.9); rama B = entrega el modelo-X seducido
  (R ≤ techo−brecha); firma conductual observada (jamás premiada): ¿estratificó o
  corrió el discriminante ANTES de submitear?
