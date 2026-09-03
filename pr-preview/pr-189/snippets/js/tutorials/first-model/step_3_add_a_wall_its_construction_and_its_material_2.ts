// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const wall: IdfObject;

// --8<-- [start:example]
wall.extensible.push(
  { vertex_x_coordinate: 0, vertex_y_coordinate: 0, vertex_z_coordinate: 2.7 },
  { vertex_x_coordinate: 0, vertex_y_coordinate: 0, vertex_z_coordinate: 0 },
  { vertex_x_coordinate: 5, vertex_y_coordinate: 0, vertex_z_coordinate: 0 },
  { vertex_x_coordinate: 5, vertex_y_coordinate: 0, vertex_z_coordinate: 2.7 }
);

console.log(wall.extensible.length);
// --8<-- [end:example]
