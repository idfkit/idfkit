# Cloud & Remote Storage

idfkit's simulation module supports pluggable storage backends through the
`FileSystem` protocol, enabling cloud-native workflows with S3 and other
storage systems.

## The FileSystem Protocol

The `FileSystem` protocol defines a minimal interface for file operations:

```python
--8<-- "docs/snippets/concepts/cloud-storage/the_filesystem_protocol.py:example"
```

## Built-in Implementations

### LocalFileSystem

The default backend, wrapping `pathlib.Path` operations:

```python
--8<-- "docs/snippets/concepts/cloud-storage/localfilesystem.py:example"
```

### S3FileSystem

Amazon S3 backend for cloud workflows:

```python
--8<-- "docs/snippets/concepts/cloud-storage/s3filesystem.py:example"
```

Requires the `boto3` package: `pip install idfkit[s3]`

## Cloud Workflow Pattern

For cloud-based parametric simulations (AWS Batch, Kubernetes, etc.), the
typical workflow is:

### 1. Local Preparation

Create simulation jobs with S3 output paths:

```python
--8<-- "docs/snippets/concepts/cloud-storage/1_local_preparation.py:example"
```

### 2. Cloud Execution

Workers run simulations locally, results upload to S3:

```python
--8<-- "docs/snippets/concepts/cloud-storage/2_cloud_execution.py:example"
```

### 3. Result Collection

Retrieve results from S3 from any machine:

```python
--8<-- "docs/snippets/concepts/cloud-storage/3_result_collection.py:example"
```

## S3 Configuration

### Authentication

S3FileSystem uses boto3's credential chain:

1. Explicit credentials in constructor
2. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
3. IAM role (on EC2/ECS/Lambda)
4. Shared credentials file (`~/.aws/credentials`)

```python
--8<-- "docs/snippets/concepts/cloud-storage/authentication.py:example"
```

### S3-Compatible Services

Works with MinIO, LocalStack, and other S3-compatible services:

```python
--8<-- "docs/snippets/concepts/cloud-storage/s3_compatible_services.py:example"
```

### Key Prefixes

Use prefixes to namespace simulations:

```python
--8<-- "docs/snippets/concepts/cloud-storage/key_prefixes.py:example"
```

## Implementing Custom Backends

Implement the `FileSystem` protocol for other storage systems:

```python
--8<-- "docs/snippets/concepts/cloud-storage/implementing_custom_backends.py:example"
```

## Async File System

For use with `async_simulate()` and the async batch functions, an
`AsyncFileSystem` protocol is available.  This avoids blocking the event
loop during file uploads and result reads — important for
network-backed storage like S3.

### Built-in: AsyncLocalFileSystem

Wraps `LocalFileSystem` via `asyncio.to_thread()`:

```python
from idfkit.simulation import AsyncLocalFileSystem, async_simulate

fs = AsyncLocalFileSystem()
result = await async_simulate(
    model, "weather.epw",
    output_dir="run-001",
    fs=fs,
)

# Non-blocking result access
errors = await result.async_errors()
sql = await result.async_sql()
```

### Custom Async Backend

Implement the `AsyncFileSystem` protocol for full control:

```python
from idfkit.simulation import AsyncFileSystem


class AsyncS3FileSystem:
    """Example async S3 backend using aioboto3."""

    async def read_bytes(self, path, **kw):
        ...

    async def write_bytes(self, path, data, **kw):
        ...

    # ... implement all AsyncFileSystem methods
```

### Backward Compatibility

A sync `FileSystem` passed to `async_simulate()` is automatically wrapped
in `asyncio.to_thread()` for the upload step, so existing code continues
to work without changes.  However, using `AsyncFileSystem` avoids the
thread-pool overhead and provides true non-blocking I/O.

## EnergyPlus Execution

Important: **EnergyPlus always runs locally**. The FileSystem abstraction
covers:

- **Pre-simulation**: Preparing run directory
- **Post-simulation**: Uploading results
- **Result reading**: Downloading files on demand

The actual simulation happens in a local temporary directory, then results
are copied to the configured FileSystem.

## Performance Considerations

### Lazy Loading

Result files are read on-demand, so only accessed data is downloaded:

```python
--8<-- "docs/snippets/concepts/cloud-storage/lazy_loading.py:example"
```

### Local Caching

For repeated access, consider downloading to local disk:

```python
--8<-- "docs/snippets/concepts/cloud-storage/local_caching.py:example"
```

## See Also

- [Simulation Architecture](simulation-architecture.md) — Overall design
- [Caching Strategy](caching.md) — Local caching
- [Cloud Simulations Example](../examples/cloud-simulations.md) — Complete example
