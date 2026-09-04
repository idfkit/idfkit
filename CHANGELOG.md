# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `load_idf_with_diagnostics(path)` returns a `ParseResult` carrying the document
  and the recoverable findings from the parse: a skipped unknown type, a
  malformed object, a formatting tree that could not be linked. One call, with
  nothing to configure first.

  These findings were always produced. They went to the logging module and
  nowhere else, so reaching them meant installing a handler before the parse,
  and what arrived was a formatted sentence rather than a structured value.
  **Every log record still fires, unchanged**: this is a second way to reach
  the same findings, not a replacement, and code that installed a handler sees
  exactly what it saw before.

  There is no `strict_parsing` argument. A strict parse has no recoverable
  findings by definition, since the first one stops it. Findings that stop a
  parse still raise `IDFParseError`, which has always carried them on
  `.diagnostics`, and that path is unchanged.

  `ParseResult` is the same name, with the same two members in the same order,
  as the JavaScript library's.

- `ParseDiagnostic` gains a `code`, one of eight values shared with the
  JavaScript library and derived from this library's own exception hierarchy by
  dropping the `Error` suffix. It is the field to match on: the conformance
  corpus compares findings on `(code, line, obj_type)` and never on message
  text, so wording stays free to improve.

  Added as the last field, so every existing positional construction of a
  `ParseDiagnostic` keeps working.

- `write_idf` and `save_idf` take three new keyword arguments: `indent`,
  `comment_column`, and `ordering`. Every default is exactly what it was, so no
  file this library has ever written changes shape.

  `ordering` takes `"sorted"` or `"source"` rather than a boolean, because
  three orderings exist across the two libraries and two formats and a flag
  cannot say which is wanted. `"sorted"` is this writer's default. The
  `!-Option` directive follows it: `SortedOrder` as before when sorted, and
  `OriginalOrderTop` when `"source"`, because IDFEditor reads that line and it
  must state the order the file is actually in.

  The three land on `write_idf` and `save_idf` only. `write_epjson` and
  `save_epjson` do not take them: all three describe IDF text, and
  `write_epjson` already has an `indent` that means JSON indentation.

  Passing `preserve_formatting=True` together with any of the three raises:
  reproducing the original text and reformatting it are contradictory requests,
  and silently doing the first would be the wrong answer.

- `save_idf(doc, path, ...)` and `save_epjson(doc, path, ...)` write a serialized
  model to disk. They are the disk-writing half of the `write_*` split described
  under Changed.

- `idfkit.CONFORMANCE_LEVEL` names the cross-language conformance corpus level
  this release is checked against. It is not a version number and is not
  comparable to one: two installed libraries agree about the formats when they
  report the same level, whatever their own versions say. The equivalent constant
  is exported from `@idfkit/core` in JavaScript.

- `HTMLResult` and `HTMLTable` are importable from `idfkit.simulation`, beside
  `SQLResult`, `CSVResult`, and `ESOResult`. `result.html` returned a type you
  could not import from the module the documentation sent you to; reaching into
  `idfkit.simulation.parsers.html` is no longer necessary.

- New **"Developing with idfkit"** landing page documenting the
  `developing-with-idfkit` skill: what the bundled agent references are, why they
  are version-matched to the installed idfkit, and how to install the skill for
  Claude Code, Cursor, Copilot, Gemini CLI, and Codex.

