// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import { loadIdf } from '@idfkit/core/node';

// --8<-- [start:example]
const doc = await loadIdf('fragment.idf', { version: '26.1.0' });
// --8<-- [end:example]
