"""End-to-end HUMAN inspection dossier: the world + its traps + the solver's
episode, turn by turn (Decision Log v0.62).

Factory/report tooling -- NEVER the reward path. Renders one self-contained
HTML per case from artifacts already on disk: brief.md (what the agent saw),
meta.json (the examiner's answer sheet: operators, corrupted sources, stakes),
certificates.json (gates + ladder), and every trace in traces/ (the solver's
reasoning, cells, verbs, submits, final code, R).

CLI:  python -m wager.report.episode_report cases/<case_id>
  -> reports/<case_id>_e2e.html (gitignored, regenerable)
"""

import html
import json
import sys
from pathlib import Path

MAX_OUT = 4000  # chars of cell output shown before truncation


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def md(text: str) -> str:
    try:
        import markdown

        return markdown.markdown(text)
    except Exception:  # noqa: BLE001
        return f"<pre class='block'>{esc(text)}</pre>"


CSS = """
:root{
  --paper:#FAF9F5; --ink:#20242B; --dim:#6E6A61; --rule:#DBD8CE;
  --accent:#0F6B62; --accent-ink:#0A4A44; --card:#FFFFFF;
  --ok:#2E7D4F; --bad:#B4452C; --warn:#9A6B15; --code-bg:#F1EFE9;
}
@media (prefers-color-scheme: dark){:root{
  --paper:#15181C; --ink:#E7E4DC; --dim:#9B968A; --rule:#31363D;
  --accent:#54B8AB; --accent-ink:#7ACCC1; --card:#1C2026;
  --ok:#5CB884; --bad:#D97B60; --warn:#CFA24C; --code-bg:#22262D;
}}
:root[data-theme="dark"]{
  --paper:#15181C; --ink:#E7E4DC; --dim:#9B968A; --rule:#31363D;
  --accent:#54B8AB; --accent-ink:#7ACCC1; --card:#1C2026;
  --ok:#5CB884; --bad:#D97B60; --warn:#CFA24C; --code-bg:#22262D;
}
:root[data-theme="light"]{
  --paper:#FAF9F5; --ink:#20242B; --dim:#6E6A61; --rule:#DBD8CE;
  --accent:#0F6B62; --accent-ink:#0A4A44; --card:#FFFFFF;
  --ok:#2E7D4F; --bad:#B4452C; --warn:#9A6B15; --code-bg:#F1EFE9;
}
body{background:var(--paper);color:var(--ink);
  font:15px/1.55 "Segoe UI",system-ui,-apple-system,sans-serif;
  margin:0;padding:2.2rem 1.2rem 5rem;}
.wrap{max-width:980px;margin:0 auto;display:flex;flex-direction:column;gap:2.4rem;}
h1{font-size:1.7rem;line-height:1.2;margin:0;text-wrap:balance;}
h2{font-size:1.15rem;margin:0 0 .8rem;border-bottom:2px solid var(--accent);
   padding-bottom:.35rem;display:flex;align-items:baseline;gap:.6rem;}
h3{font-size:1rem;margin:1.1rem 0 .45rem;}
.eyebrow{font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-ink);font-weight:600;}
.dim{color:var(--dim);} .small{font-size:.8rem;}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;}
.tablewrap{overflow-x:auto;}
th{font-size:.7rem;letter-spacing:.09em;text-transform:uppercase;color:var(--dim);
   text-align:left;padding:.3rem .6rem;border-bottom:1px solid var(--rule);}
td{padding:.34rem .6rem;border-bottom:1px solid var(--rule);vertical-align:top;}
tr:last-child td{border-bottom:none;}
.chip{display:inline-block;border-radius:999px;padding:.08rem .6rem;font-size:.74rem;
      font-weight:600;border:1px solid transparent;}
.chip.ok{color:var(--ok);border-color:var(--ok);}
.chip.bad{color:var(--bad);border-color:var(--bad);}
.chip.info{color:var(--accent-ink);border-color:var(--accent);}
.card{background:var(--card);border:1px solid var(--rule);border-radius:6px;padding:1rem 1.15rem;}
pre,code{font-family:"Cascadia Code",Consolas,ui-monospace,monospace;font-size:.8rem;}
pre.block{background:var(--code-bg);border:1px solid var(--rule);border-radius:5px;
  padding:.7rem .85rem;overflow-x:auto;white-space:pre;margin:.4rem 0;}
details{border:1px solid var(--rule);border-radius:5px;background:var(--card);
  padding:.5rem .8rem;margin:.35rem 0;}
details>summary{cursor:pointer;font-weight:600;font-size:.85rem;color:var(--accent-ink);}
.turn{border-left:3px solid var(--accent);padding-left:1rem;margin:1.2rem 0;}
.turn.fail{border-left-color:var(--bad);}
.kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:.6rem;}
.kv>div{background:var(--card);border:1px solid var(--rule);border-radius:5px;padding:.5rem .7rem;}
.kv .n{font-size:1.25rem;font-weight:650;font-variant-numeric:tabular-nums;}
.kv .l{font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);}
.brief{border:1px dashed var(--rule);border-radius:6px;padding:.2rem 1.15rem;background:var(--card);}
.note{font-size:.85rem;color:var(--dim);margin:.3rem 0 0;}
.tabs{display:flex;flex-wrap:wrap;gap:.45rem;margin:.2rem 0 1rem;}
.tabs button{font:inherit;font-size:.82rem;font-weight:600;color:var(--ink);
  background:var(--card);border:1px solid var(--rule);border-radius:999px;
  padding:.35rem .95rem;cursor:pointer;display:flex;align-items:center;gap:.5rem;}
.tabs button .r{font-variant-numeric:tabular-nums;font-weight:700;}
.tabs button .r.ok{color:var(--ok);} .tabs button .r.bad{color:var(--bad);}
.tabs button[aria-selected="true"]{border-color:var(--accent);color:var(--accent-ink);
  box-shadow:inset 0 0 0 1px var(--accent);}
.tabs button:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
.ep[hidden]{display:none;}
"""


