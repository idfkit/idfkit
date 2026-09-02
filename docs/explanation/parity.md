# About capability parity

Two libraries now answer to one name. That is the point of the unification, and
it is also its sharpest risk. Once both are called `idfkit`, a reader who finds
something in Python and not in JavaScript has no way to tell whether they have
met a deliberate boundary or a defect, and the reasonable assumption is defect.

The parity ledger removes the guesswork. Every public capability of either
library appears on it exactly once, with its availability in both languages, and
every absence is described rather than left to be discovered. A written-down
absence is documentation. An undocumented one is a bug report waiting to be
filed against behaviour that is working as designed.

This page is the reader-facing view of that ledger. Everything below the
generated marker comes from `governance/parity.toml` in the
[conformance repository](https://github.com/idfkit/idfkit-conformance), read at
the immutable governance tag this release pins, so the page you are reading and
the file both libraries' CI gates read cannot disagree. For the vocabulary side
of the same governance, which name each concept carries in each language, see
[the naming map](naming-map.md).

## Three states, not two

A capability is `complete`, `partial`, or `absent` in each language.

The middle state is the one that earns its keep. A capability that exists in
both languages and behaves differently is neither present nor absent, and
calling it present is precisely the lie this ledger exists to prevent. Anything
recorded as `partial` carries a description of what differs, because `partial`
with nothing said about it is indistinguishable from `complete`.

## Two kinds of absence

An absence alone tells you almost nothing. What you need to know is whether to
wait or to plan around it, so every absent side is recorded as one of two kinds.

- **Not yet.** The second language could have this and does not have it today.
  The entry names the issue tracking the port. Expect this to change.
- **Never.** The capability is permanently single-language, and the entry says
  why. A permanent record is a stronger claim than a temporary one, so moving a
  capability out of `never` takes a constitutional amendment rather than an edit
  to the ledger.

On the page, a temporary gap is an amber notice naming a tracking issue and a
permanent one is a plain notice naming a reason. In the table at the top, the
same distinction reads as `absent (not yet)` against `absent (never)`.

## One entry per mechanism

Where the two libraries do something recognisably similar by fundamentally
different means, that is two capabilities and not one.

Simulation is the case that forces the rule. Python drives a locally installed
EnergyPlus through a subprocess; JavaScript runs a WebAssembly build in the
browser. Recorded as a single `simulation` entry, whichever language the entry
was written from would make the other read as deficient, and every page
describing it would print a gap notice for a capability that is not missing.
Visual output splits for the same reason: a static vector image drawn once is
not a real-time rendered scene.

So [`local-simulation`](#local-simulation) and
[`browser-simulation`](#browser-simulation) appear separately, as do
[`svg-visualisation`](#svg-visualisation) and
[`scene-rendering`](#scene-rendering). Neither pair is ever collapsed. When you
read one of them as Python-only or JavaScript-only, its partner entry is where
the other language's answer lives.

## The ids are load-bearing

Each capability's ledger id is a permanent public identifier, and it does three
jobs at once. It is the anchor on this page, so a link to `#local-simulation`
keeps resolving. It is the argument the `parity()` macro takes on every page
that describes the capability, which is how availability reaches the point of
use instead of living only here. And it is what the gates in both libraries
match their exported surface against.

Ids get added and deprecated. They do not get renamed.

<!-- BEGIN GENERATED FROM parity.toml. Edit the ledger, not this page. -->

Generated from
[`governance/parity.toml`](https://github.com/idfkit/idfkit-conformance/blob/governance-2026.7/governance/parity.toml)
at `governance-2026.7`, the governance tag this release pins. Correct the ledger and
regenerate; a correction made on this page would be overwritten, and it would never
reach either library's CI gate.

## Every capability at a glance { #at-a-glance }

30 capabilities, counted by availability and then listed in full. Follow a capability to
read what differs where the two libraries differ, and whether an absence is temporary or
permanent.

| Availability | Python | JavaScript |
| ------------ | ------ | ---------- |
| complete | 26 | 12 |
| partial | 2 | 2 |
| absent, not yet | 0 | 13 |
| absent, never | 2 | 3 |

| Capability | Tier | Python | JavaScript |
| ---------- | ---- | ------ | ---------- |
| [Reading IDF and epJSON](#parse) | 1 | complete | complete |
| [Writing IDF and epJSON](#write) | 1 | complete | complete |
| [Documents, collections, and objects](#document-model) | 1 | complete | complete |
| [Reference graph](#references) | 1 | complete | complete |
| [Schema access and the version registry](#schema-access) | 1 | complete | complete |
| [Model validation](#validation) | 1 | complete | complete |
| [Describing an object type from the schema](#introspection) | 1 | complete | partial |
| [Building EnergyPlus documentation URLs](#documentation-urls) | 1 | complete | complete |
| [Static types generated from the schema](#generated-object-types) | 1 | partial | complete |
| [Diagnostics from a parse](#parse-diagnostics) | 1 | partial | complete |
| [Weather station index and file retrieval](#weather-index) | 1 | complete | partial |
| [Geocoding a place name](#geocoding) | 1 | complete | complete |
| [Formatting-preserving round-trip](#lossless-round-trip) | 2 | complete | absent (not yet) |
| [Reading geometry from a model](#geometry-extraction) | 2 | complete | absent (not yet) |
| [Building and transforming geometry](#geometry-authoring) | 2 | complete | absent (not yet) |
| [Intersecting and matching surfaces](#surface-matching) | 2 | complete | absent (not yet) |
| [Generating zoned blocks from a footprint](#zoning) | 2 | complete | absent (not yet) |
| [Construction thermal properties](#thermal-properties) | 2 | complete | absent (not yet) |
| [Schedule evaluation](#schedules) | 2 | complete | absent (not yet) |
| [Reading the output variable dictionary and selecting variables](#output-variable-selection) | 2 | complete | absent (not yet) |
| [Design days and ASHRAE sizing conditions](#design-day-sizing) | 2 | complete | absent (not yet) |
| [Forward-migrating a model between EnergyPlus versions](#version-migration) | 3 | complete | absent (not yet) |
| [Command-line interface](#command-line) | 3 | complete | absent (not yet) |
| [Checking source against another EnergyPlus version's schema](#schema-compatibility-check) | 3 | complete | absent (not yet) |
| [Plotting simulation results](#result-plotting) | 3 | complete | absent (not yet) |
| [Running a locally installed EnergyPlus and reading its results](#local-simulation) | permanent | complete | absent (never) |
| [Running EnergyPlus in the browser](#browser-simulation) | permanent | absent (never) | complete |
| [Rendering a model to a vector image](#svg-visualisation) | permanent | complete | absent (never) |
| [Rendering a three-dimensional scene](#scene-rendering) | permanent | absent (never) | complete |
| [eppy compatibility surface](#eppy-compatibility) | permanent | complete | absent (never) |

## Tier 1: the shared core { #tier-1 }

Both libraries carry these, and both are expected to keep carrying them. A difference
you meet inside this tier is either stated below or a bug, and there is no third
possibility.

### Reading IDF and epJSON { #parse }

**Python** complete &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `parse`

??? note "Vocabulary this capability owns in the naming register"

    - parse IDF from a string
    - parse epJSON from a string
    - read IDF from disk
    - read epJSON from disk
    - the parse error type
    - detect a document version
    - an epJSON document value
    - read IDF from disk, keeping diagnostics
    - detect an epJSON document version

### Writing IDF and epJSON { #write }

**Python** complete &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `write`

??? note "Vocabulary this capability owns in the naming register"

    - serialize IDF to a string
    - serialize epJSON to a string
    - write IDF to disk
    - write epJSON to disk
    - serialize a document to an epJSON value
    - serialize one object

### Documents, collections, and objects { #document-model }

**Python** complete &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `document-model`

??? note "Vocabulary this capability owns in the naming register"

    - the document class
    - the collection class
    - the object class
    - an extensible group
    - create a new document
    - add an object
    - remove an object
    - rename an object
    - every object of a type
    - untyped collection access
    - one object, or nothing
    - one object, or an error
    - collection to a sequence
    - an object's type name
    - version

### Reference graph { #references }

**Python** complete &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `references`

??? note "Vocabulary this capability owns in the naming register"

    - the reference graph
    - objects referencing a name
    - a reference edge

### Schema access and the version registry { #schema-access }

**Python** complete &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `schema-access`

??? note "Vocabulary this capability owns in the naming register"

    - load a schema for a version
    - the supported version list
    - resolve a version string
    - one version's schema
    - the difference between two schema versions
    - resolve the schema for a detected version
    - the process-wide schema source

### Model validation { #validation }

**Python** complete &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `validation`

??? note "Vocabulary this capability owns in the naming register"

    - validate a document
    - validate an object
    - validation result
    - validation finding
    - validation severity

### Describing an object type from the schema { #introspection }

**Python** complete &middot; **JavaScript** partial &middot; Tier 1 &middot; ledger id `introspection`

!!! info "What differs, and why"

    TypeScript never populates `memo` or `note`. Both are members of the two types, so the field set
    matches, but they are always undefined. Python fills `memo` for 845 of 858 object types and `note`
    for 6,212 of 12,712 fields in 26.1.0, both from epJSON keys that `@idfkit/schemas` drops on purpose
    to keep the bundle off the parse critical path. The `@idfkit/schemas/docs` subpath its own header
    comment promises does not exist. Describing a type is what a REPL, a notebook, and an LSP hover are
    for, so the prose is most of the value; this is partial rather than complete.

    Two further differences, both small and both pinned by tests. `enumValues` omits the empty string
    that Python includes for 1,378 of its 2,293 enum-bearing fields, and omits the sentinel lists
    (`Autosize`, `Autocalculate`) Python recovers from an anyOf branch for 769 fields. Field ORDER
    differs for exactly two types in 26.1.0, `ZoneProperty:UserViewFactors:BySurfaceName` and
    `ZoneTerminalUnitList`, and for six more in 8.9.0 through 9.2.0, because the bundle sorts property
    keys for content-addressing and those types carry no positional field list to restore declaration
    order from.

??? note "Vocabulary this capability owns in the naming register"

    - describe an object type
    - object description
    - field description

### Building EnergyPlus documentation URLs { #documentation-urls }

**Python** complete &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `documentation-urls`

??? note "Vocabulary this capability owns in the naming register"

    - resolved documentation URL
    - documentation URL for an object type
    - I/O reference URL
    - engineering reference URL
    - documentation search URL

### Static types generated from the schema { #generated-object-types }

**Python** partial &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `generated-object-types`

!!! info "What differs, and why"

    Coverage differs, and the difference is visible to anyone not on the newest release. The Python
    stub set is generated for one EnergyPlus version at a time and is currently shipped for 26.1.0
    only, so a model loaded at 9.4 gets the 26.1 field names and choice lists from the editor. The
    TypeScript type maps are emitted per version and selected by the caller, who parameterises the
    document with the map for the version being read, so an older model is typed as that older model
    or is left untyped rather than mistyped.

    Application differs too. Python's stubs apply implicitly to every document. TypeScript's are opt-in
    by construction: an unparameterised document stays untyped, which is what version-generic code
    needs.

??? note "Vocabulary this capability owns in the naming register"

    - generated object types
    - a version type map

### Diagnostics from a parse { #parse-diagnostics }

**Python** partial &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `parse-diagnostics`

!!! info "What differs, and why"

    Both libraries produce diagnostics for a malformed input; only one hands them back. Python raises
    IDFParseError carrying the diagnostics that stopped the parse, and reports the recoverable ones
    (skipped malformed objects, discarded formatting trees, surplus fields on a non-extensible type)
    through the logging module, where a caller who wants them must install a handler. TypeScript
    returns them: parseIdf and loadIdfWithDiagnostics both yield a ParseResult whose `diagnostics`
    array holds the non-fatal findings alongside the document.

    This matters to the conformance corpus, whose `diagnostics` assertion compares what each side
    reports for a malformed case (contracts/conformance-corpus.md).

??? note "Vocabulary this capability owns in the naming register"

    - a parse diagnostic
    - diagnostics from a parse

### Weather station index and file retrieval { #weather-index }

**Python** complete &middot; **JavaScript** partial &middot; Tier 1 &middot; ledger id `weather-index`

!!! info "What differs, and why"

    Installation differs, and the difference is deliberate. `pip install idfkit` installs weather and
    its station index unconditionally, because Python extras gate dependencies rather than files, so a
    Python reader has weather whether or not they wanted it. `npm install idfkit` installs neither:
    weather is an opt-in peer there, added with `npm install @idfkit/weather`. Both libraries ship
    their own index once installed and neither retrieves one to get started (FR-043, FR-075,
    research R11). A JavaScript reader who follows a weather page without installing that package
    gets a resolution error, not a smaller feature, which is why the packaging is recorded here as a
    stated difference rather than left as an undescribed detail.

    Freshness handling differs. Python fires a throttled nudge from StationIndex.load(): at most once
    every 24 hours it probes the upstream KML files, warns when the bundled or cached index is behind,
    records the check under the cache directory, and can be turned off with
    IDFKIT_NO_WEATHER_UPDATE_CHECK. JavaScript has no such nudge and no timestamp to throttle against.
    It exposes checkForUpdates and refreshStationIndex for a caller who asks, and does nothing on its
    own, because the nudge is built on a writable cache directory and a browser-targeted package has
    none. The consequence for a reader is concrete: a stale index goes unmentioned in JavaScript until
    they check for themselves.

??? note "Vocabulary this capability owns in the naming register"

    - the station index
    - search stations
    - a weather station
    - download a weather file
    - refresh the station index
    - a text search result
    - a proximity search result
    - which field a text search matched
    - the station wire record
    - the upstream index base URL
    - fetch a prebuilt station index
    - parse a KML station index
    - read station metadata from a download URL
    - great-circle distance between two points
    - the retrieved weather files
    - read a ZIP archive
    - the injectable fetch
    - write weather files to disk
    - the written weather file paths
    - the weather options-object types
    - the station index wire form
    - build an index from index data
    - the upstream index file list
    - the bundled station index
    - check the station index for updates
    - download a station's archive
    - download a station's EPW file
    - download an EPW file by filename

### Geocoding a place name { #geocoding }

**Python** complete &middot; **JavaScript** complete &middot; Tier 1 &middot; ledger id `geocoding`

??? note "Vocabulary this capability owns in the naming register"

    - geocode a place name
    - detect the current location
    - the geocoding rate limiter
    - a geocoding failure

## Tier 2: portable, not ported yet { #tier-2 }

Capabilities the second language could have and does not have today. Every entry carries
a tracking issue, because recording any of them as permanent would claim more than the
code supports.

### Formatting-preserving round-trip { #lossless-round-trip }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `lossless-round-trip`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#12](https://github.com/idfkit/idfkit-js/issues/12).

??? note "Vocabulary this capability owns in the naming register"

    - preserve formatting on a round-trip

### Reading geometry from a model { #geometry-extraction }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `geometry-extraction`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#13](https://github.com/idfkit/idfkit-js/issues/13).

??? note "Vocabulary this capability owns in the naming register"

    - three-dimensional vector
    - three-dimensional polygon
    - read a surface's coordinates
    - a zone's origin
    - a zone's rotation
    - transform relative coordinates to world coordinates
    - a surface's area
    - a surface's tilt
    - a surface's azimuth
    - a zone's floor area
    - a zone's volume

### Building and transforming geometry { #geometry-authoring }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `geometry-authoring`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#14](https://github.com/idfkit/idfkit-js/issues/14).

??? note "Vocabulary this capability owns in the naming register"

    - set the window to wall ratio
    - rotate a building
    - translate a building
    - scale a building
    - add a shading block
    - set default constructions

### Intersecting and matching surfaces { #surface-matching }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `surface-matching`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#15](https://github.com/idfkit/idfkit-js/issues/15).

??? note "Vocabulary this capability owns in the naming register"

    - intersect and match surfaces
    - a surface match report

### Generating zoned blocks from a footprint { #zoning }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `zoning`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#16](https://github.com/idfkit/idfkit-js/issues/16).

??? note "Vocabulary this capability owns in the naming register"

    - create a zoned block
    - a zone footprint
    - a zoning scheme
    - link blocks

### Construction thermal properties { #thermal-properties }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `thermal-properties`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#17](https://github.com/idfkit/idfkit-js/issues/17).

??? note "Vocabulary this capability owns in the naming register"

    - construction thermal properties
    - a construction's U-value
    - a construction's R-value
    - a construction's solar heat gain coefficient
    - a construction's layers

### Schedule evaluation { #schedules }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `schedules`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#18](https://github.com/idfkit/idfkit-js/issues/18).

??? note "Vocabulary this capability owns in the naming register"

    - evaluate a schedule
    - a schedule's values for a year
    - a schedule as a series
    - create a constant schedule
    - create a compact schedule
    - extract special days
    - the holidays in a model

### Reading the output variable dictionary and selecting variables { #output-variable-selection }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `output-variable-selection`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#19](https://github.com/idfkit/idfkit-js/issues/19).

??? note "Vocabulary this capability owns in the naming register"

    - read the output variable dictionary
    - an output variable
    - an output meter
    - select output variables for a run

### Design days and ASHRAE sizing conditions { #design-day-sizing }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 2 &middot; ledger id `design-day-sizing`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#20](https://github.com/idfkit/idfkit-js/issues/20).

??? note "Vocabulary this capability owns in the naming register"

    - apply ASHRAE sizing conditions
    - the design day manager

## Tier 3: tooling and Node-bound capabilities { #tier-3 }

Absent from JavaScript today and not permanently so. Each one is reachable in Node,
which is why none of them is recorded as permanent.

### Forward-migrating a model between EnergyPlus versions { #version-migration }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 3 &middot; ledger id `version-migration`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#21](https://github.com/idfkit/idfkit-js/issues/21).

??? note "Vocabulary this capability owns in the naming register"

    - migrate a model to a newer version
    - a migration report
    - a migration step

### Command-line interface { #command-line }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 3 &middot; ledger id `command-line`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#22](https://github.com/idfkit/idfkit-js/issues/22).

??? note "Vocabulary this capability owns in the naming register"

    - the command line entry point

### Checking source against another EnergyPlus version's schema { #schema-compatibility-check }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 3 &middot; ledger id `schema-compatibility-check`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#23](https://github.com/idfkit/idfkit-js/issues/23).

??? note "Vocabulary this capability owns in the naming register"

    - check source compatibility with a version
    - diff two schemas
    - a compatibility diagnostic

### Plotting simulation results { #result-plotting }

**Python** complete &middot; **JavaScript** absent (not yet) &middot; Tier 3 &middot; ledger id `result-plotting`

!!! warning "Not in JavaScript yet"

    A temporary gap, not a boundary. The port is tracked in
    [idfkit-js#24](https://github.com/idfkit/idfkit-js/issues/24).

??? note "Vocabulary this capability owns in the naming register"

    - plot an energy balance
    - plot a temperature profile
    - plot comfort hours
    - a plotting backend

## Permanently single-language { #permanently-single-language }

Pairs of capabilities that were never one capability. Neither library is missing
anything here, which is why these entries sit apart from the gaps above: each pair is
two different mechanisms serving two different runtimes.

### Running a locally installed EnergyPlus and reading its results { #local-simulation }

**Python** complete &middot; **JavaScript** absent (never) &middot; Permanently single-language &middot; ledger id `local-simulation`

!!! abstract "Python only, permanently"

    Requires an EnergyPlus installation on the machine and a subprocess to drive it, then reads the
    eplusout files that run leaves on disk. Neither the installation nor the subprocess is available in
    a browser, which is the runtime the JavaScript library targets. JavaScript reaches EnergyPlus by
    the other mechanism instead: see [`browser-simulation`](#browser-simulation), which is not a workaround for this entry but
    a different capability.

??? note "Vocabulary this capability owns in the naming register"

    - the local simulation surface

### Running EnergyPlus in the browser { #browser-simulation }

**Python** absent (never) &middot; **JavaScript** complete &middot; Permanently single-language &middot; ledger id `browser-simulation`

!!! abstract "JavaScript only, permanently"

    Delivered by @idfkit/engine, installed separately and deliberately not part of the shared install
    name: not a subpath, not a dependency, not an optional peer (research R19). The WebAssembly build
    exists to reach a runtime Python does not target, so Python has no counterpart and is not getting
    one. @idfkit/engine-assets is roughly 51 MB and versions on the EnergyPlus release it carries,
    while the loader versions on its own API, which is a second reason the facade does not carry it.

    This is not a gap in Python. Python runs EnergyPlus by the other mechanism: see
    [`local-simulation`](#local-simulation).

### Rendering a model to a vector image { #svg-visualisation }

**Python** complete &middot; **JavaScript** absent (never) &middot; Permanently single-language &middot; ledger id `svg-visualisation`

!!! abstract "Python only, permanently"

    A Python-side capability with no JavaScript counterpart and no plan for one. The output is a static
    vector image produced for a notebook, a report, or a file on disk, which is a Python workflow. A
    JavaScript caller wanting to look at a model is already in a runtime that draws, and is served by
    the other mechanism: see [`scene-rendering`](#scene-rendering). Recording the two as one `visualization` entry would
    make each language read as missing something the other has, which is exactly the failure FR-078
    and FR-068 forbid.

??? note "Vocabulary this capability owns in the naming register"

    - the vector image surface

### Rendering a three-dimensional scene { #scene-rendering }

**Python** absent (never) &middot; **JavaScript** complete &middot; Permanently single-language &middot; ledger id `scene-rendering`

!!! abstract "JavaScript only, permanently"

    Delivered by @idfkit/viewer, installed by its own name like the simulation engine, and NOT reachable
    through the shared install name: no subpath, no dependency, no export-map entry, and no reserved
    name in the naming register. A reader reaches it by installing it explicitly, and the documentation
    says so rather than implying the facade carries it.

    Python has no counterpart and is not getting one. A real-time interactive scene needs a rendering
    context that a Python process does not have, and Python's static vector output is a different
    mechanism serving a different workflow: see [`svg-visualisation`](#svg-visualisation). Neither is a gap in the other.

### eppy compatibility surface { #eppy-compatibility }

**Python** complete &middot; **JavaScript** absent (never) &middot; Permanently single-language &middot; ledger id `eppy-compatibility`

!!! abstract "Python only, permanently"

    A Python ecosystem concern with no JavaScript counterpart. These methods exist solely so that code
    written against eppy keeps working after a move to idfkit; every one of them names an idfkit
    alternative in its own docstring. There is no eppy in JavaScript, so there is nothing to be
    compatible with. Listed explicitly so it is never ported by mistake.

??? note "Vocabulary this capability owns in the naming register"

    - eppy compatibility surface

<!-- END GENERATED FROM parity.toml. -->
