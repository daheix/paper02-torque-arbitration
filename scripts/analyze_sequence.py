#!/usr/bin/env python3
"""Analyse the mesh-sequence results: convergence of integral vs field-product
formulations, Richardson/GCI for monotone quantities, ring-radius consistency
test for the Maxwell-stress formulation. Writes data/analysis_summary.csv."""
import csv
import math
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "data" / "results_mesh_sequence.csv"


def load():
    rows = list(csv.DictReader(open(CSV)))
    rows.sort(key=lambda r: float(r["lc_air"]))
    return rows


def gci(f1, f2, f3, r=2.0):
    """Richardson observed order + GCI fine-grid error band (Roache).
    f1/f2/f3 = three successive refinements (coarse -> fine)."""
    d1 = abs(f2 - f1)
    d2 = abs(f3 - f2)
    if d2 == 0 or r ** (math.log(d1 / d2) / math.log(r)) - 1 == 0:
        return None
    p = math.log(d1 / d2) / math.log(r)
    fs = f3 + (f3 - f2) / (r ** p - 1)
    gci = 1.25 * abs(d2 / f3) if f3 else float("inf")
    return p, fs, gci


def main():
    rows = load()
    out = []
    print(f"{'quantity':<16}{'M2':>12}{'M3':>12}{'M4':>12}{'M5':>12}  {'spread%':>8}  GCI(fine)")
    for col in ("T_slope", "T_amp", "T_form_4coil", "T_sum_r292", "T_sum_r295", "T_sum_r298", "W_pm", "Bn_noload"):
        assert len(rows) >= 4, "need >=4 mesh levels"
        vals = [float(r[col]) for r in rows[-4:]]  # last 4 levels
        spread = (max(vals) - min(vals)) / abs(vals[-1]) * 100
        g = gci(vals[-3], vals[-2], vals[-1])
        gtxt = f"p={g[0]:.2f} ext={g[1]:.4f} GCI={g[2]*100:.2f}%" if g else "n/a"
        print(f"{col:<16}{vals[0]:>12.4f}{vals[1]:>12.4f}{vals[2]:>12.4f}{vals[3]:>12.4f}  {spread:>7.2f}%  {gtxt}")
        out.append({"quantity": col, "M2": vals[0], "M3": vals[1], "M4": vals[2], "M5": vals[3],
                    "spread_pct": f"{spread:.2f}",
                    "richardson_p": f"{g[0]:.3f}" if g else "",
                    "extrapolated": f"{g[1]:.5f}" if g else "",
                    "gci_fine_pct": f"{g[2]*100:.3f}" if g else ""})

    # ring-radius consistency test on the stress formulation (same mesh, 3 radii)
    print("\nMaxwell ring-radius consistency (same mesh):")
    for r in rows[-4:]:
        v = [float(r[f"T_sum_r{x}"]) for x in ("292", "295", "298")]
        band = (max(v) - min(v)) / abs(v[1]) * 100
        print(f"  {r['level']}: {v[0]:+.4f} {v[1]:+.4f} {v[2]:+.4f}  band={band:5.1f}% of mid-radius")
        out.append({"quantity": f"ring_band_{r['level']}", "M2": v[0], "M3": v[1], "M4": v[2], "M5": "",
                    "spread_pct": f"{band:.2f}", "richardson_p": "", "extrapolated": "", "gci_fine_pct": ""})

    # integral-quantity triangle: slope vs amplitude vs formula (mean-torque trio)
    print("\nMean-torque trio cross-check (|amp|/|slope| and |form4coil|/|slope|, % deviation):")
    for r in rows[-4:]:
        s, a, f4 = abs(float(r["T_slope"])), abs(float(r["T_amp"])), float(r["T_form_4coil"])
        print(f"  {r['level']}: |slope|={s:.4f}  amp={a:.4f} ({abs(a/s-1)*100:.2f}%)  "
              f"form4={f4:.4f} ({abs(f4/s-1)*100:.2f}%)  <- form uses coil-flux lamda, "
              f"known {abs(f4/s-1)*100:.0f}% lambda-gauge gap (energy-consistent lambda would close it)")

    with open(CSV.parent / "analysis_summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["quantity", "M2", "M3", "M4", "M5", "spread_pct",
                                           "richardson_p", "extrapolated", "gci_fine_pct"])
        w.writeheader()
        w.writerows(out)
    print(f"\nwrote {CSV.parent / 'analysis_summary.csv'}")


if __name__ == "__main__":
    main()
