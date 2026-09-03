// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;

// --8<-- [start:example]
// Every zone
for (const zone of doc.all('Zone')) {
  console.log(`Zone: ${zone.name}`);
}

// One zone by name
const office = doc.require('Zone', 'Office');
console.log(`Origin: (${office.x_origin}, ${office.y_origin}, ${office.z_origin})`);
// --8<-- [end:example]
