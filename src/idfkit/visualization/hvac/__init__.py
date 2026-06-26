"""HVAC system diagrams reconstructed from an :class:`~idfkit.IDFDocument`.

Build a graph of the air/plant/condenser loops directly from IDF objects (no
simulation run) and render it to Mermaid, Graphviz DOT, or a structured dict —
similar in spirit to the EnergyPlus HVAC-Diagram utility.

Example:
    >>> from idfkit import load_idf
    >>> from idfkit.visualization import hvac_to_mermaid
    >>>
    >>> model = load_idf("expanded_system.idf")
    >>> print(hvac_to_mermaid(model))      # doctest: +SKIP
    flowchart LR
      ...

The document must be expanded first: if ``HVACTemplate:*`` objects are present,
:func:`build_hvac_graph` raises :class:`~idfkit.exceptions.HVACDiagramError`
unless ``expand=True`` is passed (which runs ``model.expand()``).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .build import build_hvac_graph
from .model import (
    HVACDiagramConfig,
    HVACEdge,
    HVACGraph,
    HVACLoop,
    HVACNode,
    HVACVertex,
    HVACWarning,
    HVACZone,
    LoopMembership,
)

if TYPE_CHECKING:
    from idfkit.document import IDFDocument


def hvac_to_mermaid(
    source: IDFDocument | HVACGraph,
    config: HVACDiagramConfig | None = None,
    *,
    expand: bool = False,
) -> str:
    """Render an HVAC diagram as Mermaid from a document or a prebuilt graph.

    Args:
        source: An :class:`~idfkit.IDFDocument` (a graph is built from it) or an
            already-built :class:`HVACGraph`.
        config: Optional :class:`HVACDiagramConfig` rendering options.
        expand: Forwarded to :func:`build_hvac_graph` when *source* is a document.
    """
    graph = source if isinstance(source, HVACGraph) else build_hvac_graph(source, expand=expand)
    return graph.to_mermaid(config)


def hvac_to_dot(
    source: IDFDocument | HVACGraph,
    config: HVACDiagramConfig | None = None,
    *,
    expand: bool = False,
) -> str:
    """Render an HVAC diagram as Graphviz DOT from a document or a prebuilt graph.

    See :func:`hvac_to_mermaid` for the argument meanings.
    """
    graph = source if isinstance(source, HVACGraph) else build_hvac_graph(source, expand=expand)
    return graph.to_dot(config)


__all__ = [
    "HVACDiagramConfig",
    "HVACEdge",
    "HVACGraph",
    "HVACLoop",
    "HVACNode",
    "HVACVertex",
    "HVACWarning",
    "HVACZone",
    "LoopMembership",
    "build_hvac_graph",
    "hvac_to_dot",
    "hvac_to_mermaid",
]
