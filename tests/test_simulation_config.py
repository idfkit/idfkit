"""Tests for EnergyPlus installation discovery and configuration."""

from __future__ import annotations

import os
import pickle
import platform
from pathlib import Path
from unittest.mock import patch

import pytest

from idfkit.exceptions import EnergyPlusNotFoundError
from idfkit.simulation.config import (
    EnergyPlusConfig,
    _extract_version,
    _glob_sorted,
    find_energyplus,
    normalize_version,
)

# ---------------------------------------------------------------------------
# EnergyPlusConfig.from_path
# ---------------------------------------------------------------------------


class TestEnergyPlusConfigFromPath:
    """Tests for EnergyPlusConfig.from_path()."""

    def _setup_install(self, tmp_path: Path, dirname: str = "EnergyPlusV24-1-0") -> Path:
        """Create a minimal EnergyPlus installation directory."""
        install_dir = tmp_path / dirname
        install_dir.mkdir()
        exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
        (install_dir / exe_name).touch()
        (install_dir / exe_name).chmod(0o755)
        idd = install_dir / "Energy+.idd"
        idd.write_text("!IDD_Version 24.1.0\n!IDD_BUILD xxxx\n")
        return install_dir

    def test_valid_directory(self, tmp_path: Path) -> None:
        install_dir = self._setup_install(tmp_path)
        config = EnergyPlusConfig.from_path(install_dir)
        assert config.version == (24, 1, 0)
        assert config.install_dir == install_dir.resolve()
        assert config.idd_path.is_file()

    def test_from_executable_path(self, tmp_path: Path) -> None:
        install_dir = self._setup_install(tmp_path)
        exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
        config = EnergyPlusConfig.from_path(install_dir / exe_name)
        assert config.version == (24, 1, 0)

    def test_missing_executable(self, tmp_path: Path) -> None:
        install_dir = tmp_path / "EnergyPlusV24-1-0"
        install_dir.mkdir()
        (install_dir / "Energy+.idd").write_text("!IDD_Version 24.1.0\n")
        with pytest.raises(EnergyPlusNotFoundError):
            EnergyPlusConfig.from_path(install_dir)

    def test_missing_idd(self, tmp_path: Path) -> None:
        install_dir = tmp_path / "EnergyPlusV24-1-0"
        install_dir.mkdir()
        exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
        (install_dir / exe_name).touch()
        with pytest.raises(EnergyPlusNotFoundError):
            EnergyPlusConfig.from_path(install_dir)

    def test_optional_paths_absent(self, tmp_path: Path) -> None:
        install_dir = self._setup_install(tmp_path)
        config = EnergyPlusConfig.from_path(install_dir)
        assert config.weather_dir is None
        assert config.schema_path is None
        assert config.expand_objects_exe is None

    def test_optional_paths_present(self, tmp_path: Path) -> None:
        install_dir = self._setup_install(tmp_path)
        (install_dir / "WeatherData").mkdir()
        (install_dir / "Energy+.schema.epJSON").touch()
        expand_name = "ExpandObjects.exe" if platform.system() == "Windows" else "ExpandObjects"
        (install_dir / expand_name).touch()
        config = EnergyPlusConfig.from_path(install_dir)
        assert config.weather_dir is not None
        assert config.schema_path is not None
        assert config.expand_objects_exe is not None

    def test_version_from_idd_fallback(self, tmp_path: Path) -> None:
        """When dir name has no version, fall back to IDD header."""
        install_dir = self._setup_install(tmp_path, dirname="myenergyplus")
        config = EnergyPlusConfig.from_path(install_dir)
        assert config.version == (24, 1, 0)


# ---------------------------------------------------------------------------
# find_energyplus
# ---------------------------------------------------------------------------


