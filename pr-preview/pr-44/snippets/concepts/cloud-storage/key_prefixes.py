from __future__ import annotations

from idfkit.simulation import S3FileSystem

# --8<-- [start:example]
# All files stored under "project-x/batch-42/"
fs = S3FileSystem(
    bucket="simulations",
    prefix="project-x/batch-42/",
)

# output_dir="run-001" → s3://simulations/project-x/batch-42/run-001/
# --8<-- [end:example]
