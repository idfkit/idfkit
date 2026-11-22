"""idfkit's schedule values must equal EnergyPlus's, bit for bit.

`tests/fixtures/schedules/energyplus/expected.json.gz` holds the `Schedule Value` EnergyPlus reported for
every schedule in `model.idf`: on both design days at several timesteps per hour, and on ordinary days
of a weather-file run across the end of February. It was read from EnergyPlus's SQLite output, which
keeps the full double. Regenerate it with `scripts/generate_schedule_fixture.py`; this test needs no
EnergyPlus.
"""

from __future__ import annotations

import gzip
import json
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from idfkit import load_idf
from idfkit.objects import IDFObject
from idfkit.schedules.evaluate import values

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "schedules" / "energyplus"
DESIGN_DAYS = {"12/21": "winter", "7/21": "summer"}
SCHEDULE_TYPES = ("Schedule:Compact", "Schedule:Year", "Schedule:File", "Schedule:Constant")


@cache
def _expected() -> dict[str, Any]:
    with gzip.open(FIXTURE / "expected.json.gz", "rt") as f:
        data: dict[str, Any] = json.load(f)
    return data


@cache
def _schedules() -> dict[str, IDFObject]:
    doc = load_idf(FIXTURE / "model.idf")
    return {obj.name.upper(): obj for kind in SCHEDULE_TYPES for obj in doc.get_collection(kind)}


def _label(run: dict[str, Any]) -> str:
    return f"ts{run['timestep']}" if run["design_days"] else f"weather-ts{run['timestep']}"


CASES = [(i, name) for i, run in enumerate(_expected()["runs"]) for name in sorted(run["values"])]


@pytest.mark.parametrize(("run_index", "name"), CASES, ids=[f"{n}-{_label(_expected()['runs'][i])}" for i, n in CASES])
def test_values_equal_energyplus(run_index: int, name: str) -> None:
    run = _expected()["runs"][run_index]
    for day, want in run["values"][name].items():
        month, dom = (int(p) for p in day.split("/"))
        got = values(
            _schedules()[name],
            year=_expected()["year"],
            timestep=run["timestep"],
            start_date=(month, dom),
            end_date=(month, dom),
            day_type=DESIGN_DAYS[day] if run["design_days"] else None,
            base_path=FIXTURE,
        )
        mismatches = [(i, g, w) for i, (g, w) in enumerate(zip(got, want, strict=True)) if g != w]
        assert not mismatches, (
            f"{day}: {len(mismatches)} of {len(want)} differ, first (index, idfkit, EnergyPlus): {mismatches[:3]}"
        )
