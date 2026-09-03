// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { WeatherStation } from '@idfkit/weather';
declare const station: WeatherStation;

// --8<-- [start:example]
import { fetchWeatherFiles } from 'idfkit/weather';
import { saveWeatherFiles } from '@idfkit/weather/node';

const files = await fetchWeatherFiles(station);
const saved = await saveWeatherFiles(files, './weather');
console.log(saved.epw);
// --8<-- [end:example]
