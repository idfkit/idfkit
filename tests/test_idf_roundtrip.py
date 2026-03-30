"""Tests for IDF parser roundtrip correctness.

Covers:
- Nameless/single-field objects (Timestep, SimulationControl)
- Duplicate-named objects (Output:Variable with key_value=*)
- Phantom objects from non-EnergyPlus text
- Extensible fields (BuildingSurface:Detailed vertices)
- Named objects (Zone, Material, Construction)
- Full parse -> write -> re-parse roundtrip
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field as dc_field
from pathlib import Path

import pytest

from idfkit.exceptions import IDFParseError
from idfkit.idf_parser import (  # pyright: ignore[reportPrivateUsage]
    IDFParser,
    _coerce_value_fast,
    iter_idf_objects,
    parse_idf,
)
from idfkit.schema import get_schema
from idfkit.writers import write_idf

# ---------------------------------------------------------------------------
# Shared helpers for coverage gap tests
# ---------------------------------------------------------------------------


@dataclass
class _FakePC:
    """Minimal stand-in for ParsingCache used in extensible-field tests."""

    ext_size: int = 0
    ext_field_names: list[str] = dc_field(default_factory=list)
    field_types: dict[str, str | None] = dc_field(default_factory=dict)


@pytest.fixture
def schema():
    return get_schema((24, 1, 0))


@pytest.fixture
def minimal_idf(tmp_path: Path) -> Path:
    """Create a minimal IDF file with various object types for roundtrip testing."""
    content = """\
! Minimal IDF for roundtrip testing
! This line and above should not become objects

Version, 24.1;

Timestep,4;

SimulationControl,
  Yes,                     !- Do Zone Sizing Calculation
  No,                      !- Do System Sizing Calculation
  No,                      !- Do Plant Sizing Calculation
  Yes,                     !- Run Simulation for Sizing Periods
  No;                      !- Run Simulation for Weather File Run Periods

Building,
  TestBuilding,            !- Name
  0,                       !- North Axis
  City,                    !- Terrain
  0.04,                    !- Loads Convergence Tolerance Value
  0.4,                     !- Temperature Convergence Tolerance Value
  FullInteriorAndExterior, !- Solar Distribution
  25,                      !- Maximum Number of Warmup Days
  6;                       !- Minimum Number of Warmup Days

Zone,
  ZONE ONE,                !- Name
  0,                       !- Direction of Relative North
  0, 0, 0;                 !- X,Y,Z Origin

Material,
  C12 - 2 IN HW CONCRETE,  !- Name
  MediumRough,              !- Roughness
  0.0510,                   !- Thickness {m}
  1.7296,                   !- Conductivity {W/m-K}
  2243,                     !- Density {kg/m3}
  837;                      !- Specific Heat {J/kg-K}

Construction,
  TestConstruction,        !- Name
  C12 - 2 IN HW CONCRETE; !- Outside Layer

GlobalGeometryRules,
  UpperLeftCorner,         !- Starting Vertex Position
  Counterclockwise,        !- Vertex Entry Direction
  Relative;                !- Coordinate System

BuildingSurface:Detailed,
  Zn001:Wall001,           !- Name
  Wall,                    !- Surface Type
  TestConstruction,        !- Construction Name
  ZONE ONE,                !- Zone Name
  ,                        !- Space Name
  Outdoors,                !- Outside Boundary Condition
  ,                        !- Outside Boundary Condition Object
  SunExposed,              !- Sun Exposure
  WindExposed,             !- Wind Exposure
  0.5,                     !- View Factor to Ground
  4,                       !- Number of Vertices
  0, 0, 3.048,             !- Vertex 1
  0, 0, 0,                 !- Vertex 2
  6.096, 0, 0,             !- Vertex 3
  6.096, 0, 3.048;         !- Vertex 4

Output:Variable,*,Site Outdoor Air Drybulb Temperature,Timestep;
Output:Variable,*,Zone Mean Air Temperature,Timestep;
Output:Variable,*,Zone Air System Sensible Heating Energy,Timestep;

