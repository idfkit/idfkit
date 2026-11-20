"""Tests for the ``idfkit migrate`` CLI subcommand."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import idfkit.compat._cli as cli_module
import idfkit.simulation.config as simulation_config
from idfkit import load_idf, new_document, save_idf
from idfkit.compat._cli import main
from idfkit.exceptions import EnergyPlusNotFoundError, MigrationError, UnsupportedVersionError
from idfkit.migration.report import FieldDelta, MigrationDiff, MigrationReport, MigrationStep
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.versions import LATEST_VERSION, version_string


@pytest.fixture
def source_idf(tmp_path: Path) -> Path:
    """A minimal IDF file at v24.1.0 on disk."""
    doc = new_document(version=(24, 1, 0))
    path = tmp_path / "source.idf"
    save_idf(doc, path)
    return path


def _make_fake_migrate(
    *,
    target: tuple[int, int, int],
    source: tuple[int, int, int] = (24, 1, 0),
    success: bool = True,
    raise_exc: BaseException | None = None,
    record: dict[str, Any] | None = None,
) -> Any:
    """Build a stand-in for ``idfkit.migration.migrate`` that returns a canned report.

    When *raise_exc* is supplied the fake raises it instead of returning.
    When *record* is supplied the call kwargs are written into it for inspection.
    """

    def fake_migrate(model: Any, **kwargs: Any) -> MigrationReport:
        if record is not None:
            record["model"] = model
            record["kwargs"] = kwargs
        if raise_exc is not None:
            raise raise_exc
        # A no-op report carries a copy of the input, as migrate() does.
        migrated = new_document(version=target) if target != source else model.copy()
        step = MigrationStep(
            from_version=source,
            to_version=target,
            success=success,
            stdout="ok",
            stderr="",
            runtime_seconds=0.01,
        )
        diff = MigrationDiff(
            added_object_types=("NewType",),
            removed_object_types=(),
            object_count_delta={"Building": 0},
            field_changes={"Building": FieldDelta(added=("new_field",), removed=())},
        )
        return MigrationReport(
            migrated_model=migrated,
            source_version=source,
            target_version=target,
            requested_target=target,
            steps=() if target == source else (step,),
            diff=diff if target != source else MigrationDiff(),
        )

    return fake_migrate


def _fake_energyplus(root: Path, version: tuple[int, int, int]) -> EnergyPlusConfig:
    """An installation record for *version*; the CLI only reads its version before calling migrate."""
    return EnergyPlusConfig(
        executable=root / "energyplus",
        version=version,
        install_dir=root,
        idd_path=root / "Energy+.idd",
    )


class TestCliMigrateDefaults:
    """Argument resolution: defaults for --to and --output."""

    def test_defaults_to_installed_energyplus(
        self,
        source_idf: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Without --to, the target is the discovered installation's release, not the newest schema."""
        installed = _fake_energyplus(tmp_path, (25, 1, 0))
        monkeypatch.setattr(simulation_config, "find_energyplus", lambda: installed)
        record: dict[str, Any] = {}
        monkeypatch.setattr(cli_module, "migrate", _make_fake_migrate(target=(25, 1, 0), record=record))

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf)])

        assert exc.value.code == 0
        assert record["kwargs"]["target_version"] == (25, 1, 0)
        assert record["kwargs"]["energyplus"] is installed
        assert LATEST_VERSION != (25, 1, 0)

        expected = source_idf.with_name("source-v25-1-0.idf")
        assert expected.is_file()
        captured = capsys.readouterr()
        assert "Wrote:" in captured.out
        assert str(expected) in captured.out

    def test_default_target_without_energyplus_exits_2(
        self,
        source_idf: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        def not_found() -> EnergyPlusConfig:
            raise EnergyPlusNotFoundError(["/nowhere"])

        monkeypatch.setattr(simulation_config, "find_energyplus", not_found)
        monkeypatch.setattr(cli_module, "migrate", _make_fake_migrate(target=LATEST_VERSION))

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf)])

        assert exc.value.code == 2
        err = capsys.readouterr().err
        assert "no EnergyPlus installation found" in err
        assert "--energyplus" in err

    def test_target_older_than_model_exits_2(
        self,
        source_idf: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(target=(23, 2, 0), raise_exc=ValueError("Backward migration is not supported")),
        )

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf), "--to", "23.2"])

        assert exc.value.code == 2
        assert "Backward migration" in capsys.readouterr().err

    def test_explicit_to_and_output(
        self,
        source_idf: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(target=(25, 2, 0)),
        )
        out = tmp_path / "nested" / "out.idf"

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf), "--to", "25.2", "--output", str(out)])

        assert exc.value.code == 0
        assert out.is_file()
        # Sanity-check the output parses at the new version.
        migrated = load_idf(str(out))
        assert migrated.version == (25, 2, 0)

    def test_noop_does_not_write_without_explicit_output(
        self,
        source_idf: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(target=(24, 1, 0), source=(24, 1, 0)),
        )

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf), "--to", "24.1"])

        assert exc.value.code == 0
        # No default output file should appear next to the source.
        stragglers = [p for p in tmp_path.iterdir() if p != source_idf]
        assert stragglers == []
        out = capsys.readouterr().out
        assert "No migration needed" in out

    def test_noop_with_explicit_output_copies_input(
        self,
        source_idf: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(target=(24, 1, 0), source=(24, 1, 0)),
        )
        out = tmp_path / "copy.idf"

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf), "--to", "24.1", "--output", str(out)])

        assert exc.value.code == 0
        assert out.is_file()


