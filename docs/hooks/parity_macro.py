"""The ``parity(id)`` documentation macro (FR-047).

A page that describes a capability writes one token on a line of its own::

    {{ parity("weather-index") }}

and this hook replaces it with an explicit statement of what the *other* language does with that
capability: nothing at all when both libraries carry it in full, a stated difference when one side
is ``partial``, a tracked gap when one side is temporarily absent, and a permanent boundary when one
side is absent for good. Availability then reaches the reader at the point of use instead of living
only on ``docs/explanation/parity.md``.

WHY A HOOK AND NOT A MACRO PLUGIN

``mkdocs-macros-plugin`` would turn every ``{{ ... }}`` on every page into Jinja, which is a large
blast radius for one token and a live hazard for the code samples this site is mostly made of. A
hook substitutes exactly the token below, leaves every other brace alone, and can abort the build
itself. It also adds no third-party dependency.

WHAT IT REFUSES TO DO (FR-047, T126)

An argument that does not resolve to a ledger id fails the build, naming the page, the id, and the
closest ids that do exist. Rendering an empty block instead would turn a typo into a silently
missing parity statement, which is the exact failure this macro exists to prevent. A line that opens
with ``{{`` and mentions ``parity(`` but does not parse fails the same way, so a malformed call
cannot survive as literal text on the page either.

WHERE THE LEDGER COMES FROM

``governance/parity.toml`` in ``idfkit/idfkit-conformance``, read with ``git show`` at the immutable
``governance-YYYY.N`` tag pinned in ``[tool.idfkit.governance] level``, never from a branch: a
moving ref would change what this site claims without any change landing in it. The checkout is
found in the order ``scripts/render_parity_page.py`` uses (``$IDFKIT_CONFORMANCE_DIR``, then a
sibling ``idfkit-conformance``), and this module imports that script rather than restating its
lookup, its ledger model, or its contract checks. ``$IDFKIT_GOVERNANCE_DIR`` reads a working tree
instead and says so loudly, matching the override ``scripts/check_parity_ledger.py`` offers.

The ledger is read lazily, on the first page that uses the macro, so a docs build of a tree with no
conformance checkout and no parity tokens still works.

Like the two render scripts, this is maintainer-side tooling and is not part of the distributed
package, so it needs Python 3.11 or newer for ``tomllib`` even though ``idfkit`` supports 3.10.
"""

from __future__ import annotations

import difflib
import functools
import importlib.util
import logging
import os
import posixpath
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import tomllib  # pyright: ignore[reportMissingTypeStubs]
from mkdocs.exceptions import PluginError

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from mkdocs.structure.pages import Page

log = logging.getLogger("mkdocs.hooks.parity_macro")

REPO_ROOT = Path(__file__).resolve().parents[2]
RENDERER_PATH = REPO_ROOT / "scripts" / "render_parity_page.py"

# The page every notice links back to, as a docs-relative source path.
PARITY_PAGE = "explanation/parity.md"
LEDGER_RELATIVE = "governance/parity.toml"

# The token, on a line of its own, in either quote style, with whitespace anywhere it can go.
TOKEN = re.compile(
    r"""^[ \t]*\{\{[ \t]*parity[ \t]*\([ \t]*(?P<quote>["'])(?P<id>[^"']*)(?P=quote)[ \t]*\)[ \t]*\}\}[ \t]*$"""
)
# Anything that opens a call but is not the token above: a typo in the syntax rather than in the id.
MALFORMED = re.compile(r"\{\{[ \t]*parity[ \t]*\(")
# Fenced code. A page documenting this macro shows the token; showing it must not invoke it.
FENCE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")


# ---------------------------------------------------------------------------
# The ledger, read at the pinned tag
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LedgerSource:
    """The capabilities the macro resolves against, and where they were read from."""

    level: str
    origin: str
    pinned: bool
    capabilities: dict[str, Any]


def _refuse(function: Callable[..., Any], *args: Any) -> Any:
    """Call a render-script helper, turning its ``sys.exit`` into a build failure.

    ``render_parity_page`` is a command-line script and exits on a missing ledger or a missing
    governance pin. A hook must not take the interpreter down mid-build, so the message it would
    have printed becomes the build error instead.
    """
    try:
        return function(*args)
    except SystemExit as stop:
        message = str(stop.code)
        raise PluginError(message) from stop


@functools.cache
def renderer() -> Any:
    """``scripts/render_parity_page.py``, imported for its ledger model and its prose helpers.

    Imported by path rather than copied: the ledger's dataclass, its contract checks, and the
    wording of the issue sentence have one definition, and the macro and the generated page cannot
    drift apart. The script guards its entry point, so importing it runs nothing.
    """
    spec = importlib.util.spec_from_file_location("idfkit_parity_renderer", RENDERER_PATH)
    if spec is None or spec.loader is None:
        message = f"cannot import {RENDERER_PATH}, which the parity macro shares its ledger model with"
        raise PluginError(message)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _git_show(repo: Path, ref: str, relative: str) -> str:
    """Read one file out of a git object, at a tag, without touching the working tree."""
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(repo), "show", f"{ref}:{relative}"],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = (
            f"the parity macro cannot read {relative} at {ref} from {repo}:\n"
            f"    {result.stderr.strip()}\n"
            "  The governance tag must exist and must be fetched. Set IDFKIT_GOVERNANCE_DIR to read "
            "a working tree instead, and understand that this is an override."
        )
        raise PluginError(message)
    return result.stdout


