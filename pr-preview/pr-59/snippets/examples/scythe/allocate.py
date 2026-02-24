from __future__ import annotations

# --8<-- [start:example]
import itertools

import boto3
import pandas as pd
from scythe.base import BaseExperiment
from scythe.utils.recursion import RecursionMap

# Assume these are defined in your experiments module
from experiments.building_energy import BuildingSimInput, simulate_building

# Define parameter grid
r_values = [2.0, 3.5, 5.0, 7.0]
lpds = [5.0, 8.0, 12.0]
setpoints = [22.0, 24.0, 26.0]
economizers = ["NoEconomizer", "DifferentialDryBulb"]

# Build a DataFrame of all combinations
combos = list(itertools.product(r_values, lpds, setpoints, economizers))
df = pd.DataFrame(combos, columns=["r_value", "lpd", "setpoint", "economizer"])

# Add file references (same base model + weather for all runs)
df["idf_file"] = "s3://my-bucket/models/office_base.idf"
df["weather_file"] = "s3://my-bucket/weather/USA_MA_Boston-Logan.epw"
df["design_day_file"] = "s3://my-bucket/weather/USA_MA_Boston-Logan.ddy"

# Validate and allocate
specs = [BuildingSimInput.model_validate(row.to_dict()) for _, row in df.iterrows()]

experiment = BaseExperiment(experiment=simulate_building)
experiment.allocate(
    specs,
    version="bumpminor",
    s3_client=boto3.client("s3"),
    recursion_map=RecursionMap(factor=2, max_depth=3),
)
# --8<-- [end:example]
