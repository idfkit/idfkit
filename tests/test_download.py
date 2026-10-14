"""Tests for idfkit.download module."""

from __future__ import annotations

import gzip
import io
import json
import tarfile
from email.message import Message
from http.client import IncompleteRead
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request

import pytest

from idfkit.download import (
    _GITHUB_API_BASE,
    _SCHEMA_FILENAME,
    _SCHEMA_FILENAME_GZ,
    _extract_schema_from_tarball,
    _find_linux_tarball_url,
    _get_release_assets,
    _request,
    download_all_schemas,
    download_schema,
)
from idfkit.download import main as download_main
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


def test_find_linux_tarball_url_prefers_ubuntu_x86_64() -> None:
    """Releases since 26.1.0 list an AlmaLinux tarball and an arm64 tarball ahead of it."""
    assets: list[dict[str, Any]] = [
        {"name": "EnergyPlus-26.2.0-4bd7a1f26f-Linux-AlmaLinux9.6-x86_64.tar.gz", "browser_download_url": "alma"},
        {"name": "EnergyPlus-26.2.0-4bd7a1f26f-Linux-Ubuntu24.04-arm64.tar.gz", "browser_download_url": "arm"},
        {"name": "EnergyPlus-26.2.0-4bd7a1f26f-Linux-Ubuntu24.04-x86_64.sh", "browser_download_url": "installer"},
        {"name": "EnergyPlus-26.2.0-4bd7a1f26f-Linux-Ubuntu24.04-x86_64.tar.gz", "browser_download_url": "ubuntu"},
    ]
    assert _find_linux_tarball_url(assets) == "ubuntu"


def test_find_linux_tarball_url_falls_back_to_another_linux_tarball() -> None:
    assets: list[dict[str, Any]] = [
        {"name": "EnergyPlus-26.2.0-4bd7a1f26f-Linux-AlmaLinux9.6-x86_64.tar.gz", "browser_download_url": "alma"},
        {"name": "EnergyPlus-26.2.0-4bd7a1f26f-Windows-x86_64.zip", "browser_download_url": "windows"},
    ]
    assert _find_linux_tarball_url(assets) == "alma"


# ---------------------------------------------------------------------------
# python -m idfkit.download
# ---------------------------------------------------------------------------


