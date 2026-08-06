from __future__ import annotations

from idfkit.simulation import S3FileSystem

# --8<-- [start:example]
fs = S3FileSystem(
    bucket="local-bucket",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)
# --8<-- [end:example]
