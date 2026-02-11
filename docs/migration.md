# Migrating from eppy

idfkit provides a compatibility layer so most eppy code works with only
minor changes. You can migrate gradually -- all the eppy-style methods
listed below are available alongside the newer idfkit API.

## Loading a file

**eppy** requires you to locate and pass the IDD file yourself:

```python
from eppy.modeleditor import IDF

IDF.setiddname("/path/to/Energy+.idd")
idf = IDF("/path/to/in.idf")
```

**idfkit** bundles schemas and detects the version automatically:

```python
from idfkit import load_idf

doc = load_idf("in.idf")
```

No IDD path is needed. If you want to target a specific EnergyPlus version:

```python
doc = load_idf("in.idf", version=(24, 1, 0))
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
| Output type | `idf.outputtype = "compressed"` | `write_idf(doc, path, output_type="compressed")` | -- |
| Batch update | `json_functions.updateidf(idf, d)` | `doc.update(d)` | `doc.update(d)` |
| HTML tables | `readhtml.titletable(html)` | `result.html.titletable()` | -- |

## Creating objects

**eppy:**

```python
zone = idf.newidfobject("ZONE")
zone.Name = "Office"
zone.X_Origin = 0.0
```

**idfkit:**

```python
zone = doc.add("Zone", "Office", x_origin=0.0)
```

Or using the eppy-compatible method:

```python
zone = doc.newidfobject("Zone", Name="Office", X_Origin=0.0)
```

## Accessing fields

**eppy** uses the capitalised IDD field names:

```python
print(zone.X_Origin)
zone.X_Origin = 5.0
```

**idfkit** uses snake_case names:

```python
print(zone.x_origin)
zone.x_origin = 5.0
```

Both styles resolve to the same underlying data.

## Reference tracking (new in idfkit)

eppy has no built-in way to find which objects reference a given name.
idfkit maintains a live reference graph:

```python
# Find every object that points to the "Office" zone
for obj in doc.get_referencing("Office"):
    print(obj.obj_type, obj.name)

# Find every name that the People object references
names = doc.get_references(people_obj)
```

## Renaming with cascading updates (new in idfkit)

In eppy, renaming a zone requires you to manually update every surface,
people, lights, and other object that references it. In idfkit the
reference graph handles this automatically:

```python
zone = doc["Zone"]["Office"]
zone.name = "Open_Office"
# All fields across the document that pointed to "Office" now say "Open_Office"
```

## Validation (new in idfkit)

```python
from idfkit import validate_document

result = validate_document(doc)
if not result.is_valid:
    for error in result.errors:
        print(error)
```

## Saving files

**eppy** saves through methods on the IDF object:

```python
idf.saveas("out.idf")
idf.savecopy("backup.idf")
idf.save()
```

**idfkit** supports the same methods:

```python
doc.saveas("out.idf")    # save and update doc.filepath
doc.savecopy("backup.idf")  # save without changing doc.filepath
doc.save()               # save to current doc.filepath
```

Or use the standalone writer for more control:

```python
from idfkit import write_idf, write_epjson

write_idf(doc, "out.idf")
write_epjson(doc, "out.epJSON")  # or convert to epJSON
```

## Output formatting modes

**eppy** controls output formatting with `idf.outputtype`:

```python
idf.outputtype = "nocomment"
idf.saveas("out.idf")
```

**idfkit** passes the mode to the writer:

```python
from idfkit import write_idf

write_idf(doc, "out.idf", output_type="nocomment")    # no field comments
write_idf(doc, "out.idf", output_type="compressed")   # single-line objects
write_idf(doc, "out.idf", output_type="standard")     # default, with comments
```

## Following references

**eppy** lets you follow a reference field to get the target object:

```python
surface = idf.idfobjects["BuildingSurface:Detailed"][0]
construction = surface.get_referenced_object("Construction_Name")
```

**idfkit** provides the same method:

```python
surface = doc["BuildingSurface:Detailed"][0]
construction = surface.get_referenced_object("construction_name")
```

## Finding referring objects

**eppy** finds all objects that reference a given object:

```python
zone = idf.idfobjects["ZONE"][0]
referrers = zone.getreferingobjs()
```

**idfkit** provides both the eppy spelling and a corrected alias:

```python
zone = doc["Zone"]["Office"]

