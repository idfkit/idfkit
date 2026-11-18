"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class WindowMaterialGlazingRefractionExtinctionMethod:
    def __call__(
        self,
        name: str,
        /,
        *,
        thickness: float,
        solar_index_of_refraction: float,
        solar_extinction_coefficient: float,
        visible_index_of_refraction: float,
        visible_extinction_coefficient: float,
        infrared_transmittance_at_normal_incidence: float | None = 0,
        infrared_hemispherical_emissivity: float | None = 0.84,
        conductivity: float | None = 0.9,
        dirt_correction_factor_for_solar_and_visible_transmittance: float | None = 1,
        solar_diffusing: Literal["No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``WindowMaterial:Glazing:RefractionExtinctionMethod`` and add it to the document.

        Glass material properties for Windows or Glass Doors Index of Refraction/Extinction Coefficient input method Not to be used for coated glass

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialglazingrefractionextinctionmethod
        """

class SwimmingPoolIndoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        average_depth: float,
        activity_factor_schedule_name: str,
        cover_schedule_name: str,
        pool_water_inlet_node: str,
        pool_water_outlet_node: str,
        setpoint_temperature_schedule: str,
        maximum_number_of_people: float,
        make_up_water_supply_schedule_name: str | None = ...,
        cover_evaporation_factor: float | None = 0,
        cover_convection_factor: float | None = 0,
        cover_short_wavelength_radiation_factor: float | None = 0,
        cover_long_wavelength_radiation_factor: float | None = 0,
        pool_heating_system_maximum_water_flow_rate: float | None = ...,
        pool_miscellaneous_equipment_power: float | None = ...,
        people_schedule: str | None = ...,
        people_heat_gain_schedule: str | None = ...,
    ) -> None:
        """Create a new ``SwimmingPool:Indoor`` and add it to the document.

        Specifies an indoor swimming pools linked to a floor surface. The pool is assumed to cover the entire floor to which it is linked.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#swimmingpoolindoor
        """

class ZoneInfiltrationEffectiveLeakageArea:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        effective_air_leakage_area: float,
        stack_coefficient: float,
        wind_coefficient: float,
        schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneInfiltration:EffectiveLeakageArea`` and add it to the document.

        Infiltration is specified as effective leakage area at 4 Pa, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * (AL /1000) SQRT(Cs*|(Tzone-Todb)| + Cw*WindSpd**2 ) If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneinfiltrationeffectiveleakagearea
        """

class AnyZoneHVACOutdoorAirUnitEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_1_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_1_name: str | None = ...,
        component_2_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_3_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_4_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_5_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_6_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_7_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_8_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_8_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:OutdoorAirUnit:EquipmentList`` and add it to the document.

        Equipment list for components in a ZoneHVAC:OutdoorAirUnit. Components are simulated sequentially in the order given in the equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacoutdoorairunitequipmentlist
        """

class AirTerminalDualDuctConstantVolume:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        hot_air_inlet_node_name: str,
        cold_air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:DualDuct:ConstantVolume`` and add it to the document.

        Central air system terminal unit, dual duct, constant volume.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminaldualductconstantvolume
        """

class AnyCoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_to_refrigerant_hx_water_inlet_node_name: str,
        water_to_refrigerant_hx_water_outlet_node_name: str,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_total_cooling_capacity: float,
        speed_1_reference_unit_gross_rated_sensible_heat_ratio: float,
        speed_1_reference_unit_gross_rated_cooling_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str,
        speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float,
        speed_1_waste_heat_function_of_temperature_curve_name: str,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float
        | Literal["Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
        flag_for_using_hot_gas_reheat_0_or_1: float | None = 0,
        speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_2_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_3_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_4_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_5_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_5_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_6_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_6_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_7_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_7_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_8_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_8_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_9_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_9_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_10_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_10_waste_heat_function_of_temperature_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), variable-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance. Requires two to ten sets of performance data and will interpolate between speeds. Modeled as a single coil with variable-speed compressor.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpvariablespeedequationfit
        """
