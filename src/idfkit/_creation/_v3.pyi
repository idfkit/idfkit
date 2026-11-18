"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

class ZoneControlHumidistat_v8_9_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        humidifying_relative_humidity_setpoint_schedule_name: str,
        dehumidifying_relative_humidity_setpoint_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneControl:Humidistat`` and add it to the document.

        Specifies zone relative humidity setpoint schedules for humidifying and dehumidifying.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-zone-controls-thermostats/#zonecontrolhumidistat
        """
