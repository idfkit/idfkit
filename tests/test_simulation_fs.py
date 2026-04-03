"""Tests for the file system abstraction module."""

from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from conftest import InMemoryAsyncFileSystem, InMemoryFileSystem

from idfkit.simulation.fs import (
    AsyncFileSystem,
    AsyncLocalFileSystem,
    AsyncS3FileSystem,
    FileSystem,
    LocalFileSystem,
    S3FileSystem,
)

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
# AsyncS3FileSystem
# ---------------------------------------------------------------------------


def _make_fake_aiobotocore() -> ModuleType:
    """Create a fake aiobotocore.session module with a mocked get_session."""
    session_mod = ModuleType("aiobotocore.session")

    mock_session = MagicMock()

    def get_session() -> MagicMock:  # type: ignore[return-value]
        return mock_session

    session_mod.get_session = get_session  # type: ignore[attr-defined]
    return session_mod


class TestAsyncS3FileSystem:
    """Tests for AsyncS3FileSystem."""

    def test_import_error_when_aiobotocore_missing(self) -> None:
        with (
            patch.dict(sys.modules, {"aiobotocore": None, "aiobotocore.session": None}),
            pytest.raises(ImportError, match="aiobotocore is required"),
        ):
            AsyncS3FileSystem(bucket="test-bucket")

    def test_constructor_with_mocked_aiobotocore(self) -> None:
        fake_mod = _make_fake_aiobotocore()
        # Need both aiobotocore and aiobotocore.session to pass import
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="my-bucket", prefix="results")
            assert fs._bucket == "my-bucket"
            assert fs._prefix == "results"

    def test_key_with_prefix(self) -> None:
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="b", prefix="pre/fix")
            assert fs._key("file.txt") == "pre/fix/file.txt"

    def test_key_without_prefix(self) -> None:
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="b", prefix="")
            assert fs._key("file.txt") == "file.txt"

    @pytest.mark.asyncio
    async def test_makedirs_is_noop(self) -> None:
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="b")
            # Should not raise or need a client
            await fs.makedirs("some/dir", exist_ok=True)
            await fs.makedirs("some/dir", exist_ok=False)

    def test_ensure_client_raises_without_context(self) -> None:
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="b")
            with pytest.raises(RuntimeError, match="not initialised"):
                fs._ensure_client()

    def test_is_detected_as_async_fs(self) -> None:
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            from idfkit.simulation.async_runner import _is_async_fs

            fs = AsyncS3FileSystem(bucket="b")
            assert _is_async_fs(fs)


# ---------------------------------------------------------------------------
# Custom FileSystem (InMemoryFileSystem)
# ---------------------------------------------------------------------------


class TestCustomFileSystem:
    """Tests for a custom dict-backed FileSystem."""

    def test_isinstance_check(self) -> None:
        assert isinstance(InMemoryFileSystem(), FileSystem)


# ---------------------------------------------------------------------------
# AsyncFileSystem protocol
# ---------------------------------------------------------------------------


class TestAsyncFileSystemProtocol:
    """Tests for the AsyncFileSystem protocol."""

    def test_async_local_satisfies_protocol(self) -> None:
        assert isinstance(AsyncLocalFileSystem(), AsyncFileSystem)

    def test_in_memory_async_satisfies_protocol(self) -> None:
        assert isinstance(InMemoryAsyncFileSystem(), AsyncFileSystem)

    def test_sync_fs_does_not_match_async_protocol(self) -> None:
        """A sync FileSystem should not satisfy AsyncFileSystem isinstance check."""
        # sync methods are not coroutines, so runtime_checkable only checks
        # attribute existence — but we document the intended usage.
        fs = LocalFileSystem()
        # isinstance will pass because runtime_checkable only checks attr existence;
        # the actual distinction is made via inspect.iscoroutinefunction at runtime.
        # This test verifies that the helper function can distinguish them.
        from idfkit.simulation.async_runner import _is_async_fs

        assert not _is_async_fs(fs)

    def test_async_fs_detected_by_helper(self) -> None:
        from idfkit.simulation.async_runner import _is_async_fs

        assert _is_async_fs(AsyncLocalFileSystem())
        assert _is_async_fs(InMemoryAsyncFileSystem())


