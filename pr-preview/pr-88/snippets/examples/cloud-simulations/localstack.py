from __future__ import annotations

from idfkit.simulation import S3FileSystem

# --8<-- [start:example]
fs = S3FileSystem(
    bucket="test-bucket",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
)
# --8<-- [end:example]
