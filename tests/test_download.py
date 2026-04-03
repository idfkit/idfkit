"""Tests for idfkit.download module."""

from __future__ import annotations

import gzip
import io
import json
import tarfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest

from idfkit.download import (
    _GITHUB_API_BASE,
    _SCHEMA_FILENAME,
    _SCHEMA_FILENAME_GZ,
    _extract_schema_from_tarball,
    _find_linux_tarball_url,
    _get_release_assets,
    download_all_schemas,
    download_schema,
)
from idfkit.versions import ENERGYPLUS_VERSIONS


def _make_tarball_bytes(schema_content: bytes, member_name: str = "EnergyPlus/Energy+.schema.epJSON") -> bytes:
    """Create an in-memory tar.gz containing a single file."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name=member_name)
        info.size = len(schema_content)
        tar.addfile(info, io.BytesIO(schema_content))
    return buf.getvalue()


def _make_assets(*, has_linux: bool = True) -> list[dict[str, Any]]:
    """Build a list of fake GitHub release assets."""
    assets: list[dict[str, Any]] = [
        {"name": "EnergyPlus-24.1.0-Windows-x86_64.zip", "browser_download_url": "https://example.com/win.zip"},
    ]
    if has_linux:
        assets.append({
            "name": "EnergyPlus-24.1.0-Linux-Ubuntu-22.04-x86_64.tar.gz",
            "browser_download_url": "https://example.com/linux.tar.gz",
        })
    return assets


def _mock_urlopen_response(data: bytes) -> MagicMock:
    """Create a MagicMock that behaves like a urlopen context manager response."""
    mock_resp = MagicMock()
    mock_resp.read.return_value = data
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


# ---------------------------------------------------------------------------
# _get_release_assets
# ---------------------------------------------------------------------------


@patch("idfkit.download.urlopen")
def test_get_release_assets(mock_urlopen: MagicMock) -> None:
    payload = {"assets": [{"name": "file.tar.gz"}]}
    mock_urlopen.return_value = _mock_urlopen_response(json.dumps(payload).encode())

    result = _get_release_assets((24, 1, 0))
    assert result == [{"name": "file.tar.gz"}]

    # Verify the constructed URL contains the expected version tag (v24.1.0)
    called_url: str = mock_urlopen.call_args[0][0].full_url
    assert called_url.startswith(_GITHUB_API_BASE)
    assert "v24.1.0" in called_url


@patch("idfkit.download.urlopen")
def test_get_release_assets_empty(mock_urlopen: MagicMock) -> None:
    mock_urlopen.return_value = _mock_urlopen_response(json.dumps({}).encode())

    result = _get_release_assets((24, 1, 0))
    assert result == []


# ---------------------------------------------------------------------------
# _find_linux_tarball_url
# ---------------------------------------------------------------------------


def test_find_linux_tarball_url_found() -> None:
    assets = _make_assets(has_linux=True)
    assert _find_linux_tarball_url(assets) == "https://example.com/linux.tar.gz"


def test_find_linux_tarball_url_not_found() -> None:
    assets = _make_assets(has_linux=False)
    assert _find_linux_tarball_url(assets) is None


def test_find_linux_tarball_url_empty() -> None:
    assert _find_linux_tarball_url([]) is None


# ---------------------------------------------------------------------------
# _extract_schema_from_tarball
# ---------------------------------------------------------------------------


def test_extract_schema_from_tarball_success() -> None:
    content = b'{"epJSON_schema_version": "24.1.0"}'
    tarball = _make_tarball_bytes(content)
    result = _extract_schema_from_tarball(tarball)
    assert result == content


def test_extract_schema_from_tarball_no_match() -> None:
    tarball = _make_tarball_bytes(b"data", member_name="other/file.txt")
    result = _extract_schema_from_tarball(tarball)
    assert result is None


def test_extract_schema_from_tarball_directory_member() -> None:
    """A directory member ending with the schema filename but not extractable returns None."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        # Add a directory entry whose name ends with the schema filename
        info = tarfile.TarInfo(name="EnergyPlus/Energy+.schema.epJSON")
        info.type = tarfile.DIRTYPE
        tar.addfile(info)
    result = _extract_schema_from_tarball(buf.getvalue())
    assert result is None


# ---------------------------------------------------------------------------
# download_schema
# ---------------------------------------------------------------------------


