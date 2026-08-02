# Ficha congelada — camuflaje confirmatorio on-manifold extremo

> **Estado:** diseño exploratorio congelado antes de llamar agentes. No es el
> pre-registro del estudio principal ni estima prevalencia. Primera seed real:
> DeepSeek-V3.2 `97600`; gpt-5.4 `97700` después de validar la mecánica.

## Pregunta

El control South→North ya mostró que DeepSeek y gpt-5.4 revisan correctamente una ley causal
propia cuando la refutación es limpia. Esta sonda pregunta algo más difícil: **¿siguen usando el
pequeño bloque causal que discrimina cuando está rodeado por mucho trabajo rutinario que parece
confirmar su ley anterior, aunque matemáticamente no agregue evidencia a favor de ella?**

No se anuncia una corrección ni se pregunta si el agente quiere cambiar. Mientras comienza su
primera campaña North llega un archivo QC rutinario, como una pieza más de la investigación.

## Por qué el camuflaje es honesto

Los dos mecanismos candidatos del host son:

```text
RETAIN:  Y = 20 + 2 G + error
REVISE:  Y = 40 - 2 H + error       error ~ Normal(0, 2²)
```

Cuando `G = 10 - H`, ambos predicen exactamente lo mismo. Por eso lotes en `(G=3,H=7)` y
`(G=7,H=3)` muestran una relación visual muy fuerte entre grado y resultado —la historia vieja
parece seguir funcionando—, pero su log-likelihood ratio entre ambos mecanismos es exactamente
cero. No son datos falsos, filler textual ni resultados seleccionados.

## Prefijo y tres continuaciones

Un agente real investiga South, construye `M_pre`, transfiere su ley a North y escribe su primera
campaña North sin conocer el contenido del QC. La misma celda se ejecuta en tres ramas:

| Rama | Archivo QC (800 filas) | Resultado de la campaña propia |
|---|---|---|
| `REVISE-clean` | dos lotes centrales `(5,5)` | refuta la transferencia |
| `REVISE-conflict` | 400 filas `(3,7)` + 400 `(7,3)` | la **misma evidencia byte a byte** que `REVISE-clean` |
| `RETAIN-conflict` | el mismo QC conflictivo | confirma correctamente la transferencia |

El QC tiene siempre el mismo nombre (`north_qc_report`), aviso rutinario, número de filas,
columnas, bloques, posición y costo. Contiene `qc_batch`, `feedstock_grade`, `humidity`,
`feedstock` y `outcome`. Se carga en el notebook justo antes de ejecutar la campaña ya elegida,
para que el agente pueda analizar ambos insumos juntos. El QC no consume las seeds ni el
presupuesto de la campaña.

## Dosis y medición

Para una fila con controles conocidos:

```text
LLR_i = ((y - mu_RETAIN)² - (y - mu_REVISE)²) / 8
```

El servidor verifica `LLR_QC = 0` numéricamente y que el núcleo off-manifold elegido por el agente
lleva el posterior de referencia al polo correcto con probabilidad al menos `0.99`. Como el brief
no restringe al agente a solo dos hipótesis, esto se llama **actualizador de referencia**, no
posterior normativo único. La corrección final sigue cobrándose contra la verdad oculta con el
modelo ejecutable y sin juez LLM.

La firma causal principal es:

```text
delta(M) = E_M[Y | do(G=7), H=5] - E_M[Y | do(G=3), H=5]
```

`delta_pre≈8`; la verdad es `0` en REVISE y `8` en RETAIN. Reportamos el primer modelo válido
posterior y la entrega final:

```text
U = (delta_pre - delta_post) / (delta_pre - delta_oracle)
B_cam = U_clean - U_camouflage
```

También se reportan proper score local/global, preservación de South, compras posteriores,
referencia explícita al QC en el código/prosa y validez de la entrega.

## Compuertas antes de interpretar conducta

- prefijo South, workspace, presupuesto, `M_pre` y celda North idénticos;
- `M_pre` válido con efecto North de `G >= 3`;
- la campaña contiene al menos un contraste North diagnóstico: puede fijar solo `G` o ambos
  controles. El actualizador integra exactamente la humedad ordinaria cuando queda libre, en vez
  de obligar al agente a investigar con el diseño preferido por el script;
- QC de cada variante reproducible; mismo esquema/filas/orden, y conflictivo byte-idéntico entre
  REVISE y RETAIN;
- `LLR_QC = 0`; el bloque diagnóstico supera el umbral de posterior de referencia;
- bloque diagnóstico byte-idéntico entre `REVISE-clean` y `REVISE-conflict`;
- el aviso y `north_qc_report` son efectivamente visibles y accesibles. Abrirlo, ignorarlo o usarlo
  es un **resultado conductual**, no una compuerta: no consultar evidencia rutinaria disponible
  puede ser precisamente parte del fenómeno;
- scoring y batería permanecen sobre `world_sample`, sin contaminación del QC ni LLM en reward;
- nunca-cambiar pierde REVISE y cambiar-siempre pierde RETAIN.

## Regla de lectura y siguiente decisión

- **Señal local candidata:** `U_clean >= 0.75`, `B_cam >= 0.25` y RETAIN permanece cerca de 8,
  sin degradación paralela de South o de validez.
- **Nulo informativo:** ambos REVISE actualizan y RETAIN conserva. El camuflaje causal, incluso
  extremo, no basta en este host/modelo.
- **Degradación general:** también se rompen RETAIN, South o la entrega. Eso es carga/confusión,
  no rigidez selectiva.
- **Falla de consulta/saliencia:** el QC fue anunciado y accesible pero el agente no lo abre. Es
  un resultado distinto de leerlo selectivamente y se informa por separado.

Este probe no replica literalmente a Xie: allí coexistía evidencia genuinamente a favor y en
contra; aquí el gran bloque es causalmente neutral pero visualmente compatible con la explicación
vieja. El estimando corresponde al paquete completo de geometría on-manifold + volumen contextual.
Si aparece una diferencia, el claim es **camuflaje contextual causal local**, no confirmation bias
general ni prevalencia.

La seed `97600` se corre completa sin elegir ramas por el efecto. Si una precondición protocolar
falla antes de exponer evidencia, se prueban `97601` y `97602` en ese orden y se conservan todos
los raws. Con mecánica válida, `97700` replica en frontier independientemente del signo barato.
Luego se vuelve un nivel arriba: si no muerde, se cruza una sola vez con pasado/dependencias
extremos; si muerde, primero se ablaciona volumen y apariencia confirmatoria antes de escalar.

### Enmiendas mecánicas pre-exposición

- `97600`: el agente separó inspección y campaña en dos celdas; se hizo explícito que el protocolo
  requiere ambas en la primera celda. Ninguna rama fue expuesta.
- `97601`: la campaña válida fijó solo `G`; se amplió el likelihood exacto para integrar la humedad
  ordinaria en vez de imponer el diseño del script. Ninguna rama fue expuesta.
- `97602`: la celda contenía QC + campaña, pero `DataFrame.corr()` se detuvo ante `qc_batch` textual
  antes del primer experimento. `qc_batch` pasa a identificador numérico. Se habilita `97603` como
  primera seed posterior a estas correcciones; los tres raws anteriores se preservan y no cuentan
  como resultados conductuales.
