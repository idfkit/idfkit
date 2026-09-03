// --8<-- [start:example]
import { schemas } from '@idfkit/core/node';

const bundle = schemas();
(await bundle.versions()).length; // 17
await bundle.latest(); // '26.1.0'
// --8<-- [end:example]
