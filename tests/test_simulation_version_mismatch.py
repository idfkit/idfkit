"""Tests for the ``run_simulation`` pre-flight version check."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit import load_idf, new_document
from idfkit.document import IDFDocument
from idfkit.exceptions import SimulationError, UnsupportedVersionError, VersionMismatchError
from idfkit.migration.report import MigrationReport
from idfkit.simulation._common import async_resolve_version_mismatch, resolve_version_mismatch
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.runner import simulate


@pytest.fixture
def ep_config(tmp_path: Path) -> EnergyPlusConfig:
    """Minimal EnergyPlusConfig at v24.2.0."""
    exe = tmp_path / "energyplus"
    exe.touch()
    exe.chmod(0o755)
    idd = tmp_path / "Energy+.idd"
    idd.write_text("!IDD_Version 24.2.0\n")
    return EnergyPlusConfig(
        executable=exe,
        version=(24, 2, 0),
        install_dir=tmp_path,
        idd_path=idd,
    )


class TestResolveVersionMismatch:
    def test_matching_versions_pass_through(self, ep_config: EnergyPlusConfig) -> None:
        model = new_document(version=(24, 2, 0))
        result, report = resolve_version_mismatch(model=model, config=ep_config, auto_migrate=False)
        assert result is model
        assert report is None

    def test_forward_mismatch_without_auto_migrate_raises(
        self,
        ep_config: EnergyPlusConfig,
    ) -> None:
        model = new_document(version=(24, 1, 0))
        with pytest.raises(VersionMismatchError) as exc_info:
            resolve_version_mismatch(model=model, config=ep_config, auto_migrate=False)

        err = exc_info.value
        assert err.current == (24, 1, 0)
        assert err.target == (24, 2, 0)
        assert err.direction == "forward"
        assert err.migration_chain == (((24, 1, 0), (24, 2, 0)),)

    def test_backward_mismatch_always_raises(
        self,
        ep_config: EnergyPlusConfig,
    ) -> None:
        model = new_document(version=(25, 1, 0))
        with pytest.raises(VersionMismatchError) as exc_info:
            resolve_version_mismatch(model=model, config=ep_config, auto_migrate=True)

        assert exc_info.value.direction == "backward"
        assert exc_info.value.migration_chain == ()


def _config_at(tmp_path: Path, version: tuple[int, int, int]) -> EnergyPlusConfig:
    exe = tmp_path / "energyplus"
    exe.touch()
    exe.chmod(0o755)
    idd = tmp_path / "Energy+.idd"
    idd.write_text(f"!IDD_Version {version[0]}.{version[1]}.{version[2]}\n")
    return EnergyPlusConfig(executable=exe, version=version, install_dir=tmp_path, idd_path=idd)


def _load_two_component_9_0(tmp_path: Path) -> IDFDocument:
    """A document loaded from a file headed ``Version, 9.0;``: it reads as 9.0.0, the release is 9.0.1."""
    path = tmp_path / "v9_0.idf"
    path.write_text("Version,\n  9.0;\n", encoding="latin-1")
    doc = load_idf(path)
    assert doc.version == (9, 0, 0)
    return doc


class TestTwoComponentModelVersion:
    """A ``Version, 9.0;`` model is matched to the 9.0.1 release, as schema selection matches it."""

    def test_matches_installed_release(self, tmp_path: Path) -> None:
        model = _load_two_component_9_0(tmp_path)
        result, report = resolve_version_mismatch(
            model=model, config=_config_at(tmp_path, (9, 0, 1)), auto_migrate=False
        )
        assert result is model
        assert report is None

    @pytest.mark.asyncio
    async def test_matches_installed_release_async(self, tmp_path: Path) -> None:
        model = _load_two_component_9_0(tmp_path)
        result, report = await async_resolve_version_mismatch(
            model=model, config=_config_at(tmp_path, (9, 0, 1)), auto_migrate=False
        )
        assert result is model
        assert report is None

    def test_mismatch_reports_the_release_chain(self, tmp_path: Path) -> None:
        model = _load_two_component_9_0(tmp_path)
        with pytest.raises(VersionMismatchError) as exc_info:
            resolve_version_mismatch(model=model, config=_config_at(tmp_path, (9, 2, 0)), auto_migrate=False)

        err = exc_info.value
        assert err.current == (9, 0, 1)
        assert err.target == (9, 2, 0)
        assert err.migration_chain == (((9, 0, 1), (9, 1, 0)), ((9, 1, 0), (9, 2, 0)))
        assert "Model version 9.0.1" in str(err)

    @patch("idfkit.migration.runner.migrate")
    def test_auto_migrate_migrates_from_the_release(self, mock_migrate: MagicMock, tmp_path: Path) -> None:
        migrated = new_document(version=(9, 2, 0))
        mock_migrate.return_value = MagicMock(spec=MigrationReport, migrated_model=migrated)
        model = _load_two_component_9_0(tmp_path)
        config = _config_at(tmp_path, (9, 2, 0))

        result, report = resolve_version_mismatch(model=model, config=config, auto_migrate=True)

        assert result is migrated
        assert report is mock_migrate.return_value
        mock_migrate.assert_called_once_with(model, target_version=(9, 2, 0), energyplus=config)

    @pytest.mark.asyncio
    @patch("idfkit.migration.async_runner.async_migrate")
    async def test_auto_migrate_migrates_from_the_release_async(self, mock_migrate: MagicMock, tmp_path: Path) -> None:
        migrated = new_document(version=(9, 2, 0))
        mock_migrate.return_value = MagicMock(spec=MigrationReport, migrated_model=migrated)
        model = _load_two_component_9_0(tmp_path)
        config = _config_at(tmp_path, (9, 2, 0))

        result, _ = await async_resolve_version_mismatch(model=model, config=config, auto_migrate=True)

        assert result is migrated
        mock_migrate.assert_called_once_with(model, target_version=(9, 2, 0), energyplus=config)

    def test_unsupported_model_version_still_raises(self, ep_config: EnergyPlusConfig) -> None:
        model = IDFDocument(version=(8, 8, 0))
        with pytest.raises(UnsupportedVersionError):
            resolve_version_mismatch(model=model, config=ep_config, auto_migrate=True)

    def test_newer_unsupported_model_is_a_backward_mismatch(self, ep_config: EnergyPlusConfig) -> None:
        model = IDFDocument(version=(27, 1, 0))
        with pytest.raises(VersionMismatchError) as exc_info:
            resolve_version_mismatch(model=model, config=ep_config, auto_migrate=True)
        assert exc_info.value.current == (27, 1, 0)
        assert exc_info.value.direction == "backward"


class TestSimulateRaisesOnMismatch:
    @patch("idfkit.simulation.runner.resolve_config")
    def test_simulate_raises_version_mismatch_by_default(
        self,
        mock_resolve: MagicMock,
        ep_config: EnergyPlusConfig,
        tmp_path: Path,
    ) -> None:
        mock_resolve.return_value = ep_config
        model = new_document(version=(24, 1, 0))
        weather = tmp_path / "weather.epw"
        weather.write_text("dummy")

        with pytest.raises(VersionMismatchError):
            simulate(model, weather, energyplus=ep_config)


class TestSimulateMigrationWithoutWeather:
    @patch("idfkit.simulation.runner.subprocess.run")
    @patch("idfkit.migration.runner.migrate")
    def test_migration_without_weather(
        self,
        mock_migrate: MagicMock,
        mock_run: MagicMock,
        ep_config: EnergyPlusConfig,
        tmp_path: Path,
    ) -> None:
        mock_migrate.return_value = MagicMock(migrated_model=new_document(version=(24, 2, 0)))
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        model = new_document(version=(24, 1, 0))

        result = simulate(
            model,
            design_day=True,
            auto_migrate=True,
            energyplus=ep_config,
            output_dir=tmp_path / "run",
        )

        mock_migrate.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "-D" in cmd
        assert "-w" not in cmd
        assert result.migration_report is mock_migrate.return_value

    @patch("idfkit.simulation.runner.subprocess.run")
    @patch("idfkit.migration.runner.migrate")
    def test_default_weather_refused_before_migration(
        self,
        mock_migrate: MagicMock,
        mock_run: MagicMock,
        ep_config: EnergyPlusConfig,
        tmp_path: Path,
    ) -> None:
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        (run_dir / "in.epw").write_text("LOCATION,Elsewhere\n")

        with pytest.raises(SimulationError, match=r"contains in\.epw"):
            simulate(
                new_document(version=(24, 1, 0)),
                design_day=True,
                auto_migrate=True,
                energyplus=ep_config,
                output_dir=run_dir,
            )

        mock_migrate.assert_not_called()
        mock_run.assert_not_called()
