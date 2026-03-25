"""Documentation URL builder for docs.idfkit.com.

Generates URLs pointing to the correct page on the documentation site
for any EnergyPlus object type, given version and schema metadata.
This module is stdlib-only (no third-party dependencies).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schema import EpJSONSchema

BASE_URL = "https://docs.idfkit.com"


@dataclass(frozen=True, slots=True)
class DocsUrl:
    """A resolved documentation URL with metadata."""

    url: str
    doc_set: str  # "io-reference", "engineering-reference", "search"
    version: str  # "v25.2"
    label: str  # Human-readable label, e.g. "Zone — I/O Reference"


_ANCHOR_STRIP_RE = re.compile(r"[:/() ]")

# Lazy-loaded mapping from object type → doc location path.
# Generated from idfkit-docs search index; stable across versions.
_doc_locations: dict[str, str] | None = None


def _get_doc_locations() -> dict[str, str]:
    """Load the bundled doc_locations.json mapping (cached after first call)."""
    global _doc_locations
    if _doc_locations is None:
        mapping_path = Path(__file__).parent / "schemas" / "doc_locations.json"
        with open(mapping_path) as f:
            locations: dict[str, str] = json.load(f)
        _doc_locations = locations
    return _doc_locations


def _version_short(version: tuple[int, int, int]) -> str:
    """Format version tuple as 'vM.m' for URL paths."""
    return f"v{version[0]}.{version[1]}"


def _resolve_doc_version(version: tuple[int, int, int]) -> str | None:
    """Return the short version string only if docs exist for this version.

    Returns ``None`` for versions that have no documentation on
    docs.idfkit.com, so callers can avoid emitting dead links.
    """
    from .versions import is_supported_version

    if is_supported_version(version):
        return _version_short(version)
    return None


def _object_anchor(obj_type: str) -> str:
    """Convert an object type to an anchor slug matching idfkit-docs build output."""
    return _ANCHOR_STRIP_RE.sub("", obj_type.lower())


def io_reference_url(
    obj_type: str,
    version: tuple[int, int, int],
    schema: EpJSONSchema | None = None,
    *,
    base_url: str = BASE_URL,
) -> DocsUrl | None:
    """Build a docs.idfkit.com URL for an object's I/O Reference page.

    Uses a bundled mapping from the documentation search index for accurate
    URLs. Falls back to schema-based group slug construction when the object
    type is not in the mapping.

    Returns ``None`` when the object type cannot be resolved or the version
    has no documentation.

    Args:
        obj_type: EnergyPlus object type name (e.g. ``"Zone"``).
        version: EnergyPlus version as ``(major, minor, patch)`` tuple.
        schema: Optional schema for fallback group lookup.  When ``None`` the
            function tries to load the schema for *version* via :func:`get_schema`.
        base_url: Documentation site base URL (for testing overrides).
    """
    ver = _resolve_doc_version(version)
    if ver is None:
        return None

    # Primary: use the bundled mapping (accurate, from search index)
    locations = _get_doc_locations()
    location = locations.get(obj_type)
    if location is not None:
        url = f"{base_url}/{ver}/{location}"
        return DocsUrl(url=url, doc_set="io-reference", version=ver, label=f"{obj_type} — I/O Reference")

    # Fallback: derive from schema group (may be inaccurate for some groups)
    group = _resolve_group(obj_type, schema)
    if group is None:
        return None
    slug = group.lower().replace(" ", "-")
    anchor = _object_anchor(obj_type)
    url = f"{base_url}/{ver}/io-reference/overview/group-{slug}/#{anchor}"
    return DocsUrl(url=url, doc_set="io-reference", version=ver, label=f"{obj_type} — I/O Reference")


def engineering_reference_url(
    version: tuple[int, int, int],
    *,
    base_url: str = BASE_URL,
) -> DocsUrl | None:
    """Build a docs.idfkit.com URL for the Engineering Reference landing page.

    Returns ``None`` if the version has no documentation.
    """
    ver = _resolve_doc_version(version)
    if ver is None:
        return None
    url = f"{base_url}/{ver}/engineering-reference/"
    return DocsUrl(url=url, doc_set="engineering-reference", version=ver, label="Engineering Reference")


def search_url(
    query: str,
    version: tuple[int, int, int],
    *,
    base_url: str = BASE_URL,
) -> DocsUrl | None:
    """Build a docs.idfkit.com URL for searching/browsing documentation.

    Links to the version's I/O Reference overview page where the user
    can browse or search for the object type.  Returns ``None`` if the
    version has no documentation.
    """
    ver = _resolve_doc_version(version)
    if ver is None:
        return None
    url = f"{base_url}/{ver}/io-reference/overview/"
    return DocsUrl(url=url, doc_set="search", version=ver, label=f"Search: {query}")


def docs_url_for_object(
    obj_type: str,
    version: tuple[int, int, int],
    schema: EpJSONSchema | None = None,
    *,
    base_url: str = BASE_URL,
) -> DocsUrl | None:
    """Convenience wrapper: get the best documentation URL for an object type.

    Tries the I/O Reference first; returns ``None`` if the object type cannot
    be resolved or the version has no documentation.
    """
    return io_reference_url(obj_type, version, schema, base_url=base_url)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _resolve_group(obj_type: str, schema: EpJSONSchema | None) -> str | None:
    """Get the IDD group for an object type, loading schema if needed."""
    if schema is not None:
        return schema.get_group(obj_type)
    # Attempt to load the default schema
    try:
        from .schema import get_schema
        from .versions import LATEST_VERSION

        loaded = get_schema(LATEST_VERSION)
        return loaded.get_group(obj_type)
    except Exception:
        return None