def chips_from_gates(gates: dict) -> str:
    out = []
    for k, v in gates.items():
        if k == "all":
            continue
        cls = "ok" if v else "bad"
        out.append(f"<span class='chip {cls}'>{esc(k)}: {'PASS' if v else 'FAIL'}</span>")
    return " ".join(out)


def world_section(meta: dict) -> str:
    ops = meta.get("operators", [])
    rows = "".join(
        f"<tr><td><b>{esc(o['name'])}</b></td><td>{esc(o['layer'])}</td>"
        f"<td><code>{esc(json.dumps(o.get('knobs', {})))}</code></td>"
        f"<td><code>{esc(json.dumps(o.get('ablation', {})))}</code></td></tr>"
        for o in ops
    )
    src_rows = []
    for name, s in (meta.get("episode", {}).get("observe_sources", {}) or {}).items():
        traps = []
        if s.get("selection"):
            w = s["selection"]["weights"]
            traps.append(f"selección: Σ({', '.join(f'{k}·{v:g}' for k, v in w.items())}) "
                         f"{'&gt;' if s['selection'].get('keep', 'above') == 'above' else '&lt;'} "
                         f"{s['selection']['threshold']:g} [{s.get('pipeline_order', 'select_then_measure')}]")
        if s.get("channel"):
            ch = s["channel"]
            traps.append(f"canal: {ch['column']} + N(0, {ch['noise_sd']:g})"
                         + (f" × {ch['replicates']} lecturas" if ch.get("replicates", 1) > 1 else ""))
        src_rows.append(f"<tr><td><b>{esc(name)}</b></td><td>{s['cost_per_row']:g}/fila</td>"
                        f"<td>{esc('; '.join(traps)) if traps else '<span class=dim>limpia</span>'}</td></tr>")
    cols = "".join(f"<tr><td><code>{esc(c['name'])}</code></td><td>{esc(c.get('dtype', ''))}</td>"
                   f"<td>{esc(c.get('description', ''))}</td></tr>" for c in meta.get("columns", []))
    fx = meta.get("stakes", {}).get("functionals", [])
    fx_html = "".join(
        f"<p><span class='chip info'>{esc(f['name'])}</span> "
        f"<code>P({esc(f['column'])} {'&lt;' if f.get('direction') == 'below' else '&gt;'} "
        f"{f.get('threshold')})</code> — <em>“{esc(f['brief_clause'])}”</em></p>"
        for f in fx
    )
    return f"""
<section><h2><span class='eyebrow'>lado fábrica</span> El mundo y sus trampas</h2>
<h3>Operadores instalados (la hoja de respuestas del examinador)</h3>
<div class='tablewrap'><table><tr><th>operador</th><th>capa</th><th>knobs</th><th>ablación</th></tr>{rows}</table></div>
<h3>Fuentes (lo que corrompe cada vista)</h3>
<div class='tablewrap'><table><tr><th>fuente</th><th>costo</th><th>corrupciones declaradas</th></tr>{''.join(src_rows)}</table></div>
<h3>Columnas del entregable</h3>
<div class='tablewrap'><table><tr><th>col</th><th>tipo</th><th>descripción</th></tr>{cols}</table></div>
<h3>Funcional de stakes (la moneda del cliente)</h3>{fx_html or "<p class='dim'>sin funcional declarado</p>"}
</section>"""


