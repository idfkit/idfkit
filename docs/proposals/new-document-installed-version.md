# Proposal: create a model at the installed EnergyPlus release

Status: exploration, with a prototype on this branch (`docs/new-document-installed-version`).
Scope: `new_document()`, its typing, and how it meets `simulate()`.

## Problem

`new_document()` defaults to `LATEST_VERSION` (26.2). A user whose installed EnergyPlus is 25.1 gets a
26.2 model, and `simulate()` refuses it with `VersionMismatchError`, because backward migration is never
attempted. Today's workaround is `new_document(version=find_energyplus().version)`, which is in the
`new_document` docstring, the `VersionMismatchError` message and the bundled agent reference
(`simulation-execution.md`). It has two flaws:

1. **It is typed as the wrong release.** The tuple overloads return `IDFDocument`, the latest release's
   type, whatever the tuple says (verified with pyright, below). The documented fix for the version
   mismatch is therefore type-checked against 26.2's object types, fields and choices.
2. **It does not resolve the release line.** `find_energyplus().version` is the install's own version.
   `new_document((9, 0, 0))` raises `UnsupportedVersionError` because the registry entry is 9.0.1, while
   `simulate()` matches release lines (`find_release`). The two disagree on what "the same version" means.

## Findings

### Q3: the tuple overload types every tuple as the latest release (confirmed)

```python
d = new_document((9, 4, 0))
reveal_type(d)             # IDFDocument[Literal[True]]   <- 26.2's type
reveal_type(d["Space"])    # IDFCollection[Space]  (no error; Space was added in 9.6)
x: IDFDocumentV9_4 = d     # error: IDFDocument is not assignable to IDFDocumentV9_4
```

At run time `d["Space"]` / `d.add("Space", ...)` raises `UnknownObjectTypeError`, so pyright accepts code
that fails. This is a known, documented caveat (the `new_document` docstring says "Given a tuple, it is
typed for the latest release whatever the version, since a type checker does not read the tuple";
`document-and-objects.md` says a fixture built that way "is checked against the wrong release"). It is
also inconsistent with `migrate()`, whose tuple form already returns `AnyIDFDocument[bool]`
(`migrate(old, (24, 1, 0))` in `tests/type_checks/versioned_fixture.py`).

The premise "a type checker does not read the tuple" is not true for pyright: an overload on
`tuple[Literal[26], Literal[2], Literal[0]]` is matched by the literal `(26, 2, 0)`, by a `Final` bound
to one, and by a tuple variable whose declared type pyright has narrowed to the literal. A variable typed
`tuple[int, int, int]` falls through to the next overload. (mypy was not checked.)

### Q1: discovery and import cost

* `find_energyplus()` (`simulation/config.py`) tries an explicit `path`, then `ENERGYPLUS_DIR`, then
  `energyplus` on `PATH`, then `/opt/eplus`, then the platform directories newest first, and raises
  `EnergyPlusNotFoundError` listing what it found. `simulate(energyplus=None)` uses the same discovery,
  so the install `find_energyplus()` returns is the one `simulate()` would run on.
* **`import idfkit` already imports `idfkit.simulation`.** `idfkit.migration.subprocess_backend` imports
  `idfkit.simulation._cancel`, which runs `idfkit/simulation/__init__.py` (results, parsers, `sqlite3`,
  `html.parser`, plotting registry). Measured with `python -X importtime`: `import idfkit` is about
  160–190 ms, of which `idfkit.simulation` is about 36 ms cumulative. So a `new_document` that reads an
  `EnergyPlusConfig` costs nothing extra at import time today. The prototype still imports it inside the
  function so it does not add a dependency; making `idfkit.migration` stop loading the simulation package
  eagerly is a separate, independent improvement.
* The core package stays stdlib-only: nothing here needs a third-party package.

### Q4: what `simulate()` does with a version mismatch today

`resolve_version_mismatch` (`simulation/_common.py`) matches both versions to their release line with
`find_release`, then:

| Model vs installed | `auto_migrate=False` (default) | `auto_migrate=True` |
|---|---|---|
| same release line | runs | runs |
| model older | `VersionMismatchError`, naming the migration chain | forward-migrates, `result.migration_report` set |
| model newer | `VersionMismatchError` (backward migration is never attempted) | same |
| installed release unknown to idfkit | `UnsupportedVersionError` from the chain planner | same |

A default `new_document()` on a 25.1 install hits row 3. Nothing about this needs to change: refusing a
backward migration is right, and the fix is to create the model at the right release. Only the error
message should change (below).

## Options for the API (Q1)

| Option | Verdict |
|---|---|
| `new_document("installed")` | **No.** `version` refuses strings on purpose (`new_document("26.1")` raises `TypeError` pointing at the tuple). A magic string re-opens that and hides file-system and environment lookups inside a constructor that is otherwise pure (and run in doctests). |
| `new_document(installed=True)` | **No.** A flag that conflicts with `version`, needs its own overload pair per `strict`, and still hides discovery. There is no place to say *which* install (`path=`, `version=` filter). |
| `new_document_for_installed(...)` | Workable, but a second constructor duplicating `strict`/`normalize_choices`, and it still has to choose between discovering and taking a config. |
| **`new_document(find_energyplus())`**, i.e. `version` accepts an `EnergyPlusConfig` | **Recommended.** |

