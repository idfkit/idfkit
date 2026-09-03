// --8<-- [start:example]
import { loadIdf } from 'idfkit/node';

const doc = await loadIdf('whatever.idf');
doc.version; // '9.0.1', say
// --8<-- [end:example]
