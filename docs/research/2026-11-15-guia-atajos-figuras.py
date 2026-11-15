"""Figuras de la guia en llano (propuesta 'atajos', 2026-11-15).

Genera dos PNG:
  1) ...-guia-atajos-partida.png : como es una partida, en cuatro pasos (diagrama).
  2) ...-guia-atajos-pajar.png   : la medida 'ver o buscar' (ESQUEMA, no son datos).

Uso:  python 2026-11-15-guia-atajos-figuras.py [carpeta_de_salida]
No usa ningun LLM ni datos externos. Solo matplotlib.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
BLUE = "#2a78d6"      # serie 1
ORANGE = "#eb6834"    # serie 2
BLUE_SOFT = "#cde2fb"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def fig_partida(path):
    fig, ax = plt.subplots(figsize=(12.0, 4.05), dpi=170)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.05)
    ax.axis("off")

    ax.text(0.15, 3.75, "Una partida, en cuatro pasos", fontsize=17, fontweight="bold",
            color=INK, va="center", ha="left")

    steps = [
        ("1", "Recibe", "La regla completa\ny una pregunta lejana:\n«¿cómo va a estar la\ncasilla 7 en el paso\nun trillón?»"),
        ("2", "Experimenta", "Corre el sistema y\nprueba ideas en una\nmáquina chica.\nNo le alcanza para\nllegar paso por paso."),
        ("3", "Entrega", "Un programita que\ncontesta rápido,\ny cuán segura está\nde la respuesta."),
        ("4", "Se corrige", "Contra la respuesta\nexacta. Es una cuenta:\nninguna IA hace\nde juez."),
    ]
    w, h, gap, x0, y0 = 2.55, 2.12, 0.5, 0.15, 1.02
    for i, (num, title, body) in enumerate(steps):
        x = x0 + i * (w + gap)
        box = FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                             linewidth=1.2, edgecolor=AXIS, facecolor="#ffffff")
        ax.add_patch(box)
        ax.add_patch(plt.Circle((x + 0.36, y0 + h - 0.38), 0.21, color=BLUE, zorder=3))
        ax.text(x + 0.36, y0 + h - 0.385, num, color="#ffffff", fontsize=12.5,
                fontweight="bold", ha="center", va="center", zorder=4)
        ax.text(x + 0.72, y0 + h - 0.38, title, color=INK, fontsize=13.5, fontweight="bold",
                ha="left", va="center")
        ax.text(x + 0.2, y0 + h - 0.82, body, color=SECONDARY, fontsize=11, ha="left",
                va="top", linespacing=1.35)
        if i < len(steps) - 1:
            arrow = FancyArrowPatch((x + w + 0.06, y0 + h / 2), (x + w + gap - 0.06, y0 + h / 2),
                                    arrowstyle="-|>", mutation_scale=16, linewidth=1.6,
                                    color=SECONDARY)
            ax.add_patch(arrow)

    ax.text(0.15, 0.48, "Sin el atajo, la pregunta es imposible: la máquina no alcanza.   "
            "Con el atajo, es fácil.", fontsize=12.5, color=INK, ha="left", va="center")
    ax.text(0.15, 0.12, "Diagrama de la propuesta. Todavía no se jugó ninguna partida con una IA.",
            fontsize=9.5, color=MUTED, ha="left", va="center")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(path)
    plt.close(fig)


def fig_pajar(path):
    fig, ax = plt.subplots(figsize=(9.6, 5.6), dpi=170)
    xs = [0, 1, 2]
    ciegas = [1.75, 4.7, 9.0]
    busca = [1.2, 3.4, 6.6]
    ve = [0.65, 0.8, 0.95]

    ax.plot(xs, ciegas, color=SECONDARY, linewidth=2, linestyle=(0, (5, 3)), marker="o",
            markersize=8, markeredgecolor=SURFACE, markeredgewidth=2,
            label="Buscador a ciegas (programa nuestro, sin inteligencia)")
    ax.plot(xs, busca, color=ORANGE, linewidth=2, marker="o", markersize=8,
            markeredgecolor=SURFACE, markeredgewidth=2,
            label="Una IA que busca: su esfuerzo crece con el pajar")
    ax.plot(xs, ve, color=BLUE, linewidth=2, marker="o", markersize=8,
            markeredgecolor=SURFACE, markeredgewidth=2,
            label="Una IA que ve: su esfuerzo casi no crece")

    ax.text(2.07, ciegas[-1], "a ciegas", color=INK, fontsize=11.5, va="center", ha="left")
    ax.text(2.07, busca[-1], "busca", color=INK, fontsize=11.5, va="center", ha="left")
    ax.text(2.07, ve[-1], "ve", color=INK, fontsize=11.5, va="center", ha="left")

    ax.set_xlim(-0.25, 2.55)
    ax.set_ylim(0, 10.3)
    ax.set_xticks(xs)
    ax.set_xticklabels(["Pajar chico", "Pajar mediano", "Pajar grande"], fontsize=12, color=INK)
    ax.set_yticks([])
    ax.set_ylabel("Esfuerzo  (más arriba = más trabajo)", fontsize=11.5, color=SECONDARY, labelpad=10)
    ax.set_xlabel("El mismo atajo, escondido entre cada vez más opciones", fontsize=11.5,
                  color=SECONDARY, labelpad=10)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.tick_params(axis="x", length=0, pad=8)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)

    leg = ax.legend(loc="upper left", frameon=False, fontsize=10.8, labelcolor=INK,
                    handlelength=2.6, borderaxespad=0.2, labelspacing=0.55)
    for line in leg.get_lines():
        line.set_linewidth(2)

    fig.suptitle("¿Lo ve o lo busca? Se nota al agrandar el pajar", fontsize=16.5,
                 fontweight="bold", color=INK, x=0.065, ha="left", y=0.965)
    fig.text(0.065, 0.895, "ESQUEMA de lo que se mediría. No son datos: todavía no se corrió nada.",
             fontsize=10.8, color=SECONDARY, ha="left")
    fig.subplots_adjust(left=0.085, right=0.93, top=0.84, bottom=0.14)
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    out.mkdir(parents=True, exist_ok=True)
    fig_partida(out / "2026-11-15-guia-atajos-partida.png")
    fig_pajar(out / "2026-11-15-guia-atajos-pajar.png")
    print("ok:", out)
