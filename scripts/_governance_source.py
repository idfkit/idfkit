"""Read a governance file at the immutable tag a release pins.

FR-081: governance is read at the ``governance-YYYY.N`` tag in
``[tool.idfkit.governance] level``, never from a branch and never from a working tree. A
moving source changes a verdict without any change landing in the repository being read,
which is the whole reason the pin exists.

Both page renderers claimed in their module docstrings that they did this, and neither did.
They read ``governance/*.toml`` straight off the sibling checkout, so ``--check`` passed or
failed on somebody's uncommitted edit, and a generated page could disagree with the two
things that *do* read at the tag: ``scripts/check_parity_ledger.py`` and the ``parity(id)``
documentation macro. A page and a gate that disagree is the failure the ledger header warns
about, committed in the tooling that renders the ledger.

Reading at a tag means the tag has to be fetched. That is a real new requirement for CI and
for a docs build, and it is the correct one: a build that quietly renders governance from
whatever happens to be on disk is worse than one that stops and says the tag is missing.

An explicit path is still honoured as a deliberate override, for a maintainer working on an
unreleased ledger, and it announces itself rather than passing silently for the pinned read.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GovernanceSource:
    """The text of a governance file, and an honest account of where it came from."""

    text: str
    description: str
    pinned: bool


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    # `git` from PATH with a fully argument-quoted command line. The ref comes from
    # pyproject.toml in this same checkout and no shell is involved.
    return subprocess.run(  # noqa: S603
        ["git", "-C", str(repo), *args],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )


def _toplevel(start: Path) -> Path:
    result = _run_git(start, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        sys.exit(
            f"{start} is not inside a git repository, so the governance tag cannot be read from it. "
            "Check out idfkit-conformance, or pass an explicit path to override the pinned read."
        )
    return Path(result.stdout.strip())


def read_pinned(file_path: Path, level: str, *, override: bool) -> GovernanceSource:
    """Return *file_path*'s content at *level*, or from the working tree when overridden."""
    if override:
        return GovernanceSource(
            text=file_path.read_text(encoding="utf-8"),
            description=f"{file_path} (working tree, overriding the pinned read at {level})",
            pinned=False,
        )

    repo = _toplevel(file_path.parent)
    try:
        relative = file_path.resolve().relative_to(repo.resolve())
    except ValueError:
        sys.exit(f"{file_path} is not inside {repo}, so it cannot be read at {level}")

    result = _run_git(repo, "show", f"{level}:{relative.as_posix()}")
    if result.returncode != 0:
        sys.exit(
            f"cannot read {relative.as_posix()} at {level} from {repo}:\n"
            f"    {result.stderr.strip()}\n"
            f"  The governance tag must exist and must be fetched. In CI, check the conformance "
            f"repository out at the pinned ref with its tags. Locally, pass an explicit path to "
            f"read a working tree instead, and understand that this is an override."
        )
    return GovernanceSource(
        text=result.stdout,
        description=f"{relative.as_posix()} at {level} in {repo}",
        pinned=True,
    )
