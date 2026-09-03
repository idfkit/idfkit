// --8<-- [start:example]
import { localBundle } from '@idfkit/schemas/node';

const bundle = localBundle();
const older = await bundle.load('9.4.0');
const newer = await bundle.load('26.1.0');

const delta = newer.changedFrom(older);

delta.added;   // type names introduced since 9.4
delta.removed; // type names that no longer exist
delta.changed; // type names whose definition differs
// --8<-- [end:example]
