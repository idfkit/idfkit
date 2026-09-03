// --8<-- [start:example]
import { compareVersions } from '@idfkit/core';

['22.1.0', '8.9.0', '9.6.0'].sort(compareVersions);
// ['8.9.0', '9.6.0', '22.1.0']
// --8<-- [end:example]
