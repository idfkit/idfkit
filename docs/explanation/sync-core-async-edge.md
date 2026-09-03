# A synchronous core with async edges

*This page is about the TypeScript library. The Python library has a different
I/O boundary, described in
[simulation architecture](../concepts/simulation-architecture.md).*

`parseIdf`, `writeIdf`, and every method on `IdfDocument` are synchronous and
take strings. None of them can read a file, fetch a URL, or return a promise.
Everything that touches a disk or a network lives in one of two places:
`@idfkit/core/node`, or `SchemaBundle`.

## Why not simply accept a path

Because a function that can read a file has to be async, and async is
load-bearing in a way that spreads. If `parseIdf` returned a promise, every
caller of it would return a promise, and so would every caller of those. A pure
transformation of text into a data structure would be modelled as an I/O
operation for the whole call graph, on the strength of one convenience.

The convenience is small anyway. `await readFile(path)` is one line, and
`@idfkit/core/node` supplies `loadIdf` for the common case.

## What the constraint buys

**The same core runs everywhere:** Node, a browser, a web worker, an edge
runtime. There is no environment detection, no conditional import, and no
polyfill. The portable entry point cannot import `node:*`, so a browser bundle
physically cannot pull in `node:fs`.

Bundles stay small, because a bundler tracing `@idfkit/core` finds no I/O and so
has nothing to shim and nothing to exclude. Testing stays simple, because parser
tests pass strings: no fixtures on disk to keep in sync, no temp directories, no
cleanup.

The payoff that shapes the rest of the design is the seam with other tools.
`writeIdf(document)` produces a string and
[`@idfkit/engine`](https://www.npmjs.com/package/@idfkit/engine) takes a string,
so neither library needs to know anything about the other's object model. That
is why [running EnergyPlus in the browser](parity.md#browser-simulation) is a
separate package rather than a feature of this one.

## The one asynchronous step

Loading a schema. A schema has to come from somewhere, whether the package's own
data directory, an HTTP fetch, or a bundler-driven `import()`, and there is no
way to make that synchronous in a browser.

So it is explicit rather than hidden:

```ts
--8<-- "docs/snippets/js/explanation/sync-core-async-edge/the_one_asynchronous_step.ts:example"
```

Hold one `SchemaBundle` for the lifetime of the process. It caches by version,
shares one blob store across versions, and collapses concurrent loads of the
same version into a single fetch, so calling `load` freely is fine. The sharing
is not only a size property: see
[content-addressed schemas](content-addressed-schemas.md).

The alternative, an async `parseIdf` that loads the schema itself, would hide
the one genuine I/O operation inside the one function with no other reason to be
async, and would do it once per parse instead of once per process.
