"""Content-hash simulation cache.

Caches simulation results keyed by a SHA-256 digest of the normalised model,
weather file, and simulation flags.  Cache entries are full copies of the
simulation run directory so that all output files remain available.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..document import IDFDocument
    from .result import SimulationResult


def default_simulation_cache_dir() -> Path:
    """Return the platform-appropriate cache directory for simulation results."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "idfkit" / "cache" / "simulation"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "idfkit" / "simulation"
    # Linux / other POSIX
    xdg = os.environ.get("XDG_CACHE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".cache"
    return base / "idfkit" / "simulation"


@dataclass(frozen=True, slots=True)
class CacheKey:
    """Opaque cache key wrapping a hex digest string."""

    hex_digest: str


class SimulationCache:
    """Content-addressed simulation result cache.

    Each entry is a directory named by the cache key containing a full copy
    of the simulation run directory plus a ``_cache_meta.json`` manifest.
    """

    __slots__ = ("_cache_dir",)

    _META_FILE = "_cache_meta.json"

    def __init__(self, cache_dir: Path | None = None) -> None:
        self._cache_dir = cache_dir if cache_dir is not None else default_simulation_cache_dir()

    @property
    def cache_dir(self) -> Path:
        """Root directory for cached simulation entries."""
        return self._cache_dir

    def compute_key(
        self,
        model: IDFDocument,
        weather: str | Path,
        *,
        expand_objects: bool = True,
        annual: bool = False,
        design_day: bool = False,
        output_suffix: Literal["C", "L", "D"] = "C",
        extra_args: list[str] | tuple[str, ...] | None = None,
    ) -> CacheKey:
        """Compute a deterministic cache key for a simulation invocation.

        The model is copied and normalised (``Output:SQLite`` is ensured) so
        that models differing only in the presence of that object produce the
        same key.

        Args:
            model: The EnergyPlus model.
            weather: Path to the weather file.
            expand_objects: Whether ExpandObjects will run.
            annual: Whether annual simulation is used.
            design_day: Whether design-day-only simulation is used.
            output_suffix: Output file naming suffix (``"C"``, ``"L"``, or ``"D"``).
            extra_args: Additional command-line arguments.

        Returns:
            A :class:`CacheKey` for use with :meth:`get` / :meth:`put`.
        """
        from ..writers import write_idf

        normalised = model.copy()
        if "Output:SQLite" not in normalised:
            normalised.add("Output:SQLite", "", data={"option_type": "SimpleAndTabular"})
        idf_text: str = write_idf(normalised) or ""

        weather_path = Path(weather).resolve()
        weather_bytes = weather_path.read_bytes()

        flags = json.dumps(
            {
                "expand_objects": expand_objects,
                "annual": annual,
                "design_day": design_day,
                "output_suffix": output_suffix,
                "extra_args": list(extra_args) if extra_args else [],
            },
            sort_keys=True,
        )

        h = hashlib.sha256()
        h.update(idf_text.encode("utf-8"))
        h.update(weather_bytes)
        h.update(flags.encode("utf-8"))
        return CacheKey(hex_digest=h.hexdigest())

    def get(self, key: CacheKey) -> SimulationResult | None:
        """Retrieve a cached simulation result.

        Args:
            key: Cache key from :meth:`compute_key`.

        Returns:
            A :class:`SimulationResult` if a cache hit exists, otherwise
            ``None``.
        """
        entry_dir = self._cache_dir / key.hex_digest
        meta_path = entry_dir / self._META_FILE
        if not meta_path.is_file():
            return None

        meta = json.loads(meta_path.read_text(encoding="utf-8"))

        from .result import SimulationResult

        return SimulationResult(
            run_dir=entry_dir,
            success=meta["success"],
            exit_code=meta["exit_code"],
            stdout="",
            stderr="",
            runtime_seconds=meta["runtime_seconds"],
            output_prefix=meta["output_prefix"],
        )

    def put(self, key: CacheKey, result: SimulationResult) -> None:
        """Store a successful simulation result in the cache.

        Only results with ``success=True`` are cached.  The entire run
        directory is copied into the cache atomically.

        Args:
            key: Cache key from :meth:`compute_key`.
            result: Successful simulation result to cache.
        """
        if not result.success:
            return

        target_dir = self._cache_dir / key.hex_digest
        if target_dir.is_dir():
            return  # already cached

        self._cache_dir.mkdir(parents=True, exist_ok=True)

        tmp_dir = Path(tempfile.mkdtemp(dir=self._cache_dir, prefix=".tmp_"))
        try:
            # Copy output files (ignore_dangling_symlinks for robustness)
            shutil.copytree(result.run_dir, tmp_dir, dirs_exist_ok=True)

            # Write metadata
            meta = {
                "success": result.success,
                "exit_code": result.exit_code,
                "runtime_seconds": result.runtime_seconds,
                "output_prefix": result.output_prefix,
            }
            meta_path = tmp_dir / self._META_FILE
            meta_path.write_text(json.dumps(meta), encoding="utf-8")

            # Atomic rename
            os.rename(tmp_dir, target_dir)
        except OSError:
            # Another thread/process beat us — clean up
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def contains(self, key: CacheKey) -> bool:
        """Check whether a cache entry exists for *key*."""
        return (self._cache_dir / key.hex_digest / self._META_FILE).is_file()

    def clear(self) -> None:
        """Remove all cached entries."""
        if self._cache_dir.is_dir():
            shutil.rmtree(self._cache_dir)
