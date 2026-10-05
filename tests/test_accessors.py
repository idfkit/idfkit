"""Tests for document accessor name resolution (:mod:`idfkit._accessors`).

The sweep tests are the important ones. A resolver verified on a few hand-picked
examples with special uppercase in name
"""

from __future__ import annotations

import collections
import gc
import pickle
import re
import weakref

import pytest

from idfkit import IDFDocument, new_document
from idfkit._accessors import (
    _SNAKE_OVERRIDES,
    MEMBER_CONFLICT,
    AccessorAttributeError,
    AccessorResolver,
    pluralize,
    snake_case,
)
from idfkit.objects import IDFCollection
from idfkit.schema import get_schema, get_schema_manager
from idfkit.versions import ENERGYPLUS_VERSIONS, LATEST_VERSION

# --------------------------------------------------------------------------
# snake_case: acronyms, colons, hyphens, digits
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("obj_type", "expected"),
    [
        ("Zone", "zone"),
        ("AirLoopHVAC", "air_loop_hvac"),
        ("AirLoopHVAC:UnitarySystem", "air_loop_hvac_unitary_system"),
        ("Coil:Cooling:DX:SingleSpeed", "coil_cooling_dx_single_speed"),
        ("AirTerminal:SingleDuct:VAV:Reheat", "air_terminal_single_duct_vav_reheat"),
        # HVACTemplate must not split as hvact_emplate
        ("HVACTemplate:Zone:VAV", "hvac_template_zone_vav"),
        ("ZoneHVAC:EquipmentList", "zone_hvac_equipment_list"),
        ("Chiller:Electric:ReformulatedEIR", "chiller_electric_reformulated_eir"),
        (
            "ElectricLoadCenter:Storage:LiIonNMCBattery",
            "electric_load_center_storage_li_ion_nmc_battery",
        ),
        ("ElectricLoadCenter:Inverter:PVWatts", "electric_load_center_inverter_pv_watts"),
        # The three types the case-boundary rule splits badly, fixed by _SNAKE_OVERRIDES.
        ("Output:SQLite", "output_sqlite"),
        ("Site:GroundTemperature:FCfactorMethod", "site_ground_temperature_fcfactor_method"),
        ("Daylighting:DELight:ComplexFenestration", "daylighting_delight_complex_fenestration"),
        # The one hyphenated type in the schema -- must be a valid identifier.
        (
            "PhotovoltaicPerformance:EquivalentOne-Diode",
            "photovoltaic_performance_equivalent_one_diode",
        ),
    ],
)
def test_snake_case(obj_type: str, expected: str) -> None:
    assert snake_case(obj_type) == expected
    assert expected.isidentifier()


# --------------------------------------------------------------------------
# pluralize: the real cases
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("singular", "expected"),
    [
        ("zone", "zones"),
        ("branch", "branches"),  # sibilant
        ("refrigeration_case", "refrigeration_cases"),
        ("curve_fan_pressure_rise", "curve_fan_pressure_rises"),
        ("internal_mass", "internal_masses"),  # singular ending in ss
        ("material_no_mass", "material_no_masses"),
        ("lights", "lights"),  # already plural, not 'lightses'
        ("output_schedules", "output_schedules"),
        ("convergence_limits", "convergence_limits"),
        ("people", "people"),  # irregular, not 'peoples'
        # Singular nouns that end in s, which "already plural" would leave alone.
        ("window_material_gas", "window_material_gases"),
        ("humidifier_steam_gas", "humidifier_steam_gases"),
        ("material_property_phase_change_hysteresis", "material_property_phase_change_hystereses"),
    ],
)
def test_pluralize(singular: str, expected: str) -> None:
    assert pluralize(singular) == expected


# --------------------------------------------------------------------------
# Resolution
# --------------------------------------------------------------------------


