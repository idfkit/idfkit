"""Web UI for browsing and downloading TMYx weather stations.

The browser is implemented as a stdlib-only ``http.server`` serving a
single-page Leaflet map. Bundled assets live under ``assets/``.
"""

from __future__ import annotations

from .server import launch_browser

__all__ = ["launch_browser"]
