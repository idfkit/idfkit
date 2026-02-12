"""File system abstraction for simulation I/O.

Provides a :class:`FileSystem` protocol so that simulation results can be
stored on and read from non-local backends (e.g. S3 for cloud workflows).
EnergyPlus itself always runs locally; the abstraction covers pre/post I/O
and result reading.

An :class:`AsyncFileSystem` protocol is also available for use with the
async simulation API (:func:`~idfkit.simulation.async_runner.async_simulate`).
Using ``AsyncFileSystem`` avoids blocking the event loop during file uploads
and result reads — important for S3 and other network-backed storage.

Cloud Workflow Example
----------------------

For cloud-based parametric simulations (AWS Batch, Kubernetes, etc.), the
typical workflow is:

1. **Local preparation**: Create simulation jobs with S3 output paths
2. **Cloud execution**: Workers run simulations locally, upload results to S3
3. **Result collection**: Collect results from S3 from any machine

Example::

    from idfkit import load_idf
    from idfkit.simulation import simulate, SimulationResult, S3FileSystem

    # Create an S3-backed filesystem
    fs = S3FileSystem(bucket="my-simulations", prefix="batch-42/")

    # Run simulation locally, results uploaded to S3
    model = load_idf("building.idf")
    result = simulate(model, "weather.epw", output_dir="run-001", fs=fs)

    # The result.run_dir now points to the S3 location
    print(result.run_dir)  # "run-001"

    # Query results (transparently reads from S3)
    if result.sql is not None:
        ts = result.sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
        print(f"Max temp: {max(ts.values):.1f} C")

    # Later, reconstruct results from S3 (from any machine)
    result = SimulationResult.from_directory("run-001", fs=fs)

The :class:`FileSystem` protocol can also be implemented for other backends
(Azure Blob Storage, GCS, etc.) by implementing the required methods.
"""

from __future__ import annotations

import asyncio
import fnmatch
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from types_boto3_s3 import S3Client


@runtime_checkable
class FileSystem(Protocol):
    """Protocol for file system operations used by the simulation module.

    All methods accept ``str | Path`` for path arguments.
    """

    def read_bytes(self, path: str | Path) -> bytes:
        """Read a file as raw bytes.

        Args:
            path: Path to the file.

        Returns:
            The file contents as bytes.
        """
        ...

    def write_bytes(self, path: str | Path, data: bytes) -> None:
        """Write raw bytes to a file.

        Args:
            path: Path to the file.
            data: Bytes to write.
        """
        ...

    def read_text(self, path: str | Path, encoding: str = "utf-8") -> str:
        """Read a file as text.

        Args:
            path: Path to the file.
            encoding: Text encoding (default ``"utf-8"``).

        Returns:
            The file contents as a string.
        """
        ...

    def write_text(self, path: str | Path, text: str, encoding: str = "utf-8") -> None:
        """Write text to a file.

        Args:
            path: Path to the file.
            text: Text to write.
            encoding: Text encoding (default ``"utf-8"``).
        """
        ...

    def exists(self, path: str | Path) -> bool:
        """Check whether a file exists.

        Args:
            path: Path to check.

        Returns:
            True if the file exists.
        """
        ...

    def makedirs(self, path: str | Path, *, exist_ok: bool = False) -> None:
        """Create directories recursively.

        Args:
            path: Directory path to create.
            exist_ok: If True, do not raise if the directory already exists.
        """
        ...

    def copy(self, src: str | Path, dst: str | Path) -> None:
        """Copy a file from *src* to *dst*.

        Args:
            src: Source file path.
            dst: Destination file path.
        """
        ...

    def glob(self, path: str | Path, pattern: str) -> list[str]:
        """List files matching a glob pattern under *path*.

        Args:
            path: Base directory.
            pattern: Glob pattern (e.g. ``"*.sql"``).

        Returns:
            List of matching file paths as strings.
        """
        ...

    def remove(self, path: str | Path) -> None:
        """Remove a file.

        Args:
            path: Path to the file to remove.
        """
        ...


class LocalFileSystem:
    """File system implementation backed by :mod:`pathlib` and :mod:`shutil`."""

    def read_bytes(self, path: str | Path) -> bytes:
        """Read a file as raw bytes."""
        return Path(path).read_bytes()

    def write_bytes(self, path: str | Path, data: bytes) -> None:
        """Write raw bytes to a file."""
        Path(path).write_bytes(data)

    def read_text(self, path: str | Path, encoding: str = "utf-8") -> str:
        """Read a file as text."""
        return Path(path).read_text(encoding=encoding)

    def write_text(self, path: str | Path, text: str, encoding: str = "utf-8") -> None:
        """Write text to a file."""
        Path(path).write_text(text, encoding=encoding)

    def exists(self, path: str | Path) -> bool:
        """Check whether a file exists."""
        return Path(path).exists()

    def makedirs(self, path: str | Path, *, exist_ok: bool = False) -> None:
        """Create directories recursively."""
        Path(path).mkdir(parents=True, exist_ok=exist_ok)

    def copy(self, src: str | Path, dst: str | Path) -> None:
        """Copy a file from *src* to *dst*."""
        shutil.copy2(str(src), str(dst))

    def glob(self, path: str | Path, pattern: str) -> list[str]:
        """List files matching a glob pattern under *path*."""
        return [str(p) for p in Path(path).glob(pattern)]

    def remove(self, path: str | Path) -> None:
        """Remove a file."""
        Path(path).unlink()


