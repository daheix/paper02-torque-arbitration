#!/usr/bin/env python3
"""Paper 2 — RQ3 held-out generalisation: eccentric-rotor family blind test.

Referee criterion frozen from the SPM M2–M5 study (docs/experiment_plan.md):
  (C1) mean-torque trio consistency |amp/slope - 1| <= 1.5%  → mean torque admissible
  (C2) Maxwell ring same-mesh radius band > 5%            → stress ring inadmissible
Apply unchanged to eccentric rotors (10% / 20% of the 1 mm air gap) at M3.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_grid_sequence import ARBITER, CSV_COLS, GETDP_DIR, LEVELS, mesh, parse, run_arbiter  # noqa: E402
from generate_geo import SectorGeoWriter  # noqa: E402

import csv  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402


def build_geo_ecc(ecc_mm: float, workdir: Path, tag: str) -> Path:
    w = SectorGeoWriter(params={"eccentricity_mm": ecc_mm})
    geo = workdir / f"sector_{tag}.geo"
    w.write_geo(str(geo))
    lc_air, lc_iron, lc_shaft = LEVELS["M3"]
    txt = geo.read_text()
    new_lc = f"lc_air = {lc_air};   lc_iron = {lc_iron};  lc_shaft = {lc_shaft};"
    txt, n = re.subn(r"lc_air = [^;]+;\s*lc_iron = [^;]+;\s*lc_shaft = [^;]+;", new_lc, txt, count=1)
    assert n == 1, "lc line not found"
    geo.write_text(txt)
    return geo


def main():
    root = Path("/tmp/p02_runs")
    rows = []
    for tag, ecc in (("ECC0", 0.0), ("ECC10", 0.1), ("ECC20", 0.2)):
        wd = root / tag
        if wd.exists():
            shutil.rmtree(wd)
        wd.mkdir(parents=True)
        print(f"[{tag}] eccentricity={ecc} mm at M3", flush=True)
        geo = build_geo_ecc(ecc, wd, tag)
        t0 = time.time()
        msh = mesh(geo, wd, tag)
        text = run_arbiter(msh)
        (wd / "arbiter_report.txt").write_text(text)
        row = parse(text, "M3")
        row["lc_air"] = ecc            # repurpose column: hold-out variable = eccentricity
        rows.append(row)
        s, a = abs(float(row["T_slope"])), abs(float(row["T_amp"]))
        v = [abs(float(row[f"T_sum_r{x}"])) for x in ("292", "295", "298")]
        band = (max(v) - min(v)) / v[1] * 100
        trio = abs(a / s - 1) * 100
        print(f"  trio={trio:.2f}% (C1 {'PASS' if trio <= 1.5 else 'FAIL'})  "
              f"ring_band={band:.1f}% (C2 stress {'inadmissible' if band > 5 else 'admissible'})  "
              f"[{time.time()-t0:.0f}s]", flush=True)
    csvp = Path(__file__).resolve().parent.parent / "data" / "results_eccentric_holdout.csv"
    with open(csvp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {csvp}", flush=True)


if __name__ == "__main__":
    main()
