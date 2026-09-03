# Static types generated from the schema

*This page is about the TypeScript library. Python generates types from the
same schemas by a different route: see
[type-safe development](../concepts/type-safety.md).*

`scripts/emit-types.mjs` turns one version's epJSON schema into TypeScript: 858
interfaces for EnergyPlus 26.1, one per object type, plus a `TypeMap` joining
each type name to its interface. Each version's output is its own package, so
you install the ones you want and nothing else:

```bash
npm install --save-dev @idfkit/types-v26-1
```

Parameterizing a document with that map is the whole opt-in:

```ts
--8<-- "docs/snippets/js/explanation/generated-types/static_types_generated_from_the_schema.ts:example"
```

The interfaces carry the schema's documentation with them, so units, defaults,
and choice lists reach the editor's tooltip rather than a reference tab:

```ts
--8<-- "docs/snippets/js/explanation/generated-types/static_types_generated_from_the_schema_2.ts:example"
```

## How this differs from the Python stubs

Both libraries generate types from the epJSON schema, and the parity ledger
records the capability as [complete in TypeScript and partial in
Python](parity.md#generated-object-types). Two things differ.

**Coverage.** The Python stub set is generated one EnergyPlus version at a time
and currently ships for 26.1.0 only, so a model loaded at 9.4 gets 26.1 field
names and choice lists in the editor. The TypeScript maps are emitted per
version and chosen by the caller, so an older model is typed as that older model
or left untyped, never mistyped.

**Application.** Python's stubs apply implicitly to every document. TypeScript's
are opt-in by construction: an unparameterised document stays untyped, which is
what version-generic code needs.

The runtime story differs on reads. Both libraries refuse a misspelled field
name when you write one: Python raises `InvalidFieldError` and TypeScript
throws `"celing_height" is not a field of Zone`. Reading is where they part. In
Python's strict mode, which is the default, reading `zone.celing_height` raises
as well. In TypeScript a name with no accessor behind it is simply `undefined`,
and nothing distinguishes a typo from a field the file left unset.
Parameterizing the document turns that read into a compile error, which is the
practical argument for passing the `TypeMap` even in a codebase that is
otherwise loosely typed.

## It costs nothing, installed or not

The maps are big. EnergyPlus 26.1 is 2.7 MB of declarations and 9.4 is another
2.5 MB, against a measured 1.32 MB for the whole default install of the `idfkit`
name in JavaScript. That is why they are separate packages rather than a subpath
of core: install neither and you have a complete, working library and zero bytes
of either map on disk.

Installed, they still cost nothing at run time. `TypeMap` is a type, not a
value, and it is erased at build time. A typed document and an untyped one are
the same object graph running the same code, and `doc.all('Zone')` really is
just a string argument. Omit the parameter and everything still works, untyped:

```ts
--8<-- "docs/snippets/js/explanation/generated-types/it_costs_nothing_installed_or_not.ts:example"
```

## Two design details that are easy to get wrong

**`TypeMap` must be emitted as a `type` alias, never an `interface`.**
Interfaces have no implicit index signature, so an interface cannot satisfy
`Record<string, object>` and the map would not fit the `AnyTypeMap` constraint.
This is a real constraint on the generator, not a style preference.

**`add()` and `all()` deliberately use different helpers.** `add()` takes
`ValuesOf`, which resolves to the exact field interface for a known type name,
so TypeScript's excess-property check fires on a misspelled field in an object
literal. `all()` returns `ObjectOf`, which resolves to the interface for known
names and a permissive empty object otherwise, so version-generic code and
untyped documents still work. One helper for both would force a choice between
catching typos and allowing dynamic field names; two cost nothing and give both.

`TypeNameOf` has a similar subtlety: its `(string & {})` arm is what keeps
literal completion alive while still accepting arbitrary strings. Without it,
TypeScript widens the parameter to `string` and the 858 suggestions disappear.

## Declarations only, and it is checked

A type package holds one `index.d.ts` and nothing else: no `main`, no
`dependencies`, no build step, and no JavaScript. Nothing compiles a declaration
file, so there is nowhere for runtime code to be produced the way there was when
these were ordinary `.ts` modules inside `@idfkit/core`. `npm run
check:type-packages` measures the emitted JavaScript in every type package,
both in the working tree and in what `npm pack` would ship, and fails the build
on one byte of it, or on an exported value, which a declaration file will accept
and then emit nothing for, leaving an export that crashes whoever imports it.

`@idfkit/core` is a peer range rather than an exact version. The map borrows
exactly one type from core, `ExtensibleGroup`, and neither package carries
runtime, so a skew between the two is a type error at your build and never a
failure at run time.

## How this is kept honest

Vitest transpiles without typechecking. A change that silently breaks the type
map passes `npm test` cleanly, so the `@ts-expect-error` assertions in
`packages/core/tests/typed.test.ts`, the ones proving the generated types
actually reject bad input, mean nothing unless `tsc` runs:

```bash
npx tsc -p tsconfig.test.json
```

That is why it is a separate, non-optional step in
[CONTRIBUTING](https://github.com/idfkit/idfkit-js/blob/main/CONTRIBUTING.md)
and a separate job in CI.
