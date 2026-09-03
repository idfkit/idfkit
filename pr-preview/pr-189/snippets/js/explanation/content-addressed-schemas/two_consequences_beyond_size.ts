// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const bundle: SchemaBundle;

// --8<-- [start:example]
const delta = (await bundle.load('26.1.0')).changedFrom(await bundle.load('9.4.0'));
// { added: [...], removed: [...], changed: [...] }
// --8<-- [end:example]