Output:Meter,EnergyTransfer:Building,Hourly;
"""
    filepath = tmp_path / "minimal.idf"
    filepath.write_text(content, encoding="latin-1")
    return filepath


class TestNamelessObjects:
    """Bug fix 2: Nameless/single-field objects should preserve their data."""

    def test_timestep_parsed_correctly(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        collection = doc["Timestep"]
        assert len(collection) == 1
        obj = collection[0]
        assert obj.name == ""
        assert obj.data.get("number_of_timesteps_per_hour") == 4

    def test_simulation_control_parsed_correctly(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        collection = doc["SimulationControl"]
        assert len(collection) == 1
        obj = collection[0]
        assert obj.name == ""
        assert obj.data.get("do_zone_sizing_calculation") == "Yes"
        assert obj.data.get("do_system_sizing_calculation") == "No"

    def test_timestep_roundtrip(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        output = write_idf(doc)
        assert output is not None
        # Should write "4" as the field value, not as the name
        assert "Timestep," in output
        assert "4;" in output

    def test_global_geometry_rules_parsed_correctly(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        collection = doc["GlobalGeometryRules"]
        assert len(collection) == 1
        obj = collection[0]
        assert obj.name == ""
        assert obj.data.get("starting_vertex_position") == "UpperLeftCorner"


class TestDuplicateNames:
    """Bug fix 1: Multiple objects with the same key (e.g. Output:Variable with *)."""

    def test_multiple_output_variables_survive(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        collection = doc["Output:Variable"]
        assert len(collection) == 3

    def test_output_variable_fields_correct(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        variables = list(doc["Output:Variable"])
        variable_names = [v.data.get("variable_name") for v in variables]
        assert "Site Outdoor Air Drybulb Temperature" in variable_names
        assert "Zone Mean Air Temperature" in variable_names
        assert "Zone Air System Sensible Heating Energy" in variable_names

    def test_output_variable_key_value_preserved(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        for obj in doc["Output:Variable"]:
            assert obj.name == ""
            assert obj.data.get("key_value") == "*"


class TestPhantomObjects:
    """Bug fix 3: Non-EnergyPlus text should not create phantom objects."""

    def test_comments_not_parsed_as_objects(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        # Comments at the top should not appear as objects
        obj_types = set(doc.collections.keys())
        assert "Minimal IDF for roundtrip testing" not in obj_types

    def test_unknown_type_raises(self, tmp_path: Path) -> None:
        """Garbage text matching the object regex should fail strict parsing."""
        content = """\
Version, 24.1;

design days,
  some value;

Zone,
  TestZone,
  0, 0, 0, 0;
"""
        filepath = tmp_path / "phantom.idf"
        filepath.write_text(content, encoding="latin-1")
        with pytest.raises(IDFParseError, match="Unknown object type"):
            parse_idf(filepath)


class TestExtensibleFieldsWithEmptyValues:
    """Bug fix 5: Empty values in extensible fields must be preserved.

    ZoneHVAC:EquipmentList has 6 fields per equipment group, including
    optional schedule fields that are often empty. If empty fields are
    dropped, the field positions shift and EnergyPlus fails with:
    "zone_equipment_object_type - 2 - Failed to match against any enum values."
    """

    @pytest.fixture
    def hvac_equipment_idf(self, tmp_path: Path) -> Path:
        """IDF with ZoneHVAC:EquipmentList containing empty schedule fields."""
        content = """\
Version, 24.1;

Zone,
  Main Zone,
  0, 0, 0, 0;

ZoneHVAC:EquipmentConnections,
  Main Zone,               !- Zone Name
  Main Zone Equipment,     !- Zone Conditioning Equipment List Name
  Main Zone Inlet Node,    !- Zone Air Inlet Node or NodeList Name
  ,                        !- Zone Air Exhaust Node or NodeList Name
  Main Zone Air Node,      !- Zone Air Node Name
  Main Zone Return Node;   !- Zone Return Air Node or NodeList Name

