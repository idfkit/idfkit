from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import save_idf

save_idf(doc, "out.idf", output_type="nocomment")  # no field comments
save_idf(doc, "out.idf", output_type="compressed")  # single-line objects
save_idf(doc, "out.idf", output_type="standard")  # default, with comments
# --8<-- [end:example]
