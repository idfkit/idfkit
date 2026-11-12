"""Qualify the connection checks on EnergyPlus example files (SC-001, SC-001a; research R-18, R-34).

Opt-in: ``pytest -m integration tests/test_hvac_corpus.py``. Point it at example files with
``--corpus VERSION=PATH`` (repeatable). The 26.2 test also finds an installed EnergyPlus 26.2.

- SC-001: no error-severity finding on any 26.2 example file. Every example file simulates, so an
  error there is a false error.
- SC-001a: earlier versions are measured, not qualified; their counts feed ``_version_caps.py``
  through ``python -m idfkit.codegen.generate_version_caps``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.codegen.generate_version_caps import measure
from idfkit.simulation import find_energyplus

pytestmark = pytest.mark.integration


def _examples_26_2(corpus_dirs: dict[str, Path]) -> Path:
    for key in ("26.2.0", "26.2"):
        if key in corpus_dirs:
            return corpus_dirs[key]
    try:
        config = find_energyplus(version=(26, 2, 0))
    except Exception:
        pytest.skip("EnergyPlus 26.2 example files not given (--corpus 26.2.0=PATH) and not installed")
    examples = Path(config.install_dir) / "ExampleFiles"
    if not examples.is_dir():
        pytest.skip(f"No ExampleFiles under {config.install_dir}")
    return examples


def test_no_error_findings_on_the_26_2_example_files(corpus_dirs: dict[str, Path]) -> None:
    m = measure(_examples_26_2(corpus_dirs), (26, 2, 0))
    assert m.models > 500
    assert m.unreadable == []
    errors = {code: n for (code, severity), n in m.findings.items() if severity == "error"}
    assert errors == {}, {code: m.examples.get(code) for code in errors}


def test_earlier_versions_are_measured(corpus_dirs: dict[str, Path]) -> None:
    earlier = {v: p for v, p in corpus_dirs.items() if not v.startswith("26.2")}
    if not earlier:
        pytest.skip("No earlier-version corpus given (--corpus 9.6.0=PATH --corpus 23.2.0=PATH)")
    for version_text, path in earlier.items():
        parts = [int(p) for p in version_text.split(".")]
        m = measure(path, (parts[0], parts[1], parts[2] if len(parts) > 2 else 0))
        assert m.models > 0, version_text
        print(f"{version_text}: {m.models} models; findings {dict(m.findings)}")
