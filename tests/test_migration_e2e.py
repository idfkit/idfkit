"""End-to-end migration tests against a real EnergyPlus installation.

Skipped when no EnergyPlus install is available or when the installed
version does not ship the ``IDFVersionUpdater`` directory.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import load_idf, new_document
from idfkit.exceptions import EnergyPlusNotFoundError
from idfkit.migration import migrate
from idfkit.simulation import find_energyplus
from idfkit.simulation.config import EnergyPlusConfig

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def energyplus() -> EnergyPlusConfig:
    try:
        return find_energyplus()
    except EnergyPlusNotFoundError:
        pytest.skip("EnergyPlus not installed")
        raise  # unreachable


@pytest.fixture(scope="module")
def updater_dir(energyplus: EnergyPlusConfig) -> Path:
    d = energyplus.version_updater_dir
    if d is None:
        pytest.skip("IDFVersionUpdater directory not present in EP install")
    return d


def _find_example_idf(energyplus: EnergyPlusConfig) -> Path:
    candidate = energyplus.install_dir / "ExampleFiles" / "1ZoneUncontrolled.idf"
    if not candidate.is_file():
        pytest.skip(f"Example IDF not found at {candidate}")
    return candidate


def test_noop_migration_returns_success(energyplus: EnergyPlusConfig) -> None:
    example = _find_example_idf(energyplus)
    model = load_idf(str(example))
    report = migrate(model, target_version=model.version, energyplus=energyplus)
    assert report.success is True
    assert report.steps == ()
    assert report.migrated_model.version == model.version


def test_migrate_pinned_fixture_to_installed_version(
    energyplus: EnergyPlusConfig,
    updater_dir: Path,
) -> None:
    """Migrate a 1-zone example from the installed EP version back to itself.

    We use the installed version's own example file; this ensures the source
    version is always supported by the installed ``IDFVersionUpdater``
    binaries regardless of what version is installed. If the installed
    version is the first in the registry, the chain is empty (no-op).
    """
    example = _find_example_idf(energyplus)
    model = load_idf(str(example))

    # Migrate to the same version (trivially successful). Exercises the full
    # code path through chain planning, migrator resolution, and result
    # construction without requiring an older fixture IDF to be staged.
    report = migrate(model, target_version=energyplus.version, energyplus=energyplus)
    assert report.success
    assert report.target_version == energyplus.version


def test_migration_renames_output_variables(energyplus: EnergyPlusConfig, updater_dir: Path) -> None:
    """The ``Report Variables`` rename tables must reach the transition binary's CWD."""
    if not (updater_dir / "Report Variables 9-3-0 to 9-4-0.csv").is_file():
        pytest.skip("9.3 -> 9.4 transition files not shipped with this EnergyPlus")
    doc = new_document(version=(9, 3, 0))
    doc.add(
        "Output:Variable",
        key_value="*",
        variable_name="Other Equipment FuelOil#1 Rate",
        reporting_frequency="Hourly",
    )
    report = migrate(doc, target_version=(9, 4, 0), energyplus=energyplus, cache=False)
    assert report.success
    assert report.migrated_model is not None
    names = [o.variable_name for o in report.migrated_model["Output:Variable"]]
    assert names == ["Other Equipment FuelOilNo1 Rate"]
    assert "not found" not in (report.steps[0].stdout or "")
