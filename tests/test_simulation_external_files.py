"""Tests for the external files an EnergyPlus model reads, and how the cache key covers them (#216)."""

from __future__ import annotations

import gzip
import json
import re
from pathlib import Path

import pytest

from idfkit import new_document
from idfkit.document import IDFDocument
from idfkit.simulation._external_files import (
    EXTERNAL_FILE_FIELDS,
    ExternalFileRef,
    external_file_refs,
    resolve_external_file,
    search_dirs_for_run,
    uncacheable_reason,
)
from idfkit.simulation.cache import SimulationCache

SCHEMAS = Path(__file__).parent.parent / "src" / "idfkit" / "schemas"


def _schedule_file_model(file_name: str) -> IDFDocument:
    model = new_document()
    model.add(
        "Schedule:File",
        "Staged",
        file_name=file_name,
        column_number=1,
        rows_to_skip_at_top=0,
        validate=False,
    )
    return model


@pytest.fixture
def cache(tmp_path: Path) -> SimulationCache:
    return SimulationCache(cache_dir=tmp_path / "cache")


@pytest.fixture
def weather_file(tmp_path: Path) -> Path:
    epw = tmp_path / "weather.epw"
    epw.write_text("LOCATION,Chicago\n")
    return epw


class TestExternalFileRefs:
    def test_no_refs_in_empty_model(self) -> None:
        assert external_file_refs(new_document()) == []

    def test_schedule_file(self) -> None:
        refs = external_file_refs(_schedule_file_model("data/hourly.csv"))
        assert refs == [ExternalFileRef("Schedule:File", "file_name", "data/hourly.csv")]

    def test_duplicates_collapse_and_sort(self) -> None:
        model = _schedule_file_model("b.csv")
        model.add("Schedule:File", "Second", file_name="a.csv", column_number=1, validate=False)
        model.add("Schedule:File", "Third", file_name="b.csv", column_number=2, validate=False)
        assert [r.value for r in external_file_refs(model)] == ["a.csv", "b.csv"]

    def test_blank_window_data_file_uses_default_name(self) -> None:
        model = new_document()
        model.add("Construction:WindowDataFile", "Glazing", validate=False)
        assert external_file_refs(model) == [
            ExternalFileRef("Construction:WindowDataFile", "file_name", "Window5DataFile.dat")
        ]

    def test_table_lookup(self) -> None:
        model = new_document()
        model.add(
            "Table:Lookup", "Curve", independent_variable_list_name="Vars", external_file_name="t.csv", validate=False
        )
        assert [r.obj_type for r in external_file_refs(model)] == ["Table:Lookup"]


class TestResolveExternalFile:
    def test_absolute(self, tmp_path: Path) -> None:
        f = tmp_path / "a.csv"
        f.write_text("1\n")
        assert resolve_external_file(str(f), []) == f
        assert resolve_external_file(str(tmp_path / "missing.csv"), []) is None

    def test_relative_tries_dirs_in_order(self, tmp_path: Path) -> None:
        first, second = tmp_path / "run", tmp_path / "exe"
        (first / "data").mkdir(parents=True)
        second.mkdir()
        (second / "x.csv").write_text("exe\n")
        assert resolve_external_file("x.csv", [first, second]) == second / "x.csv"
        (first / "x.csv").write_text("run\n")
        assert resolve_external_file("x.csv", [first, second]) == first / "x.csv"

    def test_backslashes_are_separators(self, tmp_path: Path) -> None:
        (tmp_path / "data").mkdir()
        (tmp_path / "data" / "x.csv").write_text("1\n")
        assert resolve_external_file("data\\x.csv", [tmp_path]) is not None

    def test_directory_is_not_a_file(self, tmp_path: Path) -> None:
        (tmp_path / "data").mkdir()
        assert resolve_external_file("data", [tmp_path]) is None

    def test_search_dirs_for_run(self, tmp_path: Path) -> None:
        exe = tmp_path / "ep" / "energyplus"
        assert search_dirs_for_run(None, exe) == [exe.resolve().parent]
        assert search_dirs_for_run(tmp_path / "run", exe) == [(tmp_path / "run").resolve(), exe.resolve().parent]


