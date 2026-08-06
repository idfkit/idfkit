# How to cache simulation results

The `SimulationCache` provides content-addressed caching to avoid redundant
simulations: identical inputs return a stored result instead of re-running
EnergyPlus. For how the cache key is computed, what gets stored, and why
invalidation is automatic, see
[Caching strategy](../concepts/caching.md).

## Basic Usage

```python
--8<-- "docs/snippets/simulation/caching/basic_usage.py:example"
```

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

Share a cache across batch simulations. The cache is thread- and process-safe
(atomic writes via a temp directory and rename), so a shared cache is safe for
concurrent `simulate_batch()` runs and across multiple processes:

```python
--8<-- "docs/snippets/simulation/caching/batch_processing.py:example"
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
