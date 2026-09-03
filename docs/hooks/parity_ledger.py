"""The parity ledger: how it is found, how it is parsed, and how its prose is rendered.

This module is the one definition of the ledger. Two things read it:

* ``docs/hooks/parity_macro.py``, the ``{{ parity("id") }}`` hook every page can use;
* ``scripts/render_parity_page.py``, which regenerates ``docs/explanation/parity.md``.

WHY IT LIVES UNDER ``docs/hooks/`` AND NOT UNDER ``scripts/``

It used to live in the render script, and the hook imported it by an absolute path computed from
its own location, two directories up and out of the documentation tree. That made ``docs/`` a tree
that cannot be copied: the hook ``mkdocs.yml`` lists crashed with ``FileNotFoundError`` anywhere the
repository's ``scripts/`` was not sitting next to it, which is every place the site will be built
after the documentation moves to its own repository (research R7).

The dependency now points the other way. The documentation tree carries what the documentation build
needs, and the maintainer script reaches down into the documentation tree for it, because that script
runs from the repository and the repository is where both halves are. Nothing here computes a path
out of its own directory, and ``.github/workflows/docs.yml`` fails the build if anything under
``docs/`` starts doing so again.

WHAT IS NOT HERE

The page layout is not: headings, tables, the generated-region markers and the splice belong to
``scripts/render_parity_page.py``, which is the only thing that writes a page. What is here is what
both readers must agree on, because a second definition of any of it is a way for the generated page
and the in-page notices to say different things about the same capability.

Like the render scripts and the hook, this is maintainer-side and build-side tooling. It is not part
of the distributed package, so it needs Python 3.11 or newer for ``tomllib`` even though ``idfkit``
itself supports 3.10.
"""

from __future__ import annotations

import os
import re
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

import tomllib

# The ledger's path inside idfkit/idfkit-conformance. One definition: the lookup below joins it, and
# `ledger_repo_root` strips it back off.
LEDGER_RELATIVE = Path("governance") / "parity.toml"

STATES = ("complete", "partial", "absent")
ABSENCE_KINDS = ("not-yet", "never")

PYTHON = "Python"
JAVASCRIPT = "JavaScript"


# ---------------------------------------------------------------------------
# Finding the ledger, and the tag to read it at
# ---------------------------------------------------------------------------


def project_pyproject() -> Path:
    """Where a build that runs from the repository finds the governance pin.

    MkDocs runs from the directory holding ``mkdocs.yml``, which in this repository is the repository
    root. A documentation tree copied out of the repository has no ``pyproject.toml`` there and none
    anywhere else, which is exactly the case ``resolve_level`` treats as "not pinned here": it falls
    to ``$IDFKIT_GOVERNANCE_LEVEL`` rather than failing on the missing path.
    """
    return Path.cwd() / "pyproject.toml"


def resolve_level(pyproject: Path | None = None) -> str:
    """The governance tag to read the ledger at, or an exit that says how to declare one.

    In order: ``$IDFKIT_GOVERNANCE_LEVEL``, then ``[tool.idfkit.governance] level`` in *pyproject*.

    *pyproject* may be ``None``, and it may name a file that does not exist. Both mean the same
    thing and both are ordinary: a documentation tree that has been copied out of the repository
    carries no ``pyproject.toml``, and there the environment variable is the only source. That is
    not a degraded mode. The portable build passes the level down from the same pin the repository
    declares, so the pinned tag still governs what the site says; what changes is only where the
    build reads the pin from.

    There is no default tag and there must not be one. A build that guessed a governance level would
    render parity claims that nothing in this release pins.
    """
    from_env = os.environ.get("IDFKIT_GOVERNANCE_LEVEL")
    if from_env:
        return from_env
    if pyproject is not None and pyproject.is_file():
        with pyproject.open("rb") as handle:
            document = tomllib.load(handle)
        level = document.get("tool", {}).get("idfkit", {}).get("governance", {}).get("level")
        if isinstance(level, str) and level:
            return level
    where = f" in {pyproject}" if pyproject is not None else ""
    sys.exit(
        f"no governance level declared: set [tool.idfkit.governance] level{where}, or set "
        "IDFKIT_GOVERNANCE_LEVEL. A documentation tree copied out of the repository has no "
        "pyproject.toml, and the environment variable is how the pinned tag reaches it."
    )


def resolve_ledger_path(
    explicit: Path | None = None,
    conformance_dir: Path | None = None,
    *,
    sibling_of: Path | None = None,
) -> Path:
    """Find the ledger, using the same lookup order as ``scripts/render_naming_map.py``.

    In order: *explicit*, then *conformance_dir*, then ``$IDFKIT_CONFORMANCE_DIR``, then a checkout
    named ``idfkit-conformance`` sitting next to *sibling_of*, which defaults to the directory the
    build is running from. A build inside the repository is run from the repository root, so that
    default is the repository's own sibling; a build somewhere else has no repository to be a sibling
    of, and there the environment variable is the way in.

    The file this returns locates the repository. The text is then read at the pinned tag, never from
    the working tree, by ``scripts/_governance_source.read_pinned`` or by the hook's own ``git show``.
    """
    if explicit is not None:
        return explicit
    roots = [conformance_dir] if conformance_dir else []
    if not roots:
        from_env = os.environ.get("IDFKIT_CONFORMANCE_DIR")
        if from_env:
            roots.append(Path(from_env).expanduser())
    roots.append((sibling_of or Path.cwd()).resolve().parent / "idfkit-conformance")
    for root in roots:
        candidate = root / LEDGER_RELATIVE
        if candidate.is_file():
            return candidate
    tried = ", ".join(str(root / LEDGER_RELATIVE) for root in roots)
    sys.exit(f"No parity ledger found. Tried: {tried}. Pass --ledger PATH or set IDFKIT_CONFORMANCE_DIR.")


def ledger_repo_root(ledger_path: Path) -> Path:
    """The repository a resolved ledger path sits in.

    Strips ``LEDGER_RELATIVE`` rather than counting directories, so this stays correct if the ledger
    ever moves inside its own repository.
    """
    root = ledger_path
    for _ in LEDGER_RELATIVE.parts:
        root = root.parent
    return root


# ---------------------------------------------------------------------------
# The tiers the page is organised into
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# The ledger itself
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Wording, shared by the generated page and the in-page notices
# ---------------------------------------------------------------------------


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
    the parity page. Making the pointer clickable is a mechanical transform over text the ledger
    already wrote, not an edit to it.

    The link is a bare fragment, which is what the parity page itself needs. A page that is not the
    parity page has to put the path to it in front of the fragment, and ``docs/hooks/parity_macro.py``
    has its own variant that does exactly that.
    """

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        return f"[`{name}`](#{name})" if name in known_ids else match.group(0)

    return re.sub(r"`([A-Za-z0-9][A-Za-z0-9-]*)`", replace, text)
