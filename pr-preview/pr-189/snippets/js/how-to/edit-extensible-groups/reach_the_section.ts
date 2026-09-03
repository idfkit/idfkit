// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const doc: IdfDocument;

// --8<-- [start:example]
const surface = doc.require('BuildingSurface:Detailed', 'Wall-1');

surface.extensible.length; // number of vertices
surface.extensible[0].vertex_z_coordinate;
surface.extensible[0]; // { vertex_x_coordinate: ..., ... }
// --8<-- [end:example]