ZoneHVAC:EquipmentList,
  Main Zone Equipment,     !- Name
  SequentialLoad,          !- Load Distribution Scheme
  ZoneHVAC:IdealLoadsAirSystem,!- Zone Equipment 1 Object Type
  Main Zone Ideal Loads,   !- Zone Equipment 1 Name
  1,                       !- Zone Equipment 1 Cooling Sequence
  1,                       !- Zone Equipment 1 Heating or No-Load Sequence
  ,                        !- Zone Equipment 1 Sequential Cooling Fraction Schedule Name
  ,                        !- Zone Equipment 1 Sequential Heating Fraction Schedule Name
  ZoneHVAC:IdealLoadsAirSystem,!- Zone Equipment 2 Object Type
  Main Zone Ideal Loads 2, !- Zone Equipment 2 Name
  2,                       !- Zone Equipment 2 Cooling Sequence
  2,                       !- Zone Equipment 2 Heating or No-Load Sequence
  ,                        !- Zone Equipment 2 Sequential Cooling Fraction Schedule Name
  ;                        !- Zone Equipment 2 Sequential Heating Fraction Schedule Name

ZoneHVAC:IdealLoadsAirSystem,
  Main Zone Ideal Loads,
  ,
  Main Zone Inlet Node,
  ;

ZoneHVAC:IdealLoadsAirSystem,
  Main Zone Ideal Loads 2,
  ,
  Main Zone Inlet Node 2,
  ;
