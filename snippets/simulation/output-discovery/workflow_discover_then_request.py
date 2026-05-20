from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.simulation import SimulationResult, TimeSeriesResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate

# Step 1: Discovery run
result = simulate(model, weather, design_day=True)

# Step 2: Find interesting outputs
matches = result.variables.search("Zone Mean Air Temperature")
print(f"Found {len(matches)} matching variables")

# Step 3: Add outputs to model
result.variables.add_all_to_model(
    model,
    filter_pattern="Zone Mean Air Temperature",
    reporting_frequency="Hourly",
)

# Step 4: Full run with outputs
result = simulate(model, weather, annual=True)

# Step 5: Query the data
for zone in ["ZONE 1", "ZONE 2"]:
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        zone,
    )
    print(f"{zone}: avg {sum(ts.values) / len(ts.values):.1f}°C")
# --8<-- [end:example]
