// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;

// --8<-- [start:example]
import { describeObjectType } from '@idfkit/core';

// Every field a Zone has
const zone = describeObjectType(doc.schema, 'Zone');
for (const field of zone.fields) {
  console.log(`  ${field.name} (${field.fieldType}) ${field.units ?? ''}`);
}

// The fields a Material cannot do without
const material = describeObjectType(doc.schema, 'Material');
console.log(
  'Required:',
  material.fields.filter((field) => field.required).map((field) => field.name)
);
// --8<-- [end:example]
