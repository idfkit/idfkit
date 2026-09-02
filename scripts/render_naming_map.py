"""Render the generated half of ``docs/explanation/naming-map.md`` from the naming register.

The register lives in a third repository, ``idfkit/idfkit-conformance``, as
``governance/naming.toml``. It is the single machine-readable record of every concept the two
libraries share and of every accepted difference between them, and it is read at the immutable
``governance-YYYY.N`` tag this release pins in ``[tool.idfkit.governance] level``, never from a
moving branch.

Every name, every divergence reason, every note, and every section heading below the generated
marker comes from that file, so the page a reader sees and the file both libraries' naming gates
read cannot disagree. The prose above the markers explains why the register exists and how to read
the page; it names no identifier, because prose that spells a name out is prose that can contradict
the register.

Two kinds of check keep the generated half honest beyond the plain transcription:

* the concepts in ``ILLUSTRATIONS`` are looked up before anything is written, so a rule stated in
  script-held prose cannot outlive the entry it illustrates;
* ``OFF_MAP_PACKAGES`` must stay off the register, because the hand-written half tells the reader
  they are off the map.

Usage::

    uv run python scripts/render_naming_map.py            # rewrite the generated region
    uv run python scripts/render_naming_map.py --check     # fail if the page is stale

The register is located, in order: ``--register PATH``, then ``$IDFKIT_GOVERNANCE_DIR/naming.toml``,
then a sibling ``idfkit-conformance`` checkout next to this repository.
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
PAGE_PATH = REPO_ROOT / "docs" / "explanation" / "naming-map.md"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"

BEGIN_MARKER = "<!-- BEGIN GENERATED FROM naming.toml. Edit the register, not this page. -->"
END_MARKER = "<!-- END GENERATED FROM naming.toml. -->"

REGISTER_REPO = "https://github.com/idfkit/idfkit-conformance"

KINDS = ("aligned", "divergent", "excluded")

# Concepts the script-held prose points at. A lookup that misses stops the render, because prose
# naming a concept the register no longer carries is the disagreement this page exists to prevent.
ILLUSTRATIONS = (
    "acronym casing",
    "the document class",
    "set the window to wall ratio",
    "a construction's solar heat gain coefficient",
    "version",
)

# Two JavaScript-only packages the register deliberately does not carry, and which the hand-written
# half of the page describes as off the map. Checked rather than assumed.
OFF_MAP_PACKAGES = ("@idfkit/engine", "@idfkit/viewer")


@dataclass(frozen=True)
class RenameCount:
    """How many times each spelling of one concept has been changed during the unification."""

    python: int = 0
    typescript: int = 0


@dataclass(frozen=True)
class Entry:
    """One register entry: a concept, and how each language spells it."""

    concept: str
    python: str
    typescript: str
    kind: str
    group: str
    divergence_reason: str = ""
    canonical_form: str = ""
    notes: str = ""
    renames: RenameCount = RenameCount()

    @property
    def python_names(self) -> tuple[str, ...]:
        return split_names(self.python)

    @property
    def typescript_names(self) -> tuple[str, ...]:
        return split_names(self.typescript)

    @property
    def has_detail(self) -> bool:
        """Whether the page gives this entry a section of its own, and therefore an anchor."""
        return self.kind in ("divergent", "excluded")


@dataclass(frozen=True)
class ReservedPackage:
    """A package name held before the port that will carry it begins."""

    capability: str
    npm_package: str
    subpath: str
    mirrors: tuple[str, ...]
    tier: int
    built: bool


@dataclass
class Register:
    """A parsed register, together with every way it failed its own contract."""

    schema_version: str = ""
    governs: tuple[str, ...] = ()
    read_at: str = ""
    review: str = ""
    gate_exit_zero: str = ""
    gate_failures: tuple[str, ...] = ()
    verbs: tuple[str, ...] = ()
    meanings: tuple[tuple[str, str], ...] = ()
    entries: list[Entry] = field(default_factory=list)
    reserved: list[ReservedPackage] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    def by_concept(self, concept: str) -> Entry | None:
        return next((entry for entry in self.entries if entry.concept == concept), None)

    def of_kind(self, kind: str) -> list[Entry]:
        return [entry for entry in self.entries if entry.kind == kind]

    @property
    def groups(self) -> list[str]:
        seen: list[str] = []
        for entry in self.entries:
            if entry.group not in seen:
                seen.append(entry.group)
        return seen


# ---------------------------------------------------------------------------
# Reading the register
# ---------------------------------------------------------------------------

GROUP_RE = re.compile(r"^#\s+Entries:\s+(?P<title>.+?)\s*$")


def entry_groups(raw: str) -> list[str]:
    """Return the group heading in force at each ``[[entry]]``, in document order.

    The groups are TOML comments, so they never reach ``tomllib``. Reading them from the raw text
    keeps the page's sections in step with the register's own organisation, rather than inventing a
    second one here that has to be maintained by hand.
    """
    groups: list[str] = []
    current = "entries"
    for line in raw.splitlines():
        match = GROUP_RE.match(line)
        if match is not None:
            current = match.group("title")
            continue
        if line.strip() == "[[entry]]":
            groups.append(current)
    return groups


def as_str(raw: dict[str, Any], key: str) -> str | None:
    value = raw.get(key)
    return value if isinstance(value, str) else None


def rename_count(raw: dict[str, Any], where: str, problems: list[str]) -> RenameCount:
    counts = raw.get("rename_count")
    if not isinstance(counts, dict):
        problems.append(f"{where}: no rename_count, so the one-rename budget cannot be shown")
        return RenameCount()
    table = cast("dict[str, Any]", counts)
    python = table.get("python", 0)
    typescript = table.get("typescript", 0)
    if not isinstance(python, int) or not isinstance(typescript, int):
        problems.append(f"{where}: rename_count is not a pair of integers")
        return RenameCount()
    return RenameCount(python=python, typescript=typescript)


def build_entry(raw: dict[str, Any], group: str, position: int, problems: list[str]) -> Entry | None:
    concept = as_str(raw, "concept")
    where = concept or f"entry {position}"
    kind = as_str(raw, "kind")
    python = as_str(raw, "python")
    typescript = as_str(raw, "typescript")

    missing = [
        name
        for name, value in (("concept", concept), ("kind", kind), ("python", python), ("typescript", typescript))
        if value is None
    ]
    if missing or concept is None or kind is None or python is None or typescript is None:
        problems.append(f"{where}: missing required field(s) {', '.join(missing)}")
        return None
    if kind not in KINDS:
        problems.append(f"{where}: unknown kind {kind!r}, so the page has nowhere to put it")
        return None

    reason = as_str(raw, "divergence_reason") or ""
    if kind in ("divergent", "excluded") and not reason:
        problems.append(f"{where}: {kind} with no divergence_reason, and an unexplained difference reads as a defect")
    if kind == "aligned" and (not python or not typescript):
        problems.append(f"{where}: aligned but absent in one language")

    return Entry(
        concept=concept,
        python=python,
        typescript=typescript,
        kind=kind,
        group=group,
        divergence_reason=reason,
        canonical_form=as_str(raw, "canonical_form") or "",
        notes=as_str(raw, "notes") or "",
        renames=rename_count(raw, where, problems),
    )


def parse_register(document: dict[str, Any], raw_text: str) -> Register:
    """Turn the decoded TOML into the shape the page renders from, collecting every violation.

    Violations are collected rather than raised so that one run reports everything wrong with the
    register instead of only the first thing.
    """
    register = Register()
    read_header(document, register)
    read_gate(document, register)
    read_vocabulary(document, register)
    read_entries(document, raw_text, register)
    read_reserved(document, register)
    check_page_claims(register)
    return register


def as_str_tuple(value: object) -> tuple[str, ...]:
    return tuple(str(item) for item in cast("list[object]", value)) if isinstance(value, list) else ()


def read_header(document: dict[str, Any], register: Register) -> None:
    header = document.get("register")
    if not isinstance(header, dict):
        register.problems.append("the register declares no [register] table")
        return
    table = cast("dict[str, Any]", header)
    register.schema_version = as_str(table, "schema_version") or ""
    register.governs = as_str_tuple(table.get("governs"))
    register.read_at = as_str(table, "read_at") or ""
    register.review = as_str(table, "review") or ""


def read_gate(document: dict[str, Any], register: Register) -> None:
    gate = document.get("gate")
    if not isinstance(gate, dict):
        return
    table = cast("dict[str, Any]", gate)
    register.gate_exit_zero = as_str(table, "exit_zero") or ""
    register.gate_failures = as_str_tuple(table.get("failures"))


def read_vocabulary(document: dict[str, Any], register: Register) -> None:
    vocabulary = document.get("vocabulary")
    if not isinstance(vocabulary, dict):
        register.problems.append("the register declares no [vocabulary] table")
        return
    table = cast("dict[str, Any]", vocabulary)
    register.verbs = as_str_tuple(table.get("verbs"))
    meaning = table.get("meaning")
    meanings = cast("dict[str, Any]", meaning) if isinstance(meaning, dict) else {}
    register.meanings = tuple((verb, str(meanings[verb])) for verb in register.verbs if verb in meanings)
    missing = [verb for verb in register.verbs if verb not in meanings]
    if missing:
        register.problems.append(f"the verb vocabulary defines no meaning for {', '.join(missing)}")


def read_entries(document: dict[str, Any], raw_text: str, register: Register) -> None:
    raw_entries = document.get("entry")
    if not isinstance(raw_entries, list) or not raw_entries:
        register.problems.append("the register declares no [[entry]] tables")
        return
    entries = cast("list[object]", raw_entries)

    groups = entry_groups(raw_text)
    if len(groups) != len(entries):
        register.problems.append(f"found {len(groups)} '[[entry]]' lines for {len(entries)} parsed entries")
        return

    seen: set[str] = set()
    for position, (item, group) in enumerate(zip(entries, groups, strict=True), start=1):
        if not isinstance(item, dict):
            register.problems.append(f"entry {position} is not a table")
            continue
        entry = build_entry(cast("dict[str, Any]", item), group, position, register.problems)
        if entry is None:
            continue
        if entry.concept in seen:
            register.problems.append(f"{entry.concept}: duplicate concept, and concepts are the page's anchors")
        seen.add(entry.concept)
        register.entries.append(entry)


def read_reserved(document: dict[str, Any], register: Register) -> None:
    raw_reserved = document.get("reserved_package")
    if not isinstance(raw_reserved, list):
        return
    for item in cast("list[object]", raw_reserved):
        if not isinstance(item, dict):
            continue
        table = cast("dict[str, Any]", item)
        register.reserved.append(
            ReservedPackage(
                capability=as_str(table, "capability") or "",
                npm_package=as_str(table, "npm_package") or "",
                subpath=as_str(table, "subpath") or "",
                mirrors=as_str_tuple(table.get("mirrors")),
                tier=int(table.get("tier", 0)),
                built=bool(table.get("built", False)),
            )
        )


def check_page_claims(register: Register) -> None:
    """Verify the two claims the page's script-held and hand-written prose make about the register."""
    for concept in ILLUSTRATIONS:
        if register.by_concept(concept) is None:
            register.problems.append(
                f"the page's prose illustrates a rule with the concept {concept!r}, which the register no longer "
                f"carries; update scripts/render_naming_map.py before regenerating"
            )
    registered = {entry.typescript for entry in register.entries}
    registered |= {package.npm_package for package in register.reserved}
    for package in OFF_MAP_PACKAGES:
        if package in registered:
            register.problems.append(
                f"the register now carries {package}, which the page describes as off the map; update the prose "
                f"in docs/explanation/naming-map.md before regenerating"
            )


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------


