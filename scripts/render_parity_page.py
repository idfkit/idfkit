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

WHERE THE LEDGER MODEL LIVES, AND WHY IT IS NOT HERE

The dataclasses, the contract checks, the lookup and the shared wording are in
``docs/hooks/parity_ledger.py``, and this script imports them from there. The direction is
deliberate. ``docs/hooks/parity_macro.py`` needs the same model to resolve ``{{ parity("id") }}``
on a page, and it must keep working when the documentation tree is copied somewhere this
repository's ``scripts/`` is not (research R7, ``.github/workflows/docs.yml``). So the model sits
inside the tree that has to travel, and this script, which only ever runs from the repository,
reaches into it. It used to be the other way round, and the copied tree could not build.

This is a maintainer script and is not part of the distributed package, so it needs Python 3.11
or newer for ``tomllib`` even though ``idfkit`` itself supports 3.10.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import tomllib

# `scripts/` is sys.path[0] when this file is run as a script and not when it is imported some
# other way, and `docs/hooks/` is never on the path at all. Put both there so the two imports
# below resolve however this file is loaded. Nothing but these two path edits may sit between the
# imports above and the imports below.
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
if str(Path(__file__).resolve().parents[1] / "docs" / "hooks") not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "docs" / "hooks"))

from _governance_source import read_pinned
from parity_ledger import (
    JAVASCRIPT,
    PYTHON,
    TIER_BY_KEY,
    TIER_SECTIONS,
    Capability,
    indent_block,
    issue_sentence,
    linkify_ids,
    parse_ledger,
    resolve_ledger_path,
    resolve_level,
    state_label,
    wrap,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = REPO_ROOT / "docs" / "explanation" / "parity.md"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"

BEGIN_MARKER = "<!-- BEGIN GENERATED FROM parity.toml. Edit the ledger, not this page. -->"
END_MARKER = "<!-- END GENERATED FROM parity.toml. -->"

LEDGER_REPO = "https://github.com/idfkit/idfkit-conformance"


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

    # Both resolvers are told what this script knows and a copied documentation tree does not: the
    # repository root, so the sibling checkout and the governance pin are found from there rather
    # than from wherever the script happens to have been invoked.
    ledger_path = resolve_ledger_path(args.ledger, args.conformance_dir, sibling_of=REPO_ROOT)
    if not ledger_path.is_file():
        sys.exit(f"parity ledger not found at {ledger_path}")

    level = resolve_level(PYPROJECT_PATH)
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
