"""Build the committed fixtures that result linking is tested against.

WHY THIS EXISTS

Result linking joins what EnergyPlus reports (sizing rows, messages, zone multipliers, tabular
rows, the keys of reported variables) back to the objects of the model that produced it. Testing
that needs real runs, and the default test suite must never need EnergyPlus (FR-044). So the runs
are made once, here, on a machine that has EnergyPlus, and their outputs are committed as
`(IDF, SQL, ERR)` triples under `tests/fixtures/simulation/linked/`.

WHAT IT DOES

For each reference model from the installation's `ExampleFiles`:

  1. Adds `Output:SQLite` (SimpleAndTabular), `Output:Table:SummaryReports` (AllSummary) and a
     small set of `Output:Variable` objects with `*` keys, replacing any existing SQLite and
     summary-report objects.
  2. Runs EnergyPlus with the model's own `SimulationControl` and run periods.
  3. Trims the SQL to the tables linking reads (never `ReportData`, `Time` or the other bulky
     tables) and `VACUUM`s it.
  4. Copies the IDF as simulated (with the added outputs), the trimmed SQL and the ERR file to the
     output directory as `<model>.idf`, `<model>.sql` and `<model>.err`.

Optional models (HospitalLowEnergy) are kept only while the directory stays within budget. The
script exits non-zero when any required model fails or when the directory exceeds the budget
(10 MB by default).

EnergyPlus is located with `idfkit.simulation.find_energyplus`, which reads `ENERGYPLUS_DIR`
before searching `PATH` and the platform's default install directories.

Usage:
    ENERGYPLUS_DIR=/usr/local/EnergyPlus-26-2-0 uv run python scripts/build_linking_fixtures.py
    uv run python scripts/build_linking_fixtures.py --energyplus /path/to/EnergyPlus --models 5ZoneAirCooled
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from idfkit import load_idf
from idfkit.document import IDFDocument
from idfkit.exceptions import EnergyPlusNotFoundError
from idfkit.simulation import EnergyPlusConfig, find_energyplus, simulate
from idfkit.writers import save_idf

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = REPO_ROOT / "tests" / "fixtures" / "simulation" / "linked"
DEFAULT_VERSION = "26.2"
DEFAULT_WEATHER = "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"
BUDGET_BYTES = 10 * 1024 * 1024

# About ten reference models, chosen for what linking must resolve: single zones, zone multipliers
# (MultiStory), HVAC templates, air loops, plant loops, water-loop heat pumps and DOAS.
REQUIRED_MODELS: tuple[str, ...] = (
    "1ZoneUncontrolled",
    "1ZoneEvapCooler",
    "5ZoneAirCooled",
    "5ZoneAutoDXVAV",
    "5ZoneWaterLoopHeatPump",
    "MultiStory",
    "HVACTemplate-5ZoneVAVWaterCooled",
    "PlantLoopChainCooling",
    "ShopWithSimplePVT",
    "DOASDualDuctSchool",
)
# Kept only while the output directory stays within budget.
OPTIONAL_MODELS: tuple[str, ...] = ("HospitalLowEnergy",)

# A small set of variables reported for every key, so the dictionary carries zone, surface, node,
# fan and coil keys for linking to resolve.
OUTPUT_VARIABLES: tuple[str, ...] = (
    "Zone Mean Air Temperature",
    "Zone Air System Sensible Heating Energy",
    "Zone Air System Sensible Cooling Energy",
    "Surface Inside Face Temperature",
    "System Node Temperature",
    "Fan Electricity Energy",
    "Heating Coil Heating Energy",
    "Cooling Coil Total Cooling Energy",
)
REPORTING_FREQUENCY = "Hourly"

# Tables linking reads, plus what they reference. Everything else is dropped.
KEEP_TABLES: frozenset[str] = frozenset({
    "Simulations",
    "EnvironmentPeriods",
    "Errors",
    "Zones",
    "ZoneLists",
    "ZoneGroups",
    "ZoneInfoZoneLists",
    "ZoneSizes",
    "SystemSizes",
    "ComponentSizes",
    "ReportDataDictionary",
    "TabularData",
    "Strings",
    "StringTypes",
})
KEEP_VIEWS: frozenset[str] = frozenset({"TabularDataWithStrings"})


@dataclass(frozen=True, slots=True)
class FixtureResult:
    """What building one model's triple produced."""

    model: str
    ok: bool
    detail: str
    size_bytes: int = 0


def prepare_model(doc: IDFDocument) -> None:
    """Add the outputs linking reads, replacing any SQLite or summary-report object already present."""
    for obj_type in ("Output:SQLite", "Output:Table:SummaryReports"):
        if obj_type in doc:
            for obj in list(doc[obj_type]):
                doc.removeidfobject(obj)
    doc.add("Output:SQLite", "", option_type="SimpleAndTabular", validate=False)
    doc.add("Output:Table:SummaryReports", "", reports=[{"report_name": "AllSummary"}], validate=False)
    for variable in OUTPUT_VARIABLES:
        doc.add(
            "Output:Variable",
            "",
            key_value="*",
            variable_name=variable,
            reporting_frequency=REPORTING_FREQUENCY,
            validate=False,
        )


