// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const doc: IdfDocument;

// --8<-- [start:example]
doc.schema.get('BuildingSurface:Detailed')?.x?.fields;
// ['vertex_x_coordinate', 'vertex_y_coordinate', 'vertex_z_coordinate']
doc.schema.get('BuildingSurface:Detailed')?.x?.key;
// 'vertices'
// --8<-- [end:example]
