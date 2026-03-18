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

from pathlib import Path

import pytest

from idfkit.exceptions import IDFParseError
from idfkit.idf_parser import parse_idf
from idfkit.schema import get_schema
from idfkit.writers import write_idf


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

        doc = parse_idf(idf_path, strict=True)

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

        doc = parse_idf(idf_path, strict=True)

        assert doc["Schedule:Compact"]["TestSchedule"] is not None

    def test_canonical_names_in_collections(self, tmp_path: Path) -> None:
        """Collections should use canonical PascalCase keys, not raw IDF casing."""
        idf_content = "VERSION, 24.1;\n\nZONE,\n  TestZone, 0, 0, 0, 0, 1, 1;\n"
        idf_path = tmp_path / "caps.idf"
        idf_path.write_text(idf_content)

        doc = parse_idf(idf_path, strict=True)

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

        doc = parse_idf(idf_path, strict=True)

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

        doc = parse_idf(idf_path, schema=None, version=(24, 1, 0), strict=False)

        # schema=None triggers auto-load from version, so normalization still applies
        assert "Zone" in doc.collections
        assert "ZONE" not in doc.collections
