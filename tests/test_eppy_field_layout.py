"""eppy's field layout, field spellings and surface geometry on IDFObject.

Covers ``fieldnames``/``fieldvalues`` in eppy's ``[key, Name, fields..., groups...]`` layout, eppy's
punctuation-free spelling of IDD names (``Vertex_1_Xcoordinate``), the surface geometry attributes
(``surf.area``, ``surf.coords``, ...) and the hints an unknown eppy-only attribute carries.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import pytest

from idfkit import IDFDocument, load_idf, new_document
from idfkit._eppy_names import (
    _GROUP_NUMBER_POSITION,  # pyright: ignore[reportPrivateUsage]
    eppy_field_aliases,
    eppy_field_name,
    numbered_idd_name,
)
from idfkit.exceptions import InvalidFieldError, MissingRequiredFieldError

_IDF = """\
Version, 24.1;
Material, RG01, Rough, 0.0127, 1.442, 881, 1674;
Material, BR01, VeryRough, 0.0095, 0.162, 1121, 1464;
Material, IN46, VeryRough, 0.0762, 0.023, 24, 1590;
Construction, ROOF-1, RG01, BR01, IN46;
Zone, Z1;
BuildingSurface:Detailed, WALL-1, Wall, ROOF-1, Z1, , Outdoors, , SunExposed, WindExposed, 0.5, 4,
    0, 0, 3,
    0, 0, 0,
    10, 0, 0,
    10, 0, 3;
BuildingSurface:Detailed, ROOF-1S, Roof, ROOF-1, Z1, , Outdoors, , SunExposed, WindExposed, 0, 4,
    0, 5, 3,
    0, 0, 3,
    10, 0, 3,
    10, 5, 3;
FenestrationSurface:Detailed, WIN-1, Window, ROOF-1, WALL-1, , 0.5, , 1, 4,
    2, 0, 2.5,
    2, 0, 1,
    8, 0, 1,
    8, 0, 2.5;
