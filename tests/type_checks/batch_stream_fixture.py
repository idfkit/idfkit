"""Type-check fixture for ``async_simulate_batch_stream`` (never called; checked by ``make check``).

The stream's documentation recommends closing it with ``contextlib.aclosing(...)``, which needs an
object with ``aclose()``. This fixture proves that documented pattern type-checks under strict mode.
"""

# pyright: strict

from __future__ import annotations

import contextlib

from typing_extensions import assert_type

from idfkit.simulation import SimulationJob
from idfkit.simulation.async_batch import SimulationEvent, async_simulate_batch_stream


async def aclosing_stream(jobs: list[SimulationJob]) -> None:
    async with contextlib.aclosing(async_simulate_batch_stream(jobs)) as stream:
        async for event in stream:
            assert_type(event, SimulationEvent)
            break
