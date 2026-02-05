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

    def test_unknown_type_filtered(self, tmp_path: Path) -> None:
        """Garbage text matching the object regex should be filtered out."""
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
        doc = parse_idf(filepath)
        obj_types = set(doc.collections.keys())
        assert "design days" not in obj_types
        assert "Zone" in obj_types


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
