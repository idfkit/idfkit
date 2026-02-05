# Cloud & Remote Storage

idfkit's simulation module supports pluggable storage backends through the
`FileSystem` protocol, enabling cloud-native workflows with S3 and other
storage systems.

## The FileSystem Protocol

The `FileSystem` protocol defines a minimal interface for file operations:

```python
class FileSystem(Protocol):
    def read_bytes(self, path: str | Path) -> bytes: ...
    def write_bytes(self, path: str | Path, data: bytes) -> None: ...
    def read_text(self, path: str | Path, encoding: str = "utf-8") -> str: ...
    def write_text(self, path: str | Path, text: str, encoding: str = "utf-8") -> None: ...
    def exists(self, path: str | Path) -> bool: ...
    def makedirs(self, path: str | Path, *, exist_ok: bool = False) -> None: ...
    def copy(self, src: str | Path, dst: str | Path) -> None: ...
    def glob(self, path: str | Path, pattern: str) -> list[str]: ...
    def remove(self, path: str | Path) -> None: ...
```

## Built-in Implementations

### LocalFileSystem

The default backend, wrapping `pathlib.Path` operations:

```python
from idfkit.simulation import LocalFileSystem

fs = LocalFileSystem()  # This is the default
result = simulate(model, weather)  # Implicitly uses LocalFileSystem
```

### S3FileSystem

Amazon S3 backend for cloud workflows:

```python
from idfkit.simulation import S3FileSystem

fs = S3FileSystem(
    bucket="my-simulations",
    prefix="batch-42/",
)

result = simulate(model, weather, output_dir="run-001", fs=fs)
```

Requires the `boto3` package: `pip install idfkit[s3]`

## Cloud Workflow Pattern

For cloud-based parametric simulations (AWS Batch, Kubernetes, etc.), the
typical workflow is:

### 1. Local Preparation

Create simulation jobs with S3 output paths:

```python
from idfkit.simulation import SimulationJob, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

jobs = [
    SimulationJob(
        model=variant,
        weather="weather.epw",
        label=f"case-{i}",
        output_dir=f"case-{i}",
        fs=fs,
    )
    for i, variant in enumerate(variants)
]
```

### 2. Cloud Execution

Workers run simulations locally, results upload to S3:

```python
# In your AWS Batch / Kubernetes job:
from idfkit.simulation import simulate, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")
result = simulate(model, weather, output_dir="case-42", fs=fs)

# Result files are now in s3://simulations/study-001/case-42/
```

### 3. Result Collection

Retrieve results from S3 from any machine:

```python
from idfkit.simulation import SimulationResult, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

# Reconstruct result from S3
result = SimulationResult.from_directory("case-42", fs=fs)

# Query data (transparently reads from S3)
ts = result.sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
```

## S3 Configuration

### Authentication

S3FileSystem uses boto3's credential chain:

1. Explicit credentials in constructor
2. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
3. IAM role (on EC2/ECS/Lambda)
4. Shared credentials file (`~/.aws/credentials`)

```python
# IAM role (recommended for cloud)
fs = S3FileSystem(bucket="my-bucket")

# Explicit credentials (for testing)
fs = S3FileSystem(
    bucket="my-bucket",
    aws_access_key_id="AKIA...",
    aws_secret_access_key="...",
)
```

### S3-Compatible Services

Works with MinIO, LocalStack, and other S3-compatible services:

```python
# MinIO
fs = S3FileSystem(
    bucket="local-bucket",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

# LocalStack
fs = S3FileSystem(
    bucket="test-bucket",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
)
```

### Key Prefixes

Use prefixes to namespace simulations:

```python
# All files stored under "project-x/batch-42/"
fs = S3FileSystem(
    bucket="simulations",
    prefix="project-x/batch-42/",
)

# output_dir="run-001" → s3://simulations/project-x/batch-42/run-001/
```

## Implementing Custom Backends

Implement the `FileSystem` protocol for other storage systems:

```python
from idfkit.simulation import FileSystem

class AzureBlobFileSystem:
    """Azure Blob Storage backend."""

    def __init__(self, container: str, connection_string: str):
        from azure.storage.blob import ContainerClient
        self._client = ContainerClient.from_connection_string(
            connection_string, container
        )

    def read_bytes(self, path: str | Path) -> bytes:
        blob = self._client.get_blob_client(str(path))
        return blob.download_blob().readall()

    def write_bytes(self, path: str | Path, data: bytes) -> None:
        blob = self._client.get_blob_client(str(path))
        blob.upload_blob(data, overwrite=True)

    # ... implement remaining methods
```

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
result = SimulationResult.from_directory("run-001", fs=s3_fs)

# Nothing downloaded yet
# ...

# Downloads only the SQLite file
ts = result.sql.get_timeseries(...)
```

### Local Caching

For repeated access, consider downloading to local disk:

```python
import tempfile
import shutil

# Download entire result directory
with tempfile.TemporaryDirectory() as tmp:
    # Copy from S3 to local
    for path in s3_fs.glob("run-001", "*"):
        data = s3_fs.read_bytes(path)
        local_path = Path(tmp) / Path(path).name
        local_path.write_bytes(data)

    # Use local result
    result = SimulationResult.from_directory(tmp)
    # Multiple queries without network calls
```

## See Also

- [Simulation Architecture](simulation-architecture.md) — Overall design
- [Caching Strategy](caching.md) — Local caching
- [Cloud Simulations Example](../examples/cloud-simulations.md) — Complete example
