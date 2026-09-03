"""Type-name-keyed lookup on IDFDocument: case folding, unknown names, no mutation on read.

EnergyPlus matches object type names case-insensitively, so ``d["zone"]``,
``d["ZONE"]`` and ``d["Zone"]`` must be one collection.  Before this suite
existed, only ``d["Zone"]`` found anything: ``__getitem__`` was a plain dict
lookup that, on a miss, created an empty collection and *stored* it, so a
mis-cased read returned empty and left a junk key behind.  ``@idfkit/core``
folded case from the start, which made the same call return six zones there and
none here.

The companion TypeScript suite is ``packages/core/tests/document.test.ts``,
under "type-name lookup".  The two must stay in step.
"""

from __future__ import annotations

import pytest

from idfkit import IDFDocument, new_document
from idfkit.objects import IDFCollection, IDFObject


@pytest.fixture
def doc() -> IDFDocument:
    """A schema-backed document with two zones and one material."""
    model = new_document()
    model.add("Zone", "Perimeter_ZN_1")
    model.add("Zone", "Core_ZN")
    model.add(
        "Material",
        "Concrete_200mm",
        roughness="MediumRough",
        thickness=0.2,
        conductivity=1.4,
        density=2240.0,
        specific_heat=900.0,
    )
    return model


@pytest.fixture
def schemaless() -> IDFDocument:
    """A document with no schema at all, which is a supported construction."""
    return IDFDocument()


class TestCanonicalName:
    def test_canonical_name_returns_the_objects(self, doc: IDFDocument) -> None:
        assert [obj.name for obj in doc["Zone"]] == ["Perimeter_ZN_1", "Core_ZN"]

    def test_canonical_name_returns_the_stored_collection(self, doc: IDFDocument) -> None:
        assert doc["Zone"] is doc.collections["Zone"]

    def test_contains_and_get_collection_agree(self, doc: IDFDocument) -> None:
        assert "Zone" in doc
        assert len(doc.get_collection("Zone")) == 2


class TestMiscasedName:
    @pytest.mark.parametrize("written", ["zone", "ZONE", "ZoNe", "zOnE"])
    def test_every_casing_finds_the_same_objects(self, doc: IDFDocument, written: str) -> None:
        assert [obj.name for obj in doc[written]] == ["Perimeter_ZN_1", "Core_ZN"]

    @pytest.mark.parametrize("written", ["zone", "ZONE", "ZoNe"])
    def test_every_casing_returns_the_one_stored_collection(self, doc: IDFDocument, written: str) -> None:
        assert doc[written] is doc["Zone"]

    def test_internal_capitals_are_recovered_from_the_schema(self) -> None:
        # "scheduletypelimits" carries no casing information at all, so a
        # transformation rule cannot recover "ScheduleTypeLimits". Only a
        # schema lookup can.
        model = new_document()
        model.add("ScheduleTypeLimits", "Any Number")
        assert len(model["scheduletypelimits"]) == 1
        assert len(model["SCHEDULETYPELIMITS"]) == 1

    def test_a_colon_in_the_name_is_not_a_word_boundary(self) -> None:
        model = new_document()
        model.add(
            "Output:Variable", "", key_value="*", variable_name="Zone Air Temperature", reporting_frequency="Hourly"
        )
        assert len(model["output:variable"]) == 1
        assert len(model["OuTpUt:VaRiAbLe"]) == 1

    def test_contains_folds_case_too(self, doc: IDFDocument) -> None:
        assert "zone" in doc
        assert "ZONE" in doc

    def test_getobject_folds_case(self, doc: IDFDocument) -> None:
        found = doc.getobject("zone", "Core_ZN")
        assert found is not None
        assert found.name == "Core_ZN"

    def test_idfobjects_view_agrees(self, doc: IDFDocument) -> None:
        assert doc.idfobjects["ZONE"] is doc["Zone"]

    def test_removeidfobject_finds_a_miscased_collection(self, doc: IDFDocument) -> None:
        zone = doc["Zone"]["Core_ZN"]
        # The object's own type string is mis-cased relative to the key it is
        # filed under, which is reachable through IDFObject construction.
        object.__setattr__(zone, "_type", "ZONE")
        doc.removeidfobject(zone)
        assert len(doc["Zone"]) == 1


