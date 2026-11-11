"""Tests for the identity and coverage types shared by the model-graph layers."""

from __future__ import annotations

import pytest

from idfkit._graph_common import MAX_EXAMPLES, Coverage, ObjectKey, UncoveredPart


class TestObjectKey:
    def test_equality_ignores_case_of_both_fields(self) -> None:
        assert ObjectKey("Coil:Heating:Water", "Reheat 1") == ObjectKey("COIL:HEATING:WATER", "reheat 1")

    def test_hash_matches_equality(self) -> None:
        keys = {ObjectKey("Zone", "Office"), ObjectKey("ZONE", "OFFICE"), ObjectKey("zone", "office")}
        assert len(keys) == 1

    def test_display_spelling_is_kept(self) -> None:
        key = ObjectKey("Zone", "Office East")
        assert key.object_type == "Zone"
        assert key.name == "Office East"

    def test_same_name_different_type_differs(self) -> None:
        assert ObjectKey("Zone", "A") != ObjectKey("Node", "A")
        assert len({ObjectKey("Zone", "A"), ObjectKey("Node", "A")}) == 2

    def test_not_equal_to_other_types(self) -> None:
        assert ObjectKey("Zone", "A") != ("Zone", "A")

    def test_is_frozen(self) -> None:
        key = ObjectKey("Zone", "A")
        with pytest.raises(AttributeError):
            key.name = "B"  # type: ignore[misc]


class TestUncoveredPart:
    def test_three_examples_allowed(self) -> None:
        examples = tuple(ObjectKey("EnergyManagementSystem:Program", f"P{i}") for i in range(MAX_EXAMPLES))
        part = UncoveredPart("ems_program", 7, examples, "EMS program text is not parsed.")
        assert len(part.examples) == 3
        assert part.count == 7

    def test_more_than_three_examples_rejected(self) -> None:
        examples = tuple(ObjectKey("EnergyManagementSystem:Program", f"P{i}") for i in range(4))
        with pytest.raises(ValueError, match="at most 3"):
            UncoveredPart("ems_program", 4, examples, "EMS program text is not parsed.")

    def test_negative_count_rejected(self) -> None:
        with pytest.raises(ValueError, match="negative"):
            UncoveredPart("hvac_template", -1, (), "Templates are not expanded.")


class TestCoverage:
    def test_empty_is_not_partial(self) -> None:
        coverage = Coverage.of(())
        assert coverage.partial is False
        assert coverage.uncovered == ()
        assert coverage.resolved is None
        assert coverage.unresolved is None

    def test_uncovered_makes_partial(self) -> None:
        part = UncoveredPart("hvac_template", 1, (ObjectKey("HVACTemplate:Zone:IdealLoadsAirSystem", "Z"),), "x")
        assert Coverage.of((part,)).partial is True

    def test_linking_counts(self) -> None:
        coverage = Coverage.of((), resolved=95, unresolved=5)
        assert (coverage.resolved, coverage.unresolved) == (95, 5)

    @pytest.mark.parametrize("partial", [True, False])
    def test_inconsistent_partial_rejected(self, partial: bool) -> None:
        part = UncoveredPart("unlinked_result", 1, (ObjectKey("Unresolved", "FOO"),), "x")
        uncovered = () if partial else (part,)
        with pytest.raises(ValueError, match="partial"):
            Coverage(partial=partial, uncovered=uncovered)
