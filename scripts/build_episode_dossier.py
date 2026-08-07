"""Dossier post-mortem — TEMPLATE GENERAL, tres niveles:

  index.html            las TAREAS (suites): descripción simple + nº de corridas
  task_<suite>.html     la tarea en detalle (qué ve el agente, dataset, verdad
                        oculta por variante) + tabla de corridas por fecha
  run_<...>.html        una corrida: qué se le dio (ayudas), trayectoria
                        completa y evaluación detallada — sin repetir la tarea

Todo sale de artefactos del caso (meta/brief) y de los JSONs estándar del
runner (case_id, run_at, initial_note, brief, trace, delivered_code,
instruments). Nada hardcodeado por caso. Una tarea = una suite; las variantes
(p. ej. el gemelo) son condición SECRETA del servidor y se muestran como
columna, explicadas en la sección de verdad oculta.

Uso: python scripts/build_episode_dossier.py [dir]   (default: scripts/out/count_mix_smoke)
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


def metric_chips(ins: dict) -> str:
    chips = [f"<code title='{esc(k)}'>{esc(k)}={v:.3f}</code>"
             for k, v in ins.items() if isinstance(v, (int, float))]
    esp = ins.get("espurio") or {}
    if isinstance(esp, dict) and "spurious" in esp:
        chips.append(f"<code>espurio={'SÍ' if esp['spurious'] else 'no'}</code>")
    return " ".join(chips) or "—"


def svg_hist(y_truth, y_model, title: str, integer: bool) -> str:
    if integer:
        kmax = int(min(max(y_truth.max(), (y_model.max() if y_model is not None else 0), 10), 24))
        edges = np.arange(-0.5, kmax + 1.5)
    else:
        lo = float(min(y_truth.min(), (y_model.min() if y_model is not None else np.inf)))
        hi = float(max(y_truth.max(), (y_model.max() if y_model is not None else -np.inf)))
        edges = np.linspace(lo, hi, 21)
    ft, _ = np.histogram(y_truth, bins=edges, density=True)
    fm = np.histogram(y_model, bins=edges, density=True)[0] if y_model is not None else None
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
        if i % max(1, nb // 12) == 0:
            label = f"{(edges[i]+edges[i+1])/2:.0f}" if integer else f"{edges[i]:.1f}"
            parts.append(f"<text x='{x0+bw:.1f}' y='{H-pad+14}' font-size='10' text-anchor='middle' fill='#666'>{label}</text>")
    legend = (f"<rect x='{pad}' y='8' width='12' height='12' fill='#ea580c'/><text x='{pad+16}' y='18' font-size='12'>proceso real</text>"
              + (f"<rect x='{pad+120}' y='8' width='12' height='12' fill='#2563eb'/><text x='{pad+136}' y='18' font-size='12'>modelo entregado</text>" if fm is not None else ""))
    return (f"<div><b>{esc(title)}</b><br><svg width='{W}' height='{H}' "
            f"style='background:#fff;border:1px solid #e3e3e3;border-radius:8px'>{legend}{''.join(parts)}</svg></div>")


def sample_stats(y: np.ndarray, integer: bool) -> dict:
    d = {"media": float(y.mean()), "desvío": float(y.std()),
         "p10": float(np.percentile(y, 10)), "mediana": float(np.percentile(y, 50)),
         "p90": float(np.percentile(y, 90)), "máx": float(y.max())}
    if integer:
        d["% ceros"] = float((y == 0).mean() * 100)
    return d


class CaseCtx:
    def __init__(self, case_id: str):
        self.case_id = case_id
        self.dir = ROOT / "cases" / case_id
        self.meta = load_meta(self.dir)
        self.sample = load_world_sample(self.dir)
        self.outcome = self.meta.columns[-1]
        self.regime = (self.meta.episode.smoke_regimes[0] if self.meta.episode else None)
        try:
            srv = build_world_server(self.dir, seed_offset=0)
            self.source_name = next(iter(self.meta.episode.observe_sources))
            self.preview = srv.observe(self.source_name, 10)
        except Exception:
            self.preview, self.source_name = None, None
        mpath = self.dir / "metrics.json"
        self.metrics_doc = json.loads(mpath.read_text()) if mpath.exists() else None
        v = (self.metrics_doc or {}).get("variante", {})
        self.titulo = v.get("titulo", case_id)
        self.rol = v.get("rol", "principal")
        self.descripcion = v.get("descripcion", "")

    def truth_samples(self, n=3000, seed=424242):
        return self.sample(self.regime, n, seed)[self.outcome.name].to_numpy(float)


def run_html(p: dict, ctx: CaseCtx, task_page: str) -> str:
    ins = p.get("instruments", {})
    ayuda = (p.get("initial_note") or "").strip()
    hdr = [["tarea", f"<a href='{task_page}'>{esc(p.get('suite', '?'))}</a> (ver ahí la explicación completa)"],
           ["mundo (secreto para el agente)", ctx.titulo],
           ["modelo agente", p["model"]], ["fecha", p.get("run_at", "—")], ["seed", p["seed"]],
           ["terminó por", p.get("abort_reason")], ["turnos", p.get("turns")],
           ["presupuesto gastado", f"{p.get('budget_spent', 0):.0f}"],
           ["tokens", (p.get("tokens") or {}).get("total")]]
    body = [f"<h1>Corrida — {esc(p['model'])} — {esc(p.get('run_at', ''))}</h1>",
            "<table>" + "".join(f"<tr><td>{k}</td><td>{v if k == 'tarea' else esc(str(v))}</td></tr>" for k, v in hdr) + "</table>"]

    dado = ""
    if ayuda:
        dado += f"<div class='warn'><b>AYUDA agregada al primer mensaje de esta corrida:</b> {esc(ayuda)}</div>"
    else:
        dado += "<p>Sin ayudas: solo el encargo estándar de la tarea.</p>"
    dado += details("brief exacto que vio ESTA corrida (por si cambió entre fechas)",
                    md(p.get("brief") or "(no registrado)"))
    dado += details("rol (system prompt, idéntico en todas las corridas)", code(SYSTEM))
    body.append(section("Qué se le dio al agente", dado, "student"))

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
        if rec.get("verbs"):
            inner.append(table(["acción", "detalle", "costo", "presupuesto restante"],
                               [[v["verb"], json.dumps(v.get("args", {}), ensure_ascii=False)[:90],
                                 f"{v.get('cost', 0):.0f}", f"{v.get('budget_remaining', 0):.0f}"] for v in rec["verbs"]]))
        turns.append(f"<div class='turn'><h3>Turno {rec['turn']}</h3>{''.join(inner)}</div>")
    body.append(section(f"Trayectoria completa ({len(turns)} turnos)", "".join(turns), "student"))

    if p.get("delivered_code"):
        body.append(section("La entrega", code(p["delivered_code"]), "student"))
        integer = ctx.outcome.dtype == "int"
        ym = None
        try:
            ns: dict = {}
            exec(p["delivered_code"], ns)
            ym = ns["model"](ctx.regime, 3000, 424242)[ctx.outcome.name].to_numpy(float)
        except Exception:
            pass
        yt = ctx.truth_samples()
        ev = [svg_hist(yt, ym, f"{ctx.outcome.name}: proceso real vs modelo entregado", integer)]
        if ym is not None:
            st, sm = sample_stats(yt, integer), sample_stats(ym, integer)
            ev.append("<p><b>¿En qué se parecen y en qué difieren los datos?</b></p>")
            ev.append(table(["estadístico", "proceso real", "modelo entregado", "diferencia"],
                            [[k, f"{st[k]:.2f}", f"{sm[k]:.2f}", f"{sm[k]-st[k]:+.2f}"] for k in st]))
        mdoc = ctx.metrics_doc or {}
        defs = {m["key"]: m for m in mdoc.get("metricas", [])}
        filas = []
        for k, v in ins.items():
            if isinstance(v, (int, float)):
                d = defs.get(k, {})
                filas.append([d.get("nombre", k), f"{v:.3f}",
                              d.get("que_mide", "—"), d.get("anclas", "—")])
        esp = ins.get("espurio") or {}
        if isinstance(esp, dict) and "spurious" in esp:
            d = defs.get("espurio", {})
            filas.append([d.get("nombre", "espurio"), "SÍ" if esp["spurious"] else "no",
                          d.get("que_mide", "—"), d.get("anclas", "—")])
        if p.get("R") is not None:
            filas.append(["R (nota estándar)", f"{p.get('R'):.3f}",
                          mdoc.get("R", "comparación gruesa de datos generados"), "0 a 1"])
        if filas:
            ev.append("<p><b>Las métricas, explicadas:</b></p>")
            ev.append(table(["métrica", "valor", "qué mide", "cómo leerla"], filas))
        fn = ins.get("functionals")
        if fn:
            fdefs = mdoc.get("funcionales", {})
            ev.append(details("funcionales de forma de la entrega",
                              table(["funcional", "valor", "qué es"],
                                    [[k, f"{v:.3f}", fdefs.get(k, "—")] for k, v in fn.items()])))
        body.append(section("Evaluación", "".join(ev), "eval"))
    else:
        body.append(section("Evaluación", "<div class='warn'>Censurada: no hubo entrega.</div>", "eval"))
    body.append(f"<p><a href='{task_page}'>← volver a la tarea</a></p>")
    return page(f"corrida {p['model']} {p['seed']}", "".join(body))


def task_html(suite: str, cases: dict[str, CaseCtx], runs: list[dict], out: Path) -> str:
    any_ctx = next(iter(cases.values()))
    m = any_ctx.meta
    body = [f"<h1>Tarea: {esc(suite)}</h1>",
            f"<p class='sub'>{len(runs)} corridas · {len(cases)} variantes del mundo</p>",
            section("Qué es esta tarea",
                    f"<p>{esc(m.stakes.narrative)}</p>"
                    "<p><b>Qué ve el agente:</b> el encargo de abajo, la hoja técnica (perillas, "
                    "fuentes y precios) y NADA más — el dataset solo aparece cuando lo compra, y "
                    "jamás ve su nota.</p>"
                    + details("el encargo actual (cada corrida guarda además el suyo exacto)",
                              md((any_ctx.dir / "brief.md").read_text()))
                    + details("rol (system prompt)", code(SYSTEM)), "student"),
            section("El dataset",
                    table(["columna", "tipo", "unidad", "qué es"],
                          [[c.name, c.dtype, c.unit or "—", c.description or "—"] for c in m.columns])
                    + (("<p><b>Primeras filas de la fuente «" + esc(any_ctx.source_name) + "»</b> "
                        "(cada corrida ve su propia tirada):</p>"
                        + table(list(any_ctx.preview.columns),
                                [[f"{v:g}" for v in row] for row in any_ctx.preview.itertuples(index=False)]))
                       if any_ctx.preview is not None else ""), "student")]

    mdoc = any_ctx.metrics_doc or {}
    if mdoc.get("metricas"):
        body.append(section("Cómo se mide (las métricas de esta tarea)",
                            table(["métrica", "qué mide", "cómo leerla", "aplica a"],
                                  [[m.get("nombre", m["key"]), m.get("que_mide", "—"),
                                    m.get("anclas", "—"), m.get("aplica", "ambas")]
                                   for m in mdoc["metricas"]])
                            + f"<p class='note'><b>R:</b> {esc(mdoc.get('R', ''))}</p>", "eval"))

    truth_rows = []
    for cid, ctx in sorted(cases.items(), key=lambda kv: (kv[1].rol != "principal", kv[0])):
        for o in ctx.meta.operators:
            truth_rows.append([ctx.titulo, o.name, json.dumps(o.knobs, ensure_ascii=False)])
    body.append(section("La verdad oculta (lado servidor — el agente NUNCA sabe en qué mundo está)",
                        table(["mundo", "mecanismo", "parámetros"], truth_rows), "truth"))

    # una tabla POR MUNDO (principal primero), con filtros propios
    tablas = ""
    ordered = sorted(cases.items(), key=lambda kv: (kv[1].rol != "principal", kv[0]))
    for ti, (cid, ctx) in enumerate(ordered):
        rs = [r for r in runs if r.get("case_id") == cid]
        if not rs:
            continue
        modelos = sorted({r["model"] for r in rs})
        trs = ""
        for r in rs:
            ayuda = (r.get("initial_note") or "").strip()
            lab = r.get("ayuda_label") or ("sí" if ayuda else "no")
            r_txt = f"{r.get('R'):.3f}" if r.get("R") is not None else "—"
            toks = (r.get("tokens") or {}).get("total") or "—"
            trs += (f"<tr data-t='t{ti}' data-modelo='{esc(r['model'])}' data-ayuda='{esc(lab)}'>"
                    f"<td class='num'>{esc(r.get('run_at', '—'))}</td><td>{esc(r['model'])}</td>"
                    f"<td title='{esc(ayuda) if ayuda else 'sin ayuda'}'><b>{esc(lab)}</b></td>"
                    f"<td class='num'>{r['seed']}</td><td class='num'>{r.get('turns', '—')}</td>"
                    f"<td class='num'>{r.get('budget_spent', 0):.0f}</td><td class='num'>{toks}</td>"
                    f"<td>{metric_chips(r.get('instruments', {}))}</td><td class='num'>{r_txt}</td>"
                    f"<td>{esc(r.get('abort_reason'))}</td><td><a href='{r['_page']}'>abrir</a></td></tr>")
        bts_m = "".join(f"<button onclick=\"setF('t{ti}','modelo','{esc(m)}')\">{esc(m)}</button>" for m in modelos)
        labs = sorted({(r.get("ayuda_label") or ("sí" if (r.get("initial_note") or "").strip() else "no")) for r in rs},
                      key=lambda x: ["no", "poca", "media", "mucha", "sí"].index(x) if x in ["no", "poca", "media", "mucha", "sí"] else 9)
        bts_a = "".join(f"<button onclick=\"setF('t{ti}','ayuda','{esc(l)}')\">{esc(l)}</button>" for l in labs)
        filtros = (f"<div style='margin:8px 0;padding:8px;border:1px solid #e3e3e3;border-radius:8px;background:#fafafa'>"
                   f"<b>Modelo:</b> <button onclick=\"setF('t{ti}','modelo','todos')\">Todos</button>{bts_m}"
                   f" &nbsp;<b>Ayuda:</b> <button onclick=\"setF('t{ti}','ayuda','todos')\">Todas</button>{bts_a}"
                   f"<span id='count-t{ti}' style='margin-left:10px;color:#666'></span></div>")
        tablas += (f"<h3>{esc(ctx.titulo)}</h3><p class='note'>{esc(ctx.descripcion)}</p>" + filtros
                   + "<table><tr><th>fecha</th><th>modelo</th><th>ayuda</th><th>seed</th><th>turnos</th>"
                     "<th>gastado</th><th>tokens</th><th>métricas</th><th>R</th><th>fin</th><th></th></tr>"
                   + trs + "</table>")
    tablas += ("<script>var FS={};"
               "function setF(t,k,v){(FS[t]=FS[t]||{modelo:'todos',ayuda:'todos'})[k]=v;aplicar(t);}"
               "function aplicar(t){var F=FS[t]||{modelo:'todos',ayuda:'todos'};var n=0;"
               "document.querySelectorAll(\"tr[data-t='\"+t+\"']\").forEach(function(tr){var ok=true;"
               "if(F.modelo!=='todos')ok=(tr.dataset.modelo===F.modelo);"
               "if(ok&&F.ayuda!=='todos')ok=(tr.dataset.ayuda===F.ayuda);"
               "tr.style.display=ok?'':'none';if(ok)n++;});"
               "var c=document.getElementById('count-'+t);if(c)c.textContent=n+' corridas';}"
               "</script>")
    body += ["<h2>Las corridas (más nueva arriba)</h2>", tablas,
             "<p><a href='index.html'>← todas las tareas</a></p>"]
    return page(f"tarea {suite}", "".join(body))


def main() -> None:
    src_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scripts/out/count_mix_smoke"
    out = src_dir / "dossier"
    out.mkdir(parents=True, exist_ok=True)
    episodes = [json.loads(f.read_text()) | {"_file": f} for f in sorted(src_dir.glob("*.json"))]
    episodes.sort(key=lambda p: p.get("run_at", ""), reverse=True)

    ctxs: dict[str, CaseCtx] = {}
    for p in episodes:
        cid = p.get("case_id", "?")
        if cid not in ctxs:
            ctxs[cid] = CaseCtx(cid)
        p["suite"] = ctxs[cid].meta.suite

    suites: dict[str, list[dict]] = {}
    for p in episodes:
        suites.setdefault(p["suite"], []).append(p)

    for suite, runs in suites.items():
        task_page = f"task_{suite}.html"
        for p in runs:
            p["_page"] = f"run_{p['_file'].stem}.html"
            (out / p["_page"]).write_text(run_html(p, ctxs[p["case_id"]], task_page))
        cases = {p["case_id"]: ctxs[p["case_id"]] for p in runs}
        (out / task_page).write_text(task_html(suite, cases, runs, out))

    cards = ""
    for suite, runs in suites.items():
        narrative = ctxs[runs[0]["case_id"]].meta.stakes.narrative
        fechas = [r.get("run_at", "") for r in runs if r.get("run_at")]
        cards += (f"<section><h2><a href='task_{suite}.html'>{esc(suite)}</a></h2>"
                  f"<p>{esc(narrative)}</p>"
                  f"<p class='note'>{len(runs)} corridas · {len({r['case_id'] for r in runs})} mundos (principal + control) · "
                  f"última: {esc(max(fechas) if fechas else '—')}</p></section>")
    (out / "index.html").write_text(page("Tareas", f"<h1>Tareas</h1>{cards}"))
    print(f"OK: {len(episodes)} corridas, {len(suites)} tareas -> {out / 'index.html'}")


if __name__ == "__main__":
    main()
