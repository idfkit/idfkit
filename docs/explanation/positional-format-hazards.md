# The hazards of a positional format

IDF has no field names. An object is a type name followed by comma-separated
values, and which field a value belongs to is decided entirely by how many
commas precede it:

```idf
Zone,
    SPACE1-1,      !- Name
    0,             !- Direction of Relative North
    0, 0, 0,       !- Origin
    1,             !- Type
    1,             !- Multiplier
    2.7;           !- Ceiling Height
```

The `!-` annotations are comments, and EnergyPlus ignores them entirely. Delete
one value and every value after it silently becomes a different field.

This is why a bug in an IDF parser or writer is worse than it sounds. Code that
gets a positional rule wrong does not raise; it produces a model that loads,
validates, and simulates a different building than the one on disk. Two rules
below exist for exactly that reason, and both apply to any library that touches
the format.

{{ parity("parse") }}

## Trailing fields may be trimmed only when no extensible group follows

EnergyPlus defaults omitted trailing fields, and a long run of bare commas is
noise, so a writer normally stops at the last field that holds a value.

That is safe right up until the object has an extensible group. The group's
values follow the fixed fields in the same comma stream, so trimming a fixed
field shifts every group value one slot earlier. A surface's vertices then come
back with the X of one vertex read as the Z of the one before it: geometry that
is subtly and silently wrong.

The rule is therefore that a type with an extensible group emits every fixed
slot, empty or not. The corpus tags this hazard `positional` and pins both
halves of it: an unset fixed field before an extensible group, and unset
trailing slots inside a group. This is not settled work. Python currently
carries open entries in the corpus's divergence register against two of these
cases, and the sweep that found the first counted the shape 5,558 times across
579 of the EnergyPlus example files.

## A blank name is not the same as no name

Three things look similar in a file and are not:

| Case | Example | Occupies a field slot? |
| ---- | ------- | ---------------------- |
| Named | `Zone` | Yes |
| Optional name, left blank | `WeatherProperty:SkyTemperature` | Yes |
| No name field at all | `Version`, `GlobalGeometryRules` | No |

The middle case is the trap. `WeatherProperty:SkyTemperature` has a name field
that is allowed to be empty, and that empty field still consumes a position.
Skip it on write and every subsequent field of the object is off by one.

An object's name as written is therefore not the same thing as the identity it
is filed under, and both libraries keep the written name available whatever it
is:

=== "Python"

    ```python
    for obj in document["WeatherProperty:SkyTemperature"]:
        obj.name  # '' when the file left the name blank
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/explanation/positional-format-hazards/a_blank_name_is_not_the_same_as_no_name.ts:example"
    ```

Conflating the two gives you either a collection where the second blank-named
object of a type overwrites the first, or an output file missing a comma. Both
have been real bugs. The corpus tags them `naming`, with separate cases for a
blank name against an absent one, for the key synthesised when a type has no
name field, and for the collision that happens when a synthesised key matches a
real name.

## Both rules were found by round-tripping, not by review

Neither rule is visible from reading a writer. Both surfaced from parsing real
files, writing them back out, re-parsing, and requiring the two documents to be
deeply equal: see
[how conformance is established](conformance.md). A field that shifted by one
slot is invisible after a single parse and obvious after a round trip, because
the second parse puts the value somewhere different.

The practical consequence for anyone extending either library is that a
positional change is never a local change. If you touch the writer, the evidence
that you were right is a corpus run, not a unit test you wrote alongside the
code you were already thinking about.