"""
        filepath = tmp_path / "hvac_equipment.idf"
        filepath.write_text(content, encoding="latin-1")
        return filepath

    def test_empty_schedule_fields_stored(self, hvac_equipment_idf: Path) -> None:
        """Empty schedule fields should be stored as empty strings."""
        doc = parse_idf(hvac_equipment_idf)
        eq_list = doc["ZoneHVAC:EquipmentList"][0]

        # Equipment 1 - verify all 6 fields are present
        assert eq_list.data.get("zone_equipment_object_type") == "ZoneHVAC:IdealLoadsAirSystem"
        assert eq_list.data.get("zone_equipment_name") == "Main Zone Ideal Loads"
        assert eq_list.data.get("zone_equipment_cooling_sequence") == 1.0
        assert eq_list.data.get("zone_equipment_heating_or_no_load_sequence") == 1.0
        # Empty schedule fields must be stored as ""
        assert eq_list.data.get("zone_equipment_sequential_cooling_fraction_schedule_name") == ""
        assert eq_list.data.get("zone_equipment_sequential_heating_fraction_schedule_name") == ""

        # Equipment 2 - these would have wrong values if empty fields weren't stored
        assert eq_list.data.get("zone_equipment_object_type_2") == "ZoneHVAC:IdealLoadsAirSystem"
        assert eq_list.data.get("zone_equipment_name_2") == "Main Zone Ideal Loads 2"
        assert eq_list.data.get("zone_equipment_cooling_sequence_2") == 2.0
        assert eq_list.data.get("zone_equipment_heating_or_no_load_sequence_2") == 2.0

    def test_empty_schedule_fields_roundtrip(self, hvac_equipment_idf: Path, tmp_path: Path) -> None:
        """Empty schedule fields should survive roundtrip."""
        doc1 = parse_idf(hvac_equipment_idf)
        output_path = tmp_path / "roundtrip.idf"
        write_idf(doc1, output_path)

        # Check written IDF has empty fields in correct positions
        content = output_path.read_text(encoding="latin-1")

        # The empty schedule fields should appear before equipment 2
        lines = content.split("\n")
        eq_list_lines = []
        in_eq_list = False
        for line in lines:
            if "ZoneHVAC:EquipmentList" in line:
                in_eq_list = True
            if in_eq_list:
                eq_list_lines.append(line)
                if ";" in line:
                    break

        # Should have 14 fields: name, scheme, 6 for equip 1, 6 for equip 2
        # But trailing empty fields are trimmed, so we check structure
        eq_text = "\n".join(eq_list_lines)
        # Equipment 2's object type should come AFTER empty schedule fields
        assert "Zone Equipment Sequential Cooling Fraction Schedule Name" in eq_text
        assert "Zone Equipment Sequential Heating Fraction Schedule Name" in eq_text

        # Re-parse and verify data integrity
        doc2 = parse_idf(output_path)
        eq_list2 = doc2["ZoneHVAC:EquipmentList"][0]
        # If empty fields weren't preserved, equipment 2 would have wrong values
        assert eq_list2.data.get("zone_equipment_object_type_2") == "ZoneHVAC:IdealLoadsAirSystem"
        assert eq_list2.data.get("zone_equipment_name_2") == "Main Zone Ideal Loads 2"


class TestExtensibleFields:
    """Bug fix 4: Extensible fields (vertices) should be preserved."""

    def test_surface_vertices_parsed(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        wall = doc["BuildingSurface:Detailed"][0]
        # First vertex group: vertex_x_coordinate, vertex_y_coordinate, vertex_z_coordinate
        assert wall.data.get("vertex_x_coordinate") == 0.0
        assert wall.data.get("vertex_y_coordinate") == 0.0
        assert wall.data.get("vertex_z_coordinate") == 3.048
        # Second vertex group: _2 suffix
        assert wall.data.get("vertex_x_coordinate_2") == 0.0
        assert wall.data.get("vertex_y_coordinate_2") == 0.0
        assert wall.data.get("vertex_z_coordinate_2") == 0.0
        # Third vertex group: _3 suffix
        assert wall.data.get("vertex_x_coordinate_3") == 6.096
        assert wall.data.get("vertex_y_coordinate_3") == 0.0
        assert wall.data.get("vertex_z_coordinate_3") == 0.0
        # Fourth vertex group: _4 suffix
        assert wall.data.get("vertex_x_coordinate_4") == 6.096
        assert wall.data.get("vertex_y_coordinate_4") == 0.0
        assert wall.data.get("vertex_z_coordinate_4") == 3.048

    def test_surface_vertices_roundtrip(self, minimal_idf: Path, tmp_path: Path) -> None:
        doc = parse_idf(minimal_idf)
        output_path = tmp_path / "roundtrip.idf"
        write_idf(doc, output_path)
        doc2 = parse_idf(output_path)
        wall = doc2["BuildingSurface:Detailed"][0]
        assert wall.data.get("vertex_x_coordinate") == 0.0
        assert wall.data.get("vertex_z_coordinate") == 3.048
        assert wall.data.get("vertex_x_coordinate_3") == 6.096
        assert wall.data.get("vertex_z_coordinate_4") == 3.048


class TestNamedObjects:
    """Named objects should still parse correctly with the fix."""

    def test_zone_parsed_correctly(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        zone = doc["Zone"][0]
        assert zone.name == "ZONE ONE"
        assert zone.data.get("direction_of_relative_north") == 0.0

    def test_material_parsed_correctly(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        mat = doc["Material"][0]
        assert mat.name == "C12 - 2 IN HW CONCRETE"
        assert mat.data.get("roughness") == "MediumRough"
        assert mat.data.get("thickness") == 0.0510
        assert mat.data.get("conductivity") == 1.7296

    def test_building_parsed_correctly(self, minimal_idf: Path) -> None:
        doc = parse_idf(minimal_idf)
        building = doc["Building"][0]
        assert building.name == "TestBuilding"
        assert building.data.get("terrain") == "City"


class TestFullRoundtrip:
    """Parse -> write -> re-parse should preserve object counts and data."""

    def test_object_counts_preserved(self, minimal_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(minimal_idf)
        output_path = tmp_path / "roundtrip.idf"
        write_idf(doc1, output_path)
        doc2 = parse_idf(output_path)

        # Compare object counts per type
        for obj_type in doc1.collections:
            count1 = len(doc1[obj_type])
            count2 = len(doc2[obj_type])
            assert count1 == count2, f"{obj_type}: {count1} != {count2}"

    def test_total_object_count_preserved(self, minimal_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(minimal_idf)
        output_path = tmp_path / "roundtrip.idf"
        write_idf(doc1, output_path)
        doc2 = parse_idf(output_path)
        assert len(doc1) == len(doc2)

    def test_data_preserved_after_roundtrip(self, minimal_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(minimal_idf)
        output_path = tmp_path / "roundtrip.idf"
        write_idf(doc1, output_path)
        doc2 = parse_idf(output_path)

        # Check specific values survive
        assert doc2["Timestep"][0].data.get("number_of_timesteps_per_hour") == 4
        assert len(doc2["Output:Variable"]) == 3
        assert doc2["Zone"][0].name == "ZONE ONE"
        assert doc2["BuildingSurface:Detailed"][0].data.get("vertex_z_coordinate") == 3.048


# ---------------------------------------------------------------------------
# Case-insensitive type name parsing
# ---------------------------------------------------------------------------


class TestCaseInsensitiveTypes:
    """IDF files may use ALL-CAPS or mixed-case type names."""

    def test_all_caps_types_parsed_strict(self, tmp_path: Path) -> None:
        """Parser should accept ALL-CAPS type names like ZONE, MATERIAL."""
        idf_content = """\
