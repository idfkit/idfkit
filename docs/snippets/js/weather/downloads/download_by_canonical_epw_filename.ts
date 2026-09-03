// Preamble, not shown on the page: the values this example assumes it already
// has, each with the type the page's earlier steps would have given it.
import type { StationIndex } from '@idfkit/weather';
declare const index: StationIndex;

// --8<-- [start:example]
import { fetchEpwByFilename } from 'idfkit/weather';

const epw = await fetchEpwByFilename(
  'USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023',
  index
);
// --8<-- [end:example]