def trim_sql(path: Path) -> None:
    """Drop every table and view linking does not read, then VACUUM the file in place."""
    conn = sqlite3.connect(path)
    try:
        rows: list[tuple[str, str]] = conn.execute(
            "SELECT type, name FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        for kind, name in rows:
            if kind == "view" and name not in KEEP_VIEWS:
                conn.execute(f'DROP VIEW IF EXISTS "{name}"')
        for kind, name in rows:
            if kind == "table" and name not in KEEP_TABLES:
                conn.execute(f'DROP TABLE IF EXISTS "{name}"')
        conn.commit()
        conn.execute("VACUUM")
    finally:
        conn.close()


def directory_size(path: Path) -> int:
    """Total size in bytes of every file under *path*."""
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def build_one(model: str, config: EnergyPlusConfig, weather: Path, output_dir: Path, timeout: float) -> FixtureResult:
    """Simulate one example model and write its trimmed triple to *output_dir*."""
    source = config.install_dir / "ExampleFiles" / f"{model}.idf"
    if not source.is_file():
        return FixtureResult(model, ok=False, detail=f"example file not found: {source}")

    doc = load_idf(str(source))
    prepare_model(doc)

    with tempfile.TemporaryDirectory(prefix=f"linked_{model}_") as tmp:
        run_dir = Path(tmp) / "run"
        result = simulate(doc, weather, output_dir=run_dir, energyplus=config, timeout=timeout)
        sql_path = result.sql_path
        err_path = result.err_path
        if not result.success or sql_path is None or err_path is None:
            return FixtureResult(model, ok=False, detail=f"simulation failed (exit code {result.exit_code})")

        idf_out = output_dir / f"{model}.idf"
        sql_out = output_dir / f"{model}.sql"
        err_out = output_dir / f"{model}.err"
        save_idf(doc, idf_out)
        shutil.copyfile(sql_path, sql_out)
        shutil.copyfile(err_path, err_out)

    trim_sql(sql_out)
    size = sum(p.stat().st_size for p in (idf_out, sql_out, err_out))
    return FixtureResult(model, ok=True, detail="ok", size_bytes=size)


def remove_triple(model: str, output_dir: Path) -> None:
    """Delete a model's triple, used when an optional model does not fit the budget."""
    for suffix in (".idf", ".sql", ".err"):
        (output_dir / f"{model}{suffix}").unlink(missing_ok=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the command line."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0] if __doc__ else None)
    parser.add_argument(
        "--energyplus",
        type=Path,
        default=None,
        help="EnergyPlus install directory (default: ENERGYPLUS_DIR, then PATH, then platform defaults)",
    )
    parser.add_argument(
        "--version",
        default=DEFAULT_VERSION,
        help=f"EnergyPlus version the fixtures must come from (default: {DEFAULT_VERSION})",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="where the triples are written")
    parser.add_argument(
        "--weather",
        type=Path,
        default=None,
        help=f"weather file (default: {DEFAULT_WEATHER} from the installation's WeatherData)",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=None,
        help="required models to build, by example-file stem (default: the built-in list of ten)",
    )
    parser.add_argument("--no-optional", action="store_true", help="skip the optional models (HospitalLowEnergy)")
    parser.add_argument(
        "--budget-mb", type=float, default=BUDGET_BYTES / (1024 * 1024), help="size budget for the output directory"
    )
    parser.add_argument("--timeout", type=float, default=3600.0, help="per-run EnergyPlus timeout in seconds")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Build every triple, then enforce the size budget."""
    args = parse_args(argv)
    budget = int(float(args.budget_mb) * 1024 * 1024)
    energyplus_path: Path | None = args.energyplus
    try:
        config = find_energyplus(version=str(args.version), path=energyplus_path)
    except EnergyPlusNotFoundError as error:
        print(f"EnergyPlus {args.version} not found: {error}", file=sys.stderr)
        return 2
    weather: Path = args.weather or (config.install_dir / "WeatherData" / DEFAULT_WEATHER)
    if not weather.is_file():
        print(f"weather file not found: {weather}", file=sys.stderr)
        return 2

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    required: list[str] = list(args.models) if args.models else list(REQUIRED_MODELS)
    optional: list[str] = [] if args.no_optional else [m for m in OPTIONAL_MODELS if m not in required]
    print(f"EnergyPlus {'.'.join(map(str, config.version))} at {config.install_dir}")
    print(f"writing to {output_dir}")

    failures: list[FixtureResult] = []
    for model in required:
        result = build_one(model, config, weather, output_dir, float(args.timeout))
        print(f"  {model:<36} {result.detail}  {result.size_bytes / 1024:.0f} KB")
        if not result.ok:
            failures.append(result)

    for model in optional:
        result = build_one(model, config, weather, output_dir, float(args.timeout))
        if not result.ok:
            print(f"  {model:<36} skipped (optional): {result.detail}")
            continue
        if directory_size(output_dir) > budget:
            remove_triple(model, output_dir)
            print(f"  {model:<36} skipped (optional): {result.size_bytes / 1024:.0f} KB does not fit the budget")
            continue
        print(f"  {model:<36} {result.detail}  {result.size_bytes / 1024:.0f} KB")

    total = directory_size(output_dir)
    print(f"total {total / (1024 * 1024):.2f} MB of {budget / (1024 * 1024):.2f} MB")
    if failures:
        print(f"{len(failures)} required model(s) failed: {', '.join(f.model for f in failures)}", file=sys.stderr)
        return 1
    if total > budget:
        print(f"{output_dir} exceeds the {budget / (1024 * 1024):.2f} MB budget", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
