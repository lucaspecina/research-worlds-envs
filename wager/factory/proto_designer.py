"""Proto-designer -- the world GENERATOR half of the factory (ADR 0093).

FACTORY SIDE: LLMs are allowed here (the reward path stays zero-LLM; a generated
world.py is verified ONLY by the zero-LLM certification pipeline). This module is
never imported by wager.reward.

Rung 1 (FACIL, re-skin): re-skin a certified world into a NEW domain with the
mathematics IDENTICAL, and verify the certificates' R values are preserved (a
no-op test of the generator plumbing). Higher rungs (new static world, World B)
compose from the operator library and are added as their commissions are signed
(decisions A/B/C/D of docs/proto-designer.md).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RESKIN_SYSTEM = (
    "You are a world-designer on the factory side of an ML research harness. You re-skin "
    "an existing simulated 'world' into a NEW industrial/scientific domain WITHOUT changing "
    "any mathematics. A pure vocabulary/domain swap: mechanism, all numbers and all structure "
    "stay byte-for-byte equivalent; only human-facing names and prose change."
)

RESKIN_RULES = """Re-skin this world into a NEW concrete domain of your choice, different from
the source. HARD RULES (a verifier checks them mechanically):

1. CHANGE the column names to fit the new domain, keeping their ROLES (the settable decision
   knob; any inline reading(s); the final quality/outcome score with its threshold).
2. CHANGE all prose: column descriptions, the stakes narrative, the brief, the notes.
3. KEEP EVERY NUMBER IDENTICAL: all PARAMS values, knobs/ablations, functional threshold and
   direction, all weights/budgets/costs/seeds, n_samples/m_reps/lambda_mdl/c_f.
4. KEEP the mechanism STRUCTURE identical: the same equations in world.py, the same operator
   name+knobs+ablation in meta, the same smoke_regimes shape.
5. KEEP the PARAMS dict KEYS identical -- only the COLUMN names change, never internal keys.
6. The functional's "column" must be your NEW outcome column name; its "brief_clause" must be
   a sentence appearing VERBATIM in your new brief.md (copy it exactly).
7. In world.py, COLUMNS and the returned DataFrame keys are your new column names; the
   regime.config / control_surface settable keys use the new decision-knob name.

