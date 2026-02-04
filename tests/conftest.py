"""Shared fixtures for idfkit tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idfkit import IDFDocument, new_document
from idfkit.objects import IDFObject
from idfkit.references import ReferenceGraph
from idfkit.schema import EpJSONSchema, get_schema


@pytest.fixture
def schema() -> EpJSONSchema:
    """Load the v24.1.0 schema."""
    return get_schema((24, 1, 0))


@pytest.fixture
def empty_doc() -> IDFDocument:
    """Create an empty IDFDocument with schema loaded."""
    return new_document(version=(24, 1, 0))


@pytest.fixture
def simple_doc() -> IDFDocument:
    """Create a document with a zone, material, construction, and surface."""
    doc = new_document(version=(24, 1, 0))

    doc.add("Zone", "TestZone", {"x_origin": 0.0, "y_origin": 0.0, "z_origin": 0.0})
    doc.add(
        "Material",
        "TestMaterial",
        {
            "roughness": "MediumSmooth",
            "thickness": 0.1,
            "conductivity": 1.0,
            "density": 2000.0,
            "specific_heat": 1000.0,
        },
    )
    doc.add("Construction", "TestConstruction", {"outside_layer": "TestMaterial"})
    doc.add(
        "BuildingSurface:Detailed",
        "TestWall",
        {
            "surface_type": "Wall",
            "construction_name": "TestConstruction",
            "zone_name": "TestZone",
            "outside_boundary_condition": "Outdoors",
            "number_of_vertices": 4,
            "vertex_1_x_coordinate": 0.0,
            "vertex_1_y_coordinate": 0.0,
            "vertex_1_z_coordinate": 3.0,
            "vertex_2_x_coordinate": 0.0,
            "vertex_2_y_coordinate": 0.0,
            "vertex_2_z_coordinate": 0.0,
            "vertex_3_x_coordinate": 10.0,
            "vertex_3_y_coordinate": 0.0,
            "vertex_3_z_coordinate": 0.0,
            "vertex_4_x_coordinate": 10.0,
            "vertex_4_y_coordinate": 0.0,
            "vertex_4_z_coordinate": 3.0,
        },
    )
    doc.add(
        "BuildingSurface:Detailed",
        "TestFloor",
        {
            "surface_type": "Floor",
            "construction_name": "TestConstruction",
            "zone_name": "TestZone",
            "outside_boundary_condition": "Ground",
            "number_of_vertices": 4,
            "vertex_1_x_coordinate": 0.0,
            "vertex_1_y_coordinate": 0.0,
            "vertex_1_z_coordinate": 0.0,
            "vertex_2_x_coordinate": 10.0,
            "vertex_2_y_coordinate": 0.0,
            "vertex_2_z_coordinate": 0.0,
            "vertex_3_x_coordinate": 10.0,
            "vertex_3_y_coordinate": 10.0,
            "vertex_3_z_coordinate": 0.0,
            "vertex_4_x_coordinate": 0.0,
            "vertex_4_y_coordinate": 10.0,
            "vertex_4_z_coordinate": 0.0,
        },
    )
    return doc


@pytest.fixture
def idf_file(tmp_path: Path) -> Path:
    """Create a temporary IDF file."""
    content = """\
Version, 24.1;

Zone,
  TestZone,              !- Name
  0,                     !- Direction of Relative North
  0, 0, 0,               !- X,Y,Z Origin
  1,                     !- Type
  1;                     !- Multiplier

Material,
  TestMaterial,           !- Name
  MediumSmooth,           !- Roughness
  0.1,                    !- Thickness
  1.0,                    !- Conductivity
  2000,                   !- Density
  1000;                   !- Specific Heat

Construction,
  TestConstruction,       !- Name
  TestMaterial;           !- Outside Layer

ScheduleTypeLimits,
  Fraction,               !- Name
  0,                      !- Lower Limit
  1,                      !- Upper Limit
  Continuous;             !- Numeric Type

Schedule:Constant,
  AlwaysOn,               !- Name
  Fraction,               !- Schedule Type Limits Name
  1.0;                    !- Hourly Value

People,
  TestPeople,             !- Name
  TestZone,               !- Zone Name
  AlwaysOn,               !- Number of People Schedule Name
  People,                 !- Number of People Calculation Method
  10;                     !- Number of People
"""
    filepath = tmp_path / "test.idf"
    filepath.write_text(content)
    return filepath


@pytest.fixture
def epjson_file(tmp_path: Path) -> Path:
    """Create a temporary epJSON file."""
    data = {
        "Version": {"Version 1": {"version_identifier": "24.1"}},
        "Zone": {
            "TestZone": {
                "direction_of_relative_north": 0,
                "x_origin": 0,
                "y_origin": 0,
                "z_origin": 0,
                "type": 1,
                "multiplier": 1,
            }
        },
        "Material": {
            "TestMaterial": {
                "roughness": "MediumSmooth",
                "thickness": 0.1,
                "conductivity": 1.0,
                "density": 2000,
                "specific_heat": 1000,
            }
        },
        "Construction": {"TestConstruction": {"outside_layer": "TestMaterial"}},
    }
    filepath = tmp_path / "test.epJSON"
    filepath.write_text(json.dumps(data, indent=2))
    return filepath


@pytest.fixture
def reference_graph() -> ReferenceGraph:
    """Create a ReferenceGraph with some sample data."""
    graph = ReferenceGraph()
    obj_a = IDFObject(obj_type="People", name="PeopleA", data={"zone_name": "Zone1"})
    obj_b = IDFObject(obj_type="Lights", name="LightsB", data={"zone_name": "Zone1"})
    obj_c = IDFObject(obj_type="People", name="PeopleC", data={"zone_name": "Zone2"})

    graph.register(obj_a, "zone_name", "Zone1")
    graph.register(obj_b, "zone_name", "Zone1")
    graph.register(obj_c, "zone_name", "Zone2")

    return graph