class TestFindEnergyPlus:
    """Tests for find_energyplus()."""

    def _setup_install(self, tmp_path: Path, dirname: str = "EnergyPlusV24-1-0") -> Path:
        install_dir = tmp_path / dirname
        install_dir.mkdir()
        exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
        (install_dir / exe_name).touch()
        (install_dir / exe_name).chmod(0o755)
        (install_dir / "Energy+.idd").write_text("!IDD_Version 24.1.0\n")
        return install_dir

    def test_explicit_path(self, tmp_path: Path) -> None:
        install_dir = self._setup_install(tmp_path)
        config = find_energyplus(path=install_dir)
        assert config.version == (24, 1, 0)

    def test_env_var(self, tmp_path: Path) -> None:
        install_dir = self._setup_install(tmp_path)
        with patch.dict("os.environ", {"ENERGYPLUS_DIR": str(install_dir)}):
            config = find_energyplus()
        assert config.version == (24, 1, 0)

    def test_not_found(self, tmp_path: Path) -> None:
        with (
            patch.dict("os.environ", {}, clear=True),
            patch("idfkit.simulation.config.shutil.which", return_value=None),
            patch("idfkit.simulation.config._platform_search_dirs", return_value=[]),
            pytest.raises(EnergyPlusNotFoundError),
        ):
            find_energyplus()

    def test_version_filter_match(self, tmp_path: Path) -> None:
        install_dir = self._setup_install(tmp_path)
        config = find_energyplus(path=install_dir, version=(24, 1, 0))
        assert config.version == (24, 1, 0)

    def test_version_filter_mismatch(self, tmp_path: Path) -> None:
        install_dir = self._setup_install(tmp_path)
        with pytest.raises(EnergyPlusNotFoundError, match=r"No EnergyPlus 23\.2\.0 found; found 24\.1\.0 at ") as info:
            find_energyplus(path=install_dir, version=(23, 2, 0))
        assert info.value.requested_version == (23, 2, 0)
        assert info.value.found == [((24, 1, 0), str(install_dir.resolve()))]
        # 24.1.0 is newer than 23.2.0, so a model can be migrated to it.
        assert "auto_migrate=True" in str(info.value)

    def test_discovered_other_version_is_named(self, tmp_path: Path) -> None:
        """An install at another version is reported with its version and path, not as 'not found'."""
        install_dir = self._setup_install(tmp_path)
        with (
            patch("idfkit.simulation.config._discovery_candidates", return_value=[install_dir.resolve()]),
            pytest.raises(EnergyPlusNotFoundError) as info,
        ):
            find_energyplus(version="25.1")
        msg = str(info.value)
        assert f"No EnergyPlus 25.1.0 found; found 24.1.0 at {install_dir.resolve()}" in msg
        assert "Could not find an EnergyPlus installation" not in msg
        assert "Drop version=" in msg
        # Nothing installed is newer than 25.1.0, so migration is not offered.
        assert "auto_migrate" not in msg

    def test_searched_locations_are_not_repeated(self, tmp_path: Path) -> None:
        """A path reached by two discovery routes is tried and listed once."""
        missing = (tmp_path / "missing").resolve()
        with (
            patch("idfkit.simulation.config._discovery_candidates", return_value=[missing, missing]),
            pytest.raises(EnergyPlusNotFoundError) as info,
        ):
            find_energyplus(version=(24, 1, 0))
        assert info.value.searched_locations == [str(missing)]
        assert "Could not find an EnergyPlus installation of version 24.1.0" in str(info.value)

    def test_not_found_error_survives_pickling(self) -> None:
        """The message and attributes cross a process boundary intact (multiprocessing)."""
        err = EnergyPlusNotFoundError(["/a"], requested_version=(24, 1, 0), found=[((26, 1, 0), "/b")])
        back = pickle.loads(pickle.dumps(err))  # noqa: S301
        assert str(back) == str(err)
        assert back.searched_locations == ["/a"]
        assert back.requested_version == (24, 1, 0)
        assert back.found == [((26, 1, 0), "/b")]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class TestExtractVersion:
    """Tests for _extract_version()."""

    def test_standard_format(self) -> None:
        assert _extract_version(Path("EnergyPlusV24-1-0")) == (24, 1, 0)

    def test_dotted_format(self) -> None:
        assert _extract_version(Path("EnergyPlus-24.1.0")) == (24, 1, 0)

    def test_no_match(self) -> None:
        assert _extract_version(Path("some-random-dir")) is None


