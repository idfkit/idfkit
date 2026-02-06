"""Tests for the expand_objects, run_slab_preprocessor, and run_basement_preprocessor functionality."""

from __future__ import annotations

import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit import IDFDocument, new_document
from idfkit.exceptions import ExpandObjectsError
from idfkit.objects import IDFObject
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.expand import (
    _has_basement_objects,
    _has_slab_objects,
    _needs_expansion,
    expand_objects,
    run_basement_preprocessor,
    run_slab_preprocessor,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def model_with_hvac_template() -> IDFDocument:
    """Create a document with an HVACTemplate object."""
    doc = new_document(version=(24, 1, 0))
    doc.add("Zone", "Office", {"x_origin": 0.0, "y_origin": 0.0, "z_origin": 0.0})
    doc.add(
        "HVACTemplate:Zone:IdealLoadsAirSystem",
        "Office Ideal Loads",
        {"zone_name": "Office"},
        validate=False,
    )
    return doc


@pytest.fixture
def mock_config(tmp_path: Path) -> EnergyPlusConfig:
    """Create a mock EnergyPlusConfig with fake preprocessor executables."""
    exe = tmp_path / "energyplus"
    exe.touch()
    idd = tmp_path / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")

    # ExpandObjects
    expand_exe = tmp_path / "ExpandObjects"
    expand_exe.touch()
    expand_exe.chmod(0o755)

    # Slab & Basement
    preprocess = tmp_path / "PreProcess" / "GrndTempCalc"
    preprocess.mkdir(parents=True)
    slab_exe = preprocess / "Slab"
    slab_exe.touch()
    slab_exe.chmod(0o755)
    (preprocess / "SlabGHT.idd").write_text("! Slab IDD\n")
    basement_exe = preprocess / "Basement"
    basement_exe.touch()
    basement_exe.chmod(0o755)
    (preprocess / "BasementGHT.idd").write_text("! Basement IDD\n")

    return EnergyPlusConfig(
        executable=exe,
        version=(24, 1, 0),
        install_dir=tmp_path,
        idd_path=idd,
    )


def _fake_expand_run(expanded_content: str = "Version, 24.1;\n\nZone,\n  Office;\n"):
    """Return a fake subprocess.run side-effect that writes expanded.idf."""

    def side_effect(cmd: list[str], **kwargs: object) -> MagicMock:
        cwd = Path(str(kwargs.get("cwd", "")))
        (cwd / "expanded.idf").write_text(expanded_content)
        result = MagicMock()
        result.returncode = 0
        result.stdout = ""
        result.stderr = ""
        return result

    return side_effect


# ---------------------------------------------------------------------------
# expand_objects tests
# ---------------------------------------------------------------------------


class TestExpandObjects:
    def test_calls_executable(
        self,
        model_with_hvac_template: IDFDocument,
        mock_config: EnergyPlusConfig,
    ) -> None:
        expanded_idf_content = """\
Version, 24.1;

Zone,
  Office,
  0,
  0, 0, 0,
  1,
  1;

ZoneHVAC:IdealLoadsAirSystem,
  Office Ideal Loads Air,
  ,
  ,
  ,
  50,
  ,
  13,
  ,
  ,
  ,
  ,
  ,
  ;
"""
        with patch("idfkit.simulation.expand.subprocess.run", side_effect=_fake_expand_run(expanded_idf_content)):
            expanded = expand_objects(model_with_hvac_template, energyplus=mock_config)

        assert "ZoneHVAC:IdealLoadsAirSystem" in expanded
        assert expanded["ZoneHVAC:IdealLoadsAirSystem"].first().name == "Office Ideal Loads Air"

    def test_no_expand_exe_raises(self, model_with_hvac_template: IDFDocument, tmp_path: Path) -> None:
        exe = tmp_path / "energyplus"
        exe.touch()
        idd = tmp_path / "Energy+.idd"
        idd.write_text("!IDD_Version 24.1.0\n")
        config = EnergyPlusConfig(executable=exe, version=(24, 1, 0), install_dir=tmp_path, idd_path=idd)

        with pytest.raises(ExpandObjectsError, match="ExpandObjects executable not found"):
            expand_objects(model_with_hvac_template, energyplus=config)

    def test_no_expanded_file_raises(
        self, model_with_hvac_template: IDFDocument, mock_config: EnergyPlusConfig
    ) -> None:
        proc = MagicMock()
        proc.returncode = 1
        proc.stderr = "some error"

        with (
            patch("idfkit.simulation.expand.subprocess.run", return_value=proc),
            pytest.raises(ExpandObjectsError, match=r"did not produce expanded\.idf"),
        ):
            expand_objects(model_with_hvac_template, energyplus=mock_config)

    def test_timeout_raises(self, model_with_hvac_template: IDFDocument, mock_config: EnergyPlusConfig) -> None:
        import subprocess

        with (
            patch(
                "idfkit.simulation.expand.subprocess.run",
                side_effect=subprocess.TimeoutExpired(cmd="ExpandObjects", timeout=1),
            ),
            pytest.raises(ExpandObjectsError, match="timed out"),
        ):
            expand_objects(model_with_hvac_template, energyplus=mock_config, timeout=1.0)

    def test_os_error_raises(self, model_with_hvac_template: IDFDocument, mock_config: EnergyPlusConfig) -> None:
        with (
            patch("idfkit.simulation.expand.subprocess.run", side_effect=OSError("Permission denied")),
            pytest.raises(ExpandObjectsError, match="Failed to start ExpandObjects"),
        ):
            expand_objects(model_with_hvac_template, energyplus=mock_config)

    def test_auto_discovers_energyplus(
        self, model_with_hvac_template: IDFDocument, mock_config: EnergyPlusConfig
    ) -> None:
        with (
            patch("idfkit.simulation.expand.find_energyplus", return_value=mock_config) as mock_find,
            patch("idfkit.simulation.expand.subprocess.run", side_effect=_fake_expand_run()),
        ):
            expand_objects(model_with_hvac_template)
        mock_find.assert_called_once()

    def test_document_expand_method(self, model_with_hvac_template: IDFDocument, mock_config: EnergyPlusConfig) -> None:
        with patch("idfkit.simulation.expand.subprocess.run", side_effect=_fake_expand_run()):
            expanded = model_with_hvac_template.expand(energyplus=mock_config)
        assert isinstance(expanded, IDFDocument)
        assert "Zone" in expanded

    def test_does_not_mutate_original(
        self, model_with_hvac_template: IDFDocument, mock_config: EnergyPlusConfig
    ) -> None:
        original_types = set(model_with_hvac_template.keys())

        with patch("idfkit.simulation.expand.subprocess.run", side_effect=_fake_expand_run()):
            expand_objects(model_with_hvac_template, energyplus=mock_config)

        assert set(model_with_hvac_template.keys()) == original_types
        assert "HVACTemplate:Zone:IdealLoadsAirSystem" in model_with_hvac_template

    def test_skips_subprocess_when_nothing_to_expand(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Office", {"x_origin": 0.0})

        with patch("idfkit.simulation.expand.subprocess.run") as mock_run:
            result = expand_objects(doc)

        mock_run.assert_not_called()
        assert isinstance(result, IDFDocument)
        assert result is not doc


# ---------------------------------------------------------------------------
# Detection helper tests
# ---------------------------------------------------------------------------


class TestNeedsExpansion:
    def test_uses_schema_group(self, model_with_hvac_template: IDFDocument) -> None:
        assert model_with_hvac_template.schema is not None
        assert _needs_expansion(model_with_hvac_template) is True

    def test_ignores_ground_heat_transfer(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Control", "", {"name": "test", "run_basement_preprocessor": "No"}, validate=False)
        assert _needs_expansion(doc) is False

    def test_false_for_plain_model(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Office", {"x_origin": 0.0})
        assert _needs_expansion(doc) is False

    def test_falls_back_to_prefix_without_schema(self) -> None:
        doc = IDFDocument(version=(24, 1, 0), schema=None)
        doc.addidfobject(IDFObject(obj_type="HVACTemplate:Zone:IdealLoadsAirSystem", name="Test", data={}))
        assert _needs_expansion(doc) is True

    def test_prefix_fallback_negative(self) -> None:
        doc = IDFDocument(version=(24, 1, 0), schema=None)
        doc.addidfobject(IDFObject(obj_type="Zone", name="Office", data={}))
        assert _needs_expansion(doc) is False


class TestHasSlabObjects:
    def test_detects_slab_objects(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
        assert _has_slab_objects(doc) is True

    def test_false_for_basement_only(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Basement:SimParameters", "", {}, validate=False)
        assert _has_slab_objects(doc) is False

    def test_false_for_plain_model(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Office", {"x_origin": 0.0})
        assert _has_slab_objects(doc) is False

    def test_prefix_fallback(self) -> None:
        doc = IDFDocument(version=(24, 1, 0), schema=None)
        doc.addidfobject(IDFObject(obj_type="GroundHeatTransfer:Slab:Materials", name="", data={}))
        assert _has_slab_objects(doc) is True


class TestHasBasementObjects:
    def test_detects_basement_objects(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Basement:SimParameters", "", {}, validate=False)
        assert _has_basement_objects(doc) is True

    def test_false_for_slab_only(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
        assert _has_basement_objects(doc) is False

    def test_false_for_plain_model(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Office", {"x_origin": 0.0})
        assert _has_basement_objects(doc) is False


# ---------------------------------------------------------------------------
# run_slab_preprocessor tests
# ---------------------------------------------------------------------------


class TestRunSlabPreprocessor:
    def test_skips_when_no_slab_objects(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Office", {"x_origin": 0.0})

        with patch("idfkit.simulation.expand.subprocess.run") as mock_run:
            result = run_slab_preprocessor(doc)

        mock_run.assert_not_called()
        assert result is not doc
        assert "Zone" in result

    def test_runs_expand_then_slab(self, mock_config: EnergyPlusConfig) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
        doc.add("GroundHeatTransfer:Slab:BldgProps", "", {}, validate=False)
        doc.add("GroundHeatTransfer:Control", "", {"run_slab_preprocessor": "Yes"}, validate=False)
        doc.add("Zone", "Office", {"x_origin": 0.0})

        calls: list[str] = []

        def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
            cwd = Path(str(kwargs.get("cwd", "")))
            exe_name = Path(cmd[0]).name
            calls.append(exe_name)

            if exe_name == "ExpandObjects":
                (cwd / "expanded.idf").write_text("Version, 24.1;\n\nZone,\n  Office;\n")
                (cwd / "GHTIn.idf").write_text("! slab input extracted\n")
            elif exe_name == "Slab":
                (cwd / "SLABSurfaceTemps.TXT").write_text(
                    "Site:GroundTemperature:BuildingSurface,\n  18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18;\n"
                )

            result = MagicMock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run):
            expanded = run_slab_preprocessor(doc, energyplus=mock_config)

        assert calls == ["ExpandObjects", "Slab"]
        assert "Site:GroundTemperature:BuildingSurface" in expanded

    def test_raises_when_ght_input_missing(self, mock_config: EnergyPlusConfig) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)

        with (
            patch("idfkit.simulation.expand.subprocess.run", side_effect=_fake_expand_run()),
            pytest.raises(ExpandObjectsError, match=r"did not produce GHTIn\.idf"),
        ):
            run_slab_preprocessor(doc, energyplus=mock_config)

    def test_raises_when_slab_exe_missing(self, tmp_path: Path) -> None:
        exe = tmp_path / "energyplus"
        exe.touch()
        idd = tmp_path / "Energy+.idd"
        idd.write_text("!IDD_Version 24.1.0\n")
        expand_exe = tmp_path / "ExpandObjects"
        expand_exe.touch()
        # No PreProcess/GrndTempCalc/Slab
        config = EnergyPlusConfig(executable=exe, version=(24, 1, 0), install_dir=tmp_path, idd_path=idd)

        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)

        def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
            cwd = Path(str(kwargs.get("cwd", "")))
            (cwd / "expanded.idf").write_text("Version, 24.1;\n")
            (cwd / "GHTIn.idf").write_text("! input\n")
            result = MagicMock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with (
            patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run),
            pytest.raises(ExpandObjectsError, match="Slab preprocessor not found"),
        ):
            run_slab_preprocessor(doc, energyplus=config)

    def test_copies_idd_to_run_dir(self, mock_config: EnergyPlusConfig) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)

        idd_copied = []

        original_copy2 = shutil.copy2

        def track_copy(src: object, dst: object) -> object:
            idd_copied.append(str(dst))
            return original_copy2(src, dst)  # type: ignore[arg-type]

        def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
            cwd = Path(str(kwargs.get("cwd", "")))
            exe_name = Path(cmd[0]).name
            if exe_name == "ExpandObjects":
                (cwd / "expanded.idf").write_text("Version, 24.1;\n")
                (cwd / "GHTIn.idf").write_text("! input\n")
            elif exe_name == "Slab":
                (cwd / "SLABSurfaceTemps.TXT").write_text("! temps\n")
            result = MagicMock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with (
            patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run),
            patch("idfkit.simulation.expand.shutil.copy2", side_effect=track_copy),
        ):
            run_slab_preprocessor(doc, energyplus=mock_config)

        assert len(idd_copied) == 1
        assert idd_copied[0].endswith("SlabGHT.idd")

    def test_weather_file_copied(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)

        epw = tmp_path / "test.epw"
        epw.write_text("LOCATION,Chicago\n")

        run_dirs: list[Path] = []

        def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
            cwd = Path(str(kwargs.get("cwd", "")))
            run_dirs.append(cwd)
            exe_name = Path(cmd[0]).name
            if exe_name == "ExpandObjects":
                (cwd / "expanded.idf").write_text("Version, 24.1;\n")
                (cwd / "GHTIn.idf").write_text("! input\n")
            elif exe_name == "Slab":
                (cwd / "SLABSurfaceTemps.TXT").write_text("! temps\n")
            result = MagicMock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run):
            run_slab_preprocessor(doc, energyplus=mock_config, weather=epw)

        assert len(run_dirs) > 0
        assert (run_dirs[0] / "in.epw").is_file()
        assert (run_dirs[0] / "in.epw").read_text() == "LOCATION,Chicago\n"


# ---------------------------------------------------------------------------
# run_basement_preprocessor tests
# ---------------------------------------------------------------------------


class TestRunBasementPreprocessor:
    def test_skips_when_no_basement_objects(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Office", {"x_origin": 0.0})

        with patch("idfkit.simulation.expand.subprocess.run") as mock_run:
            result = run_basement_preprocessor(doc)

        mock_run.assert_not_called()
        assert result is not doc

    def test_runs_expand_then_basement(self, mock_config: EnergyPlusConfig) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Basement:SimParameters", "", {}, validate=False)
        doc.add("GroundHeatTransfer:Control", "", {"run_basement_preprocessor": "Yes"}, validate=False)
        doc.add("Zone", "Office", {"x_origin": 0.0})

        calls: list[str] = []

        def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
            cwd = Path(str(kwargs.get("cwd", "")))
            exe_name = Path(cmd[0]).name
            calls.append(exe_name)

            if exe_name == "ExpandObjects":
                (cwd / "expanded.idf").write_text("Version, 24.1;\n\nZone,\n  Office;\n")
                (cwd / "BasementGHTIn.idf").write_text("! basement input extracted\n")
            elif exe_name == "Basement":
                (cwd / "EPObjects.TXT").write_text(
                    "Site:GroundTemperature:BuildingSurface,\n  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16;\n"
                )

            result = MagicMock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run):
            expanded = run_basement_preprocessor(doc, energyplus=mock_config)

        assert calls == ["ExpandObjects", "Basement"]
        assert "Site:GroundTemperature:BuildingSurface" in expanded

    def test_raises_when_basement_input_missing(self, mock_config: EnergyPlusConfig) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Basement:SimParameters", "", {}, validate=False)

        with (
            patch("idfkit.simulation.expand.subprocess.run", side_effect=_fake_expand_run()),
            pytest.raises(ExpandObjectsError, match=r"did not produce BasementGHTIn\.idf"),
        ):
            run_basement_preprocessor(doc, energyplus=mock_config)

    def test_weather_file_copied(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Basement:SimParameters", "", {}, validate=False)
        doc.add("GroundHeatTransfer:Control", "", {"run_basement_preprocessor": "Yes"}, validate=False)
        doc.add("Zone", "Office", {"x_origin": 0.0})

        epw = tmp_path / "test.epw"
        epw.write_text("LOCATION,Chicago\n")

        run_dirs: list[Path] = []

        def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
            cwd = Path(str(kwargs.get("cwd", "")))
            run_dirs.append(cwd)
            exe_name = Path(cmd[0]).name
            if exe_name == "ExpandObjects":
                (cwd / "expanded.idf").write_text("Version, 24.1;\n\nZone,\n  Office;\n")
                (cwd / "BasementGHTIn.idf").write_text("! basement input extracted\n")
            elif exe_name == "Basement":
                (cwd / "EPObjects.TXT").write_text(
                    "Site:GroundTemperature:BuildingSurface,\n  16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16;\n"
                )
            result = MagicMock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run):
            expanded = run_basement_preprocessor(doc, energyplus=mock_config, weather=epw)

        assert len(run_dirs) > 0
        assert (run_dirs[0] / "in.epw").is_file()
        assert "Site:GroundTemperature:BuildingSurface" in expanded

    def test_raises_when_weather_file_missing(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Basement:SimParameters", "", {}, validate=False)

        with pytest.raises(ExpandObjectsError, match="Weather file not found"):
            run_basement_preprocessor(doc, energyplus=mock_config, weather=tmp_path / "nonexistent.epw")

    def test_raises_when_basement_exe_missing(self, tmp_path: Path) -> None:
        exe = tmp_path / "energyplus"
        exe.touch()
        idd = tmp_path / "Energy+.idd"
        idd.write_text("!IDD_Version 24.1.0\n")
        expand_exe = tmp_path / "ExpandObjects"
        expand_exe.touch()
        config = EnergyPlusConfig(executable=exe, version=(24, 1, 0), install_dir=tmp_path, idd_path=idd)

        doc = new_document(version=(24, 1, 0))
        doc.add("GroundHeatTransfer:Basement:SimParameters", "", {}, validate=False)

        def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
            cwd = Path(str(kwargs.get("cwd", "")))
            (cwd / "expanded.idf").write_text("Version, 24.1;\n")
            (cwd / "BasementGHTIn.idf").write_text("! input\n")
            result = MagicMock()
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
            return result

        with (
            patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run),
            pytest.raises(ExpandObjectsError, match="Basement preprocessor not found"),
        ):
            run_basement_preprocessor(doc, energyplus=config)


# ---------------------------------------------------------------------------
# EnergyPlusConfig property tests
# ---------------------------------------------------------------------------


class TestConfigProperties:
    def test_slab_exe(self, mock_config: EnergyPlusConfig) -> None:
        assert mock_config.slab_exe is not None
        assert mock_config.slab_exe.name == "Slab"

    def test_slab_idd(self, mock_config: EnergyPlusConfig) -> None:
        assert mock_config.slab_idd is not None
        assert mock_config.slab_idd.name == "SlabGHT.idd"

    def test_basement_exe(self, mock_config: EnergyPlusConfig) -> None:
        assert mock_config.basement_exe is not None
        assert mock_config.basement_exe.name == "Basement"

    def test_basement_idd(self, mock_config: EnergyPlusConfig) -> None:
        assert mock_config.basement_idd is not None
        assert mock_config.basement_idd.name == "BasementGHT.idd"

    def test_missing_preprocessors(self, tmp_path: Path) -> None:
        exe = tmp_path / "energyplus"
        exe.touch()
        idd = tmp_path / "Energy+.idd"
        idd.write_text("!IDD_Version 24.1.0\n")
        config = EnergyPlusConfig(executable=exe, version=(24, 1, 0), install_dir=tmp_path, idd_path=idd)

        assert config.slab_exe is None
        assert config.slab_idd is None
        assert config.basement_exe is None
        assert config.basement_idd is None
