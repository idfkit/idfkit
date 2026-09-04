#!/usr/bin/env python3
"""Copy the four weather-browser files out of the installed idfkit into docs/weather/browse/.

Four files are simultaneously part of the library's distribution and part of a page:

    docs/weather/browse/app.js            <- idfkit/weather/_browser/assets/app.js
    docs/weather/browse/index.html        <- idfkit/weather/_browser/assets/index.html
    docs/weather/browse/style.css         <- idfkit/weather/_browser/assets/style.css
    docs/weather/browse/stations.json.gz  <- idfkit/weather/data/stations.json.gz

They reached the page by symlink into `src/`, which worked only because the site and the library
shared a repository. A symlink does not survive a repository boundary, so this script replaces
them: it locates the INSTALLED distribution and copies, before mkdocs runs, on every build
including the portable one (003 contracts/shipped-assets.md).

WHY COPY RATHER THAN VENDOR. Vendoring with a `--check` byte comparison is how the TypeScript
examples and reference cross their repository boundary, and symmetry argued for doing the same
here. It was rejected because the two cases differ in the one respect that decides it: no package
carries the TypeScript artifacts, so vendoring is the only route, whereas the library is installed
here anyway for mkdocstrings and already carries these four. A copy step is strictly less
machinery than a vendor-plus-verify step, and it cannot go stale between releases because there is
nothing to update.

WHY THE COPY IS NEVER COMMITTED. `docs/weather/browse/` is gitignored. A committed copy is a
snapshot, and a snapshot of a shipped asset drifts silently: it does not fail a build, it shows a
reader a weather browser the library no longer has.

WHY A MISSING ASSET IS FATAL. If the installed distribution does not carry one of the four, that is
a change in what the library ships. It must surface as a build failure and not as a page with a
broken widget, so there is no partial copy and no placeholder.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Each asset as (path inside the installed idfkit package, name under docs/weather/browse/).
ASSETS: tuple[tuple[str, str], ...] = (
    ("weather/_browser/assets/app.js", "app.js"),
    ("weather/_browser/assets/index.html", "index.html"),
    ("weather/_browser/assets/style.css", "style.css"),
    ("weather/data/stations.json.gz", "stations.json.gz"),
)

DESTINATION = Path("docs/weather/browse")


class MissingAsset(Exception):
    """The installed distribution does not carry a file the site publishes."""


def installed_package_root() -> Path:
    """Return the directory of the installed idfkit package.

    Imported rather than searched for: the site declares an exact library level and installs it,
    so the interpreter running the build already resolves the one distribution the pages describe.
    Searching the filesystem could find a different one.
    """
    try:
        import idfkit
    except ImportError as error:  # pragma: no cover - the environment is broken, not the input
        raise MissingAsset(
            "idfkit is not importable, so the four weather-browser files the site publishes "
            "cannot be located.\n"
            "The site declares its library level in [tool.idfkit.library]; install it with "
            "`uv sync`."
        ) from error

    if idfkit.__file__ is None:  # pragma: no cover - namespace package, not a real installation
        raise MissingAsset("idfkit resolves to a namespace package rather than an installation.")
    return Path(idfkit.__file__).parent


def copy_assets(destination: Path) -> list[Path]:
    """Copy all four assets into *destination*, creating it. Return what was written."""
    root = installed_package_root()

    missing = [relative for relative, _ in ASSETS if not (root / relative).is_file()]
    if missing:
        listed = "\n".join(f"  {root / relative}" for relative in missing)
        raise MissingAsset(
            f"The installed idfkit at {root} does not carry "
            f"{len(missing)} of the {len(ASSETS)} files the weather browser page publishes:\n"
            f"{listed}\n\n"
            "That is a change in what the library ships, not a problem with this build. The page "
            "must not render with a broken widget, so the build stops here.\n"
            "Fix it by pinning [tool.idfkit.library] to a release that still ships these files, "
            "or by updating the page and this script together if the library moved them."
        )

    destination.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for relative, name in ASSETS:
        target = destination / name
        shutil.copyfile(root / relative, target)
        written.append(target)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--destination",
        type=Path,
        default=DESTINATION,
        help=f"Where to write the four files (default: {DESTINATION}).",
    )
    args = parser.parse_args()

    try:
        written = copy_assets(args.destination)
    except MissingAsset as error:
        print(f"❌ {error}", file=sys.stderr)
        return 1

    root = installed_package_root()
    print(f"Copied {len(written)} weather-browser files from {root} into {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
