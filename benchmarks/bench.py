#!/usr/bin/env python
"""
Benchmark idfkit against eppy, opyplus, and energyplus-idd-idf-utilities.

This script generates a realistic IDF file and benchmarks each tool on:
- Parsing/loading IDF files
- Querying objects by type
- Querying a single object by name
- Adding new objects
- Modifying object fields
- Writing IDF to string/file

Usage:
    uv run --group benchmark python benchmarks/bench.py
"""

from __future__ import annotations

import gc
import json
import os
import platform
import sys
import tempfile
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NUM_ZONES = 500
NUM_MATERIALS = 100
NUM_SURFACES = 1000
ITERATIONS = 10  # Repeat each benchmark
RESULTS_FILE = Path(__file__).parent / "results.json"

# The V24.1 IDD template is fetched from EnergyPlus source and patched at
# runtime.  We cache the result under a .gitignored directory so repeated
# runs are fast.
_IDD_CACHE_DIR = Path(__file__).parent / ".cache"
_IDD_FILE = _IDD_CACHE_DIR / "Energy+V24_1_0.idd"
_IDD_TEMPLATE_URL = "https://raw.githubusercontent.com/NREL/EnergyPlus/v24.1.0/idd/Energy%2B.idd.in"

# Tool names (display order)
TOOL_IDFKIT = "idfkit"
TOOL_EPPY = "eppy"
TOOL_OPYPLUS = "opyplus"
TOOL_IDDIDF = "energyplus-\nidd-idf-utilities"

# Chart colours - one per tool
COLORS = {
    TOOL_IDFKIT: "#4C78A8",
    TOOL_EPPY: "#E45756",
    TOOL_OPYPLUS: "#F58518",
    TOOL_IDDIDF: "#72B7B2",
}


# ---------------------------------------------------------------------------
# IDD download helper
# ---------------------------------------------------------------------------


def _ensure_idd() -> Path:
    """Download and cache the EnergyPlus V24.1 IDD if not already present."""
    if _IDD_FILE.exists():
        return _IDD_FILE

    import subprocess

    _IDD_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print("  Downloading EnergyPlus V24.1 IDD template from GitHub ...")
    result = subprocess.run(
        ["curl", "-sL", _IDD_TEMPLATE_URL],
        capture_output=True,
        check=True,
    )
    # Replace CMake template variables with actual version numbers
    content = result.stdout.decode("latin-1")
    content = (
        content.replace("${CMAKE_VERSION_MAJOR}", "24")
        .replace("${CMAKE_VERSION_MINOR}", "1")
        .replace("${CMAKE_VERSION_PATCH}", "0")
        .replace("${CMAKE_VERSION_BUILD}", "9d7789a3ac")
    )
    _IDD_FILE.write_text(content, encoding="latin-1")
    print(f"  Cached IDD at {_IDD_FILE} ({_IDD_FILE.stat().st_size / 1024:.0f} KB)")
    return _IDD_FILE


# ---------------------------------------------------------------------------
# Test-file generation
# ---------------------------------------------------------------------------


