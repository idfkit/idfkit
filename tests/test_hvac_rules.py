"""The generated connection-rule table (research R-04, FR-010a).

Every node-bearing type of the latest schema must have a rule, and every rule must say where it
came from. These checks run on the committed tables; regenerating them needs EnergyPlus and is not
part of the test suite.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import tomllib

from idfkit.hvac._node_fields import NODE_FIELDS
from idfkit.hvac._port_rules import PORT_RULES
from idfkit.hvac.topology import STRUCTURAL_TYPES
from idfkit.schema import get_schema

OVERRIDES = Path(__file__).resolve().parents[1] / "src" / "idfkit" / "codegen" / "port_rule_overrides.toml"
PROVENANCES = {"eplus_examples", "eplus_test_model", "hand_written"}


def _rule_fields(object_type: str) -> set[str]:
    top, ext = NODE_FIELDS[object_type]
    return set(top) | {f"*.{e}" for e in ext}


def _leaf(field: str) -> str:
    return field if "." not in field else f"*.{field.split('.', 1)[1]}"


def test_every_node_bearing_type_in_the_latest_schema_has_a_rule() -> None:
    schema = get_schema((26, 2, 0))
    missing = sorted(t for t in NODE_FIELDS if t in schema and t not in STRUCTURAL_TYPES and not PORT_RULES.get(t))
    assert missing == []


def test_every_rule_carries_a_known_provenance() -> None:
    bad = [
        (t, r.field, r.provenance) for t, rules in PORT_RULES.items() for r in rules if r.provenance not in PROVENANCES
    ]
    assert bad == []


def test_rules_name_node_fields_and_valid_streams() -> None:
    for object_type, rules in PORT_RULES.items():
        fields = _rule_fields(object_type)
        for rule in rules:
            assert _leaf(rule.field) in fields, (object_type, rule.field)
            assert rule.stream >= 1, (object_type, rule.field)


def test_predicates_name_existing_fields() -> None:
    schema = get_schema((26, 2, 0))
    for object_type, rules in PORT_RULES.items():
        for rule in rules:
            if rule.when is not None and object_type in schema:
                assert rule.when[0] in schema.get_all_field_names(object_type), (object_type, rule.when)


def test_most_rules_come_from_energyplus() -> None:
    counts = dict.fromkeys(PROVENANCES, 0)
    for rules in PORT_RULES.values():
        for rule in rules:
            counts[rule.provenance] += 1
    total = sum(counts.values())
    assert counts["eplus_examples"] + counts["eplus_test_model"] > 0.75 * total
    assert counts["eplus_test_model"] > 0


@pytest.mark.parametrize("section", ["rule", "accept", "ambiguous"])
def test_every_reviewed_override_states_its_reason(section: str) -> None:
    data = tomllib.loads(OVERRIDES.read_text(encoding="utf-8"))
    entries = data.get(section, [])
    assert entries, section
    assert all(str(e.get("reason", "")).strip() for e in entries)


def test_condenser_roles_depend_on_the_condenser_type() -> None:
    rules = [r for r in PORT_RULES["Chiller:Electric:EIR"] if r.field == "condenser_inlet_node_name"]
    by_type = {r.when[1]: r.connection.value for r in rules if r.when is not None}
    assert by_type == {"AirCooled": "OutsideAir", "EvaporativelyCooled": "OutsideAir", "WaterCooled": "Inlet"}
