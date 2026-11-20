"""Content-hash simulation cache.

Caches simulation results keyed by a SHA-256 digest of the normalised model,
weather file, simulation flags, and the contents of every other file the model
names (a ``Schedule:File`` CSV, a ``Table:Lookup`` data file, a window data
file, an ASHRAE 205 representation, an FMU).  Cache entries are full copies of
the simulation run directory so that all output files remain available.

A model whose inputs the key cannot cover (one that runs a Python plugin, or
that exchanges data with another program through ``ExternalInterface``) is
never looked up or stored; the runners log a warning and simulate.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import logging
import os
import shutil
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal

__all__ = [
    "CacheKey",
    "SimulationCache",
    "default_simulation_cache_dir",
]

logger = logging.getLogger(__name__)

CACHE_META_FILE = "_cache_meta.json"
"""Name of the metadata file inside each cache entry; not a simulation output."""

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..document import AnyIDFDocument
    from .config import EnergyPlusConfig
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


def _external_files_bytes(model: AnyIDFDocument, search_dirs: list[Path]) -> bytes:
    """Return the bytes that bring every external file *model* names into the key.

    Empty when the model names no external file, so such a model keeps the
    key it had before external files were covered.
    """
    from ._external_files import external_file_refs, resolve_external_file

    refs = external_file_refs(model)
    if not refs:
        return b""
    parts = [b"\0external-files\0"]
    for ref in refs:
        parts.append(json.dumps([ref.obj_type, ref.field, ref.value]).encode("utf-8"))
        path = resolve_external_file(ref.value, search_dirs)
        if path is None:
            parts.append(b"\0missing\0")
            continue
        try:
            parts.append(b"\0found\0" + _file_digest(path))
        except OSError:
            # EnergyPlus cannot read it either; the run fails and is not stored.
            parts.append(b"\0unreadable\0")
    return b"".join(parts)


def _file_digest(path: Path) -> bytes:
    """Return the SHA-256 digest of *path*'s contents, read in chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.digest()


def runner_cache_key(
    cache: SimulationCache | None,
    model: AnyIDFDocument,
    weather: Path | None,
    *,
    output_dir: str | Path | None,
    config: EnergyPlusConfig,
    expand_objects: bool,
    annual: bool,
    design_day: bool,
    output_suffix: Literal["C", "L", "D"],
    readvars: bool,
    extra_args: list[str] | None,
) -> CacheKey | None:
    """Compute the cache key for one runner invocation, or ``None`` when the run must not use the cache.

    Internal helper shared by [simulate][idfkit.simulation.runner.simulate]
    and [async_simulate][idfkit.simulation.async_runner.async_simulate].  It
    returns ``None`` when there is no cache, and when *model* has inputs the
    key cannot cover, in which case it logs a warning naming them.
    """
    if cache is None:
        return None
    from ._external_files import search_dirs_for_run, uncacheable_reason

    reason = uncacheable_reason(model)
    if reason is not None:
        logger.warning("Not using the simulation cache: %s", reason)
        return None
    return cache.compute_key(
        model,
        weather,
        expand_objects=expand_objects,
        annual=annual,
        design_day=design_day,
        output_suffix=output_suffix,
        readvars=readvars,
        extra_args=extra_args,
        search_dirs=search_dirs_for_run(output_dir, config.executable),
    )


@dataclass(frozen=True, slots=True)
class CacheKey:
    """Opaque cache key wrapping a hex digest string."""

    hex_digest: str


