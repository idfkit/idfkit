// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const surface: IdfObject;

// --8<-- [start:example]
surface.extensible.push({
  vertex_x_coordinate: 0,
  vertex_y_coordinate: 0,
  vertex_z_coordinate: 3,
});

surface.extensible.splice(2, 1); // drop the third vertex
surface.extensible[0].vertex_z_coordinate = 3.5;
// --8<-- [end:example]
