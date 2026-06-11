from __future__ import annotations

from idfkit.simulation import TimeSeriesResult

ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
df = ts.to_dataframe()
print(df.head())
#                              Zone Mean Air Temperature
# timestamp
# 2017-01-01 01:00:00                               21.2
# 2017-01-01 02:00:00                               21.1
# ...
# --8<-- [end:example]
