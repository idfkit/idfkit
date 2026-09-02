# About the naming map

idfkit is one toolkit published as two libraries. The Python package and the
JavaScript package read the same EnergyPlus models, and the promise of the pair
is that you learn the vocabulary once and spend it in either language. This page
is the map between the two spellings. Hand it an operation you already know in
one library and it gives you the counterpart in the other, or tells you plainly
that there isn't one and why.

It explains the vocabulary rather than documenting it. The API reference says
what a function takes and returns; the map says which function to look up, and
why its name is the shape it is. Read it once and most lookups afterwards are
guesses you barely need to check.

Every name, every difference, and every reason below the generated marker comes
from `governance/naming.toml` in the
[conformance repository](https://github.com/idfkit/idfkit-conformance), read at
the immutable governance tag this release pins. That same file is what the
naming gate in both repositories reads on every pull request, so the page you
are reading and the check that guards the libraries cannot disagree. For the
capability side of the same governance, which library has what, see
[the parity ledger](parity.md).

## One concept, one entry

The register records concepts, not names. Each concept appears exactly once, and
each entry says how each language spells it. That shape is what makes the map
usable in both directions and what makes a missing counterpart visible instead
of merely absent.

Every entry is one of three kinds, and the kind tells you how much to trust your
instincts:

- **Aligned.** The two spellings say the same word, differing only by the casing
  convention of each ecosystem. Guess and you will be right.
- **Divergent.** The two spellings differ by more than casing, or the same
  spelling means something different. Every divergent entry carries the reason,
  and the reason always says why each side is correct where it lives. None of
  them is a defect awaiting a fix.
- **Excluded.** The surface exists in one language and will not cross. Excluded
  is terminal, not a queue: a counterpart appearing in the other language fails
  the gate.

Exactly one public name per concept per language, too. A second public spelling
of one operation is the thing that makes a reader wonder which one is the real
one, so the gate fails on it.

## Names are decided before they are written

An entry may name something neither library has yet, and that is not an
oversight: it is the point. A name decided while a port is underway is decided
by one language, under schedule pressure, by whoever got there first. A name
decided in the register is decided by both languages, in the open, before any
code depends on it.

Registering a name costs nothing on the day it is written down and saves a
breaking change later. So the register runs ahead of both libraries, and the
notes say which names are reserved rather than callable.

The same reasoning gives every name a budget of exactly one rename. Renames
below are spent budgets, not plans.

## What the map does not cover

**Behaviour.** Two libraries can agree perfectly on a name and disagree about
what it returns. The conformance corpus is what holds behaviour together, and
where the corpus and the register disagree neither wins silently: the
disagreement blocks the merge and is resolved by amending whichever is wrong.

**Whether a capability exists at all.** The map answers "what is this called
over there". [The parity ledger](parity.md) answers "is it over there at all,
and if not, is that for now or for good".

**The single-language packages.** Two JavaScript-only packages, `@idfkit/engine`
and `@idfkit/viewer`, have no entry here. Neither is reachable through the
shared install name and neither is a capability the other language is missing,
so neither belongs on a map of shared vocabulary. Both appear on the parity
ledger, where permanent single-language capabilities are recorded as such.

<!-- BEGIN GENERATED FROM naming.toml. Edit the register, not this page. -->

Generated from
[`governance/naming.toml`](https://github.com/idfkit/idfkit-conformance/blob/governance-2026.6/governance/naming.toml)
at `governance-2026.6`, the governance tag this release pins. It governs `idfkit` and
`@idfkit/core` and `@idfkit/weather`, and it is read at a pinned governance-YYYY.N tag
of idfkit-conformance, never the default branch. Correct the register and regenerate; a
correction made on this page would be overwritten, and it would never reach either
library's naming gate.

## Guessing a name before you look it up

Most counterparts are derivable, and the quickest way to use this page is to guess first
and confirm second.

**Convert the casing.** Python spells a member in snake_case and JavaScript spells it in
camelCase. Converting one to the other mechanically gives the right name for the large
majority of the register: `create_compact_schedule_from_values` becomes
`createCompactScheduleFromValues`, with nothing else changed.

**Expect acronyms to differ in type names.** `IDFObject` in Python is `IdfObject` in
TypeScript, and the same split runs through every type built on the abbreviation, so the
document class is `IDFDocument` against `IdfDocument`. PEP 8 capitalises a whole acronym
inside a CapWords name; the Google TypeScript style guide treats an abbreviation as an
ordinary word. Each is right where it lives, and neither is a candidate for renaming to
match the other.

**Expect an abbreviation inside a camelCase name to become one word.** The rule that
gives `IdfObject` also gives `setWwr` for Python's `set_wwr`, and `calculateShgc` for
`calculate_shgc`.

**Read the verb first.** One operation carries one verb in both languages, so the verb
tells you what a call does to your disk before you have read the rest of the name.

Where the guess fails it fails in one of the ways listed under [where the two libraries
differ](#where-the-two-libraries-differ-and-why), and each of those is a difference with
a reason rather than an oversight. A guess that appears neither in the map nor in that
list does not exist: the gate fails on any public name the register cannot resolve,
which is what makes the map complete rather than merely long.

## The verb vocabulary

These verbs are fixed. A capability that needs one of these operations spells it with
the verb below, in the casing of its own ecosystem, and a capability that does something
else does not borrow one of them.

| Verb | What it means |
| ---- | ------------- |
| `parse` | Read a model out of text already in memory. Never touches a disk. |
| `load` | Read a model from a path. The disk-reading counterpart of parse. |
| `write` | Serialize a model to text. Returns the text, never writes it. |
| `save` | Serialize a model and put it on disk. The disk-writing counterpart of write. |
| `add` | Create an object and attach it to the document. |
| `remove` | Detach an object from the document. |
| `rename` | Change an object's name and repoint every reference to it. |
| `validate` | Check a model or an object against its schema and report findings. |

The pair worth the most attention is `write` against `save`. Both libraries draw the
line in the same place: `write` hands you text and never touches your disk, `save` puts
it on disk. `parse` against `load` is the same line drawn on the way in.

## The map

The map follows the register's own order, which groups related operations together. A
row marked divergent or excluded links to the entry that says why, and a cell reading
*absent* means the operation genuinely has no counterpart in that language.

### Parsing, reading, writing, saving { #map-parsing-reading-writing-saving }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| parse IDF from a string | `parse_idf` | `parseIdf` | aligned |
| parse epJSON from a string | `parse_epjson` | `parseEpJson` | aligned |
| read IDF from disk | `load_idf` | `loadIdf` | aligned |
| read epJSON from disk | `load_epjson` | `loadEpJson` | aligned |
| serialize IDF to a string | `write_idf` | `writeIdf` | aligned |
| write IDF to disk | `save_idf` | `saveIdf` | aligned |
| serialize epJSON to a string | `write_epjson` | `writeEpJson` | aligned |
| write epJSON to disk | `save_epjson` | `saveEpJson` | aligned |

### Editing a document { #map-editing-a-document }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| add an object | `add` | `add` | aligned |
| remove an object | `remove` | `remove` | aligned |
| rename an object | `rename` | `rename` | aligned |

### Validation (registered ahead of the TypeScript implementation) { #map-validation-registered-ahead-of-the-typescript-implementation }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| validate a document | `validate_document` | `validateDocument` | aligned |
| validate an object | `validate_object` | `validateObject` | aligned |
| validation result | `ValidationResult` | `ValidationResult` | aligned |
| validation finding | `ValidationError` | `ValidationError` | aligned |
| validation severity | `idfkit.validation.Severity` | `Severity` | aligned |

### Introspection (registered ahead of the TypeScript implementation) { #map-introspection-registered-ahead-of-the-typescript-implementation }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| describe an object type | `idfkit.introspection.describe_object_type` | `describeObjectType` | aligned |
| object description | `ObjectDescription` | `ObjectDescription` | aligned |
| field description | `FieldDescription` | `FieldDescription` | aligned |

### Documentation URL builders (registered ahead of the TypeScript port) { #map-documentation-url-builders-registered-ahead-of-the-typescript-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| resolved documentation URL | `DocsUrl` | `DocsUrl` | aligned |
| documentation URL for an object type | `docs_url_for_object` | `docsUrlForObject` | aligned |
| I/O reference URL | `io_reference_url` | `ioReferenceUrl` | aligned |
| engineering reference URL | `engineering_reference_url` | `engineeringReferenceUrl` | aligned |
| documentation search URL | `search_url` | `searchUrl` | aligned |

### The declared conformance level { #map-the-declared-conformance-level }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| declared conformance level | `idfkit.CONFORMANCE_LEVEL` | `CONFORMANCE_LEVEL` | aligned |

### Accepted divergences { #map-accepted-divergences }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| acronym casing | `IDFObject` | `IdfObject` | [divergent](#acronym-casing) |
| the document class | `IDFDocument` | `IdfDocument` | [divergent](#the-document-class) |
| the collection class | `IDFCollection` | `IdfCollection` | [divergent](#the-collection-class) |
| the parse error type | `IDFParseError` | `IdfParseError` | [divergent](#the-parse-error-type) |
| every object of a type | `doc["Zone"]` | `doc.all('Zone')` | [divergent](#every-object-of-a-type) |
| untyped collection access | `IDFDocument.get_collection` | *absent* | [excluded](#untyped-collection-access) |
| one object, or nothing | `col.get(name)` | `col.get(name)` | aligned |
| one object, or an error | `col[name]` | `col.require(name)` | [divergent](#one-object-or-an-error) |
| collection to a sequence | `to_list()` | `toArray()` | [divergent](#collection-to-a-sequence) |
| an object's type name | `obj.obj_type` | `obj.typeName` | [divergent](#an-objects-type-name) |
| version | `doc.version` | `doc.version` | [divergent](#version) |
| all input and output | `synchronous` | `asynchronous` | [divergent](#all-input-and-output) |

### Excluded from alignment { #map-excluded-from-alignment }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| eppy compatibility surface | [15 names](#eppy-compatibility-surface) | *absent* | [excluded](#eppy-compatibility-surface) |

### Geometry extraction, registered before the second-tier port begins { #map-geometry-extraction-registered-before-the-second-tier-port-begins }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| three-dimensional vector | `Vector3D` | `Vector3D` | aligned |
| three-dimensional polygon | `Polygon3D` | `Polygon3D` | aligned |
| read a surface's coordinates | `get_surface_coords` | `getSurfaceCoords` | aligned |
| a zone's origin | `get_zone_origin` | `getZoneOrigin` | aligned |
| a zone's rotation | `get_zone_rotation` | `getZoneRotation` | aligned |
| transform relative coordinates to world coordinates | `translate_to_world` | `translateToWorld` | aligned |
| a surface's area | `calculate_surface_area` | `calculateSurfaceArea` | aligned |
| a surface's tilt | `calculate_surface_tilt` | `calculateSurfaceTilt` | aligned |
| a surface's azimuth | `calculate_surface_azimuth` | `calculateSurfaceAzimuth` | aligned |

### The object model { #map-the-object-model }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the object class | `IDFObject` | `IdfObject` | [divergent](#the-object-class) |
| an extensible group | `idfkit.objects.ExtensibleGroup` | `ExtensibleGroup` | aligned |
| create a new document | `new_document` | `new IdfDocument(schema)` | [divergent](#create-a-new-document) |

### The reference graph { #map-the-reference-graph }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the reference graph | `ReferenceGraph` | `ReferenceGraph` | aligned |
| objects referencing a name | `get_referencing` | `referencingObjects` | [divergent](#objects-referencing-a-name) |

### Schema access and the version registry { #map-schema-access-and-the-version-registry }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| load a schema for a version | `get_schema` | `SchemaBundle.load` | [divergent](#load-a-schema-for-a-version) |
| the supported version list | `ENERGYPLUS_VERSIONS` | `SchemaBundle.versions` | [divergent](#the-supported-version-list) |
| resolve a version string | `find_closest_version` | `resolveVersion` | [divergent](#resolve-a-version-string) |

### Static types generated from the schema { #map-static-types-generated-from-the-schema }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| generated object types | `idfkit._generated_types` | `@idfkit/core/types` | [divergent](#generated-object-types) |
| a version type map | *absent* | `AnyTypeMap` | [divergent](#a-version-type-map) |

### Diagnostics from a parse { #map-diagnostics-from-a-parse }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| a parse diagnostic | `idfkit.exceptions.ParseDiagnostic` | `ParseDiagnostic` | aligned |
| diagnostics from a parse | `IDFParseError.diagnostics` | `ParseResult.diagnostics` | [divergent](#diagnostics-from-a-parse) |

### Weather stations, files, and geocoding { #map-weather-stations-files-and-geocoding }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the station index | `StationIndex` | `StationIndex` | aligned |
| search stations | `StationIndex.search` | `StationIndex.search` | aligned |
| a weather station | `WeatherStation` | `WeatherStation` | aligned |
| download a weather file | `WeatherDownloader.download` | `fetchWeatherFiles` | [divergent](#download-a-weather-file) |
| refresh the station index | *absent* | `refreshStationIndex` | [divergent](#refresh-the-station-index) |
| geocode a place name | `geocode` | `geocode` | aligned |
| detect the current location | `detect_location` | `detectLocation` | aligned |

### The rest of the weather surface { #map-the-rest-of-the-weather-surface }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| a text search result | `SearchResult` | `SearchResult` | aligned |
| a proximity search result | `SpatialResult` | `SpatialResult` | aligned |
| which field a text search matched | *absent* | `MatchField` | [divergent](#which-field-a-text-search-matched) |
| the station wire record | *absent* | `StationRecord` | [divergent](#the-station-wire-record) |
| the station index wire form | *absent* | `IndexData` | [divergent](#the-station-index-wire-form) |

### Building the station index, and keeping it fresh { #map-building-the-station-index-and-keeping-it-fresh }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| great-circle distance between two points | `haversine_km` | `haversineKm` | aligned |
| parse a KML station index | *absent* | `parseKml` | [divergent](#parse-a-kml-station-index) |
| read station metadata from a download URL | *absent* | `parseUrlMetadata` | [divergent](#read-station-metadata-from-a-download-url) |
| check the station index for updates | `StationIndex.check_for_updates` | `checkForUpdates` | aligned |
| build an index from index data | *absent* | `indexFromData` | [divergent](#build-an-index-from-index-data) |
| the upstream index file list | *absent* | `INDEX_FILES` | [divergent](#the-upstream-index-file-list) |
| the upstream index base URL | *absent* | `SOURCES_BASE_URL` | [divergent](#the-upstream-index-base-url) |
| fetch a prebuilt station index | *absent* | `loadStationIndex` | [divergent](#fetch-a-prebuilt-station-index) |
| the bundled station index | `StationIndex.load` | `loadBundledIndex` | [divergent](#the-bundled-station-index) |

### Retrieving the files, and the disk edge { #map-retrieving-the-files-and-the-disk-edge }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| download a station's EPW file | `WeatherDownloader.get_epw` | `fetchEpw` | [divergent](#download-a-stations-epw-file) |
| download an EPW file by filename | `WeatherDownloader.get_epw_by_filename` | `fetchEpwByFilename` | [divergent](#download-an-epw-file-by-filename) |
| download a station's archive | *absent* | `fetchWeatherArchive` | [divergent](#download-a-stations-archive) |
| the retrieved weather files | `WeatherFiles` | `WeatherFiles` | [divergent](#the-retrieved-weather-files) |
| read a ZIP archive | *absent* | `unzip` | [divergent](#read-a-zip-archive) |

### Geocoding, beside `geocode a place name` and `detect the current location` { #map-geocoding-beside-geocode-a-place-name-and-detect-the-current-location }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| a geocoding failure | `GeocodingError` | `GeocodingError` | aligned |
| the geocoding rate limiter | `RateLimiter` | `RateLimiter` | aligned |
| the injectable fetch | *absent* | `FetchLike` | [divergent](#the-injectable-fetch) |
| write weather files to disk | *absent* | `saveWeatherFiles` | [divergent](#write-weather-files-to-disk) |
| the written weather file paths | *absent* | `SavedWeatherFiles` | [divergent](#the-written-weather-file-paths) |

### The weather options-object types { #map-the-weather-options-object-types }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the weather options-object types | *absent* | [10 names](#the-weather-options-object-types) | [excluded](#the-weather-options-object-types) |

### The formatting-preserving round-trip (registered ahead of the port) { #map-the-formatting-preserving-round-trip-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| preserve formatting on a round-trip | `preserve_formatting` | `preserveFormatting` | aligned |

### Zone measures, with the geometry extraction group above { #map-zone-measures-with-the-geometry-extraction-group-above }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| a zone's floor area | `calculate_zone_floor_area` | `calculateZoneFloorArea` | aligned |
| a zone's volume | `calculate_zone_volume` | `calculateZoneVolume` | aligned |

### Geometry authoring (registered ahead of the port) { #map-geometry-authoring-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| set the window to wall ratio | `set_wwr` | `setWwr` | aligned |
| rotate a building | `rotate_building` | `rotateBuilding` | aligned |
| translate a building | `translate_building` | `translateBuilding` | aligned |
| scale a building | `scale_building` | `scaleBuilding` | aligned |
| add a shading block | `add_shading_block` | `addShadingBlock` | aligned |
| set default constructions | `set_default_constructions` | `setDefaultConstructions` | aligned |

### Surface matching (registered ahead of the port) { #map-surface-matching-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| intersect and match surfaces | `intersect_and_match` | `intersectAndMatch` | aligned |
| a surface match report | `MatchReport` | `MatchReport` | aligned |

### Zoning (registered ahead of the port) { #map-zoning-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| create a zoned block | `create_block` | `createBlock` | aligned |
| a zone footprint | `ZoneFootprint` | `ZoneFootprint` | aligned |
| a zoning scheme | `ZoningScheme` | `ZoningScheme` | aligned |
| link blocks | `link_blocks` | `linkBlocks` | aligned |

### Construction thermal properties (registered ahead of the port) { #map-construction-thermal-properties-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| construction thermal properties | `ConstructionThermalProperties` | `ConstructionThermalProperties` | aligned |
| a construction's U-value | `calculate_u_value` | `calculateUValue` | aligned |
| a construction's R-value | `calculate_r_value` | `calculateRValue` | aligned |
| a construction's solar heat gain coefficient | `calculate_shgc` | `calculateShgc` | aligned |
| a construction's layers | `get_construction_layers` | `getConstructionLayers` | aligned |

### Schedules (registered ahead of the port) { #map-schedules-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| evaluate a schedule | `idfkit.schedules.evaluate` | `evaluate` | aligned |
| a schedule's values for a year | `idfkit.schedules.values` | `values` | aligned |
| a schedule as a series | `to_series` | *absent* | [divergent](#a-schedule-as-a-series) |
| create a constant schedule | `create_constant_schedule` | `createConstantSchedule` | aligned |
| create a compact schedule | `create_compact_schedule_from_values` | `createCompactScheduleFromValues` | aligned |
| extract special days | `extract_special_days` | `extractSpecialDays` | aligned |
| the holidays in a model | `get_holidays` | `getHolidays` | aligned |

### Output variable selection (registered ahead of the port) { #map-output-variable-selection-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| read the output variable dictionary | `parse_rdd_file` | `parseRddFile` | aligned |
| an output variable | `OutputVariable` | `OutputVariable` | aligned |
| an output meter | `OutputMeter` | `OutputMeter` | aligned |
| select output variables for a run | `prep_outputs` | `prepOutputs` | aligned |

### Design days and sizing (registered ahead of the port) { #map-design-days-and-sizing-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| apply ASHRAE sizing conditions | `apply_ashrae_sizing` | `applyAshraeSizing` | aligned |
| the design day manager | `DesignDayManager` | `DesignDayManager` | aligned |

### Version migration (registered ahead of the port) { #map-version-migration-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| migrate a model to a newer version | `migrate` | `migrate` | aligned |
| a migration report | `MigrationReport` | `MigrationReport` | aligned |
| a migration step | `MigrationStep` | `MigrationStep` | aligned |

### The command line (registered ahead of the port) { #map-the-command-line-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the command line entry point | `idfkit` | `idfkit` | aligned |

### Schema compatibility checking (registered ahead of the port) { #map-schema-compatibility-checking-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| check source compatibility with a version | `check_compatibility` | `checkCompatibility` | aligned |
| diff two schemas | `diff_schemas` | `diffSchemas` | aligned |
| a compatibility diagnostic | `idfkit.compat.Diagnostic` | `Diagnostic` | aligned |

### Plotting simulation results (registered ahead of the port) { #map-plotting-simulation-results-registered-ahead-of-the-port }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| plot an energy balance | `plot_energy_balance` | `plotEnergyBalance` | aligned |
| plot a temperature profile | `plot_temperature_profile` | `plotTemperatureProfile` | aligned |
| plot comfort hours | `plot_comfort_hours` | `plotComfortHours` | aligned |
| a plotting backend | `PlotBackend` | `PlotBackend` | aligned |

### Permanently single-language surfaces { #map-permanently-single-language-surfaces }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the local simulation surface | [19 names](#the-local-simulation-surface) | *absent* | [excluded](#the-local-simulation-surface) |
| the vector image surface | [9 names](#the-vector-image-surface) | *absent* | [excluded](#the-vector-image-surface) |

### The error hierarchy { #map-the-error-hierarchy }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the base error type | `IdfKitError` | *absent* | [divergent](#the-base-error-type) |
| an unknown object type | `UnknownObjectTypeError` | *absent* | [divergent](#an-unknown-object-type) |
| an invalid field | `InvalidFieldError` | *absent* | [divergent](#an-invalid-field) |
| a value outside its range | `RangeError` | *absent* | [divergent](#a-value-outside-its-range) |
| a duplicate object | `DuplicateObjectError` | *absent* | [divergent](#a-duplicate-object) |
| a version mismatch | `VersionMismatchError` | *absent* | [divergent](#a-version-mismatch) |
| an unsupported version | `UnsupportedVersionError` | *absent* | [divergent](#an-unsupported-version) |
| a schema that cannot be found | `SchemaNotFoundError` | *absent* | [divergent](#a-schema-that-cannot-be-found) |
| a version that cannot be detected | `VersionNotFoundError` | *absent* | [divergent](#a-version-that-cannot-be-detected) |
| a validation that failed | `ValidationFailedError` | *absent* | [divergent](#a-validation-that-failed) |
| a migration that failed | `MigrationError` | *absent* | [divergent](#a-migration-that-failed) |
| a DDY file with no design days | `NoDesignDaysError` | *absent* | [divergent](#a-ddy-file-with-no-design-days) |
| the local simulation error types | [3 names](#the-local-simulation-error-types) | *absent* | [excluded](#the-local-simulation-error-types) |

### Version constants and version helpers { #map-version-constants-and-version-helpers }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the newest supported version | `LATEST_VERSION` | `SchemaBundle.latest` | [divergent](#the-newest-supported-version) |
| the oldest supported version | `MINIMUM_VERSION` | *absent* | [divergent](#the-oldest-supported-version) |
| the ASHRAE perimeter depth | `ASHRAE_PERIMETER_DEPTH` | `ASHRAE_PERIMETER_DEPTH` | aligned |
| detect a document version | `get_idf_version` | `getIdfVersion` | aligned |
| detect an epJSON document version | `idfkit.epjson_parser.get_epjson_version` | `getEpJsonVersion` | aligned |
| render a version as text | `version_string` | *absent* | [divergent](#render-a-version-as-text) |
| whether a version is supported | `is_supported_version` | *absent* | [divergent](#whether-a-version-is-supported) |
| version string ordering | *absent* | [2 names](#version-string-ordering) | [excluded](#version-string-ordering) |

### Footprint builders and two-dimensional polygon helpers { #map-footprint-builders-and-two-dimensional-polygon-helpers }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| a rectangular footprint | `footprint_rectangle` | `footprintRectangle` | aligned |
| an L-shaped footprint | `footprint_l_shape` | `footprintLShape` | aligned |
| a T-shaped footprint | `footprint_t_shape` | `footprintTShape` | aligned |
| a U-shaped footprint | `footprint_u_shape` | `footprintUShape` | aligned |
| an H-shaped footprint | `footprint_h_shape` | `footprintHShape` | aligned |
| a courtyard footprint | `footprint_courtyard` | `footprintCourtyard` | aligned |
| a two-dimensional polygon's area | `polygon_area_2d` | `polygonArea2D` | aligned |
| whether a two-dimensional polygon contains a point | `polygon_contains_2d` | `polygonContains2D` | aligned |
| the difference of two two-dimensional polygons | `polygon_difference_2d` | `polygonDifference2D` | aligned |
| the intersection of two two-dimensional polygons | `polygon_intersection_2d` | `polygonIntersection2D` | aligned |
| a model's bounding box | `bounding_box` | `boundingBox` | aligned |

### Zoning and horizontal surface matching, with the groups above { #map-zoning-and-horizontal-surface-matching-with-the-groups-above }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| a zoned block | `ZonedBlock` | `ZonedBlock` | aligned |
| a horizontal adjacency | `HorizontalAdjacency` | `HorizontalAdjacency` | aligned |
| surface matching options | `MatchOptions` | `MatchOptions` | aligned |
| detect horizontal adjacencies | `detect_horizontal_adjacencies` | `detectHorizontalAdjacencies` | aligned |
| link horizontal surfaces | `link_horizontal_surfaces` | `linkHorizontalSurfaces` | aligned |
| split a horizontal surface | `split_horizontal_surface` | `splitHorizontalSurface` | aligned |
| a zone's ceiling area | `calculate_zone_ceiling_area` | `calculateZoneCeilingArea` | aligned |
| a zone's height | `calculate_zone_height` | `calculateZoneHeight` | aligned |

### Schema objects and the parser object { #map-schema-objects-and-the-parser-object }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| one version's schema | `EpJSONSchema` | `Schema` | [divergent](#one-versions-schema) |
| the schema source | `SchemaManager` | `SchemaBundle` | [divergent](#the-schema-source) |
| the process-wide schema source | `get_schema_manager` | `schemas` | [divergent](#the-process-wide-schema-source) |
| the IDF parser object | `IDFParser` | *absent* | [divergent](#the-idf-parser-object) |
| the schema bundle source surface | *absent* | [2 names](#the-schema-bundle-source-surface) | [excluded](#the-schema-bundle-source-surface) |
| the slimmed schema record types | *absent* | [2 names](#the-slimmed-schema-record-types) | [excluded](#the-slimmed-schema-record-types) |
| the difference between two schema versions | *absent* | `SchemaDelta` | [divergent](#the-difference-between-two-schema-versions) |
| resolve the schema for a detected version | *absent* | `schemaFor` | [divergent](#resolve-the-schema-for-a-detected-version) |

### TypeScript-only structural surfaces { #map-typescript-only-structural-surfaces }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the options-object types | *absent* | [5 names](#the-options-object-types) | [excluded](#the-options-object-types) |
| the static typing surface | *absent* | [4 names](#the-static-typing-surface) | [excluded](#the-static-typing-surface) |
| the per-type prototype surface | *absent* | [3 names](#the-per-type-prototype-surface) | [excluded](#the-per-type-prototype-surface) |
| the object-model value types | *absent* | [4 names](#the-object-model-value-types) | [excluded](#the-object-model-value-types) |
| the lexer surface | *absent* | [4 names](#the-lexer-surface) | [excluded](#the-lexer-surface) |

### Remaining single-language names on the JavaScript side { #map-remaining-single-language-names-on-the-javascript-side }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| a reference edge | *absent* | `ReferenceEdge` | [divergent](#a-reference-edge) |
| an epJSON document value | *absent* | `EpJson` | [divergent](#an-epjson-document-value) |
| serialize one object | *absent* | `writeObject` | [divergent](#serialize-one-object) |
| serialize a document to an epJSON value | *absent* | `toEpJson` | [divergent](#serialize-a-document-to-an-epjson-value) |
| read IDF from disk, keeping diagnostics | *absent* | `loadIdfWithDiagnostics` | [divergent](#read-idf-from-disk-keeping-diagnostics) |

### The document's own members { #map-the-documents-own-members }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| the path a document was read from | `IDFDocument.filepath` | *absent* | [divergent](#the-path-a-document-was-read-from) |
| strict field access | `IDFDocument.strict` | *absent* | [divergent](#strict-field-access) |
| a document's schema | `IDFDocument.schema` | `IdfDocument.schema` | aligned |
| the concrete syntax tree | `IDFDocument.cst` | *absent* | [divergent](#the-concrete-syntax-tree) |
| the original source text | `IDFDocument.raw_text` | *absent* | [divergent](#the-original-source-text) |
| every collection in a document | `IDFDocument.collections` | *absent* | [divergent](#every-collection-in-a-document) |
| a document's reference graph | `IDFDocument.references` | `IdfDocument.references` | aligned |
| the object types present in a document | `IDFDocument.keys` | `types` | [divergent](#the-object-types-present-in-a-document) |
| every non-empty collection | `IDFDocument.values` | *absent* | [divergent](#every-non-empty-collection) |
| every object type and its collection | `IDFDocument.items` | *absent* | [divergent](#every-object-type-and-its-collection) |
| an object's outgoing references | `IDFDocument.get_references` | `referencedBy` | [divergent](#an-objects-outgoing-references) |
| a model's schedules by name | `IDFDocument.schedules_dict` | *absent* | [divergent](#a-models-schedules-by-name) |
| one schedule by name | `IDFDocument.get_schedule` | `getSchedule` | aligned |
| the schedules a model uses | `IDFDocument.get_used_schedules` | `getUsedSchedules` | aligned |
| a zone's surfaces | `IDFDocument.get_zone_surfaces` | `getZoneSurfaces` | aligned |
| every object in a document | `IDFDocument.all_objects` | `objects` | [divergent](#every-object-in-a-document) |
| an object's name changed | `IDFDocument.notify_name_change` | `onNameChanged` | [divergent](#an-objects-name-changed) |
| an object's field changed | `IDFDocument.notify_reference_change` | `onFieldChanged` | [divergent](#an-objects-field-changed) |
| copy a document | `IDFDocument.copy` | `IdfDocument.copy` | aligned |
| run the ExpandObjects preprocessor | `IDFDocument.expand` | *absent* | [excluded](#run-the-expandobjects-preprocessor) |
| second Python spellings of a registered concept | [4 names](#second-python-spellings-of-a-registered-concept) | *absent* | [excluded](#second-python-spellings-of-a-registered-concept) |

### Remaining top-level Python names { #map-remaining-top-level-python-names }

| Concept | Python | TypeScript | Kind |
| ------- | ------ | ---------- | ---- |
| migrate a model without blocking | `async_migrate` | *absent* | [divergent](#migrate-a-model-without-blocking) |
| create schedule type limits | `create_schedule_type_limits` | `createScheduleTypeLimits` | aligned |

## What the notes add

Some names carry a note the tables cannot hold. Notes are grouped here, so a note that
applies to many names is stated once. "Registered before it is written" means exactly
that: the name is decided and reserved, and the implementation follows it rather than
the other way round.

**parse epJSON from a string**

The casing of the format name follows each ecosystem's rule for the rest of the
identifier, so Python's single-case snake_case gives `epjson` and TypeScript's camelCase
gives `EpJson`. Both recover the same word.

**read IDF from disk, read epJSON from disk**

TypeScript exports this from `@idfkit/core/node`, the async edge; see the I/O entry.

**serialize IDF to a string**

Python's `write_idf` keeps its spelling through the rename batch and loses only its
`filepath` parameter and the three `@overload` stanzas that parameter forced. The
disk-writing half moves to `save_idf`, so the string-serializing name is unchanged and
its rename count stays at 0.

**write IDF to disk**

Python's rename count is 1: this operation was spelled `write_idf(doc, filepath)` before
the rename batch. TypeScript already exports `saveIdf` from `@idfkit/core/node` and does
not change. Python's `save_idf` does not exist yet at the time this entry is registered;
it is written by the rename batch under this name.

**serialize epJSON to a string**

Same construction and same reasoning as the IDF pair above.

**write epJSON to disk**

Python's rename count is 1, for the same reason as `save_idf`: this operation was
spelled `write_epjson(doc, filepath)`. `save_epjson` is written by the rename batch
under this name.

**add an object**

`IDFDocument.add(obj_type, name, **fields)` against `IdfDocument.add(type, name,
values)`. The keyword-argument form is idiomatic Python and has no TypeScript
equivalent, so the field values arrive as an object literal there. Same verb, same
argument order, same result.

**remove an object**

Python spells it `IDFCollection.remove(obj)`; TypeScript spells it
`IdfDocument.remove(obj)`. The receiver differs because Python reaches a collection
through `doc["Zone"]` and TypeScript through `doc.all('Zone')`, which is the operator
divergence recorded below, not a second verb.

**rename an object**

The two signatures differ: Python's `IDFDocument.rename(obj_type, old_name, new_name)`
against TypeScript's `IdfDocument.rename(obj, next)`.

Both languages support `obj.name = new`, which is unambiguous in either, needs no
object-type argument, and repoints every reference in both implementations. That
assignment is the PRIMARY PATH and is what the documentation teaches on both sides. The
method signatures are left alone rather than forced into agreement: aligning them would
rename a working method for a gain the assignment form already delivers, and would spend
a rename budget on syntax no reader has to use. Recorded per research R14.

**validate a document**

Registered before it is written. The TypeScript side does not exist at registration
time; the Tier 1 port writes it under this name, into
`idfkit-js/packages/core/src/validate/`. Naming an unwritten capability costs nothing
now and is breaking later, which is the entire reason for FR-007.

**validate an object**

Registered before it is written, with `validate_document`.

**validation result**

Registered before the TypeScript type is written. No acronym, so no casing divergence.

**validation finding**

Registered before the TypeScript type is written. The name says Error and the type is a
record, not a thrown exception: a finding carries a severity and a location and is
collected into a `ValidationResult`. Both languages keep the existing Python spelling
rather than improving it here, because renaming it would spend a rename budget on a type
the port has not yet shipped.

**validation severity**

Registered before the TypeScript type is written. Python reaches it at
`idfkit.validation.Severity` rather than through the top-level `__all__`; the values are
`error`, `warning`, `info` and the TypeScript port renders the same three strings.

**describe an object type**

Registered before it is written, into `idfkit-js/packages/core/src/introspect/`. Python
reaches it at `idfkit.introspection.describe_object_type` and through
`IDFDocument.describe(obj_type)`; the module-level function is the registered name.

**object description**

Registered before the TypeScript type is written. Same field set on both sides.

**field description**

Registered before the TypeScript type is written. Same field set and constraints on both
sides.

**resolved documentation URL**

Registered before the TypeScript type is written. Carries `url`, `doc_set`, `version`,
and `label` in Python; the TypeScript port spells the field `docSet` and keeps the rest,
which is the field-name casing rule rather than a divergence in the type.

**documentation URL for an object type**

Registered before it is written, into `idfkit-js/packages/core/src/docs-url/`.

**I/O reference URL**

Registered before it is written. `io` stays lowercase in TypeScript by the same rule
that gives `IdfObject`.

**engineering reference URL, documentation search URL, a surface's area, rotate a
building, translate a building, scale a building, add a shading block, set default
constructions, link blocks, a construction's U-value, a construction's R-value, a
construction's layers, create a constant schedule, create a compact schedule, extract
special days, the holidays in a model, select output variables for a run, diff two
schemas, plot an energy balance, plot a temperature profile, plot comfort hours, whether
a two-dimensional polygon contains a point, the intersection of two two-dimensional
polygons, split a horizontal surface**

Registered before it is written.

**declared conformance level**

The `conformance-YYYY.N` tag of this repository that the release passes. A constant, not
a function, in both languages, and a string in both, so the two claims compare directly.

Each side reads it from one place rather than restating it, so the declaration and the
pin cannot diverge: Python from `[tool.idfkit.conformance] level` in `pyproject.toml`,
TypeScript from `idfkit.conformance` in `packages/core/package.json`. Registered here so
that the export passes the naming gate on the change that adds it.

Screaming snake case is the constant convention in both ecosystems, so this name is
identical on both sides rather than merely aligned.

**one object, or nothing**

Returns `None` in Python and `undefined` in TypeScript, each language's own absent
value.

**three-dimensional vector**

Registered before the TypeScript type is written. `3D` is a numeral and a letter rather
than an acronym, so the casing rule that splits `IDFObject` from `IdfObject` does not
apply and the two names are identical.

**three-dimensional polygon**

Registered before the TypeScript type is written. Carries `normal`, `area`, `centroid`,
`tilt`, `azimuth`, `is_horizontal`, and `is_vertical` in Python; the TypeScript port
spells the two predicates `isHorizontal` and `isVertical` by the field-casing rule and
keeps the rest.

**read a surface's coordinates**

Registered before it is written. Returns the surface's `Polygon3D`, or the absent value
when it has no vertices.

**a zone's origin**

Registered before it is written. Returns a `Vector3D`.

**a zone's rotation**

Registered before it is written. Returns degrees about the vertical axis.

**transform relative coordinates to world coordinates**

Registered before it is written. The one member of this group that mutates the document:
it rewrites relative surface coordinates in place and updates `GlobalGeometryRules`. It
is registered with the extraction group because every calculation below depends on
knowing which coordinate system it is reading.

**a surface's tilt**

Registered before it is written. Degrees, using the EnergyPlus convention.

**a surface's azimuth**

Registered before it is written. Degrees clockwise from north, using the EnergyPlus
convention.

**an extensible group**

One row of a repeated field group, for example a single vertex inside a surface's vertex
list. Python reaches it at `idfkit.objects.ExtensibleGroup` rather than through the
top-level `__all__`; TypeScript exports the type from `@idfkit/core`. No acronym, so no
casing divergence.

**the reference graph**

Exported by both libraries under the same name. No acronym, so no casing divergence.

**a parse diagnostic**

One finding from a parse: a message, a location, and a severity. Python reaches it at
`idfkit.exceptions.ParseDiagnostic` rather than through the top-level `__all__`.

**the station index**

Both libraries ship their own index and neither retrieves one to get started (FR-043,
FR-075).

**search stations**

Same receiver, same name, same argument, and `SearchResult` on both sides.

**a text search result**

One hit from `StationIndex.search`: the station, a relevance score from 0 to 1, and the
field that matched. Identical names, and the field carrying the last of the three is
spelled `match_field` in Python and `matchField` in TypeScript by the field-casing rule.
Python reaches the type at `idfkit.weather.SearchResult` rather than through the
top-level `__all__`.

**a proximity search result**

One hit from `StationIndex.nearest`: the station and its great-circle distance,
`distance_km` in Python and `distanceKm` in TypeScript. Same construction and same
reasoning as `a text search result` above.

**great-circle distance between two points**

The Haversine formula over four decimal degrees, in kilometres. Both sides use the same
6371 km radius and the same clamp before the `asin`, so `nearest` orders a query
identically in either library. Python reaches it at
`idfkit.weather.spatial.haversine_km`.

**check the station index for updates**

The same operation under corresponding names: send HEAD requests for the upstream KML
files, compare `Last-Modified` against the values the index was built with, and answer
false when the index carries none or the probe cannot be completed.

The receiver differs and the names do not. Python hangs it on the index, because the
index it compares against is the one it is called on. TypeScript takes the index as an
argument, because everything reaching the network there is a free function taking an
overridable `fetch`. That is the `download a weather file` divergence, not a second name
for this operation.

Python also fires this check by itself from `StationIndex.load`, at most once a day.
That nudge has no TypeScript counterpart, for the reason `refresh the station index`
above gives, and the parity ledger records the consequence under `weather-index`.

**a geocoding failure**

Identical names, and one of the few failures the JavaScript side throws rather than
returns: an address that resolves to nothing leaves no partial answer to hand back, so
there is no value for the failure to be. Python reaches it at
`idfkit.weather.GeocodingError`.

**the geocoding rate limiter**

Nominatim asks callers to stay under one request per second, and both libraries hold to
it with an object of this name carrying a minimum interval, a `wait`, and a `reset`. The
implementations differ as the languages do: Python takes a lock, because threads exist
there, and TypeScript chains a promise, because they do not.

Public on both sides and advertised on neither. Python reaches it at
`idfkit.weather.geocode.RateLimiter` rather than through the sub-package's `__all__`,
the same shape as `idfkit.exceptions.ParseDiagnostic`. Registered so that the two
spellings cannot drift apart, not as a promise that either is prominent.

**preserve formatting on a round-trip**

An option, not a function: `load_idf(path, preserve_formatting=True)` builds a concrete
syntax tree that `write_idf` reproduces, and `load_epjson` retains the raw JSON text the
same way. Registered before the TypeScript side is written; the parity ledger records
the absence as Tier 2 under `lossless-round-trip`. Registering the option name now costs
nothing and is breaking later.

**a zone's floor area**

Registered before it is written, with the geometry extraction group above. Read-only,
like the rest of that group.

**a zone's volume**

Registered before it is written, with the geometry extraction group above.

**set the window to wall ratio**

Registered before it is written. `wwr` stays lowercase in TypeScript by the same rule
that gives `IdfObject`.

**intersect and match surfaces**

Registered before it is written. Python currently exports a second public name for the
same operation, `intersect_match`, which FR-005 prohibits; that duplicate is resolved by
the change that withdraws it, not here, and this entry records the surviving name.

**a surface match report, a zone footprint, a zoning scheme, an output variable, an
output meter, a migration report, a migration step**

Registered before the TypeScript type is written.

**create a zoned block**

Registered before it is written, into the reserved `@idfkit/geometry` package.

**construction thermal properties**

Registered before the TypeScript type is written. Produced by `get_thermal_properties`
in Python.

**a construction's solar heat gain coefficient**

Registered before it is written. `shgc` is an abbreviation, so TypeScript writes it as
one word by the same rule that gives `IdfObject`, and Python keeps the lowercase run its
snake_case gives.

**evaluate a schedule**

Registered before it is written. One value at one instant.

**a schedule's values for a year**

Registered before it is written. The whole year at a chosen timestep.

**read the output variable dictionary**

Registered before it is written. Python reaches it at
`idfkit.simulation.parsers.rdd.parse_rdd_file` and pairs it with `parse_mdd_file` for
the meter dictionary.

**apply ASHRAE sizing conditions**

Registered before it is written. `ashrae` is an abbreviation, so TypeScript writes it as
one word by the same rule that gives `IdfObject`.

**the design day manager**

Registered before the TypeScript type is written. Reads a DDY file and injects design
days into a model.

**migrate a model to a newer version**

Registered before it is written. Python pairs it with `async_migrate`; the TypeScript
port is async by construction.

**the command line entry point**

The console script name, not a module member. Python installs it from
`idfkit.compat._cli:main` with the `check` and `migrate` subcommands. Registered before
the JavaScript side is written so that a port cannot land under a different command
name; the parity ledger records the absence as Tier 3 under `command-line`.

**check source compatibility with a version**

Registered before it is written. Python reaches it at
`idfkit.compat.check_compatibility`.

**a compatibility diagnostic**

Registered before the TypeScript type is written. Distinct from `a parse diagnostic`:
this one reports a source construct that will not hold against another EnergyPlus
version, and it carries one of `DIAGNOSTIC_CODES`.

**a plotting backend**

Registered before the TypeScript type is written. Python selects one with
`get_default_backend`.

**the ASHRAE perimeter depth**

Registered before it is written, with the zoning group. The default perimeter depth used
when a footprint is split into core and perimeter zones, 4.57 m, which is 15 feet in the
ASHRAE source. Screaming snake case is the constant convention in both ecosystems, so
this name is identical on both sides rather than merely aligned, the same as
`CONFORMANCE_LEVEL`. The abbreviation stays fully capitalised in TypeScript because that
is what the constant convention does to every letter, which is why this does not
contradict the rule that gives `applyAshraeSizing`.

**detect a document version**

Read the EnergyPlus version out of an IDF document without a schema. Both sides exist
and both are the minimum scan needed to break the chicken-and-egg between choosing a
schema and reading the version that selects it.

TypeScript's rename count is 1. The package shipped this as `detectVersion`; it becomes
`getIdfVersion`, which settles the `get` against `detect` conflict in favour of `get`,
the verb the register already uses for every accessor pair it has decided:
`get_surface_coords` to `getSurfaceCoords`, `get_zone_origin` to `getZoneOrigin`,
`get_construction_layers` to `getConstructionLayers`. The new name also says which
format it reads, which the old one did not, and which matters now that
`getEpJsonVersion` sits beside it. Python's `get_idf_version` is unchanged and its count
stays 0.

DECIDED 2026-09-02. The rename lands in the T061 to T069 batch, with the rest of the
batch, and is breaking for anyone importing `detectVersion` from `@idfkit/core@0.1.0`.

The signatures are not identical and are not being aligned: Python's takes a path and
returns `tuple[int, int, int]`, TypeScript's takes IDF text and returns `string |
undefined`. That is the `version` type divergence and the input and output divergence,
both already recorded, and the string is canonical across the boundary.

**detect an epJSON document version**

The epJSON counterpart of `detect a document version`, and it is named here so that the
pair cannot drift apart later.

TypeScript's rename count is 1. The package shipped this as `detectEpJsonVersion`; it
becomes `getEpJsonVersion` with `detectVersion`, in the same batch and for the same
reason. DECIDED 2026-09-02, landing in the T061 to T069 batch, and breaking for anyone
importing `detectEpJsonVersion` from `@idfkit/core@0.1.0`.

Python's `get_epjson_version` already carries the settled spelling and its count stays
0. It is reached at `idfkit.epjson_parser.get_epjson_version` rather than through the
top-level `__all__`, which is the same shape as
`idfkit.introspection.describe_object_type` and `idfkit.schedules.evaluate`. Promoting
it to the top level would be additive and is not part of this feature; whether or not
that happens, the name is fixed here.

The casing of the format name follows each ecosystem's rule for the rest of the
identifier, so Python gives `epjson` and TypeScript gives `EpJson`, exactly as
`parse_epjson` against `parseEpJson`.

**a rectangular footprint**

Registered before it is written. Returns the plan outline as a list of two-dimensional
points.

**an L-shaped footprint**

Registered before it is written. The single letter is a word of the name in both
languages, so Python's snake_case separates it and TypeScript's camelCase capitalises
it.

**a T-shaped footprint, a U-shaped footprint, an H-shaped footprint**

Registered before it is written, with the other lettered footprints.

**a courtyard footprint**

Registered before it is written. A rectangular outline with a rectangular hole.

**a two-dimensional polygon's area**

Registered before it is written. Signed area, so the sign reports the winding direction.

**the difference of two two-dimensional polygons**

Registered before it is written. Returns the possibly several pieces the subtraction
leaves.

**a model's bounding box**

Registered before it is written. The plan extent of every surface in the model, or the
absent value when the model has no coordinates to bound.

**a zoned block**

Registered before the TypeScript type is written. What `create_block` produces, with the
zoning group above.

**a horizontal adjacency**

Registered before the TypeScript type is written. One ceiling-and-floor pair found
between two stories.

**surface matching options**

Registered before the TypeScript type is written. The tolerances `intersect_and_match`
works to, beside `MatchReport`.

**detect horizontal adjacencies**

Registered before it is written. The verb is `detect` rather than `get` because the
operation searches: it compares outdoor horizontal surfaces across stories and reports
the overlaps it finds, which is not an accessor. That distinction is what `detect a
document version` gives up by becoming `getIdfVersion`, and it is why the two are not
the same case.

**link horizontal surfaces**

Registered before it is written. Sets each of a ceiling and floor pair as the other's
outside boundary.

**a zone's ceiling area**

Registered before it is written, with `calculate_zone_floor_area` and
`calculate_zone_volume`.

**a zone's height**

Registered before it is written, with the other zone measures.

**a document's schema**

The schema the document was parsed against. Python's is `EpJSONSchema | None`, because a
document can be built without one; TypeScript's is a required `Schema`, because its
constructor takes one. Same name, same meaning, and the optionality difference follows
from `create a new document`.

**a document's reference graph**

The live `ReferenceGraph` for the document, under the same name on both sides. The
queries hung on it differ, which is recorded separately under `objects referencing a
name` and `an object's outgoing references`; the accessor itself does not.

**one schedule by name**

Registered before the TypeScript side is written, with the schedules group above.
Case-insensitive, because EnergyPlus resolves names that way, and returns the language's
own absent value on a miss: `None` in Python, `undefined` in TypeScript, as `one object,
or nothing` records.

**the schedules a model uses**

Registered before the TypeScript side is written, with the schedules group above. The
names of schedules something in the model actually references, answered from the
reference graph rather than by scanning.

**a zone's surfaces**

Registered before the TypeScript side is written, with the geometry group above, whose
`get_*` to `get*` pairing it follows.

**copy a document**

Registered before the TypeScript side is written. A deep, independent copy, which is
what makes parametric work possible without reparsing the baseline. Python preserves the
strict mode on the copy; the TypeScript port has no such mode to preserve.

**create schedule type limits**

Registered before it is written, with the schedule builders above.

## Where the two libraries differ, and why

Each difference below stays. None is a defect and none is a candidate for a future
rename: forcing either spelling onto the other language makes it wrong there, and wrong
in a way that language's readers would feel on every line.

### Acronym casing

| Python | TypeScript |
| ------ | ---------- |
| `IDFObject` | `IdfObject` |

PEP 8 capitalises every letter of an acronym inside a CapWords name, which gives
`IDFObject`. The Google TypeScript style guide treats an abbreviation as an ordinary
word, which gives `IdfObject`. Each spelling is the correct one in its own ecosystem,
and forcing either onto the other makes it wrong there and inconsistent with every
neighbouring library its users already read.

The rule, not the single name: this governs `IDF*` against `Idf*` across both surfaces.

### The document class

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument` | `IdfDocument` |

The acronym casing rule above. TypeScript's rename count is 1: the package shipped
`IDFDocument` alongside `IdfObject`, `IdfCollection`, and `IdfParseError`, so the old
spelling contradicted both its own neighbours and the Google rule. The rename batch
fixes it, once.

Breaking for anyone importing `IDFDocument` from `@idfkit/core@0.1.0`. Recorded in the
changelog as such.

### The collection class

| Python | TypeScript |
| ------ | ---------- |
| `IDFCollection` | `IdfCollection` |

The acronym casing rule above. Both sides already spell it correctly for their
ecosystem.

### The parse error type

| Python | TypeScript |
| ------ | ---------- |
| `IDFParseError` | `IdfParseError` |

The acronym casing rule above. Both sides already spell it correctly for their
ecosystem.

### Every object of a type

| Python | TypeScript |
| ------ | ---------- |
| `doc["Zone"]` | `doc.all('Zone')` |

Python has operator overloading and `__getitem__` is the idiomatic spelling of keyed
access; TypeScript has no such operator, and an index signature on a class cannot carry
the generic return type that makes the call statically checked against the generated
type map. `all()` is a method because it has to be, and it is typed because that is the
point of the type maps.

This is a syntactic divergence forced by the languages, not a naming disagreement, so
neither side is a candidate for renaming to match the other.

### One object, or an error

| Python | TypeScript |
| ------ | ---------- |
| `col[name]` | `col.require(name)` |

Same reason as `doc["Zone"]`: Python spells throwing lookup with the subscript operator,
which raises `KeyError` on a miss and is what every Python reader expects of `[]`.
TypeScript has no operator that can throw here, so the throwing variant needs a name,
and `require` says what it does at the call site.

The contract is identical on both sides, and identical to `get` except for the miss:
`get` returns the absent value, this raises.

### Collection to a sequence

| Python | TypeScript |
| ------ | ---------- |
| `to_list()` | `toArray()` |

The sequence type is named differently by the two languages. Python's is `list` and
`to_list` is the conventional spelling; JavaScript's is `Array` and `toArray` matches
`Array.from`, `toSorted`, and every neighbouring API. Renaming either to the other's
word would name a type that does not exist in that language.

### An object's type name

| Python | TypeScript |
| ------ | ---------- |
| `obj.obj_type` | `obj.typeName` |

Python's `obj_type` avoids shadowing the builtin `type`, which is the standard Python
workaround and reads naturally in snake_case. TypeScript has no such collision, and
`typeName` is clearer than `objType` in a language where `type` is a keyword only in
type position. Both name the same string, the EnergyPlus object type as the schema
spells it.

### Version

| Python | TypeScript |
| ------ | ---------- |
| `doc.version` | `doc.version` |

Python returns `tuple[int, int, int]`, for example `(26, 1, 0)`. TypeScript returns
`string`, for example `"26.1.0"`.

This is worse than a rename and is recorded rather than reconciled. The name is
identical, the prose describing it is identical, and the value behaves differently, so
code written from one side's documentation compiles against the other and is wrong at
runtime. Each language keeps its idiomatic type: Python's tuple compares and sorts
correctly with no helper, which is why `LATEST_VERSION`, `MINIMUM_VERSION`, and
`find_closest_version` are all tuples; TypeScript has no comparable tuple literal and
its schema keys, `resolveVersion`, `compareVersions`, and `versionKey` are all strings
already.

The STRING is canonical for anything crossing the boundary, because IDF text, epJSON,
and the schema keys are strings already. Python renders it with `version_string`. The
corpus asserts that both libraries render the same string for the same model (FR-004),
so the divergence is documented AND tested rather than documented only.

Canonical form across the boundary: **string**.

No signature changes anywhere. This entry is documentation and a corpus case, not a
rename.

### All input and output

| Python | TypeScript |
| ------ | ---------- |
| `synchronous` | `asynchronous` |

Python's file API is synchronous, its ecosystem is synchronous by default, and
`load_idf(path)` returning a document is what every Python reader expects. TypeScript's
core is deliberately synchronous and pure so that it runs unchanged in a browser, a
worker, or an edge runtime; every operation that touches a disk or a network is
therefore pushed to `@idfkit/core/node` and is `async`, which is the only shape a
portable core can have without forcing `node:fs` into browser bundles.

Making Python async would be wrong for its ecosystem; making the TypeScript core sync
would either break the browser target or force the whole portable surface to be async
just in case. The split is the design, not an accident.

The verb pairs still align across the boundary: `parse` and `write` are sync and pure in
BOTH languages, and only `load` and `save` differ by being awaited in TypeScript.

### The object class

| Python | TypeScript |
| ------ | ---------- |
| `IDFObject` | `IdfObject` |

The acronym casing rule recorded above, which names this very pair as its exemplar. Both
sides already spell it correctly for their ecosystem, and neither is a candidate for
renaming to match the other.

The `acronym casing` entry states the rule; this entry is the class it governs, so that
the object class has a concept of its own in the same way the document class, the
collection class, and the parse error type each do.

### Create a new document

| Python | TypeScript |
| ------ | ---------- |
| `new_document` | `new IdfDocument(schema)` |

Python offers a module-level factory because the constructor needs a loaded schema the
caller would otherwise fetch itself, and because loading a schema in Python is
synchronous, so the factory can do it. `new_document()` also seeds the baseline
singletons a usable model needs: Version, Building, SimulationControl, and
GlobalGeometryRules.

TypeScript loads a schema asynchronously from a `BundleSource`, and a constructor cannot
await, so the caller loads the schema first and hands it over. A synchronous factory is
not available to write there, which makes `new` both the idiomatic and the only possible
spelling. This is the input and output divergence recorded above, seen from the
construction side.

### Objects referencing a name

| Python | TypeScript |
| ------ | ---------- |
| `get_referencing` | `referencingObjects` |

The receiver carries the difference, not the operation. Python hangs the query on the
document, `IDFDocument.get_referencing(name)`, because the graph is reached through the
document there. TypeScript exposes the graph itself as `doc.references` and hangs the
query on it, `doc.references.referencingObjects(name)`, where repeating the word would
read as `references.getReferencing`. Each spelling says exactly what its receiver does
not already say, and aligning them would make one of the two stutter.

### Load a schema for a version

| Python | TypeScript |
| ------ | ---------- |
| `get_schema` | `SchemaBundle.load` |

Python ships every schema inside the package and reads it from disk synchronously, so a
module-level `get_schema(version)` is enough and is what a Python reader expects.
TypeScript cannot assume a filesystem: a browser fetches the bundle over HTTP and a
bundler-driven app resolves it through `import()`, so the caller constructs a
`SchemaBundle` over a `BundleSource` and loads from that. The operation is a method on
the object that owns the source because there is no process-wide source that would let
it be a free function. This is the input and output divergence recorded above.

### The supported version list

| Python | TypeScript |
| ------ | ---------- |
| `ENERGYPLUS_VERSIONS` | `SchemaBundle.versions` |

Python's supported set is a constant because the schemas ship with the package, so the
answer is known at import time. TypeScript's depends on which bundle the caller
supplied, so it can only be a query on that bundle, and it is asynchronous for the same
reason `SchemaBundle.load` is. A constant there would name a set the library does not
control.

Python's members are version tuples and TypeScript's are strings, which is the `version`
divergence recorded above. The string is canonical for anything crossing the boundary.

Canonical form across the boundary: **string**.

### Resolve a version string

| Python | TypeScript |
| ------ | ---------- |
| `find_closest_version` | `resolveVersion` |

Both answer the same question: given a version the caller has in hand, which supported
release should the model be read as. Python's takes the version tuple and consults the
constant list, and `closest` names what it does when the exact release is not supported.
TypeScript's takes the detected string and the list the bundle reports, so both are
arguments, and `resolve` names the same operation over the string form that is canonical
across the boundary.

Neither signature exists in the other language, so neither name is a candidate for
renaming to match: the Python name would describe a search over a list TypeScript does
not have, and the TypeScript name would describe a resolution Python does not perform.

### Generated object types

| Python | TypeScript |
| ------ | ---------- |
| `idfkit._generated_types` | `@idfkit/core/types` |

Python generates one stub set at a time, ships it for the newest EnergyPlus release, and
applies it implicitly to every document through `idfkit/document.pyi`. TypeScript emits
one type map per version and the caller parameterises the document with the map for the
version being read, so an older model is typed as that older model or is left untyped.

Each mechanism is the one its type checker allows. Python cannot select a stub set per
value, so an implicit set is the only thing available; TypeScript has generics, so an
opt-in map is both possible and necessary for version-generic code. The consequence for
a reader is recorded in the parity ledger under `generated-object-types` rather than
left here.

### A version type map

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `AnyTypeMap` |

Absent from Python, and correctly so. TypeScript names the map because the caller
selects one and passes it as a type argument. Python's stubs apply to every document
with nothing for a caller to select, so there is no value and no type to name, and a
Python counterpart would name a choice the Python type checker cannot express.

### Diagnostics from a parse

| Python | TypeScript |
| ------ | ---------- |
| `IDFParseError.diagnostics` | `ParseResult.diagnostics` |

Python raises and TypeScript returns. `IDFParseError` carries the diagnostics that
stopped the parse, which is how a Python caller expects to meet a failure it must
handle, and the recoverable findings go to the logging module. TypeScript's `parseIdf`
returns a `ParseResult` whose `diagnostics` array holds the non-fatal findings alongside
the document, because a throwing parser in a browser costs the caller the partial
document it could still show.

Each is idiomatic where it lives. The difference is visible to a reader, so the parity
ledger records it under `parse-diagnostics` and the corpus asserts what each side
reports for a malformed case.

### Download a weather file

| Python | TypeScript |
| ------ | ---------- |
| `WeatherDownloader.download` | `fetchWeatherFiles` |

Python's downloader is an object because it owns state a Python caller expects it to
own: a cache directory, its own session, and the settings that govern both. TypeScript's
is a free function because it owns none of that. It reaches the network through the
global `fetch`, which the caller overrides per call, and it caches nothing, so there is
no instance for a method to hang on and `fetch` names the platform primitive a
JavaScript reader already knows.

The packaging and freshness consequences are recorded in the parity ledger under
`weather-index`.

### Refresh the station index

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `refreshStationIndex` |

Absent from Python because Python does it without being asked. `StationIndex.load()`
probes upstream at most once every 24 hours, warns when the bundled or cached index is
behind, records the check under the cache directory, and is turned off with
IDFKIT_NO_WEATHER_UPDATE_CHECK, so a Python caller needs no name for the operation.

JavaScript has no writable cache directory to throttle against in a browser, so the same
nudge cannot exist there. It exposes the refresh explicitly instead and does nothing on
its own. A Python counterpart would be a second public path to something already
automatic, which FR-005 prohibits.

### Which field a text search matched

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `MatchField` |

The same six strings on both sides: `wmo`, `name`, `state`, `country`, `filename`, and
the empty string for no match. TypeScript names the union because it appears in a
checked signature, on `SearchResult.matchField`, so a `switch` over it is exhaustive and
a misspelled case is a compile error.

Python annotates `SearchResult.match_field` as `str` and documents the same values on
the field itself. A `Literal` alias there is a fair thing to want and is additive rather
than part of this feature, so this is recorded as a divergence rather than as an
exclusion: it is a name Python may grow later, not one it must never have. Registering
the TypeScript spelling fixes it either way.

### The station wire record

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `StationRecord` |

One station as `stations.json.gz` stores it, with the snake_case keys both libraries
read and write, so that an index refreshed by either side loads in the other. TypeScript
names the record because `WeatherStation.fromJSON` and `toJSON` carry it in their
signatures, and because those keys deliberately do not match the camelCase class they
convert to, which is exactly the mismatch a checked type is for.

Python moves the same content through `WeatherStation.to_dict` and `from_dict` as
`dict[str, Any]`. A TypedDict there would add real checking, so this too is a divergence
rather than an exclusion.

### The station index wire form

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `IndexData` |

The whole serialized index: when it was built, the upstream `Last-Modified` values it
was built against, and the array of station records. TypeScript names it because
`indexFromData` takes it and `loadStationIndex` parses into it, so a caller that fetched
or imported the JSON itself hands over a value the compiler has checked.

Python reads the same file inside `StationIndex.load` and never hands the parsed payload
back, so there is no signature for the type to appear in. As with `the station wire
record`, that is a consequence of who opens the file rather than a name Python must
never have.

### Parse a KML station index

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `parseKml` |

Both libraries build their index by regex over the upstream KML descriptions rather than
through a DOM, and for the same reason: each description is a small HTML table inside a
CDATA block, and a parser with no XML dependency runs in a worker or an edge runtime.

The step is public in TypeScript and private in Python because the two take different
inputs. TypeScript's takes the fetched text, which is the only form a browser ever has,
and the package's own offline index builder runs over that same text. Python's
`_parse_kml` takes a `Path` to a file `StationIndex.refresh` has already downloaded, so
a caller holding KML text could not call it in any case. Publishing it would mean
changing what it accepts first, which is a change to the code rather than to its name.

### Read station metadata from a download URL

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `parseUrlMetadata` |

Country, state, city, and WMO number, recovered from the filename in a station's ZIP
URL. Public in TypeScript because it is the half of index building a caller can reuse on
its own, against a URL it already holds, with no KML anywhere in sight.

Python keeps `_parse_url_metadata` private beside `_parse_kml`, for the same reason that
one is private: the index-building path there is `StationIndex.refresh`, which owns the
whole download, and neither half of it is offered separately.

### Build an index from index data

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `indexFromData` |

Turn an already-parsed `IndexData` into a searchable `StationIndex`, synchronously and
with no I/O. TypeScript needs the name because its callers legitimately hold the
payload: one has fetched it, one has imported it through a bundler, and
`loadBundledIndex` reads it off disk in Node. All three then need the same pure step.

Python has no such caller. `StationIndex.load` opens the file, decompresses it, and
returns the index in one call, and `StationIndex.from_stations` covers the other
construction anyone wants, from stations the caller built itself. A Python counterpart
would be a public name for the middle of a method nobody stands in.

### The upstream index file list

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `INDEX_FILES` |

The ten regional KML files that together cover the globe, identical on both sides down
to the order. TypeScript exports the list because `refreshStationIndex` and
`checkForUpdates` both accept a `baseUrl` and a `fetch`, so a caller routing around the
missing CORS header has to know which ten files will be requested through its proxy.

Python's `_INDEX_FILES` is private because `StationIndex.refresh` offers no such
override: it owns the whole download, so the list names nothing a Python caller could
point anywhere else.

### The upstream index base URL

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `SOURCES_BASE_URL` |

`https://climate.onebuilding.org/sources`, the same string on both sides. Public in
TypeScript for the reason `the upstream index file list` is public: it is the default a
caller replaces through `baseUrl`, and a proxy prefix is built by rewriting it.

Python's `_SOURCES_BASE_URL` is private for the reason its file list is private. Nothing
in the Python API accepts a base URL, so exporting the default would publish a constant
no signature takes.

### Fetch a prebuilt station index

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `loadStationIndex` |

Fetch `stations.json.gz` from a URL, inflate it, and build the index. It exists because
a browser cannot read the copy inside `node_modules`: the page serves that file from its
own origin and points this at it.

Python needs no counterpart, and the absence must not be read as a gap. Its index is
installed with the package and `StationIndex.load` reads it from disk, so there is no
URL to load from. Neither library retrieves an index over the network to get started
(FR-043, FR-075): this names how a browser reaches the copy it was already shipped, not
a different starting point.

### The bundled station index

| Python | TypeScript |
| ------ | ---------- |
| `StationIndex.load` | `loadBundledIndex` |

The same operation, read the index shipped inside the package from disk with no network
call, under two names that cannot be shared.

Python's is `StationIndex.load` because the index is always on disk there: `load` is the
register's verb for reading from a path, the class is the only place to reach it, and a
cached copy written by a refresh is preferred over the bundled one transparently.
TypeScript's says `bundled` because it has to distinguish itself from
`loadStationIndex`, which is the portable path and loads over the network, and because
it lives in `@idfkit/weather/node` where it touches `node:fs`. Spelling it `load` there
would name the disk path as the default in a package whose default runtime has no disk.

Python's `load` also fires the throttled freshness check recorded under `refresh the
station index`. The Node function does not, and has no cache directory to throttle
against.

### Download a station's EPW file

| Python | TypeScript |
| ------ | ---------- |
| `WeatherDownloader.get_epw` | `fetchEpw` |

The shortest path to one station's EPW, and the two libraries return different things
because their callers need different things. Python returns a `Path`, because the file
is in its cache and a path is what EnergyPlus is given. TypeScript returns the EPW text,
because a browser has no disk and the text is what `@idfkit/engine` takes.

The verbs follow the receivers, exactly as in `download a weather file`: `get_` reads
something the downloader's cache already holds or will hold, and `fetch` names the
platform primitive the free function reaches through. Neither could take the other's
spelling without describing something it does not do.

### Download an EPW file by filename

| Python | TypeScript |
| ------ | ---------- |
| `WeatherDownloader.get_epw_by_filename` | `fetchEpwByFilename` |

Resolve a canonical EPW filename to a station through the index, then retrieve that
station's EPW. The same `get_` against `fetch` split as `download a station's EPW file`
above, for the same reason.

The index arrives differently, which is the packaging asymmetry rather than a second
naming disagreement: Python's is an optional keyword defaulting to the bundled index,
because it can always find one on disk. TypeScript's is a required argument, because the
caller had to obtain an index already and the function has nowhere to load one from.

### Download a station's archive

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `fetchWeatherArchive` |

The low-level retrieval step: fetch the station's ZIP and return every member as raw
bytes. Public in TypeScript because it is the only way to reach the members with no
decoded convenience field, `.clm`, `.wea`, `.rain`, and `.pvsyst` among them, and
because a caller can hand the bytes anywhere.

Python reaches the same members as files. `WeatherDownloader.download` extracts the
archive into the cache and hands back `WeatherFiles.zip_path` beside the extracted
paths, so the archive is already addressable, and a method returning bytes would be a
second route to the same content in a language whose caller asked for paths.

### The retrieved weather files

| Python | TypeScript |
| ------ | ---------- |
| `WeatherFiles` | `WeatherFiles` |

Identical names, different values, and recorded rather than reconciled for the same
reason as `version`: `files.epw` is a `Path` in Python and the EPW text in TypeScript,
so code written from one side's documentation reads against the other and is wrong at
runtime.

Each is right where it lives, and the difference is the packaging asymmetry the parity
ledger records under `weather-index`. Python downloads into a cache directory, so paths
are what it has and what it should hand back, and `zip_path` and a guaranteed `ddy`
follow from the same fact. TypeScript writes nothing to disk, so text is the only thing
it can return, and it carries the undecoded members beside the three it decodes as a map
of bytes.

Renaming either side would not fix the collision and would spend a rename budget on
making it harder to find. `write weather files to disk` below names the step that turns
one into the other in Node.

Python's `PartialWeatherFiles`, returned by `download(station, only=...)`, is the same
record with every path optional. It has no TypeScript counterpart and is not a gap:
selective extraction is a property of writing into a cache, and the JavaScript side
decodes from memory whatever the archive held.

### Read a ZIP archive

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `unzip` |

Read a ZIP into a map of member name to bytes. TypeScript ships one and exports it
because JavaScript has no archive reader in its standard library and this package takes
no dependencies: it reads the central directory itself and inflates with
`DecompressionStream('deflate-raw')`, which browsers and Node 20 and later both have.

Python has `zipfile` in its standard library and `WeatherDownloader` uses it directly. A
public `unzip` there would be a wrapper over a module the caller can already import,
which is a public name for an import statement.

### The injectable fetch

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `FetchLike` |

The subset of the `fetch` signature every network call in the package accepts, so that a
caller can substitute its own. It exists because climate.onebuilding.org sends no
`Access-Control-Allow-Origin` header: from a page, the only way to reach it is through a
proxy the caller supplies, and this type is what makes that argument checked rather than
hopeful.

Python has nothing to inject and needs no name for it. `WeatherDownloader` reaches the
network with `urllib.request` and owns its own requests, and a Python caller runs under
no same-origin policy, so a seam here would name an override nobody has a reason to
pass.

### Write weather files to disk

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `saveWeatherFiles` |

Write a retrieved `WeatherFiles` into a directory, Latin-1, the encoding EPW uses, and
return the paths. It is a separate step, and a Node-only one, because the portable half
writes nothing to disk. That is the asymmetry the parity ledger records under
`weather-index`.

Python has no counterpart and lacks nothing. Retrieving and saving are one operation
there: `WeatherDownloader.download` puts the files in its cache directory on the way to
returning their paths, so a second name would be a public spelling for something already
done. The verb is still the register's `save`, so the two surfaces do not disagree about
the word for putting bytes on a disk, only about how many steps it takes to get there.

### The written weather file paths

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `SavedWeatherFiles` |

Where `saveWeatherFiles` put each file, or the absent value for one the archive did not
carry. TypeScript needs a second record because its `WeatherFiles` holds text: the paths
do not exist until a Node caller has written them.

Python needs no second record because its `WeatherFiles` is paths already, which is the
`the retrieved weather files` divergence seen from the disk-writing side.

### A schedule as a series

| Python | TypeScript |
| ------ | ---------- |
| `to_series` | *absent* |

Absent from JavaScript, and not a gap. `to_series` returns a pandas Series, which is the
shape a Python analyst wants and is why the function exists. JavaScript has no pandas
and no equivalent labelled series type in its standard library, so a counterpart would
either invent a container this library has no business defining or wrap an array in a
name that promises more than it delivers. The year's values themselves are covered by `a
schedule's values for a year`, which does port.

### The base error type

| Python | TypeScript |
| ------ | ---------- |
| `IdfKitError` | *absent* |

Python gives every failure the library raises one catchable base, so `except
IdfKitError` holds a whole library's errors in one clause. That is the convention every
Python package a reader already imports follows, and it is why the sixteen classes in
`exceptions.py` all derive from it.

JavaScript's core throws exactly one type, `IdfParseError`, and only when
`ParseOptions.strict` is left on. Everything else it reports as a value. A base class
there would be a class with one subclass and nothing to catch, which names a hierarchy
the library does not have.

### An unknown object type

| Python | TypeScript |
| ------ | ---------- |
| `UnknownObjectTypeError` | *absent* |

Python raises, and this class also derives from `KeyError` so that `doc["Nope"]` behaves
the way a subscript is expected to. JavaScript reports the same condition as a
`ParseDiagnostic`, because a browser caller wants the partial document alongside the
finding rather than instead of it.

The canonical form is the shared diagnostic code the corpus compares on, so the two
libraries agree about the condition even though only one of them names a class for it.

Canonical form across the boundary: **UnknownObjectType**.

### An invalid field

| Python | TypeScript |
| ------ | ---------- |
| `InvalidFieldError` | *absent* |

Python raises, and derives from `AttributeError` so that a mistyped field on an object
in a strict document fails the way attribute access is expected to. JavaScript catches
the same mistake in the type system: the generated type maps make `zone.celing_height` a
compile error, so the runtime condition it still reports is a diagnostic rather than a
throw.

The canonical form is the shared diagnostic code the corpus compares on.

Canonical form across the boundary: **InvalidField**.

### A value outside its range

| Python | TypeScript |
| ------ | ---------- |
| `RangeError` | *absent* |

Python raises when a field value falls outside the minimum or maximum the schema
declares. JavaScript reports it as a diagnostic, and cannot spell the class the same way
in any case: `RangeError` is a built-in global there, so a library type of that name
would shadow a language primitive inside every module that imported it.

The canonical form is the shared diagnostic code the corpus compares on, and it is
`Range` rather than `RangeError` for the same reason: stripping the suffix is what keeps
the code out of the way of the JavaScript global.

Canonical form across the boundary: **Range**.

### A duplicate object

| Python | TypeScript |
| ------ | ---------- |
| `DuplicateObjectError` | *absent* |

Python raises when a name is added twice within one object type. JavaScript reports it
as a diagnostic and keeps parsing, which is what lets a viewer show a model that a
strict reader would have refused.

The canonical form is the shared diagnostic code the corpus compares on.

Canonical form across the boundary: **DuplicateObject**.

### A version mismatch

| Python | TypeScript |
| ------ | ---------- |
| `VersionMismatchError` | *absent* |

Python raises when the version a caller asked for disagrees with the version the
document declares. JavaScript takes the version as an argument to `schemaFor` instead,
so the same disagreement is resolved at the call site rather than raised from inside the
parse.

The canonical form is the shared diagnostic code the corpus compares on.

Canonical form across the boundary: **VersionMismatch**.

### An unsupported version

| Python | TypeScript |
| ------ | ---------- |
| `UnsupportedVersionError` | *absent* |

Python raises when a version outside `ENERGYPLUS_VERSIONS` is requested, which it can do
because the supported set ships with the package and is known at import time.
JavaScript's supported set depends on the bundle the caller supplied, so
`resolveVersion` returns the absent value instead of throwing: it has no standing to
call a version unsupported, only to report that this bundle does not serve it.

The canonical form is the shared diagnostic code the corpus compares on.

Canonical form across the boundary: **UnsupportedVersion**.

### A schema that cannot be found

| Python | TypeScript |
| ------ | ---------- |
| `SchemaNotFoundError` | *absent* |

Python raises when the bundled schema file for a supported version is missing, which is
a packaging failure of the installed distribution. JavaScript reaches its schemas
through a `BundleSource` it does not own, so the same condition surfaces as a rejected
promise from the source rather than as a library type: the library cannot distinguish a
missing file from a network failure, and inventing a class that claimed to would be
wrong more often than right.

The canonical form is the shared diagnostic code the corpus compares on.

Canonical form across the boundary: **SchemaNotFound**.

### A version that cannot be detected

| Python | TypeScript |
| ------ | ---------- |
| `VersionNotFoundError` | *absent* |

Python raises when a file carries no readable `Version` object. TypeScript's
`getIdfVersion` and `getEpJsonVersion` return `undefined` for the same input, which
their own doc comments state as the contract: they exist to break the chicken-and-egg
between choosing a schema and reading the version, so a throw would put the caller back
where it started with nothing to fall back on.

No shared diagnostic code: the corpus vocabulary is derived from the parse hierarchy,
and this condition is detected before a parse begins.

### A validation that failed

| Python | TypeScript |
| ------ | ---------- |
| `ValidationFailedError` | *absent* |

Python raises this when a caller asks for validation to be enforced rather than
reported. The TypeScript counterpart is already registered above and is a value, not a
throw: `validateDocument` returns a `ValidationResult` carrying `ValidationError`
findings, each with a severity and a location. Adding a thrown class beside it would
give the same failure two public shapes in one language.

### A migration that failed

| Python | TypeScript |
| ------ | ---------- |
| `MigrationError` | *absent* |

Python raises when a transition step fails. The registered TypeScript migration surface
reports the same failure through `MigrationReport`, which already carries the per-step
outcome, so the report is the counterpart and a thrown class would be a second way to
learn the same thing.

The TypeScript migration surface is registered above and is not written yet (FR-007).

### A DDY file with no design days

| Python | TypeScript |
| ------ | ---------- |
| `NoDesignDaysError` | *absent* |

Python raises when a DDY file carries no `SizingPeriod:DesignDay`, and the exception
carries the station name and a list of nearby stations that do have design conditions,
which is what makes it actionable rather than merely true. The registered TypeScript
design-day surface, `DesignDayManager`, is not written yet and reports its outcomes as
values like the rest of that side, so the empty file is a result there rather than a
class.

### The newest supported version

| Python | TypeScript |
| ------ | ---------- |
| `LATEST_VERSION` | `SchemaBundle.latest` |

Python's answer is a constant because the schemas ship with the package, so the newest
supported release is known at import time and `LATEST_VERSION` can be read without a
call. TypeScript's answer depends on which bundle the caller supplied, so it is a query
on that bundle and it is asynchronous for the same reason `SchemaBundle.load` is. A
constant there would name a release the library does not control.

This is the `the supported version list` divergence applied to one member of that list,
and the same canonical form applies: Python's value is a tuple, TypeScript's is a
string, and the string is what crosses the boundary.

Canonical form across the boundary: **string**.

### The oldest supported version

| Python | TypeScript |
| ------ | ---------- |
| `MINIMUM_VERSION` | *absent* |

Python names the oldest supported release as a constant, beside `LATEST_VERSION`, for
the same reason it can name the newest one. TypeScript names nothing, and correctly so:
`SchemaBundle.versions` returns the bundle's versions oldest first, so the answer is the
first element of a list the caller already has, and a second asynchronous method
returning it would be a public name for an array index.

Canonical form across the boundary: **string**.

### Render a version as text

| Python | TypeScript |
| ------ | ---------- |
| `version_string` | *absent* |

Absent from TypeScript, and not a gap. Python's version is a tuple, so turning it into
the canonical string needs a function, and the `version` entry above already names
`version_string` as the renderer the corpus asserts against. TypeScript's version is
that string already, so a counterpart would be the identity function under a name that
promised a conversion.

Canonical form across the boundary: **string**.

### Whether a version is supported

| Python | TypeScript |
| ------ | ---------- |
| `is_supported_version` | *absent* |

Absent from TypeScript, and not a gap. Python can answer the question from
`ENERGYPLUS_VERSIONS`, a constant, so a predicate over it is cheap and honest.
TypeScript's supported set belongs to the bundle the caller supplied, so the same
question is already answered by `resolveVersion` returning the absent value, and a
separate predicate would either ask the bundle twice or answer for a set the library
does not own.

### One version's schema

| Python | TypeScript |
| ------ | ---------- |
| `EpJSONSchema` | `Schema` |

The same object on both sides, one EnergyPlus version's schema, with the format in the
Python name and not in the TypeScript one. Python has a flat top-level namespace where
`Schema` alone would sit beside `SchemaManager` and say nothing about which of the two
formats it describes, so the qualifier earns its place. TypeScript's is exported from
`@idfkit/schemas` and is reached through that import, so `EpJsonSchema` would repeat the
package name at every call site and read as the stutter the `objects referencing a name`
entry rejects for the same reason.

### The schema source

| Python | TypeScript |
| ------ | ---------- |
| `SchemaManager` | `SchemaBundle` |

Each name says what its own object is, and the two objects are genuinely different.
Python's `SchemaManager` manages schemas the package already owns: it finds the file for
a version, parses it, and caches the result, so `manager` names the work. TypeScript's
`SchemaBundle` owns no schemas at all; it wraps a `BundleSource` the caller supplied and
serves versions out of it, so `bundle` names the thing it was handed.

Renaming either to the other would be a misdescription rather than an alignment: there
is no bundle in Python and nothing to manage in TypeScript.

### The process-wide schema source

| Python | TypeScript |
| ------ | ---------- |
| `get_schema_manager` | `schemas` |

Both return the one instance a process should hold, so that loading 26.1.0 and then
9.4.0 costs far less than twice one version. The names diverge because the objects do,
which is the divergence recorded directly above: Python's accessor is named after the
`SchemaManager` it returns, and TypeScript's is named after the schemas the default
bundle serves.

TypeScript's also lives in `@idfkit/core/node`, because the default bundle reads from
disk. That is the input and output divergence, and it is why the plural noun rather than
a `get` verb: a caller writes `schemas()` once and hands the result to `schemaFor`,
where `getSchemaBundle` would name the container instead of the contents.

### The IDF parser object

| Python | TypeScript |
| ------ | ---------- |
| `IDFParser` | *absent* |

Python exposes the parser as an object because it holds state worth reusing: a file
path, an encoding, a memory-mapped view of the content, and a loaded schema, so a caller
parsing the same file at several versions constructs it once. `parse_idf` is the
one-line front door over it and is the name the documentation teaches.

TypeScript's `parseIdf` is a pure function that takes the text and the schema as
arguments and holds nothing between calls, which is what lets it run unchanged in a
browser or a worker. A class there would be a function with a constructor in front of
it.

`parse IDF from a string` above is the operation. This entry is the Python object that
implements it.

### The difference between two schema versions

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `SchemaDelta` |

TypeScript names the delta because `Schema` hands it out, so it is part of the package's
public shape whether or not anyone asked for it. Python computes the same comparison
inside `idfkit.compat` and keeps the result type private, reaching it only through
`diff_schemas`, which is registered above.

Recorded rather than reconciled: the operation is registered and aligned, and only one
side has a public name for what it returns.

### Resolve the schema for a detected version

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `schemaFor` |

Absent from Python because Python has nothing to resolve. `get_schema(version)` takes
the version and returns the schema, synchronously, from the package's own files.

TypeScript needs the step and exports it: the version arrives as a string detected from
the file, the bundle is asynchronous and caller-supplied, and the caller may have
overridden the version or the bundle through `LoadOptions`. It is exported rather than
kept internal because a caller who parses text itself still has to take this step, and
taking it wrongly, loading 26.1 for a 9.0 file, mis-maps every positional field silently
instead of failing.

### A reference edge

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `ReferenceEdge` |

One field of one object pointing at a name, with the repeat index when the field lives
inside an extensible group. TypeScript names the record because `referencing`,
`retarget`, and `dangling` all return it, and a reader meeting `edge.from`,
`edge.field`, `edge.target` at the call site can see what it is.

Python returns the same three values as an anonymous `tuple[IDFObject, str, str]` from
`get_dangling_references` and names nothing, so a caller unpacks by position. That is
worth recording rather than hiding: the two libraries carry the same information and
only one of them says what the parts are.

A Python counterpart would be additive and is not part of this feature. Registering the
TypeScript name fixes the spelling either way.

### An epJSON document value

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `EpJson` |

The epJSON document as a value, type to name to field values. TypeScript names it
because `parseEpJson` accepts it as an alternative to text and `toEpJson` returns it, so
it appears in two public signatures.

Python passes and returns plain dictionaries at the same points, and `dict[str, Any]` is
what a Python reader expects there. A type alias for it would be a name that adds no
checking, since the value is a nested `Any` at every level.

### Serialize one object

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `writeObject` |

TypeScript exports the single-object writer because the whole-document writer is built
out of it and a caller assembling IDF text by hand, a diff view or a snippet in a
report, needs the same field alignment the document writer produces.

Python renders one object through `IDFObject.__str__`, which is the idiomatic place for
it: `str(obj)` and `print(obj)` already work, and a module-level `write_object` would be
a second public spelling of something the language already provides at the object.

### Serialize a document to an epJSON value

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `toEpJson` |

TypeScript separates producing the epJSON value from producing epJSON text, because a
JavaScript caller usually wants the value: it is already a JavaScript object, and
stringifying it only to parse it again would be work for nothing.

Python's `write_epjson` returns the text, and the same conversion is reached at
`idfkit.writers.EpJSONWriter.to_dict` rather than as a module-level function. Promoting
it would be additive and is not part of this feature.

`serialize epJSON to a string` above is the text-producing operation and is aligned on
both sides.

### Read IDF from disk, keeping diagnostics

| Python | TypeScript |
| ------ | ---------- |
| *absent* | `loadIdfWithDiagnostics` |

TypeScript needs two loaders because it returns rather than raises: `loadIdf` hands back
the document and drops the non-fatal findings, and this one hands back the `ParseResult`
with both. A single loader would either force every caller to unwrap a result they
usually do not want, or throw away findings a viewer wants to show.

Python needs only `load_idf`, because the findings that stop a parse arrive on
`IDFParseError` and the recoverable ones go to the logging module. That is the
`diagnostics from a parse` divergence, seen from the disk-reading side.

### The path a document was read from

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.filepath` | *absent* |

Python's `load_idf` opens the file itself, so the document it returns knows where it
came from and error messages can say so.

TypeScript's core never sees a path. `@idfkit/core/node` reads the text and hands it to
the pure `parseIdf`, which is what lets the same function run in a browser, so a
`filepath` on the document would be absent on every document a browser produced and
misleading on the rest. This is the input and output divergence, seen from the document.

### Strict field access

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.strict` | *absent* |

Python's `strict` is a property of the document: with it on, reading or writing an
unknown field name raises `InvalidFieldError` instead of returning `None`. It is
read-only and set through the constructor, and it is also a type parameter, so the
checker knows which behaviour a document has.

TypeScript needs no such switch, because the generated type maps reject an unknown field
at compile time, which is the same protection earlier and without a runtime mode.

Recorded because of a collision a reader will otherwise walk into: TypeScript's
`ParseOptions.strict` is a DIFFERENT setting with the same word, meaning throw on the
first parse diagnostic rather than collect them. The two are not the same switch and
neither is renamed here, because each is the correct word for its own setting; the
register's job is to say so out loud.

### The concrete syntax tree

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.cst` | *absent* |

Present only when the document was read with `preserve_formatting=True`, and it is what
lets `write_idf` reproduce the original text byte for byte.

TypeScript has no counterpart because it has no lossless round-trip yet: `writeIdf`'s
own doc comment states the caveat plainly, that `3.0` comes back as `3` because
JavaScript has one number type and the distinction is lost at parse time. The parity
ledger records the absence under `lossless-round-trip` as Tier 2, and `preserve
formatting on a round-trip` above registers the option name ahead of it.

### The original source text

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.raw_text` | *absent* |

The other half of the formatting-preserving round-trip, beside `cst`: the source as it
was read, kept only when `preserve_formatting=True`. Absent from TypeScript for the same
reason and recorded under the same parity entry.

### Every collection in a document

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.collections` | *absent* |

Python hands out the whole map of object type to collection, which is a plain dict a
Python reader iterates without being taught anything.

TypeScript exposes no equivalent. Its typed path is `types()` and `all()`, and handing
out the internal map would be an untyped second route to the same objects: exactly what
withdrawing `collection()` removed, recorded above under `untyped collection access`.

### The object types present in a document

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.keys` | `types` |

Both return the object type names the document actually holds. Python's document
implements the mapping protocol, since `doc["Zone"]` is its idiomatic access, and `keys`
is the word that protocol requires: a Python reader who has seen `doc[...]` will reach
for `keys()`, `values()`, and `items()` without being told.

TypeScript's document is not a Map and cannot be one, for the reason recorded under
`every object of a type`, so `keys` there would promise a protocol the class does not
implement. `types()` says what the strings are instead.

### Every non-empty collection

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.values` | *absent* |

The second member of Python's mapping protocol, beside `keys` and `items`. It exists
because the first one does: a class that offers `keys()` and stops is a mapping that
half works.

TypeScript implements no mapping protocol, so there is nothing for it to complete. The
same content is reached by mapping `types()` through `all()`, which stays typed, where a
`values()` returning every collection could not be.

### Every object type and its collection

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.items` | *absent* |

The third member of Python's mapping protocol. Absent from TypeScript for the same
reason as `values`, and reached there by pairing `types()` with `all()`.

### An object's outgoing references

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.get_references` | `referencedBy` |

The receiver carries the difference, exactly as it does for `objects referencing a
name`, and this is that entry's mirror image. Python hangs the query on the document,
`IDFDocument.get_references(obj)`, because the graph is reached through the document
there. TypeScript hangs it on the graph, `doc.references.referencedBy(obj)`, where
`getReferences` would read as `references.getReferences` and say the word twice.

Both answer the same question, which names does this object point at, and the pair of
them is why neither language can borrow the other's spelling without stuttering on one
side.

### A model's schedules by name

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.schedules_dict` | *absent* |

A cached map from schedule name to object, spanning every `Schedule:*` type at once,
which is what makes repeated schedule lookup cheap in a model with thousands of them.

Absent from TypeScript, where schedules are a Tier 2 capability the parity ledger
records as not yet ported. The name is not registered ahead, unlike the rest of the
schedules group, because the `_dict` suffix names a Python container: it is the
`to_list` against `toArray` case, and fixing a TypeScript spelling now would fix the
wrong one.

### Every object in a document

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.all_objects` | `objects` |

Both walk every object in the document lazily. Python needs the `all_` qualifier because
a bare `objects` on a document whose `collections` is a map of objects would read as
that map, and because `objects_by_type` sits beside it; it is a property rather than a
method because a lazy view spelled as a property is what a Python reader expects of an
iterable attribute.

TypeScript has neither neighbour, so `objects()` is unambiguous there, and it is a
method because a property returning a fresh generator on each read is a trap in
JavaScript: two reads would silently give two independent iterators.

### An object's name changed

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.notify_name_change` | `onNameChanged` |

The same hook: an object tells its document that its name changed, so the collection can
be re-keyed and every reference to the old name repointed. Both are public because the
object calls them from outside the class, not because a user is meant to.

Python names the direction, `notify_*`, which is how a Python reader reads a callback
the callee invokes on its owner. TypeScript names the event, `on*Changed`, which is the
JavaScript convention and is what the `ObjectOwner` interface has to declare for a
detached object to stay free of the document.

### An object's field changed

| Python | TypeScript |
| ------ | ---------- |
| `IDFDocument.notify_reference_change` | `onFieldChanged` |

The other half of the hook pair above, and the same naming split, `notify_*` against
`on*Changed`.

The nouns differ too, and honestly: Python's fires only for fields the schema marks as
references, which is why it says `reference`, and TypeScript's fires for any field and
filters inside `updateField`, which is why it says `field`. Each name describes what its
own implementation does. Whether the two should agree on when they fire is a behaviour
question for the corpus, not a naming one, and renaming either without changing that
would make the name wrong.

### Migrate a model without blocking

| Python | TypeScript |
| ------ | ---------- |
| `async_migrate` | *absent* |

Python ships a second entry point because its ecosystem is synchronous by default:
`migrate` blocks while the transition binaries run, and an async caller needs a name of
its own rather than a thread.

TypeScript needs no second name because the registered `migrate` is async by
construction, like everything else that reaches a disk there. A TypeScript
`asyncMigrate` would be the same function under two names, which FR-005 prohibits. This
is the input and output divergence, seen from the migration side.

`migrate a model to a newer version` above is the operation. Its note already names this
pair; this entry gives the second name a concept of its own.

## The canonical form across the boundary

A divergence in a name costs you a lookup. A divergence in a value costs you a bug,
because the code reads the same in both languages and behaves differently. Where the two
libraries hold one thing in two shapes, the register names the text form both sides
render, and the conformance corpus asserts that they render it identically for the same
model.

| Concept | Python | TypeScript | Canonical form |
| ------- | ------ | ---------- | -------------- |
| declared conformance level | `idfkit.CONFORMANCE_LEVEL` | `CONFORMANCE_LEVEL` | string |
| [version](#version) | `doc.version` | `doc.version` | string |
| [the supported version list](#the-supported-version-list) | `ENERGYPLUS_VERSIONS` | `SchemaBundle.versions` | string |
| [an unknown object type](#an-unknown-object-type) | `UnknownObjectTypeError` | *absent* | UnknownObjectType |
| [an invalid field](#an-invalid-field) | `InvalidFieldError` | *absent* | InvalidField |
| [a value outside its range](#a-value-outside-its-range) | `RangeError` | *absent* | Range |
| [a duplicate object](#a-duplicate-object) | `DuplicateObjectError` | *absent* | DuplicateObject |
| [a version mismatch](#a-version-mismatch) | `VersionMismatchError` | *absent* | VersionMismatch |
| [an unsupported version](#an-unsupported-version) | `UnsupportedVersionError` | *absent* | UnsupportedVersion |
| [a schema that cannot be found](#a-schema-that-cannot-be-found) | `SchemaNotFoundError` | *absent* | SchemaNotFound |
| [the newest supported version](#the-newest-supported-version) | `LATEST_VERSION` | `SchemaBundle.latest` | string |
| [the oldest supported version](#the-oldest-supported-version) | `MINIMUM_VERSION` | *absent* | string |
| detect a document version | `get_idf_version` | `getIdfVersion` | string |
| detect an epJSON document version | `idfkit.epjson_parser.get_epjson_version` | `getEpJsonVersion` | string |
| [render a version as text](#render-a-version-as-text) | `version_string` | *absent* | string |

The rule to carry away: keep each language's idiomatic shape in memory, and move the
canonical form across the boundary. Anything written to a file, sent in a message, or
compared in a test fixture is crossing the boundary.

## Surfaces that stay in one language

Excluded does not mean "not yet". It is terminal: a counterpart appearing in the other
language fails the gate, and adding one takes an amendment to the register reviewed by
both languages. These surfaces are excluded because their names are quotations rather
than choices. They reproduce another ecosystem's spelling, or they name a mechanism the
other runtime does not have.

### Untyped collection access

**Python**: `IDFDocument.get_collection`.

**TypeScript**: none, and never.

`IdfDocument.collection()` was public in `@idfkit/core@0.1.0` and is withdrawn to
in-package use. Two public methods for one operation is what FR-005 prohibits, and
`all()` is the designed public surface: `collection()`'s own doc comment describes
itself as the escape hatch that exists so the single unavoidable cast lives in one
place. The version-generic case that would argue for keeping it is already covered,
because `all()` accepts unknown type names and returns them untyped.

Python's `get_collection` stays public: it is the named alternative to the `doc["Zone"]`
operator rather than a second untyped path, and Python has no generated type map
narrowing to lose. Recorded per research R1.

TypeScript's rename count is 1 and is spent on the withdrawal, which is as breaking as a
rename and must not happen twice. No third name is introduced: `untyped()` was
considered and rejected, because it would still be two public names and would invite
users onto the untyped path for a case `all()` already handles.

### Eppy compatibility surface

**Python**, 15 names:

- `addidfobject`
- `newidfobject`
- `popidfobject`
- `removeidfobject`
- `removeallidfobjects`
- `getiddgroupdict`
- `getobject`
- `getsurfaces`
- `idfobjects`
- `saveas`
- `savecopy`
- `theidf`
- `fieldnames`
- `getreferingobjs`
- `IDFObject.Name`

**TypeScript**: none, and never.

Fifteen aliases that exist to let code written against eppy, a Python library, run
unchanged against idfkit. They are correct in Python precisely because they are NOT
idiomatic: they reproduce another Python library's spelling, lowercase-run-together and
all, so that a migration is a one-line import change. `getreferingobjs` even reproduces
eppy's misspelling of "referring", which is the clearest possible evidence that these
names are quotations rather than choices.

JavaScript has no eppy and no code to migrate, so a JavaScript counterpart would import
a foreign Python library's spelling into a language that never had it, and would add
fifteen public names that nothing calls. They are listed here individually, rather than
described as a category, because a category is something a future contributor can
misread as "port these too". A name written out is not portable by accident.

Excluded is terminal. A counterpart appearing on the TypeScript side fails the gate.
Adding one requires amending this entry, reviewed by both languages.

Live at `idfkit/src/idfkit/_compat.py` (`EppyDocumentMixin`, mixed into `IDFDocument`)
and `idfkit/src/idfkit/_compat_object.py` (`EppyObjectMixin`, mixed into `IDFObject`).
The fifteen above are the register's named exclusions; the same exclusion covers the
whole of both mixins, including the further eppy members reachable from the same surface
(`addidfobjects`, `removeidfobjects`, `copyidfobject`, `key`, `fieldvalues`,
`getfieldidd`, `getfieldidd_item`, `getrange`, `checkrange`, `save`, `run`, `update`).
None of them crosses to TypeScript either.

### The weather options-object types

**Python**: none, and never.

**TypeScript**, 10 names:

- `SearchOptions`
- `NearestOptions`
- `FilterOptions`
- `LoadIndexOptions`
- `RefreshIndexOptions`
- `FetchWeatherOptions`
- `GeocodeOptions`
- `DetectLocationOptions`
- `SaveWeatherFilesOptions`
- `WeatherStationFields`

Ten interfaces naming argument objects, under one entry for the same reason `the
options-object types` covers the five in `@idfkit/core`: TypeScript has to name an
option bag, because it arrives as one argument and its type is what makes a misspelled
option a compile error instead of a silently ignored key, and Python passes the same
options as keyword arguments, which the language names and checks at the call site by
itself.

Nine are options in the plain sense, on `search`, `nearest`, `filter`,
`loadStationIndex`, `refreshStationIndex`, the three retrieval functions, `geocode` and
`detectLocation`, and `saveWeatherFiles`. The tenth, `WeatherStationFields`, is the same
mechanism at a constructor rather than at a call: `new WeatherStation(fields)` takes one
object, so its shape needs a name, where Python's `WeatherStation` is a frozen dataclass
whose constructor keywords are that list already.

Excluded is terminal. A Python counterpart appearing later fails the gate.

Option NAMES are not excluded here, only the containers that carry them. An option that
is a concept of its own gets its own entry, as `preserve formatting on a round-trip`
does, and the `fetch` these bags accept is typed by `the injectable fetch` above.

### The local simulation surface

**Python**, 19 names:

- `simulate`
- `simulate_batch`
- `async_simulate`
- `async_simulate_batch`
- `async_simulate_batch_stream`
- `find_energyplus`
- `expand_objects`
- `run_preprocessing`
- `EnergyPlusConfig`
- `SimulationResult`
- `BatchResult`
- `SimulationCache`
- `SimulationJob`
- `SimulationProgress`
- `ESOResult`
- `CSVResult`
- `SQLResult`
- `TimeSeriesResult`
- `ErrorReport`

**TypeScript**: none, and never.

Running a locally installed EnergyPlus needs the installation and a subprocess to drive
it, then reads the eplusout files that run leaves on disk. Neither the installation nor
the subprocess exists in a browser, which is the runtime the JavaScript library targets,
so these names are correct in Python precisely because they name a mechanism JavaScript
cannot have.

JavaScript reaches EnergyPlus by the other mechanism, a WebAssembly build in
`@idfkit/engine`, which is a different capability rather than a workaround for this one.
Recording a JavaScript counterpart here would make one language read as deficient at
something it does not lack, which is what FR-068 and FR-078 forbid.

Narrowed on purpose. Choosing which variables to ask for and drawing the results are
both pure and both portable, so `select output variables for a run` and the plotting
group above are registered rather than excluded.

Live under idfkit/src/idfkit/simulation/. The names above are the register's named
exclusions; the same exclusion covers the rest of that subpackage, including the
FileSystem family, the progress reporters, and the remaining result readers. None of
them crosses to TypeScript.

### The vector image surface

**Python**, 9 names:

- `construction_to_svg`
- `generate_construction_svg`
- `view_model`
- `view_floor_plan`
- `view_exploded`
- `view_normals`
- `ColorBy`
- `ModelViewConfig`
- `SVGConfig`

**TypeScript**: none, and never.

All nine produce a vector image handed back for a notebook, a report, or a file on disk,
which is a Python workflow. A JavaScript caller wanting to look at a model is already in
a runtime that draws and is served by the other mechanism, `@idfkit/viewer`, which
renders an interactive scene. The two are different capabilities, and merging them would
make each language read as missing something the other has.

Excluded is terminal here for the same reason it is terminal for the eppy surface: a
JavaScript counterpart would add public names that nothing calls, in a runtime that
already draws.

Live at idfkit/src/idfkit/visualization/, nine exports, verified against `__all__`.
`construction_to_svg` and `generate_construction_svg` are two public names for one
operation, which FR-005 prohibits; that duplicate is resolved by the change that
withdraws one, not here.

### The local simulation error types

**Python**, 3 names:

- `EnergyPlusNotFoundError`
- `ExpandObjectsError`
- `SimulationError`

**TypeScript**: none, and never.

Three failures of the mechanism `the local simulation surface` already excludes: no
EnergyPlus installation was found, the ExpandObjects preprocessor failed, and the
simulation itself failed. Each names a subprocess or an installation, and neither exists
in a browser, so each is correct in Python precisely because it names something
JavaScript cannot have.

They are listed here rather than folded into the `the local simulation surface` entry
because they live in `exceptions.py` and are exported from the top level, so a reader
meets them on `idfkit.` completion rather than inside `idfkit.simulation`.

Excluded is terminal. A counterpart appearing on the TypeScript side fails the gate.

### Version string ordering

**Python**: none, and never.

**TypeScript**, 2 names:

- `compareVersions`
- `versionKey`

Two JavaScript names that exist only because TypeScript's version is a string. Plain
string ordering puts 8.9.0 after 22.1.0, so the library computes a numeric sort key and
compares on that.

Python needs neither and must never grow them. Its version is `tuple[int, int, int]`,
which the built-in comparison operators already order correctly, which is exactly why
`ENERGYPLUS_VERSIONS`, `LATEST_VERSION`, `MINIMUM_VERSION`, and `find_closest_version`
are all tuples. A Python `compare_versions` would be a public name for `<`.

Excluded is terminal. A Python counterpart appearing later fails the gate.

### The schema bundle source surface

**Python**: none, and never.

**TypeScript**, 2 names:

- `BundleSource`
- `httpSource`

The one runtime-specific seam in `@idfkit/schemas`: an interface saying where bundle
files come from, and the fetch-based implementation of it for browsers. They exist
because JavaScript runs in places that have no filesystem, and everything above the
interface is portable precisely because the seam is named.

Python must never grow a counterpart. Its schemas are installed with the package and
read from disk by `SchemaManager`, so a `BundleSource` there would be an abstraction
over one implementation, and an `http_source` would invite a Python caller to fetch over
the network what is already on their disk.

Excluded is terminal. A Python counterpart appearing later fails the gate.

### The slimmed schema record types

**Python**: none, and never.

**TypeScript**, 2 names:

- `SlimType`
- `SlimField`

The two record shapes `@idfkit/schemas` hands out: one object type as the bundle stores
it, and one field of it. They are public because a TypeScript caller reading
`type.x.fields` needs a checked shape for what it is reading, and because `ObjectShape`
is built from them.

Python reads the same content as the nested dictionaries the epJSON schema already is,
through `EpJSONSchema`'s methods, and its reader-facing view of a type is
`ObjectDescription` and `FieldDescription`, which are registered above and are a
different thing: a description assembled for a human, not the storage record. Naming the
storage records in Python would add public types with no accessor of their own.

Excluded is terminal. A Python counterpart appearing later fails the gate.

### The options-object types

**Python**: none, and never.

**TypeScript**, 5 names:

- `ParseOptions`
- `LoadOptions`
- `WriteIdfOptions`
- `ObjectWriteOptions`
- `WriteEpJsonOptions`

Five interfaces that name the option bags `parseIdf`, `loadIdf`, `writeIdf`,
`writeObject`, and `writeEpJson` accept. TypeScript has to name them: an options object
is one argument, and its type is what makes a misspelled option a compile error instead
of a silently ignored key.

Python passes the same options as keyword arguments, which are named and checked at the
call site by the language itself, so a Python counterpart would be a dataclass nobody
constructs, sitting between the caller and a signature that already reads better. The
`add an object` entry records the same difference from the other end, where Python's
keyword form has no TypeScript equivalent and the values arrive as an object literal
instead.

Excluded is terminal. A Python counterpart appearing later fails the gate.

Option NAMES still align: `preserve_formatting` against `preserveFormatting` is
registered above as its own concept. This entry excludes the container types, not the
options they carry.

### The static typing surface

**Python**: none, and never.

**TypeScript**, 4 names:

- `TypeNameOf`
- `ObjectOf`
- `ValuesOf`
- `UntypedMap`

Four type-level helpers that make `doc.all('Zone')` resolve to a collection of objects
with `Zone`'s fields: the accepted type names for a map, the field interface for one of
them, the values accepted when creating one, and the map of a document with no version
types attached. They are erased at build time and none of them exists once the code is
running.

Python cannot express any of it. Its stubs apply implicitly to every document, with
nothing for a caller to select, which is the divergence `generated object types` and `a
version type map` already record. A Python counterpart would name a choice its type
checker cannot make.

Excluded is terminal. A Python counterpart appearing later fails the gate.

`AnyTypeMap`, the base constraint these are written against, has its own entry above.

### The per-type prototype surface

**Python**: none, and never.

**TypeScript**, 3 names:

- `ObjectShape`
- `shapeFor`
- `shapeOf`

JavaScript's answer to `__getattr__`. Python resolves `zone.ceiling_height` at runtime
through a lookup hook; the mechanical translation of that is a `Proxy`, which the
library deliberately does not use because proxies defeat inline caches and are invisible
to TypeScript, so nothing would complete. Instead each object type gets one prototype
carrying real accessors, built once and shared, and `ObjectShape` is that prototype plus
the field metadata the graph and the writer read off it.

Python already has the hook these three replace, so a counterpart there would be a
second, slower way to do what the language does for free.

Excluded is terminal. A Python counterpart appearing later fails the gate.

### The object-model value types

**Python**: none, and never.

**TypeScript**, 4 names:

- `FieldValue`
- `StoredValue`
- `FieldValues`
- `ObjectOwner`

Three types naming what a field slot may hold and one interface naming what an object
needs from whatever owns it. TypeScript must name all four because they appear in
checked signatures, and `ObjectOwner` in particular is an interface rather than a
reference to the document class so that a detached object carries no dependency on the
document at all.

Python needs none of them. A field value is whatever the schema says it is, checked at
runtime by `IDFObject`, and an object reaches its document through an attribute rather
than through a declared interface. Naming them in Python would add four public types
that no signature would be improved by.

Excluded is terminal. A Python counterpart appearing later fails the gate.

### The lexer surface

**Python**: none, and never.

**TypeScript**, 4 names:

- `lex`
- `RawObject`
- `LexDiagnostic`
- `LexOptions`

JavaScript splits IDF text into raw objects before any schema is involved, and exports
that step: a hand-written character scan, the raw object it yields, and its diagnostic
and option types. The split is what makes the diagnostics linear-time and line-accurate,
and it is what lets a caller read a file whose version is not yet known.

Python tokenises inside `IDFParser.parse` with a regex and exposes no lexer. Exporting
one would be a second public parse path over the same text, which FR-005 prohibits, and
it would publish an internal representation that the concrete syntax tree, registered
above as `preserve formatting on a round-trip`, already covers for the one case a caller
has a reason to see.

Excluded is terminal. A Python counterpart appearing later fails the gate.

### Run the ExpandObjects preprocessor

**Python**: `IDFDocument.expand`.

**TypeScript**: none, and never.

Replaces `HVACTemplate:*` objects with their low-level equivalents and returns a new
document. It does that by running the ExpandObjects binary that ships with an EnergyPlus
installation, in a subprocess, which is the mechanism `the local simulation surface`
already excludes and which a browser does not have.

It is listed separately from that entry because it hangs on the document rather than
living in `idfkit.simulation`, so a reader meets it on `doc.` completion.

Excluded is terminal. A counterpart appearing on the TypeScript side fails the gate.

### Second Python spellings of a registered concept

**Python**, 4 names:

- `ParseError`
- `intersect_match`
- `IDFDocument.describe`
- `IDFDocument.objects_by_type`

**TypeScript**: none, and never.

Four Python names, each a second public spelling of a concept whose registered name is
elsewhere in this file. They are listed here so that the gate sees the whole surface,
and listed individually so that no future contributor reads a category and ports them.

`ParseError` is bound to `IdfKitError`, not to `IDFParseError`, and is kept so that code
written against an older release still imports. Note the trap: the corpus's shared
diagnostic code `ParseError` is derived from `IDFParseError`, so the Python name and the
shared code are the same word for two different things.

`intersect_match` is a second name for `intersect_and_match`, which the `intersect and
match surfaces` entry already records as the surviving one.

`IDFDocument.describe` is the document-bound spelling of `describe_object_type`, which
the `describe an object type` entry already records as the registered name. The two take
different arguments, the method supplying the document's own schema, but they answer one
question.

`IDFDocument.objects_by_type` yields exactly what `items` returns, lazily rather than as
a list.

None of the four is a name JavaScript should acquire: each would import a Python
duplicate into a language that never had the original. Excluded is terminal, and a
counterpart appearing on the TypeScript side fails the gate.

This entry covers the surface. It does not resolve the FR-005 duplication, which is
resolved by the change that withdraws or renames each name, as the `intersect and match
surfaces` and `the vector image surface` entries already say for their own duplicates. A
withdrawal counts as a rename, so each of these has one budget to spend and no more.

## Names that have spent their rename

Every name gets one rename during the unification. One. A name that has spent it is
frozen: the gate blocks the change that would take it to a second, and unblocking it
takes an amendment saying why the first rename was wrong. A user absorbs one rename with
a changelog entry and a search-and-replace, and absorbs a second by concluding the
library is unstable.

| Concept | Name | Language | Renames |
| ------- | ---- | -------- | ------- |
| write IDF to disk | `save_idf` | Python | 1 |
| write epJSON to disk | `save_epjson` | Python | 1 |
| [the document class](#the-document-class) | `IdfDocument` | TypeScript | 1 |
| [untyped collection access](#untyped-collection-access) | *withdrawn* | TypeScript | 1 |
| detect a document version | `getIdfVersion` | TypeScript | 1 |
| detect an epJSON document version | `getEpJsonVersion` | TypeScript | 1 |

A withdrawal counts as a rename. It is at least as breaking, and it must not happen
twice to one name either.

## Package names reserved before their ports

No package below is built yet, and the shared install map gains no entry for any of
them: an entry that resolves to nothing breaks a clean install, which is worse than an
unreserved name. The reservation exists because an npm package name cannot be corrected
after publication, and a name chosen at the moment its port begins is a name chosen by
one language under schedule pressure.

| Capability | npm package | Subpath | Mirrors | Tier | Built |
| ---------- | ----------- | ------- | ------- | ---- | ----- |
| schedules | `@idfkit/schedules` | `idfkit/schedules` | `idfkit.schedules` | 2 | not yet |
| geometry, geometry builders, surface matching, zoning | `@idfkit/geometry` | `idfkit/geometry` | `idfkit.geometry`, `idfkit.geometry_builders`, `idfkit.surface_matching`, `idfkit.zoning` | 2 | not yet |

## What the gate refuses

The gate that reads the register refuses a pull request when:

- **A public name has no entry.** It reports the name, its library, and the file it is
  exported from.
- **A concept has two public names in one language.** It reports the concept and both
  names.
- **An excluded entry gains a counterpart in the other language.** It reports the
  concept and the offending name.
- **A divergent entry has no divergence_reason.** It reports the concept.
- **A change takes a name to rename_count 2.** It reports the name and its first rename.

It passes when every public name in both libraries resolves to an entry.

Changing the register itself needs a maintainer of the other language, enforced by
CODEOWNERS in both repositories.

Names that were never meant to be public are not registered to keep the gate quiet. They
are deleted. A public surface that leaks an import or an assembly artefact fails
outright, and adding an entry for one is the wrong fix.

<!-- END GENERATED FROM naming.toml. -->
