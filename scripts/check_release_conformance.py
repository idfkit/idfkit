#!/usr/bin/env python3
"""Assert this release passes the corpus at the level it declares (FR-024, SC-025).

A release states one thing about agreement: the conformance level it passes. FR-024 makes that
a claim the release's own checks assert, so a release whose claim is false cannot ship. This is
that assertion, run from ``make release-check`` and from ``make build-and-publish`` ahead of the
upload.

It runs the corpus **at the declared tag**, materialised out of the conformance repository's git
object store into a temporary directory, never from that checkout's working tree. The distinction
is the whole point: a maintainer with local corpus edits would otherwise get a green release check
for a corpus nobody else can obtain, which is the moving-source failure ``_governance_source.py``
exists to prevent, one level up.

Three refusals rather than a fallback, because a release check that guesses is not one:

* no ``[tool.idfkit.conformance] level`` in ``pyproject.toml`` -> refuse to run;
* the declared tag absent from the conformance checkout -> refuse to run;
* the tag present but not an immutable ``conformance-YYYY.N`` -> refuse to run.

Exit codes: 0 the corpus passes at the declared level, 1 it does not, 2 the check could not run.

Usage::

    python scripts/check_release_conformance.py
    python scripts/check_release_conformance.py --conformance-repo ../idfkit-conformance
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any, Protocol

REPO = Path(__file__).resolve().parents[1]
CONFORMANCE_TAG_RE = re.compile(r"^conformance-\d{4}\.\d+$")
CANNOT_RUN = 2


class _TomlReader(Protocol):
    def loads(self, s: str, /) -> dict[str, Any]: ...


def _toml_reader() -> _TomlReader | None:
    """tomllib on 3.11+, tomli on 3.10, None when neither is installed."""
    try:  # Python 3.11+
        import tomllib  # pyright: ignore[reportMissingTypeStubs]
    except ModuleNotFoundError:  # pragma: no cover - exercised only on 3.10
        try:
            import tomli  # pyright: ignore[reportMissingImports]
        except ModuleNotFoundError:  # pragma: no cover
            return None
        return tomli  # pyright: ignore[reportReturnType, reportUnknownVariableType]
    return tomllib


def _load_toml(text: str) -> dict[str, Any]:
    """Parse TOML with whatever reader this interpreter has, or refuse to run."""
    reader = _toml_reader()
    if reader is None:
        fail_to_run("No TOML reader available. Python 3.11+ ships tomllib; on 3.10 install tomli.")
        raise AssertionError("unreachable")
    return reader.loads(text)


def fail_to_run(*lines: str) -> None:
    for line in lines:
        print(line, file=sys.stderr)
    raise SystemExit(CANNOT_RUN)


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        ["git", "-C", str(repo), *args],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )


def declared_level() -> str:
    """Return ``[tool.idfkit.conformance] level``, the one place the claim is authored."""
    data = _load_toml((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    level = data.get("tool", {}).get("idfkit", {}).get("conformance", {}).get("level")
    if not isinstance(level, str) or not level:
        fail_to_run(
            "No conformance level is declared in pyproject.toml.",
            '  Add [tool.idfkit.conformance] level = "conformance-YYYY.N".',
        )
    if not CONFORMANCE_TAG_RE.match(level):  # type: ignore[arg-type]
        fail_to_run(
            f"The declared conformance level {level!r} is not an immutable conformance-YYYY.N tag.",
            "  A release cannot claim agreement against a branch: it moves after the release ships.",
        )
    return level  # type: ignore[return-value]


def resolve_conformance_repo(explicit: str | None) -> Path:
    path = Path(explicit).expanduser() if explicit else REPO.parent / "idfkit-conformance"
    if not (path / ".git").exists():
        fail_to_run(
            f"No idfkit-conformance git checkout at {path}.",
            "  Pass --conformance-repo PATH. A release check cannot be skipped for want of a clone:",
            "  skipping it would let the release ship the claim unexamined, which is what FR-024 forbids.",
        )
    return path


def materialise_corpus(repo: Path, tag: str, into: Path) -> Path:
    """Extract the corpus at *tag* into *into*, so the run reads the tag and not a working tree."""
    if _git(repo, "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}^{{commit}}").returncode != 0:
        fail_to_run(
            f"The declared conformance tag {tag} does not exist in {repo}.",
            "  Fetch the tags, or cut the level before declaring it: FR-084 requires an artefact be",
            "  published and versioned before anything pins it.",
        )
    archive = into / "corpus.tar"
    with archive.open("wb") as handle:
        result = subprocess.run(  # noqa: S603
            ["git", "-C", str(repo), "archive", "--format=tar", tag],  # noqa: S607
            stdout=handle,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    if result.returncode != 0:
        fail_to_run(f"cannot export {tag} from {repo}:", f"    {result.stderr.strip()}")
    corpus = into / "corpus"
    corpus.mkdir()
    with tarfile.open(archive) as tar:
        # filter="data" is the 3.12+ safe extraction; the archive is one this process just produced
        # from a local tag, so on older interpreters the default is no worse than reading the tree.
        if sys.version_info >= (3, 12):
            tar.extractall(corpus, filter="data")
        else:  # pragma: no cover - 3.10, 3.11
            tar.extractall(corpus)  # noqa: S202
    return corpus


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--conformance-repo",
        metavar="PATH",
        help="Path to the idfkit-conformance checkout carrying the conformance tags.",
    )
    args = parser.parse_args()

    level = declared_level()
    conformance_repo = resolve_conformance_repo(args.conformance_repo)

    with tempfile.TemporaryDirectory(prefix="idfkit-release-conformance-") as tmp:
        corpus = materialise_corpus(conformance_repo, level, Path(tmp))
        runner = corpus / "runners" / "run.py"
        if not runner.is_file():
            fail_to_run(f"{level} carries no runners/run.py; it is not a corpus this check can run.")
        print(f"🚀 Running the conformance corpus at {level} (exported from {conformance_repo})")
        outcome = subprocess.run(  # noqa: S603
            [sys.executable, str(runner), "--library", str(REPO), "--corpus", str(corpus), "--level", level],
            check=False,
        )

    if outcome.returncode != 0:
        print(
            f"\n❌ This release declares {level} and does not pass it.\n"
            f"   Fix the library, or record the difference in known-divergence.toml and cut a new level.\n"
            f"   Do not lower the declaration to whatever currently passes: the level is the claim.",
            file=sys.stderr,
        )
        return 1
    print(f"\n✅ The corpus at {level} passes; the release may state it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