VERSION, 24.1;

ZONE,
  TestZone,              !- Name
  0,                     !- Direction of Relative North
  0, 0, 0,              !- X,Y,Z Origin
  1,                     !- Type
  1;                     !- Multiplier

MATERIAL,
  TestMaterial,          !- Name
  MediumSmooth,          !- Roughness
  0.1,                   !- Thickness
  1.0,                   !- Conductivity
  2000,                  !- Density
  1000;                  !- Specific Heat

CONSTRUCTION,
  TestConstruction,      !- Name
  TestMaterial;          !- Outside Layer
"""
        idf_path = tmp_path / "caps.idf"
        idf_path.write_text(idf_content)

        doc = parse_idf(idf_path, strict_parsing=True)

        # Objects should be accessible under canonical PascalCase names
        assert doc["Zone"]["TestZone"] is not None
        assert doc["Material"]["TestMaterial"] is not None
        assert doc["Construction"]["TestConstruction"] is not None

    def test_mixed_case_colon_types(self, tmp_path: Path) -> None:
        """Types with colons like SCHEDULE:COMPACT should resolve."""
        idf_content = """\
VERSION, 24.1;

SCHEDULETYPELIMITS,
  Temperature,           !- Name
  -100,                  !- Lower Limit Value
  200,                   !- Upper Limit Value
  Continuous;            !- Numeric Type

SCHEDULE:COMPACT,
  TestSchedule,          !- Name
  Temperature,           !- Schedule Type Limits Name
  Through: 12/31,        !- Field 1
  For: AllDays,          !- Field 2
  Until: 24:00, 21.0;   !- Field 3
"""
        idf_path = tmp_path / "schedule.idf"
        idf_path.write_text(idf_content)

        doc = parse_idf(idf_path, strict_parsing=True)

        assert doc["Schedule:Compact"]["TestSchedule"] is not None

    def test_canonical_names_in_collections(self, tmp_path: Path) -> None:
        """Collections should use canonical PascalCase keys, not raw IDF casing."""
        idf_content = "VERSION, 24.1;\n\nZONE,\n  TestZone, 0, 0, 0, 0, 1, 1;\n"
        idf_path = tmp_path / "caps.idf"
        idf_path.write_text(idf_content)

        doc = parse_idf(idf_path, strict_parsing=True)

        # The collection key should be canonical "Zone", not "ZONE"
        assert "Zone" in doc.collections
        assert "ZONE" not in doc.collections

    def test_mixed_casing_same_type_merges(self, tmp_path: Path) -> None:
        """Objects with different casings of the same type go into one collection."""
        idf_content = """\
VERSION, 24.1;

Zone,
  ZoneA, 0, 0, 0, 0, 1, 1;

ZONE,
  ZoneB, 0, 0, 0, 0, 1, 1;

zone,
  ZoneC, 0, 0, 0, 0, 1, 1;
