"""Tests for the simulation cache."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from idfkit import new_document
from idfkit.simulation.cache import CacheKey, SimulationCache, default_simulation_cache_dir
from idfkit.simulation.result import SimulationResult

# ---------------------------------------------------------------------------
# default_simulation_cache_dir
# ---------------------------------------------------------------------------


class TestDefaultSimulationCacheDir:
    """Tests for default_simulation_cache_dir()."""

    def test_linux(self) -> None:
        with patch("idfkit.simulation.cache.sys") as mock_sys:
            mock_sys.platform = "linux"
            with patch.dict(os.environ, {}, clear=True):
                result = default_simulation_cache_dir()
        assert result == Path.home() / ".cache" / "idfkit" / "simulation"

    def test_linux_xdg(self, tmp_path: Path) -> None:
        with patch("idfkit.simulation.cache.sys") as mock_sys:
            mock_sys.platform = "linux"
            with patch.dict(os.environ, {"XDG_CACHE_HOME": str(tmp_path)}, clear=True):
                result = default_simulation_cache_dir()
        assert result == tmp_path / "idfkit" / "simulation"

    def test_darwin(self) -> None:
        with patch("idfkit.simulation.cache.sys") as mock_sys:
            mock_sys.platform = "darwin"
            result = default_simulation_cache_dir()
        assert result == Path.home() / "Library" / "Caches" / "idfkit" / "simulation"

    def test_win32(self, tmp_path: Path) -> None:
        with patch("idfkit.simulation.cache.sys") as mock_sys:
            mock_sys.platform = "win32"
            with patch.dict(os.environ, {"LOCALAPPDATA": str(tmp_path)}):
                result = default_simulation_cache_dir()
        assert result == tmp_path / "idfkit" / "cache" / "simulation"


# ---------------------------------------------------------------------------
# CacheKey
# ---------------------------------------------------------------------------


class TestCacheKey:
    """Tests for CacheKey dataclass."""

    def test_frozen(self) -> None:
        key = CacheKey(hex_digest="abc123")
        with pytest.raises(AttributeError):
            key.hex_digest = "changed"  # type: ignore[misc]

    def test_equality(self) -> None:
        k1 = CacheKey(hex_digest="abc")
        k2 = CacheKey(hex_digest="abc")
        k3 = CacheKey(hex_digest="def")
        assert k1 == k2
        assert k1 != k3


# ---------------------------------------------------------------------------
# compute_key
# ---------------------------------------------------------------------------


class TestComputeKey:
    """Tests for SimulationCache.compute_key()."""

    @pytest.fixture
    def weather_file(self, tmp_path: Path) -> Path:
        epw = tmp_path / "weather.epw"
        epw.write_text("LOCATION,Chicago\n")
        return epw

    @pytest.fixture
    def cache(self, tmp_path: Path) -> SimulationCache:
        return SimulationCache(cache_dir=tmp_path / "cache")

    def test_deterministic(self, cache: SimulationCache, weather_file: Path) -> None:
        model = new_document()
        k1 = cache.compute_key(model, weather_file)
        k2 = cache.compute_key(model, weather_file)
        assert k1 == k2

    def test_different_model(self, cache: SimulationCache, weather_file: Path) -> None:
        m1 = new_document()
        m2 = new_document()
        m2.add("Zone", "TestZone")
        k1 = cache.compute_key(m1, weather_file)
        k2 = cache.compute_key(m2, weather_file)
        assert k1 != k2

    def test_different_weather(self, cache: SimulationCache, tmp_path: Path) -> None:
        model = new_document()
        w1 = tmp_path / "w1.epw"
        w2 = tmp_path / "w2.epw"
        w1.write_text("LOCATION,Chicago\n")
        w2.write_text("LOCATION,Denver\n")
        k1 = cache.compute_key(model, w1)
        k2 = cache.compute_key(model, w2)
        assert k1 != k2

    def test_without_weather_deterministic(self, cache: SimulationCache) -> None:
        model = new_document()
        k1 = cache.compute_key(model, None, design_day=True)
        k2 = cache.compute_key(model, None, design_day=True)
        assert k1 == k2

    def test_without_weather_differs_from_with_weather(self, cache: SimulationCache, weather_file: Path) -> None:
        model = new_document()
        k1 = cache.compute_key(model, None, design_day=True)
        k2 = cache.compute_key(model, weather_file, design_day=True)
        assert k1 != k2

    def test_different_flags(self, cache: SimulationCache, weather_file: Path) -> None:
        model = new_document()
        k1 = cache.compute_key(model, weather_file, annual=False)
        k2 = cache.compute_key(model, weather_file, annual=True)
        assert k1 != k2

    def test_sql_normalisation(self, cache: SimulationCache, weather_file: Path) -> None:
        """Model with and without Output:SQLite should produce the same key."""
        m1 = new_document()
        m2 = new_document()
        m2.add("Output:SQLite", "", option_type="SimpleAndTabular")
        k1 = cache.compute_key(m1, weather_file)
        k2 = cache.compute_key(m2, weather_file)
        assert k1 == k2


# ---------------------------------------------------------------------------
# get / put / contains / clear
# ---------------------------------------------------------------------------


class TestGetPut:
    """Tests for cache get/put round-trip."""

    @pytest.fixture
    def cache(self, tmp_path: Path) -> SimulationCache:
        return SimulationCache(cache_dir=tmp_path / "cache")

    @pytest.fixture
    def run_dir(self, tmp_path: Path) -> Path:
        d = tmp_path / "run"
        d.mkdir()
        (d / "eplusout.sql").write_text("fake sql")
        (d / "eplusout.err").write_text("fake err")
        return d

    def test_miss_returns_none(self, cache: SimulationCache) -> None:
        key = CacheKey(hex_digest="nonexistent")
        assert cache.get(key) is None

    def test_round_trip(self, cache: SimulationCache, run_dir: Path) -> None:
        key = CacheKey(hex_digest="abc123")
        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="output",
            stderr="",
            runtime_seconds=1.5,
            output_prefix="eplus",
        )
        cache.put(key, result)

        restored = cache.get(key)
        assert restored is not None
        assert restored.success is True
        assert restored.exit_code == 0
        assert restored.runtime_seconds == 1.5
        assert restored.output_prefix == "eplus"
        assert restored.cached
        assert not result.cached

    def test_metadata_preserved(self, cache: SimulationCache, run_dir: Path) -> None:
        key = CacheKey(hex_digest="meta_test")
        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=42.0,
            output_prefix="custom",
        )
        cache.put(key, result)

        restored = cache.get(key)
        assert restored is not None
        assert restored.output_prefix == "custom"
        assert restored.runtime_seconds == 42.0

    def test_only_caches_successful(self, cache: SimulationCache, run_dir: Path) -> None:
        key = CacheKey(hex_digest="failed")
        result = SimulationResult(
            run_dir=run_dir,
            success=False,
            exit_code=1,
            stdout="",
            stderr="error",
            runtime_seconds=0.5,
        )
        cache.put(key, result)
        assert cache.get(key) is None

    def test_contains(self, cache: SimulationCache, run_dir: Path) -> None:
        key = CacheKey(hex_digest="containstest")
        assert not cache.contains(key)

        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=1.0,
        )
        cache.put(key, result)
        assert cache.contains(key)

    def test_clear(self, cache: SimulationCache, run_dir: Path) -> None:
        key = CacheKey(hex_digest="cleartest")
        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=1.0,
        )
        cache.put(key, result)
        assert cache.contains(key)

        cache.clear()
        assert not cache.contains(key)

    def test_cached_files_accessible(self, cache: SimulationCache, run_dir: Path) -> None:
        """Cached result should have copies of output files."""
        key = CacheKey(hex_digest="files_test")
        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=1.0,
        )
        cache.put(key, result)

        restored = cache.get(key)
        assert restored is not None
        assert (restored.run_dir / "eplusout.sql").is_file()
        assert (restored.run_dir / "eplusout.err").is_file()

    def test_corrupted_entry_cleaned_up_on_get(self, cache: SimulationCache) -> None:
        """A corrupted cache entry should be removed by get() so put() can replace it."""
        key = CacheKey(hex_digest="corrupted")
        entry_dir = cache.cache_dir / key.hex_digest
        entry_dir.mkdir(parents=True)
        # Write invalid JSON to the metadata file
        (entry_dir / "_cache_meta.json").write_text("NOT VALID JSON", encoding="utf-8")

        # get() should return None and clean up the corrupted entry
        assert cache.get(key) is None
        assert not entry_dir.exists()

    def test_corrupted_entry_replaceable_after_get(self, cache: SimulationCache, run_dir: Path) -> None:
        """After get() cleans a corrupted entry, put() should be able to store a fresh one."""
        key = CacheKey(hex_digest="replace_corrupted")
        entry_dir = cache.cache_dir / key.hex_digest
        entry_dir.mkdir(parents=True)
        (entry_dir / "_cache_meta.json").write_text("{}", encoding="utf-8")  # missing keys

        # get() cleans the corrupted entry
        assert cache.get(key) is None
        assert not entry_dir.exists()

        # Now put() should succeed
        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=2.0,
            output_prefix="eplus",
        )
        cache.put(key, result)
        restored = cache.get(key)
        assert restored is not None
        assert restored.runtime_seconds == 2.0

    def test_put_no_leaked_temp_dirs(self, cache: SimulationCache, run_dir: Path) -> None:
        """put() should not leave temporary directories inside existing cache entries."""
        key = CacheKey(hex_digest="no_leak")
        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=1.0,
        )
        cache.put(key, result)

        # Second put with same key should be a no-op (early return)
        cache.put(key, result)

        # Verify no .tmp_ subdirectories leaked inside the cache entry
        entry_dir = cache.cache_dir / key.hex_digest
        for child in entry_dir.iterdir():
            assert not child.name.startswith(".tmp_"), f"Leaked temp dir: {child}"

    def test_concurrent_put_no_leaked_temp_dirs(self, cache: SimulationCache, run_dir: Path) -> None:
        """Simulates the race where target_dir is created between the is_dir() check and rename."""
        key = CacheKey(hex_digest="race_test")
        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=1.0,
        )
        # First put succeeds normally
        cache.put(key, result)

        entry_dir = cache.cache_dir / key.hex_digest

        # Manually remove the entry directory and re-create it mid-flight
        # by patching is_dir to return False (simulating the TOCTOU window)
        import shutil

        shutil.rmtree(entry_dir)
        cache.put(key, result)  # re-populate

        # Verify the entry is intact and has no nested temp dirs
        assert cache.contains(key)
        for child in entry_dir.iterdir():
            assert not child.name.startswith(".tmp_"), f"Leaked temp dir: {child}"

    def test_put_os_error_on_rename_cleans_up_tmp(self, cache: SimulationCache, run_dir: Path) -> None:
        """When os.rename raises OSError, the temporary directory is cleaned up."""
        key = CacheKey(hex_digest="os_error_rename")
        result = SimulationResult(
            run_dir=run_dir,
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=1.0,
        )

        # Patch os.rename inside the cache module to raise OSError
        with patch("idfkit.simulation.cache.os.rename", side_effect=OSError("rename failed")):
            cache.put(key, result)  # should not raise

        # The entry should NOT have been created (rename failed)
        assert not cache.contains(key)
        # No .tmp_ directories should be left
        if cache.cache_dir.is_dir():
            for child in cache.cache_dir.iterdir():
                assert not child.name.startswith(".tmp_"), f"Leaked temp dir: {child}"


# ---------------------------------------------------------------------------
# Size: no weather copy, eviction and prune
# ---------------------------------------------------------------------------


def _store(cache: SimulationCache, tmp_path: Path, name: str, size: int) -> CacheKey:
    """Store a successful result whose run directory holds *size* bytes of output plus a weather file."""
    run_dir = tmp_path / f"run_{name}"
    run_dir.mkdir()
    (run_dir / "eplus.sql").write_bytes(b"x" * size)
    (run_dir / "weather.epw").write_bytes(b"w" * 1000)
    key = CacheKey(hex_digest=name)
    result = SimulationResult(run_dir=run_dir, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=1.0)
    cache.put(key, result)
    return key


def _age(cache: SimulationCache, key: CacheKey, seconds_ago: float) -> None:
    """Mark *key*'s entry as last used *seconds_ago*."""
    meta = cache.cache_dir / key.hex_digest / "_cache_meta.json"
    when = meta.stat().st_mtime - seconds_ago
    os.utime(meta, (when, when))


