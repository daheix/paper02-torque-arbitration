# paper02-torque-arbitration

**Series · Paper 2** — industrial simulation software research series.
← Previous: [paper01-sim-ui-replication](https://github.com/daheix/paper01-sim-ui-replication) · Series index: [daheix/daheix](https://github.com/daheix/daheix) → Next: (pending)

## What this is

Replication package for **Paper 2: "Root-Cause Analysis and Referee Criteria for Discrepant FEM Torque Formulations under Mesh Refinement"** (working title; target journal: IET Science, Measurement & Technology, then COMPEL).

**Research question.** The three classical finite-element torque formulations — Maxwell stress integration, virtual work, and magnetic co-energy differentiation — disagree by tens of percent on the same meshed machine. When, under a systematic mesh-refinement sequence, do they diverge, and can an *identity residual* (`W_int = W_dl − W_nl − W_arm`, interaction co-energy vs. stress-decomposed work balance) serve as a **reference-free referee criterion** that tells a practitioner which torque number to trust?

**Why it matters.** Practitioners routinely see Maxwell-stress and virtual-work torques disagree on the same model and have no principled way to pick. Classical references stop at "which is more accurate"; there is no modern, mesh-sequence-based root-cause taxonomy nor an arbitration criterion. (Gap evidence: search of 2019–2026 literature, see `docs/gap_evidence.md`.)

## Repository layout

```
scripts/   experiment drivers (mesh sequences, batch runs, tabulation)
data/      machine-readable results (CSV per run; frozen per release tag)
docs/      experiment plan, gap evidence, decisions
```

Paper text is **not** hosted here (journal policy); this repository carries data + code only.

## Status

- [x] v0.1.0 — skeleton: experiment plan, arbiter toolchain inventory, gap evidence
- [ ] v0.2.0 — single-model mesh-sequence pilot (5 levels × 3 formulations)
- [ ] v1.0.0 — full matrix + referee-criterion generalization + analytic cross-check (paper submission)

See [CHANGELOG.md](CHANGELOG.md).

## Provenance

Standalone P1 FEM arbiter (`vw_arbiter` lineage) cross-checked against the Gmsh+GetDP production chain of the ChinaSim Motor Pro workbench; analytic ladder (A1 current-loaded disc, A2 transversely magnetised cylinder, Carter factor) in `analytic_verify` lineage. Design parameters and formula conventions are frozen in `docs/experiment_plan.md`.
