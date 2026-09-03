// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;

// --8<-- [start:example]
import { writeIdf } from '@idfkit/core';
import { saveEpJson, saveIdf } from '@idfkit/core/node';

// Write IDF
await saveIdf(doc, 'output.idf');

// Or epJSON
await saveEpJson(doc, 'output.epJSON');

// Or take the text and decide where it goes yourself
const idfText = writeIdf(doc);
// --8<-- [end:example]
