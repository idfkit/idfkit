"""Generate doc_locations.json from built idfkit-docs HTML.

Scans the idfkit-docs ``dist/`` directory for HTML anchor IDs that match
EnergyPlus object types and produces a mapping of
``{object_type: "relative/path/#anchor"}``.

The generated file is committed and shipped with the package so that
:mod:`idfkit.docs` can generate accurate documentation URLs without any
runtime dependency on idfkit-docs.

Usage::

    python -m idfkit.codegen.generate_doc_locations               # default: ../idfkit-docs/dist
    python -m idfkit.codegen.generate_doc_locations /path/to/dist  # explicit path
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from idfkit.schema import get_schema
from idfkit.versions import LATEST_VERSION

# Regex to extract id="..." attributes from HTML.  We match
# lowercase-alphanumeric plus hyphens (the docs build convention for
# EnergyPlus object-type heading anchors).
_ANCHOR_RE = re.compile(r'id="([a-z0-9-]+)"')

# Same transform used by the docs build to turn object type names into
# heading anchors: strip colons, slashes, parens, and spaces.
_ANCHOR_STRIP_RE = re.compile(r"[:/() ]")

# Default location of idfkit-docs dist output relative to this repo.
_DEFAULT_DOCS_DIST = Path(__file__).resolve().parents[4] / "idfkit-docs" / "dist"

# Output path for the generated JSON.
_OUTPUT_PATH = Path(__file__).resolve().parents[1] / "schemas" / "doc_locations.json"


def _build_anchor_to_object_map() -> dict[str, str]:
    """Build a reverse mapping from anchor slug → canonical object type."""
    schema = get_schema(LATEST_VERSION)
    mapping: dict[str, str] = {}
    for obj_type in schema.object_types:
        anchor = _ANCHOR_STRIP_RE.sub("", obj_type.lower())
        mapping[anchor] = obj_type
    return mapping


def _find_latest_version_dir(dist_dir: Path) -> Path | None:
    """Find the latest versioned directory (e.g. ``v25.2``) in the dist."""
    version_dirs = sorted(
        (d for d in dist_dir.iterdir() if d.is_dir() and d.name.startswith("v")),
        key=lambda d: tuple(int(x) for x in d.name[1:].split(".") if x.isdigit()),
        reverse=True,
    )
    return version_dirs[0] if version_dirs else None


def generate(dist_dir: Path) -> dict[str, str]:
    """Scan *dist_dir* and return ``{object_type: relative_path}`` mapping."""
    version_dir = _find_latest_version_dir(dist_dir)
    if version_dir is None:
        print(f"Error: no versioned directories found in {dist_dir}", file=sys.stderr)
        sys.exit(1)

    io_ref = version_dir / "io-reference"
    if not io_ref.is_dir():
        print(f"Error: {io_ref} does not exist", file=sys.stderr)
        sys.exit(1)

    anchor_to_obj = _build_anchor_to_object_map()
    locations: dict[str, str] = {}

    # Walk all HTML files under io-reference/
    for html_path in sorted(io_ref.rglob("index.html")):
        content = html_path.read_text(encoding="utf-8", errors="replace")
        anchors = _ANCHOR_RE.findall(content)

        # Build the relative path from the versioned dir to this page
        page_dir = html_path.parent
        relative = page_dir.relative_to(version_dir)

        for anchor in anchors:
            obj_type = anchor_to_obj.get(anchor)
            if obj_type is not None and obj_type not in locations:
                locations[obj_type] = f"{relative}/#{anchor}"

    return dict(sorted(locations.items()))


def main() -> None:
    dist_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else _DEFAULT_DOCS_DIST

    if not dist_dir.is_dir():
        print(f"Error: docs dist directory not found: {dist_dir}", file=sys.stderr)
        print("Build idfkit-docs first, or pass the path explicitly.", file=sys.stderr)
        sys.exit(1)

    locations = generate(dist_dir)
    print(f"Found {len(locations)} object type → docs page mappings")

    _OUTPUT_PATH.write_text(json.dumps(locations, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
