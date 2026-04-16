"""Tests for EnergyPlusConfig transition-binary discovery."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.simulation.config import EnergyPlusConfig


def _make_config(install_dir: Path) -> EnergyPlusConfig:
    """Create a bare-bones ``EnergyPlusConfig`` rooted at *install_dir*."""
    exe = install_dir / "energyplus"
    exe.touch()
    exe.chmod(0o755)
    idd = install_dir / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")
    return EnergyPlusConfig(
        executable=exe,
        version=(24, 1, 0),
        install_dir=install_dir,
        idd_path=idd,
    )


class TestVersionUpdaterDir:
    def test_returns_none_when_missing(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        assert config.version_updater_dir is None

    def test_returns_directory_when_present(self, tmp_path: Path) -> None:
        updater = tmp_path / "PreProcess" / "IDFVersionUpdater"
        updater.mkdir(parents=True)
        config = _make_config(tmp_path)
        assert config.version_updater_dir == updater


class TestTransitionExe:
    @pytest.fixture
    def config_with_updater(self, tmp_path: Path) -> tuple[EnergyPlusConfig, Path]:
        updater = tmp_path / "PreProcess" / "IDFVersionUpdater"
        updater.mkdir(parents=True)
        return _make_config(tmp_path), updater

    def test_returns_none_when_binary_missing(
        self,
        config_with_updater: tuple[EnergyPlusConfig, Path],
    ) -> None:
        config, _ = config_with_updater
        assert config.transition_exe((24, 1, 0), (24, 2, 0)) is None

    def test_returns_path_for_exact_match(
        self,
        config_with_updater: tuple[EnergyPlusConfig, Path],
    ) -> None:
        config, updater = config_with_updater
        binary = updater / "Transition-V24-1-0-to-V24-2-0"
        binary.touch()
        assert config.transition_exe((24, 1, 0), (24, 2, 0)) == binary

    def test_returns_none_when_updater_dir_missing(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        assert config.transition_exe((24, 1, 0), (24, 2, 0)) is None


class TestTransitionIdd:
    def test_returns_path_when_present(self, tmp_path: Path) -> None:
        updater = tmp_path / "PreProcess" / "IDFVersionUpdater"
        updater.mkdir(parents=True)
        idd = updater / "V24-1-0-Energy+.idd"
        idd.write_text("! dummy\n")
        config = _make_config(tmp_path)
        assert config.transition_idd((24, 1, 0)) == idd

    def test_returns_none_when_absent(self, tmp_path: Path) -> None:
        updater = tmp_path / "PreProcess" / "IDFVersionUpdater"
        updater.mkdir(parents=True)
        config = _make_config(tmp_path)
        assert config.transition_idd((24, 1, 0)) is None
