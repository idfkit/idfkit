"""Tests for rule ``C006``: a literal in an ``add()`` call that no target release accepts."""

from __future__ import annotations

import textwrap

from idfkit.compat import check_compatibility
from idfkit.compat._models import DEFAULT_RULES, DIAGNOSTIC_CODES, RULE_SEVERITIES, CompatSeverity
from idfkit.versions import ENERGYPLUS_VERSIONS

_V89 = (8, 9, 0)
_V262 = (26, 2, 0)
_ALL = list(ENERGYPLUS_VERSIONS)
_IMP = "from idfkit import new_document, as_version\n"


def _check(body: str, *, imports: bool = True, targets: list[tuple[int, int, int]] | None = None) -> list[str]:
    source = (_IMP if imports else "") + textwrap.dedent(body)
    return [
        f"{d.code}:{d.message}" for d in check_compatibility(source, "t.py", targets or [_V89, _V262], select=["C006"])
    ]


class TestRegistered:
    def test_is_a_default_error(self) -> None:
        assert "C006" in DIAGNOSTIC_CODES
        assert RULE_SEVERITIES["C006"] is CompatSeverity.ERROR
        assert "C006" in DEFAULT_RULES


class TestObjectType:
    def test_a_type_no_target_has(self) -> None:
        (found,) = _check('doc = new_document()\ndoc.add("Zoen", "Office")\n')
        assert found.startswith("C006:")
        assert "'Zoen'" in found
        assert "UnknownObjectTypeError" in found
        assert "did you mean 'Zone'?" in found

    def test_suggested_fix_names_the_closest_type(self) -> None:
        source = _IMP + 'doc = new_document()\ndoc.add("Zoen", "Office")\n'
        (diagnostic,) = check_compatibility(source, "t.py", [_V89, _V262], select=["C006"])
        assert diagnostic.suggested_fix == '"Zone"'
        assert diagnostic.severity is CompatSeverity.ERROR

    def test_keywords_count_as_more_than_the_type_name(self) -> None:
        assert len(_check('doc = new_document()\ndoc.add("Output:SQLlite", option_type="SimpleAndTabular")\n')) == 1

    def test_a_type_some_target_has_is_c001s(self) -> None:
        assert _check('doc = new_document()\ndoc.add("Space", "S")\n') == []

    def test_case_is_not_a_misspelling(self) -> None:
        assert _check('doc = new_document()\ndoc.add("zone", "Office")\n') == []

    def test_a_lone_argument_is_not_reported(self) -> None:
        """set.add("x") takes one argument; idfkit's add() is called with a name or fields."""
        assert _check('seen = set()\nseen.add("Zoen")\n') == []

    def test_a_file_without_idfkit_is_not_reported(self) -> None:
        assert _check('registry.add("Zoen", "Office")\n', imports=False) == []

    def test_narrowed_scope_names_its_targets(self) -> None:
        (found,) = _check(
            'def f(doc):\n    as_version(doc, since="25.1").add("Zoen", "Office")\n',
            targets=_ALL,
        )
        assert "(25.1.0, 25.2.0, 26.1.0, 26.2.0)" in found


class TestChoiceValue:
    def test_a_value_no_target_lists(self) -> None:
        (found,) = _check('doc = new_document()\ndoc.add("Zone", "A", zone_inside_convection_algorithm="Bogus")\n')
        assert found.startswith("C006:")
        assert "'Bogus'" in found
        assert "Zone.zone_inside_convection_algorithm" in found
        assert "ValidationFailedError" in found

    def test_suggestion_for_a_near_miss(self) -> None:
        (found,) = _check('doc = new_document()\ndoc.add("Material", "M", roughness="MediumRuff")\n')
        assert "did you mean 'MediumRough'?" in found

    def test_case_differences_are_accepted(self) -> None:
        """EnergyPlus and add() match choices case-insensitively."""
        assert _check('doc = new_document()\ndoc.add("Zone", "A", zone_inside_convection_algorithm="Tarp")\n') == []

    def test_a_value_some_target_lists_is_c002s(self) -> None:
        source = 'doc = new_document()\ndoc.add("WaterHeater:Mixed", "W", heater_fuel_type="DistrictHeatingSteam")\n'
        assert _check(source, targets=[(23, 2, 0), _V262]) == []

    def test_a_free_text_field_in_some_target_is_not_reported(self) -> None:
        """8.9 to 9.2 accept any string for heater_fuel_type, so no value is refused by every target."""
        source = 'doc = new_document()\ndoc.add("WaterHeater:Mixed", "W", heater_fuel_type="Anything")\n'
        assert _check(source, targets=[_V89, _V262]) == []
        assert len(_check(source, targets=[(23, 2, 0), _V262])) == 1

    def test_dict_argument(self) -> None:
        assert (
            len(_check('doc = new_document()\ndoc.add("Zone", "A", {"zone_inside_convection_algorithm": "Bogus"})\n'))
            == 1
        )

    def test_unknown_type_reports_only_the_type(self) -> None:
        (found,) = _check('doc = new_document()\ndoc.add("Zoen", "A", zone_inside_convection_algorithm="Bogus")\n')
        assert "'Zoen'" in found

    def test_a_file_without_idfkit_is_not_reported(self) -> None:
        assert _check('registry.add("Zone", "A", zone_inside_convection_algorithm="Bogus")\n', imports=False) == []


class TestSuppression:
    def test_comment_silences(self) -> None:
        source = _IMP + 'doc = new_document()\ndoc.add("Zoen", "Office")  # idfkit: ignore[C006]\n'
        assert check_compatibility(source, "t.py", [_V89, _V262]) == []


class TestGroupFilter:
    def test_a_group_filter_does_not_hide_a_misspelled_type(self) -> None:
        source = _IMP + 'doc = new_document()\ndoc.add("Zoen", "Office")\n'
        diagnostics = check_compatibility(
            source, "t.py", [_V89, _V262], select=["C006"], include_groups={"Simulation Parameters"}
        )
        assert [d.code for d in diagnostics] == ["C006"]
