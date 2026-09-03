"""Put the levels this site was built from in front of the reader, on every page (FR-063, SC-023).

A page of reference material describes some particular version of something. This site's
TypeScript reference is generated from an artifact pinned at a `docs-YYYY.N` tag, and its parity
and naming claims are read at a `governance-YYYY.N` tag, and both of those are invisible to a
reader looking at the page. SC-023 says they should not be: someone comparing what the site says
against what their installed copy does needs to know which copy the site is describing.

So three values reach every template through `config.extra`:

    conformance_level   the corpus level the Python library declares it passes (FR-024)
    governance_level    the tag the parity ledger and naming register were read at (FR-081)
    docs_level          the tag the TypeScript examples and reference came from (FR-062, FR-064)

WHERE THEY COME FROM, AND WHY NOT FROM mkdocs.yml

Every one of them is already declared in `pyproject.toml`, and restating them here would make two
facts out of one apiece. That failure has happened on this site before: `explanation/naming-map.md`
told readers it was generated at `governance-2026.6` while the release pinned 2026.7, because
advancing the pin had not re-rendered the page and nothing caught it.

A documentation tree copied out of the repository has no `pyproject.toml`, which is ordinary
rather than degraded: the portable build passes each level down through the environment, from the
same pin the repository declares. That is why every read here has an environment variable ahead of
it, and why this hook computes no path out of its own location.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - 3.10 only
    import tomli as tomllib  # pyright: ignore[reportMissingImports]

#: `(config.extra key, [tool.idfkit.<section>] level, environment override)`.
_LEVELS: tuple[tuple[str, str, str], ...] = (
    ("conformance_level", "conformance", "IDFKIT_CONFORMANCE_LEVEL"),
    ("governance_level", "governance", "IDFKIT_GOVERNANCE_LEVEL"),
    ("docs_level", "docs", "IDFKIT_DOCS_LEVEL"),
)


def _declared(section: str, pyproject: Path) -> str | None:
    if not pyproject.is_file():
        return None
    with pyproject.open("rb") as handle:
        document: dict[str, Any] = tomllib.load(handle)
    level = document.get("tool", {}).get("idfkit", {}).get(section, {}).get("level")
    return level if isinstance(level, str) and level else None


def on_config(config: Any) -> Any:
    """Resolve each pinned level and hand it to the templates."""
    # Path.cwd(), never a path derived from __file__. mkdocs runs from the directory holding
    # mkdocs.yml, which is the repository root here and the scratch directory in the portable
    # build; there, the file is absent and the environment answers instead.
    pyproject = Path.cwd() / "pyproject.toml"
    missing: list[str] = []
    for key, section, variable in _LEVELS:
        level = os.environ.get(variable) or _declared(section, pyproject)
        if level is None:
            missing.append(f"[tool.idfkit.{section}] level, or ${variable}")
            continue
        config.extra[key] = level
    if missing:
        # Not a warning. A site that silently omits the level it was built from is exactly what
        # SC-023 forbids, and a build that cannot state one has nothing useful to publish.
        raise SystemExit(
            "the site cannot state which levels it was built from. Declare each of:\n  " + "\n  ".join(missing)
        )
    return config
