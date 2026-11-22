"""Generate the EnergyPlus schedule-value fixture that `tests/schedules/test_energyplus_parity.py` reads.

Writes `tests/fixtures/schedules/energyplus/`:

- `model.idf`: EnergyPlus's `1ZoneUncontrolled` example, run on its two design days only, with a set of
  schedules covering every schedule type and interpolation mode idfkit evaluates.
- `hourly.csv`, `half_hourly.csv`: the data the model's Schedule:File objects read.
- `expected.json.gz`: EnergyPlus's `Schedule Value` for every schedule, read from the SQLite output,
  which holds the full double that EnergyPlus computed. One run per timestep in `TIMESTEPS` covers
  both design days; one weather-file run covers `WEATHER_DAYS` of `WEATHER_YEAR`, ordinary days
  across the end of February.

Run it with EnergyPlus installed (found as `idfkit.simulation.find_energyplus` finds it):

    uv run python scripts/generate_schedule_fixture.py

The test then needs no EnergyPlus: it compares idfkit's `values()` with these numbers for equality.
"""

from __future__ import annotations

import gzip
import json
import re
import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path

from idfkit.simulation import find_energyplus
from idfkit.simulation.config import EnergyPlusConfig

FIXTURE_DIR = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "schedules" / "energyplus"
TIMESTEPS = (1, 3, 4, 6, 60)
WEATHER_YEAR = 2023
WEATHER_DAYS = ((2, 27), (3, 2))
WEATHER_TIMESTEP = 4

# Times that fall on no timestep boundary except at 60 per hour, and values that do not sum exactly.
_ODD_TIMES = ("07:10", "12:37", "17:45", "24:00")
_ODD_VALUES = ("0.2", "0.9", "0.35", "0.05")
_FRACTIONS = (("06:00", "0.1"), ("09:30", "0.7"), ("15:20", "0.3"), ("24:00", "1.0"))


def _until(pairs: tuple[tuple[str, str], ...]) -> str:
    return ", ".join(f"Until: {t}, {v}" for t, v in pairs)


def _compact(name: str, body: str) -> str:
    return f"Schedule:Compact, {name}, , Through: 12/31, {body};\n"


def _day_chain(name: str, day: str) -> str:
    """A Schedule:Year -> Schedule:Week:Daily -> ``day`` chain; ``day`` is the IDF text of ``{name}_DAY``."""
    week = ", ".join([f"{name}_DAY"] * 12)
    return f"{day}\nSchedule:Week:Daily, {name}_WEEK, {week};\nSchedule:Year, {name}, , {name}_WEEK, 1, 1, 12, 31;\n"


def _day_interval(name: str, interpolate: str) -> str:
    fields = ", ".join(f"{t}, {v}" for t, v in zip(_ODD_TIMES, _ODD_VALUES, strict=True))
    return _day_chain(name, f"Schedule:Day:Interval, {name}_DAY, , {interpolate}, {fields};")


