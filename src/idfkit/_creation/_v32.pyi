"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class CoilCoolingDXCurveFitOperatingMode_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        speed_1_name: str,
        rated_gross_total_cooling_capacity: float | Literal["Autosize"] | None = "Autosize",
        rated_evaporator_air_flow_rate: float | Literal["Autosize"] | None = ...,
        rated_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        apply_latent_degradation_to_speeds_greater_than_1: Literal["No", "Yes"] | None = "No",
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        nominal_evaporative_condenser_pump_power: float | Literal["Autosize"] | None = 0,
        nominal_speed_number: float | None = ...,
        speed_2_name: str | None = ...,
        speed_3_name: str | None = ...,
        speed_4_name: str | None = ...,
        speed_5_name: str | None = ...,
        speed_6_name: str | None = ...,
        speed_7_name: str | None = ...,
        speed_8_name: str | None = ...,
        speed_9_name: str | None = ...,
        speed_10_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:OperatingMode`` and add it to the document.

        DX cooling coil performance for a single operating mode which may have one or more speeds.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitoperatingmode
        """
