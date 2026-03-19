from __future__ import annotations

from idfkit.simulation import SimulationResult

result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Check stderr
print(result.stderr)

# Check the run directory
print(f"Outputs in: {result.run_dir}")
# --8<-- [end:example]
