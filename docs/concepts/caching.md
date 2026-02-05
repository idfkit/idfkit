# Caching Strategy

idfkit uses content-addressed caching to avoid redundant work across
both simulation and weather operations.

## Content-Addressed Caching

Cache keys are computed from the **content** of inputs, not filenames or
timestamps. This means:

- Same inputs → same cache key → cache hit
- Different inputs → different cache key → fresh computation
- Moving or renaming files doesn't affect caching

## Simulation Cache

The `SimulationCache` stores complete simulation results keyed by a SHA-256
digest of:

1. **Normalised IDF content** — Model with `Output:SQLite` ensured
2. **Weather file bytes** — Complete weather file content
3. **Simulation flags** — `annual`, `design_day`, `expand_objects`, etc.

```python
from idfkit.simulation import simulate, SimulationCache

cache = SimulationCache()

# First run: executes EnergyPlus
result1 = simulate(model, weather, cache=cache)

# Second run: instant cache hit
result2 = simulate(model, weather, cache=cache)
```

### How It Works

1. Before simulation, compute the cache key
2. Check if a cached result exists
3. If hit: return the cached `SimulationResult` immediately
4. If miss: run EnergyPlus, cache the result, return

### What Gets Cached

The entire simulation **run directory** is copied into the cache:

- SQLite output database
- Error report
- RDD/MDD variable files
- All other output files

This means cached results have full access to all output data, identical
to a fresh run.

### Cache Location

The cache uses platform-appropriate directories:

| Platform | Default Location |
|----------|------------------|
| Linux | `~/.cache/idfkit/simulation/` |
| macOS | `~/Library/Caches/idfkit/simulation/` |
| Windows | `%LOCALAPPDATA%\idfkit\cache\simulation\` |

Override with a custom path:

```python
cache = SimulationCache(cache_dir=Path("/path/to/cache"))
```

### Cache Management

```python
# Check if a result would hit cache
key = cache.compute_key(model, weather, design_day=True)
if cache.contains(key):
    print("Would be a cache hit")

# Clear all cached results
cache.clear()
```

## Weather Cache

Weather data uses a simpler file-based cache:

| Data Type | Cache Behavior |
|-----------|----------------|
| Station indexes | Cached until explicit refresh |
| EPW/DDY files | Cached permanently by URL hash |

### Station Index Cache

The pre-compiled station index is bundled with the package. When you call
`StationIndex.refresh()`, updated indexes are cached locally:

```
~/.cache/idfkit/weather/indexes/
├── africa.parquet
├── americas.parquet
├── asia.parquet
└── ...
```

### Weather File Cache

Downloaded weather files are cached by URL:

```
~/.cache/idfkit/weather/files/
├── abc123def456.epw
├── abc123def456.ddy
└── ...
```

Files are never automatically deleted. Manual cleanup:

```python
import shutil
from idfkit.weather.download import default_cache_dir

shutil.rmtree(default_cache_dir())
```

## Cache Invalidation

Content-addressed caching means **automatic invalidation**:

- Change the model → different key → fresh simulation
- Change the weather file → different key → fresh simulation
- Same inputs → same key → cache hit

No manual cache invalidation is needed in normal workflows.

## Parallel Safety

Both caches are **thread-safe** and **process-safe**:

- Atomic writes using temporary directories + rename
- Safe for concurrent `simulate_batch()` with shared cache
- Multiple processes can share the same cache directory

```python
from idfkit.simulation import simulate_batch, SimulationCache

cache = SimulationCache()

# Safe: all workers share the cache
batch = simulate_batch(jobs, max_workers=8, cache=cache)
```

## Memory vs Disk

idfkit uses **disk-based caching** rather than in-memory caching because:

- Simulation results are often large (SQLite databases)
- Cache persists across Python sessions
- Multiple processes can share the cache
- Memory isn't exhausted by large batch runs

## Disabling Caching

Pass `cache=None` (the default) to skip caching:

```python
# No caching — always runs EnergyPlus
result = simulate(model, weather)

# With caching
cache = SimulationCache()
result = simulate(model, weather, cache=cache)
```

## See Also

- [Simulation Caching](../simulation/caching.md) — Practical guide
- [Weather Downloads](../weather/downloads.md) — Weather file caching
- [Simulation Architecture](simulation-architecture.md) — Design decisions
