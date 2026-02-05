"""Parser for EnergyPlus .err files.

Parses the structured error/warning output from EnergyPlus simulations
into categorized, queryable dataclasses.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Regex patterns for severity markers in .err files
_FATAL_RE = re.compile(r"^\s*\*\*\s+Fatal\s+\*\*")
_SEVERE_RE = re.compile(r"^\s*\*\*\s+Severe\s+\*\*")
_WARNING_RE = re.compile(r"^\s*\*\*\s+Warning\s+\*\*")
_INFO_RE = re.compile(r"^\s*\*\*\s+~~~\s+\*\*")

# Markers for simulation status
_WARMUP_CONVERGED_RE = re.compile(r"Warmup Converged", re.IGNORECASE)
_SIM_COMPLETE_RE = re.compile(r"EnergyPlus Completed Successfully", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class ErrorMessage:
    """A single error/warning message from EnergyPlus.

    Attributes:
        severity: One of "Fatal", "Severe", "Warning", "Info".
        message: The primary message text.
        details: Additional continuation lines (``** ~~~   **`` lines).
    """

    severity: str
    message: str
    details: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ErrorReport:
    """Parsed contents of an EnergyPlus .err file.

    Attributes:
        fatal: Fatal error messages.
        severe: Severe error messages.
        warnings: Warning messages.
        info: Informational messages.
        warmup_converged: Whether warmup convergence was reported.
        simulation_complete: Whether the simulation completed successfully.
        raw_text: The original unparsed file text.
    """

    fatal: tuple[ErrorMessage, ...]
    severe: tuple[ErrorMessage, ...]
    warnings: tuple[ErrorMessage, ...]
    info: tuple[ErrorMessage, ...]
    warmup_converged: bool
    simulation_complete: bool
    raw_text: str

    @property
    def has_fatal(self) -> bool:
        """Whether any fatal errors were found."""
        return len(self.fatal) > 0

    @property
    def has_severe(self) -> bool:
        """Whether any severe errors were found."""
        return len(self.severe) > 0

    @property
    def fatal_count(self) -> int:
        """Number of fatal errors."""
        return len(self.fatal)

    @property
    def severe_count(self) -> int:
        """Number of severe errors."""
        return len(self.severe)

    @property
    def error_count(self) -> int:
        """Total number of fatal + severe errors."""
        return len(self.fatal) + len(self.severe)

    @property
    def warning_count(self) -> int:
        """Total number of warnings."""
        return len(self.warnings)

    def summary(self) -> str:
        """Return a human-readable summary of the error report.

        Returns:
            A multi-line summary string.
        """
        lines: list[str] = []
        lines.append(
            f"Fatal: {len(self.fatal)}, Severe: {len(self.severe)}, "
            f"Warnings: {len(self.warnings)}, Info: {len(self.info)}"
        )
        if self.warmup_converged:
            lines.append("Warmup: converged")
        if self.simulation_complete:
            lines.append("Simulation: completed successfully")
        elif self.has_fatal:
            lines.append("Simulation: terminated with fatal error(s)")
        return "\n".join(lines)

    @classmethod
    def from_file(cls, path: str | Path) -> ErrorReport:
        """Parse an .err file from disk.

        Args:
            path: Path to the .err file.

        Returns:
            Parsed ErrorReport.
        """
        text = Path(path).read_text(encoding="latin-1")
        return _parse_err(text)

    @classmethod
    def from_string(cls, text: str) -> ErrorReport:
        """Parse .err content from a string.

        Args:
            text: Raw .err file contents.

        Returns:
            Parsed ErrorReport.
        """
        return _parse_err(text)


_MARKER_RE = re.compile(r"^\s*\*\*\s+\S.*?\*\*\s*(.*)")

_SEVERITY_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (_FATAL_RE, "Fatal"),
    (_SEVERE_RE, "Severe"),
    (_WARNING_RE, "Warning"),
)


def _strip_marker(line: str) -> str:
    """Strip the severity marker prefix from a line.

    Args:
        line: A line from the .err file.

    Returns:
        The message portion after the marker.
    """
    match = _MARKER_RE.match(line)
    if match:
        return match.group(1).strip()
    return line.strip()


def _detect_severity(line: str) -> str | None:
    """Detect the severity level of a line.

    Args:
        line: A line from the .err file.

    Returns:
        Severity string or None if not a severity line.
    """
    for pattern, severity in _SEVERITY_PATTERNS:
        if pattern.search(line):
            return severity
    return None


def _check_status_flags(line: str, warmup_converged: bool, simulation_complete: bool) -> tuple[bool, bool]:
    """Update simulation status flags from a line.

    Args:
        line: A line from the .err file.
        warmup_converged: Current warmup convergence state.
        simulation_complete: Current simulation completion state.

    Returns:
        Updated (warmup_converged, simulation_complete) flags.
    """
    if _WARMUP_CONVERGED_RE.search(line):
        warmup_converged = True
    if _SIM_COMPLETE_RE.search(line):
        simulation_complete = True
    return warmup_converged, simulation_complete


def _append_message(
    buckets: dict[str, list[ErrorMessage]],
    severity: str,
    message: str,
    details: list[str],
) -> None:
    """Create an ErrorMessage and append it to the appropriate bucket.

    Args:
        buckets: Mapping of severity to message lists.
        severity: Severity level key.
        message: Primary message text.
        details: Continuation line details.
    """
    msg = ErrorMessage(severity=severity, message=message, details=tuple(details))
    buckets[severity].append(msg)


def _parse_err(text: str) -> ErrorReport:
    """Parse raw .err file text into an ErrorReport.

    Uses a line-by-line state machine to group messages with their
    continuation lines.

    Args:
        text: Raw .err file contents.

    Returns:
        Parsed ErrorReport.
    """
    buckets: dict[str, list[ErrorMessage]] = {"Fatal": [], "Severe": [], "Warning": [], "Info": []}
    warmup_converged = False
    simulation_complete = False

    current_severity: str | None = None
    current_message: str | None = None
    current_details: list[str] = []

    for line in text.splitlines():
        warmup_converged, simulation_complete = _check_status_flags(line, warmup_converged, simulation_complete)

        severity = _detect_severity(line)
        if severity is not None:
            # Flush previous message
            if current_severity is not None and current_message is not None:
                _append_message(buckets, current_severity, current_message, current_details)
            current_severity = severity
            current_message = _strip_marker(line)
            current_details = []
        elif _INFO_RE.search(line):
            detail_text = _strip_marker(line)
            if current_severity is not None and detail_text:
                current_details.append(detail_text)
            elif detail_text:
                buckets["Info"].append(ErrorMessage(severity="Info", message=detail_text, details=()))

    # Flush the last message
    if current_severity is not None and current_message is not None:
        _append_message(buckets, current_severity, current_message, current_details)

    return ErrorReport(
        fatal=tuple(buckets["Fatal"]),
        severe=tuple(buckets["Severe"]),
        warnings=tuple(buckets["Warning"]),
        info=tuple(buckets["Info"]),
        warmup_converged=warmup_converged,
        simulation_complete=simulation_complete,
        raw_text=text,
    )