def generate_test_idf(
    num_zones: int = NUM_ZONES,
    num_materials: int = NUM_MATERIALS,
    num_surfaces: int = NUM_SURFACES,
) -> str:
    """Generate a realistic IDF file for benchmarking.

    Uses Version 24.1 with a downloaded V24.1 IDD for eppy and idfkit's
    bundled V24.1 epJSON schema.
    """
    lines: list[str] = []
    lines.append("Version, 24.1;")
    lines.append("")

    # Zones
    for i in range(num_zones):
        lines.append(
            f"Zone,\n"
            f"  Zone_{i},                !- Name\n"
            f"  0,                       !- Direction of Relative North {{deg}}\n"
            f"  {i * 10},               !- X Origin {{m}}\n"
            f"  0,                       !- Y Origin {{m}}\n"
            f"  0,                       !- Z Origin {{m}}\n"
            f"  1,                       !- Type\n"
            f"  1;                       !- Multiplier"
        )
        lines.append("")

    # Materials
    for i in range(num_materials):
        lines.append(
            f"Material,\n"
            f"  Material_{i},            !- Name\n"
            f"  MediumRough,             !- Roughness\n"
            f"  0.{i + 1:03d},              !- Thickness {{m}}\n"
            f"  0.16,                    !- Conductivity {{W/m-K}}\n"
            f"  784,                     !- Density {{kg/m3}}\n"
            f"  830,                     !- Specific Heat {{J/kg-K}}\n"
            f"  0.9;                     !- Thermal Absorptance"
        )
        lines.append("")

    # Constructions
    for i in range(num_materials):
        lines.append(f"Construction,\n  Construction_{i},        !- Name\n  Material_{i};            !- Outside Layer")
        lines.append("")

    # Building surfaces
    for i in range(num_surfaces):
        zone_idx = i % num_zones
        const_idx = i % num_materials
        lines.append(
            f"BuildingSurface:Detailed,\n"
            f"  Surface_{i},             !- Name\n"
            f"  Wall,                    !- Surface Type\n"
            f"  Construction_{const_idx},!- Construction Name\n"
            f"  Zone_{zone_idx},         !- Zone Name\n"
            f"  ,                        !- Space Name\n"
            f"  Outdoors,                !- Outside Boundary Condition\n"
            f"  ,                        !- Outside Boundary Condition Object\n"
            f"  SunExposed,              !- Sun Exposure\n"
            f"  WindExposed,             !- Wind Exposure\n"
            f"  0.5,                     !- View Factor to Ground\n"
            f"  4,                       !- Number of Vertices\n"
            f"  0, 0, 3,                 !- Vertex 1 X/Y/Z\n"
            f"  0, 0, 0,                 !- Vertex 2 X/Y/Z\n"
            f"  10, 0, 0,                !- Vertex 3 X/Y/Z\n"
            f"  10, 0, 3;                !- Vertex 4 X/Y/Z"
        )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Timing helper
# ---------------------------------------------------------------------------


def bench(func, iterations: int = ITERATIONS) -> dict[str, float]:
    """Run *func* multiple times and return timing statistics (seconds)."""
    times: list[float] = []
    for _ in range(iterations):
        gc.collect()
        gc.disable()
        t0 = time.perf_counter()
        func()
        t1 = time.perf_counter()
        gc.enable()
        times.append(t1 - t0)
    return {
        "min": min(times),
        "mean": sum(times) / len(times),
        "max": max(times),
        "times": times,
    }


# ---------------------------------------------------------------------------
# idfkit benchmarks
# ---------------------------------------------------------------------------


def benchmark_idfkit(idf_path: str) -> dict[str, dict[str, float]]:
    """Benchmark idfkit on all operations."""
    from idfkit import load_idf, new_document, write_idf

    results: dict[str, dict[str, float]] = {}

    # 1. Parse / Load
    def load():
        load_idf(idf_path)

    results["Load IDF file"] = bench(load)
    model = load_idf(idf_path)

    # 2. Query all objects of a type
    def query_type():
        _ = list(model["Zone"])

    results["Get all objects by type"] = bench(query_type, iterations=ITERATIONS * 10)

    # 3. Query single object by name
    def query_name():
        _ = model["Zone"]["Zone_250"]

    results["Get single object by name"] = bench(query_name, iterations=ITERATIONS * 10)

    # 4. Add 100 new objects
    def add_objects():
        doc = new_document(version=(24, 1, 0))
        for i in range(100):
            doc.add("Zone", f"NewZone_{i}", {"x_origin": float(i * 5)})

    results["Add 100 objects"] = bench(add_objects)

    # 5. Modify fields on all zones
    def modify_fields():
        for zone in model["Zone"]:
            zone.x_origin = 99.0

    results["Modify fields (all zones)"] = bench(modify_fields)

    # 6. Write to string
    def write():
        write_idf(model, None)

    results["Write IDF to string"] = bench(write)

    return results