class TestCliMigrateJson:
    """``--json`` produces a machine-readable report."""

    def test_json_payload_shape(
        self,
        source_idf: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(target=(25, 2, 0)),
        )

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf), "--to", "25.2", "--json"])

        assert exc.value.code == 0
        captured = capsys.readouterr()
        # With --json, stderr progress output should be suppressed.
        assert captured.err == ""
        payload = json.loads(captured.out)
        assert payload["success"] is True
        assert payload["source_version"] == "24.1.0"
        assert payload["target_version"] == "25.2.0"
        assert payload["requested_target"] == "25.2.0"
        assert payload["input"] == str(source_idf)
        assert payload["output"] is not None
        assert len(payload["steps"]) == 1
        assert payload["steps"][0]["from"] == "24.1.0"
        assert payload["steps"][0]["to"] == "25.2.0"
        assert payload["diff"]["added_object_types"] == ["NewType"]
        assert payload["diff"]["field_changes"]["Building"] == {
            "added": ["new_field"],
            "removed": [],
        }

    def test_quiet_suppresses_progress(
        self,
        source_idf: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        record: dict[str, Any] = {}
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(target=(25, 2, 0), record=record),
        )

        with pytest.raises(SystemExit):
            main(["migrate", str(source_idf), "--to", "25.2", "--quiet"])

        assert record["kwargs"]["on_progress"] is None
        captured = capsys.readouterr()
        assert captured.err == ""


class TestCliMigrateErrors:
    """Failure modes surface with the right exit codes and messages."""

    def test_input_not_found(self, capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as exc:
            main(["migrate", "/nonexistent/input.idf", "--to", "25.2"])

        assert exc.value.code == 2
        assert "file not found" in capsys.readouterr().err

    def test_unsupported_target_version(
        self,
        source_idf: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(
                target=(24, 1, 0),
                raise_exc=UnsupportedVersionError((99, 0, 0), ((24, 1, 0),)),
            ),
        )

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf), "--to", "24.1"])

        assert exc.value.code == 2
        assert "error:" in capsys.readouterr().err

    def test_energyplus_not_found(
        self,
        source_idf: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(
                target=(25, 2, 0),
                raise_exc=EnergyPlusNotFoundError(["/nowhere"]),
            ),
        )

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf), "--to", "25.2"])

        assert exc.value.code == 2
        assert "no EnergyPlus installation found" in capsys.readouterr().err

    def test_migration_error_exits_1(
        self,
        source_idf: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.setattr(
            cli_module,
            "migrate",
            _make_fake_migrate(
                target=(25, 2, 0),
                raise_exc=MigrationError(
                    "boom",
                    from_version=(24, 1, 0),
                    to_version=(24, 2, 0),
                    exit_code=1,
                    stderr="",
                    completed_steps=(),
                ),
            ),
        )

        with pytest.raises(SystemExit) as exc:
            main(["migrate", str(source_idf), "--to", "25.2"])

        assert exc.value.code == 1
        assert "migration failed" in capsys.readouterr().err


def test_target_version_string_roundtrip() -> None:
    """Sanity check: version_string is stable for tuples used in payload fields."""
    assert version_string((25, 2, 0)) == "25.2.0"
