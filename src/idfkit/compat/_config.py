"""Target releases and project configuration for ``idfkit check``.

Settings live in ``pyproject.toml`` under ``[tool.idfkit.check]`` (the other ``[tool.idfkit.*]``
tables used across the idfkit family are ``conformance``, ``governance``, ``docs``, ``identity``
and ``library``)::

    [tool.idfkit.check]
    targets = "all"                 # or ["9.4", "24.1", "26.2"]; or since/before instead
    # since = "9.4"                 # every supported release from 9.4 on (inclusive)
    # before = "24.1"               # ... and before 24.1 (exclusive), as as_version() reads them
    paths = ["src"]                 # what to lint when no path is given on the command line
    exclude = ["src/legacy/**"]     # glob patterns, relative to this pyproject.toml
    select = ["C001", "C002", "C003", "C005"]
    extend-select = ["C004"]
    ignore = []
    per-file-ignores = { "tests/**" = ["C004"] }
    fail-on = "warning"             # or "error": the lowest severity that makes the exit code 1
"""

from __future__ import annotations

import fnmatch
import importlib
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePath
from typing import Any, cast

from ..versions import ENERGYPLUS_VERSIONS, LATEST_VERSION, MINIMUM_VERSION, find_release, version_string

Release = tuple[int, int, int]

_TABLE_RE = re.compile(r"^\s*\[\s*tool\s*\.\s*idfkit\s*\.\s*check\s*\]", re.MULTILINE)
_KNOWN_KEYS = frozenset({
    "targets",
    "since",
    "before",
    "paths",
    "exclude",
    "select",
    "extend-select",
    "ignore",
    "per-file-ignores",
    "group",
    "exclude-group",
    "fail-on",
})


class ConfigError(ValueError):
    """A ``[tool.idfkit.check]`` table, or a target release, that cannot be used."""


# ---------------------------------------------------------------------------
# Releases
# ---------------------------------------------------------------------------


def _supported() -> str:
    return f"{version_string(MINIMUM_VERSION)} to {version_string(LATEST_VERSION)}"


def parse_release(spec: str) -> Release:
    """Return the supported release *spec* names.

    ``MAJOR.MINOR`` names the release of that line, so ``9.0`` is 9.0.1, the only release with a
    non-zero patch. ``MAJOR.MINOR.PATCH`` is accepted for any patch of a supported line
    (``9.0.0`` and ``24.1.0`` both work), because EnergyPlus files and ``doc.version`` spell
    versions both ways. A line idfkit does not support is an error, newer ones included: a CI
    gate given ``27.1`` must fail rather than quietly check 26.2.

    Raises:
        ConfigError: If *spec* is malformed or names no supported release.
    """
    text = spec.strip()
    parts = text.split(".")
    if len(parts) not in {2, 3} or not all(p.isdecimal() for p in parts):
        msg = f"Invalid version specifier: '{spec}'. Expected MAJOR.MINOR or MAJOR.MINOR.PATCH."
        raise ConfigError(msg)
    release = find_release((int(parts[0]), int(parts[1]), 0))
    if release is None:
        msg = f"EnergyPlus {text} is not a release idfkit supports ({_supported()})"
        raise ConfigError(msg)
    return release


def releases_between(since: Release | None, before: Release | None) -> list[Release]:
    """Every supported release from *since* (inclusive) to *before* (exclusive), as ``as_version`` reads them."""
    return [v for v in ENERGYPLUS_VERSIONS if (since is None or v >= since) and (before is None or v < before)]


def parse_targets(spec: str | list[str]) -> list[Release]:
    """Read a ``--targets`` value: ``"all"``, or releases as a comma-separated string or a list.

    Raises:
        ConfigError: If an entry is not a supported release.
    """
    entries = spec.split(",") if isinstance(spec, str) else spec
    if [e.strip().lower() for e in entries] == ["all"]:
        return list(ENERGYPLUS_VERSIONS)
    return [parse_release(e) for e in entries]