@pytest.fixture
def resolver() -> AccessorResolver:
    return AccessorResolver([
        "Zone",
        "ZoneList",
        "AirLoopHVAC",
        "AirLoopHVAC:UnitarySystem",
        "Branch",
        "BranchList",
        "Lights",
        "People",
        "InternalMass",
        "Coil:Cooling:DX:SingleSpeed",
        "Schedule:Compact",
    ])


def test_canonical_attribute_names(resolver: AccessorResolver) -> None:
    assert resolver.attr_for["Zone"] == "zones"
    assert resolver.attr_for["AirLoopHVAC"] == "air_loop_hvacs"
    assert resolver.attr_for["Coil:Cooling:DX:SingleSpeed"] == "coil_cooling_dx_single_speeds"
    assert resolver.attr_for["Lights"] == "lights"
    assert resolver.attr_for["People"] == "people"


def test_plural_singular_and_raw_all_resolve(resolver: AccessorResolver) -> None:
    for form in ("air_loop_hvacs", "air_loop_hvac", "AirLoopHVAC", "airloophvac", "AIRLOOPHVAC"):
        assert resolver.resolve(form) == "AirLoopHVAC"


def test_raw_name_with_colons_resolves(resolver: AccessorResolver) -> None:
    assert resolver.resolve("Coil:Cooling:DX:SingleSpeed") == "Coil:Cooling:DX:SingleSpeed"
    assert resolver.resolve("CoilCoolingDXSingleSpeed") == "Coil:Cooling:DX:SingleSpeed"


@pytest.mark.parametrize(
    ("spelling", "expected"),
    [
        ("Schedule_Compact", "Schedule:Compact"),
        ("schedule_compact", "Schedule:Compact"),
        ("SCHEDULE_COMPACT", "Schedule:Compact"),
        ("AirLoopHVAC_UnitarySystem", "AirLoopHVAC:UnitarySystem"),
        ("airloophvac_unitarysystem", "AirLoopHVAC:UnitarySystem"),
        ("Coil_Cooling_DX_SingleSpeed", "Coil:Cooling:DX:SingleSpeed"),
    ],
)
def test_raw_name_with_underscores_for_colons_resolves(
    resolver: AccessorResolver, spelling: str, expected: str
) -> None:
    """These spellings resolved on main through a case-insensitive ':' -> '_' match."""
    assert resolver.resolve(spelling) == expected


@pytest.mark.parametrize(
    "bad", ["z_o_n_e", "zone_", "zone_s", "_zone", "airloophvacs", "air_loophvacs", "AIR_LOOP_HVACS"]
)
def test_separator_noise_does_not_resolve(resolver: AccessorResolver, bad: str) -> None:
    assert resolver.resolve(bad) is None


def test_case_never_changes_which_type(resolver: AccessorResolver) -> None:
    """No string resolves to one type while its re-cased twin resolves to another."""
    clashes = [k for k in resolver._raw if k in resolver._exact and resolver._exact[k] != resolver._raw[k]]
    assert not clashes


def test_unknown_resolves_to_none(resolver: AccessorResolver) -> None:
    assert resolver.resolve("totally_not_a_type") is None


def test_suggestions_on_typo(resolver: AccessorResolver) -> None:
    assert "zones" in resolver.suggest("zonez")
    assert "branches" in resolver.suggest("brnaches")
    assert "lights" in resolver.suggest("lightss")


def test_attribute_error_names_the_intent(resolver: AccessorResolver) -> None:
    msg = str(AccessorAttributeError("Document", "zonez", resolver))
    assert "zonez" in msg
    assert "Did you mean" in msg
    assert "zones" in msg
    assert "(Zone)" in msg  # the object type is shown alongside


def test_attribute_error_stays_plain_when_nothing_is_close(resolver: AccessorResolver) -> None:
    msg = str(AccessorAttributeError("Document", "qqqqqqqqqq", resolver))
    assert "Did you mean" not in msg


def test_attribute_error_without_resolver_is_plain() -> None:
    assert str(AccessorAttributeError("Document", "zonez")) == "'Document' object has no attribute 'zonez'"


