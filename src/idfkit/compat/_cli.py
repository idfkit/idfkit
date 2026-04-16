"""CLI entry points for idfkit.

Subcommands:

- ``idfkit check`` — statically lint Python source files that use idfkit and
  report object types or enumerated choice values that differ between
  EnergyPlus schema versions.
- ``idfkit migrate`` — forward-migrate an IDF model to a newer EnergyPlus
  version via the installed ``IDFVersionUpdater`` transition binaries.

Usage examples::

    idfkit check script.py --from 24.2 --to 25.1
    idfkit check script.py --targets 24.2,25.1,25.2 --json
    idfkit migrate old.idf --to 25.2
    idfkit migrate old.idf --output new.idf --to 25.2 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING

from ..exceptions import EnergyPlusNotFoundError, MigrationError, UnsupportedVersionError
from ..migration import MigrationProgress, MigrationReport, migrate
from ..versions import ENERGYPLUS_VERSIONS, LATEST_VERSION, version_string
from ._checker import check_compatibility, resolve_version
from ._models import DIAGNOSTIC_CODES, CompatSeverity, Diagnostic
from ._sarif import format_sarif

if TYPE_CHECKING:
    from ..document import IDFDocument
    from ..simulation.config import EnergyPlusConfig


def _parse_version_spec(spec: str) -> tuple[int, int, int]:
    """Parse a version string like ``"24.2"`` or ``"25.1.0"`` into a tuple."""
    parts = spec.strip().split(".")
    if len(parts) not in {2, 3}:
        msg = f"Invalid version specifier: '{spec}'. Expected MAJOR.MINOR or MAJOR.MINOR.PATCH."
        raise argparse.ArgumentTypeError(msg)

    if any(part == "" for part in parts):
        msg = f"Invalid version specifier: '{spec}'. Expected MAJOR.MINOR or MAJOR.MINOR.PATCH."
        raise argparse.ArgumentTypeError(msg)

    try:
        values = tuple(int(part) for part in parts)
    except ValueError as exc:
        msg = f"Invalid version specifier: '{spec}'. Expected MAJOR.MINOR or MAJOR.MINOR.PATCH."
        raise argparse.ArgumentTypeError(msg) from exc

    if len(values) == 2:
        major, minor = values
        matching_minor = [v for v in ENERGYPLUS_VERSIONS if v[0] == major and v[1] == minor]
        if matching_minor:
            return max(matching_minor, key=lambda v: v[2])
        return (major, minor, 0)

    if len(values) == 3:
        major, minor, patch = values
        return (major, minor, patch)

    msg = f"Invalid version specifier: '{spec}'. Expected MAJOR.MINOR or MAJOR.MINOR.PATCH."
    raise argparse.ArgumentTypeError(msg)


def _build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    top = argparse.ArgumentParser(
        prog="idfkit",
        description="idfkit command-line tools",
    )
    sub = top.add_subparsers(dest="command")

    check = sub.add_parser(
        "check",
        help="Lint Python files for EnergyPlus cross-version compatibility issues",
        description=(
            "Statically lint Python source files that use idfkit and report "
            "object types or enumerated choice values that differ between "
            "EnergyPlus schema versions."
        ),
    )
    check.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="Python file(s) to lint",
    )

    # ---- version selection (required, mutually exclusive) ----
    version_group = check.add_mutually_exclusive_group(required=True)
    version_group.add_argument(
        "--from",
        dest="from_version",
        type=_parse_version_spec,
        help="Source EnergyPlus version (e.g. 24.2)",
    )
    check.add_argument(
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

    # ---- output format (mutually exclusive) ----
    output_group = check.add_mutually_exclusive_group()
    output_group.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output lint diagnostics as JSON",
    )
    output_group.add_argument(
        "--sarif",
        dest="sarif_output",
        action="store_true",
        default=False,
        help="Output lint diagnostics as SARIF 2.1.0 (for GitHub Code Scanning, VS Code, etc.)",
    )

    # ---- rule selection ----
    check.add_argument(
        "--select",
        type=str,
        default=None,
        metavar="CODES",
        help="Comma-separated list of lint rule codes to enable (e.g. C001,C002). Only matching rules are reported.",
    )
    check.add_argument(
        "--ignore",
        type=str,
        default=None,
        metavar="CODES",
        help="Comma-separated list of lint rule codes to suppress (e.g. C002).",
    )

    # ---- group filtering ----
    check.add_argument(
        "--group",
        type=str,
        default=None,
        metavar="GROUPS",
        help=(
            "Comma-separated IDD group names. Only object types belonging to "
            "these groups are linted (e.g. 'Thermal Zones and Surfaces,Surface Construction Elements')."
        ),
    )
    check.add_argument(
        "--exclude-group",
        type=str,
        default=None,
        metavar="GROUPS",
        help="Comma-separated IDD group names to exclude from linting.",
    )

    # ---- severity filter ----
    check.add_argument(
        "--severity",
        type=str,
        choices=["warning", "error"],
        default=None,
        metavar="LEVEL",
        help="Minimum severity level to report (warning or error). Default: report all.",
    )

    migrate_cmd = sub.add_parser(
        "migrate",
        help="Forward-migrate an IDF model to a newer EnergyPlus version",
        description=(
            "Forward-migrate an IDF model through EnergyPlus IDFVersionUpdater "
            "transition binaries. Requires a local EnergyPlus installation."
        ),
    )
    migrate_cmd.add_argument(
        "input",
        metavar="INPUT",
        help="Path to the source IDF file",
    )
    migrate_cmd.add_argument(
        "-o",
        "--output",
        dest="output",
        default=None,
        metavar="OUTPUT",
        help="Output IDF path. Defaults to '<input_stem>-v<target>.idf' next to the input.",
    )
    migrate_cmd.add_argument(
        "--to",
        dest="to_version",
        type=_parse_version_spec,
        default=None,
        metavar="VERSION",
        help=f"Target EnergyPlus version (e.g. 25.2). Defaults to the latest supported ({version_string(LATEST_VERSION)}).",
    )
    migrate_cmd.add_argument(
        "--energyplus",
        dest="energyplus_path",
        default=None,
        metavar="PATH",
        help=(
            "Path to the EnergyPlus installation directory or executable. "
            "When omitted, idfkit auto-discovers via $ENERGYPLUS_DIR, PATH, and platform defaults."
        ),
    )
    migrate_cmd.add_argument(
        "--work-dir",
        dest="work_dir",
        default=None,
        metavar="DIR",
        help="Directory in which to stage per-step transition output. Defaults to a temporary directory.",
    )
    migrate_cmd.add_argument(
        "--keep-work-dir",
        dest="keep_work_dir",
        action="store_true",
        default=False,
        help="Preserve intermediate files for inspection (only meaningful for the default temp directory).",
    )
    migrate_cmd.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Emit a JSON report on stdout instead of a human-readable summary.",
    )
    migrate_cmd.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        default=False,
        help="Suppress progress output (final report is still written unless --json is off).",
    )

    return top


def _resolve_targets(args: argparse.Namespace) -> list[tuple[int, int, int]]:
    """Resolve the user-specified versions to actual bundled schema versions."""
    raw_versions: list[tuple[int, int, int]] = []

    if args.targets is not None:
        for part in args.targets.split(","):
            try:
                raw_versions.append(_parse_version_spec(part))
            except argparse.ArgumentTypeError as exc:
                print(f"error: {exc}", file=sys.stderr)
                sys.exit(2)
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


def _parse_code_list(spec: str) -> set[str]:
    """Parse a comma-separated list of diagnostic codes."""
    return {c.strip().upper() for c in spec.split(",") if c.strip()}


def _parse_group_list(spec: str) -> set[str]:
    """Parse a comma-separated list of IDD group names."""
    return {g.strip() for g in spec.split(",") if g.strip()}


def _filter_diagnostics(
    diagnostics: list[Diagnostic],
    *,
    select: set[str] | None,
    ignore: set[str] | None,
    severity: str | None,
) -> list[Diagnostic]:
    """Apply post-check filters (rule codes, severity) to diagnostics."""
    result: list[Diagnostic] = []
    for d in diagnostics:
        if select is not None and d.code not in select:
            continue
        if ignore is not None and d.code in ignore:
            continue
        if severity == "error" and d.severity != CompatSeverity.ERROR:
            continue
        result.append(d)
    return result


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

    if args.command == "check":
        _run_check(args)
    elif args.command == "migrate":
        _run_migrate(args)


def _run_check(args: argparse.Namespace) -> None:
    """Execute the ``check`` subcommand."""
    targets = _resolve_targets(args)

    # Parse optional filters
    select = _parse_code_list(args.select) if args.select else None
    ignore = _parse_code_list(args.ignore) if args.ignore else None
    include_groups = _parse_group_list(args.group) if args.group else None
    exclude_groups = _parse_group_list(args.exclude_group) if args.exclude_group else None

    # Validate --select / --ignore codes
    all_codes = set(DIAGNOSTIC_CODES.keys())
    for label, codes in [("--select", select), ("--ignore", ignore)]:
        if codes is not None:
            unknown = codes - all_codes
            if unknown:
                print(
                    f"error: unknown rule code(s) for {label}: {', '.join(sorted(unknown))}. "
                    f"Valid codes: {', '.join(sorted(all_codes))}",
                    file=sys.stderr,
                )
                sys.exit(2)

    all_diagnostics: list[Diagnostic] = []

    for filepath_str in args.files:
        filepath = Path(filepath_str)
        if not filepath.is_file():
            print(f"error: file not found: {filepath}", file=sys.stderr)
            sys.exit(2)

        source = filepath.read_text(encoding="utf-8")
        try:
            diagnostics = check_compatibility(
                source,
                str(filepath),
                targets,
                include_groups=include_groups,
                exclude_groups=exclude_groups,
            )
        except SyntaxError as exc:
            print(f"error: failed to parse {filepath}: {exc}", file=sys.stderr)
            sys.exit(2)
        all_diagnostics.extend(diagnostics)

    # Post-check filtering (rule codes, severity)
    all_diagnostics = _filter_diagnostics(
        all_diagnostics,
        select=select,
        ignore=ignore,
        severity=args.severity,
    )

    # Output
    if args.sarif_output:
        print(format_sarif(all_diagnostics))
    elif args.json_output:
        print(_format_json(all_diagnostics, targets))
    else:
        print(_format_text(all_diagnostics))

    # Exit code: 1 if any issues, 0 otherwise
    sys.exit(1 if all_diagnostics else 0)


def _default_output_path(input_path: Path, target: tuple[int, int, int]) -> Path:
    """Compute the default output path next to *input_path*."""
    tag = f"v{target[0]}-{target[1]}-{target[2]}"
    return input_path.with_name(f"{input_path.stem}-{tag}{input_path.suffix or '.idf'}")


def _progress_printer() -> Callable[[MigrationProgress], None]:
    """Return a callable that prints migration progress events to stderr."""

    def _print(event: MigrationProgress) -> None:
        prefix = f"[{event.phase}]"
        if event.step_index is not None and event.total_steps:
            prefix += f" {event.step_index + 1}/{event.total_steps}"
        print(f"{prefix} {event.message}", file=sys.stderr)

    return _print


def _format_migrate_json(report: MigrationReport, *, input_path: Path, output_path: Path | None) -> str:
    """Serialize a MigrationReport for ``--json`` output."""
    payload: dict[str, object] = {
        "input": str(input_path),
        "output": str(output_path) if output_path is not None else None,
        "success": report.success,
        "source_version": version_string(report.source_version),
        "target_version": version_string(report.target_version),
        "requested_target": version_string(report.requested_target),
        "steps": [
            {
                "from": version_string(s.from_version),
                "to": version_string(s.to_version),
                "success": s.success,
                "runtime_seconds": s.runtime_seconds,
                "binary": str(s.binary) if s.binary is not None else None,
            }
            for s in report.steps
        ],
        "diff": {
            "added_object_types": list(report.diff.added_object_types),
            "removed_object_types": list(report.diff.removed_object_types),
            "object_count_delta": dict(report.diff.object_count_delta),
            "field_changes": {k: asdict(v) for k, v in report.diff.field_changes.items()},
        },
    }
    return json.dumps(payload, indent=2)


def _resolve_migrate_target(spec: tuple[int, int, int] | None) -> tuple[int, int, int]:
    """Resolve the requested target to a bundled schema version, exiting on failure."""
    target = spec if spec is not None else LATEST_VERSION
    try:
        return resolve_version(target)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)


def _invoke_migrate(
    *,
    model: IDFDocument,
    target: tuple[int, int, int],
    energyplus: EnergyPlusConfig | None,
    on_progress: Callable[[MigrationProgress], None] | None,
    work_dir: str | None,
    keep_work_dir: bool,
) -> MigrationReport:
    """Call ``migrate`` and translate raised exceptions into CLI exits."""
    try:
        return migrate(
            model,
            target_version=target,
            energyplus=energyplus,
            on_progress=on_progress,
            work_dir=work_dir,
            keep_work_dir=keep_work_dir,
        )
    except UnsupportedVersionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)
    except EnergyPlusNotFoundError as exc:
        print(f"error: no EnergyPlus installation found ({exc})", file=sys.stderr)
        sys.exit(2)
    except MigrationError as exc:
        print(f"error: migration failed: {exc}", file=sys.stderr)
        sys.exit(1)


def _write_migrate_output(
    report: MigrationReport,
    *,
    input_path: Path,
    fallback_model: IDFDocument,
    resolved_target: tuple[int, int, int],
    explicit_output: str | None,
) -> Path | None:
    """Write the migrated IDF to disk and return the resulting path, if any."""
    from ..writers import write_idf

    if report.migrated_model is not None:
        output_path = Path(explicit_output) if explicit_output else _default_output_path(input_path, resolved_target)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_idf(report.migrated_model, output_path)
        return output_path
    if explicit_output is not None:
        # No-op migration: still honor an explicit --output by copying the input model.
        output_path = Path(explicit_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_idf(fallback_model, output_path)
        return output_path
    return None


def _load_source_idf(input_path: Path) -> IDFDocument:
    """Load the source IDF, exiting on any parse/IO error."""
    from .. import load_idf

    try:
        return load_idf(str(input_path))
    except Exception as exc:
        print(f"error: failed to load {input_path}: {exc}", file=sys.stderr)
        sys.exit(2)


def _resolve_energyplus_arg(path_arg: str | None) -> EnergyPlusConfig | None:
    """Resolve an optional ``--energyplus`` path into a config, exiting on failure."""
    if path_arg is None:
        return None
    from ..simulation.config import find_energyplus

    try:
        return find_energyplus(path=path_arg)
    except EnergyPlusNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)


def _run_migrate(args: argparse.Namespace) -> None:
    """Execute the ``migrate`` subcommand."""
    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"error: file not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    resolved_target = _resolve_migrate_target(args.to_version)
    model = _load_source_idf(input_path)
    energyplus = _resolve_energyplus_arg(args.energyplus_path)
    on_progress = None if (args.quiet or args.json_output) else _progress_printer()

    report = _invoke_migrate(
        model=model,
        target=resolved_target,
        energyplus=energyplus,
        on_progress=on_progress,
        work_dir=args.work_dir,
        keep_work_dir=args.keep_work_dir,
    )

    output_path = _write_migrate_output(
        report,
        input_path=input_path,
        fallback_model=model,
        resolved_target=resolved_target,
        explicit_output=args.output,
    )

    if args.json_output:
        print(_format_migrate_json(report, input_path=input_path, output_path=output_path))
    elif not args.quiet:
        print(report.summary())
        if output_path is not None:
            print(f"Wrote: {output_path}")
        elif report.migrated_model is None:
            print("No migration needed (source equals target).")

    sys.exit(0 if report.success else 1)
