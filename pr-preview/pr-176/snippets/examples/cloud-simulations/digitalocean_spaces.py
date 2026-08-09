from __future__ import annotations

from idfkit.simulation import S3FileSystem

# --8<-- [start:example]
fs = S3FileSystem(
    bucket="my-space",
    endpoint_url="https://nyc3.digitaloceanspaces.com",
    region_name="nyc3",
)
# --8<-- [end:example]
