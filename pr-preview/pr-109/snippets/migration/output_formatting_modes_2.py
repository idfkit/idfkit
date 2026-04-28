from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import write_idf

write_idf(doc, "out.idf", output_type="nocomment")  # no field comments
write_idf(doc, "out.idf", output_type="compressed")  # single-line objects
write_idf(doc, "out.idf", output_type="standard")  # default, with comments
# --8<-- [end:example]
