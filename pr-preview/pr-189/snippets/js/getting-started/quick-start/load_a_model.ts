// --8<-- [start:example]
import { loadIdf } from '@idfkit/core/node';
import type { TypeMap } from '@idfkit/types-v26-1';

// Load an existing IDF file
const doc = await loadIdf<TypeMap>('building.idf');
console.log(`Loaded ${doc.size} objects`);

// For migration-only tolerant loading of legacy or noisy files:
const legacy = await loadIdf<TypeMap>('legacy_building.idf', { strict: false });
console.log(`Tolerant load parsed ${legacy.size} objects`);
// --8<-- [end:example]
