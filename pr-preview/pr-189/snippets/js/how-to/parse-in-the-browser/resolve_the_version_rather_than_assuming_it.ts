// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const bundle: SchemaBundle;
declare const idfText: string;

// --8<-- [start:example]
import { getIdfVersion, parseIdf, resolveVersion } from '@idfkit/core';

const detected = getIdfVersion(idfText);
if (detected === undefined) throw new Error('This file has no Version object');

const resolved = resolveVersion(detected, await bundle.versions());
if (resolved === undefined) throw new Error(`EnergyPlus ${detected} is not in the bundle`);

const schema = await bundle.load(resolved);
const { document } = parseIdf(idfText, schema);
// --8<-- [end:example]
