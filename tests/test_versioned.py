"""Tests for the per-version document types: the run-time stand-ins and the generated stubs.

What a type checker reports for these types is checked by ``tests/type_checks/versioned_fixture.py``
under ``make check``. Here: the run-time half (``isinstance``, ``as_version``), and the generator's
promise that the stubs describe every supported version exactly, today and after each adoption.
"""

from __future__ import annotations

import re
import typing
from pathlib import Path
from typing import Annotated, Any, Literal, get_args, get_origin, get_type_hints

import pytest

import idfkit.versioned as versioned
from idfkit import load_idf, new_document, write_idf
from idfkit._document_types import release_of
from idfkit.codegen import generate_stubs as gen
from idfkit.codegen.verify_stubs import verify
from idfkit.document import AnyIDFDocument, IDFDocument
from idfkit.exceptions import UnsupportedVersionError
from idfkit.versions import ENERGYPLUS_VERSIONS, LATEST_VERSION, version_string

_PACKAGE = Path(versioned.__file__).resolve().parent


_Sources = tuple[str, str, str, str, dict[str, str]]


def _committed() -> _Sources:
    """The committed stubs: types, document, versioned, the per-release document modules joined, and
    the creation signature modules by name."""
    documents = sorted((_PACKAGE / "_versioned").glob("v*.pyi"))
    return (
        (_PACKAGE / "_generated_types.pyi").read_text(encoding="utf-8"),
        (_PACKAGE / "document.pyi").read_text(encoding="utf-8"),
        (_PACKAGE / "versioned.pyi").read_text(encoding="utf-8"),
        "\n".join(path.read_text(encoding="utf-8") for path in documents),
        {path.stem: path.read_text(encoding="utf-8") for path in sorted((_PACKAGE / "_creation").glob("_*.pyi"))},
    )


def _generated() -> _Sources:
    """What the generator writes now, in the shape of :func:`_committed`."""
    documents = gen.generate_versioned_documents()
    creation = gen._CreationModules()  # pyright: ignore[reportPrivateUsage]
    versioned_creation = gen._CreationModules("_v", "_cv")  # pyright: ignore[reportPrivateUsage]
    types = gen.generate_stubs(sink=creation)
    versioned_source = gen.generate_versioned_pyi(versioned_creation)
    modules = {**creation.sources(), **versioned_creation.sources()}
    return (
        types,
        gen.generate_document_pyi(),
        versioned_source,
        "\n".join(source for name, source in sorted(documents.items()) if name != "__init__.pyi"),
        {name.removesuffix(".pyi"): source for name, source in modules.items()},
    )


def _verify(sources: _Sources | list[Any], versions: tuple[tuple[int, int, int], ...]) -> list[str]:
    return verify(sources[0], sources[1], [sources[2], sources[3]], versions, sources[4])


# ---------------------------------------------------------------------------
# Run time
# ---------------------------------------------------------------------------


class TestRuntimeTypes:
    def test_every_supported_version_has_a_document_type(self) -> None:
        for ver in ENERGYPLUS_VERSIONS:
            name = f"IDFDocumentV{ver[0]}_{ver[1]}"
            assert name in versioned.__all__
            assert hasattr(versioned, name)

    def test_the_latest_version_is_idfdocument(self) -> None:
        latest = getattr(versioned, f"IDFDocumentV{LATEST_VERSION[0]}_{LATEST_VERSION[1]}")
        assert latest is IDFDocument

    def test_isinstance_compares_versions(self) -> None:
        legacy = new_document(version=(9, 4, 0))
        current = new_document()
        assert isinstance(legacy, versioned.IDFDocumentV9_4)
        assert not isinstance(current, versioned.IDFDocumentV9_4)
        assert not isinstance(legacy, versioned.IDFDocumentV9_5)
        assert not isinstance("a document", versioned.IDFDocumentV9_4)

    def test_any_document_holds_every_document(self) -> None:
        assert isinstance(new_document(version=(9, 4, 0)), AnyIDFDocument)
        assert isinstance(new_document(), AnyIDFDocument)
        assert versioned.AnyIDFDocument is AnyIDFDocument

    def test_a_two_component_version_line_matches_its_release(self, tmp_path: Path) -> None:
        # A file states 9.0.1 as "9.0", which reads as 9.0.0, the way the schema is chosen.
        path = tmp_path / "legacy.idf"
        path.write_text("Version,9.0;\nZone,Office;\n", encoding="latin-1")
        doc = load_idf(str(path))
        assert doc.version == (9, 0, 0)
        assert isinstance(doc, versioned.IDFDocumentV9_0)
        assert not isinstance(doc, versioned.IDFDocumentV9_1)
        assert versioned.as_version(doc, versioned.IDFDocumentV9_0) is doc
        copied = new_document(version=(9, 0, 1)).copy()
        assert versioned.as_version(copied, versioned.IDFDocumentV9_0) is copied

    def test_document_types_take_type_arguments(self) -> None:
        # The stubs declare them generic, so an annotation evaluated at run time must not raise.
        assert get_origin(versioned.IDFDocumentV9_4[bool]) is versioned.IDFDocumentV9_4
        assert get_origin(AnyIDFDocument[bool]) is AnyIDFDocument

    def test_document_types_are_not_instantiated(self) -> None:
        with pytest.raises(TypeError, match=r"new_document\(IDFDocumentV9_4\)"):
            versioned.IDFDocumentV9_4()
        # AnyIDFDocument stands for no release, so the advice is the tuple form, which works.
        with pytest.raises(TypeError, match=r"new_document\(version=\.\.\.\)"):
            AnyIDFDocument()


