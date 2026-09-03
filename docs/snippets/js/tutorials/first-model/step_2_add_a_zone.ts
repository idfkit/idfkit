// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;

// --8<-- [start:example]
const zone = doc.add('Zone', 'Open Office', {
  ceiling_height: 2.7,
  multiplier: 1,
});

console.log(zone.name, zone.ceiling_height);
// --8<-- [end:example]
