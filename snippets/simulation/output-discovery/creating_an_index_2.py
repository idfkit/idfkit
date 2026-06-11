from __future__ import annotations

# --8<-- [start:example]
from idfkit.simulation import OutputVariableIndex

index = OutputVariableIndex.from_files(
    rdd_path="/path/to/eplusout.rdd",
    mdd_path="/path/to/eplusout.mdd",
)
# --8<-- [end:example]
