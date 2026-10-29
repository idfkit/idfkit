# Threads and free-threaded Python

idfkit is pure Python with no C extensions, and it is tested on free-threaded CPython (`python3.14t`, run with the GIL disabled). This reference states what is safe to share between threads, and when threads actually buy parallelism.

## When to use

- You want to load, validate, or write many models at once on a thread pool.
- You share one document between threads (a web server, a GUI, a worker pool) and need to know the rules.
- You're deciding between threads and processes for CPU-bound idfkit work.

## The contract

| Shared between threads | Safe? |
|---|---|
| The schema manager, `get_schema(...)`, and the schema it returns | Yes. A version requested by many threads at once loads once, and every thread gets the same instance. |
| Separate documents, one per thread | Yes. They share nothing but the read-only schema. |
| One document, only read (attribute reads, `write_idf`, `validate_document`, `doc.copy()`, `get_referencing`, schedule evaluation) | Yes, as long as no thread mutates it at the same time. |
| One document, mutated (`add`, `removeidfobject`, `rename`, field assignment) by several threads, or by one while others read | **No.** Nothing raises; the model silently ends up inconsistent (lost objects, dangling references, a reference graph out of step with the fields). Give each thread a `doc.copy()`, or guard every access with your own lock. |
| `simulate_batch` / `async_simulate_batch` | Yes. Each job copies its model before changing anything, and the simulation cache commits each entry with an atomic rename. |

## Separate documents in parallel

```python
# Separate documents are independent: load, validate and write them on any number of threads.
# On a free-threaded build (python3.14t) this runs in parallel; on a GIL build it only interleaves.
with ThreadPoolExecutor() as pool:
    docs = list(pool.map(load_idf, paths))
    results = list(pool.map(validate_document, docs))
```

## Reading one document from many threads

```python
# One document may be READ from many threads at once, as long as nothing mutates it meanwhile.
with ThreadPoolExecutor() as pool:
    texts = list(pool.map(lambda _: write_idf(doc), range(8)))
```

## Changing a shared model

Copy per thread:

```python
# To change a shared model on several threads, give each thread its own copy.
def make_variant(thickness: float) -> IDFDocument:
    variant = doc.copy()
    variant["Material"]["Insulation"].thickness = thickness
    return variant


with ThreadPoolExecutor() as pool:
    variants = list(pool.map(make_variant, [0.05, 0.10, 0.15]))
```

Or lock:

```python
# Or serialise every access to the one document behind a lock you own.
doc_lock = threading.Lock()


def add_zone(name: str) -> None:
    with doc_lock:
        doc.add("Zone", name)


with ThreadPoolExecutor() as pool:
    list(pool.map(add_zone, ["North", "South", "East", "West"]))
```

## Do threads make it faster?

Only on a free-threaded build with the GIL off. On a regular build, CPU-bound idfkit work on a thread pool runs no faster than one thread, and usually 5–20% slower. Measured with `benchmarks/bench_free_threading.py` on 4 CPUs, 16 independent jobs per batch, compared with one thread on regular CPython 3.14:

| Workload | 1 thread on 3.14t | 4 threads on 3.14t |
|---|---|---|
| `load_idf` | 0.86x | 2.6x |
| `write_idf` (with a `doc.copy()`) | 0.84x | 1.6x |
| ESO parse (`eager=True`) | 1.1x | 1.5x |
| geometry (with a `doc.copy()`) | 0.72x | 1.4x |
| schedule evaluation (with a `doc.copy()`) | 0.77x | 1.4x |
| `validate_document` (with a `doc.copy()`) | 0.72x | 1.0x |

Two things follow. The free-threaded build costs 15–40% on a single thread, so it only pays at two or more busy threads. And most workloads scale well short of linearly, because every thread reads the same schema-derived tables, and on 3.14 concurrent reads of a shared object contend on its reference count. Parsing scales best.

For CPU-bound batch work on a regular build, use processes. Documents pickle cheaply, because the schema travels by version, not by content:

```python
# On a GIL build, CPU-bound work parallelises across processes instead. Documents pickle, and the
# schema travels by version, so handing one to a worker is cheap.
with ProcessPoolExecutor() as pool:
    docs = list(pool.map(load_idf, paths))
```

## Optional extras on free-threaded builds

The core package has no dependencies, so importing it never re-enables the GIL. Of the extras, `pandas` before 3.0 does: its compiled modules do not declare free-threading support, so the interpreter turns the GIL back on at import time and warns. `pandas>=3.0`, `numpy`, `matplotlib`, `plotly`, `boto3`, `aiobotocore`, `tqdm` and `openpyxl` keep it off.
