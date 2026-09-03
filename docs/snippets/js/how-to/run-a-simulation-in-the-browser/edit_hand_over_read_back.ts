// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
declare const epwText: string;
declare const idfText: string;

// --8<-- [start:example]
import { parseIdf, writeIdf, SchemaBundle, httpSource } from '@idfkit/core';
import { createEnergyPlus } from '@idfkit/engine';
import type { TypeMap } from '@idfkit/types-v26-1';

// 1. Edit the model here.
const schema = await new SchemaBundle(httpSource('/schemas/')).load('26.1.0');
const { document } = parseIdf<TypeMap>(idfText, schema);
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
// --8<-- [end:example]