def _ledger_text(level: str) -> tuple[str, str, bool]:
    """The ledger's text, where it came from, and whether that was the pinned tag."""
    override = os.environ.get("IDFKIT_GOVERNANCE_DIR")
    if override:
        path = Path(override).expanduser() / "parity.toml"
        if not path.is_file():
            message = f"IDFKIT_GOVERNANCE_DIR is set but {path} does not exist"
            raise PluginError(message)
        log.warning(
            "LOCAL OVERRIDE: the parity macro is reading %s instead of the pinned tag %s. "
            "The pages it renders say nothing about what the pinned ledger records.",
            path,
            level,
        )
        return path.read_text(encoding="utf-8"), str(path), False

    # The same lookup order as scripts/render_parity_page.py, so one checkout serves the generated
    # page and this macro. The working-tree file locates the repository; the text comes from the tag.
    ledger_path = Path(_refuse(renderer().resolve_ledger_path, None, None)).resolve()
    repo = ledger_path.parents[1]
    return _git_show(repo, level, LEDGER_RELATIVE), f"{repo} at {level}", True


@functools.cache
def ledger() -> LedgerSource:
    """Parse the ledger once per build, and refuse to run against one that fails its own contract."""
    level = str(_refuse(renderer().resolve_level))
    text, origin, pinned = _ledger_text(level)
    parsed = renderer().parse_ledger(tomllib.loads(text))
    if parsed.problems:
        problems = "\n".join(f"    - {problem}" for problem in parsed.problems)
        message = f"the parity ledger read from {origin} does not satisfy its own contract:\n{problems}"
        raise PluginError(message)
    capabilities = {capability.capability_id: capability for capability in parsed.capabilities}
    log.info("parity macro: %d capabilities from %s", len(capabilities), origin)
    return LedgerSource(level=level, origin=origin, pinned=pinned, capabilities=capabilities)


# ---------------------------------------------------------------------------
# Rendering one notice
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Notice:
    """One rendered block: a Material admonition kind, its title, and its paragraphs."""

    kind: str
    title: str
    paragraphs: tuple[str, ...]

    def render(self) -> str:
        body = "\n\n".join(paragraph for paragraph in self.paragraphs if paragraph.strip())
        return f'!!! {self.kind} "{self.title}"\n\n{renderer().indent_block(body)}\n'


def wrap_prose(text: str) -> str:
    """Hard-wrap ledger prose, keeping its paragraph breaks.

    ``render_parity_page.wrap`` collapses all whitespace, which is right for one paragraph and wrong
    for the multi-paragraph ``differences`` and ``note`` fields, so each paragraph is wrapped alone.
    """
    paragraphs = [block for block in re.split(r"\n[ \t]*\n", text.strip()) if block.strip()]
    return "\n\n".join(renderer().wrap(paragraph) for paragraph in paragraphs)


def linkify_ids(text: str, known_ids: set[str], link: str) -> str:
    """Point a code span naming another ledger id at that capability's entry on the parity page.

    ``render_parity_page`` does the same thing with a bare fragment, because there the target is the
    same page. Here the target is another page, so the fragment needs the path in front of it.
    """

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        return f"[`{name}`]({link}#{name})" if name in known_ids else match.group(0)

    return re.sub(r"`([A-Za-z0-9][A-Za-z0-9-]*)`", replace, text)


def _states(capability: Any) -> str:
    module = renderer()
    python = module.state_label(capability.python, capability.absence_kind)
    javascript = module.state_label(capability.typescript, capability.absence_kind)
    return f"Python {python}, JavaScript {javascript}"


def _full_entry(capability: Any, link: str) -> str:
    return (
        f"The full entry, including the vocabulary this capability owns, is on "
        f"[the capability parity page]({link}#{capability.capability_id})."
    )


def _partial_notice(capability: Any, link: str, known_ids: set[str]) -> Notice:
    module = renderer()
    differing = [
        language
        for language, state in ((module.PYTHON, capability.python), (module.JAVASCRIPT, capability.typescript))
        if state == "partial"
    ]
    where = " and ".join(differing)
    lead = (
        f"**{capability.title}** exists in both libraries and does not behave the same way in "
        f"{where}. The ledger records it as {_states(capability)}, and what differs is stated here "
        "rather than left to be discovered."
    )
    return Notice(
        kind="info",
        title=f"Differs in {where}",
        paragraphs=(
            renderer().wrap(lead),
            wrap_prose(linkify_ids(capability.differences or "", known_ids, link)),
            renderer().wrap(_full_entry(capability, link)),
        ),
    )


