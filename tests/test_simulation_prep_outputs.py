"""Tests for prep_outputs utility."""

from __future__ import annotations

import pytest

from idfkit import new_document, write_idf
from idfkit.simulation._common import prep_outputs
from idfkit.versions import ENERGYPLUS_VERSIONS


class TestPrepOutputs:
    def test_adds_sql_output(self) -> None:
        model = new_document()
        prep_outputs(model)
        assert "Output:SQLite" in model

    def test_adds_summary_reports(self) -> None:
        model = new_document()
        prep_outputs(model)
        assert "Output:Table:SummaryReports" in model

    def test_summary_reports_requests_all_summary(self) -> None:
        # It used to pass ``report_1=``, which is no spelling of the ``reports`` group: the value was
        # stored under an unknown key, dropped by the IDF writer, and the object came out empty.
        model = new_document()
        prep_outputs(model)
        reports = model["Output:Table:SummaryReports"].first()
        assert reports is not None
        assert reports.data == {"reports": [{"report_name": "AllSummary"}]}
        assert "AllSummary" in write_idf(model)

    @pytest.mark.parametrize("version", ENERGYPLUS_VERSIONS, ids=lambda v: ".".join(map(str, v)))
    def test_summary_reports_request_all_summary(self, version: tuple[int, int, int]) -> None:
        """The report name must reach the written file, not only the object (it was once dropped)."""
        model = new_document(version=version)
        prep_outputs(model)
        reports = model["Output:Table:SummaryReports"].first()
        assert reports is not None
        assert [group.report_name for group in reports.reports] == ["AllSummary"]
        assert "AllSummary;" in write_idf(model)

    def test_adds_variable_dictionary(self) -> None:
        model = new_document()
        prep_outputs(model)
        assert "Output:VariableDictionary" in model

    def test_idempotent(self) -> None:
        model = new_document()
        prep_outputs(model)
        prep_outputs(model)
        assert len(model["Output:SQLite"]) == 1
        assert len(model["Output:Table:SummaryReports"]) == 1
        assert len(model["Output:VariableDictionary"]) == 1

    def test_preserves_existing_sql_output(self) -> None:
        model = new_document()
        model.add("Output:SQLite", "", option_type="SimpleAndTabular", validate=False)
        prep_outputs(model)
        assert len(model["Output:SQLite"]) == 1
