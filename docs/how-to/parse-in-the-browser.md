# How to parse in the browser

This guide is TypeScript only. There is no Python browser runtime, so nothing
here has a Python counterpart.

The parser itself needs nothing special: `@idfkit/core` has no I/O and no
`node:*` imports, so a bundler pulls in the parser and nothing else. The only
question is where the schema comes from, and the answers below are about that.

## Serve the bundle

Copy the data directory to a path your server serves:

```bash
cp -r node_modules/@idfkit/schemas/data public/schemas
```

Then point `httpSource` at it:

```ts
import { parseIdf, SchemaBundle, httpSource } from '@idfkit/core';

const bundle = new SchemaBundle(httpSource('/schemas/'));
const schema = await bundle.load('26.1.0');

const { document } = parseIdf(idfText, schema);
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
import { SchemaBundle, type BundleSource } from '@idfkit/core';

const source: BundleSource = {
  async read(fileName) {
    return (await import(`./schemas/${fileName}.json`)).default;
  },
};

const bundle = new SchemaBundle(source);
```

That keeps each manifest in its own chunk, fetched on demand.

## Read a file the user picked as latin-1

`File.text()` decodes as UTF-8, which is wrong for IDF often enough to matter:
real models carry single high bytes in degree signs and accented station names.
Decode as latin-1, the way `loadIdf` does on the server:

```ts
const buffer = await file.arrayBuffer();
const text = new TextDecoder('latin1').decode(buffer);
```

Reading it as UTF-8 turns those bytes into U+FFFD, and they will still be
U+FFFD when you write the model back out.

## Resolve the version rather than assuming it

A file states its own version, and it usually states two components where the
schema keys have three: `Version, 9.0;` against a bundle keyed `9.0.1`. Loading
26.1 for a 9.0 file mis-maps every positional field silently instead of
failing, so resolve the version before you load a schema:

```ts
import { getIdfVersion, parseIdf, resolveVersion } from '@idfkit/core';

const detected = getIdfVersion(idfText);
if (detected === undefined) throw new Error('This file has no Version object');

const resolved = resolveVersion(detected, await bundle.versions());
if (resolved === undefined) throw new Error(`EnergyPlus ${detected} is not in the bundle`);

const schema = await bundle.load(resolved);
const { document } = parseIdf(idfText, schema);
```

`resolveVersion` matches on major and minor when the patch component does not
line up, and returns `undefined` rather than guessing when there is no match at
all. On the server, `schemaFor` from `@idfkit/core/node` does the same three
steps in one call.

## Parse off the main thread

Nothing here needs the DOM, so a worker works unchanged:

```ts
// worker.ts
import { parseIdf, writeIdf, SchemaBundle, httpSource } from '@idfkit/core';

const bundle = new SchemaBundle(httpSource('/schemas/'));

self.onmessage = async ({ data }) => {
  const schema = await bundle.load(data.version);
  const { document } = parseIdf(data.text, schema);
  self.postMessage({ objects: document.size, idf: writeIdf(document) });
};
```

Documents themselves are not structured-cloneable: they hold prototypes and a
live reference graph. Pass text across the boundary in both directions.

## See also

- [How to run a simulation in the browser](run-a-simulation-in-the-browser.md)
  for what to do with the document once you have one
- [Supported versions](../reference/versions.md) for what the bundle carries
- [A synchronous core with async edges](../explanation/sync-core-async-edge.md)
  for why loading the schema is the only step you have to await
