// --8<-- [start:example]
import { loadBundledIndex } from '@idfkit/weather/node';
import { fetchWeatherFiles } from 'idfkit/weather';

const index = await loadBundledIndex();
const [best] = index.search('chicago ohare');

const files = await fetchWeatherFiles(best.station);
console.log(files.epw.length, files.ddy?.length);
// --8<-- [end:example]
