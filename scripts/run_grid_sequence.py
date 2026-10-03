#!/usr/bin/env python3
"""Paper 2 — mesh-refinement sequence driver (M1..M5).

Generates the SPM sector .geo per level (parameterised characteristic lengths,
zero patch to the engineering repo's generate_geo.py — we rewrite only the
`lc_*` definition line after write_geo), meshes with Gmsh (msh2), runs the
standalone P1 FEM torque arbiter, and parses its fixed-format report into CSV.

Usage: run_grid_sequence.py --levels M1 M2 M3 --out data/
"""
import argparse
import csv
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

GETDP_DIR = Path("/home/wsc/wsc/ChinaSimStdio/src/plugins/motor_workbench/simulation/getdp")
ARBITER = GETDP_DIR / "vw_arbiter"
GMSH = Path("/home/wsc/wsc/ChinaSimStdio/bin/third_party/gmsh/bin/gmsh")
sys.path.insert(0, str(GETDP_DIR))
from generate_geo import SectorGeoWriter  # noqa: E402

# Mesh levels: (name, lc_air, lc_iron, lc_shaft) — air gap 1 mm wide, so
# lc_air gives the radial layer count directly (2/4/8/... layers at levels below).
LEVELS = {
    "M1": (0.0020, 0.0048, 0.0080),
    "M2": (0.0010, 0.0024, 0.0040),
    "M3": (0.0005, 0.0012, 0.0020),   # engineering-chain default baseline
    "M4": (0.00025, 0.0006, 0.0010),
    "M5": (0.000125, 0.0003, 0.0005),
}

CSV_COLS = ["level", "lc_air", "n_nodes", "n_tris", "n_gap_tris",
            "T_pm_r292", "T_arm_r292", "T_cross_r292", "T_sum_r292", "T_sum_r295", "T_sum_r298",
            "W_pm", "W_arm90", "W_int_75", "W_int_90", "W_int_105",
            "T_slope", "T_amp", "Bn_noload", "lam2_2coil", "T_form_2coil", "T_form_4coil"]


def build_geo(level: str, workdir: Path) -> Path:
    lc_air, lc_iron, lc_shaft = LEVELS[level]
    w = SectorGeoWriter()                      # frozen design defaults (experiment_plan.md)
    geo = workdir / f"sector_{level}.geo"
    w.write_geo(str(geo))
    txt = geo.read_text()
    new_lc = f"lc_air = {lc_air};   lc_iron = {lc_iron};  lc_shaft = {lc_shaft};"
    txt, n = re.subn(r"lc_air = [^;]+;\s*lc_iron = [^;]+;\s*lc_shaft = [^;]+;", new_lc, txt, count=1)
    assert n == 1, "lc line not found in generated .geo"
    geo.write_text(txt)
    return geo


def mesh(geo: Path, workdir: Path, level: str) -> Path:
    msh = workdir / f"sector_{level}.msh"
    t0 = time.time()
    r = subprocess.run([str(GMSH), "-2", "-format", "msh2", "-o", str(msh), str(geo)],
                       capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, f"gmsh failed M{level}:\n{r.stderr[-2000:]}"
    print(f"  gmsh {level}: {msh.stat().st_size/1e6:.1f} MB in {time.time()-t0:.1f}s", flush=True)
    return msh


def run_arbiter(msh: Path) -> str:
    r = subprocess.run([str(ARBITER), str(msh)], capture_output=True, text=True, timeout=1800)
    assert r.returncode == 0, f"arbiter failed on {msh}:\n{r.stderr[-2000:]}"
    return r.stdout


def grab(pat: str, text: str, cast=float):
    m = re.search(pat, text)
    assert m, f"pattern not found: {pat}"
    return cast(m.group(1))


def parse(text: str, level: str) -> dict:
    row = {"level": level, "lc_air": LEVELS[level][0]}
    row["n_nodes"] = grab(r"mesh: N=(\d+)", text, int)
    row["n_tris"] = grab(r"tris=(\d+)", text, int)
    row["n_gap_tris"] = grab(r"气隙单元 (\d+)", text, int)
    for tag, col in (("29.2", "r292"),):
        pass
    def tsum(rmm):
        m = re.search(rf"r={rmm}mm: T_pm=([+-][\d.]+) T_arm=([+-][\d.]+) T_cross\(90°\)=([+-][\d.]+)\s+和=([+-][\d.]+)", text)
        assert m, f"stress row {rmm} not found"
        return [float(g) for g in m.groups()]
    row["T_pm_r292"], row["T_arm_r292"], row["T_cross_r292"], row["T_sum_r292"] = tsum("29.2")
    row["T_sum_r295"] = tsum("29.5")[3]
    row["T_sum_r298"] = tsum("29.8")[3]
    row["W_pm"] = grab(r"W_pm=([+-]?[\d.]+) J", text)
    row["W_arm90"] = grab(r"W_arm\(90°\)=([+-]?[\d.]+) J", text)
    row["W_int_75"] = grab(r"W_int\(75°\)=([+-][\d.]+)", text)
    row["W_int_90"] = grab(r"W_int\(90°\)=([+-][\d.]+)", text)
    row["W_int_105"] = grab(r"W_int\(105°\)=([+-][\d.]+)", text)
    row["T_slope"] = grab(r"T_avg = p·\(−dW/dδ\) = ([+-][\d.]+) Nm", text)
    row["T_amp"] = grab(r"/ ([\d.]+) Nm \(幅值法", text)
    row["Bn_noload"] = grab(r"极下 <Bn> = ([+-][\d.]+) T", text)
    row["lam2_2coil"] = grab(r"λm\(×2线圈\)=([\d.]+) Wb", text)
    row["T_form_2coil"] = grab(r"T_form\(2线圈\)=([+-]?[\d.]+)", text)
    row["T_form_4coil"] = grab(r"T_form\(4线圈\)=([+-]?[\d.]+) Nm", text)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--levels", nargs="+", default=["M1", "M2", "M3", "M4", "M5"])
    ap.add_argument("--out", default="data")
    args = ap.parse_args()
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    root = Path("/tmp/p02_runs")
    rows = []
    for lv in args.levels:
        wd = root / lv
        if wd.exists():
            shutil.rmtree(wd)
        wd.mkdir(parents=True)
        print(f"[{lv}] lc_air={LEVELS[lv][0]}", flush=True)
        geo = build_geo(lv, wd)
        msh = mesh(geo, wd, lv)
        text = run_arbiter(msh)
        (wd / "arbiter_report.txt").write_text(text)
        rows.append(parse(text, lv))
        print(f"  parsed: T_sum292={rows[-1]['T_sum_r292']} slope={rows[-1]['T_slope']}", flush=True)
    csvp = outdir / "results_mesh_sequence.csv"
    new = not csvp.exists()
    with open(csvp, "a", newline="") as f:
        wcsv = csv.DictWriter(f, fieldnames=CSV_COLS)
        if new:
            wcsv.writeheader()
        wcsv.writerows(rows)
    print(f"appended {len(rows)} rows -> {csvp}", flush=True)


if __name__ == "__main__":
    main()
