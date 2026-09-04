"""Guard that the bundled agent references match their source.

The agent reference docs are generated: the example code lives in pyright-checked
snippet files under ``agent_references/snippets/`` and the prose lives in templates
under ``agent_references/templates/``. ``bake_references`` inlines the snippet
sections into the bundled, wheel-packaged markdown at
``src/idfkit/.agents/skills/developing-with-idfkit/``.

Both source directories used to sit under ``docs/`` and the 16 topics were also
published on the site. Feature 003 moved the site out of this repository and retired
the published copies rather than moving these with it: the skill loads the reference
set baked into the idfkit version installed in the reader's project, and a published
page can only show the one version the site pins, so the published copy was the only
one that could be wrong for a given reader.

Correctness of the *code* is enforced by pyright (``make check`` runs pyright over
``agent_references/snippets`` with a strict execution environment scoped to it). This
test only guards that the committed bundle is in sync with its source — the same
contract ``make check``'s ``check-baker`` target enforces, but available under
``make test`` too and without shelling out.
"""

from __future__ import annotations

from pathlib import Path

from idfkit.codegen.bake_references import bake_markdown

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SOURCE_DIR = _REPO_ROOT / "agent_references" / "templates"
_SKILL_DIR = _REPO_ROOT / "src" / "idfkit" / ".agents" / "skills" / "developing-with-idfkit"


def _baked_sources() -> list[Path]:
    """Source templates the baker turns into bundle files.

    ``index.md`` is the docs-site landing page for the section, not a reference
    topic, so the baker skips it and so must the sync assertions below.
    """
    return [p for p in sorted(_SOURCE_DIR.glob("*.md")) if p.name != "index.md"]


def _source_to_bundle(source: Path) -> Path:
    """Map a source template path to its baked destination."""
    if source.name == "SKILL.md":
        return _SKILL_DIR / "SKILL.md"
    return _SKILL_DIR / "references" / source.name


def test_source_templates_exist() -> None:
    sources = _baked_sources()
    assert sources, "no agent-reference source templates found"
    # SKILL.md + 16 topic references. index.md is not here: it is the site's landing page
    # for the skill and was never baked, so it stayed with the site.
    assert len(sources) == 17, f"expected 17 source templates, found {len(sources)}"


def test_bundle_in_sync_with_source() -> None:
    """Each committed bundle file must equal a fresh bake of its source.

    If this fails, run: uv run python -m idfkit.codegen.bake_references
    """
    for source in _baked_sources():
        expected = bake_markdown(source.read_text(encoding="utf-8"))
        bundle = _source_to_bundle(source)
        assert bundle.is_file(), f"missing bundled file for {source.name}; run the baker"
        actual = bundle.read_text(encoding="utf-8")
        assert actual == expected, (
            f"{bundle.relative_to(_REPO_ROOT)} is out of sync with "
            f"{source.relative_to(_REPO_ROOT)}; run: "
            "uv run python -m idfkit.codegen.bake_references"
        )


def test_bundle_has_no_unresolved_includes() -> None:
    """No baked reference may still contain a pymdownx snippet directive."""
    for bundled in (_SKILL_DIR / "references").glob("*.md"):
        text = bundled.read_text(encoding="utf-8")
        assert "--8<--" not in text, f"{bundled.name} has an unresolved include directive"
