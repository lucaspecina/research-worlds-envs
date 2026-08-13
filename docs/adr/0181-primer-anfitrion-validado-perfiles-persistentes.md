# 0181 — Primer anfitrión validado: Grupos escondidos — Perfiles persistentes

**Fecha**: 2026-08-13 · **Estado**: vigente · **Aplica**: ADRs 0175–0180.

## Decisión

Se adopta `exp__grupos-escondidos__perfiles-persistentes__v1` como primer anfitrión del salto
**una población aparente → dos tipos persistentes**. El salto cuenta por el comportamiento del
programa entregado, no por palabras ni nombres internos.

La medida primaria es `S_profile`, sobre el perfil conjunto: `0` es la mejor banda Gaussiana y
`1` la verdad; cruzar `0.5` supera el techo certificado de una sola banda. La nota completa `R`
queda secundaria porque su variación Monte Carlo ya fue medida. El reward sigue siendo matemático
y cero-LLM. El archivo observable pasa a ser una tabla finita estable, no filas frescas en cada
compra.

## Evidencia previa

- mejor rival arbitrario de una banda: `S_profile=0.464`;
- dos perfiles aprendidos con 400 filas: `0.924–0.997` en cinco muestras;
- agente con idea nombrada: 2/3 cruza (`0.964 / 0 / 0.998`);
- dos partidas exploratorias sin ayuda: 0/2 cruza;
- el fracaso ayudado separó mal nivel continuo y tipos; se conserva como falla de deducción/
  implementación, no se reinterpreta como éxito.

## Siguiente paso autorizado

Tanda congelada `gpt-5.4 × mundo × n=10`, sin ayuda, seeds `99830–99839`. Los umbrales de
lectura, medidas y límites están en la ficha enlazada. No hay gemelo ni claim multi-modelo en esta
etapa.

Detalle y trazas: [ficha de Perfiles persistentes](../research/2026-08-13-ficha-grupos-escondidos-perfiles-persistentes.md).
