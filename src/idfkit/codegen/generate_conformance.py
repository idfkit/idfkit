"""Generate ``idfkit._conformance`` from ``[tool.idfkit.conformance] level``.

FR-024 requires each release to state the conformance corpus level it passes, and requires
that statement to be readable from the installed library rather than only from its packaging
metadata. ``pyproject.toml`` is not shipped inside the wheel, so ``idfkit.CONFORMANCE_LEVEL``
cannot read the declaration at import time; the value has to cross the build boundary somehow.

It crosses as generated, committed source, the same way ``_generated_types.pyi`` and
``doc_locations.json`` already do. The declaration stays a single authored fact in
``pyproject.toml``, this module derives the constant from it, and ``make check`` regenerates
and diffs, so a level advanced in ``pyproject.toml`` and not here fails the build instead of
shipping a release whose exported claim is one tag stale.

The rejected alternative was reading ``pyproject.toml`` at import time. It works from a source
checkout and returns nothing from an installed wheel, which is the only place the constant is
worth having, and a constant that is correct only for maintainers is worse than no constant.

Usage::

    python -m idfkit.codegen.generate_conformance
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import tomllib

# tomllib unconditionally, so this module needs Python 3.11. That is a constraint on the
# maintainer running codegen, never on the library: the generated file is committed, and a
# reader on 3.10 imports a string constant that was produced elsewhere. The two sibling
# generators are the same kind of tool, and the CI gates already run on 3.11 for this reason.

_REPO_ROOT = Path(__file__).resolve().parents[3]
_OUTPUT_PATH = Path(__file__).resolve().parents[1] / "_conformance.py"

_TEMPLATE = '''"""Auto-generated conformance declaration.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_conformance

The value is derived from ``[tool.idfkit.conformance] level`` in ``pyproject.toml``, which is
the one place the level is authored. ``make check`` regenerates this file and diffs it, so the
declaration and the export cannot drift apart.
"""

from __future__ import annotations

from typing import Final

#: The conformance corpus level this release is checked against, as an immutable tag in
#: idfkit/idfkit-conformance. A release asserts this claim in its own checks (FR-024): the
#: corpus at this tag passes against this library, or the release does not ship.
#:
#: This is not a version number and it is not compared to one. Two installed libraries agree
#: on the formats when they declare the same level, whatever their own versions say (FR-025).
CONFORMANCE_LEVEL: Final[str] = "{level}"
'''


def read_declared_level(repo_root: Path) -> str:
    """Return ``[tool.idfkit.conformance] level``, or refuse to guess one."""
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        sys.exit(f"No pyproject.toml at {pyproject}; there is no declaration to generate from.")
    data: dict[str, Any] = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    tool: Any = data.get("tool", {})
    level: Any = tool.get("idfkit", {}).get("conformance", {}).get("level")
    if not isinstance(level, str) or not level:
        sys.exit(
            "No conformance level is declared in pyproject.toml.\n"
            '  Add [tool.idfkit.conformance] level = "conformance-YYYY.N".'
        )
    return level


def main() -> None:
    level = read_declared_level(_REPO_ROOT)
    _OUTPUT_PATH.write_text(_TEMPLATE.format(level=level), encoding="utf-8")
    print(f"Wrote {_OUTPUT_PATH.relative_to(_REPO_ROOT)} declaring {level}")


if __name__ == "__main__":
    main()
