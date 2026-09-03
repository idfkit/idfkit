# How to compare two EnergyPlus versions

Both libraries carry every schema from 8.9.0 to 26.1.0, so "what changed
between 9.4 and 26.1" is a question you can answer locally, without downloading
anything and without opening two 10 MB schema documents side by side.

This guide diffs two releases, reads the detail on a type that moved, and
checks whether a specific model still holds up under the other version. It does
not migrate anything; that is a separate job, and the last section says where
it lives.

## Diff the two schemas

=== "Python"

    ```python
    from idfkit import get_schema
    from idfkit.compat import build_schema_index, diff_schemas

    older = get_schema((9, 4, 0))
    newer = get_schema((26, 1, 0))

    delta = diff_schemas(build_schema_index(older), build_schema_index(newer))

    delta.added_types       # type names introduced since 9.4
    delta.removed_types     # type names that no longer exist
    delta.added_choices     # {(obj_type, field): new choice values}
    delta.removed_choices   # {(obj_type, field): choice values withdrawn}
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/how-to/compare-versions/diff_the_two_schemas.ts:example"
    ```

Read the direction off the call. Python's `diff_schemas(from_index, to_index)`
takes the older index first and reports the move forward. TypeScript's
`changedFrom` reads as "what this version changed, relative to that one", so
call it on the newer schema.

The two diffs are not the same shape, and the difference decides what you do
next. TypeScript hands back a third list, `changed`, naming every type whose
definition differs without saying how; Python has no such list but reports the
enumerated choice values that were added or withdrawn, keyed by object type and
field. So a TypeScript caller narrows to a candidate list and then compares the
two definitions, while a Python caller already has the choice-list answer and
compares definitions only for the field order.

In a browser, swap `localBundle()` for
`new SchemaBundle(httpSource('/schemas/'))`. Nothing else in the TypeScript
snippet changes.

## Compare one type's field order

Field order is the change that matters most for reading old files, because IDF
is positional: a field inserted in the middle of a type shifts everything after
it. Both schemas expose the positional order directly, so comparing two
releases is a list comparison.

=== "Python"

    ```python
    type_name = "Coil:Cooling:DX:SingleSpeed"

    before = older.get_field_names(type_name)
    after = newer.get_field_names(type_name)

    gained = [f for f in after if f not in before]
    lost = [f for f in before if f not in after]
    # gained: ['2017_rated_evaporator_fan_power_per_volume_flow_rate', ...]
    # lost:   ['rated_evaporator_fan_power_per_volume_flow_rate']
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/how-to/compare-versions/compare_one_type_s_field_order.ts:example"
    ```

A type can differ between two releases without gaining or losing a field. A
default, a range, or a choice list may have moved instead, and none of those
show up in a field-order comparison.

## Check whether a model holds up under another version

Validation takes the schema to validate against, which turns "is this model
valid?" into "would this model be valid under 26.1?" for the price of one
argument. A type the target release removed comes back as a `W002` warning
naming the object; the codes are the same in both languages.

=== "Python"

    ```python
    from idfkit import get_schema, validate_document

    target = get_schema((26, 1, 0))
    result = validate_document(model, schema=target)

    for finding in result.warnings:
        if finding.code == "W002":
            print(f"{finding.obj_type} '{finding.obj_name}' does not exist in 26.1")
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/how-to/compare-versions/check_whether_a_model_holds_up_under_another_version.ts:example"
    ```

This catches types the target release removed, and it catches fields whose
type, range, or required status the target release tightened. It does not
catch a field that changed meaning while keeping its name and its type, and it
is not a migration.

## Migrating is a different job

Answering "what changed" is not the same as moving a model across the gap.
Migration is done by the `IDFVersionUpdater` transition binaries that ship with
EnergyPlus itself, so it needs an EnergyPlus installation rather than a schema.

Python wraps them:

```python
from idfkit import migrate

report = migrate(model, "26.1.0")
migrated = report.migrated_model
```

There is no TypeScript equivalent yet. The name is reserved in the naming
register so that a port cannot land under a different one, and the absence is
recorded on the [parity ledger](../explanation/parity.md).

## Why this is cheap

Neither diff walks two schema documents. Python compares two pre-built indexes
of type names and choice sets, and pays for building each index once per
version. TypeScript compares
[content-address hashes](../explanation/content-addressed-schemas.md) straight
out of the two manifests, which is why loading the second version only costs
the definitions the two releases do not already share. Either way, "what
changed between two releases" is a question you can afford to ask in a loop.

## See also

- [How to check version compatibility](../concepts/version-compatibility.md)
  for linting your own Python source against a version bump, which is the same
  diff pointed at your code rather than at a model
- [How to migrate models between EnergyPlus versions](../simulation/migrating-versions.md)
  for the full migration workflow, including the CLI
- [Supported versions](../reference/versions.md) for the list both libraries
  carry
