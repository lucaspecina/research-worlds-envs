# 0184 — Regla de episodios inválidos en la réplica DeepSeek

**Fecha**: 2026-08-13 · **Estado**: vigente · **Aplica**: ADR 0183.

Antes de ejecutar la primera partida se congela esta distinción: una falla externa de API,
harness o infraestructura pausa el gate y no entra al denominador; no se reemplaza sin una
enmienda previa. Una entrega inválida, `max_turns` o código roto producido por el agente sí cuenta
como no-cruce, porque forma parte de su capacidad para resolver la tarea. Ninguna seed se reejecuta.
