#!/usr/bin/env python3
"""The site hosts no engine bytes, and the build fetched none (FR-072, SC-027).

The browser-simulation pages document a 51 MB WebAssembly build of EnergyPlus and embed a runner
that executes it. Everything it needs comes from a CDN, at the moment a reader presses a button.
This is the check that keeps it that way, because the two ways it stops being true are both quiet:

WHAT IS ASSERTED

1.  The built site hosts no `.wasm` file, and no other file large enough to be an engine asset
    that arrived by accident. A copied binary would be served from this origin to every reader
    who opened the page, whether or not they pressed anything.

2.  No page, script or stylesheet in the built site references an engine asset in a way a browser
    acts on before a reader asks. A `<link rel=preload>`, a `<link rel=prefetch>`, an
    `import` at parse time, or a `<script src>` pointing at the CDN copy all defeat the whole
    arrangement while leaving the site's own byte count unchanged. Naming the CDN in prose, in a
    `data-` attribute the runner reads on click, or inside a `const` in the runner is fine and is
    what the page is for.

WHAT IS NOT ASSERTED

That the runner works. Nothing here executes JavaScript.

Exit codes: 0 the site is clean, 1 it is not, 2 the check could not run.

Usage::

    python scripts/check_engine_assets.py            # default: ./site
    python scripts/check_engine_assets.py path/to/site
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CANNOT_RUN = 2

#: A binary this size did not come from a documentation page. Applied to NON-TEXT files only:
#: the generated Python reference produces one HTML page of 28 MB, which is a real problem and a
#: different one, and a check that conflated it with a stray WebAssembly binary would be wrong
#: about both.
LARGE_BINARY_BYTES = 8 * 1024 * 1024

#: Extensions a WebAssembly build arrives with.
BINARY_SUFFIXES = frozenset({".wasm", ".wat"})

#: A reference the browser acts on without being asked. Each is matched against the rendered
#: HTML, CSS and JavaScript of the built site.
EAGER_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("preload or prefetch", re.compile(r"<link[^>]+rel=[\"']?(?:preload|prefetch|modulepreload)[^>]*engine", re.I)),
    ("script src", re.compile(r"<script[^>]+src=[\"'][^\"']*@idfkit/engine", re.I)),
    ("static import", re.compile(r"^\s*import\s[^;\n]*['\"][^'\"]*@idfkit/engine", re.M)),
)

TEXT_SUFFIXES = frozenset({".html", ".js", ".css", ".mjs"})


def hosted_binaries(site: Path) -> list[str]:
    """Engine bytes served from this origin: a WebAssembly file, or any large non-text file."""
    findings: list[str] = []
    for path in sorted(site.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        size = path.stat().st_size
        if suffix in BINARY_SUFFIXES:
            findings.append(f"  hosts a WebAssembly file: {path.relative_to(site)} ({size:,} bytes)")
        elif suffix not in TEXT_SUFFIXES and size >= LARGE_BINARY_BYTES:
            findings.append(f"  hosts a {size:,}-byte binary: {path.relative_to(site)}")
    return findings


def eager_references(site: Path) -> list[str]:
    """References a browser acts on before a reader presses anything."""
    findings: list[str] = []
    for path in sorted(site.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.relative_to(site).parts[:1] == ("snippets",):
            # The snippet tree is source on display, published the same way the Python snippets
            # are. live_runner.js genuinely contains `import ... from '@idfkit/engine'`, because
            # that is the example; nothing on the site loads it as a module. The runner fetches it
            # as TEXT, rewrites the specifier, and evaluates a blob, which is the whole reason the
            # rewrite exists. Flagging it would mean the example could not show its own imports.
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "@idfkit/engine" not in text:
            continue
        findings.extend(
            f"  {label} of an engine asset in {path.relative_to(site)}"
            for label, pattern in EAGER_PATTERNS
            if pattern.search(text)
        )
    return findings


def main() -> int:
    site = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "site"
    if not site.is_dir():
        print(f"No built site at {site}. Run `mkdocs build` first.", file=sys.stderr)
        return CANNOT_RUN

    findings = hosted_binaries(site) + eager_references(site)
    wasm = sum(1 for p in site.rglob("*") if p.is_file() and p.suffix.lower() in BINARY_SUFFIXES)
    total = sum(p.stat().st_size for p in site.rglob("*") if p.is_file())
    print(f"Built site: {total:,} bytes, {wasm} WebAssembly file(s).")

    if findings:
        print(
            "\n❌ The site would serve engine bytes, or ask a browser to fetch them before a "
            "reader does (FR-072, SC-027):",
            file=sys.stderr,
        )
        for line in findings:
            print(line, file=sys.stderr)
        print(
            "\n   The engine is reached from the CDN on activation and from nowhere else. If a "
            "page needs to name it, name it in prose or in a data- attribute the runner reads "
            "when the reader presses the button.",
            file=sys.stderr,
        )
        return 1
    print("✅ No engine bytes are hosted, and nothing fetches them before a reader asks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
