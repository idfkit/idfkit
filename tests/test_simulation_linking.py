"""Result linking on the paired fixtures (spec 014, User Story 3, SC-004).

Every test reads the committed ``(IDF, SQL)`` pairs under ``tests/fixtures/simulation/linked/``; none needs
EnergyPlus.
"""

from __future__ import annotations

import json
import re
import shutil
from functools import cache
from pathlib import Path

import pytest

from idfkit import IDFDocument, load_idf
from idfkit._graph_common import ObjectKey
from idfkit.simulation.linking import ResultIndex, _Context, _Model, _resolve
from idfkit.simulation.result import SimulationResult

LINKED = Path(__file__).parent / "fixtures" / "simulation" / "linked"
FIXTURES = sorted(path.stem for path in LINKED.glob("*.sql"))
TEMPLATE_FIXTURES = {"HVACTemplate-5ZoneVAVWaterCooled"}
"""Unexpanded HVACTemplate models: the objects EnergyPlus sized are not in the input."""

SC004_SOURCES = ("sizing", "timeseries", "tabular")


def _run(tmp: Path, fixture: str) -> SimulationResult:
    tmp.mkdir(parents=True, exist_ok=True)
    shutil.copy(LINKED / f"{fixture}.sql", tmp / "eplusout.sql")
    return SimulationResult(run_dir=tmp, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0)


@cache
def _built(fixture: str) -> tuple[IDFDocument, ResultIndex]:
    import tempfile

    doc = load_idf(LINKED / f"{fixture}.idf")
    run = _run(Path(tempfile.mkdtemp(prefix=f"linked_{fixture}_")), fixture)
    return doc, ResultIndex.build(doc, run, run_revision=doc.revision, run_model_hash="fixture")


def _rates(index: ResultIndex) -> dict[str, tuple[int, int]]:
    """``source -> (linked, total)`` from the index's tally."""
    tally = index._tally  # pyright: ignore[reportPrivateUsage]
    out: dict[str, tuple[int, int]] = {}
    for source in (*SC004_SOURCES, "message"):
        linked = tally.resolved_by.get(source, 0)
        out[source] = (linked, linked + sum(1 for s, _ in index.unresolved if s == source))
    return out


# ------------------------------------------------------------------------------------------ SC-004


def test_sc004_at_least_95_percent_linked_per_source() -> None:
    totals = dict.fromkeys(SC004_SOURCES, (0, 0))
    for fixture in FIXTURES:
        if fixture in TEMPLATE_FIXTURES:
            continue
        for source, (linked, total) in _rates(_built(fixture)[1]).items():
            if source in totals:
                held = totals[source]
                totals[source] = (held[0] + linked, held[1] + total)
    for source, (linked, total) in totals.items():
        assert total > 0, source
        assert linked / total >= 0.95, f"{source}: {linked}/{total} linked"


@pytest.mark.parametrize("fixture", [f for f in FIXTURES if f not in TEMPLATE_FIXTURES])
def test_each_paired_run_links_at_least_95_percent(fixture: str) -> None:
    for source, (linked, total) in _rates(_built(fixture)[1]).items():
        if source in SC004_SOURCES and total:
            assert linked / total >= 0.95, f"{fixture} {source}: {linked}/{total}"


def test_template_model_lists_what_it_cannot_link() -> None:
    _, index = _built("HVACTemplate-5ZoneVAVWaterCooled")
    coverage = index.coverage
    kinds = {part.kind for part in coverage.uncovered}
    assert {"hvac_template", "unlinked_result"} <= kinds
    assert coverage.partial
    assert coverage.unresolved == len(index.unresolved) > 0
    unlinked = next(part for part in coverage.uncovered if part.kind == "unlinked_result")
    assert all(example.object_type == "Unresolved" for example in unlinked.examples)
    assert len(unlinked.examples) <= 3


def test_unresolved_items_are_listed_never_dropped() -> None:
    for fixture in FIXTURES:
        _, index = _built(fixture)
        coverage = index.coverage
        assert coverage.unresolved == len(index.unresolved)
        assert all(source in {"sizing", "timeseries", "tabular", "message"} for source, _ in index.unresolved)


# ---------------------------------------------------------------------------------- linking rules


def test_shared_names_across_types_stay_separate() -> None:
    # ShopWithSimplePVT names a Zone and a People object ZN_1_FLR_1_SEC_1.
    _, index = _built("ShopWithSimplePVT")
    zone = index.facts(ObjectKey("Zone", "ZN_1_FLR_1_SEC_1"))
    people = index.facts(ObjectKey("People", "ZN_1_FLR_1_SEC_1"))
    assert zone
    assert ObjectKey("Zone", "ZN_1_FLR_1_SEC_1") != ObjectKey("People", "ZN_1_FLR_1_SEC_1")
    assert {fact.where for fact in zone}.isdisjoint({fact.where for fact in people})
    assert index.variables(ObjectKey("Zone", "ZN_1_FLR_1_SEC_1"))