def test_attribute_error_is_an_attribute_error(resolver: AccessorResolver) -> None:
    err = AccessorAttributeError("Document", "zonez", resolver)
    assert isinstance(err, AttributeError)
    assert err.name == "zonez"


def test_attribute_error_pickles_as_plain_attribute_error(resolver: AccessorResolver) -> None:
    """Crossing a process boundary must not fail on the three-argument __init__."""
    restored = pickle.loads(pickle.dumps(AccessorAttributeError("Document", "zonez", resolver)))  # noqa: S301
    assert type(restored) is AttributeError
    assert "zones" in str(restored)


def test_hasattr_never_computes_suggestions(empty_doc: IDFDocument, monkeypatch: pytest.MonkeyPatch) -> None:
    """Deterministic rather than timed: a silent probe must never reach suggest()."""

    def boom(*_args: object, **_kwargs: object) -> list[str]:
        raise AssertionError("suggest() ran on a silent probe")  # noqa: TRY003

    monkeypatch.setattr(AccessorResolver, "suggest", boom)
    assert hasattr(empty_doc, "definitely_not_a_type") is False
    assert getattr(empty_doc, "definitely_not_a_type", None) is None


# --------------------------------------------------------------------------
# Integration with IDFDocument.__getattr__
# --------------------------------------------------------------------------


def test_document_resolves_arbitrary_type_by_attribute() -> None:
    doc = new_document(version=LATEST_VERSION)
    for form in ("air_loop_hvacs", "air_loop_hvac", "AirLoopHVAC"):
        coll = getattr(doc, form)
        assert isinstance(coll, IDFCollection)
    doc.add("AirLoopHVAC", "Main Loop", validate=False)
    assert len(doc.air_loop_hvacs) == 1
    assert len(doc.coil_cooling_dx_single_speeds) == 0


@pytest.mark.parametrize("good", ["zones", "zone", "Zone", "ZONE"])
def test_document_documented_forms_resolve(empty_doc: IDFDocument, good: str) -> None:
    # An empty type hands back a fresh collection each time, so compare the type, not identity.
    assert getattr(empty_doc, good).obj_type == "Zone"


def test_document_z_o_n_e_does_not_resolve(empty_doc: IDFDocument) -> None:
    """From the #202 review: "tighten _key a bit (doc.z_o_n_e shouldn't resolve)".

    Underscores are never stripped, so interleaving them through a type name is a
    typo that fails loudly instead of silently returning ``Zone``.
    """
    assert empty_doc.zones.obj_type == "Zone"  # the real name still works
    with pytest.raises(AttributeError, match="z_o_n_e"):
        _ = empty_doc.z_o_n_e


@pytest.mark.parametrize(
    ("spelling", "expected"),
    [
        # The spellings #202 review found raising once a schema was loaded.
        ("Site_Location", "Site:Location"),
        ("Output_Variable", "Output:Variable"),
        ("BuildingSurface_Detailed", "BuildingSurface:Detailed"),
        ("SITE_LOCATION", "Site:Location"),
    ],
)
def test_document_underscore_spellings_still_resolve(empty_doc: IDFDocument, spelling: str, expected: str) -> None:
    assert getattr(empty_doc, spelling).obj_type == expected


@pytest.mark.parametrize(
    ("spelling", "expected"),
    [
        ("output_sqlite", "Output:SQLite"),
        ("output_sqlites", "Output:SQLite"),
        ("site_ground_temperature_fcfactor_methods", "Site:GroundTemperature:FCfactorMethod"),
        ("daylighting_delight_complex_fenestrations", "Daylighting:DELight:ComplexFenestration"),
        ("window_material_gases", "WindowMaterial:Gas"),
        ("window_material_gas", "WindowMaterial:Gas"),
        ("humidifier_steam_gases", "Humidifier:Steam:Gas"),
        ("material_property_phase_change_hystereses", "MaterialProperty:PhaseChangeHysteresis"),
    ],
)
def test_document_naming_cases_from_review(empty_doc: IDFDocument, spelling: str, expected: str) -> None:
    """The names #202 review found misspelled or missing, and the plural of each."""
    assert getattr(empty_doc, spelling).obj_type == expected


