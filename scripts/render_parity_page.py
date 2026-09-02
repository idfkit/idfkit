"""Render the generated half of ``docs/explanation/parity.md`` from the parity ledger.

The ledger lives in a third repository, ``idfkit/idfkit-conformance``, as
``governance/parity.toml``. It is the single machine-readable record of which public capability each
library has, and it is read at the immutable ``governance-YYYY.N`` tag this release pins in
``[tool.idfkit.governance] level``, never from a moving branch.

Every capability section on the page comes from that file. Nothing between the generated markers is
written by hand, so the page a reader sees and the file the CI gates read cannot disagree. The prose
above the markers explains how to read the page and is not derived from the ledger.

Usage::

    uv run python scripts/render_parity_page.py            # rewrite the generated region
    uv run python scripts/render_parity_page.py --check     # fail if the page is stale

The ledger is located, in order: ``--ledger PATH``, then ``--conformance-dir``, then
``$IDFKIT_CONFORMANCE_DIR``, then a sibling ``idfkit-conformance`` checkout. That is the same
lookup order ``scripts/render_naming_map.py`` uses, so one checkout serves both pages.

This is a maintainer script and is not part of the distributed package, so it needs Python 3.11
or newer for ``tomllib`` even though ``idfkit`` itself supports 3.10.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

import tomllib

# `scripts/` is sys.path[0] when this file is run as a script, but not when it is imported by
# path, which is how docs/hooks/parity_macro.py loads it. Make the sibling import work in both.
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from _governance_source import read_pinned

REPO_ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = REPO_ROOT / "docs" / "explanation" / "parity.md"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"

BEGIN_MARKER = "<!-- BEGIN GENERATED FROM parity.toml. Edit the ledger, not this page. -->"
END_MARKER = "<!-- END GENERATED FROM parity.toml. -->"

LEDGER_REPO = "https://github.com/idfkit/idfkit-conformance"
LEDGER_RELATIVE = Path("governance") / "parity.toml"

STATES = ("complete", "partial", "absent")
ABSENCE_KINDS = ("not-yet", "never")

PYTHON = "Python"
JAVASCRIPT = "JavaScript"


@dataclass(frozen=True)
class TierSection:
    """Presentation metadata for one tier heading.

    The tier keys and their membership come from the ledger. Only the heading wording and the
    one-line gloss live here, because they are page furniture rather than capability data.
    """

    key: str
    anchor: str
    heading: str
    lede: str
    short: str


TIER_SECTIONS: tuple[TierSection, ...] = (
    TierSection(
        key="tier-1",
        anchor="tier-1",
        heading="Tier 1: the shared core",
        short="1",
        lede=(
            "Both libraries carry these, and both are expected to keep carrying them. A difference "
            "you meet inside this tier is either stated below or a bug, and there is no third "
            "possibility."
        ),
    ),
    TierSection(
        key="tier-2",
        anchor="tier-2",
        heading="Tier 2: portable, not ported yet",
        short="2",
        lede=(
            "Capabilities the second language could have and does not have today. Every entry "
            "carries a tracking issue, because recording any of them as permanent would claim more "
            "than the code supports."
        ),
    ),
    TierSection(
        key="tier-3",
        anchor="tier-3",
        heading="Tier 3: tooling and Node-bound capabilities",
        short="3",
        lede=(
            "Absent from JavaScript today and not permanently so. Each one is reachable in Node, "
            "which is why none of them is recorded as permanent."
        ),
    ),
    TierSection(
        key="never",
        anchor="permanently-single-language",
        heading="Permanently single-language",
        short="permanent",
        lede=(
            "Pairs of capabilities that were never one capability. Neither library is missing "
            "anything here, which is why these entries sit apart from the gaps above: each pair is "
            "two different mechanisms serving two different runtimes."
        ),
    ),
)

TIER_BY_KEY = {section.key: section for section in TIER_SECTIONS}
SECTION_ANCHORS = {section.anchor for section in TIER_SECTIONS} | {"at-a-glance"}


@dataclass(frozen=True)
class Capability:
    """One capability as the ledger records it."""

    capability_id: str
    title: str
    tier: str
    python: str
    typescript: str
    names: tuple[str, ...] = ()
    absence_kind: str | None = None
    differences: str | None = None
    issue: str | None = None
    note: str | None = None

    @property
    def has_absence(self) -> bool:
        return "absent" in (self.python, self.typescript)

    @property
    def has_partial(self) -> bool:
        return "partial" in (self.python, self.typescript)

    @property
    def present_language(self) -> str | None:
        """The language that has the capability, when exactly one of them does."""
        if self.python != "absent" and self.typescript == "absent":
            return PYTHON
        if self.typescript != "absent" and self.python == "absent":
            return JAVASCRIPT
        return None

    @property
    def absent_language(self) -> str | None:
        """The language that lacks the capability, when exactly one of them does."""
        if self.python == "absent" and self.typescript != "absent":
            return PYTHON
        if self.typescript == "absent" and self.python != "absent":
            return JAVASCRIPT
        return None


@dataclass
class Ledger:
    """A parsed ledger, together with every way it failed its own contract."""

    capabilities: list[Capability] = field(default_factory=list[Capability])
    problems: list[str] = field(default_factory=list[str])


def _as_str(raw: dict[str, Any], key: str) -> str | None:
    value = raw.get(key)
    return value if isinstance(value, str) else None


def parse_ledger(document: dict[str, Any]) -> Ledger:
    """Turn the decoded TOML into capabilities, collecting every contract violation.

    Violations are collected rather than raised so that one run reports every problem in the
    ledger instead of only the first.
    """
    ledger = Ledger()
    entries: object = document.get("capability")
    if not isinstance(entries, list) or not entries:
        ledger.problems.append("the ledger declares no [[capability]] entries")
        return ledger

    seen: set[str] = set()
    for position, entry in enumerate(cast("list[object]", entries), start=1):
        if not isinstance(entry, dict):
            ledger.problems.append(f"capability {position} is not a table")
            continue
        raw = cast("dict[str, Any]", entry)
        where = _as_str(raw, "id") or f"capability {position}"
        capability = _build_capability(raw, where, ledger.problems)
        if capability is None:
            continue
        if capability.capability_id in seen:
            ledger.problems.append(f"{where}: duplicate id, and ids are the page's anchors")
        seen.add(capability.capability_id)
        if capability.capability_id in SECTION_ANCHORS:
            ledger.problems.append(f"{where}: id collides with a section anchor on the page")
        ledger.capabilities.append(capability)
    return ledger


def _build_capability(raw: dict[str, Any], where: str, problems: list[str]) -> Capability | None:
    capability_id = _as_str(raw, "id")
    title = _as_str(raw, "title")
    tier = _as_str(raw, "tier")
    python = _as_str(raw, "python")
    typescript = _as_str(raw, "typescript")

    missing = [
        name
        for name, value in (
            ("id", capability_id),
            ("title", title),
            ("tier", tier),
            ("python", python),
            ("typescript", typescript),
        )
        if not value
    ]
    if missing:
        problems.append(f"{where}: missing required field(s) {', '.join(missing)}")
        return None
    assert capability_id and title and tier and python and typescript  # noqa: S101

    if tier not in TIER_BY_KEY:
        problems.append(f"{where}: unknown tier {tier!r}, so the page has nowhere to put it")
        return None
    for language, state in ((PYTHON, python), (JAVASCRIPT, typescript)):
        if state not in STATES:
            problems.append(f"{where}: {language} state {state!r} is not one of {', '.join(STATES)}")
            return None

    raw_names: object = raw.get("names")
    names = tuple(str(name) for name in cast("list[object]", raw_names)) if isinstance(raw_names, list) else ()

    capability = Capability(
        capability_id=capability_id,
        title=title,
        tier=tier,
        python=python,
        typescript=typescript,
        names=names,
        absence_kind=_as_str(raw, "absence_kind"),
        differences=_as_str(raw, "differences"),
        issue=_as_str(raw, "issue"),
        note=_as_str(raw, "note"),
    )
    _check_contract(capability, where, problems)
    return capability


def _check_contract(capability: Capability, where: str, problems: list[str]) -> None:
    if capability.has_partial and not (capability.differences or "").strip():
        problems.append(f"{where}: partial with no differences is indistinguishable from complete")
    if not capability.has_absence:
        return
    if capability.absence_kind not in ABSENCE_KINDS:
        problems.append(f"{where}: an absent side needs absence_kind of {' or '.join(ABSENCE_KINDS)}")
        return
    if capability.absence_kind == "not-yet" and not (capability.issue or "").strip():
        problems.append(f"{where}: absence_kind not-yet needs an issue, or the gap is untracked")
    if capability.absence_kind == "never" and not (capability.note or "").strip():
        problems.append(f"{where}: absence_kind never needs a note saying why it is permanent")


def state_label(state: str, absence_kind: str | None) -> str:
    """Render one availability cell, keeping the two kinds of absence apart."""
    if state != "absent":
        return state
    if absence_kind == "never":
        return "absent (never)"
    if absence_kind == "not-yet":
        return "absent (not yet)"
    return "absent (unrecorded)"


def wrap(text: str, width: int = 88) -> str:
    """Hard-wrap generated prose so the page reads the same in an editor as on the site.

    Long words and hyphens are never broken: a Markdown link destination split across two lines
    stops being a link, and every URL on this page is longer than the wrap width.
    """
    lines = textwrap.wrap(
        " ".join(text.split()),
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )
    return "\n".join(lines)


def indent_block(text: str, prefix: str = "    ") -> str:
    """Indent an admonition body, leaving blank lines genuinely blank."""
    lines = text.strip("\n").splitlines()
    return "\n".join(prefix + line if line.strip() else "" for line in lines)


def issue_sentence(issue: str) -> str:
    """Say where the port is tracked, or say plainly that nothing tracks it yet.

    A tracking value that is not a URL is rendered as literal text rather than as a link, because a
    dead link would read as a tracked gap and would pass for one.
    """
    if not issue.startswith(("http://", "https://")):
        return f"No tracking issue is open yet. The ledger records `{issue}`."
    match = re.search(r"github\.com/[^/]+/([^/]+)/issues/(\d+)", issue)
    label = f"{match.group(1)}#{match.group(2)}" if match else issue
    return f"The port is tracked in [{label}]({issue})."


def linkify_ids(text: str, known_ids: set[str]) -> str:
    """Turn a code span naming another ledger id into a link to that capability's anchor.

    Ledger prose points a reader at the partner entry of a split capability, and the partner is on
    this page. Making the pointer clickable is a mechanical transform over text the ledger already
    wrote, not an edit to it.
    """

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        return f"[`{name}`](#{name})" if name in known_ids else match.group(0)

    return re.sub(r"`([A-Za-z0-9][A-Za-z0-9-]*)`", replace, text)


def render_summary_table(capabilities: list[Capability]) -> list[str]:
    lines = [
        "| Capability | Tier | Python | JavaScript |",
        "| ---------- | ---- | ------ | ---------- |",
    ]
    for capability in capabilities:
        tier = TIER_BY_KEY[capability.tier]
        lines.append(
            f"| [{capability.title}](#{capability.capability_id}) "
            f"| {tier.short} "
            f"| {state_label(capability.python, capability.absence_kind)} "
            f"| {state_label(capability.typescript, capability.absence_kind)} |"
        )
    return lines


def render_counts_table(capabilities: list[Capability]) -> list[str]:
    rows = ("complete", "partial", "absent, not yet", "absent, never")
    tally = {row: {PYTHON: 0, JAVASCRIPT: 0} for row in rows}
    for capability in capabilities:
        for language, state in ((PYTHON, capability.python), (JAVASCRIPT, capability.typescript)):
            if state != "absent":
                tally[state][language] += 1
            elif capability.absence_kind == "never":
                tally["absent, never"][language] += 1
            else:
                tally["absent, not yet"][language] += 1
    lines = [
        "| Availability | Python | JavaScript |",
        "| ------------ | ------ | ---------- |",
    ]
    lines.extend(f"| {row} | {tally[row][PYTHON]} | {tally[row][JAVASCRIPT]} |" for row in rows)
    return lines


def render_capability(capability: Capability, known_ids: set[str]) -> list[str]:
    tier = TIER_BY_KEY[capability.tier]
    tier_text = "Permanently single-language" if tier.key == "never" else f"Tier {tier.short}"
    lines = [
        f"### {capability.title} {{ #{capability.capability_id} }}",
        "",
        f"**Python** {state_label(capability.python, capability.absence_kind)}"
        f" &middot; **JavaScript** {state_label(capability.typescript, capability.absence_kind)}"
        f" &middot; {tier_text}"
        f" &middot; ledger id `{capability.capability_id}`",
        "",
    ]

    if capability.has_partial and capability.differences:
        body = linkify_ids(capability.differences, known_ids)
        lines += ['!!! info "What differs, and why"', "", indent_block(body), ""]

    if capability.has_absence:
        lines += render_absence(capability, known_ids)

    if capability.names:
        lines += ['??? note "Vocabulary this capability owns in the naming register"', ""]
        lines += [indent_block("\n".join(f"- {name}" for name in capability.names)), ""]

    return lines


def render_absence(capability: Capability, known_ids: set[str]) -> list[str]:
    absent = capability.absent_language
    present = capability.present_language

    if capability.absence_kind == "never":
        title = "Permanently absent" if present is None else f"{present} only, permanently"
        body = linkify_ids(capability.note or "", known_ids)
        return [f'!!! abstract "{title}"', "", indent_block(body), ""]

    title = f"Not in {absent} yet" if absent else "Not implemented yet"
    body = f"A temporary gap, not a boundary. {issue_sentence(capability.issue or '')}"
    return [f'!!! warning "{title}"', "", indent_block(wrap(body)), ""]


def render(capabilities: list[Capability], level: str) -> str:
    """Render everything that sits between the generated markers."""
    source_url = f"{LEDGER_REPO}/blob/{level}/governance/parity.toml"
    known_ids = {capability.capability_id for capability in capabilities}
    provenance = (
        f"Generated from [`governance/parity.toml`]({source_url}) at `{level}`, the governance tag "
        "this release pins. Correct the ledger and regenerate; a correction made on this page would "
        "be overwritten, and it would never reach either library's CI gate."
    )
    count = len(capabilities)
    lead_in = (
        f"{count} {'capability' if count == 1 else 'capabilities'}, counted by availability and then "
        "listed in full. Follow a capability to read what differs where the two libraries differ, "
        "and whether an absence is temporary or permanent."
    )
    lines = [wrap(provenance), "", "## Every capability at a glance { #at-a-glance }", "", wrap(lead_in), ""]
    lines += render_counts_table(capabilities)
    lines += ["", *render_summary_table(capabilities), ""]

    for tier in TIER_SECTIONS:
        members = [capability for capability in capabilities if capability.tier == tier.key]
        if not members:
            continue
        lines += [f"## {tier.heading} {{ #{tier.anchor} }}", "", wrap(tier.lede), ""]
        for capability in members:
            lines += render_capability(capability, known_ids)

    return "\n".join(lines).rstrip() + "\n"


def splice(page: str, body: str) -> str:
    """Replace the generated region of the page, leaving the hand-written prose alone."""
    begin = page.find(BEGIN_MARKER)
    end = page.find(END_MARKER)
    if begin == -1 or end == -1 or end < begin:
        sys.exit(f"{PAGE_PATH}: the generated markers are missing or out of order")
    head = page[: begin + len(BEGIN_MARKER)]
    tail = page[end:]
    return f"{head}\n\n{body}\n{tail}"


def resolve_ledger_path(explicit: Path | None, conformance_dir: Path | None) -> Path:
    """Find the ledger, using the same lookup order as ``scripts/render_naming_map.py``."""
    if explicit is not None:
        return explicit
    roots = [conformance_dir] if conformance_dir else []
    if not roots:
        from_env = os.environ.get("IDFKIT_CONFORMANCE_DIR")
        if from_env:
            roots.append(Path(from_env).expanduser())
    roots.append(REPO_ROOT.parent / "idfkit-conformance")
    for root in roots:
        candidate = root / LEDGER_RELATIVE
        if candidate.is_file():
            return candidate
    tried = ", ".join(str(root / LEDGER_RELATIVE) for root in roots)
    sys.exit(f"No parity ledger found. Tried: {tried}. Pass --ledger PATH or set IDFKIT_CONFORMANCE_DIR.")


def resolve_level() -> str:
    from_env = os.environ.get("IDFKIT_GOVERNANCE_LEVEL")
    if from_env:
        return from_env
    if PYPROJECT_PATH.is_file():
        with PYPROJECT_PATH.open("rb") as handle:
            pyproject = tomllib.load(handle)
        level = pyproject.get("tool", {}).get("idfkit", {}).get("governance", {}).get("level")
        if isinstance(level, str) and level:
            return level
    sys.exit("no governance level declared: set [tool.idfkit.governance] level or IDFKIT_GOVERNANCE_LEVEL")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ledger", type=Path, default=None, help="Path to governance/parity.toml.")
    parser.add_argument(
        "--conformance-dir",
        type=Path,
        default=None,
        help="Root of an idfkit-conformance checkout. Defaults to a sibling of this repository.",
    )
    parser.add_argument("--check", action="store_true", help="Fail if the page on disk is not what this would write.")
    args = parser.parse_args(argv)

    ledger_path = resolve_ledger_path(args.ledger, args.conformance_dir)
    if not ledger_path.is_file():
        sys.exit(f"parity ledger not found at {ledger_path}")

    level = resolve_level()
    source = read_pinned(ledger_path, level, override=args.ledger is not None)
    if not source.pinned:
        print(f"note: reading {source.description}", file=sys.stderr)
    ledger = parse_ledger(tomllib.loads(source.text))
    if ledger.problems:
        print(f"{source.description}: the ledger does not satisfy its own contract")
        for problem in ledger.problems:
            print(f"  - {problem}")
        return 2

    body = render(ledger.capabilities, level)
    current = PAGE_PATH.read_text(encoding="utf-8")
    updated = splice(current, body)

    if args.check:
        if updated != current:
            print(f"{PAGE_PATH} is stale. Run: uv run python scripts/render_parity_page.py")
            return 1
        print(f"{PAGE_PATH} is up to date with {source.description} ({len(ledger.capabilities)} capabilities)")
        return 0

    if updated != current:
        PAGE_PATH.write_text(updated, encoding="utf-8")
        print(f"rewrote {PAGE_PATH} from {ledger_path} ({len(ledger.capabilities)} capabilities)")
    else:
        print(f"{PAGE_PATH} already matches {ledger_path} ({len(ledger.capabilities)} capabilities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
