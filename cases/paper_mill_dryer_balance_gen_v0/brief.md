# brief.md

# Brief: Dryer Balance and Sheet Finish

You have been engaged as an outside consultant to advise a paper mill on how the **dryer balance index** affects final **sheet finish quality**.

The mill’s operating belief is straightforward: increasing the dryer balance index tends to improve the final sheet finish score. That belief did not arise in a vacuum. In targeted pilot work, when engineers deliberately set the dryer balance index higher, the resulting sheets often appeared to finish better. Those pilot experiences reinforced the view that the knob is a meaningful lever for quality.

However, the picture from day-to-day production records has been less clear. In normal operations, the machine crew responds to the condition of the incoming pulp. When the stock is draining well and the sheet is already drying easily, operators often back the dryer balance index down rather than pushing it up. At the same time, those favorable incoming conditions tend to improve sheet finish on their own. As a result, historical records can make the dryer balance index look less useful than it may actually be, simply because lower knob settings often occurred on easier, better-running days.

Your task is to sort out what is really going on and provide guidance that can support confident operating decisions. This matters because the mill is quality-sensitive and risk-aware: **"a scrap -- sheet_finish_score below the acceptance line of 26.7 -- is far costlier than a forgone gain"**.

## What you can do

You may work within a total budget of **20000** using either or both of the following:

1. **Observe historical records**  
   Access `registros_linea` at a cost of **1.0 per row**. These are production records collected under baseline operating conditions.

2. **Run experiments**  
   Conduct experimental data collection at a cost of **100.0 fixed + 2.0 per row** per experiment. For each experiment, you may choose:
   - `dryer_balance_index` decision knob in **[0, 10]**
   - context `shift` in **[-1.5, 1.5]**

## Available columns

- `dryer_balance_index` — float, au  
  0-10 operator-set balance knob that biases steam and airflow split across the paper machine dryer section.
- `wet_end_response_signal` — float  
  Inline wet-end sensor aggregate that noisily reflects how easily the incoming pulp slurry releases water.
- `sheet_finish_score` — float  
  Final quality score summarizing smoothness, curl control, and surface uniformity of the finished paper.

## Deliverable

Deliver exactly the following interface:

`model(regime, n, seed) -> table over [dryer_balance_index, wet_end_response_signal, sheet_finish_score].`