class TestNewDocument:
    @pytest.mark.parametrize("version", ENERGYPLUS_VERSIONS[:-1], ids=version_string)
    def test_creates_a_document_of_the_types_release(self, version: tuple[int, int, int]) -> None:
        document_type: Any = getattr(versioned, f"IDFDocumentV{version[0]}_{version[1]}")
        doc = new_document(document_type)
        assert type(doc) is IDFDocument
        assert doc.version == version
        assert versioned.as_version(doc, document_type) is doc

    def test_creates_what_a_version_tuple_creates(self) -> None:
        assert write_idf(new_document(versioned.IDFDocumentV9_4)) == write_idf(new_document(version=(9, 4, 0)))

    def test_a_type_argument_states_the_strictness(self) -> None:
        assert new_document(versioned.IDFDocumentV9_4).strict is True
        assert new_document(versioned.IDFDocumentV9_4[Literal[False]]).strict is False
        assert new_document(versioned.IDFDocumentV9_4[Literal[True]]).strict is True
        assert new_document(versioned.IDFDocumentV9_4[Annotated[Literal[False], "lax"]]).strict is False
        # No single literal bool states none, as for a bare type.
        for argument in (bool, Any, Literal[True, False], Literal[1]):
            assert new_document(versioned.IDFDocumentV9_4[argument]).strict is True

    @pytest.mark.skipif(not hasattr(typing, "TypeAliasType"), reason="typing.TypeAliasType is new in 3.12")
    def test_a_type_alias_argument_states_the_strictness(self) -> None:
        # pyright reads IDFDocumentV9_4[Lax] as IDFDocumentV9_4[Literal[False]], so the document must be lax.
        alias_type: Any = vars(typing)["TypeAliasType"]
        lax: Any = alias_type("Lax", Literal[False])
        assert new_document(versioned.IDFDocumentV9_4[lax]).strict is False
        assert new_document(versioned.IDFDocumentV9_4[Annotated[lax, "lax"]]).strict is False

    def test_strict_from_an_untyped_caller(self) -> None:
        # The type overload takes no strict; at run time it applies, unless the type contradicts it.
        untyped: Any = new_document
        assert untyped(versioned.IDFDocumentV9_4, strict=False).strict is False
        with pytest.raises(TypeError, match="contradicts"):
            untyped(versioned.IDFDocumentV9_4[Literal[True]], strict=False)

    def test_refuses_a_string_type_argument(self) -> None:
        with pytest.raises(TypeError, match="unquoted"):
            new_document(versioned.IDFDocumentV9_4["Literal[False]"])  # pyright: ignore[reportInvalidTypeArguments]

    def test_refuses_idfdocument_so_type_of_a_document_fails_loudly(self) -> None:
        # Every document's run-time class is IDFDocument, whatever its release: new_document(type(doc))
        # must not create a latest-release document typed as doc's release.
        legacy = new_document(versioned.IDFDocumentV9_4)
        latest_name = f"IDFDocumentV{LATEST_VERSION[0]}_{LATEST_VERSION[1]}"
        latest_type = getattr(versioned, latest_name)
        for document_type in (type(legacy), IDFDocument, IDFDocument[Literal[False]], latest_type):
            with pytest.raises(TypeError, match=r"Call new_document\(\) for the latest release"):
                new_document(document_type)
        # A caller who passed the latest release's own type is told that it is IDFDocument.
        with pytest.raises(TypeError, match=f"{latest_name}, which is IDFDocument"):
            new_document(latest_type)

    def test_refuses_what_names_no_single_release(self) -> None:
        with pytest.raises(TypeError, match="names 2"):
            new_document(versioned.IDFDocumentV9_4 | versioned.IDFDocumentV9_6)
        for no_release in (AnyIDFDocument, AnyIDFDocument[Literal[False]]):
            with pytest.raises(TypeError, match="no single EnergyPlus release"):
                new_document(no_release)  # pyright: ignore[reportArgumentType, reportCallIssue]

    def test_refuses_a_class_that_is_not_a_release_type(self) -> None:
        class Lax(versioned.IDFDocumentV9_4[Literal[False]]): ...

        with pytest.raises(TypeError, match="subclass of a release type"):
            new_document(Lax)
        # Instantiating the subclass points to the release's type, which new_document takes, not to Lax.
        with pytest.raises(TypeError, match=r"new_document\(IDFDocumentV9_4\)"):
            Lax()
        with pytest.raises(TypeError, match="not a document type"):
            new_document(dict)  # pyright: ignore[reportArgumentType, reportCallIssue]
        with pytest.raises(TypeError, match="not a document type"):
            new_document(list[Literal[False]])  # pyright: ignore[reportArgumentType, reportCallIssue]

    def test_a_version_that_is_not_a_tuple_is_still_an_unsupported_version(self) -> None:
        with pytest.raises(UnsupportedVersionError):
            new_document("24.1.0")  # pyright: ignore[reportArgumentType, reportCallIssue]

    def test_annotations_resolve_at_run_time(self) -> None:
        hints = get_type_hints(new_document)
        assert hints["strict"] is bool


