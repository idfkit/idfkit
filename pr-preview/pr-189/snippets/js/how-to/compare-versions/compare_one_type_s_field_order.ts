// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const newer: Schema;
declare const older: Schema;

// --8<-- [start:example]
const typeName = 'Coil:Cooling:DX:SingleSpeed';

const before = older.require(typeName).f;
const after = newer.require(typeName).f;

const gained = after.filter((field) => !before.includes(field));
const lost = before.filter((field) => !after.includes(field));
// --8<-- [end:example]
