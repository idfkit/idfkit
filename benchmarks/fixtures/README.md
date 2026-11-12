# Benchmark fixtures

## `HospitalLowEnergy.idf.gz`

The reference model for the performance budget gate (`tests/test_perf_budgets.py`, research R-21 of
the model knowledge graph feature): the largest EnergyPlus example file, 6,876 objects.

- **Source:** `ExampleFiles/HospitalLowEnergy.idf` of the EnergyPlus **26.2.0** installation,
  unmodified (`Version,26.2;`).
- **SHA-256 of the uncompressed file:** `f29fee09bddfe914d8f202c04883ac5197abe4c47c953c1e5f8b4d13c6dc1296`.
- **Compressed with:** `gzip -9 -n`, so the archive carries no name or timestamp and is reproducible.

It is stored compressed (about 260 KB against 4.6 MB) because only the benchmarks read it.
`benchmarks/_timing.py` decompresses it to a temporary file before timing, since `idfkit.load_idf`
reads from a path.