class TestNormalizeVersion:
    """Tests for normalize_version()."""

    def test_tuple_passthrough(self) -> None:
        assert normalize_version((24, 1, 0)) == (24, 1, 0)

    def test_string_three_parts(self) -> None:
        assert normalize_version("24.1.0") == (24, 1, 0)

    def test_string_two_parts(self) -> None:
        assert normalize_version("24.1") == (24, 1, 0)

    def test_string_invalid(self) -> None:
        with pytest.raises(ValueError, match="Cannot parse"):
            normalize_version("24")


class TestGlobSorted:
    """Tests for _glob_sorted()."""

    def test_newest_first(self, tmp_path: Path) -> None:
        for name in ("EnergyPlusV23-1-0", "EnergyPlusV24-1-0", "EnergyPlusV23-2-0"):
            (tmp_path / name).mkdir()
        result = _glob_sorted([tmp_path])
        versions = [_extract_version(p) for p in result]
        assert versions == [(24, 1, 0), (23, 2, 0), (23, 1, 0)]

    def test_empty_dir(self, tmp_path: Path) -> None:
        assert _glob_sorted([tmp_path]) == []

    def test_nonexistent_dir(self) -> None:
        assert _glob_sorted([Path("/nonexistent/path")]) == []


# ---------------------------------------------------------------------------
# Additional coverage for uncovered branches
# ---------------------------------------------------------------------------


class TestFromPathVersionFallback:
    """Tests for EnergyPlusConfig.from_path version extraction edge cases."""

    def _setup_install(self, tmp_path: Path, dirname: str = "energyplus-install") -> Path:
        """Create an install dir with no version in the name (forces IDD fallback)."""
        install_dir = tmp_path / dirname
        install_dir.mkdir()
        exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
        (install_dir / exe_name).touch()
        (install_dir / exe_name).chmod(0o755)
        return install_dir

    def test_version_not_in_dir_or_idd_raises(self, tmp_path: Path) -> None:
        """When neither the dir name nor IDD contain a version, raise."""
        install_dir = self._setup_install(tmp_path)
        idd = install_dir / "Energy+.idd"
        idd.write_text("! No version here\n")
        with pytest.raises(EnergyPlusNotFoundError):
            EnergyPlusConfig.from_path(install_dir)


class TestExtractVersionFromIDD:
    """Tests for _extract_version_from_idd()."""

    def test_oserror_returns_none(self, tmp_path: Path) -> None:
        """OSError reading the IDD should return None."""
        from idfkit.simulation.config import _extract_version_from_idd  # pyright: ignore[reportPrivateUsage]

        result = _extract_version_from_idd(tmp_path / "nonexistent.idd")
        assert result is None

    def test_no_header_returns_none(self, tmp_path: Path) -> None:
        """IDD without the version header returns None."""
        from idfkit.simulation.config import _extract_version_from_idd  # pyright: ignore[reportPrivateUsage]

        idd = tmp_path / "Energy+.idd"
        idd.write_text("! IDD file without version\n")
        result = _extract_version_from_idd(idd)
        assert result is None


class TestLoadCandidate:
    """Tests for _load_candidate() helper."""

    def _setup_install(self, tmp_path: Path, dirname: str = "EnergyPlusV24-1-0") -> Path:
        install_dir = tmp_path / dirname
        install_dir.mkdir()
        exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
        (install_dir / exe_name).touch()
        (install_dir / exe_name).chmod(0o755)
        (install_dir / "Energy+.idd").write_text("!IDD_Version 24.1.0\n")
        return install_dir

    def test_returns_config_whatever_its_version(self, tmp_path: Path) -> None:
        """_load_candidate returns the install it finds; find_energyplus does the version check."""
        from idfkit.simulation.config import _load_candidate  # pyright: ignore[reportPrivateUsage]

        install_dir = self._setup_install(tmp_path)
        result = _load_candidate(install_dir)
        assert result is not None
        assert result.version == (24, 1, 0)

    def test_invalid_path_returns_none(self, tmp_path: Path) -> None:
        """_load_candidate returns None when path doesn't contain EnergyPlus."""
        from idfkit.simulation.config import _load_candidate  # pyright: ignore[reportPrivateUsage]

        result = _load_candidate(tmp_path / "nonexistent")
        assert result is None


