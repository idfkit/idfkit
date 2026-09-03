// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;
declare const surface: IdfObject & TypeMap['BuildingSurface:Detailed'];

// --8<-- [start:example]
const zone = doc.require('Zone', 'SPACE1-1');
zone.name = 'Open Office';
surface.zone_name; // 'Open Office'
// --8<-- [end:example]
