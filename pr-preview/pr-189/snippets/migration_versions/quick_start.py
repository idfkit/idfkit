from __future__ import annotations

from idfkit import IDFDocument, MigrationReport

model: IDFDocument = ...  # type: ignore[assignment]
report: MigrationReport = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf, migrate
from idfkit.simulation import find_energyplus

# Load an older IDF (e.g. v22.1.0) and migrate to the installed EnergyPlus.
model = load_idf("old_building.idf")
config = find_energyplus()

report = migrate(model, target_version=config.version, energyplus=config)

print(report.summary())

migrated = report.migrated_model
if migrated is not None:
    print(f"Migrated model version: {migrated.version}")
# --8<-- [end:example]
