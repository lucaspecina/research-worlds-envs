# cases/archive — mundos de eras anteriores

Archivados 2026-08-08 (limpieza "proyecto nuevo", GO de Lucas). Son los mundos certificados y
probes de las eras previas (rabbit_hole/paper_drying = era fundacional; first_story/ode/scm/
overgen/latent_mix/lab_largo = era revisión-de-creencias). **Nada se borró**: quedan como
registro reproducible de los resultados documentados en `docs/` y `docs/adr/`. No los cargan
ni los tests ni los scripts vivos; si un probe archivado se re-ejecuta, sus imports de
`cases.*_common` pueden requerir ajustar rutas.

Los mundos VIVOS (era saltos + fixtures del motor) siguen en `cases/`: count_mix*,
count_regime*, dummy_dose_v0, final_note_decoy_v0, confounded_gen_v0, reskin_pilot_v0,
logistic_yield_v0 (fixture del motor),
latent_mix_v2 (EL TROFEO — vivo con su test) y overgen_stream_v0/twin (el par del
operador +1 transferencia — vivo con sus tests).
