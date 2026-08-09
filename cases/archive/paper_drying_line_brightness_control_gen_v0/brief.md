# brief.md

# Brightness on the Edge

The mill has brought in an outside investigator to answer a practical question with real production consequences: does increasing **steam_profile_bias** actually improve the brightness of finished sheets enough to justify running the line harder in that direction?

Operators on the machine floor believe it does. In day-to-day practice, nudging the dryer steam profile upward is intended to improve final sheet brightness and surface uniformity. But the client is not comfortable relying on shop intuition alone, because the historical record is messy in an important way.

Past operating logs were gathered while the incoming pulp’s underlying bleachability varied from lot to lot. When that latent condition was favorable, the line tended to look easy to run, and operators often backed the steam bias down. At the same time, that same favorable condition naturally pushed finished brightness higher on its own. As a result, the mill worries that the observational record may understate the true value of the steam adjustment: lower settings often appeared alongside better outcomes, not because the lower setting helped, but because the incoming material was already unusually cooperative.

That is why this episode matters. The investigator is being asked to separate line-setting effects from changing incoming conditions and recommend what operating range is actually justified.

You may gather evidence in two ways:

- **Observe historical records** via `registros_linea` at a cost of **1.0 per row**. These records were captured under baseline operating conditions.
- **Run experiments** at a cost of **100.0 fixed + 2.0 per row**. In experiments, you may set:
  - `steam_profile_bias` from **0 to 10**
  - context `shift` from **-1.5 to 1.5**

Total budget: **20000**.

Available data columns are:

- `steam_profile_bias` — 0–10 operator-set bias on the dryer steam profile intended to improve final sheet brightness and surface uniformity.
- `wet_end_fluorescence` — inline fluorescence reading near the wet end, a noisy proxy for how easily the incoming pulp responds to bleaching and drying.
- `final_brightness_score` — end-of-line quality score summarizing the finished paper’s measured brightness and visual acceptability.

The client’s risk posture is explicit: **"a scrap -- final_brightness_score below the acceptance line of 26.7 -- is far costlier than a forgone gain"**.

Your work should aim to support a decision that is both profitable and safe under uncertainty, with particular attention to whether the historical relationship between steam settings and brightness is confounded by variation in incoming pulp quality.

**Deliverable contract:** `model(regime, n, seed) -> table over [steam_profile_bias, wet_end_fluorescence, final_brightness_score]`.