def split_names(value: str) -> tuple[str, ...]:
    """Split a register name field, which holds a whole surface as a comma-separated list."""
    return tuple(part.strip() for part in value.split(",") if part.strip())


def wrap(text: str, width: int = 88) -> str:
    """Hard-wrap generated prose so the page reads the same in an editor as on the site.

    Long words and hyphens are never broken: a Markdown link destination split across two lines
    stops being a link, and an identifier split across two lines stops being an identifier.
    """
    lines = textwrap.wrap(
        " ".join(text.split()),
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )
    return "\n".join(lines)


def wrap_prose(text: str) -> list[str]:
    """Wrap register prose, keeping the paragraph breaks it carries."""
    lines: list[str] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        if not block.strip():
            continue
        lines += [wrap(block), ""]
    return lines


def bullet_item(text: str) -> str:
    """Wrap one list item, indenting the continuation lines so the bullet stays readable."""
    return textwrap.fill(
        " ".join(text.split()),
        width=88,
        initial_indent="- ",
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )


def name_or_withdrawn(name: str) -> str:
    """Render a name, or say plainly that the concept no longer has one in that language."""
    return f"`{cell(name)}`" if name else "*withdrawn*"


def slug(text: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", cleaned).strip("-")


def cell(value: str) -> str:
    return value.replace("|", r"\|")


def sentence_case(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


FR_GROUP_RE = re.compile(r"\s*\(FR-\d+(?:,\s*FR-\d+)*\)")
FR_TRAILING_RE = re.compile(r",\s*FR-\d+(?:,\s*FR-\d+)*")


def without_requirement_ids(text: str) -> str:
    """Drop the spec requirement ids the register cites in its own headings and gate messages.

    They are how the register talks to its contributors. A reader looking for a name has no way to
    resolve FR-007, so a heading that carries it spends the reader's attention on nothing.
    """
    return FR_TRAILING_RE.sub("", FR_GROUP_RE.sub("", text)).strip()


def name_cell(entry: Entry, names: tuple[str, ...]) -> str:
    """Render one name column, sending a whole excluded surface to its own section."""
    if not names:
        return "*absent*"
    if len(names) > 1:
        target = f"#{slug(entry.concept)}" if entry.has_detail else ""
        label = f"{len(names)} names"
        return f"[{label}]({target})" if target else label
    return f"`{cell(names[0])}`"


def kind_cell(entry: Entry) -> str:
    if not entry.has_detail:
        return entry.kind
    return f"[{entry.kind}](#{slug(entry.concept)})"


# ---------------------------------------------------------------------------
# Script-held prose
#
# Framing that belongs to the generated region because it states a rule the register decides. Each
# placeholder is filled from the register itself, so the illustration cannot drift from the file.
# ---------------------------------------------------------------------------

GUESSING = (
    "Most counterparts are derivable, and the quickest way to use this page is to guess first and confirm second."
)

GUESSING_RULES = (
    (
        "Convert the casing.",
        "Python spells a member in snake_case and JavaScript spells it in camelCase. Converting one "
        "to the other mechanically gives the right name for the large majority of the register: "
        "`{casing_python}` becomes `{casing_typescript}`, with nothing else changed.",
    ),
    (
        "Expect acronyms to differ in type names.",
        "`{acronym_python}` in Python is `{acronym_typescript}` in TypeScript, and the same split "
        "runs through every type built on the abbreviation, so the document class is "
        "`{document_python}` against `{document_typescript}`. PEP 8 capitalises a whole acronym "
        "inside a CapWords name; the Google TypeScript style guide treats an abbreviation as an "
        "ordinary word. Each is right where it lives, and neither is a candidate for renaming to "
        "match the other.",
    ),
    (
        "Expect an abbreviation inside a camelCase name to become one word.",
        "The rule that gives `{acronym_typescript}` also gives `{abbrev_one_typescript}` for "
        "Python's `{abbrev_one_python}`, and `{abbrev_two_typescript}` for `{abbrev_two_python}`.",
    ),
    (
        "Read the verb first.",
        "One operation carries one verb in both languages, so the verb tells you what a call does "
        "to your disk before you have read the rest of the name.",
    ),
)

GUESSING_CLOSE = (
    "Where the guess fails it fails in one of the ways listed under "
    "[where the two libraries differ](#where-the-two-libraries-differ-and-why), and each of those "
    "is a difference with a reason rather than an oversight. A guess that appears neither in the "
    "map nor in that list does not exist: the gate fails on any public name the register cannot "
    "resolve, which is what makes the map complete rather than merely long."
)

VOCABULARY_LEAD = (
    "These verbs are fixed. A capability that needs one of these operations spells it with the verb "
    "below, in the casing of its own ecosystem, and a capability that does something else does not "
    "borrow one of them."
)

VOCABULARY_CLOSE = (
    "The pair worth the most attention is `write` against `save`. Both libraries draw the line in "
    "the same place: `write` hands you text and never touches your disk, `save` puts it on disk. "
    "`parse` against `load` is the same line drawn on the way in."
)

MAP_LEAD = (
    "The map follows the register's own order, which groups related operations together. A row "
    "marked divergent or excluded links to the entry that says why, and a cell reading *absent* "
    "means the operation genuinely has no counterpart in that language."
)

NOTES_LEAD = (
    "Some names carry a note the tables cannot hold. Notes are grouped here, so a note that applies "
    'to many names is stated once. "Registered before it is written" means exactly that: the name '
    "is decided and reserved, and the implementation follows it rather than the other way round."
)

DIVERGENCE_LEAD = (
    "Each difference below stays. None is a defect and none is a candidate for a future rename: "
    "forcing either spelling onto the other language makes it wrong there, and wrong in a way that "
    "language's readers would feel on every line."
)

CANONICAL_LEAD = (
    "A divergence in a name costs you a lookup. A divergence in a value costs you a bug, because "
    "the code reads the same in both languages and behaves differently. Where the two libraries "
    "hold one thing in two shapes, the register names the text form both sides render, and the "
    "conformance corpus asserts that they render it identically for the same model."
)

CANONICAL_CLOSE = (
    "The rule to carry away: keep each language's idiomatic shape in memory, and move the canonical "
    "form across the boundary. Anything written to a file, sent in a message, or compared in a test "
    "fixture is crossing the boundary."
)

EXCLUDED_LEAD = (
    'Excluded does not mean "not yet". It is terminal: a counterpart appearing in the other '
    "language fails the gate, and adding one takes an amendment to the register reviewed by both "
    "languages. These surfaces are excluded because their names are quotations rather than "
    "choices. They reproduce another ecosystem's spelling, or they name a mechanism the other "
    "runtime does not have."
)

SPENT_LEAD = (
    "Every name gets one rename during the unification. One. A name that has spent it is frozen: "
    "the gate blocks the change that would take it to a second, and unblocking it takes an "
    "amendment saying why the first rename was wrong. A user absorbs one rename with a changelog "
    "entry and a search-and-replace, and absorbs a second by concluding the library is unstable."
)

SPENT_CLOSE = (
    "A withdrawal counts as a rename. It is at least as breaking, and it must not happen twice to one name either."
)

RESERVED_LEAD = (
    "No package below is built yet, and the shared install map gains no entry for any of them: an "
    "entry that resolves to nothing breaks a clean install, which is worse than an unreserved name. "
    "The reservation exists because an npm package name cannot be corrected after publication, and "
    "a name chosen at the moment its port begins is a name chosen by one language under schedule "
    "pressure."
)

GATE_LEAD = "The gate that reads the register refuses a pull request when:"

GATE_CLOSE = (
    "Names that were never meant to be public are not registered to keep the gate quiet. They are "
    "deleted. A public surface that leaks an import or an assembly artefact fails outright, and "
    "adding an entry for one is the wrong fix."
)


def illustrations(register: Register) -> dict[str, str]:
    """Fill the placeholders in the script-held prose from the register."""
    acronym = register.by_concept("acronym casing")
    document = register.by_concept("the document class")
    wwr = register.by_concept("set the window to wall ratio")
    shgc = register.by_concept("a construction's solar heat gain coefficient")
    casing = casing_pair(register)
    if acronym is None or document is None or wwr is None or shgc is None or casing is None:
        sys.exit("the register no longer carries the concepts the page's prose illustrates")
    return {
        "acronym_python": acronym.python,
        "acronym_typescript": acronym.typescript,
        "document_python": document.python,
        "document_typescript": document.typescript,
        "abbrev_one_python": wwr.python,
        "abbrev_one_typescript": wwr.typescript,
        "abbrev_two_python": shgc.python,
        "abbrev_two_typescript": shgc.typescript,
        "casing_python": casing.python,
        "casing_typescript": casing.typescript,
    }


def camel(snake: str) -> str:
    head, *rest = snake.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in rest)


def casing_pair(register: Register) -> Entry | None:
    """Pick the aligned entry whose two names differ by nothing but the casing convention.

    Derived rather than chosen, so the example cannot drift away from the register. The longest
    such pair shows the conversion most clearly.
    """
    candidates = [
        entry
        for entry in register.of_kind("aligned")
        if "_" in entry.python and camel(entry.python) == entry.typescript
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda entry: len(entry.python))


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_guessing(register: Register) -> list[str]:
    filled = illustrations(register)
    lines = ["## Guessing a name before you look it up", "", wrap(GUESSING), ""]
    for title, body in GUESSING_RULES:
        lines += [wrap(f"**{title}** {body.format(**filled)}"), ""]
    lines += [wrap(GUESSING_CLOSE), ""]
    return lines


def render_vocabulary(register: Register) -> list[str]:
    if not register.meanings:
        return []
    lines = ["## The verb vocabulary", "", wrap(VOCABULARY_LEAD), ""]
    lines += ["| Verb | What it means |", "| ---- | ------------- |"]
    for verb, meaning in register.meanings:
        lines.append(f"| `{cell(verb)}` | {cell(sentence_case(' '.join(meaning.split())))}. |")
    lines += ["", wrap(VOCABULARY_CLOSE), ""]
    return lines


def render_map(register: Register) -> list[str]:
    lines = ["## The map", "", wrap(MAP_LEAD), ""]
    for group in register.groups:
        rows = [entry for entry in register.entries if entry.group == group]
        lines += [
            # An explicit anchor, because a group heading and an entry heading can carry the same
            # words and a concept's anchor is the one links point at.
            f"### {sentence_case(without_requirement_ids(group))} {{ #map-{slug(without_requirement_ids(group))} }}",
            "",
            "| Concept | Python | TypeScript | Kind |",
            "| ------- | ------ | ---------- | ---- |",
        ]
        for entry in rows:
            lines.append(
                f"| {cell(entry.concept)} "
                f"| {name_cell(entry, entry.python_names)} "
                f"| {name_cell(entry, entry.typescript_names)} "
                f"| {kind_cell(entry)} |"
            )
        lines.append("")
    return lines


def render_notes(register: Register) -> list[str]:
    grouped: dict[str, tuple[str, list[str]]] = {}
    for entry in register.entries:
        if not entry.notes or entry.has_detail:
            continue
        key = " ".join(entry.notes.split())
        note, concepts = grouped.setdefault(key, (entry.notes, []))
        concepts.append(entry.concept)
    if not grouped:
        return []
    lines = ["## What the notes add", "", wrap(NOTES_LEAD), ""]
    for note, concepts in grouped.values():
        lines += [wrap(f"**{', '.join(concepts)}**"), ""]
        lines += wrap_prose(note)
    return lines


def render_entry_detail(entry: Entry) -> list[str]:
    python = ", ".join(f"`{cell(name)}`" for name in entry.python_names) or "*absent*"
    typescript = ", ".join(f"`{cell(name)}`" for name in entry.typescript_names) or "*absent*"
    lines = [
        f"### {sentence_case(entry.concept)}",
        "",
        "| Python | TypeScript |",
        "| ------ | ---------- |",
        f"| {python} | {typescript} |",
        "",
    ]
    lines += wrap_prose(entry.divergence_reason)
    if entry.canonical_form:
        lines += [wrap(f"Canonical form across the boundary: **{entry.canonical_form}**."), ""]
    if entry.notes:
        lines += wrap_prose(entry.notes)
    return lines


def render_divergences(register: Register) -> list[str]:
    divergent = register.of_kind("divergent")
    if not divergent:
        return []
    lines = ["## Where the two libraries differ, and why", "", wrap(DIVERGENCE_LEAD), ""]
    for entry in divergent:
        lines += render_entry_detail(entry)
    return lines


def render_canonical(register: Register) -> list[str]:
    carriers = [entry for entry in register.entries if entry.canonical_form]
    if not carriers:
        return []
    lines = ["## The canonical form across the boundary", "", wrap(CANONICAL_LEAD), ""]
    lines += [
        "| Concept | Python | TypeScript | Canonical form |",
        "| ------- | ------ | ---------- | -------------- |",
    ]
    for entry in carriers:
        concept = f"[{cell(entry.concept)}](#{slug(entry.concept)})" if entry.has_detail else cell(entry.concept)
        lines.append(
            f"| {concept} "
            f"| {name_cell(entry, entry.python_names)} "
            f"| {name_cell(entry, entry.typescript_names)} "
            f"| {cell(entry.canonical_form)} |"
        )
    lines += ["", wrap(CANONICAL_CLOSE), ""]
    return lines


def render_excluded(register: Register) -> list[str]:
    excluded = register.of_kind("excluded")
    if not excluded:
        return []
    lines = ["## Surfaces that stay in one language", "", wrap(EXCLUDED_LEAD), ""]
    for entry in excluded:
        lines += [f"### {sentence_case(entry.concept)}", ""]
        for language, names in (("Python", entry.python_names), ("TypeScript", entry.typescript_names)):
            if not names:
                lines += [f"**{language}**: none, and never.", ""]
            elif len(names) == 1:
                lines += [f"**{language}**: `{cell(names[0])}`.", ""]
            else:
                lines += [f"**{language}**, {len(names)} names:", ""]
                lines += [f"- `{cell(name)}`" for name in names]
                lines.append("")
        lines += wrap_prose(entry.divergence_reason)
        if entry.notes:
            lines += wrap_prose(entry.notes)
    return lines


def render_spent(register: Register) -> list[str]:
    rows: list[tuple[str, str, str, int]] = []
    for entry in register.entries:
        if entry.renames.python:
            rows.append((entry.concept, name_or_withdrawn(entry.python), "Python", entry.renames.python))
        if entry.renames.typescript:
            rows.append((entry.concept, name_or_withdrawn(entry.typescript), "TypeScript", entry.renames.typescript))
    if not rows:
        return []
    lines = ["## Names that have spent their rename", "", wrap(SPENT_LEAD), ""]
    lines += ["| Concept | Name | Language | Renames |", "| ------- | ---- | -------- | ------- |"]
    for concept, name, language, count in rows:
        anchor = f"[{cell(concept)}](#{slug(concept)})"
        entry = register.by_concept(concept)
        label = anchor if entry is not None and entry.has_detail else cell(concept)
        lines.append(f"| {label} | {name} | {language} | {count} |")
    lines += ["", wrap(SPENT_CLOSE), ""]
    return lines


def render_reserved(register: Register) -> list[str]:
    if not register.reserved:
        return []
    lines = ["## Package names reserved before their ports", "", wrap(RESERVED_LEAD), ""]
    lines += [
        "| Capability | npm package | Subpath | Mirrors | Tier | Built |",
        "| ---------- | ----------- | ------- | ------- | ---- | ----- |",
    ]
    for package in register.reserved:
        mirrors = ", ".join(f"`{cell(name)}`" for name in package.mirrors) or "none"
        lines.append(
            f"| {cell(package.capability)} "
            f"| `{cell(package.npm_package)}` "
            f"| `{cell(package.subpath)}` "
            f"| {mirrors} "
            f"| {package.tier} "
            f"| {'yes' if package.built else 'not yet'} |"
        )
    lines.append("")
    return lines


def render_gate(register: Register) -> list[str]:
    if not register.gate_failures and not register.gate_exit_zero:
        return []
    lines = ["## What the gate refuses", ""]
    if register.gate_failures:
        lines += [wrap(GATE_LEAD), ""]
        for failure in register.gate_failures:
            head, _, detail = failure.partition(":")
            bullet = f"**{sentence_case(without_requirement_ids(' '.join(head.split())))}.**"
            if detail.strip():
                bullet += f" It {' '.join(detail.split())}."
            lines.append(bullet_item(bullet))
        lines.append("")
    if register.gate_exit_zero:
        lines += [wrap(f"It passes when {register.gate_exit_zero}."), ""]
    if register.review:
        lines += [wrap(f"Changing the register itself needs {register.review}."), ""]
    lines += [wrap(GATE_CLOSE), ""]
    return lines


def render(register: Register, level: str) -> str:
    """Render everything that sits between the generated markers."""
    source_url = f"{REGISTER_REPO}/blob/{level}/governance/naming.toml"
    governs = " and ".join(f"`{name}`" for name in register.governs) or "both libraries"
    provenance = (
        f"Generated from [`governance/naming.toml`]({source_url}) at `{level}`, the governance tag "
        f"this release pins. It governs {governs}, and it is read at {register.read_at}. Correct "
        "the register and regenerate; a correction made on this page would be overwritten, and it "
        "would never reach either library's naming gate."
    )
    lines = [wrap(provenance), ""]
    lines += render_guessing(register)
    lines += render_vocabulary(register)
    lines += render_map(register)
    lines += render_notes(register)
    lines += render_divergences(register)
    lines += render_canonical(register)
    lines += render_excluded(register)
    lines += render_spent(register)
    lines += render_reserved(register)
    lines += render_gate(register)

    body = "\n".join(line.rstrip() for line in lines).rstrip() + "\n"
    duplicate = duplicate_anchor(body)
    if duplicate is not None:
        sys.exit(f"two generated headings share the anchor #{duplicate}, so a link would land on the wrong one")
    return body


EXPLICIT_ANCHOR_RE = re.compile(r"\{\s*#(?P<anchor>[\w-]+)\s*\}\s*$")


def duplicate_anchor(body: str) -> str | None:
    seen: set[str] = set()
    for line in body.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip()
        explicit = EXPLICIT_ANCHOR_RE.search(heading)
        anchor = explicit.group("anchor") if explicit else slug(heading)
        if anchor in seen:
            return anchor
        seen.add(anchor)
    return None


def splice(page: str, body: str) -> str:
    """Replace the generated region of the page, leaving the hand-written prose alone."""
    begin = page.find(BEGIN_MARKER)
    end = page.find(END_MARKER)
    if begin == -1 or end == -1 or end < begin:
        sys.exit(f"{PAGE_PATH}: the generated markers are missing or out of order")
    head = page[: begin + len(BEGIN_MARKER)]
    tail = page[end:]
    return f"{head}\n\n{body}\n{tail}"


def resolve_register_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    governance_dir = os.environ.get("IDFKIT_GOVERNANCE_DIR")
    if governance_dir:
        candidate = Path(governance_dir).expanduser().resolve()
        return candidate if candidate.is_file() else candidate / "naming.toml"
    return REPO_ROOT.parent / "idfkit-conformance" / "governance" / "naming.toml"


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
    parser.add_argument("--register", help="path to naming.toml, overriding the usual resolution order")
    parser.add_argument("--check", action="store_true", help="fail if the page is stale instead of rewriting it")
    args = parser.parse_args(argv)

    register_path = resolve_register_path(args.register)
    if not register_path.is_file():
        sys.exit(
            f"naming register not found at {register_path}; check out idfkit-conformance or set IDFKIT_GOVERNANCE_DIR"
        )

    level = resolve_level()
    overridden = args.register is not None or bool(os.environ.get("IDFKIT_GOVERNANCE_DIR"))
    source = read_pinned(register_path, level, override=overridden)
    if not source.pinned:
        print(f"note: reading {source.description}", file=sys.stderr)
    raw_text = source.text
    register = parse_register(tomllib.loads(raw_text), raw_text)
    if register.problems:
        print(f"{source.description}: the register does not satisfy its own contract")
        for problem in register.problems:
            print(f"  - {problem}")
        return 2

    body = render(register, resolve_level())
    current = PAGE_PATH.read_text(encoding="utf-8")
    updated = splice(current, body)

    if args.check:
        if updated != current:
            print(f"{PAGE_PATH} is stale. Run: uv run python scripts/render_naming_map.py")
            return 1
        print(f"{PAGE_PATH} is up to date with {source.description} ({len(register.entries)} entries)")
        return 0

    if updated != current:
        PAGE_PATH.write_text(updated, encoding="utf-8")
        print(f"rewrote {PAGE_PATH} from {source.description} ({len(register.entries)} entries)")
    else:
        print(f"{PAGE_PATH} already matches {register_path} ({len(register.entries)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
