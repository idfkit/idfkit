"""Helpers shared by the Mermaid-family renderers (``mermaid`` and ``overview``)."""

from __future__ import annotations


def mermaid_escape(text: str) -> str:
    """Escape text for a quoted Mermaid label.

    ``|`` is escaped too: it delimits edge labels (``-->|label|``), so a raw pipe
    in a node name would otherwise break the flowchart. Mermaid honors the HTML
    numeric entity in labels.
    """
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("|", "&#124;")
    )
