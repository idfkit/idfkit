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

![Load IDF file](assets/benchmark_load_idf.svg#only-light)
![Load IDF file](assets/benchmark_load_idf_dark.svg#only-dark)

## Get all objects by type

![Get all objects by type](assets/benchmark_get_by_type.svg#only-light)
![Get all objects by type](assets/benchmark_get_by_type_dark.svg#only-dark)

## Get single object by name

![Get single object by name](assets/benchmark_get_by_name.svg#only-light)
![Get single object by name](assets/benchmark_get_by_name_dark.svg#only-dark)

## Add 100 objects

![Add 100 objects](assets/benchmark_add_objects.svg#only-light)
![Add 100 objects](assets/benchmark_add_objects_dark.svg#only-dark)

## Modify fields (all zones)

![Modify fields](assets/benchmark_modify_fields.svg#only-light)
![Modify fields](assets/benchmark_modify_fields_dark.svg#only-dark)

## Write IDF to string

![Write IDF to string](assets/benchmark_write_idf.svg#only-light)
![Write IDF to string](assets/benchmark_write_idf_dark.svg#only-dark)

## ESO reader

idfkit's `.eso`/`.mtr` reader is benchmarked against other EnergyPlus ESO
readers on a **104 MB annual file** (RefBldgLargeOffice, ~5.1 million data
points): [esoreader](https://github.com/architecture-building-systems/esoreader),
[opyplus](https://github.com/openergy/opyplus),
[pyeso](https://github.com/frantp/pyeso),
[db-eplusout-reader](https://github.com/DesignBuilderSoftware/db-eplusout-reader),
and EnergyPlus's native `ReadVarsESO`.

### Extract one variable

![Extract one variable](assets/benchmark_eso_single_variable.svg#only-light)
![Extract one variable](assets/benchmark_eso_single_variable_dark.svg#only-dark)

idfkit's reader is **lazy**: pulling one variable float-parses only that
variable's records, so it is the fastest *correct* way to read a few variables
from a large file. Every other reader parses the whole file first, even to
return a single series.

### Full parse

![Parse every variable](assets/benchmark_eso_full_parse.svg#only-light)
![Parse every variable](assets/benchmark_eso_full_parse_dark.svg#only-dark)

When you do want everything, idfkit's eager full parse (pure Python, ~1.7M
points/s) matches the fully-correct, pandas-based opyplus and beats the native
C++ `ReadVarsESO`. `esoreader` and `pyeso` are faster only because they skip
correctness — they concatenate design-day and run-period data into one series,
drop daily/monthly min/max, and (pyeso) return raw strings. idfkit is also more
robust: it reads reference-building files that crash `db-eplusout-reader` (a
weekday/holiday bug) and that `ReadVarsESO` truncates to its 255-variable cap.

To reproduce:

```bash
uv run --group benchmark python benchmarks/bench_eso.py --eso path/to/eplusout.eso
```

## Supported EnergyPlus versions

| Tool | Versions | Schema format |
|---|---|---|
| **idfkit** | 8.9 -- 26.1 | epJSON schema (bundled, gzip-compressed) |
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
