#!/usr/bin/env python3
"""Assert the release tag and the version declared in ``pyproject.toml`` agree.

The release workflow used to patch the field instead of checking it. It wrote the raw tag in,
``sed -i "s/^version = \".*\"/version = \"$RELEASE_VERSION\"/"``, and the tag format is
``vX.Y.Z``, so ``v1.0.0-rc.5`` became the declared version. Hatchling normalised the wheel's
filename to ``idfkit-1.0.0rc5-py3-none-any.whl`` and wrote the raw string into the metadata, so
``idfkit.__version__`` was ``"v1.0.0-rc.5"`` and every file the writer generated carried
``!-Generator idfkit vv1.0.0-rc.5`` (idfkit#212). 1.0.0-rc.5 is the first release to reach PyPI
that way; rc.4 and earlier carry the manifest's own value.

Checking rather than patching is what the repository already says it does. CLAUDE.md requires the
field to be bumped in the release commit and the two to agree, which makes the patch redundant,
and there are two publish paths: ``on-release-main.yml`` and ``make publish``, which builds from
whatever the field says. Only one of them patched, so the two produced different metadata from the
same commit. Now neither patches, and a disagreement fails the release instead of being written
over.

Comparison is by PEP 440 equality, not by string, so the ``v`` prefix and the punctuation the tag
format uses are not differences: ``v1.0.0-rc.5`` and ``1.0.0rc5`` are the same version. A tag that
is not a version at all is a refusal rather than a failure, because it means this was run against
something that is not a release.

Exit codes: 0 they agree, 1 they disagree, 2 the check could not run.

Usage::

    python scripts/check_release_version.py --tag v1.0.0-rc.6
    python scripts/check_release_version.py              # reads GITHUB_REF_NAME
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Protocol

from packaging.version import InvalidVersion, Version

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "pyproject.toml"


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


def declared_version() -> str:
    """The version ``pyproject.toml`` states, or a refusal if it states none."""
    reader = _toml_reader()
    if reader is None:
        raise SystemExit("2: no TOML reader available. Python 3.11+ ships tomllib; on 3.10 install tomli.")
    manifest = reader.loads(MANIFEST.read_text(encoding="utf-8"))
    version = manifest.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise SystemExit(f"2: {MANIFEST} declares no [project] version, so there is nothing to check.")
    return version


def parse(value: str, what: str) -> Version:
    try:
        return Version(value)
    except InvalidVersion:
        raise SystemExit(f"2: the {what} {value!r} is not a version this can compare.") from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--tag",
        default=os.environ.get("GITHUB_REF_NAME"),
        help="the release tag, with or without the v prefix. Defaults to GITHUB_REF_NAME.",
    )
    args = parser.parse_args(argv)

    if not args.tag:
        print("2: no tag given and GITHUB_REF_NAME is unset.", file=sys.stderr)
        return 2

    declared = declared_version()
    tagged = parse(args.tag.removeprefix("v"), "tag")
    if parse(declared, "declared version") != tagged:
        print(
            f"FAILED: pyproject.toml declares {declared!r} and the release is tagged {args.tag!r}.\n"
            f"  Bump version in pyproject.toml in the release commit, to the version being tagged.\n"
            f"  See the Releases section of CLAUDE.md. Nothing is patched here on purpose: the\n"
            f"  manifest is what both publish paths build from.",
            file=sys.stderr,
        )
        return 1

    print(f"OK: pyproject.toml declares {declared}, the release is tagged {args.tag}, and they are the same version.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
