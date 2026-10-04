# Paper 2 — manuscript skeleton (working draft, NOT for the repo release)

Series Paper 2 · genre: **methods/validation study** (formulation-disagreement root-cause + referee criterion)
Target journal: IET Science, Measurement & Technology (main) → COMPEL (backup)
Writing rules: `.claude/skills/sci-paper-writing/SKILL.md（语言层见 references/语言润色-*.md）` (title-style, quantified abstract, zero-fabrication red lines)

## Title candidates (8–16 words, declarative, tool-paper style)

1. "Why Maxwell-Stress and Virtual-Work Torque Disagree in First-Order FEM: A Mesh-Refinement Root-Cause Analysis" (17 words — trim)
2. "Root Causes of FEM Torque Formulation Discrepancies and a Reference-Free Referee Criterion" (14 words) ← **working title**
3. "Arbitrating Discrepant FEM Torque Formulations by an Energy-Balance Identity Residual"

## Abstract skeleton (150–250 words, single paragraph, quantified ending)

- Context: three classical torque formulations applied to the same FEM model routinely disagree by O(10%) — practitioners lack a principled tie-breaker.
- Gap: literature stops at accuracy folklore; no mesh-sequence root-cause taxonomy, no reference-free criterion (docs/gap_evidence.md).
- Method: 5-level mesh refinement × 3 formulations (Maxwell stress ring at 3 radii, virtual-work co-energy slope, formula torque) on a frozen 4-pole/12-slot SPM sector; identity residual ε_id = |W_int − (W_dl − W_nl − W_arm)| tracked per level; analytic ladder cross-check.
- Results (v0.2.0 measured, data/results_mesh_sequence.csv + analysis_summary.csv): integral-quantity trio (virtual-work slope vs co-energy amplitude vs formula torque) agrees to 1.15% CONSTANTLY across M2–M5 (energy side self-consistent); Maxwell stress ring spread across mesh levels 15–43% and SAME-MESH ring-radius band up to 77% (M4) — point-sampled Bn·Bt of P0 piecewise-constant fields carries no convergence meaning; formula torque sits at a constant 12.4% gap due to coil-flux vs energy-consistent λ gauge (flux-gauge gap, not a torque-formulation gap).
- Meaning: practitioners get an operational recipe (mesh level + identity check) to certify torque numbers without reference experiments.

## Section plan

1. **Introduction** — funnel: torque is the design driver → three formulations coexist → published disagreements → no arbitration method → contributions (3 bold bullets, isomorphic):
   - A mesh-sequence root-cause taxonomy of formulation divergence (air-gap resolution vs ring radius vs slope bracketing);
   - A reference-free referee criterion from an exact energy-balance identity;
   - Validation on analytic ladder + production GetDP chain cross-checks.
2. **Related work** — (a) torque computation methods (textbook trio + application-side usage doi:10.1049/iet-epa.2019.0276, doi:10.3390/en13226108); (b) mesh-adaptive quantification (GCI practice); (c) open-stack EM studies (doi:10.1002/2050-7038.12773) — differentiation sentence each.
3. **Methods** — frozen design params; formulations (discrete P1 forms of each); identity derivation; referee-criterion definition (admissible iff GCI band brackets identity-implied balance AND ε_id stabilises); mesh levels table.
4. **Results** — RQ1 divergence taxonomy (CSV tables + convergence plots); RQ2 residual vs spread; RQ3 held-out eccentric family generalisation.
5. **Discussion** — scope (first-order elements, linear magnetics sector model); what breaks at higher order (threats to validity).
6. **Conclusion**.

## Evidence discipline (red lines)

- every number in Results must trace to `data/results_mesh_sequence.csv` at a released tag;
- analytic-ladder values computed by `analytic_verify` lineage, not quoted from memory;
- literature claims only with verified DOIs; H appears only as hypothesis in Intro.
