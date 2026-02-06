"""Tests for the expand_objects functionality."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit import IDFDocument, new_document
from idfkit.exceptions import ExpandObjectsError
from idfkit.objects import IDFObject
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.expand import _needs_expansion, expand_objects


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
    """Create a mock EnergyPlusConfig with a fake ExpandObjects executable."""
    exe = tmp_path / "energyplus"
    exe.touch()
    idd = tmp_path / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")
    expand_exe = tmp_path / "ExpandObjects"
    expand_exe.touch()
    expand_exe.chmod(0o755)
    return EnergyPlusConfig(
        executable=exe,
        version=(24, 1, 0),
        install_dir=tmp_path,
        idd_path=idd,
    )


def test_expand_objects_calls_executable(
    model_with_hvac_template: IDFDocument,
    mock_config: EnergyPlusConfig,
    tmp_path: Path,
) -> None:
    """ExpandObjects executable is invoked in a temp directory with in.idf."""
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

    def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
        cwd = kwargs.get("cwd", "")
        expanded = Path(str(cwd)) / "expanded.idf"
        expanded.write_text(expanded_idf_content)
        result = MagicMock()
        result.returncode = 0
        result.stdout = ""
        result.stderr = ""
        return result

    with patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run):
        expanded = expand_objects(model_with_hvac_template, energyplus=mock_config)

    # The original HVACTemplate should be gone, replaced by detailed object
    assert "ZoneHVAC:IdealLoadsAirSystem" in expanded
    assert len(expanded["ZoneHVAC:IdealLoadsAirSystem"]) == 1
    assert expanded["ZoneHVAC:IdealLoadsAirSystem"].first().name == "Office Ideal Loads Air"


def test_expand_objects_no_expand_exe_raises(
    model_with_hvac_template: IDFDocument,
    tmp_path: Path,
) -> None:
    """Raise ExpandObjectsError when ExpandObjects is not in the installation."""
    exe = tmp_path / "energyplus"
    exe.touch()
    idd = tmp_path / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")
    # No ExpandObjects executable created
    config = EnergyPlusConfig(
        executable=exe,
        version=(24, 1, 0),
        install_dir=tmp_path,
        idd_path=idd,
    )

    with pytest.raises(ExpandObjectsError, match="ExpandObjects executable not found"):
        expand_objects(model_with_hvac_template, energyplus=config)


def test_expand_objects_no_expanded_file_raises(
    model_with_hvac_template: IDFDocument,
    mock_config: EnergyPlusConfig,
) -> None:
    """Raise ExpandObjectsError when expanded.idf is not produced."""
    proc = MagicMock()
    proc.returncode = 1
    proc.stderr = "some error"

    with (
        patch("idfkit.simulation.expand.subprocess.run", return_value=proc),
        pytest.raises(ExpandObjectsError, match=r"did not produce expanded\.idf"),
    ):
        expand_objects(model_with_hvac_template, energyplus=mock_config)


def test_expand_objects_timeout_raises(
    model_with_hvac_template: IDFDocument,
    mock_config: EnergyPlusConfig,
) -> None:
    """Raise ExpandObjectsError on subprocess timeout."""
    import subprocess

    with (
        patch(
            "idfkit.simulation.expand.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="ExpandObjects", timeout=1),
        ),
        pytest.raises(ExpandObjectsError, match="timed out"),
    ):
        expand_objects(model_with_hvac_template, energyplus=mock_config, timeout=1.0)


def test_expand_objects_os_error_raises(
    model_with_hvac_template: IDFDocument,
    mock_config: EnergyPlusConfig,
) -> None:
    """Raise ExpandObjectsError on OS error starting the process."""
    with (
        patch(
            "idfkit.simulation.expand.subprocess.run",
            side_effect=OSError("Permission denied"),
        ),
        pytest.raises(ExpandObjectsError, match="Failed to start ExpandObjects"),
    ):
        expand_objects(model_with_hvac_template, energyplus=mock_config)


def test_expand_objects_auto_discovers_energyplus(
    model_with_hvac_template: IDFDocument,
    mock_config: EnergyPlusConfig,
) -> None:
    """When no config is given, find_energyplus is called."""
    expanded_content = "Version, 24.1;\n\nZone,\n  Office;\n"

    def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
        cwd = kwargs.get("cwd", "")
        Path(str(cwd), "expanded.idf").write_text(expanded_content)
        result = MagicMock()
        result.returncode = 0
        result.stdout = ""
        result.stderr = ""
        return result

    with (
        patch("idfkit.simulation.expand.find_energyplus", return_value=mock_config) as mock_find,
        patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run),
    ):
        expand_objects(model_with_hvac_template)

    mock_find.assert_called_once()


def test_document_expand_method(
    model_with_hvac_template: IDFDocument,
    mock_config: EnergyPlusConfig,
) -> None:
    """IDFDocument.expand() delegates to expand_objects."""
    expanded_content = "Version, 24.1;\n\nZone,\n  Office;\n"

    def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
        cwd = kwargs.get("cwd", "")
        Path(str(cwd), "expanded.idf").write_text(expanded_content)
        result = MagicMock()
        result.returncode = 0
        result.stdout = ""
        result.stderr = ""
        return result

    with patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run):
        expanded = model_with_hvac_template.expand(energyplus=mock_config)

    assert isinstance(expanded, IDFDocument)
    assert "Zone" in expanded


def test_expand_objects_does_not_mutate_original(
    model_with_hvac_template: IDFDocument,
    mock_config: EnergyPlusConfig,
) -> None:
    """The original document should remain unchanged after expansion."""
    original_types = set(model_with_hvac_template.keys())

    expanded_content = "Version, 24.1;\n\nZone,\n  Office;\n"

    def fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
        cwd = kwargs.get("cwd", "")
        Path(str(cwd), "expanded.idf").write_text(expanded_content)
        result = MagicMock()
        result.returncode = 0
        result.stdout = ""
        result.stderr = ""
        return result

    with patch("idfkit.simulation.expand.subprocess.run", side_effect=fake_run):
        expand_objects(model_with_hvac_template, energyplus=mock_config)

    assert set(model_with_hvac_template.keys()) == original_types
    assert "HVACTemplate:Zone:IdealLoadsAirSystem" in model_with_hvac_template


def test_expand_objects_skips_subprocess_when_nothing_to_expand() -> None:
    """When there are no expandable objects, return a copy without invoking ExpandObjects."""
    doc = new_document(version=(24, 1, 0))
    doc.add("Zone", "Office", {"x_origin": 0.0, "y_origin": 0.0, "z_origin": 0.0})

    # No mock config needed — the function should never look for EnergyPlus
    with patch("idfkit.simulation.expand.subprocess.run") as mock_run:
        result = expand_objects(doc)

    mock_run.assert_not_called()
    assert isinstance(result, IDFDocument)
    assert "Zone" in result
    assert result["Zone"]["Office"].name == "Office"
    # Verify it's a copy, not the same object
    assert result is not doc


def test_needs_expansion_uses_schema_group(model_with_hvac_template: IDFDocument) -> None:
    """_needs_expansion checks the schema group field, not just the prefix."""
    # model_with_hvac_template has a schema loaded (new_document gives one)
    assert model_with_hvac_template.schema is not None
    assert _needs_expansion(model_with_hvac_template) is True


def test_needs_expansion_detects_ground_heat_transfer() -> None:
    """Schema-based detection works for GroundHeatTransfer objects too."""
    doc = new_document(version=(24, 1, 0))
    doc.add("GroundHeatTransfer:Control", "", {"name": "test", "run_basement_preprocessor": "No"}, validate=False)
    assert _needs_expansion(doc) is True


def test_needs_expansion_false_for_plain_model() -> None:
    """A plain model with only Zone objects does not need expansion."""
    doc = new_document(version=(24, 1, 0))
    doc.add("Zone", "Office", {"x_origin": 0.0})
    assert _needs_expansion(doc) is False


def test_needs_expansion_falls_back_to_prefix_without_schema() -> None:
    """Without a schema, fall back to prefix matching."""
    doc = IDFDocument(version=(24, 1, 0), schema=None)
    obj = IDFObject(
        obj_type="HVACTemplate:Zone:IdealLoadsAirSystem",
        name="Test",
        data={"zone_name": "Office"},
    )
    doc.addidfobject(obj)

    assert doc.schema is None
    assert _needs_expansion(doc) is True


def test_needs_expansion_prefix_fallback_negative() -> None:
    """Prefix fallback returns False for non-expandable objects."""
    doc = IDFDocument(version=(24, 1, 0), schema=None)
    obj = IDFObject(obj_type="Zone", name="Office", data={})
    doc.addidfobject(obj)

    assert doc.schema is None
    assert _needs_expansion(doc) is False
