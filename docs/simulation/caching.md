# How to cache simulation results

The `SimulationCache` provides content-addressed caching to avoid redundant
simulations. Cache keys are computed from model content, weather data, and
simulation flags.

## Basic Usage

```python
--8<-- "docs/snippets/simulation/caching/basic_usage.py:example"
```

## How It Works

### Cache Key Computation

The cache key is a SHA-256 digest of:

1. **Normalized IDF content** — Model text with `Output:SQLite` ensured
2. **Weather file bytes** — Complete weather file content
3. **Simulation flags** — `annual`, `design_day`, `expand_objects`, etc.

```python
--8<-- "docs/snippets/simulation/caching/cache_key_computation.py:example"
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
--8<-- "docs/snippets/simulation/caching/custom_location.py:example"
```

## Cache Operations

### Check for Hit

```python
--8<-- "docs/snippets/simulation/caching/check_for_hit.py:example"
```

### Manual Get/Put

```python
--8<-- "docs/snippets/simulation/caching/manual_getput.py:example"
```

### Clear Cache

```python
--8<-- "docs/snippets/simulation/caching/clear_cache.py:example"
```

## Batch Processing

Share a cache across batch simulations:

```python
--8<-- "docs/snippets/simulation/caching/batch_processing.py:example"
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
--8<-- "docs/snippets/simulation/caching/thread_and_process_safety.py:example"
```

## Storage Considerations

### Disk Space

Each cached entry is a full copy of the run directory. Monitor usage:

```bash
du -sh ~/.cache/idfkit/simulation/
```

### Cleanup

```python
--8<-- "docs/snippets/simulation/caching/cleanup.py:example"
```

## Disabling Caching

Pass `cache=None` (the default) to skip caching:

```python
--8<-- "docs/snippets/simulation/caching/disabling_caching.py:example"
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
