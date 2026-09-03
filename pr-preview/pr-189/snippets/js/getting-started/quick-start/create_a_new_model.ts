// --8<-- [start:example]
import { IdfDocument } from '@idfkit/core';
import { schemas } from '@idfkit/core/node';
import type { TypeMap } from '@idfkit/types-v26-1';

// A new model against one EnergyPlus release
const schema = await schemas().load('26.1.0');
const doc = new IdfDocument<TypeMap>(schema);

// Nothing is pre-seeded: add the singletons you want
doc.add('Version', null, { version_identifier: '26.1' });
doc.add('Building', 'My Building', { north_axis: 0, terrain: 'City' });
doc.add('GlobalGeometryRules', null, {
  starting_vertex_position: 'UpperLeftCorner',
  vertex_entry_direction: 'Counterclockwise',
  coordinate_system: 'Relative',
});

// Named objects
doc.add('Zone', 'Office', { x_origin: 0, y_origin: 0, z_origin: 0 });

// And unnamed singletons
doc.add('Timestep', null, { number_of_timesteps_per_hour: 4 });
// --8<-- [end:example]
