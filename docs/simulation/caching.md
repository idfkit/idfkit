# Simulation Caching

The `SimulationCache` provides content-addressed caching to avoid redundant
simulations. Cache keys are computed from model content, weather data, and
simulation flags.

## Basic Usage

```python
from idfkit.simulation import simulate, SimulationCache

cache = SimulationCache()

# First run: executes EnergyPlus
result1 = simulate(model, "weather.epw", cache=cache)
print(f"Runtime: {result1.runtime_seconds:.1f}s")

# Second run: instant cache hit
result2 = simulate(model, "weather.epw", cache=cache)
print(f"Runtime: {result2.runtime_seconds:.1f}s")  # Near zero
```

## How It Works

### Cache Key Computation

The cache key is a SHA-256 digest of:

1. **Normalized IDF content** — Model text with `Output:SQLite` ensured
2. **Weather file bytes** — Complete weather file content
3. **Simulation flags** — `annual`, `design_day`, `expand_objects`, etc.

```python
key = cache.compute_key(
    model,
    "weather.epw",
    design_day=True,
    annual=False,
)
print(f"Cache key: {key.hex_digest[:16]}...")
```

### What Gets Cached

The **entire run directory** is copied into the cache:

- SQLite output database (`.sql`)
- Error report (`.err`)
- Variable files (`.rdd`, `.mdd`)
- All other output files

Cached results have full access to all outputs, identical to a fresh run.

## Cache Location

Default locations by platform:

| Platform | Default Path |
|----------|--------------|
| Linux | `~/.cache/idfkit/simulation/` |
| macOS | `~/Library/Caches/idfkit/simulation/` |
| Windows | `%LOCALAPPDATA%\idfkit\cache\simulation\` |

### Custom Location

```python
from pathlib import Path

cache = SimulationCache(cache_dir=Path("/data/sim_cache"))
```

## Cache Operations

### Check for Hit

```python
key = cache.compute_key(model, weather, design_day=True)

if cache.contains(key):
    print("Would be a cache hit")
else:
    print("Would be a cache miss")
```

### Manual Get/Put

```python
# Compute key
key = cache.compute_key(model, weather)

# Check cache
cached_result = cache.get(key)
if cached_result is not None:
    print("Cache hit!")
else:
    # Run simulation
    result = simulate(model, weather)

    # Store in cache (only successful results)
    cache.put(key, result)
```

### Clear Cache

```python
# Remove all cached entries
cache.clear()
```

## Batch Processing

Share a cache across batch simulations:

```python
from idfkit.simulation import simulate_batch, SimulationJob, SimulationCache

cache = SimulationCache()

# All jobs share the same cache
batch1 = simulate_batch(jobs, cache=cache)

# Re-running unchanged jobs hits cache
batch2 = simulate_batch(jobs, cache=cache)  # Instant for unchanged
```

## Cache Invalidation

Content-addressed caching means **automatic invalidation**:

| Change | Effect |
|--------|--------|
| Modify model | Different key → fresh simulation |
| Change weather file | Different key → fresh simulation |
| Change flags | Different key → fresh simulation |
| Same inputs | Same key → cache hit |

No manual invalidation is needed.

## Cache Key Details

### Model Normalization

Before hashing, the model is:

1. Copied to avoid mutation
2. Has `Output:SQLite` added if missing
3. Written to IDF text format

This ensures models differing only in `Output:SQLite` produce the same key.

### Flag Influence

Flags that affect the cache key:

- `expand_objects`
- `annual`
- `design_day`
- `output_suffix`
- `extra_args`

Flags that don't affect the key:

- `output_dir` (just affects where results go)
- `timeout` (affects execution, not results)
- `readvars` (post-processing only)

## Thread and Process Safety

The cache is safe for concurrent access:

- **Atomic writes** — Uses temp directory + rename
- **Thread-safe** — Safe for `simulate_batch()` with shared cache
- **Process-safe** — Multiple Python processes can share the cache

```python
# Safe: concurrent access from multiple workers
batch = simulate_batch(jobs, max_workers=8, cache=cache)
```

## Storage Considerations

### Disk Space

Each cached entry is a full copy of the run directory. Monitor usage:

```bash
du -sh ~/.cache/idfkit/simulation/
```

### Cleanup

```python
# Clear everything
cache.clear()

# Or manually delete specific entries
import shutil
shutil.rmtree(cache.cache_dir / "abc123...")
```

## Disabling Caching

Pass `cache=None` (the default) to skip caching:

```python
# No caching
result = simulate(model, weather)

# With caching
result = simulate(model, weather, cache=SimulationCache())
```

## Best Practices

1. **Use for development** — Cache during iterative testing
2. **Clear for production** — Start fresh for final runs
3. **Share across batch** — Pass same cache to `simulate_batch()`
4. **Monitor disk usage** — Large studies can fill disk
5. **Custom location** — Use fast SSD for better performance

## See Also

- [Caching Strategy](../concepts/caching.md) — Design concepts
- [Running Simulations](running.md) — Basic simulation guide
- [Batch Processing](batch.md) — Parallel execution
