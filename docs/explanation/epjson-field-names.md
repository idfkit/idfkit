# Why field names come from epJSON

EnergyPlus spells the same field three ways. The IDD calls it
`Ceiling Height`, an IDF file does not name it at all, and epJSON calls it
`ceiling_height`. Any library over these formats has to choose one spelling for
the identifier its users type, and the choice leaks into every layer: the parse
result, the writer, the reference graph, the type information, and every example
anyone copies.

Both libraries choose the epJSON spelling, unchanged. Fields are
`ceiling_height` and `outside_boundary_condition`, never `ceilingHeight` and
never `Ceiling Height`. There is no name-conversion layer to learn, and that
absence is deliberate.

## The name on disk is the name in your code

=== "Python"

    ```python
    zone = document["Zone"]["SPACE1-1"]
    surface = document["BuildingSurface:Detailed"]["WALL-1"]

    zone.ceiling_height
    surface.outside_boundary_condition
    ```

=== "TypeScript"

    ```ts
    const zone = doc.require('Zone', 'SPACE1-1');
    const surface = doc.require('BuildingSurface:Detailed', 'WALL-1');

    zone.ceiling_height;
    surface.outside_boundary_condition;
    ```

The gain is that the epJSON schema, the EnergyPlus documentation, an epJSON file
open in a text editor, and both libraries all use one word for one thing. When
you meet an unfamiliar object type, whatever the schema calls a field is what
you type, in either language.

The gain is also negative, in the sense that matters most: there is no
conversion table to maintain, no round-tripping question about whether
`zone_name` survives as `zone_name`, and no class of bug where a field works
everywhere except the one place a mapping was applied inconsistently.

## What each language gives up for it

TypeScript gives up idiom. `zone.outside_boundary_condition` is not how a
JavaScript library would normally read; `zone.outsideBoundaryCondition` is. That
cost is paid on purpose, because a camelCase layer would need a bidirectional
mapping applied on parse, on write, on field access, on the reference graph, and
in the type generator: five places to keep consistent, for a cosmetic gain, in a
library whose whole job is to be a faithful representation of a model.

Python gives up less, because the epJSON spelling is already a legal Python
attribute name. It also accepts the IDD spelling as an alias, so `Ceiling
Height` and `CEILING_HEIGHT` both reach `ceiling_height`. Storage and output are
unaffected: the epJSON name is what is held and what is written.

## Where the rule stops

The verbatim rule covers schema-derived names, meaning object type names and
field names, because those are data. Everything that is API follows the
conventions of its language: `IDFObject.get_referring_objects` in Python and
`IdfObject.outgoingReferences` in TypeScript are both ordinary for the language
they live in. Which name a concept carries in each language is recorded
in [the naming map](naming-map.md), and the alignment is checked by a gate in
both repositories.

Object type names keep their EnergyPlus spelling, colons and all:
`BuildingSurface:Detailed`, `HVACTemplate:Zone:VAV`. Object names match
case-insensitively in both libraries, as they do in EnergyPlus, so a reference
written `SPACE1-1` finds an object named `Space1-1`. It is never rewritten to
the target's casing on the way through: the corpus pins that under its
`references` tag, alongside dangling and self-referential names.
