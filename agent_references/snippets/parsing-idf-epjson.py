from __future__ import annotations

from pathlib import Path

from idfkit import IDFObject
from idfkit.document import AnyIDFDocument

doc: AnyIDFDocument = ...  # type: ignore[assignment]
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
# --8<-- [end:strict-mode]


# --8<-- [start:strict-false]
doc = load_idf("legacy.idf", strict=False)
zone = doc["Zone"]["Office"]
# --8<-- [end:strict-false]


# --8<-- [start:strict-parsing]
from idfkit.exceptions import IDFParseError

try:
    doc = load_idf("noisy.idf", strict_parsing=False)
except IDFParseError as e:
    for d in e.diagnostics:
        print(d.line, d.column, d.message)
# --8<-- [end:strict-parsing]


# --8<-- [start:blank-fields]
# Zone, Office, 0, 0, 0, 0, , , ;  -- type, multiplier and ceiling height left blank
zone = doc["Zone"]["Office"]
zone.ceiling_height  # None, exactly as if the semicolon had come earlier
"ceiling_height" in zone.data  # False: a blank field is not stored
if zone.ceiling_height is None:
    zone.ceiling_height = "Autocalculate"
# --8<-- [end:blank-fields]


# --8<-- [start:version]
from idfkit import get_idf_version

version = get_idf_version("building.idf")  # (25, 2, 0)
# --8<-- [end:version]


# --8<-- [start:version-override]
doc = load_idf("legacy.idf", version=(9, 6, 0))
# --8<-- [end:version-override]


# --8<-- [start:stated-release]
from idfkit import load_epjson, load_idf, load_idf_with_diagnostics
from idfkit.versioned import IDFDocumentV9_4, IDFDocumentV26_1

model = load_idf("model.idf")  # AnyIDFDocument: what every supported release has
legacy = load_idf("legacy.idf", as_type=IDFDocumentV9_4)  # IDFDocumentV9_4; TypeError unless 9.4
legacy["People"]["Office"].zone_or_zonelist_name = "Office"  # the 9.4 field name
recent = load_epjson("recent.epJSON", since="9.6")  # 9.6 or later: IDFDocumentSince9_6
recent["Space"].first()  # every release from 9.6 on has Space
older = load_idf("older.idf", since="25.2", before="26.2")  # 25.2 or 26.1
result = load_idf_with_diagnostics("hand_edited.idf", as_type=IDFDocumentV26_1)
print(result.document["Zone"].first(), result.diagnostics)  # result.document is IDFDocumentV26_1
# --8<-- [end:stated-release]


# --8<-- [start:preserve]
from idfkit import load_idf, save_idf

doc = load_idf("building.idf", preserve_formatting=True)
doc["Zone"]["Office"].x_origin = 10.0
save_idf(doc, "modified.idf")  # unmodified objects render byte-identical
# --8<-- [end:preserve]


# --8<-- [start:convert]
from idfkit import load_idf, save_epjson

doc = load_idf("building.idf")
save_epjson(doc, "building.epJSON")
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
from idfkit import migrate, load_idf, save_idf

legacy = load_idf("legacy.idf")
report = migrate(legacy, target_version=(25, 2, 0))
if report.success and report.migrated_model is not None:
    doc = report.migrated_model
    save_idf(doc, "legacy_v25.idf")
# --8<-- [end:mistake-version-good]


# --8<-- [start:mistake-blank-good]
if zone.multiplier is None:  # blank or never written: both read as None
    ...
# --8<-- [end:mistake-blank-good]


# --8<-- [start:mistake-preserve-good]
doc = load_idf("building.idf", preserve_formatting=True)
save_idf(doc, "out.idf")  # byte-identical
# --8<-- [end:mistake-preserve-good]
