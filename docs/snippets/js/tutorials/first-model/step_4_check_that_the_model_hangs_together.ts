// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const doc: IdfDocument;

// --8<-- [start:example]
import { validateDocument } from '@idfkit/core';

const result = validateDocument(doc);

console.log(result.errors.length);
// --8<-- [end:example]
