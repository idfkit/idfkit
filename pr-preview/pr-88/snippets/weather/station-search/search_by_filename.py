from __future__ import annotations

from idfkit.weather import StationIndex

index: StationIndex = ...  # type: ignore[assignment]
# --8<-- [start:example]
# EPW filenames are detected automatically by search()
results = index.search("USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023")

# Extensions are tolerated
results = index.search("GBR_London.Heathrow.AP.037720_TMYx.epw")

# Works the same as any other search query
for r in results[:3]:
    print(f"{r.station.display_name} (score={r.score:.2f})")
# --8<-- [end:example]
