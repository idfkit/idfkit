"""Tests for prep_outputs utility."""

from __future__ import annotations

from idfkit import new_document
from idfkit.simulation._common import prep_outputs


class TestPrepOutputs:
    def test_adds_sql_output(self) -> None:
        model = new_document()
        prep_outputs(model)
        assert "Output:SQLite" in model

    def test_adds_summary_reports(self) -> None:
        model = new_document()
        prep_outputs(model)
        assert "Output:Table:SummaryReports" in model

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
