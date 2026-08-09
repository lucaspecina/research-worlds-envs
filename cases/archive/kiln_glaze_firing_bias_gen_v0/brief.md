# Kiln Soak Intensity and Glaze Finish

The client is a ceramic tile manufacturer trying to decide how much confidence to place in a long-held production belief: that stronger **soak intensity** improves final **glaze finish** by giving the coating more time to level, settle, and mature near peak firing. On the factory floor, that view fits practical experience. But when the team looks back at historical production results, the pattern is murkier than expected.

Their concern is that the historical records were not generated under clean, controlled conditions. While soak settings changed from lot to lot, another important factor was moving too: a hidden difference in **green-body moisture balance** before firing. When that latent condition ran high, operators often responded conservatively and turned soak intensity down to reduce perceived overfiring risk. At the same time, that same latent condition tended to improve final glaze finish on its own. In plain terms, better-finish lots were often paired with lower soak settings for reasons unrelated to soak’s actual effect, which means observational production data may understate how helpful soak intensity really is.

To support the investigation, the following fields are available:

- **soak_intensity**: 0–10 kiln soak intensity setting that lengthens and deepens the high-temperature hold near peak firing  
- **dryer_exit_signature**: inline dryer-exit sensor signature, a noisy proxy related to hidden moisture balance in the green bodies  
- **glaze_finish_score**: final end-of-line quality score combining glaze smoothness, color development, and defect-free appearance  

You may work in two ways. First, you can inspect **historical records** through `registros_linea`, priced at **1.0 per row**; these are recorded under baseline conditions. Second, you can commission **controlled experiments**, priced at **100.0 fixed plus 2.0 per row**, in which you directly set the **decision knob** `soak_intensity` anywhere from **0 to 10** and choose a contextual **shift** anywhere in **[-1.5, 1.5]**. The total investigation budget is **20000**.

Controlled experiments matter here because they break the link between operator choices and the hidden lot condition. The manufacturer wants a credible estimate of the true benefit of stronger soak intensity, not just a historical association clouded by how operators reacted to changing upstream conditions.

The operating priority is conservative quality control: **"a scrap -- glaze_finish_score below the acceptance line of 24.1 -- is far costlier than a forgone gain"**.

**Deliverable:** `model(regime, n, seed) -> table over [soak_intensity, dryer_exit_signature, glaze_finish_score]`.