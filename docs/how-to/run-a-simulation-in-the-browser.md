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

{{ parity("browser-simulation") }}

## Install and serve the engine assets

The engine is installed by its own name. `npm install idfkit` does not reach it
and is not going to: the assets are about 51 MB of WebAssembly and they pin one
EnergyPlus release, so nothing that the shared name installs may depend on them
(FR-070).

```bash
npm install @idfkit/engine @idfkit/engine-assets@26.1
npx idfkit-engine-assets public/energyplus   # copy the WASM engine to your own origin
```

`@idfkit/core` and `@idfkit/schemas` are separate and are what edits the model;
add them if you have not already.

!!! info "This engine executes EnergyPlus 26.1"

    `@idfkit/engine-assets` is versioned by the EnergyPlus release it carries,
    so `@idfkit/engine-assets@26.1` runs **EnergyPlus 26.1** and nothing else. A
    model written for another release has to be migrated before it will run
    here.

    That version is not a conformance level and has no relationship to the
    levels in this site's footer. Those say which corpus the two libraries agree
    on when they read a file; this says which simulation engine your browser
    downloads. The two move independently and comparing them means nothing.

## Edit, hand over, read back

```ts
--8<-- "docs/snippets/js/how-to/run-a-simulation-in-the-browser/edit_hand_over_read_back.ts:example"
```

## Keep the versions aligned

A document can be any of the [17 supported
versions](../reference/versions.md), and the engine executes exactly one of
them, so load the schema that matches the asset package you installed.

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
--8<-- "docs/snippets/js/how-to/run-a-simulation-in-the-browser/a_model_that_reads_a_file_needs_that_file_handed_over_too.ts:example"
```

Read the key off the document rather than hardcoding it, and the two cannot
drift apart:

```ts
--8<-- "docs/snippets/js/how-to/run-a-simulation-in-the-browser/a_model_that_reads_a_file_needs_that_file_handed_over_too_2.ts:example"
```

A model naming a file that is not in `files` fails before the engine starts,
with `success: false` and a `fatalError` naming the object and the path, so you
get "you forgot occupancy.csv" rather than an error from inside the engine.
`detectExternalFileReferences(idf)`, also from `@idfkit/engine`, lists what a
model needs before you run it.

## Try it here

The example below is the one this page's runner executes. It is the same file
`npm run typecheck:docs` compiles in `idfkit-js`, fetched from this site and run
verbatim, so what you press is what you read.

```js
--8<-- "docs/snippets/js/how-to/run-a-simulation-in-the-browser/live_runner.js:example"
```

<div class="engine-runner"
     data-engine-example="../../snippets/js/how-to/run-a-simulation-in-the-browser/live_runner.js"
     data-engine-schemas="https://cdn.jsdelivr.net/npm/@idfkit/schemas@0.1.0/data/"
     data-engine-weather="https://cdn.jsdelivr.net/npm/@idfkit/engine-assets@26.1/weather/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw">
  <button class="md-button" type="button" data-engine-run>
    Run EnergyPlus in this tab
  </button>
  <p class="engine-runner__status" data-engine-status>
    Nothing is downloaded until you press the button. Doing so fetches about
    51&nbsp;MB of WebAssembly from a CDN, once.
  </p>
</div>

This page hosts none of that: the assets come from the CDN at the moment you
ask for them, and the built site contains no engine bytes at all, which its
own build checks assert (SC-027). If the download fails, or your browser
declines it, the example above is unchanged and copying it into a project is
the whole of what the button was going to do.

The runner is a demonstration and not a test. Nothing in this project's CI runs
EnergyPlus in a browser, so it establishes that the example runs on *your*
machine today and nothing more. What catches a renamed engine API is the
type-check, described in [browser
simulation](../explanation/browser-simulation.md).

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
