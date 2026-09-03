# Supported EnergyPlus versions

Both libraries bundle schemas for the same 17 EnergyPlus releases, 8.9.0
through 26.1.0. 8.9.0 is the first release to publish an epJSON schema. Every
release ships inside the package: there is no per-version install and no build
step to select one.

| EnergyPlus | Schema key | EnergyPlus | Schema key |
| ---------- | ---------- | ---------- | ---------- |
| 8.9        | `8.9.0`    | 23.1       | `23.1.0`   |
| 9.0        | `9.0.1`    | 23.2       | `23.2.0`   |
| 9.1        | `9.1.0`    | 24.1       | `24.1.0`   |
| 9.2        | `9.2.0`    | 24.2       | `24.2.0`   |
| 9.3        | `9.3.0`    | 25.1       | `25.1.0`   |
| 9.4        | `9.4.0`    | 25.2       | `25.2.0`   |
| 9.5        | `9.5.0`    | 26.1       | `26.1.0`   |
| 9.6        | `9.6.0`    |            |            |
| 22.1       | `22.1.0`   |            |            |
| 22.2       | `22.2.0`   |            |            |

The schema key carries the patch component that the release name usually drops:
9.0 is keyed `9.0.1`.

## Reading the list at runtime

Both libraries expose the list, oldest first, and the newest entry on its own.

=== "Python"

    ```python
    from idfkit import ENERGYPLUS_VERSIONS, LATEST_VERSION, version_string

    len(ENERGYPLUS_VERSIONS)        # 17
    version_string(LATEST_VERSION)  # '26.1.0'
    ```

    Versions are `(major, minor, patch)` tuples. The rest of the module is at
    [Versions](../api/versions.md).

=== "TypeScript"

    ```ts
    import { schemas } from '@idfkit/core/node';

    const bundle = schemas();
    (await bundle.versions()).length; // 17
    await bundle.latest(); // '26.1.0'
    ```

    Versions are strings. Both accessors are async because the bundle index is
    read on first use.

## Matching a file's version to a schema

An IDF file writes two components:

```idf
Version, 9.0;
```

Schemas are keyed on three, so the version read from a file is often not a key
in the list. Each library closes that gap on load, and they close it
differently.

=== "Python"

    `find_closest_version` returns the newest supported release that is less
    than or equal to the version read. `9.0` parses as `9.0.0`, and the closest
    supported release at or below it is 8.9.0, so that is the schema loaded.
    When nothing qualifies, `get_schema` raises `SchemaNotFoundError`.

    ```python
    from idfkit import load_idf

    doc = load_idf("fragment.idf", version=(26, 1, 0))
    ```

=== "TypeScript"

    `resolveVersion` takes every candidate sharing the major and minor
    components and returns the newest by patch, so `9.0` resolves to `9.0.1`.
    With no candidate sharing major and minor it returns `undefined`, and
    `loadIdf` turns that into an error naming the versions that were available.

    ```ts
    const doc = await loadIdf('fragment.idf', { version: '26.1.0' });
    ```

!!! note "The two libraries resolve `9.0` differently"
    For a file declaring `Version, 9.0;`, Python loads the 8.9.0 schema and
    TypeScript loads the 9.0.1 schema.

Loading the wrong schema does not raise. IDF is positional, so a field-order
difference between two releases mis-maps values into neighbouring slots and the
parse succeeds against a corrupted model. Pass `version` explicitly to remove
the guess.

A file with no `Version` object is a different case: Python raises
`VersionNotFoundError` and TypeScript throws an error naming the missing
object. Both accept the same explicit `version` argument shown above.

## Comparing versions

Sort on the numeric components, never on the version string. String order puts
`8.9.0` after `22.1.0`.

=== "Python"

    ```python
    sorted([(22, 1, 0), (8, 9, 0), (9, 6, 0)])
    # [(8, 9, 0), (9, 6, 0), (22, 1, 0)]
    ```

=== "TypeScript"

    ```ts
    import { compareVersions } from '@idfkit/core';

    ['22.1.0', '8.9.0', '9.6.0'].sort(compareVersions);
    // ['8.9.0', '9.6.0', '22.1.0']
    ```

    `versionKey` gives the same ordering as a single number, for when a sort
    key is more convenient than a comparator.

## Static types cover fewer releases than schemas

Schemas ship for all 17 releases. Generated static types do not, and what they
cover differs by language.

| Language   | Releases with generated types | Delivery                                               |
| ---------- | ----------------------------- | ------------------------------------------------------ |
| Python     | 26.1.0                        | stubs bundled in `idfkit`, no install step             |
| TypeScript | 26.1.0 and 9.4.0              | `@idfkit/types-v26-1` and `@idfkit/types-v9-4`, opt-in |

```bash
npm install --save-dev @idfkit/types-v26-1
```

Each TypeScript type package is a single declaration file, 2.7 MB for 26.1.0
and 2.5 MB for 9.4.0, which is why neither is a dependency of `@idfkit/core`.
Installing neither leaves the library complete: a document with no type map
behaves identically at runtime.

Any release can have a TypeScript package generated for it. The generator reads
the raw epJSON schemas from the Python repository, so its output is committed
rather than produced at install time:

```bash
npm run codegen -- 25.2.0
```

See [Static types generated from the schema](../explanation/generated-types.md)
and [Type-safe development](../concepts/type-safety.md).
