# Operativa Codex–Claude para WAGER

> **Estado:** vigente desde 2026-08-02 · **Decisión:** Lucas · **Autoridad:** ADR 0172.

## Para qué existe

Esta separación existe para acelerar un ciclo científico: caso real → mundo mínimo fiel → agente
real → autopsia → explicaciones rivales → cambio de contenido → nueva prueba. No convierte el
proyecto en un flujo de ingeniería.

Separar dos trabajos que el proyecto venía mezclando:

- **Codex mantiene la visión superior:** qué importa investigar, qué aprendimos, si el mundo sirve,
  qué explicación rival queda viva y cuándo detener o pivotear.
- **Claude ejecuta y piensa en profundidad:** implementa slices, corre validaciones/agentes,
  inspecciona trazas, investiga subtareas y ofrece una segunda lectura crítica.

Lucas decide cambios de objetivo, autoridad externa y gasto material. Codex conduce el ciclo
cotidiano dentro de ese marco.

## Ciclo obligatorio

1. **Zoom out de Codex.** Antes de delegar: objetivo superior, estado de evidencia, por qué este
   mundo puede producir el fenómeno y qué resultado cambiaría la decisión.
2. **Encargo acotado.** Codex entrega a Claude una tarea con alcance, archivos, criterio de éxito o
   falsación, límite de gasto y condición de salida.
3. **Trabajo de Claude.** Claude implementa o analiza; preserva negativos y crudos; no expande la
   pregunta por iniciativa propia.
4. **Auditoría de Codex.** Codex lee el diff y la evidencia original, no solo el resumen de Claude.
   Puede pedir una crítica independiente o una alternativa, pero no una cadena ilimitada de retoques.
5. **Decisión superior.** Codex registra y comunica: MANTENER, MODIFICAR, PIVOTEAR o ABANDONAR.

Después de una señal válida se permite un solo control decisivo en el mismo anfitrión. El siguiente
paso debe cambiar de mundo/nivel o llevar una excepción explícita. Esta es una restricción de
proceso, no un recordatorio blando.

## Memoria que no depende del chat

- Codex recibe siempre `AGENTS.md`.
- Claude Code recibe siempre `CLAUDE.md`.
- Ambos deben consultar la cabecera de `docs/roadmap.md`, fuente única del estado científico.
- Este documento es la fuente única del reparto de roles.
- La sesión Claude worker se conserva entre encargos; su identificador local vive en
  `scratch/claude-worker-session.json` y no se versiona.
- `scripts/claude_worker.ps1` inyecta un recordatorio corto del rol en **cada** turno y fuerza los
  únicos modelos autorizados.

Cada tres encargos sustantivos —y siempre tras compactación, resultado sorpresivo o pivote— Codex
envía además un refresco completo: objetivo del proyecto, estado actual, límites del claim, rol de
cada parte y pregunta superior vigente.

## Dos modos de uso de Claude

### Worker

Implementar, ejecutar tests y agentes reales, producir análisis reproducibles y documentar. Debe
devolver: archivos cambiados, comprobaciones realizadas, crudos, resultados negativos, sorpresas y
pendientes reales. No hace commit/push ni acciones externas salvo autorización explícita.

### Contrapunto

Atacar diseños, interpretar resultados, proponer explicaciones rivales o nuevas direcciones. Codex
debe pedir una opinión independiente antes de exponer la propia cuando esa independencia importe.
La salida es insumo: Codex compara contra evidencia y decide.

## Chequeo de cierre de cada encargo

Claude termina con un bloque breve **“Nivel arriba”**:

1. qué aprendimos realmente;
2. qué no autoriza a concluir;
3. explicación rival principal;
4. si seguir en este mundo sigue siendo la acción de mayor valor.

Codex termina su revisión preguntándose lo mismo y verifica especialmente si está repitiendo el
patrón de mejorar el instrumento local en vez de mejorar el mundo o la pregunta.

## Canal técnico

El canal vigente es Claude Code CLI con sesión persistente, no MCP. El wrapper reanuda la sesión,
usa `fable/max` por defecto y solo permite `opus/max` como alternativa explícita. No hay fallback a
modelos menores. Para evitar colisiones, la sesión worker es exclusiva de Codex y distinta de la
sesión interactiva principal de Lucas.
