// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import { writeIdf } from '@idfkit/core';
declare const csvText: string;
declare const epwText: string;
import type { IdfDocument } from '@idfkit/core';
import type { EnergyPlus } from '@idfkit/engine';
declare const ep: EnergyPlus;
declare const document: IdfDocument;

// --8<-- [start:example]
const result = await ep.run({
  idf: writeIdf(document),
  epw: epwText,
  files: { 'occupancy.csv': csvText },
});
// --8<-- [end:example]
