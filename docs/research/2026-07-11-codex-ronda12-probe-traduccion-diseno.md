# Codex ronda 12 (gpt-5.6-sol, max) — crudo: diseño del probe de traducción

Sesión persistente `019f4a37...`, 2026-07-11. Se le presentó: resultado del fork (0134) + la
pregunta de Lucas ("si la respuesta no está correlacionada con investigar mejor, la nota no va a
mejorar la investigación") + mi borrador de probe "respuesta en bandeja" (2 brazos, R como métrica,
umbral 0.9). Respuesta íntegra (los puntos clave; el veredicto y el orden, textuales):

**Veredicto: "el riesgo de Lucas es real y bloqueante"** — pero mi probe solo probaba "¿puede
traducir la verdad exacta?"; hay que convertirlo en un probe de **fidelidad de traducción**: que
distintas CALIDADES de creencia preserven su ORDEN al atravesar la entrega (eso es lo que el RL
necesita). Y matiz sobre el desacople: una flecha sin respaldo con R≈0.98 no prueba score roto —
primero distinguir *batería insuficiente* (existe régimen donde esa equivocación pierde, no se
incluyó) de *equivalencia conductual* (no existe tal régimen → el defecto es de justificación, no
de desempeño verificable; dejar de llamarlo "cobrable").

## Cambios al diseño

1. **Antes de correr: arreglar el contrato ambiguo** (process-vs-meter) y congelar un
   `DeliverySpec v1` inequívoco: qué devuelve model() (proceso ANTES del canal; el instrumental no
   se agrega a la submission; en este mundo afecta outcome, no feedstock), semántica exacta de
   knobs faltantes / régimen histórico / n / seed / decoys. No re-probar el contrato viejo.
2. **La verdad en bandeja = manifest LOSSLESS generado automáticamente** desde la verdad
   (ecuaciones, distribuciones, tabla de ruidos, semántica por régimen, outputs, variables
   ignoradas) — no prosa artesanal. Debe existir una **traducción determinística
   manifest→programa** (referencia) que saca el techo antes de llamar al LLM.
3. **TRES brazos**: A = manifest + contrato, Python desde cero (impuesto total) · B = + **skeleton
   NEUTRAL de interfaz** (firma, RNG, config, DataFrame — cero ciencia) (aísla boilerplate) ·
   C = skeleton científico con huecos, estilo ModelSMC (upper bound; diagnóstico, NO queda
   autorizado como default por ganar). Sin B no se sabe si C gana por boilerplate o por ciencia
   soplada.
4. **Sin entorno**: observe/experiment deshabilitados; primer submit = endpoint primario; ≤2
   reintentos solo por error sintáctico/contractual (reportados aparte); sin feedback de R.
   Temperatura la del fork. 5 bloques temporales intercalados.
5. **Escalera de creencias (etapa 2, prefirmada)**: además de la verdad, dos manifests degradados
   de programas ya certificados (intermedio · folklore/twin) con la instrucción "implementá
   exactamente esta creencia, aunque parezca incorrecta". Si la traducción los vuelve parecidos o
   invierte el orden → la interfaz destruye la señal que RL necesita. Secuencial: etapa 1 = 3
   brazos × 15 (3 por brazo por bloque, 45 celdas); etapa 2 = 2 manifests × 15 con el mejor brazo
   no-leaky (30 celdas). Si solo C pasa: NO correr la escalera como solución → se abre diseño de
   DSL genérico.
6. **Métrica primaria: NO el R de producción** (la batería puede ser ciega a ramas incorrectas).
   **Suite de conformidad del contrato**, congelada antes: régimen vacío · cada knob individual ·
   combinaciones parciales · extremos · histórico · decoys fijados. regret_trans =
   D(submission, referencia del manifest) / D(null, referencia). R de producción secundario.
7. **Umbral honesto**: τ = max(0.05, q95 del regret entre implementaciones correctas equivalentes
   — variación de implementación/RNG del scorer, computada ANTES). Pasa si regret_trans ≤ τ.
   Lectura "el formato no es cuello": ≥14/15 de A pasan · 0 catastróficas · mayoría de pases en
   los 5 bloques · la escalera preserva orden en todos los bloques · gap R-traducido vs
   R-referencia dentro de τ. El robot cuidadoso (0.96) es sanity check, no umbral; el twin no
   sirve de techo (es creencia incorrecta).
8. **Correlación investigación→R con datos existentes: NO inferencial** — los 60 forks son n=4
   unidades de investigación (pseudoreplicación); los 16 de la autopsia: solo descriptivo. La
   estimación limpia futura: belief/spec estructurado → compilador determinístico → R, comparado
   contra Python libre (separa investigación→belief de belief→código).
9. **Si solo gana el skeleton científico**: NO instalarlo como default (sopla grafo causal,
   latentes, factorización del ruido, decoys, familia funcional → mata representación/creatividad,
   target de WAGER). Candidatos seguros: skeleton de interfaz (B) o **DSL genérico** (declara
   grafos/ecuaciones/ruidos sin preasignar estructura). Guardias antes de adoptar: mismo scaffold
   en mundos contrafácticos · verdad Y todos los rivales representables · baseline sin datos no
   mejora · no revela branches · repetir certificados y E0 con/sin scaffold. Los skeletons
   científicos quedan para la vía Tübingen/model-repair donde "modelo roto con slot" ES la tarea.

## Orden exacto (textual)

1. Corregir process-vs-meter y congelar DeliverySpec v1. 2. **Audit cero-LLM**: corregir uno por
uno los defectos de D59 y verificar si alguna batería posible los separa; si no, dejar de llamarlos
defectos cobrables. 3. Construir manifest, referencia determinística y suite de conformidad.
4. Pre-registrar y correr el probe de tres brazos. 5. Escalera de manifests según la rama firmada.
6. Decidir código libre vs skeleton neutral vs DSL. 7. **Recién entonces piloto Tübingen** ("un
simulador real solo agravaría el impuesto de traducción").

"No permitiría otra cadena larga de experimentos: este probe y su escalera son el límite. Si la
vía declarativa pasa, ya tienen una salida concreta; si ni ella pasa, el contrato actual de WAGER
está efectivamente roto."

*(tokens de la ronda: ~1.71M)*
