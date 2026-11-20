"""Type-check fixture for the choice aliases of ``idfkit.choices`` (never called; checked by ``make check``).

Each alias has exactly the choices the stubs give its field (``verify_stubs`` proves it), so a
value annotated with the alias passes to ``add()``, ``update()`` and assignment of that field: through ``IDFDocument``,
through a ``since=`` range, and, with the ``Any`` alias, through ``AnyIDFDocument``. A string the
field does not list, and a set wider than the field takes, are refused.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``: if a seeded error stops being reported, the ignore
becomes unnecessary and the check fails, so the fixture proves the errors are caught.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import Any

from typing_extensions import assert_type

from idfkit import IDFDocument
from idfkit.choices import (
    AnyOutputMeterReportingFrequency,
    AnyOutputTableSummaryReportsReportName,
    OutputMeterReportingFrequency,
    OutputTableSummaryReportsReportName,
    OutputVariableReportingFrequency,
)
from idfkit.versioned import AnyIDFDocument, IDFDocumentSince24_1


def latest(
    doc: IDFDocument[Any],
    frequency: OutputMeterReportingFrequency,
    variable_frequency: OutputVariableReportingFrequency,
    report: OutputTableSummaryReportsReportName,
) -> None:
    meter = doc["Output:Meter"].add(key_name="Electricity:Facility", reporting_frequency=frequency)
    meter.update(reporting_frequency=frequency)
    meter.reporting_frequency = frequency
    # Reading the field gives the alias (the field always holds a value), so a value read passes back.
    assert_type(meter.reporting_frequency, OutputMeterReportingFrequency)
    doc["Output:Variable"].add(
        variable_name="Site Outdoor Air Drybulb Temperature", reporting_frequency=variable_frequency
    )
    # A group's inner field has its alias too.
    doc["Output:Table:SummaryReports"].add(reports=[{"report_name": report}])


def since_range(doc: IDFDocumentSince24_1, frequency: OutputMeterReportingFrequency) -> None:
    doc["Output:Meter"].add(key_name="Electricity:Facility", reporting_frequency=frequency)


def any_release(
    doc: AnyIDFDocument,
    frequency: AnyOutputMeterReportingFrequency,
    report: AnyOutputTableSummaryReportsReportName,
) -> None:
    doc["Output:Meter"].add(key_name="Electricity:Facility", reporting_frequency=frequency)
    doc["Output:Table:SummaryReports"].add(reports=[{"report_name": report}])


def any_into_latest(doc: IDFDocument[Any], report: AnyOutputTableSummaryReportsReportName) -> None:
    # What every release accepts, the latest release accepts.
    doc["Output:Table:SummaryReports"].add(reports=[{"report_name": report}])


def seeded_errors(doc: IDFDocument[Any], any_doc: AnyIDFDocument, report: OutputTableSummaryReportsReportName) -> None:
    doc["Output:Meter"].add(key_name="Electricity:Facility", reporting_frequency="Weekly")  # pyright: ignore[reportArgumentType]
    wrong: OutputMeterReportingFrequency = "Weekly"  # pyright: ignore[reportAssignmentType]
    print(wrong)
    # The latest release's reports include some an older release lacks, which AnyIDFDocument refuses.
    any_doc["Output:Table:SummaryReports"].add(reports=[{"report_name": report}])  # pyright: ignore[reportArgumentType]
