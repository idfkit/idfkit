// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
declare const text: string;

// --8<-- [start:example]
import { getIdfVersion, parseIdf } from 'idfkit';
import { schemaFor } from 'idfkit/node';

const schema = await schemaFor(getIdfVersion(text));
const { document } = parseIdf(text, schema);
// --8<-- [end:example]
