# How to store simulation results in S3

This guide shows how to run simulations with results stored in Amazon S3,
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
--8<-- "docs/snippets/examples/cloud-simulations/basic_s3_usage.py:example"
```

## Cloud Workflow Pattern

For large-scale simulations on AWS Batch, Kubernetes, or similar:

### Step 1: Create Jobs Locally

```python
--8<-- "docs/snippets/examples/cloud-simulations/step_1_create_jobs_locally.py:example"
```

### Step 2: Run on Cloud Workers

Each worker runs a subset of jobs:

```python
--8<-- "docs/snippets/examples/cloud-simulations/step_2_run_on_cloud_workers.py:example"
```

### Step 3: Collect Results

From any machine with S3 access:

```python
--8<-- "docs/snippets/examples/cloud-simulations/step_3_collect_results.py:example"
```

## Batch Processing with S3

```python
--8<-- "docs/snippets/examples/cloud-simulations/batch_processing_with_s3.py:example"
```

## S3-Compatible Services

Works with MinIO, LocalStack, and other S3-compatible APIs:

### MinIO

```python
--8<-- "docs/snippets/examples/cloud-simulations/minio.py:example"
```

### LocalStack

```python
--8<-- "docs/snippets/examples/cloud-simulations/localstack.py:example"
```

### DigitalOcean Spaces

```python
--8<-- "docs/snippets/examples/cloud-simulations/digitalocean_spaces.py:example"
```

## Weather File Handling

Important: Weather files must be local. Download before simulating:

```python
--8<-- "docs/snippets/examples/cloud-simulations/weather_file_handling.py:example"
```

## Performance Considerations

### Minimize S3 Round-Trips

```python
--8<-- "docs/snippets/examples/cloud-simulations/minimize_s3_round_trips.py:example"
```

### Batch Downloads

For heavy analysis, download everything locally first:

```python
--8<-- "docs/snippets/examples/cloud-simulations/batch_downloads.py:example"
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
