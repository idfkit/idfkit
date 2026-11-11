"""Performance budget gate (research R-21 of the model knowledge graph feature).

Every test here is marked ``perf`` and deselected by default (``addopts`` in ``pyproject.toml``).
Run the gate with::

    uv run pytest -m perf tests/test_perf_budgets.py

Each budget is a stated baseline times :data:`CI_ALLOWANCE`. The baseline is a figure measured on
a developer machine; the allowance absorbs slower and noisier CI runners and Python 3.10. A test
fails only when an operation is more than twice as slow as its baseline, which is a regression,
not noise.

Baselines, all on the vendored reference model ``benchmarks/fixtures/HospitalLowEnergy.idf.gz``
(6,876 objects) and timed as the best of :data:`RUNS` runs:

- :data:`LOAD_IDF_BASELINE_S`, 0.228 s: ``load_idf`` of the reference model, as measured during
  planning (``specs/001-model-knowledge-graph/background/04-performance-measurements.md`` in
  idfkit-mcp, Python 3.12, 4 vCPU). On the 26.1 file and the same class of machine it measured
  0.13 to 0.16 s when this gate was added, so the budget of 0.456 s holds about 3x headroom.

Adding a budget: state its baseline as a module constant next to the others, list it above, and
add a test that compares a measurement against ``CI_ALLOWANCE * baseline``. Use the
``reference_model`` fixture for operations on an already loaded model, so the model is parsed once
for the whole module.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# `benchmarks/` is not a package on the import path: pytest puts `tests/` there, not the repository
# root. Adding the root explicitly makes `benchmarks._timing` importable however pytest is invoked.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks._timing import best_of, load_reference_model, reference_model_path  # noqa: E402
from idfkit import IDFDocument, load_idf  # noqa: E402

pytestmark = pytest.mark.perf

CI_ALLOWANCE = 2.0
"""Factor between a stated baseline and the budget the gate enforces."""

RUNS = 5
"""Number of timed runs; the fastest is compared against the budget."""

LOAD_IDF_BASELINE_S = 0.228
"""``load_idf`` of the reference model, seconds (planning measurement, R-21)."""


@pytest.fixture(scope="module")
def reference_model_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The reference model decompressed once to disk, so gzip never enters a timing."""
    return reference_model_path(tmp_path_factory.mktemp("reference-model"))


@pytest.fixture(scope="module")
def reference_model(tmp_path_factory: pytest.TempPathFactory) -> IDFDocument:
    """The reference model, loaded once for the tests that time operations on a loaded model."""
    return load_reference_model(tmp_path_factory.mktemp("reference-model-doc"))


def test_reference_model_is_the_large_one(reference_model: IDFDocument) -> None:
    """Guard the budgets' premise: a smaller fixture would make every budget meaningless."""
    assert len(reference_model) > 6000


def test_load_idf_within_budget(reference_model_file: Path) -> None:
    path = str(reference_model_file)
    budget = CI_ALLOWANCE * LOAD_IDF_BASELINE_S
    elapsed = best_of(lambda: load_idf(path), RUNS)
    assert elapsed <= budget, (
        f"load_idf of the reference model took {elapsed * 1000:.0f} ms (best of {RUNS}); "
        f"budget {budget * 1000:.0f} ms = {CI_ALLOWANCE:g} x baseline {LOAD_IDF_BASELINE_S * 1000:.0f} ms"
    )