Return EXACTLY three fenced code blocks, each preceded by a line with only its filename:
world.py
```python
...
```
meta.json
```json
...
```
brief.md
```markdown
...
```
No other prose."""


def _extract_blocks(text: str) -> dict:
    blocks = {}
    for name, lang in (("world.py", "python"), ("meta.json", "json"), ("brief.md", "markdown")):
        m = re.search(rf"{re.escape(name)}\s*```(?:{lang}|\w*)?\n(.*?)```", text, re.S)
        blocks[name] = (m.group(1).rstrip() + "\n") if m else None
    return blocks


def reskin(source_dir: Path, target_dir: Path, model: str = "gpt-5.4") -> dict:
    """Generate a re-skinned world and CERTIFY it. Returns a yield record:
    {passed: bool, r_identical: bool, gates_ok: bool, domain, reason}."""
    from wager.agent.llm_client import FoundryChat  # lazy: keeps LLM out of import graph

    source_dir, target_dir = Path(source_dir), Path(target_dir)
    src = {f: (source_dir / f).read_text(encoding="utf-8")
           for f in ("world.py", "meta.json", "brief.md")}
    src_cert = json.loads((source_dir / "certificates.json").read_text(encoding="utf-8"))

    chat = FoundryChat(system=RESKIN_SYSTEM, model=model, max_completion_tokens=8000)
    reply = chat.ask(f"{RESKIN_RULES}\n\n=== SOURCE world.py ===\n{src['world.py']}\n\n"
                     f"=== SOURCE meta.json ===\n{src['meta.json']}\n\n"
                     f"=== SOURCE brief.md ===\n{src['brief.md']}")
    blocks = _extract_blocks(reply.content)
    if any(v is None for v in blocks.values()):
        return {"passed": False, "reason": "parse_fail",
                "have": {k: v is not None for k, v in blocks.items()}}

    target_dir.mkdir(exist_ok=True)
    (target_dir / "world.py").write_text(blocks["world.py"], encoding="utf-8", newline="\n")
    meta = json.loads(blocks["meta.json"])
    meta["case_id"] = target_dir.name
    (target_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (target_dir / "brief.md").write_text(blocks["brief.md"], encoding="utf-8", newline="\n")
    for f in ("build_and_certify.py", "make_ladder_fixtures.py"):
        if (source_dir / f).exists():
            (target_dir / f).write_text((source_dir / f).read_text(encoding="utf-8"),
                                        encoding="utf-8", newline="\n")

    r = subprocess.run([sys.executable, str(target_dir / "build_and_certify.py")],
                       capture_output=True, text=True, cwd=str(ROOT))
    if r.returncode != 0:
        return {"passed": False, "reason": "certify_crash", "stderr": r.stderr[-800:],
                "domain": [c["name"] for c in meta["columns"]]}
    gen_cert = json.loads((target_dir / "certificates.json").read_text(encoding="utf-8"))
    r_identical = all(abs(src_cert["R"][k] - gen_cert["R"].get(k, 1e9)) < 1e-6
                      for k in src_cert["R"])
    gates_ok = bool(gen_cert["gates"]["all"])
    return {"passed": r_identical and gates_ok, "r_identical": r_identical,
            "gates_ok": gates_ok, "domain": [c["name"] for c in meta["columns"]],
            "reason": "ok" if (r_identical and gates_ok) else "math_not_preserved"}


# ---------------------------------------------------------------------------
# MEDIO rung -- fresh-instantiation PILOT of the typed confounded template
# (ADR 0128; los 8 requisitos de Codex r9). La matemática es NUESTRA
# (template-fill, decisión A-i firmada en ADR 0094): el LLM solo elige dominio,
# nombres, prosa y VALORES de parámetros dentro del estrato CONGELADO. El
# generador es STATELESS: jamás ve confounded_gen_v0, baterías, rivales,
# thresholds ni diagnósticos históricos.
#
# STRATUM_B -- congelado 2026-07-10 ANTES de cualquier llamada al LLM (sellado
# por commit; req iii de ADR 0128): banda paramétrica DISTINTA del fixture --
# el confusor ahora SUPRIME la asignación histórica (confound_coef < 0), así
# que la asociación observacional SUBESTIMA (o invierte vs) el efecto causal,
# en vez de inflarlo como en el fixture. Salida fuera del estrato = FALLO
# (fuera-de-clase), no "interesante".
# ---------------------------------------------------------------------------
STRATUM_B = {
    "u_sd": (1.0, 1.0),               # fijo
    "proxy_coef": (0.9, 1.6),
    "proxy_noise": (0.8, 1.5),
    "base": (8.0, 40.0),
    "driver_coef": (0.9, 1.5),
    "u_coef": (3.5, 5.5),
    "outcome_noise": (1.2, 2.2),
    "shift_coef": (0.8, 1.2),
    "driver_base": (4.0, 6.0),
    "driver_sd": (1.2, 1.8),
    "confound_coef": (-3.2, -1.6),    # banda NEGATIVA (el fixture era +2.24)
}

MEDIO_WORLD_TEMPLATE = '''"""{case_id} -- GENERATED confounded static world (proto-designer MEDIO pilot, ADR 0128).

Domain: {domain}. Confounding trap: a latent {latent_name} drives BOTH the historical
{decision} assignment AND the {outcome}, so the record's {decision}->{outcome} slope is
confounded; experiments (do) de-confound. Server-side only.
"""

import numpy as np
import pandas as pd

COLUMNS = ["{decision}", "{proxy}", "{outcome}"]

PARAMS = {params!r}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    {proxy} = p["proxy_coef"] * u + rng.normal(0.0, p["proxy_noise"], n)
    if "{decision}" in regime.config:
        {decision} = np.full(n, float(regime.config["{decision}"]))
    else:
        {decision} = np.clip(rng.normal(p["driver_base"] + p["confound_coef"] * u, p["driver_sd"], n),
                           DRIVER_MIN, DRIVER_MAX)
    {outcome} = (p["base"] + p["driver_coef"] * {decision} + p["u_coef"] * u
                 + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({{"{decision}": {decision}, "{proxy}": {proxy}, "{outcome}": {outcome}}})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
'''

MEDIO_GEN_SYSTEM = (
    "You are a world-designer on the factory side of an ML research harness. You INSTANTIATE a typed "
    "world template into a NEW concrete industrial/scientific domain. The mathematics is fixed by the "
    "template; you only choose the domain, the variable names, the prose, and parameter VALUES inside "
    "the given bands. A mechanical validator rejects anything outside the bands."
)

MEDIO_GEN_RULES = """Instantiate this world template in a NEW concrete process/industrial domain of your
choice. FORBIDDEN domains: injection molding, syringes, anything medical-device molding. The template
(math, fixed): a latent nuisance variable u drives BOTH the historical setting of a 0-10 decision knob
(negatively: when u is high, operators historically turned the knob DOWN) and the final outcome score
(positively). An inline sensor reading is a noisy proxy of u. Experiments set the knob directly.

