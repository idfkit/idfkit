// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import { SchemaBundle } from '@idfkit/core';
import { httpSource } from '@idfkit/core';
import { parseIdf } from '@idfkit/core';
declare const idfText: string;

// --8<-- [start:example]
const bundle = new SchemaBundle(httpSource('/schemas/'));
const schema = await bundle.load('26.1.0'); // the async part, once
const { document } = parseIdf(idfText, schema); // sync from here on
// --8<-- [end:example]
