"""Dossier HTML de las corridas count_mix: la tarea EXACTA que vio el agente,
cada turno (razonamiento / codigo / salida del kernel / compras / presupuesto),
la entrega, y la evaluacion con histograma verdad-vs-entrega (SVG, sin deps).

Uso:  python scripts/build_count_mix_dossier.py
Sale: scripts/out/count_mix_smoke/dossier/index.html  (abrir en el navegador)
"""

from __future__ import annotations

import json
import re
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
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import SYSTEM  # noqa: E402
from wager.report.html import code, details, esc, md, page, section, table  # noqa: E402

SMOKE = ROOT / "scripts/out/count_mix_smoke"
OUT = SMOKE / "dossier"

# brief por era: v0 (tecnico/main/pista) desde git, v0.2 (v02_*) el actual
_SHEET = ""  # se llena en main()
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


def _sheet_json() -> str:
    srv = build_world_server(ROOT / "cases/count_mix_v0", seed_offset=0)
    sheet = srv.describe()
    return json.dumps({k: v for k, v in sheet.items() if k != "brief"},
                      indent=2, ensure_ascii=False, default=str)


def _dataset_preview() -> str:
    srv = build_world_server(ROOT / "cases/count_mix_v0", seed_offset=99300)
    df = srv.observe("archivo", 12)
    filas = table(["unit_id", "y (defectos)"],
                  [[f"{r.unit_id:.0f}", f"{r.y:.0f}"] for r in df.itertuples()])
    return ("<p><b>Columnas:</b> <code>unit_id</code> (identificador del lote; se repite si el "
            "mismo lote se mide varias veces) y <code>y</code> (defectos de esa medición, entero "
            "≥ 0). Así se ven las primeras 12 filas del archivo histórico (velocidad 1.0, tope "
            "400 filas por partida; cada partida ve su propia tirada — las filas exactas de cada "
            "una están en su dossier, turno 1):</p>" + filas)


def first_prompt_html(tag: str) -> str:
    note = NOTES.get(tag)
    body = ("<p><b>1) El rol (system prompt — idéntico en todos los mundos WAGER):</b></p>"
            + code(SYSTEM)
            + "<p><b>2) El primer mensaje que recibe (brief + hoja técnica, textual):</b></p>"
            + code("Here is the brief:\n\n" + brief_for(tag)
                   + (("\n\n" + note) if note else "")
                   + "\n\nMachine-readable sheet:\n" + _SHEET
                   + "\n\nReason briefly about your opening plan, then write your first cell. "
                     "`env` is already in the namespace.")
            + "<p class='note'>A partir de ahí, cada turno recibe la salida de su propia celda "
              "(stdout + presupuesto restante) y nada más. El dataset NUNCA se le muestra de "
              "entrada: solo ve lo que compra con env.observe / env.experiment.</p>")
    return details("ver el PROMPT EXACTO (rol + primer mensaje con hoja técnica)", body)


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
    body.append(section("La tarea exacta que vio el agente",
                        details("ver el encargo completo", task) + first_prompt_html(tag),
                        "student"))

    turns = []
    for rec in p["episode"]["trace"]:
        # la prosa sola: el bloque de codigo se muestra UNA vez, en su seccion
        prosa = re.sub(r"```(?:python)?.*?```", "", rec.get("reply_text", ""), flags=re.S).strip()
        inner = ["<h4>Razonamiento</h4>", md(prosa)]
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


