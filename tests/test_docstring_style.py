"""Docstrings and signatures read well in the rendered API reference.

The reference at developers.idfkit.com is rendered by mkdocstrings, which does not interpret
Sphinx roles: ``:class:`Foo``` reaches the page as raw text and links nowhere. Cross-references
use the mkdocs-autorefs form, ``[Foo][idfkit.module.Foo]``.

A private type alias in a public signature is rendered by name, so the reader sees
``idfkit._loaders._Target`` instead of the type it stands for.
"""

from __future__ import annotations

import inspect
import re
from pathlib import Path
from typing import Any

import pytest

import idfkit
from idfkit.versioned import as_version

SRC = Path(idfkit.__file__).parent

# A role whose target holds a ``{`` is a template the stub generator fills in for the
# generated ``.pyi`` docstrings, which the reference does not render.
_ROLE = re.compile(r":(?:class|func|mod|meth|attr|exc|data|obj):`(?P<target>[^`{]+)`")


def test_no_sphinx_roles_in_docstrings() -> None:
    found = [
        f"{path.relative_to(SRC)}:{lineno}: {match.group(0)}"
        for path in sorted(SRC.rglob("*.py"))
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        for match in _ROLE.finditer(line)
    ]
    assert not found, "Sphinx roles render as raw text; use [Name][idfkit.path] instead:\n" + "\n".join(found)


_PRIVATE_NAME = re.compile(r"(?<![\w.])_[A-Za-z]\w*")


@pytest.mark.parametrize(
    "function",
    [idfkit.load_idf, idfkit.load_idf_with_diagnostics, idfkit.load_epjson, as_version],
    ids=lambda f: f.__name__,
)
def test_public_signatures_name_no_private_types(function: Any) -> None:
    annotations = [str(p.annotation) for p in inspect.signature(function).parameters.values()]
    private = sorted({name for a in annotations for name in _PRIVATE_NAME.findall(a)} - {"_D"})
    assert not private, f"{function.__name__} annotates with private names {private}"