def certificates_section(cert: dict) -> str:
    if not cert:
        return ""
    r_rows = "".join(f"<tr><td>{esc(k)}</td><td>{v:+.4f}</td></tr>"
                     for k, v in (cert.get("R") or {}).items())
    extra = ""
    if "R_canonical" in cert:
        extra = (f"<p><b>Techo alcanzable</b> (canónico-con-réplicas): R = {cert['R_canonical']:.4f}"
                 f" · σ̂_med = {cert.get('sigma_hat', float('nan')):.4f}</p>")
    return f"""
<section><h2><span class='eyebrow'>certificación</span> Gates y escalera</h2>
<p>{chips_from_gates(cert.get('gates', {}))}</p>
<p class='small dim'>denominador S_verdad − S_ingenuo = {cert.get('denom_raw', float('nan')):.4f}
 · batería K = {cert.get('battery_k', '—')} ({cert.get('obs_items', '—')} observacionales)</p>{extra}
<div class='tablewrap'><table><tr><th>rung / rival</th><th>R</th></tr>{r_rows}</table></div>
</section>"""


def episode_section(trace: dict, fname: str) -> str:
    sig = trace.get("signal", {})
    # aborted episodes (e.g. no_cell) carry R=None: show the abort, never a score
    if trace.get("R") is None:
        r_chip = f"<span class='chip bad'>abortado: {esc(str(trace.get('abort_reason', '?')))}</span>"
    else:
        r_chip = (f"<span class='chip {'ok' if trace['R'] > 0.5 else 'bad'}'>R = {trace['R']:.3f}</span>"
                  f" <span class='small dim'>(R_uncl {trace.get('R_unclipped', 0):+.3f})</span>")
    head = f"""
<h3>{esc(fname)} — {r_chip}</h3>
<div class='kv'>
 <div><div class='n'>{trace.get('turns')}</div><div class='l'>turnos</div></div>
 <div><div class='n'>{trace.get('budget_spent', 0):.0f}</div><div class='l'>presupuesto / {trace.get('budget_total', 0):.0f}</div></div>
 <div><div class='n'>{trace.get('tokens', {}).get('total', '—')}</div><div class='l'>tokens</div></div>
 <div><div class='n'>{trace.get('wall_seconds', '—')}s</div><div class='l'>reloj</div></div>
 <div><div class='n'>{'✓' if sig.get('attribution_before_experiment') else '✗'}</div><div class='l'>atribuye antes de experimentar</div></div>
</div>"""
    turns = []
    for t in trace.get("trace", []):
        verbs = t.get("verbs", [])
        submits = t.get("submit_attempts", [])
        fail = any(not s["args"].get("accepted") for s in submits)
        vrows = "".join(
            f"<tr><td><b>{esc(v['verb'])}</b></td><td><code>{esc(json.dumps(v['args'], ensure_ascii=False))[:160]}</code></td>"
            f"<td>{v['cost']:g}</td><td class='small dim'>{esc(v.get('note', ''))[:220]}</td></tr>"
            for v in verbs + submits)
        raw_out = t.get("cell_result") or ""
        if isinstance(raw_out, dict):
            raw_out = raw_out.get("stdout") or json.dumps(raw_out, ensure_ascii=False, indent=1)
        out = str(raw_out)[:MAX_OUT]
        turns.append(f"""
<div class='turn{' fail' if fail else ''}'>
 <div class='eyebrow'>turno {t.get('turn')}</div>
 <details><summary>razonamiento del solver</summary><pre class='block'>{esc(t.get('reply_text', ''))}</pre></details>
 <details><summary>celda python</summary><pre class='block'>{esc(t.get('cell', ''))}</pre></details>
 <details><summary>salida de la celda</summary><pre class='block'>{esc(out)}</pre></details>
 {f"<div class='tablewrap'><table><tr><th>verbo</th><th>args</th><th>costo</th><th>nota</th></tr>{vrows}</table></div>" if vrows else ""}
</div>""")
    code = trace.get("submission_code") or "(sin código en el trace)"
    return f"""{head}{''.join(turns)}
<details open><summary>SUBMISSION final (lo que se calificó)</summary>
<pre class='block'>{esc(code)}</pre></details>"""