# ---------------------------------------------------------------------------
# AsyncLocalFileSystem
# ---------------------------------------------------------------------------


class TestAsyncLocalFileSystem:
    """Tests for AsyncLocalFileSystem backed by tmp_path."""

    @pytest.fixture
    def fs(self) -> AsyncLocalFileSystem:
        return AsyncLocalFileSystem()

    @pytest.mark.asyncio
    async def test_write_and_read_bytes(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "data.bin"
        await fs.write_bytes(p, b"\x00\x01\x02")
        assert await fs.read_bytes(p) == b"\x00\x01\x02"

    @pytest.mark.asyncio
    async def test_write_and_read_text(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "hello.txt"
        await fs.write_text(p, "hello world")
        assert await fs.read_text(p) == "hello world"

    @pytest.mark.asyncio
    async def test_read_text_encoding(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "latin.txt"
        await fs.write_text(p, "caf\u00e9", encoding="latin-1")
        assert await fs.read_text(p, encoding="latin-1") == "caf\u00e9"

    @pytest.mark.asyncio
    async def test_exists(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "exists.txt"
        assert await fs.exists(p) is False
        p.write_text("yes")
        assert await fs.exists(p) is True

    @pytest.mark.asyncio
    async def test_makedirs(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        d = tmp_path / "a" / "b" / "c"
        await fs.makedirs(d)
        assert d.is_dir()

    @pytest.mark.asyncio
    async def test_copy(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        src = tmp_path / "src.txt"
        dst = tmp_path / "dst.txt"
        src.write_text("content")
        await fs.copy(src, dst)
        assert dst.read_text() == "content"

    @pytest.mark.asyncio
    async def test_glob(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        (tmp_path / "c.csv").write_text("c")
        matches = await fs.glob(tmp_path, "*.txt")
        assert len(matches) == 2
        names = {Path(m).name for m in matches}
        assert names == {"a.txt", "b.txt"}

    @pytest.mark.asyncio
    async def test_remove(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        p = tmp_path / "removeme.txt"
        p.write_text("bye")
        await fs.remove(p)
        assert not p.exists()

    @pytest.mark.asyncio
    async def test_read_nonexistent_raises(self, fs: AsyncLocalFileSystem, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            await fs.read_bytes(tmp_path / "nope.bin")


# ---------------------------------------------------------------------------
# S3FileSystem — mocked S3 operations
# ---------------------------------------------------------------------------


def _make_s3fs(prefix: str = "pfx") -> tuple[S3FileSystem, MagicMock]:
    """Create an S3FileSystem with a mocked boto3 client."""
    fake_boto3 = _make_fake_boto3()
    mock_client = MagicMock()
    fake_boto3.client = MagicMock(return_value=mock_client)  # type: ignore[attr-defined]
    with patch.dict(sys.modules, {"boto3": fake_boto3}):
        fs = S3FileSystem(bucket="bkt", prefix=prefix)
    return fs, mock_client


class TestS3FileSystemOperations:
    """Tests for S3FileSystem read/write/copy/glob/remove operations."""

    def test_read_bytes(self) -> None:
        fs, client = _make_s3fs()
        body_mock = MagicMock()
        body_mock.read.return_value = b"hello"
        client.get_object.return_value = {"Body": body_mock}

        result = fs.read_bytes("file.txt")

        assert result == b"hello"
        client.get_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt")

    def test_write_bytes(self) -> None:
        fs, client = _make_s3fs()
        fs.write_bytes("file.txt", b"data")
        client.put_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt", Body=b"data")

    def test_read_text(self) -> None:
        fs, client = _make_s3fs()
        body_mock = MagicMock()
        body_mock.read.return_value = "caf\u00e9".encode()
        client.get_object.return_value = {"Body": body_mock}

        assert fs.read_text("file.txt") == "caf\u00e9"

    def test_write_text(self) -> None:
        fs, client = _make_s3fs()
        fs.write_text("file.txt", "hello", encoding="utf-8")
        client.put_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt", Body=b"hello")

    def test_exists_true(self) -> None:
        fs, client = _make_s3fs()
        assert fs.exists("file.txt") is True
        client.head_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt")

    def test_exists_false(self) -> None:
        fs, client = _make_s3fs()
        client.head_object.side_effect = Exception("not found")
        assert fs.exists("file.txt") is False

    def test_copy(self) -> None:
        fs, client = _make_s3fs()
        fs.copy("src.txt", "dst.txt")
        client.copy_object.assert_called_once_with(
            Bucket="bkt",
            CopySource={"Bucket": "bkt", "Key": "pfx/src.txt"},
            Key="pfx/dst.txt",
        )

    def test_glob_matches(self) -> None:
        fs, client = _make_s3fs()
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [
            {
                "Contents": [
                    {"Key": "pfx/dir/a.sql"},
                    {"Key": "pfx/dir/b.csv"},
                    {"Key": "pfx/dir/c.sql"},
                    {"Key": ""},  # empty key — should be skipped
                ]
            },
        ]
        result = fs.glob("dir", "*.sql")
        assert result == ["dir/a.sql", "dir/c.sql"]

    def test_glob_no_contents(self) -> None:
        fs, client = _make_s3fs()
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{}]  # no "Contents" key
        assert fs.glob("dir", "*.sql") == []

    def test_remove(self) -> None:
        fs, client = _make_s3fs()
        fs.remove("file.txt")
        client.delete_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt")


# ---------------------------------------------------------------------------
# AsyncS3FileSystem — mocked async S3 operations
# ---------------------------------------------------------------------------


def _make_async_s3fs(prefix: str = "pfx") -> tuple[AsyncS3FileSystem, MagicMock]:
    """Create an AsyncS3FileSystem with a mocked aiobotocore session, pre-initialised."""
    fake_mod = _make_fake_aiobotocore()
    fake_parent = ModuleType("aiobotocore")
    with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
        fs = AsyncS3FileSystem(bucket="bkt", prefix=prefix)
    # Inject a mock client directly to avoid needing __aenter__
    mock_client = MagicMock()
    fs._client = mock_client  # type: ignore[assignment]
    return fs, mock_client


class TestAsyncS3FileSystemOperations:
    """Tests for AsyncS3FileSystem async read/write/copy/glob/remove operations."""

    @pytest.mark.asyncio
    async def test_aenter_aexit(self) -> None:
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="bkt", prefix="pfx")

        mock_client = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_client)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)
        fs._session = MagicMock()
        fs._session.create_client = MagicMock(return_value=mock_ctx)

        result = await fs.__aenter__()
        assert result is fs
        assert fs._client is mock_client

        await fs.__aexit__(None, None, None)
        assert fs._client is None
        assert fs._client_ctx is None

    @pytest.mark.asyncio
    async def test_aexit_without_ctx(self) -> None:
        """__aexit__ with no client_ctx should be a no-op."""
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="bkt")
        assert fs._client_ctx is None
        await fs.__aexit__(None, None, None)  # should not raise

    @pytest.mark.asyncio
    async def test_read_bytes(self) -> None:
        fs, client = _make_async_s3fs()
        stream_mock = AsyncMock()
        stream_mock.read = AsyncMock(return_value=b"data")

        resp_body = MagicMock()
        resp_body.__aenter__ = AsyncMock(return_value=stream_mock)
        resp_body.__aexit__ = AsyncMock(return_value=None)

        client.get_object = AsyncMock(return_value={"Body": resp_body})

        result = await fs.read_bytes("file.txt")
        assert result == b"data"
        client.get_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt")

    @pytest.mark.asyncio
    async def test_write_bytes(self) -> None:
        fs, client = _make_async_s3fs()
        client.put_object = AsyncMock()
        await fs.write_bytes("file.txt", b"payload")
        client.put_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt", Body=b"payload")

    @pytest.mark.asyncio
    async def test_read_text(self) -> None:
        fs, client = _make_async_s3fs()
        stream_mock = AsyncMock()
        stream_mock.read = AsyncMock(return_value="caf\u00e9".encode())

        resp_body = MagicMock()
        resp_body.__aenter__ = AsyncMock(return_value=stream_mock)
        resp_body.__aexit__ = AsyncMock(return_value=None)
        client.get_object = AsyncMock(return_value={"Body": resp_body})

        assert await fs.read_text("file.txt") == "caf\u00e9"

    @pytest.mark.asyncio
    async def test_write_text(self) -> None:
        fs, client = _make_async_s3fs()
        client.put_object = AsyncMock()
        await fs.write_text("file.txt", "hello")
        client.put_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt", Body=b"hello")

    @pytest.mark.asyncio
    async def test_exists_true(self) -> None:
        fs, client = _make_async_s3fs()
        client.head_object = AsyncMock()
        assert await fs.exists("file.txt") is True

    @pytest.mark.asyncio
    async def test_exists_false(self) -> None:
        fs, client = _make_async_s3fs()
        client.head_object = AsyncMock(side_effect=Exception("not found"))
        assert await fs.exists("file.txt") is False

    @pytest.mark.asyncio
    async def test_copy(self) -> None:
        fs, client = _make_async_s3fs()
        client.copy_object = AsyncMock()
        await fs.copy("src.txt", "dst.txt")
        client.copy_object.assert_called_once_with(
            Bucket="bkt",
            CopySource={"Bucket": "bkt", "Key": "pfx/src.txt"},
            Key="pfx/dst.txt",
        )

    @pytest.mark.asyncio
    async def test_glob_matches(self) -> None:
        fs, client = _make_async_s3fs()

        async def _fake_paginate(**kwargs: Any) -> Any:
            yield {
                "Contents": [
                    {"Key": "pfx/dir/a.sql"},
                    {"Key": "pfx/dir/b.csv"},
                    {"Key": "pfx/dir/c.sql"},
                    {"Key": ""},  # empty — skipped
                ]
            }

        paginator = MagicMock()
        paginator.paginate = _fake_paginate
        client.get_paginator = MagicMock(return_value=paginator)

        result = await fs.glob("dir", "*.sql")
        assert result == ["dir/a.sql", "dir/c.sql"]

    @pytest.mark.asyncio
    async def test_glob_no_contents(self) -> None:
        fs, client = _make_async_s3fs()

        async def _fake_paginate(**kwargs: Any) -> Any:
            yield {}

        paginator = MagicMock()
        paginator.paginate = _fake_paginate
        client.get_paginator = MagicMock(return_value=paginator)

        assert await fs.glob("dir", "*.sql") == []

    @pytest.mark.asyncio
    async def test_remove(self) -> None:
        fs, client = _make_async_s3fs()
        client.delete_object = AsyncMock()
        await fs.remove("file.txt")
        client.delete_object.assert_called_once_with(Bucket="bkt", Key="pfx/file.txt")

    @pytest.mark.asyncio
    async def test_context_manager_exercises_ensure_client(self) -> None:
        """Entering via 'async with' wires up _client so _ensure_client succeeds."""
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="bkt", prefix="pfx")

        # Confirm client is None before entering the context manager.
        assert fs._client is None

        mock_client = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_client)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)
        fs._session = MagicMock()
        fs._session.create_client = MagicMock(return_value=mock_ctx)

        # Enter via the context-manager protocol (async with), not __aenter__ directly.
        async with fs:
            # _ensure_client must now return the live client without raising.
            assert fs._ensure_client() is mock_client

        # After exit the client is cleaned up.
        assert fs._client is None


# ---------------------------------------------------------------------------
# makedirs no-op / return-value tests
# ---------------------------------------------------------------------------


class TestMakedirsNoop:
    """Ensure makedirs is a no-op and returns None for S3 backends."""

    def test_s3_makedirs_returns_none(self) -> None:
        fake_boto3 = _make_fake_boto3()
        mock_client = MagicMock()
        fake_boto3.client = MagicMock(return_value=mock_client)  # type: ignore[attr-defined]
        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            fs = S3FileSystem(bucket="bkt")
        result = fs.makedirs("any/path", exist_ok=True)
        assert result is None
        mock_client.put_object.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_s3_makedirs_returns_none(self) -> None:
        fake_mod = _make_fake_aiobotocore()
        fake_parent = ModuleType("aiobotocore")
        with patch.dict(sys.modules, {"aiobotocore": fake_parent, "aiobotocore.session": fake_mod}):
            fs = AsyncS3FileSystem(bucket="bkt")
        result = await fs.makedirs("any/path", exist_ok=True)
        assert result is None