class TestCommandLine:
    """The entry point the EnergyPlus adoption roster calls to bundle a schema."""

    def test_the_schema_is_written_under_the_target_and_its_path_printed(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        content = b'{"epJSON_schema_version": "24.1.0"}'
        responses = [
            _mock_urlopen_response(json.dumps({"assets": _make_assets()}).encode()),
            _mock_urlopen_response(_make_tarball_bytes(content)),
        ]
        with patch("idfkit.download.urlopen", side_effect=responses):
            code = download_main(["24.1.0", "--target-dir", str(tmp_path)])

        target = tmp_path / "V24-1-0" / _SCHEMA_FILENAME_GZ
        assert code == 0
        assert gzip.decompress(target.read_bytes()) == content
        assert capsys.readouterr().out.strip() == str(target)

    def test_a_present_schema_is_not_downloaded_again(self, tmp_path: Path) -> None:
        target = tmp_path / "V24-1-0" / _SCHEMA_FILENAME_GZ
        target.parent.mkdir(parents=True)
        target.write_bytes(b"present")

        with patch("idfkit.download.urlopen", side_effect=AssertionError("the network was used")):
            code = download_main(["v24.1.0", "--target-dir", str(tmp_path)])

        assert code == 0
        assert target.read_bytes() == b"present"

    def test_an_unregistered_version_is_refused(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        code = download_main(["99.9.9", "--target-dir", str(tmp_path)])

        assert code == 1
        assert "not a supported EnergyPlus version" in capsys.readouterr().err
        assert not (tmp_path / "V99-9-9").exists()

    def test_a_malformed_version_is_refused(self) -> None:
        with pytest.raises(SystemExit) as stopped:
            download_main(["26.2"])

        assert stopped.value.code == 2


# ---------------------------------------------------------------------------
# Authentication of the request to api.github.com
# ---------------------------------------------------------------------------

_API_ASSETS = [
    {
        "name": "EnergyPlus-24.1.0-Linux-Ubuntu-22.04-x86_64.tar.gz",
        "browser_download_url": "https://github.com/NatLabRockies/EnergyPlus/releases/download/v24.1.0/linux.tar.gz",
    }
]


@pytest.fixture
def no_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove both variables, which a developer's shell and a workflow runner both set."""
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)


def _requests_of_one_download(tmp_path: Path) -> list[Request]:
    """Run one successful download with the network replaced, and return the requests it issued."""
    responses = [
        _mock_urlopen_response(json.dumps({"assets": _API_ASSETS}).encode()),
        _mock_urlopen_response(_make_tarball_bytes(b"{}")),
    ]
    with patch("idfkit.download.urlopen", side_effect=responses) as opened:
        download_schema((24, 1, 0), target_dir=tmp_path)
    return [call.args[0] for call in opened.call_args_list]


@pytest.mark.usefixtures("no_token")
class TestAuthentication:
    """The token goes to api.github.com, and nowhere else."""

    def test_the_token_is_sent_to_the_api_when_set(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GITHUB_TOKEN", "secret")

        api, asset = _requests_of_one_download(tmp_path)

        assert api.host == "api.github.com"
        assert api.get_header("Authorization") == "Bearer secret"
        assert api.get_header("Accept") == "application/vnd.github.v3+json"
        assert asset.host == "github.com"

    def test_gh_token_is_preferred_to_github_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GITHUB_TOKEN", "second")
        monkeypatch.setenv("GH_TOKEN", "first")

        assert _request(f"{_GITHUB_API_BASE}/v24.1.0").get_header("Authorization") == "Bearer first"

    def test_an_empty_gh_token_yields_to_github_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GH_TOKEN", "")
        monkeypatch.setenv("GITHUB_TOKEN", "second")

        assert _request(f"{_GITHUB_API_BASE}/v24.1.0").get_header("Authorization") == "Bearer second"

    def test_no_header_is_sent_when_neither_variable_is_set(self, tmp_path: Path) -> None:
        api, asset = _requests_of_one_download(tmp_path)

        assert not api.has_header("Authorization")
        assert not asset.has_header("Authorization")
        assert api.header_items() == [("Accept", "application/vnd.github.v3+json")]
        assert asset.header_items() == []

    def test_the_token_is_not_sent_to_the_asset_host(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GH_TOKEN", "secret")

        _, asset = _requests_of_one_download(tmp_path)

        assert not asset.has_header("Authorization")
        assert "secret" not in str(asset.header_items())

    @pytest.mark.parametrize(
        "url",
        [
            "https://github.com/NatLabRockies/EnergyPlus/releases/download/v24.1.0/linux.tar.gz",
            "https://objects.githubusercontent.com/asset",
            "https://api.github.com.example.org/repos",
            "https://example.org/api.github.com",
            "http://api.github.com/repos/NatLabRockies/EnergyPlus/releases/tags/v24.1.0",
        ],
    )
    def test_the_token_is_never_sent_to_another_host(self, url: str, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GH_TOKEN", "secret")

        assert not _request(url).has_header("Authorization")

    @pytest.mark.parametrize("target", ["https://example.org/elsewhere", "https://api.github.com/repositories/1"])
    def test_the_token_does_not_follow_a_redirect(self, target: str, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GH_TOKEN", "secret")
        original = _request(f"{_GITHUB_API_BASE}/v24.1.0", headers={"Accept": "application/vnd.github.v3+json"})
        assert original.has_header("Authorization")

        followed = HTTPRedirectHandler().redirect_request(original, io.BytesIO(), 301, "Moved", Message(), target)

        assert followed is not None
        assert followed.get_header("Accept") == "application/vnd.github.v3+json"
        assert not followed.has_header("Authorization")


# ---------------------------------------------------------------------------
# A failed download leaves nothing behind
# ---------------------------------------------------------------------------


def _truncated_tarball() -> bytes:
    """An archive cut off part of the way through, as an interrupted download leaves it."""
    whole = _make_tarball_bytes(bytes(range(256)) * 400)
    return whole[: len(whole) // 2]


def _incomplete_read() -> MagicMock:
    response = _mock_urlopen_response(b"")
    response.read.side_effect = IncompleteRead(b"partial", 1000)
    return response


_FAILING_DOWNLOADS = {
    "truncated archive": (lambda: _mock_urlopen_response(_truncated_tarball()), "Failed to read release tarball"),
    "not an archive": (lambda: _mock_urlopen_response(b"<html>rate limited</html>"), "Failed to read release tarball"),
    "body cut short": (_incomplete_read, "Failed to download tarball"),
    "schema absent": (lambda: _mock_urlopen_response(_make_tarball_bytes(b"x", "other.txt")), "Could not find"),
}


@pytest.mark.usefixtures("no_token")
class TestFailedDownload:
    """A failure removes the version directory the call created, and is reported on one line."""

    @pytest.mark.parametrize("case", sorted(_FAILING_DOWNLOADS))
    def test_a_directory_the_call_created_is_removed(self, case: str, tmp_path: Path) -> None:
        response, message = _FAILING_DOWNLOADS[case]
        responses = [_mock_urlopen_response(json.dumps({"assets": _API_ASSETS}).encode()), response()]

        with patch("idfkit.download.urlopen", side_effect=responses), pytest.raises(RuntimeError, match=message):
            download_schema((24, 1, 0), target_dir=tmp_path)

        assert not (tmp_path / "V24-1-0").exists()
        assert tmp_path.is_dir()

    def test_a_directory_is_removed_when_the_release_cannot_be_read(self, tmp_path: Path) -> None:
        with (
            patch("idfkit.download.urlopen", side_effect=ConnectionResetError("reset by peer")),
            pytest.raises(RuntimeError, match="Failed to fetch release info"),
        ):
            download_schema((24, 1, 0), target_dir=tmp_path)

        assert not (tmp_path / "V24-1-0").exists()

    @pytest.mark.parametrize("case", sorted(_FAILING_DOWNLOADS))
    def test_a_directory_that_existed_before_the_call_is_kept(self, case: str, tmp_path: Path) -> None:
        response, _ = _FAILING_DOWNLOADS[case]
        existing = tmp_path / "V24-1-0"
        existing.mkdir()
        (existing / "note.txt").write_text("kept")
        responses = [_mock_urlopen_response(json.dumps({"assets": _API_ASSETS}).encode()), response()]

        with patch("idfkit.download.urlopen", side_effect=responses), pytest.raises(RuntimeError):
            download_schema((24, 1, 0), target_dir=tmp_path)

        assert [entry.name for entry in existing.iterdir()] == ["note.txt"]

    def test_a_failed_write_leaves_no_temporary_file(self, tmp_path: Path) -> None:
        existing = tmp_path / "V24-1-0"
        existing.mkdir()
        responses = [
            _mock_urlopen_response(json.dumps({"assets": _API_ASSETS}).encode()),
            _mock_urlopen_response(_make_tarball_bytes(b"{}")),
        ]

        with (
            patch("idfkit.download.urlopen", side_effect=responses),
            patch("idfkit.download.shutil.move", side_effect=OSError(28, "No space left on device")),
            pytest.raises(OSError, match="No space left"),
        ):
            download_schema((24, 1, 0), target_dir=tmp_path)

        assert list(existing.iterdir()) == []

    @pytest.mark.parametrize("case", sorted(_FAILING_DOWNLOADS))
    def test_the_command_reports_the_cause_on_one_line_and_exits_1(
        self, case: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        response, message = _FAILING_DOWNLOADS[case]
        responses = [_mock_urlopen_response(json.dumps({"assets": _API_ASSETS}).encode()), response()]

        with patch("idfkit.download.urlopen", side_effect=responses):
            code = download_main(["24.1.0", "--target-dir", str(tmp_path)])

        captured = capsys.readouterr()
        assert code == 1
        assert captured.out == ""
        assert captured.err.startswith("error: ")
        assert message in captured.err
        assert captured.err.count("\n") == 1
        assert not (tmp_path / "V24-1-0").exists()

    def test_the_command_reports_an_unwritable_target_and_exits_1(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        blocker = tmp_path / "file"
        blocker.write_text("not a directory")

        with patch("idfkit.download.urlopen", side_effect=AssertionError("the network was used")):
            code = download_main(["24.1.0", "--target-dir", str(blocker)])

        assert code == 1
        assert capsys.readouterr().err.startswith("error: ")
