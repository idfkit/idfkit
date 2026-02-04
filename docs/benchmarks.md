# Benchmarks

idfkit is benchmarked against
[eppy](https://github.com/santoshphilip/eppy),
[opyplus](https://github.com/openergy/opyplus), and
[energyplus-idd-idf-utilities](https://github.com/Myoldmopar/py-idd-idf) on a
**1,700-object IDF file** (500 zones, 100 materials, 100 constructions, 1,000
surfaces) using EnergyPlus V9.3 -- the newest version natively supported by all
four tools.

Each operation was run 10 times (100 for sub-millisecond ops) and the minimum
time is reported. Bars are sorted fastest to slowest.

## Load IDF file

![Load IDF file](assets/benchmark_load_idf.png)

## Get all objects by type

![Get all objects by type](assets/benchmark_get_by_type.png)

## Get single object by name

![Get single object by name](assets/benchmark_get_by_name.png)

## Add 100 objects

![Add 100 objects](assets/benchmark_add_objects.png)

## Modify fields (all zones)

![Modify fields](assets/benchmark_modify_fields.png)

## Write IDF to string

![Write IDF to string](assets/benchmark_write_idf.png)

## Supported EnergyPlus versions

| Tool | Versions | Schema format |
|---|---|---|
| **idfkit** | 8.9 -- 25.2 | epJSON schema (bundled, gzip-compressed) |
| **eppy** | 1.1 -- 9.2 (bundled IDD); any version with external IDD | IDD file |
| **opyplus** | 8.0 -- 9.6, 22.1 -- 24.1 | IDD file (bundled) |
| **idd-idf-utilities** | any version up to ~23.2 (IDD parser breaks on 24.1+) | IDD file (external) |

## Methodology

Benchmarks are run with `gc.collect()` before each iteration and `gc.disable()`
during timing to avoid GC pauses. The test IDF is generated programmatically
with realistic object types (zones, materials, constructions, surfaces).

To reproduce:

```bash
uv run --group benchmark python benchmarks/bench.py
```
