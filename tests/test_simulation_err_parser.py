"""Tests for the EnergyPlus .err file parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.simulation.parsers.err import ErrorReport

FIXTURES = Path(__file__).parent / "fixtures" / "simulation"


class TestErrorReportFromFile:
    """Tests for ErrorReport.from_file()."""

    def test_successful_simulation(self) -> None:
        report = ErrorReport.from_file(FIXTURES / "sample.err")
        assert report.warning_count == 2
        assert report.error_count == 0
        assert not report.has_fatal
        assert not report.has_severe
        assert report.warmup_converged
        assert report.simulation_complete

    def test_fatal_simulation(self) -> None:
        report = ErrorReport.from_file(FIXTURES / "sample_fatal.err")
        assert report.has_fatal
        assert report.has_severe
        assert len(report.fatal) == 1
        assert len(report.severe) == 2
        assert report.error_count == 3
        assert report.warning_count == 0
        assert not report.simulation_complete


class TestErrorReportFromString:
    """Tests for ErrorReport.from_string()."""

    def test_empty_string(self) -> None:
        report = ErrorReport.from_string("")
        assert report.error_count == 0
        assert report.warning_count == 0
        assert not report.warmup_converged
        assert not report.simulation_complete
        assert report.raw_text == ""

    def test_single_warning(self) -> None:
        text = "   ** Warning ** Some warning message\n"
        report = ErrorReport.from_string(text)
        assert report.warning_count == 1
        assert report.warnings[0].message == "Some warning message"
        assert report.warnings[0].severity == "Warning"

    def test_single_severe(self) -> None:
        text = "   ** Severe  ** A severe error occurred\n"
        report = ErrorReport.from_string(text)
        assert report.has_severe
        assert report.severe[0].message == "A severe error occurred"

    def test_single_fatal(self) -> None:
        text = "   **  Fatal  ** Cannot continue\n"
        report = ErrorReport.from_string(text)
        assert report.has_fatal
        assert report.fatal[0].message == "Cannot continue"


class TestContinuationGrouping:
    """Tests for continuation line grouping."""

    def test_continuation_lines_attached_to_warning(self) -> None:
        report = ErrorReport.from_file(FIXTURES / "sample.err")
        # First warning should have 3 continuation lines
        first_warning = report.warnings[0]
        assert len(first_warning.details) == 3
        assert "Weather File Location" in first_warning.details[1]

    def test_continuation_lines_attached_to_severe(self) -> None:
        report = ErrorReport.from_file(FIXTURES / "sample_fatal.err")
        # First severe should have 1 continuation line
        first_severe = report.severe[0]
        assert len(first_severe.details) == 1

    def test_multiple_messages_with_details(self) -> None:
        report = ErrorReport.from_file(FIXTURES / "sample.err")
        # Second warning should have 2 continuation lines
        second_warning = report.warnings[1]
        assert len(second_warning.details) == 2


class TestSummary:
    """Tests for ErrorReport.summary()."""

    def test_successful_summary(self) -> None:
        report = ErrorReport.from_file(FIXTURES / "sample.err")
        summary = report.summary()
        assert "Fatal: 0" in summary
        assert "Warnings: 2" in summary
        assert "completed successfully" in summary
        assert "converged" in summary

    def test_fatal_summary(self) -> None:
        report = ErrorReport.from_file(FIXTURES / "sample_fatal.err")
        summary = report.summary()
        assert "Fatal: 1" in summary
        assert "Severe: 2" in summary
        assert "terminated with fatal error" in summary


class TestFrozenImmutability:
    """Tests that ErrorReport and ErrorMessage are immutable."""

    def test_error_report_frozen(self) -> None:
        report = ErrorReport.from_string("")
        with pytest.raises(AttributeError):
            report.warmup_converged = True  # type: ignore[misc]

    def test_error_message_frozen(self) -> None:
        report = ErrorReport.from_file(FIXTURES / "sample.err")
        msg = report.warnings[0]
        with pytest.raises(AttributeError):
            msg.severity = "Fatal"  # type: ignore[misc]