@pytest.mark.parametrize("bad", ["output_sq_lite", "output_sq_lites", "daylighting_de_light_complex_fenestration"])
def test_document_old_awkward_names_are_gone(empty_doc: IDFDocument, bad: str) -> None:
    """These never shipped, so the rule's first answer is replaced, not kept as an alias."""
    assert not hasattr(empty_doc, bad)


@pytest.mark.parametrize("bad", ["z_o_n_e", "zone_", "zone_s", "airloophvacs"])
def test_document_separator_noise_does_not_resolve(empty_doc: IDFDocument, bad: str) -> None:
    assert not hasattr(empty_doc, bad)


def test_derived_name_wins_over_shorthand(empty_doc: IDFDocument) -> None:
    """#202 review decision: singular and plural of one name must agree."""
    assert empty_doc.shading_building.obj_type == "Shading:Building"
    assert empty_doc.shading_buildings.obj_type == "Shading:Building"
    assert empty_doc.shading_building_detaileds.obj_type == "Shading:Building:Detailed"


def test_losing_shorthand_is_recorded_not_registered() -> None:
    r = AccessorResolver(
        ["Shading:Building", "Shading:Building:Detailed", "Zone"],
        shorthands={"shading_building": "Shading:Building:Detailed", "zones": "Zone"},
    )
    assert r.conflicts == {"shading_building": ("Shading:Building:Detailed", "Shading:Building")}
    assert r.shorthands == {"zones": "Zone"}
    assert r.resolve("shading_building") == "Shading:Building"


def test_shorthand_for_a_type_missing_from_the_schema_is_skipped() -> None:
    r = AccessorResolver(["Zone"], shorthands={"ideal_loads": "ZoneHVAC:IdealLoadsAirSystem"})
    assert r.resolve("ideal_loads") is None
    assert "ideal_loads" not in r.names()


def test_member_names_are_recorded_and_never_suggested() -> None:
    r = AccessorResolver(["Version", "Zone"], shorthands={"version": "Version"}, reserved={"version"})
    assert r.conflicts["version"] == ("Version", MEMBER_CONFLICT)
    assert "version" not in r.names()
    assert "versions" in r.names()


def test_version_property_is_untouched(empty_doc: IDFDocument) -> None:
    """A real member always wins; __getattr__ never fires for it."""
    assert not isinstance(empty_doc.version, IDFCollection)
    assert empty_doc.versions.obj_type == "Version"


def test_suggestions_include_shorthands(empty_doc: IDFDocument) -> None:
    with pytest.raises(AttributeError, match="ideal_loads"):
        _ = empty_doc.ideal_load


def test_document_without_schema_still_uses_shorthands() -> None:
    doc = IDFDocument(version=LATEST_VERSION)  # no schema
    with pytest.raises(AttributeError, match="object has no attribute 'nonsense'"):
        _ = doc.nonsense


def test_probing_an_uninitialised_document_does_not_recurse() -> None:
    """copy.deepcopy and pickle build the object without __init__, then probe it.

    Without the '_' guard, __getattr__ reaches for self._schema, which is also
    missing, re-enters __getattr__, and recurses until RecursionError.
    """
    blank = IDFDocument.__new__(IDFDocument)
    assert not hasattr(blank, "__setstate__")
    assert not hasattr(blank, "_schema")
    with pytest.raises(AttributeError):
        _ = blank.zones


def test_dir_lists_generated_and_shorthand_names(empty_doc: IDFDocument) -> None:
    names = dir(empty_doc)
    assert "air_loop_hvacs" in names  # derived from the schema
    assert "zones" in names  # shorthand
    assert "shading_building_detaileds" in names
    assert "air_loop_hvac" not in names  # singular resolves, but is left out of completion
    assert "AirLoopHVAC" not in names  # so is the raw type name


