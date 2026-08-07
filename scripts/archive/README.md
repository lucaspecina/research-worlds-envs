# Archivo de scripts de eras cerradas (2026-08-07, orden de Lucas)

Probes congelados de eras previas (matriz E1, catalogo de vicios, revision de
creencias, y las tandas count_mix pre-v0.2). NADA se borro: git conserva toda
la historia (`git log --follow scripts/archive/<f>`). Los paths citados en
docs/ADRs anteriores a esta fecha refieren a `scripts/<f>` (ubicacion
original). Los OUTPUTS viejos de scripts/out/ quedan en su lugar porque los
ADRs los citan como evidencia; el Trajectory Explorer los ignora. Tres scripts
viejos siguen vivos porque tests actuales los importan (analyze_scm_topology,
probe_ode_second_wave, probe_scm_topology_controlled_2d).
