#!/usr/bin/env python
"""Generate the real ESO/MTR test fixtures by running EnergyPlus.

The committed ``sample.eso`` / ``sample.mtr`` / ``sample.sql`` fixtures are
**genuine EnergyPlus output** — never hand-authored. This helper reproduces
them so they can be regenerated (e.g. for a new EnergyPlus version).

It loads the bundled ``1ZoneUncontrolled.idf`` example (which conveniently
reports a mix of hourly, daily, and monthly variables plus meters), shortens
the run period to two days so the output stays small, adds ``Output:SQLite``
as a correctness oracle, runs EnergyPlus, and copies the outputs here. It also
writes a truncated copy used to exercise the parser's error handling.

Usage:
    uv run python tests/fixtures/simulation/generate_eso_fixtures.py
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import idfkit
from idfkit.simulation import find_energyplus
from idfkit.writers import write_idf

_HERE = Path(__file__).parent
_EXAMPLE = "1ZoneUncontrolled.idf"


def main() -> None:
    config = find_energyplus()
    example = config.install_dir / "ExampleFiles" / _EXAMPLE
    weather = next((config.install_dir / "WeatherData").glob("USA_CO_Golden*.epw"))

    # Load the example and trim it to a short, small run while keeping the
    # variety of reporting frequencies and meters intact.
    doc = idfkit.load_idf(str(example))
    run_period = doc["RunPeriod"][0]
    run_period.begin_month = 1
    run_period.begin_day_of_month = 1
    run_period.end_month = 1
    run_period.end_day_of_month = 2
    doc.add("Output:SQLite", option_type="SimpleAndTabular")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        idf_path = tmp_path / "in.idf"
        write_idf(doc, idf_path)
        out_dir = tmp_path / "out"
        subprocess.run(  # noqa: S603
            [str(config.executable), "-w", str(weather), "-d", str(out_dir), "-r", str(idf_path)],
            check=True,
            capture_output=True,
        )
        for ext in (".eso", ".mtr", ".sql"):
            shutil.copyfile(out_dir / f"eplusout{ext}", _HERE / f"sample{ext}")

    # A truncated copy for error-handling tests: keep the full dictionary plus
    # the first half of the data section, cut mid-record with no trailing
    # "End of Data" terminator. The cut point is the midpoint between the end of
    # the dictionary and EOF, biased a few bytes to land inside a line.
    full = (_HERE / "sample.eso").read_bytes()
    dict_end = full.find(b"End of Data Dictionary")
    data_start = full.find(b"\n", dict_end) + 1
    cut = (data_start + len(full)) // 2 + 3
    (_HERE / "sample_truncated.eso").write_bytes(full[:cut])

    print(f"Wrote fixtures to {_HERE} from {config.install_dir.name}")


if __name__ == "__main__":
    main()
