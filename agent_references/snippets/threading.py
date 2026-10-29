from __future__ import annotations

import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from idfkit import IDFDocument, ValidationResult, load_idf, validate_document, write_idf

doc: IDFDocument = ...  # type: ignore[assignment]
paths: list[str] = ...  # type: ignore[assignment]
docs: list[IDFDocument] = ...  # type: ignore[assignment]
texts: list[str] = ...  # type: ignore[assignment]
results: list[ValidationResult] = ...  # type: ignore[assignment]
variants: list[IDFDocument] = ...  # type: ignore[assignment]

# --8<-- [start:parallel-load]
# Separate documents are independent: load, validate and write them on any number of threads.
# On a free-threaded build (python3.14t) this runs in parallel; on a GIL build it only interleaves.
with ThreadPoolExecutor() as pool:
    docs = list(pool.map(load_idf, paths))
    results = list(pool.map(validate_document, docs))
# --8<-- [end:parallel-load]


# --8<-- [start:shared-read]
# One document may be READ from many threads at once, as long as nothing mutates it meanwhile.
with ThreadPoolExecutor() as pool:
    texts = list(pool.map(lambda _: write_idf(doc), range(8)))
# --8<-- [end:shared-read]


# --8<-- [start:copy-per-thread]
# To change a shared model on several threads, give each thread its own copy.
def make_variant(thickness: float) -> IDFDocument:
    variant = doc.copy()
    variant["Material"]["Insulation"].thickness = thickness
    return variant


with ThreadPoolExecutor() as pool:
    variants = list(pool.map(make_variant, [0.05, 0.10, 0.15]))
# --8<-- [end:copy-per-thread]


# --8<-- [start:lock]
# Or serialise every access to the one document behind a lock you own.
doc_lock = threading.Lock()


def add_zone(name: str) -> None:
    with doc_lock:
        doc.add("Zone", name)


with ThreadPoolExecutor() as pool:
    list(pool.map(add_zone, ["North", "South", "East", "West"]))
# --8<-- [end:lock]


# --8<-- [start:processes]
# On a GIL build, CPU-bound work parallelises across processes instead. Documents pickle, and the
# schema travels by version, so handing one to a worker is cheap.
with ProcessPoolExecutor() as pool:
    docs = list(pool.map(load_idf, paths))
# --8<-- [end:processes]
