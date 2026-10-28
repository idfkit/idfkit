"""Tests for the per-version document types: the run-time stand-ins and the generated stubs.

What a type checker reports for these types is checked by ``tests/type_checks/versioned_fixture.py``
under ``make check``. Here: the run-time half (``isinstance``, ``as_version``), and the generator's
promise that the stubs describe every supported version exactly, today and after each adoption.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import get_origin

import pytest

import idfkit.versioned as versioned
from idfkit import load_idf, new_document
from idfkit.codegen import generate_stubs as gen
from idfkit.codegen.verify_stubs import verify
from idfkit.document import AnyIDFDocument, IDFDocument
from idfkit.versions import ENERGYPLUS_VERSIONS, LATEST_VERSION, version_string

_PACKAGE = Path(versioned.__file__).resolve().parent


def _committed() -> tuple[str, str, str]:
    return (
        (_PACKAGE / "_generated_types.pyi").read_text(encoding="utf-8"),
        (_PACKAGE / "document.pyi").read_text(encoding="utf-8"),
        (_PACKAGE / "versioned.pyi").read_text(encoding="utf-8"),
    )


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
        with pytest.raises(TypeError, match="new_document"):
            versioned.IDFDocumentV9_4()
        with pytest.raises(TypeError, match="new_document"):
            AnyIDFDocument()


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
            versioned.as_version(new_document(), dict)  # pyright: ignore[reportArgumentType]


# ---------------------------------------------------------------------------
# Generated stubs
# ---------------------------------------------------------------------------


class TestCommittedStubs:
    def test_describe_every_supported_version_exactly(self) -> None:
        assert verify(*_committed(), ENERGYPLUS_VERSIONS) == []

    @pytest.mark.parametrize(
        ("source", "pattern", "replacement", "expected"),
        [
            # A 9.4 field dropped from the class of its range.
            (2, r"(?m)^    rated_evaporator_fan_power_per_volume_flow_rate: float \| None\n", "", "missing"),
            # A type filed under the wrong class for a range of versions.
            (2, r"IDFCollection\[Space_v9_6_to_v22_1\]", "IDFCollection[Space_v22_2_to_v26_1]", "Space"),
            # An accessor typed with the wrong class.
            (
                2,
                r"def spaces\(self\) -> IDFCollection\[Space_v9_6_to_v22_1\]",
                "def spaces(self) -> IDFCollection[_g.Zone]",
                "accessors",
            ),
            # A type every version has, dropped from AnyIDFDocument.
            (0, r'(?m)^\s+"Zone": ReadOnly\[IDFCollection\[_ZoneBase\]\],\n', "", "AnyIDFDocument"),
        ],
    )
    def test_a_misdescription_is_reported(self, source: int, pattern: str, replacement: str, expected: str) -> None:
        sources = list(_committed())
        mutated = re.sub(pattern, replacement, sources[source], count=1)
        assert mutated != sources[source], "the mutation did not apply"
        sources[source] = mutated
        problems = verify(sources[0], sources[1], sources[2], ENERGYPLUS_VERSIONS)
        assert any(expected in problem for problem in problems), problems


class TestAdoption:
    """Adopting a release is regenerating; the stubs must come out right without a hand edit."""

    def test_adopting_the_latest_release_regenerates_correctly(self) -> None:
        previous = ENERGYPLUS_VERSIONS[-2]
        with gen.supported_up_to(previous):
            before = gen.generate_versioned_pyi()
            sources = (gen.generate_stubs(), gen.generate_document_pyi(), before)
            assert verify(*sources, gen.SUPPORTED.versions) == []
            assert f"class IDFDocumentV{previous[0]}_{previous[1]}(" not in before

        # After the adoption, the release that was the latest has a document type of its own ...
        after = (_PACKAGE / "versioned.pyi").read_text(encoding="utf-8")
        assert f"class IDFDocumentV{previous[0]}_{previous[1]}(" in after
        # ... and a class of a version range that had already ended keeps its name, so an annotation
        # written against it before the adoption still resolves.
        ended = re.findall(r"(?ms)^class (\w+_v\d+_\d+(?:_to_v\d+_\d+)?)\(.*?(?=^\S)", before)
        assert ended
        for name in ended:
            assert re.search(rf"(?m)^class {name}\(", after), f"{name} disappeared on adoption"

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
