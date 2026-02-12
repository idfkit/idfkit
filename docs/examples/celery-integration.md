# Celery Integration

This tutorial shows how to run EnergyPlus simulations as distributed
[Celery](https://docs.celeryq.dev/) tasks.  The pattern works well when you
need to:

- Run hundreds or thousands of simulations across a cluster of machines.
- Integrate simulation jobs into a larger web application or data pipeline.
- Get automatic retries, rate limiting, and monitoring for free.

!!! tip "When to use Celery vs `simulate_batch()`"
    idfkit's built-in [`simulate_batch()`](../simulation/batch.md) is the
    simplest way to run simulations in parallel on a **single machine**.
    Reach for Celery when you need to distribute work across **multiple
    machines**, integrate with an existing task queue, or require features
    like retries, priority queues, and persistent result storage.

## Prerequisites

Install idfkit and Celery with a Redis broker:

```bash
pip install idfkit celery[redis]
```

You also need a running Redis instance.  The fastest way to get one locally:

```bash
docker run -d -p 6379:6379 redis:7-alpine
```

## Project Layout

```text
--8<-- "docs/snippets/examples/celery-integration/project_layout.py:example"
```

## Step 1: Configure Celery

```python
--8<-- "docs/snippets/examples/celery-integration/celeryconfig.py:example"
```

Key choices explained:

| Setting | Why |
|---------|-----|
| `task_acks_late = True` | The message stays in Redis until the task finishes. If a worker crashes mid-simulation, another worker picks up the job automatically. |
| `worker_concurrency = 1` | EnergyPlus is CPU-bound. Running one simulation per worker process avoids CPU contention. Scale by adding more worker processes or machines instead. |
| `task_serializer = "json"` | Task arguments must be JSON-serializable (strings, numbers, bools). This avoids pickle security issues and makes task payloads inspectable. |
| `task_time_limit` | Kills the worker process if a simulation exceeds the hard limit, preventing runaway jobs from blocking the queue. |

## Step 2: Define a Simulation Task

```python
--8<-- "docs/snippets/examples/celery-integration/tasks_basic.py:example"
```

!!! warning "Pass file paths, not objects"
    Celery serializes task arguments to JSON.  Pass **file paths** (strings)
    to the task and call `load_idf()` inside the worker.  Never try to pass
    an `IDFDocument` directly — it is not JSON-serializable.

## Step 3: Submit Jobs

### Single Simulation

```python
--8<-- "docs/snippets/examples/celery-integration/submit_single.py:example"
```

### Fan-Out Batch

Use Celery's `group` primitive to submit many simulations at once:

```python
--8<-- "docs/snippets/examples/celery-integration/submit_batch.py:example"
```

Each job runs on whichever worker is available.  With 4 workers, up to 4
simulations run in parallel.

## Parametric Studies

For parametric sweeps, pass scalar parameters to the task and build the
model variant on the worker:

### Task Definition

```python
--8<-- "docs/snippets/examples/celery-integration/tasks_parametric.py:example"
```

### Submitting a Parameter Grid

```python
--8<-- "docs/snippets/examples/celery-integration/submit_parametric.py:example"
```

This fans out 9 jobs (3 conductivities x 3 U-factors) across all available
workers.

## Error Handling and Retries

EnergyPlus can fail for transient reasons (file system issues, resource
exhaustion).  Celery's built-in retry mechanism handles this:

```python
--8<-- "docs/snippets/examples/celery-integration/tasks_with_retry.py:example"
```

The `autoretry_for` parameter catches both idfkit `SimulationError` and
OS-level errors.  The task retries up to 3 times with exponential backoff
(60s, then 120s, capped at 600s).

## Progress Reporting

idfkit's `on_progress` callback integrates naturally with Celery's custom
state updates:

### Task with Progress

```python
--8<-- "docs/snippets/examples/celery-integration/tasks_with_progress.py:example"
```

### Polling Progress from the Client

```python
--8<-- "docs/snippets/examples/celery-integration/poll_progress.py:example"
```

## Caching

Share a [`SimulationCache`](../simulation/caching.md) across workers to
skip duplicate simulations.  If workers run on the same machine (or share a
network file system), point the cache at a shared directory:

```python
--8<-- "docs/snippets/examples/celery-integration/tasks_with_cache.py:example"
```

When the same model + weather combination is submitted again, the worker
returns the cached result instantly instead of re-running EnergyPlus.

## Cloud Storage (S3)

Upload simulation results directly to S3 from workers:

```python
--8<-- "docs/snippets/examples/celery-integration/tasks_with_s3.py:example"
```

Workers need AWS credentials (environment variables, IAM role, or
`~/.aws/credentials`).  See [Cloud Simulations (S3)](cloud-simulations.md)
for details.

## Task Composition

Celery's `chain` primitive lets you compose multi-step workflows — for
example, running a simulation and then post-processing the results:

```python
--8<-- "docs/snippets/examples/celery-integration/chain_workflow.py:example"
```

## Deployment with Docker

### Dockerfile

```dockerfile
--8<-- "docs/snippets/examples/celery-integration/dockerfile.py:example"
```

### Docker Compose

```yaml
--8<-- "docs/snippets/examples/celery-integration/docker_compose.py:example"
```

Start everything with:

```bash
docker compose up -d --scale worker=4
```

This starts 4 worker containers (4 concurrent simulations), a Redis
broker, and the [Flower](https://flower.readthedocs.io/) monitoring
dashboard at `http://localhost:5555`.

## Monitoring

### Flower Dashboard

[Flower](https://flower.readthedocs.io/) provides a real-time web UI for
monitoring workers, tasks, and queues:

```bash
pip install flower
celery -A tasks flower --port=5555
```

Open `http://localhost:5555` to see active workers, task history, success
rates, and runtime distributions.

### CLI Inspection

```bash
# List active workers
celery -A tasks inspect active

# Purge all pending tasks
celery -A tasks purge

# View task result
celery -A tasks result <task-id>
```

## Best Practices

1. **One simulation per worker process.**
   Set `worker_concurrency = 1`.  EnergyPlus is CPU-bound, and running
   multiple simulations in one process causes contention.  Scale
   horizontally by adding workers.

2. **Use `acks_late` with `reject_on_worker_lost`.**
   This ensures that if a worker dies mid-simulation, the job is re-queued
   and retried by another worker.

3. **Pass paths, not objects.**
   All task arguments must be JSON-serializable.  Pass IDF file paths and
   scalar parameters — load models inside the worker.

4. **Set time limits.**
   Use `task_time_limit` (hard kill) and `task_soft_time_limit` (raises
   `SoftTimeLimitExceeded`) to prevent runaway simulations from blocking
   workers indefinitely.

5. **Use a shared cache for parametric studies.**
   Point `SimulationCache` at a network file system or shared volume so
   workers skip duplicate model + weather combinations.

6. **Pin the EnergyPlus version.**
   Ensure all workers use the same EnergyPlus version (set `ENERGYPLUS_DIR`
   or embed it in the Docker image) to avoid inconsistent results.

7. **Separate queues for fast and slow jobs.**
   Route design-day simulations to a "fast" queue and annual simulations to
   a "slow" queue using Celery's
   [task routing](https://docs.celeryq.dev/en/stable/userguide/routing.html).

8. **Monitor with Flower.**
   Run [Flower](https://flower.readthedocs.io/) to track worker health,
   task throughput, and failure rates in production.

## See Also

- [Batch Processing](../simulation/batch.md) — Single-machine parallel execution
- [Async Simulation](../simulation/async.md) — Non-blocking execution for async apps
- [Cloud Simulations (S3)](cloud-simulations.md) — S3 result storage
- [Caching](../simulation/caching.md) — Content-addressed simulation caching
