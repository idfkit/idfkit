"""Auto-generated conformance declaration.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_conformance

The value is derived from ``[tool.idfkit.conformance] level`` in ``pyproject.toml``, which is
the one place the level is authored. ``make check`` regenerates this file and diffs it, so the
declaration and the export cannot drift apart.
"""

from __future__ import annotations

from typing import Final

#: The conformance corpus level this release is checked against, as an immutable tag in
#: idfkit/idfkit-conformance. A release asserts this claim in its own checks (FR-024): the
#: corpus at this tag passes against this library, or the release does not ship.
#:
#: This is not a version number and it is not compared to one. Two installed libraries agree
#: on the formats when they declare the same level, whatever their own versions say (FR-025).
CONFORMANCE_LEVEL: Final[str] = "conformance-2026.11"
