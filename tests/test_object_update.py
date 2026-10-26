"""Tests for IDFObject.update: one multi-field update, examined in full before anything is applied."""

from __future__ import annotations

from typing import Any

import pytest

from idfkit import IDFDocument, IDFObject, new_document
from idfkit.exceptions import InvalidFieldError, RefusedEntry

_VERTEX = {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0}


def _heater(doc: IDFDocument[Any]) -> IDFObject:
    return doc.add(
        "WaterHeater:Mixed",
        "Heater",
        setpoint_temperature_schedule_name="Setpoint",
        ambient_temperature_indicator="Schedule",
        heater_fuel_type="NaturalGas",
        heater_thermal_efficiency=0.8,
    )


def _surface(doc: IDFDocument[Any]) -> IDFObject:
    return doc.add(
        "BuildingSurface:Detailed",
        "Wall",
        surface_type="Wall",
        construction_name="Construction",
        zone_name="Zone A",
        outside_boundary_condition="Outdoors",
        vertices=[dict(_VERTEX), dict(_VERTEX), dict(_VERTEX)],
    )


def _snapshot(obj: IDFObject) -> tuple[str, dict[str, Any], int]:
    return obj.name, obj.to_dict(), obj.mutation_version


class TestApplied:
    def test_four_fields_in_one_call(self) -> None:
        heater = _heater(new_document())
        heater.update(
            heater_fuel_type="Electricity",
            off_cycle_parasitic_fuel_type="Electricity",
            heater_thermal_efficiency=1.0,
            on_cycle_parasitic_fuel_type="Electricity",
        )
        assert heater.heater_fuel_type == "Electricity"
        assert heater.off_cycle_parasitic_fuel_type == "Electricity"
        assert heater.heater_thermal_efficiency == 1.0
        assert heater.on_cycle_parasitic_fuel_type == "Electricity"

    def test_returns_none(self) -> None:
        heater = _heater(new_document())
        assert heater.update(heater_thermal_efficiency=0.9) is None

    def test_mapping_and_keywords_keyword_wins(self) -> None:
        heater = _heater(new_document())
        heater.update(
            {"heater_thermal_efficiency": 0.5, "heater_fuel_type": "Electricity"},
            heater_thermal_efficiency=0.95,
        )
        assert heater.heater_thermal_efficiency == 0.95
        assert heater.heater_fuel_type == "Electricity"

    def test_values_keyword_is_a_field_name_not_the_mapping(self) -> None:
        # ``values`` is positional-only, so ``values=`` is an entry and is examined as one.
        heater = _heater(new_document())
        with pytest.raises(InvalidFieldError):
            heater.update(values=1.0)

    @pytest.mark.parametrize(
        "mapping",
        [{"X Origin": 2.0}, {"x_origin": 1.0, "X Origin": 2.0}, {"X Origin": 2.0, "x_origin": 1.0}],
    )
    def test_keyword_wins_over_any_spelling_in_the_mapping(self, mapping: dict[str, float]) -> None:
        zone = new_document().add("Zone", "Office")
        zone.update(mapping, x_origin=3.0)
        assert zone.x_origin == 3.0

    def test_field_names_normalized_as_single_assignment(self) -> None:
        heater = _heater(new_document())
        heater.update({"Heater Thermal Efficiency": 0.7})
        assert heater.heater_thermal_efficiency == 0.7

    def test_none_clears_a_field(self) -> None:
        heater = _heater(new_document())
        heater.update(heater_thermal_efficiency=None)
        assert heater.heater_thermal_efficiency is None

    def test_empty_group_changes_nothing(self) -> None:
        heater = _heater(new_document())
        before = _snapshot(heater)
        heater.update()
        heater.update({})
        assert _snapshot(heater) == before

    def test_wrapper_key_replaces_the_list(self) -> None:
        surface = _surface(new_document())
        surface.update(vertices=[{**_VERTEX, "vertex_x_coordinate": 1.0}, dict(_VERTEX)])
        assert len(surface.vertices) == 2
        assert surface.vertices[0].vertex_x_coordinate == 1.0


