"""Smoke test to verify CI environment setup and caching."""

from __future__ import annotations


def test_import_idfkit() -> None:
    """Verify that idfkit can be imported successfully."""
    import idfkit

    assert idfkit is not None
