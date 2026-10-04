#!/usr/bin/env python3
"""S5 numeric verification for paper02: main.tex numbers vs frozen CSVs.

Exit 0 = all verified. Data: data/analysis_summary.csv,
data/results_mesh_sequence.csv, data/results_eccentric_holdout.csv,
data/analytic_ladder.txt (frozen releases v0.1--v0.3).
"""
import csv
import sys
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "data"
ok, bad = [], []


def check(name, got, want, tol=0.0):
    if isinstance(want, (list, tuple)):
        good = all(abs(g - w) <= (tol or 1e-9) for g, w in zip(got, want)) \
            and len(got) == len(want)
    else:
        good = abs(got - want) <= tol if tol else got == want
    (ok if good else bad).append(f"{name}: got {got}, manuscript {want}")


seq = {r["level"]: r for r in csv.DictReader(open(D / "results_mesh_sequence.csv"))}
summ = {r["quantity"]: r for r in csv.DictReader(open(D / "analysis_summary.csv"))}
hold = list(csv.DictReader(open(D / "results_eccentric_holdout.csv")))
LEVELS = ["M2", "M3", "M4", "M5"]

# --- node counts (abstract, RQ1) ---
check("n_nodes M2", int(seq["M2"]["n_nodes"]), 7489)
check("n_nodes M5", int(seq["M5"]["n_nodes"]), 187600)

# --- trio consistency 1.15% at every level (abstract, RQ1, RQ2: 1.14--1.16) ---
trios = []
for lv in LEVELS:
    r = seq[lv]
    trios.append(abs(abs(float(r["T_amp"]) / float(r["T_slope"])) - 1) * 100)
trios_r = [round(t, 2) for t in trios]
check("trio all within stated 1.14--1.16 (2-dp)", min(trios_r) >= 1.14 and max(trios_r) <= 1.16, 1)
check("trio nominal 1.15 (median)", round(sorted(trios)[1], 2), 1.15)
check("trio min stated 1.14", round(min(trios), 2), 1.14)
check("trio max stated 1.16", round(max(trios), 2), 1.16)

# --- T_slope total spread 0.28% (RQ1: 1.0084..1.0112) ---
sl = [abs(float(seq[lv]["T_slope"])) for lv in LEVELS]
check("T_slope endpoints", (round(min(sl), 4), round(max(sl), 4)), (1.0084, 1.0112))
check("T_slope spread_pct", float(summ["T_slope"]["spread_pct"]), 0.28)

# --- formula-torque constant offset 12.4% (RQ1) ---
offs = [abs(float(seq[lv]["T_form_4coil"]) / abs(float(seq[lv]["T_slope"])) - 1) * 100
        for lv in LEVELS]
check("T_form offset max 12.4", max(offs), 12.4, tol=0.05)

# --- stress ring: level spread 15.4--43.2%, M4 radii, band 77.2% ---
spread_r = [float(summ[q]["spread_pct"]) for q in
            ["T_sum_r292", "T_sum_r295", "T_sum_r298"]]
check("ring spread min", round(min(spread_r), 1), 15.4)
check("ring spread max", round(max(spread_r), 1), 43.2)
m4 = [-float(seq["M4"][q]) for q in ["T_sum_r292", "T_sum_r295", "T_sum_r298"]]
check("M4 radii", tuple(round(v, 4) for v in m4), (0.7795, 0.9724, 1.5306))
band = lambda lv: (max(float(seq[lv][q]) for q in ["T_sum_r292", "T_sum_r295", "T_sum_r298"])
                   - min(float(seq[lv][q]) for q in ["T_sum_r292", "T_sum_r295", "T_sum_r298"])) \
    / abs(float(seq[lv]["T_sum_r295"])) * 100
bands = {lv: round(band(lv), 1) for lv in LEVELS}
check("bands M2..M5", [bands[lv] for lv in LEVELS], [1.0, 25.7, 77.2, 20.2], tol=0.05)

# --- self-energy / Bn diagnostics (RQ1) ---
check("W_pm spread", float(summ["W_pm"]["spread_pct"]), 0.56)
check("Bn spread", float(summ["Bn_noload"]["spread_pct"]), 0.63)
getdp_bn = 0.7585
check("M3 Bn within 0.33% of GetDP",
      round(abs(float(seq["M3"]["Bn_noload"]) - getdp_bn) / getdp_bn * 100, 2), 0.33)

# --- eccentric hold-out (abstract, RQ3): trio 1.15/1.15/1.16, bands 25.7/5.4/7.6 ---
ht, hb = [], []
for r in hold:
    ht.append(round(abs(abs(float(r["T_amp"]) / float(r["T_slope"])) - 1) * 100, 2))
    vs = [float(r[q]) for q in ["T_sum_r292", "T_sum_r295", "T_sum_r298"]]
    hb.append(round((max(vs) - min(vs)) / abs(float(r["T_sum_r295"])) * 100, 1))
check("holdout trios", ht, [1.15, 1.15, 1.16])
check("holdout bands", hb, [25.7, 5.4, 7.6])

# --- analytic ladder (RQ anchor): 0.917% / 0.661% ---
lad = open(D / "analytic_ladder.txt", encoding="utf-8").read()
check("ladder A1 max err", 0.917, 0.917 if "|err|=0.917%" in lad else -1)
check("ladder A2 max err", 0.661, 0.661 if "|err|=0.661%" in lad else -1)

# --- literal scan of headline numbers in main.tex ---
tex = open(Path(__file__).resolve().parents[1] / "manuscript" / "main.tex",
           encoding="utf-8").read()
for lit in ["7{,}489", "187{,}600", "1.15", "15--43", "77", "1.5\\%", "5\\%",
            "1.15--1.16", "5.4--25.7", "0.92", "0.66", "12.4", "0.56", "0.63",
            "0.7585", "25.7", "77.2", "20.2"]:
    if lit not in tex:
        bad.append(f"literal missing in main.tex: {lit}")
    else:
        ok.append(f"literal present: {lit}")

print(f"PASS {len(ok)}")
for b in bad:
    print("FAIL", b)
sys.exit(1 if bad else 0)
