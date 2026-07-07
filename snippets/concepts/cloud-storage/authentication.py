from __future__ import annotations

from idfkit.simulation import S3FileSystem

# --8<-- [start:example]
# IAM role (recommended for cloud)
fs = S3FileSystem(bucket="my-bucket")

# Explicit credentials (for testing)
fs = S3FileSystem(
    bucket="my-bucket",
    aws_access_key_id="AKIA...",
    aws_secret_access_key="...",
)
# --8<-- [end:example]