# ---------------------------------------------------------------------------
# eppy benchmarks
# ---------------------------------------------------------------------------


def benchmark_eppy(idf_path: str) -> dict[str, dict[str, float]]:
    """Benchmark eppy on all operations."""
    from eppy.modeleditor import IDF

    idd_path = _ensure_idd()
    IDF.setiddname(str(idd_path))

    results: dict[str, dict[str, float]] = {}

    # 1. Parse / Load
    def load():
        IDF(idf_path)

    results["Load IDF file"] = bench(load)
    idf = IDF(idf_path)

    # 2. Query all objects of a type
    def query_type():
        _ = idf.idfobjects["Zone"]

    results["Get all objects by type"] = bench(query_type, iterations=ITERATIONS * 10)

    # 3. Query single object by name
    def query_name():
        _ = idf.getobject("Zone", "Zone_250")

    results["Get single object by name"] = bench(query_name, iterations=ITERATIONS * 10)

    # 4. Add 100 new objects
    def add_objects():
        tmp_idf = IDF(idf_path)
        for i in range(100):
            tmp_idf.newidfobject("Zone", Name=f"NewZone_{i}")

    results["Add 100 objects"] = bench(add_objects)

    # 5. Modify fields on all zones
    def modify_fields():
        for zone in idf.idfobjects["Zone"]:
            zone.X_Origin = 99.0

    results["Modify fields (all zones)"] = bench(modify_fields)

    # 6. Write to string
    def write():
        idf.idfstr()

    results["Write IDF to string"] = bench(write)

    return results


# ---------------------------------------------------------------------------
# opyplus benchmarks
# ---------------------------------------------------------------------------


def benchmark_opyplus(idf_path: str) -> dict[str, dict[str, float]]:
    """Benchmark opyplus on all operations."""
    from opyplus import Epm

    results: dict[str, dict[str, float]] = {}

    # 1. Parse / Load
    def load():
        Epm.from_idf(idf_path)

    results["Load IDF file"] = bench(load)
    epm = Epm.from_idf(idf_path)

    # 2. Query all objects of a type
    zones_table = epm.Zone

    def query_type():
        _ = list(zones_table)

    results["Get all objects by type"] = bench(query_type, iterations=ITERATIONS * 10)

    # 3. Query single object by name (opyplus lowercases names)
    def query_name():
        _ = zones_table.one(lambda z: z.name == "zone_250")

    results["Get single object by name"] = bench(query_name, iterations=ITERATIONS * 10)

    # 4. Add 100 new objects
    def add_objects():
        tmp_epm = Epm.from_idf(idf_path)
        tmp_zones = tmp_epm.Zone
        for i in range(100):
            tmp_zones.add(name=f"NewZone_{i}", x_origin=float(i * 5))

    results["Add 100 objects"] = bench(add_objects)

    # 5. Modify fields on all zones
    def modify_fields():
        for zone in zones_table:
            zone.x_origin = 99.0

    results["Modify fields (all zones)"] = bench(modify_fields)

    # 6. Write to file (opyplus only supports file output)
    tmp_out = tempfile.NamedTemporaryFile(suffix=".idf", delete=False)
    tmp_out.close()

    def write():
        epm.to_idf(tmp_out.name)

    results["Write IDF to string"] = bench(write)
    os.unlink(tmp_out.name)

    return results


# ---------------------------------------------------------------------------
# energyplus-idd-idf-utilities benchmarks
# ---------------------------------------------------------------------------


