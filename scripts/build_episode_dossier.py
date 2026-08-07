"""Dossier de episodios — TEMPLATE GENERAL para cualquier caso WAGER.

Todo lo que muestra sale de los artefactos del caso (brief/meta/columnas) y de
los JSONs de episodios (formato estándar del runner: case_id, run_at,
initial_note, brief, trace, delivered_code, instruments…). Cero texto
hardcodeado por caso.

Uso:
  python scripts/build_episode_dossier.py [dir_de_episodios]
  (default: scripts/out/count_mix_smoke)
Sale: <dir>/dossier/index.html
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from wager.factory.case_loader import load_meta, load_world_sample  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import SYSTEM  # noqa: E402
from wager.report.html import code, details, esc, md, page, section, table  # noqa: E402


# --- helpers genericos -------------------------------------------------------

def metric_chips(ins: dict) -> str:
    chips = []
    for k, v in ins.items():
        if isinstance(v, (int, float)):
            chips.append(f"<code title='{esc(k)}'>{esc(k)}={v:.3f}</code>")
    esp = (ins.get("espurio") or {})
    if isinstance(esp, dict) and "spurious" in esp:
        chips.append(f"<code>espurio={'SÍ' if esp['spurious'] else 'no'}</code>")
    return " ".join(chips) or "—"


def ayuda_of(p: dict) -> str:
    note = (p.get("initial_note") or "").strip()
    return note


def svg_hist(y_truth: np.ndarray, y_model: np.ndarray | None, title: str,
             integer: bool) -> str:
    if integer:
        kmax = int(min(max(y_truth.max(), (y_model.max() if y_model is not None else 0), 10), 24))
        edges = np.arange(-0.5, kmax + 1.5)
    else:
        lo = float(min(y_truth.min(), (y_model.min() if y_model is not None else np.inf)))
        hi = float(max(y_truth.max(), (y_model.max() if y_model is not None else -np.inf)))
        edges = np.linspace(lo, hi, 21)
    ft, _ = np.histogram(y_truth, bins=edges, density=True)
    fm = (np.histogram(y_model, bins=edges, density=True)[0] if y_model is not None else None)
    ft = ft / max(ft.sum(), 1e-12)
    fm = fm / max(fm.sum(), 1e-12) if fm is not None else None
    W, H, pad = 860, 240, 34
    nb = len(ft)
    bw = (W - 2 * pad) / (nb * 2.4)
    ymax = max(ft.max(), (fm.max() if fm is not None else 0), 1e-9) * 1.15
    parts = []
    for i in range(nb):
        x0 = pad + i * (W - 2 * pad) / nb
        h1 = ft[i] / ymax * (H - 2 * pad)
        parts.append(f"<rect x='{x0:.1f}' y='{H-pad-h1:.1f}' width='{bw:.1f}' height='{h1:.1f}' fill='#ea580c' opacity='.85'/>")
        if fm is not None:
            h2 = fm[i] / ymax * (H - 2 * pad)
            parts.append(f"<rect x='{x0+bw+1:.1f}' y='{H-pad-h2:.1f}' width='{bw:.1f}' height='{h2:.1f}' fill='#2563eb' opacity='.85'/>")
        label = f"{(edges[i]+edges[i+1])/2:.0f}" if integer else f"{edges[i]:.1f}"
        if i % max(1, nb // 12) == 0:
            parts.append(f"<text x='{x0+bw:.1f}' y='{H-pad+14}' font-size='10' text-anchor='middle' fill='#666'>{label}</text>")
    legend = (f"<rect x='{pad}' y='8' width='12' height='12' fill='#ea580c'/>"
              f"<text x='{pad+16}' y='18' font-size='12'>proceso real</text>"
              + (f"<rect x='{pad+120}' y='8' width='12' height='12' fill='#2563eb'/>"
                 f"<text x='{pad+136}' y='18' font-size='12'>modelo entregado</text>" if fm is not None else ""))
    return (f"<div><b>{esc(title)}</b><br><svg width='{W}' height='{H}' "
            f"style='background:#fff;border:1px solid #e3e3e3;border-radius:8px'>{legend}{''.join(parts)}</svg></div>")


class _CaseCtx:
    """Artefactos de UN caso, cargados una vez (todo generico)."""

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.dir = ROOT / "cases" / case_id
        self.meta = load_meta(self.dir)
        self.sample = load_world_sample(self.dir)
        self.outcome = self.meta.columns[-1]
        smoke = self.meta.episode.smoke_regimes[0] if self.meta.episode else None
        self.regime = smoke
        try:
            srv = build_world_server(self.dir, seed_offset=0)
            src = next(iter(self.meta.episode.observe_sources))
            self.preview = srv.observe(src, 10)
            self.source_name = src
        except Exception:
            self.preview, self.source_name = None, None

    def explainer(self) -> str:
        m = self.meta
        body = [f"<p><b>Narrativa (stakes del caso):</b> {esc(m.stakes.narrative)}</p>",
                "<p><b>Esquema del dataset (lo que devuelven las compras):</b></p>",
                table(["columna", "tipo", "unidad", "qué es"],
                      [[c.name, c.dtype, c.unit or "—", c.description or "—"] for c in m.columns])]
        if self.preview is not None:
            body.append(f"<p><b>Primeras filas de la fuente «{esc(self.source_name)}»</b> "
                        "(cada partida ve su propia tirada):</p>")
            body.append(table(list(self.preview.columns),
                              [[f"{v:g}" for v in row] for row in self.preview.itertuples(index=False)]))
        ops = [[o.name, o.layer, esc(json.dumps(o.knobs, ensure_ascii=False))] for o in m.operators]
        body.append(details("la verdad oculta del mundo (lado servidor — el agente JAMÁS la ve)",
                            table(["operador", "capa", "parámetros"], ops)))
        return section(f"Caso {esc(self.case_id)}", "".join(body), "truth")

    def truth_samples(self, n: int, seed: int) -> np.ndarray:
        df = self.sample(self.regime, n, seed)
        return df[self.outcome.name].to_numpy(float)


def episode_html(p: dict, ctx: _CaseCtx) -> str:
    ins = p.get("instruments", {})
    ayuda = ayuda_of(p)
    hdr = [["caso", p.get("case_id", "?")], ["modelo agente", p["model"]],
           ["fecha", p.get("run_at", "—")], ["seed", p["seed"]],
           ["ayuda", ayuda or "no"], ["terminó por", p.get("abort_reason")],
           ["turnos", p.get("turns")],
           ["presupuesto gastado", f"{p.get('budget_spent', 0):.0f}"],
           ["tokens", (p.get("tokens") or {}).get("total")],
           ["R (nota estándar)", p.get("R")]]
    body = [f"<h1>{esc(p.get('case_id', '?'))} — {esc(p['model'])} — seed {p['seed']}</h1>",
            table(["", ""], hdr),
            f"<p><b>Métricas del caso:</b> {metric_chips(ins)}</p>"]

    task = md(p.get("brief") or "(brief no registrado en este episodio)")
    if ayuda:
        task += f"<div class='warn'><b>Ayuda agregada al primer mensaje:</b> {esc(ayuda)}</div>"
    prompt = details("ver el PROMPT EXACTO (rol + composición del primer mensaje)",
                     "<p><b>Rol (system prompt):</b></p>" + code(SYSTEM)
                     + "<p><b>Primer mensaje = brief (arriba) + ayuda (si hay) + hoja técnica "
                       "(perillas/fuentes/precios del caso) + instrucción de arranque. Después, "
                       "cada turno recibe solo la salida de su propia celda.</b></p>")
    body.append(section("La tarea que vio el agente", details("ver el encargo completo", task) + prompt, "student"))

    turns = []
    for rec in p["episode"]["trace"]:
        prosa = re.sub(r"```(?:python)?.*?```", "", rec.get("reply_text", ""), flags=re.S).strip()
        inner = ["<h4>Razonamiento</h4>", md(prosa)]
        if rec.get("cell"):
            inner += ["<h4>Código</h4>", code(rec["cell"])]
        cr = rec.get("cell_result") or {}
        if (cr.get("stdout") or "").strip():
            inner += ["<h4>Salida del kernel</h4>", code(cr["stdout"].strip()[:4000], out=True)]
        if cr.get("error"):
            inner.append(f"<div class='warn'><b>Error:</b><pre class='out'>{esc(cr['error'][-600:])}</pre></div>")
        verbs = rec.get("verbs") or []
        if verbs:
            inner.append(table(["acción", "detalle", "costo", "presupuesto restante"],
                               [[v["verb"], json.dumps(v.get("args", {}), ensure_ascii=False)[:90],
                                 f"{v.get('cost', 0):.0f}", f"{v.get('budget_remaining', 0):.0f}"] for v in verbs]))
        turns.append(f"<div class='turn'><h3>Turno {rec['turn']}</h3>{''.join(inner)}</div>")
    body.append(section(f"La partida, turno a turno ({len(turns)} turnos)", "".join(turns), "student"))

    if p.get("delivered_code"):
        body.append(section("La entrega", code(p["delivered_code"]), "student"))
        ym = None
        try:
            ns: dict = {}
            exec(p["delivered_code"], ns)
            df = ns["model"](ctx.regime, 3000, 424242)
            ym = df[ctx.outcome.name].to_numpy(float)
        except Exception:
            pass
        yt = ctx.truth_samples(3000, 424242)
        ev = svg_hist(yt, ym, f"{ctx.outcome.name}: datos del proceso vs datos del modelo entregado",
                      integer=(ctx.outcome.dtype == "int"))
        ev += f"<p><b>Métricas:</b> {metric_chips(ins)} <span class='note'>(definidas en la ficha del caso)</span></p>"
        body.append(section("Evaluación", ev, "eval"))
    else:
        body.append(section("Evaluación", "<div class='warn'>Episodio censurado: no hubo entrega.</div>", "eval"))
    return page(f"{p.get('case_id')} {p['model']} {p['seed']}", "".join(body))


def main() -> None:
    src_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scripts/out/count_mix_smoke"
    out = src_dir / "dossier"
    out.mkdir(parents=True, exist_ok=True)
    episodes = [json.loads(f.read_text()) | {"_file": f} for f in sorted(src_dir.glob("*.json"))]
    episodes.sort(key=lambda p: p.get("run_at", ""), reverse=True)

    ctxs: dict[str, _CaseCtx] = {}
    rows = []
    for p in episodes:
        cid = p.get("case_id", "?")
        if cid not in ctxs:
            ctxs[cid] = _CaseCtx(cid)
        name = f"dossier_{p['_file'].stem}.html"
        (out / name).write_text(episode_html(p, ctxs[cid]))
        ayuda = ayuda_of(p)
        rows.append((p.get("run_at", "—"), cid, p["model"], ayuda, p["seed"],
                     metric_chips(p.get("instruments", {})),
                     f"{p.get('R'):.3f}" if p.get("R") is not None else "—",
                     p.get("abort_reason"), name))

    trs = "".join(
        f"<tr data-caso='{esc(cid)}' data-modelo='{esc(model)}' data-ayuda='{'si' if ayuda else 'no'}'>"
        f"<td class='num'>{esc(fecha)}</td><td>{esc(cid)}</td><td>{esc(model)}</td>"
        f"<td title='{esc(ayuda)}'>{esc((ayuda[:60] + '…') if len(ayuda) > 60 else (ayuda or 'no'))}</td>"
        f"<td class='num'>{seed}</td><td>{chips}</td><td class='num'>{esc(r)}</td>"
        f"<td>{esc(fin)}</td><td><a href='{name}'>abrir</a></td></tr>"
        for fecha, cid, model, ayuda, seed, chips, r, fin, name in rows)

    casos = sorted(ctxs)
    modelos = sorted({p["model"] for p in episodes})
    botones_caso = "".join(f"<button onclick=\"setF('caso','{esc(c)}')\">{esc(c)}</button>" for c in casos)
    botones_modelo = "".join(f"<button onclick=\"setF('modelo','{esc(m)}')\">{esc(m)}</button>" for m in modelos)
    filtros = ("<div style='margin:14px 0;padding:12px;border:1px solid #e3e3e3;border-radius:8px;background:#fafafa'>"
               "<b>Caso:</b> <button onclick=\"setF('caso','todos')\">Todos</button>" + botones_caso
               + " &nbsp;<b>Modelo:</b> <button onclick=\"setF('modelo','todos')\">Todos</button>" + botones_modelo
               + " &nbsp;<b>Ayuda:</b> <button onclick=\"setF('ayuda','todos')\">Todas</button>"
                 "<button onclick=\"setF('ayuda','no')\">Sin ayuda</button>"
                 "<button onclick=\"setF('ayuda','si')\">Con ayuda</button>"
                 "<span id='count' style='margin-left:12px;color:#666'></span></div>"
               "<script>var F={caso:'todos',modelo:'todos',ayuda:'todos'};"
               "function setF(k,v){F[k]=v;aplicar();}"
               "function aplicar(){var n=0;document.querySelectorAll('tr[data-caso]').forEach(function(tr){"
               "var ok=true;"
               "if(F.caso!=='todos')ok=(tr.dataset.caso===F.caso);"
               "if(ok&&F.modelo!=='todos')ok=(tr.dataset.modelo===F.modelo);"
               "if(ok&&F.ayuda!=='todos')ok=(tr.dataset.ayuda===F.ayuda);"
               "tr.style.display=ok?'':'none';if(ok)n++;});"
               "document.getElementById('count').textContent=n+' partidas';}"
               "window.addEventListener('load',aplicar);</script>")

    idx = [f"<h1>Dossier de episodios — {esc(src_dir.name)}</h1>",
           f"<p class='sub'>{len(rows)} partidas, ordenadas por fecha (la más nueva arriba). "
           "Cada fila abre la partida completa: tarea, razonamiento, código, salidas, compras, "
           "entrega y evaluación.</p>"]
    idx += [ctxs[c].explainer() for c in casos]
    idx += [filtros,
            "<table><tr><th>fecha</th><th>caso</th><th>modelo</th><th>ayuda</th><th>seed</th>"
            "<th>métricas</th><th>R</th><th>fin</th><th></th></tr>" + trs + "</table>"]
    (out / "index.html").write_text(page(f"Dossier — {src_dir.name}", "".join(idx)))
    print(f"OK: {len(rows)} dossiers -> {out / 'index.html'}")


if __name__ == "__main__":
    main()
