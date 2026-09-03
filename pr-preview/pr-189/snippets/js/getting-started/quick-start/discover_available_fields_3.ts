// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument } from '@idfkit/core';
import type { TypeMap } from '@idfkit/types-v26-1';
declare const doc: IdfDocument<TypeMap>;

// --8<-- [start:example]
// @ts-expect-error x_orgin is a typo for x_origin
doc.add('Zone', 'Office', { x_orgin: 0 }); // caught by the compiler, before it runs

// Field names are checked against the schema for the version in the type map, so
// there is nothing to switch off and nothing to pay at run time.
doc.add('Zone', 'Office', { x_origin: 0 });
// --8<-- [end:example]
