# Content-addressed schemas

*This page is about the TypeScript library, which has to send its schemas over
the network. Python installs the same schemas from a wheel, one gzipped file per
version, where their size is nobody's problem.*

The raw epJSON schemas are about 10 MB each and there are 17 of them, roughly
11.9 MB gzipped for the set. On a page load that number decides your
architecture, so the browser bundle stores the same information differently.

{{ parity("schema-access") }}

## Most of a schema is the previous schema

Object-type definitions barely change between EnergyPlus releases. `Zone` has
not changed since 8.9. Across the 17 versions the bundle indexes 14,092
type entries and finds only 2,568 distinct definitions behind them: 82% of what
17 separate schemas would carry is a repeat of something already shipped.

So the bundle stores each unique definition once, keyed by a hash of its
content, and gives every version a manifest mapping type name to hash.

|                                          | All 17 versions, gzipped |
| ---------------------------------------- | ------------------------ |
| Raw epJSON schemas, as Python ships them | 11,915 KB                |
| Slimmed (documentation metadata dropped) | 2,922 KB                 |
| Content-addressed                        | about 1,000 KB           |

The two reductions are independent. Slimming keeps only what a parse needs and
discards the documentation weight, which otherwise sits on the critical path of
every parse: see [slim schema format](../reference/slim-schema-format.md) for
what survives. Content-addressing then removes the duplication that remains.

## The alternative that looks obvious

Publish `@idfkit/schemas-26-1`, `@idfkit/schemas-25-2`, and so on, and let
people install the one they need.

It is the wrong move, for two reasons. It duplicates the shared definitions
across every package, so the ecosystem-wide total goes up rather than down. And
it makes cross-version work, meaning migration tooling, diffing, or a viewer
that opens whatever file it is handed, require several installs and a dynamic
import strategy. That is precisely the audience most likely to care about size.

## Two consequences beyond size

**Loading a second version is nearly free.** The blob store is shared across a
`SchemaBundle`, so loading 26.1.0 after 9.4.0 pays only for the definitions the
two versions do not have in common.

**A cross-version diff is a manifest comparison**, not a deep walk of two 10 MB
documents:

```ts
--8<-- "docs/snippets/js/explanation/content-addressed-schemas/two_consequences_beyond_size.ts:example"
```

`changed` falls out of comparing two hashes. There is no structural comparison
at all.

## Shared identity, and why it reaches the object model

Definitions are frozen and shared by identity, not merely by value:

```ts
--8<-- "docs/snippets/js/explanation/content-addressed-schemas/shared_identity_and_why_it_reaches_the_object_model.ts:example"
```

`@idfkit/core` keys its per-type prototypes on the definition object rather than
on the type name, so those two versions of `Zone` share one prototype. A
document holding objects from several versions stays monomorphic for free: a
performance property that fell out of a size decision, and one of the reasons
[accessors rather than a `Proxy`](accessors-not-proxies.md) work as well as they
do.

Because the definitions are shared and frozen, they must not be mutated.
Nothing enforces that beyond `Object.freeze`, and a mutation would reach every
version at once.

## The stability requirement

Hashes are computed from a canonical serialization: sorted keys, fixed
separators, no whitespace. That canonicalization has to stay stable across
rebuilds. If it drifts, every hash changes and every manifest changes, so a
regeneration produces a diff covering the entire bundle instead of the handful
of definitions a release actually changed, and the one review that matters
becomes impossible to do.
