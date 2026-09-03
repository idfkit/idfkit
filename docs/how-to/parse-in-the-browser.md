# How to parse in the browser

This guide is TypeScript only. There is no Python browser runtime, so nothing
here has a Python counterpart.

The parser itself needs nothing special: `@idfkit/core` has no I/O and no
`node:*` imports, so a bundler pulls in the parser and nothing else. The only
question is where the schema comes from, and the answers below are about that.

{{ parity("parse") }}

## Serve the bundle

Copy the data directory to a path your server serves:

```bash
cp -r node_modules/@idfkit/schemas/data public/schemas
```

Then point `httpSource` at it:

```ts
--8<-- "docs/snippets/js/how-to/parse-in-the-browser/serve_the_bundle.ts:example"
```

`httpSource` fetches the gzipped files and inflates them with
`DecompressionStream`, so the payload stays around 1 MB for all 17 versions. It
sniffs the gzip magic bytes first, so it works whether your host leaves
`Content-Encoding` unset or maps the `.gz` extension to
`Content-Encoding: gzip` (as Vite's dev server and nginx's `gzip_static` do),
where the client inflates the body itself.

Hold the `SchemaBundle` for the lifetime of the page. It caches by version,
shares one blob store across versions, and collapses concurrent loads of the
same version into a single fetch.

## Do not put the bundle behind a bundler import

It is tempting to `import schemas from '@idfkit/schemas/data/index.json'` and
let the bundler inline it. Do not: the manifests and blob store are megabytes
of JSON, and inlining them puts all 17 versions into the initial bundle whether
or not the user opens a file.

If you would rather not serve static files at all, supply your own
`BundleSource` backed by dynamic `import()`:

```ts
--8<-- "docs/snippets/js/how-to/parse-in-the-browser/do_not_put_the_bundle_behind_a_bundler_import.ts:example"
```

That keeps each manifest in its own chunk, fetched on demand.

## Read a file the user picked as latin-1

`File.text()` decodes as UTF-8, which is wrong for IDF often enough to matter:
real models carry single high bytes in degree signs and accented station names.
Decode as latin-1, the way `loadIdf` does on the server:

```ts
--8<-- "docs/snippets/js/how-to/parse-in-the-browser/read_a_file_the_user_picked_as_latin_1.ts:example"
```

Reading it as UTF-8 turns those bytes into U+FFFD, and they will still be
U+FFFD when you write the model back out.

## Resolve the version rather than assuming it

A file states its own version, and it usually states two components where the
schema keys have three: `Version, 9.0;` against a bundle keyed `9.0.1`. Loading
26.1 for a 9.0 file mis-maps every positional field silently instead of
failing, so resolve the version before you load a schema:

```ts
--8<-- "docs/snippets/js/how-to/parse-in-the-browser/resolve_the_version_rather_than_assuming_it.ts:example"
```

`resolveVersion` matches on major and minor when the patch component does not
line up, and returns `undefined` rather than guessing when there is no match at
all. On the server, `schemaFor` from `@idfkit/core/node` does the same three
steps in one call.

## Parse off the main thread

Nothing here needs the DOM, so a worker works unchanged:

```ts
--8<-- "docs/snippets/js/how-to/parse-in-the-browser/parse_off_the_main_thread.ts:example"
```

Documents themselves are not structured-cloneable: they hold prototypes and a
live reference graph. Pass text across the boundary in both directions.

## See also

- [How to run a simulation in the browser](run-a-simulation-in-the-browser.md)
  for what to do with the document once you have one
- [Supported versions](../reference/versions.md) for what the bundle carries
- [A synchronous core with async edges](../explanation/sync-core-async-edge.md)
  for why loading the schema is the only step you have to await