ARMS = {
    "tecnico":    {"orden": 1, "nombre": "Prueba técnica",
                   "desc": "1 partida para verificar que la interfaz funciona. Encargo ORIGINAL. No cuenta para conclusiones."},
    "main":       {"orden": 2, "nombre": "Tanda principal (encargo original, sin ayuda)",
                   "desc": "12 partidas: 2 modelos × 2 mundos × 3 seeds. El encargo NO explicaba bien la evaluación (falla detectada después en la auditoría)."},
    "pista":      {"orden": 3, "nombre": "Control de pista (encargo original + frase vaga)",
                   "desc": "8 partidas con la frase 'los datos pueden venir de más de una subpoblación'. No movió nada — la frase era absorbible."},
    "v02_nivel0": {"orden": 4, "nombre": "ÚLTIMA TANDA — encargo corregido, sin ayuda",
                   "desc": "4 partidas con el encargo nuevo (explica cómo se evalúa: 'datos indistinguibles del proceso'). Sin ninguna ayuda."},
    "v02_nivel3": {"orden": 5, "nombre": "ÚLTIMA TANDA — ayuda suave",
                   "desc": "4+2 partidas con la frase 'los lotes podrían venir en unos pocos tipos distintos'."},
    "v02_nivel4": {"orden": 6, "nombre": "ÚLTIMA TANDA — ayuda fuerte (la receta)",
                   "desc": "4+2 partidas con 'probá un modelo de mezcla finita: 2-3 grupos, cada uno con su tasa'."},
}

EXPLICACION = """
<section class='student'>
<h2>La tarea (idéntica en las 37 partidas)</h2>
<p><b>Todas las partidas son el MISMO problema</b>, en una única instancia congelada del mundo.
El agente es "el analista de calidad de una línea de producción". Su trabajo:</p>
<ol>
<li><b>Investigar</b>: puede comprar filas del archivo histórico (baratas; cada fila = un lote con su
cantidad de defectos, medido a velocidad normal) o pagar experimentos (elige la velocidad de la
línea y cuántas veces medir cada lote nuevo). Presupuesto finito: 1000.</li>
<li><b>Entregar</b>: un programita <code>model(...)</code> que GENERA datos de defectos — su teoría
del proceso, hecha código ejecutable.</li>
<li><b>Ser evaluado</b> (nunca ve la nota): el servidor genera datos con su programa y con el proceso
real bajo las mismas condiciones — incluidas condiciones que no vio — y mide qué tan parecidos son.</li>
</ol>
<p><b>El secreto del mundo "mezcla"</b>: los lotes vienen de DOS tipos ocultos (52% con tasa ~10.4
defectos, 48% con ~1.9). En el histograma: dos jorobas con un valle. <b>El gemelo</b> es idéntico en
todo, pero con UN solo proceso (media apareada): sirve para verificar que nadie invente grupos donde
no los hay. El agente nunca sabe en cuál de los dos está.</p>
<p><b>El dataset que ve</b>: filas (lote, defectos) — enteros: 0, 1, 9, 12, 0, 8… Nada le anuncia
que haya tipos; la señal está en la FORMA (dos jorobas, exceso de ceros, mediciones del mismo lote
que se parecen entre sí).</p>
<p><b>Las dos versiones del encargo</b>: las tandas 1–3 corrieron con el encargo ORIGINAL (decía
"reproducí el proceso" sin explicar la evaluación — la auditoría encontró que así el descubrimiento
no era necesario para cumplir). Las tandas 4–6 (<b>la última</b>) corren con el encargo CORREGIDO,
que explica cómo se evalúa sin soplar nada.</p>
</section>"""


