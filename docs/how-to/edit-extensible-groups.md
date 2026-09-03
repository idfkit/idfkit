# How to edit extensible groups

Some object types end in a section that repeats: the vertices of a surface, the
components of a branch, the zones in a zone list. In IDF those are just more
commas on the end of the object. Both libraries turn them into a live list of
groups hanging off the object, so editing one is list work rather than field
arithmetic.

This guide reads a repeating section, adds and removes groups, replaces one
wholesale, and covers the two things that surprise people: renames propagate
into groups, and the empty slots in front of a group are load-bearing.

## Reach the section

The two libraries address the section differently. Python names it by the
epJSON key that holds it, so a surface has `vertices` and a zone list has
`zones`, and the key completes in an IDE. TypeScript exposes one generic
`extensible` accessor that works the same way on every type, so code that does
not know what it was handed does not have to look the key up.

=== "Python"

    ```python
    surface = model["BuildingSurface:Detailed"]["Wall-1"]

    len(surface.vertices)  # number of vertices
    surface.vertices[0].vertex_z_coordinate
    surface.vertices[0].as_dict()  # {'vertex_x_coordinate': ..., ...}
    ```

=== "TypeScript"

    ```ts
    const surface = doc.require('BuildingSurface:Detailed', 'Wall-1');

    surface.extensible.length; // number of vertices
    surface.extensible[0].vertex_z_coordinate;
    surface.extensible[0]; // { vertex_x_coordinate: ..., ... }
    ```

Each entry is one group, keyed by the group's field names in IDF order. For a
type with no extensible section the list is empty rather than absent, so you
can read it without checking first.

## Add and remove

The list is live: changing it changes the object.

=== "Python"

    ```python
    surface.vertices.append(
        vertex_x_coordinate=0,
        vertex_y_coordinate=0,
        vertex_z_coordinate=3,
    )

    del surface.vertices[2]  # drop the third vertex
    surface.vertices[0].vertex_z_coordinate = 3.5
    ```

=== "TypeScript"

    ```ts
    surface.extensible.push({
      vertex_x_coordinate: 0,
      vertex_y_coordinate: 0,
      vertex_z_coordinate: 3,
    });

    surface.extensible.splice(2, 1); // drop the third vertex
    surface.extensible[0].vertex_z_coordinate = 3.5;
    ```

There is no `addVertex` and no `set_vertices`. It is a list, and the list
operations of the host language work on it. Python's view also takes an
`ExtensibleGroup` or a plain dict wherever it takes keyword arguments, and it
rejects a field name the schema does not define rather than storing it.

## Replace the whole section

=== "Python"

    ```python
    surface.vertices = [
        {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
        {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
        {"vertex_x_coordinate": 5, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
    ]
    ```

=== "TypeScript"

    ```ts
    surface.vertices = [
      { vertex_x_coordinate: 0, vertex_y_coordinate: 0, vertex_z_coordinate: 3 },
      { vertex_x_coordinate: 0, vertex_y_coordinate: 0, vertex_z_coordinate: 0 },
      { vertex_x_coordinate: 5, vertex_y_coordinate: 0, vertex_z_coordinate: 0 },
    ];
    ```

Assigning to the epJSON key replaces the section in both. In TypeScript this is
the only assignment that works: `extensible` is a getter with no setter, so
assigning to it throws a `TypeError`. If you would rather not name the key,
splice the generic accessor in place instead, which is usually the reason to
prefer it:

```ts
surface.extensible.splice(0, surface.extensible.length, ...vertices);
```

## Renames reach inside groups

This is the part that is easy to assume does not work. `ZoneList`, `Branch`,
and the supply and return paths carry all of their references inside repeating
groups, and both reference graphs index those alongside ordinary fields.

=== "Python"

    ```python
    zone_list = model["ZoneList"]["All Zones"]
    zone_list.zones.append(zone_name="Open Office")

    model["Zone"]["Open Office"].name = "Open Plan"
    zone_list.zones[0].zone_name  # 'Open Plan'
    ```

=== "TypeScript"

    ```ts
    const list = doc.require('ZoneList', 'All Zones');
    list.extensible.push({ zone_name: 'Open Office' });

    doc.require('Zone', 'Open Office').name = 'Open Plan';
    list.extensible[0].zone_name; // 'Open Plan'
    ```

A graph that ignored repeating groups would make a rename silently produce a
broken model, which is why reference fields inside a group are tracked
separately from the fixed ones: they need the repeat index to be addressed at
all.

## The empty slots before a group are load-bearing

Groups are positional, like everything else in IDF. If a group has four fields
and you set two, the writer emits empty slots for the other two, which is
correct: an empty slot inside a repeat is a real, meaningful thing in IDF and
it is preserved.

The related hazard is on the fixed fields in front of the group. Both writers
normally trim unset trailing fields, and both stop doing it once a group
follows, because trimming one fixed field would shift every group value a slot
early. A surface with one vertex and nothing set between the zone name and the
vertex count therefore writes out with every slot in between still there:

```text
BuildingSurface:Detailed,
  Wall-1,                     !- Name
  Wall,                       !- Surface Type
  C1,                         !- Construction Name
  Z1,                         !- Zone Name
  ,                           !- Space Name
  Outdoors,                   !- Outside Boundary Condition
  ,                           !- Outside Boundary Condition Object
  ,                           !- Sun Exposure
  ,                           !- Wind Exposure
  ,                           !- View Factor To Ground
  ,                           !- Number Of Vertices
  0,                          !- Vertex X Coordinate
  0,                          !- Vertex Y Coordinate
  3;                          !- Vertex Z Coordinate
```

That is handled for you in both languages. See
[The hazards of a positional format](../explanation/positional-format-hazards.md)
for what it would otherwise cost.

## Find the field names for a group

How much the type checker knows about the inside of a group differs. Python's
generated stubs narrow each wrapper to a per-type group class, so
`vertex_x_coordinate` completes and type-checks on a vertex. TypeScript's
generated interfaces cover the fixed fields only: `extensible` is typed as
`ExtensibleGroup[]`, which is `Record<string, string | number>[]`, so names
inside a group are plain strings.

Either way the schema is the authority, and asking it works whether or not you
installed the generated types:

=== "Python"

    ```python
    from idfkit import get_schema, LATEST_VERSION

    schema = get_schema(LATEST_VERSION)
    schema.get_extensible_field_names("BuildingSurface:Detailed")
    # ['vertex_x_coordinate', 'vertex_y_coordinate', 'vertex_z_coordinate']
    schema.get_extensible_wrapper_key("BuildingSurface:Detailed")
    # 'vertices'
    ```

=== "TypeScript"

    ```ts
    doc.schema.get('BuildingSurface:Detailed')?.x?.fields;
    // ['vertex_x_coordinate', 'vertex_y_coordinate', 'vertex_z_coordinate']
    doc.schema.get('BuildingSurface:Detailed')?.x?.key;
    // 'vertices'
    ```

## See also

- [The hazards of a positional format](../explanation/positional-format-hazards.md)
  for why the writer behaves the way it does
- [Type-Safe Development](../concepts/type-safety.md) and
  [Static types generated from the schema](../explanation/generated-types.md)
  for what each language's generated types cover
- [Slim schema format](../reference/slim-schema-format.md) for the `x` key the
  TypeScript snippet reads
