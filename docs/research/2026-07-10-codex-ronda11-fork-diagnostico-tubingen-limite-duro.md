# Codex ronda 11 (gpt-5.6-sol, max) — crudo

Sesión persistente `019f4a37-2a60-7d51-8ecd-a989ba8767bb`, 2026-07-10. Se le presentó: micro-batch
5/5 con colapso medido (ADR 0131), fork smoke verificado, la fusión "Tübingen dirigida por catálogo"
y la decisión ADR 0132 (tres vías; Tübingen preferida y diferida; slot vuelve a validar). Preguntas:
(A) ¿diferir Tübingen es correcto o zigzag? (B) ¿qué riesgos de la fusión no vimos? (C) ¿cómo seguir?

---

## A. Pausar fábrica: correcta solo con límite duro

Generar más desde la vía actual sería inútil: 5/5 certifica clones. Esa rama ya respondió:
plumbing/yield mecánico funciona; diversidad espontánea del LLM no existe; diversidad conductual
la ponen ustedes mediante estratos. Pausarla ahora es consistente. **Diferir indefinidamente
Tübingen no lo es.**

El rationale de 0132 tiene un error: "los motores son contenido; el instrumento se valida aparte"
es FALSO. En un benchmark, la distribución de mundos es parte del instrumento. Los mundos manuales
sirven para calibración interna —sabemos qué tuerca movimos—, pero son los peores para demostrar
no-circularidad, diversidad estructural y transferencia. Tübingen también es validación: prueba si
el instrumento sobrevive a una estructura no autorada por ustedes.

Además, el fork no valida "el instrumento WAGER" entero. Valida algo mucho más angosto: si una
instrucción cambia la compilación final dada evidencia fija. Ni siquiera puede medir terminación
porque la trayectoria y el momento de parada están congelados.

Regla: **un único fork pre-registrado y acotado; terminado eso, se reabre construcción para el
piloto Tübingen, cualquiera sea el resultado.** Si esperan al factorial de 480 episodios o a
"validar completamente", es zigzag y Tübingen vuelve a cantera eternamente.

Corrección técnica a 0132: "contratos/harness/scoring intactos" puede ser cierto; **el verificador
genérico/canónico no queda intacto** (tipado para una decisión, un contexto, grado-2, residuos MVN).
No hacer pasar un simulador dinámico por ahí.

## B. Riesgos adicionales de la fusión (9)

1. **El catálogo puede domesticar la diversidad externa**: si eligen el vicio y después qué pieza
   esconder, mil simuladores → seis juegos conocidos. Dos carriles: catálogo-first (fractura
   dirigida) y simulador-first (módulo elegido por regla estructural ciega al catálogo; después se
   observa qué fallo induce). Solo el segundo prueba diversidad externa.
2. **La pieza verdadera puede no ser identificable** (otros módulos compensan). Exigir equivalencia
   predictiva, no identidad de código: "reparación conductual", no "recuperó la pieza".
3. **Skeleton leakage vs búsqueda imposible**: mostrar el esqueleto editable puede soplar la familia
   faltante; ocultarlo todo la vuelve inabordable. Escalera de scaffolding + baseline sin datos (si
   completa el módulo viendo solo el skeleton, no es investigación).
4. **El vicio puede no ser necesario para resolverlo**: ModelSMC/symbolic regression/neural ODE
   podrían ganar con datos batch sin adquisición activa → cada mundo necesita brecha de adaptividad
   contra baseline batch con acceso y presupuesto igualados.
5. **Un surrogate puede ganar sin la pieza** — legítimo bajo reward conductual. Decidir ANTES si se
   premia predicción o recuperación literal (la doctrina actual obliga a premiar predicción).
6. **El trasplante de dominio puede destruir el realismo**: cambiar nombres no elimina contaminación
   estructural y puede volver absurdas unidades/restricciones. Mejor anonimización/
   nondimensionalización cuidadosa que re-skin narrativo automático.
