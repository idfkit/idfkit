# EnergyPlus Simulation Plan for IDFkit

## Executive Summary

IDFkit currently excels at parsing, manipulating, and writing EnergyPlus IDF/epJSON files with
O(1) lookups and minimal memory overhead. This plan proposes extending IDFkit with first-class
simulation execution, output variable discovery, result retrieval, and visualization -- while
avoiding the pitfalls that plague existing packages (eppy, honeybee-energy, opyplus, etc.).

In addition, finding the right weather file and injecting design day conditions into a model is
a persistent pain point across the EnergyPlus ecosystem. This plan includes a comprehensive
weather file and design day browser built on the climate.onebuilding.org TMYx dataset (17,300+
stations worldwide), with fuzzy search, lat/lon proximity search, and free address geocoding --
eliminating one of the most tedious manual steps in the simulation workflow.

The design prioritizes:

1. **No admin rights required** -- works with user-level EnergyPlus installations
2. **Cloud-native** -- isolated simulation directories, abstract file systems, stateless execution
3. **Parallel-safe** -- no shared mutable state, no singletons, no in-process EnergyPlus coupling
4. **Pluggable** -- file system backends, plotting backends, and result formats are all swappable
5. **Minimal dependencies** -- core simulation requires only the standard library; extras unlock
   pandas, plotting, and cloud storage
6. **Weather made easy** -- searchable station index, automatic EPW/DDY download, and one-line
   design day injection into IDF models

---

## 1. Lessons from Existing Packages

### 1.1 Common Failure Patterns

