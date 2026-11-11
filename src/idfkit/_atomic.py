"""Publish a file in one step, so no reader ever sees it half written.

A cache file written in place can be read by another thread or process while the write is still
running, and a reader that finds it truncated may keep it for good. Writing to a temporary file in
the same directory and renaming it over the target makes the new content appear all at once: a
reader opens either the old file or the complete new one.

The published file looks like one written in place would: a new file gets the permission bits
``open(path, "wb")`` would give it (``0o666`` less the process umask, so a cache warmed by one user
stays readable by another), and an existing file keeps its own. A symlink is followed, so its target
is replaced and the link survives.
"""

from __future__ import annotations

import os
import secrets
import stat
import time
from pathlib import Path

_IS_WINDOWS = os.name == "nt"
# Windows refuses to rename over a file another process holds open (Python's own ``open`` does not
# grant FILE_SHARE_DELETE) or that a scanner is briefly holding. POSIX never refuses for those
# reasons, so a PermissionError there is permanent and is raised at once.
_REPLACE_ATTEMPTS = 5
_REPLACE_BACKOFF_SECONDS = 0.05
_OPEN_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0) | getattr(os, "O_CLOEXEC", 0)


def write_bytes_atomically(
    target: Path,
    data: bytes,
    *,
    mtime_ns: int | None = None,
    keep_existing_if_locked: bool = False,
) -> bool:
    """Write *data* to *target* through a temporary file renamed into place.

    The temporary file is created next to the target under a short, dot-prefixed name ending in
    ``.part``, so a directory scan for the target's suffix never picks it up and a long target path
    gets no longer. It is flushed to disk before the rename, so a crash cannot publish a truncated
    file, and it is removed if anything fails before the rename.

    Args:
        target: The file to create or replace. A symlink is resolved, and its target replaced.
        data: The complete new content.
        mtime_ns: If given, the modification time to stamp on the file, in nanoseconds.
        keep_existing_if_locked: For a cache file whose existing copy is as good as the new one:
            when Windows still refuses the rename after a few retries because another process has
            the target open, keep that copy and return ``False`` instead of raising.

    Returns:
        ``True`` if *target* now holds *data*; ``False`` if an existing copy was kept instead.

    Raises:
        OSError: If the data cannot be written, or the target cannot be replaced.
    """
    target = Path(os.path.realpath(target))
    try:
        mode = stat.S_IMODE(target.stat().st_mode)
    except FileNotFoundError:
        mode = None
    tmp, fd = _create_temporary(target.parent, 0o666 if mode is None else mode)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if mode is not None and not _IS_WINDOWS:
            # The umask applied at creation; an existing file keeps its exact bits.
            os.chmod(tmp, mode)
        if mtime_ns is not None:
            os.utime(tmp, ns=(mtime_ns, mtime_ns))
        replaced = _replace(tmp, target, keep_existing_if_locked=keep_existing_if_locked)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    if not replaced:
        tmp.unlink(missing_ok=True)
    return replaced


def _create_temporary(directory: Path, mode: int) -> tuple[Path, int]:
    """Create a uniquely named file in *directory* with *mode* less the umask; return it and its fd."""
    while True:
        tmp = directory / f".{secrets.token_hex(6)}.part"
        try:
            return tmp, os.open(tmp, _OPEN_FLAGS, mode)
        except FileExistsError:
            continue


def _replace(tmp: Path, target: Path, *, keep_existing_if_locked: bool) -> bool:
    """Rename *tmp* over *target*; on Windows, retry while another process holds the target open."""
    attempts = _REPLACE_ATTEMPTS if _IS_WINDOWS else 1
    for attempt in range(attempts):
        try:
            os.replace(tmp, target)
        except PermissionError:
            if attempt + 1 < attempts:
                time.sleep(_REPLACE_BACKOFF_SECONDS)
                continue
            if _IS_WINDOWS and keep_existing_if_locked and target.exists():
                return False
            raise
        else:
            return True
    return False  # pragma: no cover - the loop always returns or raises