class TestAsVersion:
    def test_returns_the_same_document(self) -> None:
        doc = new_document(version=(9, 4, 0))
        assert versioned.as_version(doc, versioned.IDFDocumentV9_4) is doc

    def test_refuses_another_version(self) -> None:
        doc = new_document(version=(9, 4, 0))
        with pytest.raises(TypeError, match=r"EnergyPlus 9\.4\.0, not 9\.5\.0.*IDFDocumentV9_5"):
            versioned.as_version(doc, versioned.IDFDocumentV9_5)

    def test_idfdocument_means_the_latest_release(self) -> None:
        current = new_document()
        assert versioned.as_version(current, IDFDocument) is current
        with pytest.raises(TypeError, match=rf"not {re.escape(version_string(LATEST_VERSION))}"):
            versioned.as_version(new_document(version=(9, 4, 0)), IDFDocument)

    def test_accepts_a_document_type_with_type_arguments(self) -> None:
        current = new_document()
        assert versioned.as_version(current, IDFDocument[bool]) is current
        legacy = new_document(version=(9, 4, 0))
        assert versioned.as_version(legacy, versioned.IDFDocumentV9_4[bool]) is legacy

    def test_any_document_accepts_every_version(self) -> None:
        doc = new_document(version=(8, 9, 0))
        assert versioned.as_version(doc, AnyIDFDocument) is doc

    def test_refuses_a_type_that_is_not_a_document_type(self) -> None:
        with pytest.raises(TypeError, match="not a document type"):
            versioned.as_version(new_document(), dict)  # pyright: ignore[reportCallIssue]

    def test_accepts_a_document_of_any_release_in_a_tuple(self) -> None:
        since_9_6 = (versioned.IDFDocumentV9_6, versioned.IDFDocumentV26_1, IDFDocument)
        for version in [(9, 6, 0), (26, 1, 0), LATEST_VERSION]:
            doc = new_document(version=version)
            assert versioned.as_version(doc, since_9_6) is doc

    def test_refuses_a_document_outside_the_tuple_and_names_its_releases(self) -> None:
        since_9_6 = (versioned.IDFDocumentV9_6, IDFDocument)
        expected = rf"EnergyPlus 9\.4\.0, not one of 9\.6\.0, {re.escape(version_string(LATEST_VERSION))}"
        with pytest.raises(TypeError, match=expected):
            versioned.as_version(new_document(version=(9, 4, 0)), since_9_6)

    def test_accepts_a_union_as_isinstance_does(self) -> None:
        # pyright accepts the union spelled inline, so it has to work when it runs.
        doc = new_document(version=(9, 6, 0))
        assert versioned.as_version(doc, versioned.IDFDocumentV9_6 | IDFDocument) is doc
        assert versioned.as_version(doc, versioned.IDFDocumentV9_6[bool] | IDFDocument[bool]) is doc  # pyright: ignore[reportArgumentType, reportCallIssue, reportUnknownMemberType]
        with pytest.raises(TypeError, match="not one of"):
            versioned.as_version(new_document(version=(9, 4, 0)), versioned.IDFDocumentV9_6 | IDFDocument)

    def test_refuses_an_empty_tuple(self) -> None:
        with pytest.raises(TypeError, match="at least one"):
            versioned.as_version(new_document(), ())  # pyright: ignore[reportCallIssue, reportArgumentType]


