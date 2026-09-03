// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
import { parseIdf } from '@idfkit/core';
declare const schema: Schema;
declare const text: string;

// --8<-- [start:example]
const { document, diagnostics } = parseIdf(text, schema, { strict: false });

for (const d of diagnostics) {
  console.warn(`${d.line}: ${d.message}`);
}
// --8<-- [end:example]
