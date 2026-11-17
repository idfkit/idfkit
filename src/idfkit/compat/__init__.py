"""EnergyPlus version-compatibility linter for Python files using idfkit.

This module provides a reusable API and CLI for *linting* Python source files
that use idfkit, detecting cross-version breakage caused by EnergyPlus schema
changes (e.g. object-type renames, enumerated-choice additions/removals).

Quick start -- library API::

    from idfkit.compat import check_compatibility

    source = open("my_script.py").read()
    diagnostics = check_compatibility(
        source,
        filename="my_script.py",
        targets=[(24, 2, 0), (25, 1, 0)],
    )
    for d in diagnostics:
        print(d)

Quick start -- CLI::

    idfkit check src/ --targets all
    idfkit check src/ --since 9.4 --json
    idfkit check my_script.py --from 24.2 --to 25.1 --sarif
    idfkit check            # settings from [tool.idfkit.check] in pyproject.toml

A line is silenced with ``# idfkit: ignore[C001]``; a lookup on ``as_version(doc, ...)`` or inside
``if doc.version >= (9, 4, 0):`` is checked only against the releases it can run on.
"""

from __future__ import annotations

from ._checker import check_compatibility, resolve_version
from ._diff import SchemaDiff, SchemaIndex, build_schema_index, diff_schemas
from ._extract import extract_literals
from ._models import DEFAULT_RULES, DIAGNOSTIC_CODES, CompatSeverity, Diagnostic, ExtractedLiteral, LiteralKind
from ._sarif import format_sarif

__all__ = [
    "DEFAULT_RULES",
    "DIAGNOSTIC_CODES",
    "CompatSeverity",
    "Diagnostic",
    "ExtractedLiteral",
    "LiteralKind",
    "SchemaDiff",
    "SchemaIndex",
    "build_schema_index",
    "check_compatibility",
    "diff_schemas",
    "extract_literals",
    "format_sarif",
    "resolve_version",
]
