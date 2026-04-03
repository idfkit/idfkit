"""Tests for idfkit.compat._cli, SARIF output, and the check_compatibility integration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idfkit.compat._checker import check_compatibility, resolve_version
from idfkit.compat._cli import main
from idfkit.compat._models import CompatSeverity, Diagnostic
from idfkit.compat._sarif import format_sarif

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


@pytest.fixture
def removed_type_script(tmp_path: Path) -> tuple[Path, str]:
    """Create a script referencing a type that was removed between 8.9 and 25.2."""
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
    return p, removed_type


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

    def test_removed_choice_detected_for_noncanonical_obj_type_casing(self) -> None:
        """Choice checks should still work when object type casing differs from schema canonical form."""
        from idfkit.compat._diff import build_schema_index, diff_schemas
        from idfkit.schema import get_schema

        idx_old = build_schema_index(get_schema((8, 9, 0)))
        idx_new = build_schema_index(get_schema((25, 2, 0)))
        diff = diff_schemas(idx_old, idx_new)

        candidate = next(
            (
                (obj_type, field_name, choice)
                for (obj_type, field_name), choices in sorted(diff.removed_choices.items())
                if field_name.isidentifier() and choices and (obj_type, field_name) in idx_new.choices
                for choice in sorted(choices)
            ),
            None,
        )
        if candidate is None:
            pytest.skip("No suitable removed enum choice found between 8.9.0 and 25.2.0")

        obj_type, field_name, removed_choice = candidate
        source = f'doc.add("{obj_type.lower()}", "Obj1", {field_name}="{removed_choice}")\n'
        diagnostics = check_compatibility(source, "test.py", targets=[(8, 9, 0), (25, 2, 0)])

        c002_diags = [d for d in diagnostics if d.code == "C002"]
        assert len(c002_diags) >= 1
        assert any(removed_choice in d.message for d in c002_diags)


class TestCheckCompatibilityGroupFiltering:
    """Tests for include_groups / exclude_groups parameters."""

    def test_include_groups_filters_results(self) -> None:
        """Only Zone (Thermal Zones and Surfaces) should produce diagnostics."""
        source = 'doc.add("Zone", "Z1")\ndoc.add("Material", "M1")\n'
        # With include_groups, only the specified group's types are checked
        diags_all = check_compatibility(source, "t.py", targets=[(8, 9, 0), (25, 2, 0)])
        diags_filtered = check_compatibility(
            source,
            "t.py",
            targets=[(8, 9, 0), (25, 2, 0)],
            include_groups={"Thermal Zones and Surfaces"},
        )
        # Zone is in "Thermal Zones and Surfaces", Material is in
        # "Surface Construction Elements".  The filtered set should have no
        # Material diagnostics.
        mat_diags = [d for d in diags_filtered if "Material" in d.message]
        assert len(mat_diags) == 0
        # But if there were any Material diagnostics in the unfiltered set,
        # the filter removed them.
        mat_diags_all = [d for d in diags_all if "Material" in d.message]
        assert len(diags_filtered) <= len(diags_all) - len(mat_diags_all)

    def test_exclude_groups_filters_results(self) -> None:
        """Excluding 'Thermal Zones and Surfaces' should remove Zone diagnostics."""
        source = 'doc.add("Zone", "Z1")\ndoc.add("Material", "M1")\n'
        diags_filtered = check_compatibility(
            source,
            "t.py",
            targets=[(8, 9, 0), (25, 2, 0)],
            exclude_groups={"Thermal Zones and Surfaces"},
        )
        zone_diags = [d for d in diags_filtered if "Zone" in d.message]
        assert len(zone_diags) == 0

    def test_no_groups_returns_all(self) -> None:
        """Without group filters, all diagnostics are returned."""
        source = 'doc.add("Zone", "Z1")\n'
        diags = check_compatibility(source, "t.py", targets=[(24, 1, 0), (24, 2, 0)])
        diags_explicit = check_compatibility(
            source, "t.py", targets=[(24, 1, 0), (24, 2, 0)], include_groups=None, exclude_groups=None
        )
        assert len(diags) == len(diags_explicit)


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
        # Zone/Material are stable across 24.1→24.2 so we expect 0
        assert exc_info.value.code == 0

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

    def test_cli_json_diagnostic_structure(
        self, removed_type_script: tuple[Path, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """If diagnostics are emitted in JSON, each has the required fields."""
        p, _removed_type = removed_type_script

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


# ---------------------------------------------------------------------------
# SARIF output tests
# ---------------------------------------------------------------------------


class TestSARIFOutput:
    """Tests for SARIF output format."""

    def test_format_sarif_empty(self) -> None:
        """Empty diagnostics produce valid SARIF with zero results."""
        output = format_sarif([])
        data = json.loads(output)
        assert data["version"] == "2.1.0"
        assert "$schema" in data
        assert len(data["runs"]) == 1
        assert data["runs"][0]["results"] == []
        assert len(data["runs"][0]["tool"]["driver"]["rules"]) >= 2

    def test_format_sarif_with_diagnostics(self) -> None:
        """SARIF output includes correctly mapped diagnostic fields."""
        diag = Diagnostic(
            code="C001",
            message="Object type 'Foo' not found in 25.1.0 (exists in 24.2.0)",
            severity=CompatSeverity.WARNING,
            filename="test.py",
            line=10,
            col=5,
            end_col=15,
            from_version="24.2.0",
            to_version="25.1.0",
        )
        output = format_sarif([diag])
        data = json.loads(output)
        results = data["runs"][0]["results"]
        assert len(results) == 1
        r = results[0]
        assert r["ruleId"] == "C001"
        assert r["level"] == "warning"
        assert "Foo" in r["message"]["text"]
        loc = r["locations"][0]["physicalLocation"]
        assert loc["artifactLocation"]["uri"] == "test.py"
        assert loc["region"]["startLine"] == 10
        assert loc["region"]["startColumn"] == 6  # 1-based
        assert loc["region"]["endColumn"] == 16  # 1-based

    def test_format_sarif_with_suggested_fix(self) -> None:
        """SARIF output includes fixes when suggested_fix is set."""
        diag = Diagnostic(
            code="C001",
            message="Test",
            severity=CompatSeverity.WARNING,
            filename="test.py",
            line=1,
            col=0,
            end_col=5,
            from_version="24.1.0",
            to_version="25.1.0",
            suggested_fix="Use 'NewType' instead",
        )
        output = format_sarif([diag])
        data = json.loads(output)
        result = data["runs"][0]["results"][0]
        assert "fixes" in result
        assert result["fixes"][0]["description"]["text"] == "Use 'NewType' instead"

    def test_cli_sarif_output(self, removed_type_script: tuple[Path, str], capsys: pytest.CaptureFixture[str]) -> None:
        """CLI --sarif produces valid SARIF output."""
        p, _removed_type = removed_type_script

        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(p), "--from", "8.9", "--to", "25.2", "--sarif"])

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["version"] == "2.1.0"
        assert len(data["runs"][0]["results"]) >= 1

    def test_cli_json_and_sarif_mutually_exclusive(self, simple_script_file: Path) -> None:
        """CLI rejects --json and --sarif together."""
        with pytest.raises(SystemExit) as exc_info:
            main([
                "check",
                str(simple_script_file),
                "--from",
                "24.1",
                "--to",
                "24.2",
                "--json",
                "--sarif",
            ])
        assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# Rule selection tests
# ---------------------------------------------------------------------------


class TestRuleSelection:
    """Tests for --select and --ignore flags."""

    def test_cli_select_filters_codes(
        self, removed_type_script: tuple[Path, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--select C001 should only include C001 diagnostics."""
        p, _removed_type = removed_type_script

        with pytest.raises(SystemExit):
            main(["check", str(p), "--from", "8.9", "--to", "25.2", "--json", "--select", "C001"])

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        for diag in data["diagnostics"]:
            assert diag["code"] == "C001"

    def test_cli_ignore_suppresses_codes(
        self, removed_type_script: tuple[Path, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--ignore C001 should exclude C001 diagnostics."""
        p, _removed_type = removed_type_script

        with pytest.raises(SystemExit):
            main(["check", str(p), "--from", "8.9", "--to", "25.2", "--json", "--ignore", "C001"])

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        for diag in data["diagnostics"]:
            assert diag["code"] != "C001"

    def test_cli_unknown_select_code_exits_2(self, simple_script_file: Path) -> None:
        """Unknown codes in --select cause exit 2."""
        with pytest.raises(SystemExit) as exc_info:
            main([
                "check",
                str(simple_script_file),
                "--from",
                "24.1",
                "--to",
                "24.2",
                "--select",
                "C999",
            ])
        assert exc_info.value.code == 2

    def test_cli_unknown_ignore_code_exits_2(self, simple_script_file: Path) -> None:
        """Unknown codes in --ignore cause exit 2."""
        with pytest.raises(SystemExit) as exc_info:
            main([
                "check",
                str(simple_script_file),
                "--from",
                "24.1",
                "--to",
                "24.2",
                "--ignore",
                "XBAD",
            ])
        assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# Group filtering CLI tests
# ---------------------------------------------------------------------------


class TestGroupFilteringCLI:
    """Tests for --group and --exclude-group flags."""

    def test_cli_group_flag(self, simple_script_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """--group restricts linting to the specified IDD groups."""
        with pytest.raises(SystemExit):
            main([
                "check",
                str(simple_script_file),
                "--from",
                "8.9",
                "--to",
                "25.2",
                "--json",
                "--group",
                "Thermal Zones and Surfaces",
            ])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        # No Material-related diagnostics should be present
        for diag in data["diagnostics"]:
            assert "Material" not in diag["message"]

    def test_cli_exclude_group_flag(self, simple_script_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """--exclude-group removes the specified IDD groups from linting."""
        with pytest.raises(SystemExit):
            main([
                "check",
                str(simple_script_file),
                "--from",
                "8.9",
                "--to",
                "25.2",
                "--json",
                "--exclude-group",
                "Surface Construction Elements",
            ])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        for diag in data["diagnostics"]:
            assert "Material" not in diag["message"]


# ---------------------------------------------------------------------------
# Severity filtering tests
# ---------------------------------------------------------------------------


class TestSeverityFiltering:
    """Tests for --severity flag."""

    def test_cli_severity_error_suppresses_warnings(
        self, removed_type_script: tuple[Path, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--severity error should suppress warning-level diagnostics."""
        p, _removed_type = removed_type_script

        with pytest.raises(SystemExit):
            main(["check", str(p), "--from", "8.9", "--to", "25.2", "--json", "--severity", "error"])

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        for diag in data["diagnostics"]:
            assert diag["severity"] == "error"

    def test_cli_severity_warning_reports_all(
        self, removed_type_script: tuple[Path, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--severity warning should report all diagnostics (the default)."""
        p, _removed_type = removed_type_script

        with pytest.raises(SystemExit):
            main(["check", str(p), "--from", "8.9", "--to", "25.2", "--json", "--severity", "warning"])

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        # Should include both warnings and errors (if any)
        assert isinstance(data["diagnostics"], list)


# ---------------------------------------------------------------------------
# Diagnostic model tests
# ---------------------------------------------------------------------------


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


class TestCompatRegressionFixes:
    """Regression tests for review feedback fixes."""

    def test_cli_resolves_two_part_minor_to_bundled_patch(self) -> None:
        """9.0 should resolve to 9.0.1, not fallback to 8.9.0."""
        from idfkit.compat._cli import _parse_version_spec  # pyright: ignore[reportPrivateUsage]

        assert _parse_version_spec("9.0") == (9, 0, 1)

    def test_cli_invalid_targets_entry_exits_2(self, simple_script_file: Path) -> None:
        """Malformed --targets entries should be treated as usage errors."""
        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(simple_script_file), "--targets", "24.2,"])

        assert exc_info.value.code == 2

    def test_object_type_check_is_case_insensitive(self) -> None:
        """Lowercase object literals should be checked the same as canonical names."""
        from idfkit.compat._diff import build_schema_index, diff_schemas
        from idfkit.schema import get_schema

        idx_old = build_schema_index(get_schema((8, 9, 0)))
        idx_new = build_schema_index(get_schema((25, 2, 0)))
        diff = diff_schemas(idx_old, idx_new)

        if not diff.removed_types:
            pytest.skip("No removed types between 8.9.0 and 25.2.0")

        removed_type = sorted(diff.removed_types)[0]
        source = f'doc.add("{removed_type.lower()}", "Obj1")\n'

        diagnostics = check_compatibility(source, "case.py", targets=[(8, 9, 0), (25, 2, 0)])
        assert any(d.code == "C001" for d in diagnostics)

    def test_cli_syntax_error_exits_2(self, tmp_path: Path) -> None:
        """Syntax-invalid sources should not crash the CLI."""
        broken = tmp_path / "broken.py"
        broken.write_text('doc.add("Zone", "Z1"\n')

        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(broken), "--from", "24.1", "--to", "24.2"])

        assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# _parse_version_spec edge cases
# ---------------------------------------------------------------------------


class TestParseVersionSpec:
    """Additional edge-case tests for _parse_version_spec."""

    def test_empty_part_raises(self) -> None:
        """A version string with an empty segment (e.g. '24..1') raises ArgumentTypeError."""
        import argparse

        from idfkit.compat._cli import _parse_version_spec  # pyright: ignore[reportPrivateUsage]

        with pytest.raises(argparse.ArgumentTypeError, match="Invalid version specifier"):
            _parse_version_spec("24..1")

    def test_non_integer_part_raises(self) -> None:
        """A version string with a non-integer segment raises ArgumentTypeError."""
        import argparse

        from idfkit.compat._cli import _parse_version_spec  # pyright: ignore[reportPrivateUsage]

        with pytest.raises(argparse.ArgumentTypeError, match="Invalid version specifier"):
            _parse_version_spec("24.abc")

    def test_three_part_version_parsed(self) -> None:
        """A three-part version string (e.g. '24.1.0') is accepted and returned as-is."""
        from idfkit.compat._cli import _parse_version_spec  # pyright: ignore[reportPrivateUsage]

        assert _parse_version_spec("24.1.0") == (24, 1, 0)

    def test_two_part_no_matching_minor_fallback(self) -> None:
        """A two-part version with no matching bundled minor falls back to MAJOR.MINOR.0."""
        from idfkit.compat._cli import _parse_version_spec  # pyright: ignore[reportPrivateUsage]

        # Version 99.0 does not exist in any bundled schema.
        result = _parse_version_spec("99.0")
        assert result == (99, 0, 0)


# ---------------------------------------------------------------------------
# _resolve_targets edge cases
# ---------------------------------------------------------------------------


class TestResolveTargetsEdgeCases:
    """Tests for _resolve_targets error paths."""

    def test_targets_with_unknown_version_exits_2(self, simple_script_file: Path) -> None:
        """--targets containing an unresolvable version causes exit 2."""
        # Versions 1.0 and 1.1 are below the minimum bundled version (8.9).
        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(simple_script_file), "--targets", "1.0,1.1"])
        assert exc_info.value.code == 2

    def test_targets_with_duplicate_version_exits_2(self, simple_script_file: Path) -> None:
        """--targets where all versions resolve to the same version causes exit 2."""
        # Both 24.1 and 24.1.0 resolve to the same bundled version.
        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(simple_script_file), "--targets", "24.1,24.1.0"])
        assert exc_info.value.code == 2

    def test_from_to_with_unknown_version_exits_2(self, simple_script_file: Path) -> None:
        """--from with an unresolvable version causes exit 2 during resolution."""
        # Version 1.0 is below the minimum bundled version (8.9) so resolve_version raises.
        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(simple_script_file), "--from", "1.0", "--to", "24.1"])
        assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# _checker.py edge cases
# ---------------------------------------------------------------------------


class TestCheckerEdgeCases:
    """Tests for uncovered branches in _checker.py."""

    def test_choice_value_with_no_obj_type_skipped(self) -> None:
        """A CHOICE_VALUE literal with no obj_type is silently skipped."""
        from idfkit.compat._checker import _check_choice_value  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._diff import SchemaIndex  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._models import ExtractedLiteral, LiteralKind

        idx = SchemaIndex(version=(24, 1, 0), object_types=frozenset(), choices={})
        literal = ExtractedLiteral(
            value="Smooth",
            kind=LiteralKind.CHOICE_VALUE,
            line=1,
            col=0,
            end_col=6,
            obj_type=None,
            field_name=None,
        )
        out: list[Diagnostic] = []
        _check_choice_value(literal, {(24, 1, 0): idx}, "test.py", out)
        assert out == []

    def test_choice_value_group_filtered_when_obj_type_is_none(self) -> None:
        """When allowed_types filter is active and literal.obj_type is None, the literal is not skipped."""

        # A CHOICE_VALUE without obj_type has _literal_obj_type return None.
        # When allowed_types is set and ot is None, the ``if ot is not None`` guard
        # prevents the skip, so the literal passes the filter and enters _check_choice_value.
        # Since obj_type is None, _check_choice_value returns immediately without diagnostics.
        source = 'doc.add("Zone", field="SomeValue")\n'
        # Use include_groups to activate the filter path.
        diagnostics = check_compatibility(
            source,
            "test.py",
            targets=[(24, 1, 0), (24, 2, 0)],
            include_groups={"Thermal Zones and Surfaces"},
        )
        # We just verify it runs without error; no assertion on count needed.
        assert isinstance(diagnostics, list)

    def test_choice_value_case_insensitive_match(self) -> None:
        """Choice values that differ only in case are treated as present."""
        from idfkit.compat._checker import _check_choice_value  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._diff import SchemaIndex  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._models import ExtractedLiteral, LiteralKind

        idx = SchemaIndex(
            version=(1, 0, 0),
            object_types=frozenset({"Material"}),
            choices={("Material", "roughness"): frozenset({"MediumSmooth"})},
        )
        # Use lowercase variant -- should match case-insensitively.
        literal = ExtractedLiteral(
            value="mediumsmooth",
            kind=LiteralKind.CHOICE_VALUE,
            line=1,
            col=0,
            end_col=12,
            obj_type="Material",
            field_name="roughness",
        )
        out: list[Diagnostic] = []
        _check_choice_value(literal, {(1, 0, 0): idx, (2, 0, 0): idx}, "test.py", out)
        # Case-insensitive match means present_in has two entries, absent_in is empty => no diagnostic.
        assert out == []

    def test_choice_value_unknown_obj_type_in_one_version(self) -> None:
        """A CHOICE_VALUE whose obj_type is unknown in one version is skipped for that version."""
        from idfkit.compat._checker import _check_choice_value  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._diff import SchemaIndex  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._models import ExtractedLiteral, LiteralKind

        # idx1 has "Material", idx2 does not -> canonical lookup for "material" returns None in idx2
        idx1 = SchemaIndex(
            version=(1, 0, 0),
            object_types=frozenset({"Material"}),
            choices={("Material", "roughness"): frozenset({"Smooth"})},
        )
        idx2 = SchemaIndex(
            version=(2, 0, 0),
            object_types=frozenset({"Zone"}),
            choices={},
        )
        literal = ExtractedLiteral(
            value="Smooth",
            kind=LiteralKind.CHOICE_VALUE,
            line=1,
            col=0,
            end_col=6,
            obj_type="material",
            field_name="roughness",
        )
        out: list[Diagnostic] = []
        _check_choice_value(literal, {(1, 0, 0): idx1, (2, 0, 0): idx2}, "test.py", out)
        # idx2 doesn't have Material at all, so no absent_in diagnostic (only one version has enum)
        assert out == []

    def test_choice_value_canonical_obj_type_lookup(self) -> None:
        """When obj_type casing differs from the schema, canonical lookup resolves choices."""
        from idfkit.compat._checker import _check_choice_value  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._diff import SchemaIndex  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._models import ExtractedLiteral, LiteralKind

        # canonical name is "Material" but literal uses "material" (lowercase)
        # choices dict only has the canonical-cased key
        idx_with_choices = SchemaIndex(
            version=(1, 0, 0),
            object_types=frozenset({"Material"}),
            choices={("Material", "roughness"): frozenset({"Smooth", "MediumSmooth"})},
        )
        # Second version has the choice missing to produce a diagnostic
        idx_missing_choice = SchemaIndex(
            version=(2, 0, 0),
            object_types=frozenset({"Material"}),
            choices={("Material", "roughness"): frozenset({"MediumSmooth"})},
        )
        literal = ExtractedLiteral(
            value="Smooth",
            kind=LiteralKind.CHOICE_VALUE,
            line=1,
            col=0,
            end_col=6,
            obj_type="material",
            field_name="roughness",
        )
        out: list[Diagnostic] = []
        _check_choice_value(
            literal,
            {(1, 0, 0): idx_with_choices, (2, 0, 0): idx_missing_choice},
            "test.py",
            out,
        )
        # "Smooth" is present in v1 (via canonical lookup) but absent in v2 -> C002 diagnostic
        assert len(out) == 1
        assert out[0].code == "C002"


class TestFilterDiagnosticsAndFormatText:
    """Tests for _filter_diagnostics and _format_text edge cases."""

    def test_filter_diagnostics_select_skips_non_matching(self) -> None:
        """_filter_diagnostics skips diagnostics whose code is not in select set."""
        from idfkit.compat._cli import _filter_diagnostics  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._models import CompatSeverity, Diagnostic

        d_c001 = Diagnostic(
            code="C001",
            message="Missing type",
            severity=CompatSeverity.WARNING,
            filename="t.py",
            line=1,
            col=0,
            end_col=4,
            from_version="24.1.0",
            to_version="25.1.0",
        )
        d_c002 = Diagnostic(
            code="C002",
            message="Missing choice",
            severity=CompatSeverity.WARNING,
            filename="t.py",
            line=2,
            col=0,
            end_col=4,
            from_version="24.1.0",
            to_version="25.1.0",
        )
        result = _filter_diagnostics([d_c001, d_c002], select={"C001"}, ignore=None, severity=None)
        assert len(result) == 1
        assert result[0].code == "C001"

    def test_format_text_with_diagnostics(self) -> None:
        """_format_text produces diagnostic lines when diagnostics are non-empty."""
        from idfkit.compat._cli import _format_text  # pyright: ignore[reportPrivateUsage]
        from idfkit.compat._models import CompatSeverity, Diagnostic

        d = Diagnostic(
            code="C001",
            message="Object type 'Foo' not found",
            severity=CompatSeverity.WARNING,
            filename="script.py",
            line=3,
            col=4,
            end_col=10,
            from_version="8.9.0",
            to_version="25.2.0",
        )
        text = _format_text([d])
        assert "C001" in text
        assert "script.py" in text

    def test_cli_text_output_with_removed_type(
        self, removed_type_script: tuple[Path, str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """CLI text output includes diagnostic lines when issues are found."""
        p, _removed_type = removed_type_script
        with pytest.raises(SystemExit) as exc_info:
            main(["check", str(p), "--from", "8.9", "--to", "25.2"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "C001" in captured.out


class _FakeParser:
    """Minimal parser stub that returns a fixed Namespace from parse_args."""

    def __init__(self, namespace: object) -> None:
        self._namespace = namespace

    def parse_args(self, argv: list[str] | None) -> object:
        return self._namespace

    def print_help(self) -> None:
        pass


class TestMainDispatch:
    """Tests for the main() command dispatch."""

    def test_main_unknown_command_is_noop(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A non-'check' command value causes main() to return without error.

        This exercises the ``if args.command == "check"`` branch that is not taken.
        """
        import argparse

        import idfkit.compat._cli as cli_module  # pyright: ignore[reportPrivateUsage]

        # Patch _build_parser to return a fake parser yielding a non-'check' command namespace.
        args = argparse.Namespace(command="unknown")
        monkeypatch.setattr(cli_module, "_build_parser", lambda: _FakeParser(args))  # pyright: ignore[reportPrivateUsage]
        cli_module.main([])  # Should return normally (no sys.exit)