"""
        idf_path = tmp_path / "mixed.idf"
        idf_path.write_text(idf_content)

        doc = parse_idf(idf_path, strict_parsing=True)

        # All three should be in the canonical "Zone" collection
        assert len(doc["Zone"]) == 3
        assert doc["Zone"]["ZoneA"] is not None
        assert doc["Zone"]["ZoneB"] is not None
        assert doc["Zone"]["ZoneC"] is not None

    def test_schema_none_still_normalizes(self, tmp_path: Path) -> None:
        """Passing schema=None with a version still resolves the schema and normalizes."""
        idf_content = "VERSION, 24.1;\n\nZONE,\n  TestZone, 0, 0, 0, 0, 1, 1;\n"
        idf_path = tmp_path / "noschema.idf"
        idf_path.write_text(idf_content)

        doc = parse_idf(idf_path, schema=None, version=(24, 1, 0), strict_parsing=False)

        # schema=None triggers auto-load from version, so normalization still applies
        assert "Zone" in doc.collections
        assert "ZONE" not in doc.collections


# ---------------------------------------------------------------------------
# Coverage gap tests: idf_parser.py uncovered lines
# ---------------------------------------------------------------------------


class TestCoerceValueFast:
    """_coerce_value_fast: integer type with non-numeric value falls back to string (L89-90)."""

    def test_integer_non_numeric_returns_string(self) -> None:
        result = _coerce_value_fast("integer", "AutoSize")
        assert result == "AutoSize"

    def test_integer_numeric_returns_int(self) -> None:
        result = _coerce_value_fast("integer", "5")
        assert result == 5

    def test_number_non_numeric_returns_string(self) -> None:
        result = _coerce_value_fast("number", "AutoSize")
        assert result == "AutoSize"


class TestMmapLargeFile:
    """_load_content uses mmap for files > 10 MB (L253-258)."""

    def test_large_file_parsed_via_mmap(self, tmp_path: Path) -> None:
        # Build a minimal valid IDF then pad it past the mmap threshold (10 MB)
        header = "Version, 24.1;\nZone, BigZone, 0, 0, 0, 0, 1, 1;\n"
        padding = "! " + "x" * 100 + "\n"
        # Need > 10 * 1024 * 1024 bytes
        repeat = (10 * 1024 * 1024 // len(padding)) + 1
        content = header + padding * repeat
        idf_path = tmp_path / "large.idf"
        idf_path.write_bytes(content.encode("latin-1"))

        doc = parse_idf(idf_path)
        assert doc["Zone"]["BigZone"] is not None


class TestParseFieldsSlowPath:
    """_parse_fields slow path: '!' in fields_raw after comment stripping (L486-493)."""

    def test_inline_comment_in_fields_raw(self, tmp_path: Path) -> None:
        idf_path = tmp_path / "dummy.idf"
        idf_path.write_text("Version, 24.1;\n")
        parser = IDFParser(idf_path)
        raw = "  ZoneA,  ! comment\n  0"
        result = parser._parse_fields(raw)  # pyright: ignore[reportPrivateUsage]
        assert result[0].strip() == "ZoneA"


class TestLineAndColumnNoNewline:
    """_line_and_column with no prior newline returns (1, offset+1) (L501)."""

    def test_offset_zero_no_newline(self, tmp_path: Path) -> None:
        idf_path = tmp_path / "dummy.idf"
        idf_path.write_text("Version, 24.1;\n")
        content = b"ZoneType, Name;"
        line, col = IDFParser._line_and_column(content, 0)
        assert line == 1
        assert col == 1


class TestResolveCacheSchemaIsNone:
    """_resolve_type_cache returns (None, False, obj_type) when schema is None (L551)."""

    def test_schema_none_returns_none_cache(self, tmp_path: Path) -> None:
        idf_path = tmp_path / "dummy.idf"
        idf_path.write_text("Version, 24.1;\n")
        parser = IDFParser(idf_path)
        cache: dict[str, object] = {}
        canonical: dict[str, str] = {}
        skipped: set[str] = set()
        pc, skip, canonical_type = parser._resolve_type_cache(  # pyright: ignore[reportPrivateUsage]
            content=b"",
            schema=None,
            type_cache=cache,
            canonical_cache=canonical,
            skipped_types=skipped,
            obj_type="Zone",
            obj_name="Z1",
            match_offset=0,
        )
        assert pc is None
        assert not skip
        assert canonical_type == "Zone"


class TestIterIDFObjectsInlineComment:
    """iter_idf_objects: field with '!' inside (L630)."""

    def test_inline_comment_in_field_stripped(self, tmp_path: Path) -> None:
        content = "Version, 24.1;\nZone, MyZone, 0 ! inline comment\n, 0, 0;\n"
        idf_path = tmp_path / "inline.idf"
        idf_path.write_bytes(content.encode("latin-1"))

        objects = list(iter_idf_objects(idf_path))
        # Zone object should be present; the inline comment should be stripped
        zone_entries = [(t, n, f) for t, n, f in objects if t.upper() == "ZONE"]
        assert zone_entries, "Expected at least one Zone entry"
        # First field after name ('0 ! inline comment') should be stripped to '0'
        fields = zone_entries[0][2]
        assert fields[0] == "0"


class TestPreserveFormattingCST:
    """CST linking: unmatched CST node logs a warning (L733->732, L755->738)."""

    def test_preserve_formatting_roundtrip(self, tmp_path: Path) -> None:
        content = """\
Version, 24.1;

Zone,
  CST Zone,
  0, 0, 0, 0, 1, 1;
