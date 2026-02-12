"""
Schema download utilities.

Downloads EnergyPlus epJSON schema files from GitHub releases
and caches them locally for use by idfkit.
"""

from __future__ import annotations

import gzip
import json
import shutil
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .versions import (
    ENERGYPLUS_VERSIONS,
    github_release_tag,
    is_supported_version,
    version_dirname,
    version_string,
)

_GITHUB_API_BASE = "https://api.github.com/repos/NatLabRockies/EnergyPlus/releases/tags"
_SCHEMA_FILENAME = "Energy+.schema.epJSON"
_SCHEMA_FILENAME_GZ = "Energy+.schema.epJSON.gz"


def _get_release_assets(version: tuple[int, int, int]) -> list[dict[str, Any]]:
    """Fetch the list of release assets from GitHub API."""
    tag = github_release_tag(version)
    url = f"{_GITHUB_API_BASE}/{tag}"
    req = Request(url, headers={"Accept": "application/vnd.github.v3+json"})  # noqa: S310
    with urlopen(req, timeout=30) as resp:  # noqa: S310
        data: dict[str, Any] = json.loads(resp.read())
    return data.get("assets", [])


def _find_linux_tarball_url(assets: list[dict[str, Any]]) -> str | None:
    """Find a Linux tar.gz asset URL from release assets."""
    for asset in assets:
        name: str = asset.get("name", "")
        if "Linux" in name and name.endswith(".tar.gz"):
            return asset.get("browser_download_url")
    return None


def _extract_schema_from_tarball(tarball_bytes: bytes) -> bytes | None:
    """Extract the Energy+.schema.epJSON file from a tarball."""
    with tarfile.open(fileobj=BytesIO(tarball_bytes), mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.name.endswith(_SCHEMA_FILENAME):
                f = tar.extractfile(member)
                if f is not None:
                    return f.read()
    return None


def download_schema(
    version: tuple[int, int, int],
    target_dir: Path | None = None,
    compress: bool = True,
) -> Path:
    """
    Download the epJSON schema for an EnergyPlus version from GitHub.

    Downloads the Linux release tarball and extracts the schema file.

    Args:
        version: EnergyPlus version tuple (major, minor, patch).
        target_dir: Directory to store the schema. Defaults to
                    ~/.idfkit/schemas/VX-Y-Z/.
        compress: If True, store as gzip-compressed .gz file.

    Returns:
        Path to the downloaded schema file.

    Raises:
        ValueError: If the version is not supported.
        RuntimeError: If the download or extraction fails.
    """
    if not is_supported_version(version):
        msg = f"Version {version_string(version)} is not a supported EnergyPlus version"
        raise ValueError(msg)

    # Determine target path
    dirname = version_dirname(version)
    target_dir = (Path.home() / ".idfkit" / "schemas" / dirname) if target_dir is None else (target_dir / dirname)
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = _SCHEMA_FILENAME_GZ if compress else _SCHEMA_FILENAME
    target_path = target_dir / filename

    if target_path.exists():
        return target_path

    # Get release assets from GitHub
    try:
        assets = _get_release_assets(version)
    except (HTTPError, URLError, TimeoutError) as e:
        msg = f"Failed to fetch release info for {version_string(version)}: {e}"
        raise RuntimeError(msg) from e

    tarball_url = _find_linux_tarball_url(assets)
    if not tarball_url:
        msg = f"No Linux tarball found in release assets for {version_string(version)}"
        raise RuntimeError(msg)

    # Download the tarball
    try:
        req = Request(tarball_url)  # noqa: S310
        with urlopen(req, timeout=300) as resp:  # noqa: S310
            tarball_bytes = resp.read()
    except (HTTPError, URLError, TimeoutError) as e:
        msg = f"Failed to download tarball for {version_string(version)}: {e}"
        raise RuntimeError(msg) from e

    # Extract the schema file
    schema_bytes = _extract_schema_from_tarball(tarball_bytes)
    if schema_bytes is None:
        msg = f"Could not find {_SCHEMA_FILENAME} in release tarball for {version_string(version)}"
        raise RuntimeError(msg)

    # Write to target (atomic via temp file)
    with tempfile.NamedTemporaryFile(dir=target_dir, delete=False, suffix=".tmp") as tmp:
        tmp_path = Path(tmp.name)
        if compress:
            with gzip.open(tmp, "wb") as gz:
                gz.write(schema_bytes)
        else:
            tmp.write(schema_bytes)

    shutil.move(str(tmp_path), str(target_path))
    return target_path


def download_all_schemas(
    target_dir: Path | None = None,
    compress: bool = True,
    on_progress: object | None = None,
) -> dict[tuple[int, int, int], Path | Exception]:
    """
    Download schemas for all supported EnergyPlus versions.

    Args:
        target_dir: Base directory to store schemas. Defaults to
                    ~/.idfkit/schemas/.
        compress: If True, store as gzip-compressed .gz files.
        on_progress: Unused, reserved for future callback support.

    Returns:
        Dict mapping version tuples to either the Path of the downloaded
        schema or the Exception that occurred during download.
    """
    results: dict[tuple[int, int, int], Path | Exception] = {}
    base_dir = target_dir if target_dir is not None else Path.home() / ".idfkit" / "schemas"

    for version in ENERGYPLUS_VERSIONS:
        try:
            path = download_schema(
                version, target_dir=base_dir.parent if target_dir is None else target_dir, compress=compress
            )
            results[version] = path
        except Exception as e:
            results[version] = e

    return results
