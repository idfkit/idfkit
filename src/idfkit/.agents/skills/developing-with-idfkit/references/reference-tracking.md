# Reference tracking

EnergyPlus models are graphs of cross-references: a `BuildingSurface:Detailed.zone_name` points at a `Zone.name`, a `People.zone_or_zonelist_or_space_or_spacelist_name` points at a `Zone` or `ZoneList`, a `Branch` component name points at a coil. idfkit keeps a live `ReferenceGraph` of every reference and uses it for two superpowers — fast "what points at this?" queries, and automatic cascading renames.

## When to use

- You want to find every object that references a given name.
- You want to rename an object without leaving stale references behind.
- You're authoring HVAC loops, schedules, or zone lists where many objects share names.
- You're auditing a model and want to find dangling (unresolved) references.

## Quick start

```python
# Who points at this zone?
for obj in doc.get_referencing("Office"):
    print(obj.obj_type, obj.name)

# What does this People object reference?
people = doc["People"]["Office People"]
for target_name in doc.get_references(people):
    print(target_name)

# Rename — every reference updates automatically
doc["Zone"]["Office"].name = "Open_Office"
# or
doc.rename("Zone", "Office", "Open_Office")
```

## Core API

| Symbol | Purpose |
|---|---|
| `doc.get_referencing(name)` | All `IDFObject`s whose fields point at `name`. |
| `doc.get_references(obj)` | All names referenced by `obj`'s fields. |
| `doc.rename(obj_type, old, new)` | Rename an object and cascade through every reference. |
| `obj.name = "new"` | Equivalent to `doc.rename(obj.obj_type, obj.name, "new")`. |
| `doc.references` | The underlying `ReferenceGraph` — use for advanced queries below. |
| `ReferenceGraph.get_referencing_with_fields(name)` | `set[(IDFObject, field_name)]` — same as above, with the originating field. |
| `ReferenceGraph.get_references_with_fields(obj)` | `set[(field_name, referenced_name)]` — what this object references and from which field. |
| `ReferenceGraph.is_referenced(name)` | Is anything pointing at this name? |
| `ReferenceGraph.get_dangling_references(valid_names)` | Iterator of `(obj, field, name)` for references to names not in the valid set. |
| `ReferenceGraph.stats()` | `{registered_objects, distinct_targets, total_edges}` — sanity-check the graph. |

## How the graph stays in sync

idfkit registers references at three points:

1. **At parse time** — `parse_idf` / `parse_epjson` walks every reference field as it builds objects.
2. **On `add` / `addidfobject`** — `doc.add("People", ..., zone_or_zonelist_or_space_or_spacelist_name="Office")` registers the edge.
3. **On field mutation** — setting `obj.zone_or_zonelist_or_space_or_spacelist_name = "Office"` swaps the edge atomically.

`doc.removeidfobject(obj)` unregisters every edge originating from `obj`. `obj.name = "new"` triggers `notify_name_change`, which rewrites every edge that pointed at `obj` to point at the new name and rewrites every field carrying the old name.

The graph is keyed off **reference lists** declared in the EpJSON schema (e.g. `ZoneNames`, `ScheduleNames`, `BranchNames`). idfkit consults the schema to know which fields participate, so you never need to register edges manually.

## Finding what points at a name

```python
# Who points at "Office"?
referencing = doc.get_referencing("Office")
print(len(referencing))  # e.g. 8 (surfaces, people, lights, HVAC objects)

# With the originating field name
for obj, field in doc.references.get_referencing_with_fields("Office"):
    print(f"{obj.obj_type} '{obj.name}'.{field}")
```

This is the single most useful idfkit affordance when authoring loops or zone lists. If a surface's `zone_name` typo doesn't show up here, you know the wiring is broken before you simulate.

## Cascading renames

The canonical pattern. Set `obj.name` (or call `doc.rename`) and every reference updates:

```python
doc["Zone"]["Office"].name = "Open_Office"
# All fields across the document that pointed to "Office" now say "Open_Office":
#   BuildingSurface:Detailed.zone_name
#   People.zone_or_zonelist_or_space_or_spacelist_name
#   ZoneInfiltration:DesignFlowRate.zone_or_zonelist_or_space_or_spacelist_name
#   ...
```

Renaming an object that nothing references is also fine — it just updates the collection key.

## Finding what an object references

```python
people = doc["People"]["Office People"]
for target_name in doc.get_references(people):
    print(target_name)
# 'Office'              (zone_or_zonelist_or_space_or_spacelist_name)
# 'Occupancy_Sched'     (number_of_people_schedule_name)
# 'Activity_Sched'      (activity_level_schedule_name)

# With field names
for field, target in doc.references.get_references_with_fields(people):
    print(field, "->", target)
```

## Auditing dangling references

After a bulk edit, scan for references that no longer resolve:

```python
all_names = {obj.name for obj in doc.all_objects if obj.name}
for obj, field, target in doc.references.get_dangling_references(all_names):
    print(f"{obj.obj_type} '{obj.name}'.{field} -> '{target}' (missing)")
```

For a richer pre-flight check, run `validate_document(doc, check_references=True)` — it reports the same broken edges as `E004` errors. See [schema-and-validation.md](schema-and-validation.md).

## Common mistakes

!!! failure "editing a name through `_data`"

    ```python
    zone._data["name"] = "Open_Office"
    # The collection key, the reference graph, and every surface.zone_name field
    # are all stale. The model is now inconsistent.
    ```

!!! success "set `.name` or call `doc.rename`"

    ```python
    zone.name = "Open_Office"
    ```

!!! failure "editing a referencing field by string mutation"

    ```python
    # Update one surface's zone_name string in place
    surfaces = doc["BuildingSurface:Detailed"]
    surfaces["South Wall"]._data["zone_name"] = "Open_Office"
    # Reference graph still thinks "South Wall".zone_name -> "Office".
    # get_referencing("Office") will return "South Wall"; get_referencing("Open_Office") will not.
    ```

!!! success "set the field through the wrapper"

    ```python
    surfaces["South Wall"].zone_name = "Open_Office"  # graph updates
    ```

!!! failure "counting references with a manual loop"

    ```python
    # O(N * M) and easy to miss extensible fields
    count = sum(
        1 for obj in doc.all_objects
        for value in obj._data.values()
        if value == "Office"
    )
    ```

!!! success "ask the graph"

    ```python
    count = len(doc.get_referencing("Office"))  # O(1)
    ```

## Related

- [document-and-objects.md](document-and-objects.md) — where field mutations originate.
- [hvac-loops.md](hvac-loops.md) — the canonical place reference tracking shines.
- [schema-and-validation.md](schema-and-validation.md) — `check_references=True` surfaces dangling edges as errors.
- API docs: [py.idfkit.com/api/references/](https://py.idfkit.com/api/references/)
