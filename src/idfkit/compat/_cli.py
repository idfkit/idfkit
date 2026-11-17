"""CLI entry points for idfkit.

Subcommands:

- ``idfkit check`` — statically lint Python source files that use idfkit and
  report object types or enumerated choice values that differ between
  EnergyPlus schema versions, and literal object types passed to
  ``get_collection``.
- ``idfkit migrate`` — forward-migrate an IDF model to a newer EnergyPlus
  version via the installed ``IDFVersionUpdater`` transition binaries.
- ``idfkit tmy`` — search and download TMYx typical meteorological year
  weather data from climate.onebuilding.org (EPW + DDY + STAT), optionally
  via an interactive map browser.

Usage examples::

    idfkit check src/ --targets all
    idfkit check src/ --since 9.4
    idfkit check script.py --from 24.2 --to 25.1
    idfkit check script.py --targets 24.2,25.1,25.2 --json
    idfkit check            # paths and targets from [tool.idfkit.check] in pyproject.toml
    idfkit migrate old.idf --to 25.2
    idfkit migrate old.idf --output new.idf --to 25.2 --json
    idfkit tmy "chicago ohare"
    idfkit tmy --wmo 725300 --download ./weather/
    idfkit tmy --browse
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING, NoReturn

from ..exceptions import EnergyPlusNotFoundError, MigrationError, UnsupportedVersionError
from ..migration import MigrationProgress, MigrationReport, migrate
from ..versions import ENERGYPLUS_VERSIONS, LATEST_VERSION, version_string
from ..weather._cli import add_subparser as _add_tmy_subparser
from ..weather._cli import run_tmy as _run_tmy
from ._checker import check_compatibility, resolve_version
from ._config import (
    CheckConfig,
    ConfigError,
    find_config,
    finish_targets,
    load_config,
    matches,
    parse_release,
    parse_targets,
    relative_posix,
    releases_between,
)
from ._models import DEFAULT_RULES, DIAGNOSTIC_CODES, CompatSeverity, Diagnostic
from ._sarif import format_sarif

if TYPE_CHECKING:
    from ..document import AnyIDFDocument, IDFDocument
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
            "EnergyPlus schema versions (C001, C002), and literal object types passed to "
            "get_collection, which a type checker does not check (C003 for a name "
            "no target has; the opt-in C004 suggests the typed model[...] lookup). "
            "A lookup on as_version(doc, ...) or inside 'if doc.version >= (9, 4, 0):' is checked "
            "only against the targets it can run on. '# idfkit: ignore[C001]' on a line silences "
            "the listed rules there; a comment that silences nothing is reported as C005. "
            "Settings are read from [tool.idfkit.check] in the nearest pyproject.toml; "
            "command-line options override them."
        ),
        epilog=(
            "Exit status: 0 when nothing at or above --fail-on is reported, 1 when something is, "
            "2 for a usage, configuration or syntax error."
        ),
    )
    check.add_argument(
        "files",
        nargs="*",
        metavar="PATH",
        help=(
            "Python files or directories to lint (directories are searched for *.py). "
            "Defaults to 'paths' in [tool.idfkit.check], else the current directory."
        ),
    )

    # ---- version selection (mutually exclusive kinds) ----
    version_group = check.add_mutually_exclusive_group()
    version_group.add_argument(
        "--from",
        dest="from_version",
        type=str,
        metavar="VERSION",
        help=(
            "Source release of a single migration (e.g. 24.2), with --to. Only those two releases "
            "are compared; for every release in between use --since/--before."
        ),
    )
    check.add_argument(
        "--to",
        dest="to_version",
        type=str,
        metavar="VERSION",
        help="Target release of the migration (required with --from)",
    )
    version_group.add_argument(
        "--targets",
        type=str,
        metavar="VERSIONS",
        help="Comma-separated target releases (e.g. 9.4,24.2,26.2), or 'all' for every supported release",
    )
    version_group.add_argument(
        "--since",
        type=str,
        metavar="VERSION",
        help="Target every supported release from VERSION on (inclusive), as as_version(since=) reads it",
    )
    check.add_argument(
        "--before",
        type=str,
        metavar="VERSION",
        help="Target every supported release before VERSION (exclusive); combines with --since",
    )

    # ---- configuration ----
    config_group = check.add_mutually_exclusive_group()
    config_group.add_argument(
        "--config",
        type=str,
        default=None,
        metavar="PYPROJECT",
        help="Read [tool.idfkit.check] from this pyproject.toml instead of searching for one",
    )
    config_group.add_argument(
        "--isolated",
        action="store_true",
        default=False,
        help="Ignore every pyproject.toml",
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
        help=(
            "Comma-separated rule codes to check, replacing the default set "
            f"({','.join(sorted(DEFAULT_RULES))}) and the configured one."
        ),
    )
    check.add_argument(
        "--extend-select",
        type=str,
        default=None,
        metavar="CODES",
        help="Comma-separated rule codes to check in addition to the selected ones (e.g. C004).",
    )
    check.add_argument(
        "--ignore",
        type=str,
        default=None,
        metavar="CODES",
        help="Comma-separated rule codes not to check, added to the configured ones (e.g. C002).",
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

    # ---- severity filter and exit status ----
    check.add_argument(
        "--severity",
        type=str,
        choices=["warning", "error"],
        default=None,
        metavar="LEVEL",
        help="Minimum severity level to report (warning or error). Default: report all.",
    )
    check.add_argument(
        "--fail-on",
        type=str,
        choices=["warning", "error"],
        default=None,
        metavar="LEVEL",
        help="Lowest reported severity that makes the exit status 1 (default: warning).",
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

    _add_tmy_subparser(sub)

    return top


def _usage_error(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(2)


def _resolve_targets(args: argparse.Namespace, config: CheckConfig | None = None) -> list[tuple[int, int, int]]:
    """The target releases: from the command line if it names any, else from the configuration.

    Raises SystemExit(2) for a malformed or unsupported release, or fewer than two targets.
    """
    if args.before is not None and (args.targets is not None or args.from_version is not None):
        _usage_error("--before combines with --since, not --targets or --from")
    if args.to_version is not None and args.from_version is None:
        _usage_error("--to is the second release of --from; it does not combine with --targets, --since or --before")
    try:
        if args.targets is not None:
            return finish_targets(parse_targets(args.targets))
        if args.since is not None or args.before is not None:
            since = parse_release(args.since) if args.since is not None else None
            before = parse_release(args.before) if args.before is not None else None
            return finish_targets(releases_between(since, before))
        if args.from_version is not None:
            if args.to_version is None:
                _usage_error("--from and --to must both be specified")
            return finish_targets([parse_release(args.from_version), parse_release(args.to_version)])
    except ConfigError as exc:
        _usage_error(str(exc))
    if config is not None and config.targets is not None:
        return config.targets
    _usage_error(
        "no target releases: pass --targets (e.g. --targets all), --since/--before, or --from/--to, "
        "or set targets in [tool.idfkit.check]"
    )


def _parse_code_list(spec: str) -> set[str]:
    """Parse a comma-separated list of diagnostic codes."""
    return {c.strip().upper() for c in spec.split(",") if c.strip()}


def _parse_group_list(spec: str) -> set[str]:
    """Parse a comma-separated list of IDD group names."""
    return {g.strip() for g in spec.split(",") if g.strip()}


def _filter_diagnostics(diagnostics: list[Diagnostic], *, severity: str | None) -> list[Diagnostic]:
    """Apply the ``--severity`` filter. Rule codes are selected inside ``check_compatibility``."""
    if severity != "error":
        return diagnostics
    return [d for d in diagnostics if d.severity == CompatSeverity.ERROR]


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def _format_text(diagnostics: list[Diagnostic]) -> str:
    """Format diagnostics as human-readable text, one per line, then a summary line."""
    if not diagnostics:
        return "No compatibility issues found."
    lines = [str(d) for d in diagnostics]
    errors = sum(1 for d in diagnostics if d.severity == CompatSeverity.ERROR)
    files = len({d.filename for d in diagnostics})
    lines.append(
        f"Found {_plural(len(diagnostics), 'issue')} ({_plural(errors, 'error')}, "
        f"{_plural(len(diagnostics) - errors, 'warning')}) in {_plural(files, 'file')}."
    )
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
    elif args.command == "tmy":
        sys.exit(_run_tmy(args))


_SKIPPED_DIRS = frozenset({
    "__pycache__",
    "node_modules",
    "venv",
    "build",
    "dist",
    "site-packages",
})


@dataclass
class _Settings:
    """Everything ``check`` needs, merged from the configuration and the command line."""

    targets: list[tuple[int, int, int]]
    select: set[str]
    ignore: set[str]
    per_file_ignores: dict[str, list[str]]
    include_groups: set[str] | None
    exclude_groups: set[str] | None
    exclude: list[str]
    root: Path
    fail_on: str


def _load_check_config(args: argparse.Namespace) -> CheckConfig | None:
    try:
        if args.config is not None:
            return load_config(Path(args.config))
        if args.isolated:
            return None
        found = find_config(Path.cwd())
        return load_config(found) if found is not None else None
    except ConfigError as exc:
        _usage_error(str(exc))


def _settings(args: argparse.Namespace, config: CheckConfig | None) -> _Settings:
    """Merge *config* and the command line: a command-line --select replaces, --ignore and --extend-select add."""
    config = config or CheckConfig()
    if args.select is not None:
        # The command line replaces the configured selection, extend-select included, as in ruff.
        select = _parse_code_list(args.select)
    else:
        select = {c.upper() for c in config.select} if config.select is not None else set(DEFAULT_RULES)
        select |= {c.upper() for c in config.extend_select}
    if args.extend_select:
        select |= _parse_code_list(args.extend_select)
    ignore = {c.upper() for c in config.ignore}
    if args.ignore:
        ignore |= _parse_code_list(args.ignore)
    per_file_codes = {c.upper() for codes in config.per_file_ignores.values() for c in codes}

    all_codes = set(DIAGNOSTIC_CODES)
    for label, codes in [("select", select), ("ignore", ignore), ("per-file-ignores", per_file_codes)]:
        unknown = codes - all_codes
        if unknown:
            _usage_error(
                f"unknown rule code(s) for {label}: {', '.join(sorted(unknown))}. Valid codes: {', '.join(sorted(all_codes))}"
            )

    if not select - ignore:
        _usage_error("the rule selection is empty, so nothing would be checked; select at least one rule")

    include_groups = _parse_group_list(args.group) if args.group else None
    if include_groups is None and config.group is not None:
        include_groups = set(config.group)
    exclude_groups = _parse_group_list(args.exclude_group) if args.exclude_group else None
    if exclude_groups is None and config.exclude_group is not None:
        exclude_groups = set(config.exclude_group)

    return _Settings(
        targets=_resolve_targets(args, config),
        select=select,
        ignore=ignore,
        per_file_ignores=config.per_file_ignores,
        include_groups=include_groups,
        exclude_groups=exclude_groups,
        exclude=config.exclude,
        root=config.root,
        fail_on=args.fail_on or config.fail_on or "warning",
    )


def _excluded(path: Path, settings: _Settings) -> bool:
    relative = relative_posix(path, settings.root)
    return any(matches(relative, pattern) for pattern in settings.exclude)


def _discover(paths: list[str], settings: _Settings) -> list[Path]:
    """Every Python file named or found under *paths*, less the excluded ones, in a stable order.

    Directories are searched for ``*.py``, skipping hidden directories, virtual environments,
    caches and build output. ``exclude`` applies to files named explicitly too, so a pre-commit
    hook that passes file names honours it.
    """
    found: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_file():
            candidates = [path]
        elif path.is_dir():
            candidates = sorted(
                (
                    p
                    for p in path.rglob("*.py")
                    if not any(part.startswith(".") or part in _SKIPPED_DIRS for part in p.relative_to(path).parts[:-1])
                ),
                key=lambda p: p.as_posix(),
            )
        else:
            _usage_error(f"file not found: {path}")
        found.extend(p for p in candidates if not _excluded(p, settings))
    unique: dict[Path, None] = {}
    for p in found:
        unique.setdefault(p, None)
    return list(unique)


def _display_path(path: Path) -> str:
    """*path* relative to the working directory when it can be, so output does not depend on the checkout."""
    try:
        return os.path.relpath(path)
    except ValueError:  # another drive on Windows
        return str(path)


def _package_of(path: Path) -> str | None:
    """The dotted package *path* belongs to, read from the ``__init__.py`` files around it."""
    parts: list[str] = []
    directory = path.resolve().parent
    while (directory / "__init__.py").is_file():
        parts.insert(0, directory.name)
        directory = directory.parent
    return ".".join(parts) or None


def _file_ignores(path: Path, settings: _Settings) -> set[str]:
    relative = relative_posix(path, settings.root)
    return {
        c.upper() for pattern, codes in settings.per_file_ignores.items() if matches(relative, pattern) for c in codes
    }


def _run_check(args: argparse.Namespace) -> None:
    """Execute the ``check`` subcommand."""
    config = _load_check_config(args)
    settings = _settings(args, config)
    raw_paths: list[str] = list(args.files)
    if not raw_paths and config is not None and config.paths:
        raw_paths = [_display_path(config.root / p) for p in config.paths]
    files = _discover(raw_paths or ["."], settings)

    all_diagnostics: list[Diagnostic] = []
    failed_to_parse = False
    for filepath in files:
        try:
            source = filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"error: failed to read {filepath}: {exc}", file=sys.stderr)
            failed_to_parse = True
            continue
        try:
            diagnostics = check_compatibility(
                source,
                str(filepath),
                settings.targets,
                include_groups=settings.include_groups,
                exclude_groups=settings.exclude_groups,
                select=settings.select,
                ignore=settings.ignore | _file_ignores(filepath, settings),
                package=_package_of(filepath),
            )
        except (SyntaxError, ValueError) as exc:  # ValueError: a null byte, on Python 3.10 and 3.11
            print(f"error: failed to parse {filepath}: {exc}", file=sys.stderr)
            failed_to_parse = True
            continue
        all_diagnostics.extend(diagnostics)

    # Post-check filtering (severity). Rule selection was applied per file, before suppression.
    all_diagnostics = _filter_diagnostics(all_diagnostics, severity=args.severity)
    # Files stay in discovery order (sorted within each directory); each is sorted by line,
    # column and rule, so the output is stable from run to run and diffs cleanly.

    # Output
    if args.sarif_output:
        from .. import __version__

        print(format_sarif(all_diagnostics, tool_version=__version__))
    elif args.json_output:
        print(_format_json(all_diagnostics, settings.targets))
    else:
        print(_format_text(all_diagnostics))

    if failed_to_parse:
        sys.exit(2)
    failing = [d for d in all_diagnostics if settings.fail_on == "warning" or d.severity == CompatSeverity.ERROR]
    sys.exit(1 if failing else 0)


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
    model: AnyIDFDocument,
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
    fallback_model: AnyIDFDocument,
    resolved_target: tuple[int, int, int],
    explicit_output: str | None,
) -> Path | None:
    """Write the migrated IDF to disk and return the resulting path, if any."""
    from ..writers import save_idf

    if report.migrated_model is not None:
        output_path = Path(explicit_output) if explicit_output else _default_output_path(input_path, resolved_target)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_idf(report.migrated_model, output_path)
        return output_path
    if explicit_output is not None:
        # No-op migration: still honor an explicit --output by copying the input model.
        output_path = Path(explicit_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_idf(fallback_model, output_path)
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
