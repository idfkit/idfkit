// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { ExtensibleGroup } from '@idfkit/core';
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const surface: IdfObject;
declare const vertices: ExtensibleGroup[];

// --8<-- [start:example]
surface.extensible.splice(0, surface.extensible.length, ...vertices);
// --8<-- [end:example]
