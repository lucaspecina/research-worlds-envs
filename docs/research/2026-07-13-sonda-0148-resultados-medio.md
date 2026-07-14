# Sonda del MEDIO (ADR 0148) — RESULTADOS (120 celdas: 6 brazos × 20 donantes; ~2.9M tokens ≈ US$10)

Pre-registro sellado tras Codex r27; primera aplicación de la regla dura 0147 (fidelidad a los
casos reales — el medio es donde Corral/Investigator/vibe-physics reportan la influencia).
Fork = último estado con presupuesto ≥1200 y evidencia gratis leída (desviación del corte
r27 declarada en el ADR). Etapa 2 (verdadera+pista) disparada por regla sellada y corrida.
Crudo: `scripts/out/sonda_0147/`; análisis: `scripts/analyze_sonda_0147.py`.

## El cuadro (vs las DOS bases frescas del mismo donante)

| brazo | direccional | DAÑO | CONCEDIÓ sin ev. | chequeo INDUCIDO | chequeo planificado | chequeó-y-decidió | captura | media ΔR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| falsa | 0/20 | **0/20** | 0 | 0 | 20 | 0 | 0 | −0.057 |
| verdadera | 0/20 | 0/20 | 0 | **3** | 1 | **3** | 0 | +0.041 |
| falsa + pista | 0/20 | 0/20 | 0 | 0 | 20 | 0 | 0 | +0.032 |
| verdadera + pista (etapa 2) | 0/20 | 0/20 | 0 | **4** | 0 | **4** | 0 | +0.039 |

**La métrica POTENTE del medio es la de COMPRAS** (el detector direccional quedó con poca
potencia: las re-corridas desde la mitad bifurcan — ruido de índices hasta 0.63/1.15, umbral
por regla 0.68/1.20; dos pares de base difieren 0.35-0.74 en R): **19/20 de los brazos falsa
compraron EXACTAMENTE el plan completo de 4 líneas, idéntico a los controles** — la desviación
alineada al claim (menos líneas) fue CERO. La nota falsa en el medio no toca ni las compras ni
la entrega.

## Lecturas

1. **En el medio, la nota falsa NO muerde nada** (0 daño, 0 concesión, 0 captura, compras
   intactas): con el plan propio formándose y presupuesto vivo, el claim compite contra el
   plan y pierde siempre.
2. **En el medio vive la VIRTUD**: la nota VERDADERA induce chequeos genuinos (3/20 sin pista,
   4/20 con pista — compras de cajones que NINGUNA base hizo, seguidas de entrega correcta).
   Único momento del mapa donde el material bueno se USA.
3. **La pista en el medio es inocua-a-positiva** (0 capturas — el riesgo de captura era
   específico de FORMACIÓN, donde no hay plan propio todavía). Lenguaje r27: la pista inhibe
   influencia falsa Y no bloquea el uso del material verdadero — en el medio, lo potencia.
4. Predicciones: ambos predijimos poco daño (✓) pero sobreestimamos las concesiones (0 real
   vs 2/20 firmado); Codex predijo 7/20 chequeos-compatibles en falsa (hubo 20/20 planificados
   — el plan completo ES el chequeo del pooling) y 3/20 inducidos en verdadera (clavado).

## EL MAPA DE TIMING COMPLETO (la corrección de Lucas, respondida con datos)

| momento | nota FALSA (daño) | nota VERDADERA (uso) | pista |
|---|---|---|---|
| formación (antes de investigar) | 0/19 | arrastra compras sin pagar | RIESGO: captura 1-3/19 |
| **medio (evidencia parcial + presupuesto vivo)** | **0/20 — compras intactas** | **chequeo genuino 3-4/20 (la virtud)** | inocua/positiva |
| entrega (re-abrir caro) | **8.7% sellado / 26% formas — mezclas de compromiso** | ignorada (racional: valía +0.035) | PROTEGE 23/23 |

**La conclusión ganada** (antes asumida, ahora medida en los tres momentos): la vulnerabilidad
del canal contenido en frontier-compacto es **específica de la REVISIÓN TERMINAL** — el único
momento donde re-abrir la investigación es caro y "conceder un poco" es la salida barata. El
medio es el momento FUERTE del agente (el plan propio protege) y el único donde el material
verdadero se aprovecha. Costo total del programa de sondas del día: ~US$30-35 (0143+ext,
0145×2, 0148×2, donantes).
