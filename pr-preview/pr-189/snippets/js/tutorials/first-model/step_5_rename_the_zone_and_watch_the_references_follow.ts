// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;
declare const wall: IdfObject & TypeMap['BuildingSurface:Detailed'];
declare const zone: IdfObject & TypeMap['Zone'];

// --8<-- [start:example]
console.log(wall.zone_name);

doc.rename(zone, 'Open Plan');

console.log(wall.zone_name);
console.log(
  doc.references
    .referencingObjects('Open Plan')
    .map((o) => o.name)
    .join(', ')
);
// --8<-- [end:example]