class TestUnknownName:
    def test_unknown_name_is_empty_rather_than_raising(self, doc: IDFDocument) -> None:
        assert len(doc["Zoen"]) == 0

    def test_unknown_name_is_not_contained(self, doc: IDFDocument) -> None:
        assert "Zoen" not in doc

    def test_unknown_name_keeps_the_written_spelling_on_the_collection(self, doc: IDFDocument) -> None:
        # Nothing resolves it, so the collection reports the name asked for.
        assert doc["Zoen"].obj_type == "Zoen"

    def test_the_write_path_still_rejects_the_typo(self, doc: IDFDocument) -> None:
        from idfkit.exceptions import UnknownObjectTypeError

        with pytest.raises(UnknownObjectTypeError):
            doc.add("Zoen", "X")

    def test_describe_still_rejects_the_typo(self, doc: IDFDocument) -> None:
        from idfkit.exceptions import UnknownObjectTypeError

        with pytest.raises(UnknownObjectTypeError):
            doc.describe("Zoen")

    def test_the_schema_answers_the_question_directly(self, doc: IDFDocument) -> None:
        assert doc.schema is not None
        assert doc.schema.resolve_type_name("Zoen") is None
        assert doc.schema.resolve_type_name("zone") == "Zone"


class TestSchemalessDocument:
    def test_a_present_type_is_found_case_insensitively(self, schemaless: IDFDocument) -> None:
        obj = IDFObject(obj_type="Zone", name="Z1", data={})
        schemaless.addidfobject(obj)
        assert len(schemaless["Zone"]) == 1
        assert len(schemaless["zone"]) == 1
        assert len(schemaless["ZONE"]) == 1
        assert "zone" in schemaless

    def test_an_absent_type_is_empty_and_never_raises(self, schemaless: IDFDocument) -> None:
        assert len(schemaless["Zone"]) == 0
        assert len(schemaless["Zoen"]) == 0
        assert "Zoen" not in schemaless

    def test_reading_leaves_the_document_untouched(self, schemaless: IDFDocument) -> None:
        _ = schemaless["Zone"], schemaless["zone"], schemaless["Zoen"]
        assert schemaless.collections == {}


class TestNoMutationOnRead:
    def test_reading_an_absent_type_adds_no_collection(self, doc: IDFDocument) -> None:
        before = list(doc.collections)
        for name in ("Lights", "People", "Zoen", "NotAThing", "zone", "ZONE"):
            _ = doc[name]
        assert list(doc.collections) == before

    def test_membership_tests_add_no_collection(self, doc: IDFDocument) -> None:
        before = list(doc.collections)
        for name in ("Lights", "Zoen", "zone"):
            _ = name in doc
        assert list(doc.collections) == before

    def test_the_collection_returned_for_an_absent_type_is_detached(self, doc: IDFDocument) -> None:
        orphan = doc["Lights"]
        orphan.add(IDFObject(obj_type="Lights", name="L1", data={}))
        assert len(doc["Lights"]) == 0
        assert "Lights" not in doc.collections

    def test_each_read_of_an_absent_type_is_a_fresh_collection(self, doc: IDFDocument) -> None:
        assert doc["Lights"] is not doc["Lights"]

    def test_keys_and_items_stay_clean_after_probing(self, doc: IDFDocument) -> None:
        for name in ("Zoen", "NotAThing", "Lights"):
            _ = doc[name]
        assert "Zoen" not in doc.keys()  # noqa: SIM118  # doc.keys() is a method, not a mapping view
        assert "Zoen" not in [t for t, _ in doc.items()]
        assert "Zoen" not in list(doc)


class TestWritePathStillCreatesCollections:
    def test_add_creates_the_collection(self) -> None:
        model = new_document()
        assert "Zone" not in model.collections
        model.add("Zone", "Z1")
        assert isinstance(model.collections["Zone"], IDFCollection)

    def test_add_with_a_miscased_type_files_under_the_canonical_key(self) -> None:
        model = new_document()
        model.add("zONE", "Z1")
        assert "Zone" in model.collections
        assert "zONE" not in model.collections

    def test_addidfobject_with_a_miscased_type_files_under_the_canonical_key(self) -> None:
        model = new_document()
        model.addidfobject(IDFObject(obj_type="ZONE", name="Z1", data={}))
        assert "Zone" in model.collections
        assert "ZONE" not in model.collections
        assert len(model["Zone"]) == 1
