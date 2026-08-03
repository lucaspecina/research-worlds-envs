# Estrategia de modelos chicos para minería de vicios

> **Estado:** protocolo exploratorio vigente desde 2026-08-02. No es un pre-registro ni autoriza
> inferencia sobre modelos frontier.

## Objetivo

Usar modelos más baratos para recorrer rápidamente variaciones reales de mundo, historia,
interacción y presentación de evidencia; leer sus trazas; y encontrar condiciones prometedoras.
Después, congelar esas condiciones y comprobarlas con modelos fuertes en instancias que no hayan
sido usadas para iterar.

Los modelos chicos son **canarios y generadores de hipótesis**, no sustitutos baratos de la muestra
publicable. Si una falla aparece solo en ellos, puede servir como perfil de capacidad o como futuro
curriculum de entrenamiento, pero no sostiene un claim sobre agentes frontier.

## Escalera

| Etapa | Modelos candidatos disponibles en Foundry | Uso |
|---|---|---|
| Interfaz | `gpt-5.4-nano` o `Phi-4` | Endpoint, turnos, sandbox y entrega ejecutable; sin lectura conductual |
| Minería | `gpt-5.4-mini`; luego `Phi-4` si hace falta otra familia | Buscar firmas baratas antes de promoverlas |
| Puente | `DeepSeek-V3.2` | Comparar con la evidencia WAGER ya acumulada |
| Confirmación | `gpt-5.4` y una segunda familia frontier si el presupuesto lo permite | Estudio congelado sobre donantes/instancias reservados |

La restricción Fable/Opus del ADR 0172 rige al **Claude worker**, no a los modelos que actúan como
sujetos experimentales.

Los nombres de la tabla son los **deployments realmente disponibles** en `amalia-resource`,
verificados el 2026-08-02. `claude-haiku-4-5` figura desplegado pero no acepta el endpoint Chat
Completions usado por el harness actual; `qwen3-32b` no está desplegado. No se construye otra API
solo para esta minería mientras haya sujetos baratos compatibles.

## Gate para no confundir incapacidad con vicio

Una falla es candidata a vicio solo si el agente produce artefactos válidos, forma una creencia
previa sustantiva, resuelve el control limpio y la evidencia es recuperable por el oráculo
cero-LLM. Además se comparan, según el caso, RETAIN y un analista fresco.

- Timeout, contrato inválido o código roto: falla de interfaz; episodio censurado.
- No forma `Mpre` o falla también el control limpio: capacidad básica insuficiente.
- Nativo y analista fresco fallan igual: dificultad general de inferencia/modelado.
- El oráculo tampoco recupera la estructura: evidencia o mundo insuficiente.
- Pasa los controles pero falla tras su propia trayectoria: candidato real de revisión/compromiso.
- Revisa el modelo pero deja decisiones o artefactos viejos: candidato de propagación.
- Cambia también en RETAIN: sobreactualización o sugestibilidad.

Los inválidos y negativos se conservan y reportan; no se reinterpretan como terquedad.

## Ciclo rápido

1. Partir de un caso real y declarar qué condiciones se cree que causan la falla.
2. Materializarlas en el slice más chico **fiel**, sin rebajar el contrato real de entrega.
3. Correr pocos donantes por modelo chico y una condición deliberadamente extrema.
4. Leer transcript, experimentos, modelos intermedios y entrega; proponer explicaciones rivales.
5. Cambiar una sola decisión importante de contenido, no pulir infraestructura por inercia.
6. Promover una firma si aparece en al menos dos donantes y, de ser posible, dos familias.
7. Congelar diseño y probar DeepSeek/frontier con instancias reservadas.
8. Cerrar cada lote con **MANTENER / MODIFICAR / PIVOTEAR / ABANDONAR** y volver a auditar el
   mundo a nivel fundamental.