def benchmark_iddidf(idf_path: str) -> dict[str, dict[str, float]]:
    """Benchmark energyplus-idd-idf-utilities on supported operations.

    This tool has a minimal, read-oriented API - no add/modify support.
    """
    from energyplus_iddidf.idf_processor import IDFProcessor

    results: dict[str, dict[str, float]] = {}
    processor = IDFProcessor()

    # 1. Parse / Load
    def load():
        processor.process_file_given_file_path(idf_path)

    results["Load IDF file"] = bench(load)
    idf = processor.process_file_given_file_path(idf_path)

    # 2. Query all objects of a type
    def query_type():
        _ = idf.get_idf_objects_by_type("Zone")

    results["Get all objects by type"] = bench(query_type, iterations=ITERATIONS * 10)

    # 3. Query single object by name (manual linear scan)
    def query_name():
        for obj in idf.get_idf_objects_by_type("Zone"):
            if obj.fields[0] == "Zone_250":
                return obj
        return None

    results["Get single object by name"] = bench(query_name, iterations=ITERATIONS * 10)

    # 4-5. Add / Modify not supported by this library
    # 6. Write - whole_idf_string() requires a paired IDD which this tool
    #    cannot parse for recent EnergyPlus versions, so we skip it.

    return results


# ---------------------------------------------------------------------------
# Chart generation
# ---------------------------------------------------------------------------


