"""Resolve a variable lookup to exactly one reported series, shared by the result readers.

Internal module — not part of the public API.

[SQLResult][idfkit.simulation.parsers.sql.SQLResult],
[ESOResult][idfkit.simulation.parsers.eso.ESOResult] and
[CSVResult][idfkit.simulation.parsers.csv.CSVResult] all answer "which series is this
variable, key and frequency?" the same way: names match case-insensitively, a typo raises
[ResultLookupError][idfkit.exceptions.ResultLookupError] with the closest names, and several
matching keys or frequencies raise rather than pick one.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import TypeVar

from ...exceptions import ResultLookupError, closest_names

T = TypeVar("T")


def unique(values: Iterable[str]) -> list[str]:
    """*values* without repeats, in first-seen order."""
    return list(dict.fromkeys(values))


def listing(values: Sequence[str], limit: int = 10) -> str:
    """Up to *limit* of *values*, comma-separated, then how many were left out."""
    shown = ", ".join(v or "''" for v in values[:limit])
    if len(values) > limit:
        shown += f" and {len(values) - limit} more"
    return shown


def count(values: Sequence[str], noun: str) -> str:
    """``"3 keys"`` / ``"1 key"``."""
    return f"{len(values)} {noun}{'' if len(values) == 1 else 's'}"


def did_you_mean(close: Sequence[str]) -> str:
    """`` Did you mean 'a' or 'b'?`` for *close*, or nothing when it is empty."""
    if not close:
        return ""
    quoted = [f"'{c}'" for c in close]
    head = ", ".join(quoted[:-1])
    return f" Did you mean {head + ' or ' if head else ''}{quoted[-1]}?"


def for_key(key_value: str | None) -> str:
    """`` for key 'X'``, or nothing when no key was asked for."""
    return "" if key_value is None or key_value == "*" else f" for key '{key_value}'"


def resolve_series(
    series: Sequence[T],
    variable_name: str,
    key_value: str | None,
    frequency: str | None,
    *,
    name_of: Callable[[T], str],
    key_of: Callable[[T], str],
    frequency_of: Callable[[T], str],
    frequency_matches: Callable[[T, str], bool] | None = None,
    not_found_hint: str,
) -> T:
    """The one entry of *series* reported for *variable_name*, *key_value* and *frequency*.

    Args:
        series: Every reported series, in file order.
        variable_name: The variable asked for; matches case-insensitively.
        key_value: The key asked for, or ``None`` (or ``"*"``) for any key.
        frequency: The frequency asked for, or ``None`` for any.
        name_of: Reads a series' variable name.
        key_of: Reads a series' key.
        frequency_of: Reads a series' frequency, as the error should name it.
        frequency_matches: Whether a series is reported at the (case-folded) frequency asked
            for; defaults to comparing ``frequency_of`` case-insensitively.
        not_found_hint: A sentence appended when the variable is not reported at all.

    Raises:
        ResultLookupError: If the variable, key or frequency is not reported (naming the
            closest names and the reported keys), or several keys or frequencies match.
    """
    folded = variable_name.casefold()
    rows = [s for s in series if name_of(s).casefold() == folded]
    if not rows:
        close = closest_names(variable_name, unique(name_of(s) for s in series), n=3)
        msg = f"Variable '{variable_name}' is not in this run's output." + did_you_mean(close) + not_found_hint
        raise ResultLookupError(msg, suggestions=close)
    name = name_of(rows[0])

    if key_value is not None and key_value != "*":
        keys = unique(key_of(s) for s in rows)
        wanted = key_value.casefold()
        rows = [s for s in rows if key_of(s).casefold() == wanted]
        if not rows:
            close = closest_names(key_value, keys)
            msg = f"Variable '{name}' has no key '{key_value}'." + did_you_mean(close)
            if keys == [""]:
                msg += " It is reported with no key (as meters are); leave key_value at its default."
            else:
                msg += f" It is reported for {count(keys, 'key')}: {listing(keys)}."
            raise ResultLookupError(msg, suggestions=close, available=keys)

    if frequency is not None:
        freqs = unique(frequency_of(s) for s in rows)
        wanted = frequency.casefold()
        if frequency_matches is None:
            rows = [s for s in rows if frequency_of(s).casefold() == wanted]
        else:
            matches = frequency_matches
            rows = [s for s in rows if matches(s, wanted)]
        if not rows:
            msg = f"Variable '{name}'{for_key(key_value)} is not reported at frequency '{frequency}'."
            msg += f" It is reported at: {listing(freqs)}."
            raise ResultLookupError(msg, available=freqs)

    keys = unique(key_of(s) for s in rows)
    if len(keys) > 1:
        msg = f"Variable '{name}' is reported for {count(keys, 'key')} ({listing(keys)}); pass key_value= to pick one."
        raise ResultLookupError(msg, available=keys)
    freqs = unique(frequency_of(s) for s in rows)
    if len(freqs) > 1:
        msg = (
            f"Variable '{name}'{for_key(key_value)} is reported at {len(freqs)} frequencies "
            f"({listing(freqs)}); pass frequency= to pick one."
        )
        raise ResultLookupError(msg, available=freqs)
    return rows[0]
