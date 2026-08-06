from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from idfkit.simulation import simulate, SimulationProgress

with Progress(
    SpinnerColumn(),
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    TextColumn("{task.percentage:>3.0f}%"),
    TextColumn("[dim]{task.fields[phase]}"),
) as progress:
    task = progress.add_task("Simulating", total=100, phase="starting")

    def on_progress(event: SimulationProgress) -> None:
        if event.percent is not None:
            progress.update(task, completed=event.percent, phase=event.phase)
        else:
            progress.update(task, phase=event.phase)

    result = simulate(model, "weather.epw", annual=True, on_progress=on_progress)
# --8<-- [end:example]