"""
        idf_path = tmp_path / "cst.idf"
        idf_path.write_bytes(content.encode("latin-1"))

        doc = parse_idf(idf_path, preserve_formatting=True)
        assert doc.cst is not None

        # Round-trip should produce output with the zone
        output = write_idf(doc)
        assert output is not None
        assert "CST Zone" in output

    def test_cst_unmatched_node_warning(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        """A CST node for an unknown type logs a warning rather than failing."""
        import logging

        from idfkit.cst import CSTNode, DocumentCST
        from idfkit.idf_parser import _link_cst_to_objects  # pyright: ignore[reportPrivateUsage]

        # Build a minimal doc
        content = "Version, 24.1;\nZone, Z1, 0, 0, 0, 0, 1, 1;\n"
        idf_path = tmp_path / "cst2.idf"
        idf_path.write_bytes(content.encode("latin-1"))
        doc = parse_idf(idf_path)

        # Create a CST with a node that won't match any parsed object
        orphan_node = CSTNode(text="UnknownType, Some Value;\n")
        cst = DocumentCST(nodes=[orphan_node])

        with caplog.at_level(logging.WARNING, logger="idfkit.idf_parser"):
            result = _link_cst_to_objects(cst, doc)

        assert result is True
        assert any("CST linking" in r.message for r in caplog.records)


class TestExtensibleInvalidGroupSize:
    """_append_extensible_fields: ext_size <= 0 raises ValueError in strict mode (L441-444)."""

    def test_invalid_ext_size_strict(self, tmp_path: Path) -> None:
        """ext_size=0 with strict_parsing=True raises ValueError."""
        idf_path = tmp_path / "dummy.idf"
        idf_path.write_text("Version, 24.1;\n")
        parser = IDFParser(idf_path, strict_parsing=True)

        with pytest.raises(ValueError, match="extensible group size is invalid"):
            parser._append_extensible_fields(  # pyright: ignore[reportPrivateUsage]
                data={},
                extra=["v1"],
                field_names=[],
                field_types={},
                pc=_FakePC(),  # type: ignore[arg-type]
            )

    def test_invalid_ext_size_non_strict(self, tmp_path: Path) -> None:
        """ext_size=0 with strict_parsing=False returns early without storing anything."""
        idf_path = tmp_path / "dummy.idf"
        idf_path.write_text("Version, 24.1;\n")
        parser = IDFParser(idf_path, strict_parsing=False)
        data: dict[str, object] = {}
        parser._append_extensible_fields(  # pyright: ignore[reportPrivateUsage]
            data=data,
            extra=["v1"],
            field_names=[],
            field_types={},
            pc=_FakePC(),  # type: ignore[arg-type]
        )
        assert data == {}


class TestExtensibleJGeNumExt:
    """_append_extensible_fields: j >= num_ext guard skips excess values (L457, L471)."""

    def test_extra_values_beyond_ext_names_skipped(self, tmp_path: Path) -> None:
        """ext_size=2 but only one ext_name: second value per group is silently skipped."""
        # _FakePC.ext_size=2 means groups of 2; ext_field_names has only 1 entry,
        # so j=1 (the second slot) hits the `j >= num_ext` guard and is dropped.
        idf_path = tmp_path / "dummy.idf"
        idf_path.write_text("Version, 24.1;\n")
        parser = IDFParser(idf_path, strict_parsing=True)
        data: dict[str, object] = {}
        field_names: list[str] = []
        pc = _FakePC(ext_size=2, ext_field_names=["field_a"])
        parser._append_extensible_fields(  # pyright: ignore[reportPrivateUsage]
            data=data,
            extra=["val_a", "val_b", "val_c", "val_d"],
            field_names=field_names,
            field_types={},
            pc=pc,  # type: ignore[arg-type]
        )
        assert "field_a" in data
        assert "field_a_2" in data
        assert "field_b" not in data


class TestNonStrictSkipsUnknownType:
    """With strict_parsing=False, unknown object types are skipped (L569-570)."""

    def test_unknown_type_skipped_non_strict(self, tmp_path: Path) -> None:
        content = """\
Version, 24.1;

Zone, GoodZone, 0, 0, 0, 0, 1, 1;

