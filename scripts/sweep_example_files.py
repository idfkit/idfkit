"""Parse every EnergyPlus example file for one release and report what the parser found.

WHY THIS EXISTS

The unit suite reads a handful of hand-written fixtures and, when an EnergyPlus install happens to
be present, the example files of ONE release. That is not enough. Two classes of defect are only
visible across releases:

  * A file whose content belongs to one version while its `Version` object declares another. The
    schema and the content then disagree, every value after the first added field lands one field
    early, and nothing says so. EnergyPlus ships several: `UnitarySystem_VSCoolingCoil_2.idf` in the
    25.2 release declares `Version, 24.2` and uses a field added in 25.2.
  * A parser change that is safe on the newest schema and wrong on an older one, because field
    lists, extensible groups and sentinel spellings all moved between releases.

Neither is reachable from a single version, which is why this sweeps them all.

WHAT IT CHECKS

Reading is the assertion. A file that raises, or that produces a diagnostic, is reported. The exit
code is governed by `--max-findings`, so a release with a known count does not fail the build while
a regression that adds one does.

The findings this currently surfaces on a clean tree are all true positives: files using the
parametric preprocessor, whose `=$insDepth` really is not a number until that preprocessor has run,
and files with a stale `Version` stamp.

Usage:
    uv run python scripts/sweep_example_files.py <dir> [--max-findings N] [--max-errors N]
"""

from __future__ import annotations

import argparse
import collections
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path

import idfkit


@dataclass(frozen=True, slots=True)
class SweepResult:
    """What reading a directory of example files produced."""

    files: int
    errors: list[str]
    findings: list[str]
    by_code: collections.Counter[str]


def sweep(files: list[Path]) -> SweepResult:
    """Read every file, collecting what would not read and what each read reported."""
    by_code: collections.Counter[str] = collections.Counter()
    findings: list[str] = []
    errors: list[str] = []

    for path in files:
        try:
            result = idfkit.load_idf_with_diagnostics(str(path))
        except Exception as error:  # a file that will not read at all is the louder problem
            errors.append(f"{path.name}: {type(error).__name__}: {error}")
            continue
        for diagnostic in result.diagnostics:
            by_code[diagnostic.code] += 1
            findings.append(f"{path.name}:{diagnostic.line}: [{diagnostic.code}] {diagnostic.message}")

    return SweepResult(files=len(files), errors=errors, findings=findings, by_code=by_code)


def report(result: SweepResult) -> None:
    """Print the counts, then the detail, truncated so a bad run stays readable."""
    print(f"files read      {result.files}")
    print(f"unreadable      {len(result.errors)}")
    print(f"diagnostics     {len(result.findings)}")
    for code, count in sorted(result.by_code.items()):
        print(f"  {code:<20} {count}")

    if result.errors:
        print("\nunreadable files:")
        for line in result.errors[:40]:
            print(f"  {line}")
    if result.findings:
        print("\ndiagnostics:")
        for line in result.findings[:60]:
            print(f"  {line}")
        if len(result.findings) > 60:
            print(f"  ... {len(result.findings)} in total, 60 shown")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="sweep_example_files.py", description=__doc__)
    parser.add_argument("directory", type=Path, help="directory of .idf files to read")
    parser.add_argument(
        "--max-findings",
        type=int,
        default=0,
        help="fail if more than this many diagnostics are reported (default: 0)",
    )
    parser.add_argument(
        "--max-errors",
        type=int,
        default=0,
        help="fail if more than this many files fail to read at all (default: 0)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if not args.directory.is_dir():
        print(f"::error::{args.directory} is not a directory", file=sys.stderr)
        return 2

    files = sorted(args.directory.glob("*.idf"))
    if not files:
        # An empty sweep passes every threshold while proving nothing, which is the one outcome
        # this must never report as success.
        print(f"::error::no .idf files under {args.directory}; the sweep proved nothing", file=sys.stderr)
        return 2

    warnings.filterwarnings("ignore")
    result = sweep(files)
    report(result)

    failed = False
    if len(result.errors) > args.max_errors:
        print(f"\n::error::{len(result.errors)} files failed to read, budget is {args.max_errors}")
        failed = True
    if len(result.findings) > args.max_findings:
        print(f"\n::error::{len(result.findings)} diagnostics, budget is {args.max_findings}")
        failed = True

    if failed:
        return 1
    print("\nPASSED: every example file read, within budget.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