def main() -> None:
    inst = load_instance()
    OUT.mkdir(parents=True, exist_ok=True)
    geo, tail_at = inst["geometry"], inst["tail_at"]
    y_train = _sample_counts("mix", inst["params"], _DictRegime({"speed": 1.0}),
                             inst["witness_n"], inst["witness_sample_seed"])["y"].to_numpy(float)
    truth_f = program_functionals(
        lambda r, n, s: _sample_counts("mix", inst["params"], r, n, s), geo, tail_at)
    strong_f = program_functionals(strong_baseline_program(y_train), geo, tail_at)
    global _SHEET
    _SHEET = _sheet_json()
    explic_extra = ("<h3>El prompt exacto y el dataset</h3>" + first_prompt_html("main")
                    + _dataset_preview())
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
        rows.append((ARMS[p["tag"]]["orden"], name, p["tag"], p["model"],
                     "mezcla" if p["pole"] == "mix" else "gemelo", p["seed"], metric,
                     f"{p.get('R'):.3f}" if p.get("R") is not None else "—",
                     p.get("abort_reason")))
    rows.sort()

    leyenda = "".join(
        f"<tr><td class='num'>{a['orden']}</td><td><b>{esc(a['nombre'])}</b></td><td>{esc(a['desc'])}</td></tr>"
        for a in sorted(ARMS.values(), key=lambda x: x["orden"]))
    trs = "".join(
        f"<tr data-tanda='{orden}' data-modelo='{esc(model)}' data-mundo='{mundo}'>"
        f"<td class='num'>{orden}</td><td><a href='{name}'>abrir</a></td>"
        f"<td>{esc(ARMS[tag]['nombre'])}</td><td>{esc(model)}</td><td>{mundo}</td>"
        f"<td class='num'>{seed}</td><td class='num'>{esc(metric)}</td>"
        f"<td class='num'>{esc(r)}</td><td>{esc(fin)}</td></tr>"
        for orden, name, tag, model, mundo, seed, metric, r, fin in rows)

    filtros = """
<div style='margin:14px 0;padding:12px;border:1px solid #e3e3e3;border-radius:8px;background:#fafafa'>
<b>Tanda:</b>
<button onclick="setF('tanda','ultima')" id="b-ultima">Última (encargo corregido)</button>
<button onclick="setF('tanda','todas')" id="b-todas">Todas</button>
<button onclick="setF('tanda','2')" id="b-2">Principal</button>
<button onclick="setF('tanda','3')" id="b-3">Pista</button>
&nbsp;&nbsp;<b>Modelo:</b>
<button onclick="setF('modelo','todos')">Todos</button>
<button onclick="setF('modelo','DeepSeek-V3.2')">DeepSeek</button>
<button onclick="setF('modelo','gpt-5.4')">gpt-5.4</button>
&nbsp;&nbsp;<b>Mundo:</b>
<button onclick="setF('mundo','todos')">Ambos</button>
<button onclick="setF('mundo','mezcla')">Mezcla</button>
<button onclick="setF('mundo','gemelo')">Gemelo</button>
<span id='count' style='margin-left:12px;color:#666'></span>
</div>
<script>
var F = {tanda:'ultima', modelo:'todos', mundo:'todos'};
function setF(k, v){ F[k] = v; aplicar(); }
function aplicar(){
  var n = 0;
  document.querySelectorAll('tr[data-tanda]').forEach(function(tr){
    var t = tr.dataset.tanda, ok = true;
    if (F.tanda === 'ultima') ok = (t === '4' || t === '5' || t === '6');
    else if (F.tanda !== 'todas') ok = (t === F.tanda);
    if (ok && F.modelo !== 'todos') ok = (tr.dataset.modelo === F.modelo);
    if (ok && F.mundo !== 'todos') ok = (tr.dataset.mundo === F.mundo);
    tr.style.display = ok ? '' : 'none';
    if (ok) n++;
  });
  document.getElementById('count').textContent = n + ' partidas';
}
window.addEventListener('load', aplicar);
</script>"""

    idx = ["<h1>Dossier count_mix — las 37 partidas de la semana</h1>",
           "<p class='sub'>Mismo problema en todas; lo que cambia entre tandas es el encargo y la ayuda. "
           "Vara del salto (mundos mezcla): 0 = entregó el modelo continuo, 1 = descubrió los dos grupos. "
           "Limpieza (gemelo): 1 = no inventó nada.</p>",
           EXPLICACION, explic_extra,
           "<h2>Las seis tandas, en orden cronológico</h2>",
           "<table><tr><th>#</th><th>tanda</th><th>qué fue</th></tr>" + leyenda + "</table>",
           "<h2>Las partidas</h2>", filtros,
           "<table><tr><th>#</th><th></th><th>tanda</th><th>modelo</th><th>mundo</th><th>seed</th>"
           "<th>vara / limpieza</th><th>R</th><th>fin</th></tr>" + trs + "</table>"]
    (OUT / "index.html").write_text(page("Dossier count_mix", "".join(idx)))
    print(f"OK: {len(rows)} dossiers -> {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
