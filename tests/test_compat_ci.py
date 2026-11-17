"""Tests for running ``idfkit check`` as a CI gate.

Covers suppression comments (and ``C005``), version narrowing through ``as_version`` and
``doc.version`` guards, target selection (``all``, ``--since``/``--before``), the
``[tool.idfkit.check]`` table, path discovery, output and exit status.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from idfkit.compat import check_compatibility, extract_literals
from idfkit.compat._cli import main
from idfkit.compat._config import (
    ConfigError,
    find_config,
    load_config,
    matches,
    parse_release,
    parse_targets,
    releases_between,
)
from idfkit.compat._models import DEFAULT_RULES
from idfkit.compat._suppress import parse_suppressions
from idfkit.versions import ENERGYPLUS_VERSIONS, LATEST_VERSION

_V89 = (8, 9, 0)
_V94 = (9, 4, 0)
_V96 = (9, 6, 0)
_V221 = (22, 1, 0)
_V262 = (26, 2, 0)
_ALL = list(ENERGYPLUS_VERSIONS)
_IMP = "from idfkit import as_version\nfrom idfkit.versioned import IDFDocumentV9_4, IDFDocumentV9_6, IDFDocument\n"


def _src(body: str) -> str:
    return _IMP + textwrap.dedent(body)


def _codes(
    source: str,
    targets: list[tuple[int, int, int]] | None = None,
    *,
    select: list[str] | None = None,
    ignore: list[str] | None = None,
    suppressions: bool = True,
    exclude_groups: set[str] | None = None,
) -> list[str]:
    diagnostics = check_compatibility(
        source,
        "t.py",
        targets or [_V89, _V262],
        select=select,
        ignore=ignore,
        suppressions=suppressions,
        exclude_groups=exclude_groups,
    )
    return [d.code for d in diagnostics]


def _releases(source: str, value: str) -> frozenset[tuple[int, int, int]] | None:
    """The narrowed releases of the first literal named *value* in *source*."""
    return next(lit for lit in extract_literals(source) if lit.value == value).releases


def _since(release: tuple[int, int, int]) -> frozenset[tuple[int, int, int]]:
    return frozenset(v for v in ENERGYPLUS_VERSIONS if v >= release)


def _before(release: tuple[int, int, int]) -> frozenset[tuple[int, int, int]]:
    return frozenset(v for v in ENERGYPLUS_VERSIONS if v < release)


# ---------------------------------------------------------------------------
# Suppression comments
# ---------------------------------------------------------------------------


class TestSuppressionParsing:
    def test_codes_are_read_and_upper_cased(self) -> None:
        found = parse_suppressions("x = 1  # idfkit: ignore[c001, C004]\n")
        assert found[1].codes == frozenset({"C001", "C004"})

    def test_bare_comment_covers_everything(self) -> None:
        found = parse_suppressions("x = 1  # idfkit: ignore\n")
        assert found[1].codes is None
        assert found[1].covers("C003")

    def test_comment_after_another_tools_comment(self) -> None:
        found = parse_suppressions("x = 1  # noqa: E501  # idfkit: ignore[C001]\n")
        assert found[1].codes == frozenset({"C001"})

    def test_text_in_a_string_is_not_a_comment(self) -> None:
        assert parse_suppressions('x = "# idfkit: ignore[C001]"\n') == {}

    @pytest.mark.parametrize("comment", ["# idfkit: ignore-file", "# idfkit: ignore[C001", "# idfkit: ignorex"])
    def test_unknown_directive_is_not_a_bare_ignore(self, comment: str) -> None:
        assert parse_suppressions(f"x = 1  {comment}\n") == {}

    def test_space_before_codes(self) -> None:
        assert parse_suppressions("x = 1  # idfkit: ignore [C001]\n")[1].codes == frozenset({"C001"})

    def test_other_tools_comments_are_not_read(self) -> None:
        assert parse_suppressions("x = 1  # noqa: C001\ny = 2  # type: ignore[C001]\n") == {}


class TestSuppression:
    SPACE_ADD = 'def f(doc):\n    doc.add("Space", "S")  # idfkit: ignore[C001]\n'

    def test_listed_code_is_silenced(self) -> None:
        assert _codes(_src(self.SPACE_ADD)) == []

    def test_other_codes_stay(self) -> None:
        source = _src('def f(doc):\n    doc.get_collection("Space")  # idfkit: ignore[C001]\n')
        assert _codes(source, select=[*DEFAULT_RULES, "C004"]) == ["C004"]

    def test_bare_comment_silences_every_rule(self) -> None:
        source = _src('def f(doc):\n    doc.get_collection("Zoen")  # idfkit: ignore\n')
        assert _codes(source) == []

    def test_comment_on_another_line_does_nothing(self) -> None:
        source = _src('def f(doc):\n    # idfkit: ignore[C001]\n    doc.add("Space", "S")\n')
        codes = _codes(source)
        assert "C001" in codes
        assert "C005" in codes

    def test_suppressions_can_be_turned_off(self) -> None:
        codes = _codes(_src(self.SPACE_ADD), suppressions=False)
        assert codes
        assert set(codes) == {"C001"}

    def test_works_in_a_file_without_an_idfkit_import(self) -> None:
        assert _codes('doc.add("Space", "S")  # idfkit: ignore[C001]\n') == []


class TestUnusedSuppression:
    def test_unused_code_is_c005(self) -> None:
        diagnostics = check_compatibility(
            _src('def f(doc):\n    doc.add("Zone", "Z")  # idfkit: ignore[C001]\n'), "t.py", [_V89, _V262]
        )
        assert [d.code for d in diagnostics] == ["C005"]
        assert "Unused suppression of C001" in diagnostics[0].message
        assert diagnostics[0].suggested_fix == "remove the comment"

    def test_unused_bare_comment_is_c005(self) -> None:
        assert _codes(_src("x = 1  # idfkit: ignore\n")) == ["C005"]

    def test_unknown_code_is_c005(self) -> None:
        diagnostics = check_compatibility(_src("x = 1  # idfkit: ignore[C099]\n"), "t.py", [_V89, _V262])
        assert [d.code for d in diagnostics] == ["C005"]
        assert "unknown rule code(s) C099" in diagnostics[0].message

    def test_empty_code_list_is_c005(self) -> None:
        assert _codes(_src("x = 1  # idfkit: ignore[]\n")) == ["C005"]

    def test_code_of_a_rule_that_did_not_run_is_not_unused(self) -> None:
        """C004 is opt-in: a C004 comment is not stale in a run that does not check C004."""
        source = _src('def f(doc):\n    doc.get_collection("Zone")  # idfkit: ignore[C004]\n')
        assert _codes(source) == []

    def test_partly_used_comment_reports_the_unused_code(self) -> None:
        source = _src('def f(doc):\n    doc.add("Space", "S")  # idfkit: ignore[C001, C003]\n')
        diagnostics = check_compatibility(source, "t.py", [_V89, _V262])
        assert [d.code for d in diagnostics] == ["C005"]
        assert "C003" in diagnostics[0].message
        assert diagnostics[0].suggested_fix is None

    def test_narrower_targets_make_a_suppression_stale(self) -> None:
        source = _src('def f(doc):\n    doc.add("Space", "S")  # idfkit: ignore[C001]\n')
        assert _codes(source, targets=[_V96, _V262]) == ["C005"]

    def test_ignoring_c005_hides_it(self) -> None:
        assert _codes(_src("x = 1  # idfkit: ignore\n"), ignore=["C005"]) == []

    def test_group_filter_does_not_report_unused(self) -> None:
        source = _src('def f(doc):\n    doc.add("Space", "S")  # idfkit: ignore[C001]\n')
        assert _codes(source, exclude_groups={"Thermal Zones and Surfaces"}) == []


class TestRuleSelection:
    def test_c004_is_off_by_default(self) -> None:
        assert "C004" not in DEFAULT_RULES
        assert _codes(_src('def f(doc):\n    doc.get_collection("Zone")\n')) == []

    def test_c004_can_be_selected(self) -> None:
        source = _src('def f(doc):\n    doc.get_collection("Zone")\n')
        assert _codes(source, select=["C004"]) == ["C004"]

    def test_unknown_code_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown rule code"):
            _codes(_src(""), select=["C999"])


# ---------------------------------------------------------------------------
# Narrowing: as_version
# ---------------------------------------------------------------------------


class TestAsVersionNarrowing:
    def test_single_type(self) -> None:
        source = _src('def f(doc):\n    as_version(doc, IDFDocumentV9_4)["Space"]\n')
        assert _releases(source, "Space") == frozenset({_V94})

    def test_tuple_of_types(self) -> None:
        source = _src('def f(doc):\n    as_version(doc, (IDFDocumentV9_4, IDFDocumentV9_6))["Space"]\n')
        assert _releases(source, "Space") == frozenset({_V94, _V96})

    def test_union_and_latest(self) -> None:
        source = _src('def f(doc):\n    as_version(doc, IDFDocumentV9_6 | IDFDocument)["Space"]\n')
        assert _releases(source, "Space") == frozenset({_V96, LATEST_VERSION})

    def test_generic_and_qualified_type(self) -> None:
        source = _IMP + "from idfkit import versioned\n" + 'as_version(doc, versioned.IDFDocumentV9_6[bool])["Space"]\n'
        assert _releases(source, "Space") == frozenset({_V96})

    def test_document_type_keyword(self) -> None:
        source = _src('as_version(doc, document_type=IDFDocumentV9_6)["Space"]\n')
        assert _releases(source, "Space") == frozenset({_V96})

    @pytest.mark.parametrize("bound", ['"9.6"', '"9.6.0"', "(9, 6, 0)", "(9, 6)", "IDFDocumentV9_6"])
    def test_since(self, bound: str) -> None:
        source = _src(f'as_version(doc, since={bound})["Space"]\n')
        assert _releases(source, "Space") == _since(_V96)

    def test_before(self) -> None:
        source = _src('as_version(doc, before="9.6").add("Zone", "Z")\n')
        assert _releases(source, "Zone") == _before(_V96)

    def test_since_and_before(self) -> None:
        source = _src('as_version(doc, since="9.4", before="22.1")["Space"]\n')
        assert _releases(source, "Space") == frozenset({_V94, (9, 5, 0), _V96})

    def test_unreadable_bound_is_ignored(self) -> None:
        source = _src('as_version(doc, since=first, before="9.6")["Zone"]\n')
        assert _releases(source, "Zone") == _before(_V96)

    def test_unknown_type_is_not_narrowed(self) -> None:
        assert _releases(_src('as_version(doc, SomethingElse)["Space"]\n'), "Space") is None

    def test_name_bound_once_is_followed(self) -> None:
        source = _src(
            """\
            _SINCE_9_4 = (IDFDocumentV9_4, IDFDocumentV9_6)

            def f(doc):
                legacy = as_version(doc, _SINCE_9_4)
                legacy.add("Space", "S")
            """
        )
        assert _releases(source, "Space") == frozenset({_V94, _V96})

    def test_name_bound_twice_is_not_followed(self) -> None:
        source = _src(
            """\
            def f(doc, other):
                legacy = as_version(doc, IDFDocumentV9_6)
                legacy = other
                legacy["Space"]
            """
        )
        assert _releases(source, "Space") is None

    def test_global_name_is_not_followed(self) -> None:
        source = _src(
            """\
            legacy = None

            def f(doc):
                global legacy
                legacy = as_version(doc, IDFDocumentV9_6)
                legacy["Space"]
            """
        )
        assert _releases(source, "Space") is None

    def test_parameter_shadows_module_name(self) -> None:
        source = _src(
            """\
            legacy = as_version(doc, IDFDocumentV9_6)

            def f(legacy):
                legacy["Space"]
            """
        )
        assert _releases(source, "Space") is None

    def test_narrowing_removes_c001(self) -> None:
        source = _src('def f(doc):\n    as_version(doc, since="9.6")["Space"]\n')
        assert _codes(source, targets=_ALL) == []

    def test_narrowed_targets_still_report_what_they_lack(self) -> None:
        source = _src('def f(doc):\n    as_version(doc, since="9.4")["Space"]\n')
        diagnostics = check_compatibility(source, "t.py", _ALL)
        assert [(d.code, d.to_version) for d in diagnostics] == [("C001", "9.4.0"), ("C001", "9.5.0")]

    def test_c003_lists_only_the_narrowed_targets(self) -> None:
        source = _src('def f(doc):\n    as_version(doc, since="25.1").get_collection("Zoen")\n')
        diagnostics = check_compatibility(source, "t.py", _ALL)
        assert [d.code for d in diagnostics] == ["C003"]
        assert "(25.1.0, 25.2.0, 26.1.0, 26.2.0)" in diagnostics[0].message


# ---------------------------------------------------------------------------
# Narrowing: version guards
# ---------------------------------------------------------------------------


class TestVersionGuards:
    def test_greater_equal(self) -> None:
        source = _src('def f(doc):\n    if doc.version >= (9, 6, 0):\n        doc["Space"]\n')
        assert _releases(source, "Space") == _since(_V96)

    def test_reversed_and_two_part(self) -> None:
        source = _src('def f(doc):\n    if (9, 6) <= doc.version:\n        doc["Space"]\n')
        assert _releases(source, "Space") == _since(_V96)

    def test_chained_comparison(self) -> None:
        source = _src('def f(doc):\n    if (9, 4, 0) <= doc.version < (22, 1, 0):\n        doc["Space"]\n')
        assert _releases(source, "Space") == frozenset({_V94, (9, 5, 0), _V96})

    def test_else_gets_the_complement(self) -> None:
        source = _src(
            """\
            def f(doc):
                if doc.version >= (9, 6, 0):
                    doc["Space"]
                else:
                    doc.add("Zone", "Z")
            """
        )
        assert _releases(source, "Zone") == _before(_V96)

    def test_elif_narrows_both_ways(self) -> None:
        source = _src(
            """\
            def f(doc):
                if doc.version < (9, 4, 0):
                    pass
                elif doc.version < (22, 1, 0):
                    doc["Space"]
            """
        )
        assert _releases(source, "Space") == frozenset({_V94, (9, 5, 0), _V96})

    def test_and_with_another_condition(self) -> None:
        """The idfkit-mcp case: a version test and a membership test, then an as_version lookup."""
        source = _src(
            """\
            _SINCE_9_4 = (IDFDocumentV9_4, IDFDocumentV9_6, IDFDocument)

            def f(doc):
                if doc.version >= (9, 4, 0) and "OutputControl:Files" in doc:
                    ctrl = as_version(doc, _SINCE_9_4)["OutputControl:Files"].first()
                else:
                    doc["Space"]
            """
        )
        assert _releases(source, "OutputControl:Files") == frozenset({_V94, _V96, LATEST_VERSION})
        # The else of a partly read test is not narrowed.
        assert _releases(source, "Space") is None
        diagnostics = check_compatibility(source, "t.py", _ALL)
        assert {d.message.split("'")[1] for d in diagnostics} == {"Space"}

    def test_guard_and_as_version_intersect(self) -> None:
        source = _src('def f(doc):\n    if doc.version < (22, 1, 0):\n        as_version(doc, since="9.4")["Space"]\n')
        assert _releases(source, "Space") == frozenset({_V94, (9, 5, 0), _V96})

    def test_guard_on_an_alias_applies_to_the_document(self) -> None:
        source = _src(
            """\
            def f(doc):
                d = doc
                if d.version >= (9, 6, 0):
                    doc["Space"]
            """
        )
        assert _releases(source, "Space") == _since(_V96)

    def test_or_on_one_document(self) -> None:
        source = _src(
            'def f(doc):\n    if doc.version == (9, 4, 0) or doc.version == (9, 6, 0):\n        doc["Space"]\n'
        )
        assert _releases(source, "Space") == frozenset({_V94, _V96})

    def test_not(self) -> None:
        source = _src('def f(doc):\n    if not doc.version < (9, 6, 0):\n        doc["Space"]\n')
        assert _releases(source, "Space") == _since(_V96)

    def test_guard_on_another_document_does_not_apply(self) -> None:
        source = _src('def f(doc, other):\n    if other.version >= (9, 6, 0):\n        doc["Space"]\n')
        assert _releases(source, "Space") is None

    def test_block_that_rebinds_the_document_drops_the_guard(self) -> None:
        source = _src(
            """\
            def f(doc, other):
                if doc.version >= (9, 6, 0):
                    doc = other
                    doc["Space"]
            """
        )
        assert _releases(source, "Space") is None

    @pytest.mark.parametrize(
        "rebinding",
        [
            "[doc['Space'] for doc in others]",
            "try:\n            pass\n        except Exception as doc:\n            doc['Space']",
            "import doc\n        doc['Space']",
            "def doc():\n            pass\n        doc['Space']",
        ],
    )
    def test_every_binding_form_drops_the_guard(self, rebinding: str) -> None:
        source = _src(f"def f(doc, others):\n    if doc.version >= (9, 6, 0):\n        {rebinding}\n")
        assert _releases(source, "Space") is None

    def test_subscripted_receiver_is_not_a_guard(self) -> None:
        source = _src('def f(docs, i):\n    if docs[i].version >= (9, 6, 0):\n        docs[i]["Space"]\n')
        assert _releases(source, "Space") is None

    def test_dotted_receiver_is_a_guard(self) -> None:
        source = _src('def f(self):\n    if self.doc.version >= (9, 6, 0):\n        self.doc["Space"]\n')
        assert _releases(source, "Space") == _since(_V96)

    def test_guard_on_a_local_does_not_narrow_a_module_alias(self) -> None:
        source = _src(
            """\
            legacy = as_version(doc, since="9.4")

            def f(doc):
                if doc.version >= (9, 6, 0):
                    legacy["Space"]
            """
        )
        assert _releases(source, "Space") == _since(_V94)

    def test_alias_of_a_rebound_document_is_not_guarded(self) -> None:
        source = _src(
            """\
            def f(doc, other):
                legacy = as_version(doc, since="9.4")
                doc = other
                if doc.version >= (9, 6, 0):
                    legacy["Space"]
            """
        )
        assert _releases(source, "Space") == _since(_V94)

    def test_declared_version_within_a_release_line(self) -> None:
        """A ``Version, 9.0;`` model is ``(9, 0, 0)`` on the 9.0.1 schema."""
        source = _src('def f(doc):\n    if doc.version == (9, 0, 0):\n        doc["Space"]\n')
        assert _releases(source, "Space") == frozenset({(9, 0, 1)})

    def test_version_newer_than_every_release_keeps_the_latest(self) -> None:
        source = _src('def f(doc):\n    if doc.version >= (27, 0, 0):\n        doc["Space"]\n')
        assert _releases(source, "Space") == frozenset({LATEST_VERSION})

    def test_nested_function_is_outside_the_guard(self) -> None:
        source = _src(
            """\
            def f(doc):
                if doc.version >= (9, 6, 0):
                    def g():
                        return doc["Space"]
            """
        )
        assert _releases(source, "Space") is None

    def test_early_return_is_not_recognised(self) -> None:
        source = _src('def f(doc):\n    if doc.version < (9, 6, 0):\n        return\n    doc["Space"]\n')
        assert _releases(source, "Space") is None

    def test_non_tuple_comparison_is_not_read(self) -> None:
        source = _src('def f(doc, v):\n    if doc.version >= v:\n        doc["Space"]\n')
        assert _releases(source, "Space") is None

    def test_guard_excluding_every_target_reports_nothing(self) -> None:
        source = _src('def f(doc):\n    if doc.version < (9, 0, 0):\n        doc.get_collection("Zoen")\n')
        assert _codes(source, targets=[_V96, _V262]) == []

    def test_guard_removes_c001_and_c002(self) -> None:
        source = _src('def f(doc):\n    if doc.version >= (9, 6, 0):\n        doc.add("Space", "S")\n')
        assert _codes(source, targets=_ALL) == []

    def test_no_narrowing_without_an_idfkit_import(self) -> None:
        source = 'if doc.version >= (9, 6, 0):\n    doc.add("Space", "S")\n'
        assert _releases(source, "Space") is None


# ---------------------------------------------------------------------------
# Relative imports inside idfkit
# ---------------------------------------------------------------------------


class TestPackageImports:
    SOURCE = 'from .document import IDFDocument\ndef f(doc):\n    doc.get_collection("Zoen")\n'

    def test_relative_import_inside_idfkit_counts(self) -> None:
        assert [lit.value for lit in extract_literals(self.SOURCE, package="idfkit.simulation")] == ["Zoen"]

    def test_relative_import_elsewhere_does_not(self) -> None:
        assert extract_literals(self.SOURCE, package="myapp") == []
        assert extract_literals(self.SOURCE) == []

    def test_parent_relative_import(self) -> None:
        source = 'from ..document import IDFDocument\ndoc.get_collection("Zoen")\n'
        assert len(extract_literals(source, package="idfkit.simulation")) == 1
        assert extract_literals(source, package="idfkit") == []


# ---------------------------------------------------------------------------
# Target releases
# ---------------------------------------------------------------------------


class TestReleases:
    @pytest.mark.parametrize("spec", ["9.0", "9.0.0", "9.0.1"])
    def test_nine_zero_is_nine_zero_one(self, spec: str) -> None:
        assert parse_release(spec) == (9, 0, 1)

    @pytest.mark.parametrize("spec", ["27.1", "26.3", "10.0", "1.0"])
    def test_unsupported_line_is_an_error(self, spec: str) -> None:
        with pytest.raises(ConfigError, match="not a release idfkit supports"):
            parse_release(spec)

    @pytest.mark.parametrize("spec", ["24", "24.x", "24..1", "", "9.\u00b2"])
    def test_malformed_is_an_error(self, spec: str) -> None:
        with pytest.raises(ConfigError, match="Invalid version specifier"):
            parse_release(spec)

    def test_all(self) -> None:
        assert parse_targets("all") == _ALL
        assert parse_targets(["ALL"]) == _ALL

    def test_since_before(self) -> None:
        assert releases_between((22, 1, 0), (23, 2, 0)) == [(22, 1, 0), (22, 2, 0), (23, 1, 0)]
        assert releases_between(None, (9, 1, 0)) == [(8, 9, 0), (9, 0, 1)]


# ---------------------------------------------------------------------------
# CLI: targets, config, discovery, output
# ---------------------------------------------------------------------------

_GUARDED = """\
from idfkit import as_version

