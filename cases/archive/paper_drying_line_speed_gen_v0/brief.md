# Brief: Dryer Speed Bias and Finished Roll Quality

A paper mill has asked you, as an outside consultant, to assess whether adjusting **dryer speed bias** can safely improve performance on a production line.

The operating team’s current belief is straightforward: pushing the dryer section a bit faster should improve throughput, and they suspect it does **not** harm the finished roll. Some on the team even think a higher bias may help quality by stabilizing the sheet path through the dryers. On its face, that sounds plausible.

However, the mill is wary of drawing the wrong conclusion from routine production history alone. Historically, operators did not choose settings at random. During periods when incoming pulp was easier to dewater, they often turned the dryer speed bias **down**, because the sheet already appeared easy to dry. Those same periods also tended to produce better finished rolls. In other words, the historical records may understate the value of the knob: the bias can look less effective than it really is because it was often set lower when conditions were already favorable.

That is why the team wants a careful investigation that distinguishes what can be learned from existing records versus what can be learned from controlled intervention.

You may work within a total budget of **20000** using two information sources:

- **Historical records** via `registros_linea`  
  - Cost: **1.0 per row**
  - Recorded under baseline operating conditions
- **Experiments**  
  - Cost: **100.0 fixed + 2.0 per row**
  - You may directly set:
    - `dryer_speed_bias` from **0 to 10**
    - contextual `shift` from **-1.5 to 1.5**

Relevant variables in the returned data are:

- `dryer_speed_bias` — operator-adjusted 0–10 bias on drying section line speed, where higher values push the sheet through faster
- `wet_end_drain_index` — inline wet-end sensor index that noisily reflects how freely water leaves the fiber web before the dryers
- `roll_quality_score` — final composite quality score for the finished paper roll based on moisture uniformity, strength, and surface finish

The mill’s decision criterion is conservative: **"a scrap -- roll_quality_score below the acceptance line of 24.7 -- is far costlier than a forgone gain"**. Your analysis should therefore focus not just on average performance, but on whether higher bias settings can be recommended without creating unacceptable quality risk.

**Deliverable contract line:**  
`model(regime, n, seed) -> table over [dryer_speed_bias, wet_end_drain_index, roll_quality_score].`