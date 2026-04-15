"""Tests for the default subprocess-based migration backend."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit.exceptions import MigrationError
from idfkit.migration.subprocess_backend import SubprocessMigrator, binary_candidates


class TestBinaryCandidates:
    def test_exact_patch_first(self) -> None:
        names = binary_candidates((24, 1, 0), (24, 2, 0))
        assert names[0] == "Transition-V24-1-0-to-V24-2-0"

    def test_zero_patch_fallback_for_9_0_1(self) -> None:
        names = binary_candidates((8, 9, 0), (9, 0, 1))
        assert "Transition-V8-9-0-to-V9-0-0" in names
        # 8.9.0 is already patch-0, so the candidate with b's patch preserved comes first.
        assert names[0] == "Transition-V8-9-0-to-V9-0-1"

    def test_deduplicates(self) -> None:
        # When both sides are already patch-0, fallbacks collapse into a single name.
        names = binary_candidates((24, 1, 0), (24, 2, 0))
        assert len(set(names)) == len(names)
        assert names == ["Transition-V24-1-0-to-V24-2-0"]


class TestSubprocessMigrator:
    @pytest.fixture
    def updater_dir(self, tmp_path: Path) -> Path:
        d = tmp_path / "IDFVersionUpdater"
        d.mkdir()
        return d

    def test_missing_updater_dir_raises(self, tmp_path: Path) -> None:
        migrator = SubprocessMigrator(version_updater_dir=tmp_path / "nonexistent")
        with pytest.raises(MigrationError, match="IDFVersionUpdater directory not found"):
            migrator.migrate_step(
                "Version,24.1;",
                (24, 1, 0),
                (24, 2, 0),
                work_dir=tmp_path / "work",
            )

    def test_missing_binary_raises(self, tmp_path: Path, updater_dir: Path) -> None:
        migrator = SubprocessMigrator(version_updater_dir=updater_dir)
        with pytest.raises(MigrationError, match="No transition binary found"):
            migrator.migrate_step(
                "Version,24.1;",
                (24, 1, 0),
                (24, 2, 0),
                work_dir=tmp_path / "work",
            )

    @patch("idfkit.migration.subprocess_backend.subprocess.run")
    def test_success_path(
        self,
        mock_run: MagicMock,
        tmp_path: Path,
        updater_dir: Path,
    ) -> None:
        # Stage the binary so _locate_binary succeeds.
        binary = updater_dir / "Transition-V24-1-0-to-V24-2-0"
        binary.touch()
        binary.chmod(0o755)

        work = tmp_path / "work"

        def _fake_run(cmd: list[str], **kwargs: object) -> MagicMock:
            # The transition binary "migrates" by overwriting the input IDF in place.
            input_idf = Path(cmd[1])
            input_idf.write_text("Version,24.2;\n", encoding="latin-1")
            proc = MagicMock()
            proc.returncode = 0
            proc.stdout = "ok"
            proc.stderr = ""
            return proc

        mock_run.side_effect = _fake_run

        migrator = SubprocessMigrator(version_updater_dir=updater_dir)
        result = migrator.migrate_step(
            "Version,24.1;\n",
            (24, 1, 0),
            (24, 2, 0),
            work_dir=work,
        )
        assert result.idf_text == "Version,24.2;\n"
        assert result.stdout == "ok"

    @patch("idfkit.migration.subprocess_backend.subprocess.run")
    def test_nonzero_exit_raises(
        self,
        mock_run: MagicMock,
        tmp_path: Path,
        updater_dir: Path,
    ) -> None:
        binary = updater_dir / "Transition-V24-1-0-to-V24-2-0"
        binary.touch()

        proc = MagicMock()
        proc.returncode = 2
        proc.stdout = ""
        proc.stderr = "boom"
        mock_run.return_value = proc

        migrator = SubprocessMigrator(version_updater_dir=updater_dir)
        with pytest.raises(MigrationError, match="non-zero status"):
            migrator.migrate_step(
                "Version,24.1;\n",
                (24, 1, 0),
                (24, 2, 0),
                work_dir=tmp_path / "work",
            )

    @patch("idfkit.migration.subprocess_backend.subprocess.run")
    def test_timeout_raises(
        self,
        mock_run: MagicMock,
        tmp_path: Path,
        updater_dir: Path,
    ) -> None:
        binary = updater_dir / "Transition-V24-1-0-to-V24-2-0"
        binary.touch()
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["x"], timeout=1)

        migrator = SubprocessMigrator(version_updater_dir=updater_dir, step_timeout=1.0)
        with pytest.raises(MigrationError, match="timed out"):
            migrator.migrate_step(
                "Version,24.1;\n",
                (24, 1, 0),
                (24, 2, 0),
                work_dir=tmp_path / "work",
            )
