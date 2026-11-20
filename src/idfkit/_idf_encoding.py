"""The codec a document's IDF text is written back in.

A document read from an IDF file remembers the codec it was read in, so that saving it writes the
bytes it was read from. A UTF-8 file that began with a byte-order mark is remembered as
``utf-8-sig``. The mark belongs to that file's text, so only a lossless rewrite of the text puts it
back: regenerated text, and every file idfkit writes for an EnergyPlus program, is written without
it, as the Transition programs report a mark on the first line as a severe error.
"""

from __future__ import annotations

#: The codec of a document not read from an IDF file, which is what EnergyPlus writes.
DEFAULT_IDF_ENCODING = "latin-1"


def source_encoding(doc: object, *, bom: bool) -> str:
    """The codec *doc*'s IDF file was read in, or latin-1 for a document not read from one.

    Args:
        doc: The document.
        bom: Whether a byte-order mark the source file had is kept. ``False`` writes its UTF-8
            without the mark.
    """
    # Read with a default: a document pickled before the slot existed has no value in it.
    encoding: str = getattr(doc, "_source_encoding", None) or DEFAULT_IDF_ENCODING
    if not bom and encoding == "utf-8-sig":
        return "utf-8"
    return encoding
