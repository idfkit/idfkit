"""
Schema download utilities.

Downloads EnergyPlus epJSON schema files from GitHub releases
and caches them locally for use by idfkit.

Command line, used when a new EnergyPlus release is bundled into the source tree::

    python -m idfkit.download 26.2.0 --target-dir src/idfkit/schemas

The version must already be listed in ``idfkit.versions.ENERGYPLUS_VERSIONS``. The command writes
``<target-dir>/VX-Y-Z/Energy+.schema.epJSON.gz``, prints the path, and does nothing when the file
is already present.

The request to ``api.github.com`` is authenticated when ``GH_TOKEN`` or ``GITHUB_TOKEN`` is set, in
that order of preference. An unauthenticated address is allowed 60 requests per hour. The token is
sent to ``api.github.com`` only: never to the host that serves the release asset, and never to the
target of a redirect.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import sys
import tarfile
import tempfile
import zlib
from http.client import HTTPException
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
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

_GITHUB_API_HOST = "api.github.com"
# In order of preference. An empty value counts as unset.
_TOKEN_VARIABLES = ("GH_TOKEN", "GITHUB_TOKEN")

# Every way a request or the reading of its body fails. HTTPError, URLError, TimeoutError and a
# reset connection are all OSError; a body shorter than its declared length is
# http.client.IncompleteRead, which is an HTTPException and not an OSError.
_TRANSFER_ERRORS = (OSError, HTTPException)
# Every way a truncated or corrupt archive fails to be read. gzip.BadGzipFile is an OSError.
_ARCHIVE_ERRORS = (tarfile.TarError, EOFError, zlib.error, OSError)


def _github_token() -> str | None:
    """Return the token of the first of ``GH_TOKEN`` and ``GITHUB_TOKEN`` that is set and not empty."""
    for name in _TOKEN_VARIABLES:
        token = os.environ.get(name, "").strip()
        if token:
            return token
    return None


def _request(url: str, headers: dict[str, str] | None = None) -> Request:
    """Build a request, authenticated only when it is addressed to ``api.github.com`` over HTTPS.

    The token is added as an unredirected header. ``urllib`` copies the ordinary headers of a
    request to the request it issues on a redirect, whatever the new host, and does not copy the
    unredirected ones, so the token cannot follow a redirect.
    """
    req = Request(url, headers=headers or {})  # noqa: S310
    parts = urlsplit(url)
    if parts.scheme == "https" and parts.hostname == _GITHUB_API_HOST:
        token = _github_token()
        if token is not None:
            req.add_unredirected_header("Authorization", f"Bearer {token}")
    return req


def _get_release_assets(version: tuple[int, int, int]) -> list[dict[str, Any]]:
    """Fetch the list of release assets from GitHub API."""
    tag = github_release_tag(version)
    url = f"{_GITHUB_API_BASE}/{tag}"
    req = _request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urlopen(req, timeout=30) as resp:  # noqa: S310
        data: dict[str, Any] = json.loads(resp.read())
    return data.get("assets", [])


def _find_linux_tarball_url(assets: list[dict[str, Any]]) -> str | None:
    """Find a Linux tar.gz asset URL from release assets.

    The Ubuntu x86_64 tarball is preferred when a release carries several Linux tarballs, so that
    the asset read is the same one on every run. Releases since 26.1.0 list an AlmaLinux tarball
    ahead of it. Any other Linux tarball is used when no Ubuntu x86_64 tarball exists.
    """
    fallback: str | None = None
    for asset in assets:
        name: str = asset.get("name", "")
        if "Linux" not in name or not name.endswith(".tar.gz"):
            continue
        if "Ubuntu" in name and "x86_64" in name:
            return asset.get("browser_download_url")
        if fallback is None:
            fallback = asset.get("browser_download_url")
    return fallback


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
        OSError: If the target directory or the schema file cannot be written.

    A version directory that this call created is removed when the call fails, so that a failed
    download leaves no empty ``VX-Y-Z/`` behind. A directory that existed before the call is kept.
    """
    if not is_supported_version(version):
        msg = f"Version {version_string(version)} is not a supported EnergyPlus version"
        raise ValueError(msg)

    # Determine target path
    dirname = version_dirname(version)
    target_dir = (Path.home() / ".idfkit" / "schemas" / dirname) if target_dir is None else (target_dir / dirname)
    created = not target_dir.exists()
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        return _download_into(version, target_dir, compress)
    except BaseException:
        if created:
            shutil.rmtree(target_dir, ignore_errors=True)
        raise