def f(doc):
    doc.add("Space", "S")
"""


def _run(argv: list[str], capsys: pytest.CaptureFixture[str]) -> tuple[int, str, str]:
    with pytest.raises(SystemExit) as exc_info:
        main(argv)
    captured = capsys.readouterr()
    code = exc_info.value.code
    return (code if isinstance(code, int) else 0), captured.out, captured.err


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An empty repository root as the working directory."""
    (tmp_path / ".git").mkdir()
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _write_config(root: Path, body: str) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = 'x'\n\n[tool.idfkit.check]\n" + textwrap.dedent(body))


class TestCliTargets:
    def test_targets_all(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        (project / "a.py").write_text(_GUARDED)
        code, out, _ = _run(["check", "a.py", "--targets", "all", "--json"], capsys)
        assert code == 1
        assert json.loads(out)["targets"] == [f"{v[0]}.{v[1]}.{v[2]}" for v in ENERGYPLUS_VERSIONS]

    def test_since(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        (project / "a.py").write_text(_GUARDED)
        code, out, _ = _run(["check", "a.py", "--since", "9.6", "--json"], capsys)
        assert code == 0
        assert json.loads(out)["targets"][0] == "9.6.0"

    def test_since_before(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        (project / "a.py").write_text(_GUARDED)
        _code, out, _ = _run(["check", "a.py", "--since", "9.4", "--before", "22.1", "--json"], capsys)
        assert json.loads(out)["targets"] == ["9.4.0", "9.5.0", "9.6.0"]

    def test_before_alone(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        (project / "a.py").write_text(_GUARDED)
        _code, out, _ = _run(["check", "a.py", "--before", "9.1", "--json"], capsys)
        assert json.loads(out)["targets"] == ["8.9.0", "9.0.1"]

    def test_from_to_compares_only_two(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        (project / "a.py").write_text(_GUARDED)
        _code, out, _ = _run(["check", "a.py", "--from", "8.9", "--to", "26.2", "--json"], capsys)
        assert json.loads(out)["targets"] == ["8.9.0", "26.2.0"]

    @pytest.mark.parametrize(
        "argv",
        [
            ["--targets", "all", "--since", "9.4"],
            ["--from", "9.4", "--since", "9.6"],
            ["--targets", "9.4,26.2", "--before", "9.6"],
            ["--to", "26.2"],
            ["--from", "8.9", "--to", "26.2", "--before", "9.6"],
            ["--since", "24.1", "--to", "9.4"],
            ["--targets", "9.4,26.2", "--to", "24.1"],
            ["--since", "26.2"],
            ["--targets", "24.1,27.1"],
            [],
        ],
    )
    def test_usage_errors_exit_2(self, project: Path, capsys: pytest.CaptureFixture[str], argv: list[str]) -> None:
        (project / "a.py").write_text(_GUARDED)
        code, _, _ = _run(["check", "a.py", *argv], capsys)
        assert code == 2


class TestCliConfig:
    def test_targets_and_paths_from_config(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        _write_config(project, 'targets = "all"\npaths = ["src"]\n')
        (project / "src").mkdir()
        (project / "src" / "a.py").write_text(_GUARDED)
        (project / "b.py").write_text(_GUARDED)  # outside paths
        code, out, _ = _run(["check"], capsys)
        assert code == 1
        assert "a.py" in out
        assert "b.py" not in out

    def test_found_from_a_subdirectory(
        self, project: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _write_config(project, 'since = "9.6"\n')
        sub = project / "pkg"
        sub.mkdir()
        (sub / "a.py").write_text(_GUARDED)
        monkeypatch.chdir(sub)
        code, out, _ = _run(["check", "a.py"], capsys)
        assert (code, out.strip()) == (0, "No compatibility issues found.")

    def test_search_stops_at_the_repository_root(self, tmp_path: Path) -> None:
        _write_config(tmp_path, 'targets = "all"\n')
        repo = tmp_path / "repo"
        (repo / ".git").mkdir(parents=True)
        assert find_config(repo) is None
        assert find_config(tmp_path) == tmp_path / "pyproject.toml"

    def test_command_line_targets_override(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        _write_config(project, 'since = "9.6"\n')
        (project / "a.py").write_text(_GUARDED)
        code, _, _ = _run(["check", "a.py", "--targets", "all"], capsys)
        assert code == 1

    def test_isolated_ignores_config(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        _write_config(project, 'since = "9.6"\n')
        (project / "a.py").write_text(_GUARDED)
        code, _, err = _run(["check", "a.py", "--isolated"], capsys)
        assert code == 2
        assert "no target releases" in err

    def test_explicit_config(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        other = project / "conf"
        other.mkdir()
        _write_config(other, 'since = "9.6"\n')
        (project / "a.py").write_text(_GUARDED)
        code, _, _ = _run(["check", "a.py", "--config", str(other / "pyproject.toml")], capsys)
        assert code == 0

    def test_select_extend_select_and_ignore(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        _write_config(project, 'targets = "all"\nextend-select = ["C004"]\nignore = ["C001"]\n')
        (project / "a.py").write_text("import idfkit\ndoc.get_collection('Space')\n")
        _code, out, _ = _run(["check", "a.py", "--json"], capsys)
        assert {d["code"] for d in json.loads(out)["diagnostics"]} == {"C004"}
        # A command-line --select replaces the configured selection, extend-select included.
        code, out, _ = _run(["check", "a.py", "--select", "C003"], capsys)
        assert (code, out.strip()) == (0, "No compatibility issues found.")
        # --extend-select on the command line adds to a command-line --select.
        _code, out, _ = _run(["check", "a.py", "--json", "--select", "C003", "--extend-select", "C004"], capsys)
        assert {d["code"] for d in json.loads(out)["diagnostics"]} == {"C004"}
        # --ignore on the command line adds to the configured ignore.
        code, out, _ = _run(["check", "a.py", "--ignore", "C004"], capsys)
        assert (code, out.strip()) == (0, "No compatibility issues found.")

    @pytest.mark.parametrize("argv", [["--select", ""], ["--select", "C001", "--ignore", "C001"]])
    def test_empty_rule_selection_exits_2(
        self, project: Path, capsys: pytest.CaptureFixture[str], argv: list[str]
    ) -> None:
        (project / "a.py").write_text(_GUARDED)
        code, _, err = _run(["check", "a.py", "--targets", "all", *argv], capsys)
        assert code == 2
        assert "rule selection is empty" in err

    def test_config_paths_are_reported_relative(
        self, project: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _write_config(project, 'targets = "all"\npaths = ["src"]\n')
        (project / "src").mkdir()
        (project / "src" / "a.py").write_text(_GUARDED)
        _code, out, _ = _run(["check", "--json"], capsys)
        assert {d["filename"] for d in json.loads(out)["diagnostics"]} == {"src/a.py"}
        (project / "sub").mkdir()
        monkeypatch.chdir(project / "sub")
        _code, out, _ = _run(["check", "--json"], capsys)
        assert {d["filename"] for d in json.loads(out)["diagnostics"]} == {"../src/a.py"}

    def test_per_file_ignores(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        _write_config(project, 'targets = "all"\n[tool.idfkit.check.per-file-ignores]\n"tests/**" = ["C001"]\n')
        (project / "tests" / "deep").mkdir(parents=True)
        (project / "tests" / "deep" / "t.py").write_text(_GUARDED)
        (project / "a.py").write_text(_GUARDED)
        _code, out, _ = _run(["check", ".", "--json"], capsys)
        assert {d["filename"] for d in json.loads(out)["diagnostics"]} == {"a.py"}

    def test_exclude_applies_to_named_files_too(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        _write_config(project, 'targets = "all"\nexclude = ["legacy"]\n')
        (project / "legacy").mkdir()
        (project / "legacy" / "old.py").write_text(_GUARDED)
        code, out, _ = _run(["check", "legacy/old.py", "."], capsys)
        assert (code, out.strip()) == (0, "No compatibility issues found.")

    def test_fail_on_error(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        _write_config(project, 'targets = "all"\nfail-on = "error"\n')
        (project / "a.py").write_text(_GUARDED)
        code, out, _ = _run(["check", "a.py"], capsys)
        assert code == 0
        assert "C001" in out
        (project / "b.py").write_text("import idfkit\ndoc.get_collection('Zoen')\n")
        code, _, _ = _run(["check", "b.py"], capsys)
        assert code == 1
        code, _, _ = _run(["check", "a.py", "--fail-on", "warning"], capsys)
        assert code == 1

    @pytest.mark.parametrize(
        ("body", "message"),
        [
            ('targts = "all"\n', "unknown key(s) in [tool.idfkit.check]: targts"),
            ('targets = "all"\nsince = "9.4"\n', "not both"),
            ('targets = ["9.4", "27.1"]\n', "not a release idfkit supports"),
            ('targets = ["9.4"]\n', "at least two"),
            ('targets = "all"\nselect = "C001"\n', "must be a list of strings"),
            ('targets = "all"\nselect = ["C009"]\n', "unknown rule code"),
            ('targets = "all"\nfail-on = "info"\n', "must be 'warning' or 'error'"),
            ('targets = "all"\nper-file-ignores = { "x.py" = "C001" }\n', "must be a list of rule codes"),
            ("targets = [\n", "pyproject.toml"),
        ],
    )
    def test_invalid_config_exits_2(
        self, project: Path, capsys: pytest.CaptureFixture[str], body: str, message: str
    ) -> None:
        _write_config(project, body)
        (project / "a.py").write_text(_GUARDED)
        code, _, err = _run(["check", "a.py"], capsys)
        assert code == 2
        assert message in err

    def test_load_config_without_the_table(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n")
        with pytest.raises(ConfigError, match=r"no \[tool\.idfkit\.check\] table"):
            load_config(tmp_path / "pyproject.toml")


class TestPatterns:
    @pytest.mark.parametrize(
        ("path", "pattern", "expected"),
        [
            ("tests/a/b.py", "tests/**", True),
            ("tests/a/b.py", "tests/*", True),
            ("tests/a/b.py", "tests", True),
            ("src/conftest.py", "conftest.py", True),
            ("src/a.py", "./src/a.py", True),
            ("src/a.py", "tests/**", False),
            ("src/a/conftest.py", "src/conftest.py", False),
            ("src/app/migrations/m.py", "migrations", True),
            ("src/app/migrations_old/m.py", "migrations", False),
            ("conftest.py", "**/conftest.py", True),
            ("tests/a.py", "tests/**/*.py", True),
            ("tests/x/a.py", "tests/**/*.py", True),
            ("src/a.py", "tests/**/*.py", False),
        ],
    )
    def test_matches(self, path: str, pattern: str, expected: bool) -> None:
        assert matches(path, pattern) is expected


class TestCliDiscoveryAndOutput:
    def test_directory_is_searched_skipping_hidden_and_venvs(
        self, project: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        for rel in ["pkg/a.py", "pkg/sub/b.py", ".venv/lib/c.py", "pkg/__pycache__/d.py", "node_modules/e.py"]:
            path = project / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(_GUARDED)
        _code, out, _ = _run(["check", ".", "--targets", "9.4,26.2", "--json"], capsys)
        assert sorted({d["filename"] for d in json.loads(out)["diagnostics"]}) == ["pkg/a.py", "pkg/sub/b.py"]

    def test_missing_path_exits_2(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        code, _, err = _run(["check", "nope.py", "--targets", "all"], capsys)
        assert code == 2
        assert "file not found" in err

    def test_undecodable_file_exits_2_and_the_others_are_checked(
        self, project: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        (project / "a.py").write_bytes(b'x = "\xff"\n')
        (project / "b.py").write_text(_GUARDED)
        code, out, err = _run(["check", "a.py", "b.py", "--targets", "9.4,26.2"], capsys)
        assert code == 2
        assert "failed to read a.py" in err
        assert "b.py" in out

    def test_syntax_error_does_not_stop_the_other_files(
        self, project: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        (project / "a.py").write_text("def broken(:\n")
        (project / "b.py").write_text(_GUARDED)
        code, out, err = _run(["check", "a.py", "b.py", "--targets", "9.4,26.2"], capsys)
        assert code == 2
        assert "failed to parse a.py" in err
        assert "b.py" in out

    def test_text_summary_line(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        (project / "a.py").write_text(_GUARDED)
        _code, out, _ = _run(["check", "a.py", "--since", "9.4", "--before", "22.1"], capsys)
        lines = out.strip().splitlines()
        assert lines[-1] == "Found 2 issues (0 errors, 2 warnings) in 1 file."
        assert all(line.startswith("a.py:4:12: C001 [warning]") for line in lines[:-1])

    def test_output_order_is_stable(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        for name in ["b.py", "a.py", "c/z.py"]:
            (project / name).parent.mkdir(parents=True, exist_ok=True)
            (project / name).write_text(_GUARDED)
        _code, first, _ = _run(["check", ".", "--targets", "all"], capsys)
        _code, second, _ = _run(["check", ".", "--targets", "all"], capsys)
        assert first == second
        order = [line.split(":")[0] for line in first.splitlines()[:-1]]
        assert order == sorted(order)

    def test_sarif_carries_the_idfkit_version(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        import idfkit

        (project / "a.py").write_text(_GUARDED)
        _code, out, _ = _run(["check", "a.py", "--targets", "9.4,26.2", "--sarif"], capsys)
        driver = json.loads(out)["runs"][0]["tool"]["driver"]
        assert driver["version"] == idfkit.__version__
        assert {r["id"] for r in driver["rules"]} >= {"C004", "C005"}

    def test_suppression_through_the_cli(self, project: Path, capsys: pytest.CaptureFixture[str]) -> None:
        (project / "a.py").write_text(_GUARDED.replace('"S")', '"S")  # idfkit: ignore[C001]'))
        code, _, _ = _run(["check", "a.py", "--targets", "all"], capsys)
        assert code == 0
        code, out, _ = _run(["check", "a.py", "--since", "9.6"], capsys)
        assert code == 1
        assert "C005" in out


_NARROW_TARGETS = [_V94, (24, 1, 0)]


class TestNarrowingKeepsDefiniteMisses:
    """A literal no release in scope has, but another target has, is reported, not skipped."""

    def test_version_guard(self) -> None:
        source = _src('def f(doc):\n    if doc.version < (9, 6, 0):\n        doc.add("Space", "S")\n')
        assert [d.code for d in check_compatibility(source, "t.py", _NARROW_TARGETS)] == ["C001"]

    def test_as_version(self) -> None:
        source = _src('def f(doc):\n    legacy = as_version(doc, IDFDocumentV9_4)\n    legacy.add("Space", "S")\n')
        assert [d.code for d in check_compatibility(source, "t.py", _NARROW_TARGETS)] == ["C001"]

    def test_get_collection_is_c001_not_a_misspelling(self) -> None:
        source = _src('def f(doc):\n    if doc.version < (9, 6, 0):\n        doc.get_collection("Space")\n')
        assert [d.code for d in check_compatibility(source, "t.py", _NARROW_TARGETS)] == ["C001"]

    def test_range_alias_narrows(self) -> None:
        source = (
            "from idfkit.versioned import IDFDocumentSince9_2, as_version\n"
            'def f(doc):\n    as_version(doc, IDFDocumentSince9_2)["Construction:AirBoundary"]\n'
        )
        assert check_compatibility(source, "t.py", [(9, 1, 0), _V94]) == []

    def test_default_is_read_in_the_enclosing_scope(self) -> None:
        source = _src(
            'legacy = doc\ndef f(x=legacy["Construction:AirBoundary"]):\n    legacy = as_version(x, IDFDocumentV9_4)\n'
        )
        (literal,) = extract_literals(source, "t.py")
        assert literal.releases is None
