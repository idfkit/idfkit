// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const doc: IdfDocument;

// --8<-- [start:example]
doc.add('Material', 'Brick 100mm', {
  roughness: 'MediumRough',
  thickness: 0.1,
  conductivity: 0.89,
  density: 1920,
  specific_heat: 790,
});

doc.add('Construction', 'Exterior Wall', {
  outside_layer: 'Brick 100mm',
});

const wall = doc.add('BuildingSurface:Detailed', 'North Wall', {
  surface_type: 'Wall',
  construction_name: 'Exterior Wall',
  zone_name: 'Open Office',
  outside_boundary_condition: 'Outdoors',
  sun_exposure: 'SunExposed',
  wind_exposure: 'WindExposed',
});
// --8<-- [end:example]