def generate_chart(
    all_results: dict[str, dict[str, dict[str, float]]],
    output_path: Path,
) -> None:
    """Generate horizontal bar charts comparing all tools."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    # Use all operations from idfkit (the superset)
    operations = list(all_results[TOOL_IDFKIT].keys())
    tools = [TOOL_IDFKIT, TOOL_EPPY, TOOL_OPYPLUS, TOOL_IDDIDF]

    fig, axes = plt.subplots(
        len(operations),
        1,
        figsize=(10, 2.0 * len(operations) + 1.2),
        constrained_layout=True,
    )
    if len(operations) == 1:
        axes = [axes]

    for idx, (ax, op) in enumerate(zip(axes, operations)):
        # Collect times for tools that support this operation
        tool_names = []
        times = []
        bar_colors = []
        for tool in reversed(tools):  # reversed so idfkit is at the top
            tool_results = all_results.get(tool, {})
            if op in tool_results:
                tool_names.append(tool)
                times.append(tool_results[op]["min"])
                bar_colors.append(COLORS[tool])

        max_t = max(times) if times else 1
        idfkit_t = all_results[TOOL_IDFKIT][op]["min"]

        # Compute speedup vs slowest for title
        slowest = max(times)
        speedup = slowest / idfkit_t if idfkit_t > 0 else float("inf")

        bars = ax.barh(
            tool_names,
            times,
            color=bar_colors,
            height=0.6,
            edgecolor="white",
            linewidth=0.5,
        )

        # Add time labels on bars
        for bar, t in zip(bars, times):
            label = _format_time(t)
            x_pos = bar.get_width()
            if x_pos < max_t * 0.3:
                ax.text(
                    x_pos + max_t * 0.02,
                    bar.get_y() + bar.get_height() / 2,
                    label,
                    va="center",
                    ha="left",
                    fontsize=9,
                    fontweight="bold",
                    color="#333",
                )
            else:
                ax.text(
                    x_pos - max_t * 0.02,
                    bar.get_y() + bar.get_height() / 2,
                    label,
                    va="center",
                    ha="right",
                    fontsize=9,
                    fontweight="bold",
                    color="white",
                )

        title = f"{op}  ({speedup:.1f}x)" if speedup > 1.05 else op
        ax.set_title(title, fontsize=11, fontweight="bold", loc="left", pad=8)
        ax.set_xlim(0, max_t * 1.18)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: _format_time(x)))
        ax.tick_params(axis="x", labelsize=9)
        ax.tick_params(axis="y", labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.invert_yaxis()

    fig.suptitle(
        f"idfkit vs eppy vs opyplus vs energyplus-idd-idf-utilities\n"
        f"{NUM_ZONES} zones, {NUM_MATERIALS} materials, "
        f"{NUM_SURFACES} surfaces ({_total_objects()} total objects)",
        fontsize=12,
        fontweight="bold",
        y=1.02,
    )

    fig.savefig(str(output_path), dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Chart saved to {output_path}")


def _total_objects() -> int:
    return NUM_ZONES + NUM_MATERIALS + NUM_MATERIALS + NUM_SURFACES


def _format_time(seconds: float) -> str:
    """Human-readable time string."""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.0f}ns"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.1f}\u00b5s"
    if seconds < 1:
        return f"{seconds * 1e3:.1f}ms"
    return f"{seconds:.2f}s"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 60)
    print("  idfkit performance benchmark")
    print("=" * 60)
    print(f"  Python  : {sys.version.split()[0]}")
    print(f"  Platform: {platform.system()} {platform.machine()}")
    print(f"  Objects : {NUM_ZONES} zones, {NUM_MATERIALS} materials,")
    print(f"            {NUM_MATERIALS} constructions, {NUM_SURFACES} surfaces")
    print(f"            ({_total_objects()} total)")
    print(f"  Iters   : {ITERATIONS}")
    print("=" * 60)

    # Generate test IDF
    print("\nGenerating test IDF file ...")
    idf_text = generate_test_idf()
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".idf", delete=False)
    tmp.write(idf_text)
    tmp.close()
    idf_path = tmp.name
    file_size = os.path.getsize(idf_path)
    print(f"  File size: {file_size / 1024:.1f} KB")

    # Ensure the IDD is ready before starting timers
    _ensure_idd()

    all_results: dict[str, dict[str, dict[str, float]]] = {}

    try:
        runners = [
            (TOOL_IDFKIT, benchmark_idfkit),
            (TOOL_EPPY, benchmark_eppy),
            (TOOL_OPYPLUS, benchmark_opyplus),
            (TOOL_IDDIDF, benchmark_iddidf),
        ]

        for name, runner_fn in runners:
            print(f"\nBenchmarking {name} ...")
            results = runner_fn(idf_path)
            all_results[name] = results
            for op, r in results.items():
                print(f"  {op:30s}  {_format_time(r['min']):>10s}")

        # Summary
        print("\n" + "=" * 60)
        print("  Speedup vs idfkit  (higher = idfkit is faster)")
        print("=" * 60)
        for op in all_results[TOOL_IDFKIT]:
            ik = all_results[TOOL_IDFKIT][op]["min"]
            row = f"  {op:30s}"
            for tool in [TOOL_EPPY, TOOL_OPYPLUS, TOOL_IDDIDF]:
                if op in all_results.get(tool, {}):
                    other = all_results[tool][op]["min"]
                    ratio = other / ik if ik > 0 else float("inf")
                    if ratio >= 1:
                        row += f"  {ratio:6.1f}x"
                    else:
                        row += f"  {1 / ratio:5.1f}x*"
                else:
                    row += "     n/a"
            print(row)
        print("  (* = other tool is faster)")

        # Save results
        output = {
            "metadata": {
                "python": sys.version.split()[0],
                "platform": f"{platform.system()} {platform.machine()}",
                "num_zones": NUM_ZONES,
                "num_materials": NUM_MATERIALS,
                "num_surfaces": NUM_SURFACES,
                "total_objects": _total_objects(),
                "file_size_bytes": file_size,
                "iterations": ITERATIONS,
            },
        }
        for tool_name, tool_results in all_results.items():
            output[tool_name] = {op: {"min": r["min"], "mean": r["mean"]} for op, r in tool_results.items()}

        with open(RESULTS_FILE, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\nResults saved to {RESULTS_FILE}")

        # Generate chart
        chart_path = Path(__file__).parent.parent / "docs" / "assets" / "benchmark.png"
        chart_path.parent.mkdir(parents=True, exist_ok=True)
        generate_chart(all_results, chart_path)

    finally:
        os.unlink(idf_path)


if __name__ == "__main__":
    main()
