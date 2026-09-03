#!/usr/bin/env python3
"""Every capability page declares the capability it describes (FR-047, SC-017).

WHAT THIS IS FOR

The parity ledger says which capabilities exist in which language. A reader does not visit the
ledger; they arrive on the page for the thing they want to do. FR-047 puts the answer where they
are, and the ``parity(id)`` macro renders it. This gate is what stops a page being added without
one, which is how availability quietly stops rendering at the point of use.

WHAT COUNTS AS A CAPABILITY PAGE

A page under ``docs/`` that shows code. A page with no example is prose about the project rather
than about an operation, and there is nothing on it whose availability could differ. That is a
deliberately mechanical test: it needs no list of pages to maintain, and a new page that teaches
an operation is caught on the day it is written.

THE EXEMPTIONS, AND WHY EACH IS ONE

``docs/agent-references/``   FR-059's declared Diataxis exception. It is bundled inside the Python
                             wheel and read by tooling, not by a person on the site, so a macro
                             that renders an admonition would put site markup into a shipped
                             artifact. It is Python material by construction.
``docs/index.md``            the site root: a landing page, not a page about an operation.
``docs/tutorials/index.md``  and the other section landing pages, for the same reason.

Everything else is either declared or reported. There is no allowlist of pages that are exempt
"for now": a page that shows code and names no capability is a finding, and the fix is to name
one, not to add it here.

Exit codes: 0 every capability page declares one, 1 some do not, 2 the gate could not run.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"

EXEMPT_PREFIXES = (
    "agent-references/",
    # Build wiring rather than pages, and excluded from the site in mkdocs.yml for the same
    # reason. They live under docs/ only because `custom_templates:` and the TypeDoc shim resolve
    # relative to it and have to survive the portable build.
    "templates/",
    "typedoc/",
    "hooks/",
    # Generated reference. Every symbol on these pages comes from the TypeDoc artifact, and the
    # capability a package covers is stated on the task and explanation pages that teach it, where
    # a reader deciding whether an operation exists in their language actually is.
    "reference/typescript/",
)
EXEMPT_PAGES = frozenset({
    "index.md",
    "tutorials/index.md",
    "how-to/index.md",
    "reference/index.md",
    "explanation/index.md",
    "api/index.md",
    # Installation is about packaging, not about an operation. The page teaches both ecosystems
    # side by side and its subject is exactly the difference between them, so a statement that a
    # capability is absent in one language has nothing to attach to.
    "getting-started/installation.md",
})

CODE_FENCE = re.compile(r"^```(python|py|ts|typescript)\b", re.M)
DECLARATION = re.compile(r"\{\{\s*parity\(")


def is_exempt(relative: str) -> bool:
    return relative in EXEMPT_PAGES or any(relative.startswith(p) for p in EXEMPT_PREFIXES)


def main() -> int:
    if not DOCS.is_dir():
        print(f"No documentation tree at {DOCS}.", file=sys.stderr)
        return 2

    undeclared: list[str] = []
    declared = 0
    exempt = 0
    for page in sorted(DOCS.rglob("*.md")):
        relative = page.relative_to(DOCS).as_posix()
        if is_exempt(relative):
            exempt += 1
            continue
        text = page.read_text(encoding="utf-8")
        if not CODE_FENCE.search(text):
            continue
        if DECLARATION.search(text):
            declared += 1
        else:
            undeclared.append(relative)

    print(f"Capability pages: {declared} declared, {len(undeclared)} undeclared, {exempt} exempt.")
    if undeclared:
        print(
            "\n❌ These pages show code and name no capability, so a reader cannot see from the\n"
            "   page whether the operation exists in their language (FR-047, SC-017):",
            file=sys.stderr,
        )
        for relative in undeclared:
            print(f"     {relative}", file=sys.stderr)
        print(
            '\n   Add {{ parity("<id>") }} after the page\'s opening prose, naming the ledger\n'
            "   capability the page is about. The macro fails the build on an unknown id, so a\n"
            "   typo cannot render an empty block.",
            file=sys.stderr,
        )
        return 1
    print("✅ Every capability page declares the capability it describes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