def test_dir_keeps_real_members(empty_doc: IDFDocument) -> None:
    names = dir(empty_doc)
    assert "add" in names
    assert "version" in names
    assert names == sorted(names)


def test_dir_names_all_resolve(empty_doc: IDFDocument) -> None:
    """Completion must never offer a name that then raises."""
    resolver = empty_doc._accessor_resolver_or_none()
    assert resolver is not None
    for name in resolver.names():
        assert isinstance(getattr(empty_doc, name), IDFCollection), name


def test_dir_without_schema_lists_shorthands_but_not_derived_names() -> None:
    """Only the shorthands resolve without a schema, so only they are offered."""
    doc = IDFDocument(version=LATEST_VERSION)  # no schema
    names = dir(doc)
    assert "add" in names
    assert "zones" in names
    assert "air_loop_hvacs" not in names
    assert names == sorted(names)
    assert len(names) == len(set(names))


def test_dir_has_no_duplicates(empty_doc: IDFDocument) -> None:
    names = dir(empty_doc)
    assert len(names) == len(set(names))


def test_names_is_sorted_and_the_copy_is_safe_to_mutate(resolver: AccessorResolver) -> None:
    names = resolver.names()
    assert names == sorted(names)
    names.clear()
    assert resolver.names()  # clearing the copy did not touch the resolver


def test_reserved_name_never_resolves_but_other_casing_does() -> None:
    r = AccessorResolver(["Version", "Zone"], shorthands={"version": "Version"}, reserved={"version"})
    assert r.resolve("version") is None
    assert r.resolve("Version") == "Version"  # not the member, so still reachable
    assert r.resolve("VERSION") == "Version"
    assert r.resolve("versions") == "Version"


def _broken_property(self: object) -> object:
    raise AttributeError("the getter itself failed")  # noqa: TRY003


@pytest.mark.parametrize("with_schema", [True, False])
def test_failing_member_getter_is_not_masked_by_an_accessor(monkeypatch: pytest.MonkeyPatch, with_schema: bool) -> None:
    """A property that raises AttributeError falls back to __getattr__, which must not answer.

    Without this, ``doc.version`` would quietly return the ``Version`` collection
    instead of failing, with or without a schema loaded.
    """
    monkeypatch.setattr(IDFDocument, "version", property(_broken_property))
    doc = new_document(version=LATEST_VERSION) if with_schema else IDFDocument(version=LATEST_VERSION)
    with pytest.raises(AttributeError):
        _ = doc.version


def test_document_attribute_error_suggests(empty_doc: IDFDocument) -> None:
    with pytest.raises(AttributeError, match="Did you mean"):
        _ = empty_doc.zonez


def test_document_without_schema_falls_back() -> None:
    doc = IDFDocument(version=LATEST_VERSION)  # no schema
    with pytest.raises(AttributeError):
        _ = doc.air_loop_hvacs


def test_resolver_is_built_once_per_schema() -> None:
    doc = new_document(version=LATEST_VERSION)
    first = doc._accessor_resolver_or_none()
    assert first is not None
    assert doc._accessor_resolver_or_none() is first
    assert new_document(version=LATEST_VERSION)._accessor_resolver_or_none() is first  # same cached schema


def test_schema_is_collectable_after_accessor_use() -> None:
    """The resolver must not pin its schema once the schema manager lets go of it.

    Uses the oldest bundled version so no shared fixture holds the same schema.
    """
    doc = new_document(version=ENERGYPLUS_VERSIONS[0])
    _ = doc.air_loop_hvacs  # forces the resolver to build
    ref = weakref.ref(doc.schema)

    del doc, _
    get_schema_manager().clear_cache()
    gc.collect()

    assert ref() is None, "schema still pinned after clear_cache()"


