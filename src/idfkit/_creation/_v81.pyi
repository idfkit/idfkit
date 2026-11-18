"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class SteamEquipment_v9_6_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_zone_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``SteamEquipment`` and add it to the document.

        Sets internal gains for steam equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-internal-gains-people-lights-other/#steamequipment
        """

class HeatPumpPlantLoopEIRHeating_v23_2_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        condenser_type: Literal["AirSource", "WaterSource"] | None = "WaterSource",
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 3,
        sizing_factor: float | None = 1,
        heating_to_cooling_capacity_sizing_ratio: float | None = 1,
        heat_pump_sizing_method: Literal["CoolingCapacity", "GreaterOfHeatingOrCooling", "HeatingCapacity"]
        | None = "CoolingCapacity",
        control_type: Literal["Load", "Setpoint"] | None = "Load",
        flow_mode: Literal["ConstantFlow", "VariableSpeedPumping"] | None = "ConstantFlow",
        minimum_part_load_ratio: float | None = 0,
        minimum_source_inlet_temperature: float | None = -100,
        maximum_source_inlet_temperature: float | None = 100,
        minimum_supply_water_temperature_curve_name: str | None = ...,
        maximum_supply_water_temperature_curve_name: str | None = ...,
        dry_outdoor_correction_factor_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 10,
        heat_pump_defrost_control: Literal["None", "OnDemand", "Timed", "TimedEmpirical"] | None = ...,
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        timed_empirical_defrost_frequency_curve_name: str | None = ...,
        timed_empirical_defrost_heat_load_penalty_curve_name: str | None = ...,
        timed_empirical_defrost_heat_input_energy_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatPump:PlantLoop:EIR:Heating`` and add it to the document.

        An EIR formulated water to water heat pump model, heating operation

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-plant-equipment/#heatpumpplantloopeirheating
        """
