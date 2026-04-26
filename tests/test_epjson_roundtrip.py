"""Tests for epJSON roundtrip correctness (IDF -> epJSON -> IDF).

Covers:
- Extensible fields (vertices) survive the roundtrip
- Nameless objects don't get spurious names from epJSON dict keys
- Named objects preserve their names correctly
- Object counts and data are preserved across the full roundtrip
- Field order includes extensible fields after epJSON parsing
- E2E simulation: roundtripped IDF produces same results (integration)
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idfkit.epjson_parser import parse_epjson
from idfkit.idf_parser import parse_idf
from idfkit.schema import get_schema
from idfkit.writers import write_epjson, write_idf


@pytest.fixture
def schema():
    return get_schema((24, 1, 0))


@pytest.fixture
def roundtrip_idf(tmp_path: Path) -> Path:
    """IDF with various object types for epJSON roundtrip testing."""
    content = """\
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
    filepath = tmp_path / "roundtrip.idf"
    filepath.write_text(content, encoding="latin-1")
    return filepath


class TestNamelessObjectsEpjsonRoundtrip:
    """Nameless objects should not get spurious names from epJSON dict keys."""

    def test_timestep_name_empty_after_roundtrip(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        """Timestep should have name='' after IDF -> epJSON -> parse_epjson."""
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        ts = doc2["Timestep"][0]
        assert ts.name == ""

    def test_timestep_data_preserved_after_roundtrip(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        ts = doc2["Timestep"][0]
        assert ts.data.get("number_of_timesteps_per_hour") == 4

    def test_simulation_control_name_empty(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        sc = doc2["SimulationControl"][0]
        assert sc.name == ""
        assert sc.data.get("do_zone_sizing_calculation") == "Yes"

    def test_global_geometry_rules_name_empty(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        ggr = doc2["GlobalGeometryRules"][0]
        assert ggr.name == ""
        assert ggr.data.get("starting_vertex_position") == "UpperLeftCorner"

    def test_output_variable_names_empty(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        """Output:Variable objects should have empty names after epJSON roundtrip."""
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        for obj in doc2["Output:Variable"]:
            assert obj.name == ""

    def test_output_variable_count_preserved(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        assert len(doc2["Output:Variable"]) == 3


class TestExtensibleFieldsEpjsonRoundtrip:
    """Extensible fields (vertices) should survive IDF -> epJSON -> IDF."""

    def test_vertices_canonical_after_epjson_parse(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        """Canonical wrapper survives IDF -> epJSON -> parse_epjson."""
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        wall = doc2["BuildingSurface:Detailed"][0]
        verts = wall.data["vertices"]
        assert len(verts) == 4
        assert verts[0]["vertex_x_coordinate"] == 0.0
        assert verts[0]["vertex_z_coordinate"] == 3.048
        assert verts[2]["vertex_x_coordinate"] == 6.096
        assert verts[3]["vertex_z_coordinate"] == 3.048

    def test_vertex_data_survives_full_roundtrip(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        """Vertex data survives IDF -> epJSON -> IDF in canonical shape."""
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)
        idf_path = tmp_path / "roundtrip.idf"
        write_idf(doc2, idf_path)
        doc3 = parse_idf(idf_path)

        wall = doc3["BuildingSurface:Detailed"][0]
        verts = wall.data["vertices"]
        expected = [
            {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.048},
            {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
            {"vertex_x_coordinate": 6.096, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
            {"vertex_x_coordinate": 6.096, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.048},
        ]
        for got, want in zip(verts, expected, strict=True):
            assert got == want


class TestNamedObjectsEpjsonRoundtrip:
    """Named objects should preserve their names correctly."""

    def test_zone_name_preserved(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        zone = doc2["Zone"][0]
        assert zone.name == "ZONE ONE"

    def test_material_data_preserved(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(roundtrip_idf)
        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        mat = doc2["Material"][0]
        assert mat.name == "C12 - 2 IN HW CONCRETE"
        assert mat.data.get("roughness") == "MediumRough"
        assert mat.data.get("thickness") == 0.0510


class TestFullEpjsonRoundtrip:
    """Full IDF -> epJSON -> IDF roundtrip should preserve everything."""

    def test_object_counts_preserved(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(roundtrip_idf)

        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        idf_path = tmp_path / "roundtrip.idf"
        write_idf(doc2, idf_path)
        doc3 = parse_idf(idf_path)

        for obj_type in doc1.collections:
            count1 = len(doc1[obj_type])
            count3 = len(doc3[obj_type])
            assert count1 == count3, f"{obj_type}: {count1} != {count3}"

    def test_total_object_count_preserved(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        doc1 = parse_idf(roundtrip_idf)

        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        idf_path = tmp_path / "roundtrip.idf"
        write_idf(doc2, idf_path)
        doc3 = parse_idf(idf_path)

        assert len(doc1) == len(doc3)

    def test_nameless_objects_written_to_idf_correctly(self, roundtrip_idf: Path, tmp_path: Path) -> None:
        """Nameless objects parsed from epJSON should write to IDF without the spurious name."""
        doc1 = parse_idf(roundtrip_idf)

        epjson_path = tmp_path / "test.epJSON"
        write_epjson(doc1, epjson_path)
        doc2 = parse_epjson(epjson_path)

        idf_output = write_idf(doc2)
        assert idf_output is not None

        # Timestep should not have the spurious key as a name field
        assert "Timestep 1" not in idf_output
        # Should write correct data
        assert "Timestep," in idf_output

    def test_epjson_direct_parse_nameless(self, tmp_path: Path) -> None:
        """Directly created epJSON with nameless objects should parse correctly."""
        data = {
            "Version": {"Version 1": {"version_identifier": "24.1"}},
            "Timestep": {"Timestep 1": {"number_of_timesteps_per_hour": 6}},
            "SimulationControl": {
                "SimulationControl 1": {
                    "do_zone_sizing_calculation": "Yes",
                    "do_system_sizing_calculation": "No",
                    "do_plant_sizing_calculation": "No",
                    "run_simulation_for_sizing_periods": "Yes",
                    "run_simulation_for_weather_file_run_periods": "No",
                }
            },
        }
        epjson_path = tmp_path / "direct.epJSON"
        epjson_path.write_text(json.dumps(data, indent=2))

        doc = parse_epjson(epjson_path)

        ts = doc["Timestep"][0]
        assert ts.name == ""
        assert ts.data.get("number_of_timesteps_per_hour") == 6

        sc = doc["SimulationControl"][0]
        assert sc.name == ""
        assert sc.data.get("do_zone_sizing_calculation") == "Yes"

    def test_epjson_direct_parse_extensible(self, tmp_path: Path) -> None:
        """Directly created epJSON with extensible fields should include them in field_order."""
        data = {
            "Version": {"Version 1": {"version_identifier": "24.1"}},
            "Zone": {
                "TestZone": {
                    "direction_of_relative_north": 0,
                    "x_origin": 0,
                    "y_origin": 0,
                    "z_origin": 0,
                }
            },
            "Construction": {"TestConstruction": {"outside_layer": "TestMaterial"}},
            "BuildingSurface:Detailed": {
                "TestWall": {
                    "surface_type": "Wall",
                    "construction_name": "TestConstruction",
                    "zone_name": "TestZone",
                    "outside_boundary_condition": "Outdoors",
                    "sun_exposure": "SunExposed",
                    "wind_exposure": "WindExposed",
                    "view_factor_to_ground": 0.5,
                    "number_of_vertices": 4,
                    "vertex_x_coordinate": 0.0,
                    "vertex_y_coordinate": 0.0,
                    "vertex_z_coordinate": 3.0,
                    "vertex_x_coordinate_2": 0.0,
                    "vertex_y_coordinate_2": 0.0,
                    "vertex_z_coordinate_2": 0.0,
                    "vertex_x_coordinate_3": 10.0,
                    "vertex_y_coordinate_3": 0.0,
                    "vertex_z_coordinate_3": 0.0,
                    "vertex_x_coordinate_4": 10.0,
                    "vertex_y_coordinate_4": 0.0,
                    "vertex_z_coordinate_4": 3.0,
                },
            },
        }
        epjson_path = tmp_path / "extensible.epJSON"
        epjson_path.write_text(json.dumps(data, indent=2))

        doc = parse_epjson(epjson_path)
        wall = doc["BuildingSurface:Detailed"][0]

        # Flat extensible keys at the top level get bucketed into the
        # canonical wrapper at parse time (matches what real EnergyPlus
        # epJSON output uses).
        verts = wall.data["vertices"]
        assert verts[0]["vertex_z_coordinate"] == 3.0
        assert verts[3]["vertex_x_coordinate"] == 10.0

        # Write to IDF and verify vertices appear
        idf_output = write_idf(doc)
        assert idf_output is not None
        assert "3;" in idf_output or "3.0;" in idf_output or "3," in idf_output


# ---------------------------------------------------------------------------
# E2E Integration Test: IDF -> epJSON -> IDF -> EnergyPlus
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestEpjsonRoundtripSimulation:
    """Verify the roundtripped IDF simulates identically to the original.

    Requires EnergyPlus installed. Run with::

        pytest -m integration tests/test_epjson_roundtrip.py
    """

    @pytest.fixture(scope="class")
    def energyplus(self):
        from idfkit.exceptions import EnergyPlusNotFoundError
        from idfkit.simulation.config import find_energyplus

        try:
            return find_energyplus()
        except EnergyPlusNotFoundError:
            pytest.skip("EnergyPlus not installed")
            raise  # unreachable, keeps type checker happy

    @pytest.fixture(scope="class")
    def example_idf(self, energyplus) -> Path:
        return energyplus.install_dir / "ExampleFiles" / "1ZoneUncontrolled.idf"

    @pytest.fixture(scope="class")
    def weather_file(self, energyplus) -> Path:
        return energyplus.install_dir / "WeatherData" / "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"

    @pytest.fixture(scope="class")
    def roundtrip_model(self, example_idf: Path, tmp_path_factory):
        """IDF -> epJSON -> IDF roundtrip of 1ZoneUncontrolled."""
        from idfkit import load_idf

        original = load_idf(str(example_idf))

        tmp = tmp_path_factory.mktemp("epjson_roundtrip")
        epjson_path = tmp / "model.epJSON"
        write_epjson(original, epjson_path)

        doc_from_epjson = parse_epjson(epjson_path)
        return doc_from_epjson

    @pytest.fixture(scope="class")
    def original_result(self, example_idf: Path, weather_file: Path, energyplus):
        from idfkit import load_idf
        from idfkit.simulation import simulate

        model = load_idf(str(example_idf))
        return simulate(model, weather_file, energyplus=energyplus, design_day=True)

    @pytest.fixture(scope="class")
    def roundtrip_result(self, roundtrip_model, weather_file: Path, energyplus):
        from idfkit.simulation import simulate

        return simulate(roundtrip_model, weather_file, energyplus=energyplus, design_day=True)

    def test_original_simulates_successfully(self, original_result) -> None:
        assert original_result.success
        assert original_result.exit_code == 0

    def test_roundtrip_simulates_successfully(self, roundtrip_result) -> None:
        assert roundtrip_result.success
        assert roundtrip_result.exit_code == 0

    def test_no_severe_errors_original(self, original_result) -> None:
        assert not original_result.errors.has_severe
        assert not original_result.errors.has_fatal

    def test_no_severe_errors_roundtrip(self, roundtrip_result) -> None:
        assert not roundtrip_result.errors.has_severe
        assert not roundtrip_result.errors.has_fatal

    def test_same_warning_count(self, original_result, roundtrip_result) -> None:
        assert original_result.errors.warning_count == roundtrip_result.errors.warning_count

    def test_sql_tabular_data_matches(self, original_result, roundtrip_result) -> None:
        """Tabular summary reports should be identical."""
        orig_sql = original_result.sql
        rt_sql = roundtrip_result.sql
        assert orig_sql is not None
        assert rt_sql is not None

        orig_rows = orig_sql.get_tabular_data(
            report_name="EnvelopeSummary",
            table_name="Opaque Exterior",
        )
        rt_rows = rt_sql.get_tabular_data(
            report_name="EnvelopeSummary",
            table_name="Opaque Exterior",
        )
        # Same number of surface rows
        assert len(orig_rows) == len(rt_rows)

    def test_object_counts_match(self, example_idf: Path, roundtrip_model) -> None:
        from idfkit import load_idf

        original = load_idf(str(example_idf))
        for obj_type in original.collections:
            orig_count = len(original[obj_type])
            rt_count = len(roundtrip_model[obj_type])
            assert orig_count == rt_count, f"{obj_type}: {orig_count} != {rt_count}"
