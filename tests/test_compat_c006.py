"""Tests for rule ``C006``: a literal in an ``add()`` call that no target release accepts."""

from __future__ import annotations

import textwrap

from idfkit.compat import check_compatibility
from idfkit.compat._models import DEFAULT_RULES, DIAGNOSTIC_CODES, RULE_SEVERITIES, CompatSeverity
from idfkit.versions import ENERGYPLUS_VERSIONS

_V89 = (8, 9, 0)
_V262 = (26, 2, 0)
_ALL = list(ENERGYPLUS_VERSIONS)
_IMP = "from idfkit import new_document, as_version, load_idf, load_epjson\n"


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


class TestReceivers:
    """``doc.add("Zone", "Office")`` takes a type first, a collection's ``add("Office")`` a name."""

    def test_collection_add_names_are_not_types(self) -> None:
        source = """\
doc = new_document()
doc.zones.add("Office", ceiling_height=3.0)
doc["Zone"].add("Lab")
zones = doc.zones
zones.add("Core", multiplier=1)
doc.get_collection("Zone").add("Annex")
"""
        assert _check(source) == []

    def test_collection_add_choices_are_checked_against_its_type(self) -> None:
        for receiver in ['doc["Zone"]', "doc.zones", 'doc.get_collection("Zone")']:
            source = f'doc = new_document()\n{receiver}.add("A", zone_inside_convection_algorithm="Bogus")\n'
            (found,) = _check(source)
            assert "Zone.zone_inside_convection_algorithm" in found

    def test_a_name_bound_to_a_collection(self) -> None:
        source = 'doc = new_document()\nzones = doc["Zone"]\nzones.add("A", zone_inside_convection_algorithm="Bogus")\n'
        assert len(_check(source)) == 1

    def test_a_parameter_annotated_as_a_collection(self) -> None:
        source = 'def f(zones: "IDFCollection[Zone]") -> None:\n    zones.add("Office", multiplier=1)\n'
        assert _check(source) == []

    def test_a_parameter_annotated_as_a_document(self) -> None:
        for annotation in ["IDFDocument", "AnyIDFDocument", "IDFDocumentV9_4", '"IDFDocument[Any]"']:
            source = f'def f(doc: {annotation}) -> None:\n    doc.add("Zoen", "Office")\n'
            assert len(_check(source)) == 1, annotation

    def test_documents_from_factories(self) -> None:
        for binding in ["new_document()", 'load_idf("m.idf")', 'load_epjson("m.epJSON")', "new_document().copy()"]:
            assert len(_check(f'doc = {binding}\ndoc.add("Zoen", "Office")\n')) == 1, binding

    def test_an_unknown_receiver_reports_no_type(self) -> None:
        """An unannotated parameter may be a collection, whose first argument is a name."""
        assert _check('def f(thing):\n    thing.add("Office", multiplier=1)\n') == []

    def test_an_unknown_receiver_still_reports_choices(self) -> None:
        source = 'def f(doc):\n    doc.add("Zone", "A", zone_inside_convection_algorithm="Bogus")\n'
        assert len(_check(source)) == 1

    def test_c001_is_not_read_from_a_collection_name(self) -> None:
        source = 'doc = new_document()\ndoc.zones.add("Space", multiplier=1)\n'
        diagnostics = check_compatibility(_IMP + source, "t.py", [_V89, _V262])
        assert diagnostics == []

    def test_a_document_held_in_a_dict_is_not_a_collection(self) -> None:
        """``docs["base"]`` is no object type: its add() takes a type first, which C001 checks."""
        source = 'docs = {"base": new_document()}\ndocs["base"].add("Space", "S")\n'
        diagnostics = check_compatibility(_IMP + source, "t.py", [(9, 4, 0), _V262])
        assert [d.code for d in diagnostics] == ["C001"]

    def test_a_misspelled_key_on_a_document_is_still_a_collection(self) -> None:
        source = 'doc = new_document()\ndoc["Zoen"].add("Space", multiplier=1)\n'
        assert check_compatibility(_IMP + source, "t.py", [(9, 4, 0), _V262], select=["C001", "C006"]) == []

    def test_a_bound_collection_keeps_its_narrowing(self) -> None:
        """A collection read from a narrowed document is checked against that document's releases."""
        for source in [
            'doc = new_document()\nheaters = as_version(doc, since="23.2")["WaterHeater:Mixed"]\n'
            'heaters.add("H", heater_fuel_type="DistrictHeatingSteam")\n',
            'doc = new_document()\nif doc.version >= (23, 2, 0):\n    heaters = doc["WaterHeater:Mixed"]\n'
            '    heaters.add("H", heater_fuel_type="DistrictHeatingSteam")\n',
        ]:
            assert check_compatibility(_IMP + source, "t.py", [(9, 4, 0), _V262]) == [], source


