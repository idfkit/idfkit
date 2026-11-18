"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class ElectricEquipment_v9_6_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal["EquipmentLevel", "Watts/Area", "Watts/Person"]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        watts_per_zone_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``ElectricEquipment`` and add it to the document.

        Sets internal gains for electric equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-internal-gains-people-lights-other/#electricequipment
        """

class CoilHeatingFuel_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fuel_type: Literal[
            "Diesel", "FuelOilNo1", "FuelOilNo2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ]
        | None = "NaturalGas",
        burner_efficiency: float | None = 0.8,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        parasitic_electric_load: float | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        parasitic_fuel_load: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Fuel`` and add it to the document.

        Gas or other fuel heating coil. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/energyplus-economics/cost-estimating/#coilheatingfuel
        """

class HeatPumpAirToWaterFuelFiredHeating_v23_1_to_v25_1:
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
        companion_cooling_heat_pump_name: str | None = ...,
        fuel_type: Literal[
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
        nominal_heating_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 60,
        design_temperature_lift: float | Literal["Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["EnteringCondenser", "LeavingCondenser"]
        | None = "EnteringCondenser",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        defrost_control_type: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_operation_time_fraction: float | None = 0,
        fuel_energy_input_ratio_defrost_adjustment_curve_name: str | None = ...,
        resistive_defrost_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
    ) -> None:
        """Create a new ``HeatPump:AirToWater:FuelFired:Heating`` and add it to the document.

        The object defines a fuel-fired absorption heat pump based on equation-fit models.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-plant-heating-and-cooling-equipment/#heatpumpairtowaterfuelfiredheating
        """
