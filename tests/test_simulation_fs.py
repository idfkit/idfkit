"""Tests for the file system abstraction module."""

from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest
from conftest import InMemoryFileSystem

from idfkit.simulation.fs import FileSystem, LocalFileSystem, S3FileSystem

# ---------------------------------------------------------------------------
# FileSystem protocol
# ---------------------------------------------------------------------------


class TestFileSystemProtocol:
    """Tests for the FileSystem protocol."""

    def test_local_satisfies_protocol(self) -> None:
        assert isinstance(LocalFileSystem(), FileSystem)

    def test_custom_class_satisfies_protocol(self) -> None:
        """A custom class implementing all methods passes isinstance."""

        class Custom:
            def read_bytes(self, path: str | Path) -> bytes:
                return b""

            def write_bytes(self, path: str | Path, data: bytes) -> None:
                pass

            def read_text(self, path: str | Path, encoding: str = "utf-8") -> str:
                return ""

            def write_text(self, path: str | Path, text: str, encoding: str = "utf-8") -> None:
                pass

            def exists(self, path: str | Path) -> bool:
                return False

            def makedirs(self, path: str | Path, *, exist_ok: bool = False) -> None:
                pass

            def copy(self, src: str | Path, dst: str | Path) -> None:
                pass

            def glob(self, path: str | Path, pattern: str) -> list[str]:
                return []

            def remove(self, path: str | Path) -> None:
                pass

        assert isinstance(Custom(), FileSystem)


# ---------------------------------------------------------------------------
# LocalFileSystem
# ---------------------------------------------------------------------------


class TestLocalFileSystem:
    """Tests for LocalFileSystem backed by tmp_path."""

    @pytest.fixture
    def fs(self) -> LocalFileSystem:
        return LocalFileSystem()

    def test_write_and_read_bytes(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "data.bin"
        fs.write_bytes(p, b"\x00\x01\x02")
        assert fs.read_bytes(p) == b"\x00\x01\x02"

    def test_write_and_read_text(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "hello.txt"
        fs.write_text(p, "hello world")
        assert fs.read_text(p) == "hello world"

    def test_read_text_encoding(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "latin.txt"
        fs.write_text(p, "caf\u00e9", encoding="latin-1")
        assert fs.read_text(p, encoding="latin-1") == "caf\u00e9"

    def test_exists_true(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "exists.txt"
        p.write_text("yes")
        assert fs.exists(p) is True

    def test_exists_false(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        assert fs.exists(tmp_path / "nope.txt") is False

    def test_makedirs(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        d = tmp_path / "a" / "b" / "c"
        fs.makedirs(d)
        assert d.is_dir()

    def test_makedirs_exist_ok(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        d = tmp_path / "existing"
        d.mkdir()
        # Should not raise
        fs.makedirs(d, exist_ok=True)

    def test_makedirs_raises_without_exist_ok(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        d = tmp_path / "existing2"
        d.mkdir()
        with pytest.raises(FileExistsError):
            fs.makedirs(d, exist_ok=False)

    def test_copy(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        src = tmp_path / "src.txt"
        dst = tmp_path / "dst.txt"
        src.write_text("content")
        fs.copy(src, dst)
        assert dst.read_text() == "content"

    def test_glob(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        (tmp_path / "c.csv").write_text("c")
        matches = fs.glob(tmp_path, "*.txt")
        assert len(matches) == 2
        names = {Path(m).name for m in matches}
        assert names == {"a.txt", "b.txt"}

    def test_remove(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "removeme.txt"
        p.write_text("bye")
        fs.remove(p)
        assert not p.exists()

    def test_read_nonexistent_raises(self, fs: LocalFileSystem, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            fs.read_bytes(tmp_path / "nope.bin")


# ---------------------------------------------------------------------------
# S3FileSystem
# ---------------------------------------------------------------------------


def _make_fake_boto3() -> ModuleType:
    """Create a fake boto3 module with a mocked client factory."""
    mod = ModuleType("boto3")
    mod.client = MagicMock()  # type: ignore[attr-defined]
    return mod


class TestS3FileSystem:
    """Tests for S3FileSystem."""

    def test_import_error_when_boto3_missing(self) -> None:
        with patch.dict(sys.modules, {"boto3": None}), pytest.raises(ImportError, match="boto3 is required"):
            S3FileSystem(bucket="test-bucket")

    def test_constructor_with_mocked_boto3(self) -> None:
        fake_boto3 = _make_fake_boto3()
        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            fs = S3FileSystem(bucket="my-bucket", prefix="results")
            assert fs._bucket == "my-bucket"
            assert fs._prefix == "results"
            fake_boto3.client.assert_called_once_with("s3")  # type: ignore[union-attr]

    def test_key_with_prefix(self) -> None:
        fake_boto3 = _make_fake_boto3()
        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            fs = S3FileSystem(bucket="b", prefix="pre/fix")
            assert fs._key("file.txt") == "pre/fix/file.txt"

    def test_key_without_prefix(self) -> None:
        fake_boto3 = _make_fake_boto3()
        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            fs = S3FileSystem(bucket="b", prefix="")
            assert fs._key("file.txt") == "file.txt"

    def test_makedirs_is_noop(self) -> None:
        fake_boto3 = _make_fake_boto3()
        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            fs = S3FileSystem(bucket="b")
            # Should not raise or call any S3 method
            fs.makedirs("some/dir", exist_ok=True)
            fs.makedirs("some/dir", exist_ok=False)


# ---------------------------------------------------------------------------
# Custom FileSystem (InMemoryFileSystem)
# ---------------------------------------------------------------------------


class TestCustomFileSystem:
    """Tests for a custom dict-backed FileSystem."""

    def test_isinstance_check(self) -> None:
        assert isinstance(InMemoryFileSystem(), FileSystem)
