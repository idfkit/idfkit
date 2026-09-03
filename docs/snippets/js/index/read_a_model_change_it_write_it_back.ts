// --8<-- [start:example]
import { loadIdf, saveIdf } from '@idfkit/core/node';
import type { TypeMap } from '@idfkit/types-v26-1';

// Load an existing IDF file
const doc = await loadIdf<TypeMap>('in.idf');

// Query objects with O(1) lookups
const zone = doc.require('Zone', 'Office');
console.log(zone.x_origin, zone.y_origin);

// Modify a field
zone.x_origin = 10;

// See what references the zone
for (const obj of doc.references.referencingObjects('Office')) {
  console.log(obj.typeName, obj.name);
}

// Write back to IDF (or epJSON)
await saveIdf(doc, 'out.idf');
// --8<-- [end:example]
