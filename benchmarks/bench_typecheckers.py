"""Benchmark type checker performance with and without generated stubs.

Measures wall-clock time for pyright, mypy, and ty to type-check:
1. The full idfkit package (src/idfkit/)
2. A small consumer script that exercises typed APIs

Run:
    uv run python benchmarks/bench_typecheckers.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "idfkit"
STUBS = [SRC / "_generated_types.pyi", SRC / "document.pyi"]

# A small script that exercises the typed API surface
CONSUMER_SCRIPT = textwrap.dedent("""\
    from idfkit import new_document, load_idf, IDFDocument

    doc = new_document()
    zones = doc["Zone"]
    zone = doc.add("Zone", "Office")
    name: str = zone.name

    strict_doc = new_document(strict=True)
    copy = strict_doc.copy()
""")

RUNS = 3  # number of runs per benchmark


def _run_timed(cmd: list[str], label: str, *, cwd: Path | None = None) -> float:
    """Run a command, return wall-clock seconds. Returns -1 on failure."""
    times: list[float] = []
    for i in range(RUNS):
        start = time.perf_counter()
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or ROOT)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        if i == 0 and result.returncode != 0:
            errors = [line for line in result.stdout.splitlines() if "error" in line.lower()]
            if errors:
                print(f"    {label}: {len(errors)} error(s) on first run")

    avg = sum(times) / len(times)
    return avg


def _hide_stubs() -> list[tuple[Path, Path]]:
    """Temporarily rename stub files so type checkers don't see them."""
    moved: list[tuple[Path, Path]] = []
    for stub in STUBS:
        if stub.exists():
            hidden = stub.with_suffix(".pyi.hidden")
            stub.rename(hidden)
            moved.append((hidden, stub))
    return moved


def _restore_stubs(moved: list[tuple[Path, Path]]) -> None:
    """Restore hidden stub files."""
    for hidden, original in moved:
        if hidden.exists():
            hidden.rename(original)


def bench_pyright_package(with_stubs: bool) -> float:
    """Benchmark pyright on the full package."""
    cmd = [sys.executable, "-m", "pyright", str(SRC)]
    label = f"pyright package ({'with' if with_stubs else 'without'} stubs)"
    return _run_timed(cmd, label)


def bench_pyright_consumer(consumer_path: Path, with_stubs: bool) -> float:
    """Benchmark pyright on a small consumer script."""
    cmd = [sys.executable, "-m", "pyright", str(consumer_path)]
    label = f"pyright consumer ({'with' if with_stubs else 'without'} stubs)"
    return _run_timed(cmd, label)


def bench_mypy_package(with_stubs: bool) -> float:
    """Benchmark mypy on the full package."""
    cmd = [
        sys.executable,
        "-m",
        "mypy",
        "--no-incremental",
        "--ignore-missing-imports",
        str(SRC),
    ]
    label = f"mypy package ({'with' if with_stubs else 'without'} stubs)"
    return _run_timed(cmd, label)


def bench_mypy_consumer(consumer_path: Path, with_stubs: bool) -> float:
    """Benchmark mypy on a small consumer script."""
    cmd = [
        sys.executable,
        "-m",
        "mypy",
        "--no-incremental",
        "--ignore-missing-imports",
        str(consumer_path),
    ]
    label = f"mypy consumer ({'with' if with_stubs else 'without'} stubs)"
    return _run_timed(cmd, label)


def bench_ty_package(with_stubs: bool) -> float:
    """Benchmark ty on the full package."""
    ty_bin = shutil.which("ty")
    if not ty_bin:
        return -1.0
    cmd = [ty_bin, "check", str(SRC)]
    label = f"ty package ({'with' if with_stubs else 'without'} stubs)"
    return _run_timed(cmd, label)


def bench_ty_consumer(consumer_path: Path, with_stubs: bool) -> float:
    """Benchmark ty on a small consumer script."""
    ty_bin = shutil.which("ty")
    if not ty_bin:
        return -1.0
    cmd = [ty_bin, "check", str(consumer_path)]
    label = f"ty consumer ({'with' if with_stubs else 'without'} stubs)"
    return _run_timed(cmd, label)


