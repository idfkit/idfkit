from __future__ import annotations

from idfkit.simulation import SQLResult

sql: SQLResult | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
environments = sql.get_environments()

for env in environments:
    print(f"{env.index}: {env.name} (type={env.environment_type})")
# --8<-- [end:example]
