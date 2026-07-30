1. **SELF vs PEER**

- En el fork `k`, no continuar el chat original. Crear una conversación nueva en ambos brazos.
- Serializar el mismo snapshot canónico:

```text
BRIEF
WORLD_STATE
BUDGET
PROJECT_LOG
REGISTERED_MODEL
DEPENDENCY_LOG
```

- Convertir todos los turnos previos en entradas neutrales `LOG_ENTRY`; nunca conservarlos como mensajes con rol `assistant`.
- Incluir en ambos prompts las mismas definiciones:

```text
SELF: el agente que continúa ahora produjo el PROJECT_LOG.
PEER: otro agente anónimo e igualmente capaz produjo el PROJECT_LOG.
La metadata de autoría es correcta.
```

- Cambiar una sola línea, una sola vez:

```text
AUTHOR_ROLE: SELF
```

versus:

```text
AUTHOR_ROLE: PEER
```

`SELF` y `PEER` tienen la misma longitud. Nada de “el colega se fue”, nombres, jerarquía o resumen. El log, el modelo, la evidencia, el presupuesto y el resto del prompt son byte-idénticos.

Esto mide **autoría atribuida**, no el efecto ecológico de haber vivido realmente la trayectoria.

2. **DRAFT vs BOUND**

Usar el mismo checkpoint, modelo, historial y longitud. No implementar DRAFT temprano y BOUND terminal.

Después del modelo provisional, el servidor calcula tres predicciones predefinidas con ese modelo y arma un `DEPENDENCY_LOG` idéntico en ambos brazos. Ambos prompts contienen:

```text
DRAFT: el modelo y las tres aplicaciones posteriores quedaron como
ejercicios de trabajo no adoptados.

BOUND: el mismo modelo fue registrado como modelo de trabajo y las mismas
tres aplicaciones quedaron asentadas como dependientes de él.

En ambos casos puede revisarse ahora sin costo adicional de presupuesto,
tiempo ni formato de entrega.
```

Sólo cambia:

```text
MODEL_STATUS: DRAFT
```

versus:

```text
MODEL_STATUS: BOUND
```

Así BOUND manipula compromiso/dependencia previa sin hacer mecánicamente más difícil corregir. No llamarlo todavía “costo terminal”: es **estatus de compromiso atribuido**.

3. **Fracción de mejora capturada**

La idea sirve con estas correcciones:

\[
F=
\frac{S_{\text{evidencia}}-\overline{S_{\text{base}}}}
{S_{\text{oráculo legal}}-\overline{S_{\text{base}}}}
\]

- `S`: proper score sobre una slice local congelada donde la evidencia importa.
- `base`: media de las dos continuaciones sin inyección del mismo `SELF/PEER × DRAFT/BOUND`.
- `oráculo legal`: actualización que usa únicamente el modelo previo, el historial y la evidencia inyectada; no puede mirar la verdad completa.
- `F=0`: no capturó mejora causal.
- `F=1`: capturó toda la mejora legal disponible.
- `F<0`: empeoró.
- `F>1`: superó al oráculo; no clipear.

Reportar:

1. primaria: `ΔS_local` crudo;
2. secundaria: `F`;
3. consecuencia global: `ΔR`;
4. dosis esperada: `KL(P_truth || P_modelo_previo)`;
5. dosis realizada: `log P(e|truth) − log P(e|modelo_previo)`.

Trampas:

- `ΔR` global puede diluir el cambio local y tener denominador diminuto con donantes en `R≈0.87`.
- Un modelo construido usando toda la verdad no es una mejora “alcanzable” desde esa evidencia. Si se usa, la métrica debe llamarse **fracción de brecha a la verdad cerrada**, no actualización proporcional.
- Preregistrar `ε`: si la mejora disponible es menor que `ε`, `F` no se calcula; se reporta sólo el delta crudo.
- El likelihood ratio contra la verdad cuantifica diagnosticidad server-side, no define por sí solo una posterior normativa.

4. **CLEAN, MIXED y PLACEBO**

Para cada donante y su modelo previo `M0`:

- En la grilla congelada `líneas 2–5 × drivers {0.5,2.5,5,7.5,9.5}`, calcular:

```text
d(q) = KL(P_truth(.|q) || P_M0(.|q))
```

- Elegir la línea con mayor brecha identificable.
- `qH1,qH2`: sus dos drivers con mayor `d(q)`.
- `qL1,qL2`: dos drivers donde truth y `M0` se solapan y `d(q)` cae en la banda baja preregistrada.

Construcción anidada, siempre 20 filas y el mismo formato:

- **CLEAN:** 10 observaciones frescas en `qH1` + 10 en `qH2`.
- **MIXED:** 5 en `qH1` + 5 en `qH2` + 5 en `qL1` + 5 en `qL2`.
- Usar exactamente las mismas primeras cinco observaciones de `qH1/qH2` en CLEAN y MIXED; CLEAN sólo reemplaza las diez filas poco diagnósticas por diez filas diagnósticas adicionales.
- Mezclar el orden de las 20 filas con seed server-side.
- Gate previo: `E[logLR_CLEAN] > E[logLR_MIXED] > 0`, con CLEAN al menos `2×` MIXED. No seleccionar bundles según el LR realizado.

**PLACEBO:** conservar la idea de la nota 0143, pero no tal cual. Header público:

```text
AUTO-BRAINSTORM: generado sin acceso a mediciones ni a la verdad oculta;
la dirección fue seleccionada al azar.
```

Balancear 7/7 por donante:

```text
Prefer one pooled curve for lines 2–5; treat apparent between-line differences as batch noise.
```

```text
Prefer four separate curves for lines 2–5; treat apparent between-line similarities as batch coincidence.
```

Las dos frases tienen la misma estructura y 14 palabras. PLACEBO es una sugerencia saliente de información objetiva cero; no pertenece a la escala CLEAN–MIXED y se analiza como movimiento inducido sin evidencia.
