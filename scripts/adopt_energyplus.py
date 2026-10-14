#!/usr/bin/env python3
"""Perform the two edits of an EnergyPlus release adoption that no existing command performs.

The adoption procedure is held in idfkit-conformance (``energyplus/README.md``) and its roster
(``governance/energyplus.toml``) names one command per step. Five steps of this project already
have a command. Two did not, and were hand edits:

1. ``register``   adds the release to ``ENERGYPLUS_VERSIONS`` in ``src/idfkit/versions.py``.
   ``LATEST_VERSION`` is the last entry of that tuple and needs no edit of its own.
2. ``sweep-row``  adds the release's row to the example sweep matrix in
   ``.github/workflows/main.yml``, with the two counts measured by reading that release's example
   files with ``scripts/sweep_example_files.py``. No EnergyPlus installation is required: the
   files are fetched by the same sparse clone the workflow uses, and they are parsed against the
   bundled schema, which must therefore be present first.

Both subcommands are idempotent. A release that is already present is reported and left as it is,
and ``sweep-row`` then measures nothing.

The counts ``sweep-row`` writes become ceilings in continuous integration. They are printed with
the per-code breakdown so that a reviewer can compare them with the sweep's log before accepting.

Exit codes: 0 the release is present, 1 the edit could not be made, 2 the arguments could not be
read.

Usage::

    uv run python scripts/adopt_energyplus.py register 26.2.0
    uv run python scripts/adopt_energyplus.py sweep-row 26.2.0
    uv run python scripts/adopt_energyplus.py sweep-row 26.2.0 --examples path/to/testfiles
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_VERSIONS = _REPO_ROOT / "src" / "idfkit" / "versions.py"
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "main.yml"
_SPARSE = _REPO_ROOT / ".github" / "ep-testfiles.sparse"
_SCHEMAS = _REPO_ROOT / "src" / "idfkit" / "schemas"

# The canonical name of the upstream repository, as in the workflow's own fetch step.
_UPSTREAM = "https://github.com/NatLabRockies/EnergyPlus"

_REGISTRY = re.compile(
    r"(?P<head>^ENERGYPLUS_VERSIONS: [^\n]*= \(\n)(?P<rows>(?:[ \t]*\(\d+, \d+, \d+\),\n)+)(?P<tail>\)\n)",
    re.MULTILINE,
)
_REGISTRY_ROW = re.compile(r"\((\d+), (\d+), (\d+)\),")

_MATRIX = re.compile(
    r'(?P<rows>(?:^[ \t]*- \{ version: "\d+\.\d+\.\d+", findings: \d+, errors: \d+ \}\n)+)',
    re.MULTILINE,
)
_MATRIX_ROW = re.compile(r'^(?P<indent>[ \t]*)- \{ version: "(?P<version>\d+\.\d+\.\d+)", findings: ', re.MULTILINE)


class AdoptionError(Exception):
    """An edit could not be made, with the reason stated for the person reading the log."""


@dataclass(frozen=True, order=True, slots=True)
class Release:
    """An EnergyPlus release, ordered as its three numbers."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, text: str) -> Release:
        match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", text)
        if match is None:
            raise argparse.ArgumentTypeError(f"{text!r} is not an EnergyPlus release of the form X.Y.Z")
        return cls(int(match[1]), int(match[2]), int(match[3]))

    @property
    def full(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def tag(self) -> str:
        return f"v{self.full}"

    @property
    def directory(self) -> str:
        return f"V{self.major}-{self.minor}-{self.patch}"

    @property
    def tuple_literal(self) -> str:
        return f"({self.major}, {self.minor}, {self.patch})"


@dataclass(frozen=True, slots=True)
class Edit:
    """The text of a file after an edit, and whether the edit changed it."""

    text: str
    changed: bool


@dataclass(frozen=True, slots=True)
class Measurement:
    """What reading one release's example files produced."""

    files: int
    findings: int
    errors: int


# ── register ───────────────────────────────────────────────────────────────────────────────────────


def register(text: str, release: Release) -> Edit:
    """Return ``versions.py`` with the release listed in ``ENERGYPLUS_VERSIONS``, in ascending order."""
    match = _REGISTRY.search(text)
    if match is None:
        raise AdoptionError("ENERGYPLUS_VERSIONS was not found as a tuple of one (major, minor, patch) per line")
    listed = [Release(int(a), int(b), int(c)) for a, b, c in _REGISTRY_ROW.findall(match["rows"])]
    if release in listed:
        return Edit(text, changed=False)
    prefix = match["rows"][: len(match["rows"]) - len(match["rows"].lstrip(" \t"))]
    rows = "".join(f"{prefix}{entry.tuple_literal},\n" for entry in sorted([*listed, release]))
    return Edit(text[: match.start("rows")] + rows + text[match.end("rows") :], changed=True)


# ── sweep-row ──────────────────────────────────────────────────────────────────────────────────────


def has_row(text: str, release: Release) -> bool:
    return any(found["version"] == release.full for found in _MATRIX_ROW.finditer(text))


def _row_release(line: str) -> Release:
    found = _MATRIX_ROW.match(line)
    if found is None:
        raise AdoptionError(f"unreadable sweep matrix row: {line.strip()}")
    return Release.parse(found["version"])


def add_row(text: str, release: Release, findings: int, errors: int) -> Edit:
    """Return ``main.yml`` with the release's row in the sweep matrix, in ascending order."""
    if has_row(text, release):
        return Edit(text, changed=False)
    blocks = list(_MATRIX.finditer(text))
    if len(blocks) != 1:
        raise AdoptionError(f"expected one block of sweep matrix rows in main.yml, found {len(blocks)}")
    block = blocks[0]
    lines = block["rows"].splitlines(keepends=True)
    first = _MATRIX_ROW.match(lines[0])
    indent = first["indent"] if first else "          "
    new = f'{indent}- {{ version: "{release.full}", findings: {findings}, errors: {errors} }}\n'
    position = sum(1 for line in lines if _row_release(line) < release)
    lines.insert(position, new)
    return Edit(text[: block.start()] + "".join(lines) + text[block.end() :], changed=True)


def sparse_patterns(text: str) -> list[str]:
    """The patterns of ``.github/ep-testfiles.sparse``: one per line, comments and blanks removed."""
    return [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]


def fetch_examples(release: Release, into: Path) -> Path:
    """Fetch the release's example files as the workflow does, and return the directory holding them."""
    clone = into / "ep"
    patterns = sparse_patterns(_SPARSE.read_text(encoding="utf-8"))
    commands = [
        ["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout", "--depth", "1", "--branch", release.tag, _UPSTREAM, str(clone)],
        ["git", "-C", str(clone), "sparse-checkout", "set", "--no-cone", *patterns],
        ["git", "-C", str(clone), "checkout", "--quiet"],
    ]  # fmt: skip
    for command in commands:
        done = subprocess.run(command, capture_output=True, text=True, check=False)  # noqa: S603
        if done.returncode != 0:
            raise AdoptionError(f"`{' '.join(command[:4])} ...` exited {done.returncode}: {done.stderr.strip()}")
    return clone / "testfiles"


def measure(directory: Path) -> Measurement:
    """Read every example file in the directory with the sweep the workflow runs."""
    import warnings

    import sweep_example_files

    files = sorted(directory.glob("*.idf"))
    if not files:
        # The same refusal as the sweep itself: an empty directory measures zero and proves nothing.
        raise AdoptionError(f"no .idf files under {directory}; nothing was measured")
    warnings.filterwarnings("ignore")
    result = sweep_example_files.sweep(files)
    sweep_example_files.report(result)
    return Measurement(files=result.files, findings=len(result.findings), errors=len(result.errors))


# ── Command line ───────────────────────────────────────────────────────────────────────────────────


def _write(path: Path, edit: Edit) -> None:
    if edit.changed:
        path.write_text(edit.text, encoding="utf-8")


def _register(release: Release) -> int:
    edit = register(_VERSIONS.read_text(encoding="utf-8"), release)
    _write(_VERSIONS, edit)
    print(f"{release.full} {'added to' if edit.changed else 'already listed in'} ENERGYPLUS_VERSIONS")
    return 0


def require_bundled_schema(release: Release, schemas: Path) -> None:
    """Refuse to measure a release whose schema is not bundled.

    Without it the counts written as this release's ceilings would not be this release's. A release
    that is not registered is read against the newest schema the library has, and a release that is
    registered without a schema makes every file unreadable, which the row would record as its
    permitted number of errors.
    """
    if not any((schemas / release.directory).glob("Energy+.schema.epJSON*")):
        raise AdoptionError(
            f"no bundled schema under {schemas / release.directory}; bundle it first with "
            f"`python -m idfkit.download {release.full} --target-dir src/idfkit/schemas`"
        )


def _sweep_row(release: Release, examples: Path | None) -> int:
    text = _WORKFLOW.read_text(encoding="utf-8")
    if has_row(text, release):
        print(f"{release.full} already has a row in the sweep matrix; nothing was measured")
        return 0
    require_bundled_schema(release, _SCHEMAS)
    with tempfile.TemporaryDirectory() as scratch:
        directory = examples if examples is not None else fetch_examples(release, Path(scratch))
        measured = measure(directory)
    _write(_WORKFLOW, add_row(text, release, measured.findings, measured.errors))
    print(
        f"\n{release.full} added to the sweep matrix: findings {measured.findings}, errors {measured.errors}, "
        f"measured over {measured.files} files"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="adopt_energyplus.py", description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    registry = commands.add_parser("register", help="list the release in ENERGYPLUS_VERSIONS")
    registry.add_argument("release", type=Release.parse, help="the EnergyPlus release, as X.Y.Z")
    row = commands.add_parser("sweep-row", help="add the release's measured row to the example sweep matrix")
    row.add_argument("release", type=Release.parse, help="the EnergyPlus release, as X.Y.Z")
    row.add_argument(
        "--examples",
        type=Path,
        default=None,
        help="a directory of that release's .idf example files (default: fetched from upstream)",
    )
    args = parser.parse_args(argv)

    try:
        if args.command == "register":
            return _register(args.release)
        return _sweep_row(args.release, args.examples)
    except AdoptionError as error:
        print(f"::error::{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
