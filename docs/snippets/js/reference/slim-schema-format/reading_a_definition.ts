// --8<-- [start:example]
import { localBundle } from '@idfkit/schemas/node';

const schema = await localBundle().load('26.1.0');

schema.resolve('ZONE'); // 'Zone'. IDF type names are case-insensitive
schema.get('Zone'); // the SlimType
schema.field('Zone', 'x_origin'); // { t: 'n', u: 'm', d: 0 }
// --8<-- [end:example]
