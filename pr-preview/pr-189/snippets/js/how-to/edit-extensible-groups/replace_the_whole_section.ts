// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfObject } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const surface: IdfObject & TypeMap['BuildingSurface:Detailed'];

// --8<-- [start:example]
surface.vertices = [
  { vertex_x_coordinate: 0, vertex_y_coordinate: 0, vertex_z_coordinate: 3 },
  { vertex_x_coordinate: 0, vertex_y_coordinate: 0, vertex_z_coordinate: 0 },
  { vertex_x_coordinate: 5, vertex_y_coordinate: 0, vertex_z_coordinate: 0 },
];
// --8<-- [end:example]
