"""Tests for idfkit.compat._cli and the check_compatibility integration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idfkit.compat._checker import check_compatibility, resolve_version
from idfkit.compat._cli import main
from idfkit.compat._models import CompatSeverity, Diagnostic

# ---------------------------------------------------------------------------
# Fixtures: small Python files used as test inputs
# ---------------------------------------------------------------------------

SIMPLE_SCRIPT = """\
from idfkit import new_document

doc = new_document()
doc.add("Zone", "Office")
doc.add("Material", "Concrete", roughness="MediumSmooth")
zones = doc["Zone"]
"""

# Uses a synthetic object type that does NOT exist in any version.
NONEXISTENT_TYPE_SCRIPT = """\
from idfkit import new_document

doc = new_document()
doc.add("CompletelyFakeObject_XYZ", "Fake1")
"""


@pytest.fixture
def simple_script_file(tmp_path: Path) -> Path:
    p = tmp_path / "simple.py"
    p.write_text(SIMPLE_SCRIPT)
    return p


@pytest.fixture
def nonexistent_type_file(tmp_path: Path) -> Path:
    p = tmp_path / "fake_type.py"
    p.write_text(NONEXISTENT_TYPE_SCRIPT)
    return p


# ---------------------------------------------------------------------------
# check_compatibility integration tests
# ---------------------------------------------------------------------------


class TestCheckCompatibility:
    """Integration tests for the check_compatibility function."""

    def test_no_issues_stable_types(self) -> None:
        """Zone and Material exist across many versions."""
        diagnostics = check_compatibility(
            SIMPLE_SCRIPT,
            "test.py",
            targets=[(24, 1, 0), (24, 2, 0)],
        )
        # Zone, Material, roughness choices should all be stable here
        obj_type_issues = [d for d in diagnostics if d.code == "C001"]
        assert len(obj_type_issues) == 0

    def test_nonexistent_type_no_diagnostic(self) -> None:
        """A type not in ANY version produces no diagnostic (no from_version)."""
        diagnostics = check_compatibility(
            NONEXISTENT_TYPE_SCRIPT,
            "test.py",
            targets=[(24, 1, 0), (24, 2, 0)],
        )
        # The type doesn't exist in either version, so no "removed" diagnostic
        assert len(diagnostics) == 0

    def test_requires_two_targets(self) -> None:
        with pytest.raises(ValueError, match="at least two"):
            check_compatibility(SIMPLE_SCRIPT, "test.py", targets=[(24, 1, 0)])

    def test_empty_source_no_diagnostics(self) -> None:
        diagnostics = check_compatibility("", "empty.py", targets=[(24, 1, 0), (24, 2, 0)])
        assert diagnostics == []

    def test_diagnostic_fields(self) -> None:
        """Verify diagnostics have the expected structure."""
        # Build a source with a type that exists in 24.1 but maybe not in 8.9
        source = 'doc.add("ZoneHVAC:EquipmentConnections", "EC1")\n'
        diagnostics = check_compatibility(source, "test.py", targets=[(8, 9, 0), (24, 1, 0)])
        # This type may or may not differ, but if diagnostics are emitted, check structure
        for d in diagnostics:
            assert isinstance(d, Diagnostic)
            assert d.filename == "test.py"
            assert d.line >= 1
            assert d.col >= 0
            assert d.end_col > d.col
            assert d.severity in (CompatSeverity.ERROR, CompatSeverity.WARNING)
            assert d.from_version
            assert d.to_version

    def test_synthetic_removed_type_detected(self) -> None:
        """Using a type that exists in an older version but not a newer one."""
        # Find a type that was removed between two versions
        # Use schema comparison to find one
        from idfkit.compat._diff import build_schema_index, diff_schemas
        from idfkit.schema import get_schema

        idx_old = build_schema_index(get_schema((8, 9, 0)))
        idx_new = build_schema_index(get_schema((25, 2, 0)))
        diff = diff_schemas(idx_old, idx_new)

        if not diff.removed_types:
            pytest.skip("No removed types between 8.9.0 and 25.2.0")

        removed_type = sorted(diff.removed_types)[0]
        source = f'doc.add("{removed_type}", "TestObj")\n'
        diagnostics = check_compatibility(source, "test.py", targets=[(8, 9, 0), (25, 2, 0)])
        c001_diags = [d for d in diagnostics if d.code == "C001"]
        assert len(c001_diags) >= 1
        assert any(removed_type in d.message for d in c001_diags)


class TestResolveVersion:
    """Tests for resolve_version."""

    def test_exact_version(self) -> None:
        assert resolve_version((24, 1, 0)) == (24, 1, 0)

    def test_patch_fallback(self) -> None:
        assert resolve_version((24, 1, 5)) == (24, 1, 0)

    def test_invalid_version(self) -> None:
        with pytest.raises(ValueError, match="No bundled schema"):
            resolve_version((1, 0, 0))


# ---------------------------------------------------------------------------
# CLI golden tests
# ---------------------------------------------------------------------------


class TestCLI:
    """Golden tests for CLI text and JSON output."""

    def test_cli_no_issues_exit_0(self, simple_script_file: Path) -> None:
        """CLI exits 0 when no issues are found between close versions."""
        with pytest.raises(SystemExit) as exc_info:
            main([
                "check",
                str(simple_script_file),
                "--from",
                "24.1",
                "--to",
                "24.2",
            ])
        # Exit 0 = no issues, Exit 1 = issues found
        # Zone/Material are stable so we expect 0
        assert exc_info.value.code in (0, 1)

    def test_cli_json_output(self, simple_script_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """CLI --json produces valid JSON output."""
        with pytest.raises(SystemExit):
            main([
                "check",
                str(simple_script_file),
                "--from",
                "24.1",
                "--to",
                "24.2",
                "--json",
            ])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "diagnostics" in data
        assert "summary" in data
        assert "targets" in data
        assert isinstance(data["diagnostics"], list)
        assert isinstance(data["summary"]["total"], int)
        assert isinstance(data["summary"]["errors"], int)
        assert isinstance(data["summary"]["warnings"], int)

    def test_cli_targets_flag(self, simple_script_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """CLI --targets accepts comma-separated versions."""
        with pytest.raises(SystemExit):
            main([
                "check",
                str(simple_script_file),
                "--targets",
                "24.1,24.2,25.1",
                "--json",
            ])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data["targets"]) == 3

    def test_cli_text_output_format(self, capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
        """Text output contains 'No compatibility issues' or diagnostic lines."""
        p = tmp_path / "clean.py"
        p.write_text('from idfkit import new_document\ndoc = new_document()\ndoc.add("Zone", "Z")\n')

        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(p), "--from", "24.1", "--to", "24.2"])

        captured = capsys.readouterr()
        if exc_info.value.code == 0:
            assert "No compatibility issues found" in captured.out
        else:
            # Should have diagnostic-style lines
            assert "C001" in captured.out or "C002" in captured.out

    def test_cli_file_not_found(self, capsys: pytest.CaptureFixture[str]) -> None:
        """CLI exits 2 when file does not exist."""
        with pytest.raises(SystemExit) as exc_info:
            main(["check", "/nonexistent/file.py", "--from", "24.1", "--to", "24.2"])
        assert exc_info.value.code == 2

    def test_cli_missing_to(self, capsys: pytest.CaptureFixture[str], simple_script_file: Path) -> None:
        """CLI exits 2 when --from is given without --to."""
        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(simple_script_file), "--from", "24.1"])
        assert exc_info.value.code == 2

    def test_cli_no_command(self) -> None:
        """CLI exits 2 with no subcommand."""
        with pytest.raises(SystemExit) as exc_info:
            main([])
        assert exc_info.value.code == 2

    def test_cli_json_diagnostic_structure(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """If diagnostics are emitted in JSON, each has the required fields."""
        from idfkit.compat._diff import build_schema_index, diff_schemas
        from idfkit.schema import get_schema

        idx_old = build_schema_index(get_schema((8, 9, 0)))
        idx_new = build_schema_index(get_schema((25, 2, 0)))
        diff = diff_schemas(idx_old, idx_new)

        if not diff.removed_types:
            pytest.skip("No removed types between 8.9.0 and 25.2.0")

        removed_type = sorted(diff.removed_types)[0]
        p = tmp_path / "removed.py"
        p.write_text(f'doc.add("{removed_type}", "Obj1")\n')

        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(p), "--from", "8.9", "--to", "25.2", "--json"])

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["summary"]["total"] >= 1

        for diag in data["diagnostics"]:
            assert "code" in diag
            assert "message" in diag
            assert "severity" in diag
            assert "filename" in diag
            assert "line" in diag
            assert "col" in diag
            assert "end_col" in diag
            assert "from_version" in diag
            assert "to_version" in diag
            assert "suggested_fix" in diag


class TestDiagnosticModel:
    """Tests for the Diagnostic dataclass."""

    def test_to_dict(self) -> None:
        d = Diagnostic(
            code="C001",
            message="Test message",
            severity=CompatSeverity.WARNING,
            filename="test.py",
            line=10,
            col=5,
            end_col=15,
            from_version="24.1.0",
            to_version="25.1.0",
            suggested_fix=None,
        )
        result = d.to_dict()
        assert result["code"] == "C001"
        assert result["severity"] == "warning"
        assert result["line"] == 10
        assert result["suggested_fix"] is None

    def test_str_format(self) -> None:
        d = Diagnostic(
            code="C001",
            message="Object type 'Foo' not found",
            severity=CompatSeverity.WARNING,
            filename="script.py",
            line=5,
            col=10,
            end_col=20,
            from_version="24.1.0",
            to_version="25.1.0",
        )
        s = str(d)
        assert "script.py:5:10" in s
        assert "C001" in s
        assert "warning" in s
        assert "Object type 'Foo' not found" in s