class TestAsVersionRange:
    """``since=`` and ``before=``: a range of the releases idfkit supports, with no list to maintain."""

    def test_since_accepts_every_supported_release_from_it_on(self) -> None:
        for version in ENERGYPLUS_VERSIONS:
            doc = new_document(version=version)
            if version >= (9, 6, 0):
                assert versioned.as_version(doc, since="9.6") is doc
            else:
                with pytest.raises(TypeError, match=r"not 9\.6\.0 or later"):
                    versioned.as_version(doc, since="9.6")

    def test_before_accepts_every_supported_release_before_it(self) -> None:
        for version in ENERGYPLUS_VERSIONS:
            doc = new_document(version=version)
            if version < (9, 6, 0):
                assert versioned.as_version(doc, before="9.6") is doc
            else:
                with pytest.raises(TypeError, match=r"not a release before 9\.6\.0"):
                    versioned.as_version(doc, before="9.6")

    def test_since_and_before_bound_a_range(self) -> None:
        inside = new_document(version=(22, 1, 0))
        assert versioned.as_version(inside, since="9.6", before="22.2") is inside
        expected = r"EnergyPlus 22\.2\.0, not from 9\.6\.0 to before 22\.2\.0 \(9\.6\.0, 22\.1\.0\)"
        with pytest.raises(TypeError, match=expected):
            versioned.as_version(new_document(version=(22, 2, 0)), since="9.6", before="22.2")

    def test_the_latest_release_is_in_a_range_from_any_earlier_release(self) -> None:
        # The failure a hand-listed tuple ending in IDFDocument meets on release adoption cannot
        # happen: the range is computed from ENERGYPLUS_VERSIONS when the call runs.
        current = new_document()
        for version in ENERGYPLUS_VERSIONS:
            assert versioned.as_version(current, since=version_string(version)) is current

    def test_a_bound_can_be_a_document_type(self) -> None:
        doc = new_document(version=(9, 6, 0))
        assert versioned.as_version(doc, since=versioned.IDFDocumentV9_6) is doc
        assert versioned.as_version(doc, since=versioned.IDFDocumentV9_6[bool]) is doc
        assert versioned.as_version(doc, before=versioned.IDFDocumentV22_1) is doc
        current = new_document()
        assert versioned.as_version(current, since=IDFDocument) is current
        with pytest.raises(TypeError, match="not a release before"):
            versioned.as_version(current, before=IDFDocument)

    def test_a_bound_can_be_a_full_version_string(self) -> None:
        doc = new_document(version=(9, 0, 1))
        assert versioned.as_version(doc, since="9.0.1", before="9.1.0") is doc
        assert versioned.as_version(doc, since="9.0.0") is doc  # a file's 9.0 is the 9.0.1 release

    def test_a_bound_can_be_a_version_tuple(self) -> None:
        doc = new_document(version=(9, 6, 0))
        assert versioned.as_version(doc, since=(9, 6, 0)) is doc
        assert versioned.as_version(doc, since=(9, 6), before=(22, 1, 0)) is doc
        assert versioned.as_version(doc, since=doc.version) is doc
        legacy = new_document(version=(9, 0, 1))
        assert versioned.as_version(legacy, since=(9, 0, 0), before=(9, 1, 0)) is legacy  # a file's 9.0 is 9.0.1

    def test_refuses_a_tuple_that_is_not_a_version(self) -> None:
        with pytest.raises(ValueError, match="is not a release"):
            versioned.as_version(new_document(), since=(9,))  # pyright: ignore[reportCallIssue, reportArgumentType]
        with pytest.raises(ValueError, match="is not a release"):
            versioned.as_version(new_document(), since=(9, "6"))  # pyright: ignore[reportCallIssue, reportArgumentType]

    def test_a_bound_that_is_not_a_release_names_the_forms_accepted(self) -> None:
        with pytest.raises(TypeError, match=r"since=1\.5 is not a release: give .*version tuple"):
            versioned.as_version(new_document(), since=1.5)  # pyright: ignore[reportCallIssue, reportArgumentType]

    def test_a_version_newer_than_every_release_is_no_bound(self) -> None:
        # A file of 27.1 is read as the latest release; as a bound it names nothing.
        with pytest.raises(ValueError, match="supports no such EnergyPlus release"):
            versioned.as_version(new_document(), since=(27, 1, 0))

    def test_refuses_a_release_idfkit_does_not_support(self) -> None:
        with pytest.raises(ValueError, match="supports no such EnergyPlus release"):
            versioned.as_version(new_document(), since="27.1")
        with pytest.raises(ValueError, match="is not a release"):
            versioned.as_version(new_document(), since="latest")

    def test_refuses_an_empty_range(self) -> None:
        with pytest.raises(ValueError, match=r"No supported EnergyPlus release is from 26\.1\.0 to before 9\.4\.0"):
            versioned.as_version(new_document(), since="26.1", before="9.4")

    def test_refuses_any_document_as_a_bound(self) -> None:
        with pytest.raises(TypeError, match="names none"):
            any_release: Any = AnyIDFDocument  # names no release: a type error, so passed untyped
            versioned.as_version(new_document(), since=any_release)

    def test_refuses_a_document_type_and_a_range_together(self) -> None:
        with pytest.raises(TypeError, match="not both"):
            both: Any = {"since": "9.6"}  # both a type and a range: a type error, so passed untyped
            versioned.as_version(new_document(), IDFDocument, **both)

    def test_refuses_neither(self) -> None:
        with pytest.raises(TypeError, match="needs a document type"):
            versioned.as_version(new_document())  # pyright: ignore[reportCallIssue]


class TestRangeAliases:
    def test_every_release_has_a_since_alias_and_every_later_one_a_before_alias(self) -> None:
        types = [getattr(versioned, f"IDFDocumentV{v[0]}_{v[1]}") for v in ENERGYPLUS_VERSIONS]
        for i, version in enumerate(ENERGYPLUS_VERSIONS):
            tag = f"{version[0]}_{version[1]}"
            since = getattr(versioned, f"IDFDocumentSince{tag}")
            # The latest release is a stand-in, not IDFDocument, which every document is an instance of.
            assert [release_of(t) for t in get_args(since) or (since,)] == list(ENERGYPLUS_VERSIONS[i:])
            assert f"IDFDocumentSince{tag}" in versioned.__all__
            if i:
                before = getattr(versioned, f"IDFDocumentBefore{tag}")
                assert (get_args(before) or (before,)) == tuple(types[:i])
                assert f"IDFDocumentBefore{tag}" in versioned.__all__

    def test_isinstance_checks_the_release(self) -> None:
        old, latest = new_document(version=(9, 1, 0)), new_document()
        assert not isinstance(old, versioned.IDFDocumentSince9_4)
        assert isinstance(latest, versioned.IDFDocumentSince9_4)
        assert isinstance(old, versioned.IDFDocumentBefore9_4)
        assert not isinstance(latest, versioned.IDFDocumentBefore9_4)

    def test_an_alias_accepts_its_releases_at_run_time(self) -> None:
        doc = new_document(version=(23, 2, 0))
        alias: Any = versioned.IDFDocumentSince23_2  # to a type checker an alias is no class; it runs
        assert versioned.as_version(doc, alias) is doc


