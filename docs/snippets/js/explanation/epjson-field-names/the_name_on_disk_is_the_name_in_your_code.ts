// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;

// --8<-- [start:example]
const zone = doc.require('Zone', 'SPACE1-1');
const surface = doc.require('BuildingSurface:Detailed', 'WALL-1');

zone.ceiling_height;
surface.outside_boundary_condition;
// --8<-- [end:example]
