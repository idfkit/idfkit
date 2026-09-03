// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument } from '@idfkit/core';
declare const document: IdfDocument;

// --8<-- [start:example]
const name = document.require('Schedule:File', 'Occupancy').get('file_name');
// --8<-- [end:example]
