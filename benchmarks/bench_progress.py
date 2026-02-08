#!/usr/bin/env python
"""Benchmark the performance overhead of on_progress callbacks.

Runs real EnergyPlus simulations (design-day and annual) with and without
progress callbacks, measuring wall-clock time across multiple iterations.

Requirements:
    - EnergyPlus installed and discoverable (or set ENERGYPLUS_DIR)
    - idfkit installed (uv sync)

Usage:
    ENERGYPLUS_DIR=/path/to/EnergyPlus uv run python benchmarks/bench_progress.py
"""

from __future__ import annotations

import asyncio
import gc
import json
import statistics
import sys
import time
from pathlib import Path

from idfkit import load_idf
from idfkit.simulation import SimulationProgress, find_energyplus, simulate
from idfkit.simulation.async_runner import async_simulate
from idfkit.simulation.config import EnergyPlusConfig

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ITERATIONS = 10  # runs per scenario
WARMUP_RUNS = 2  # discarded runs to warm filesystem caches


def _discover_energyplus() -> EnergyPlusConfig:
    try:
        return find_energyplus()
    except Exception:
        print("ERROR: EnergyPlus not found. Set ENERGYPLUS_DIR.", file=sys.stderr)
        sys.exit(1)


def _noop_callback(event: SimulationProgress) -> None:
    """Minimal sync callback — does nothing."""


def _counting_callback() -> tuple[list[int], callable]:
    """Returns a list and a callback that counts events."""
    counts: list[int] = [0]

    def _cb(event: SimulationProgress) -> None:
        counts[0] += 1

    return counts, _cb


def _heavy_callback() -> tuple[list[int], callable]:
    """Callback that does light work (dict creation) per event."""
    counts: list[int] = [0]

    def _cb(event: SimulationProgress) -> None:
        counts[0] += 1
        # Simulate typical real-world work: serialize to dict for logging
        _ = {
            "phase": event.phase,
            "message": event.message,
            "percent": event.percent,
            "environment": event.environment,
            "job_index": event.job_index,
        }

    return counts, _cb


async def _async_noop_callback(event: SimulationProgress) -> None:
    """Minimal async callback."""


# ---------------------------------------------------------------------------
# Benchmark runners
# ---------------------------------------------------------------------------


def run_sync_benchmark(
    model_path: Path,
    weather_path: Path,
    config: EnergyPlusConfig,
    *,
    annual: bool = False,
    design_day: bool = False,
) -> dict:
    """Run sync simulations with different callback configurations."""
    model = load_idf(str(model_path))
    label = "annual" if annual else "design-day"

    scenarios = {
        "no_callback": None,
        "noop_callback": _noop_callback,
        "counting_callback": None,  # placeholder
        "heavy_callback": None,  # placeholder
    }

    results: dict[str, dict] = {}

    for name in scenarios:
        print(f"  [{label}] sync {name}: ", end="", flush=True)
        times: list[float] = []

        for i in range(WARMUP_RUNS + ITERATIONS):
            gc.collect()
            gc.disable()

            if name == "counting_callback":
                counts, cb = _counting_callback()
            elif name == "heavy_callback":
                counts, cb = _heavy_callback()
            elif name == "noop_callback":
                cb = _noop_callback
                counts = None
            else:
                cb = None
                counts = None

            start = time.perf_counter()
            result = simulate(
                model,
                weather_path,
                energyplus=config,
                annual=annual,
                design_day=design_day,
                on_progress=cb,
            )
            elapsed = time.perf_counter() - start
            gc.enable()

            if not result.success:
                print(f"\n    WARNING: simulation failed (exit={result.exit_code})")
                break

            if i >= WARMUP_RUNS:
                times.append(elapsed)
                print(".", end="", flush=True)

        print()

        event_count = counts[0] if counts else 0
        results[name] = {
            "times": times,
            "mean": statistics.mean(times) if times else 0,
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "min": min(times) if times else 0,
            "max": max(times) if times else 0,
            "median": statistics.median(times) if times else 0,
            "event_count_last_run": event_count,
        }

    return results


