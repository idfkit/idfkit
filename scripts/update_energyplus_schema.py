#!/usr/bin/env python3
"""Check for new EnergyPlus releases and bundle the schema if found.

Queries the NREL/EnergyPlus GitHub releases API for the latest version,
and if it is not yet in the idfkit version registry, downloads the schema
and updates ``src/idfkit/versions.py`` accordingly.

Exit codes:
    0 - A new version was found and bundled (or --check reports a new version).
    1 - No new version found; everything is up to date.
    2 - An error occurred.

Environment variables:
    GITHUB_TOKEN - Optional GitHub personal access token for higher API rate limits.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
import tarfile
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent.parent
_VERSIONS_PY = _ROOT / "src" / "idfkit" / "versions.py"
_SCHEMAS_DIR = _ROOT / "src" / "idfkit" / "schemas"

_GITHUB_API_RELEASES = "https://api.github.com/repos/NREL/EnergyPlus/releases"
_SCHEMA_FILENAME = "Energy+.schema.epJSON"


# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------


def _github_headers() -> dict[str, str]:
    """Return HTTP headers for GitHub API requests."""
    headers: dict[str, str] = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def _get_latest_release() -> dict[str, Any]:
    """Fetch the latest *non-prerelease* release from NREL/EnergyPlus."""
    url = f"{_GITHUB_API_RELEASES}?per_page=20"
    req = Request(url, headers=_github_headers())  # noqa: S310
    with urlopen(req, timeout=30) as resp:  # noqa: S310
        releases: list[dict[str, Any]] = json.loads(resp.read())

    for release in releases:
        if release.get("prerelease") or release.get("draft"):
            continue
        return release

    msg = "No stable release found in the last 20 NREL/EnergyPlus releases"
    raise RuntimeError(msg)


def _parse_version_tag(tag: str) -> tuple[int, int, int]:
    """Parse a GitHub release tag like 'v24.1.0' into a version tuple."""
    m = re.match(r"v?(\d+)\.(\d+)\.(\d+)", tag)
    if not m:
        msg = f"Cannot parse version from tag: {tag}"
        raise ValueError(msg)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


# ---------------------------------------------------------------------------
# Schema download (simplified from idfkit.download)
# ---------------------------------------------------------------------------


def _find_linux_tarball_url(assets: list[dict[str, Any]]) -> str | None:
    """Find the Linux tar.gz asset URL from release assets."""
    for asset in assets:
        name = str(asset.get("name", ""))
        if "Linux" in name and name.endswith(".tar.gz"):
            return str(asset.get("browser_download_url", ""))
    return None


def _download_and_extract_schema(assets: list[dict[str, Any]]) -> bytes:
    """Download the Linux tarball and extract the epJSON schema."""
    tarball_url = _find_linux_tarball_url(assets)
    if not tarball_url:
        msg = "No Linux tarball found in release assets"
        raise RuntimeError(msg)

    req = Request(tarball_url)  # noqa: S310
    with urlopen(req, timeout=300) as resp:  # noqa: S310
        tarball_bytes = resp.read()

    with tarfile.open(fileobj=BytesIO(tarball_bytes), mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.name.endswith(_SCHEMA_FILENAME):
                f = tar.extractfile(member)
                if f is not None:
                    return f.read()

    msg = f"Could not find {_SCHEMA_FILENAME} in release tarball"
    raise RuntimeError(msg)


def _save_schema(version: tuple[int, int, int], schema_bytes: bytes) -> Path:
    """Save compressed schema to the bundled schemas directory."""
    dirname = f"V{version[0]}-{version[1]}-{version[2]}"
    dest_dir = _SCHEMAS_DIR / dirname
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_path = dest_dir / f"{_SCHEMA_FILENAME}.gz"
    with gzip.open(dest_path, "wb") as gz:
        gz.write(schema_bytes)

    print(f"Saved schema to {dest_path}")
    return dest_path


# ---------------------------------------------------------------------------
# versions.py updater
# ---------------------------------------------------------------------------


def _read_current_versions() -> list[tuple[int, int, int]]:
    """Parse existing ENERGYPLUS_VERSIONS from versions.py."""
    text = _VERSIONS_PY.read_text()
    matches = re.findall(r"\((\d+),\s*(\d+),\s*(\d+)\)", text)
    return [(int(a), int(b), int(c)) for a, b, c in matches]


def _update_versions_py(new_version: tuple[int, int, int]) -> None:
    """Add *new_version* to the ENERGYPLUS_VERSIONS tuple in versions.py."""
    text = _VERSIONS_PY.read_text()

    # Find the closing paren of the ENERGYPLUS_VERSIONS tuple.
    # We insert the new entry just before the closing ")".
    pattern = r"(ENERGYPLUS_VERSIONS:\s*Final\[tuple\[.*?\]\]\s*=\s*\()(.*?)(\))"
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        msg = "Could not find ENERGYPLUS_VERSIONS in versions.py"
        raise RuntimeError(msg)

    existing_body = m.group(2).rstrip()
    # Ensure trailing comma on existing last entry
    if not existing_body.rstrip().endswith(","):
        existing_body = existing_body.rstrip() + ","
    new_entry = f"    ({new_version[0]}, {new_version[1]}, {new_version[2]}),"
    new_body = f"{existing_body}\n{new_entry}\n"
    updated = text[: m.start(2)] + new_body + text[m.end(2) :]

    _VERSIONS_PY.write_text(updated)
    print(f"Updated {_VERSIONS_PY} with version {new_version}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Check for new EnergyPlus releases and bundle the schema.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check if a new version exists; do not download or update files.",
    )
    args = parser.parse_args()

    print("Fetching latest NREL/EnergyPlus release...")
    try:
        release = _get_latest_release()
    except (HTTPError, URLError, TimeoutError, RuntimeError) as e:
        print(f"Error fetching release: {e}", file=sys.stderr)
        return 2

    tag = str(release.get("tag_name", ""))
    print(f"Latest release tag: {tag}")

    try:
        version = _parse_version_tag(tag)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    current_versions = _read_current_versions()
    if version in current_versions:
        print(f"Version {version} is already supported. Nothing to do.")
        return 1

    print(f"New version detected: {version}")

    if args.check:
        # Output for downstream workflow steps
        print(f"::set-output name=new_version::{version[0]}.{version[1]}.{version[2]}")
        return 0

    # Download and bundle the schema
    assets: list[dict[str, Any]] = release.get("assets", [])

    print("Downloading schema from release tarball...")
    try:
        schema_bytes = _download_and_extract_schema(assets)
    except (HTTPError, URLError, TimeoutError, RuntimeError) as e:
        print(f"Error downloading schema: {e}", file=sys.stderr)
        return 2

    _save_schema(version, schema_bytes)
    _update_versions_py(version)

    print(f"Successfully added EnergyPlus {version[0]}.{version[1]}.{version[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