@runtime_checkable
class AsyncFileSystem(Protocol):
    """Protocol for async file system operations used by the async simulation module.

    This is the async counterpart to :class:`FileSystem`.  Use this with
    :func:`~idfkit.simulation.async_runner.async_simulate` and the async batch
    functions to avoid blocking the event loop during file I/O — especially
    important for network-backed storage like S3.

    All methods accept ``str | Path`` for path arguments.
    """

    async def read_bytes(self, path: str | Path) -> bytes:
        """Read a file as raw bytes.

        Args:
            path: Path to the file.

        Returns:
            The file contents as bytes.
        """
        ...

    async def write_bytes(self, path: str | Path, data: bytes) -> None:
        """Write raw bytes to a file.

        Args:
            path: Path to the file.
            data: Bytes to write.
        """
        ...

    async def read_text(self, path: str | Path, encoding: str = "utf-8") -> str:
        """Read a file as text.

        Args:
            path: Path to the file.
            encoding: Text encoding (default ``"utf-8"``).

        Returns:
            The file contents as a string.
        """
        ...

    async def write_text(self, path: str | Path, text: str, encoding: str = "utf-8") -> None:
        """Write text to a file.

        Args:
            path: Path to the file.
            text: Text to write.
            encoding: Text encoding (default ``"utf-8"``).
        """
        ...

    async def exists(self, path: str | Path) -> bool:
        """Check whether a file exists.

        Args:
            path: Path to check.

        Returns:
            True if the file exists.
        """
        ...

    async def makedirs(self, path: str | Path, *, exist_ok: bool = False) -> None:
        """Create directories recursively.

        Args:
            path: Directory path to create.
            exist_ok: If True, do not raise if the directory already exists.
        """
        ...

    async def copy(self, src: str | Path, dst: str | Path) -> None:
        """Copy a file from *src* to *dst*.

        Args:
            src: Source file path.
            dst: Destination file path.
        """
        ...

    async def glob(self, path: str | Path, pattern: str) -> list[str]:
        """List files matching a glob pattern under *path*.

        Args:
            path: Base directory.
            pattern: Glob pattern (e.g. ``"*.sql"``).

        Returns:
            List of matching file paths as strings.
        """
        ...

    async def remove(self, path: str | Path) -> None:
        """Remove a file.

        Args:
            path: Path to the file to remove.
        """
        ...


class AsyncLocalFileSystem:
    """Non-blocking local file system using :func:`asyncio.to_thread`.

    Wraps :class:`LocalFileSystem` so that each blocking I/O call runs in
    the default executor, keeping the event loop free.
    """

    def __init__(self) -> None:
        self._sync = LocalFileSystem()

    async def read_bytes(self, path: str | Path) -> bytes:
        """Read a file as raw bytes without blocking the event loop."""
        return await asyncio.to_thread(self._sync.read_bytes, path)

    async def write_bytes(self, path: str | Path, data: bytes) -> None:
        """Write raw bytes to a file without blocking the event loop."""
        await asyncio.to_thread(self._sync.write_bytes, path, data)

    async def read_text(self, path: str | Path, encoding: str = "utf-8") -> str:
        """Read a file as text without blocking the event loop."""
        return await asyncio.to_thread(self._sync.read_text, path, encoding)

    async def write_text(self, path: str | Path, text: str, encoding: str = "utf-8") -> None:
        """Write text to a file without blocking the event loop."""
        await asyncio.to_thread(self._sync.write_text, path, text, encoding)

    async def exists(self, path: str | Path) -> bool:
        """Check whether a file exists without blocking the event loop."""
        return await asyncio.to_thread(self._sync.exists, path)

    async def makedirs(self, path: str | Path, *, exist_ok: bool = False) -> None:
        """Create directories recursively without blocking the event loop."""
        await asyncio.to_thread(self._sync.makedirs, path, exist_ok=exist_ok)

    async def copy(self, src: str | Path, dst: str | Path) -> None:
        """Copy a file without blocking the event loop."""
        await asyncio.to_thread(self._sync.copy, src, dst)

    async def glob(self, path: str | Path, pattern: str) -> list[str]:
        """List files matching a glob pattern without blocking the event loop."""
        return await asyncio.to_thread(self._sync.glob, path, pattern)

    async def remove(self, path: str | Path) -> None:
        """Remove a file without blocking the event loop."""
        await asyncio.to_thread(self._sync.remove, path)