def _format_time(seconds: float) -> str:
    if seconds < 0:
        return "N/A"
    return f"{seconds:.2f}s"


def _format_delta(with_val: float, without_val: float) -> str:
    if with_val < 0 or without_val < 0:
        return "N/A"
    delta = with_val - without_val
    pct = (delta / without_val) * 100 if without_val > 0 else 0
    sign = "+" if delta > 0 else ""
    return f"{sign}{delta:.2f}s ({sign}{pct:.0f}%)"


def main() -> None:
    print("=" * 72)
    print("Type Checker Benchmark: idfkit with vs without generated stubs")
    print("  Stubs: _generated_types.pyi + document.pyi")
    print("  Stub sizes: ", end="")
    for s in STUBS:
        if s.exists():
            print(f"{s.name}={s.stat().st_size / 1024:.0f}KB  ", end="")
    print()
    print(f"  Runs per benchmark: {RUNS} (reporting average)")
    print("=" * 72)

    # Write consumer script to a temp file
    tmp_dir = Path(tempfile.mkdtemp(prefix="idfkit_bench_"))
    consumer_path = tmp_dir / "consumer.py"
    consumer_path.write_text(CONSUMER_SCRIPT)

    results: dict[str, dict[str, float]] = {}

    # ---- WITH stubs ----
    print("\n--- WITH stubs ---")
    results["with"] = {}

    print("  Running pyright (package)...")
    results["with"]["pyright_pkg"] = bench_pyright_package(True)

    print("  Running pyright (consumer)...")
    results["with"]["pyright_con"] = bench_pyright_consumer(consumer_path, True)

    print("  Running mypy (package)...")
    results["with"]["mypy_pkg"] = bench_mypy_package(True)

    print("  Running mypy (consumer)...")
    results["with"]["mypy_con"] = bench_mypy_consumer(consumer_path, True)

    print("  Running ty (package)...")
    results["with"]["ty_pkg"] = bench_ty_package(True)

    print("  Running ty (consumer)...")
    results["with"]["ty_con"] = bench_ty_consumer(consumer_path, True)

    # ---- WITHOUT stubs ----
    print("\n--- WITHOUT stubs ---")
    moved = _hide_stubs()
    results["without"] = {}

    try:
        print("  Running pyright (package)...")
        results["without"]["pyright_pkg"] = bench_pyright_package(False)

        print("  Running pyright (consumer)...")
        results["without"]["pyright_con"] = bench_pyright_consumer(consumer_path, False)

        print("  Running mypy (package)...")
        results["without"]["mypy_pkg"] = bench_mypy_package(False)

        print("  Running mypy (consumer)...")
        results["without"]["mypy_con"] = bench_mypy_consumer(consumer_path, False)

        print("  Running ty (package)...")
        results["without"]["ty_pkg"] = bench_ty_package(False)

        print("  Running ty (consumer)...")
        results["without"]["ty_con"] = bench_ty_consumer(consumer_path, False)
    finally:
        _restore_stubs(moved)

    # ---- Results table ----
    print("\n" + "=" * 72)
    print(f"RESULTS (average of {RUNS} runs)")
    print("=" * 72)
    print(f"{'Benchmark':<28} {'Without':>10} {'With':>10} {'Delta':>18}")
    print("-" * 72)

    labels = {
        "pyright_pkg": "pyright (full package)",
        "pyright_con": "pyright (consumer script)",
        "mypy_pkg": "mypy (full package)",
        "mypy_con": "mypy (consumer script)",
        "ty_pkg": "ty (full package)",
        "ty_con": "ty (consumer script)",
    }

    for key, label in labels.items():
        w = results["with"].get(key, -1)
        wo = results["without"].get(key, -1)
        delta = _format_delta(w, wo)
        print(f"  {label:<26} {_format_time(wo):>10} {_format_time(w):>10} {delta:>18}")

    print("-" * 72)

    # Stub file info
    print("\nStub file sizes:")
    for s in STUBS:
        if s.exists():
            size_kb = s.stat().st_size / 1024
            lines = len(s.read_text().splitlines())
            print(f"  {s.name}: {size_kb:.0f} KB, {lines:,} lines")

    # Cleanup
    shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
