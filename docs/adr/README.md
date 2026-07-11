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
| 0090 | v0.90 | 2026-07-06 | [Barrido c_F sampling: TECHO DE ANCHURA confirmado; c_F* narrow=0.25 vindicado; decision d/split pendiente](0090-v0.90-barrido-cf-sampling-corrido-techo-de-anchura-confirmado.md) | Vigente |
| 0091 | v0.91 | 2026-07-06 | [Opcion (d) firmada + c_F=0.25 congelado + diagnostico profundo (energy=model-recovery indiscriminado) + candado selectivo](0091-v0.91-opcion-d-firmada-cf-congelado-diagnostico-profundo-candado-selectivo.md) | Vigente |
| 0092 | v0.92 | 2026-07-06 | [Compuerta del candado CERRADA: el funcional no es gameable (oracle-gamer R=-0.53); (d) puro; freeze c_F doblemente correcto](0092-v0.92-compuerta-del-candado-cerrada-el-funcional-no-es-gameable.md) | Vigente |
| 0093 | v0.93 | 2026-07-06 | [Proto-designer: spec de trabajo de la fabrica automatica (consigna->generador->certificacion->yield); escalera facil/medio/Mundo B](0093-v0.93-proto-designer-spec-de-trabajo.md) | Vigente |
| 0094 | v0.94 | 2026-07-06 | [Proto-designer MEDIO: el generador anda, el verificador generico necesita completarse (cadena de deudas); freno antes del rabbit-hole](0094-v0.94-proto-designer-medio-el-generador-anda-el-verificador-generico-necesita-completarse.md) | Vigente |
| 0095 | v0.95 | 2026-07-06 | [Experimento de validez libre vs cuidadoso (trampas vs controles): PRE-REGISTRO firmado antes de mirar](0095-v0.95-experimento-de-validez-libre-vs-cuidadoso-preregistro-firmado.md) | Vigente |
| 0096 | v0.96 | 2026-07-06 | [Experimento de validez CORRIDO: la prediccion primaria FALLO -- el cuidado mueve fiabilidad general, no un vicio; subpotenciado](0096-v0.96-experimento-de-validez-corrido-la-prediccion-primaria-fallo.md) | Vigente |
| 0097 | v0.97 | 2026-07-06 | [Experimento de pista ESPECIFICA por vicio (idea original de Lucas): pre-registro firmado antes de mirar](0097-v0.97-experimento-pista-especifica-por-vicio-preregistro.md) | Vigente |
| 0098 | v0.98 | 2026-07-06 | [Experimento de pista especifica CORRIDO: con mediana + ejecucion-vs-juicio, la pista dirigida AISLA el vicio -- senal positiva de validez](0098-v0.98-experimento-de-pista-especifica-la-pista-dirigida-aisla-el-vicio.md) | Vigente |
| 0099 | v0.99 | 2026-07-06 | [Catalogo de failure modes + scaffold de diseno (docs/failure-modes.md): taxonomia por dinamica de mundo](0099-v0.99-catalogo-de-failure-modes-scaffold-de-diseno.md) | Vigente |
| 0100 | v1.00 | 2026-07-06 | [El corte primario OPERACION vs JUICIO: define el alcance de WAGER y ordena el catalogo (correccion de Lucas)](0100-v1.00-corte-primario-operacion-vs-juicio.md) | Vigente |
| 0101 | v1.01 | 2026-07-07 | [Cosecha deep-research integrada al catalogo (19 claims verificadas); familia G (causal) PROPUESTA pendiente OK](0101-v1.01-cosecha-deep-research-integrada-familia-causal-propuesta.md) | Vigente |
| 0102 | v1.02 | 2026-07-07 | [Familia G (razonamiento causal) ADOPTADA como grupo propio del catalogo (decision de Lucas)](0102-v1.02-familia-g-causal-adoptada.md) | Vigente |
| 0103 | v1.03 | 2026-07-07 | [Diversidad ESTRUCTURAL por vicio (no solo de disfraz) como requisito anti-overfitting (precision de Lucas)](0103-v1.03-diversidad-estructural-por-vicio.md) | Vigente |
| 0104 | v1.04 | 2026-07-07 | [Case-search: mapa de estructuras rebuildables por vicio; puntos ciegos #4/#5/#2 identificados](0104-v1.04-case-search-mapa-de-estructuras-por-vicio.md) | Vigente |
| 0105 | v1.05 | 2026-07-07 | [3a busqueda (puntos ciegos): vicios 4/5/2 llenados; nuevo hueco = colisionador/seleccion (vicio 7)](0105-v1.05-tercera-busqueda-puntos-ciegos-llenados.md) | Vigente |
| 0106 | v1.06 | 2026-07-09 | [Catalogo espejo de AHAs + doctrina de PARES (certificado y metrica) + decision de construccion: Neptuno/Vulcano](0106-v1.06-catalogo-espejo-de-ahas-doctrina-de-pares-decision-neptuno-vulcano.md) | Vigente |
| 0107 | v1.07 | 2026-07-09 | [Cola de trabajo UNICA + regla de WIP (auditoria de organizacion pedida por Lucas)](0107-v1.07-cola-de-trabajo-unica-y-regla-wip.md) | Vigente |
| 0108 | v1.08 | 2026-07-09 | [Cola reordenada por VALOR, no por orden de llegada (orden de Lucas)](0108-v1.08-cola-reordenada-por-valor.md) | Vigente |
| 0109 | v1.09 | 2026-07-09 | [La definicion operativa del juicio investigativo (dos polos; la lista NO es el juicio)](0109-v1.09-definicion-operativa-del-juicio-dos-polos.md) | Vigente |
| 0110 | v1.10 | 2026-07-09 | [Replica DeepSeek de la validez (ADR 0098): la senal positiva se sostiene con un 2do modelo (+ hallazgo de perfil)](0110-v1.10-replica-deepseek-validez-se-sostiene.md) | Vigente |
| 0111 | v1.11 | 2026-07-09 | [Hallazgo con nombre: PERFILES DE VICIO POR MODELO (la presion es PERILLA calibrable por modelo, no ingrediente necesario)](0111-v1.11-perfiles-de-vicio-por-modelo-presion-es-perilla.md) | Vigente |
| 0112 | v1.12 | 2026-07-09 | [Auditoria cruzada cartera-vs-catalogo: tres capas + dos niveles de diversidad; decisiones de cartera; tabla de re-derivacion (papel)](0112-v1.12-auditoria-cruzada-cartera-vs-catalogo-tres-capas.md) | Vigente |
| 0113 | v1.13 | 2026-07-09 | [Derivacion oficial vicio->mundo, catalogo-primero (docs/mundos-por-vicio.md)](0113-v1.13-derivacion-oficial-vicio-a-mundo-catalogo-primero.md) | Vigente |
| 0114 | v1.14 | 2026-07-09 | [El foco de la documentacion de vicios es IA-INVESTIGADORA; lo humano al margen (correccion de Lucas)](0114-v1.14-foco-ia-en-la-documentacion-de-vicios.md) | Vigente (claim "busqueda lanzada" CORREGIDO en 0115) |
| 0115 | v1.15 | 2026-07-09 | [Regla: los papers se leen a TEXTO COMPLETO; registro de lectura; correccion de un claim falso de 0114](0115-v1.15-regla-leer-papers-texto-completo-registro.md) | Vigente |
| 0116 | v1.16 | 2026-07-10 | [Codex (GPT-5.6 Sol) como segunda opinion de diseno/reflexion, NO como escritor de codigo](0116-v1.16-codex-como-segunda-opinion-de-diseno.md) | Vigente |
| 0117 | v1.17 | 2026-07-10 | [Lo FUNDAMENTAL es disenar mundos-vicio generables automaticamente con diversidad; los gemelos son AGREGADO (decision de Lucas tras la ronda Codex)](0117-v1.17-fundamento-fabrica-de-mundos-vicio-gemelos-agregado.md) | Vigente |
| 0118 | v1.18 | 2026-07-10 | [PRE-REGISTRO: experimento de pista CORREGIDO y minimo (misma pista + control con headroom + placebo; 1 modelo)](0118-v1.18-preregistro-experimento-pista-corregido-minimo.md) | Vigente — PRE-REGISTRO firmado; adenda sellada en 0119 |
| 0119 | v1.19 | 2026-07-10 | [SELLO PRE-APERTURA: analisis secundarios y limites de interpretacion de 0118 + implicancias fabrica de la ronda 2 de Codex](0119-v1.19-sello-pre-apertura-analisis-secundarios-0118-e-implicancias-ronda2.md) | Vigente — SELLO (firmado a ~11/46 episodios, cero contrastes vistos) |
| 0120 | v1.20 | 2026-07-10 | [Canonico LEGAL (legal_plan_v0) factorizado por regimen: cierre de D1 sobre el fixture de desarrollo (0.8929 -> 0.9966 ALL-PASS; reskin 0.9848 ALL-PASS)](0120-v1.20-canonico-legal-plan-v0-factorizado-por-regimen.md) | Vigente (gate por particion ENMENDADO a regret absoluto — Codex ronda 4, commit post-f08643c) |
| 0121 | v1.21 | 2026-07-10 | [AUTOPSIA del experimento 0118 (protocolo sellado): metodo de pistas RETIRADO como evidencia de validez; fragilidad corrida-a-corrida documentada](0121-v1.21-autopsia-0118-metodo-de-pistas-retirado.md) | Vigente — RESULTADO NEGATIVO (alcance del "retiro" acotado por 0122) |
| 0122 | v1.22 | 2026-07-10 | [El metodo de pistas NO se abandona (decision de Lucas): el negativo de 0121 ordena redisenar la MEDICION, no matar el metodo](0122-v1.22-el-metodo-de-pistas-no-se-abandona-redisenar-la-medicion.md) | Vigente |
| 0123 | v1.23 | 2026-07-10 | [Dos papers integrados: el "reflejo de sintesis" (tier A, justificacion del proyecto) + validacion independiente del par Vulcano](0123-v1.23-dos-papers-integrados-sintesis-reflejo-tierA-y-validacion-vulcano.md) | Vigente |
| 0124 | v1.24 | 2026-07-10 | [Protocolo HONESTO de validez-por-pista en 3 fases (redisenio de 0122, con Codex ronda 5): 3 eslabones, control epistemico activo, metricas de tasa](0124-v1.24-protocolo-honesto-de-validez-por-pista-3-fases.md) | Vigente — concretado por 0125 |
| 0125 | v1.25 | 2026-07-10 | [Disenio concreto de pistas v2: PRINCIPIOS balanceados derivados del catalogo + VARIANTES como unidad de robustez + factorial simetrico (ideas de Lucas + Codex r6; 480 episodios en Fase 3)](0125-v1.25-disenio-concreto-pistas-v2-principios-variantes-factorial.md) | Vigente — Fase 1 ejecutable YA; Fase 3 espera GO |
| 0126 | v1.26 | 2026-07-10 | [DOCTRINA: por que WAGER si el RLVR sobre tareas abiertas verificables ya existe — la pregunta existencial consolidada (notas de Lucas + feedback externo + Codex r7/r8)](0126-v1.26-doctrina-por-que-wager-si-rlvr-ya-existe.md) | Vigente |
| 0127 | v1.27 | 2026-07-10 | [PRE-REGISTRO de la AUTOPSIA de pistas (Fase 1): taxonomia ciega de fallos + banco de 10 variantes congelado ANTES de correr; 16 episodios con registro completo](0127-v1.27-preregistro-autopsia-pistas-fase1.md) | Vigente — PRE-REGISTRO firmado |
| 0128 | v1.28 | 2026-07-10 | [Decision de construccion (delegada por Lucas a Claude+Codex): piloto fresco -> micro-batch N=5 -> plantilla de RIGOR ESTADISTICO; el pozo se degrada a perilla](0128-v1.28-decision-de-construccion-piloto-microbatch-rigor.md) | Vigente |
| 0129 | v1.29 | 2026-07-10 | [Resultado autopsia Fase 1: varianza demostrada en 3 corridas (+0.52/-0.58/+0.64); T4 atractor-preexistente gana a T2; el fallo vive en la ENTREGA](0129-v1.29-autopsia-fase1-resultado-varianza-demostrada-t4-gana.md) | Vigente (veredicto MATIZADO por 0130) |
| 0130 | v1.30 | 2026-07-10 | [Auditoria r10 matiza 0129: cuello HETEROGENEO; el FORK pasa a experimento central; first_story_scarce degradado como confirmatorio para DeepSeek](0130-v1.30-auditoria-r10-matiza-0129-fork-central-first-story-degradado.md) | Vigente |
| 0131 | v1.31 | 2026-07-10 | [Micro-batch N=5: yield mecanico 5/5, colapso de dominio y parametros MEDIDO por el panel; maquinaria del fork verificada](0131-v1.31-microbatch-5de5-colapso-medido-fork-maquinaria-ok.md) | Vigente |
| 0132 | v1.32 | 2026-07-10 | [Tres vias de generacion de motores registradas (plantilla+composicion / semilla-paper / semilla-simulador); Tubingen PREFERIDA para diversidad profunda y DIFERIDA; el slot vuelve a validar](0132-v1.32-tres-vias-de-generacion-de-motores-tubingen-preferida-diferida.md) | Vigente |
| 0133 | v1.33 | 2026-07-10 | [GO al fork diagnostico (pre-registro completo: 4 donantes x 3 brazos x 5 bloques) + regla de limite duro: terminado el fork se reabre construccion, calibrar-mundos-primero (piloto Tubingen en esa tanda)](0133-v1.33-go-fork-diagnostico-preregistro-y-regla-limite-duro.md) | Vigente — PRE-REGISTRO firmado |
| 0134 | v1.34 | 2026-07-11 | [Resultado del fork: manipulacion por susurro FALLA (0/0/5.3% limpias); defectos de integracion UNIVERSALES (59/60), deterministas por donante, y el score NO los ve (R 0.98 con flechas sin respaldo); se reabre construccion (limite duro)](0134-v1.34-fork-resultado-manipulacion-fallida-defectos-universales-score-desacoplado.md) | Vigente |
| 0135 | v1.35 | 2026-07-11 | [El probe de TRADUCCION es bloqueante (pregunta de Lucas): diseno de 3 brazos + escalera de creencias adoptado (Codex r12); DeliverySpec v1 + audit cero-LLM primero; nada se construye hasta su veredicto](0135-v1.35-probe-de-traduccion-bloqueante-diseno-adoptado-orden.md) | Vigente |
| 0136 | v1.36 | 2026-07-11 | [Resultado del probe: el CANAL DE ENTREGA ESTA SANO (45/45 al piso; orden de creencias preservado 5/5 con separacion 1x/31x/2143x); el desacople era BATERIA INSUFICIENTE con receta; DeliverySpec v1 adoptado; el bloqueo se levanta](0136-v1.36-probe-resultado-canal-sano-orden-preservado-bateria-insuficiente.md) | Vigente |