def _day_list(name: str, interpolate: str, minutes: int) -> str:
    items = ", ".join(str(((i * 37) % 100) / 100) for i in range(1440 // minutes))
    return _day_chain(name, f"Schedule:Day:List, {name}_DAY, , {interpolate}, {minutes}, {items};")


def _file(name: str, csv: str, interpolate: str, minutes: int) -> str:
    return f"Schedule:File, {name}, , {csv}, 1, 0, , Comma, {interpolate}, {minutes};\n"


def schedules() -> str:
    """The IDF text of every schedule the fixture reports."""
    odd = tuple(zip(_ODD_TIMES, _ODD_VALUES, strict=True))
    step = (("08:00", "0"), ("18:00", "1"), ("24:00", "0"))
    per_block = (("12:30", "0.25"), ("24:00", "1"))
    hourly = ", ".join(str(((h * 13) % 24) / 24) for h in range(24))
    return "".join([
        _compact("C_NO_BOUNDARY", f"For: AllDays, {_until(step)}"),
        _compact("C_NO_ODD", f"For: AllDays, {_until(odd)}"),
        _compact("C_AVERAGE_ODD", f"For: AllDays, Interpolate: Average, {_until(odd)}"),
        _compact("C_LINEAR_ODD", f"For: AllDays, Interpolate: Linear, {_until(odd)}"),
        _compact("C_LINEAR_FRACTIONS", f"For: AllDays, Interpolate: Linear, {_until(_FRACTIONS)}"),
        _compact("C_AVERAGE_FRACTIONS", f"For: AllDays, Interpolate: Average, {_until(_FRACTIONS)}"),
        _compact(
            "C_PER_BLOCK",
            f"For: WinterDesignDay, {_until(per_block)}, "
            f"For: SummerDesignDay, Interpolate: Average, {_until(per_block)}, "
            f"For: AllOtherDays, Interpolate: Linear, {_until(per_block)}",
        ),
        _day_interval("DI_NO", "No"),
        _day_interval("DI_AVERAGE", "Average"),
        _day_interval("DI_LINEAR", "Linear"),
        _day_list("DL_NO", "No", 10),
        _day_list("DL_AVERAGE", "Average", 10),
        _day_list("DL_LINEAR", "Linear", 10),
        _day_list("DL_AVERAGE_30", "Average", 30),
        _day_chain("DH", f"Schedule:Day:Hourly, DH_DAY, , {hourly};"),
        _file("F_HOURLY_YES", "hourly.csv", "Yes", 60),
        _file("F_HALF_HOURLY_YES", "half_hourly.csv", "Yes", 30),
        _file("F_HALF_HOURLY_NO", "half_hourly.csv", "No", 30),
        _file("F_HALF_HOURLY_BLANK", "half_hourly.csv", "", 30),
        "Schedule:Constant, CONSTANT, , 0.37;\n",
    ])


def _write_csvs(directory: Path) -> None:
    (directory / "hourly.csv").write_text("".join(f"{((i * 37) % 100) / 100}\n" for i in range(8760)))
    (directory / "half_hourly.csv").write_text("".join(f"{((i * 53) % 100) / 100}\n" for i in range(8760 * 2)))


def _model(example: Path, timestep: int, *, weather: bool = False) -> str:
    """The example model with the fixture's schedules, on its design days or on ``WEATHER_DAYS``."""
    text = example.read_text()
    text = text.replace("  Timestep,4;", f"  Timestep,{timestep};")
    sizing, weather_run = ("No", "Yes") if weather else ("Yes", "No")
    text = text.replace(
        "    Yes,                     !- Run Simulation for Sizing Periods",
        f"    {sizing + ',':<25}!- Run Simulation for Sizing Periods",
    )
    text = text.replace(
        "    Yes,                     !- Run Simulation for Weather File Run Periods",
        f"    {weather_run + ',':<25}!- Run Simulation for Weather File Run Periods",
    )
    if weather:
        (m1, d1), (m2, d2) = WEATHER_DAYS
        y = WEATHER_YEAR
        text = re.sub(
            r"  RunPeriod,.*?;[^\n]*\n",
            f"  RunPeriod, Fixture, {m1}, {d1}, {y}, {m2}, {d2}, {y}, , Yes, Yes, No, Yes, Yes;\n",
            text,
            count=1,
            flags=re.DOTALL,
        )
    return text + "\n" + schedules() + "Output:SQLite, Simple;\nOutput:Variable, *, Schedule Value, Timestep;\n"


def _run(config: EnergyPlusConfig, idf: str, weather: Path) -> dict[str, dict[str, list[float]]]:
    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp)
        (run / "in.idf").write_text(idf)
        for csv in ("hourly.csv", "half_hourly.csv"):
            shutil.copy(FIXTURE_DIR / csv, run / csv)
        subprocess.run(  # noqa: S603
            [str(config.executable), "-r", "-w", str(weather), "-d", str(run), str(run / "in.idf")],
            check=True,
            capture_output=True,
        )
        err = (run / "eplusout.err").read_text()
        if "** Severe  **" in err or "**  Fatal  **" in err:
            raise RuntimeError(err)
        return _read_values(run / "eplusout.sql")


def _read_values(sql: Path) -> dict[str, dict[str, list[float]]]:
    """``{schedule name: {"month/day": [value per timestep]}}`` from EnergyPlus's SQLite output."""
    query = """
        SELECT d.KeyValue, t.Month, t.Day, r.Value
        FROM ReportData r
        JOIN ReportDataDictionary d ON d.ReportDataDictionaryIndex = r.ReportDataDictionaryIndex
        JOIN Time t ON t.TimeIndex = r.TimeIndex
        WHERE d.Name = 'Schedule Value' AND (t.WarmupFlag IS NULL OR t.WarmupFlag = 0)
        ORDER BY r.TimeIndex
    """
    result: dict[str, dict[str, list[float]]] = {}
    with sqlite3.connect(sql) as con:
        for key, month, day, value in con.execute(query):
            result.setdefault(key.upper(), {}).setdefault(f"{month}/{day}", []).append(value)
    return result


def main() -> None:
    config = find_energyplus()
    example = config.install_dir / "ExampleFiles" / "1ZoneUncontrolled.idf"
    weather = config.install_dir / "WeatherData" / "USA_CO_Golden-NREL.724666_TMY3.epw"
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    _write_csvs(FIXTURE_DIR)

    (FIXTURE_DIR / "model.idf").write_text(_model(example, TIMESTEPS[0]))
    runs: list[dict[str, object]] = [
        {"timestep": ts, "design_days": True, "values": _run(config, _model(example, ts), weather)} for ts in TIMESTEPS
    ]
    runs.append({
        "timestep": WEATHER_TIMESTEP,
        "design_days": False,
        "values": _run(config, _model(example, WEATHER_TIMESTEP, weather=True), weather),
    })
    expected = {"energyplus": ".".join(map(str, config.version)), "year": WEATHER_YEAR, "runs": runs}

    with gzip.open(FIXTURE_DIR / "expected.json.gz", "wt") as f:
        json.dump(expected, f, separators=(",", ":"))


if __name__ == "__main__":
    main()
