"""CLI entry point for the version compatibility checker.

Usage examples::

    idfkit check-compat script.py --from 24.2 --to 25.1
    idfkit check-compat script.py --targets 24.2,25.1,25.2
    idfkit check-compat script.py --targets 24.2,25.1,25.2 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..versions import version_string
from ._checker import check_compatibility, resolve_version
from ._models import CompatSeverity, Diagnostic


def _parse_version_spec(spec: str) -> tuple[int, int, int]:
    """Parse a version string like ``"24.2"`` or ``"25.1.0"`` into a tuple."""
    parts = spec.strip().split(".")
    if len(parts) == 2:
        return (int(parts[0]), int(parts[1]), 0)
    if len(parts) == 3:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    msg = f"Invalid version specifier: '{spec}'. Expected MAJOR.MINOR or MAJOR.MINOR.PATCH."
    raise argparse.ArgumentTypeError(msg)


def _build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    top = argparse.ArgumentParser(
        prog="idfkit",
        description="idfkit command-line tools",
    )
    sub = top.add_subparsers(dest="command")

    compat = sub.add_parser(
        "check-compat",
        help="Check Python files for EnergyPlus cross-version compatibility issues",
        description=(
            "Analyse Python source files that use idfkit and report "
            "object types or enumerated choice values that differ between "
            "EnergyPlus schema versions."
        ),
    )
    compat.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="Python file(s) to check",
    )

    version_group = compat.add_mutually_exclusive_group(required=True)
    version_group.add_argument(
        "--from",
        dest="from_version",
        type=_parse_version_spec,
        help="Source EnergyPlus version (e.g. 24.2)",
    )
    compat.add_argument(
        "--to",
        dest="to_version",
        type=_parse_version_spec,
        help="Target EnergyPlus version (required with --from)",
    )
    version_group.add_argument(
        "--targets",
        type=str,
        help="Comma-separated list of target versions (e.g. 24.2,25.1,25.2)",
    )

    compat.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output diagnostics as JSON",
    )

    return top


def _resolve_targets(args: argparse.Namespace) -> list[tuple[int, int, int]]:
    """Resolve the user-specified versions to actual bundled schema versions."""
    raw_versions: list[tuple[int, int, int]] = []

    if args.targets is not None:
        for part in args.targets.split(","):
            raw_versions.append(_parse_version_spec(part))
    else:
        if args.from_version is None or args.to_version is None:
            print("error: --from and --to must both be specified", file=sys.stderr)
            sys.exit(2)
        raw_versions.append(args.from_version)
        raw_versions.append(args.to_version)

    resolved: list[tuple[int, int, int]] = []
    for v in raw_versions:
        try:
            resolved.append(resolve_version(v))
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(2)

    # Deduplicate while preserving order
    seen: set[tuple[int, int, int]] = set()
    unique: list[tuple[int, int, int]] = []
    for v in resolved:
        if v not in seen:
            seen.add(v)
            unique.append(v)

    if len(unique) < 2:
        print("error: at least two distinct target versions are required", file=sys.stderr)
        sys.exit(2)

    return sorted(unique)


def _format_text(diagnostics: list[Diagnostic]) -> str:
    """Format diagnostics as human-readable text."""
    if not diagnostics:
        return "No compatibility issues found."
    lines: list[str] = []
    for d in diagnostics:
        lines.append(str(d))
    return "\n".join(lines)


def _format_json(diagnostics: list[Diagnostic], targets: list[tuple[int, int, int]]) -> str:
    """Format diagnostics as a JSON string."""
    error_count = sum(1 for d in diagnostics if d.severity == CompatSeverity.ERROR)
    warning_count = sum(1 for d in diagnostics if d.severity == CompatSeverity.WARNING)
    payload = {
        "targets": [version_string(v) for v in targets],
        "diagnostics": [d.to_dict() for d in diagnostics],
        "summary": {
            "total": len(diagnostics),
            "errors": error_count,
            "warnings": warning_count,
        },
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(2)

    if args.command == "check-compat":
        _run_check_compat(args)


def _run_check_compat(args: argparse.Namespace) -> None:
    """Execute the ``check-compat`` subcommand."""
    targets = _resolve_targets(args)
    all_diagnostics: list[Diagnostic] = []

    for filepath_str in args.files:
        filepath = Path(filepath_str)
        if not filepath.is_file():
            print(f"error: file not found: {filepath}", file=sys.stderr)
            sys.exit(2)

        source = filepath.read_text(encoding="utf-8")
        diagnostics = check_compatibility(source, str(filepath), targets)
        all_diagnostics.extend(diagnostics)

    if args.json_output:
        print(_format_json(all_diagnostics, targets))
    else:
        print(_format_text(all_diagnostics))

    # Exit code: 1 if any issues, 0 otherwise
    sys.exit(1 if all_diagnostics else 0)