def test_lookup_is_case_insensitive_and_returns_model_spelling() -> None:
    _, index = _built("MultiStory")
    results = index.for_object(ObjectKey("zone", "gnd west zone"))
    assert results.object.name == "Gnd West Zone"
    assert results.object.object_type == "Zone"
    assert results.facts
    assert "Zone Mean Air Temperature" in results.available_variables


def test_zone_facts_carry_the_multiplier() -> None:
    # MultiStory: GND CENTER ZONE has Multiplier 4; MID CENTER ZONE has 4 times a list multiplier of 8.
    _, index = _built("MultiStory")
    assert {fact.multiplier for fact in index.facts(ObjectKey("Zone", "GND CENTER ZONE"))} == {4}
    assert {fact.multiplier for fact in index.facts(ObjectKey("Zone", "MID CENTER ZONE"))} == {32}
    assert {fact.multiplier for fact in index.facts(ObjectKey("Zone", "GND WEST ZONE"))} == {1}
    coil = index.facts(ObjectKey("Coil:Cooling:DX:SingleSpeed", "Top East OA DX Coil"))
    assert coil
    assert {fact.multiplier for fact in coil} == {None}


def test_sizing_facts_name_their_row() -> None:
    _, index = _built("5ZoneAirCooled")
    facts = index.facts(ObjectKey("Boiler:HotWater", "Central Boiler"))
    sizing = [fact for fact in facts if fact.source == "sizing"]
    assert sizing
    assert all(re.fullmatch(r"ComponentSizes#\d+", fact.where) for fact in sizing)
    assert all(fact.metric == fact.metric.lower() and " " not in fact.metric for fact in sizing)
    assert facts[0].source == "sizing"


def test_tabular_facts_name_report_table_row_and_column() -> None:
    _, index = _built("MultiStory")
    tabular = [f for f in index.facts(ObjectKey("Zone", "Gnd West Zone")) if f.source == "tabular"]
    assert tabular
    assert all(len(fact.where.split("/")) >= 4 for fact in tabular)


def test_nodes_link_as_nodes() -> None:
    _, index = _built("5ZoneAirCooled")
    variables = index.variables(ObjectKey("Node", "Mixed Air Node 1"))
    assert "System Node Temperature" in variables


def test_aggregates_are_classified_not_linked_to_objects() -> None:
    _, index = _built("MultiStory")
    assert ObjectKey("Aggregate", "Environment") in index.keys
    assert all(raw.strip().upper() not in {"TOTAL", "ENVIRONMENT"} for _, raw in index.unresolved)


def test_mirrored_shading_and_zonelist_composites_link_by_convention() -> None:
    _, index = _built("MultiStory")
    lights = index.facts(ObjectKey("Lights", "Office Buildings"))
    assert any("TOP WEST ZONE OFFICE BUILDINGS" in fact.where.upper() for fact in lights)


def test_objects_with_ranks_by_value() -> None:
    _, index = _built("5ZoneAirCooled")
    metric = index.facts(ObjectKey("Boiler:HotWater", "Central Boiler"))[0].metric
    ranked = index.objects_with(metric, top=3)
    assert ranked
    values = [fact.value for _, fact in ranked]
    assert all(isinstance(value, float) for value in values)
    numbers = [value for value in values if isinstance(value, float)]
    assert numbers == sorted(numbers, reverse=True)
    assert len(ranked) <= 3


# ---------------------------------------------------------------------------------------- messages


def test_messages_carry_kind_objects_and_occurrences() -> None:
    _, index = _built("MultiStory")
    coil = index.for_object(ObjectKey("Coil:Cooling:DX:SingleSpeed", "Top East OA DX Coil"))
    assert coil.messages
    message = coil.messages[0]
    assert message.kind == "dxcoil.low_outlet_temp"
    assert message.severity == "warning"
    assert message.occurrences >= 1
    assert "\n" not in message.text
    assert all(link.key is not None for link in message.objects)


def test_first_seen_is_read_from_the_continuation_text() -> None:
    _, index = _built("ShopWithSimplePVT")
    timed = [m for m in index.messages if m.first_seen is not None]
    assert timed
    assert all(re.fullmatch(r".+ \d\d/\d\d \d\d:\d\d", m.first_seen or "") for m in timed)
    assert any(m.first_seen == "RUN PERIOD 1 01/04 17:20" for m in timed)


def test_messages_are_deduplicated_by_kind_for_one_object() -> None:
    _, index = _built("MultiStory")
    for key in index.keys:
        kinds = [message.kind for message in index.messages_for(key)]
        assert len(kinds) == len(set(kinds))


def test_info_messages_are_not_linked() -> None:
    for fixture in FIXTURES:
        assert all(message.severity != "info" for message in _built(fixture)[1].messages)


# -------------------------------------------------------------------------------- object results


def test_for_object_returns_neighbours_with_their_top_fact() -> None:
    _, index = _built("5ZoneAirCooled")
    results = index.for_object(ObjectKey("Boiler:HotWater", "Central Boiler"))
    assert results.neighbours
    assert len(results.neighbours) <= 20
    assert all(neighbour.object != results.object for neighbour in results.neighbours)
    assert results.coverage == index.coverage


