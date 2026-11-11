"""Publish a file in one step, so no reader ever sees it half written.

A cache file written in place can be read by another thread or process while the write is still
running, and a reader that finds it truncated may keep it for good. Writing to a temporary file in
the same directory and renaming it over the target makes the new content appear all at once: a
reader opens either the old file or the complete new one.
"""

from __future__ import annotations

import contextlib
import os
import tempfile
import time
from pathlib import Path

# Windows refuses to replace a file another process holds open. Retried briefly, then the copy
# already in place is kept: it was itself published whole.
_REPLACE_ATTEMPTS = 5
_REPLACE_BACKOFF_SECONDS = 0.05


def write_bytes_atomically(target: Path, data: bytes) -> None:
    """Write *data* to *target* through a temporary file renamed into place.

    The temporary file ends in ``.part`` and starts with a dot, so a directory scan for the
    target's suffix never picks it up. It is removed if anything fails before the rename.

    Raises:
        OSError: If the data cannot be written, or *target* cannot be replaced and does not exist.
    """
    fd, tmp_name = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.", suffix=".part")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        _replace(tmp, target)
    finally:
        with contextlib.suppress(FileNotFoundError):
            tmp.unlink()


def _replace(tmp: Path, target: Path) -> None:
    """Rename *tmp* over *target*, tolerating a target held open by another process on Windows."""
    for attempt in range(_REPLACE_ATTEMPTS):
        try:
            os.replace(tmp, target)
        except PermissionError:
            if attempt + 1 < _REPLACE_ATTEMPTS:
                time.sleep(_REPLACE_BACKOFF_SECONDS)
                continue
            if not target.exists():
                raise
            # Another process is reading a complete copy; keep it rather than fail the caller.
            return
        else:
            return
