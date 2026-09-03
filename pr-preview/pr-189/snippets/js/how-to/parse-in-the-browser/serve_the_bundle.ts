// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
declare const idfText: string;

// --8<-- [start:example]
import { parseIdf, SchemaBundle, httpSource } from '@idfkit/core';

const bundle = new SchemaBundle(httpSource('/schemas/'));
const schema = await bundle.load('26.1.0');

const { document } = parseIdf(idfText, schema);
// --8<-- [end:example]