async def run_async_benchmark(
    model_path: Path,
    weather_path: Path,
    config: EnergyPlusConfig,
    *,
    annual: bool = False,
    design_day: bool = False,
) -> dict:
    """Run async simulations with different callback configurations."""
    model = load_idf(str(model_path))
    label = "annual" if annual else "design-day"

    scenario_names = ["no_callback", "sync_callback", "async_callback"]
    results: dict[str, dict] = {}

    for name in scenario_names:
        print(f"  [{label}] async {name}: ", end="", flush=True)
        times: list[float] = []

        for i in range(WARMUP_RUNS + ITERATIONS):
            gc.collect()
            gc.disable()

            if name == "sync_callback":
                cb = _noop_callback
            elif name == "async_callback":
                cb = _async_noop_callback
            else:
                cb = None

            start = time.perf_counter()
            result = await async_simulate(
                model,
                weather_path,
                energyplus=config,
                annual=annual,
                design_day=design_day,
                on_progress=cb,
            )
            elapsed = time.perf_counter() - start
            gc.enable()

            if not result.success:
                print(f"\n    WARNING: simulation failed (exit={result.exit_code})")
                break

            if i >= WARMUP_RUNS:
                times.append(elapsed)
                print(".", end="", flush=True)

        print()

        results[name] = {
            "times": times,
            "mean": statistics.mean(times) if times else 0,
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "min": min(times) if times else 0,
            "max": max(times) if times else 0,
            "median": statistics.median(times) if times else 0,
        }

    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_comparison(label: str, results: dict) -> None:
    """Print a comparison table for a set of benchmark results."""
    baseline_key = "no_callback"
    baseline = results.get(baseline_key, {})
    baseline_mean = baseline.get("mean", 0)

    print(f"\n{'=' * 72}")
    print(f"  {label}")
    print(f"{'=' * 72}")
    print(f"  {'Scenario':<22} {'Mean':>8} {'Stdev':>8} {'Min':>8} {'Max':>8} {'Overhead':>10} {'Events':>8}")
    print(f"  {'-' * 22} {'-' * 8} {'-' * 8} {'-' * 8} {'-' * 8} {'-' * 10} {'-' * 8}")

    for name, data in results.items():
        mean = data["mean"]
        stdev = data["stdev"]
        mn = data["min"]
        mx = data["max"]
        events = data.get("event_count_last_run", "")

        if baseline_mean > 0 and name != baseline_key:
            overhead_pct = ((mean - baseline_mean) / baseline_mean) * 100
            overhead_str = f"{overhead_pct:+.2f}%"
        else:
            overhead_str = "baseline"

        print(f"  {name:<22} {mean:>7.3f}s {stdev:>7.4f}s {mn:>7.3f}s {mx:>7.3f}s {overhead_str:>10} {events!s:>8}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    config = _discover_energyplus()
    print(f"EnergyPlus: {config.version} at {config.install_dir}")

    example_idf = config.install_dir / "ExampleFiles" / "1ZoneUncontrolled.idf"
    weather = config.install_dir / "WeatherData" / "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"

    if not example_idf.is_file():
        print(f"ERROR: Example IDF not found: {example_idf}", file=sys.stderr)
        sys.exit(1)
    if not weather.is_file():
        print(f"ERROR: Weather file not found: {weather}", file=sys.stderr)
        sys.exit(1)

    all_results: dict = {
        "energyplus_version": str(config.version),
        "iterations": ITERATIONS,
        "warmup_runs": WARMUP_RUNS,
    }

    # --- Design-day sync ---
    print("\n--- Sync Design-Day Simulations ---")
    dd_sync = run_sync_benchmark(example_idf, weather, config, design_day=True)
    print_comparison("Sync Design-Day (fast, ~0.5s per run)", dd_sync)
    all_results["sync_design_day"] = dd_sync

    # --- Design-day async ---
    print("\n--- Async Design-Day Simulations ---")
    dd_async = asyncio.run(run_async_benchmark(example_idf, weather, config, design_day=True))
    print_comparison("Async Design-Day", dd_async)
    all_results["async_design_day"] = dd_async

    # --- Annual sync ---
    print("\n--- Sync Annual Simulations ---")
    annual_sync = run_sync_benchmark(example_idf, weather, config, annual=True)
    print_comparison("Sync Annual (longer, ~3-10s per run)", annual_sync)
    all_results["sync_annual"] = annual_sync

    # --- Annual async ---
    print("\n--- Async Annual Simulations ---")
    annual_async = asyncio.run(run_async_benchmark(example_idf, weather, config, annual=True))
    print_comparison("Async Annual", annual_async)
    all_results["async_annual"] = annual_async

    # --- Summary ---
    print("\n" + "=" * 72)
    print("  SUMMARY")
    print("=" * 72)

    for section_label, section_key in [
        ("Sync Design-Day", "sync_design_day"),
        ("Async Design-Day", "async_design_day"),
        ("Sync Annual", "sync_annual"),
        ("Async Annual", "async_annual"),
    ]:
        section = all_results.get(section_key, {})
        baseline = section.get("no_callback", {}).get("mean", 0)
        if baseline <= 0:
            continue
        print(f"\n  {section_label} (baseline: {baseline:.3f}s):")
        for name, data in section.items():
            if name == "no_callback":
                continue
            mean = data.get("mean", 0)
            overhead_pct = ((mean - baseline) / baseline) * 100
            print(f"    {name:<22} {mean:.3f}s ({overhead_pct:+.2f}%)")

    # Save raw results (strip non-serializable fields)
    results_path = Path(__file__).parent / "progress_benchmark_results.json"
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nRaw results saved to: {results_path}")


if __name__ == "__main__":
    main()
