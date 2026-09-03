// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { WeatherStation } from '@idfkit/weather';
import { fetchWeatherFiles } from '@idfkit/weather';
declare const station: WeatherStation;

// --8<-- [start:example]
try {
  const files = await fetchWeatherFiles(station);
} catch (error) {
  console.error(`Download failed: ${String(error)}`);
}
// --8<-- [end:example]