def _codes(body: str, targets: list[tuple[int, int, int]] | None = None) -> list[str]:
    """Every default rule's diagnostics, as codes."""
    source = _IMP + "from idfkit import IDFDocument\nfrom typing import Optional\n" + body
    return [d.code for d in check_compatibility(source, "t.py", targets or [(9, 4, 0), _V262])]


class TestDocumentsUnderCollectionLikeNames:
    """A document held where a collection could be keeps the checks main gave its add() calls."""

    def test_an_attribute_named_like_a_singleton_accessor(self) -> None:
        source = """\
class Model:
    def __init__(self, path):
        self.building = load_idf(path)

    def spaces(self):
        self.building.add("Space", "S1", zone_name="Z")
"""
        assert _codes(source) == ["C001"]

    def test_an_attribute_named_like_a_raw_type_name(self) -> None:
        assert _codes('def f(app):\n    app.window.add("Space", "S1")\n') == ["C001"]

    def test_a_dict_of_documents(self) -> None:
        source = 'variants = {"Window": new_document()}\nvariants["Window"].add("Space", "S1")\n'
        assert _codes(source) == ["C001"]

    def test_a_parameter_annotated_as_a_mapping(self) -> None:
        source = 'def f(variants: "dict[str, IDFDocument]"):\n    variants["Window"].add("Space", "S1")\n'
        assert _codes(source) == ["C001"]

    def test_a_suppression_on_such_a_line_is_still_used(self) -> None:
        source = 'def f(app):\n    app.building.add("Space", "S1")  # idfkit: ignore[C001]\n'
        assert _codes(source) == []

    def test_collections_are_still_recognised(self) -> None:
        assert _codes('def f(doc):\n    doc.zones.add("Space", multiplier=1)\n') == []
        assert _codes('def f(doc):\n    doc["Zone"].add("Space", multiplier=1)\n') == []
        # On a known document, a raw accessor spelling and a singleton accessor are collections.
        assert _codes('doc = new_document()\ndoc.zone.add("Space")\ndoc.building.add("Space")\n') == []


class TestNarrowingFromAnEnclosingScope:
    def test_a_module_collection_read_through_as_version(self) -> None:
        source = """\
doc = load_idf("m.idf")
heaters = as_version(doc, since="23.2")["WaterHeater:Mixed"]

def f():
    heaters.add("H", heater_fuel_type="DistrictHeatingSteam")
"""
        assert _codes(source) == []

    def test_a_module_collection_under_a_version_guard(self) -> None:
        source = """\
doc = load_idf("m.idf")
heaters = doc["WaterHeater:Mixed"]

def f():
    if doc.version >= (23, 2, 0):
        heaters.add("H", heater_fuel_type="DistrictHeatingSteam")
"""
        assert _codes(source) == []

    def test_a_rebound_document_does_not_narrow(self) -> None:
        source = """\
doc = load_idf("m.idf")
heaters = as_version(doc, since="23.2")["WaterHeater:Mixed"]

def f(doc):
    heaters.add("H", heater_fuel_type="DistrictHeatingSteam")
"""
        # heaters is still the module's collection, narrowed where it was read.
        assert _codes(source) == []


class TestMoreReceivers:
    def test_get_collection_with_a_keyword_type(self) -> None:
        source = 'doc = new_document()\ndoc.get_collection(obj_type="Zone").add("A", zone_inside_convection_algorithm="Bogus")\n'
        assert len(_check(source)) == 1

    def test_a_union_of_document_and_collection_is_unknown(self) -> None:
        source = 'def f(x: "IDFDocument | IDFCollection[Zone]"):\n    x.add("Office", multiplier=1)\n'
        assert _check(source) == []

    def test_optional_documents(self) -> None:
        for annotation in ['"Optional[IDFDocument]"', '"IDFDocument | None"', "Optional[IDFDocument]"]:
            source = f'from idfkit import IDFDocument\nfrom typing import Optional\ndef f(doc: {annotation}):\n    doc.add("Zoen", "x")\n'
            assert len(_check(source)) == 1, annotation

    def test_a_schema_less_document_accepts_any_type(self) -> None:
        assert _check('from idfkit import IDFDocument\ndoc = IDFDocument()\ndoc.add("Zoen", "x")\n') == []


class TestArityAndValidation:
    def test_a_type_alone_on_a_known_document(self) -> None:
        (found,) = _check('doc = new_document()\ndoc.add("SimulationControls")\n')
        assert "did you mean 'SimulationControl'?" in found

    def test_a_type_alone_on_an_unknown_receiver_is_not_read(self) -> None:
        assert _check('def f(doc):\n    doc.add("SimulationControls")\n') == []

    def test_validate_false_stores_a_value_outside_the_choices(self) -> None:
        source = (
            'doc = new_document()\ndoc.add("Zone", "A", zone_inside_convection_algorithm="Bogus", validate=False)\n'
        )
        assert _check(source) == []

    def test_validate_false_still_raises_on_an_unknown_type(self) -> None:
        assert len(_check('doc = new_document()\ndoc.add("Zoen", "A", validate=False)\n')) == 1
