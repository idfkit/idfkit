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
  planning (``specs/014-model-knowledge-graph/background/04-performance-measurements.md`` in
  idfkit-unification, Python 3.12, 4 vCPU). On the same class of machine it measured
  0.13 to 0.16 s when this gate was added, so the budget of 0.456 s holds about 3x headroom.

- :data:`TOPOLOGY_BUILD_BASELINE_S`, 0.050 s: ``HVACTopology.from_document`` plus ``check()`` on a
  freshly loaded reference model, the plan's budget (R-21). Measured 0.027 s when added, 11% of
  ``load_idf``. It must also stay within :data:`TOPOLOGY_SHARE_OF_LOAD` of ``load_idf``.
- :data:`TOPOLOGY_CACHED_BASELINE_S`, 0.0001 s: ``from_document`` again with no edit in between.
- :data:`TOPOLOGY_MEMORY_BASELINE_B`, 10 MB: peak memory the topology build with checks allocates.
- :data:`TOPOLOGY_QUERY_BASELINE_S`, 0.005 s: one topology query (a 3-hop walk, a node's uses).
- :data:`LOOP_QUERY_BASELINE_S`, 0.005 s: one ``memberships(obj)`` or ``chain(loop, side)`` call,
  timed both as the first call on a fresh view (which builds the memoised answer: ``memberships``
  builds every object's memberships at once) and as a repeated, cached call.

Adding a budget: state its baseline as a module constant next to the others, list it above, and
add a test that compares a measurement against ``CI_ALLOWANCE * baseline``. Use the
``reference_model`` fixture for operations on an already loaded model, so the model is parsed once
for the whole module.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Literal

import pytest

# `benchmarks/` is not a package on the import path: pytest puts `tests/` there, not the repository
# root. Adding the root explicitly makes `benchmarks._timing` importable however pytest is invoked.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks._timing import best_of, load_reference_model, peak_memory, reference_model_path  # noqa: E402
from idfkit import IDFDocument, IDFObject, load_idf  # noqa: E402
from idfkit.hvac import HVACTopology  # noqa: E402

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


TOPOLOGY_BUILD_BASELINE_S = 0.050
"""``HVACTopology.from_document`` plus ``check()`` after a load, seconds (plan budget, R-21)."""

TOPOLOGY_SHARE_OF_LOAD = 0.25
"""The topology build with checks may cost at most this share of ``load_idf`` (SC-011)."""

TOPOLOGY_CACHED_BASELINE_S = 0.0001
"""A repeated ``from_document`` with no edit, seconds."""

TOPOLOGY_QUERY_BASELINE_S = 0.005
"""One topology query, seconds."""


def test_topology_build_with_checks_within_budget(reference_model_file: Path) -> None:
    path = str(reference_model_file)
    docs = [load_idf(path) for _ in range(RUNS)]
    pending = iter(docs)
    elapsed = best_of(lambda: HVACTopology.from_document(next(pending)).check(), RUNS)
    load = best_of(lambda: load_idf(path), 3)
    budget = CI_ALLOWANCE * TOPOLOGY_BUILD_BASELINE_S
    assert elapsed <= budget, f"topology build + checks took {elapsed * 1000:.1f} ms; budget {budget * 1000:.0f} ms"
    assert elapsed <= TOPOLOGY_SHARE_OF_LOAD * load, (
        f"topology build + checks took {elapsed / load:.0%} of load_idf; budget {TOPOLOGY_SHARE_OF_LOAD:.0%}"
    )


def test_cached_topology_within_budget(reference_model: IDFDocument) -> None:
    HVACTopology.from_document(reference_model)
    elapsed = best_of(lambda: HVACTopology.from_document(reference_model), RUNS)
    assert elapsed <= CI_ALLOWANCE * TOPOLOGY_CACHED_BASELINE_S, f"cached view took {elapsed * 1e6:.1f} us"


def test_topology_query_within_budget(reference_model: IDFDocument) -> None:
    topo = HVACTopology.from_document(reference_model)
    node = max(topo.nodes(), key=lambda n: len(topo.uses(n)))
    elapsed = max(
        best_of(lambda: topo.downstream(node, hops=3), RUNS),
        best_of(lambda: topo.upstream(node, hops=3), RUNS),
        best_of(lambda: topo.uses(node), RUNS),
    )
    assert elapsed <= CI_ALLOWANCE * TOPOLOGY_QUERY_BASELINE_S, f"slowest query took {elapsed * 1000:.2f} ms"


TOPOLOGY_MEMORY_BASELINE_B = 10 * 1024 * 1024
"""Peak memory of the topology build with checks, bytes (R-21: at most 10 MB extra per model)."""


def test_topology_memory_within_budget(reference_model_file: Path) -> None:
    doc = load_idf(str(reference_model_file))
    _, peak = peak_memory(lambda: HVACTopology.from_document(doc).check())
    assert peak <= TOPOLOGY_MEMORY_BASELINE_B, f"topology build + checks peaked at {peak / 1e6:.1f} MB"


LOOP_QUERY_BASELINE_S = 0.005
"""One ``memberships(obj)`` or ``chain(loop, side)`` call, first on a fresh view or cached, seconds."""


def _first_call(doc: IDFDocument, query: Callable[[HVACTopology], object]) -> float:
    """Best of :data:`RUNS` first calls of *query*, each on its own freshly built view.

    The views are built before timing starts, with the constructor rather than ``from_document``,
    which would hand back the cached view whose memoised answers are already built.
    """
    views = iter([HVACTopology(doc) for _ in range(RUNS)])
    return best_of(lambda: query(next(views)), RUNS)


def _water_coil(topo: HVACTopology, doc: IDFDocument) -> IDFObject:
    """A water coil on both an air loop and a water loop, the component with the most memberships."""
    coils = [
        obj
        for obj_type in doc.collections
        if obj_type.startswith("Coil:") and ":Water" in obj_type
        for obj in doc.get_collection(obj_type)
    ]
    return max(coils, key=lambda c: len({m.kind for m in topo.memberships(c)}))


def test_memberships_within_budget(reference_model: IDFDocument) -> None:
    topo = HVACTopology(reference_model)
    coil = _water_coil(topo, reference_model)
    assert {m.kind for m in topo.memberships(coil)} >= {"air", "plant"}, "premise: a coil on an air and a water loop"
    budget = CI_ALLOWANCE * LOOP_QUERY_BASELINE_S
    first = _first_call(reference_model, lambda view: view.memberships(coil))
    cached = best_of(lambda: topo.memberships(coil), RUNS)
    assert first <= budget, (
        f"first memberships() on a fresh view took {first * 1000:.2f} ms; budget {budget * 1000:.0f} ms"
    )
    assert cached <= budget, f"cached memberships() took {cached * 1000:.3f} ms; budget {budget * 1000:.0f} ms"


Side = Literal["supply", "demand"]
SIDES: tuple[Side, ...] = ("supply", "demand")


def _assert_chain_within_budget(doc: IDFDocument, topo: HVACTopology, loop: IDFObject, side: Side) -> None:
    budget = CI_ALLOWANCE * LOOP_QUERY_BASELINE_S
    first = _first_call(doc, lambda view: view.chain(loop, side))
    cached = best_of(lambda: topo.chain(loop, side), RUNS)
    label = f"chain({loop.name!r}, {side!r}), {len(topo.chain(loop, side))} paths"
    assert first <= budget, f"first {label} on a fresh view took {first * 1000:.2f} ms; budget {budget * 1000:.0f} ms"
    assert cached <= budget, f"cached {label} took {cached * 1000:.3f} ms; budget {budget * 1000:.0f} ms"


def test_chain_within_budget(reference_model: IDFDocument) -> None:
    topo = HVACTopology(reference_model)
    sides: list[tuple[IDFObject, Side]] = [(loop, side) for loop in topo.loops() for side in SIDES]
    # The side with the most branches (a plant loop's demand side), and the air loop demand side with
    # the most paths, which takes the other code path: a walk of the demand side, not a BranchList.
    widest = max(sides, key=lambda s: len(topo.chain(*s)))
    air = max(
        (s for s in sides if s[0].obj_type == "AirLoopHVAC" and s[1] == "demand"), key=lambda s: len(topo.chain(*s))
    )
    assert len(topo.chain(*widest)) > 100, "premise: the reference model has a loop side with over 100 branches"
    _assert_chain_within_budget(reference_model, topo, *widest)
    _assert_chain_within_budget(reference_model, topo, *air)