ScheduleTypeLimits, Fraction, 0, 1, Continuous;
Schedule:Compact, OCCUPY-1, Fraction, Through: 12/31, For: AllDays, Until: 24:00, 1.0;
BranchList, Branches, Main Branch, Second Branch;
Timestep, 4;
"""


@pytest.fixture
def doc(tmp_path: Path) -> IDFDocument:
    path = tmp_path / "eppy.idf"
    path.write_text(_IDF)
    return load_idf(path)


class TestEppyNames:
    def test_eppy_field_name_drops_punctuation(self) -> None:
        assert eppy_field_name("Vertex 1 X-coordinate") == "Vertex_1_Xcoordinate"
        assert eppy_field_name("U-Factor") == "UFactor"

    def test_numbered_idd_name(self) -> None:
        assert numbered_idd_name("Vertex X-coordinate", 4) == "Vertex 4 X-coordinate"
        assert numbered_idd_name("Field", 2) == "Field 2"
        assert numbered_idd_name("Value Until Time", 1, 3) == "Value Until Time 1"
        assert numbered_idd_name("Fenestration Surface Name", 2, 2) == "Fenestration Surface 2 Name"

    def test_aliases_only_for_differing_spellings(self, doc: IDFDocument) -> None:
        schema = doc.schema
        assert schema is not None
        pc = schema.get_parsing_cache("FenestrationSurface:Detailed")
        assert pc is not None
        assert pc.eppy_aliases["vertex_1_xcoordinate"] == "vertex_1_x_coordinate"
        assert "surface_type" not in pc.eppy_aliases
        zone = schema.get_parsing_cache("Zone")
        assert zone is not None
        assert eppy_field_aliases(zone.obj_schema) == {}


class TestFieldLayout:
    def test_construction_layers_follow_name(self, doc: IDFDocument) -> None:
        c = doc.idfobjects["CONSTRUCTION"][0]
        assert c.fieldvalues[:2] == [c.key, "ROOF-1"]
        # The eppy idiom: every layer, outside layer first, with no trailing padding.
        assert c.fieldvalues[2:] == ["RG01", "BR01", "IN46"]
        assert c.fieldnames[:4] == ["key", "Name", "Outside_Layer", "Layer_2"]

    def test_surface_vertices_are_flattened(self, doc: IDFDocument) -> None:
        s = doc.idfobjects["BUILDINGSURFACE:DETAILED"]["WALL-1"]
        names, values = s.fieldnames, s.fieldvalues
        start = names.index("Vertex_1_Xcoordinate")
        assert names[start : start + 4] == [
            "Vertex_1_Xcoordinate",
            "Vertex_1_Ycoordinate",
            "Vertex_1_Zcoordinate",
            "Vertex_2_Xcoordinate",
        ]
        assert values[start:] == [0, 0, 3, 0, 0, 0, 10, 0, 0, 10, 0, 3]
        assert len(names) == len(values)

    def test_schedule_compact_fields(self, doc: IDFDocument) -> None:
        sched = doc.idfobjects["SCHEDULE:COMPACT"][0]
        assert sched.fieldvalues[3:] == ["Through: 12/31", "For: AllDays", "Until: 24:00", 1.0]
        assert sched.fieldnames[3:5] == ["Field_1", "Field_2"]

    def test_branchlist_is_flat(self, doc: IDFDocument) -> None:
        bl = doc.idfobjects["BRANCHLIST"][0]
        assert bl.fieldvalues == [bl.key, "Branches", "Main Branch", "Second Branch"]
        assert bl.fieldnames == ["key", "Name", "Branch_1_Name", "Branch_2_Name"]

    def test_nameless_type_has_no_name_entry(self, doc: IDFDocument) -> None:
        ts = doc.idfobjects["TIMESTEP"][0]
        assert ts.fieldnames == ["key", "Number_of_Timesteps_per_Hour"]
        assert ts.fieldvalues == [ts.key, 4]

    def test_every_name_reads_its_value(self, doc: IDFDocument) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            for collection in doc.collections.values():
                for obj in collection:
                    for name, value in zip(obj.fieldnames, obj.fieldvalues, strict=False):
                        assert obj[name] == value, (obj.obj_type, name)

    def test_required_blank_reads_none_through_get(self) -> None:
        doc = new_document()
        wall = doc.add(
            "BuildingSurface:Detailed",
            "W",
            surface_type="Wall",
            construction_name="C",
            outside_boundary_condition="Outdoors",
            validate=False,
        )
        assert wall.fieldvalues[wall.fieldnames.index("Zone_Name")] is None
        assert [wall.get(n) for n in wall.fieldnames[: len(wall.fieldvalues)]] == wall.fieldvalues
        with pytest.raises(MissingRequiredFieldError):
            _ = wall["Zone_Name"]


class TestGroupNumberPosition:
    """Extensible fields the IDD numbers somewhere other than after the first word."""

    def test_schedule_day_interval(self) -> None:
        doc = new_document()
        sd = doc.add(
            "Schedule:Day:Interval",
            "SD",
            data=[{"time": "24:00", "value_until_time": 1.0}],
            validate=False,
        )
        assert sd.fieldnames[-2:] == ["Time_1", "Value_Until_Time_1"]
        with pytest.warns(DeprecationWarning, match="flat-extensible"):
            assert sd["Value_Until_Time_1"] == 1.0

    def test_schedule_week_compact_and_window_shading(self) -> None:
        doc = new_document()
        wk = doc.add(
            "Schedule:Week:Compact",
            "W",
            data=[{"daytype_list": "AllDays", "schedule_day_name": "SD"}],
            validate=False,
        )
        assert wk.fieldnames[2:] == ["DayType_List_1", "ScheduleDay_Name_1"]
        wsc = doc.add(
            "WindowShadingControl",
            "WSC",
            fenestration_surfaces=[{"fenestration_surface_name": "Win1"}, {"fenestration_surface_name": "Win2"}],
            validate=False,
        )
        assert wsc.fieldnames[-2:] == ["Fenestration_Surface_1_Name", "Fenestration_Surface_2_Name"]

    @pytest.mark.parametrize("obj_type", sorted(_GROUP_NUMBER_POSITION))
    def test_every_name_reads_its_value(self, obj_type: str) -> None:
        doc = new_document()
        schema = doc.schema
        assert schema is not None
        pc = schema.get_parsing_cache(obj_type)
        assert pc is not None
        assert pc.ext_wrapper_key is not None
        groups = [{key: f"v{g}{i}" for i, key in enumerate(pc.ext_field_names)} for g in range(2)]
        obj = doc.add(obj_type, "N" if pc.has_name else "", validate=False, **{pc.ext_wrapper_key: groups})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            for name, value in zip(obj.fieldnames, obj.fieldvalues, strict=True):
                assert obj.get(name) == value, (obj_type, name)


class TestEppyVertexSpelling:
    def test_extensible_vertex_read_and_write(self, doc: IDFDocument) -> None:
        s = doc.idfobjects["BUILDINGSURFACE:DETAILED"]["WALL-1"]
        with pytest.warns(DeprecationWarning, match=r"vertices\[1\]\.vertex_z_coordinate"):
            assert s.Vertex_2_Zcoordinate == 0
        with pytest.warns(DeprecationWarning):
            s.Vertex_1_Xcoordinate = 5.0
        assert s.vertices[0].vertex_x_coordinate == 5.0

    def test_fixed_vertex_fields(self, doc: IDFDocument) -> None:
        f = doc.idfobjects["FENESTRATIONSURFACE:DETAILED"][0]
        assert f.Vertex_1_Xcoordinate == 2
        f.Vertex_1_Xcoordinate = 3.0
        assert f.vertex_1_x_coordinate == 3.0
        f.update(Vertex_2_Xcoordinate=4.0)
        assert f.vertex_2_x_coordinate == 4.0
        assert f["Vertex_3_Zcoordinate"] == 1

    def test_unknown_field_error_shows_group_access(self, doc: IDFDocument) -> None:
        s = doc.idfobjects["BUILDINGSURFACE:DETAILED"]["WALL-1"]
        with pytest.raises(InvalidFieldError, match=r"obj\.vertices\[0\]\.vertex_x_coordinate"):
            _ = s.vertex_x
        sched = doc.idfobjects["SCHEDULE:COMPACT"][0]
        with pytest.raises(InvalidFieldError, match=r"obj\['data'\]\[0\]\.field"):
            _ = sched.fieldz


class TestSurfaceGeometry:
    def test_wall_geometry(self, doc: IDFDocument) -> None:
        s = doc.idfobjects["BUILDINGSURFACE:DETAILED"]["WALL-1"]
        assert s.area == pytest.approx(30.0)
        assert s.azimuth == pytest.approx(180.0)
        assert s.tilt == pytest.approx(90.0)
        assert s.height == pytest.approx(3.0)
        assert s.width == pytest.approx(10.0)
        assert s.coords == [(0.0, 0.0, 3.0), (0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (10.0, 0.0, 3.0)]

    def test_roof_and_window(self, doc: IDFDocument) -> None:
        roof = doc.idfobjects["BUILDINGSURFACE:DETAILED"]["ROOF-1S"]
        assert roof.tilt == pytest.approx(0.0)
        assert roof.area == pytest.approx(50.0)
        win = doc.idfobjects["FENESTRATIONSURFACE:DETAILED"][0]
        assert win.area == pytest.approx(9.0)
        assert win.height == pytest.approx(1.5)
        assert win.width == pytest.approx(6.0)

    def test_surface_without_vertices(self, doc: IDFDocument) -> None:
        s = doc.idfobjects["BUILDINGSURFACE:DETAILED"]["WALL-1"]
        s.vertices = []
        assert s.area == 0.0
        assert s.coords == []

    @pytest.mark.parametrize("obj_type", ["Wall:Detailed", "RoofCeiling:Detailed", "Floor:Detailed"])
    def test_zone_detailed_surfaces(self, obj_type: str) -> None:
        doc = new_document()
        corners = [(0.0, 0.0, 3.0), (0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (10.0, 0.0, 3.0)]
        surf = doc.add(
            obj_type,
            "S",
            vertices=[
                {"vertex_x_coordinate": x, "vertex_y_coordinate": y, "vertex_z_coordinate": z} for x, y, z in corners
            ],
            validate=False,
        )
        assert surf.area == pytest.approx(30.0)
        assert surf.tilt == pytest.approx(90.0)
        assert surf.coords == corners

    def test_non_surface_points_to_replacement(self, doc: IDFDocument) -> None:
        zone = doc.idfobjects["ZONE"][0]
        with pytest.raises(InvalidFieldError, match="calculate_zone_floor_area"):
            _ = zone.area
        with pytest.raises(InvalidFieldError, match=r"obj\.fieldvalues"):
            _ = zone.obj
        with pytest.raises(InvalidFieldError, match="get_field_idd"):
            _ = zone.objidd

    def test_true_azimuth_points_to_replacement(self, doc: IDFDocument) -> None:
        s = doc.idfobjects["BUILDINGSURFACE:DETAILED"]["WALL-1"]
        with pytest.raises(InvalidFieldError, match="calculate_surface_azimuth"):
            _ = s.true_azimuth


class TestNewIdfObjectEppySpelling:
    def test_newidfobject_takes_eppy_vertex_names(self, doc: IDFDocument) -> None:
        win = doc.newidfobject("FENESTRATIONSURFACE:DETAILED", Name="W2", Vertex_1_Xcoordinate=1.0)
        assert win.vertex_1_x_coordinate == 1.0
        with pytest.warns(DeprecationWarning, match="flat-extensible"):
            wall = doc.newidfobject(
                "BUILDINGSURFACE:DETAILED",
                Name="S2",
                Vertex_1_Xcoordinate=1.0,
                Vertex_1_Ycoordinate=2.0,
                Vertex_1_Zcoordinate=3.0,
            )
        assert wall.vertices[0].as_dict() == {
            "vertex_x_coordinate": 1.0,
            "vertex_y_coordinate": 2.0,
            "vertex_z_coordinate": 3.0,
        }
