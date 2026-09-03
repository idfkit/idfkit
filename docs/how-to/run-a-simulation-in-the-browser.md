# How to run a simulation in the browser

This guide is TypeScript only. There is no Python browser runtime; to run
EnergyPlus locally from Python, see
[How to run a simulation](../simulation/running.md) instead.

`@idfkit/core` stops at the model. To simulate one in a browser, hand the IDF
text to [`@idfkit/engine`](https://www.npmjs.com/package/@idfkit/engine), which
runs EnergyPlus via WebAssembly.

The seam between the two libraries is plain IDF text, which is the practical
payoff of
[keeping the core synchronous and string-based](../explanation/sync-core-async-edge.md).

## Install and serve the engine assets

```bash
npm install @idfkit/core @idfkit/schemas @idfkit/engine @idfkit/engine-assets
npx idfkit-engine-assets public/energyplus   # copy the WASM engine to your own origin
```

## Edit, hand over, read back

```ts
import { parseIdf, writeIdf, SchemaBundle, httpSource } from '@idfkit/core';
import { createEnergyPlus } from '@idfkit/engine';

// 1. Edit the model here.
const schema = await new SchemaBundle(httpSource('/schemas/')).load('26.1.0');
const { document } = parseIdf(idfText, schema);
document.require('Zone', 'SPACE1-1').ceiling_height = 3;

// 2. Hand it over as IDF text. Loading compiles a ~28 MB binary, so create the
//    engine once and reuse it across runs.
const ep = await createEnergyPlus({ assetBaseUrl: '/energyplus' });
const result = await ep.run({ idf: writeIdf(document), epw: epwText });

// 3. A failed run is data, not an exception: the err report is worth reading.
if (result.success) {
  console.log(result.eso?.variables.size, 'output variables');
} else {
  console.error(result.fatalError, result.err?.entries);
}
ep.dispose();
```

## Keep the versions aligned

`@idfkit/engine-assets` is versioned by the EnergyPlus release it carries, so
`@idfkit/engine-assets@26.1.0` is EnergyPlus 26.1.0. A document can be any of
the [17 supported versions](../reference/versions.md), so load the schema that
matches the asset package you installed.

Nothing checks this for you. A mismatch means the engine reads a model written
for a different release.

## `HVACTemplate:*` objects need no special handling

`run()` expands them with the bundled ExpandObjects preprocessor before
simulating. Call `expandObjects` from `@idfkit/engine` yourself only when you
want the expanded IDF back, and if you do, `parseIdf` reads it straight into a
document.

## A model that reads a file needs that file handed over too

The seam is IDF text plus, when the model needs them, the files it names.
`Schedule:File`, `Table:Lookup` and `Chiller:Electric:ASHRAE205` all point at
something on disk, and the engine cannot open a file nobody gave it.

Pass the contents in `files`, keyed by exactly the path written in the model:
relative to it, and case-sensitive, because the simulation filesystem is.

```ts
const result = await ep.run({
  idf: writeIdf(document),
  epw: epwText,
  files: { 'occupancy.csv': csvText },
});
```

Read the key off the document rather than hardcoding it, and the two cannot
drift apart:

```ts
const name = document.require('Schedule:File', 'Occupancy').get('file_name');
```

A model naming a file that is not in `files` fails before the engine starts,
with `success: false` and a `fatalError` naming the object and the path, so you
get "you forgot occupancy.csv" rather than an error from inside the engine.
`detectExternalFileReferences(idf)`, also from `@idfkit/engine`, lists what a
model needs before you run it.

## Results do not come back through this library

The engine returns its own parsed `err`, `eso`, and `mtr` structures, along
with raw `sql` and `html`. `@idfkit/core` has no output-reading API and is not
planning one. Re-parsing expanded IDF is the only return path that involves it.

<!-- Maintainers: `@idfkit/engine` is developed in a private repository. Link
     to npm rather than to GitHub in anything public. -->

## See also

- [How to parse in the browser](parse-in-the-browser.md) for serving the schema
  bundle and getting the version right
- [How to run a simulation](../simulation/running.md) for the Python path,
  which drives a local EnergyPlus installation instead
- [About capability parity](../explanation/parity.md) for how absences like
  this one are recorded