class SimulationCache:
    """Content-addressed simulation result cache.

    Each entry is a directory named by the cache key containing a copy of
    the simulation run directory, less the weather file (whose contents are
    already part of the key), plus a ``_cache_meta.json`` manifest.

    The cache grows with every new run unless it is bounded: pass
    *max_bytes* to evict the least recently used entries after each store,
    or call [prune][idfkit.simulation.cache.SimulationCache.prune] to trim it
    by size or age.

    The key covers the model, the weather file, the run flags and the
    contents of every other file the model names, so editing a staged
    ``Schedule:File`` CSV (in ``output_dir`` or anywhere else) is a miss and
    restoring it is a hit again.  A model that runs a ``PythonPlugin:Instance``
    or an ``ExternalInterface`` in ``PtolemyServer`` or
    ``FunctionalMockupUnitExport`` mode has inputs no key can cover, so
    [simulate][idfkit.simulation.runner.simulate] and
    [async_simulate][idfkit.simulation.async_runner.async_simulate] neither
    look it up nor store it, and log a warning.
    """

    __slots__ = ("_cache_dir", "_max_bytes")

    _META_FILE = CACHE_META_FILE

    def __init__(self, cache_dir: str | Path | None = None, *, max_bytes: int | None = None) -> None:
        """Open a cache rooted at *cache_dir*.

        Args:
            cache_dir: Root directory for the entries; the platform cache
                directory when ``None``.
            max_bytes: Upper bound on the cache's total size. After each
                [put][idfkit.simulation.cache.SimulationCache.put] the least
                recently used entries are evicted until the cache fits.
                ``None`` (the default) never evicts. An entry larger than
                *max_bytes* on its own is evicted as soon as it is stored.
                Eviction also removes the entries behind earlier cache hits
                read without an ``output_dir`` (whose ``run_dir`` is the
                entry itself), so a batch can lose files of results it
                already returned; give runs whose results you keep an
                ``output_dir``, which receives a copy.

        Raises:
            ValueError: If *max_bytes* is negative.
        """
        if max_bytes is not None and max_bytes < 0:
            msg = f"max_bytes must be non-negative, got {max_bytes}"
            raise ValueError(msg)
        self._cache_dir = Path(cache_dir) if cache_dir is not None else default_simulation_cache_dir()
        self._max_bytes = max_bytes

    @property
    def cache_dir(self) -> Path:
        """Root directory for cached simulation entries."""
        return self._cache_dir

    def compute_key(
        self,
        model: AnyIDFDocument,
        weather: str | Path | None,
        *,
        expand_objects: bool = True,
        annual: bool = False,
        design_day: bool = False,
        output_suffix: Literal["C", "L", "D"] = "C",
        readvars: bool = False,
        extra_args: list[str] | tuple[str, ...] | None = None,
        search_dirs: Sequence[str | Path] = (),
    ) -> CacheKey:
        """Compute a deterministic cache key for a simulation invocation.

        The model is copied and normalised (``Output:SQLite`` is ensured) so
        that models differing only in the presence of that object produce the
        same key.

        Every file the model names for EnergyPlus to read contributes its
        contents: ``Schedule:File``, ``Schedule:File:Shading``, the
        ``Table:*`` external data files, ``Construction:WindowDataFile``, the
        ASHRAE 205 representation files and FMUs.  An absolute path is read
        as is; a relative path is looked up in *search_dirs* in order, as
        EnergyPlus looks in its working directory and then next to its
        executable.  A file that cannot be found contributes a marker
        instead, so its later appearance changes the key.  A model that names
        no such file gets the same key as it did before this was added.

        Args:
            model: The EnergyPlus model.
            weather: Path to the weather file, or ``None`` for a run without
                one. A key computed with ``None`` never equals a key computed
                with a weather file.
            expand_objects: Whether ExpandObjects will run.
            annual: Whether annual simulation is used.
            design_day: Whether design-day-only simulation is used.
            output_suffix: Output file naming suffix (``"C"``, ``"L"``, or ``"D"``).
            readvars: Whether ReadVarsESO post-processing will run.
            extra_args: Additional command-line arguments.
            search_dirs: Directories a relative external file path resolves
                against, in order.  The runners pass the run directory
                (when ``output_dir`` is given) and the EnergyPlus
                executable's directory.

        Returns:
            A [CacheKey][idfkit.simulation.cache.CacheKey] for use with [get][idfkit.simulation.cache.SimulationCache.get] / [put][idfkit.simulation.cache.SimulationCache.put].
        """
        from ..writers import write_idf

        normalised = model.copy()
        if "Output:SQLite" not in normalised:
            normalised["Output:SQLite"].add(option_type="SimpleAndTabular")
        idf_text: str = write_idf(normalised)

        flag_values: dict[str, object] = {
            "expand_objects": expand_objects,
            "annual": annual,
            "design_day": design_day,
            "output_suffix": output_suffix,
            "readvars": readvars,
            "extra_args": list(extra_args) if extra_args else [],
        }
        if weather is None:
            # The extra member separates these keys from every key with a weather file.
            weather_bytes = b""
            flag_values["weather"] = None
        else:
            weather_bytes = Path(weather).resolve().read_bytes()

        flags = json.dumps(flag_values, sort_keys=True)

        h = hashlib.sha256()
        h.update(idf_text.encode("utf-8"))
        h.update(weather_bytes)
        h.update(flags.encode("utf-8"))
        dirs = [search_dirs] if isinstance(search_dirs, str) else search_dirs
        h.update(_external_files_bytes(model, [Path(d) for d in dirs]))
        key = CacheKey(hex_digest=h.hexdigest())
        logger.debug("Computed cache key %s", key.hex_digest[:12])
        return key

    def get(self, key: CacheKey) -> SimulationResult | None:
        """Retrieve a cached simulation result.

        Args:
            key: Cache key from [compute_key][idfkit.simulation.cache.SimulationCache.compute_key].

        Returns:
            A [SimulationResult][idfkit.simulation.result.SimulationResult] if a cache hit exists, otherwise
            ``None``. Its ``cached`` is ``True`` and its ``run_dir`` is the
            cache entry itself: treat that directory as read-only.
            [simulate][idfkit.simulation.runner.simulate] copies a hit into its
            ``output_dir``, when it has one, before returning it.
        """
        entry_dir = self._cache_dir / key.hex_digest
        meta_path = entry_dir / self._META_FILE
        if not meta_path.is_file():
            logger.debug("Cache miss for %s", key.hex_digest[:12])
            return None

        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            # Mark the entry as recently used, for least-recently-used eviction.
            with contextlib.suppress(OSError):
                os.utime(meta_path)

            from .result import SimulationResult

            logger.debug("Cache hit for %s", key.hex_digest[:12])
            return SimulationResult(
                run_dir=entry_dir,
                success=meta["success"],
                exit_code=meta["exit_code"],
                stdout="",
                stderr="",
                runtime_seconds=meta["runtime_seconds"],
                output_prefix=meta["output_prefix"],
                output_suffix=meta.get("output_suffix"),
                cached=True,
            )
        except (json.JSONDecodeError, KeyError, OSError):
            # Corrupted or incomplete cache entry — remove it so that
            # a subsequent put() can write a fresh copy, then treat as miss.
            logger.debug("Removing corrupted cache entry %s", key.hex_digest[:12])
            shutil.rmtree(entry_dir, ignore_errors=True)
            return None

    def put(self, key: CacheKey, result: SimulationResult) -> None:
        """Store a successful simulation result in the cache.

        Only results with ``success=True`` are cached.  The run directory,
        less any ``.epw`` weather file, is copied into the cache atomically.
        With *max_bytes* set, the least recently used entries are then
        evicted until the cache fits.

        Args:
            key: Cache key from [compute_key][idfkit.simulation.cache.SimulationCache.compute_key].
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
            # The weather file is an input whose contents the key already covers.
            shutil.copytree(result.run_dir, tmp_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns("*.epw"))

            # Write metadata
            meta = {
                "success": result.success,
                "exit_code": result.exit_code,
                "runtime_seconds": result.runtime_seconds,
                "output_prefix": result.output_prefix,
                "output_suffix": result.output_suffix,
            }
            meta_path = tmp_dir / self._META_FILE
            meta_path.write_text(json.dumps(meta), encoding="utf-8")

            # Atomic rename — os.rename fails if target_dir already exists
            # (another process beat us), unlike shutil.move which would nest
            # tmp_dir inside the existing target as a subdirectory.
            os.rename(str(tmp_dir), str(target_dir))
            logger.debug("Cached result for %s", key.hex_digest[:12])
        except OSError as exc:
            # Another thread/process beat us, or a real filesystem error
            # — clean up the temporary directory.
            shutil.rmtree(tmp_dir, ignore_errors=True)
            if not target_dir.is_dir():
                # Not a lost race: the entry was not stored, so every later lookup misses. Say so.
                logger.warning("Could not cache result for %s from %s: %s", key.hex_digest[:12], result.run_dir, exc)
        if self._max_bytes is not None:
            self.prune(max_bytes=self._max_bytes)

    def contains(self, key: CacheKey) -> bool:
        """Check whether a cache entry exists for *key*."""
        return (self._cache_dir / key.hex_digest / self._META_FILE).is_file()

    def size_bytes(self) -> int:
        """Total size in bytes of the cache's stored entries."""
        return sum(size for _, _, size in self._entries())

    def prune(self, *, max_bytes: int | None = None, max_age: float | None = None) -> int:
        """Evict entries to bound the cache's size and age.

        Entries not used for longer than *max_age* are removed first; then,
        while the cache is larger than *max_bytes*, the least recently used
        entry is removed. An entry counts as used when it is stored and on
        every [get][idfkit.simulation.cache.SimulationCache.get] hit.

        A result whose ``run_dir`` is a cache entry (a hit read without an
        ``output_dir``) stops working when its entry is removed.

        Args:
            max_bytes: Size to bring the cache under, or ``None`` for no size bound.
            max_age: Age in seconds since last use beyond which an entry is
                removed, or ``None`` for no age bound.

        Returns:
            The number of entries removed.

        Raises:
            ValueError: If *max_bytes* or *max_age* is negative.
        """
        for bound, value in (("max_bytes", max_bytes), ("max_age", max_age)):
            if value is not None and value < 0:
                msg = f"{bound} must be non-negative, got {value}"
                raise ValueError(msg)
        entries = sorted(self._entries(), key=lambda entry: entry[1])  # least recently used first
        now = time.time()
        total = sum(size for _, _, size in entries)
        removed = 0
        for entry_dir, used_at, size in entries:
            too_old = max_age is not None and now - used_at > max_age
            too_big = max_bytes is not None and total > max_bytes
            if not too_old and not too_big:
                continue
            shutil.rmtree(entry_dir, ignore_errors=True)
            total -= size
            removed += 1
            logger.debug("Evicted cache entry %s", entry_dir.name[:12])
        return removed

    def _entries(self) -> list[tuple[Path, float, int]]:
        """Every stored entry as ``(directory, last-used time, size in bytes)``."""
        if not self._cache_dir.is_dir():
            return []
        entries: list[tuple[Path, float, int]] = []
        for entry_dir in self._cache_dir.iterdir():
            meta_path = entry_dir / self._META_FILE
            try:
                used_at = meta_path.stat().st_mtime
                size = sum(f.stat().st_size for f in entry_dir.rglob("*") if f.is_file())
            except OSError:
                continue  # not an entry (a .tmp_ staging directory), or removed meanwhile
            entries.append((entry_dir, used_at, size))
        return entries

    def clear(self) -> None:
        """Remove all cached entries."""
        if self._cache_dir.is_dir():
            shutil.rmtree(self._cache_dir)
            logger.debug("Cleared simulation cache at %s", self._cache_dir)