# ---------------------------------------------------------------------------
# Generated stubs
# ---------------------------------------------------------------------------


class TestCommittedStubs:
    def test_describe_every_supported_version_exactly(self) -> None:
        assert _verify(_committed(), ENERGYPLUS_VERSIONS) == []

    def test_a_reordered_group_is_not_a_new_class(self) -> None:
        # 8.9 lists BuildingSurface:Detailed's vertex fields in another order than 9.3; nothing a
        # type checker sees differs, so the releases share one class rather than two.
        versioned_source = _committed()[2]
        assert re.search(r"(?m)^class BuildingSurfaceDetailed_v8_9_to_v9_5\(", versioned_source)
        assert not re.search(r"(?m)^class BuildingSurfaceDetailed_v8_9_to_v9_2\(", versioned_source)

    def test_any_class_docstrings_name_the_releases_they_cover(self) -> None:
        types_source = _committed()[0]
        assert '"""``Zone`` as every supported EnergyPlus version declares it."""' in types_source
        # Space arrived in 9.6: AnySpace covers every Space there is, from 9.6 on, and says so.
        expected = '"""``Space`` as every supported EnergyPlus version that has it declares it: 9.6.0 and later."""'
        assert expected in types_source

    def test_no_document_type_is_a_typed_dict(self) -> None:
        # pyright narrows a TypedDict on `"Space" in doc` by its own rules: a positive test retyped an
        # AnyIDFDocument as the latest release, a negative one on a type every release has made its
        # branch unreachable, and it offered get(), setdefault() and pop(), which a document does not
        # have. So documents index through __getitem__ overloads, and no object-type map is generated.
        for source in _committed()[:4]:
            assert "_ObjectTypeMap" not in source
            assert "_CommonTypeMap" not in source
            assert "closed=True" not in source
            assert "extra_items=" not in source
            for header in re.findall(r"(?ms)^class (?:IDFDocument\w*)\((.*?)\):", source):
                assert "TypedDict" not in header
                assert "TypeMap" not in header

    def test_every_older_release_is_re_exported_from_its_own_module(self) -> None:
        versioned_source = _committed()[2]
        modules = {path.name for path in (_PACKAGE / "_versioned").glob("*.pyi")}
        assert "__init__.pyi" in modules
        for ver in ENERGYPLUS_VERSIONS[:-1]:
            tag = f"{ver[0]}_{ver[1]}"
            assert f"v{tag}.pyi" in modules
            assert f"from ._versioned.v{tag} import IDFDocumentV{tag} as IDFDocumentV{tag}" in versioned_source
            assert f"class IDFDocumentV{tag}(" not in versioned_source
        assert len(modules) == len(ENERGYPLUS_VERSIONS)  # one per older release, and __init__.pyi

    @pytest.mark.parametrize(
        ("source", "pattern", "replacement", "expected"),
        [
            # A 9.4 field dropped from the class of its range.
            (2, r"(?m)^    rated_evaporator_fan_power_per_volume_flow_rate: float \| None\n", "", "missing"),
            # A type filed under the wrong class for a range of versions.
            (3, r"IDFCollection\[_v\.Space_v9_6_to_v22_1\]", "IDFCollection[_v.Space_v22_2_to_v26_1]", "Space"),
            # A type overloaded on no release's document: indexing with it would match nothing.
            (
                3,
                r'(?m)^    @overload\n    def __getitem__\(self, obj_type: Literal\["Space"\].*\n',
                "",
                "missing types ['Space']",
            ),
            # A release's last overload taking a name, which every name the release lacks would match.
            (
                3,
                r"obj_type: _NotAnObjectTypeOfEnergyPlus9_4, /\)",
                "obj_type: str, /)",
                "IDFDocumentV9_4: __getitem__ does not end with the one overload that matches no object type",
            ),
            # A release's last overload taking the class itself rather than a Sequence of it: mypy would
            # then list every overload under a misspelled name instead of reporting this one alone.
            (
                3,
                r"(?m)^_NotAnObjectTypeOfEnergyPlus9_4: TypeAlias = Sequence\[(\w+)\]",
                r"_NotAnObjectTypeOfEnergyPlus9_4: TypeAlias = \1",
                "IDFDocumentV9_4: __getitem__ does not end with the one overload that matches no object type",
            ),
            # A release's document that no longer derives from IDFDocumentAllVersions.
            (
                3,
                r"(?m)^    IDFDocumentAllVersions\[Strict\],\n\):\n(    \"\"\"An :class:`~idfkit.document.IDFDocument` typed for EnergyPlus 9\.4)",
                r"):\n\1",
                "IDFDocumentV9_4: does not derive from IDFDocumentAllVersions",
            ),
            # An accessor typed with the wrong class.
            (
                2,
                r"def spaces\(self\) -> IDFCollection\[Space_v9_6_to_v22_1\]",
                "def spaces(self) -> IDFCollection[_g.Zone]",
                "accessors",
            ),
            # A type some version lacks, added to AnyIDFDocument: indexing a document of any release
            # with it would type-check.
            (
                1,
                r'(?m)^    def __getitem__\(self, obj_type: Literal\["Zone"\], /\) -> IDFCollection\[AnyZone\]: \.\.\.\n',
                r'\g<0>    @overload\n    def __getitem__(self, obj_type: Literal["Space"], /) -> IDFCollection[Space]: ...\n',
                "extra ['Space']",
            ),
            # A group every version has, dropped from the any-release class.
            (
                0,
                r"(?m)^    vertices: ExtensibleList\[BuildingSurfaceDetailedVerticesGroup\]\n",
                "",
                "AnyBuildingSurfaceDetailed: no vertices group",
            ),
            # A merged group's field made writable with a value some version rejects (a float from 22.2 on).
            (
                0,
                r"def digits_after_decimal\(self, value: int \| None\)",
                "def digits_after_decimal(self, value: float | None)",
                "digits_after_decimal: writable values some version rejects",
            ),
            # An object type without its public any-release name.
            (0, r"(?m)^AnyZoneList: TypeAlias = ZoneList\n", "", "no AnyZoneList"),
            # A value only some versions accept, made writable through the shared base.
            (
                0,
                r'(?ms)(@heater_fuel_type\.setter.*?value: Literal\[\n\s+)"Coal",',
                r'\1"Coal",\n            "Steam",',
                "heater_fuel_type: writable values some version rejects",
            ),
            # A type every version has, dropped from AnyIDFDocument.
            (
                1,
                r'(?m)^    @overload\n    def __getitem__\(self, obj_type: Literal\["Zone"\], /\) -> IDFCollection\[AnyZone\]: \.\.\.\n',
                "",
                "AnyIDFDocument",
            ),
            # AnyIDFDocument typing a collection with a class that is not defined: reported, not a KeyError.
            (
                1,
                r'Literal\["Zone"\], /\) -> IDFCollection\[AnyZone\]',
                'Literal["Zone"], /) -> IDFCollection[AnyZoneX]',
                "class AnyZoneX not defined",
            ),
            # A group's item type that misnames one of the group's fields.
            (
                0,
                r"(class BuildingSurfaceDetailedVerticesItem\(TypedDict, total=False\):\n(?:.*\n)*?    )vertex_x_coordinate",
                r"\1vertex_x_coordinat",
                "BuildingSurfaceDetailedVerticesItem does not hold the version's inner fields",
            ),
            # A writable field that some version lacks (People before 9.6): reported, not a KeyError.
            (
                0,
                r'(?m)^(class AnyPeople\(_TypedIDFObject\):\n    """[^\n]*"""\n)',
                r"\1    @property\n"
                r"    def zone_or_zonelist_or_space_or_spacelist_name(self) -> str | None: ...\n"
                r"    @zone_or_zonelist_or_space_or_spacelist_name.setter\n"
                r"    def zone_or_zonelist_or_space_or_spacelist_name(self, value: str | None) -> None: ...\n",
                "zone_or_zonelist_or_space_or_spacelist_name: writable, but not a field of every version",
            ),
            # A field every release requires, read as optional: the type would promise less than the run time.
            (
                0,
                r"(class AnyMaterial\(_TypedIDFObject\):\n(?:.*\n)*?    thickness: )float\n",
                r"\1float | None\n",
                "mistyped ['thickness']",
            ),
            # A field no release requires, read as never None: the type would promise more than the run time.
            (
                0,
                r'(class AnyZone\(_TypedIDFObject\):\n(?:.*\n)*?    ceiling_height: float \| Literal\["Autocalculate"\]) \| None\n',
                r"\1\n",
                "mistyped ['ceiling_height']",
            ),
            # The blank "" back among a field's values: a blank is stored as absent and never read.
            (
                0,
                r'(class AnyZone\(_TypedIDFObject\):\n(?:.*\n)*?    ceiling_height: float \| Literal\[)"Autocalculate"\]',
                r'\1"", "Autocalculate"]',
                "mistyped ['ceiling_height']",
            ),
            # A range alias one release short.
            (
                2,
                r"(IDFDocumentBefore9_6: TypeAlias = \(\n(?:    .*\n)*?)    \| IDFDocumentV9_5\n",
                r"\1",
                "IDFDocumentBefore9_6: names",
            ),
            # A since= overload typed with the wrong range.
            (
                2,
                r'(since: type\[IDFDocumentV9_6\] \| Literal\["9\.6", "9\.6\.0"\]\n\) -> )IDFDocumentSince9_6',
                r"\1IDFDocumentSince9_5",
                "as_version(since=(9, 6, 0), before=None): returns",
            ),
            # A bound's literal naming another release than its type.
            (
                2,
                r'(since: type\[IDFDocumentV9_6\] \| Literal\[)"9\.6"',
                r'\1"9.5"',
                "as_version(since=IDFDocumentV9_6): typed",
            ),
            # A range left without an overload.
            (
                2,
                r"@overload\ndef as_version\(\n    doc: AnyIDFDocument, \*, since: type\[IDFDocumentV9_6\] "
                r'\| Literal\["9\.6", "9\.6\.0"\]\n\) -> IDFDocumentSince9_6: \.\.\.\n',
                "",
                "as_version(since=(9, 6, 0), before=None): no overload",
            ),
        ],
    )
    def test_a_misdescription_is_reported(self, source: int, pattern: str, replacement: str, expected: str) -> None:
        sources = list(_committed())
        mutated = re.sub(pattern, replacement, sources[source], count=1)
        assert mutated != sources[source], "the mutation did not apply"
        sources[source] = mutated
        problems = _verify(sources, ENERGYPLUS_VERSIONS)
        assert any(expected in problem for problem in problems), problems

    @pytest.mark.parametrize(
        ("pattern", "replacement", "expected"),
        [
            (
                r"(class Material:.*?)thickness: float,",
                r"\1thickness: float | None = ...,",
                "Material in 26.2.0 (Material): add() does not require thickness",
            ),
            (
                r"(class Material:.*?)thermal_absorptance: float \| None = 0\.9",
                r"\1thermal_absorptance: float | None = 0.8",
                "add() shows thermal_absorptance = 0.8, not the schema's default",
            ),
            (
                r"(class OutputSQLite:\s+def __call__\(\s*self,)",
                r'\1 name: str = "",',
                "the name is optional in add(), none in the schema",
            ),
            (
                r"(class OutputSQLite:.*?)this_type_has_no_name_field: _g\._PassFieldsAsKeywords = \.\.\.,",
                r"\1",
                "Output:SQLite in 26.2.0 (OutputSQLite): add() does not refuse a name with this_type_has_no_name_field",
            ),
            (
                r"(class OutputSQLite:.*?)this_type_has_no_name_field: _g\._PassFieldsAsKeywords",
                r"\1this_type_has_no_name_field: str",
                "(OutputSQLite): add() does not refuse a name with this_type_has_no_name_field",
            ),
            (
                # Option A: AnyIDFDocument requires what any release requires.
                r"(class AnyBuildingSurfaceDetailed:.*?)construction_name: str,",
                r"\1construction_name: str | None = ...,",
                "(AnyBuildingSurfaceDetailed): add() does not require construction_name",
            ),
            (
                r"(class AnyPeople:.*?)narrow_with_as_version_first: Never,",
                r"\1",
                "(AnyPeople): add() can satisfy no release's required fields or name but does not say so",
            ),
            (
                r"(class WindowMaterialGap:.*?)\) -> None",
                r"\1gas_or_gas_mixture: str | None = ...) -> None",
                "WindowMaterial:Gap in 26.2.0 (WindowMaterialGap): add() keywords differ",
            ),
            (
                r"(class InternalMass_v9_2_to_v9_5:.*?)zone_or_zonelist_name: str,",
                r"\1zone_or_zonelist_name: str | None = ...,",
                "add() does not require zone_or_zonelist_name",
            ),
            # The docstring an editor shows for add(): the type's own, and the way out when there is one.
            (
                r"(class Material:.*?)Create a new ``Material``",
                r"\1Create a new ``Zone``",
                "Material in 26.2.0 (Material): add() is not documented as creating a Material",
            ),
            (
                r'(class Zone:.*?\) -> None:)\n\s+""".*?"""',
                r"\1 ...",
                "Zone in 26.2.0 (Zone): add() is not documented as creating a Zone",
            ),
            (
                r"(class AnyPeople:.*?)No call suits every release: narrow the document with ``as_version`` first\.",
                r"\1",
                "(AnyPeople): add()'s docstring and narrow_with_as_version_first disagree on narrowing first",
            ),
        ],
    )
    def test_a_misdescribed_creation_signature_is_reported(self, pattern: str, replacement: str, expected: str) -> None:
        sources = list(_committed())
        creation = dict(sources[4])
        name = next(name for name, source in creation.items() if re.search(pattern, source, flags=re.S))
        creation[name] = re.sub(pattern, replacement, creation[name], count=1, flags=re.S)
        sources[4] = creation
        problems = _verify(sources, ENERGYPLUS_VERSIONS)
        assert any(expected in problem for problem in problems), problems

    def test_a_fault_in_the_generators_type_mapping_is_reported(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # The check derives each field's values from the schema itself, so a generator that maps a
        # schema type wrongly is caught rather than repeated: here every integer becomes a float.
        real = gen._schema_type_to_python  # pyright: ignore[reportPrivateUsage]

        def faulty(field_schema: dict[str, Any] | None, field_type: str | None, has_any_of: bool = False) -> str:
            return "float" if field_type == "integer" else real(field_schema, field_type, has_any_of)

        # The fault stays in place while the check runs: a check that borrowed the generator's
        # mapping would then expect the same wrong types and report nothing.
        monkeypatch.setattr(gen, "_schema_type_to_python", faulty)
        gen._clear_version_caches()  # pyright: ignore[reportPrivateUsage]
        try:
            problems = _verify(_generated(), gen.SUPPORTED.versions)
        finally:
            monkeypatch.undo()
            gen._clear_version_caches()  # pyright: ignore[reportPrivateUsage]
        assert any("mistyped" in problem for problem in problems), problems


class TestAdoption:
    """Adopting a release is regenerating; the stubs must come out right without a hand edit."""

    def test_adopting_the_latest_release_regenerates_correctly(self) -> None:
        previous = ENERGYPLUS_VERSIONS[-2]
        with gen.supported_up_to(previous):
            sources = _generated()
            before = sources[2]
            assert _verify(sources, gen.SUPPORTED.versions) == []
            assert f"class IDFDocumentV{previous[0]}_{previous[1]}(" not in sources[3]

        # After the adoption, the release that was the latest has a document type of its own ...
        after = (_PACKAGE / "versioned.pyi").read_text(encoding="utf-8")
        assert f"class IDFDocumentV{previous[0]}_{previous[1]}(" in _committed()[3]
        # ... and a class of a version range that had already ended keeps its name, so an annotation
        # written against it before the adoption still resolves.
        ended = re.findall(r"(?ms)^class (\w+_v\d+_\d+(?:_to_v\d+_\d+)?)\(.*?(?=^\S)", before)
        assert ended
        for name in ended:
            assert re.search(rf"(?m)^class {name}\(", after), f"{name} disappeared on adoption"

    def test_generating_for_an_older_release_does_not_leak_into_the_latest(self) -> None:
        # Every version-dependent cache must be cleared when the supported releases change, or an
        # earlier generation for 24.1 is reused for the full set (a merged group did, once).
        with gen.supported_up_to((24, 1, 0)):
            gen.generate_versioned_documents()
        gen.generate_stubs((24, 1, 0))
        assert _verify(_generated(), gen.SUPPORTED.versions) == []

    def test_the_as_version_docstring_names_the_latest_release_it_was_generated_for(self) -> None:
        # The advice "name the latest release by its own type" must move on with the latest release.
        with gen.supported_up_to((24, 1, 0)):
            stub = gen.generate_versioned_pyi()
        assert "``IDFDocumentV24_1``, not\n    ``IDFDocument``" in stub
        assert "IDFDocumentV26_2``, not" not in stub

    def test_generating_for_an_older_release_keeps_the_run_time_module(self) -> None:
        # versioned.py is what as_version checks against at run time, so it always names every
        # bundled release: generating stubs for 24.1 must not make IDFDocumentV24_1 IDFDocument.
        committed = (_PACKAGE / "versioned.py").read_text(encoding="utf-8")
        with gen.supported_up_to((24, 1, 0)):
            assert gen.generate_versioned_py() == committed

    def test_rejects_a_release_that_is_not_bundled(self) -> None:
        with pytest.raises(ValueError, match="not a bundled"), gen.supported_up_to((7, 2, 0)):
            pass

    def test_restores_the_supported_versions(self) -> None:
        with gen.supported_up_to((22, 1, 0)):
            assert gen.SUPPORTED.latest == (22, 1, 0)
        assert gen.SUPPORTED.versions == ENERGYPLUS_VERSIONS


class TestEndpointEncoding:
    def test_pairs_are_filed_under_the_range_that_holds_them(self) -> None:
        first, second, third = ENERGYPLUS_VERSIONS[:3]
        spans = gen._group_by_span({  # pyright: ignore[reportPrivateUsage]
            first: {"Zone": "A", "Material": "M"},
            second: {"Zone": "A", "Material": "M"},
            third: {"Zone": "B", "Material": "M"},
        })
        assert spans[(first, second)] == {"Zone": "A"}
        assert spans[(third, third)] == {"Zone": "B"}
        assert spans[(first, third)] == {"Material": "M"}

    def test_a_pair_that_returns_is_filed_under_each_run(self) -> None:
        first, second, third = ENERGYPLUS_VERSIONS[:3]
        spans = gen._group_by_span({  # pyright: ignore[reportPrivateUsage]
            first: {"Zone": "A"},
            second: {"Zone": "B"},
            third: {"Zone": "A"},
        })
        assert spans[(first, first)] == {"Zone": "A"}
        assert spans[(third, third)] == {"Zone": "A"}

    def test_union_merges_choices(self) -> None:
        merged = gen._merge_types([  # pyright: ignore[reportPrivateUsage]
            'Literal["Coal", "Steam"]',
            'float | Literal["Coal", "DistrictHeatingWater"]',
            "str",
        ])
        assert merged == 'float | str | Literal["Coal", "Steam", "DistrictHeatingWater"]'

    def test_versions_sharing_a_type_name_are_refused(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(gen.SUPPORTED, "versions", ((9, 0, 0), (9, 0, 1)))
        with pytest.raises(ValueError, match=r"share a major\.minor"):
            gen._check_version_tags()  # pyright: ignore[reportPrivateUsage]
