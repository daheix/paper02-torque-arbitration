# Experiment plan — Paper 2 (frozen conventions)

## RQ (testable)

RQ1: Under mesh refinement (≥5 levels, uniform refinements plus air-gap band control), how do the three FEM torque formulations — Maxwell stress ring integration, virtual work (co-energy slope), and formula torque (1.5·p·λ₁·i_pk) — converge, and what is the divergence taxonomy (air-gap resolution vs. non-linear convergence vs. discretisation order)?

RQ2: Does the identity residual `W_int = W_dl − W_nl − W_arm` shrink faster than the inter-formulation spread, such that it can act as a reference-free referee criterion?

RQ3: Does the referee criterion generalise on held-out topologies (eccentric fault family) not used to derive it?

## Frozen design parameters (single-source, from generate_geo.py lineage)

R_RI=0.026 m, MAG_T=0.003 m, R_SI=0.030 m, SLOT_DEPTH=0.012 m, R_SO=0.050 m,
SLOT_HALF_DEG=2.0°, MAG_HALF_DEG=33.75°, P_POLE=2, L_STACK=0.1 m, NC=100,
BR=1.16 T, MUR_MAG=1.05, MUR_IRON=7000, HC=BR/(MUR_MAG·μ0)=8.804e5 A/m.
Load points: armature current phase δ ∈ {75°, 90°, 105°} electrical; js=2e6 A/m² sinusoidal three-phase.

## Matrix

| axis | levels |
|------|--------|
| mesh | M1..M5 (global size ÷2 per level; M3+ adds air-gap band ≤0.2 mm; report N nodes, N tris, min gap layers) |
| formulation | Maxwell stress ring (r = 29.2/29.5/29.8 mm), virtual work slope (W over ±15° electrical), formula torque |
| topology | SPM baseline (frozen params above); eccentric fault (rotor offset 10%/20% air gap); (IPM deferred to T2 scope if runtime exceeds budget) |
| load | no-load (PM only), δ=90° (MTPA-aligned), δ=75°/105° (slope brackets) |

## Metrics (all objective)

1. per-formulation torque value + inter-formulation spread (% of converged reference).
2. GCI (Richardson extrapolation, r=2 refinement ratio, observed order p).
3. identity residual ε_id = |W_int − (W_dl − W_nl − W_arm)| in J and as % of W_dl.
4. analytic-ladder cross-check error (A1/A2/Carter), same P1 code path.

## Referee criterion (to be validated, not assumed)

A formulation result is *admissible* iff (a) its GCI band brackets the identity-residual-implied work balance and (b) ε_id at that mesh level is below the level-4→5 change of ε_id (stabilisation test). Generalisation test: fix criterion from SPM grid sequence; apply unchanged to eccentric family; report hit/miss against analytic and GetDP production-chain values.

## Run protocol

- every run: `--workdir` isolated; seed mesh written by gmsh 4.15.2; solver = standalone P1 FEM (Eigen SimplicialLLT) — deterministic direct solve, no iterative tolerance;
- outputs appended to `data/results_mM_tT_lL.csv` (machine-readable, one row per (mesh, topology, load));
- each release tag freezes the CSV set; no silent edits of published values (new tag + CHANGELOG entry instead).