Why the `EnergyPlusConfig` form:

* **Discovery stays explicit and composable.** Every rule about *which* install (env var, `PATH`,
  newest-first, `find_energyplus(version="25.1")`, `find_energyplus(path=...)`) is `find_energyplus`'s,
  unchanged. The same object goes to `simulate(..., energyplus=config)`, so the model and the run cannot
  disagree:

  ```python
  ep = find_energyplus()
  model = new_document(ep)
  ...
  simulate(model, weather, energyplus=ep)
  ```

* **No EnergyPlus found** raises `EnergyPlusNotFoundError` from `find_energyplus()`, with the searched
  paths. No silent fallback to the latest release: that is exactly the bug being fixed, moved to
  `simulate()`. A caller who wants a fallback writes it, and it is visible:

  ```python
  try:
      model = new_document(find_energyplus())
  except EnergyPlusNotFoundError:
      model = new_document()
  ```

* **Multiple installs:** whichever `find_energyplus()` returns, which is the one `simulate()` would use.
  `ENERGYPLUS_DIR` first, newest platform install last. No new precedence rules.
* **Patch versions:** the install's version is matched to its release line with `find_release`, the same
  function `simulate()` uses, so 9.0.0 and 9.0.1 both give a 9.0.1 model, and a model created this way
  never trips `simulate()`'s version check (tested in the prototype for 9.0.0, 9.0.1, 25.1 and 26.2).
* **An installed release idfkit has no schema for** (newer than 26.2, or older than 8.9) raises
  `UnsupportedVersionError`. Not "closest older": a 26.2 model on a 27.1 install cannot be migrated
  (`plan_migration_chain((26, 2, 0), (27, 1, 0))` raises `UnsupportedVersionError`), so the fallback only
  defers the failure to `simulate()`. Note that this deliberately differs from `find_closest_version`,
  which snaps a newer-than-latest *file* to the latest schema for reading.

## Typing (Q2, Q3)

### `new_document(config)` returns `AnyIDFDocument` (Q2: yes)

The release is only known at run time, exactly like `load_idf()`. `AnyIDFDocument` lets only what every
supported release has type-check, so nothing release-specific slips through. Offer `as_type=`, as
`load_idf` does, so the run-time check and the static type agree in one call:

```python
model = new_document(find_energyplus(), as_type=IDFDocumentV25_1)   # IDFDocumentV25_1
# TypeError at run time if the install is another release
```

`since=` / `before=` should follow, for parity with `load_idf` and `as_version`. They need one overload per
range of releases, so they belong in the generator (as `_loaders.pyi` does), not in hand-written
overloads; the prototype leaves them out. Until then `as_version(new_document(ep), since="25.1")` works.

### Fix the tuple overload (Q3)

Two variants were measured on this branch (by editing the overloads, running pyright over `src/`,
`agent_references/snippets` and `tests/`, and reverting):

| Variant | `new_document()` / `(26, 2, 0)` | `(9, 4, 0)` | tuple variable | New pyright errors | Cold pyright on a 5-line caller |
|---|---|---|---|---|---|
| today | `IDFDocument` | `IDFDocument` (wrong) | `IDFDocument` (wrong) | — | ~1.7 s |
| **A: latest literal → `IDFDocument`, other tuples → `AnyIDFDocument`** | `IDFDocument` | `AnyIDFDocument` | `AnyIDFDocument` | 90, all in `tests/` | ~1.7 s |
| B: one literal overload per release | `IDFDocument` | `IDFDocumentV9_4` | `AnyIDFDocument` | 81, all in `tests/` | **~3.3 s** |

Neither variant adds an error in `src/` or the snippets. B is the more precise, but it makes every module
that calls `new_document` load the 24k-line `versioned.pyi`, doubling cold pyright time for any caller
(the reason the existing `type[_D]` overload is bound to a plain base). A gives the right answer at no
cost, and the precise type is already one call away: `new_document(IDFDocumentV9_4)`.

**Recommendation: A.** Details:

* The latest-release overload names `tuple[Literal[26], Literal[2], Literal[0]]`. It must move with each
  release adoption: either generate `new_document`'s overloads with the other stubs, or add a test that
  the literal equals `LATEST_VERSION` (cheap; the prototype does not include it).
* Declare `LATEST_VERSION` with a literal type (`Final = (26, 2, 0)`, asserted equal to
  `ENERGYPLUS_VERSIONS[-1]`), so `new_document(LATEST_VERSION)` keeps `IDFDocument`. It is in the agent
  reference's table as `new_document(version=LATEST_VERSION)`.

**How breaking:** run time is unchanged. Statically, code that wrote `new_document((24, 1, 0))` and used it
as an `IDFDocument` (annotated it, passed it to a function taking `IDFDocument`, or used a type only newer
releases have) gets errors; each such error is either a real bug or should state the release with
`new_document(IDFDocumentV24_1)`. In this repository the 90 errors fall in 22 test modules, mostly helpers
annotated `IDFDocument` (e.g. `tests/conftest.py::add_design_day`), plus five deliberate assertions in
`tests/type_checks/versioned_fixture.py`. Ship it as a `**Breaking:**` changelog entry, typing only.

