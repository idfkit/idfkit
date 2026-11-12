"""Benchmark result linking on the largest paired fixture (research R-21, task T084).

Prints the figures the performance contract budgets: ``ResultIndex.build`` (at most 50 ms, never
reading ``ReportData``) and ``ResultIndex.for_object`` (at most 10 ms) on
``tests/fixtures/simulation/linked/DOASDualDuctSchool``, the largest committed ``(IDF, SQL)`` pair.
The HVAC topology is built first, as it is after any topology question; the SQLite file is opened
first, as it is once a run's results have been read. Needs no EnergyPlus installation.

Usage::

    uv run python benchmarks/bench_result_index.py
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from itertools import count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmarks._timing import best_of
from idfkit import load_idf
from idfkit.hvac import HVACTopology
from idfkit.simulation import ObjectKey, ResultIndex, SimulationResult

LINKED = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "simulation" / "linked"
FIXTURE = "DOASDualDuctSchool"


def linked_run(fixture: str = FIXTURE) -> tuple[Path, SimulationResult]:
    """The fixture's IDF path and a run whose directory holds its SQLite output."""
    run_dir = Path(tempfile.mkdtemp(prefix=f"bench_{fixture}_"))
    shutil.copy(LINKED / f"{fixture}.sql", run_dir / "eplusout.sql")
    result = SimulationResult(run_dir=run_dir, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0)
    return LINKED / f"{fixture}.idf", result


def main() -> None:
    """Time each operation as the best of several runs and print a Markdown table."""
    idf, result = linked_run()
    doc = load_idf(str(idf))
    HVACTopology.from_document(doc)
    if result.sql is None:
        msg = f"no SQLite output in {result.run_dir}"
        raise RuntimeError(msg)
    runs = count()

    def build() -> ResultIndex:
        # A new hash each time defeats the per-run cache, so every call links from scratch.
        return ResultIndex.build(doc, result, run_revision=doc.revision, run_model_hash=str(next(runs)))

    index = build()
    zone = ObjectKey("Zone", "Offices")
    coil = next(iter(doc["Coil:Cooling:Water"]))
    rows = [
        (f"ResultIndex.build ({FIXTURE})", f"{best_of(build, 5) * 1000:.1f} ms"),
        ("for_object(Zone Offices)", f"{best_of(lambda: index.for_object(zone), 5) * 1000:.2f} ms"),
        (
            f"for_object(Coil:Cooling:Water {coil.name})",
            f"{best_of(lambda: index.for_object(ObjectKey(coil.obj_type, coil.name)), 5) * 1000:.2f} ms",
        ),
    ]
    coverage = index.coverage
    print(f"resolved {coverage.resolved}, unresolved {coverage.unresolved}\n")
    print("| Operation | Best of 5 |")
    print("|---|---|")
    for label, figure in rows:
        print(f"| {label} | {figure} |")


if __name__ == "__main__":
    main()
