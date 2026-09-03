// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;
declare const office: IdfObject & TypeMap['Zone'];

// --8<-- [start:example]
// Update a field
office.x_origin = 10.0;

// See what references this zone
for (const obj of doc.references.referencingObjects('Office')) {
  console.log(`  ${obj.typeName}: ${obj.name}`);
}
// --8<-- [end:example]
