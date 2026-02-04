# EnergyPlus Simulation Plan for IDFkit

## Executive Summary

IDFkit currently excels at parsing, manipulating, and writing EnergyPlus IDF/epJSON files with
O(1) lookups and minimal memory overhead. This plan proposes extending IDFkit with first-class
simulation execution, output variable discovery, result retrieval, and visualization -- while
avoiding the pitfalls that plague existing packages (eppy, honeybee-energy, opyplus, etc.).

The design prioritizes:

1. **No admin rights required** -- works with user-level EnergyPlus installations
2. **Cloud-native** -- isolated simulation directories, abstract file systems, stateless execution
3. **Parallel-safe** -- no shared mutable state, no singletons, no in-process EnergyPlus coupling
4. **Pluggable** -- file system backends, plotting backends, and result formats are all swappable
5. **Minimal dependencies** -- core simulation requires only the standard library; extras unlock
   pandas, plotting, and cloud storage

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
                                      │
                            ┌─────────┴──────────┐
                            │  idfkit.sim.fs      │
                            │  (file system       │
                            │   abstraction)      │
                            └─────────────────────┘
                             LocalFS / S3FS / ...
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

## 9. Dependency Strategy

### 9.1 Core (Zero Extra Dependencies)

The `idfkit.sim` core module should work with **only the standard library**:

- `subprocess` for execution
- `sqlite3` for SQL output parsing
- `json` for serialization
- `tempfile` for isolated directories
- `pathlib` for path handling
- `re` for RDD/MDD parsing
- `datetime` for timestamps
- `hashlib` for simulation caching

### 9.2 Optional Extras

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

### 9.3 Lazy Imports

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

## 10. Implementation Phases

### Phase 1: Core Simulation (Foundation)

**Scope**: Discover EnergyPlus, run simulations, parse errors, return structured results.

- `EnergyPlusConfig` with full discovery chain
- `simulate()` function with subprocess execution
- `SimulationResult` with lazy-loaded error parsing
- Automatic `Output:SQLite` injection
- Simulation directory isolation
- Basic `.err` file parsing
- Unit tests with mocked EnergyPlus (test file structure, not actual simulation)

**New files**:
- `src/idfkit/sim/__init__.py`
- `src/idfkit/sim/config.py`
- `src/idfkit/sim/runner.py`
- `src/idfkit/sim/result.py`
- `src/idfkit/sim/parsers/err.py`
- `tests/test_sim_config.py`
- `tests/test_sim_runner.py`

### Phase 2: Output Parsing and Variable Discovery

**Scope**: Parse simulation outputs, discover available variables, add them to models.

- SQL output parser (using `sqlite3`)
- RDD/MDD parser and `OutputVariableIndex`
- `TimeSeriesResult` data class
- ESO parser (as fallback when SQL is unavailable)
- CSV parser (for ReadVarsESO output)
- HTML table parser
- `to_dataframe()` methods (optional pandas)

**New files**:
- `src/idfkit/sim/outputs.py`
- `src/idfkit/sim/parsers/__init__.py`
- `src/idfkit/sim/parsers/sql.py`
- `src/idfkit/sim/parsers/eso.py`
- `src/idfkit/sim/parsers/csv.py`
- `src/idfkit/sim/parsers/html.py`
- `src/idfkit/sim/parsers/eio.py`
- `tests/test_sim_outputs.py`
- `tests/test_sim_parsers.py`

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

---

## 11. End-to-End Usage Example

```python
from idfkit import load_idf
from idfkit.sim import simulate, find_energyplus, OutputVariableIndex

# Load and configure
model = load_idf("office.idf")
eplus = find_energyplus()  # auto-discovers installation

# Step 1: Discovery run to find available outputs
discovery = simulate(model, "weather.epw", design_day=True, energyplus=eplus)
index = OutputVariableIndex.from_simulation(discovery)

# Step 2: Search and add outputs
for var in index.search("Temperature"):
    print(f"  {var.name} [{var.units}]")

model.add("Output:Variable", Key_Value="*",
          Variable_Name="Zone Mean Air Temperature",
          Reporting_Frequency="Hourly")
model.add("Output:Meter", Key_Name="Electricity:Facility",
          Reporting_Frequency="Monthly")

# Step 3: Full simulation
result = simulate(model, "weather.epw", annual=True, energyplus=eplus)

# Step 4: Check for errors
if result.errors.has_fatal:
    for err in result.errors.fatal:
        print(f"FATAL: {err}")
    raise SystemExit(1)

print(f"Warnings: {len(result.errors.warnings)}")

# Step 5: Query results
ts = result.sql.get_timeseries("Zone Mean Air Temperature", "THERMAL ZONE 1")
print(f"Min: {min(ts.values):.1f} {ts.units}")
print(f"Max: {max(ts.values):.1f} {ts.units}")

# Step 6: Plot (if matplotlib/plotly available)
ts.plot()

# Step 7: Export to DataFrame (if pandas available)
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

## 12. Testing Strategy

### 12.1 Unit Tests (No EnergyPlus Required)

Most tests should run without an EnergyPlus installation:

- **Config discovery**: mock filesystem to test path scanning logic
- **RDD/MDD parsing**: use fixture files with known content
- **SQL parsing**: use a pre-built SQLite fixture file
- **ESO/CSV parsing**: use fixture files
- **Error parsing**: use fixture `.err` files
- **Simulation directory preparation**: verify file layout without running EnergyPlus
- **Caching**: verify hash computation and directory management
- **FileSystem protocol**: test LocalFileSystem against temp directories

### 12.2 Integration Tests (EnergyPlus Required)

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

### 12.3 Test Fixtures

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
```

---

## 13. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| EnergyPlus not installed | Users cannot simulate | Clear error messages with install instructions; discovery function returns `None` gracefully |
| EnergyPlus version mismatch | IDF written for v24.1, only v23.2 installed | Detect version mismatch and warn; optionally run version transition executables |
| Windows path length limits | Paths >260 chars fail | Use short temp directory names; document `LongPathsEnabled` registry key |
| SQLite file locking on network drives | Concurrent reads fail | Copy SQL file locally before querying |
| Large ESO files (>1GB) | Memory exhaustion | Stream-parse ESO files; prefer SQL output |
| Weather file not found | Simulation fails cryptically | Validate weather file existence before launching subprocess |
| EnergyPlus hangs (infinite loop) | Process never returns | `timeout` parameter on `subprocess.run`; default 1-hour timeout |

---

## 14. Open Questions

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
