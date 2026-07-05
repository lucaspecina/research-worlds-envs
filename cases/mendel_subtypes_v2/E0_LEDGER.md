# E0_LEDGER — mendel_subtypes_v2 (contabilidad completa de episodios)

GENERADO por build_ledger.py — no editar a mano; regenerar para auditar.
Fase pre-fix = antes de documentar experiment()=un-lote-por-llamada (v0.64-e).
Rama A: R>=0.85 (uso la ventana para la ley del outcome). Rama B: scoreado abajo.
|dP| = error absoluto de P(outcome<-5) (scrap) por item de bateria, server-side.

| trace | modelo | seed | fase | R | R_uncl | \|dP\| mean | \|dP\| max | lee ventana | KB | gasto | turnos | tokens | rama |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e05_DeepSeek-V3.2_seed4.json | DeepSeek-V3.2 | 4 | post-fix | 0.621 | 0.621 | 0.161 | 0.592 | 1 | 1.7 | 8000 | 12 | 81510 | B |
| e05_DeepSeek-V3.2_seed5.json | DeepSeek-V3.2 | 5 | post-fix | 0.666 | 0.666 | 0.256 | 0.483 | 1 | 1.4 | 6310 | 16 | 147918 | B |
| e05_gpt-5.4_seed4.json | gpt-5.4 | 4 | post-fix | 0.639 | 0.639 | 0.265 | 0.65 | 1 | 2.3 | 12040 | 8 | 59131 | B |
| e05_gpt-5.4_seed5.json | gpt-5.4 | 5 | post-fix | 0 | -5.663 | — | — | 1 | 249.3 | 5540 | 6 | 31045 | B |
| e05_gpt-5.4_seed6.json | gpt-5.4 | 6 | post-fix | 0 | -4.937 | 0.184 | 0.641 | 1 | 224.8 | 5660 | 7 | 46220 | B |
| e05_gpt-5.4_seed7.json | gpt-5.4 | 7 | post-fix | 0 | -0.822 | 0.195 | 0.52 | 1 | 72.4 | 6200 | 8 | 48038 | B |
| e0_gpt-5.4_seed0.json | gpt-5.4 | 0 | pre-fix | 0 | -2.317 | 0.243 | 0.731 | 1 | 123.9 | 7100 | 7 | 38658 | B |
| e0_gpt-5.4_seed1.json | gpt-5.4 | 1 | pre-fix | 0 | -1.064 | 0.287 | 0.794 | 1 | 153.9 | 10760 | 7 | 40753 | B |
| e0_gpt-5.4_seed2.json | gpt-5.4 | 2 | post-fix | — | — | — | — | 0 | 0 | 6340 | 7 | 47631 | abort:no_cell |
| e0_gpt-5.4_seed3.json | gpt-5.4 | 3 | post-fix | 0.096 | 0.096 | 0.182 | 0.609 | 1 | 25.7 | 9340 | 7 | 42569 | B |