def _permanent_notice(capability: Any, link: str, known_ids: set[str]) -> Notice:
    present = capability.present_language
    absent = capability.absent_language
    title = f"{present} only, permanently" if present else "Permanently absent"
    if absent and present:
        lead = (
            f"**{capability.title}** belongs to {present} alone. {absent} is not waiting on a port "
            "and will not gain a counterpart: this is a permanent boundary, so no issue tracks it, "
            "and moving the capability out of that state takes a constitutional amendment rather "
            "than a ledger edit."
        )
    else:
        lead = (
            f"**{capability.title}** is permanently absent. No issue tracks it, because there is "
            "nothing here awaiting work."
        )
    return Notice(
        kind="abstract",
        title=title,
        paragraphs=(
            renderer().wrap(lead),
            wrap_prose(linkify_ids(capability.note or "", known_ids, link)),
            renderer().wrap(_full_entry(capability, link)),
        ),
    )


def _gap_notice(capability: Any, link: str) -> Notice:
    absent = capability.absent_language
    present = capability.present_language
    title = f"Not in {absent} yet" if absent else "Not implemented yet"
    if absent and present:
        lead = f"**{capability.title}** is available in {present} and is not in {absent} today."
    else:
        lead = f"**{capability.title}** is not available today."
    lead += " A temporary gap, not a boundary. " + renderer().issue_sentence(capability.issue or "")
    return Notice(
        kind="warning",
        title=title,
        paragraphs=(renderer().wrap(lead), renderer().wrap(_full_entry(capability, link))),
    )


def build_notices(capability: Any, link: str, known_ids: set[str]) -> tuple[Notice, ...]:
    """Every block one capability contributes to a page. Empty when both libraries carry it in full.

    A capability that is complete on both sides renders nothing at all, not an empty admonition: a
    reader on a page with no parity story to tell should see no furniture about parity.
    """
    notices: list[Notice] = []
    if capability.has_partial:
        notices.append(_partial_notice(capability, link, known_ids))
    if capability.has_absence:
        if capability.absence_kind == "never":
            notices.append(_permanent_notice(capability, link, known_ids))
        else:
            notices.append(_gap_notice(capability, link))
    return tuple(notices)


# ---------------------------------------------------------------------------
# Substituting the token
# ---------------------------------------------------------------------------


def parity_page_link(src_uri: str) -> str:
    """The path from the page being rendered to the parity page, as MkDocs resolves links."""
    directory = posixpath.dirname(src_uri)
    return posixpath.relpath(PARITY_PAGE, directory or ".")


def resolve(capability_id: str, src_uri: str, capabilities: Mapping[str, Any]) -> Any:
    """The capability this id names, or a build failure that says what to write instead (T126)."""
    capability = capabilities.get(capability_id)
    if capability is not None:
        return capability
    close = difflib.get_close_matches(capability_id, sorted(capabilities), n=3, cutoff=0.4)
    suggestion = f"\n  Closest ids in the ledger: {', '.join(close)}." if close else ""
    message = (
        f'docs/{src_uri}: parity("{capability_id}") does not name a capability in the parity '
        f"ledger.{suggestion}\n"
        f"  Ids are stable and every one of them is listed on docs/{PARITY_PAGE}. The macro fails "
        "the build rather than render an empty block, because a silently missing parity statement "
        "reads to a user as a capability that has no difference to report."
    )
    raise PluginError(message)


def substitute(markdown: str, src_uri: str, capabilities: Mapping[str, Any]) -> str:
    """Replace every parity token on a page, leaving fenced code and every other brace alone."""
    link = parity_page_link(src_uri)
    known_ids = set(capabilities)
    out: list[str] = []
    fence: str | None = None

    for line in markdown.split("\n"):
        opener = FENCE.match(line)
        if opener is not None:
            marker = opener.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            out.append(line)
            continue

        if fence is not None or not line.lstrip().startswith("{{"):
            out.append(line)
            continue

        match = TOKEN.match(line)
        if match is None:
            if MALFORMED.search(line):
                message = (
                    f"docs/{src_uri}: {line.strip()!r} looks like the parity macro and does not "
                    'parse. Write it as {{ parity("capability-id") }} on a line of its own.'
                )
                raise PluginError(message)
            out.append(line)
            continue

        capability = resolve(match.group("id"), src_uri, capabilities)
        notices = build_notices(capability, link, known_ids)
        if notices:
            out.append("\n".join(notice.render() for notice in notices))

    return "\n".join(out)


def declares_a_capability(markdown: str) -> bool:
    """Whether a page opens a line with something that wants to be a parity call.

    Cheap and deliberately loose: it decides only whether this page is worth reading the ledger
    for, and ``substitute`` still makes every real decision. Loose in the safe direction, too. It
    accepts a malformed call so that the failure below reports it, and it ignores a token shown
    inline in prose, so a page that talks about the macro does not pull the ledger in.
    """
    return any(line.lstrip().startswith("{{") and "parity" in line for line in markdown.split("\n"))


def on_page_markdown(markdown: str, page: Page, config: Any, files: Any) -> str:
    """MkDocs event: substitute the parity tokens on one page."""
    if not declares_a_capability(markdown):
        return markdown
    return substitute(markdown, page.file.src_uri, ledger().capabilities)
