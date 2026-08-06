from __future__ import annotations

from pathlib import Path
from typing import Any

data: Any = ...  # type: ignore[assignment]


# --8<-- [start:example]
class AzureBlobFileSystem:
    """Azure Blob Storage backend."""

    def __init__(self, container: str, connection_string: str):
        from azure.storage.blob import ContainerClient

        self._client = ContainerClient.from_connection_string(connection_string, container)

    def read_bytes(self, path: str | Path) -> bytes:
        blob = self._client.get_blob_client(str(path))
        return blob.download_blob().readall()

    def write_bytes(self, path: str | Path, data: bytes) -> None:
        blob = self._client.get_blob_client(str(path))
        blob.upload_blob(data, overwrite=True)

    # ... implement remaining methods


# --8<-- [end:example]
