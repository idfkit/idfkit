# Distributed Simulations with Scythe

[Scythe](https://github.com/szvsw/scythe) is a lightweight framework for running
embarrassingly parallel experiments at scale via the
[Hatchet](https://hatchet.run) distributed task queue. It handles artifact
management, S3 storage, and result collection so you can focus on the
simulation logic.

By combining **idfkit** for EnergyPlus model manipulation and simulation with
**Scythe** for distributed orchestration, you can run large parametric studies
across hundreds or thousands of building variants without writing your own
queuing or storage infrastructure.

!!! note
    Scythe is an independent project in early development. See the
    [Scythe documentation](https://szvsw.github.io/scythe/) for the latest
    API details and setup instructions.

## Prerequisites

Install both packages:

```bash
pip install idfkit scythe-engine
```

Workers need EnergyPlus installed. The
[NREL Docker images](https://hub.docker.com/r/nrel/energyplus) are a convenient
base for containerized deployments.

You also need a running [Hatchet](https://hatchet.run) instance (self-hosted or
cloud) and an S3-compatible bucket for artifacts. See
[hatchet-sst](https://github.com/szvsw/hatchet-sst) for a self-hosting guide.

## How It Works

Scythe follows a **scatter-gather** pattern:

1. **Define** input and output schemas as Pydantic models
2. **Register** an experiment function that maps one input to one output
3. **Allocate** a batch of input specs; Scythe uploads artifacts and enqueues tasks
4. **Workers** pull tasks from the Hatchet queue and execute them
5. **Gather** results from S3 as organized Parquet files

idfkit fits into step 2: the registered experiment function uses idfkit to
load an IDF, apply parameter changes, run the EnergyPlus simulation, and
extract results.

## Step 1: Define Input/Output Schemas

Schemas inherit from Scythe's `ExperimentInputSpec` and `ExperimentOutputSpec`.
Use `FileReference` fields for files that Scythe should manage (upload to / download
from S3 automatically).

```python
--8<-- "docs/snippets/examples/scythe/input_output_specs.py:example"
```

Key points:

- **Scalar fields** (`r_value`, `lpd`, etc.) are collected into a Parquet table
  for analysis.
- **`FileReference` fields** accept local paths, HTTP URLs, or S3 URIs. Scythe
  uploads local files to S3 at allocation time and resolves them back to local
  paths on the worker.
- Pydantic `Field` constraints (`ge`, `le`) provide automatic validation.

## Step 2: Register the Experiment Function

The experiment function receives a single `BuildingSimInput` and a temporary
working directory, and returns a `BuildingSimOutput`. This is where idfkit
does the heavy lifting.

```python
--8<-- "docs/snippets/examples/scythe/experiment_function.py:example"
```

Inside the function you have full access to the idfkit API:

- **`load_idf()`** parses the model file that Scythe downloaded to a local path
- **Object manipulation** applies parametric changes (R-values, lighting, setpoints)
- **`DesignDayManager`** loads a DDY file by path and injects design days into the model
- **`simulate()`** runs EnergyPlus and returns structured results
- **`result.sql.get_tabular_data()`** queries the SQLite output for tabular end-use data
- **`result.csv`** provides access to time-series column data

Any file you write to `tempdir` and return as a `FileReference` gets uploaded
to S3 automatically.

## Step 3: Prepare Weather Data

Use idfkit's weather module to find stations and download EPW/DDY files before
allocating experiments:

```python
--8<-- "docs/snippets/examples/scythe/weather_prep.py:example"
```

You can pass local file paths, HTTP URLs, or S3 URIs as `FileReference` values
in your input specs. Scythe handles the upload and distribution to workers.

## Step 4: Allocate the Experiment

Create a parameter grid, build input specs, and let Scythe enqueue everything:

```python
--8<-- "docs/snippets/examples/scythe/allocate.py:example"
```

This creates `4 x 3 x 3 x 2 = 72` simulation tasks. Scythe uploads the IDF,
EPW, and DDY files to S3 (deduplicating shared files), serializes the specs,
and pushes work items to the Hatchet queue.

The `RecursionMap` controls how Scythe fans out work across workers. A
`factor=2, max_depth=3` configuration splits the batch into progressively
smaller chunks for efficient scheduling.

## Step 5: Run Workers

Each worker imports the registered experiments and starts the Scythe worker
loop:

```python
--8<-- "docs/snippets/examples/scythe/worker.py:example"
```

Workers pull tasks from the Hatchet queue, download input artifacts from S3,
call the experiment function, and upload outputs back to S3.

### Docker Setup

For containerized workers with EnergyPlus pre-installed:

```dockerfile
FROM nrel/energyplus:24.2.0

RUN pip install idfkit scythe-engine

COPY experiments/ /app/experiments/
COPY main.py /app/main.py

WORKDIR /app
CMD ["python", "main.py"]
```

Scale horizontally by running multiple container instances against the same
Hatchet queue.

## Step 6: Gather Results

Once all tasks complete, Scythe organizes outputs in S3:

```
s3://my-bucket/experiments/<name>/<version>/
    manifest.yml              # Experiment metadata
    specs.pq                  # All input specs as Parquet
    scalars.pq                # All scalar outputs (heating, cooling, etc.)
    result_file_refs.pq       # S3 paths to output files (timeseries CSVs)
    experiment_io_spec.yml    # JSON Schema of input/output definitions
```

Load the scalar results directly with pandas:

```python
import pandas as pd

scalars = pd.read_parquet("s3://my-bucket/experiments/.../scalars.pq")
print(scalars.describe())
```

The `scalars.pq` file contains a MultiIndex linking each output row back to
its input parameters, making it straightforward to pivot, group, and plot
results.

## idfkit Features Useful in Scythe Experiments

| idfkit Feature | Use Case in Scythe |
|---|---|
| `load_idf()` / `load_epjson()` | Load base model from `FileReference` |
| Object field manipulation | Apply parametric changes per spec |
| `DesignDayManager` | Inject design days from DDY files |
| `simulate()` | Run EnergyPlus inside the experiment function |
| `result.sql.get_tabular_data()` | Query tabular end-use summaries |
| `result.csv` | Extract time-series for `FileReference` output |
| `rotate_building()` | Orientation studies |
| `model.copy()` | Create variants from a shared base |
| Weather station search | Prepare EPW/DDY files before allocation |

## Tips

- **Keep experiment functions focused.** Do model setup, simulation, and result
  extraction in the registered function. Avoid heavy post-processing; save raw
  outputs and analyze after gathering.
- **Use `FileReference` for large outputs.** Scalar fields go into the Parquet
  summary; file references point to full time-series or report files in S3.
- **Deduplicate shared inputs.** When all specs share the same IDF or EPW file,
  Scythe uploads it once. Use S3 URIs to avoid redundant uploads.
- **Pin EnergyPlus versions.** Use `idfkit.find_energyplus(version=...)` or set
  `ENERGYPLUS_DIR` in your Docker image to ensure reproducible results.
- **Test locally first.** Call your experiment function directly with a single
  spec and a temporary directory before allocating a full batch.

## See Also

- [Scythe documentation](https://szvsw.github.io/scythe/)
- [Scythe example repository](https://github.com/szvsw/scythe-example)
- [Batch Processing](../simulation/batch.md) -- idfkit's built-in thread-pool batch runner
- [Cloud Simulations (S3)](cloud-simulations.md) -- Using idfkit with S3 directly
- [Running Simulations](../simulation/running.md) -- Single simulation guide
