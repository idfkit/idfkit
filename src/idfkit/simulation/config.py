"""EnergyPlus installation discovery and configuration.

Provides automatic detection of EnergyPlus installations across platforms,
with support for explicit paths, environment variables, and standard
installation directories.
"""

from __future__ import annotations

import os
import platform
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from ..exceptions import EnergyPlusNotFoundError


@dataclass(frozen=True, slots=True)
class EnergyPlusConfig:
    """Validated EnergyPlus installation configuration.

    Attributes:
        executable: Path to the energyplus executable.
        version: Parsed version as (major, minor, patch).
        install_dir: Root installation directory.
        idd_path: Path to the Energy+.idd file.
    """

    executable: Path
    version: tuple[int, int, int]
    install_dir: Path
    idd_path: Path

    @property
    def weather_dir(self) -> Path | None:
        """Path to the bundled WeatherData directory, if present."""
        d = self.install_dir / "WeatherData"
        return d if d.is_dir() else None

    @property
    def schema_path(self) -> Path | None:
        """Path to Energy+.schema.epJSON, if present."""
        p = self.install_dir / "Energy+.schema.epJSON"
        return p if p.is_file() else None

    @property
    def expand_objects_exe(self) -> Path | None:
        """Path to ExpandObjects executable, if present."""
        name = "ExpandObjects.exe" if platform.system() == "Windows" else "ExpandObjects"
        p = self.install_dir / name
        return p if p.is_file() else None

    @classmethod
    def from_path(cls, path: str | Path) -> EnergyPlusConfig:
        """Create config from an explicit installation path.

        The path can point to either the installation directory or the
        energyplus executable directly.

        Args:
            path: Path to EnergyPlus install directory or executable.

        Returns:
            Validated EnergyPlusConfig.

        Raises:
            EnergyPlusNotFoundError: If the path is not a valid installation.
        """
        path = Path(path).resolve()

        # If path is an executable, derive install dir
        if path.is_file():
            install_dir = path.parent
            exe = path
        else:
            install_dir = path
            exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
            exe = install_dir / exe_name

        if not exe.is_file():
            raise EnergyPlusNotFoundError([str(install_dir)])

        idd = install_dir / "Energy+.idd"
        if not idd.is_file():
            raise EnergyPlusNotFoundError([str(install_dir)])

        version = _extract_version(install_dir)
        if version is None:
            version = _extract_version_from_idd(idd)
        if version is None:
            raise EnergyPlusNotFoundError([str(install_dir)])

        return cls(
            executable=exe,
            version=version,
            install_dir=install_dir,
            idd_path=idd,
        )


# ---------------------------------------------------------------------------
# Public discovery function
# ---------------------------------------------------------------------------


def find_energyplus(
    *,
    version: tuple[int, int, int] | str | None = None,
    path: str | Path | None = None,
) -> EnergyPlusConfig:
    """Find an EnergyPlus installation.

    Discovery order:
        1. Explicit *path* argument.
        2. ``ENERGYPLUS_DIR`` environment variable.
        3. ``energyplus`` on ``PATH`` (via :func:`shutil.which`).
        4. Platform-specific default directories (newest version first).

    Args:
        version: Optional version filter. Accepts ``(major, minor, patch)``
            tuple or a string like ``"24.1.0"`` or ``"24.1"``.
        path: Explicit path to EnergyPlus install directory or executable.

    Returns:
        Validated EnergyPlusConfig.

    Raises:
        EnergyPlusNotFoundError: If no matching installation is found.
    """
    target_version = _normalize_version(version) if version is not None else None
    searched: list[str] = []

    # 1. Explicit path
    if path is not None:
        p = Path(path).resolve()
        searched.append(str(p))
        config = EnergyPlusConfig.from_path(p)
        if target_version is not None and config.version != target_version:
            raise EnergyPlusNotFoundError(searched)
        return config

    # 2-4. Try candidates from env var, PATH, and platform dirs
    for candidate in _discovery_candidates():
        searched.append(str(candidate))
        result = _try_candidate(candidate, target_version)
        if result is not None:
            return result

    raise EnergyPlusNotFoundError(searched)


