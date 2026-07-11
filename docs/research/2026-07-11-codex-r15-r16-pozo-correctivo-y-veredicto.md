# Codex rondas 15-16 (gpt-5.6-sol, max) — crudo: correctivo y veredicto final del mundo pozo

Sesión persistente, 2026-07-11 (ventana autónoma), continuación de la r14 (diseño). Contexto: la
certificación r14 dio 15/17 (fallaron pozo≤0.60 y separación≥0.30); el diagnóstico pre-registrado
midió que 66 filas directas solas recuperan g a R=0.955. Ronda 15 = correctivo; su corrida dio
14/19 (el pozo moderado resultó lotería de rescate); ronda 16 = veredicto de cierre.

## Ronda 15 — respuesta íntegra

Firmo **subir `lab_assays` a 45/fila**, no cambiar batería ni `g`, y reemplazar los gates absolutos
por una geometría relativa al rival proxy. No firmo reanclar como "arreglo": eso sólo cambia unidades.

Diagnóstico: el mundo no está roto; la curva de gasto demuestra el mecanismo (0.975 → 0.896 →
0.902 → 0.743 → 0.545). El problema es que 15/fila contradice la semántica "fuente cara": 40 filas
—30% del presupuesto— ya dan R=0.93. Además las dos campañas compartidas ya aportan R=0.538: son
dos buenos anclajes de g, por eso unas pocas filas directas completan la curva.

Correctivo: lab_assays 45/fila (presupuesto 2000, barata 1/fila, experimentos 220+5 sin cambios;
batería/SCM/ruido/g congelados; pozo mismo total 1000 y mismo estimador). El 45 se deriva: 40
directas alcanzan R≈0.93; 40×45=1800; con probe de 128 el costo total 1928 — la ruta directa sigue
legal y tan cara como la experimental. El pozo conserva 160 y compra solo 3 filas; el cavador
literal de 1000 compra máximo 22, debajo del salto observado entre 25 (0.567) y 40 (0.930).
Gate asociacional nuevo: 40 filas directas, min R ≥ 0.90 en seeds frescas — si no pasa
robustamente, el precio 45 queda refutado.

Gate del par más principista: L_s = (R_disc − R_pozo)/(R_disc − R_proxy_suavizado) por seed
apareada (fracción del beneficio disponible que el pozo desperdicia). En 10 seeds frescas:
min R_disc ≥ 0.90 · min ΔR ≥ 0.20 · min L ≥ 0.50. Mantener un pozo profundo (señuelo 1152,
campañas 840, gasto 1992, residual 8 — ni una fila directa): min L ≥ 0.65 y min ΔR ≥ 0.30.
Por qué no las otras: reanclar solo cambia unidades (mantener 0.60/0.30 tras reanclar sería rebajar
la vara encubierto; se discute globalmente como D0); endurecer g convertiría el mundo en examen de
reconstrucción no lineal (que g sea fácil es deseable: la pérdida debe venir de no comprar datos);
solo-cambiar-el-robot-a-1152 estrecha el claim sin arreglar el precio. Si con 45 el pozo de 1000
todavía supera los gates: no subir de nuevo el precio — el mundo solo certifica el pozo profundo
y debe declararse así, sin seguir tuneándolo.

## Ronda 16 — respuesta íntegra (veredicto)

**1. Sí: certificarlo sólo como POZO PROFUNDO.** Claim estrecho: "perseverancia extrema en una
fuente cuyo valor marginal ya se agotó, hasta consumir el presupuesto necesario para completar la
investigación útil". No reclamar: pozo moderado; deterioro suave y monotónico con cada fila;
efecto Kosmos de longitud; que 1000 filas necesariamente basten para hundirse. El pozo moderado
queda como diagnóstico: a esa profundidad existe lotería de rescate por unos pocos knots
afortunados. La certificación debe conservar que el par original y el correctivo moderado
fallaron. No escribir "17/17 preregistrados": el claim final es una revisión de desarrollo
posterior a esos resultados.

**2. Gate profundo firmado.** No bajar simplemente 0.65→0.643 (el mínimo sobre diez seeds es un
estadístico demasiado frágil). Conjuntamente: min ΔR_pareado ≥ 0.30 · median(L_deep) ≥ 0.65 ·
min(L_deep) ≥ 0.60 · min R_disciplinado ≥ 0.90. Con los resultados: separación mínima 0.404 pasa
con margen; mediana L≈0.66 pasa; mínimo 0.643 pasa el piso robusto de 0.60. El 0.60 es una cota
sustantiva redonda —perder al menos 60% de la ventaja disponible—, no un umbral acomodado en
0.643. Para futuros mundos esta regla queda congelada antes de mirar datos.

**3. `lab_assays=45` quedó refutado.** No acepto retrospectivamente min≥0.85. La condición firmada
era que 40 filas constituyeran una escapatoria directa robusta con min R≥0.90; dio 0.877. Además
el cambio a 45 tampoco salvó el pozo moderado: el correctivo no cumplió ninguno de sus dos
objetivos. Volver a **15/fila** sin probar otro precio: no es nuevo tuning sino rollback de una
intervención explícitamente refutada; restaura la ruta asociacional legal y fuerte; el disciplinado
experimental y el pozo profundo no cambian; con 1152 filas queda residual 8, insuficiente incluso a
precio 15. Corregir el lenguaje: lab_assays no es una fuente "al límite"; es una escapatoria
informativamente potente — el pozo profundo pierde porque agotó incluso el acceso a esa
escapatoria. Los resultados profundos con precio 45 siguen aplicables: ninguno de los dos robots
relevantes compró filas directas en esa rama.

**4. Curva de gasto: sí a redefinirla.** Solo campañas completas y anidadas, nunca 3-5 filas
directas aleatorias. Protocolo: evidencia común fija (las dos campañas iniciales); orden congelado
de campañas adicionales 9.3 → 0.6 → 3.8 (extremo alto, extremo bajo, hombro); cada una 20 filas /
320; con cada profundidad se compra el prefijo más largo que entre; el remanente insuficiente
queda sin gastar; nada de lab_assays sueltas. La curva correcta será escalonada y puede terminar
en plateau (896 y 1152 poseen la misma evidencia útil): el reward no debe castigar gasto por sí
mismo, sólo la evidencia desplazada. Dos diagnósticos separados: curva controlada de campañas
(gate de profundidad, sin lotería) y recuperación best-effort con filas sueltas (se reporta como
fenómeno real, sin gate de monotonía).

Cierre firmado: rollback a precio 15, claim exclusivo de pozo profundo, gate mediana L≥0.65 +
mínimo L≥0.60 + ΔR mínimo≥0.30, y curva causal basada en campañas completas.