def test_for_object_on_an_unknown_key_is_empty() -> None:
    _, index = _built("5ZoneAirCooled")
    results = index.for_object(ObjectKey("Zone", "No Such Zone"))
    assert results.facts == ()
    assert results.messages == ()
    assert results.available_variables == ()
    assert results.neighbours == ()


# ---------------------------------------------------------------------------- freshness and build


def test_index_is_fresh_until_the_document_changes(tmp_path: Path) -> None:
    doc = load_idf(LINKED / "1ZoneUncontrolled.idf")
    index = ResultIndex.build(doc, _run(tmp_path, "1ZoneUncontrolled"), run_revision=doc.revision, run_model_hash="h")
    assert index.is_fresh(doc)
    assert index.is_fresh(doc, "h")
    assert not index.is_fresh(doc, "other")
    zone = next(iter(doc["Zone"]))
    zone.multiplier = 2
    assert not index.is_fresh(doc)


def test_build_is_cached_per_run(tmp_path: Path) -> None:
    doc = load_idf(LINKED / "1ZoneUncontrolled.idf")
    run = _run(tmp_path, "1ZoneUncontrolled")
    first = ResultIndex.build(doc, run, run_revision=doc.revision, run_model_hash="h")
    assert ResultIndex.build(doc, run, run_revision=doc.revision, run_model_hash="h") is first
    assert ResultIndex.build(doc, run, run_revision=doc.revision, run_model_hash="other") is not first


def test_build_never_reads_report_data(tmp_path: Path) -> None:
    doc = load_idf(LINKED / "5ZoneAirCooled.idf")
    run = _run(tmp_path, "5ZoneAirCooled")
    sql = run.sql
    assert sql is not None
    statements: list[str] = []
    sql._conn.set_trace_callback(statements.append)  # pyright: ignore[reportPrivateUsage]
    ResultIndex.build(doc, run, run_revision=doc.revision, run_model_hash="h")
    assert statements
    assert not [s for s in statements if re.search(r"\bReportData\b(?!Dictionary)", s)]


def test_build_without_sql_output_is_an_error(tmp_path: Path) -> None:
    doc = load_idf(LINKED / "1ZoneUncontrolled.idf")
    run = SimulationResult(run_dir=tmp_path, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0)
    with pytest.raises(ValueError, match=r"Output:SQLite"):
        ResultIndex.build(doc, run, run_revision=doc.revision, run_model_hash="h")


# ------------------------------------------------------------------------- hand-checked sample


def _hand_checked() -> list[dict[str, str]]:
    data = json.loads((LINKED / "hand_checked_links.json").read_text(encoding="utf-8"))
    return data["links"]


def test_hand_checked_sample_has_100_links() -> None:
    links = _hand_checked()
    assert len(links) == 100
    assert {link["source"] for link in links} == {"sizing", "timeseries", "tabular", "message"}


@pytest.mark.parametrize("fixture", sorted({link["fixture"] for link in _hand_checked()}))
def test_hand_checked_links_resolve_as_checked(fixture: str) -> None:
    model = _Model(_built(fixture)[0])
    wrong: list[str] = []
    for link in (entry for entry in _hand_checked() if entry["fixture"] == fixture):
        context = _Context(link["source"], link["hint"])  # type: ignore[arg-type]
        found = _resolve(link["raw"], context, model, substring=link["source"] == "timeseries")
        expected = ObjectKey(link["object_type"], link["name"])
        if found is None or found.key != expected or found.confidence != link["confidence"]:
            wrong.append(f"{link['raw']!r} -> {found} (checked: {expected}, {link['confidence']})")
    assert not wrong, "\n".join(wrong)


def test_no_hand_checked_exact_link_is_wrong() -> None:
    exact = [link for link in _hand_checked() if link["confidence"] == "exact"]
    assert exact
    for link in exact:
        doc = _built(link["fixture"])[0]
        objects = doc.collections.get(link["object_type"])
        assert objects is not None, link
        assert any((obj.name or "").upper() == link["name"].upper() for obj in objects), link
        assert link["hint"].upper() == link["object_type"].upper(), link


def test_zone_keyed_tables_link_to_the_zone_not_a_same_named_schedule(tmp_path: Path) -> None:
    doc = load_idf(LINKED / "5ZoneAirCooled.idf")
    doc.add("Schedule:Constant", "SPACE1-1", hourly_value=1.0, validate=False)
    index = ResultIndex.build(doc, _run(tmp_path, "5ZoneAirCooled"), run_revision=doc.revision, run_model_hash="h")
    zone_rows = [f.where for f in index.facts(ObjectKey("Zone", "SPACE1-1")) if "Thermostat Schedules" in f.where]
    assert zone_rows
    assert not [f for f in index.facts(ObjectKey("Schedule:Constant", "SPACE1-1")) if "Thermostat" in f.where]
