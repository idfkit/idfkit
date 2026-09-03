// --8<-- [start:example]
import { loadIdf } from '@idfkit/core/node';
import type { TypeMap } from '@idfkit/types-v26-1';

const doc = await loadIdf<TypeMap>('model.idf');

doc.all('Zone'); // completes among 858 type names
// @ts-expect-error celing_height is a typo for ceiling_height
doc.add('Zone', 'Z1', { celing_height: 3 }); // compile error: typo
// @ts-expect-error the schema's choices are NoSun and SunExposed
doc.add('BuildingSurface:Detailed', 'S1', { sun_exposure: 'Sunny' }); // compile error
// --8<-- [end:example]
