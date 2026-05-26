#!/usr/bin/env python
"""Benchmark idfkit's ESO reader against other EnergyPlus ESO readers.

Compares, on a real EnergyPlus ``.eso`` file, two operations:

- **Single variable** — load the file and extract one variable's time series.
  This is idfkit's design target: its lazy reader float-parses only the
  requested variable, so it does far less work than readers that must parse the
  whole file first.
- **Full parse** — make every variable's numeric values available.

Competing readers are benchmarked when importable (install them into the
``benchmark`` group / your environment):

- **esoreader** (``pip install esoreader``) — pure-Python, eager, no environment
  separation, drops daily/monthly min/max.
- **opyplus** (``pip install opyplus``) — pandas-based, environment-aware.
- **pyeso** (``pip install git+https://github.com/frantp/pyeso``) — pure-Python,
  returns raw strings, no environment separation.
- **db_eplusout_reader** (``pip install
  git+https://github.com/DesignBuilderSoftware/db-eplusout-reader``) — fails on
  some reference-building files (weather-file holidays), handled gracefully here.
- **ReadVarsESO** — the native EnergyPlus C++ post-processor (whole-file → CSV).

Usage::

    # Point at an existing .eso, or let the script generate a large one via E+:
    uv run --group benchmark python benchmarks/bench_eso.py [--eso PATH] [--iterations N]
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from pathlib import Path

import bench  # reuse the COLORS / theme palette for visual consistency

_HERE = Path(__file__).parent
RESULTS_FILE = _HERE / "eso_results.json"
ASSETS_DIR = _HERE.parent / "docs" / "assets"

# A variable that exists in the generated reference-office file (and most models).
_VARIABLE = "Zone Mean Air Temperature"

# Display order + chart colours (idfkit first, reuse bench palette where shared).
TOOL_IDFKIT_LAZY = "idfkit\n(lazy)"
TOOL_IDFKIT_FULL = "idfkit\n(eager)"
COLORS: dict[str, str] = {
    TOOL_IDFKIT_LAZY: "#4C78A8",
    TOOL_IDFKIT_FULL: "#3B5F84",
    "esoreader": "#E45756",
    "opyplus": "#F58518",
    "pyeso": "#72B7B2",
    "db_eplusout_reader": "#B279A2",
    "ReadVarsESO": "#9D755D",
}


# ---------------------------------------------------------------------------
# Reader adapters — each returns the number of values it produced (to prove it
# did the work) or raises if unavailable / unable to read the file.
# ---------------------------------------------------------------------------


def _idfkit_one(path: Path) -> int:
    from idfkit.simulation.parsers.eso import ESOResult

    col = ESOResult.from_file(path).get_column(_VARIABLE)
    return len(col.values) if col else 0


def _idfkit_full(path: Path) -> int:
    from idfkit.simulation.parsers.eso import ESOResult

    return sum(len(c.values) for c in ESOResult.from_file(path, eager=True).columns)


def _esoreader_one(path: Path) -> int:
    import esoreader

    eso = esoreader.read_from_path(str(path))
    freq, key, var = eso.find_variable(_VARIABLE, frequency="Hourly")[0]
    return len(eso.data[eso.dd.index[(freq, key, var)]])


def _esoreader_full(path: Path) -> int:
    import esoreader

    eso = esoreader.read_from_path(str(path))
    return sum(len(v) for v in eso.data.values())


def _pyeso_one(path: Path) -> int:
    import pyeso

    data = pyeso.read(str(path))
    for var in data.values():
        if var.name == _VARIABLE and "Hourly" in var.freq:
            return len(var.data)
    return 0


def _pyeso_full(path: Path) -> int:
    import pyeso

    return sum(len(v.data) for v in pyeso.read(str(path)).values())


def _opyplus_one(path: Path) -> int:
    import opyplus

    out = opyplus.StandardOutput(str(path))
    env = list(out.get_environments())[-1]
    df = out.get_data(env, frequency="hourly")
    cols = [c for c in df.columns if _VARIABLE.lower() in c.lower()]
    return int(df[cols[0]].notna().sum()) if cols else 0


def _opyplus_full(path: Path) -> int:
    import opyplus

    out = opyplus.StandardOutput(str(path))
    total = 0
    for env in out.get_environments():
        for freq in ("timestep", "hourly", "daily", "monthly"):
            try:
                df = out.get_data(env, frequency=freq)
            except Exception:
                continue
            if df is not None:
                total += int(df.notna().to_numpy().sum())
    return total


def _dbeso_one(path: Path) -> int:
    from db_eplusout_reader import DBEsoFileCollection, Variable
    from db_eplusout_reader.constants import H

    coll = DBEsoFileCollection.from_path(str(path))
    target = max(coll, key=lambda ef: len(ef.get_results([Variable(None, _VARIABLE, None)], H).first_array))
    return len(target.get_results([Variable(None, _VARIABLE, None)], H).first_array)


def _dbeso_full(path: Path) -> int:
    from db_eplusout_reader import DBEsoFileCollection, Variable
    from db_eplusout_reader.constants import H

    coll = DBEsoFileCollection.from_path(str(path))
    return sum(len(a) for ef in coll for a in ef.get_results([Variable(None, None, None)], H).arrays)


def _readvars_full(path: Path) -> int:
    """Run the native EnergyPlus ReadVarsESO (whole-file -> CSV)."""
    exe = _find_readvars()
    if exe is None:
        raise RuntimeError("ReadVarsESO not found")
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copyfile(path, work / "eplusout.eso")
        subprocess.run([str(exe)], cwd=work, check=True, capture_output=True)
        csv = work / "eplusout.csv"
        return sum(1 for _ in csv.open()) if csv.exists() else 0


def _find_readvars() -> Path | None:
    try:
        from idfkit.simulation import find_energyplus

        post = find_energyplus().install_dir / "PostProcess" / "ReadVarsESO"
        return post if post.exists() else None
    except Exception:
        return None


# name -> (single_variable_fn | None, full_parse_fn | None)
_READERS: dict[str, tuple[Callable[[Path], int] | None, Callable[[Path], int] | None]] = {
    TOOL_IDFKIT_LAZY: (_idfkit_one, None),
    TOOL_IDFKIT_FULL: (None, _idfkit_full),
    "esoreader": (_esoreader_one, _esoreader_full),
    "opyplus": (_opyplus_one, _opyplus_full),
    "pyeso": (_pyeso_one, _pyeso_full),
    "db_eplusout_reader": (_dbeso_one, _dbeso_full),
    "ReadVarsESO": (None, _readvars_full),
}


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------


def _time(fn: Callable[[Path], int], path: Path, iterations: int) -> tuple[float, float, int] | None:
    """Best-of and mean wall time for ``fn(path)``. Returns None if it fails."""
    try:
        n = fn(path)  # warm-up + correctness sentinel
    except Exception as exc:
        print(f"    skipped ({type(exc).__name__}: {str(exc)[:60]})")
        return None
    times: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn(path)
        times.append(time.perf_counter() - start)
    return min(times), sum(times) / len(times), n


def run(eso_path: Path, iterations: int) -> dict[str, object]:
    points = _count_points(eso_path)
    results: dict[str, object] = {
        "metadata": {
            "python": platform.python_version(),
            "platform": f"{platform.system()} {platform.machine()}",
            "eso_file": eso_path.name,
            "file_size_bytes": eso_path.stat().st_size,
            "approx_data_points": points,
            "iterations": iterations,
        }
    }
    for name, (one_fn, full_fn) in _READERS.items():
        ops: dict[str, dict[str, float]] = {}
        for op_name, fn in (("Single variable", one_fn), ("Full parse", full_fn)):
            if fn is None:
                continue
            print(f"  {name!r:24} {op_name} ...", flush=True)
            timed = _time(fn, eso_path, iterations)
            if timed is not None:
                mn, mean, _ = timed
                ops[op_name] = {"min": mn, "mean": mean}
        if ops:
            results[name] = ops
    return results


def _count_points(path: Path) -> int:
    from idfkit.simulation.parsers.eso import ESOResult

    return sum(len(c.values) for c in ESOResult.from_file(path, eager=True).columns)


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------


def _chart(results: dict[str, object], op: str, slug: str, title: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = [(name, vals[op]["min"]) for name, vals in results.items() if name != "metadata" and op in vals]  # type: ignore[index]
    rows.sort(key=lambda r: r[1])
    names = [r[0] for r in rows]
    times_ms = [r[1] * 1000 for r in rows]

    for theme in ("light", "dark"):
        palette = bench._THEMES[theme]
        fig, ax = plt.subplots(figsize=(10, 0.55 * len(names) + 1.4), constrained_layout=True)
        fig.patch.set_facecolor(palette["bg"])
        ax.set_facecolor(palette["bg"])
        bars = ax.barh(names, times_ms, color=[COLORS.get(n, "#888") for n in names])
        ax.invert_yaxis()
        fastest = min(times_ms)
        for bar, t in zip(bars, times_ms):
            label = f"{t:.0f} ms" + (f"  ({t / fastest:.1f}x)" if t > fastest * 1.05 else "")
            ax.text(
                bar.get_width(),
                bar.get_y() + bar.get_height() / 2,
                "  " + label,
                va="center",
                color=palette["text"],
                fontsize=9,
            )
        ax.set_xlabel("milliseconds (lower is better)", color=palette["text"])
        ax.set_title(title, color=palette["title"], fontweight="bold")
        ax.tick_params(colors=palette["tick"])
        for spine in ax.spines.values():
            spine.set_color(palette["spine"])
        ax.set_xlim(0, max(times_ms) * 1.25)

        suffix = "_dark" if theme == "dark" else ""
        out = ASSETS_DIR / f"benchmark_eso_{slug}{suffix}.svg"
        fig.savefig(str(out), bbox_inches="tight", facecolor=palette["bg"])
        plt.close(fig)
        print(f"  chart: {out}")


def _print_table(results: dict[str, object]) -> None:
    meta = results["metadata"]
    print(
        f"\nESO benchmark — {meta['eso_file']} ({meta['file_size_bytes'] / 1e6:.1f} MB, ~{meta['approx_data_points']:,} points)"
    )  # type: ignore[index]
    print(f"{'reader':24} {'single var':>14} {'full parse':>14}")
    for name, vals in results.items():
        if name == "metadata":
            continue
        one = vals.get("Single variable", {}).get("min")  # type: ignore[union-attr]
        full = vals.get("Full parse", {}).get("min")  # type: ignore[union-attr]
        one_s = f"{one * 1000:.0f} ms" if one else "—"
        full_s = f"{full * 1000:.0f} ms" if full else "—"
        print(f"{name.replace(chr(10), ' '):24} {one_s:>14} {full_s:>14}")


def _default_eso() -> Path | None:
    tmp = Path(tempfile.gettempdir())
    for candidate in (tmp / "eso_big" / "out" / "eplusout.eso", _HERE / "large.eso"):
        if candidate.exists():
            return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eso", type=Path, default=None, help="Path to a .eso file to benchmark.")
    parser.add_argument("--iterations", type=int, default=3, help="Timed runs per reader/op.")
    parser.add_argument("--no-render", action="store_true", help="Skip chart generation.")
    args = parser.parse_args()

    eso_path = args.eso or _default_eso()
    if eso_path is None or not eso_path.exists():
        print(
            "No .eso file found. Pass --eso PATH, or generate one, e.g.:\n"
            "  run a large annual EnergyPlus simulation and point --eso at eplusout.eso",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print(f"Benchmarking on {eso_path} ({eso_path.stat().st_size / 1e6:.1f} MB)\n")
    results = run(eso_path, args.iterations)
    RESULTS_FILE.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {RESULTS_FILE}")
    _print_table(results)

    if not args.no_render:
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        _chart(results, "Single variable", "single_variable", "Extract one variable from a large .eso")
        _chart(results, "Full parse", "full_parse", "Parse every variable in a large .eso")


if __name__ == "__main__":
    sys.path.insert(0, str(_HERE))
    main()
