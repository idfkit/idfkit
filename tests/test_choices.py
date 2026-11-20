"""Tests for ``idfkit.choices``: one ``Literal`` alias per EnergyPlus choice field.

The stubs keep each choice inline, for type-checking speed; the stub verifier
(``tests/test_versioned.py``) proves every alias equal to its field's choices in the releases it
names, and each ``Any`` alias equal to what ``Any<Class>`` accepts. That a value of an alias passes
to ``add()`` is checked by ``tests/type_checks/choices_fixture.py`` under ``make check``. Here: the
run-time module against the schemas directly.
"""

from __future__ import annotations

from typing import Any, get_args

import idfkit.choices as choices
from idfkit.codegen import generate_stubs as gen
from idfkit.schema import EpJSONSchema, get_schema
from idfkit.versions import ENERGYPLUS_VERSIONS, LATEST_VERSION


def _schema_choices(schema: EpJSONSchema, obj_type: str, field: str, *, group: bool = False) -> set[str]:
    """The non-blank values the schema lists for a field (or an extensible group's inner field)."""
    if group:
        pc = schema.get_parsing_cache(obj_type)
        assert pc is not None
        field_schema: dict[str, Any] = pc.ext_inner_props[field]
    else:
        inner = schema.get_inner_schema(obj_type)
        assert inner is not None
        field_schema = inner["properties"][field]
    return {value for value in field_schema["enum"] if value != ""}


def _alias(name: str) -> set[str]:
    return set(get_args(getattr(choices, name)))


def test_reporting_frequencies_match_the_schema() -> None:
    schema = get_schema(LATEST_VERSION)
    for obj_type, name in (
        ("Output:Meter", "OutputMeterReportingFrequency"),
        ("Output:Variable", "OutputVariableReportingFrequency"),
    ):
        assert _alias(name) == _schema_choices(schema, obj_type, "reporting_frequency")
        assert len(_alias(name)) == 8


def test_group_key_alias_matches_the_schema() -> None:
    schema = get_schema(LATEST_VERSION)
    expected = _schema_choices(schema, "Output:Table:SummaryReports", "report_name", group=True)
    assert _alias("OutputTableSummaryReportsReportName") == expected


def test_any_alias_is_what_every_release_lists() -> None:
    # Before 9.3 the schema lists no reports and takes any string, so those releases restrict nothing.
    listed: list[set[str]] = []
    for ver in ENERGYPLUS_VERSIONS:
        pc = get_schema(ver).get_parsing_cache("Output:Table:SummaryReports")
        assert pc is not None
        if "enum" in pc.ext_inner_props["report_name"]:
            listed.append(_schema_choices(get_schema(ver), "Output:Table:SummaryReports", "report_name", group=True))
    every = listed[0].intersection(*listed[1:])
    assert _alias("AnyOutputTableSummaryReportsReportName") == every
    assert every < _alias("OutputTableSummaryReportsReportName")
    # Where every release lists the latest choices, the Any alias names the latest one.
    assert choices.AnyOutputMeterReportingFrequency is choices.OutputMeterReportingFrequency


def test_every_latest_choice_field_has_its_alias() -> None:
    schema = get_schema(LATEST_VERSION)
    for obj_type in schema.object_types:
        inner = schema.get_inner_schema(obj_type) or {}
        properties: dict[str, Any] = inner.get("properties", {})
        for field in schema.get_field_names(obj_type):
            field_schema = properties.get(field)
            if not field.isidentifier() or field_schema is None or "enum" not in field_schema:
                continue
            expected = {value for value in field_schema["enum"] if value != ""}
            if expected:
                name = gen._choice_base_name((obj_type, False, field))  # pyright: ignore[reportPrivateUsage]
                assert _alias(name) == expected, name


def test_older_choice_sets_are_named_for_their_releases() -> None:
    # 9.3 is the only release whose summary reports list is exactly this one.
    expected = _schema_choices(get_schema((9, 3, 0)), "Output:Table:SummaryReports", "report_name", group=True)
    assert _alias("OutputTableSummaryReportsReportName_v9_3") == expected


def test_module_defines_every_generated_alias() -> None:
    names = {line.split(":", 1)[0] for line in gen.generate_choices_py().splitlines() if ": TypeAlias = " in line}
    assert names == set(choices.__all__)
    assert all(hasattr(choices, name) for name in names)


def test_a_set_that_stops_and_resumes_lists_its_releases() -> None:
    versions = ((9, 0, 1), (9, 1, 0), (9, 2, 0), (9, 4, 0))
    with gen.supported_up_to((9, 4, 0)):
        assert gen._releases_text(versions) == "9.0 to 9.2 and 9.4"  # pyright: ignore[reportPrivateUsage]
        assert gen._releases_text(versions[:1]) == "9.0"  # pyright: ignore[reportPrivateUsage]
