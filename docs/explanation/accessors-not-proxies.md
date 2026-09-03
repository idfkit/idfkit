# Why accessors and not a `Proxy`

*This page is about the TypeScript library.*

`zone.ceiling_height` is a real property. It is not a `Proxy` trap, and the
difference is not academic.

## The obvious translation, and why it was rejected

The Python library resolves `zone.ceiling_height` at runtime through
`IDFObject.__getattr__`: the attribute does not exist, Python calls a hook, and
the hook consults the schema. The mechanical translation of that to JavaScript
is a `Proxy`, and a `Proxy` was rejected for two reasons.

**Property access through a trap is not free.** Reading an ordinary property is
an inline cache hit; reading through a proxy is a call into a trap, every time.
A parse creates one object per record in the file and then reads every field
again to write the document back out, so the cost lands on the whole document
rather than on a few call sites. Neither library has published a measurement of
the difference, and the decision was made on the mechanism rather than on a
number.

**A trap is not what the generated types describe.** The `.d.ts` interfaces in
each version's type package describe named properties. Real accessors on a
prototype are exactly that; a proxy's properties come into existence only when
something asks for them, so the type would have to be asserted separately from
the object that carries it, and the assertion would be the thing that goes
stale. Python reaches the same destination by a different route, pairing the
`__getattr__` hook with generated `.pyi` stubs: see
[type-safe development](../concepts/type-safety.md) and
[static types generated from the schema](generated-types.md).

## What is done instead

Each object type gets one prototype, built once by `ObjectShape`, carrying
`Object.defineProperty` accessors for every field in the schema. Every instance
of that type shares it. Reads are ordinary monomorphic property lookups, and the
generated `.d.ts` interfaces describe them statically.

Shapes are keyed by the schema definition object rather than by type name.
Because the bundle is [content-addressed](content-addressed-schemas.md), `Zone`
in 9.4.0 and `Zone` in 26.1.0 are the same frozen definition, so they share one
shape and one prototype. A document holding objects from two EnergyPlus versions
stays monomorphic without anyone arranging for it.

## Why the setter matters

The reference graph is live. Renaming an object rewrites every field elsewhere
that pointed at the old name:

```ts
const zone = doc.require('Zone', 'SPACE1-1');
zone.name = 'Open Office';
surface.zone_name; // 'Open Office'
```

Nothing was called to make that happen. There is no `update()`, no
`rebuildIndex()`, and no invalidation step for a caller to forget. The write
went through the accessor's setter, and the setter is where the graph edge
moves.

That is the real argument for defining accessors rather than storing plain data
properties. A plain property would be faster still and would leave the graph
stale on every write, which is a correctness problem rather than a performance
one. Extensible groups are covered too: `ZoneList`, `Branch`, and the supply and
return paths carry all of their references inside repeat groups, so a graph that
ignored those would let a rename quietly produce a broken model.
