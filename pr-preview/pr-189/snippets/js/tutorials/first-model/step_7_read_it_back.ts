// --8<-- [start:example]
import { loadIdf } from '@idfkit/core/node';
import type { TypeMap } from '@idfkit/types-v26-1';

const reread = await loadIdf<TypeMap>('office.idf');

console.log(reread.version);

for (const z of reread.all('Zone')) {
  console.log(`${z.name}: ceiling ${z.ceiling_height} m`);
}

const wallAgain = reread.require('BuildingSurface:Detailed', 'North Wall');
console.log(wallAgain.extensible.length);
console.log(wallAgain.extensible[0].vertex_z_coordinate);
// --8<-- [end:example]