def test_download_schema_unsupported_version(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not a supported"):
        download_schema((99, 99, 99), target_dir=tmp_path)


def test_download_schema_already_exists(tmp_path: Path) -> None:
    """If the target file already exists, return it immediately without downloading."""
    target = tmp_path / "V24-1-0"
    target.mkdir(parents=True)
    existing = target / _SCHEMA_FILENAME_GZ
    existing.write_bytes(b"cached")

    result = download_schema((24, 1, 0), target_dir=tmp_path, compress=True)
    assert result == existing


def test_download_schema_already_exists_uncompressed(tmp_path: Path) -> None:
    target = tmp_path / "V24-1-0"
    target.mkdir(parents=True)
    existing = target / _SCHEMA_FILENAME
    existing.write_bytes(b"cached")

    result = download_schema((24, 1, 0), target_dir=tmp_path, compress=False)
    assert result == existing


@patch("idfkit.download._get_release_assets")
def test_download_schema_release_fetch_error(mock_assets: MagicMock, tmp_path: Path) -> None:
    mock_assets.side_effect = HTTPError("url", 404, "Not Found", {}, None)  # type: ignore[arg-type]
    with pytest.raises(RuntimeError, match="Failed to fetch release info"):
        download_schema((24, 1, 0), target_dir=tmp_path)


@patch("idfkit.download._get_release_assets")
def test_download_schema_release_fetch_url_error(mock_assets: MagicMock, tmp_path: Path) -> None:
    mock_assets.side_effect = URLError("connection refused")
    with pytest.raises(RuntimeError, match="Failed to fetch release info"):
        download_schema((24, 1, 0), target_dir=tmp_path)


@patch("idfkit.download._get_release_assets")
def test_download_schema_release_fetch_timeout(mock_assets: MagicMock, tmp_path: Path) -> None:
    mock_assets.side_effect = TimeoutError("timed out")
    with pytest.raises(RuntimeError, match="Failed to fetch release info"):
        download_schema((24, 1, 0), target_dir=tmp_path)


@patch("idfkit.download._get_release_assets")
def test_download_schema_no_linux_tarball(mock_assets: MagicMock, tmp_path: Path) -> None:
    mock_assets.return_value = _make_assets(has_linux=False)
    with pytest.raises(RuntimeError, match="No Linux tarball found"):
        download_schema((24, 1, 0), target_dir=tmp_path)


@patch("idfkit.download.urlopen")
@patch("idfkit.download._get_release_assets")
def test_download_schema_tarball_download_error(
    mock_assets: MagicMock, mock_urlopen: MagicMock, tmp_path: Path
) -> None:
    mock_assets.return_value = _make_assets(has_linux=True)
    mock_urlopen.side_effect = HTTPError("url", 500, "Server Error", {}, None)  # type: ignore[arg-type]
    with pytest.raises(RuntimeError, match="Failed to download tarball"):
        download_schema((24, 1, 0), target_dir=tmp_path)


@patch("idfkit.download.urlopen")
@patch("idfkit.download._get_release_assets")
def test_download_schema_tarball_download_url_error(
    mock_assets: MagicMock, mock_urlopen: MagicMock, tmp_path: Path
) -> None:
    mock_assets.return_value = _make_assets(has_linux=True)
    mock_urlopen.side_effect = URLError("timeout")
    with pytest.raises(RuntimeError, match="Failed to download tarball"):
        download_schema((24, 1, 0), target_dir=tmp_path)


@patch("idfkit.download.urlopen")
@patch("idfkit.download._get_release_assets")
def test_download_schema_tarball_download_timeout(
    mock_assets: MagicMock, mock_urlopen: MagicMock, tmp_path: Path
) -> None:
    mock_assets.return_value = _make_assets(has_linux=True)
    mock_urlopen.side_effect = TimeoutError("timed out")
    with pytest.raises(RuntimeError, match="Failed to download tarball"):
        download_schema((24, 1, 0), target_dir=tmp_path)


@patch("idfkit.download.urlopen")
@patch("idfkit.download._get_release_assets")
def test_download_schema_schema_not_in_tarball(mock_assets: MagicMock, mock_urlopen: MagicMock, tmp_path: Path) -> None:
    mock_assets.return_value = _make_assets(has_linux=True)
    tarball = _make_tarball_bytes(b"data", member_name="other/file.txt")
    mock_urlopen.return_value = _mock_urlopen_response(tarball)

    with pytest.raises(RuntimeError, match="Could not find"):
        download_schema((24, 1, 0), target_dir=tmp_path)


@patch("idfkit.download.urlopen")
@patch("idfkit.download._get_release_assets")
def test_download_schema_success_compressed(mock_assets: MagicMock, mock_urlopen: MagicMock, tmp_path: Path) -> None:
    schema_content = b'{"epJSON_schema_version": "24.1.0"}'
    mock_assets.return_value = _make_assets(has_linux=True)
    mock_urlopen.return_value = _mock_urlopen_response(_make_tarball_bytes(schema_content))

    result = download_schema((24, 1, 0), target_dir=tmp_path, compress=True)
    assert result.name == _SCHEMA_FILENAME_GZ
    assert result.exists()
    with gzip.open(result, "rb") as f:
        assert f.read() == schema_content


@patch("idfkit.download.urlopen")
@patch("idfkit.download._get_release_assets")
def test_download_schema_success_uncompressed(mock_assets: MagicMock, mock_urlopen: MagicMock, tmp_path: Path) -> None:
    schema_content = b'{"epJSON_schema_version": "24.1.0"}'
    mock_assets.return_value = _make_assets(has_linux=True)
    mock_urlopen.return_value = _mock_urlopen_response(_make_tarball_bytes(schema_content))

    result = download_schema((24, 1, 0), target_dir=tmp_path, compress=False)
    assert result.name == _SCHEMA_FILENAME
    assert result.exists()
    assert result.read_bytes() == schema_content


@patch("idfkit.download.urlopen")
@patch("idfkit.download._get_release_assets")
def test_download_schema_default_target_dir(mock_assets: MagicMock, mock_urlopen: MagicMock, tmp_path: Path) -> None:
    """When target_dir is None, uses ~/.idfkit/schemas/."""
    schema_content = b'{"epJSON_schema_version": "24.1.0"}'
    mock_assets.return_value = _make_assets(has_linux=True)
    mock_urlopen.return_value = _mock_urlopen_response(_make_tarball_bytes(schema_content))

    fake_home = tmp_path / "fakehome"
    fake_home.mkdir()
    with patch("idfkit.download.Path.home", return_value=fake_home):
        result = download_schema((24, 1, 0), target_dir=None, compress=True)

    assert fake_home / ".idfkit" / "schemas" / "V24-1-0" / _SCHEMA_FILENAME_GZ == result
    assert result.exists()


# ---------------------------------------------------------------------------
# download_all_schemas
# ---------------------------------------------------------------------------


@patch("idfkit.download.download_schema")
def test_download_all_schemas_success(mock_download: MagicMock, tmp_path: Path) -> None:
    mock_download.return_value = tmp_path / "schema.epJSON.gz"
    results = download_all_schemas(target_dir=tmp_path, compress=True)
    assert all(isinstance(v, Path) for v in results.values())
    assert mock_download.call_count > 0
    # Keys must be exactly the supported version tuples
    assert set(results.keys()) == set(ENERGYPLUS_VERSIONS)


@patch("idfkit.download.download_schema")
def test_download_all_schemas_with_failures(mock_download: MagicMock, tmp_path: Path) -> None:
    mock_download.side_effect = RuntimeError("download failed")
    results = download_all_schemas(target_dir=tmp_path)
    assert all(isinstance(v, Exception) for v in results.values())


@patch("idfkit.download.download_schema")
def test_download_all_schemas_default_target_dir(mock_download: MagicMock, tmp_path: Path) -> None:
    """When target_dir is None, the base_dir logic branches differently."""
    mock_download.return_value = tmp_path / "schema.epJSON.gz"
    fake_home = tmp_path / "fakehome"
    with patch("idfkit.download.Path.home", return_value=fake_home):
        results = download_all_schemas(target_dir=None, compress=True)
    assert all(isinstance(v, Path) for v in results.values())
    # Verify download_schema was called with the expected target_dir derived from Path.home()
    expected_target_dir = fake_home / ".idfkit"
    for call in mock_download.call_args_list:
        if "target_dir" in call.kwargs:
            target_dir = call.kwargs["target_dir"]
        elif len(call.args) >= 2:
            target_dir = call.args[1]
        else:
            target_dir = None
        assert target_dir == expected_target_dir
