"""Guard the page-kinds gate (FR-055, FR-059, SC-022, T112).

The gate lives in ``scripts/check_page_kinds.py``. It is a maintainer script rather than part of the
distributed package, so it is loaded by path, the way ``tests/test_parity_macro.py`` loads the docs
hook it guards.

Every test builds its own miniature site in ``tmp_path``: a ``mkdocs.yml`` and a handful of pages.
Nothing here reads the repository's own documentation except the one test that deliberately does, so
none of it needs a network, a sibling checkout, or a built site.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "check_page_kinds.py"


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gate = _load("check_page_kinds", _SCRIPT)


FOUR_KINDS = """\
  - Tutorials:
    - tutorials/index.md
  - How-to guides:
    - how-to/index.md
  - Reference:
    - reference/index.md
  - Explanation:
    - explanation/index.md
"""


def build(root: Path, nav: str, pages: dict[str, str], *, preamble: str = "") -> Path:
    """Write one miniature site and return the path to its mkdocs.yml."""
    docs = root / "docs"
    for relative, body in pages.items():
        page = docs / relative
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(body, encoding="utf-8")
    docs.mkdir(parents=True, exist_ok=True)
    config = root / "mkdocs.yml"
    config.write_text(f"site_name: test\n{preamble}nav:\n{nav}", encoding="utf-8")
    return config


def codes(report: Any) -> list[str]:
    return sorted(finding.code for finding in report.findings)


def kind_of(report: Any, path: str) -> str:
    return next(page.kind_label for page in report.pages if page.path == path)


class TestKindComesFromTheNavigation:
    def test_each_top_level_section_declares_a_kind(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            FOUR_KINDS,
            {
                "tutorials/index.md": "# Learning\n",
                "how-to/index.md": "# Tasks\n",
                "reference/index.md": "# Facts\n",
                "explanation/index.md": "# Understanding\n",
            },
        )
        report = gate.run(config, None)

        assert report.ok
        assert kind_of(report, "tutorials/index.md") == "tutorial"
        assert kind_of(report, "how-to/index.md") == "how-to"
        assert kind_of(report, "reference/index.md") == "reference"
        assert kind_of(report, "explanation/index.md") == "explanation"

    def test_wording_variants_of_a_section_title_still_resolve(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Guides:\n    - guides/one.md\n  - Explanations:\n    - explanation/one.md\n",
            {"guides/one.md": "# One\n", "explanation/one.md": "# Two\n"},
        )
        report = gate.run(config, None)

        assert kind_of(report, "guides/one.md") == "how-to"
        assert kind_of(report, "explanation/one.md") == "explanation"

    def test_a_page_in_two_sections_is_two_kinds_and_fails(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Tutorials:\n    - shared.md\n  - Reference:\n    - shared.md\n",
            {"shared.md": "# Shared\n"},
        )
        report = gate.run(config, None)

        assert codes(report) == ["two-kinds"]
        assert "tutorial" in report.findings[0].message
        assert "reference" in report.findings[0].message

    def test_a_page_listed_twice_in_one_section_is_a_warning(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Tutorials:\n    - one.md\n    - Again: one.md\n",
            {"one.md": "# One\n"},
        )
        report = gate.run(config, None)

        assert report.ok
        assert any("listed 2 times" in warning for warning in report.warnings)

    def test_a_fifth_section_fails(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            FOUR_KINDS + "  - Troubleshooting:\n    - troubleshooting/errors.md\n",
            {
                "tutorials/index.md": "# A\n",
                "how-to/index.md": "# B\n",
                "reference/index.md": "# C\n",
                "explanation/index.md": "# D\n",
                "troubleshooting/errors.md": "# E\n",
            },
        )
        report = gate.run(config, None)

        assert codes(report) == ["unclassified-section"]
        assert report.findings[0].subject == "Troubleshooting"

    def test_the_site_home_carries_no_kind_and_is_not_a_section(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Home: index.md\n  - Tutorials:\n    - one.md\n",
            {"index.md": "# Home\n", "one.md": "# One\n"},
        )
        report = gate.run(config, None)

        assert report.ok
        assert kind_of(report, "index.md") == "unclassified"

    def test_a_page_no_navigation_entry_reaches_is_reported(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Tutorials:\n    - one.md\n",
            {"one.md": "# One\n", "orphan.md": "# Orphan\n"},
        )
        report = gate.run(config, None)

        assert codes(report) == ["no-declared-kind"]
        assert report.findings[0].subject == "orphan.md"

    def test_a_navigation_entry_pointing_at_nothing_is_reported(self, tmp_path: Path) -> None:
        config = build(tmp_path, "  - Tutorials:\n    - gone.md\n", {"kept.md": "# Kept\n"})
        report = gate.run(config, None)

        assert "missing-page" in codes(report)

    def test_exclude_docs_keeps_a_non_page_out_of_the_count(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Tutorials:\n    - one.md\n",
            {"one.md": "# One\n", "bundle/SKILL.md": "# Not a page\n"},
            preamble="exclude_docs: |\n  # a comment\n  bundle/SKILL.md\n",
        )
        report = gate.run(config, None)

        assert report.ok
        assert [page.path for page in report.pages] == ["one.md"]


class TestTheOneDeclaredException:
    def test_the_agent_references_tree_is_a_section_without_being_a_kind(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Tutorials:\n    - one.md\n  - Developing with idfkit:\n    - agent-references/index.md\n",
            {"one.md": "# One\n", "agent-references/index.md": "# Dispatch\n"},
        )
        report = gate.run(config, None)

        assert report.ok
        assert kind_of(report, "agent-references/index.md") == "agent-references"

    def test_the_exception_is_recognised_by_path_not_by_title(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Something else entirely:\n    - agent-references/index.md\n",
            {"agent-references/index.md": "# Dispatch\n"},
        )
        report = gate.run(config, None)

        assert report.ok
        assert kind_of(report, "agent-references/index.md") == "agent-references"

    def test_a_human_page_inside_the_exception_section_leaks(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Developing with idfkit:\n    - agent-references/index.md\n    - how-to/one.md\n",
            {"agent-references/index.md": "# Dispatch\n", "how-to/one.md": "# One\n"},
        )
        report = gate.run(config, None)

        # The section stops being the exception the moment a page outside the tree joins it.
        assert codes(report) == ["unclassified-section"]

    def test_an_exception_page_filed_under_a_kind_leaks(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Reference:\n    - agent-references/index.md\n",
            {"agent-references/index.md": "# Dispatch\n"},
        )
        report = gate.run(config, None)

        assert "exception-leak" in codes(report)

    def test_a_second_exception_makes_the_gate_refuse_to_run(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        config = build(tmp_path, "  - Tutorials:\n    - one.md\n", {"one.md": "# One\n"})
        monkeypatch.setattr(gate, "DECLARED_EXCEPTIONS", ("agent-references/", "something-else/"))

        with pytest.raises(gate.Refusal, match="FR-059 permits exactly one"):
            gate.run(config, None)


class TestReadingPages:
    def test_a_heading_inside_a_fence_is_not_a_heading(self) -> None:
        headings, blocks = gate.parse_markdown("# Real\n\n```markdown\n# Not real\n```\n")

        assert [heading.text for heading in headings] == ["Real"]
        assert len(blocks) == 1

    def test_a_trailing_anchor_and_inline_markup_normalise_away(self) -> None:
        assert gate.normalize_heading("`simulate()` and Friends {#anchor}") == "simulate and friends"

    def test_a_notebook_is_read_rather_than_skipped(self, tmp_path: Path) -> None:
        notebook = (
            '{"cells": [{"cell_type": "markdown", "source": ["# Build a first model\\n"]}, '
            '{"cell_type": "code", "source": ["import idfkit\\n", "print(idfkit)\\n"]}]}'
        )
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "one.ipynb").write_text(notebook, encoding="utf-8")
        page = gate.read_page(tmp_path / "docs", "one.ipynb", gate.PageKind.TUTORIAL)

        assert [heading.text for heading in page.headings] == ["Build a first model"]
        assert page.code_blocks[0].content.startswith("import idfkit")
        assert page.unreadable is None

    def test_a_broken_notebook_reports_rather_than_crashing(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - Tutorials:\n    - one.ipynb\n",
            {"one.ipynb": "{not json at all"},
        )
        report = gate.run(config, None)

        assert report.ok
        assert any("could not be read" in warning for warning in report.warnings)


class TestDuplication:
    def test_the_same_heading_under_two_kinds_fails(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - How-to guides:\n    - how-to/one.md\n  - Explanation:\n    - explanation/one.md\n",
            {
                "how-to/one.md": "# Run a design day simulation\n",
                "explanation/one.md": "## run a **design day** simulation\n",
            },
        )
        report = gate.run(config, None)

        assert codes(report) == ["duplicate-heading"]
        assert "text match, not a semantic one" in report.findings[0].message

    def test_the_same_heading_within_one_kind_is_only_a_warning(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - How-to guides:\n    - one.md\n    - two.md\n",
            {"one.md": "# Run a design day simulation\n", "two.md": "# Run a design day simulation\n"},
        )
        report = gate.run(config, None)

        assert report.ok
        assert any("repeats within one kind" in warning for warning in report.warnings)

    def test_a_short_or_structural_heading_is_not_duplication(self, tmp_path: Path) -> None:
        config = build(
            tmp_path,
            "  - How-to guides:\n    - how-to/one.md\n  - Explanation:\n    - explanation/one.md\n",
            {
                "how-to/one.md": "# Example\n\n## How it works\n",
                "explanation/one.md": "# Example\n\n## How it works\n",
            },
        )
        report = gate.run(config, None)

        assert report.ok
        assert not report.warnings

    def test_the_same_code_block_under_two_kinds_fails(self, tmp_path: Path) -> None:
        block = (
            "```python\n"
            "from idfkit import load_idf\n"
            "document = load_idf('model.idf')\n"
            "print(len(document.objects))\n"
            "```\n"
        )
        config = build(
            tmp_path,
            "  - Tutorials:\n    - tutorials/one.md\n  - Reference:\n    - reference/one.md\n",
            {"tutorials/one.md": f"# A tutorial page\n\n{block}", "reference/one.md": f"# A reference page\n\n{block}"},
        )
        report = gate.run(config, None)

        assert codes(report) == ["duplicate-code-block"]

    def test_a_short_code_block_is_below_the_floor(self, tmp_path: Path) -> None:
        block = "```bash\npip install idfkit\n```\n"
        config = build(
            tmp_path,
            "  - Tutorials:\n    - tutorials/one.md\n  - Reference:\n    - reference/one.md\n",
            {"tutorials/one.md": f"# A tutorial page\n\n{block}", "reference/one.md": f"# A reference page\n\n{block}"},
        )
        report = gate.run(config, None)

        assert report.ok

    def test_a_shared_snippet_include_is_reported_not_failed(self, tmp_path: Path) -> None:
        block = '```python\n--8<-- "docs/snippets/simulation/running/basic_usage.py:example"\n```\n'
        config = build(
            tmp_path,
            "  - Tutorials:\n    - tutorials/one.md\n  - Reference:\n    - reference/one.md\n",
            {"tutorials/one.md": f"# A tutorial page\n\n{block}", "reference/one.md": f"# A reference page\n\n{block}"},
        )
        report = gate.run(config, None)

        assert report.ok
        assert any("single-sourced rather than copied" in warning for warning in report.warnings)

    def test_the_exception_tree_takes_no_part_in_the_scan(self, tmp_path: Path) -> None:
        heading = "# Load and inspect a document\n"
        config = build(
            tmp_path,
            "  - Reference:\n    - reference/one.md\n  - Developing with idfkit:\n    - agent-references/one.md\n",
            {"reference/one.md": heading, "agent-references/one.md": heading},
        )
        report = gate.run(config, None)

        assert report.ok


class TestExitContract:
    def test_a_clean_site_exits_zero(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        config = build(tmp_path, "  - Tutorials:\n    - one.md\n", {"one.md": "# One\n"})

        assert gate.main(["--config", str(config)]) == gate.EXIT_OK
        assert "OK: every page is exactly one kind" in capsys.readouterr().out

    def test_a_finding_exits_one(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        config = build(
            tmp_path,
            "  - Tutorials:\n    - shared.md\n  - Reference:\n    - shared.md\n",
            {"shared.md": "# Shared\n"},
        )

        assert gate.main(["--config", str(config)]) == gate.EXIT_FAILED
        assert "FAILED" in capsys.readouterr().out

    def test_a_missing_config_exits_two(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        assert gate.main(["--config", str(tmp_path / "nowhere.yml")]) == gate.EXIT_REFUSED
        assert "refusing to run" in capsys.readouterr().err

    def test_a_config_without_a_nav_exits_two(self, tmp_path: Path) -> None:
        config = tmp_path / "mkdocs.yml"
        config.write_text("site_name: test\n", encoding="utf-8")
        (tmp_path / "docs").mkdir()

        with pytest.raises(gate.Refusal, match="declares no `nav:`"):
            gate.run(config, None)

    def test_the_docs_directory_can_be_given_positionally(self, tmp_path: Path) -> None:
        config = build(tmp_path, "  - Tutorials:\n    - one.md\n", {"one.md": "# One\n"})

        assert gate.main([str(tmp_path / "docs"), "--config", str(config)]) == gate.EXIT_OK


class TestAgainstThisRepository:
    """One test that reads the real navigation, because its `!!python/name:` tags are the hazard."""

    def test_the_repository_navigation_parses_and_classifies(self) -> None:
        report = gate.run(_REPO_ROOT / "mkdocs.yml", None)

        assert report.pages
        assert {page.kind_label for page in report.pages} >= {"tutorial", "how-to", "reference", "explanation"}
