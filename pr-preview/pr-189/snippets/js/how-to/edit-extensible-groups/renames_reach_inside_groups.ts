// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;

// --8<-- [start:example]
const list = doc.require('ZoneList', 'All Zones');
list.extensible.push({ zone_name: 'Open Office' });

doc.require('Zone', 'Open Office').name = 'Open Plan';
list.extensible[0].zone_name; // 'Open Plan'
// --8<-- [end:example]
