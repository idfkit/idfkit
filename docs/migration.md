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
| Copy object | `idf.copyidfobject(obj)` | `doc.copyidfobject(obj)` | `doc.copyidfobject(obj)` |
| Object type | `obj.key` | `obj.obj_type` | `obj.key` |
| Object name | `obj.Name` | `obj.name` | `obj.Name` |
| Parent document | `obj.theidf` | `obj._document` | `obj.theidf` |
| Field names | `obj.fieldnames` | `list(obj.data.keys())` | `obj.fieldnames` |
| Field values | `obj.fieldvalues` | `list(obj.data.values())` | `obj.fieldvalues` |
| Field IDD info | `obj.getfieldidd(name)` | `obj.get_field_idd(name)` | `obj.getfieldidd(name)` |
| Group dict | `idf.getiddgroupdict()` | `doc.getiddgroupdict()` | `doc.getiddgroupdict()` |
| Get surfaces | `idf.getsurfaces()` | `doc.getsurfaces()` | `doc.getsurfaces()` |

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

## Writing output

**eppy:**

```python
idf.saveas("out.idf")
```

**idfkit:**

```python
from idfkit import write_idf, write_epjson

write_idf(doc, "out.idf")
write_epjson(doc, "out.epJSON")  # or convert to epJSON
```

## Geometry

eppy relies on [geomeppy](https://github.com/jamiebull1/geomeppy) for
geometry operations. idfkit ships its own `Vector3D` and `Polygon3D`
classes:

```python
from idfkit.geometry import calculate_surface_area, calculate_zone_volume

for surface in doc["BuildingSurface:Detailed"]:
    print(surface.name, calculate_surface_area(surface))

print("Zone volume:", calculate_zone_volume(doc, "Office"))
```
