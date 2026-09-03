// --8<-- [start:example]
// worker.ts
import { parseIdf, writeIdf, SchemaBundle, httpSource } from '@idfkit/core';

const bundle = new SchemaBundle(httpSource('/schemas/'));

self.onmessage = async ({ data }) => {
  const schema = await bundle.load(data.version);
  const { document } = parseIdf(data.text, schema);
  self.postMessage({ objects: document.size, idf: writeIdf(document) });
};
// --8<-- [end:example]
