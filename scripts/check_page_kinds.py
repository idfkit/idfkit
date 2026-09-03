#!/usr/bin/env python3
"""Hold every documentation page to exactly one kind, and report material repeated across kinds.

Implements FR-055 and SC-022, with the single declared exception of FR-059. The companion prose is
in ``contracts/documentation-site.md`` under "Page kinds"; this script is the gate that makes it
more than an intention.

WHAT A "KIND" IS, AND WHERE IT COMES FROM

A page's kind is not written on the page. It is where the page sits in ``mkdocs.yml``. That is the
only definition a reader ever experiences: a page filed under "How-to guides" is a how-to guide to
everyone who arrives at it, whatever its front matter claims. So the gate reads the navigation and
takes the top-level section a page hangs from as its kind:

    Tutorials         -> tutorial
    How-to guides     -> how-to
    Reference         -> reference
    Explanation       -> explanation

Three consequences follow, and all three are the point.

* A page reachable from two different top-level sections is classified as two kinds and fails
  (FR-055). Two nav entries pointing at one file is the ordinary way this happens.
* A top-level section whose title is none of the four fails. Troubleshooting is the live example:
  the contract files troubleshooting pages as how-to guides, so a separate top-level
  "Troubleshooting" section is a fifth kind by accident and is reported as one.
* A page under ``docs/`` that no nav entry reaches has no declared kind at all. MkDocs warns about
  it separately in a strict build, but silence in the navigation is exactly how a page comes to
  belong to no kind, so it is reported here too.

THE ONE DECLARED EXCEPTION (FR-059)

``docs/agent-references/`` is material addressed to automated tooling and shipped inside the Python
wheel. It has an audience and a link discipline the human documentation does not share, and it is a
fifth section by explicit amendment rather than by drift.

It is hard-coded below as ``DECLARED_EXCEPTIONS``, a tuple with exactly one member, and the gate
refuses to run if that tuple ever holds more than one. There is deliberately no flag, no
configuration key and no environment variable that adds a second: widening the exception means
editing this file, which means someone reviews the edit against FR-059.

The exception is recognised by *path*, not by section title, because the path is what the
requirement names. A section is the exception when every page in it lives under the prefix. An
``agent-references/`` page filed inside one of the four kinds, or a human page filed inside the
exception's section, is reported as a leak in either direction.

``docs/index.md`` is the site root. It is a landing page rather than content, it carries no kind,
and it is not a fifth section. Any *other* top-level page entry is reported.

WHAT THE DUPLICATION CHECK CAN AND CANNOT SEE

This is the half worth being honest about, so it is stated plainly rather than implied by a green
run.

Detected:

* the same heading on two pages of different kinds, compared after normalisation, which absorbs
  case, inline formatting, links, trailing anchors and punctuation. Headings shorter than
  ``MINIMUM_HEADING_WORDS`` words, and a small stop-list of structural phrases, are ignored: every
  page has an "Example", and saying so is furniture rather than duplication.
* the same fenced code block, verbatim once trailing whitespace is stripped, on two pages of
  different kinds, once the block is at least ``MINIMUM_CODE_LINES`` lines and
  ``MINIMUM_CODE_CHARS`` characters.

Not detected, and no attempt is made to pretend otherwise:

* the same explanation written twice in different words. That is semantic duplication and it needs
  a reader.
* a concept taught in a tutorial and re-taught in an explanation under different headings.
* duplication against anything outside this site.

Two deliberate softenings, both reported rather than hidden:

* duplication *within* one kind is a warning, not a failure. Two how-to guides that both show a
  document being loaded are usually doing their job.
* a block that only pulls in a snippet (``--8<--``) is single-sourced by construction. The same
  snippet reaching pages of different kinds is reported as a warning, because one file feeding two
  pages is the opposite of a copy.

The exception tree takes no part in the duplication scan. Restating library material for a machine
reader is what that tree is for, so comparing it against the human pages would produce findings
nobody can act on.

EXIT CODES

  0  every page is exactly one kind, and nothing is duplicated across kinds
  1  at least one blocking finding
  2  the gate could not run: no mkdocs.yml, no navigation in it, no YAML reader

Usage:

    python scripts/check_page_kinds.py
    python scripts/check_page_kinds.py docs/
    python scripts/check_page_kinds.py --config mkdocs.yml --verbose
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import cast

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_REFUSED = 2

# FR-059: the one tree that is a navigation section without being one of the four kinds. Adding a
# second member here is a constitutional amendment rather than a configuration change, and the gate
# refuses to run if one appears.
DECLARED_EXCEPTIONS: tuple[str, ...] = ("agent-references/",)

# The site root. A landing page rather than content, so it carries no kind. It is not a fifth
# section: any other top-level page entry is a finding.
SITE_HOME = "index.md"

PAGE_SUFFIXES = frozenset({".md", ".ipynb"})

# Top-level directories under docs/ that hold build inputs rather than pages. Pages are only ever
# .md or .ipynb, so this exists for the occasional markdown file living beside them.
NON_PAGE_DIRECTORIES = frozenset({"hooks", "overrides", "snippets", "stylesheets", "assets", "javascripts"})

# Pages generated from the governance files, listed by the script that writes each one.
#
# They are exempt from the duplication scan and from nothing else. Their headings ARE the
# registered concept names and the ledger's capability names, so restating those is the whole
# point of the artefact rather than a copy of another page. A gate that failed here would be
# telling us that an index names the things it indexes.
#
# Narrow on purpose: this exempts two named files, not a directory and not a kind. A third
# generated page has to be added here deliberately, next to the script that generates it.
GENERATED_PAGES: dict[str, str] = {
    "explanation/naming-map.md": "scripts/render_naming_map.py",
    "explanation/parity.md": "scripts/render_parity_page.py",
}

MINIMUM_HEADING_WORDS = 3
MINIMUM_CODE_LINES = 3
MINIMUM_CODE_CHARS = 60

# Structural headings that recur on every page of a well-written site. Normalised spelling.
GENERIC_HEADINGS = frozenset({
    "before you begin",
    "further reading",
    "how it works",
    "next steps",
    "related pages",
    "see also",
    "what happens next",
    "what you get",
    "what you need",
    "when to use it",
    "when to use this",
})

NO_YAML_READER = (
    "no YAML reader is installed. PyYAML arrives with mkdocs, so `uv sync` fixes this; the "
    "navigation cannot be read without it."
)
NO_CONFIG = "no mkdocs.yml at {path}. The navigation is the only record of what kind a page is."
NO_NAV = "mkdocs.yml at {path} declares no `nav:`, so no page has a declared kind."
NO_DOCS_DIR = "no documentation directory at {path}."
TOO_MANY_EXCEPTIONS = (
    "DECLARED_EXCEPTIONS holds {count} entries. FR-059 permits exactly one, the agent-references "
    "tree. A second exception is a constitutional amendment, not an edit to this tuple."
)

_ATX_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_FENCE = re.compile(r"^(?P<indent>\s*)(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
_TRAILING_ANCHOR = re.compile(r"\s*\{[^}]*\}\s*$")
_INLINE_MARKUP = re.compile(r"[`*_~]")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_NON_WORD = re.compile(r"[^a-z0-9]+")
_SNIPPET_INCLUDE = re.compile(r"^\s*(?:;|//|#)?\s*--8<--")


class Refusal(Exception):
    """The gate cannot run at all. Distinct from a gate failure."""


class PageKind(Enum):
    """The four kinds, plus the one declared exception."""

    TUTORIAL = "tutorial"
    HOW_TO = "how-to"
    REFERENCE = "reference"
    EXPLANATION = "explanation"
    AGENT_REFERENCES = "agent-references"

    @property
    def is_exception(self) -> bool:
        return self is PageKind.AGENT_REFERENCES


# Section titles are reader-facing wording, so a handful of spellings map to each kind. A title
# outside this table is an undeclared fifth section and is reported as one.
SECTION_KINDS: dict[str, PageKind] = {
    "tutorial": PageKind.TUTORIAL,
    "tutorials": PageKind.TUTORIAL,
    "how to": PageKind.HOW_TO,
    "how to guide": PageKind.HOW_TO,
    "how to guides": PageKind.HOW_TO,
    "guides": PageKind.HOW_TO,
    "reference": PageKind.REFERENCE,
    "explanation": PageKind.EXPLANATION,
    "explanations": PageKind.EXPLANATION,
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NavNode:
    """One navigation entry as MkDocs reads it: a page, or a labelled list of further nodes."""

    title: str | None
    path: str | None
    children: tuple[NavNode, ...]


@dataclass(frozen=True)
class NavEntry:
    """One navigation entry pointing at one file, with the trail that reached it."""

    path: str
    kind: PageKind | None
    trail: tuple[str, ...]

    @property
    def where(self) -> str:
        return " > ".join(self.trail) if self.trail else "(top level)"

    @property
    def kind_label(self) -> str:
        return self.kind.value if self.kind else "unclassified"


@dataclass(frozen=True)
class NavSection:
    """A top-level navigation section and the kind its title declares."""

    title: str
    kind: PageKind | None
    paths: tuple[str, ...]


@dataclass(frozen=True)
class Navigation:
    """Everything the navigation says about kinds."""

    sections: tuple[NavSection, ...]
    entries: tuple[NavEntry, ...]
    home: str | None

    def entries_for(self, path: str) -> tuple[NavEntry, ...]:
        return tuple(entry for entry in self.entries if entry.path == path)

    def kinds_for(self, path: str) -> tuple[PageKind | None, ...]:
        seen: list[PageKind | None] = []
        for entry in self.entries_for(path):
            if entry.kind not in seen:
                seen.append(entry.kind)
        return tuple(seen)

    @property
    def paths(self) -> frozenset[str]:
        return frozenset(entry.path for entry in self.entries)


@dataclass(frozen=True)
class Heading:
    """A heading, as written and as compared."""

    text: str
    normalized: str
    line: int

    @property
    def comparable(self) -> bool:
        if self.normalized in GENERIC_HEADINGS:
            return False
        return len(self.normalized.split()) >= MINIMUM_HEADING_WORDS


@dataclass(frozen=True)
class CodeBlock:
    """A fenced code block, normalised for comparison."""

    language: str
    content: str
    line: int
    is_include: bool

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()[:12]

    @property
    def comparable(self) -> bool:
        if self.is_include:
            return False
        body = [line for line in self.content.splitlines() if line.strip()]
        return len(body) >= MINIMUM_CODE_LINES and len(self.content) >= MINIMUM_CODE_CHARS

    @property
    def summary(self) -> str:
        first = next((line.strip() for line in self.content.splitlines() if line.strip()), "")
        return first if len(first) <= 70 else f"{first[:67]}..."


@dataclass(frozen=True)
class Page:
    """One page, read once, with everything the duplication scan needs."""

    path: str
    kind: PageKind | None
    headings: tuple[Heading, ...]
    code_blocks: tuple[CodeBlock, ...]
    unreadable: str | None = None

    @property
    def kind_label(self) -> str:
        return self.kind.value if self.kind else "unclassified"


@dataclass(frozen=True)
class Finding:
    """One gate failure."""

    code: str
    subject: str
    message: str
    detail: tuple[str, ...] = ()

    def render(self) -> str:
        head = f"  [{self.code}] {self.subject}: {self.message}"
        if not self.detail:
            return head
        body = "\n".join(f"      {line}" for line in self.detail)
        return f"{head}\n{body}"


@dataclass
class Report:
    """Everything one run of the gate produced."""

    config_path: Path
    docs_dir: Path
    navigation: Navigation
    pages: tuple[Page, ...]
    findings: list[Finding] = field(default_factory=lambda: [])
    warnings: list[str] = field(default_factory=lambda: [])

    @property
    def ok(self) -> bool:
        return not self.findings


# ---------------------------------------------------------------------------
# Reading mkdocs.yml
# ---------------------------------------------------------------------------


def _ignore_unknown_tag(_loader: object, _suffix: str, _node: object) -> None:
    """Read a tag SafeLoader does not know, such as ``!!python/name:``, as None."""
    return None


def load_config(text: str) -> dict[str, object]:
    """Parse mkdocs.yml, tolerating the ``!!python/name:`` tags the theme configuration carries."""
    try:
        import yaml  # pyright: ignore[reportMissingModuleSource]
    except ModuleNotFoundError as exc:  # pragma: no cover - PyYAML arrives with mkdocs
        raise Refusal(NO_YAML_READER) from exc

    class _NavLoader(yaml.SafeLoader):  # pyright: ignore[reportUntypedBaseClass]
        """A SafeLoader that reads unknown tags as None instead of refusing the document."""

    _NavLoader.add_multi_constructor(None, _ignore_unknown_tag)  # pyright: ignore[reportUnknownMemberType, reportArgumentType]
    loaded: object = yaml.load(text, Loader=_NavLoader)  # noqa: S506 - _NavLoader derives from SafeLoader
    if not isinstance(loaded, dict):
        return {}
    return {str(key): value for key, value in cast("dict[object, object]", loaded).items()}


def _nav_nodes(value: object) -> tuple[NavNode, ...]:
    """Turn one nav list, as YAML produced it, into typed nodes. Shapes MkDocs rejects are dropped."""
    if not isinstance(value, list):
        return ()
    nodes: list[NavNode] = []
    for item in cast("list[object]", value):
        if isinstance(item, str):
            nodes.append(NavNode(title=None, path=item, children=()))
            continue
        if not isinstance(item, dict):
            continue
        pairs = list(cast("dict[object, object]", item).items())
        if len(pairs) != 1:
            continue
        key, child = pairs[0]
        title = str(key)
        if isinstance(child, str):
            nodes.append(NavNode(title=title, path=child, children=()))
        elif isinstance(child, list):
            nodes.append(NavNode(title=title, path=None, children=_nav_nodes(cast("list[object]", child))))
    return tuple(nodes)


def _walk(nodes: Sequence[NavNode], trail: tuple[str, ...]) -> Iterator[tuple[str, tuple[str, ...]]]:
    """Yield ``(docs-relative path, trail)`` for every file entry under a list of nodes."""
    for node in nodes:
        deeper = (*trail, node.title) if node.title else trail
        if node.path is not None:
            yield node.path, deeper
        else:
            yield from _walk(node.children, deeper)


def _normalize_title(title: str) -> str:
    return _NON_WORD.sub(" ", title.lower()).strip()


def _in_exception(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in DECLARED_EXCEPTIONS)


def classify_section(title: str, paths: Sequence[str]) -> PageKind | None:
    """The kind of a top-level section: its title first, then the one declared path exception."""
    kind = SECTION_KINDS.get(_normalize_title(title))
    if kind is not None:
        return kind
    if paths and all(_in_exception(path) for path in paths):
        return PageKind.AGENT_REFERENCES
    return None


def read_navigation(config: dict[str, object], config_path: Path) -> Navigation:
    """Turn the ``nav:`` block into sections, entries and the site home."""
    nav = config.get("nav")
    if not isinstance(nav, list):
        raise Refusal(NO_NAV.format(path=config_path))

    sections: list[NavSection] = []
    entries: list[NavEntry] = []
    home: str | None = None

    for node in _nav_nodes(cast("list[object]", nav)):
        if node.path is not None:
            if node.path == SITE_HOME:
                home = node.path
            else:
                entries.append(NavEntry(path=node.path, kind=None, trail=(node.title,) if node.title else ()))
            continue
        title = node.title or ""
        walked = tuple(_walk(node.children, (title,)))
        paths = tuple(path for path, _ in walked)
        kind = classify_section(title, paths)
        sections.append(NavSection(title=title, kind=kind, paths=paths))
        entries.extend(NavEntry(path=path, kind=kind, trail=trail) for path, trail in walked)

    return Navigation(sections=tuple(sections), entries=tuple(entries), home=home)


# ---------------------------------------------------------------------------
# Which files under docs/ are pages
# ---------------------------------------------------------------------------


def excluded_patterns(config: dict[str, object]) -> tuple[str, ...]:
    """The ``exclude_docs:`` block, with comments and negations dropped."""
    raw = config.get("exclude_docs")
    if not isinstance(raw, str):
        return ()
    patterns: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "!")):
            continue
        patterns.append(stripped.lstrip("/"))
    return tuple(patterns)


def _is_excluded(relative: str, patterns: Sequence[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/"):
            if relative.startswith(pattern):
                return True
        elif relative == pattern or fnmatch.fnmatch(relative, pattern):
            return True
    return False


def discover_pages(docs_dir: Path, patterns: Sequence[str]) -> tuple[str, ...]:
    """Every file under docs/ that MkDocs would publish as a page."""
    found: list[str] = []
    for path in sorted(docs_dir.rglob("*")):
        if not path.is_file() or path.suffix not in PAGE_SUFFIXES:
            continue
        relative = path.relative_to(docs_dir).as_posix()
        if relative.split("/")[0] in NON_PAGE_DIRECTORIES or _is_excluded(relative, patterns):
            continue
        found.append(relative)
    return tuple(found)


# ---------------------------------------------------------------------------
# Reading a page
# ---------------------------------------------------------------------------


def normalize_heading(text: str) -> str:
    """Fold a heading to the form two pages are compared on."""
    without_anchor = _TRAILING_ANCHOR.sub("", text)
    unlinked = _LINK.sub(r"\1", without_anchor)
    plain = _INLINE_MARKUP.sub("", unlinked)
    return _NON_WORD.sub(" ", plain.lower()).strip()


def _normalize_code(lines: Sequence[str]) -> str:
    trimmed = [line.rstrip() for line in lines]
    while trimmed and not trimmed[0].strip():
        trimmed.pop(0)
    while trimmed and not trimmed[-1].strip():
        trimmed.pop()
    return "\n".join(trimmed)


def _code_block(info: str, lines: Sequence[str], line: int) -> CodeBlock:
    content = _normalize_code(lines)
    body = [entry for entry in content.splitlines() if entry.strip()]
    is_include = bool(body) and all(_SNIPPET_INCLUDE.match(entry) for entry in body)
    words = info.split()
    return CodeBlock(language=words[0] if words else "", content=content, line=line, is_include=is_include)


def parse_markdown(text: str) -> tuple[tuple[Heading, ...], tuple[CodeBlock, ...]]:
    """Headings and fenced code blocks, with headings inside a fence left alone."""
    headings: list[Heading] = []
    blocks: list[CodeBlock] = []
    fence: str | None = None
    info = ""
    start = 0
    buffer: list[str] = []

    for number, line in enumerate(text.splitlines(), start=1):
        match = _FENCE.match(line)
        if fence is None:
            if match is not None:
                fence, info, start, buffer = match.group("fence"), match.group("info").strip(), number, []
            else:
                heading = _ATX_HEADING.match(line)
                if heading is not None:
                    title = heading.group(2)
                    headings.append(Heading(text=title, normalized=normalize_heading(title), line=number))
            continue
        if match is not None and _closes(match.group("fence"), match.group("info"), fence):
            blocks.append(_code_block(info, buffer, start))
            fence = None
        else:
            buffer.append(line)

    if fence is not None:
        blocks.append(_code_block(info, buffer, start))
    return tuple(headings), tuple(blocks)


def _closes(candidate: str, info: str, fence: str) -> bool:
    """A fence closes when it uses the same character, is no shorter, and carries no info string."""
    return candidate[0] == fence[0] and len(candidate) >= len(fence) and not info.strip()


def _cell_source(cell: dict[str, object]) -> str:
    source = cell.get("source")
    if isinstance(source, str):
        return source
    if isinstance(source, list):
        return "".join(str(part) for part in cast("list[object]", source))
    return ""


def parse_notebook(text: str) -> tuple[tuple[Heading, ...], tuple[CodeBlock, ...]]:
    """The same two things out of a notebook, so a .ipynb in the nav is read rather than skipped."""
    document: object = json.loads(text)
    if not isinstance(document, dict):
        return (), ()
    cells = cast("dict[object, object]", document).get("cells")
    if not isinstance(cells, list):
        return (), ()

    headings: list[Heading] = []
    blocks: list[CodeBlock] = []
    for index, raw_cell in enumerate(cast("list[object]", cells), start=1):
        if not isinstance(raw_cell, dict):
            continue
        cell = cast("dict[str, object]", raw_cell)
        source = _cell_source(cell)
        kind = cell.get("cell_type")
        if kind == "markdown":
            cell_headings, cell_blocks = parse_markdown(source)
            headings.extend(cell_headings)
            blocks.extend(cell_blocks)
        elif kind == "code":
            blocks.append(_code_block("python", source.splitlines(), index))
    return tuple(headings), tuple(blocks)


def read_page(docs_dir: Path, relative: str, kind: PageKind | None) -> Page:
    """Read one page. A file that cannot be read becomes a page that says why."""
    path = docs_dir / relative
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return Page(path=relative, kind=kind, headings=(), code_blocks=(), unreadable=str(exc))
    if path.suffix == ".ipynb":
        try:
            headings, blocks = parse_notebook(text)
        except (json.JSONDecodeError, ValueError) as exc:
            return Page(path=relative, kind=kind, headings=(), code_blocks=(), unreadable=f"not valid JSON: {exc}")
        return Page(path=relative, kind=kind, headings=headings, code_blocks=blocks)
    headings, blocks = parse_markdown(text)
    return Page(path=relative, kind=kind, headings=headings, code_blocks=blocks)


# ---------------------------------------------------------------------------
# The checks
# ---------------------------------------------------------------------------


def check_sections(navigation: Navigation) -> list[Finding]:
    """Every top-level section declares one of the four kinds, or is the one declared exception."""
    return [
        Finding(
            code="unclassified-section",
            subject=section.title,
            message=(
                "top-level section is none of tutorial, how-to, reference or explanation, and is not "
                "the one declared exception, so the pages under it have no declared kind"
            ),
            detail=section.paths[:10],
        )
        for section in navigation.sections
        if section.kind is None
    ]


def check_one_kind(navigation: Navigation) -> tuple[list[Finding], list[str]]:
    """A page reachable from two kinds is two kinds. A page listed twice in one kind is a wart."""
    findings: list[Finding] = []
    warnings: list[str] = []

    for path in sorted(navigation.paths):
        entries = navigation.entries_for(path)
        kinds = navigation.kinds_for(path)
        if len(kinds) > 1:
            named = ", ".join(kind.value if kind else "unclassified" for kind in kinds)
            findings.append(
                Finding(
                    code="two-kinds",
                    subject=path,
                    message=f"reachable from {len(kinds)} kinds ({named}); a page is exactly one",
                    detail=tuple(f"{entry.kind_label}: {entry.where}" for entry in entries),
                )
            )
        elif len(entries) > 1:
            warnings.append(f"{path} is listed {len(entries)} times inside {entries[0].kind_label}")
    return findings, warnings


def check_exception_boundary(navigation: Navigation) -> list[Finding]:
    """The exception tree stays inside its own section, and nothing else moves into it."""
    findings: list[Finding] = []
    for entry in navigation.entries:
        if entry.kind is None:
            continue
        inside = _in_exception(entry.path)
        if inside and not entry.kind.is_exception:
            findings.append(
                Finding(
                    code="exception-leak",
                    subject=entry.path,
                    message=f"the declared exception tree is filed under {entry.kind.value}",
                    detail=(entry.where,),
                )
            )
        elif not inside and entry.kind.is_exception:
            findings.append(
                Finding(
                    code="exception-leak",
                    subject=entry.path,
                    message="filed inside the declared exception without living under it",
                    detail=(entry.where, f"exception prefixes: {', '.join(DECLARED_EXCEPTIONS)}"),
                )
            )
    return findings


def check_reachable(navigation: Navigation, discovered: Sequence[str], docs_dir: Path) -> list[Finding]:
    """Pages the navigation never reaches, and navigation entries pointing at nothing."""
    home: set[str] = {navigation.home} if navigation.home else set()
    navigated = set(navigation.paths) | home

    findings: list[Finding] = [
        Finding(
            code="no-declared-kind",
            subject=relative,
            message="no navigation entry reaches this page, so it declares no kind",
        )
        for relative in discovered
        if relative not in navigated
    ]
    findings.extend(
        Finding(
            code="missing-page",
            subject=path,
            message="the navigation points at a file that does not exist",
        )
        for path in sorted(navigated)
        if not (docs_dir / path).is_file()
    )
    return findings


def _scannable(pages: Sequence[Page]) -> list[Page]:
    """Pages the duplication scan compares.

    Classified, readable, outside the exception tree, and not generated from the governance
    files. See ``GENERATED_PAGES`` for why the last of those is not a loophole.
    """
    return [
        page
        for page in pages
        if page.kind is not None
        and not page.kind.is_exception
        and not page.unreadable
        and page.path not in GENERATED_PAGES
    ]


def check_duplicate_headings(pages: Sequence[Page]) -> tuple[list[Finding], list[str]]:
    """Headings identical after normalisation, across kinds and within one kind."""
    index: dict[str, list[tuple[Page, Heading]]] = {}
    for page in _scannable(pages):
        for heading in page.headings:
            if heading.comparable:
                index.setdefault(heading.normalized, []).append((page, heading))

    findings: list[Finding] = []
    warnings: list[str] = []
    for normalized in sorted(index):
        found = index[normalized]
        if len({page.path for page, _ in found}) < 2:
            continue
        title = found[0][1].text
        detail = tuple(f"{page.kind_label}: {page.path}:{heading.line}" for page, heading in found)
        if len({page.kind for page, _ in found}) > 1:
            findings.append(
                Finding(
                    code="duplicate-heading",
                    subject=title,
                    message=(
                        "the same heading appears under more than one kind; link to the page that owns "
                        "the material rather than repeating it. A text match, not a semantic one"
                    ),
                    detail=detail,
                )
            )
        else:
            where = sorted({f"{page.path}:{heading.line}" for page, heading in found})
            warnings.append(f'heading "{title}" repeats within one kind: {", ".join(where)}')
    return findings, warnings


def check_duplicate_code(pages: Sequence[Page]) -> tuple[list[Finding], list[str]]:
    """Verbatim code blocks across kinds, and the single-sourced includes that only look like them."""
    verbatim: dict[str, list[tuple[Page, CodeBlock]]] = {}
    includes: dict[str, list[Page]] = {}
    for page in _scannable(pages):
        for block in page.code_blocks:
            if block.is_include:
                includes.setdefault(block.content, []).append(page)
            elif block.comparable:
                verbatim.setdefault(block.content, []).append((page, block))

    findings: list[Finding] = []
    warnings: list[str] = []
    for content in sorted(verbatim):
        found = verbatim[content]
        where = sorted({page.path for page, _ in found})
        if len(where) < 2:
            continue
        if len({page.kind for page, _ in found}) > 1:
            first = found[0][1]
            findings.append(
                Finding(
                    code="duplicate-code-block",
                    subject=f"{first.digest} {first.summary}",
                    message=(
                        "an identical code block appears under more than one kind; single-source it as a "
                        "snippet and include it, or link to the page that owns it"
                    ),
                    detail=tuple(f"{page.kind_label}: {page.path}:{block.line}" for page, block in found),
                )
            )
        else:
            warnings.append(f"an identical code block repeats within one kind: {', '.join(where)}")

    warnings.extend(_shared_snippet_warnings(includes))
    return findings, warnings


def _shared_snippet_warnings(includes: dict[str, list[Page]]) -> list[str]:
    """One snippet feeding pages of different kinds is single-sourced, so it is said rather than failed."""
    warnings: list[str] = []
    for content in sorted(includes):
        pages = includes[content]
        where = sorted({page.path for page in pages})
        if len(where) > 1 and len({page.kind for page in pages}) > 1:
            warnings.append(
                f"one snippet feeds pages of different kinds, single-sourced rather than copied: {', '.join(where)}"
            )
    return warnings


# ---------------------------------------------------------------------------
# Running and reporting
# ---------------------------------------------------------------------------


def run(config_path: Path, docs_dir: Path | None) -> Report:
    if len(DECLARED_EXCEPTIONS) != 1:
        raise Refusal(TOO_MANY_EXCEPTIONS.format(count=len(DECLARED_EXCEPTIONS)))
    if not config_path.is_file():
        raise Refusal(NO_CONFIG.format(path=config_path))

    config = load_config(config_path.read_text(encoding="utf-8"))
    declared = config.get("docs_dir")
    resolved = docs_dir or (config_path.parent / (declared if isinstance(declared, str) else "docs"))
    if not resolved.is_dir():
        raise Refusal(NO_DOCS_DIR.format(path=resolved))

    navigation = read_navigation(config, config_path)
    discovered = discover_pages(resolved, excluded_patterns(config))
    kinds = {entry.path: entry.kind for entry in navigation.entries}
    pages = tuple(read_page(resolved, relative, kinds.get(relative)) for relative in discovered)

    findings = check_sections(navigation)
    one_kind, warnings = check_one_kind(navigation)
    findings += one_kind
    findings += check_exception_boundary(navigation)
    findings += check_reachable(navigation, discovered, resolved)

    heading_findings, heading_warnings = check_duplicate_headings(pages)
    code_findings, code_warnings = check_duplicate_code(pages)
    findings += heading_findings + code_findings
    warnings += heading_warnings + code_warnings
    warnings += [f"{page.path} could not be read: {page.unreadable}" for page in pages if page.unreadable]

    return Report(
        config_path=config_path,
        docs_dir=resolved,
        navigation=navigation,
        pages=pages,
        findings=findings,
        warnings=warnings,
    )


def _kind_counts(report: Report) -> str:
    tally: dict[str, int] = {}
    for page in report.pages:
        tally[page.kind_label] = tally.get(page.kind_label, 0) + 1
    return ", ".join(f"{label} {count}" for label, count in sorted(tally.items()))


def render(report: Report, verbose: bool) -> str:
    lines = [
        f"Navigation: {report.config_path}",
        f"Pages:      {report.docs_dir}, {len(report.pages)} pages",
        f"Kinds:      {_kind_counts(report)}",
        f"Exception:  {', '.join(DECLARED_EXCEPTIONS)} (FR-059, the only one)",
    ]

    if verbose:
        lines.append("")
        lines.append("Every page, and the kind its navigation position declares:")
        lines.extend(f"  {page.path:<52} {page.kind_label}" for page in report.pages)

    if report.warnings:
        lines.append("")
        lines.append("Reported, not failed:")
        lines.extend(f"  {warning}" for warning in report.warnings)

    if report.findings:
        by_code: dict[str, list[Finding]] = {}
        for finding in report.findings:
            by_code.setdefault(finding.code, []).append(finding)
        lines.append("")
        lines.append(f"FAILED: {len(report.findings)} finding(s).")
        for code in sorted(by_code):
            group = by_code[code]
            lines.append("")
            lines.append(f"{code} ({len(group)}):")
            lines.extend(finding.render() for finding in group)
    else:
        lines.append("")
        lines.append("OK: every page is exactly one kind, and nothing is duplicated across kinds.")

    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check that every documentation page is exactly one of the four kinds (FR-055, SC-022).",
    )
    parser.add_argument(
        "docs_dir",
        nargs="?",
        default=None,
        help="Documentation directory (default: the `docs_dir` mkdocs.yml declares).",
    )
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parent.parent / "mkdocs.yml"),
        help="Path to mkdocs.yml. Its navigation is what declares each page's kind.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="List every page and its kind.")
    args = parser.parse_args(argv)

    docs_dir = Path(str(args.docs_dir)).resolve() if args.docs_dir else None
    try:
        report = run(Path(str(args.config)).resolve(), docs_dir)
    except Refusal as refusal:
        print(f"check_page_kinds: refusing to run.\n  {refusal}", file=sys.stderr)
        return EXIT_REFUSED

    print(render(report, args.verbose))
    return EXIT_OK if report.ok else EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
