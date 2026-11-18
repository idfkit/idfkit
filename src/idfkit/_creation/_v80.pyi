"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class FanSystemModel_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        design_maximum_air_flow_rate: float | Literal["Autosize"],
        design_pressure_rise: float,
        availability_schedule_name: str | None = ...,
        speed_control_method: Literal["Continuous", "Discrete"] | None = "Discrete",
        electric_power_minimum_flow_rate_fraction: float | None = 0.2,
        motor_efficiency: float | None = 0.9,
        motor_in_air_stream_fraction: float | None = 1,
        design_electric_power_consumption: float | Literal["Autosize"] | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure", "TotalEfficiencyAndPressure"]
        | None = "PowerPerFlowPerPressure",
        electric_power_per_unit_flow_rate: float | None = ...,
        electric_power_per_unit_flow_rate_per_unit_pressure: float | None = 1.66667,
        fan_total_efficiency: float | None = 0.7,
        electric_power_function_of_flow_fraction_curve_name: str | None = ...,
        night_ventilation_mode_pressure_rise: float | None = ...,
        night_ventilation_mode_flow_fraction: float | None = ...,
        motor_loss_zone_name: str | None = ...,
        motor_loss_radiative_fraction: float | None = ...,
        end_use_subcategory: str | None = "General",
        number_of_speeds: float | None = 1,
        speed_fractions: Sequence[_g.FanSystemModelSpeedFractionsItem | _g.FanSystemModelSpeedFractionsGroup] = ...,
    ) -> None:
        """Create a new ``Fan:SystemModel`` and add it to the document.

        Versatile simple fan that can be used in variable air volume, constant volume, on-off cycling, two-speed or multi-speed applications. Performance at different flow rates, or speed levels, is determined using separate performance curve or table or prescribed power fractions at discrete speed levels for two-speed or multi-speed fans.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-fans/#fansystemmodel
        """

class MaterialPropertyHeatAndMoistureTransferThermalConductivity_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_thermal_coordinates: float,
        moisture_content_1: float,
        thermal_conductivity_1: float,
        moisture_content_2: float | None = ...,
        thermal_conductivity_2: float | None = ...,
        moisture_content_3: float | None = ...,
        thermal_conductivity_3: float | None = ...,
        moisture_content_4: float | None = ...,
        thermal_conductivity_4: float | None = ...,
        moisture_content_5: float | None = ...,
        thermal_conductivity_5: float | None = ...,
        moisture_content_6: float | None = ...,
        thermal_conductivity_6: float | None = ...,
        moisture_content_7: float | None = ...,
        thermal_conductivity_7: float | None = ...,
        moisture_content_8: float | None = ...,
        thermal_conductivity_8: float | None = ...,
        moisture_content_9: float | None = ...,
        thermal_conductivity_9: float | None = ...,
        moisture_content_10: float | None = ...,
        thermal_conductivity_10: float | None = ...,
        moisture_content_11: float | None = ...,
        thermal_conductivity_11: float | None = ...,
        moisture_content_12: float | None = ...,
        thermal_conductivity_12: float | None = ...,
        moisture_content_13: float | None = ...,
        thermal_conductivity_13: float | None = ...,
        moisture_content_14: float | None = ...,
        thermal_conductivity_14: float | None = ...,
        moisture_content_15: float | None = ...,
        thermal_conductivity_15: float | None = ...,
        moisture_content_16: float | None = ...,
        thermal_conductivity_16: float | None = ...,
        moisture_content_17: float | None = ...,
        thermal_conductivity_17: float | None = ...,
        moisture_content_18: float | None = ...,
        thermal_conductivity_18: float | None = ...,
        moisture_content_19: float | None = ...,
        thermal_conductivity_19: float | None = ...,
        moisture_content_20: float | None = ...,
        thermal_conductivity_20: float | None = ...,
        moisture_content_21: float | None = ...,
        thermal_conductivity_21: float | None = ...,
        moisture_content_22: float | None = ...,
        thermal_conductivity_22: float | None = ...,
        moisture_content_23: float | None = ...,
        thermal_conductivity_23: float | None = ...,
        moisture_content_24: float | None = ...,
        thermal_conductivity_24: float | None = ...,
        moisture_content_25: float | None = ...,
        thermal_conductivity_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:ThermalConductivity`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between thermal conductivity and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferthermalconductivity
        """

class People_v22_2_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        number_of_people_calculation_method: Literal["Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        people_per_floor_area: float | None = ...,
        floor_area_per_person: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["AngleFactor", "SurfaceWeighted", "ZoneAveraged"]
        | None = "ZoneAveraged",
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        thermal_comfort_model_1_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_2_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_3_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_4_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_5_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_6_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_7_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        ankle_level_air_velocity_schedule_name: str | None = ...,
        cold_stress_temperature_threshold: float | None = 15.56,
        heat_stress_temperature_threshold: float | None = 30,
    ) -> None:
        """Create a new ``People`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-internal-gains-people-lights-other/#people
        """

class OutputIlluminanceMap_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        z_height: float | None = 0,
        x_minimum_coordinate: float | None = 0,
        x_maximum_coordinate: float | None = 1,
        number_of_x_grid_points: float | None = 2,
        y_minimum_coordinate: float | None = 0,
        y_maximum_coordinate: float | None = 1,
        number_of_y_grid_points: float | None = 2,
    ) -> None:
        """Create a new ``Output:IlluminanceMap`` and add it to the document.

        reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-daylighting/#outputilluminancemap
        """

class AirLoopHVACUnitaryHeatPumpAirToAir_v8_9_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed", "CoilSystem:IntegratedHeatPump:AirSource"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:IntegratedHeatPump:AirSource",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir`` and add it to the document.

        Unitary heat pump system, heating and cooling, single-speed with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), and supplemental heating coil (gas, electric, hot water, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoair
        """

class AirTerminalSingleDuctVAVReheatVariableSpeedFan_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_cooling_air_flow_rate: float | Literal["Autosize"],
        maximum_heating_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        fan_object_type: Literal["Fan:SystemModel", "Fan:VariableVolume"],
        fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with reheat coil (hot water, electric, gas, or steam) and variable-speed fan. These units are usually employed in underfloor air distribution (UFAD) systems where the air is supplied at low static pressure through an underfloor plenum. The fan is used to control the flow of conditioned air that enters the space.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductvavreheatvariablespeedfan
        """
