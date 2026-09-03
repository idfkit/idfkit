// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
declare const file: File;

// --8<-- [start:example]
const buffer = await file.arrayBuffer();
const text = new TextDecoder('latin1').decode(buffer);
// --8<-- [end:example]
