// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
//
// `document` is declared even though DOM's global of that name would satisfy the compiler.
// That is the hazard: the page destructured it out of parseIdf in an earlier fence, and
// without this declaration the example type-checks against a browser Document and proves
// nothing about idfkit at all.
import type { IdfDocument, SchemaBundle } from '@idfkit/core';
declare const bundle: SchemaBundle;
declare const document: IdfDocument;

// --8<-- [start:example]
import { validateDocument } from '@idfkit/core';

const target = await bundle.load('26.1.0');
const result = validateDocument(document, { schema: target });

for (const finding of result.warnings) {
  if (finding.code === 'W002') {
    console.warn(`${finding.objType} '${finding.objName}' does not exist in 26.1`);
  }
}
// --8<-- [end:example]