- New **"Build your first model"** tutorial — a verified walkthrough that builds
  a complete two-storey office model from an empty document, then runs it through
  EnergyPlus and reads a result back, introducing the document, objects, the
  reference graph, validation, and the weather and simulation helpers along the
  way. ([79060da](https://github.com/idfkit/idfkit/commit/79060da))

### Changed

- **Breaking:** `write_idf()` and `write_epjson()` now only serialize to a string.
  Their `filepath` parameter is gone, along with the three `@overload` stanzas per
  function that existed solely to express "the return type depends on whether a
  path was passed". Writing to disk is now `save_idf()` and `save_epjson()`, which
  keep the `encoding`, `output_type`, `indent`, and `preserve_formatting`
  parameters they had. Replace `write_idf(doc, path)` with `save_idf(doc, path)`
  and `write_epjson(doc, path)` with `save_epjson(doc, path)`; a `write_*` call
  that already omitted the path is unchanged and now has a plain `str` return type
  instead of `str | None`. One operation, one verb: `write` serializes, `save`
  puts the result on disk.

- **Breaking:** the module surface of `idfkit` no longer leaks the names it
  imports to assemble itself. `idfkit.overload`, `idfkit.Literal`,
  `idfkit.TYPE_CHECKING`, `idfkit.logging`, `idfkit.annotations`, and
  `idfkit.PackageNotFoundError` were never in `__all__` and were never part of the
  API, but they were bound on the module and showed up in `dir(idfkit)` and in
  editor completion on `idfkit.`. Import them from `typing`, `logging`, and
  `importlib.metadata` instead.

- Reorganised the documentation site around the [Diátaxis](https://diataxis.fr)
  framework. The navigation is now grouped into Tutorials, How-to guides,
  Reference, and Explanation (plus Troubleshooting and the agent-facing
  "Developing with idfkit" bundle), each with a section landing page. Task-based
  pages were retitled to "How to …", reference material (environment variables,
  CLI) was regrouped under Reference, and design/architecture pages under
  Explanation. Every page kept its URL except `/idfkit-dev-guide/`, noted under
  Removed below. ([78035c5](https://github.com/idfkit/idfkit/commit/78035c5))

### Removed

- The `idfkit-dev-guide` page, which held a block of API notes to paste into a
  project's `CLAUDE.md`. It was published but never linked from the navigation,
  and had drifted from the library (it still advertised `doc.removeidfobject`
  and pre-0.15 `intersect_match()` behaviour). Agent-facing guidance now lives in
  the version-matched `developing-with-idfkit` skill that ships in the wheel, and
  is documented under "Developing with idfkit". **Breaking:** the
  `/idfkit-dev-guide/` URL now returns 404.

### Fixed

- `BatchResult` is a real `Sequence[SimulationResult]`. `for result in batch`,
  `enumerate(batch)`, `reversed(batch)`, `result in batch`, and slicing all worked
  at runtime through the legacy sequence protocol and were rejected by every type
  checker, so typed code had to write `batch.results` instead. The base class is
  now declared and the natural call type-checks.

- `validate_document()` no longer reports spurious range errors on EnergyPlus
  8.9.0 through 9.5.0. Those schemas are JSON Schema draft-04, where
  `exclusiveMinimum`/`exclusiveMaximum` are booleans qualifying the sibling
  `minimum`/`maximum`; idfkit compared values against the boolean itself, which
  Python coerces to `1`. Any value at or below 1 in a positive-bounded field was
  rejected, so a `Material` 0.2 m thick failed with
  `Value 0.2 must be greater than True`. Both dialects are now handled.

- Corrected the `idfkit tmy --json` help text, which claimed JSON output was
  "auto-enabled when piped if `--first`". No such auto-enabling exists — piped
  output is tab-separated (station list) or plain text (single download) unless
  `--json` is passed. Documentation updated to match. ([a32ba3d](https://github.com/idfkit/idfkit/commit/a32ba3d))
- The "Build your first model" tutorial no longer hard-codes EnergyPlus 24.1.
  It now pins the document to the version `find_energyplus()` discovers, falling
  back to `LATEST_VERSION` when EnergyPlus isn't installed. Previously the
  tutorial promised any supported version would work, but readers on EnergyPlus
  8.9 through 23.2 hit `VersionMismatchError` at the simulation step, because
  backward migration does not exist.
- Removed a hand-maintained `members:` allow-list from every API reference page.
  The lists silently dropped nine names that no longer existed in the source
  (`SQLResult.get_available_variables`, `WeatherStation.time_zone`,
  `DesignDayType.HUMIDIF_99_6`, and others) and omitted 68 real public members,
  including `SQLResult.list_variables()`. The pages now render every public
  member, so the reference matches the code in both directions.
- Corrected several documentation claims that contradicted the implementation: a
  non-existent on-disk cache for `geocode()` results (only `detect_location()`
  caches, to `ipgeo.json`), a rule that SQL key values must be upper-cased
  (`get_timeseries()` matches case-insensitively), and an outdated three-member
  `DayType` with a stale `evaluate()` signature on the schedule-evaluator page.
- Rewrote 76 cross-page link labels that still used pre-Diátaxis page titles, and
  pointed the Tutorials index's "Common tasks" link at the page of that name
  rather than at the How-to landing page.
- Listed `idfkit migrate` and `idfkit check` on the Reference landing page. Only
  `idfkit tmy` was shown, which made the CLI look weather-only.
- Restored the `Schedule:File` field semantics (`Column Number`,
  `Rows to Skip at Top`, `Column Separator`, `Minutes per Item`) to the
  schedule-evaluator page, and gave the `simulate()` parameter pointer on
  "How to run a simulation" its own heading so it appears in the page's contents.

### Migration

The two breaking changes above are both mechanical, but the `write_*` split is
worth knowing by its symptoms, because **neither failure names the cause**.

| Before                     | After                     |
| -------------------------- | ------------------------- |
| `write_idf(doc, path)`     | `save_idf(doc, path)`     |
| `write_epjson(doc, path)`  | `save_epjson(doc, path)`  |
| `write_idf(doc)`           | unchanged, now returns `str` rather than `str \| None` |

`write_epjson(doc, path)` now passes your path as the `indent` argument, so it
fails inside the serializer:

```
TypeError: can't multiply sequence by non-int of type 'PosixPath'
```

`write_idf(doc, path)` passes it as `output_type`, which is worse, because it
does not fail at all. It returns the serialized string, writes nothing, and
leaves an empty file behind. The failure surfaces later and somewhere else, most
often as:

```
VersionNotFoundError: Could not detect EnergyPlus version in file: ...
```

on a file that is empty because nothing was ever written to it. If you meet
either of these after upgrading, search your code for `write_idf(` and
`write_epjson(` called with two positional arguments.

A type checker catches both immediately: `pyright` and `mypy` both reject
`write_idf(doc, path)` against the new signature. If you run neither, the grep
above is the check.

**Checked against a real consumer.** `idfkit-mcp` upgraded across this release
with **seven changed call sites**, every one of them this rename. Nothing else in
the release reached it, and `pyright` was clean afterwards.

## [0.15.0] - 2026-07-07

### Added

- `intersect_and_match(doc, options=None)` — a robust intersect-and-split surface matcher. Coplanar, oppositely-facing surfaces from adjacent zones that overlap are split into congruent matched fragments (interior `Surface` boundary, cross-referenced) plus exterior remainders. A single long wall shared with several smaller neighbouring zones is split into one matched fragment per neighbour (the one-to-many case the old matcher could not handle). Works for walls and horizontal floor/ceiling pairs, re-homes detailed windows onto the fragment that contains them (a window straddling a cut leaves the surface unsplit and is reported, never silently clipped), and returns a typed `MatchReport`. Tunable via `MatchOptions` (tolerances, snap grid, sliver thresholds, surface classes). Convex-preserving and dependency-free. ([#173](https://github.com/idfkit/idfkit/pull/173))

### Changed

- **Breaking:** `intersect_match()` now intersects **and splits** surfaces instead of only linking congruent pairs. Previously it matched only same-size surfaces (areas within ±10%), bound each surface to at most one partner, and only considered `Wall` surfaces; it now splits partially-overlapping and unequal surfaces, matches every overlapping neighbour, and also matches `Floor`, `Ceiling`, and `Roof` surfaces. It is now a thin wrapper over `intersect_and_match()` with default options (still returns `None`). Models with partially-overlapping coplanar surfaces, or with non-wall surfaces that happen to be coplanar and oppositely-facing, will gain interior boundaries and split surfaces where the old behaviour left them exterior. ([#173](https://github.com/idfkit/idfkit/pull/173))

## [0.14.0] - 2026-06-11

### Added

- `SimulationResult` is now a context manager and exposes `SimulationResult.close()`. Closing releases the SQLite connection opened lazily by `result.sql` (and deletes the temporary copy made for remote file system backends). ([#170](https://github.com/idfkit/idfkit/pull/170))
- EnergyPlus discovery now checks `/opt/eplus`, the standard install location in Claude Code web sessions, after `$PATH` and before the platform default directories. ([#167](https://github.com/idfkit/idfkit/pull/167))

### Changed

- IDF files written by idfkit now carry a `!-Generator idfkit v<version>` header instead of crediting archetypal. ([#168](https://github.com/idfkit/idfkit/pull/168))

### Fixed

- Reading `result.sql` left a SQLite connection open for the lifetime of the `SimulationResult`, which on Windows kept an OS-level lock on `eplus.sql` and made deleting the run directory fail with `PermissionError [WinError 32]` (e.g. when the run directory lived inside a `tempfile.TemporaryDirectory`). The connection now releases its handle when the result is closed — use `with simulate(...) as result:` or call `result.close()` before removing the run directory. As a safety net, `SQLResult` also closes its connection on garbage collection. ([#170](https://github.com/idfkit/idfkit/pull/170))

## [0.13.0] - 2026-05-26

### Added

- High-performance ESO/MTR reader (`ESOResult` in `idfkit.simulation.parsers.eso`), exposed via `SimulationResult.eso` / `SimulationResult.mtr` (plus `async_eso()` / `async_mtr()` and a new `mtr_path`). EnergyPlus `.eso` Standard Output and `.mtr` Meter files share one grammar and one reader. The dictionary is parsed eagerly but the data section lazily: `get_column(name, key)` runs a single byte-level scan that float-parses only the requested variable, so reading a few variables from a large file does not pay to parse the whole file; `from_file(..., eager=True)` (or accessing `.columns`) materializes every variable in one pass into compact `array` buffers. Environment-aware (design days vs run period), handles all reporting frequencies, and uses the same reference-year-2017 timestamps and hour-24 rollover as the SQL reader. Pure Python, zero new dependencies; optional `to_dataframe()` via `idfkit[dataframes]`. Includes `benchmarks/bench_eso.py` comparing against esoreader, opyplus, pyeso, db-eplusout-reader, and the native ReadVarsESO. ([#163](https://github.com/idfkit/idfkit/pull/163))
- Agent-readable reference documentation packaged with the wheel at `idfkit/.agents/skills/developing-with-idfkit/`. Contains a `SKILL.md` dispatch document plus 16 focused topic references (document & objects, parsing, writing, schema & validation, reference tracking, geometry, geometry builders & zoning, HVAC templates, HVAC loops, simulation execution, result parsing, weather data, schedule evaluation, thermal properties, visualization, version migration). Reference files are accessible via `importlib.resources`, surfaced to AI coding assistants by tooling such as `idfkit-mcp`, and published on the docs site under "Developing with idfkit". Every code example is type-checked by pyright. ([#160](https://github.com/idfkit/idfkit/issues/160))

### Changed

- The bundled agent references are now **generated**, not hand-written. Example code lives in pyright-checked snippet files under `docs/snippets/agent_references/`; prose lives in templates under `docs/agent-references/`; `idfkit.codegen.bake_references` inlines the snippets into the bundled markdown. A strict pyright execution environment (`docs/snippets/agent_references`) keeps the drift-catching rules on, and a `check-baker` gate (mirroring `check-stubs`) fails CI if the committed bundle is stale. This replaces the ast-based validator from the initial drop, which structurally could not catch property-vs-method, dataclass-field, or argument-type drift. ([#160](https://github.com/idfkit/idfkit/issues/160))

### Fixed

- `idfkit.__version__` now reflects the installed package version, read from package metadata via `importlib.metadata`, instead of the hardcoded `"0.1.0"` literal it had always reported regardless of the installed release. Falls back to `"0.0.0+unknown"` when package metadata is unavailable (e.g. running from a source tree that was never installed). ([#161](https://github.com/idfkit/idfkit/pull/161))
- Reference-doc examples now match the live API, with pyright as the gate. The first drop's ast validator plus a manual audit fixed one batch (`set_wwr` single-float, `prep_outputs` no-kwargs, `get_holidays`/`extract_special_days` `(doc, year)`, `DesignDayManager.from_station`/`apply_to_model`, `apply_ashrae_sizing` `"general"`/`"90.1"` presets, `DesignDayType.COOLING_DB_0_4`, `SQLResult.to_dataframe` timeseries-only, `bounding_box` Optional, `footprint_courtyard` `outer_*`/`inner_*`, `ZoneFootprint(name_suffix=)`, `scale_building(factor=)`, `split_horizontal_surface(doc, surface, region=)`, `IDFParser(...).parse()`, `migrate(model, ...) -> MigrationReport`, `SimulationCache(cache_dir=)`, schedule `type_limits=`, `plot_*(sql, zones=[...])`, `plan_migration_chain(source=, target=)`, config-based `view_*` with `z_cut`/`separation`, `ColorBy.BOUNDARY_CONDITION`, `SVGConfig` fields, `gas_gap_resistance(gas_type, thickness, temperature_k, delta_t)`). Routing the examples through pyright then surfaced a further batch the validator could not see: `doc.all_objects` is a property (not `all_objects()`); `WeatherStation` fields are `country`/`state`/`wmo`/`elevation`/`timezone`/`source`/`url` (not `country_code`/`region`/`wmo_id`/`elevation_m`/`time_zone_offset_hours`/`tmyx_range`/`epw_url`/`ddy_url`); `MigrationDiff` exposes `added_object_types`/`removed_object_types`/`object_count_delta`/`field_changes`; `LayerThermalProperties.name`/`obj_type` (not `material_name`/`material_type`); `VariableInfo.frequency`, `EnvironmentInfo.name`, `OutputVariable.key`/`frequency`, `HTMLTable.title`; `validate_object(obj, schema)` requires the schema; `polygon_contains_2d` is polygon-in-polygon; `plot_day`/`plot_week` take `year`/`month`/`day` / `year`/`week`. ([#160](https://github.com/idfkit/idfkit/issues/160))

## [0.12.2] - 2026-05-19

### Added

- `idfkit.weather.designday.sanitize_ddy_file()` for cleaning a DDY file outside the downloader flow. ([#156](https://github.com/idfkit/idfkit/issues/156))

### Fixed

- `WeatherDownloader.download()` now blanks out the literal `N` placeholder token found in `SizingPeriod:DesignDay` numeric fields of extracted `.ddy` files. Some OneBuilding TMYx archives ship this placeholder when source data is unavailable, which previously caused EnergyPlus to reject the file with a type-constraint fatal. Affected design day names are logged at WARNING. ([#156](https://github.com/idfkit/idfkit/issues/156))
- EnergyPlus subprocesses (simulation, ExpandObjects, migration transition binaries) now have stdin explicitly redirected to `DEVNULL` instead of inheriting the parent's stdin. Prevents hangs on Windows when the parent process has a console attached. ([#158](https://github.com/idfkit/idfkit/pull/158))

## [0.12.1] - 2026-05-06

### Fixed

- RDD/MDD parsers now match `Output:VariableDictionary, IDF` lines that include the `Zone Average` / `HVAC Sum` descriptor between `!-` and the units bracket. Previously `OutputVariableIndex.from_simulation()` silently returned zero variables on real EnergyPlus output. ([#155](https://github.com/idfkit/idfkit/pull/155))
- MDD parser now recognizes `Output:Meter:Cumulative`, `Output:Meter:MeterFileOnly`, and `Output:Meter:Cumulative:MeterFileOnly` lines instead of silently skipping them. Cumulative variants are dropped from the result for now (a TODO tracks modeling all four variants on `OutputMeter`). ([#155](https://github.com/idfkit/idfkit/pull/155))

### Added

- RDD/MDD parsers now also accept the `Output:VariableDictionary, Regular` format (the EnergyPlus default). Both formats produce the same `OutputVariable` / `OutputMeter` set; for Regular lines, `key` is synthesized as `"*"` and `frequency` as `"hourly"` to match the IDF form. ([#155](https://github.com/idfkit/idfkit/pull/155))
- `DictionaryParseWarning` is emitted when `parse_rdd` / `parse_mdd` produce zero entries from a non-empty file, surfacing format mismatches that would otherwise fail silently. ([#155](https://github.com/idfkit/idfkit/pull/155))

## [0.12.0] - 2026-05-05

### Added

- `simulate()` now forwards a `preprocessor_timeout` parameter to ExpandObjects, Slab, and Basement runs. ([#152](https://github.com/idfkit/idfkit/pull/152))

### Changed

- IDFObject field reads are roughly 4x faster after hot-path slimming. ([f973e60](https://github.com/idfkit/idfkit/commit/f973e60))
- IDFObject field writes are ~43% faster via `to_python_name` caching. ([e76f83e](https://github.com/idfkit/idfkit/commit/e76f83e))
- IDFCollection string lookups are faster: string keys now bypass the type-check branch in `__getitem__`. ([4bde898](https://github.com/idfkit/idfkit/commit/4bde898))

## [0.11.1] - 2026-04-28

### Fixed

- `IDFObject.copy()` now preserves `wrapper_key` and `ext_inner_names`, so copies of objects with extensible arrays round-trip correctly. ([#150](https://github.com/idfkit/idfkit/pull/150))

## [0.11.0] - 2026-04-28

### Added

- Selective ZIP extraction in weather downloads via a new `only=` parameter on `download()`, so callers can pull just the EPW or DDY without unpacking the whole archive. ([#144](https://github.com/idfkit/idfkit/pull/144))

### Changed

- Typing improvements across the public API: `write_idf` / `write_epjson` overloads ([#145](https://github.com/idfkit/idfkit/pull/145)), `IDFCollection.get` overload ([#146](https://github.com/idfkit/idfkit/pull/146)), `TimeSeriesResult.to_dataframe()` annotated as `pd.DataFrame` ([#147](https://github.com/idfkit/idfkit/pull/147)), and `TimeSeriesResult.plot` backend parameter narrowed ([#148](https://github.com/idfkit/idfkit/pull/148)).

## [0.10.3] - 2026-04-27

### Changed

- `IDFDocument.add()` now emits a `DeprecationWarning` when it has to rewrite flat-extensible kwargs into the canonical array form. Callers should pass extensibles using the canonical API. ([#143](https://github.com/idfkit/idfkit/pull/143))

## [0.10.2] - 2026-04-27

### Fixed

- `FieldDescription.field_type` now preserves `anyOf` unions from the schema instead of collapsing them, so introspection of polymorphic fields is accurate. ([#142](https://github.com/idfkit/idfkit/pull/142))

## [0.10.1] - 2026-04-27

### Fixed

- Weather station index now falls back to the bundled index when the user cache was written by an older schema version, instead of failing on load. ([dcde4b7](https://github.com/idfkit/idfkit/commit/dcde4b7))

## [0.10.0] - 2026-04-27

### Added

- Canonical extensible-array storage and access API. Extensible groups are now read and written as arrays through a stable interface rather than via flat indexed kwargs. ([#140](https://github.com/idfkit/idfkit/pull/140))
- `idfkit tmy --nearby` auto-detects the user's location from IP and finds the closest TMY stations. ([#134](https://github.com/idfkit/idfkit/pull/134))
- Throttled freshness check for the weather station index, so the bundled index is updated when stale without nagging on every run. ([#137](https://github.com/idfkit/idfkit/pull/137))
- Environment variables reference page in the documentation. ([#138](https://github.com/idfkit/idfkit/pull/138))
- Richer station filters and a mobile-friendly layout in the TMY browser. ([#139](https://github.com/idfkit/idfkit/pull/139))
- Docstrings are now threaded into generated type stubs. ([#141](https://github.com/idfkit/idfkit/pull/141))

### Changed

- **Breaking:** `IDFDocument.add()`'s `data=` kwarg has been renamed to `fields=`. Update call sites accordingly. ([28c742d](https://github.com/idfkit/idfkit/commit/28c742d))
- Weather station index switched from Excel to KML format and now carries climate-zone metadata. The optional `[weather]` extra is no longer required for the bundled index to work — references to it have been removed from the docs. ([#136](https://github.com/idfkit/idfkit/pull/136), [4499c5c](https://github.com/idfkit/idfkit/commit/4499c5c))
- `doc["Type"]` access path was reworked alongside the canonical extensible API; behavior is preserved but the underlying storage is different. ([#141](https://github.com/idfkit/idfkit/pull/141))

## [0.9.0] - 2026-04-21

### Added

- `idfkit tmy` CLI subcommand for fetching TMYx weather data, with VHS tape recordings in the docs. ([#132](https://github.com/idfkit/idfkit/pull/132), [#133](https://github.com/idfkit/idfkit/pull/133))

## [0.8.0] - 2026-04-16

### Added

- EnergyPlus 26.1.0 schema is now bundled and supported. ([6060742](https://github.com/idfkit/idfkit/commit/6060742))
- `idfkit migrate` CLI subcommand for IDF version migration from the command line. ([#131](https://github.com/idfkit/idfkit/pull/131))

## [0.7.1] - 2026-04-16

### Fixed

- Concurrent migrations no longer collide on `audit.out`: each migration step runs in its own isolated CWD. ([#130](https://github.com/idfkit/idfkit/pull/130))

## [0.7.0] - 2026-04-15

### Added

- IDF version migration with both synchronous and asynchronous orchestrators, so models can be upgraded across EnergyPlus versions programmatically. ([#128](https://github.com/idfkit/idfkit/pull/128))

## [0.6.5] - 2026-04-03

### Added

- Windows drive root is now consulted by EnergyPlus auto-discovery, so installs at `C:\EnergyPlusV*` are found without manual configuration. ([#122](https://github.com/idfkit/idfkit/pull/122))

### Changed

- Project test coverage raised to ~100% across schedules, weather, simulation, parsers, document/schema, validation, introspection, exceptions, geometry, codegen, visualization, and the eppy compatibility layer. No user-visible API change, but the regression surface is now substantially smaller. ([#100](https://github.com/idfkit/idfkit/pull/100), [#101](https://github.com/idfkit/idfkit/pull/101), [#102](https://github.com/idfkit/idfkit/pull/102), [#103](https://github.com/idfkit/idfkit/pull/103), [#104](https://github.com/idfkit/idfkit/pull/104), [#105](https://github.com/idfkit/idfkit/pull/105), [#106](https://github.com/idfkit/idfkit/pull/106), [#110](https://github.com/idfkit/idfkit/pull/110), [#111](https://github.com/idfkit/idfkit/pull/111), [#112](https://github.com/idfkit/idfkit/pull/112), [#113](https://github.com/idfkit/idfkit/pull/113), [#114](https://github.com/idfkit/idfkit/pull/114), [#115](https://github.com/idfkit/idfkit/pull/115), [#116](https://github.com/idfkit/idfkit/pull/116), [#117](https://github.com/idfkit/idfkit/pull/117), [#118](https://github.com/idfkit/idfkit/pull/118))

## [0.6.4] - 2026-03-31

### Fixed

- Four bugs surfaced by stress testing across the parser and document layers. ([#99](https://github.com/idfkit/idfkit/pull/99))
- `Version` is now normalized as a regular collection entry rather than a special-cased object, fixing inconsistencies in iteration and lookup. ([#119](https://github.com/idfkit/idfkit/pull/119), [#120](https://github.com/idfkit/idfkit/pull/120))

## [0.6.3] - 2026-03-27

### Changed

- Public API surface of the `objects` module has been tightened — internal helpers no longer leak as importable names. ([#98](https://github.com/idfkit/idfkit/pull/98))
- Extensible field names are now normalized to the epJSON schema convention. ([#97](https://github.com/idfkit/idfkit/pull/97))

### Fixed

- Extensible field handling: `field_order` is maintained correctly across mutations, and schedule parsing no longer mishandles extensible groups. ([#96](https://github.com/idfkit/idfkit/pull/96))
- Various dead URLs across the project documentation. ([#84](https://github.com/idfkit/idfkit/pull/84))

## [0.6.2] - 2026-03-26

### Added

- `IDFCollection` now supports retrieval of unnamed/singleton objects. ([#94](https://github.com/idfkit/idfkit/pull/94))

## [0.6.1] - 2026-03-26

### Fixed

- Extensible field introspection and reference detection now work correctly. ([#92](https://github.com/idfkit/idfkit/pull/92), [#93](https://github.com/idfkit/idfkit/pull/93))

## [0.6.0] - 2026-03-25

### Changed

- **Breaking:** Strict field access is now the default — accessing an unknown field raises instead of returning `None`. Pass `strict=False` to opt out where the previous behavior is needed. ([#91](https://github.com/idfkit/idfkit/pull/91))
- **Breaking:** `strict` parameters were renamed across the API for consistency. Review call sites that pass strict-mode flags. ([#90](https://github.com/idfkit/idfkit/pull/90))
- Exception hierarchy now inherits from a common `IdfKitError` base and includes documentation URLs pointing at the relevant concept page. ([#89](https://github.com/idfkit/idfkit/pull/89))
- CST scanner optimized with regex; extensible field handling sped up. ([#82](https://github.com/idfkit/idfkit/pull/82))

### Added

- Documentation URL builder module that backs the new exception messages. ([#85](https://github.com/idfkit/idfkit/pull/85))
- PR doc preview comments now link to the changed pages. ([#83](https://github.com/idfkit/idfkit/pull/83))

### Fixed

- IDF type name resolution is now case-insensitive, matching EnergyPlus's own behavior. ([#81](https://github.com/idfkit/idfkit/pull/81))
- `set_wwr` now preserves construction names and cross-references on the rebuilt fenestration. ([#80](https://github.com/idfkit/idfkit/pull/80))

## [0.5.0] - 2026-03-14

### Added

- `new_document()` accepts a `strict` parameter to control field-access strictness up-front. ([#74](https://github.com/idfkit/idfkit/pull/74))
- Type-safety and performance improvements for `IDFDocument` and stub generation. ([#75](https://github.com/idfkit/idfkit/pull/75))

### Changed

- Renamed the experiment parameter from `experiment` to `runnable` in batch APIs. ([#73](https://github.com/idfkit/idfkit/pull/73))

### Fixed

- `get_surface_coords` no longer crashes when `number_of_vertices` is blank. ([#78](https://github.com/idfkit/idfkit/pull/78))

## [0.4.0] - 2026-03-03

### Added

- Weather search and direct download by EPW filename, in addition to lookup by station ID and coordinates. ([#69](https://github.com/idfkit/idfkit/pull/69))
- Block stacking with `base_elevation` and horizontal adjacency linking, for assembling multi-block models programmatically. ([#67](https://github.com/idfkit/idfkit/pull/67))

## [0.3.1] - 2026-03-02

### Fixed

- Strict IDF parser now raises informative errors on malformed input instead of failing partway through with unrelated tracebacks. ([#64](https://github.com/idfkit/idfkit/pull/64))

## [0.3.0] - 2026-02-26

### Added

- EnergyPlus version compatibility checker for Python files (used to validate that snippets and user code target a supported version). ([#59](https://github.com/idfkit/idfkit/pull/59))
- `validate_document` and `new_document` now seed and enforce schema singleton uniqueness via `maxProperties`. ([#58](https://github.com/idfkit/idfkit/pull/58), [#60](https://github.com/idfkit/idfkit/pull/60), [#61](https://github.com/idfkit/idfkit/pull/61))
- Enhanced extensible-object handling in `IDFDocument` and introspection. ([#57](https://github.com/idfkit/idfkit/pull/57))

## [0.2.0] - 2026-02-20

### Added

- Comprehensive logging throughout idfkit modules — every parser, simulation, and weather subsystem now logs at consistent levels. ([#53](https://github.com/idfkit/idfkit/pull/53))
- User documentation for the `create_building` API and the zoning module. ([#52](https://github.com/idfkit/idfkit/pull/52))

### Changed

- IDF/epJSON loading is approximately 2.4x faster via per-type parsing cache. ([18e620e](https://github.com/idfkit/idfkit/commit/18e620e))
- Lookup of all objects of a given type is approximately 60x faster: `__getitem__` now uses a single dict lookup instead of scanning. ([568e2d5](https://github.com/idfkit/idfkit/commit/568e2d5))

## [0.1.1] - 2026-02-12

### Added

- Comprehensive eppy compatibility layer (`idfkit._compat`) and additional geometry operations, easing migration from eppy. ([#46](https://github.com/idfkit/idfkit/pull/46))
- `AsyncFileSystem` protocol so async simulation pipelines no longer block the event loop on filesystem I/O. ([#40](https://github.com/idfkit/idfkit/pull/40))
- Documentation tutorials for using idfkit with Scythe distributed experiments and Celery. ([#42](https://github.com/idfkit/idfkit/pull/42), [#43](https://github.com/idfkit/idfkit/pull/43))

### Fixed

- Tutorial bugs surfaced during end-to-end cloud simulation testing. ([#45](https://github.com/idfkit/idfkit/pull/45), [#47](https://github.com/idfkit/idfkit/pull/47))
- HTML result detection in the simulation result parser. ([#47](https://github.com/idfkit/idfkit/pull/47))

## [0.1.0] - 2026-02-11

Initial public release.

### Added

- IDF and epJSON parser, writer, and round-trip support.
- `IDFDocument`, `IDFObject`, and name-indexed `IDFCollection` core data model with O(1) lookups. ([#3](https://github.com/idfkit/idfkit/pull/3))
- `ReferenceGraph` that tracks cross-object references and updates automatically on rename.
- Schema-driven validation against bundled epJSON schemas.
- Bundled schemas covering EnergyPlus 8.9.0 through 25.2.0. ([#4](https://github.com/idfkit/idfkit/pull/4))
- EnergyPlus simulation execution: synchronous, asynchronous (`async_simulate`), and batch runners with content-addressed result caching. ([#10](https://github.com/idfkit/idfkit/pull/10), [#17](https://github.com/idfkit/idfkit/pull/17))
- Preprocessor support for `ExpandObjects`, `Slab`, and `Basement`. ([#15](https://github.com/idfkit/idfkit/pull/15))
- Simulation progress callbacks. ([#18](https://github.com/idfkit/idfkit/pull/18))
- Weather module: ~17k-station search index, EPW/DDY download with local cache, design-day injection, and Nominatim-backed geocoding. ([#8](https://github.com/idfkit/idfkit/pull/8))
- Schedule evaluation engine covering all eight EnergyPlus schedule types, usable without running a simulation.
- Thermal property calculations: R/U-values, SHGC, gas mixture properties.
- 3D building geometry visualization with SVG output, including dark-mode support. ([#13](https://github.com/idfkit/idfkit/pull/13))
- Performance benchmarks comparing idfkit against eppy and opyplus. ([#5](https://github.com/idfkit/idfkit/pull/5))
- MkDocs Material documentation site with a full API reference, an eppy migration guide, and a getting-started Jupyter notebook. ([#2](https://github.com/idfkit/idfkit/pull/2))

[unreleased]: https://github.com/idfkit/idfkit/compare/v0.13.0...HEAD
[Unreleased]: https://github.com/idfkit/idfkit/compare/v0.15.0...HEAD
[0.15.0]: https://github.com/idfkit/idfkit/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/idfkit/idfkit/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/idfkit/idfkit/compare/v0.12.2...v0.13.0
[0.12.2]: https://github.com/idfkit/idfkit/compare/v0.12.1...v0.12.2
[0.12.1]: https://github.com/idfkit/idfkit/compare/v0.12.0...v0.12.1
[0.12.0]: https://github.com/idfkit/idfkit/compare/v0.11.1...v0.12.0
[0.11.1]: https://github.com/idfkit/idfkit/compare/v0.11.0...v0.11.1
[0.11.0]: https://github.com/idfkit/idfkit/compare/v0.10.3...v0.11.0
[0.10.3]: https://github.com/idfkit/idfkit/compare/v0.10.2...v0.10.3
[0.10.2]: https://github.com/idfkit/idfkit/compare/0.10.1...v0.10.2
[0.10.1]: https://github.com/idfkit/idfkit/compare/0.10.0...0.10.1
[0.10.0]: https://github.com/idfkit/idfkit/compare/0.9.0...0.10.0
[0.9.0]: https://github.com/idfkit/idfkit/compare/0.8.0...0.9.0
[0.8.0]: https://github.com/idfkit/idfkit/compare/0.7.1...0.8.0
[0.7.1]: https://github.com/idfkit/idfkit/compare/0.7.0...0.7.1
[0.7.0]: https://github.com/idfkit/idfkit/compare/0.6.5...0.7.0
[0.6.5]: https://github.com/idfkit/idfkit/compare/v0.6.4...0.6.5
[0.6.4]: https://github.com/idfkit/idfkit/compare/v0.6.3...v0.6.4
[0.6.3]: https://github.com/idfkit/idfkit/compare/v0.6.2...v0.6.3
[0.6.2]: https://github.com/idfkit/idfkit/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/idfkit/idfkit/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/idfkit/idfkit/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/idfkit/idfkit/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/idfkit/idfkit/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/idfkit/idfkit/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/idfkit/idfkit/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/idfkit/idfkit/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/idfkit/idfkit/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/idfkit/idfkit/releases/tag/v0.1.0
