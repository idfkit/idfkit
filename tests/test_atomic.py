"""Tests for idfkit._atomic: publishing a file in one rename."""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

import pytest

import idfkit._atomic as atomic
from idfkit._atomic import write_bytes_atomically

posix_only = pytest.mark.skipif(sys.platform == "win32", reason="POSIX permission bits")


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def test_writes_the_content_and_leaves_no_temporary_file(tmp_path: Path) -> None:
    target = tmp_path / "file.epw"

    assert write_bytes_atomically(target, b"data") is True

    assert target.read_bytes() == b"data"
    assert [p.name for p in tmp_path.iterdir()] == ["file.epw"]


@posix_only
def test_a_new_file_gets_the_mode_the_umask_gives_it(tmp_path: Path) -> None:
    # mkstemp made every published file 0600, so a cache warmed by one user could not be read by
    # another. A file written in place gets 0o666 less the umask, and so must this one.
    old = os.umask(0o022)
    try:
        write_bytes_atomically(tmp_path / "file.epw", b"data")
        os.umask(0o002)
        write_bytes_atomically(tmp_path / "group.epw", b"data")
    finally:
        os.umask(old)

    assert _mode(tmp_path / "file.epw") == 0o644
    assert _mode(tmp_path / "group.epw") == 0o664


@posix_only
def test_an_existing_file_keeps_its_mode(tmp_path: Path) -> None:
    target = tmp_path / "file.epw"
    target.write_bytes(b"old")
    target.chmod(0o640)

    write_bytes_atomically(target, b"new")

    assert target.read_bytes() == b"new"
    assert _mode(target) == 0o640


@posix_only
def test_a_symlink_is_followed_and_survives(tmp_path: Path) -> None:
    real = tmp_path / "real.ddy"
    real.write_bytes(b"old")
    link = tmp_path / "link.ddy"
    link.symlink_to(real)

    write_bytes_atomically(link, b"new")

    assert link.is_symlink()
    assert real.read_bytes() == b"new"


def test_the_modification_time_can_be_stamped(tmp_path: Path) -> None:
    target = tmp_path / "file.epw"
    stamp = 1_600_000_000_123_456_789

    write_bytes_atomically(target, b"data", mtime_ns=stamp)

    assert target.stat().st_mtime_ns // 1000 == stamp // 1000  # filesystems keep at least microseconds


def test_a_failed_rename_removes_the_temporary_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse(*_args: object) -> None:
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(atomic.os, "replace", refuse)

    with pytest.raises(OSError, match="No space left"):
        write_bytes_atomically(tmp_path / "file.epw", b"data")

    assert list(tmp_path.iterdir()) == []


def test_the_temporary_name_is_short(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Embedding the target name in the temporary name pushed long cache paths past Windows MAX_PATH.
    seen: list[Path] = []
    real_replace = os.replace

    def spy(src: Path, dst: Path) -> None:
        seen.append(Path(src))
        real_replace(src, dst)

    monkeypatch.setattr(atomic.os, "replace", spy)
    target = tmp_path / ("x" * 120 + ".epw")

    write_bytes_atomically(target, b"data")

    assert len(seen[0].name) < len(target.name)
    assert seen[0].name.startswith(".") and seen[0].suffix == ".part"


class TestARefusedRename:
    @staticmethod
    def _refuse_replace(monkeypatch: pytest.MonkeyPatch) -> list[int]:
        calls: list[int] = []

        def refuse(*_args: object) -> None:
            calls.append(1)
            raise PermissionError(13, "Access is denied")

        monkeypatch.setattr(atomic.os, "replace", refuse)
        monkeypatch.setattr(atomic.time, "sleep", lambda _s: None)
        return calls

    def test_on_posix_it_raises_at_once(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        # A rename on POSIX is never refused because a reader has the file open: a PermissionError
        # there (a sticky directory, an immutable file) is permanent, so retrying only hides it.
        monkeypatch.setattr(atomic, "_IS_WINDOWS", False)
        calls = self._refuse_replace(monkeypatch)
        target = tmp_path / "file.ddy"
        target.write_bytes(b"old")

        with pytest.raises(PermissionError):
            write_bytes_atomically(target, b"new", keep_existing_if_locked=True)

        assert calls == [1]
        assert target.read_bytes() == b"old"
        assert [p.name for p in tmp_path.iterdir()] == ["file.ddy"]

    def test_on_windows_it_retries_then_raises_by_default(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(atomic, "_IS_WINDOWS", True)
        calls = self._refuse_replace(monkeypatch)
        target = tmp_path / "file.ddy"
        target.write_bytes(b"old")

        with pytest.raises(PermissionError):
            write_bytes_atomically(target, b"new")

        assert len(calls) == atomic._REPLACE_ATTEMPTS  # pyright: ignore[reportPrivateUsage]
        assert [p.name for p in tmp_path.iterdir()] == ["file.ddy"]

    def test_on_windows_a_cache_write_may_keep_the_existing_copy(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(atomic, "_IS_WINDOWS", True)
        self._refuse_replace(monkeypatch)
        target = tmp_path / "file.epw"
        target.write_bytes(b"same")

        assert write_bytes_atomically(target, b"same", keep_existing_if_locked=True) is False

        assert target.read_bytes() == b"same"
        assert [p.name for p in tmp_path.iterdir()] == ["file.epw"]

    def test_on_windows_a_first_write_still_raises(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(atomic, "_IS_WINDOWS", True)
        self._refuse_replace(monkeypatch)

        with pytest.raises(PermissionError):
            write_bytes_atomically(tmp_path / "file.epw", b"data", keep_existing_if_locked=True)

        assert list(tmp_path.iterdir()) == []
