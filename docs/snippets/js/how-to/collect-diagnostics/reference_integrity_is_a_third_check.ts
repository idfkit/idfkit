// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
//
// `document` is declared even though DOM's global of that name would satisfy the compiler.
// That is the hazard: the page destructured it out of parseIdf in an earlier fence, and
// without this declaration the example type-checks against a browser Document and proves
// nothing about idfkit at all.
import type { IdfDocument } from '@idfkit/core';
declare const document: IdfDocument;

// --8<-- [start:example]
for (const edge of document.danglingReferences()) {
  console.warn(`${edge.field} points at missing "${edge.target}"`);
}
// --8<-- [end:example]