NotARealType, SomeValue;
"""
        idf_path = tmp_path / "skip.idf"
        idf_path.write_text(content)

        doc = parse_idf(idf_path, strict_parsing=False)
        assert doc["Zone"]["GoodZone"] is not None
        assert "NotARealType" not in doc.collections


class TestParseObjectCachedNoSchema:
    """_parse_object_cached with pc=None uses no-schema fallback (L382-388)."""

    def test_no_schema_fallback(self, tmp_path: Path) -> None:
        """pc=None triggers the no-schema branch; fields are stored as field_N keys."""
        from idfkit.idf_parser import _OBJECT_PATTERN  # pyright: ignore[reportPrivateUsage]

        idf_path = tmp_path / "dummy.idf"
        idf_path.write_text("Version, 24.1;\n")
        parser = IDFParser(idf_path)

        matches = list(_OBJECT_PATTERN.finditer(b"Zone, TestZone, 0, 0, 0;"))
        assert matches
        obj = parser._parse_object_cached(matches[0], None, "latin-1")  # pyright: ignore[reportPrivateUsage]
        assert obj is not None
        assert obj.name == "TestZone"

    def test_no_schema_fallback_with_empty_field(self, tmp_path: Path) -> None:
        """Empty field in no-schema fallback is not stored (falsy guard in loop body)."""
        from idfkit.idf_parser import _OBJECT_PATTERN  # pyright: ignore[reportPrivateUsage]

        idf_path = tmp_path / "dummy2.idf"
        idf_path.write_text("Version, 24.1;\n")
        parser = IDFParser(idf_path)

        matches = list(_OBJECT_PATTERN.finditer(b"Zone, TestZone, , 1;"))
        assert matches
        obj = parser._parse_object_cached(matches[0], None, "latin-1")  # pyright: ignore[reportPrivateUsage]
        assert obj is not None
        assert obj.name == "TestZone"
        assert "field_1" not in obj.data  # empty slot skipped
        assert "field_2" in obj.data


class TestCSTLinkingEmptyCollection:
    """_link_cst_to_objects: empty collection in doc skipped during obj_by_type build (L733->732)."""

    def test_empty_collection_not_added_to_obj_by_type(self, tmp_path: Path) -> None:
        """A document with an accessed-but-empty collection doesn't crash CST linking."""
        from idfkit.cst import CSTNode, DocumentCST
        from idfkit.idf_parser import _link_cst_to_objects  # pyright: ignore[reportPrivateUsage]

        content = "Version, 24.1;\nZone, Z1, 0, 0, 0, 0, 1, 1;\n"
        idf_path = tmp_path / "empty_coll.idf"
        idf_path.write_bytes(content.encode("latin-1"))
        doc = parse_idf(idf_path)

        # Access an empty collection (e.g. Material) to create it
        _ = doc["Material"]

        # Build a CST that only has a Zone node
        zone_node = CSTNode(text="Zone,\n  Z1,\n  0, 0, 0, 0, 1, 1;\n")
        cst = DocumentCST(nodes=[zone_node])

        result = _link_cst_to_objects(cst, doc)
        assert result is True


class TestCSTLinkingMultipleSameType:
    """_link_cst_to_objects: bucket not deleted when objects remain (L755->738)."""

    def test_multiple_objects_same_type_linked(self, tmp_path: Path) -> None:
        """Two objects of the same type: bucket persists after first popleft (L755->738)."""
        from idfkit.cst import CSTNode, DocumentCST
        from idfkit.idf_parser import _link_cst_to_objects  # pyright: ignore[reportPrivateUsage]

        content = """\
Version, 24.1;
Zone, ZoneA, 0, 0, 0, 0, 1, 1;
Zone, ZoneB, 0, 0, 0, 0, 1, 1;
"""
        idf_path = tmp_path / "multi_zone.idf"
        idf_path.write_bytes(content.encode("latin-1"))
        doc = parse_idf(idf_path)

        node_a = CSTNode(text="Zone,\n  ZoneA,\n  0, 0, 0, 0, 1, 1;\n")
        node_b = CSTNode(text="Zone,\n  ZoneB,\n  0, 0, 0, 0, 1, 1;\n")
        cst = DocumentCST(nodes=[node_a, node_b])

        result = _link_cst_to_objects(cst, doc)
        assert result is True
        assert node_a.obj is not None
        assert node_b.obj is not None
