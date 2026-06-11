from __future__ import annotations

from pathlib import Path

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
input_paths: list[str] = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import load_idf, load_epjson

doc = load_idf("building.idf")
doc = load_epjson("building.epJSON")
print(doc.version)  # e.g. (25, 2, 0)
print(len(doc), "objects")
# --8<-- [end:quickstart]


# --8<-- [start:strict-mode]
doc = load_idf("building.idf")  # strict=True by default
zone = doc["Zone"]["Office"]
zone.x_origin  # OK
zone.x_orign  # raises InvalidFieldError
# --8<-- [end:strict-mode]


# --8<-- [start:strict-false]
doc = load_idf("legacy.idf", strict=False)
zone.x_orign  # returns None, no error
# --8<-- [end:strict-false]


# --8<-- [start:strict-parsing]
from idfkit.exceptions import IDFParseError

try:
    doc = load_idf("noisy.idf", strict_parsing=False)
except IDFParseError as e:
    for d in e.diagnostics:
        print(d.line, d.column, d.message)
# --8<-- [end:strict-parsing]


# --8<-- [start:version]
from idfkit import get_idf_version

version = get_idf_version("building.idf")  # (25, 2, 0)
# --8<-- [end:version]


# --8<-- [start:version-override]
doc = load_idf("legacy.idf", version=(9, 6, 0))
# --8<-- [end:version-override]


# --8<-- [start:preserve]
from idfkit import load_idf, write_idf

doc = load_idf("building.idf", preserve_formatting=True)
doc["Zone"]["Office"].x_origin = 10.0
write_idf(doc, "modified.idf")  # unmodified objects render byte-identical
# --8<-- [end:preserve]


# --8<-- [start:convert]
from idfkit import load_idf, write_epjson

doc = load_idf("building.idf")
write_epjson(doc, "building.epJSON")
# --8<-- [end:convert]


# --8<-- [start:convert-explicit]
from idfkit.writers import convert_idf_to_epjson, convert_epjson_to_idf

convert_idf_to_epjson("building.idf", "building.epJSON")
convert_epjson_to_idf("building.epJSON", "building.idf")
# --8<-- [end:convert-explicit]


# --8<-- [start:bulk]
from idfkit import IDFParser
from idfkit.schema import get_schema

schema = get_schema((25, 2, 0))
docs = [IDFParser(Path(p), schema=schema).parse() for p in input_paths]
# --8<-- [end:bulk]


# --8<-- [start:mistake-strict-good]
doc = load_idf("building.idf")  # strict=True
zone.x_origin = 10.0
# --8<-- [end:mistake-strict-good]


# --8<-- [start:mistake-version-good]
from idfkit import migrate, load_idf, write_idf

legacy = load_idf("legacy.idf")
report = migrate(legacy, target_version=(25, 2, 0))
if report.success and report.migrated_model is not None:
    doc = report.migrated_model
    write_idf(doc, "legacy_v25.idf")
# --8<-- [end:mistake-version-good]


# --8<-- [start:mistake-preserve-good]
doc = load_idf("building.idf", preserve_formatting=True)
write_idf(doc, "out.idf")  # byte-identical
# --8<-- [end:mistake-preserve-good]
