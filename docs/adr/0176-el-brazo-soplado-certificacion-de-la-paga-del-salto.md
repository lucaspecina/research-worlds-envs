# 0176 — EL BRAZO SOPLADO (el privilegiado): ningún mundo certifica sin correr el mismo modelo CON la pista del salto

**Fecha**: 2026-08-10 · **Estado**: vigente · **Origen**: regla de Lucas, pedida desde siempre
y nunca institucionalizada ("¿POR QUÉ NUNCA LO HICIMOS?"). Complementa ADR 0175.

## Decisión

Toda certificación de mundo incluye el **brazo SOPLADO** (alias formal: el privilegiado): el
MISMO modelo, mismo mundo, mismo presupuesto — con una pista estandarizada que referencia el
salto objetivo ("considerá la posibilidad de X"). Se computa la **prima del descubrimiento**:

    Δ-soplo = nota(soplado) − nota(solo)

Compuertas (todas obligatorias):
1. **Capacidad**: el soplado tiene que ejecutarlo BIEN (si ni soplado puede, el mundo mide
   incapacidad básica, no descubrimiento).
2. **Paga empírica**: Δ-soplo grande. Si el soplado lo hizo bien y ≈ empata con el solo,
   el solo NO TIENE FORMA de saber que hay algo que mejorar → el mundo/vara está roto
   (formulación de Lucas — exactamente el agujero D1).
3. Junto con 0175 (mejor rival sin salto, analítico): el soplado mide la paga del salto
   contra lo que los agentes HACEN; 0175 contra lo MEJOR que podrían hacer sin saltar.
   En D1, soplado solo habría mostrado Δ≈0.35 contra los vagos mal afinados (agujero
   tapado); 0175 solo, S=0.986 (agujero visto). Con agentes competentes convergen. SIEMPRE
   ambos.

## Anti-leak (para que el soplo no contamine la medición)

Seeds del soplado QUEMADAS y separadas del rango de medición; sus episodios jamás entran en
resultados conductuales; el texto de la pista se congela y se loguea en la ficha; el solver
sigue sin ver taxonomía — la pista nombra el candidato del mundo, no la librería. Costo: 2-3
episodios por polo (~USD 2-3) — contra los ~USD 30 que costó no tenerlo en D1.
