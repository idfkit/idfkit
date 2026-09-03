// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
declare const text: string;

// --8<-- [start:example]
import { getIdfVersion, parseIdf, resolveVersion, SchemaBundle, httpSource } from 'idfkit';

const bundle = new SchemaBundle(httpSource('/schemas/'));

const detected = getIdfVersion(text); // '9.0', or undefined
if (detected === undefined) {
  throw new Error('No Version object; ask the user which release this is.');
}

const available = await bundle.versions();
const resolved = resolveVersion(detected, available);
if (resolved === undefined) {
  throw new Error(`EnergyPlus ${detected} is not supported. Available: ${available.join(', ')}`);
}

const { document } = parseIdf(text, await bundle.load(resolved));
// --8<-- [end:example]