class S3FileSystem:
    """File system implementation backed by Amazon S3.

    Requires the ``boto3`` package (install via ``pip install idfkit[s3]``).

    This backend enables cloud-native simulation workflows where results are
    stored directly in S3 for later retrieval. EnergyPlus runs locally in a
    temporary directory, then results are uploaded to S3 after completion.

    Args:
        bucket: S3 bucket name.
        prefix: Optional key prefix prepended to all paths. Use this to
            namespace simulations (e.g., ``"project-x/batch-42/"``).
        **boto_kwargs: Additional keyword arguments passed to
            ``boto3.client("s3", ...)``. Common options include:

            - ``region_name``: AWS region (e.g., ``"us-east-1"``)
            - ``endpoint_url``: Custom endpoint for S3-compatible services
              (MinIO, LocalStack, etc.)
            - ``aws_access_key_id``, ``aws_secret_access_key``: Explicit
              credentials (normally use IAM roles or environment variables)

    Example::

        # Basic usage
        fs = S3FileSystem(bucket="my-bucket", prefix="simulations/")

        # With MinIO (S3-compatible)
        fs = S3FileSystem(
            bucket="local-bucket",
            endpoint_url="http://localhost:9000",
            aws_access_key_id="minioadmin",
            aws_secret_access_key="minioadmin",
        )

        # Use with simulate()
        result = simulate(model, weather, output_dir="run-001", fs=fs)
    """

    def __init__(self, bucket: str, prefix: str = "", **boto_kwargs: Any) -> None:
        try:
            import boto3  # type: ignore[import-not-found]
        except ImportError:
            msg = "boto3 is required for S3FileSystem. Install it with: pip install idfkit[s3]"
            raise ImportError(msg) from None
        _boto3: Any = boto3
        self._bucket = bucket
        self._prefix = prefix.strip("/")
        self._client: S3Client = _boto3.client("s3", **boto_kwargs)

    def _key(self, path: str | Path) -> str:
        """Build an S3 key by prepending the configured prefix.

        Args:
            path: Logical file path.

        Returns:
            The full S3 object key.
        """
        raw = str(path).lstrip("/")
        if self._prefix:
            return f"{self._prefix}/{raw}"
        return raw

    def read_bytes(self, path: str | Path) -> bytes:
        """Read a file as raw bytes from S3."""
        resp = self._client.get_object(Bucket=self._bucket, Key=self._key(path))
        return resp["Body"].read()  # type: ignore[no-any-return]

    def write_bytes(self, path: str | Path, data: bytes) -> None:
        """Write raw bytes to S3."""
        self._client.put_object(Bucket=self._bucket, Key=self._key(path), Body=data)

    def read_text(self, path: str | Path, encoding: str = "utf-8") -> str:
        """Read a file as text from S3."""
        return self.read_bytes(path).decode(encoding)

    def write_text(self, path: str | Path, text: str, encoding: str = "utf-8") -> None:
        """Write text to S3."""
        self.write_bytes(path, text.encode(encoding))

    def exists(self, path: str | Path) -> bool:
        """Check whether an object exists in S3."""
        try:
            self._client.head_object(Bucket=self._bucket, Key=self._key(path))
        except Exception:
            return False
        return True

    def makedirs(self, path: str | Path, *, exist_ok: bool = False) -> None:
        """No-op — S3 has no directory concept."""

    def copy(self, src: str | Path, dst: str | Path) -> None:
        """Copy an object within the same bucket."""
        self._client.copy_object(
            Bucket=self._bucket,
            CopySource={"Bucket": self._bucket, "Key": self._key(src)},
            Key=self._key(dst),
        )

    def glob(self, path: str | Path, pattern: str) -> list[str]:
        """List objects matching a glob pattern under *path*.

        Returns logical paths (without the configured S3 prefix) so that
        they can be passed back to other ``S3FileSystem`` methods which
        prepend the prefix automatically via ``_key()``.
        """
        prefix = self._key(path).rstrip("/") + "/"
        paginator = self._client.get_paginator("list_objects_v2")
        matches: list[str] = []
        # Compute how much of the key is the S3 prefix, so we can strip it.
        logical_base = str(path).strip("/")
        for page in paginator.paginate(Bucket=self._bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj.get("Key", "")
                if not key:
                    continue
                # Match only the filename portion against the pattern
                name = key[len(prefix) :]
                if fnmatch.fnmatch(name, pattern):
                    # Return logical path (base/name) that _key() can prefix
                    matches.append(f"{logical_base}/{name}" if logical_base else name)
        return matches

    def remove(self, path: str | Path) -> None:
        """Delete an object from S3."""
        self._client.delete_object(Bucket=self._bucket, Key=self._key(path))
