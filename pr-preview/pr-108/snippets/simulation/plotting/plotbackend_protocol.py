from __future__ import annotations

# --8<-- [start:example]
from idfkit.simulation import PlotBackend


class MyBackend(PlotBackend):
    def line(
        self,
        x: list,
        y: list,
        *,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        label: str | None = None,
    ):
        # Return a figure object
        ...

    def bar(
        self,
        categories: list[str],
        values: list[float],
        *,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
    ):
        # Return a figure object
        ...


# --8<-- [end:example]
