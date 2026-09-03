# How conformance is established

Both libraries read and write the same two formats, IDF and epJSON, and both
pass their own test suites. That proves nothing about agreement between them.
Two implementations of one schema-driven format drift apart silently, because
each suite was written by the side it tests, and the disagreement only surfaces
when someone moves a model from one language to the other.

The evidence that counts is therefore external to both. It lives in
[idfkit-conformance](https://github.com/idfkit/idfkit-conformance): a corpus of
IDF cases with committed expected output, run by both CI pipelines, released as
immutable level tags. This page explains what the corpus asserts, what it does
not, and how to read a result from it.

## The oracle is EnergyPlus, never either library

Every expectation is produced by EnergyPlus `ConvertInputFormat`, generated
offline by a maintainer and committed next to its case. Neither library's output
is ever promoted to an expectation, and neither library's CI needs EnergyPlus
installed to run the corpus.

That is what lets the corpus report both libraries as wrong at once, which is
not hypothetical. In the case `numeric-sentinel-schema-remap`, an
`AirTerminal:SingleDuct:VAV:Reheat` field whose schema enumeration is
`["", "Autosize"]` is written in the file as `AUTOCALCULATE`. Python
canonicalises the sentinel the file wrote and answers `"Autocalculate"`.
TypeScript echoes the file's casing and answers `"AUTOCALCULATE"`. The oracle
answers `"Autosize"`,
because the schema decides which sentinel a field accepts, not the file. Had the
two libraries been checked against each other, the closest thing to a result
would have been a difference in capitalisation, and the actual bug would have
been invisible on both sides.

## Cases pin hazards, not features

A case is one input file, one declared parse outcome, and the assertions that
apply to it. Cases are grouped by the hazard each one pins:

| Tag | Pins |
| --- | ---- |
| `positional` | Trailing unset fields, with and without a following extensible group |
| `naming` | Blank name against absent name, synthetic keys, collision with a real name |
| `extensible` | Empty groups, partial groups, wrapper keys, single against multiple |
| `numeric` | autosize, autocalculate, scientific notation, integer fields, zero |
| `types` | Unknown object types, case-variant type names |
| `references` | Dangling, self-referential, case-insensitive name matching |
| `versions` | Version resolution, including `Version, 9.0` mapping to schema 9.0.1 |
| `encoding` | latin-1 high bytes in names and comments |
| `malformed` | Missing semicolon, truncated object, stray comment |
| `tier1` | Validation, type introspection, and documentation addresses |

The first set was not written from the specification. It came from running both
libraries and `ConvertInputFormat` across the whole EnergyPlus example set,
recording every three-way disagreement, and curating a minimal reproducer for
each distinct one. Hand-written cases fill the taxonomy's gaps afterwards, never
before, because a fixture drafted from the specification tests the format its
author already understands. The hazards that cost real time are the ones
[the positional format](positional-format-hazards.md) creates and nobody
predicts.

Seven assertions are defined. Six run today: the parse outcome matches what the
case declares, the canonical epJSON equals the committed expectation, re-parsing
the library's own IDF output deep-equals the original document, and the three
Tier 1 assertions compare validation findings, type descriptions, and
documentation addresses. Comparing parse diagnostics is deferred until both
languages carry a stable diagnostic code, so a case tagged `malformed` currently
proves that the parse failed and not that it failed for the stated reason.

Round-tripping earns its place among these. A single parse says nothing about
the writer, and comparing input text to output text says too much, since
formatting is not preserved. Parsing the output and comparing the two documents
isolates the property that matters: nothing was lost or displaced in the write.
A field that shifted by one slot survives a single parse unnoticed and shows up
immediately here, because the value lands somewhere different the second time.

## The level tag is the claim

A level is an immutable git tag of the form `conformance-YYYY.N`. Each library
declares the level it passes, from one value that both its CI gate and its
release check read, so the declaration and the pin cannot drift apart:

- Python: `[tool.idfkit.conformance] level` in `pyproject.toml`.
- TypeScript: `idfkit.conformance` in `packages/core/package.json`.

Both currently declare `conformance-2026.7`, and both expose it at runtime, so a
caller can ask an installed build what it claims rather than reading its
packaging:

=== "Python"

    ```python
    --8<-- "docs/snippets/explanation/conformance_level.py:example"
    ```

=== "TypeScript"

    ```typescript
    import { CONFORMANCE_LEVEL } from '@idfkit/core';

    console.log(CONFORMANCE_LEVEL); // 'conformance-2026.7'
    ```

Neither constant is written by hand. Each is generated from the one declaration
above and regenerated by a blocking check, so a pin that advances without the
export following it fails the build instead of shipping a stale claim.

### Two versions tell you nothing; two levels tell you something

The two libraries release on independent schedules. They share no version
number, no release cadence, and no coordinated tagging, and none of that is an
oversight: they are separate packages in separate ecosystems with separate
consumers, and coupling their versions would mean holding one release back for
the other with nothing gained.

So matching release numbers are never evidence of agreement, and this
documentation never presents them as such. `idfkit` 0.12.2 and `@idfkit/core`
0.12.2 would be a coincidence of numbering. Comparing them is the mistake the
declared level exists to prevent.

The declared level is the claim, and it is the stronger one precisely because
something outside both libraries tested it. Two installed builds agree about the
formats when they declare the same level, whatever their own versions say:

```console
$ python -c "import idfkit; print(idfkit.CONFORMANCE_LEVEL)"
conformance-2026.7
$ node -e "import('@idfkit/core').then(m => console.log(m.CONFORMANCE_LEVEL))"
conformance-2026.7
```

A release cannot state a level it does not pass. Each library's release runs the
corpus at its declared tag, exported from the conformance repository's git
history rather than read from a working copy, and refuses to publish if it
fails. Lowering the declaration to whatever currently passes is not the remedy
for a red release check: the level is a claim about the library, not a label for
its current state.

## Recorded disagreements are visible, not silenced

The corpus shipped with real failures already recorded in
`known-divergence.toml`, each carrying the issue tracking its resolution. That
is what let it go green on arrival and start blocking new drift immediately,
rather than waiting for every bug it had already found to be fixed.

Three rules keep the register from becoming a mute button. An entry without a
tracked issue is rejected, because an untracked exception is indistinguishable
from an accepted bug. The runners print every outstanding exception rather than
suppressing it. And an allowlisted case that starts passing fails the run, so
the entry is removed by the change that fixes the bug.

## What the corpus does not prove

Round-trip fidelity is not model correctness. The corpus shows that a library
reads and writes what is on disk faithfully; it says nothing about whether the
model is physically sensible or whether EnergyPlus will accept it.

Three gaps are open and named in the corpus README:

- **Diagnostics are not compared.** Deferred until a shared diagnostic code
  vocabulary exists on both sides.
- **Neither library's file reading is exercised.** The runners decode the input
  themselves and hand a string to the parser, which is what makes an encoding
  difference a finding rather than noise. The cost is that a bug living in the
  decode step is invisible to every case here, no matter how many are added.
- **Weather retrieval has no expressible case.** Resolving a station is not an
  input file, a parsed document, and an assertion about it, so a green run over
  the `tier1` tag is not a statement about weather.

Cases are also curated from the EnergyPlus example files, so the corpus sees
only the hazards those files exhibit. Byte-order marks, CRLF line endings, and
the rest of what real editors emit are not in that set.

Conformance and parity answer different questions, and both are needed. The
corpus answers whether the two libraries agree about a file they both claim to
read. [The parity ledger](parity.md) answers whether a capability exists in the
language you are working in at all, and
[the naming map](naming-map.md) answers what it is called there.
