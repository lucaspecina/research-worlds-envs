"""Figura del doc 2026-11-15 (reformulacion: descubrir = encontrar un atajo).
Arriba: dos reglas igual de simples; una tiene atajo, la otra no (que se sepa).
Abajo: la misma nube de puntos mirada de dos maneras (el generador RANDU: parece azar, pero
cada numero es 6*anterior - 9*anteanterior (modulo 1), y por eso los puntos caen en 15 planos).
Correr:  python docs/research/2026-11-15-atajos-figura.py docs/research/2026-11-15-atajos-figura.png
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SURFACE, INK, INK2, BLUE = "#fcfcfb", "#0b0b0b", "#52514e", "#2a78d6"


def automaton(rule_fn, steps):
    width = 2 * steps + 1
    grid = np.zeros((steps, width), dtype=np.uint8)
    grid[0, steps] = 1
    for t in range(1, steps):
        left, mid, right = np.roll(grid[t - 1], 1), grid[t - 1], np.roll(grid[t - 1], -1)
        grid[t] = rule_fn(left, mid, right)
    return grid


rule90 = automaton(lambda l, m, r: l ^ r, 128)
rule30 = automaton(lambda l, m, r: l ^ (m | r), 128)

# RANDU: x_{n+1} = 65539 * x_n mod 2^31
vals, x = [], 1
for _ in range(9002):
    x = (65539 * x) % (2**31)
    vals.append(x / 2**31)
v = np.array(vals)
X, Y, Z = v[0:9000:3], v[1:9000:3], v[2:9000:3]
U = 9 * X - 6 * Y + Z
planes = len(set(np.round(U).astype(int)))
exact = float(np.max(np.abs(U - np.round(U))))
print(f"RANDU: {len(X)} puntos; valores distintos de 9x - 6y + z: {planes}; distancia maxima a un entero: {exact:.2e}")

plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": INK2})
fig, axes = plt.subplots(2, 2, figsize=(11, 10.0), dpi=140, facecolor=SURFACE)
fig.subplots_adjust(left=0.05, right=0.95, top=0.875, bottom=0.105, hspace=0.30, wspace=0.10)

cmap = matplotlib.colors.ListedColormap([SURFACE, INK])
for ax, grid, title, sub in (
    (axes[0, 0], rule90, "Regla 90: hay atajo",
     "Se ve el orden. La casilla del paso 1.000.000.000.000.000.000\nse calcula directo, en microsegundos."),
    (axes[0, 1], rule30, "Regla 30: no se conoce atajo",
     "Para saber una casilla lejana de la columna del medio\nhay que hacer toda la cuenta, paso por paso (que se sepa)."),
):
    ax.imshow(grid, cmap=cmap, interpolation="nearest", aspect="equal")
    ax.set_title(title, fontsize=15, fontweight="bold", loc="left", pad=8)
    ax.text(0, -0.04, sub, transform=ax.transAxes, fontsize=11, color=INK2, va="top", linespacing=1.35)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

for ax, (a, b), title, sub in (
    (axes[1, 0], (X, Y), "Mirada obvia: parece puro azar",
     "Cada punto: un número del generador y el que le sigue."),
    (axes[1, 1], (U, Y), f"Mirada justa: {planes} planos, vistos de canto",
     "Los mismos puntos, girados. Aparece la regla escondida:\ncada número = 6 × el anterior − 9 × el de antes\n(quedándose con la parte decimal)."),
):
    ax.scatter(a, b, s=3.2, color=BLUE, alpha=0.75, linewidths=0)
    ax.set_title(title, fontsize=15, fontweight="bold", loc="left", pad=8)
    ax.text(0, -0.04, sub, transform=ax.transAxes, fontsize=11, color=INK2, va="top", linespacing=1.35)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor(SURFACE)
    for s in ax.spines.values():
        s.set_linewidth(0.6); s.set_color("#c9c8c2")

fig.text(0.05, 0.955, "Descubrir = encontrar la mirada que te deja saltar adelante", fontsize=18, fontweight="bold")
fig.text(0.05, 0.925, "Arriba: dos reglas igual de simples (cada casilla mira a sus vecinas). "
                      "Abajo: una misma nube de puntos, mirada de dos maneras.", fontsize=11.5, color=INK2)
out = sys.argv[1] if len(sys.argv) > 1 else "atajos_figura.png"
fig.savefig(out, facecolor=SURFACE)
print("guardado en", out)