def finish_targets(raw: list[Release]) -> list[Release]:
    """Deduplicate and sort *raw*, refusing fewer than two releases.

    Raises:
        ConfigError: If fewer than two distinct releases remain.
    """
    unique = sorted(set(raw))
    if len(unique) < 2:
        named = ", ".join(version_string(v) for v in unique) or "none"
        msg = f"at least two distinct target versions are required (got {named})"
        raise ConfigError(msg)
    return unique


# ---------------------------------------------------------------------------
# pyproject.toml
# ---------------------------------------------------------------------------


@dataclass
class CheckConfig:
    """The ``[tool.idfkit.check]`` table of one ``pyproject.toml``, validated."""

    path: Path | None = None
    targets: list[Release] | None = None
    paths: list[str] = field(default_factory=lambda: [])
    exclude: list[str] = field(default_factory=lambda: [])
    select: list[str] | None = None
    extend_select: list[str] = field(default_factory=lambda: [])
    ignore: list[str] = field(default_factory=lambda: [])
    per_file_ignores: dict[str, list[str]] = field(default_factory=lambda: {})
    group: list[str] | None = None
    exclude_group: list[str] | None = None
    fail_on: str | None = None

    @property
    def root(self) -> Path:
        """The directory relative patterns are read against."""
        return self.path.parent if self.path is not None else Path.cwd()


def find_config(start: Path) -> Path | None:
    """The nearest ``pyproject.toml`` at or above *start* that has a ``[tool.idfkit.check]`` table.

    The search stops at the repository root (the first directory holding ``.git``), so a table in
    a home directory never applies to a checkout below it.
    """
    for directory in [start, *start.parents]:
        candidate = directory / "pyproject.toml"
        if candidate.is_file() and _TABLE_RE.search(candidate.read_text(encoding="utf-8", errors="replace")):
            return candidate
        if (directory / ".git").exists():
            return None
    return None


def _toml_loads(text: str, path: Path) -> dict[str, Any]:
    """Parse TOML with ``tomllib`` (3.11+) or ``tomli`` (3.10), idfkit depending on neither."""
    module: Any = None
    for name in ("tomllib", "tomli"):
        try:
            module = importlib.import_module(name)
            break
        except ModuleNotFoundError:
            continue
    if module is None:
        msg = f"{path}: reading [tool.idfkit.check] needs Python 3.11+ or the 'tomli' package"
        raise ConfigError(msg)
    try:
        return cast("dict[str, Any]", module.loads(text))
    except ValueError as exc:  # TOMLDecodeError subclasses ValueError
        msg = f"{path}: {exc}"
        raise ConfigError(msg) from exc