def _download_into(version: tuple[int, int, int], target_dir: Path, compress: bool) -> Path:
    """Download the schema of a version into an existing version directory."""
    filename = _SCHEMA_FILENAME_GZ if compress else _SCHEMA_FILENAME
    target_path = target_dir / filename

    if target_path.exists():
        return target_path

    # Get release assets from GitHub
    try:
        assets = _get_release_assets(version)
    except _TRANSFER_ERRORS as e:
        msg = f"Failed to fetch release info for {version_string(version)}: {e}"
        raise RuntimeError(msg) from e

    tarball_url = _find_linux_tarball_url(assets)
    if not tarball_url:
        msg = f"No Linux tarball found in release assets for {version_string(version)}"
        raise RuntimeError(msg)

    # Download the tarball
    try:
        with urlopen(_request(tarball_url), timeout=300) as resp:  # noqa: S310
            tarball_bytes = resp.read()
    except _TRANSFER_ERRORS as e:
        msg = f"Failed to download tarball for {version_string(version)}: {e}"
        raise RuntimeError(msg) from e

    # Extract the schema file
    try:
        schema_bytes = _extract_schema_from_tarball(tarball_bytes)
    except _ARCHIVE_ERRORS as e:
        msg = f"Failed to read release tarball for {version_string(version)}, which may be truncated: {type(e).__name__}: {e}"
        raise RuntimeError(msg) from e
    if schema_bytes is None:
        msg = f"Could not find {_SCHEMA_FILENAME} in release tarball for {version_string(version)}"
        raise RuntimeError(msg)

    # Write to target (atomic via temp file)
    with tempfile.NamedTemporaryFile(dir=target_dir, delete=False, suffix=".tmp") as tmp:
        tmp_path = Path(tmp.name)
        try:
            if compress:
                with gzip.open(tmp, "wb") as gz:
                    gz.write(schema_bytes)
            else:
                tmp.write(schema_bytes)
        except BaseException:
            tmp_path.unlink(missing_ok=True)
            raise

    try:
        shutil.move(str(tmp_path), str(target_path))
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
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


def _parse_version(text: str) -> tuple[int, int, int]:
    """Parse ``X.Y.Z``, with or without a leading ``v``, into a version tuple."""
    parts = text.removeprefix("v").split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        msg = f"{text!r} is not an EnergyPlus version of the form X.Y.Z"
        raise argparse.ArgumentTypeError(msg)
    return int(parts[0]), int(parts[1]), int(parts[2])


def main(argv: list[str] | None = None) -> int:
    """Download one schema from the command line.

    Exit codes: 0 the schema is present at the printed path, 1 the version is not supported or the
    download failed, 2 the arguments could not be read.
    """
    parser = argparse.ArgumentParser(
        prog="python -m idfkit.download",
        description="Download the epJSON schema of one supported EnergyPlus version.",
    )
    parser.add_argument("version", type=_parse_version, help="the EnergyPlus version, as X.Y.Z")
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=None,
        help="directory that receives VX-Y-Z/ (default: ~/.idfkit/schemas)",
    )
    parser.add_argument("--no-compress", action="store_true", help="store the schema uncompressed")
    args = parser.parse_args(argv)

    try:
        path = download_schema(args.version, target_dir=args.target_dir, compress=not args.no_compress)
    except (ValueError, RuntimeError, OSError) as error:
        # One line whatever the cause: the message of a failed transfer can span several.
        sys.stderr.write(f"error: {' '.join(str(error).split())}\n")
        return 1
    sys.stdout.write(f"{path}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
