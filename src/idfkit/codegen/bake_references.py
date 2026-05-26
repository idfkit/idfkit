"""Bake agent reference docs from source templates + verified snippets.

The agent reference docs have two source-of-truth inputs:

* ``docs/agent-references/<topic>.md`` — prose + ``pymdownx.snippets`` include
  directives for verified code + inline fenced blocks for intentionally-wrong
  "BAD" examples.
* ``docs/snippets/agent_references/<topic>.py`` — the verified example code,
  type-checked by pyright (``make check`` runs ``pyright … docs/snippets``).

This module flattens the include directives — pulling the marked region out of
each snippet and inlining it — to produce the bundled, wheel-packaged copies at
``src/idfkit/.agents/skills/developing-with-idfkit/references/<topic>.md`` that
idfkit-mcp serves over MCP. MkDocs renders the same source templates via
``pymdownx.snippets`` for the docs site, so the two stay in lock-step.

Run via ``python -m idfkit.codegen.bake_references``. A ``check-baker`` Makefile
target regenerates and ``git diff --exit-code``s the output, mirroring
``check-stubs``.
"""

from __future__ import annotations

import re
from pathlib import Path

# src/idfkit/codegen/bake_references.py -> repo root
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SOURCE_DIR = _REPO_ROOT / "docs" / "agent-references"
_SKILL_DIR = _REPO_ROOT / "src" / "idfkit" / ".agents" / "skills" / "developing-with-idfkit"
_REFERENCES_OUT = _SKILL_DIR / "references"

# A pymdownx.snippets include line: optional indent, then --8<-- "path:section".
_INCLUDE_RE = re.compile(r'^(?P<indent>\s*)--8<--\s+"(?P<spec>[^"]+)"\s*$')


def _extract_section(snippet_path: Path, section: str) -> list[str]:
    """Return the lines between ``[start:section]`` and ``[end:section]`` markers."""
    start = f"# --8<-- [start:{section}]"
    end = f"# --8<-- [end:{section}]"
    lines = snippet_path.read_text(encoding="utf-8").splitlines()
    try:
        i = lines.index(start)
        j = lines.index(end, i + 1)
    except ValueError as exc:
        msg = f"Section {section!r} not found in {snippet_path.relative_to(_REPO_ROOT)}"
        raise SystemExit(msg) from exc
    return lines[i + 1 : j]


def bake_markdown(source_text: str) -> str:
    """Resolve every ``--8<--`` include in *source_text* to inline content."""
    out: list[str] = []
    for line in source_text.splitlines():
        match = _INCLUDE_RE.match(line)
        if match is None:
            out.append(line)
            continue
        spec = match.group("spec")
        indent = match.group("indent")
        path_part, _, section = spec.rpartition(":")
        snippet_path = _REPO_ROOT / path_part
        if not snippet_path.is_file():
            msg = f"Snippet not found: {path_part}"
            raise SystemExit(msg)
        for snippet_line in _extract_section(snippet_path, section):
            out.append(indent + snippet_line if snippet_line else snippet_line)
    return "\n".join(out) + "\n"


def bake_all() -> list[Path]:
    """Bake every source template into the bundled references. Returns written paths."""
    if not _SOURCE_DIR.is_dir():
        msg = f"Source directory not found: {_SOURCE_DIR}"
        raise SystemExit(msg)

    written: list[Path] = []

    # SKILL.md sits at the skill root, one level above references/.
    skill_src = _SOURCE_DIR / "SKILL.md"
    if skill_src.is_file():
        baked = bake_markdown(skill_src.read_text(encoding="utf-8"))
        dest = _SKILL_DIR / "SKILL.md"
        dest.write_text(baked, encoding="utf-8")
        written.append(dest)

    _REFERENCES_OUT.mkdir(parents=True, exist_ok=True)
    for source in sorted(_SOURCE_DIR.glob("*.md")):
        if source.name == "SKILL.md":
            continue
        baked = bake_markdown(source.read_text(encoding="utf-8"))
        dest = _REFERENCES_OUT / source.name
        dest.write_text(baked, encoding="utf-8")
        written.append(dest)

    return written


def main() -> None:
    """CLI entry point."""
    written = bake_all()
    for path in written:
        print(f"Baked {path.relative_to(_REPO_ROOT)} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