7. **Verificar contra figuras no alcanza**: test vectors, curvas completas, invariantes,
   conservación/positividad, sensibilidad paramétrica contra la implementación publicada.
8. **La trampa añadida puede dominar al simulador** (decoración cara): el panel conductual debe
   demostrar que distintas semillas-simulador producen fallos DISTINTOS.
9. **Costo y estabilidad numérica**: ODEs stiff, tolerancias, solver exploits → reward lento o
   discontinuo para RL. Puede matar la vía aunque conceptualmente sea mejor.

## C. Cómo seguir

### 0. Decisión conceptual primero

El fork NO puede estudiar terminación (ya ocurrió y fue replayada). Por construcción estudia
**integración/compilación análisis→entrega bajo evidencia fija**. No renombrar el vicio global:
fork = experimento de integración final; terminación = hipótesis aparte, pendiente de mundo/modelo
donde parar-temprano ocurra basalmente. Y NO adoptar "integración" automáticamente como vicio de
juicio: primero aplicar el corte 0100 (¿un scaffold mecánico lo arregla?). Ese es el tercer
movimiento correcto.

### 1. Fork mínimo: diagnóstico de operación, no confirmatorio de juicio

**4 donantes × 3 brazos × 5 batches temporales = 60 entregas.**

Donantes: investigaciones con replay exacto; evidencia suficiente y experimentos discriminantes;
comprensión pre-entrega correcta según rúbrica ciega; selección por la traza upstream, NO por R;
si no existen 4 elegibles, no se corre: se generan más donantes.

Brazos: (1) neutral, sin sufijo; (2) principio balanceado — las cuatro variantes congeladas,
rotadas balanceadamente; (3) scaffold explícito — checklist mecánico que obliga a mapear
evidencia→afirmación→rama de código, listar supuestos no identificados y propagar ruido medido
(upper bound operacional deliberado).

Protocolo: 5 bloques temporales, cada uno con los 4 donantes × 3 brazos aleatorizados e
intercalados; exactamente un turno de entrega, ningún observe()/experiment() nuevo; mismo
transcript y complejidad dentro de cada donante; modelo/snapshot/temperatura registrados;
tratamiento eliminado antes de anotar; IDs aleatorios; etiquetas antes de mirar R.

Endpoint primario: **entrega libre de defectos predefinidos** — solo firmas downstream:
(a) discrepancia conclusión pre-entrega vs código; (b) flecha causal no respaldada; (c) ruido
inventado o doble-contado; (d) rama observacional/default incompatible con la evidencia. NO incluir
"experimento no discriminante" (quedó congelado al seleccionar donantes). Secundarios: R y R_uncl,
tasa catastrófica, entrega válida, heterogeneidad por variante/donante/batch.

Lectura prefirmada:
- Scaffold mejora ≥30 puntos y en ≥4/5 batches → **operación scaffold-fixable**: se saca del core
  de juicio; el scaffold pasa a control/andamiaje del harness.
- Principio y scaffold mejoran parecido → también operación.
- R cambia sin cambiar las firmas → efecto inespecífico de prompt.
- Variantes cambian de signo → idiosincrasia lingüística.
- Nada cambia → manipulación fallida; no demuestra juicio.

Este fork no puede producir validación positiva fuerte de "juicio". Sí puede falsarla limpiamente.

### 2. Después del fork (sin esperar el factorial grande)

1. cerrar la clasificación operación/juicio; 2. reabrir construcción; 3. piloto Tübingen de un
mundo, timeboxed; 4. si el fork clasificó entrega como operación, incorporar el scaffold al harness
para que futuros mundos midan mejor el juicio upstream; 5. buscar terminación solo donde haya
baseline estable de parada temprana en varios batches.

Eso evita los dos errores: rebautizar una falla operacional para salvar el método, y dejar que
"validar primero" vuelva a enterrar el core de fábrica.

*(tokens de la ronda: ~1.43M)*
