"""Measure the connection checks on earlier EnergyPlus versions and write ``_version_caps.py`` (R-34).

WHY

The checks are qualified on the 26.2 example files: a check becomes an error only when it reports
nothing on any of them. Most models an agent receives are older, and field layouts change between
versions. So the example files of earlier versions are measured too, and a qualified check that
reports anything on a version's example files, which all run, is capped at warning for models of
that version. Example files are known to simulate, so every such finding counts as false.

The measurement needs the earlier versions' ``ExampleFiles`` directories, never EnergyPlus itself.

Usage::

    python -m idfkit.codegen.generate_version_caps --corpus 9.6.0=/usr/local/EnergyPlus-9-6-0/ExampleFiles \\
        --corpus 23.2.0=/usr/local/EnergyPlus-23-2-0/ExampleFiles
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

_OUTPUT_PATH: Final = Path(__file__).resolve().parents[1] / "hvac" / "_version_caps.py"


@dataclass
class Measurement:
    """What the checks reported on one version's example files."""

    version: tuple[int, int, int]
    models: int = 0
    unreadable: list[str] = field(default_factory=lambda: list[str]())
    findings: Counter[tuple[str, str]] = field(default_factory=lambda: Counter[tuple[str, str]]())
    """``(code, severity) -> count``, severities before any version cap."""
    models_with: Counter[str] = field(default_factory=lambda: Counter[str]())
    examples: dict[str, list[str]] = field(default_factory=lambda: dict[str, list[str]]())


def _check_one(path: str) -> tuple[str, list[tuple[str, str, str]] | None]:
    from idfkit import load_idf
    from idfkit.hvac import HVACTopology

    try:
        doc = load_idf(path)
    except Exception:
        return path, None
    found = [(f.capped_from or f.severity, f.code, f.message) for f in HVACTopology.from_document(doc).check()]
    return path, [(code, severity, message) for severity, code, message in found]


def measure(example_dir: Path, version: tuple[int, int, int], *, jobs: int = 4) -> Measurement:
    """Run every check on every ``*.idf`` under *example_dir*."""
    result = Measurement(version)
    files = sorted(str(p) for p in example_dir.glob("*.idf"))
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        for path, found in pool.map(_check_one, files, chunksize=8):
            if found is None:
                result.unreadable.append(Path(path).name)
                continue
            result.models += 1
            for code in {c for c, _, _ in found}:
                result.models_with[code] += 1
            for code, severity, message in found:
                result.findings[(code, severity)] += 1
                result.examples.setdefault(code, [])
                if len(result.examples[code]) < 3:
                    result.examples[code].append(f"{Path(path).name}: {message}")
    return result


def render(measurements: list[Measurement]) -> str:
    """The ``_version_caps.py`` source: one warning cap per qualified check that reported anything."""
    from idfkit.hvac.checks import QUALIFIED

    rows: list[str] = []
    for m in sorted(measurements, key=lambda m: m.version):
        for code in sorted(QUALIFIED):
            false = sum(n for (c, _), n in m.findings.items() if c == code)
            if false:
                rows.append(f'    VersionCap("{code}", {m.version!r}, "warning", {m.models}, {false}),\n')
    versions = ", ".join(repr(m.version) for m in sorted(measurements, key=lambda m: m.version))
    body = "".join(rows)
    return f'''"""Auto-generated per-version severity caps for the connection checks (research R-34).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_version_caps --corpus VERSION=PATH [--corpus VERSION=PATH ...]

Each row caps one check for models of one measured EnergyPlus version, from a corpus measurement of
that version's example files. A model takes the row of the nearest measured version at or below its
own; a model older than the oldest measured version takes the oldest; 26.2 is never capped.
"""

from __future__ import annotations

from typing import Final

from idfkit.hvac._rule_types import VersionCap

MEASURED_VERSIONS: Final[tuple[tuple[int, int, int], ...]] = ({versions}{"," if len(measurements) == 1 else ""})
"""The versions whose example files were measured, oldest first."""

VERSION_CAPS: Final[tuple[VersionCap, ...]] = (
{body})
'''


def _parse_version(text: str) -> tuple[int, int, int]:
    parts = [int(p) for p in text.split(".")]
    return (parts[0], parts[1], parts[2] if len(parts) > 2 else 0)


def main(argv: list[str] | None = None) -> int:
    """Measure each ``--corpus`` and write the table."""
    import subprocess
    import sys

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--corpus", action="append", required=True, metavar="VERSION=PATH")
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args(argv)
    measurements: list[Measurement] = []
    for spec in args.corpus:
        version_text, _, path = spec.partition("=")
        m = measure(Path(path), _parse_version(version_text), jobs=args.jobs)
        measurements.append(m)
        print(f"{version_text}: {m.models} models, {len(m.unreadable)} unreadable")
        for (code, severity), n in sorted(m.findings.items()):
            print(f"  {code} {severity}: {n} finding(s) on {m.models_with[code]} model(s)")
    _OUTPUT_PATH.write_text(render(measurements), encoding="utf-8")
    subprocess.run([sys.executable, "-m", "ruff", "format", "--quiet", str(_OUTPUT_PATH)], check=True)  # noqa: S603
    print(f"Wrote {_OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
