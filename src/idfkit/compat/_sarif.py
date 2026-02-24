"""SARIF 2.1.0 output formatter for compatibility lint diagnostics.

Produces `Static Analysis Results Interchange Format`__ (SARIF) output
that can be consumed by GitHub Code Scanning, VS Code SARIF Viewer,
and other SARIF-aware tools.

__ https://sarifweb.azurewebsites.net/
"""

from __future__ import annotations

import json
from typing import Any

from ._models import DIAGNOSTIC_CODES, CompatSeverity, Diagnostic

_SARIF_VERSION = "2.1.0"
_SARIF_SCHEMA = (
    "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json"
)

_SEVERITY_MAP: dict[CompatSeverity, str] = {
    CompatSeverity.ERROR: "error",
    CompatSeverity.WARNING: "warning",
}


def _build_rules() -> list[dict[str, Any]]:
    """Build the ``rules`` array for the SARIF ``tool.driver`` block."""
    rules: list[dict[str, Any]] = []
    for code, description in DIAGNOSTIC_CODES.items():
        rules.append({
            "id": code,
            "shortDescription": {"text": description},
            "defaultConfiguration": {"level": "warning"},
        })
    return rules


def _diagnostic_to_result(diag: Diagnostic) -> dict[str, Any]:
    """Convert a single :class:`Diagnostic` to a SARIF ``result`` object."""
    result: dict[str, Any] = {
        "ruleId": diag.code,
        "level": _SEVERITY_MAP.get(diag.severity, "warning"),
        "message": {"text": diag.message},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {"uri": diag.filename},
                    "region": {
                        "startLine": diag.line,
                        "startColumn": diag.col + 1,  # SARIF columns are 1-based
                        "endColumn": diag.end_col + 1,
                    },
                },
            },
        ],
        "properties": {
            "from_version": diag.from_version,
            "to_version": diag.to_version,
        },
    }
    if diag.suggested_fix is not None:
        result["fixes"] = [
            {
                "description": {"text": diag.suggested_fix},
            },
        ]
    return result


def format_sarif(diagnostics: list[Diagnostic], *, tool_version: str = "0.1.0") -> str:
    """Format a list of diagnostics as a SARIF 2.1.0 JSON string.

    Args:
        diagnostics: Lint diagnostics to format.
        tool_version: Version string for the tool metadata.

    Returns:
        A JSON string conforming to the SARIF 2.1.0 schema.
    """
    sarif: dict[str, Any] = {
        "$schema": _SARIF_SCHEMA,
        "version": _SARIF_VERSION,
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "idfkit",
                        "informationUri": "https://github.com/samuelduchesne/idfkit",
                        "version": tool_version,
                        "rules": _build_rules(),
                    },
                },
                "results": [_diagnostic_to_result(d) for d in diagnostics],
            },
        ],
    }
    return json.dumps(sarif, indent=2)
