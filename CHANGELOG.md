# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.12.0] - 2026-05-05

### Added

- `simulate()` now forwards a `preprocessor_timeout` parameter to ExpandObjects, Slab, and Basement runs.

### Changed

- IDFObject field reads are roughly 4x faster and field writes ~43% faster after hot-path slimming and `to_python_name` caching.
- IDFCollection string lookups are faster: string keys now bypass the type-check branch in `__getitem__`.

## [0.11.1] - 2026-04-28

### Fixed

- `IDFObject.copy()` now preserves `wrapper_key` and `ext_inner_names`, so copies of objects with extensible arrays round-trip correctly.

## [0.11.0] - 2026-04-28

### Added

- Selective ZIP extraction in weather downloads via a new `only=` parameter on `download()`, so callers can pull just the EPW or DDY without unpacking the whole archive.

### Changed

- Typing improvements across the public API: `write_idf` / `write_epjson` overloads, `IDFCollection.get` overload, `TimeSeriesResult.to_dataframe()` annotated as `pd.DataFrame`, and `TimeSeriesResult.plot` backend parameter narrowed.

## [0.10.3] - 2026-04-27

### Changed

- `IDFDocument.add()` now emits a `DeprecationWarning` when it has to rewrite flat-extensible kwargs into the canonical array form. Callers should pass extensibles using the canonical API.

## [0.10.2] - 2026-04-27

### Fixed

- `FieldDescription.field_type` now preserves `anyOf` unions from the schema instead of collapsing them, so introspection of polymorphic fields is accurate.

## [0.10.1] - 2026-04-27

### Fixed

- Weather station index now falls back to the bundled index when the user cache was written by an older schema version, instead of failing on load.

## [0.10.0] - 2026-04-27

### Added

- Canonical extensible-array storage and access API. Extensible groups are now read and written as arrays through a stable interface rather than via flat indexed kwargs.
- `idfkit tmy --nearby` auto-detects the user's location from IP and finds the closest TMY stations.
- Throttled freshness check for the weather station index, so the bundled index is updated when stale without nagging on every run.
- Environment variables reference page in the documentation.
- Richer station filters and a mobile-friendly layout in the TMY browser.
- Docstrings are now threaded into generated type stubs.

### Changed

- **Breaking:** `IDFDocument.add()`'s `data=` kwarg has been renamed to `fields=`. Update call sites accordingly.
- Weather station index switched from Excel to KML format and now carries climate-zone metadata. The optional `[weather]` extra is no longer required for the bundled index to work — references to it have been removed from the docs.
- `doc["Type"]` access path was reworked alongside the canonical extensible API; behavior is preserved but the underlying storage is different.

## [0.9.0] - 2026-04-21

### Added

- `idfkit tmy` CLI subcommand for fetching TMYx weather data, with VHS tape recordings in the docs.

## [0.8.0] - 2026-04-16

### Added

- EnergyPlus 26.1.0 schema is now bundled and supported.
- `idfkit migrate` CLI subcommand for IDF version migration from the command line.

## [0.7.1] - 2026-04-16

### Fixed

- Concurrent migrations no longer collide on `audit.out`: each migration step runs in its own isolated CWD.

## [0.7.0] - 2026-04-15

### Added

- IDF version migration with both synchronous and asynchronous orchestrators, so models can be upgraded across EnergyPlus versions programmatically.

## [0.6.5] - 2026-04-03

### Added

- Windows drive root is now consulted by EnergyPlus auto-discovery, so installs at `C:\EnergyPlusV*` are found without manual configuration.

### Changed

- Project test coverage raised to ~100% across schedules, weather, simulation, parsers, document/schema, validation, introspection, exceptions, geometry, codegen, visualization, and the eppy compatibility layer. No user-visible API change, but the regression surface is now substantially smaller.

## [0.6.4] - 2026-03-31

### Fixed

- Four bugs surfaced by stress testing across the parser and document layers.
- `Version` is now normalized as a regular collection entry rather than a special-cased object, fixing inconsistencies in iteration and lookup.

## [0.6.3] - 2026-03-27

### Changed

- Public API surface of the `objects` module has been tightened — internal helpers no longer leak as importable names.
- Extensible field names are now normalized to the epJSON schema convention.

### Fixed

- Extensible field handling: `field_order` is maintained correctly across mutations, and schedule parsing no longer mishandles extensible groups.
- Various dead URLs across the project documentation.

## [0.6.2] - 2026-03-26