class TestRefused:
    def test_unknown_name(self) -> None:
        heater = _heater(new_document())
        before = _snapshot(heater)
        with pytest.raises(InvalidFieldError) as excinfo:
            heater.update(heater_fuel_type="Electricity", heater_fuel_typo="Electricity")
        assert excinfo.value.field_name == "heater_fuel_typo"
        assert _snapshot(heater) == before

    @pytest.mark.parametrize("key", ["name", "Name", "NAME"])
    def test_name_in_any_case(self, key: str) -> None:
        heater = _heater(new_document())
        before = _snapshot(heater)
        with pytest.raises(InvalidFieldError, match="rename"):
            heater.update({"heater_thermal_efficiency": 0.9, key: "Other"})
        assert _snapshot(heater) == before

    def test_legacy_flat_extensible_name(self) -> None:
        surface = _surface(new_document())
        before = _snapshot(surface)
        with pytest.raises(InvalidFieldError, match="vertex_3_x_coordinate"):
            surface.update(surface_type="Roof", vertex_3_x_coordinate=5.0)
        assert _snapshot(surface) == before

    def test_wrapper_key_with_a_non_list_value(self) -> None:
        surface = _surface(new_document())
        before = _snapshot(surface)
        with pytest.raises(TypeError, match="vertices"):
            surface.update(surface_type="Roof", vertices=dict(_VERTEX))
        assert _snapshot(surface) == before

    @pytest.mark.parametrize(
        "vertices",
        [
            [dict(_VERTEX), dict(_VERTEX), {"bogus": 1}],
            [dict(_VERTEX), dict(_VERTEX), "vertex"],
            [dict(_VERTEX), dict(_VERTEX), 5.0],
        ],
        ids=["unknown-inner-field", "string-item", "number-item"],
    )
    def test_wrapper_list_whose_contents_single_assignment_rejects(self, vertices: list[Any]) -> None:
        surface = _surface(new_document())
        before = _snapshot(surface)
        with pytest.raises(TypeError, match="  - vertices: wrapper-value"):
            surface.update(surface_type="Roof", vertices=vertices)
        assert _snapshot(surface) == before

    @pytest.mark.parametrize("key", ["Name ", " NAME", "name_"])
    def test_names_that_resolve_to_name(self, key: str) -> None:
        heater = _heater(new_document())
        before = _snapshot(heater)
        with pytest.raises(InvalidFieldError, match=f"  - {key}: name"):
            heater.update({key: "Other"})
        assert _snapshot(heater) == before

    def test_private_attribute_name(self) -> None:
        heater = _heater(new_document())
        before = _snapshot(heater)
        with pytest.raises(InvalidFieldError):
            heater.update(_name="Other")
        assert _snapshot(heater) == before

    def test_mixed_group_lists_every_refused_entry_in_order(self) -> None:
        surface = _surface(new_document())
        before = _snapshot(surface)
        with pytest.raises(InvalidFieldError) as excinfo:
            surface.update(
                surface_type="Roof",
                bogus=1,
                name="Other",
                vertex_3_x_coordinate=5.0,
                vertices="not a list",
            )
        assert excinfo.value.field_name == "bogus"
        message = str(excinfo.value)
        positions = [message.index(f"  - {key}:") for key in ("bogus", "name", "vertex_3_x_coordinate", "vertices")]
        assert positions == sorted(positions)
        assert "surface_type" not in message.split("Available fields")[0]
        assert _snapshot(surface) == before

    def test_field_name_is_the_first_entry_refused_for_its_name(self) -> None:
        surface = _surface(new_document())
        with pytest.raises(InvalidFieldError) as excinfo:
            surface.update(vertices="not a list", bogus=1)
        assert excinfo.value.field_name == "bogus"
        assert excinfo.value.refused == (
            RefusedEntry("vertices", "wrapper-value", "expected a list, got str"),
            RefusedEntry("bogus", "unknown", "not a field of BuildingSurface:Detailed"),
        )

    def test_unknown_name_refused_in_a_non_strict_document(self) -> None:
        doc = new_document(strict=False)
        heater = _heater(doc)
        heater.bogus = 1  # single assignment accepts it here
        before = _snapshot(heater)
        with pytest.raises(InvalidFieldError):
            heater.update(heater_thermal_efficiency=0.9, other_bogus=1)
        assert _snapshot(heater) == before

    def test_reference_graph_unchanged_on_refusal(self) -> None:
        doc = new_document()
        surface = _surface(doc)
        with pytest.raises(InvalidFieldError):
            surface.update(zone_name="Zone B", bogus=1)
        assert doc.get_referencing("Zone A") == {surface}
        assert doc.get_referencing("Zone B") == set()


class TestDetached:
    def test_applies_like_single_assignment(self) -> None:
        zone = IDFObject("Zone", "Detached")
        zone.update(x_origin=1.0, anything=2)
        assert zone.x_origin == 1.0
        assert zone.anything == 2

    def test_name_still_refused_and_nothing_applied(self) -> None:
        zone = IDFObject("Zone", "Detached")
        before = _snapshot(zone)
        with pytest.raises(InvalidFieldError):
            zone.update(x_origin=1.0, name="Other")
        assert _snapshot(zone) == before


class TestEquivalentToSingleAssignment:
    """FR-007: an accepted group has exactly the effects of consecutive single assignments."""

    def test_values_references_and_notifications(self, monkeypatch: pytest.MonkeyPatch) -> None:
        group: dict[str, Any] = {
            "zone_name": "Zone B",
            "surface_type": "Roof",
            "construction_name": "Other Construction",
            "view_factor_to_ground": None,
        }
        calls: list[tuple[str, Any, Any]] = []
        original = IDFDocument.notify_reference_change

        def record(self: IDFDocument[Any], obj: IDFObject, field_name: str, old: Any, new: Any) -> None:
            calls.append((field_name, old, new))
            original(self, obj, field_name, old, new)

        monkeypatch.setattr(IDFDocument, "notify_reference_change", record)

        by_update = new_document()
        updated = _surface(by_update)
        calls.clear()
        updated.update(group)
        update_calls = list(calls)

        by_assignment = new_document()
        assigned = _surface(by_assignment)
        calls.clear()
        for key, value in group.items():
            setattr(assigned, key, value)
        assignment_calls = list(calls)

        assert updated.to_dict() == assigned.to_dict()
        assert updated.mutation_version == assigned.mutation_version
        assert update_calls == assignment_calls
        for name in ("Zone A", "Zone B", "Construction", "Other Construction"):
            assert {o.name for o in by_update.get_referencing(name)} == {
                o.name for o in by_assignment.get_referencing(name)
            }


class TestInvalidFieldErrorMessage:
    def test_existing_raise_sites_unchanged(self) -> None:
        error = InvalidFieldError("Zone", "bogus", available_fields=["x_origin", "y_origin"])
        assert str(error) == "Invalid field 'bogus' for object type 'Zone'\nAvailable fields: x_origin, y_origin"