### A side effect already in the prototype

Once `version` accepts an `EnergyPlusConfig`, an argument typed `Any` matches those overloads too, and
pyright resolves the call to the wider return, `AnyIDFDocument`, whatever the overload order
(`new_document(any_version)` was `IDFDocument`). That is correct, since an `Any` may be a config, and it
is the same answer variant A gives an untyped tuple. The prototype updates the fixture's two assertions.

## Message, `idfkit check`, stubs and agent references (Q5)

* **`VersionMismatchError`** (`exceptions.py`, around line 904) suggests
  `new_document(version=(25, 1, 0))` and `version=idfkit.simulation.find_energyplus().version`. Change it
  to `new_document(IDFDocumentV25_1)` (typed) and `new_document(find_energyplus())`.
* **`idfkit check` (C001–C006):** no rule change. `compat/_extract.py` already treats any `new_document(...)`
  call as a document receiver, so `new_document(find_energyplus())["Space"]` is still read. Rules check
  against the configured target releases, not the call's argument. A follow-up idea, not needed here:
  infer a narrower target set from `as_type=` / a release type in the call.
* **Generated stubs:** `new_document`'s overloads are hand-written in `src/idfkit/__init__.py`, so neither
  change touches the generator, unless the latest-literal overload is generated (above). `verify_stubs`
  is unaffected; `make check` passes on the prototype.
* **Agent references** (template + snippet, then `python -m idfkit.codegen.bake_references`):
  * `templates/simulation-execution.md` line 65: replace the `find_energyplus().version` workaround and its
    "typed as the latest release" caveat with `new_document(find_energyplus())` and `as_type=`; add a
    snippet section in `snippets/simulation-execution.py` (pyright-checked).
  * `templates/document-and-objects.md` line 148: drop "Given a version tuple instead, `new_document` is
    typed for the latest release whatever the version"; say a non-latest tuple gives `AnyIDFDocument`.
    Line 99/101 tables: add the `EnergyPlusConfig` form.
* **Docs site** (idfkit-developers): the `new_document` and simulation how-to pages, same edits. No new
  environment variables are read, so `environment-variables.md` is unchanged.

## Changelog impact

Under `[Unreleased]`:

```markdown
### Added
- `new_document(find_energyplus())` created a model at the installed EnergyPlus's release, typed
  `AnyIDFDocument`, or as the release named with `as_type=` ([#NNN](...)).

### Changed
- **Breaking:** `new_document()` given a tuple other than the latest release was typed `AnyIDFDocument`
  instead of the latest release's `IDFDocument`; pass the release's type, `new_document(IDFDocumentV9_4)`,
  to keep it typed ([#NNN](...)).
```

## Prototype on this branch

* `src/idfkit/__init__.py`: `new_document` accepts an `EnergyPlusConfig` as `version`; three overloads
  (strict, non-strict, `as_type=`); `_release_of_installation()` resolves the release line and refuses an
  unsupported one; `as_type=` without a config raises `TypeError`. Variant A of the tuple fix is **not**
  applied, since it is the breaking half and wants its own decision.
* `tests/test_new_document_installed.py`: release resolution, patch lines, unsupported releases,
  `strict`/`normalize_choices`, `as_type=` (match, mismatch, strictness), and that `simulate()`'s version
  check accepts the model unchanged.
* `tests/type_checks/versioned_fixture.py`: static types of the new forms, and the `Any` change above.
* Not done: `since=`/`before=`, the error message, agent references, changelog.

## Test plan for the real change

1. Run time (`tests/test_new_document_installed.py`, extended): every supported release; patch variants
   (9.0.0/9.0.1); newer-than-latest and older-than-minimum raise `UnsupportedVersionError`;
   `as_type=` single type, tuple of types, strictness conflict (`TypeError` before any document is built);
   `since=`/`before=` in and out of range; `as_type=` with a tuple version refused.
2. Agreement with `simulate()`: for each release, `resolve_version_mismatch(model=new_document(c), config=c,
   auto_migrate=False)` returns the model unchanged; one integration test (`-m integration`) creates and
   runs a design-day model on the real install.
3. Static (`tests/type_checks/versioned_fixture.py`): `new_document(config)` is `AnyIDFDocument[...]`,
   `as_type=` narrows, `new_document(config)["Space"]` is an error; after variant A, `new_document()`,
   `new_document((26, 2, 0))` and `new_document(LATEST_VERSION)` are `IDFDocument`, `new_document((9, 4, 0))`
   is `AnyIDFDocument`, `map(new_document, versions)` is `list[AnyIDFDocument]`.
4. A test that the latest-literal overload equals `LATEST_VERSION`, so adopting 26.3 cannot leave it stale.
5. Import: a test that `import idfkit` does not import more than today (or, after the separate lazy-import
   change, that it no longer imports `idfkit.simulation`).
6. `make check && make test`, re-bake the agent references, `check-baker` clean.
