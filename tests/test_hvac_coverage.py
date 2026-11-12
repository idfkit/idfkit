"""What the topology view says it did not cover (research R-35, FR-004a).

An agent must tell "nothing found" from "not looked at". EMS programs, unexpanded templates and
types without rules are named in ``coverage``; EMS sensors and actuators keyed to a node become
control uses; program text is never searched.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import IDFDocument, load_idf
from idfkit.hvac import ConnectionType, HVACTopology, ObjectKey

LINKED = Path(__file__).parent / "fixtures" / "simulation" / "linked"


@pytest.fixture
def five_zone() -> IDFDocument:
    return load_idf(str(LINKED / "5ZoneAirCooled.idf"))


def test_unmodified_model_is_fully_covered(five_zone: IDFDocument) -> None:
    coverage = HVACTopology.from_document(five_zone).coverage
    assert coverage.partial is False
    assert coverage.uncovered == ()


def test_ems_programs_and_subroutines_are_listed(five_zone: IDFDocument) -> None:
    for i in range(4):
        five_zone.add("EnergyManagementSystem:Program", f"Program {i}", lines=[{"program_line": "SET X = 1"}])
    five_zone.add("EnergyManagementSystem:Subroutine", "Helper", lines=[{"program_line": "SET Y = 2"}])
    coverage = HVACTopology.from_document(five_zone).coverage
    assert coverage.partial is True
    (part,) = [p for p in coverage.uncovered if p.kind == "ems_program"]
    assert part.count == 5
    assert len(part.examples) == 3
    assert part.examples[0] == ObjectKey("EnergyManagementSystem:Program", "Program 0")
    assert "not parsed" in part.reason


def test_ems_sensor_and_actuator_on_a_node_are_control_uses(five_zone: IDFDocument) -> None:
    five_zone.add(
        "EnergyManagementSystem:Sensor",
        "Mixed Air T",
        output_variable_or_output_meter_index_key_name="Mixed Air Node 1",
        output_variable_or_output_meter_name="System Node Temperature",
    )
    five_zone.add(
        "EnergyManagementSystem:Actuator",
        "Supply Setpoint",
        actuated_component_unique_name="VAV Sys 1 Outlet Node",
        actuated_component_type="System Node Setpoint",
        actuated_component_control_type="Temperature Setpoint",
    )
    topo = HVACTopology.from_document(five_zone)

    (sensor,) = [u for u in topo.controls("Mixed Air Node 1") if u.rule == "ems_key"]
    assert sensor.connection is ConnectionType.SENSOR
    assert sensor.object == ObjectKey("EnergyManagementSystem:Sensor", "Mixed Air T")

    (actuator,) = [u for u in topo.controls("VAV Sys 1 Outlet Node") if u.rule == "ems_key"]
    assert actuator.connection is ConnectionType.ACTUATOR
    assert topo.unresolved_ems() == []


def test_unresolved_ems_keys_are_listed(five_zone: IDFDocument) -> None:
    five_zone.add(
        "EnergyManagementSystem:Sensor",
        "Ghost",
        output_variable_or_output_meter_index_key_name="No Such Thing",
        output_variable_or_output_meter_name="System Node Temperature",
    )
    topo = HVACTopology.from_document(five_zone)
    assert topo.unresolved_ems() == [ObjectKey("EnergyManagementSystem:Sensor", "Ghost")]


def test_ems_keys_naming_an_object_are_resolved_not_listed(five_zone: IDFDocument) -> None:
    five_zone.add(
        "EnergyManagementSystem:Sensor",
        "Coil Rate",
        output_variable_or_output_meter_index_key_name="Main Cooling Coil 1",
        output_variable_or_output_meter_name="Cooling Coil Total Cooling Rate",
    )
    assert HVACTopology.from_document(five_zone).unresolved_ems() == []


def test_program_text_is_never_searched(five_zone: IDFDocument) -> None:
    before = len(HVACTopology.from_document(five_zone).uses("Mixed Air Node 1"))
    five_zone.add(
        "EnergyManagementSystem:Program",
        "Mentions A Node",
        lines=[{"program_line": "SET Mixed Air Node 1 = 12"}],
    )
    topo = HVACTopology.from_document(five_zone)
    assert len(topo.uses("Mixed Air Node 1")) == before
    assert not any(u.object.object_type.startswith("EnergyManagementSystem") for u in topo.uses("Mixed Air Node 1"))


def test_unexpanded_templates_are_listed() -> None:
    doc = load_idf(str(LINKED / "HVACTemplate-5ZoneVAVWaterCooled.idf"))
    coverage = HVACTopology.from_document(doc).coverage
    (part,) = [p for p in coverage.uncovered if p.kind == "hvac_template"]
    assert part.count > 0
    assert all(k.object_type.startswith("HVACTemplate:") for k in part.examples)
    assert len(part.examples) <= 3
