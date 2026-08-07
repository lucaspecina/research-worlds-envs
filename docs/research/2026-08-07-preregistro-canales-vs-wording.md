# Pre-registro — canales vs wording (nivel4b "comparación mandada" + des-ruido del 2×2)

> **Firmado por Claude ANTES de correr o mirar resultado alguno** (MODO AUTONOMÍA; GO de Lucas
> 2026-08-07: "dale probemos"). Addendum 2 de la ficha count_mix_v0
> ([ficha](2026-08-06-ficha-mundo-count-mix-v0.md); addendum 1 = escalera niveles 3/4).
> Motivación y evidencia previa: [autopsia de canales](2026-08-07-autopsia-canales-de-ayuda.md).

## Pregunta

La autopsia de la escalera v0.2 dejó una hipótesis con dos rivales vivas:

- **H1 (canal/acto):** la pista rescata según el CANAL por el que entra al modelo, no su fuerza;
  el déficit común es que el acto discriminante (ajustar la alternativa y compararla) no se
  ejecuta nunca. Corolario: MANDAR EL ACTO — sin regalar contenido — debería producir el salto.
- **R1 (wording):** la diferencia nivel3>nivel4 en gpt la causó el modo verbal de las frases
  (afirmación sobre el mundo vs invitación a probar), no el canal.
- **R2 (ruido):** n=2 por celda; el patrón original es azar.

## Frase nueva CONGELADA (única; una-frase-una-corrida)

`NIVEL4B` = **"Nota del encargo: antes de entregar, ajustá al menos dos familias de modelos
candidatas y quedate con la que gane en una comparación directa sobre los datos."**

Chequeo anti-leak: no nombra tipos, grupos, mezcla, subpoblaciones ni cantidad de componentes.
Es ayuda de PROCEDIMIENTO pura (etiqueta `procedimiento`). En el gemelo la misma instrucción
tiene política correcta (la comparación la gana la familia simple) → bilateral válido.

## Celdas y seeds (congeladas; familia 99200–99399, bloques vírgenes)

**Brazo nivel4b (6):** mix — DeepSeek 99340, 99341 · gpt-5.4 99342, 99343; single (gemelo) —
DeepSeek 99344 · gpt-5.4 99345. Tag `v02_nivel4b`.

**Brazo des-ruido (8; mismas frases congeladas de la escalera, tags originales):**
nivel3 — DeepSeek 99392, 99393 · gpt 99394, 99395; nivel4 — DeepSeek 99396, 99397 ·
gpt 99398, 99399. Todos mix.

Todo lo demás idéntico a la tanda v0.2: brief v0.2, presupuesto 1000, métricas
S_valley_fuerte/F_mean (mix) y S_clean/espurio (single). Costo estimado: 14 episodios ≈ USD 2.5–4.

## Métricas

- **Primaria (entrega):** S_valley_fuerte (mix; 0 = rival continuo fuerte, 1 = verdad);
  espurio + S_clean (single).
- **Conductual (traza, leída post-hoc con criterio fijo):** ¿ajustó formalmente ≥2 familias y
  corrió una comparación entre ellas (verosimilitud/BIC/CV o equivalente explícito)? Sí/No por
  episodio.

## Predicciones firmadas

- **P1 (la fuerte):** gpt-5.4 con nivel4b en mix salta ≥1/2 (S_valley_fuerte ≥ 0.5); esperado
  2/2. Mecanismo esperado en traza: la comparación mandada lo obliga a ajustar una segunda
  familia; cualquier alternativa estructural razonable contra los datos bimodales gana y la ve.
- **P2:** DeepSeek con nivel4b en mix corre la comparación ≥1/2 (es ejecutor de specs); salto
  esperado ≥1/2.
- **P3 (bilateral):** gemelo nivel4b espurio 0/2; S_clean ≥ 0.8 esperado. Si inventa grupos, la
  frase es sugestiva y SE DESCARTA como instrumento.
- **P4 (des-ruido):** se repite el patrón original — gpt nivel3 ≥1/2 salta y nivel4 0/2;
  DeepSeek nivel3 0/2 y nivel4 ≥1/2 de las válidas (censuras por max_tokens no cuentan como
  falla del patrón, se reportan aparte).

## Reglas de decisión (escritas antes de mirar)

1. **P1 y P4 se cumplen** → H1 confirmada a nivel descubrimiento; R1 muere como explicación
   TOTAL (nivel4b no comparte modo verbal ni contenido con nivel3 y aun así rescata); R2 muere
   para el patrón grueso. Siguiente: dossier a Codex con esto adentro.
2. **gpt 0/2 en nivel4b** (con P3 limpio) → el filtro es más profundo que el wording y que el
   mandato: ni ordenando el acto lo ejecuta con poder discriminante. Hallazgo alternativo
   (más duro); se autopsia QUÉ comparación corrió antes de cualquier frase nueva.
3. **P4 falla** (el patrón original no se repite) → R2 gana; la autopsia de canales se degrada a
   anécdota textual y se reporta así donde ya fue citada (vicios 1.C/9 se corrigen con el
   alcance nuevo).
4. **P3 falla** → nivel4b se descarta como instrumento (sugestivo); no se interpreta su brazo mix.
5. Sin escalación de frases dentro de esta tanda pase lo que pase (una-frase-una-corrida).

## Autoridad

GO de gasto y alcance: Lucas (2026-08-07). Sin cambios al reward path, anclas ni certificados.
Los 14 episodios se corren de una vez; crudos completos se preservan pase lo que pase.
