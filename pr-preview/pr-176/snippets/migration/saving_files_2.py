from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
doc.saveas("out.idf")  # save and update doc.filepath
doc.savecopy("backup.idf")  # save without changing doc.filepath
doc.save()  # save to current doc.filepath
# --8<-- [end:example]
