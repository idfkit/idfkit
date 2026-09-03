// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const doc: IdfDocument;

// --8<-- [start:example]
import { saveIdf } from '@idfkit/core/node';

await saveIdf(doc, 'office.idf');
// --8<-- [end:example]
