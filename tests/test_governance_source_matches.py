"""The duplicated governance reader has not drifted from the library's copy.

``scripts/_governance_source.py`` exists twice, here and in ``idfkit-developers/scripts/``. Four callers
read governance artifacts at a pinned tag and feature 003 put them in two repositories: the
library's naming and parity gates stayed with the library, the site's parity and naming
renderers followed the site.

Duplication was chosen over publishing ~90 lines as a package, which would make a release cycle
out of a file that changes twice a year, and over moving it into idfkit-conformance, which would
turn a data repository into a code dependency of both libraries. The cost is that the two can
drift, and if they do, the pinned read means two different things in two repositories: a page
and a gate can then disagree about the same tag, which is the exact failure the module was
written to prevent.

This test is what makes "must land in both" blocking rather than remembered.

WHY IT COMPARES BYTES AND NOT BEHAVIOUR. Behaviour is what matters, but behaviour is what a
diff cannot see. Two files that differ by a default argument are two files that agree on every
test anyone thought to write and disagree on the one nobody did. Bytes are the only comparison
with no gap in it, which is also why the banner at the top of both copies is identical and names
both paths rather than pointing at "the other one".
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1] / "scripts" / "_governance_source.py"

#: Where the site's copy is. A sibling checkout by default, because that is how this workspace
#: is laid out; CI sets the variable after checking the site out itself.
LIBRARY_COPY_ENV = "IDFKIT_DEVELOPERS_REPO"
DEFAULT_LIBRARY_COPY = Path(__file__).resolve().parents[2] / "idfkit-developers"


def _library_copy() -> Path:
    root = Path(os.environ.get(LIBRARY_COPY_ENV, DEFAULT_LIBRARY_COPY))
    return root / "scripts" / "_governance_source.py"


def test_this_repository_has_the_reader() -> None:
    assert HERE.is_file(), f"no governance reader at {HERE}"


def test_the_two_copies_are_byte_identical() -> None:
    """Skips when the library is not checked out. It never passes on a missing file."""
    other = _library_copy()
    if not other.is_file():
        pytest.skip(
            f"no site checkout at {other}. Set ${LIBRARY_COPY_ENV} to the idfkit-developers "
            f"repository root to run this comparison. CI checks the site out and sets it, so a "
            f"skip here is a local convenience and never how the gate passes."
        )

    mine = HERE.read_bytes()
    theirs = other.read_bytes()
    assert mine == theirs, (
        f"{HERE} and {other} have drifted.\n\n"
        "These two files must be byte-identical. A change to one MUST land in the other in the "
        "same feature: if they differ, the pinned governance read means two different things in "
        "two repositories, and a rendered page can disagree with the gate that checks it.\n\n"
        "Copy whichever is correct over the other. Do not 'reconcile' them by hand, and do not "
        "make the banner point outward: it is identical in both copies on purpose."
    )


def test_both_copies_declare_the_duplication() -> None:
    """A copy that does not say it is one is a copy someone will edit alone."""
    text = HERE.read_text(encoding="utf-8")
    assert "THIS FILE IS DUPLICATED" in text
    assert "idfkit/scripts/_governance_source.py" in text
    assert "idfkit-developers/scripts/_governance_source.py" in text
