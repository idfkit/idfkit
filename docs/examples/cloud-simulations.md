# Cloud Simulations (S3)

This example demonstrates running simulations with results stored in Amazon S3,
suitable for distributed cloud workflows.

## Prerequisites

Install S3 support:

```bash
pip install idfkit[s3]
```

Configure AWS credentials:

```bash
# Option 1: Environment variables
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1

# Option 2: AWS credentials file (~/.aws/credentials)
# Option 3: IAM role (on EC2, ECS, Lambda)
```

## Basic S3 Usage

```python
from idfkit import load_idf
from idfkit.simulation import simulate, S3FileSystem

# Create S3-backed filesystem
fs = S3FileSystem(
    bucket="my-simulations",
    prefix="project-x/",
)

# Run simulation with S3 storage
model = load_idf("building.idf")
result = simulate(
    model,
    "weather.epw",
    output_dir="run-001",  # Required with fs
    fs=fs,
)

# Results are now in s3://my-simulations/project-x/run-001/
print(f"Results stored at: {result.run_dir}")
```

## Cloud Workflow Pattern

For large-scale simulations on AWS Batch, Kubernetes, or similar:

### Step 1: Create Jobs Locally

```python
from idfkit.simulation import SimulationJob, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

# Create job specifications
jobs = []
for i, variant in enumerate(model_variants):
    jobs.append(SimulationJob(
        model=variant,
        weather="weather.epw",
        label=f"case-{i:04d}",
        output_dir=f"case-{i:04d}",
    ))

# Save job specs (e.g., as JSON or pickle)
```

### Step 2: Run on Cloud Workers

Each worker runs a subset of jobs:

```python
# worker.py (runs on AWS Batch, Kubernetes, etc.)
from idfkit.simulation import simulate, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

# Run single job
result = simulate(
    model,
    weather_path,  # Must be local
    output_dir=f"case-{job_id}",
    fs=fs,
)

# Results uploaded to S3 automatically
```

### Step 3: Collect Results

From any machine with S3 access:

```python
from idfkit.simulation import SimulationResult, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

# Reconstruct results
results = []
for i in range(num_cases):
    result = SimulationResult.from_directory(f"case-{i:04d}", fs=fs)
    results.append(result)

# Analyze
for i, result in enumerate(results):
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        "ZONE 1",
    )
    print(f"Case {i}: max temp = {max(ts.values):.1f}°C")
```

## Batch Processing with S3

```python
from idfkit.simulation import simulate_batch, SimulationJob, S3FileSystem

fs = S3FileSystem(bucket="my-bucket", prefix="batch-42/")

jobs = [
    SimulationJob(
        model=variant,
        weather="weather.epw",
        label=f"case-{i}",
        output_dir=f"case-{i}",
    )
    for i, variant in enumerate(variants)
]

batch = simulate_batch(jobs, max_workers=4, fs=fs)

# All results stored in S3
for i, result in enumerate(batch):
    print(f"Case {i}: s3://my-bucket/batch-42/case-{i}/")
```

## S3-Compatible Services

Works with MinIO, LocalStack, and other S3-compatible APIs:

### MinIO

```python
fs = S3FileSystem(
    bucket="local-bucket",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)
```

### LocalStack

```python
fs = S3FileSystem(
    bucket="test-bucket",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
)
```

### DigitalOcean Spaces

```python
fs = S3FileSystem(
    bucket="my-space",
    endpoint_url="https://nyc3.digitaloceanspaces.com",
    region_name="nyc3",
)
```

## Weather File Handling

Important: Weather files must be local. Download before simulating:

```python
from idfkit.weather import StationIndex, WeatherDownloader

# Download weather file locally
index = StationIndex.load()
station = index.search("chicago")[0].station
downloader = WeatherDownloader()
files = downloader.download(station)

# Then use local weather with S3 output
fs = S3FileSystem(bucket="results", prefix="study/")
result = simulate(
    model,
    files.epw,  # Local path
    output_dir="run-001",
    fs=fs,
)
```

## Performance Considerations

### Minimize S3 Round-Trips

```python
# Query results once, process locally
result = SimulationResult.from_directory("run-001", fs=fs)

# This downloads the SQL file
sql = result.sql

# Multiple queries are local (file is cached)
ts1 = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
ts2 = sql.get_timeseries("Zone Air Relative Humidity", "ZONE 1")
```

### Batch Downloads

For heavy analysis, download everything locally first:

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    # Download all files for a run
    for obj in fs.glob("run-001", "*"):
        data = fs.read_bytes(obj)
        local_path = Path(tmp) / Path(obj).name
        local_path.write_bytes(data)

    # Now use local result
    result = SimulationResult.from_directory(tmp)
    # Multiple queries without network calls
```

## Cost Optimization

- Store only necessary output files (filter before upload)
- Use S3 lifecycle policies to move old results to Glacier
- Consider S3 Intelligent Tiering for varying access patterns
- Use regional buckets close to compute resources

## Security

- Use IAM roles instead of access keys when possible
- Apply bucket policies to restrict access
- Enable S3 versioning for important results
- Consider server-side encryption

## See Also

- [Cloud Storage Concepts](../concepts/cloud-storage.md) — Architecture details
- [Batch Processing](../simulation/batch.md) — Parallel execution
- [Caching](../simulation/caching.md) — Local result caching