class TestPlatformSearchDirs:
    """Tests for _platform_search_dirs() on all platforms."""

    def test_linux_dirs(self) -> None:
        from idfkit.simulation.config import _platform_search_dirs  # pyright: ignore[reportPrivateUsage]

        with patch("idfkit.simulation.config.platform.system", return_value="Linux"):
            dirs = _platform_search_dirs()
        assert len(dirs) >= 2
        assert any(".local" in str(d) or "EnergyPlus" in str(d) for d in dirs)

    def test_darwin_dirs(self) -> None:
        from idfkit.simulation.config import _platform_search_dirs  # pyright: ignore[reportPrivateUsage]

        with patch("idfkit.simulation.config.platform.system", return_value="Darwin"):
            dirs = _platform_search_dirs()
        assert any("Applications" in str(d) for d in dirs)

    def test_windows_dirs(self) -> None:
        from idfkit.simulation.config import _platform_search_dirs  # pyright: ignore[reportPrivateUsage]

        with (
            patch("idfkit.simulation.config.platform.system", return_value="Windows"),
            patch.dict("os.environ", {"ProgramFiles": "C:\\Program Files", "ProgramW6432": "C:\\Program Files"}),
        ):
            dirs = _platform_search_dirs()
        assert len(dirs) >= 1
        assert any("Program Files" in str(d) for d in dirs)

    def test_windows_includes_system_drive_root(self, tmp_path: Path) -> None:
        """Drive root (e.g. C:\\) should be included on Windows for default installs."""
        from idfkit.simulation.config import _platform_search_dirs  # pyright: ignore[reportPrivateUsage]

        with (
            patch("idfkit.simulation.config.platform.system", return_value="Windows"),
            patch.dict("os.environ", {"SystemDrive": "C:", "ProgramFiles": str(tmp_path)}, clear=True),
        ):
            dirs = _platform_search_dirs()

        assert Path("C:" + os.sep) in dirs

    def test_windows_system_drive_fallback(self) -> None:
        """When SystemDrive is absent, fall back to C:\\."""
        from idfkit.simulation.config import _platform_search_dirs  # pyright: ignore[reportPrivateUsage]

        env_without_system_drive = {k: v for k, v in os.environ.items() if k != "SystemDrive"}
        with (
            patch("idfkit.simulation.config.platform.system", return_value="Windows"),
            patch.dict("os.environ", env_without_system_drive, clear=True),
        ):
            dirs = _platform_search_dirs()

        assert Path("C:" + os.sep) in dirs

    def test_unknown_platform_empty(self) -> None:
        from idfkit.simulation.config import _platform_search_dirs  # pyright: ignore[reportPrivateUsage]

        with patch("idfkit.simulation.config.platform.system", return_value="FreeBSD"):
            dirs = _platform_search_dirs()
        assert dirs == []


class TestFindEnergyPlusPathDiscovery:
    """Tests for find_energyplus() discovery ordering."""

    def _setup_install(self, tmp_path: Path, dirname: str = "EnergyPlusV24-1-0") -> Path:
        install_dir = tmp_path / dirname
        install_dir.mkdir()
        exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
        exe = install_dir / exe_name
        exe.touch()
        exe.chmod(0o755)
        (install_dir / "Energy+.idd").write_text("!IDD_Version 24.1.0\n")
        return install_dir

    def test_which_discovery(self, tmp_path: Path) -> None:
        """find_energyplus finds EnergyPlus via shutil.which."""
        install_dir = self._setup_install(tmp_path)
        exe_name = "energyplus.exe" if platform.system() == "Windows" else "energyplus"
        exe_path = str(install_dir / exe_name)
        with (
            patch.dict("os.environ", {}, clear=True),
            patch("idfkit.simulation.config.shutil.which", return_value=exe_path),
            patch("idfkit.simulation.config._platform_search_dirs", return_value=[]),
        ):
            config = find_energyplus()
        assert config.version == (24, 1, 0)
