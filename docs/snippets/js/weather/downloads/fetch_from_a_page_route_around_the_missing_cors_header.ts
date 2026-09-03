// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { WeatherStation } from '@idfkit/weather';
import { fetchEpw } from '@idfkit/weather';
declare const station: WeatherStation;

// --8<-- [start:example]
const epw = await fetchEpw(station, {
  rewriteUrl: (url) => `https://your-proxy.example/?url=${encodeURIComponent(url)}`,
});
// --8<-- [end:example]