### Added

- `IDFCollection` now supports retrieval of unnamed/singleton objects.

## [0.6.1] - 2026-03-26

### Fixed

- Extensible field introspection and reference detection now work correctly.

## [0.6.0] - 2026-03-25

### Changed

- **Breaking:** Strict field access is now the default — accessing an unknown field raises instead of returning `None`. Pass `strict=False` to opt out where the previous behavior is needed.
- **Breaking:** `strict` parameters were renamed across the API for consistency. Review call sites that pass strict-mode flags.
- Exception hierarchy now inherits from a common `IdfKitError` base and includes documentation URLs pointing at the relevant concept page.
- CST scanner optimized with regex; extensible field handling sped up.

### Added

- Documentation URL builder module that backs the new exception messages.
- PR doc preview comments now link to the changed pages.

### Fixed

- IDF type name resolution is now case-insensitive, matching EnergyPlus's own behavior.
- `set_wwr` now preserves construction names and cross-references on the rebuilt fenestration.

## [0.5.0] - 2026-03-14

### Added

- `new_document()` accepts a `strict` parameter to control field-access strictness up-front.
- Type-safety and performance improvements for `IDFDocument` and stub generation.

### Changed

- Renamed the experiment parameter from `experiment` to `runnable` in batch APIs.

### Fixed

- `get_surface_coords` no longer crashes when `number_of_vertices` is blank.

## [0.4.0] - 2026-03-03

### Added

- Weather search and direct download by EPW filename, in addition to lookup by station ID and coordinates.
- Block stacking with `base_elevation` and horizontal adjacency linking, for assembling multi-block models programmatically.

## [0.3.1] - 2026-03-02

### Fixed

- Strict IDF parser now raises informative errors on malformed input instead of failing partway through with unrelated tracebacks.

## [0.3.0] - 2026-02-26

### Added

- EnergyPlus version compatibility checker for Python files (used to validate that snippets and user code target a supported version).
- `validate_document` and `new_document` now seed and enforce schema singleton uniqueness via `maxProperties`.
- Enhanced extensible-object handling in `IDFDocument` and introspection.

## [0.2.0] - 2026-02-20

### Added

- Comprehensive logging throughout idfkit modules — every parser, simulation, and weather subsystem now logs at consistent levels.
- User documentation for the `create_building` API and the zoning module.

### Changed

- IDF/epJSON loading is approximately 2.4x faster via per-type parsing cache.
- Lookup of all objects of a given type is approximately 60x faster: `__getitem__` now uses a single dict lookup instead of scanning.

## [0.1.1] - 2026-02-12

### Added

- Comprehensive eppy compatibility layer (`idfkit._compat`) and additional geometry operations, easing migration from eppy.
- `AsyncFileSystem` protocol so async simulation pipelines no longer block the event loop on filesystem I/O.
- Documentation tutorials for using idfkit with [Scythe](https://github.com/anthropics/scythe) distributed experiments and Celery.

### Fixed

- Tutorial bugs surfaced during end-to-end cloud simulation testing.
- HTML result detection in the simulation result parser.

## [0.1.0] - 2026-02-11

Initial public release.

### Added

- IDF and epJSON parser, writer, and round-trip support.
- `IDFDocument`, `IDFObject`, and name-indexed `IDFCollection` core data model with O(1) lookups.
- `ReferenceGraph` that tracks cross-object references and updates automatically on rename.
- Schema-driven validation against bundled epJSON schemas.
- Bundled schemas covering EnergyPlus 8.9.0 through 25.2.0.
- EnergyPlus simulation execution: synchronous, asynchronous (`async_simulate`), and batch runners with content-addressed result caching.
- Preprocessor support for `ExpandObjects`, `Slab`, and `Basement`.
- Result parsers for SQL, CSV, ERR, RDD, and HTML outputs.
- Weather module: ~17k-station search index, EPW/DDY download with local cache, design-day injection, and Nominatim-backed geocoding.
- Schedule evaluation engine covering all eight EnergyPlus schedule types, usable without running a simulation.
- Thermal property calculations: R/U-values, SHGC, gas mixture properties.
- 3D building geometry visualization with SVG output, including dark-mode support.
- Performance benchmarks comparing idfkit against eppy and opyplus.
- MkDocs Material documentation site with a full API reference, an eppy migration guide, and a getting-started Jupyter notebook.

[unreleased]: https://github.com/idfkit/idfkit/compare/v0.12.0...HEAD
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
