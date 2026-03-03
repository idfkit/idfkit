# Migrating from eppy

idfkit provides a compatibility layer so most eppy code works with only
minor changes. You can migrate gradually -- all the eppy-style methods
listed below are available alongside the newer idfkit API.

## Loading a file

**eppy** requires you to locate and pass the IDD file yourself:

```python
--8<-- "docs/snippets/migration/loading_a_file.py:example"
```

**idfkit** bundles schemas and detects the version automatically:

```python
--8<-- "docs/snippets/migration/loading_a_file_2.py:example"
```

No IDD path is needed. If you want to target a specific EnergyPlus version:

```python
--8<-- "docs/snippets/migration/loading_a_file_3.py:example"
```

## Quick reference

The table below maps common eppy patterns to their idfkit equivalents.
The **eppy alias** column shows that the old spelling still works in idfkit
when one exists.

| Task | eppy | idfkit | eppy alias in idfkit? |
|------|------|--------|-----------------------|
| Load file | `IDF(idd, idf)` | `load_idf(path)` | -- |
| Create object | `idf.newidfobject("ZONE", Name=...)` | `doc.add("Zone", "name", ...)` | `doc.newidfobject(...)` |
| Get collection | `idf.idfobjects["ZONE"]` | `doc["Zone"]` or `doc.zones` | `doc.idfobjects[...]` |
| Get object by name | `idf.getobject("ZONE", "name")` | `doc["Zone"]["name"]` | `doc.getobject(...)` |
| Remove object | `idf.removeidfobject(obj)` | `doc.remove(obj)` | `doc.removeidfobject(obj)` |
| Remove by index | `idf.popidfobject("ZONE", 0)` | `doc.popidfobject("Zone", 0)` | `doc.popidfobject(...)` |
| Copy object | `idf.copyidfobject(obj)` | `doc.copyidfobject(obj)` | `doc.copyidfobject(obj)` |
| Object type | `obj.key` | `obj.obj_type` | `obj.key` |
| Object name | `obj.Name` | `obj.name` | `obj.Name` |
| Parent document | `obj.theidf` | `obj._document` | `obj.theidf` |
| Field names | `obj.fieldnames` | `list(obj.data.keys())` | `obj.fieldnames` |
| Field values | `obj.fieldvalues` | `list(obj.data.values())` | `obj.fieldvalues` |
| Field IDD info | `obj.getfieldidd(name)` | `obj.get_field_idd(name)` | `obj.getfieldidd(name)` |
| Field range | `obj.getrange(name)` | `obj.getrange(name)` | `obj.getrange(name)` |
| Check range | `obj.checkrange(name)` | `obj.checkrange(name)` | `obj.checkrange(name)` |
| Follow reference | `obj.get_referenced_object(name)` | `obj.get_referenced_object(name)` | `obj.get_referenced_object(name)` |
| Find referrers | `obj.getreferingobjs()` | `obj.get_referring_objects()` | `obj.getreferingobjs()` |
| Group dict | `idf.getiddgroupdict()` | `doc.getiddgroupdict()` | `doc.getiddgroupdict()` |
| Get surfaces | `idf.getsurfaces()` | `doc.getsurfaces()` | `doc.getsurfaces()` |
| Save file | `idf.save()` | `doc.save()` | `doc.save()` |
| Save as | `idf.saveas(path)` | `doc.saveas(path)` | `doc.saveas(path)` |
| Save copy | `idf.savecopy(path)` | `doc.savecopy(path)` | `doc.savecopy(path)` |
| Output type | `idf.outputtype = "compressed"` | `doc.save(output_type="compressed")` | -- |
| Run simulation | `idf.run(weather)` | `simulate(doc, weather)` | `doc.run(weather)` |
| Batch update | `json_functions.updateidf(idf, d)` | `doc.update(d)` | `doc.update(d)` |
| HTML tables | `readhtml.titletable(html)` | `result.html.titletable()` | -- |
| Window-wall ratio | `idf.set_wwr(0.4)` | `set_wwr(doc, 0.4)` | -- |
| Match surfaces | `idf.intersect_match()` | `intersect_match(doc)` | -- |

## Creating objects

**eppy:**

```python
--8<-- "docs/snippets/migration/creating_objects.py:example"
```

**idfkit:**

```python
--8<-- "docs/snippets/migration/creating_objects_2.py:example"
```

Or using the eppy-compatible method:

```python
--8<-- "docs/snippets/migration/creating_objects_3.py:example"
```

## Accessing fields

**eppy** uses the capitalised IDD field names:

```python
--8<-- "docs/snippets/migration/accessing_fields.py:example"
```

**idfkit** uses snake_case names:

```python
--8<-- "docs/snippets/migration/accessing_fields_2.py:example"
```

Both styles resolve to the same underlying data.

## Reference tracking (new in idfkit)

eppy has no built-in way to find which objects reference a given name.
idfkit maintains a live reference graph:

```python
--8<-- "docs/snippets/migration/reference_tracking_new_in_idfkit.py:example"
```

## Renaming with cascading updates (new in idfkit)

