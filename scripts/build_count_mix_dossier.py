"""Dossier HTML de las corridas count_mix: la tarea EXACTA que vio el agente,
cada turno (razonamiento / codigo / salida del kernel / compras / presupuesto),
la entrega, y la evaluacion con histograma verdad-vs-entrega (SVG, sin deps).

Uso:  python scripts/build_count_mix_dossier.py
Sale: scripts/out/count_mix_smoke/dossier/index.html  (abrir en el navegador)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from cases.count_mix_v0_common import (  # noqa: E402
    _DictRegime, _sample_counts, load_instance, program_functionals, s_valley,
    strong_baseline_program,
)
from wager.report.html import code, details, esc, md, page, section, table  # noqa: E402

SMOKE = ROOT / "scripts/out/count_mix_smoke"
OUT = SMOKE / "dossier"

# brief por era: v0 (tecnico/main/pista) desde git, v0.2 (v02_*) el actual
BRIEF_V02 = (ROOT / "cases/count_mix_v0/brief.md").read_text()
try:
    BRIEF_V0 = subprocess.run(
        ["git", "show", "381b64f~1:cases/count_mix_v0/brief.md"],
        capture_output=True, text=True, cwd=ROOT, check=True).stdout
except Exception:
    BRIEF_V0 = BRIEF_V02 + "\n\n*(no se pudo reconstruir el brief v0 desde git)*"

NOTES = {
    "pista": "Nota del encargo: considerá que los datos pueden venir de más de una subpoblación.",
    "v02_nivel3": "Nota del encargo: considerá la posibilidad de que los lotes vengan en unos pocos tipos distintos.",
    "v02_nivel4": "Nota del encargo: considerá probar un modelo de mezcla finita: 2 o 3 grupos de lotes, cada grupo con su propia tasa.",
}


def brief_for(tag: str) -> str:
    return BRIEF_V02 if tag.startswith("v02") else BRIEF_V0


def svg_hist(y_truth: np.ndarray, y_model: np.ndarray | None, title: str) -> str:
    """Histograma comparado como SVG puro (barras lado a lado por valor)."""
    kmax = int(max(y_truth.max(), (y_model.max() if y_model is not None else 0), 14))
    kmax = min(kmax, 22)
    ks = np.arange(kmax + 1)
    ft = np.array([(y_truth == k).mean() for k in ks])
    fm = (np.array([(y_model == k).mean() for k in ks]) if y_model is not None else None)
    W, H, pad = 860, 240, 34
    bw = (W - 2 * pad) / (len(ks) * 2.4)
    ymax = max(ft.max(), (fm.max() if fm is not None else 0), 1e-9) * 1.15
    bars = []
    for i, k in enumerate(ks):
        x0 = pad + i * (W - 2 * pad) / len(ks)
        h1 = ft[i] / ymax * (H - 2 * pad)
        bars.append(f"<rect x='{x0:.1f}' y='{H - pad - h1:.1f}' width='{bw:.1f}' height='{h1:.1f}' fill='#ea580c' opacity='0.85'/>")
        if fm is not None:
            h2 = fm[i] / ymax * (H - 2 * pad)
            bars.append(f"<rect x='{x0 + bw + 1:.1f}' y='{H - pad - h2:.1f}' width='{bw:.1f}' height='{h2:.1f}' fill='#2563eb' opacity='0.85'/>")
        bars.append(f"<text x='{x0 + bw:.1f}' y='{H - pad + 14}' font-size='10' text-anchor='middle' fill='#666'>{k}</text>")
    legend = (f"<rect x='{pad}' y='8' width='12' height='12' fill='#ea580c'/>"
              f"<text x='{pad + 16}' y='18' font-size='12'>proceso real</text>"
              + (f"<rect x='{pad + 120}' y='8' width='12' height='12' fill='#2563eb'/>"
                 f"<text x='{pad + 136}' y='18' font-size='12'>modelo entregado</text>" if fm is not None else ""))
    return (f"<div><b>{esc(title)}</b><br><svg width='{W}' height='{H}' "
            f"style='background:#fff;border:1px solid #e3e3e3;border-radius:8px'>"
            f"{legend}{''.join(bars)}"
            f"<text x='{W/2}' y='{H-4}' font-size='11' text-anchor='middle' fill='#666'>defectos por medición (frecuencia)</text>"
            f"</svg></div>")


def episode_html(p: dict, inst: dict) -> str:
    tag, model, pole, seed = p["tag"], p["model"], p["pole"], p["seed"]
    ins = p.get("instruments", {})
    hdr_rows = [
        ["mundo", "MEZCLA oculta (dos tipos de lote)" if pole == "mix" else "GEMELO (un solo proceso)"],
        ["modelo agente", model], ["seed", seed], ["brazo", tag],
        ["terminó por", p.get("abort_reason")], ["turnos", p.get("turns")],
        ["presupuesto gastado", f"{p.get('budget_spent', 0):.0f} / 1000"],
        ["tokens", (p.get("tokens") or {}).get("total")],
        ["R (nota estándar del examen)", p.get("R")],
    ]
    for k in ("S_valley_fuerte", "S_struct", "S_clean", "F_mean"):
        if ins.get(k) is not None:
            hdr_rows.append([k, f"{ins[k]:.3f}"])
    if ins.get("espurio") is not None:
        hdr_rows.append(["inventó grupos falsos (espurio)", "SÍ" if ins["espurio"]["spurious"] else "no"])
    body = [f"<h1>{esc(tag)} — {esc(model)} — {esc('mezcla' if pole == 'mix' else 'gemelo')} — seed {seed}</h1>",
            table(["", ""], hdr_rows)]

    task = md(brief_for(tag))
    note = NOTES.get(tag)
    if note:
        task += f"<div class='warn'><b>Ayuda agregada en el primer mensaje:</b> {esc(note)}</div>"
    body.append(section("La tarea exacta que vio el agente", details("ver el encargo completo", task), "student"))

    turns = []
    for rec in p["episode"]["trace"]:
        inner = ["<h4>Razonamiento</h4>", md(rec.get("reply_text", "")),]
        if rec.get("cell"):
            inner += ["<h4>Código</h4>", code(rec["cell"])]
        cr = rec.get("cell_result") or {}
        outtxt = (cr.get("stdout") or "").strip()
        if outtxt:
            inner += ["<h4>Salida del kernel</h4>", code(outtxt[:4000], out=True)]
        if cr.get("error"):
            inner += [f"<div class='warn'><b>Error:</b><pre class='out'>{esc(cr['error'][-600:])}</pre></div>"]
        verbs = rec.get("verbs") or []
        if verbs:
            inner.append(table(["acción", "detalle", "costo", "presupuesto restante"],
                               [[v["verb"], esc(json.dumps(v.get("args", {}), ensure_ascii=False))[:90],
                                 f"{v.get('cost', 0):.0f}", f"{v.get('budget_remaining', 0):.0f}"] for v in verbs]))
        turns.append(f"<div class='turn'><h3>Turno {rec['turn']}</h3>{''.join(inner)}</div>")
    body.append(section(f"La partida, turno a turno ({len(turns)} turnos)", "".join(turns), "student"))

    if p.get("delivered_code"):
        body.append(section("La entrega (el modelo que presentó)", code(p["delivered_code"]), "student"))
        # histograma comparado
        try:
            ns: dict = {}
            exec(p["delivered_code"], ns)
            ym = ns["model"](_DictRegime({"speed": 1.0}), 4000, 424242)["y"].to_numpy(float)
        except Exception:
            ym = None
        yt = _sample_counts(pole, inst["params"], _DictRegime({"speed": 1.0}), 4000, 424242)["y"].to_numpy(float)
        eval_body = svg_hist(yt, ym, "¿Los datos del modelo se distinguen de los del proceso? (speed=1)")
        eval_body += ("<p class='note'>La vara del salto (S_valley_fuerte) mide lo único que un modelo sin "
                      "grupos no puede imitar: el valle entre las dos jorobas. 0 = igual al mejor modelo "
                      "continuo; 1 = igual a la verdad. R es la nota estándar (comparación gruesa de datos); "
                      "es poco sensible a la forma — por eso convive con la vara.</p>")
        fn = ins.get("functionals")
        if fn:
            eval_body += table(["funcional", "entrega"], [[k, f"{v:.3f}"] for k, v in fn.items()])
        body.append(section("Evaluación", eval_body, "eval"))
    else:
        body.append(section("Evaluación", "<div class='warn'>Episodio censurado: no hubo entrega.</div>", "eval"))
    return page(f"{tag} {model} {pole} {seed}", "".join(body))


def main() -> None:
    inst = load_instance()
    OUT.mkdir(parents=True, exist_ok=True)
    geo, tail_at = inst["geometry"], inst["tail_at"]
    y_train = _sample_counts("mix", inst["params"], _DictRegime({"speed": 1.0}),
                             inst["witness_n"], inst["witness_sample_seed"])["y"].to_numpy(float)
    truth_f = program_functionals(
        lambda r, n, s: _sample_counts("mix", inst["params"], r, n, s), geo, tail_at)
    strong_f = program_functionals(strong_baseline_program(y_train), geo, tail_at)
    rows = []
    for f in sorted(SMOKE.glob("*.json")):
        p = json.loads(f.read_text())
        ins = p.get("instruments", {})
        if (p["pole"] == "mix" and ins.get("S_valley_fuerte") is None
                and ins.get("functionals")):
            ins["S_valley_fuerte"] = s_valley(ins["functionals"], truth_f, strong_f)
            p["instruments"] = ins
        name = f"dossier_{f.stem}.html"
        (OUT / name).write_text(episode_html(p, inst))
        key = next((k for k in ("S_valley_fuerte", "S_clean") if ins.get(k) is not None), None)
        metric = f"{ins[key]:.3f}" if key else ("censurado" if not ins.get("functionals") else "—")
        rows.append([name, f.stem, p["tag"], p["model"],
                     "mezcla" if p["pole"] == "mix" else "gemelo", p["seed"], metric,
                     f"{p.get('R'):.3f}" if p.get("R") is not None else "—",
                     p.get("abort_reason")])
    trs = "".join(
        f"<tr><td><a href='{name}'>{esc(stem)}</a></td><td>{esc(tag)}</td><td>{esc(model)}</td>"
        f"<td>{esc(mundo)}</td><td class='num'>{seed}</td><td class='num'>{esc(metric)}</td>"
        f"<td class='num'>{esc(r)}</td><td>{esc(fin)}</td></tr>"
        for name, stem, tag, model, mundo, seed, metric, r, fin in rows)
    idx = [f"<h1>Dossier count_mix — {len(rows)} episodios</h1>",
           "<p class='sub'>Cada fila abre la partida completa: tarea exacta, razonamiento, código, "
           "salidas, compras, entrega y evaluación con histograma. La vara del salto (mundos mezcla): "
           "0 = modelo continuo, 1 = capturó los dos grupos. Limpieza (gemelo): 1 = no inventó nada.</p>",
           "<table><tr><th>episodio</th><th>brazo</th><th>modelo</th><th>mundo</th><th>seed</th>"
           "<th>vara del salto / limpieza</th><th>R</th><th>fin</th></tr>" + trs + "</table>"]
    (OUT / "index.html").write_text(page("Dossier count_mix", "".join(idx)))
    print(f"OK: {len(rows)} dossiers -> {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
