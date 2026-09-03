#!/usr/bin/env python3
"""Vendor what the site needs from idfkit-js: the examples and the reference (FR-062, FR-064).

Two things, published together on one `docs-YYYY.N` tag of idfkit/idfkit-js:

    docs/snippets/js/          every TypeScript example the pages include, as the real modules
                               that repository compiles. A page that shows Python from a checked
                               file and TypeScript from hand-typed text is half-checked.
    docs/typedoc/typedoc.json  the TypeDoc output the TypeScript reference is generated from
                               (Principle V), read by docs/hooks/typedoc_shim.py in place of
                               running TypeDoc, which this build has no toolchain for (FR-058).

One tag rather than two, so the reference and the examples always describe the same commit.

WHY THE TREE IS COMMITTED RATHER THAN DOWNLOADED AT BUILD TIME

FR-058 says the documentation build needs no Node toolchain and no checkout of idfkit-js. A
build-time download satisfies the letter of that and not the point: it makes every build, every
preview, and every offline edit depend on a network round trip to another repository's releases.
Vendoring makes the build need nothing at all, which is the same reason the schemas ship inside
the wheel rather than being fetched.

What vendoring costs is that the copy can drift from its source silently, so it is not allowed
to be silent: `--check` diffs the tree against the pinned release and blocks the merge on any
difference. That check may reach the network, because it is not the documentation build.

Three sources, and they are not interchangeable:

    --from-release      the pinned tag's published asset. What CI uses. The only authority.
    --from-sibling      a local idfkit-js checkout. For trying an example before it is
                        published; announces itself on every run and is never used in CI.
    --check             compare, do not write. Exit 1 on any difference.

Usage::

    python scripts/sync_js_artifacts.py --from-release
    python scripts/sync_js_artifacts.py --from-sibling ../idfkit-js
    python scripts/sync_js_artifacts.py --check
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Protocol

REPO = Path(__file__).resolve().parents[1]
VENDORED = REPO / "docs" / "snippets" / "js"
VENDORED_TYPEDOC = REPO / "docs" / "typedoc" / "typedoc.json"
SOURCE_REPO = "idfkit/idfkit-js"
ASSET = "docs-snippets.tar.gz"
TYPEDOC_ASSET = "typedoc.json"
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


def pinned_level() -> str:
    """Read ``[tool.idfkit.docs] level``, or refuse to guess one."""
    data = _load_toml((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    level = data.get("tool", {}).get("idfkit", {}).get("docs", {}).get("level")
    if not isinstance(level, str) or not level:
        fail_to_run(
            "No documentation artifact level is declared in pyproject.toml.",
            '  Add [tool.idfkit.docs] level = "docs-YYYY.N".',
        )
    return level  # type: ignore[return-value]


def _fetch(level: str, asset: str, destination: Path) -> None:
    url = f"https://github.com/{SOURCE_REPO}/releases/download/{level}/{asset}"
    print(f"Fetching {url}")
    try:
        with urllib.request.urlopen(url) as response, destination.open("wb") as handle:  # noqa: S310
            shutil.copyfileobj(response, handle)
    except urllib.error.HTTPError as error:
        fail_to_run(
            f"cannot fetch {asset} at {level} from {SOURCE_REPO}: HTTP {error.code}.",
            "  FR-084 requires an artefact be published and versioned before anything pins it.",
            "  Publish the level from idfkit-js (.github/workflows/publish-docs-artifacts.yml),",
            "  or work against a local checkout with --from-sibling and understand that a run",
            "  under that override is not evidence about the pinned tag.",
        )
    except urllib.error.URLError as error:
        fail_to_run(f"cannot reach {SOURCE_REPO} to fetch {level}: {error.reason}")


def download_release(level: str, into: Path) -> tuple[Path, Path]:
    """Unpack the pinned release into *into*; return the snippet root and the TypeDoc JSON."""
    archive = into / ASSET
    _fetch(level, ASSET, archive)
    typedoc = into / TYPEDOC_ASSET
    _fetch(level, TYPEDOC_ASSET, typedoc)

    extracted = into / "extracted"
    extracted.mkdir()
    with tarfile.open(archive) as tar:
        if sys.version_info >= (3, 12):
            tar.extractall(extracted, filter="data")
        else:  # pragma: no cover - 3.11
            tar.extractall(extracted)  # noqa: S202
    root = extracted / "docs-snippets"
    if not root.is_dir():
        fail_to_run(f"{ASSET} at {level} carries no docs-snippets/ directory.")
    return root, typedoc


def copy_from_sibling(path: Path) -> tuple[Path, Path]:
    root = path / "docs-snippets"
    typedoc = path / ".typedoc.json"
    if not root.is_dir():
        fail_to_run(f"No docs-snippets/ under {path}. Pass the root of an idfkit-js checkout.")
    if not typedoc.is_file():
        fail_to_run(
            f"No .typedoc.json under {path}. Run `npm run docs:api` in that checkout first: the "
            f"reference is generated there, never here."
        )
    print(
        f"!! Reading {path}, a working tree, instead of the pinned release.\n"
        f"   This is an override. A build made this way says nothing about the pinned tag."
    )
    return root, typedoc


def differences(left: Path, right: Path) -> list[str]:
    """Every path that differs between two trees, as repository-relative strings."""
    found: list[str] = []

    def walk(comparison: filecmp.dircmp[str], prefix: str) -> None:
        for name in sorted(comparison.left_only):
            found.append(f"  only in the vendored copy: {prefix}{name}")
        for name in sorted(comparison.right_only):
            found.append(f"  only in the pinned release: {prefix}{name}")
        for name in sorted(comparison.diff_files):
            found.append(f"  differs: {prefix}{name}")
        for name, sub in sorted(comparison.subdirs.items()):
            walk(sub, f"{prefix}{name}/")

    walk(filecmp.dircmp(str(left), str(right)), "")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--from-release", action="store_true", help="Read the pinned release asset (default).")
    source.add_argument("--from-sibling", metavar="PATH", help="Read a local idfkit-js checkout instead.")
    parser.add_argument("--check", action="store_true", help="Compare only; exit 1 on any difference.")
    args = parser.parse_args()

    level = pinned_level()
    with tempfile.TemporaryDirectory(prefix="idfkit-js-snippets-") as tmp:
        if args.from_sibling:
            root, typedoc = copy_from_sibling(Path(args.from_sibling).expanduser().resolve())
        else:
            root, typedoc = download_release(level, Path(tmp))

        if args.check:
            if not VENDORED.is_dir():
                print(f"❌ {VENDORED.relative_to(REPO)} does not exist.", file=sys.stderr)
                return 1
            if not VENDORED_TYPEDOC.is_file():
                print(f"❌ {VENDORED_TYPEDOC.relative_to(REPO)} does not exist.", file=sys.stderr)
                return 1
            found = differences(VENDORED, root)
            if VENDORED_TYPEDOC.read_bytes() != typedoc.read_bytes():
                found.append(f"  differs: {VENDORED_TYPEDOC.relative_to(REPO)}")
            if found:
                print(f"❌ The vendored artifacts differ from {level}:", file=sys.stderr)
                for line in found:
                    print(line, file=sys.stderr)
                print(
                    "   Run: uv run python scripts/sync_js_artifacts.py --from-release",
                    file=sys.stderr,
                )
                return 1
            print(f"✅ The vendored examples and TypeDoc reference match {level}.")
            return 0

        if VENDORED.exists():
            shutil.rmtree(VENDORED)
        shutil.copytree(root, VENDORED)
        VENDORED_TYPEDOC.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(typedoc, VENDORED_TYPEDOC)
        subprocess.run(  # noqa: S603
            ["git", "add", "--intent-to-add", "-A", str(VENDORED), str(VENDORED_TYPEDOC)],  # noqa: S607
            cwd=REPO,
            check=False,
        )
        count = sum(1 for _ in VENDORED.rglob("*.ts"))
        size = VENDORED_TYPEDOC.stat().st_size
        print(f"Vendored {count} TypeScript examples and a {size:,}-byte TypeDoc reference from {level}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