# --------------------------------------------------------------------------
# Sweeps across every bundled schema
# --------------------------------------------------------------------------


@pytest.fixture(params=ENERGYPLUS_VERSIONS, ids=lambda v: f"{v[0]}.{v[1]}.{v[2]}")
def all_obj_types(request: pytest.FixtureRequest) -> list[str]:
    version: tuple[int, int, int] = request.param
    return sorted(get_schema(version).object_types)


def test_no_attribute_name_collisions(all_obj_types: list[str]) -> None:
    r = AccessorResolver(all_obj_types)
    counts = collections.Counter(r.attr_for.values())
    dupes = {a: n for a, n in counts.items() if n > 1}
    assert not dupes, f"attribute name collisions: {dupes}"


def test_every_type_resolves_from_every_alias_form(all_obj_types: list[str]) -> None:
    r = AccessorResolver(all_obj_types)
    failures: list[tuple[str, str, str | None]] = []
    for obj_type in all_obj_types:
        underscored = obj_type.replace(":", "_")
        for form in (r.attr_for[obj_type], snake_case(obj_type), obj_type, underscored):
            if r.resolve(form) != obj_type:
                failures.append((obj_type, form, r.resolve(form)))
    assert not failures, f"{len(failures)} alias failures, first 10: {failures[:10]}"


def test_case_never_changes_which_type_in_any_schema(all_obj_types: list[str]) -> None:
    r = AccessorResolver(all_obj_types)
    clashes = {k: (r._exact[k], r._raw[k]) for k in r._raw if k in r._exact and r._exact[k] != r._raw[k]}
    assert not clashes, f"re-casing changes the type: {clashes}"


# Every "CAPITALS run + lowercase" fragment in any object type, across all bundled
# schemas. The case-boundary rule splits the last capital off with the lowercase run,
# which is right when an acronym is followed by a word and wrong when it is not.
# Adding to this set is a deliberate, reviewed act: check how the new fragment splits,
# and if it splits badly add the type to _SNAKE_OVERRIDES.
REVIEWED_ACRONYM_FRAGMENTS = {
    "HVACTemplate",  # splits correctly: hvac_template
    "HVACEquipment",  # hvac_equipment
    "HVACSystem",  # hvac_system
    "NMCBattery",  # nmc_battery
    "PVWatts",  # pv_watts
    "VAVChangeover",  # vav_changeover
    "SQLite",  # split badly, fixed by _SNAKE_OVERRIDES
    "DELight",  # split badly, fixed by _SNAKE_OVERRIDES
    "FCfactor",  # split badly, fixed by _SNAKE_OVERRIDES
}


def test_snake_case_has_no_unreviewed_splits(all_obj_types: list[str]) -> None:
    found = {m.group(0) for t in all_obj_types for m in re.finditer(r"[A-Z]{2,}[a-z]+", t)}
    assert found <= REVIEWED_ACRONYM_FRAGMENTS, (
        f"new acronym fragments to review: {sorted(found - REVIEWED_ACRONYM_FRAGMENTS)}; see REVIEWED_ACRONYM_FRAGMENTS"
    )


def test_snake_case_overrides_name_real_types() -> None:
    """A typo in the override table would silently do nothing, so check each key exists somewhere."""
    known = {t for v in ENERGYPLUS_VERSIONS for t in get_schema(v).object_types}
    missing = sorted(set(_SNAKE_OVERRIDES) - known)
    assert not missing, f"overrides for types in no bundled schema: {missing}"


def test_attribute_names_are_valid_identifiers(all_obj_types: list[str]) -> None:
    r = AccessorResolver(all_obj_types)
    bad = [a for a in r.attr_for.values() if not a.isidentifier()]
    assert not bad, f"not valid Python identifiers: {bad[:10]}"


