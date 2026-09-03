// The example the live runner on the documentation page executes, and the same file CI
// type-checks. One source, two consumers, so the widget cannot drift from the checked example
// (FR-071, SC-030).
//
// THE REGION BELOW IS VALID JAVASCRIPT AS WRITTEN, and that is a constraint rather than a
// coincidence. The runner fetches this file from the site and evaluates it as a module after
// exactly one rewrite: bare specifiers become CDN URLs. No transpiler, no type stripping, no
// regex over syntax. A generic call or a `:` annotation in here would force one of those, and a
// transform nobody can see is how a widget starts running something other than what it shows.
//
// The types are therefore in JSDoc, which TypeScript checks and JavaScript ignores. That is what
// lets `npm run typecheck:docs` catch a renamed engine method here while the browser still runs
// the file verbatim.
//
// The cost is that this example cannot carry a per-version type map, so it writes fields through
// `add` rather than through `zone.ceiling_height`. The example above it on the page shows the
// typed form, and that is the one to copy.

// --8<-- [start:example]
import { IdfDocument, writeIdf } from '@idfkit/core';
import { createEnergyPlus } from '@idfkit/engine';

/**
 * Build a one-zone model, simulate it, and report what happened.
 *
 * @param {import('@idfkit/core').Schema} schema  a loaded schema for EnergyPlus 26.1
 * @param {string} epwText                        the weather file, as text
 * @param {string} assetBaseUrl                   where the engine's WebAssembly is served from
 * @param {(message: string) => void} log         called with each step, for the page to show
 * @returns {Promise<import('@idfkit/engine').EngineRunResult>}
 */
export async function run(schema, epwText, assetBaseUrl, log) {
  // 1. Build the model. Nothing here touches the network.
  const doc = new IdfDocument(schema);
  doc.add('Version', null, { version_identifier: '26.1' });
  doc.add('Building', 'Live runner', { north_axis: 0, terrain: 'City' });
  doc.add('Timestep', null, { number_of_timesteps_per_hour: 4 });
  log(`Model built: ${doc.size} objects`);

  // 2. Hand it over as IDF text. Loading compiles a ~28 MB binary, so the engine is created
  //    once and reused; this page creates it on activation and disposes it afterwards.
  const ep = await createEnergyPlus({ assetBaseUrl });
  log('Engine ready');

  // 3. A failed run is data, not an exception.
  const result = await ep.run({ idf: writeIdf(doc), epw: epwText });
  log(result.success ? 'Simulation finished' : `Failed: ${result.fatalError}`);
  ep.dispose();
  return result;
}
// --8<-- [end:example]
