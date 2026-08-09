# brief.md

# Drying-Section Tension Review

The mill has asked for an outside assessment of a practical operating question: how much value does increasing felt tension really add to final sheet quality?

Inside the plant, the working belief among engineers is straightforward. A tighter felt should help stabilize the paper web through the dryer section, reducing flutter and uneven behavior and, in turn, improving the final sheet. On the surface, that story fits operator experience. But the historical picture is muddier.

Production logs were gathered under ordinary running conditions, not under controlled trials. Over those same shifts, incoming pulp drainability changed in the background. When drainability was high, the sheet tended to behave better on its own, and operators often responded by easing off the felt tension setting because less intervention seemed necessary. That matters because the same favorable condition also tends to improve final quality directly. As a result, the old production history can make the tension knob appear less useful than it truly is, simply because lower tension often happened on easier shifts.

Your role is to sort out that ambiguity and provide a decision-oriented view of the tension setting.

You may work in two ways:

- **Observe historical records** via `registros_linea` at a cost of **1.0 per row**. These records were captured under baseline operating conditions.
- **Run experiments** at a cost of **100.0 fixed + 2.0 per row**. In experiments, you may directly set:
  - `felt_tension_setting` from **0 to 10**
  - a context variable, `shift`, in **[-1.5, 1.5]**

Total available budget: **20000**.

Available data columns:

- `felt_tension_setting` — Operator-adjusted 0–10 felt tension knob used during the drying section to stabilize the paper web.
- `vacuum_box_signal` — Inline vacuum box reading that noisily reflects how easily the incoming pulp-water mix dewaters on the machine.
- `sheet_quality_score` — Final end-of-roll quality score combining smoothness, runnability, and moisture uniformity.

The mill cares about upside, but it is even more sensitive to failure risk: **"a scrap -- sheet_quality_score below the acceptance line of 24.1 -- is far costlier than a forgone gain"**.

Because the production records reflect operator responses to varying shift conditions, controlled tests that assign tension directly are expected to be more informative than passive review alone. Still, historical records are cheap and may help frame the range of normal operation before experiments are planned.

**Deliverable contract line:**  
`model(regime, n, seed) -> table over [felt_tension_setting, vacuum_box_signal, sheet_quality_score].`