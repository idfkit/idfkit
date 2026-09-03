// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
declare const schema: Schema;
declare const text: string;

// --8<-- [start:example]
import { IdfParseError, parseIdf } from '@idfkit/core';

try {
  parseIdf(text, schema);
} catch (error) {
  if (error instanceof IdfParseError) {
    console.error(`line ${error.line} (${error.typeName ?? 'unknown type'}): ${error.message}`);
  }
  throw error;
}
// --8<-- [end:example]
