// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { IdfDocument, IdfObject, Schema, SchemaBundle } from '@idfkit/core';
import { parseIdf } from '@idfkit/core';
declare const file: File;
declare const report: (file: File, line: number, message: string) => void;
declare const schema: Schema;
declare const text: string;

// --8<-- [start:example]
parseIdf(text, schema, {
  strict: false,
  onDiagnostic: (d) => report(file, d.line, d.message),
});
// --8<-- [end:example]
