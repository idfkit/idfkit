"""Per-line suppression comments for ``idfkit check``.

A comment of the form ``# idfkit: ignore[C001]`` silences the listed rules on its own line, the
line the diagnostic is reported on (the line of the string literal), the way
``# pyright: ignore[rule]`` and ``# type: ignore[code]`` work. Several codes are separated by
commas (``# idfkit: ignore[C001, C004]``); a bare ``# idfkit: ignore`` silences every rule on the
line. The comment may follow other comments (``# noqa: E501  # idfkit: ignore[C001]``).

The ``idfkit:`` namespace is deliberate. ``# noqa: C001`` would be read by ruff and flake8 as
well, where ``C0``/``C4`` codes belong to flake8-comprehensions and mccabe: ruff reports an unknown
``noqa`` code, and its unused-``noqa`` fix (``RUF100``) deletes it.
"""

from __future__ import annotations

import io
import re
import tokenize
from dataclasses import dataclass, field

_COMMENT_RE = re.compile(r"(?:^|#)\s*idfkit:\s*ignore\b(?:\[(?P<codes>[^\]]*)\])?")


@dataclass
class Suppression:
    """One ``# idfkit: ignore`` comment.

    Attributes:
        line: 1-based line the comment is on.
        col: 0-based column of the comment.
        end_col: 0-based end column of the comment.
        codes: The rule codes listed (upper-cased), or ``None`` for a bare ``ignore``.
        used: The codes the comment actually silenced in this run.
    """

    line: int
    col: int
    end_col: int
    codes: frozenset[str] | None
    used: set[str] = field(default_factory=lambda: set())

    def covers(self, code: str) -> bool:
        """Whether this comment silences *code*."""
        return self.codes is None or code in self.codes


def parse_suppressions(source: str) -> dict[int, Suppression]:
    """Find every ``# idfkit: ignore`` comment in *source*, keyed by line.

    Only real comments are read (through :mod:`tokenize`), so the text inside a string is never
    taken for one. A source that does not tokenize yields no suppressions; the parse error is
    reported by the caller.
    """
    found: dict[int, Suppression] = {}
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, SyntaxError):
        return found
    for token in tokens:
        if token.type != tokenize.COMMENT:
            continue
        match = _COMMENT_RE.search(token.string)
        if match is None:
            continue
        raw = match.group("codes")
        codes = None if raw is None else frozenset(c.strip().upper() for c in raw.split(",") if c.strip())
        line, col = token.start
        found[line] = Suppression(line=line, col=col, end_col=token.end[1], codes=codes)
    return found
