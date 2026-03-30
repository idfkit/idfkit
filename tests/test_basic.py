"""Basic tests for idfkit."""

from __future__ import annotations

import tempfile
from pathlib import Path


def test_import():
    """Test that the package can be imported."""
    import idfkit

    assert idfkit.__version__ == "0.1.0"


def test_load_idf():
    """Test loading an IDF file."""
    from idfkit import load_idf

    idf_content = """
    Version, 24.1;
    Zone,
      TestZone,              !- Name
      0,                     !- Direction of Relative North
      0, 0, 0,               !- X,Y,Z Origin
      1,                     !- Type
      1;                     !- Multiplier
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".idf", delete=False) as f:
        f.write(idf_content)
        temp_path = Path(f.name)

    try:
        model = load_idf(str(temp_path))
        assert model.version == (24, 1, 0)
        assert len(model["Zone"]) == 1
        assert model["Zone"]["TestZone"].name == "TestZone"
    finally:
        temp_path.unlink()


def test_new_document():
    """Test creating a new document."""
    from idfkit import new_document

    model = new_document(version=(24, 1, 0))
    assert model.version == (24, 1, 0)
    assert len(model) == 4
    assert len(model["Version"]) == 1
    assert len(model["Building"]) == 1
    assert len(model["SimulationControl"]) == 1
    assert len(model["GlobalGeometryRules"]) == 1

    version_obj = model["Version"].first()
    assert version_obj is not None
    assert version_obj.version_identifier == "24.1"

    building = model["Building"].first()
    assert building is not None
    assert building.name == "Building"


def test_add_object():
    """Test adding objects to a document."""
    from idfkit import new_document

    model = new_document(version=(24, 1, 0))
    zone = model.add("Zone", "MyZone", {"x_origin": 10.0})

    assert zone.name == "MyZone"
    assert zone.x_origin == 10.0
    assert len(model["Zone"]) == 1


def test_reference_tracking():
    """Test reference tracking."""
    from idfkit import load_idf

    idf_content = """
    Version, 24.1;
    Zone, TestZone, 0, 0, 0, 0, 1, 1;
    ScheduleTypeLimits, Fraction, 0, 1, Continuous;
    Schedule:Constant, TestSchedule, Fraction, 1.0;
    People,
      TestPeople,            !- Name
      TestZone,              !- Zone Name
      TestSchedule,          !- Schedule Name
      People,                !- Calculation Method
      10;                    !- Number of People
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".idf", delete=False) as f:
        f.write(idf_content)
        temp_path = Path(f.name)

    try:
        model = load_idf(str(temp_path))
        refs = model.get_referencing("TestZone")
        assert len(refs) == 1
        assert next(iter(refs)).name == "TestPeople"
    finally:
        temp_path.unlink()


def test_write_idf() -> None:
    """Test writing IDF content."""
    from idfkit import new_document, write_idf

    model = new_document(version=(24, 1, 0))
    model.add("Zone", "MyZone", {"x_origin": 0})

    output = write_idf(model, None)
    assert output is not None
    assert "Zone," in output
    assert "MyZone" in output


def test_load_idf_unsupported_version_raises() -> None:
    """load_idf with a bad version tuple should raise UnsupportedVersionError."""
    import pytest

    from idfkit import load_idf
    from idfkit.exceptions import UnsupportedVersionError

    with tempfile.NamedTemporaryFile(mode="w", suffix=".idf", delete=False) as f:
        f.write("Version, 99.9;\n")
        temp_path = Path(f.name)

    try:
        with pytest.raises(UnsupportedVersionError):
            load_idf(str(temp_path), version=(99, 9, 0))
    finally:
        temp_path.unlink()


def test_load_epjson_unsupported_version_raises() -> None:
    """load_epjson with a bad version tuple should raise UnsupportedVersionError."""
    import json

    import pytest

    from idfkit import load_epjson
    from idfkit.exceptions import UnsupportedVersionError

    data = {
        "Version": {"Version 1": {"version_identifier": "24.1"}},
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".epJSON", delete=False) as f:
        json.dump(data, f)
        temp_path = Path(f.name)

    try:
        with pytest.raises(UnsupportedVersionError):
            load_epjson(str(temp_path), version=(99, 9, 0))
    finally:
        temp_path.unlink()


def test_cst_node_creation() -> None:
    """Cover DocumentCST and CSTNode creation (cst.py line 25 default factory)."""
    from idfkit.cst import CSTNode, DocumentCST

    node = CSTNode(text="some text")
    assert node.text == "some text"
    assert node.obj is None

    cst = DocumentCST()
    assert cst.nodes == []
    assert cst.encoding == "latin-1"

    cst2 = DocumentCST(nodes=[node], encoding="utf-8")
    assert len(cst2.nodes) == 1
    assert cst2.encoding == "utf-8"