class TestComputeKeyCoversExternalFiles:
    def test_model_without_refs_is_unaffected_by_search_dirs(
        self, cache: SimulationCache, weather_file: Path, tmp_path: Path
    ) -> None:
        model = new_document()
        assert cache.compute_key(model, weather_file) == cache.compute_key(model, weather_file, search_dirs=[tmp_path])

    def test_changed_relative_file_changes_key(
        self, cache: SimulationCache, weather_file: Path, tmp_path: Path
    ) -> None:
        run_dir = tmp_path / "run"
        (run_dir / "data").mkdir(parents=True)
        csv = run_dir / "data" / "hourly.csv"
        model = _schedule_file_model("data/hourly.csv")

        csv.write_text("0.5\n")
        k1 = cache.compute_key(model, weather_file, search_dirs=[run_dir])
        csv.write_text("1.0\n")
        k2 = cache.compute_key(model, weather_file, search_dirs=[run_dir])
        csv.write_text("0.5\n")
        k3 = cache.compute_key(model, weather_file, search_dirs=[run_dir])
        assert k1 != k2
        assert k1 == k3

    def test_changed_absolute_file_changes_key(
        self, cache: SimulationCache, weather_file: Path, tmp_path: Path
    ) -> None:
        csv = tmp_path / "elsewhere" / "occ.csv"
        csv.parent.mkdir()
        model = _schedule_file_model(str(csv))
        csv.write_text("1\n")
        k1 = cache.compute_key(model, weather_file)
        csv.write_text("2\n")
        assert cache.compute_key(model, weather_file) != k1

    def test_missing_file_differs_from_present_file(
        self, cache: SimulationCache, weather_file: Path, tmp_path: Path
    ) -> None:
        model = _schedule_file_model("hourly.csv")
        missing = cache.compute_key(model, weather_file, search_dirs=[tmp_path])
        (tmp_path / "hourly.csv").write_text("")
        assert cache.compute_key(model, weather_file, search_dirs=[tmp_path]) != missing

    def test_same_content_elsewhere_gives_same_key(
        self, cache: SimulationCache, weather_file: Path, tmp_path: Path
    ) -> None:
        """The key follows content, so two fresh run directories staged alike share one entry."""
        a, b = tmp_path / "a", tmp_path / "b"
        for d in (a, b):
            d.mkdir()
            (d / "hourly.csv").write_text("1\n")
        model = _schedule_file_model("hourly.csv")
        assert cache.compute_key(model, weather_file, search_dirs=[a]) == cache.compute_key(
            model, weather_file, search_dirs=[b]
        )


class TestUncacheableReason:
    def test_plain_model_is_cacheable(self) -> None:
        assert uncacheable_reason(new_document()) is None

    def test_python_plugin(self) -> None:
        model = new_document()
        model.add("PythonPlugin:Instance", "Plugin", python_module_name="plugin", plugin_class_name="P", validate=False)
        reason = uncacheable_reason(model)
        assert reason is not None
        assert "PythonPlugin:Instance" in reason

    @pytest.mark.parametrize("mode", ["PtolemyServer", "FunctionalMockupUnitExport", "ptolemyserver"])
    def test_cosimulation_interfaces(self, mode: str) -> None:
        model = new_document()
        model.add("ExternalInterface", "", name_of_external_interface=mode, validate=False)
        reason = uncacheable_reason(model)
        assert reason is not None
        assert mode in reason

    def test_fmu_import_is_cacheable(self) -> None:
        """An imported FMU is a file the key hashes, so the run stays cacheable."""
        model = new_document()
        model.add("ExternalInterface", "", name_of_external_interface="FunctionalMockupUnitImport", validate=False)
        assert uncacheable_reason(model) is None


# Fields whose names look like file references but do not name a file EnergyPlus reads as input.
_NOT_INPUT_FILES = {
    ("Parametric:FileNameSuffix", "suffix_for_file_name_in_run"),  # names output files of a parametric run
}
# Fields that do name input files, on object types that make a run uncacheable instead.
_UNCACHEABLE_FIELDS = {
    ("PythonPlugin:Instance", "python_module_name"),
    ("PythonPlugin:SearchPaths", "search_path"),
}
_FILE_FIELD = re.compile(r"file|path|director|module_name", re.IGNORECASE)


def _file_like_fields(schema: dict[str, object]) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    properties = schema["properties"]
    assert isinstance(properties, dict)
    for obj_type, spec in properties.items():
        for body in spec.get("patternProperties", {}).values():
            for name, field in body.get("properties", {}).items():
                candidates = [(name, field)]
                if field.get("type") == "array":
                    candidates = list(field.get("items", {}).get("properties", {}).items())
                for sub_name, sub in candidates:
                    if not _FILE_FIELD.search(sub_name) or "enum" in sub or "object_list" in sub:
                        continue
                    if sub.get("type") not in (None, "string") or "node_name" in sub_name:
                        continue
                    found.add((obj_type, re.sub(r"_\d+$", "", sub_name)))
    return found


@pytest.mark.parametrize("schema_dir", sorted(p.name for p in SCHEMAS.glob("V*")))
def test_every_file_field_in_every_bundled_schema_is_classified(schema_dir: str) -> None:
    """A schema that adds a file-reading field fails here until the cache key covers it.

    The cache key hashes files named by EXTERNAL_FILE_FIELDS.  An unclassified
    field would be a file EnergyPlus reads that the key ignores, which is the
    stale-hit bug of #216.
    """
    with gzip.open(SCHEMAS / schema_dir / "Energy+.schema.epJSON.gz") as f:
        schema = json.loads(f.read())
    covered = {(t, f) for t, fs in EXTERNAL_FILE_FIELDS.items() for f in fs}
    unclassified = _file_like_fields(schema) - covered - _NOT_INPUT_FILES - _UNCACHEABLE_FIELDS
    assert not unclassified, f"{schema_dir}: classify these file fields for the cache key: {sorted(unclassified)}"
