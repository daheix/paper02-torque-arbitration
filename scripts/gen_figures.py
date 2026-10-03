#!/usr/bin/env python3
"""Paper 2 figures. All values read from released CSVs (tag v0.3.0) — no
hand-typed numbers; regenerate with `python3 scripts/gen_figures.py`."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

plt.rcParams.update({"font.size": 9, "figure.dpi": 150, "axes.grid": True,
                     "grid.alpha": 0.3, "legend.frameon": False})


def load(name):
    return list(csv.DictReader(open(DATA / name)))


def fig_convergence():
    rows = load("results_mesh_sequence.csv")
    rows.sort(key=lambda r: float(r["lc_air"]), reverse=True)
    levels = [r["level"] for r in rows]
    x = range(len(rows))
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    for col, label, marker in (("T_slope", "virtual work (slope)", "o"),
                               ("T_amp", "co-energy amplitude", "s"),
                               ("T_form_4coil", "formula torque", "^")):
        ax.plot(x, [abs(float(r[col])) for r in rows], marker + "-", label=label, ms=4)
    for rmm, ls in (("292", "--"), ("295", ":"), ("298", "-.")):
        ax.plot(x, [abs(float(r[f"T_sum_r{rmm}"])) for r in rows], ls, marker="x", ms=4,
                color="tab:red", alpha=0.35 + 0.2 * x.__len__() * 0, label=f"Maxwell ring r={rmm[:2]}.{rmm[2]}mm")
    ax.set_xticks(list(x), levels)
    ax.set_xlabel("mesh level (refinement)")
    ax.set_ylabel("|torque| (N·m)")
    ax.set_title("Integral formulations converge; stress ring wanders", fontsize=9.5)
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(FIG / "fig_convergence.pdf")
    plt.close(fig)


def fig_ringband():
    rows = [r for r in load("results_mesh_sequence.csv") if r["level"] != "M1"]
    ecc = load("results_eccentric_holdout.csv")
    labels = [r["level"] for r in rows] + [f"{r['level']}\n(ecc {float(r['lc_air'])*1000:.0f}mm)" for r in ecc]
    vals = []
    for r in rows + ecc:
        v = [abs(float(r[f"T_sum_r{x}"])) for x in ("292", "295", "298")]
        vals.append((max(v) - min(v)) / v[1] * 100)
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    colors = ["tab:blue"] * len(rows) + ["tab:orange"] * len(ecc)
    ax.bar(labels, vals, color=colors)
    ax.axhline(5, color="k", ls="--", lw=1)
    ax.text(0.02, 5.6, "referee threshold 5%", fontsize=7.5)
    ax.set_ylabel("same-mesh ring-radius band (%)")
    ax.set_title("Stress ring fails consistency at every refinement", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(FIG / "fig_ringband.pdf")
    plt.close(fig)


def fig_trio_holdout():
    rows = load("results_eccentric_holdout.csv")
    labels = [f"{float(r['lc_air'])*1000:.0f}mm" for r in rows]
    trio = [abs(abs(float(r["T_amp"]) / float(r["T_slope"])) - 1) * 100 for r in rows]
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.bar(labels, trio, color="tab:green", width=0.5)
    ax.axhline(1.5, color="k", ls="--", lw=1)
    ax.text(0.02, 1.53, "C1 threshold 1.5%", fontsize=7.5)
    ax.set_xlabel("rotor eccentricity (blind hold-out)")
    ax.set_ylabel("trio inconsistency (%)")
    ax.set_title("Criterion passes zero-tuning", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(FIG / "fig_trio_holdout.pdf")
    plt.close(fig)


if __name__ == "__main__":
    fig_convergence()
    fig_ringband()
    fig_trio_holdout()
    print("figures ->", FIG)
