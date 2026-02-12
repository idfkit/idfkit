from __future__ import annotations

from idfkit.simulation import S3FileSystem

# --8<-- [start:example]
# MinIO
fs = S3FileSystem(
    bucket="local-bucket",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

# LocalStack
fs = S3FileSystem(
    bucket="test-bucket",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
)
# --8<-- [end:example]
