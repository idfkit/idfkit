"""Profile which stub file causes the type checker slowdown."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "idfkit"
GEN_TYPES = SRC / "_generated_types.pyi"
DOC_PYI = SRC / "document.pyi"

RUNS = 3


def _avg_time(cmd: list[str]) -> float:
    times = []
    for _ in range(RUNS):
        t0 = time.perf_counter()
        subprocess.run(cmd, capture_output=True, cwd=ROOT)
        times.append(time.perf_counter() - t0)
    return sum(times) / len(times)


def main() -> None:
    # Save originals
    gen_backup = GEN_TYPES.read_bytes() if GEN_TYPES.exists() else None
    doc_backup = DOC_PYI.read_bytes() if DOC_PYI.exists() else None

    py_cmd = [sys.executable, "-m", "pyright", str(SRC)]
    ty_bin = shutil.which("ty")
    ty_cmd = [ty_bin, "check", str(SRC)] if ty_bin else None

    scenarios = {}

    # 1) Both stubs present
    print("Testing: both stubs present...")
    scenarios["both"] = {"pyright": _avg_time(py_cmd)}
    if ty_cmd:
        scenarios["both"]["ty"] = _avg_time(ty_cmd)

    # 2) Only _generated_types.pyi (no document.pyi overloads)
    print("Testing: only _generated_types.pyi (no document.pyi)...")
    DOC_PYI.unlink(missing_ok=True)
    scenarios["types_only"] = {"pyright": _avg_time(py_cmd)}
    if ty_cmd:
        scenarios["types_only"]["ty"] = _avg_time(ty_cmd)
    if doc_backup:
        DOC_PYI.write_bytes(doc_backup)

    # 3) Only document.pyi (no _generated_types.pyi classes)
    print("Testing: only document.pyi (no _generated_types.pyi)...")
    GEN_TYPES.unlink(missing_ok=True)
    scenarios["doc_only"] = {"pyright": _avg_time(py_cmd)}
    if ty_cmd:
        scenarios["doc_only"]["ty"] = _avg_time(ty_cmd)
    if gen_backup:
        GEN_TYPES.write_bytes(gen_backup)

    # 4) Neither stub
    print("Testing: no stubs...")
    GEN_TYPES.unlink(missing_ok=True)
    DOC_PYI.unlink(missing_ok=True)
    scenarios["none"] = {"pyright": _avg_time(py_cmd)}
    if ty_cmd:
        scenarios["none"]["ty"] = _avg_time(ty_cmd)

    # Restore
    if gen_backup:
        GEN_TYPES.write_bytes(gen_backup)
    if doc_backup:
        DOC_PYI.write_bytes(doc_backup)

    # Print results
    print("\n" + "=" * 65)
    print(f"{'Scenario':<35} {'pyright':>12} {'ty':>12}")
    print("-" * 65)
    for name, label in [
        ("none", "No stubs (baseline)"),
        ("types_only", "_generated_types.pyi only (52K lines)"),
        ("doc_only", "document.pyi only (1718 overloads)"),
        ("both", "Both stubs"),
    ]:
        pr = f"{scenarios[name]['pyright']:.2f}s"
        ty = f"{scenarios[name].get('ty', -1):.2f}s" if "ty" in scenarios[name] else "N/A"
        print(f"  {label:<33} {pr:>12} {ty:>12}")
    print("-" * 65)

    # Deltas
    base_pr = scenarios["none"]["pyright"]
    base_ty = scenarios["none"].get("ty", 0)
    print("\nOverhead vs baseline:")
    for name, label in [
        ("types_only", "_generated_types.pyi"),
        ("doc_only", "document.pyi"),
        ("both", "Both stubs"),
    ]:
        pr_d = scenarios[name]["pyright"] - base_pr
        print(f"  {label:<33} pyright: +{pr_d:.2f}s", end="")
        if "ty" in scenarios[name] and base_ty > 0:
            ty_d = scenarios[name]["ty"] - base_ty
            print(f"   ty: +{ty_d:.2f}s", end="")
        print()


if __name__ == "__main__":
    main()
