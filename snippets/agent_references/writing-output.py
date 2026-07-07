from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import load_idf, write_idf, write_epjson

doc = load_idf("in.idf")
doc["Zone"]["Office"].x_origin = 10.0

# Persist
write_idf(doc, "out.idf")
write_epjson(doc, "out.epJSON")

# Or get a string back (filepath=None)
idf_text = write_idf(doc)
# --8<-- [end:quickstart]


# --8<-- [start:output-type]
write_idf(doc, "out.idf", output_type="compressed")
# --8<-- [end:output-type]


# --8<-- [start:preserve]
from idfkit import load_idf, write_idf

doc = load_idf("building.idf", preserve_formatting=True)
doc["Zone"]["Office"].x_origin = 10.0
write_idf(doc, "building_modified.idf")
# Only the Zone "Office" block is reformatted; everything else is byte-identical.
# --8<-- [end:preserve]


# --8<-- [start:string]
text = write_idf(doc)
assert "Zone," in text
# --8<-- [end:string]


# --8<-- [start:convert]
from idfkit import load_idf, write_epjson

doc = load_idf("building.idf")
write_epjson(doc, "building.epJSON")  # IDF → epJSON
# --8<-- [end:convert]


# --8<-- [start:convert-back]
from idfkit import load_epjson, write_idf

doc = load_epjson("building.epJSON")
write_idf(doc, "building.idf")  # epJSON → IDF
# --8<-- [end:convert-back]


# --8<-- [start:batch]
from pathlib import Path
from idfkit import load_idf, write_idf

base = load_idf("base.idf")
out_dir = Path("runs")
out_dir.mkdir(exist_ok=True)

for wwr in (0.2, 0.3, 0.4, 0.5):
    doc = base.copy()
    from idfkit import set_wwr

    set_wwr(doc, wwr)
    write_idf(doc, out_dir / f"wwr_{int(wwr * 100)}.idf", output_type="compressed")
# --8<-- [end:batch]


# --8<-- [start:mistake-preserve-good]
doc = load_idf("building.idf", preserve_formatting=True)
write_idf(doc, "out.idf")
# --8<-- [end:mistake-preserve-good]


# --8<-- [start:mistake-encoding-good]
write_idf(doc, "out.idf")  # latin-1
# --8<-- [end:mistake-encoding-good]


# --8<-- [start:mistake-compressed-good]
write_idf(doc, "out.idf", output_type="standard")  # lossless (default)
# or
write_idf(doc, "out.idf", output_type="compressed", preserve_formatting=False)
# --8<-- [end:mistake-compressed-good]
