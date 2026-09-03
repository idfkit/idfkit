// --8<-- [start:example]
import { geocode, loadStationIndex } from '@idfkit/weather';

// The index is a file you serve; nothing is bundled into the library
const index = await loadStationIndex('/stations.json.gz');

// Search by name
const [match] = index.search('chicago ohare');
console.log(match?.station.displayName);

// Nearest to an address
const [latitude, longitude] = await geocode('Willis Tower, Chicago, IL');
const [nearest] = index.nearest(latitude, longitude);
console.log(`${nearest?.station.displayName}: ${nearest?.distanceKm.toFixed(0)} km away`);
// --8<-- [end:example]
