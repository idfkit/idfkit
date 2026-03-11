"""Profile __getitem__ overloads vs add() overloads separately."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "idfkit"
DOC_PYI = SRC / "document.pyi"

RUNS = 3


def _avg_time(cmd: list[str]) -> float:
    times = []
    for _ in range(RUNS):
        t0 = time.perf_counter()
        subprocess.run(cmd, capture_output=True, cwd=ROOT)
        times.append(time.perf_counter() - t0)
    return sum(times) / len(times)


def _read_pyi_parts() -> tuple[str, str, str, str]:
    """Split document.pyi into header, getitem overloads, add overloads, footer."""
    content = DOC_PYI.read_text()
    lines = content.splitlines(keepends=True)

    # Find boundaries
    getitem_start = None
    getitem_end = None
    add_start = None
    add_end = None

    for i, line in enumerate(lines):
        if "def __getitem__" in line and getitem_start is None:
            getitem_start = i - 1  # include @overload
        if "def __getitem__" in line:
            getitem_end = i + 1
        if "def add(" in line and add_start is None:
            add_start = i - 1
        if "def add(" in line:
            add_end = i + 1

    assert getitem_start is not None
    assert add_start is not None

    header = "".join(lines[:getitem_start])
    getitem_block = "".join(lines[getitem_start:getitem_end])
    middle = "".join(lines[getitem_end:add_start])
    add_block = "".join(lines[add_start:add_end])
    footer = "".join(lines[add_end:])

    return header, getitem_block, middle, add_block, footer  # type: ignore[return-value]


def main() -> None:
    original = DOC_PYI.read_text()
    header, getitem_block, middle, add_block, footer = _read_pyi_parts()

    py_cmd = [sys.executable, "-m", "pyright", str(SRC)]
    ty_bin = shutil.which("ty")
    ty_cmd = [ty_bin, "check", str(SRC)] if ty_bin else None

    # Fallback overloads
    getitem_fallback = "    def __getitem__(self, obj_type: str) -> IDFCollection[IDFObject]: ...\n"
    add_fallback = "    def add(self, obj_type: str, name: str = ..., data: dict[str, Any] | None = ..., *, validate: bool = ..., **kwargs: Any) -> IDFObject: ...\n"

    results: dict[str, dict[str, float]] = {}

    # 1) Both overloads
    print("Testing: both __getitem__ + add overloads (original)...")
    results["both"] = {"pyright": _avg_time(py_cmd)}
    if ty_cmd:
        results["both"]["ty"] = _avg_time(ty_cmd)

    # 2) Only __getitem__ overloads, no add overloads
    print("Testing: only __getitem__ overloads...")
    DOC_PYI.write_text(header + getitem_block + middle + add_fallback + footer)
    results["getitem_only"] = {"pyright": _avg_time(py_cmd)}
    if ty_cmd:
        results["getitem_only"]["ty"] = _avg_time(ty_cmd)

    # 3) Only add overloads, no __getitem__ overloads
    print("Testing: only add() overloads...")
    DOC_PYI.write_text(header + getitem_fallback + middle + add_block + footer)
    results["add_only"] = {"pyright": _avg_time(py_cmd)}
    if ty_cmd:
        results["add_only"]["ty"] = _avg_time(ty_cmd)

    # 4) No overloads at all (just fallbacks)
    print("Testing: no overloads (fallbacks only)...")
    DOC_PYI.write_text(header + getitem_fallback + middle + add_fallback + footer)
    results["none"] = {"pyright": _avg_time(py_cmd)}
    if ty_cmd:
        results["none"]["ty"] = _avg_time(ty_cmd)

    # Restore original
    DOC_PYI.write_text(original)

    # Print results
    base_pr = results["none"]["pyright"]
    base_ty = results["none"].get("ty", 0)

    print("\n" + "=" * 70)
    print(f"{'Scenario':<40} {'pyright':>10} {'ty':>10}")
    print("-" * 70)
    for key, label in [
        ("none", "No overloads (fallbacks only)"),
        ("getitem_only", "__getitem__ overloads only (858)"),
        ("add_only", "add() overloads only (858)"),
        ("both", "Both overloads (1716 total)"),
    ]:
        pr = f"{results[key]['pyright']:.2f}s"
        ty = f"{results[key].get('ty', -1):.2f}s" if "ty" in results[key] else "N/A"
        print(f"  {label:<38} {pr:>10} {ty:>10}")

    print("-" * 70)
    print("\nOverhead vs no-overloads baseline:")
    for key, label in [
        ("getitem_only", "__getitem__ overloads"),
        ("add_only", "add() overloads"),
        ("both", "Both"),
    ]:
        pr_d = results[key]["pyright"] - base_pr
        print(f"  {label:<38} pyright: +{pr_d:.2f}s", end="")
        if "ty" in results[key] and base_ty > 0:
            ty_d = results[key]["ty"] - base_ty
            print(f"   ty: +{ty_d:.2f}s", end="")
        print()


if __name__ == "__main__":
    main()
