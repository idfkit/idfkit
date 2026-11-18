"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class HeatPumpAirToWaterFuelFiredCooling_v23_1_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        normalized_capacity_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_plr_curve_name: str,
        air_source_node_name: str | None = ...,
        companion_heating_heat_pump_name: str | None = ...,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "NaturalGas",
        end_use_subcategory: str | None = "General",
        nominal_cooling_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 7,
        design_temperature_lift: float | Literal["", "Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["", "DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["", "EnteringEvaporator", "LeavingEvaporator"]
        | None = "EnteringEvaporator",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
    ) -> None:
        """Create a new ``HeatPump:AirToWater:FuelFired:Cooling`` and add it to the document.

        The object defines a fuel-fired absorption heat pump based on equation-fit models.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-plant-heating-and-cooling-equipment/#heatpumpairtowaterfuelfiredcooling
        """
