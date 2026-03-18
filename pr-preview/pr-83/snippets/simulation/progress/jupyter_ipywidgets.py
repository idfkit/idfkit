from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
import ipywidgets as widgets
from IPython.display import display
from idfkit.simulation import simulate, SimulationProgress

bar = widgets.FloatProgress(min=0, max=100, description="Simulating:")
label = widgets.Label(value="Starting...")
display(widgets.HBox([bar, label]))


def on_progress(event: SimulationProgress) -> None:
    if event.percent is not None:
        bar.value = event.percent
    label.value = f"{event.phase}: {event.message[:60]}"


result = simulate(model, "weather.epw", annual=True, on_progress=on_progress)
bar.value = 100
label.value = "Done!"
# --8<-- [end:example]
