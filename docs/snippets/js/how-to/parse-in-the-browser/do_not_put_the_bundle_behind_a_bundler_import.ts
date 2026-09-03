// --8<-- [start:example]
import { SchemaBundle, type BundleSource } from '@idfkit/core';

const source: BundleSource = {
  async read(fileName) {
    return (await import(`./schemas/${fileName}.json`)).default;
  },
};

const bundle = new SchemaBundle(source);
// --8<-- [end:example]