def build_body(case_dir: Path) -> str:
    meta = json.loads((case_dir / "meta.json").read_text(encoding="utf-8"))
    brief = (case_dir / "brief.md").read_text(encoding="utf-8") if (case_dir / "brief.md").exists() else ""
    cert = (json.loads((case_dir / "certificates.json").read_text(encoding="utf-8"))
            if (case_dir / "certificates.json").exists() else {})
    traces = sorted((case_dir / "traces").glob("*.json")) if (case_dir / "traces").exists() else []
    loaded = [(p.name, json.loads(p.read_text(encoding="utf-8"))) for p in traces]
    tabs, panels = [], []
    for i, (fname, tr) in enumerate(loaded):
        r = tr.get("R") or 0.0
        label = fname.replace(".json", "").replace("e0_", "")
        tabs.append(
            f"<button role='tab' id='tab-{i}' aria-selected={'\"true\"' if i == 0 else '\"false\"'} "
            f"aria-controls='ep-{i}' onclick='selEp({i})'>{esc(label)} "
            f"<span class='r {'ok' if r > 0.5 else 'bad'}'>R {r:.3f}</span></button>"
        )
        panels.append(
            f"<div class='ep card' id='ep-{i}' role='tabpanel' aria-labelledby='tab-{i}'"
            f"{'' if i == 0 else ' hidden'}>{episode_section(tr, fname)}</div>"
        )
    eps = ""
    if loaded:
        eps = (
            f"<div class='tabs' role='tablist' aria-label='runs'>{''.join(tabs)}</div>"
            + "".join(panels)
            + """<script>
function selEp(k){
  document.querySelectorAll('.ep').forEach(function(p,i){ p.hidden = (i!==k); });
  document.querySelectorAll('.tabs [role=tab]').forEach(function(t,i){
    t.setAttribute('aria-selected', i===k ? 'true' : 'false'); });
}
</script>"""
        )
    return f"""<title>Dossier E2E — {esc(meta['case_id'])}</title>
<style>{CSS}</style>
<div class='wrap'>
<header>
 <div class='eyebrow'>WAGER · dossier de inspección humana end-to-end</div>
 <h1>{esc(meta['case_id'])} <span class='dim small'>· suite {esc(meta.get('suite', ''))}</span></h1>
 <p class='note'>Tres vistas en orden: lo que el examinador instaló, lo que el agente vio, y lo que el agente hizo — turno a turno, con su razonamiento, su código, sus compras de datos y su entrega final.</p>
</header>
{world_section(meta)}
<section><h2><span class='eyebrow'>lado agente</span> El brief (todo lo que el solver vio)</h2>
<div class='brief'>{md(brief)}</div></section>
{certificates_section(cert)}
<section><h2><span class='eyebrow'>las partidas</span> Episodios ({len(traces)})</h2>
<p class='note'>Elegí el run arriba — se muestra uno a la vez. Los turnos con borde rojo contienen un submit rechazado por el humo; el razonamiento y las celdas vienen colapsados: expandí lo que quieras auditar.</p>
{eps or "<p class='dim'>sin traces en disco</p>"}</section>
</div>"""


def main():
    case_dir = Path(sys.argv[1])
    body = build_body(case_dir)
    out_dir = case_dir.parent.parent / "reports"
    out_dir.mkdir(exist_ok=True)
    page = f"<!doctype html><html lang='es'><head><meta charset='utf-8'>" \
           f"<meta name='viewport' content='width=device-width,initial-scale=1'></head>" \
           f"<body>{body}</body></html>"
    out = out_dir / f"{case_dir.name}_e2e.html"
    out.write_text(page, encoding="utf-8")
    print(f"dossier -> {out}")


if __name__ == "__main__":
    main()
