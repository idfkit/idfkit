// --8<-- [start:example]
import { IdfDocument } from '@idfkit/core';
import { schemas } from '@idfkit/core/node';

const schema = await schemas().load('26.1.0');
const doc = new IdfDocument(schema);

doc.add('Version', null, { version_identifier: '26.1' });

console.log(doc.version);
// --8<-- [end:example]
