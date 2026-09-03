"""Guard the ``parity(id)`` documentation macro (FR-047, T125, T126).

The macro lives in ``docs/hooks/parity_macro.py`` and runs inside the MkDocs build. Two of its
properties are worth pinning down here rather than discovering in a broken docs build:

* a capability complete on both sides renders *nothing*, so a page with no parity story to tell
  carries no furniture about parity;
* an id that does not resolve fails the build, so a typo cannot render as a silently missing
  parity statement, which a reader would take as "no difference to report".

Every test builds its own capabilities, so none of this needs a conformance checkout, a git tag, or
a network. The reading of the pinned ledger is exercised by the docs build itself.

The hook is imported by path, the way MkDocs imports a hook: it is not part of the distributed
package and is not importable as ``idfkit.something``. It carries the ledger model itself, imported
from its sibling ``docs/hooks/parity_ledger.py``, so nothing here reaches into ``scripts/``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest
from mkdocs.exceptions import PluginError

_REPO_ROOT = Path(__file__).resolve().parent.parent
_HOOK_PATH = _REPO_ROOT / "docs" / "hooks" / "parity_macro.py"


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


macro = _load("parity_macro_under_test", _HOOK_PATH)


def capability(**overrides: Any) -> Any:
    """One ledger entry, built from the render script's own dataclass."""
    fields: dict[str, Any] = {
        "capability_id": "example",
        "title": "An example capability",
        "tier": "tier-1",
        "python": "complete",
        "typescript": "complete",
    }
    fields.update(overrides)
    return macro.Capability(**fields)


def page(source: str, *, src_uri: str = "how-to/example.md", **entries: Any) -> str:
    capabilities = {entry.capability_id: entry for entry in entries.values()}
    return macro.substitute(source, src_uri, capabilities)


MACRO_CALL = '{{ parity("example") }}'


class TestBothComplete:
    def test_renders_nothing(self) -> None:
        rendered = page(f"Before.\n\n{MACRO_CALL}\n\nAfter.\n", entry=capability())
        assert "admonition" not in rendered
        assert "!!!" not in rendered
        assert "parity" not in rendered
        # The token's line is dropped outright, leaving the blank lines that surrounded it.
        assert rendered == "Before.\n\n\nAfter.\n"


class TestPartial:
    def entry(self) -> Any:
        return capability(
            capability_id="weather-index",
            title="Weather station index",
            typescript="partial",
            differences="First paragraph of what differs.\n\nSecond paragraph of what differs.\n",
        )

    def test_names_the_language_that_differs(self) -> None:
        rendered = page(MACRO_CALL.replace("example", "weather-index") + "\n", entry=self.entry())
        assert rendered.startswith('!!! info "Differs in JavaScript"')

    def test_carries_every_paragraph_of_the_differences(self) -> None:
        rendered = page(MACRO_CALL.replace("example", "weather-index") + "\n", entry=self.entry())
        assert "First paragraph of what differs." in rendered
        assert "Second paragraph of what differs." in rendered

    def test_links_the_capability_anchor(self) -> None:
        rendered = page(MACRO_CALL.replace("example", "weather-index") + "\n", entry=self.entry())
        assert "(../explanation/parity.md#weather-index)" in rendered


class TestNotYet:
    def entry(self) -> Any:
        return capability(
            typescript="absent",
            absence_kind="not-yet",
            issue="https://github.com/idfkit/idfkit-js/issues/12",
        )

    def test_states_the_gap_and_links_the_issue(self) -> None:
        rendered = page(MACRO_CALL + "\n", entry=self.entry())
        assert rendered.startswith('!!! warning "Not in JavaScript yet"')
        assert "[idfkit-js#12](https://github.com/idfkit/idfkit-js/issues/12)" in rendered
        assert "temporary gap" in rendered

    def test_names_the_present_language_too(self) -> None:
        rendered = page(MACRO_CALL + "\n", entry=self.entry())
        assert "available in Python" in rendered

    def test_absent_python_side_reads_the_other_way_round(self) -> None:
        rendered = page(MACRO_CALL + "\n", entry=capability(python="absent", absence_kind="not-yet", issue="ISSUE-1"))
        assert rendered.startswith('!!! warning "Not in Python yet"')
        assert "No tracking issue is open yet" in rendered