def _discovery_candidates() -> list[Path]:
    """Collect candidate paths from env var, PATH, and platform dirs.

    Returns:
        Ordered list of candidate paths to try.
    """
    candidates: list[Path] = []

    env_dir = os.environ.get("ENERGYPLUS_DIR")
    if env_dir:
        candidates.append(Path(env_dir).resolve())

    which_result = shutil.which("energyplus")
    if which_result:
        candidates.append(Path(which_result).resolve())

    candidates.extend(_glob_sorted(_platform_search_dirs()))
    return candidates


def _try_candidate(candidate: Path, target_version: tuple[int, int, int] | None) -> EnergyPlusConfig | None:
    """Try to create a config from a candidate path.

    Args:
        candidate: Path to try.
        target_version: Required version, or None for any.

    Returns:
        Config if valid and version matches, else None.
    """
    try:
        config = EnergyPlusConfig.from_path(candidate)
    except EnergyPlusNotFoundError:
        return None
    if target_version is None or config.version == target_version:
        return config
    return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VERSION_DIR_RE = re.compile(r"EnergyPlus[Vv-]?(\d+)[.-](\d+)[.-](\d+)")
_VERSION_IDD_RE = re.compile(r"^!IDD_Version\s+(\d+)\.(\d+)\.(\d+)", re.MULTILINE)


def _normalize_version(version: tuple[int, int, int] | str) -> tuple[int, int, int]:
    """Normalize a version argument to a (major, minor, patch) tuple.

    Args:
        version: Version as tuple or dotted string.

    Returns:
        Normalized (major, minor, patch) tuple.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    if isinstance(version, tuple):
        return version
    parts = version.replace("-", ".").split(".")
    if len(parts) == 2:
        parts.append("0")
    if len(parts) != 3:
        msg = f"Cannot parse version string: {version!r}"
        raise ValueError(msg)
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def _extract_version(install_dir: Path) -> tuple[int, int, int] | None:
    """Extract version from directory name (e.g. EnergyPlusV24-1-0).

    Args:
        install_dir: Installation directory path.

    Returns:
        Version tuple or None.
    """
    match = _VERSION_DIR_RE.search(install_dir.name)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


def _extract_version_from_idd(idd_path: Path) -> tuple[int, int, int] | None:
    """Extract version from Energy+.idd header.

    Args:
        idd_path: Path to Energy+.idd file.

    Returns:
        Version tuple or None.
    """
    try:
        # Read only the first 2KB to find the header
        with idd_path.open(encoding="latin-1") as f:
            header = f.read(2048)
    except OSError:
        return None

    match = _VERSION_IDD_RE.search(header)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


def _platform_search_dirs() -> list[Path]:
    """Return platform-specific directories where EnergyPlus may be installed.

    Returns:
        List of candidate directories.
    """
    system = platform.system()
    dirs: list[Path] = []

    if system == "Linux":
        # User-level first, then system-level
        home = Path.home()
        dirs.append(home / ".local")  # Common pip/user install location
        dirs.append(home / "EnergyPlus")
        dirs.append(Path("/usr/local"))
        dirs.append(Path("/opt"))
    elif system == "Darwin":
        home = Path.home()
        dirs.append(home / "Applications")
        dirs.append(Path("/Applications"))
    elif system == "Windows":
        # Program Files variants
        for env_var in ("ProgramFiles", "ProgramFiles(x86)", "ProgramW6432"):
            val = os.environ.get(env_var)
            if val:
                dirs.append(Path(val))

    return dirs


def _glob_sorted(search_dirs: list[Path]) -> list[Path]:
    """Find EnergyPlus directories in search paths, sorted newest first.

    Args:
        search_dirs: Directories to search.

    Returns:
        Matching directories sorted by version descending.
    """
    candidates: list[tuple[tuple[int, int, int], Path]] = []

    for d in search_dirs:
        if not d.is_dir():
            continue
        for child in d.iterdir():
            if not child.is_dir():
                continue
            version = _extract_version(child)
            if version is not None:
                candidates.append((version, child))

    # Sort by version descending (newest first)
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [path for _, path in candidates]