Return EXACTLY one fenced json block with these fields:
```json
{
  "case_id": "snake_case_slug_gen_v0",
  "domain": "one-line domain description",
  "latent_name": "snake_case name of the latent nuisance (never a column)",
  "decision": {"name": "snake_case knob column", "unit": "au", "description": "..."},
  "proxy":    {"name": "snake_case inline sensor column", "unit": null, "description": "..."},
  "outcome":  {"name": "snake_case final quality score column", "unit": null, "description": "..."},
  "params": {"u_sd": 1.0, "proxy_coef": 0.0, "proxy_noise": 0.0, "base": 0.0, "driver_coef": 0.0,
             "u_coef": 0.0, "outcome_noise": 0.0, "shift_coef": 0.0, "driver_base": 0.0,
             "driver_sd": 0.0, "confound_coef": 0.0},
  "narrative": "3-4 sentence stakes narrative: the plant believes the knob helps; but records were taken
                while the latent condition ALSO moved the knob's historical setting the OTHER way, so the
                records may UNDERSTATE what the knob really buys."
}
```
Replace every 0.0 above with a value INSIDE these closed bands (validator-enforced):
{bands}
Column names must be three distinct snake_case identifiers. No other prose outside the json block."""

MEDIO_WRITER_SYSTEM = (
    "You write the client-facing brief for an investigation episode. You are BLIND to how the world is "
    "generated, to its battery and to its rivals: you only see what the client would know. Never hint "
    "at hidden mechanisms, traps, or evaluation details beyond what you are given."
)


def _text(reply):
    return getattr(reply, "content", reply)


def _extract_json(text: str):
    m = re.search(r"```json\s*\n(.*?)```", text, re.S) or re.search(r"(\{.*\})", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def _medio_validate_spec(spec) -> list:
    errs = []
    if not isinstance(spec, dict):
        return ["no parseable json"]
    if not re.fullmatch(r"[a-z][a-z0-9_]*_gen_v0", spec.get("case_id", "")):
        errs.append("case_id must be a snake_case slug ending in _gen_v0")
    names = [(spec.get(k) or {}).get("name", "") for k in ("decision", "proxy", "outcome")]
    if len(set(names)) != 3 or not all(re.fullmatch(r"[a-z][a-z0-9_]*", n or "") for n in names):
        errs.append(f"column names invalid or not distinct: {names}")
    blob = json.dumps(spec).lower()
    if any(f in blob for f in ("molding", "syringe", "inyec")):
        errs.append("forbidden fixture domain detected")
    p = spec.get("params") or {}
    for k, (lo, hi) in STRATUM_B.items():
        v = p.get(k)
        if not isinstance(v, (int, float)) or not (lo <= float(v) <= hi):
            errs.append(f"param {k}={v!r} outside frozen stratum [{lo}, {hi}]")
    return errs


def _medio_render_meta(spec: dict, threshold: float) -> dict:
    dec, prox, out = spec["decision"], spec["proxy"], spec["outcome"]
    clause = (f"a scrap -- {out['name']} below the acceptance line of {threshold} -- "
              "is far costlier than a forgone gain")
    return {
        "case_id": spec["case_id"],
        "suite": "causal_with_client",
        "columns": [
            {"name": dec["name"], "dtype": "float", "unit": dec.get("unit") or "au",
             "description": dec["description"]},
            {"name": prox["name"], "dtype": "float", "unit": prox.get("unit"),
             "description": prox["description"]},
            {"name": out["name"], "dtype": "float", "unit": out.get("unit"),
             "description": out["description"]},
        ],
        "operators": [{
            "name": "confounding_por_asignacion", "layer": "mechanism",
            "knobs": {"confound_coef": spec["params"]["confound_coef"]},
            "ablation": {"confound_coef": 0.0},
        }],
        "stakes": {
            "narrative": spec["narrative"],
            "decision_variables": [dec["name"]],
            "context_relevance": {"shift": {"center": 0.0, "sd": 1.0,
                                            "out_of_record_above_abs": 1.5,
                                            "out_of_record_floor": 0.3}},
            "decision_relevance": {},
            "functionals": [{"name": "exceedance", "column": out["name"],
                             "threshold": threshold, "direction": "below",
                             "brief_clause": clause}],
        },
        "scoring": {"lambda_mdl": 0.00010128773858650133, "lambda_provisional": True,
                    "c_f": 0.25, "n_samples": 1000, "m_reps": 2, "model_call_timeout_s": 10.0},
        "episode": {
            "budget": 20000,
            "observe_sources": {"registros_linea": {"cost_per_row": 1.0, "config": {},
                                                    "context": {"shift": 0.0}}},
            "experiment": {"cost_fixed": 100.0, "cost_per_row": 2.0},
            "experiment_meter": None,
            "smoke_regimes": [
                {"config": {dec["name"]: 2.0}, "context": {"shift": 0.0}, "horizon": None},
                {"config": {dec["name"]: 8.0}, "context": {"shift": 0.0}, "horizon": None},
                {"config": {}, "context": {"shift": 0.0}, "horizon": None},
            ],
            "control_surface": {
                "settable": {dec["name"]: {"low": 0.0, "high": 10.0, "unit": dec.get("unit") or "au"}},
                "context": {"shift": {"description": "period baseline (targetable in experiments)",
                                      "experimentable_range": [-1.5, 1.5]}},
                "instruments": {},
                "deliverable_note": (f"model(regime, n, seed) -> table over "
                                     f"[{dec['name']}, {prox['name']}, {out['name']}]."),
            },
        },
        "prior_reliability": None,
    }


def _medio_write_world(case_dir: Path, spec: dict) -> None:
    src = MEDIO_WORLD_TEMPLATE.format(
        case_id=spec["case_id"], domain=spec["domain"], latent_name=spec["latent_name"],
        decision=spec["decision"]["name"], proxy=spec["proxy"]["name"],
        outcome=spec["outcome"]["name"], params=spec["params"])
    (case_dir / "world.py").write_text(src, encoding="utf-8", newline="\n")


def medio(target_root=None, model: str = "gpt-5.4") -> dict:
    """Piloto de instanciación fresca (ADR 0128): genera UN caso nuevo de la
    plantilla confundida tipada dentro de STRATUM_B y lo certifica con el
    verificador CONGELADO. Lectura sellada: 1/1 = 'existe una segunda
    instanciación fresca certificable de esta plantilla'; 0/1 = piloto fallido.
    Ninguno estima yield. Presupuesto: 1 artefacto + <=3 reparametrizaciones
    NUMÉRICAS; el autoajuste ve solo NOMBRES de gates, jamás ítems de batería."""
    from wager.agent.llm_client import FoundryChat  # lazy: keeps LLM out of import graph

    target_root = Path(target_root) if target_root else (ROOT / "cases")
    log = {"pilot": "medio_fresh_ADR0128", "model": model,
           "stratum": {k: list(v) for k, v in STRATUM_B.items()}, "attempts": []}

    bands = "\n".join(f"  {k}: [{lo}, {hi}]" for k, (lo, hi) in STRATUM_B.items())
    gen = FoundryChat(system=MEDIO_GEN_SYSTEM, model=model, max_completion_tokens=4000)
    raw = _text(gen.ask(MEDIO_GEN_RULES.replace("{bands}", bands)))
    log["gen_raw"] = raw
    spec = _extract_json(raw)
    errs = _medio_validate_spec(spec)
    for _ in range(3):
        if not errs:
            break
        raw = _text(gen.ask("Validator rejected your spec:\n- " + "\n- ".join(errs) +
                            "\nReturn the corrected full json block. Same rules."))
        log["attempts"].append({"stage": "spec_retry", "errors": errs, "raw": raw})
        spec = _extract_json(raw)
        errs = _medio_validate_spec(spec)
    if errs:
        log["classification"] = "fuera_de_clase"
        log["errors"] = errs
        return log
    log["spec"] = spec

    case_dir = target_root / spec["case_id"]
    case_dir.mkdir(parents=True, exist_ok=False)
    _medio_write_world(case_dir, spec)

    # threshold computado DEL mecanismo (receta ADR 0094): percentil 25 del
    # outcome bajo do(medio) -- código, no LLM.
    from types import SimpleNamespace
    import numpy as np
    from wager.factory.case_loader import load_world_module
    wmod = load_world_module(case_dir)
    mid = SimpleNamespace(config={spec["decision"]["name"]: 5.0}, context={"shift": 0.0}, horizon=None)
    threshold = round(float(np.percentile(
        wmod.sample(mid, 4000, 777)[spec["outcome"]["name"]], 25)), 1)
    log["threshold"] = threshold

    meta = _medio_render_meta(spec, threshold)
    (case_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    # writer CIEGO del brief: llamada separada y stateless; ve solo lo que el
    # cliente sabría (doctrina anti-leak).
    clause = meta["stakes"]["functionals"][0]["brief_clause"]
    writer = FoundryChat(system=MEDIO_WRITER_SYSTEM, model=model, max_completion_tokens=3000)
    brief = _text(writer.ask(
        "Write brief.md (markdown, ~300-450 words) for an investigation episode. The investigator is "
        "an outside consultant. Include: a title; the client's story (narrative below, expanded "
        "naturally); what they can do -- observe historical records (registros_linea, 1.0 per row, "
        "recorded at baseline conditions) or run experiments (100.0 fixed + 2.0 per row, may set the "
        "decision knob 0-10 and the context 'shift' in [-1.5, 1.5]) with a total budget of 20000; the "
        "deliverable contract line (verbatim below); and this stakes sentence VERBATIM somewhere in "
        "the text: \"" + clause + "\"\n\n"
        "NARRATIVE: " + meta["stakes"]["narrative"] + "\n"
        "COLUMNS: " + json.dumps(meta["columns"]) + "\n"
        "DELIVERABLE: " + meta["episode"]["control_surface"]["deliverable_note"]))
    log["writer_raw"] = brief
    if clause not in brief:
        brief = brief.rstrip() + "\n\nNote: " + clause + ".\n"
        log["attempts"].append({"stage": "clause_appended_mechanically"})
    (case_dir / "brief.md").write_text(brief, encoding="utf-8", newline="\n")

    # certificar con el verificador CONGELADO; <=3 reparametrizaciones numéricas
    # viendo solo nombres de gates.
    from wager.factory.generic_certify import certify
    for attempt in range(4):
        report = certify(case_dir)
        gates = report["gates"]
        log["attempts"].append({"stage": f"certify_{attempt}",
                                "gates": {k: bool(v) for k, v in gates.items()},
                                "R_canonical": report.get("R_canonical")})
        if gates["all"]:
            log["classification"] = "pass"
            break
        if attempt == 3:
            log["classification"] = "fallo_dentro_de_clase"
            break
        failed = [k for k, v in gates.items() if not v and k != "all"]
        raw = _text(gen.ask(
            "The mechanical certification failed these gates (names only): " + ", ".join(failed) +
            ". You may adjust ONLY the numeric values in params, staying inside the original bands. "
            "Return the corrected full json block (same structure, same names, same prose)."))
        log["attempts"].append({"stage": f"reparam_{attempt}", "raw": raw})
        spec2 = _extract_json(raw)
        errs2 = _medio_validate_spec(spec2)
        if errs2 or spec2["case_id"] != spec["case_id"]:
            log["attempts"].append({"stage": f"reparam_{attempt}_rejected", "errors": errs2})
            continue
        spec = spec2
        _medio_write_world(case_dir, spec)
        meta = _medio_render_meta(spec, log["threshold"])
        (case_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    (case_dir / "gen_log.json").write_text(json.dumps(log, indent=2, default=str) + "\n",
                                           encoding="utf-8")
    return log


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "medio":
        out = medio()
        print(json.dumps({k: v for k, v in out.items()
                          if k in ("classification", "threshold", "errors", "spec")},
                         indent=2, default=str))
    else:
        src = ROOT / "cases" / (sys.argv[1] if len(sys.argv) > 1 else "prior_sweetspot_v0")
        tgt = ROOT / "cases" / (sys.argv[2] if len(sys.argv) > 2 else "reskin_pilot_v0")
        print(json.dumps(reskin(src, tgt), indent=2))
