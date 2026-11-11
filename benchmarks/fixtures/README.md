# Benchmark fixtures

## `HospitalLowEnergy.idf.gz`

The reference model for the performance budget gate (`tests/test_perf_budgets.py`, research R-21 of
the model knowledge graph feature): the largest EnergyPlus example file, 6,876 objects.

- **Source:** `ExampleFiles/HospitalLowEnergy.idf` of the EnergyPlus **26.1.0** installation,
  unmodified (`Version,26.1;`).
- **SHA-256 of the uncompressed file:** `28fd9e0be08c1145ff71fddab259d614c7460eb79dbdeeef16581a42896737a2`.
- **Compressed with:** `gzip -9 -n`, so the archive carries no name or timestamp and is reproducible.

It is stored compressed (about 260 KB against 4.6 MB) because only the benchmarks read it.
`benchmarks/_timing.py` decompresses it to a temporary file before timing, since `idfkit.load_idf`
reads from a path.

**To replace:** the plan names the EnergyPlus 26.2 example file. No 26.2 installation was at hand
when this was vendored. Replace it with `ExampleFiles/HospitalLowEnergy.idf` from EnergyPlus 26.2.0
when available, update the version and checksum above, and re-check the baselines stated in
`tests/test_perf_budgets.py`.