def test_no_attribute_name_shadows_a_document_member(all_obj_types: list[str]) -> None:
    """An accessor must never collide with a real attribute or method.

    ``__getattr__`` only fires when normal lookup fails, so a collision would
    silently make that object type unreachable by attribute rather than raise.
    """
    reserved = set(dir(IDFDocument))
    r = AccessorResolver(all_obj_types)
    clashes = {a: t for t, a in r.attr_for.items() if a in reserved}
    assert not clashes, f"accessor names shadow IDFDocument members: {clashes}"


# --------------------------------------------------------------------------
# Sweeps through the real document, in every bundled schema
#
# The sweeps above build AccessorResolver directly, with no shorthands and no
# reserved names, so they never see the precedence rules document.py applies.
# That is how shading_building and version slipped through review. These go
# through getattr on a real document instead, and check every alias, not only
# the canonical plural.
# --------------------------------------------------------------------------

# Names a real IDFDocument member owns. Adding to this set is a deliberate,
# reviewed act; a new EnergyPlus release introducing a clash fails here first.
EXPECTED_MEMBER_CONFLICTS = {"version"}


@pytest.fixture(params=ENERGYPLUS_VERSIONS, ids=lambda v: f"{v[0]}.{v[1]}.{v[2]}")
def version_doc(request: pytest.FixtureRequest) -> IDFDocument:
    version: tuple[int, int, int] = request.param
    return new_document(version=version)


def _doc_resolver(doc: IDFDocument) -> AccessorResolver:
    resolver = doc._accessor_resolver_or_none()
    assert resolver is not None
    return resolver


def test_every_alias_resolves_through_getattr(version_doc: IDFDocument) -> None:
    """Plural, singular, raw type name, and every shorthand, via __getattr__."""
    r = _doc_resolver(version_doc)
    failures: list[tuple[str, str, str]] = []
    for obj_type in r.attr_for:
        singular = snake_case(obj_type)
        forms = {pluralize(singular), singular, obj_type, obj_type.replace(":", "_")} - set(r.conflicts)
        for form in forms:
            got = getattr(version_doc, form).obj_type
            if got != obj_type:
                failures.append((form, obj_type, got))
    for alias, target in r.shorthands.items():
        got = getattr(version_doc, alias).obj_type
        if got != target:
            failures.append((alias, target, got))
    assert not failures, f"{len(failures)} (form, expected, got), first 10: {failures[:10]}"


def test_no_shorthand_contradicts_a_derived_name(version_doc: IDFDocument) -> None:
    """A losing shorthand must be deleted from _PYTHON_TO_IDF, not merely overridden.

    The stub generator reads _PYTHON_TO_IDF, so a shorthand left in place would be
    typed as one object type while runtime returns another.
    """
    r = _doc_resolver(version_doc)
    lost = {a: pair for a, pair in r.conflicts.items() if pair[1] != MEMBER_CONFLICT}
    assert not lost, f"remove from _PYTHON_TO_IDF: {lost}"


def test_member_conflicts_are_known(version_doc: IDFDocument) -> None:
    r = _doc_resolver(version_doc)
    members = {a for a, pair in r.conflicts.items() if pair[1] == MEMBER_CONFLICT}
    # <= rather than ==: a given clash need not exist in every schema version.
    assert members <= EXPECTED_MEMBER_CONFLICTS, f"new member clashes: {members - EXPECTED_MEMBER_CONFLICTS}"


def test_member_conflicts_still_return_the_member(version_doc: IDFDocument) -> None:
    r = _doc_resolver(version_doc)
    for name, (_, winner) in r.conflicts.items():
        if winner == MEMBER_CONFLICT:
            assert not isinstance(getattr(version_doc, name), IDFCollection), name


def test_case_never_changes_which_type_with_shorthands(version_doc: IDFDocument) -> None:
    """The same guarantee as above, on the resolver the document really uses."""
    r = _doc_resolver(version_doc)
    clashes = {k: (r._exact[k], r._raw[k]) for k in r._raw if k in r._exact and r._exact[k] != r._raw[k]}
    assert not clashes, f"re-casing changes the type: {clashes}"
