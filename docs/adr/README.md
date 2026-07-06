# Decision Log — ADRs

> El registro de decisiones del proyecto, **una decisión por archivo** (patrón ADR,
> [adr.github.io](https://adr.github.io/)). **Append-only**: los archivos existentes son
> INMUTABLES; superseder una decisión = archivo nuevo que la referencia, y se anota el
> estado acá. La guardia `scripts/check_decision_log.py` (pre-commit) lo verifica.
> El *por qué/qué* del proyecto está en `WIKI.md` (llano) y `ARCHITECTURE.md` → `docs/reference/`.
>
> **Mapeo de citas**: los docs viejos citan "**Decision Log v0.NN**"; equivale al ADR con esa
> **Versión** (columna de abajo). Ej.: "Decision Log v0.64" → ADR 0064. El filename preserva el `v0.NN`.

| # | Versión | Fecha | Decisión | Estado |
|---|---------|-------|----------|--------|
| 0001 | v0.1 | 2026-06-09 | [Fundación](0001-v0.1-fundacion.md) | Vigente |
| 0002 | v0.2 | 2026-06-10 | [(v0.2)](0002-v0.2.md) | Vigente |
| 0003 | v0.3 | 2026-06-10 | [(v0.3)](0003-v0.3.md) | Vigente |
| 0004 | v0.4 | 2026-06-10 | [(v0.4)](0004-v0.4.md) | Vigente |
| 0005 | v0.5 | 2026-06-10 | [(v0.5)](0005-v0.5.md) | Vigente |
| 0006 | v0.6 | 2026-06-11 | [(v0.6)](0006-v0.6.md) | Vigente |
| 0007 | v0.7 | 2026-06-11 | [(v0.7)](0007-v0.7.md) | Vigente |
| 0008 | v0.8 | 2026-06-11 | [(v0.8)](0008-v0.8.md) | Vigente |
| 0009 | v0.9 | 2026-06-11 | [paquete de revisión general + validación](0009-v0.9-paquete-de-revision-general-validacion.md) | Vigente |
| 0010 | v0.10 | 2026-06-11 | [decisiones de implementación pre-Slice 1 (sesión de arranque de código)](0010-v0.10-decisiones-de-implementacion-pre-slice-1-sesion.md) | Vigente |
| 0011 | v0.11 | 2026-06-11 | [clarificación de librería + protocolo del Slice 1](0011-v0.11-clarificacion-de-libreria-protocolo-del-slice-1.md) | Vigente |
| 0012 | v0.12 | 2026-06-11 | [hallazgos del Slice 1 (la escalera L1 hizo su trabajo)](0012-v0.12-hallazgos-del-slice-1-la-escalera-l1-hizo-su-tra.md) | Vigente |
| 0013 | v0.13 | 2026-06-11 | [post-aprobación del Slice 1](0013-v0.13-post-aprobacion-del-slice-1.md) | Vigente |
| 0014 | v0.14 | 2026-06-11 | [Slice 2 (harness interactivo), secuencia LLM-first + C1 verde](0014-v0.14-slice-2-harness-interactivo-secuencia-llm-first.md) | Vigente |
| 0015 | v0.15 | 2026-06-11 | [C2 + C3 (harness completo): investigar gana, y E0/E0.5 jugados](0015-v0.15-c2-c3-harness-completo-investigar-gana-y-e0-e0-5.md) | Vigente |
| 0016 | v0.16 | 2026-06-11 | [diagnóstico obligatorio del "R=0 de DeepSeek": RETRACTACIÓN](0016-v0.16-diagnostico-obligatorio-del-r-0-de-deepseek-retr.md) | Vigente |
| 0017 | v0.17 | 2026-06-11 | [PRE-REGISTRACIÓN del slice de derivación (predicciones ANTES de correr)](0017-v0.17-pre-registracion-del-slice-de-derivacion-predicc.md) | Vigente |
| 0018 | v0.18 | 2026-06-11 | [certificado de brecha de teoría: predicción (i) CONFIRMADA (la disciplina caz...](0018-v0.18-certificado-de-brecha-de-teoria-prediccion-i-con.md) | Vigente |
| 0019 | v0.19 | 2026-06-11 | [reglas anti-sesgo de la derivación + certificados completos del dummy](0019-v0.19-reglas-anti-sesgo-de-la-derivacion-certificados.md) | Vigente |
| 0020 | v0.20 | 2026-06-11 | [battery_builder + gemelo (rival b) + aceptación (i) parcial (para auditoría h...](0020-v0.20-battery-builder-gemelo-rival-b-aceptacion-i-parc.md) | Vigente |
| 0021 | v0.21 | 2026-06-11 | [decisión del ancla (cap universal): la verificación destapó un bug crítico + ...](0021-v0.21-decision-del-ancla-cap-universal-la-verificacion.md) | Vigente |
| 0022 | v0.22 | 2026-06-11 | [doctrina "escala antes que historias" + reglas formalizadas (PRE-REGISTRO ant...](0022-v0.22-doctrina-escala-antes-que-historias-reglas-forma.md) | Vigente |
| 0023 | v0.23 | 2026-06-11 | [auditoría humana del top-10: verificación de contrato (PRE-REGISTRO)](0023-v0.23-auditoria-humana-del-top-10-verificacion-de-cont.md) | Vigente |
| 0024 | v0.24 | 2026-06-11 | [ronda de hardening de la batería (PRE-REGISTRO; mea culpa + protocolo nuevo)](0024-v0.24-ronda-de-hardening-de-la-bateria-pre-registro-me.md) | Vigente |
| 0025 | v0.25 | 2026-06-12 | [PRE-REGISTRO Latent (2º mundo: heterogeneidad de efecto por grado latente; pr...](0025-v0.25-pre-registro-latent-2o-mundo-heterogeneidad-de-e.md) | Vigente |
| 0026 | v0.26 | 2026-06-12 | [DECISIÓN (A) funcionales de stakes + spec-first (SPEC escrito ANTES de codear...](0026-v0.26-decision-a-funcionales-de-stakes-spec-first-spec.md) | Vigente |
| 0027 | v0.27 | 2026-06-12 | [VEREDICTO sobre el spec (A) (triangulado con 2ª IA): (A) se sostiene y se REF...](0027-v0.27-veredicto-sobre-el-spec-a-triangulado-con-2a-ia.md) | Vigente |
| 0028 | v0.28 | 2026-06-12 | [score combinado: dos decisiones de implementación antes de codear (trianguladas)](0028-v0.28-score-combinado-dos-decisiones-de-implementacion.md) | Vigente |
| 0029 | v0.29 | 2026-06-12 | [acceso de rivales (β): modos (d-obs)/(d-exp) + brecha de teoría = contrafácti...](0029-v0.29-acceso-de-rivales-modos-d-obs-d-exp-brecha-de-te.md) | Vigente |
| 0030 | v0.30 | 2026-06-12 | [auditoría código-vs-docs por iniciativa propia: fix de §5 + checklist de supe...](0030-v0.30-auditoria-codigo-vs-docs-por-iniciativa-propia-f.md) | Vigente |
| 0031 | v0.31 | 2026-07-01 | [cierre de pendientes v0.24 + PRE-REGISTRO del protocolo de calibración de `c_...](0031-v0.31-cierre-de-pendientes-v0-24-pre-registro-del-prot.md) | Vigente |
| 0032 | v0.32 | 2026-07-02 | [migración de repo + sincronización de headers (deriva doc-doc; aprobada por L...](0032-v0.32-migracion-de-repo-sincronizacion-de-headers-deri.md) | Vigente |
| 0033 | v0.33 | 2026-07-02 | [hardening post-re-skin: auditoría de artefactos semánticos + lint de headers ...](0033-v0.33-hardening-post-re-skin-auditoria-de-artefactos-s.md) | Vigente |
| 0034 | v0.34 | 2026-07-02 | [bloque consolidado de Lucas: grilla de calibración VERBATIM + enmiendas pre-e...](0034-v0.34-bloque-consolidado-de-lucas-grilla-de-calibracio.md) | Vigente |
| 0035 | v0.35 | 2026-07-02 | [RESULTADOS del primer barrido de `c_F`: la guardia pre-registrada DISPARÓ — f...](0035-v0.35-resultados-del-primer-barrido-de-c-f-la-guardia.md) | Vigente |
| 0036 | v0.36 | 2026-07-02 | [LECTURA ACEPTADA de v0.35 + las 3 decisiones (Lucas) + pre-registro del DO-OVER](0036-v0.36-lectura-aceptada-de-v0-35-las-3-decisiones-lucas.md) | Vigente |
| 0037 | v0.37 | 2026-07-02 | [RESULTADOS del do-over: TODOS los gates pasan en todo el rango → `c_F*=0` → l...](0037-v0.37-resultados-del-do-over-todos-los-gates-pasan-en.md) | Vigente |
| 0038 | v0.38 | 2026-07-02 | [DECISIÓN (Lucas): OPCIÓN 1 — gate de visibilidad = max(3×std propio, PISO DE ...](0038-v0.38-decision-lucas-opcion-1-gate-de-visibilidad-max.md) | Vigente |
| 0039 | v0.39 | 2026-07-02 | [PASADA DE GENERALIZACIÓN DE LA FACTORY (la clase "recita el schema del dummy"...](0039-v0.39-pasada-de-generalizacion-de-la-factory-la-clase.md) | Vigente |
| 0040 | v0.40 | 2026-07-02 | [RESULTADOS de P2 (corrida 1): celda **AMBOS GRANDES** del árbol firmado → gua...](0040-v0.40-resultados-de-p2-corrida-1-celda-ambos-grandes-d.md) | Vigente |
| 0041 | v0.41 | 2026-07-02 | [VERIFICACIÓN del colapso (mecanismo CONFIRMADO, no narrado) + doctrina de la ...](0041-v0.41-verificacion-del-colapso-mecanismo-confirmado-no.md) | Vigente |
| 0042 | v0.42 | 2026-07-02 | [P2 corridas 2–3: bug del null en el tooling (v0.12 reintroducida, 6ª de la fa...](0042-v0.42-p2-corridas-23-bug-del-null-en-el-tooling-v0-12.md) | Vigente |
| 0043 | v0.43 | 2026-07-04 | [LECTURA de v0.42 (Lucas): "la 2×2 cambió de moneda — el cuello de botella es ...](0043-v0.43-lectura-de-v0-42-lucas-la-22-cambio-de-moneda-el.md) | Vigente |
| 0044 | v0.44 | 2026-07-04 | [RESULTADOS del cuadrante |ΔP| (localización per-régimen, n=4000): AMBAS predi...](0044-v0.44-resultados-del-cuadrante-p-localizacion-per-regi.md) | Vigente |
| 0045 | v0.45 | 2026-07-04 | [GO a la sonda de residuos empíricos (Lucas): retractación doble + spec pre-re...](0045-v0.45-go-a-la-sonda-de-residuos-empiricos-lucas-retrac.md) | Vigente |
| 0046 | v0.46 | 2026-07-04 | [RESULTADOS de la ronda de CIERRE: salida **(C) con matiz** — el supremo de la...](0046-v0.46-resultados-de-la-ronda-de-cierre-salida-c-con-ma.md) | Vigente |
| 0047 | v0.47 | 2026-07-04 | [CIERRE ACEPTADO (Lucas) + SPEC-FIRST de v2 (enmienda ARCHITECTURE §10.1 + bri...](0047-v0.47-cierre-aceptado-lucas-spec-first-de-v2-enmienda.md) | Vigente |
| 0048 | v0.48 | 2026-07-04 | [DECISIÓN DE ORDEN (Lucas): MUNDO 3 PRIMERO, v2 segundo + pre-registros del mu...](0048-v0.48-decision-de-orden-lucas-mundo-3-primero-v2-segun.md) | Vigente |
| 0049 | v0.49 | 2026-07-04 | [lint a PRE-COMMIT (hecho) + PLAN CORTO del mundo 3 (antes de codear)](0049-v0.49-lint-a-pre-commit-hecho-plan-corto-del-mundo-3-a.md) | Vigente |
| 0050 | v0.50 | 2026-07-04 | [plan del mundo 3 APROBADO con TRES CIERRES en el contrato de fuentes (decisio...](0050-v0.50-plan-del-mundo-3-aprobado-con-tres-cierres-en-el.md) | Vigente |
| 0051 | v0.51 | 2026-07-04 | [CIERRE #4 del contrato de fuentes (Lucas; misma familia que el sesgo, un mome...](0051-v0.51-cierre-4-del-contrato-de-fuentes-lucas-misma-fam.md) | Vigente |
| 0052 | v0.52 | 2026-07-04 | [dos agregados de contrato (Lucas) y CÓDIGO](0052-v0.52-dos-agregados-de-contrato-lucas-y-codigo.md) | Vigente |
| 0053 | v0.53 | 2026-07-04 | [sesión 1 aceptada + tres registros antes de world.py (Lucas)](0053-v0.53-sesion-1-aceptada-tres-registros-antes-de-world.md) | Vigente |
| 0054 | v0.54 | 2026-07-04 | [sesión 2 EN CURSO: causa raíz del sweep + identificación CONDICIONAL AL ORDEN...](0054-v0.54-sesion-2-en-curso-causa-raiz-del-sweep-identific.md) | Vigente |
| 0055 | v0.55 | 2026-07-04 | [GO con elevación (Lucas): el ruteo pool→vista es LA CLASE PREDICHA, no un fix...](0055-v0.55-go-con-elevacion-lucas-el-ruteo-poolvista-es-la.md) | Vigente |
| 0056 | v0.56 | 2026-07-04 | [v0.55 aceptado: pin como validación del no-op + LÍNEA BRILLANTE del tuning de...](0056-v0.56-v0-55-aceptado-pin-como-validacion-del-no-op-lin.md) | Vigente |
| 0057 | v0.57 | 2026-07-04 | [tres puntos pre-tramo-final (Lucas): guardias con autotest + wiring #19 VERIF...](0057-v0.57-tres-puntos-pre-tramo-final-lucas-guardias-con-a.md) | Vigente |
| 0058 | v0.58 | 2026-07-04 | [tres registros de Lucas + GO al tramo final](0058-v0.58-tres-registros-de-lucas-go-al-tramo-final.md) | Vigente |
| 0059 | v0.59 | 2026-07-05 | [MODO AUTONOMÍA, tramo final ejecutado (registro batch; firmas ANTES de mirar E0)](0059-v0.59-modo-autonomia-tramo-final-ejecutado-registro-ba.md) | Vigente |
| 0060 | v0.60 | 2026-07-05 | [E0 corrido (2+2 episodios gpt-5.4): familia #19 CAZADA y corregida en la corr...](0060-v0.60-e0-corrido-2-2-episodios-gpt-5-4-familia-19-caza.md) | Vigente |
| 0061 | v0.61 | 2026-07-05 | [v2 hasta el GATE del ancla (freno tripwire-1) + matriz E1 (borrador)](0061-v0.61-v2-hasta-el-gate-del-ancla-freno-tripwire-1-matr.md) | Vigente |
| 0062 | v0.62 | 2026-07-05 | [dossier de inspección humana END-TO-END (pedido de Lucas)](0062-v0.62-dossier-de-inspeccion-humana-end-to-end-pedido-d.md) | Vigente |
| 0063 | v0.63 | 2026-07-05 | [GATE DEL ANCLA: spec APROBADO (Lucas) con rationale + 5 correcciones ANTES de...](0063-v0.63-gate-del-ancla-spec-aprobado-lucas-con-rationale.md) | Vigente |
| 0064 | v0.64 | 2026-07-05 | [v2 CABLEADO Y CERTIFICADO + E0-v2: el tríptico confirma su predicción estruct...](0064-v0.64-v2-cableado-y-certificado-e0-v2-el-triptico-conf.md) | Vigente |
| 0065 | v0.65 | 2026-07-05 | [#6 (hermano presupuesto-escaso) CORRIDO: la escasez SÍ muerde en R, con la ar...](0065-v0.65-6-hermano-presupuesto-escaso-corrido-la-escasez.md) | Vigente |
| 0066 | v0.66 | 2026-07-05 | [CONSOLIDACIÓN v2 (orden de Lucas: E0.5, 6 episodios nuevos, 2ª familia): el t...](0066-v0.66-consolidacion-v2-orden-de-lucas-e0-5-6-episodios.md) | Vigente |
| 0067 | v0.67 | 2026-07-05 | [CONSOLIDACIÓN #6 (E0.5: 4 episodios, 2ª familia): la escasez replica, y se AF...](0067-v0.67-consolidacion-6-e0-5-4-episodios-2a-familia-la-e.md) | Vigente |
| 0068 | v0.68 | 2026-07-05 | [#6 ACEPTADA (Lucas, 3 registros) + GO MUNDO #11 con el doc de contexto y trat...](0068-v0.68-6-aceptada-lucas-3-registros-go-mundo-11-con-el.md) | Vigente |
| 0069 | v0.69 | 2026-07-05 | [REESTRUCTURA DE DOCS (orden de Lucas: "los docs crecieron brutalmente"; opció...](0069-v0.69-reestructura-de-docs-orden-de-lucas-los-docs-cre.md) | Vigente |
| 0070 | v0.70 | 2026-07-05 | [Reestructura de docs a estructura best-practice (WIKI + ADRs + NORTH_STAR disuelto)](0070-v0.70-reestructura-de-docs-a-best-practice.md) | Vigente |
| 0071 | v0.71 | 2026-07-05 | [Re-skin de casos a "línea de proceso" (neutral, anti-flag)](0071-v0.71-re-skin-a-linea-de-proceso.md) | Vigente |
| 0072 | v0.72 | 2026-07-05 | [Consolidaciones finales de docs (ARCHITECTURE→reference, CURRENT_STATE→roadmap, REDTEAM→test)](0072-v0.72-consolidaciones-finales-de-docs.md) | Vigente |
| 0073 | v0.73 | 2026-07-05 | [Auditoría post-reestructura y fixes (14 findings, método de dos frentes)](0073-v0.73-auditoria-post-reestructura-y-fixes.md) | Vigente |
| 0074 | v0.74 | 2026-07-05 | [Mundo #11 (logistic_yield_v0): el formalismo 2 VALIDADO — una extensión trivial, dos deudas](0074-v0.74-mundo-11-logistic-yield-v0-el-formalismo-2-valida.md) | Vigente |
| 0075 | v0.75 | 2026-07-05 | [Orden de trabajo (Lucas): ejecutar lo conocido primero; el diseño se piensa juntos, después](0075-v0.75-orden-de-trabajo-ejecutar-lo-conocido-primero.md) | Vigente |
| 0076 | v0.76 | 2026-07-05 | [Hallazgo #12: la trampa de truncación requiere DEGENERACIÓN temprana — cascada lineal no certifica](0076-v0.76-hallazgo-12-la-trampa-de-truncacion-requiere-degeneracion.md) | Vigente |
| 0077 | v0.77 | 2026-07-06 | [Mundo #7 (survivorship_censor_v0): capa ARCHIVAL nueva, certificado en dos coordenadas](0077-v0.77-mundo-7-survivorship-censor-v0-capa-archival-nueva.md) | Vigente |
| 0078 | v0.78 | 2026-07-06 | [Mundo #9 (batch_confound_v0): deriva confundida con la rampa — maquinaria batch, dos coordenadas](0078-v0.78-mundo-9-batch-confound-v0-deriva-confundida-certificada.md) | Vigente |
| 0079 | v0.79 | 2026-07-06 | [Mundo #16 (prior_sweetspot_v0): control de prior-confiable — el frontier toca el techo](0079-v0.79-mundo-16-prior-sweetspot-v0-control-de-prior-confiable.md) | Vigente |
| 0080 | v0.80 | 2026-07-06 | [Doctrina anti-vicio: molde unificador ACEPTADO con cuatro correcciones load-bearing](0080-v0.80-doctrina-anti-vicio-molde-unificador-con-cuatro-correcciones.md) | Vigente |
| 0081 | v0.81 | 2026-07-06 | [Mundo A: decisiones D1-D5 firmadas + robots por el pipeline de episodio real](0081-v0.81-mundo-a-decisiones-d1-d5-firmadas-robots-por-episodio.md) | Vigente |
| 0082 | v0.82 | 2026-07-06 | [Mundo #17 (first_story_v0): el PRIMER certificado de trampa necesaria — terco 0.005 vs cuidadoso 0.960](0082-v0.82-mundo-17-first-story-v0-primer-certificado-de-trampa-necesaria.md) | Vigente |
| 0083 | v0.83 | 2026-07-06 | [Maquinaria de eventos D4: la noticia sellada funciona — certificado de incorporación ALL-PASS](0083-v0.83-maquinaria-de-eventos-d4-la-noticia-sellada-funciona.md) | Vigente |
| 0084 | v0.84 | 2026-07-06 | [Mundo B: el corazón probado, tres decisiones de carpintería fina — entra como encargo difícil de la fábrica](0084-v0.84-mundo-b-el-corazon-probado-tres-decisiones-y-via-fabrica.md) | Vigente |
| 0085 | v0.85 | 2026-07-06 | [Eje anchura/enmascaramiento para el diseñador + piloto ancho pre-registrado](0085-v0.85-eje-anchura-enmascaramiento-para-el-disenador-y-piloto-ancho.md) | Vigente |
| 0086 | v0.86 | 2026-07-06 | [Piloto ancho fuera de la escalera + LEDGER de pendientes como regla + partición seed31 (retractación)](0086-v0.86-piloto-ancho-fuera-de-la-escalera-ledger-de-pendientes.md) | Vigente |
| 0087 | v0.87 | 2026-07-06 | [Celda escasez×vicio corrida: los hábitos sobreviven — la terminación no](0087-v0.87-celda-escasez-vicio-corrida-los-habitos-sobreviven-la-terminacion-no.md) | Vigente |
| 0088 | v0.88 | 2026-07-06 | [Retractación simétrica + re-lectura #6 (rushed_termination unánime en gpt) + firma nueva + vigilancia del cap](0088-v0.88-retractacion-simetrica-relectura-6-firma-rushed-termination.md) | Vigente |
| 0089 | v0.89 | 2026-07-06 | [Piloto ancho, fase instrumento: la anchura DILUYE los dientes del examen (7ª mordida de escala, cazada pre-E0)](0089-v0.89-piloto-ancho-fase-instrumento-la-anchura-diluye-los-dientes.md) | Vigente |