In eppy, renaming a zone requires you to manually update every surface,
people, lights, and other object that references it. In idfkit the
reference graph handles this automatically:

```python
--8<-- "docs/snippets/migration/renaming_with_cascading_updates_new_in_idfkit.py:example"
```

## Validation (new in idfkit)

```python
--8<-- "docs/snippets/migration/validation_new_in_idfkit.py:example"
```

## Saving files

**eppy** saves through methods on the IDF object:

```python
--8<-- "docs/snippets/migration/saving_files.py:example"
```

**idfkit** supports the same methods:

```python
--8<-- "docs/snippets/migration/saving_files_2.py:example"
```

Or use the standalone writer for more control:

```python
--8<-- "docs/snippets/migration/saving_files_3.py:example"
```

## Output formatting modes

**eppy** controls output formatting with `idf.outputtype`:

```python
--8<-- "docs/snippets/migration/output_formatting_modes.py:example"
```

**idfkit** passes the mode to the writer:

```python
--8<-- "docs/snippets/migration/output_formatting_modes_2.py:example"
```

## Following references

**eppy** lets you follow a reference field to get the target object:

```python
--8<-- "docs/snippets/migration/following_references.py:example"
```

**idfkit** provides the same method:

```python
--8<-- "docs/snippets/migration/following_references_2.py:example"
```

## Finding referring objects

**eppy** finds all objects that reference a given object:

```python
--8<-- "docs/snippets/migration/finding_referring_objects.py:example"
```

**idfkit** provides both the eppy spelling and a corrected alias:

```python
--8<-- "docs/snippets/migration/finding_referring_objects_2.py:example"
```

## Range checking

**eppy** provides range checking on numeric fields:

```python
--8<-- "docs/snippets/migration/range_checking.py:example"
```

**idfkit** supports the same API:

```python
--8<-- "docs/snippets/migration/range_checking_2.py:example"
```

## Removing objects by index

**eppy** removes objects by index with `popidfobject`:

```python
--8<-- "docs/snippets/migration/removing_objects_by_index.py:example"
```

**idfkit:**

```python
--8<-- "docs/snippets/migration/removing_objects_by_index_2.py:example"
```

## Batch updates

**eppy** uses `json_functions.updateidf()` for parametric sweeps:

```python
--8<-- "docs/snippets/migration/batch_updates.py:example"
```

**idfkit** has this as a method on the document:

```python
--8<-- "docs/snippets/migration/batch_updates_2.py:example"
```

## Geometry

eppy relies on [geomeppy](https://github.com/jamiebull1/geomeppy) for
geometry operations. idfkit ships its own `Vector3D` and `Polygon3D`
classes with no external dependencies:

```python
--8<-- "docs/snippets/migration/geometry.py:example"
```

### Building transforms

Translate or rotate all surfaces in the model:

```python
--8<-- "docs/snippets/migration/building_transforms.py:example"
```

### Window-wall ratio

**geomeppy** sets window-wall ratios as a method on the IDF:

```python
--8<-- "docs/snippets/migration/set_wwr.py:example"
```

**idfkit** uses a standalone function:

```python
--8<-- "docs/snippets/migration/set_wwr_2.py:example"
```

### Surface intersection and matching

**geomeppy** matches adjacent surfaces as a method on the IDF:

```python
--8<-- "docs/snippets/migration/intersect_match.py:example"
```

**idfkit** uses a standalone function:

```python
--8<-- "docs/snippets/migration/intersect_match_2.py:example"
```

## Strict field access (new in idfkit)

idfkit has two different strictness settings:

- **Strict parsing** (`load_idf(..., strict=True)`) validates IDF input while
  reading and is enabled by default.
- **Strict field access** (`doc.strict = True`) raises on mistyped attribute
  names when reading or writing object fields.

eppy silently returns an empty string when you mistype a field name,
making bugs hard to find. idfkit defaults to the same behaviour for
compatibility at field-access time, but you can opt in to **strict field
access** to catch typos
immediately:

```python
--8<-- "docs/snippets/migration/strict_mode.py:example"
```

Enable strict field access during migration to surface field-name
mismatches early. Once your code is clean you can leave it on or turn it
off.

## Running a simulation

**eppy** runs simulations directly on the IDF object:

```python
--8<-- "docs/snippets/migration/running_a_simulation.py:example"
```

**idfkit** uses a standalone `simulate()` function (recommended):

```python
--8<-- "docs/snippets/migration/running_a_simulation_2.py:example"
```

Or use the eppy-compatible convenience method:

```python
--8<-- "docs/snippets/migration/running_a_simulation_3.py:example"
```

## HTML tabular output

**eppy** parses HTML tabular output using `readhtml`:

```python
--8<-- "docs/snippets/migration/html_tabular_output.py:example"
```

**idfkit** parses HTML output as part of `SimulationResult`:

```python
--8<-- "docs/snippets/migration/html_tabular_output_2.py:example"
```

Or parse a standalone HTML file:

```python
--8<-- "docs/snippets/migration/html_tabular_output_3.py:example"
```