| Package | Problem | Root Cause |
|---------|---------|------------|
| eppy | Stale simulation results ([#271](https://github.com/santoshphilip/eppy/issues/271)) | Singleton IDD pattern; in-memory mutation without re-serialization |
| eppy | Windows `PermissionError` ([#155](https://github.com/santoshphilip/eppy/issues/155)) | Writing `in.idf` to EnergyPlus install directory (often `C:\Program Files`) |
| eppy | `multiprocessing.Pool` fails on Windows ([#300](https://github.com/santoshphilip/eppy/issues/300)) | `fork` vs `spawn` semantics; unpicklable objects |
| eppy | CSV generation failures ([#218](https://github.com/santoshphilip/eppy/issues/218)) | ReadVarsESO post-processor is fragile and lossy |
| honeybee-energy | Platform-specific shell scripts | Writes `.bat`/`.sh` files, uses `shell=True` |
| opyplus | `shell=True` subprocess | Security risk, platform-dependent quoting |
| pyenergyplus | Requires `sys.path` manipulation | Bundled inside EnergyPlus install directory, not pip-installable |
| pyenergyplus | GIL blocks parallel plugins | In-process execution shares Python GIL across threads |
| All packages | Hardcoded EnergyPlus paths | Each reinvents filesystem scanning with different heuristics |
| All packages | Limited output parsing | Most only parse HTML tables or delegate to ReadVarsESO |

### 1.2 What Works Well

| Package | Good Pattern | Worth Adopting? |
|---------|-------------|-----------------|
| archetypal | Simulation result caching (content hash) | Yes -- avoids redundant runs |
| energy_plus_wrapper | `joblib.Parallel` for multi-process | Yes -- more robust than `multiprocessing.Pool` |
| energy_plus_wrapper | Accepts IDF objects directly (no temp file dance) | Yes -- IDFkit already has writers |
| opyplus | Structured output accessors (`get_out_eso()`, `get_out_err()`) | Yes -- typed result objects |
| frads | Snake-case attribute access for EnergyPlus objects | Already implemented in IDFkit |
| honeybee-energy | Filesystem scanning with version sorting | Partially -- but make it configurable |

### 1.3 The pyenergyplus (Official API) Trade-off

The official EnergyPlus Python API (`pyenergyplus`) offers in-process execution via C library
bindings. While this avoids subprocess overhead, it introduces critical constraints:

- **Not pip-installable**: lives inside the EnergyPlus installation directory
- **GIL contention**: parallel simulations in the same process are throttled by Python's GIL
- **Tight coupling**: linking IDFkit to `pyenergyplus` would make it depend on a specific
  EnergyPlus installation at import time
- **State management complexity**: `state_manager.new_state()` / `reset_state()` patterns are
  error-prone

**Recommendation**: Use subprocess-based execution as the primary strategy. Offer an optional
`pyenergyplus` backend for advanced users who need runtime callbacks (EMS plugins), but never
require it.

---

## 2. Architecture Overview

```
idfkit (existing)           idfkit.sim (new)
┌─────────────────┐         ┌──────────────────────────────────────────┐
│ IDFDocument      │         │ EnergyPlusConfig    (discovery)          │
│ IDFObject        │────────>│ Simulator           (execution)          │
│ IDFCollection    │         │ SimulationResult     (outputs)           │
│ write_idf()      │         │ OutputVariableIndex  (RDD/MDD parsing)  │
│ write_epjson()   │         │ ResultsPlotter       (visualization)     │
└─────────────────┘         └──────────────────────────────────────────┘
         │                            │
         │                  ┌─────────┴──────────┐
         │                  │  idfkit.sim.fs      │
         │                  │  (file system       │
         │                  │   abstraction)      │
         │                  └─────────────────────┘
         │                   LocalFS / S3FS / ...
         │
         │                  idfkit.weather (new)
         │                  ┌──────────────────────────────────────────┐
         └─────────────────>│ WeatherStation       (station metadata)   │
                            │ StationIndex         (search & browse)    │
                            │ DesignDayManager     (DDY parsing/inject) │
                            │ WeatherDownloader    (EPW/DDY fetching)   │
                            └──────────────────────────────────────────┘
                              climate.onebuilding.org (17,300+ stations)
```

### 2.1 Module Layout

```
src/idfkit/
├── sim/
│   ├── __init__.py              # Public API: simulate(), find_energyplus()
│   ├── config.py                # EnergyPlus discovery and configuration
│   ├── runner.py                # Simulation execution engine
│   ├── result.py                # SimulationResult container
│   ├── outputs.py               # Output variable discovery (RDD/MDD)
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── eso.py               # ESO/MTR binary-text parser
│   │   ├── sql.py               # SQLite output parser
│   │   ├── err.py               # Error file parser
│   │   ├── html.py              # HTML table report parser
│   │   ├── csv.py               # CSV result parser
│   │   └── eio.py               # Invariant output parser
│   ├── fs/
│   │   ├── __init__.py          # FileSystem protocol
│   │   ├── local.py             # Local filesystem (default)
│   │   └── s3.py                # S3-compatible (optional, requires boto3)
│   └── plotting/
│       ├── __init__.py          # PlotBackend protocol
│       ├── matplotlib.py        # matplotlib backend (optional)
│       └── plotly.py            # plotly backend (optional)
├── weather/
│   ├── __init__.py              # Public API: search(), nearest(), download()
│   ├── station.py               # WeatherStation dataclass
│   ├── index.py                 # StationIndex: search, filter, spatial queries
│   ├── downloader.py            # EPW/DDY download from climate.onebuilding.org
│   ├── designday.py             # DDY parser and model injection
│   ├── geocode.py               # Free address-to-coordinates via Nominatim
│   ├── spatial.py               # Haversine distance and nearest-neighbor search
│   └── _data/
│       └── stations.csv.gz      # Bundled station index (~300KB compressed)
```

---

## 3. EnergyPlus Discovery and Configuration

### 3.1 The Problem

Every existing package hardcodes platform-specific paths and rescans the filesystem on each
invocation. Users with non-standard installations (portable, Conda, Docker, CI/CD) are left
writing boilerplate to configure paths.

### 3.2 Discovery Strategy (Priority Order)

```python
class EnergyPlusConfig:
    """Locate and configure an EnergyPlus installation."""

    @classmethod
    def find(
        cls,
        version: str | tuple[int, int, int] | None = None,
        path: str | Path | None = None,
    ) -> EnergyPlusConfig:
        """Find EnergyPlus using a layered discovery strategy."""
        ...
```

The discovery order:

1. **Explicit `path` argument** -- highest priority, no guessing
2. **`ENERGYPLUS_DIR` environment variable** -- standard override for CI/CD and containers
3. **`PATH` lookup** -- `shutil.which("energyplus")` finds it if it's on `PATH`
4. **Platform-specific well-known locations** (scanned in version order, newest first):
   - **Windows**: `%LOCALAPPDATA%\EnergyPlusV*` (user-level, no admin), then `C:\EnergyPlusV*`
   - **macOS**: `~/Applications/EnergyPlus-*`, then `/Applications/EnergyPlus-*`
   - **Linux**: `~/.local/EnergyPlus-*`, then `/usr/local/EnergyPlus-*`
5. **Version filtering** -- if `version` is specified, only matching installations are considered

### 3.3 Configuration Object

```python
@dataclass(frozen=True)
class EnergyPlusConfig:
    executable: Path          # .../energyplus(.exe)
    version: tuple[int, int, int]
    install_dir: Path         # parent directory
    idd_path: Path            # Energy+.idd
    weather_dir: Path         # WeatherData/
    preprocess_dir: Path      # PreProcess/
    schema_path: Path         # Energy+.schema.epJSON

    @property
    def expand_objects_exe(self) -> Path | None: ...

    @property
    def transition_exes(self) -> list[Path]: ...
```

### 3.4 Why This Matters for Windows

Windows users face a genuine barrier: the default EnergyPlus installer requires admin rights to
write to `C:\EnergyPlusV*`. Starting with EnergyPlus 8.8, a "per-user" install option places
files in `%LOCALAPPDATA%\EnergyPlusV*` without elevation. By checking user-level paths _first_,
IDFkit works out of the box for non-admin users.

---

## 4. Simulation Execution

### 4.1 Core API

```python
def simulate(
    model: IDFDocument,
    weather: str | Path,
    *,
    output_dir: str | Path | None = None,
    energyplus: EnergyPlusConfig | str | Path | None = None,
    expand_objects: bool = True,
    annual: bool = False,
    design_day: bool = False,
    output_prefix: str = "eplus",
    output_suffix: Literal["C", "L", "D"] = "C",
    readvars: bool = False,
    extra_args: list[str] | None = None,
    fs: FileSystem | None = None,
) -> SimulationResult:
    """Run an EnergyPlus simulation and return structured results."""
    ...
```

### 4.2 Execution Strategy

**Subprocess-based** (`subprocess.run`, not `check_call` or `Popen` with `shell=True`):

```python
cmd = [
    str(config.executable),
    "--weather", str(weather_path),
    "--output-directory", str(run_dir),
    "--output-prefix", output_prefix,
    "--output-suffix", output_suffix,
    "--idd", str(config.idd_path),
]
if expand_objects:
    cmd.append("--expandobjects")
if annual:
    cmd.append("--annual")
if design_day:
    cmd.append("--design-day-only")
if readvars:
    cmd.append("--readvars")
if extra_args:
    cmd.extend(extra_args)
cmd.append(str(idf_path))

completed = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    timeout=timeout,
    cwd=run_dir,
)
```

Key design decisions:

- **`subprocess.run`** (not `check_call`): captures stdout/stderr for diagnostics
- **No `shell=True`**: avoids injection risks and platform-dependent quoting
- **`cwd=run_dir`**: isolates the simulation to its own directory
- **No in-process execution**: avoids GIL contention and pyenergyplus dependency

### 4.3 Simulation Directory Isolation

Every simulation runs in its own isolated directory. This is critical for parallel execution and
cloud workflows:

```python
def _prepare_run_directory(
    model: IDFDocument,
    weather: Path,
    output_dir: Path | None,
    fs: FileSystem,
) -> Path:
    """Create an isolated run directory with all required inputs."""
    if output_dir is None:
        run_dir = Path(tempfile.mkdtemp(prefix="idfkit_"))
    else:
        run_dir = Path(output_dir)
        fs.makedirs(run_dir, exist_ok=True)

    # Write the IDF into the run directory (never into the EnergyPlus install dir)
    idf_path = run_dir / "in.idf"
    write_idf(model, idf_path)

    # Copy (or symlink) the weather file into the run directory
    weather_dest = run_dir / weather.name
    if not weather_dest.exists():
        fs.copy(weather, weather_dest)

    return run_dir
```

This avoids the `PermissionError` that plagues eppy on Windows (writing to `C:\Program Files`).

### 4.4 Automatic `Output:SQLite` Injection

To ensure robust result parsing, the simulator automatically adds an `Output:SQLite` object to
the model if one is not already present:

```python
def _ensure_sql_output(model: IDFDocument) -> None:
    """Inject Output:SQLite if not already present."""
    try:
        model["Output:SQLite"]
    except KeyError:
        model.add("Output:SQLite", Option_Type="SimpleAndTabular")
```

SQLite output is the most reliable and complete output format. Unlike ESO (which requires
ReadVarsESO to convert to CSV) or HTML (which requires fragile parsing), SQLite contains all
time-series data, tabular reports, and metadata in a single queryable file.

### 4.5 Parallel Simulation

#### Local Parallelism

```python
def simulate_batch(
    jobs: Iterable[SimulationJob],
    *,
    max_workers: int | None = None,
    energyplus: EnergyPlusConfig | str | Path | None = None,
    backend: Literal["process", "thread"] = "process",
    fs: FileSystem | None = None,
) -> list[SimulationResult]:
    """Run multiple simulations in parallel."""
    ...
```

Where `SimulationJob` is:

```python
@dataclass
class SimulationJob:
    model: IDFDocument
    weather: str | Path
    output_dir: str | Path | None = None
    label: str | None = None  # Human-readable identifier
```

Implementation uses `concurrent.futures.ProcessPoolExecutor` (not `multiprocessing.Pool`
directly), which handles Windows `spawn` semantics correctly. Each worker receives a
self-contained `SimulationJob` that is serialized cleanly -- no lambdas, no unpicklable objects.

**Why not `multiprocessing.Pool`?** On Windows, `multiprocessing.Pool` uses `spawn` (not `fork`),
which requires all arguments to be picklable. `concurrent.futures` handles this more gracefully
and integrates with `asyncio` for hybrid async/parallel workflows.

#### Cloud Parallelism

For massively parallel cloud computations (hundreds or thousands of simulations), local
parallelism is insufficient. The design supports cloud execution through:

1. **Serializable jobs**: `SimulationJob` can be serialized to JSON for queue-based dispatch
2. **Isolated directories**: each job writes to its own directory (local, S3, or other)
3. **Stateless execution**: no shared state between simulations
4. **Result collection**: `SimulationResult` can be constructed from a directory path after the
   fact, enabling "submit-then-collect" patterns

```python
# Cloud workflow example (user code, not part of IDFkit):
#
# 1. Prepare jobs locally
# jobs = [SimulationJob(model=m, weather=w, output_dir=f"s3://bucket/run-{i}")
#         for i, (m, w) in enumerate(parametric_sweep)]
#
# 2. Serialize and dispatch to cloud workers (AWS Batch, K8s, etc.)
# for job in jobs:
#     queue.send(job.to_dict())
#
# 3. On each worker:
# job = SimulationJob.from_dict(message)
# result = simulate(job.model, job.weather, output_dir=job.output_dir)
#
# 4. Collect results (can be done later, from any machine):
# results = [SimulationResult.from_directory(f"s3://bucket/run-{i}")
#            for i in range(len(jobs))]
```

### 4.6 Simulation Caching

Inspired by archetypal's approach, IDFkit can hash the simulation inputs to detect redundant runs:

```python
def _compute_simulation_hash(model: IDFDocument, weather: Path, options: dict[str, Any]) -> str:
    """Compute a deterministic hash of the simulation inputs."""
    import hashlib
    h = hashlib.sha256()
    h.update(write_idf(model).encode())     # IDF content
    h.update(weather.read_bytes())           # Weather file content
    h.update(json.dumps(options, sort_keys=True).encode())  # CLI options
    return h.hexdigest()[:16]
```

Caching is opt-in and controlled by a `cache_dir` parameter. When enabled, the simulator checks
if a result directory with the matching hash already exists and returns it directly.

---

## 5. Output Variable Discovery (RDD/MDD Parsing)

### 5.1 The Problem

Users frequently need to know _which_ output variables are available for a given model before they
can add `Output:Variable` or `Output:Meter` objects. This information is only available after
running an initial simulation, which produces `.rdd` (Report Data Dictionary) and `.mdd` (Meter
Data Dictionary) files.

### 5.2 RDD/MDD File Format

These files are plain text with a header, followed by lines like:

```
! Program Version,EnergyPlus, Version 24.1.0-69c052275a
! Output:Variable Objects (Alarm)
Output:Variable,*,Site Outdoor Air Drybulb Temperature,hourly; !- [C]
Output:Variable,*,Zone Mean Air Temperature,hourly; !- [C]
Output:Variable,*,Zone Air System Sensible Heating Rate,hourly; !- [W]
```

And for `.mdd`:

```
Output:Meter,Electricity:Facility,hourly; !- [J]
Output:Meter,NaturalGas:Facility,hourly; !- [J]
```

### 5.3 Data Model

```python
@dataclass(frozen=True)
class OutputVariable:
    """An available output variable from the RDD file."""
    key: str              # e.g., "*" or "ZONE 1"
    name: str             # e.g., "Zone Mean Air Temperature"
    frequency: str        # e.g., "hourly", "timestep", "detailed"
    units: str            # e.g., "C", "W", "J"

    def to_idf_object(self, key: str = "*", frequency: str = "Timestep") -> dict[str, str]:
        """Return field data suitable for model.add('Output:Variable', ...)."""
        return {
            "Key_Value": key,
            "Variable_Name": self.name,
            "Reporting_Frequency": frequency,
        }


@dataclass(frozen=True)
class OutputMeter:
    """An available meter from the MDD file."""
    name: str             # e.g., "Electricity:Facility"
    frequency: str
    units: str

    def to_idf_object(self, frequency: str = "Timestep") -> dict[str, str]:
        """Return field data suitable for model.add('Output:Meter', ...)."""
        return {
            "Key_Name": self.name,
            "Reporting_Frequency": frequency,
        }


class OutputVariableIndex:
    """Index of available output variables and meters for a model."""

    variables: list[OutputVariable]
    meters: list[OutputMeter]

    @classmethod
    def from_simulation(cls, result: SimulationResult) -> OutputVariableIndex:
        """Parse RDD and MDD from a completed simulation."""
        ...

    @classmethod
    def from_files(cls, rdd_path: Path, mdd_path: Path | None = None) -> OutputVariableIndex:
        """Parse RDD/MDD files directly."""
        ...

    def search(self, pattern: str) -> list[OutputVariable | OutputMeter]:
        """Search variables and meters by name pattern (case-insensitive regex)."""
        ...

    def filter_by_units(self, units: str) -> list[OutputVariable | OutputMeter]:
        """Filter by unit type (e.g., 'C', 'W', 'J')."""
        ...

    def add_all_to_model(
        self,
        model: IDFDocument,
        frequency: str = "Timestep",
        filter_pattern: str | None = None,
    ) -> int:
        """Add matching output variables to the model. Returns count added."""
        ...
```

### 5.4 Discovery Workflow

```python
# Step 1: Run a sizing-only simulation to discover available outputs
config = find_energyplus()
result = simulate(model, weather, design_day=True, energyplus=config)

# Step 2: Parse available outputs
index = OutputVariableIndex.from_simulation(result)

# Step 3: Search and add desired outputs
for var in index.search("Zone Mean Air Temperature"):
    model.add("Output:Variable", **var.to_idf_object(frequency="Hourly"))

for meter in index.search("Electricity"):
    model.add("Output:Meter", **meter.to_idf_object(frequency="Monthly"))

# Step 4: Run the full simulation with outputs enabled
result = simulate(model, weather, annual=True, energyplus=config)
```

---

## 6. Simulation Results

### 6.1 SimulationResult Container

```python
@dataclass
class SimulationResult:
    """Container for all outputs from an EnergyPlus simulation."""

    run_dir: Path
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    runtime_seconds: float
    energyplus_version: str

    # Lazy-loaded accessors (parsed on first access, then cached)
    @property
    def errors(self) -> ErrorReport: ...

    @property
    def sql(self) -> SQLResult | None: ...

    @property
    def eso(self) -> ESOResult | None: ...

    @property
    def csv(self) -> CSVResult | None: ...

    @property
    def html_tables(self) -> dict[str, list[list[str]]] | None: ...

    @property
    def rdd(self) -> OutputVariableIndex | None: ...

    @property
    def summary(self) -> dict[str, Any]: ...

    @classmethod
    def from_directory(
        cls,
        path: str | Path,
        fs: FileSystem | None = None,
    ) -> SimulationResult:
        """Reconstruct a result from an existing output directory."""
        ...
```

### 6.2 SQL Result Access

SQLite is the primary result format because it is:
- **Complete**: contains all time-series data, tabular reports, and simulation metadata
- **Queryable**: standard SQL, no custom parsers needed
- **Reliable**: generated by EnergyPlus directly, not by a fragile post-processor
- **Self-contained**: single file with all data

```python
class SQLResult:
    """Query interface for EnergyPlus SQL output."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def get_timeseries(
        self,
        variable_name: str,
        key_value: str = "*",
        frequency: str | None = None,
    ) -> TimeSeriesResult:
        """Retrieve a time series from the SQL database."""
        ...

    def get_tabular_data(
        self,
        report_name: str | None = None,
        table_name: str | None = None,
    ) -> list[TabularReport]:
        """Retrieve tabular report data."""
        ...

    def list_variables(self) -> list[dict[str, str]]:
        """List all available variables in the SQL database."""
        ...

    def list_reports(self) -> list[str]:
        """List all available tabular reports."""
        ...

    def to_dataframe(
        self,
        variable_name: str,
        key_value: str = "*",
    ) -> Any:
        """Return a pandas DataFrame (requires pandas)."""
        ...

    def query(self, sql: str) -> list[tuple[Any, ...]]:
        """Execute a raw SQL query."""
        ...
```

### 6.3 Time Series Representation

```python
@dataclass
class TimeSeriesResult:
    """A single time series extracted from simulation results."""

    variable_name: str
    key_value: str
    units: str
    frequency: str
    timestamps: list[datetime]
    values: list[float]

    def to_dataframe(self) -> Any:
        """Convert to pandas DataFrame (requires pandas)."""
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for DataFrame conversion: pip install pandas")
        return pd.DataFrame(
            {"timestamp": self.timestamps, self.variable_name: self.values}
        ).set_index("timestamp")
```

### 6.4 Error Report

```python
@dataclass
class ErrorReport:
    """Parsed EnergyPlus .err file."""

    fatal: list[str]
    severe: list[str]
    warnings: list[str]
    info: list[str]
    warmup_converged: bool
    simulation_complete: bool

    @property
    def has_fatal(self) -> bool:
        return len(self.fatal) > 0

    @property
    def has_severe(self) -> bool:
        return len(self.severe) > 0
```

---

## 7. File System Abstraction

### 7.1 Why Abstract?

Cloud simulation workflows need to:
- Write IDF files to S3 before dispatch to cloud workers
- Read result files from S3 after completion
- Avoid downloading entire result directories when only specific files are needed

### 7.2 FileSystem Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class FileSystem(Protocol):
    """Minimal file system interface for simulation I/O."""

    def read_bytes(self, path: str | Path) -> bytes: ...
    def write_bytes(self, path: str | Path, data: bytes) -> None: ...
    def read_text(self, path: str | Path, encoding: str = "utf-8") -> str: ...
    def write_text(self, path: str | Path, text: str, encoding: str = "utf-8") -> None: ...
    def exists(self, path: str | Path) -> bool: ...
    def makedirs(self, path: str | Path, exist_ok: bool = False) -> None: ...
    def copy(self, src: str | Path, dst: str | Path) -> None: ...
    def glob(self, path: str | Path, pattern: str) -> list[str]: ...
    def remove(self, path: str | Path) -> None: ...
```

### 7.3 Implementations

**LocalFileSystem** (default, zero dependencies):

```python
class LocalFileSystem:
    """Standard local filesystem operations."""

    def read_bytes(self, path: str | Path) -> bytes:
        return Path(path).read_bytes()

    def write_bytes(self, path: str | Path, data: bytes) -> None:
        Path(path).write_bytes(data)

    # ... etc
```

**S3FileSystem** (optional, requires `boto3` or `s3fs`):

```python
class S3FileSystem:
    """S3-compatible file system using boto3 or s3fs."""

    def __init__(self, bucket: str, prefix: str = "", **boto_kwargs: Any) -> None:
        ...
```

The protocol-based design means users can implement their own backends for Azure Blob Storage,
GCS, or any other storage system without modifying IDFkit.

### 7.4 File System in Practice

```python
# Local simulation (default)
result = simulate(model, weather)

# S3-backed simulation (for cloud workers)
fs = S3FileSystem(bucket="my-simulations", prefix="batch-42/")
result = simulate(model, weather, output_dir="run-001", fs=fs)

# Collect results from S3 (from any machine)
result = SimulationResult.from_directory("run-001", fs=fs)
ts = result.sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
```

---

## 8. Plotting and Visualization

### 8.1 Design Philosophy

IDFkit should not force a plotting library on users. Data scientists may prefer matplotlib,
web developers may prefer plotly, and some users may want raw data for their own tooling.

### 8.2 Plot Backend Protocol

```python
@runtime_checkable
class PlotBackend(Protocol):
    """Protocol for pluggable plotting backends."""

    def line(
        self,
        x: list[Any],
        y: list[float],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        label: str | None = None,
    ) -> Any: ...

    def multi_line(
        self,
        x: list[Any],
        ys: dict[str, list[float]],
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> Any: ...

    def heatmap(
        self,
        data: list[list[float]],
        *,
        x_labels: list[str] | None = None,
        y_labels: list[str] | None = None,
        title: str | None = None,
    ) -> Any: ...

    def bar(
        self,
        categories: list[str],
        values: list[float],
        *,
        title: str | None = None,
        ylabel: str | None = None,
    ) -> Any: ...
```

### 8.3 Convenience Methods on Results

```python
class TimeSeriesResult:

    def plot(self, backend: PlotBackend | None = None, **kwargs: Any) -> Any:
        """Plot this time series using the specified backend."""
        if backend is None:
            backend = _auto_detect_backend()
        return backend.line(
            self.timestamps,
            self.values,
            title=f"{self.variable_name} [{self.key_value}]",
            xlabel="Time",
            ylabel=f"{self.variable_name} [{self.units}]",
            **kwargs,
        )
```

Auto-detection tries matplotlib first (common in Jupyter), then plotly, then raises an
`ImportError` with installation instructions.

### 8.4 Common Visualization Patterns

The plotting module should provide pre-built visualization patterns for common EnergyPlus
analysis tasks:

```python
def plot_energy_balance(result: SimulationResult, backend: PlotBackend | None = None) -> Any:
    """Stacked bar chart of heating, cooling, lighting, equipment energy."""
    ...

def plot_temperature_profile(
    result: SimulationResult,
    zones: list[str] | None = None,
    backend: PlotBackend | None = None,
) -> Any:
    """Line plot of zone temperatures over time."""
    ...

def plot_comfort_hours(result: SimulationResult, backend: PlotBackend | None = None) -> Any:
    """Heatmap of comfort/discomfort hours by zone and month."""
    ...
```

---

## 9. Weather File and Design Day Browser

### 9.1 The Problem

Finding the right weather file is one of the most tedious steps in an EnergyPlus workflow:

- **Manual downloading**: Users must navigate climate.onebuilding.org's directory hierarchy
  (WMO Region > Country > State) to find a station, then download a ZIP, extract the EPW, and
  place it in the right directory.
- **Station selection**: With 17,300+ stations worldwide, users often don't know which station
  is closest to their building site. They resort to manual map browsing or guesswork.
- **Design day injection**: After downloading a DDY file, users must manually open it, identify
  the right design day objects (heating 99.6%? cooling 1%?), and copy them into their IDF model.
  This is error-prone and poorly documented across existing packages.
- **Year-range confusion**: climate.onebuilding.org offers multiple TMYx variants per station
  (full period, 2004-2018, 2007-2021, 2009-2023). Users rarely know which to choose.

No existing Python package solves this end-to-end.

### 9.2 Data Source: climate.onebuilding.org

climate.onebuilding.org provides the most comprehensive free collection of EnergyPlus weather
files, organized by WMO (World Meteorological Organization) regions:

| Region | Coverage | Stations |
|--------|----------|----------|
| WMO Region 1 | Africa | 1,382 |
| WMO Region 2 | Asia | 3,167 |
| WMO Region 3 | South America | 1,143 |
| WMO Region 4 | North & Central America | 4,327 |
| WMO Region 5 | Southwest Pacific | 1,396 |
| WMO Region 6 | Europe | 3,999 |
| WMO Region 7 | Antarctica | 109 |
| **Total** | **250+ countries** | **17,300+** |

Each station is distributed as a ZIP archive containing:

| File | Purpose |
|------|---------|
| `.epw` | EnergyPlus weather data (8,760 hourly records) |
| `.ddy` | ASHRAE design day conditions (`SizingPeriod:DesignDay` objects) |
| `.stat` | Climate statistics (ASHRAE climate zone, monthly summaries) |
| `.clm` | ESP-r weather format |
| `.wea` | Daysim daylighting format |
| `.rain` | Hourly precipitation data |
| `.pvsyst` | PV solar design format |

Up to **four TMYx variants** exist per station:

| Variant | Suffix | Best for |
|---------|--------|----------|
| Full period | `_TMYx` | Longest statistical basis |
| 2004-2018 | `_TMYx.2004-2018` | Legacy comparisons |
| 2007-2021 | `_TMYx.2007-2021` | Recent climate, ASHRAE 2021 alignment |
| 2009-2023 | `_TMYx.2009-2023` | Most current climate conditions |

### 9.3 File Naming Convention

climate.onebuilding.org uses a structured naming scheme that encodes location metadata:

```
{Country}_{State}_{Location}.{Facility}.{WMO}_{Dataset}.{YearRange}.zip

USA_CA_Los.Angeles.Intl.AP.722950_TMYx.2009-2023.zip
^^^  ^^  ^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^ ^^^^^^^^^
 |   |         |           |        |       |
 |   |         |           |        |       +-- Year range (optional)
 |   |         |           |        +---------- Dataset type
 |   |         |           +------------------- WMO station number (6 digits)
 |   |         +------------------------------- Location + facility (dot-separated)
 |   +----------------------------------------- State/Province abbreviation
 +---------------------------------------------- ISO 3166 country code
```

This naming convention is parsed during index construction to extract searchable metadata
without downloading the actual EPW files.

### 9.4 Bundled Station Index

The site does not provide a single REST API or consolidated station list. Station metadata is
spread across per-region XLSX spreadsheets and KML map files. To enable offline search, IDFkit
bundles a **pre-built station index** as a compressed CSV:

```
src/idfkit/weather/_data/stations.csv.gz  (~300KB compressed, ~2MB uncompressed)
```

#### Index Schema

| Column | Type | Example | Source |
|--------|------|---------|--------|
| `wmo` | str | `722950` | Filename |
| `name` | str | `Los Angeles Intl AP` | Filename (dots replaced with spaces) |
| `country` | str | `USA` | Filename |
| `state` | str | `CA` | Filename |
| `latitude` | float | `33.938` | EPW header or XLSX |
| `longitude` | float | `-118.389` | EPW header or XLSX |
| `elevation` | float | `30.0` | EPW header or XLSX |
| `timezone` | float | `-8.0` | EPW header or XLSX |
| `wmo_region` | int | `4` | Directory path |
| `climate_zone` | str | `3B` | STAT file |
| `datasets` | str | `TMYx,TMYx.2007-2021,TMYx.2009-2023` | Directory listing |
| `url_template` | str | `WMO_Region_4_.../USA_CA_Los.Angeles.Intl.AP.722950_{dataset}.zip` | Directory path |

#### Index Build Process

A one-time script (not shipped to users) builds the index by:

1. Downloading the per-region XLSX spreadsheets from climate.onebuilding.org/sources/
2. Parsing station metadata (WMO, name, lat, lon, elevation, timezone)
3. Cross-referencing with directory listings to determine available datasets per station
4. Extracting ASHRAE climate zones from STAT file summaries where available
5. Compressing the merged CSV with gzip

The index is regenerated periodically (quarterly or when new TMYx datasets are released) and
committed to the repository. Users get the latest index with each IDFkit release.

### 9.5 WeatherStation Data Model

```python
@dataclass(frozen=True)
class WeatherStation:
    """Metadata for a single weather station from climate.onebuilding.org."""

    wmo: str                           # WMO station number (e.g., "722950")
    name: str                          # Station name (e.g., "Los Angeles Intl AP")
    country: str                       # ISO country code (e.g., "USA")
    state: str                         # State/province abbreviation (e.g., "CA")
    latitude: float                    # Decimal degrees, N positive
    longitude: float                   # Decimal degrees, E positive
    elevation: float                   # Meters above sea level
    timezone: float                    # Hours from GMT (e.g., -8.0)
    wmo_region: int                    # WMO region number (1-7)
    climate_zone: str | None           # ASHRAE climate zone (e.g., "3B")
    datasets: tuple[str, ...]          # Available dataset variants

    @property
    def display_name(self) -> str:
        """Human-readable station identifier."""
        parts = [self.name]
        if self.state:
            parts.append(self.state)
        parts.append(self.country)
        return ", ".join(parts)

    @property
    def latest_tmyx(self) -> str | None:
        """The most recent TMYx year-range variant available."""
        # Prefer the most recent year range
        for suffix in ("TMYx.2009-2023", "TMYx.2007-2021", "TMYx.2004-2018", "TMYx"):
            if suffix in self.datasets:
                return suffix
        return None

    def download_url(self, dataset: str | None = None) -> str:
        """Construct the full download URL for a specific dataset variant."""
        ...
```

### 9.6 Station Index and Search

```python
class StationIndex:
    """Searchable index of 17,300+ weather stations worldwide."""

    def __init__(self, stations: list[WeatherStation]) -> None:
        self._stations = stations
        self._by_wmo: dict[str, WeatherStation] = {s.wmo: s for s in stations}
        # Precompute radians for spatial queries
        self._coords_rad: list[tuple[float, float]] = [
            (math.radians(s.latitude), math.radians(s.longitude))
            for s in stations
        ]

    @classmethod
    def load(cls) -> StationIndex:
        """Load the bundled station index (lazy singleton)."""
        ...

    # --- Exact Lookups ---

    def get(self, wmo: str) -> WeatherStation | None:
        """Look up a station by WMO number."""
        return self._by_wmo.get(wmo)

    # --- Fuzzy Text Search ---

    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        country: str | None = None,
        climate_zone: str | None = None,
    ) -> list[SearchResult]:
        """Fuzzy search stations by name, city, state, or WMO number.

        Uses a multi-signal scoring approach:
        1. Exact WMO match (highest priority)
        2. Exact substring match on name (high priority)
        3. Token-level fuzzy matching (medium priority)
        4. Country/climate_zone filters applied as hard constraints
        """
        ...

    # --- Spatial Search ---

    def nearest(
        self,
        latitude: float,
        longitude: float,
        *,
        limit: int = 5,
        max_distance_km: float | None = None,
        country: str | None = None,
    ) -> list[SpatialResult]:
        """Find the nearest stations to a given coordinate.

        Uses the Haversine formula for great-circle distance.
        Returns results sorted by distance, closest first.
        """
        ...

    def nearest_to_address(
        self,
        address: str,
        *,
        limit: int = 5,
        max_distance_km: float | None = None,
    ) -> list[SpatialResult]:
        """Geocode an address and find the nearest stations.

        Uses the free Nominatim (OpenStreetMap) geocoding API.
        No API key required. Rate limited to 1 request/second.
        """
        ...

    # --- Filtering ---

    def filter(
        self,
        *,
        country: str | None = None,
        state: str | None = None,
        climate_zone: str | None = None,
        wmo_region: int | None = None,
        latitude_range: tuple[float, float] | None = None,
        longitude_range: tuple[float, float] | None = None,
    ) -> list[WeatherStation]:
        """Filter stations by metadata criteria."""
        ...

    @property
    def countries(self) -> list[str]:
        """List all unique country codes."""
        ...

    @property
    def climate_zones(self) -> list[str]:
        """List all unique ASHRAE climate zones."""
        ...
```

#### Search Result Types

```python
@dataclass(frozen=True)
class SearchResult:
    """A text search result with relevance score."""
    station: WeatherStation
    score: float              # 0.0 to 1.0, higher is better
    match_field: str          # Which field matched: "wmo", "name", "state", "country"

@dataclass(frozen=True)
class SpatialResult:
    """A spatial proximity result with distance."""
    station: WeatherStation
    distance_km: float        # Great-circle distance in kilometers
```

### 9.7 Fuzzy Search Implementation

The fuzzy search must work without heavy NLP dependencies. The approach uses a multi-signal
scoring function built on standard library primitives:

```python
def _score_station(station: WeatherStation, query: str, tokens: list[str]) -> float:
    """Score a station against a search query. Returns 0.0-1.0."""
    name_lower = station.name.lower()
    score = 0.0

    # Signal 1: Exact WMO match (strongest signal)
    if query == station.wmo:
        return 1.0

    # Signal 2: Full query is a substring of the station name
    if query in name_lower:
        score = max(score, 0.85 + 0.1 * (len(query) / len(name_lower)))

    # Signal 3: All query tokens appear in the station name
    name_tokens = set(name_lower.split())
    if all(any(t.startswith(qt) for t in name_tokens) for qt in tokens):
        coverage = sum(len(qt) for qt in tokens) / max(len(name_lower), 1)
        score = max(score, 0.6 + 0.3 * coverage)

    # Signal 4: Partial token overlap (prefix matching)
    matching_tokens = sum(
        1 for qt in tokens
        if any(t.startswith(qt) for t in name_tokens)
    )
    if matching_tokens > 0:
        ratio = matching_tokens / len(tokens)
        score = max(score, 0.3 * ratio)

    # Signal 5: State or country code match (bonus)
    if query == station.state.lower() or query == station.country.lower():
        score = max(score, 0.5)

    return score
```

This avoids external dependencies like `rapidfuzz` or `thefuzz` while still providing useful
results for common queries like "chicago", "los angeles", "heathrow", or "4A" (climate zone).

### 9.8 Spatial Search Implementation

#### Haversine Distance (Zero Dependencies)

```python
import math

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points in kilometers.

    All arguments in decimal degrees.
    Accuracy: <0.5% error, sufficient for station-to-site distance.
    """
    lat1_r, lon1_r = math.radians(lat1), math.radians(lon1)
    lat2_r, lon2_r = math.radians(lat2), math.radians(lon2)
    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2.0 * math.asin(math.sqrt(a))
```

#### Nearest-Neighbor Strategy

For 17,300 stations, a brute-force scan with Haversine takes ~5-10ms in pure Python -- fast
enough for interactive use. No spatial indexing is required.

If performance becomes a concern (e.g., batch geocoding thousands of building sites), an
optional optimization path is available:

1. **Bounding-box pre-filter**: Before computing Haversine, exclude stations whose latitude or
   longitude differs by more than `max_distance_km / 111` degrees (1 degree latitude ~ 111 km).
   This reduces the candidate set by ~95% for a 200 km radius.
2. **Precomputed radians**: Store `(lat_rad, lon_rad)` tuples at index load time to avoid
   repeated `math.radians()` calls.
3. **Optional scipy integration**: If `scipy` is available, use `scipy.spatial.cKDTree` for
   O(log N) nearest-neighbor queries on Cartesian-projected coordinates.

The brute-force approach is the default. The bounding-box pre-filter is always applied. The
scipy path is used opportunistically when the package is already installed.

### 9.9 Free Address Geocoding

#### Nominatim (OpenStreetMap) Integration

Nominatim provides free geocoding (address to lat/lon) with no API key. The only requirements
are a descriptive `User-Agent` header and a rate limit of 1 request per second.

```python
import urllib.request
import urllib.parse
import json
import time

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
_USER_AGENT = "idfkit/{version} (https://github.com/samuelduchesne/idfkit)"
_last_request_time: float = 0.0

def geocode(address: str) -> tuple[float, float] | None:
    """Convert an address string to (latitude, longitude) using Nominatim.

    Free, no API key required. Rate limited to 1 request/second per
    Nominatim usage policy.

    Returns None if the address could not be geocoded.
    """
    global _last_request_time

    # Enforce rate limit
    elapsed = time.monotonic() - _last_request_time
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)

    params = urllib.parse.urlencode({
        "q": address,
        "format": "json",
        "limit": "1",
    })
    url = f"{_NOMINATIM_URL}?{params}"

    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            _last_request_time = time.monotonic()
            data = json.loads(resp.read())
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, IndexError):
        pass
    return None
```

Key design points:

- **Zero dependencies**: uses only `urllib.request` and `json` from the standard library
- **Rate limiting**: enforced client-side with `time.monotonic()` to comply with Nominatim's
  1 req/sec policy
- **Graceful failure**: returns `None` on network errors, no exceptions propagated
- **No caching needed**: the typical use case is a single geocode call followed by spatial search

#### Integration with Station Search

```python
# User searches by address -- internally geocodes then finds nearest stations
results = index.nearest_to_address("350 Fifth Avenue, New York, NY")
for r in results:
    print(f"  {r.station.display_name} ({r.distance_km:.0f} km)")
```

Output:
```
  New York J F Kennedy Intl AP, NY, USA (18 km)
  New York La Guardia AP, NY, USA (10 km)
  Newark Liberty Intl AP, NJ, USA (22 km)
  Teterboro AP, NJ, USA (29 km)
  White Plains Westchester Co AP, NY, USA (42 km)
```

### 9.10 Weather File Download

```python
class WeatherDownloader:
    """Download EPW, DDY, and related files from climate.onebuilding.org."""

    BASE_URL = "https://climate.onebuilding.org"

    def __init__(self, cache_dir: Path | None = None) -> None:
        """Initialize the downloader.

        Args:
            cache_dir: Directory for caching downloaded files. Defaults to
                       ~/.cache/idfkit/weather/ (XDG_CACHE_HOME on Linux,
                       ~/Library/Caches/idfkit/weather/ on macOS,
                       %LOCALAPPDATA%/idfkit/cache/weather/ on Windows).
        """
        self._cache_dir = cache_dir or _default_cache_dir()

    def download(
        self,
        station: WeatherStation,
        *,
        dataset: str | None = None,
        extract: bool = True,
    ) -> WeatherFiles:
        """Download weather files for a station.

        Args:
            station: The weather station to download files for.
            dataset: TMYx variant (e.g., "TMYx.2009-2023"). Defaults to
                     the most recent available variant.
            extract: If True, extract EPW and DDY from the ZIP. If False,
                     return the path to the ZIP file.

        Returns:
            WeatherFiles container with paths to downloaded files.
        """
        ...

    def get_epw(
        self,
        station: WeatherStation,
        dataset: str | None = None,
    ) -> Path:
        """Download and return the path to the EPW file."""
        files = self.download(station, dataset=dataset)
        return files.epw

    def get_ddy(
        self,
        station: WeatherStation,
        dataset: str | None = None,
    ) -> Path:
        """Download and return the path to the DDY file."""
        files = self.download(station, dataset=dataset)
        return files.ddy

    def clear_cache(self) -> None:
        """Remove all cached weather files."""
        ...


@dataclass(frozen=True)
class WeatherFiles:
    """Paths to downloaded weather-related files."""
    epw: Path
    ddy: Path
    stat: Path | None
    zip_path: Path
    station: WeatherStation
    dataset: str
```

#### Caching Strategy

Downloaded files are cached in a platform-appropriate directory:

| Platform | Default Cache Directory |
|----------|----------------------|
| Linux | `~/.cache/idfkit/weather/` (or `$XDG_CACHE_HOME/idfkit/weather/`) |
| macOS | `~/Library/Caches/idfkit/weather/` |
| Windows | `%LOCALAPPDATA%\idfkit\cache\weather\` |

Cache layout:

```
~/.cache/idfkit/weather/
├── 722950/                                    # WMO station number
│   ├── TMYx.2009-2023/                        # Dataset variant
│   │   ├── USA_CA_Los.Angeles.Intl.AP.722950_TMYx.2009-2023.epw
│   │   ├── USA_CA_Los.Angeles.Intl.AP.722950_TMYx.2009-2023.ddy
│   │   └── USA_CA_Los.Angeles.Intl.AP.722950_TMYx.2009-2023.stat
│   └── TMYx.2007-2021/
│       └── ...
```

Files are never re-downloaded if they already exist in the cache. The cache can be cleared
programmatically or by deleting the directory.

### 9.11 Design Day Parsing and Model Injection

This is the highest-value convenience feature: automatically extracting the right
`SizingPeriod:DesignDay` objects from a DDY file and injecting them into an IDF model.

#### DDY File Structure

A DDY file is a valid IDF-syntax file containing:
1. A `Site:Location` object (matching the EPW station metadata)
2. Typically **14-15** `SizingPeriod:DesignDay` objects covering:
   - Heating design days (99.6% and 99% annual conditions)
   - Cooling dry-bulb design days (0.4%, 1%, 2% annual conditions)
   - Cooling wet-bulb (evaporation) design days (0.4%, 1%, 2%)
   - Dehumidification design days (0.4%, 1%, 2%)
   - Wind speed design days (coldest month 0.4%, 1%)
   - Humidification design days (99.6%, 99%)

#### Design Day Categories

Each design day name in the DDY file follows ASHRAE naming conventions. IDFkit parses these
names to classify design days:

```python
class DesignDayType(Enum):
    """Classification of ASHRAE design day conditions."""
    HEATING_99_6 = "heating_99.6"           # Heating dry-bulb 99.6%
    HEATING_99 = "heating_99"               # Heating dry-bulb 99%
    COOLING_DB_0_4 = "cooling_db_0.4"       # Cooling dry-bulb/MCWB 0.4%
    COOLING_DB_1 = "cooling_db_1"           # Cooling dry-bulb/MCWB 1%
    COOLING_DB_2 = "cooling_db_2"           # Cooling dry-bulb/MCWB 2%
    COOLING_WB_0_4 = "cooling_wb_0.4"       # Evaporation wet-bulb/MDB 0.4%
    COOLING_WB_1 = "cooling_wb_1"           # Evaporation wet-bulb/MDB 1%
    COOLING_WB_2 = "cooling_wb_2"           # Evaporation wet-bulb/MDB 2%
    DEHUMID_0_4 = "dehumid_0.4"             # Dehumidification DP/MDB 0.4%
    DEHUMID_1 = "dehumid_1"                 # Dehumidification DP/MDB 1%
    DEHUMID_2 = "dehumid_2"                 # Dehumidification DP/MDB 2%
    HUMIDIFICATION_99_6 = "humidif_99.6"    # Humidification DP/MCDB 99.6%
    HUMIDIFICATION_99 = "humidif_99"        # Humidification DP/MCDB 99%
    WIND_0_4 = "wind_0.4"                   # Coldest month WS/MDB 0.4%
    WIND_1 = "wind_1"                       # Coldest month WS/MDB 1%
```

#### DesignDayManager API

```python
class DesignDayManager:
    """Parse DDY files and inject design day conditions into IDF models."""

    def __init__(self, ddy_path: Path) -> None:
        """Parse a DDY file into classified design day objects."""
        self._path = ddy_path
        self._design_days: dict[DesignDayType, IDFObject] = {}
        self._location: IDFObject | None = None
        self._parse()

    @classmethod
    def from_station(
        cls,
        station: WeatherStation,
        dataset: str | None = None,
    ) -> DesignDayManager:
        """Download the DDY file for a station and parse it."""
        downloader = WeatherDownloader()
        ddy_path = downloader.get_ddy(station, dataset=dataset)
        return cls(ddy_path)

    @property
    def all_design_days(self) -> list[IDFObject]:
        """All parsed SizingPeriod:DesignDay objects."""
        return list(self._design_days.values())

    def get(self, dd_type: DesignDayType) -> IDFObject | None:
        """Get a specific design day by type."""
        return self._design_days.get(dd_type)

    @property
    def heating(self) -> list[IDFObject]:
        """All heating design days."""
        return [dd for t, dd in self._design_days.items()
                if t.value.startswith("heating")]

    @property
    def cooling(self) -> list[IDFObject]:
        """All cooling design days (dry-bulb, wet-bulb, and dehumidification)."""
        return [dd for t, dd in self._design_days.items()
                if t.value.startswith("cooling") or t.value.startswith("dehumid")]

    def apply_to_model(
        self,
        model: IDFDocument,
        *,
        heating: Literal["99.6%", "99%", "both"] = "99.6%",
        cooling: Literal["0.4%", "1%", "2%", "all"] = "1%",
        include_wet_bulb: bool = False,
        include_dehumidification: bool = False,
        include_wind: bool = False,
        update_location: bool = True,
        replace_existing: bool = True,
    ) -> list[str]:
        """Inject design day objects into an IDF model.

        This is the primary convenience method. It selects the appropriate
        design days based on common ASHRAE sizing practices and adds them
        to the model.

        Args:
            model: The IDFDocument to modify.
            heating: Which heating design day to use.
            cooling: Which cooling dry-bulb percentile to use.
            include_wet_bulb: Also add evaporation wet-bulb cooling days.
            include_dehumidification: Also add dehumidification cooling days.
            include_wind: Also add wind-speed design days.
            update_location: Also update the Site:Location object in the model
                             to match the DDY station metadata.
            replace_existing: Remove existing SizingPeriod:DesignDay objects
                              before adding new ones.

        Returns:
            List of design day names that were added to the model.
        """
        ...

    def summary(self) -> str:
        """Human-readable summary of all design days in the DDY file."""
        ...
```

#### Common Presets

For users who don't want to think about percentile selection:

```python
def apply_ashrae_sizing(
    model: IDFDocument,
    station: WeatherStation,
    *,
    standard: Literal["90.1", "general"] = "general",
    dataset: str | None = None,
) -> list[str]:
    """Apply standard ASHRAE sizing design days to a model.

    Presets:
    - "90.1": Heating 99.6% + Cooling 1% DB + Cooling 1% WB
              (per ASHRAE Standard 90.1 requirements)
    - "general": Heating 99.6% + Cooling 0.4% DB
              (conservative general practice)
    """
    ddm = DesignDayManager.from_station(station, dataset=dataset)

    if standard == "90.1":
        return ddm.apply_to_model(
            model,
            heating="99.6%",
            cooling="1%",
            include_wet_bulb=True,
        )
    else:  # "general"
        return ddm.apply_to_model(
            model,
            heating="99.6%",
            cooling="0.4%",
        )
```

### 9.12 End-to-End Weather Workflow

```python
from idfkit import load_idf
from idfkit.weather import StationIndex, WeatherDownloader, apply_ashrae_sizing

model = load_idf("office.idf")
index = StationIndex.load()

# --- Search by name ---
results = index.search("chicago ohare")
station = results[0].station
print(f"{station.display_name} (WMO {station.wmo}, climate zone {station.climate_zone})")
# Chicago Ohare Intl AP, IL, USA (WMO 725300, climate zone 5A)

# --- Search by address (free, no API key) ---
results = index.nearest_to_address("Willis Tower, Chicago, IL")
for r in results[:3]:
    print(f"  {r.station.display_name} — {r.distance_km:.0f} km")
# Chicago Ohare Intl AP, IL, USA — 25 km
# Chicago Midway AP, IL, USA — 12 km
# Chicago Aurora Muni AP, IL, USA — 55 km

# --- Search by coordinates ---
results = index.nearest(41.8781, -87.6298, limit=3)

# --- Filter by ASHRAE climate zone ---
zone_4a = index.filter(climate_zone="4A", country="USA")
print(f"{len(zone_4a)} stations in ASHRAE zone 4A (USA)")

# --- Download weather files ---
downloader = WeatherDownloader()
weather_files = downloader.download(station, dataset="TMYx.2009-2023")
print(f"EPW: {weather_files.epw}")
print(f"DDY: {weather_files.ddy}")

# --- Apply design days to model (one line!) ---
added = apply_ashrae_sizing(model, station, standard="90.1")
print(f"Added {len(added)} design days: {added}")
# Added 3 design days: ['Chicago Ohare Intl AP Ann Htg 99.6% Condns DB',
#                        'Chicago Ohare Intl AP Ann Clg 1% Condns DB=>MWB',
#                        'Chicago Ohare Intl AP Ann Clg 1% Condns WB=>MDB']

# --- Or fine-grained control ---
from idfkit.weather import DesignDayManager
ddm = DesignDayManager(weather_files.ddy)
print(ddm.summary())
ddm.apply_to_model(
    model,
    heating="both",
    cooling="all",
    include_dehumidification=True,
    include_wet_bulb=True,
)

# --- Simulate with the downloaded EPW ---
from idfkit.sim import simulate
result = simulate(model, weather_files.epw)
```

### 9.13 Handling Missing Design Days

Some DDY files contain only a `Site:Location` object and no `SizingPeriod:DesignDay` objects.
This occurs when the station's WMO number is absent from the ASHRAE design conditions lookup
table (common for smaller or newer stations).

When this happens, `DesignDayManager` raises a descriptive error:

```python
class NoDesignDaysError(IdfKitError):
    """Raised when a DDY file contains no SizingPeriod:DesignDay objects."""

    def __init__(self, station: WeatherStation) -> None:
        nearby = StationIndex.load().nearest(
            station.latitude, station.longitude, limit=3
        )
        nearby_with_ddy = [r for r in nearby if r.station.wmo != station.wmo]
        suggestions = "\n".join(
            f"  - {r.station.display_name} (WMO {r.station.wmo}, {r.distance_km:.0f} km)"
            for r in nearby_with_ddy[:3]
        )
        super().__init__(
            f"DDY file for {station.display_name} (WMO {station.wmo}) contains no "
            f"SizingPeriod:DesignDay objects. This station may lack ASHRAE design "
            f"conditions data.\n\nNearest stations that may have design days:\n{suggestions}"
        )
```

---

## 10. Dependency Strategy

### 10.1 Core (Zero Extra Dependencies)

The `idfkit.sim` and `idfkit.weather` core modules should work with **only the standard library**:

- `subprocess` for execution
- `sqlite3` for SQL output parsing
- `json` for serialization
- `tempfile` for isolated directories
- `pathlib` for path handling
- `re` for RDD/MDD parsing
- `datetime` for timestamps
- `hashlib` for simulation caching
- `urllib.request` for weather file downloads and Nominatim geocoding
- `zipfile` for extracting EPW/DDY from downloaded archives
- `gzip` / `csv` for loading the bundled station index
- `math` for Haversine distance calculations
- `time` for Nominatim rate limiting

### 10.2 Optional Extras

```toml
# pyproject.toml
[project.optional-dependencies]
sim = []                        # Core simulation (no extras needed)
pandas = ["pandas>=1.5"]        # DataFrame results
plot = ["matplotlib>=3.5"]      # matplotlib plotting
plotly = ["plotly>=5.0"]         # plotly plotting
s3 = ["boto3>=1.26"]            # S3 filesystem
cloud = ["boto3>=1.26"]         # Alias for s3
all = ["pandas>=1.5", "matplotlib>=3.5", "plotly>=5.0", "boto3>=1.26"]
```

### 10.3 Lazy Imports

All optional dependencies use lazy imports with clear error messages:

```python
def _import_pandas() -> Any:
    try:
        import pandas as pd
        return pd
    except ImportError:
        raise ImportError(
            "pandas is required for this feature. "
            "Install it with: pip install idfkit[pandas]"
        ) from None
```

---

## 11. Implementation Phases

### Phase 1: Core Simulation (Foundation) ✅ COMPLETED

**Scope**: Discover EnergyPlus, run simulations, parse errors, return structured results.

- ✅ `EnergyPlusConfig` frozen dataclass with `from_path()` constructor and `weather_dir`, `schema_path`, `expand_objects_exe` properties
- ✅ `find_energyplus()` with layered discovery: explicit path → `ENERGYPLUS_DIR` env var → `shutil.which` → platform-specific dirs (newest version first)
- ✅ `simulate()` function with subprocess execution, model copy to avoid mutation, isolated run directories
- ✅ `SimulationResult` dataclass with lazy-cached `errors` property and path accessors (`sql_path`, `err_path`, `eso_path`, `csv_path`, `html_path`, `rdd_path`, `mdd_path`)
- ✅ `SimulationResult.from_directory()` for reconstructing results from existing output dirs
- ✅ Automatic `Output:SQLite` injection via `_ensure_sql_output()`
- ✅ Simulation directory isolation with `_prepare_run_directory()` (temp dir or explicit)
- ✅ `.err` file parser with `ErrorMessage` and `ErrorReport` frozen dataclasses, severity classification (Fatal/Severe/Warning/Info), continuation line grouping, warmup convergence and completion detection
- ✅ `EnergyPlusNotFoundError` and `SimulationError` exceptions with actionable error messages
- ✅ Unit tests (50 tests) with mocked subprocess, covering err parser, config discovery, and simulation runner

**Deviations from original plan**:
- Package named `idfkit.simulation` (not `idfkit.sim`) for clarity
- `EnergyPlusConfig` uses `from_path()` classmethod instead of `find()` on the config class; `find_energyplus()` is a standalone function
- `ErrorReport` uses structured `ErrorMessage` dataclasses (with `severity`, `message`, `details` tuple) instead of plain string lists
- Version extraction supports both directory name patterns and IDD header fallback
- `_build_command` uses short flags (`-w`, `-d`, `-p`, `-s`, `-x`, `-a`, `-D`, `-r`) matching EnergyPlus CLI conventions

**Files created**:
- `src/idfkit/simulation/__init__.py`
- `src/idfkit/simulation/config.py`
- `src/idfkit/simulation/runner.py`
- `src/idfkit/simulation/result.py`
- `src/idfkit/simulation/parsers/__init__.py`
- `src/idfkit/simulation/parsers/err.py`
- `tests/test_simulation_config.py`
- `tests/test_simulation_err_parser.py`
- `tests/test_simulation_runner.py`
- `tests/fixtures/simulation/sample.err`
- `tests/fixtures/simulation/sample_fatal.err`

**Files modified**:
- `src/idfkit/exceptions.py` — added `EnergyPlusNotFoundError`, `SimulationError`
- `src/idfkit/__init__.py` — added new exception exports

### Phase 2: Output Parsing and Variable Discovery ✅ COMPLETED

**Scope**: Parse simulation outputs, discover available variables, add them to models.

- ✅ RDD/MDD parser with `OutputVariable` and `OutputMeter` frozen dataclasses, regex-based line parsing, `parse_rdd()`/`parse_mdd()` functions and `_file()` variants
- ✅ `OutputVariableIndex` frozen dataclass with `from_simulation()`, `from_files()`, `search()` (case-insensitive regex), `filter_by_units()`, and `add_all_to_model()` with optional `filter_pattern`
- ✅ SQL output parser (`SQLResult`) with `sqlite3`, read-only mode, context manager, `get_timeseries()` (filters warmup, handles Hour=24 rollover), `get_tabular_data()`, `list_variables()`, `list_reports()`, `query()`
- ✅ `TimeSeriesResult` frozen dataclass with `to_dataframe()` (optional pandas via `dataframes` extra)
- ✅ `TabularRow` and `VariableInfo` frozen dataclasses for structured SQL results
- ✅ CSV parser (`CSVResult`) with header regex extraction of key_value, variable_name, units, frequency; `from_file()`/`from_string()` classmethods and `get_column()` lookup
- ✅ Lazy cached properties on `SimulationResult`: `.sql`, `.variables`, `.csv` following existing `.errors` pattern with sentinel-based caching
- ✅ Updated `__init__.py` exports: `OutputVariable`, `OutputMeter`, `OutputVariableIndex`, `SQLResult`, `TimeSeriesResult`, `TabularRow`, `VariableInfo`, `CSVResult`, `CSVColumn`
- ✅ Unit tests (84 new tests) covering all parsers, index operations, model injection, and lazy property caching

**Deviations from original plan**:
- Package named `idfkit.simulation` (not `idfkit.sim`) — consistent with Phase 1
- ESO, HTML, and EIO parsers deferred — SQL covers the same data more reliably
- `OutputVariableIndex` is a frozen dataclass (not a regular class) for consistency
- `add_all_to_model()` uses empty Key_Value (equivalent to `"*"`) to avoid `DuplicateObjectError` when multiple Output:Variable objects share the same key
- `pandas` added as optional dependency under `[project.optional-dependencies] dataframes`

**Files created**:
- `src/idfkit/simulation/parsers/rdd.py`
- `src/idfkit/simulation/outputs.py`
- `src/idfkit/simulation/parsers/sql.py`
- `src/idfkit/simulation/parsers/csv.py`
- `tests/test_simulation_rdd_parser.py`
- `tests/test_simulation_outputs.py`
- `tests/test_simulation_sql_parser.py`
- `tests/test_simulation_csv_parser.py`
- `tests/test_simulation_result.py`
- `tests/fixtures/simulation/sample.rdd`
- `tests/fixtures/simulation/sample.mdd`
- `tests/fixtures/simulation/sample.csv`

**Files modified**:
- `src/idfkit/simulation/result.py` — added `_cached_sql`, `_cached_variables`, `_cached_csv` fields and `.sql`, `.variables`, `.csv` lazy properties
- `src/idfkit/simulation/__init__.py` — added 9 new exports to `__all__`
- `pyproject.toml` — added `dataframes` optional dependency
- `uv.lock` — updated for new optional dependency

### Phase 3: Parallel Execution and Caching

**Scope**: Batch simulation, caching, and performance.

- `simulate_batch()` with `ProcessPoolExecutor`
- `SimulationJob` serializable data class
- Content-hash-based simulation caching
- Progress reporting (callback-based)
- Timeout handling and graceful cancellation

**New files**:
- `src/idfkit/sim/batch.py`
- `src/idfkit/sim/cache.py`
- `tests/test_sim_batch.py`
- `tests/test_sim_cache.py`

### Phase 4: File System Abstraction

**Scope**: Support non-local file systems for cloud workflows.

- `FileSystem` protocol
- `LocalFileSystem` implementation
- `S3FileSystem` implementation (optional boto3)
- Integration with `simulate()` and `SimulationResult.from_directory()`

**New files**:
- `src/idfkit/sim/fs/__init__.py`
- `src/idfkit/sim/fs/local.py`
- `src/idfkit/sim/fs/s3.py`
- `tests/test_sim_fs.py`

### Phase 5: Visualization

**Scope**: Pluggable plotting with common EnergyPlus visualizations.

- `PlotBackend` protocol
- matplotlib backend
- plotly backend
- Pre-built visualization functions (energy balance, temperature profiles, comfort heatmaps)
- Auto-detection of available backends

**New files**:
- `src/idfkit/sim/plotting/__init__.py`
- `src/idfkit/sim/plotting/matplotlib.py`
- `src/idfkit/sim/plotting/plotly.py`
- `tests/test_sim_plotting.py`

### Phase 6: Weather File and Design Day Browser ✅ COMPLETED

**Scope**: Searchable weather station index, EPW/DDY download, design day injection.

- ✅ `WeatherStation` frozen dataclass with `display_name`, `dataset_variant`, `to_dict()`/`from_dict()` serialization
- ✅ `StationIndex` with fuzzy text search, lat/lon proximity search, `filter()`, `get_by_wmo()`, and `countries` property
- ✅ `StationIndex.load()` — instant, loads bundled gzip JSON index (55k stations, ~930KB), no network or openpyxl needed
- ✅ `StationIndex.check_for_updates()` — HEAD requests to compare `Last-Modified` headers against stored values
- ✅ `StationIndex.refresh()` — re-downloads Excel indexes, rebuilds and caches compressed index (requires openpyxl)
- ✅ `geocode()` via Nominatim (free, no API key, 1 req/sec rate limit); raises `GeocodingError` on failure (always returns `tuple[float, float]`)
- ✅ Haversine distance (`haversine_km()`) with bounding-box pre-filter in `nearest()`
- ✅ `WeatherDownloader` with platform-appropriate cache directory and ZIP extraction
- ✅ `DesignDayManager` with DDY parsing via `load_idf()`, 20 annual `DesignDayType` enum values (heating, cooling DB/WB/enthalpy, dehumidification, humidification, heating wind, coldest-month wind), plus `monthly` property for 96 monthly design days
- ✅ `apply_ashrae_sizing()` convenience function with ASHRAE 90.1 and general presets
- ✅ `apply_to_model()` with `include_enthalpy` and `include_wind` parameters
- ✅ Build script (`scripts/build_weather_index.py`) and `make weather-index` target for regenerating the bundled index
- ✅ Getting started notebook updated with weather module examples (Part 4)
- ✅ Unit tests with fixture station data, mock DDY files, and mocked network calls

**Deviations from original plan**:
- Bundled index uses gzip-compressed JSON (`stations.json.gz`, ~930KB) instead of `stations.csv.gz` (~300KB) — JSON allows storing `Last-Modified` metadata for staleness checking
- `openpyxl` only needed for `StationIndex.refresh()`, not for `StationIndex.load()` (bundled index is self-contained)
- `geocode()` raises `GeocodingError` instead of returning `None` — enables `index.nearest(*geocode(address))` splat pattern
- `nearest_to_address()` is implemented as composable `geocode()` + `nearest()` rather than a single method on `StationIndex`
- `NoDesignDaysError` deferred — empty DDY files return an empty `all_design_days` list
- Download module named `download.py` (not `downloader.py`)

**Files created**:
- `src/idfkit/weather/__init__.py`
- `src/idfkit/weather/station.py`
- `src/idfkit/weather/index.py`
- `src/idfkit/weather/download.py`
- `src/idfkit/weather/designday.py`
- `src/idfkit/weather/geocode.py`
- `src/idfkit/weather/spatial.py`
- `src/idfkit/weather/data/stations.json.gz` — bundled pre-compiled index (55,120 stations)
- `scripts/build_weather_index.py` — maintainer build script for regenerating the bundled index
- `tests/test_weather_station.py`
- `tests/test_weather_spatial.py`
- `tests/test_weather_index.py`
- `tests/test_weather_geocode.py`
- `tests/test_weather_download.py`
- `tests/test_weather_designday.py`
- `tests/fixtures/weather/sample.ddy`
- `tests/fixtures/weather/empty.ddy`

---

## 12. End-to-End Usage Example

```python
from idfkit import load_idf
from idfkit.sim import simulate, find_energyplus, OutputVariableIndex
from idfkit.weather import StationIndex, apply_ashrae_sizing, WeatherDownloader

# Load model and find EnergyPlus
model = load_idf("office.idf")
eplus = find_energyplus()  # auto-discovers installation

# Step 1: Find the right weather station
index = StationIndex.load()
results = index.nearest_to_address("350 Fifth Avenue, New York, NY")
station = results[0].station
print(f"Using: {station.display_name} ({station.distance_km:.0f} km)")

# Step 2: Download weather files and apply design days
downloader = WeatherDownloader()
weather = downloader.download(station)
apply_ashrae_sizing(model, station, standard="90.1")

# Step 3: Discovery run to find available outputs
discovery = simulate(model, weather.epw, design_day=True, energyplus=eplus)
var_index = OutputVariableIndex.from_simulation(discovery)

# Step 4: Search and add outputs
for var in var_index.search("Temperature"):
    print(f"  {var.name} [{var.units}]")

model.add("Output:Variable", Key_Value="*",
          Variable_Name="Zone Mean Air Temperature",
          Reporting_Frequency="Hourly")
model.add("Output:Meter", Key_Name="Electricity:Facility",
          Reporting_Frequency="Monthly")

# Step 5: Full simulation
result = simulate(model, weather.epw, annual=True, energyplus=eplus)

# Step 6: Check for errors
if result.errors.has_fatal:
    for err in result.errors.fatal:
        print(f"FATAL: {err}")
    raise SystemExit(1)

print(f"Warnings: {len(result.errors.warnings)}")

# Step 7: Query results
ts = result.sql.get_timeseries("Zone Mean Air Temperature", "THERMAL ZONE 1")
print(f"Min: {min(ts.values):.1f} {ts.units}")
print(f"Max: {max(ts.values):.1f} {ts.units}")

# Step 8: Plot (if matplotlib/plotly available)
ts.plot()

# Step 9: Export to DataFrame (if pandas available)
df = ts.to_dataframe()
df.to_csv("zone_temperatures.csv")
```

### Batch Simulation Example

```python
from idfkit.sim import simulate_batch, SimulationJob

# Parametric study: vary infiltration rate
jobs = []
for rate in [0.1, 0.3, 0.5, 0.7, 1.0]:
    m = load_idf("office.idf")
    infiltration = m["ZoneInfiltration:DesignFlowRate"]["Office Infiltration"]
    infiltration.air_changes_per_hour = rate
    jobs.append(SimulationJob(
        model=m,
        weather="weather.epw",
        label=f"infiltration-{rate}",
    ))

results = simulate_batch(jobs, max_workers=4)

for job, result in zip(jobs, results):
    energy = result.sql.get_tabular_data(
        report_name="AnnualBuildingUtilityPerformanceSummary",
        table_name="End Uses",
    )
    print(f"{job.label}: {energy}")
```

---

## 13. Testing Strategy

### 13.1 Unit Tests (No EnergyPlus Required)

Most tests should run without an EnergyPlus installation:

- **Config discovery**: mock filesystem to test path scanning logic
- **RDD/MDD parsing**: use fixture files with known content
- **SQL parsing**: use a pre-built SQLite fixture file
- **ESO/CSV parsing**: use fixture files
- **Error parsing**: use fixture `.err` files
- **Simulation directory preparation**: verify file layout without running EnergyPlus
- **Caching**: verify hash computation and directory management
- **FileSystem protocol**: test LocalFileSystem against temp directories
- **Station index loading**: test CSV parsing, field types, and index construction
- **Fuzzy search**: test scoring against known station names, WMO numbers, partial matches
- **Spatial search**: test Haversine distance against known lat/lon pairs
- **DDY parsing**: test design day classification from fixture DDY files
- **Design day injection**: test `apply_to_model()` against a fixture IDF document
- **Geocoding**: mock Nominatim HTTP responses to test parsing without network calls

### 13.2 Integration Tests (EnergyPlus Required)

Marked with `@pytest.mark.integration` and skipped when EnergyPlus is not available:

```python
@pytest.fixture
def energyplus():
    """Skip test if EnergyPlus is not installed."""
    try:
        config = find_energyplus()
    except EnergyPlusNotFoundError:
        pytest.skip("EnergyPlus not installed")
    return config
```

Integration tests cover:
- End-to-end simulation with a minimal IDF
- Output file generation verification
- SQL query results
- Parallel simulation correctness

### 13.3 Test Fixtures

Pre-built fixture files checked into the repository:

```
tests/fixtures/sim/
├── sample.rdd            # Known RDD file for parsing tests
├── sample.mdd            # Known MDD file for parsing tests
├── sample.err            # Known error file (warnings + info)
├── sample_fatal.err      # Error file with fatal errors
├── sample.sql            # Pre-built SQLite output
├── sample.eso            # Known ESO file
├── sample.csv            # Known CSV output
└── minimal.idf           # Minimal valid IDF for integration tests

tests/fixtures/weather/
├── sample_stations.csv   # Small subset of station index for search tests
├── sample.ddy            # DDY file with all 14 design day types
├── empty.ddy             # DDY file with only Site:Location (no design days)
├── nominatim_response.json  # Mock Nominatim API response
└── sample.epw            # Minimal EPW file (header only, for metadata parsing)
```

---

## 14. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| EnergyPlus not installed | Users cannot simulate | Clear error messages with install instructions; discovery function returns `None` gracefully |
| EnergyPlus version mismatch | IDF written for v24.1, only v23.2 installed | Detect version mismatch and warn; optionally run version transition executables |
| Windows path length limits | Paths >260 chars fail | Use short temp directory names; document `LongPathsEnabled` registry key |
| SQLite file locking on network drives | Concurrent reads fail | Copy SQL file locally before querying |
| Large ESO files (>1GB) | Memory exhaustion | Stream-parse ESO files; prefer SQL output |
| Weather file not found | Simulation fails cryptically | Validate weather file existence before launching subprocess |
| EnergyPlus hangs (infinite loop) | Process never returns | `timeout` parameter on `subprocess.run`; default 1-hour timeout |
| climate.onebuilding.org unavailable | Cannot download weather files | Local cache survives outages; bundled station index works offline for search; clear error message |
| Nominatim rate limiting / downtime | Address geocoding fails | Graceful `None` return; users can fall back to manual lat/lon; 1 req/sec throttle prevents bans |
| DDY file has no design days | Cannot size HVAC equipment | `NoDesignDaysError` suggests nearby stations with design day data |
| Station index becomes stale | New stations or datasets missing | Quarterly regeneration; users can also pass custom station data |
| Bundled stations.csv.gz adds package size | ~300KB compressed added to wheel | Acceptable trade-off for offline search; smaller than a single EPW file |

---

## 15. Open Questions

1. **Should IDFkit bundle a minimal weather file for testing?** EPW files are ~1.5MB each. A
   design-day-only DDY file would be smaller but requires `ExpandObjects`.

2. **Should the SQL parser return raw tuples or typed dataclasses?** Dataclasses are safer but
   slower for large result sets. A hybrid approach (lazy parsing) may be best.

3. **Should `simulate()` be async-capable?** An `async def asimulate()` variant using
   `asyncio.create_subprocess_exec` would integrate well with web frameworks and async
   orchestrators. This could be added in a later phase.

4. **Should IDFkit provide EnergyPlus installation utilities?** `energy_plus_wrapper` has an
   `ensure_eplus_root` function that downloads and installs EnergyPlus on Linux. This is useful
   for CI/CD and Docker but adds significant complexity. Consider providing documentation and
   a helper script rather than embedding this in the library.

5. **Should version transition be automatic?** If the model version doesn't match the installed
   EnergyPlus version, should IDFkit automatically run the transition executables? This is
   convenient but potentially surprising. A warning + opt-in flag may be best.

6. **Should the station index include non-TMYx datasets?** climate.onebuilding.org also hosts
   TMY3 (USA), CWEC (Canada), CSWD (China), ISHRAE (India), and other country-specific datasets.
   Including them would expand coverage but increase index size and complicate the dataset
   selection UI. A phased approach (TMYx first, others later) may be best.

7. **Should IDFkit parse EPW hourly data?** Packages like opyplus parse full EPW files into
   DataFrames. IDFkit could offer this as a convenience, but it overlaps with dedicated packages
   like `pvlib` and `ladybug`. Parsing only the EPW header (location, design conditions) is
   likely sufficient for the weather browser use case.

8. **Should the weather cache have a size limit or TTL?** If a user downloads weather files for
   many stations, the cache could grow large. A configurable maximum size with LRU eviction would
   prevent unbounded growth, but adds complexity. Given that each ZIP is ~2-5MB and most users
   work with a handful of stations, an unbounded cache with manual `clear_cache()` may suffice.

9. **Should `nearest_to_address()` support batch geocoding?** For parametric studies across
   many building sites, batch geocoding would be useful. However, Nominatim's 1 req/sec limit
   makes this slow. A bulk CSV import of pre-geocoded sites (lat/lon columns) would be more
   practical for batch workflows.
