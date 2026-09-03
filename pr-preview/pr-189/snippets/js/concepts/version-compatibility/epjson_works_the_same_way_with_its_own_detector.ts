// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
declare const text: string;

// --8<-- [start:example]
import { getEpJsonVersion, parseEpJson } from 'idfkit';
import { loadEpJson, schemaFor } from 'idfkit/node';

const doc = await loadEpJson('whatever.epJSON');

// Or, from text you already have:
const { document } = parseEpJson(text, await schemaFor(getEpJsonVersion(text)));
// --8<-- [end:example]
