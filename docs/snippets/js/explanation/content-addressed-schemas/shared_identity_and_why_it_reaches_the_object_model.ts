// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const bundle: SchemaBundle;

// --8<-- [start:example]
const a = await bundle.load('25.2.0');
const b = await bundle.load('26.1.0');
a.get('Zone') === b.get('Zone'); // true
// --8<-- [end:example]
