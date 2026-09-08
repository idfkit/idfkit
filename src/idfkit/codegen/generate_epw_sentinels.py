"""Generate ``idfkit.weather._epw_sentinels`` from the corpus's reserved-value table.

WHY GENERATED AND NOT WRITTEN

The table says, per EPW field, which values are reserved and which of those mean "not measured".
It is one table serving both libraries, read from the EnergyPlus Weather File Data Dictionary and
committed in ``checks/weather-monthly/sentinels.toml`` beside the check that catches a wrong
entry. Transcribing it here would make two tables out of one, and the second would drift in the
direction nobody is watching: a wrong entry does not throw, it moves a monthly mean.

WHY THE GENERATED ARTIFACT IS PYTHON AND NOT THE TOML ITSELF

This language has both a filesystem and a TOML parser, so reading the table at import time would
work. It is still generated, for two reasons. The value crosses the build boundary the same way
``_conformance.py`` and ``_generated_types.pyi`` already do, so a wheel carries the table without
carrying a data file the packaging has to remember. And the JavaScript library MUST generate, its
portable surface having no filesystem, no TOML parser and no dependencies; generating on both
sides means the two libraries hold the table in the same shape and a difference between them is a
difference in the corpus rather than in how each read it.

WHY IT READS A TAG

The same reason the naming gate does: reading the corpus's default branch would let that
repository change this library's behaviour with no review on this side. The tag is
``[tool.idfkit.conformance] level`` in ``pyproject.toml``, because the reserved-value table lives
under ``checks/`` and ``checks/`` is what a conformance level covers.

``--ref`` exists for developing against a level that has not been cut yet, announces itself in the
output every time it is used, and does not lift the requirement that a pin be declared.

The drift is caught rather than trusted: ``make check-epw-sentinels`` regenerates and diffs, so an
edit to the emitted module, or a corpus that moved under the pin, fails the build instead of
shipping a table nobody read.

Usage::

    python -m idfkit.codegen.generate_epw_sentinels [--corpus PATH] [--ref REF]
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Final

import tomllib

_REPO_ROOT: Final = Path(__file__).resolve().parents[3]
_OUTPUT_PATH: Final = Path(__file__).resolve().parents[1] / "weather" / "_epw_sentinels.py"
_TABLE_PATH: Final = "checks/weather-monthly/sentinels.toml"
_LEVEL_PATTERN: Final = re.compile(r"^conformance-\d{4}\.\d+$")

_TEMPLATE: Final = '''"""Auto-generated EPW reserved-value table.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_epw_sentinels

Emitted from {table} in idfkit-conformance at {level}.

Source document: {document}
Versions checked: {versions}
{url}

WHAT IS HERE AND WHAT IS NOT. Only the values that mean "not measured". A field may also reserve
values that are observations — ceiling height's 77777 for an unlimited ceiling and 88888 for a
cirroform one — and those are deliberately absent, because the reader's rule is to blank what this
table lists and to leave every other number alone. A reader that instead blanked "large numbers"
would blank 55% of the ceiling column in the sampled corpus.
"""

from __future__ import annotations

from typing import Final

#: Per numeric column position, the values that mean the measurement was not made. Positions absent
#: from this table reserve nothing.
MISSING_VALUES: Final[tuple[tuple[int, tuple[float, ...]], ...]] = (
{rows}
)

#: The conformance level this table was generated from.
SENTINEL_LEVEL: Final[str] = "{level}"
'''


def declared_level(repo_root: Path) -> str:
    """Return ``[tool.idfkit.conformance] level``, or refuse to guess one."""
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        sys.exit(f"No pyproject.toml at {pyproject}; there is no declaration to generate from.")
    data: dict[str, Any] = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    level = data.get("tool", {}).get("idfkit", {}).get("conformance", {}).get("level")
    if not isinstance(level, str) or not level:
        sys.exit(
            "No conformance level is declared in pyproject.toml.\n"
            '  Add [tool.idfkit.conformance] level = "conformance-YYYY.N".'
        )
    if not _LEVEL_PATTERN.match(level):
        sys.exit(
            f"The declared conformance level {level!r} is not an immutable conformance-YYYY.N tag.\n"
            "  A generated table cannot come from a branch: it moves after the code ships."
        )
    return level


def resolve_corpus(explicit: str | None) -> Path:
    """An idfkit-conformance checkout to read the table out of."""
    candidates = (
        [Path(explicit)]
        if explicit
        else [
            Path(p)
            for p in (
                os.environ.get("IDFKIT_CONFORMANCE_DIR"),
                _REPO_ROOT / "conformance",
                _REPO_ROOT.parent / "idfkit-conformance",
            )
            if p
        ]
    )
    for candidate in candidates:
        if (candidate.expanduser().resolve() / ".git").exists():
            return candidate.expanduser().resolve()
    listed = "\n".join(f"    {c}" for c in candidates)
    sys.exit(f"No idfkit-conformance checkout found. Looked at:\n{listed}\n\nClone it, or pass --corpus PATH.")


def read_table(corpus: Path, ref: str) -> str:
    """Read the table at one ref."""
    shown = subprocess.run(  # noqa: S603
        # `git` off PATH, and a ref this repository authored rather than one a caller supplied.
        # The two sibling gates that read governance at a tag do exactly the same.
        ["git", "show", f"{ref}:{_TABLE_PATH}"],  # noqa: S607
        cwd=corpus,
        capture_output=True,
        text=True,
        check=False,
    )
    if shown.returncode != 0:
        sys.exit(
            f"Could not read {_TABLE_PATH} at {ref} in {corpus}.\n"
            f"  {shown.stderr.strip()}\n"
            "  Fetch the corpus, or pass --ref to generate against a level that is not cut yet."
        )
    return shown.stdout


def render(document: dict[str, Any], level: str) -> str:
    """The generated module's text."""
    entries: list[tuple[int, tuple[float, ...]]] = []
    for field in document.get("field", []):
        missing = tuple(value["value"] for value in field.get("values", []) if value["kind"] == "missing")
        if not missing:
            continue
        entries.append((field["position"], missing))
    entries.sort()

    names = {field["position"]: field["field"] for field in document.get("field", [])}
    rows = "\n".join(
        f"    # {names[position]}\n    ({position}, ({', '.join(repr(v) for v in values)},)),"
        for position, values in entries
    )
    source = document.get("source", {})
    return _TEMPLATE.format(
        table=_TABLE_PATH,
        level=level,
        document=source.get("document", "unknown"),
        versions=", ".join(source.get("versions_checked", [])),
        url=source.get("url", ""),
        rows=rows,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="generate_epw_sentinels", description=__doc__)
    parser.add_argument("--corpus", help="An idfkit-conformance checkout to read the table out of.")
    parser.add_argument("--ref", help="Read at this ref rather than at the pinned conformance level.")
    args = parser.parse_args(argv)

    level = declared_level(_REPO_ROOT)
    corpus = resolve_corpus(args.corpus)
    ref = args.ref or level
    if args.ref:
        print(
            f"NOTE: reading the table at {args.ref} rather than at the pinned {level}.\n"
            "      This is for developing against a level that has not been cut. A build must not rely on it."
        )

    document = tomllib.loads(read_table(corpus, ref))
    _OUTPUT_PATH.write_text(render(document, ref if args.ref else level), encoding="utf-8")
    print(f"Wrote {_OUTPUT_PATH.relative_to(_REPO_ROOT)} from {ref} in {corpus}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