def load_config(path: Path) -> CheckConfig:
    """Read and validate the ``[tool.idfkit.check]`` table of *path*.

    An unknown key is an error, so a misspelt setting cannot silently do nothing in CI.

    Raises:
        ConfigError: If the file cannot be read or the table is invalid.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        msg = f"cannot read {path}: {exc}"
        raise ConfigError(msg) from exc
    data = _toml_loads(text, path)
    table: object = data
    for key in ("tool", "idfkit", "check"):
        table = cast("dict[str, object]", table).get(key) if isinstance(table, dict) else None
    if table is None:
        msg = f"{path} has no [tool.idfkit.check] table"
        raise ConfigError(msg)
    if not isinstance(table, dict):
        msg = f"{path}: [tool.idfkit.check] must be a table"
        raise ConfigError(msg)
    return _validate(cast("dict[str, Any]", table), path)


def _where(path: Path, key: str) -> str:
    return f"{path}: [tool.idfkit.check] {key}"


def _str_list(table: dict[str, Any], key: str, path: Path) -> list[str] | None:
    value = table.get(key)
    if value is None:
        return None
    if not isinstance(value, list) or not all(isinstance(v, str) for v in cast("list[object]", value)):
        msg = f"{_where(path, key)} must be a list of strings"
        raise ConfigError(msg)
    return list(cast("list[str]", value))


def _str(table: dict[str, Any], key: str, path: Path) -> str | None:
    value = table.get(key)
    if value is not None and not isinstance(value, str):
        msg = f"{_where(path, key)} must be a string"
        raise ConfigError(msg)
    return value


def _config_targets(table: dict[str, Any], path: Path) -> list[Release] | None:
    raw_targets = table.get("targets")
    since, before = _str(table, "since", path), _str(table, "before", path)
    if raw_targets is not None and (since is not None or before is not None):
        msg = f"{path}: [tool.idfkit.check] takes targets, or since/before, not both"
        raise ConfigError(msg)
    try:
        if raw_targets is not None:
            entries = raw_targets if isinstance(raw_targets, str) else _str_list(table, "targets", path) or []
            return finish_targets(parse_targets(entries))
        if since is not None or before is not None:
            return finish_targets(
                releases_between(
                    parse_release(since) if since is not None else None,
                    parse_release(before) if before is not None else None,
                )
            )
    except ConfigError as exc:
        msg = f"{_where(path, 'targets')}: {exc}"
        raise ConfigError(msg) from exc
    return None


def _validate(table: dict[str, Any], path: Path) -> CheckConfig:
    unknown = sorted(set(table) - _KNOWN_KEYS)
    if unknown:
        msg = f"{path}: unknown key(s) in [tool.idfkit.check]: {', '.join(unknown)}; known keys: {', '.join(sorted(_KNOWN_KEYS))}"
        raise ConfigError(msg)
    config = CheckConfig(path=path, targets=_config_targets(table, path))
    config.paths = _str_list(table, "paths", path) or []
    config.exclude = _str_list(table, "exclude", path) or []
    config.select = _str_list(table, "select", path)
    config.extend_select = _str_list(table, "extend-select", path) or []
    config.ignore = _str_list(table, "ignore", path) or []
    config.group = _str_list(table, "group", path)
    config.exclude_group = _str_list(table, "exclude-group", path)

    per_file: object = table.get("per-file-ignores", {})
    if not isinstance(per_file, dict):
        msg = f"{_where(path, 'per-file-ignores')} must be a table of pattern = [codes]"
        raise ConfigError(msg)
    for pattern, codes in cast("dict[str, object]", per_file).items():
        if not isinstance(codes, list) or not all(isinstance(c, str) for c in cast("list[object]", codes)):
            msg = f"{_where(path, 'per-file-ignores')} '{pattern}' must be a list of rule codes"
            raise ConfigError(msg)
        config.per_file_ignores[pattern] = list(cast("list[str]", codes))

    fail_on = _str(table, "fail-on", path)
    if fail_on is not None and fail_on not in {"warning", "error"}:
        msg = f"{_where(path, 'fail-on')} must be 'warning' or 'error'"
        raise ConfigError(msg)
    config.fail_on = fail_on
    return config


# ---------------------------------------------------------------------------
# Path patterns
# ---------------------------------------------------------------------------


def relative_posix(path: Path, root: Path) -> str:
    """*path* relative to *root* in POSIX form, or its absolute POSIX form when outside *root*."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def matches(relative: str, pattern: str) -> bool:
    """Whether a POSIX path matches a glob *pattern*, as ruff's ``exclude`` and ``per-file-ignores`` do.

    ``*`` crosses directories (``tests/*`` and ``tests/**`` both cover ``tests/a/b.py``), a
    pattern naming a directory covers everything under it (``src/legacy``), and a pattern without
    a slash matches any single component, the file name or a directory at any depth
    (``conftest.py``, ``migrations``).
    """
    pattern = pattern.strip().removeprefix("./").rstrip("/")
    for variant in _zero_depth_variants(pattern):
        if fnmatch.fnmatchcase(relative, variant) or fnmatch.fnmatchcase(relative, variant + "/*"):
            return True
    return "/" not in pattern and any(fnmatch.fnmatchcase(part, pattern) for part in PurePath(relative).parts)


def _zero_depth_variants(pattern: str) -> set[str]:
    """*pattern* with each ``**/`` kept or dropped, so that ``**/`` also matches no directory at all.

    ``fnmatch`` reads ``**/`` as "something, then a slash", so ``**/conftest.py`` would miss a
    top-level ``conftest.py`` and ``tests/**/*.py`` a file directly in ``tests``, unlike ruff.
    """
    head, sep, tail = pattern.partition("**/")
    if not sep:
        return {pattern}
    return {head + keep + rest for rest in _zero_depth_variants(tail) for keep in ("**/", "")}