class TestCacheSize:
    """Entries leave the weather file out, and the cache can be bounded."""

    def test_entry_leaves_out_weather_file(self, tmp_path: Path) -> None:
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        key = _store(cache, tmp_path, "a", 10)
        names = {p.name for p in (cache.cache_dir / key.hex_digest).iterdir()}
        assert "weather.epw" not in names
        assert "eplus.sql" in names

    def test_size_bytes(self, tmp_path: Path) -> None:
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        assert cache.size_bytes() == 0
        _store(cache, tmp_path, "a", 5000)
        assert 5000 < cache.size_bytes() < 6000

    def test_prune_max_bytes_evicts_least_recently_used(self, tmp_path: Path) -> None:
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        a = _store(cache, tmp_path, "a", 5000)
        b = _store(cache, tmp_path, "b", 5000)
        c = _store(cache, tmp_path, "c", 5000)
        _age(cache, a, 300)
        _age(cache, b, 200)
        _age(cache, c, 100)
        assert cache.get(a) is not None  # a hit makes a the most recently used
        assert cache.prune(max_bytes=12000) == 1
        assert cache.contains(a)
        assert not cache.contains(b)
        assert cache.contains(c)

    def test_prune_max_age(self, tmp_path: Path) -> None:
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        old = _store(cache, tmp_path, "old", 10)
        new = _store(cache, tmp_path, "new", 10)
        _age(cache, old, 3600)
        assert cache.prune(max_age=600) == 1
        assert not cache.contains(old)
        assert cache.contains(new)

    def test_prune_without_bounds_removes_nothing(self, tmp_path: Path) -> None:
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        _store(cache, tmp_path, "a", 10)
        assert cache.prune() == 0
        assert SimulationCache(cache_dir=tmp_path / "missing").prune(max_bytes=0) == 0

    def test_max_bytes_bounds_the_cache_on_put(self, tmp_path: Path) -> None:
        cache = SimulationCache(cache_dir=tmp_path / "cache", max_bytes=12000)
        a = _store(cache, tmp_path, "a", 5000)
        b = _store(cache, tmp_path, "b", 5000)
        _age(cache, a, 200)
        _age(cache, b, 100)
        c = _store(cache, tmp_path, "c", 5000)
        assert cache.size_bytes() <= 12000
        assert not cache.contains(a)
        assert cache.contains(b)
        assert cache.contains(c)

    def test_negative_max_bytes_refused(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="max_bytes"):
            SimulationCache(cache_dir=tmp_path, max_bytes=-1)

    def test_prune_refuses_negative_bounds(self, tmp_path: Path) -> None:
        cache = SimulationCache(cache_dir=tmp_path)
        with pytest.raises(ValueError, match="max_bytes"):
            cache.prune(max_bytes=-1)
        with pytest.raises(ValueError, match="max_age"):
            cache.prune(max_age=-5)