# eppy-compatible spelling
referrers = zone.getreferingobjs()

# Corrected spelling
referrers = zone.get_referring_objects()

# Optional filters -- by IDD group and/or field name
surfaces = zone.getreferingobjs(
    iddgroups=["Thermal Zones and Surfaces"],
    fields=["zone_name"],
)
```

## Range checking

**eppy** provides range checking on numeric fields:

```python
obj.getrange("Density")
# {'minimum': 0, 'type': 'real'}

obj.checkrange("Density")  # raises RangeError if out of range
```

**idfkit** supports the same API:

```python
from idfkit import RangeError

obj.getrange("density")
# {'minimum': 0, 'type': 'real'}

obj.checkrange("density")  # True, or raises RangeError
```

## Removing objects by index

**eppy** removes objects by index with `popidfobject`:

```python
removed = idf.popidfobject("ZONE", 0)
```

**idfkit:**

```python
removed = doc.popidfobject("Zone", 0)
```

## Batch updates

**eppy** uses `json_functions.updateidf()` for parametric sweeps:

```python
from eppy import json_functions
json_functions.updateidf(idf, {"Zone.Office.x_origin": 10.0})
```

**idfkit** has this as a method on the document:

```python
doc.update({
    "Zone.Office.x_origin": 10.0,
    "Zone.Office.y_origin": 5.0,
})
```

## Geometry

eppy relies on [geomeppy](https://github.com/jamiebull1/geomeppy) for
geometry operations. idfkit ships its own `Vector3D` and `Polygon3D`
classes with no external dependencies:

```python
from idfkit.geometry import (
    calculate_surface_area,
    calculate_surface_tilt,
    calculate_surface_azimuth,
    calculate_zone_volume,
    calculate_zone_height,
    calculate_zone_ceiling_area,
)

for surface in doc["BuildingSurface:Detailed"]:
    area = calculate_surface_area(surface)
    tilt = calculate_surface_tilt(surface)      # 0=up, 90=vertical, 180=down
    azimuth = calculate_surface_azimuth(surface) # 0=north, 90=east, 180=south
    print(f"{surface.name}: {area:.1f} m2, tilt={tilt:.0f}, azimuth={azimuth:.0f}")

print("Zone volume:", calculate_zone_volume(doc, "Office"))
print("Zone height:", calculate_zone_height(doc, "Office"))
print("Ceiling area:", calculate_zone_ceiling_area(doc, "Office"))
```

### Building transforms

Translate or rotate all surfaces in the model:

```python
from idfkit.geometry import translate_building, rotate_building, Vector3D

# Shift the entire building 10m east and 5m north
translate_building(doc, Vector3D(10.0, 5.0, 0.0))

# Rotate 45 degrees counter-clockwise around the origin
rotate_building(doc, 45.0)

# Rotate around a custom anchor point
rotate_building(doc, 90.0, anchor=Vector3D(5.0, 5.0, 0.0))
```

## HTML tabular output

**eppy** parses HTML tabular output using `readhtml`:

```python
from eppy import readhtml
with open("eplustbl.htm") as f:
    html = f.read()
tables = readhtml.titletable(html)
```

**idfkit** parses HTML output as part of `SimulationResult`:

```python
result = simulate(doc, weather)
html = result.html  # HTMLResult, lazily parsed

# eppy-compatible (title, rows) pairs
for title, rows in html.titletable():
    print(title, len(rows), "rows")

# Lookup by name
table = html.tablebyname("Site and Source Energy")
print(table.to_dict())  # {row_key: {col_header: value}}

# Filter by report
annual = html.tablesbyreport("Annual Building Utility Performance Summary")
```

Or parse a standalone HTML file:

```python
from idfkit.simulation.parsers.html import HTMLResult

html = HTMLResult.from_file("eplustbl.htm")
```