class TestNever:
    def entry(self) -> Any:
        return capability(
            typescript="absent",
            absence_kind="never",
            note="Needs a subprocess, which a browser does not have.",
        )

    def test_states_permanence_and_carries_the_note(self) -> None:
        rendered = page(MACRO_CALL + "\n", entry=self.entry())
        assert rendered.startswith('!!! abstract "Python only, permanently"')
        assert "permanent boundary" in rendered
        assert "Needs a subprocess, which a browser does not have." in rendered

    def test_offers_no_issue_link(self) -> None:
        rendered = page(MACRO_CALL + "\n", entry=self.entry())
        assert "tracked in" not in rendered
        assert "issues/" not in rendered
        assert "no issue tracks it" in rendered


class TestUnresolvableId:
    """T126: a typo fails the build rather than rendering an empty block."""

    def test_raises_and_names_page_id_and_near_misses(self) -> None:
        with pytest.raises(PluginError) as raised:
            page(
                '{{ parity("weater-index") }}\n',
                src_uri="weather/downloads.md",
                entry=capability(capability_id="weather-index"),
            )
        message = str(raised.value)
        assert "docs/weather/downloads.md" in message
        assert 'parity("weater-index")' in message
        assert "weather-index" in message

    def test_raises_even_with_no_near_miss(self) -> None:
        with pytest.raises(PluginError):
            page('{{ parity("nothing-like-this-at-all") }}\n', entry=capability())

    def test_raises_against_an_empty_ledger(self) -> None:
        with pytest.raises(PluginError):
            macro.substitute(MACRO_CALL + "\n", "index.md", {})


class TestMalformedToken:
    @pytest.mark.parametrize(
        "line",
        [
            "{{ parity(example) }}",
            '{{ parity("example" }}',
            "{{ parity() }}",
        ],
    )
    def test_a_call_that_does_not_parse_fails_the_build(self, line: str) -> None:
        with pytest.raises(PluginError, match="looks like the parity macro"):
            page(line + "\n", entry=capability())


class TestTokenRecognition:
    @pytest.mark.parametrize(
        "line",
        [
            '{{ parity("example") }}',
            "{{ parity('example') }}",
            '{{parity("example")}}',
            '   {{  parity( "example" )  }}   ',
        ],
    )
    def test_whitespace_and_quote_variants_all_resolve(self, line: str) -> None:
        rendered = page(line + "\n", entry=capability(typescript="absent", absence_kind="not-yet", issue="ISSUE-1"))
        assert rendered.startswith("!!! warning")

    def test_a_token_inside_a_fence_is_left_alone(self) -> None:
        source = f"```markdown\n{MACRO_CALL}\n```\n"
        assert page(source, entry=capability()) == source

    def test_a_token_inside_a_tilde_fence_is_left_alone(self) -> None:
        source = f"~~~\n{MACRO_CALL}\n~~~\n"
        assert page(source, entry=capability()) == source

    def test_a_token_shown_inline_in_code_is_left_alone(self) -> None:
        source = f"Write `{MACRO_CALL}` on its own line.\n"
        assert page(source, entry=capability()) == source


class TestParityPageLink:
    @pytest.mark.parametrize(
        ("src_uri", "expected"),
        [
            ("index.md", "explanation/parity.md"),
            ("how-to/example.md", "../explanation/parity.md"),
            ("api/simulation/runner.md", "../../explanation/parity.md"),
            ("explanation/parity.md", "parity.md"),
        ],
    )
    def test_link_is_relative_to_the_page(self, src_uri: str, expected: str) -> None:
        assert macro.parity_page_link(src_uri) == expected


class TestLedgerIsReadLazily:
    """The ledger is only read for a page that actually declares a capability.

    A docs build of a tree with no conformance checkout still works as long as no page uses the
    macro, and a page that merely writes about the macro does not pull the ledger in.
    """

    @pytest.mark.parametrize(
        "markdown",
        [
            '{{ parity("example") }}\n',
            "  {{parity('example')}}\n",
            "{{ parity(broken \n",
        ],
    )
    def test_a_leading_token_is_worth_reading_the_ledger_for(self, markdown: str) -> None:
        assert macro.declares_a_capability(markdown) is True

    @pytest.mark.parametrize(
        "markdown",
        [
            "The `parity()` macro takes a ledger id.\n",
            'Write `{{ parity("example") }}` on its own line.\n',
            "Nothing here at all.\n",
        ],
    )
    def test_prose_about_the_macro_is_not(self, markdown: str) -> None:
        assert macro.declares_a_capability(markdown) is False
