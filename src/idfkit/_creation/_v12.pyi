"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class WeatherPropertySkyTemperature_v8_9_to_v9_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        calculation_type: Literal["DifferenceScheduleDewPointValue", "DifferenceScheduleDryBulbValue", "ScheduleValue"],
        schedule_name: str,
    ) -> None:
        """Create a new ``WeatherProperty:SkyTemperature`` and add it to the document.

        This object is used to override internal sky temperature calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-location-climate-weather-file-access/#weatherpropertyskytemperature
        """

class ControllerWaterCoil_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal["HumidityRatio", "Temperature", "TemperatureAndHumidityRatio"],
        actuator_variable: Literal["Flow"],
        sensor_node_name: str,
        actuator_node_name: str,
        action: Literal["Normal", "Reverse"] | None = ...,
        controller_convergence_tolerance: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_actuated_flow: float | Literal["Autosize"] | None = ...,
        minimum_actuated_flow: float | None = ...,
    ) -> None:
        """Create a new ``Controller:WaterCoil`` and add it to the document.

        Controller for a water coil which is located directly in an air loop branch or outdoor air equipment list. Controls the coil water flow to meet the specified leaving air setpoint(s). Used with Coil:Heating:Water, Coil:Cooling:Water, Coil:Cooling:Water:DetailedGeometry, and CoilSystem:Cooling:Water:HeatexchangerAssisted.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-controllers/#controllerwatercoil
        """

class ZoneHVACCoolingPanelRadiantConvectiveWater_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        maximum_chilled_water_flow_rate: float | Literal["Autosize"],
        fraction_radiant: float,
        rated_inlet_water_temperature: float | None = 5,
        rated_inlet_space_temperature: float | None = 24,
        rated_water_mass_flow_rate: float | None = 0.063,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "ZoneTotalLoad",
            "ZoneConvectiveLoad",
        ]
        | None = "MeanAirTemperature",
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: list[_g.ZoneHVACCoolingPanelRadiantConvectiveWaterSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:CoolingPanel:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-radiative-convective-units/#zonehvaccoolingpanelradiantconvectivewater
        """

class ZoneHVACLowTemperatureRadiantVariableFlow_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        fluid_to_radiant_surface_heat_transfer_model: Literal["", "ConvectionOnly", "ISOStandard"]
        | None = "ConvectionOnly",
        hydronic_tubing_inside_diameter: float | None = 0.013,
        hydronic_tubing_outside_diameter: float | None = 0.016,
        hydronic_tubing_length: float | Literal["", "Autosize"] | None = "Autosize",
        hydronic_tubing_conductivity: float | None = 0.35,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "SurfaceFaceTemperature",
            "SurfaceInteriorTemperature",
        ]
        | None = "MeanAirTemperature",
        setpoint_control_type: Literal["", "HalfFlowPower", "ZeroFlowPower"] | None = "HalfFlowPower",
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        maximum_hot_water_flow: float | Literal["Autosize"] | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_control_throttling_range: float | None = 0.5,
        heating_control_temperature_schedule_name: str | None = ...,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        maximum_cold_water_flow: float | Literal["Autosize"] | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
        changeover_delay_time_period_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:VariableFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water flow to the unit.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantvariableflow
        """

class SurfacePropertyExposedFoundationPerimeter_v8_9_to_v9_2:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        exposed_perimeter_calculation_method: Literal["BySegment", "ExposedPerimeterFraction", "TotalExposedPerimeter"],
        total_exposed_perimeter: float | None = ...,
        exposed_perimeter_fraction: float | None = ...,
        surfaces: list[_vd.SurfacePropertyExposedFoundationPerimeterSurfacesItem_v8_9_to_v9_2] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:ExposedFoundationPerimeter`` and add it to the document.

        Defines the perimeter of a foundation floor that is exposed to the exterior environment through the floor. User may either define the total exposed perimeter, fraction of perimeter exposed or individually define which segments of the floor surface perimeter are exposed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyexposedfoundationperimeter
        """

class ZoneInfiltrationFlowCoefficient_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        flow_coefficient: float,
        stack_coefficient: float,
        wind_coefficient: float,
        shelter_factor: float,
        pressure_exponent: float | None = 0.67,
    ) -> None:
        """Create a new ``ZoneInfiltration:FlowCoefficient`` and add it to the document.

        Infiltration is specified as flow coefficient, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * SQRT( (c * Cs*|(Tzone-Todb)|**n)**2 + (c* Cw*(s * WindSpd)**2n)**2 )

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zoneinfiltrationflowcoefficient
        """

class ZoneHVACPackagedTerminalAirConditioner_v22_2_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["", "None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalAirConditioner`` and add it to the document.

        Packaged terminal air conditioner (PTAC). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam) and fixed-position outdoor air mixer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalairconditioner
        """

class PlantEquipmentOperationSchemes_v9_0_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_scheme_1_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ],
        control_scheme_1_name: str,
        control_scheme_1_schedule_name: str,
        control_scheme_2_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_2_name: str | None = ...,
        control_scheme_2_schedule_name: str | None = ...,
        control_scheme_3_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_3_name: str | None = ...,
        control_scheme_3_schedule_name: str | None = ...,
        control_scheme_4_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_4_name: str | None = ...,
        control_scheme_4_schedule_name: str | None = ...,
        control_scheme_5_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_5_name: str | None = ...,
        control_scheme_5_schedule_name: str | None = ...,
        control_scheme_6_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_6_name: str | None = ...,
        control_scheme_6_schedule_name: str | None = ...,
        control_scheme_7_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_7_name: str | None = ...,
        control_scheme_7_schedule_name: str | None = ...,
        control_scheme_8_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_8_name: str | None = ...,
        control_scheme_8_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperationSchemes`` and add it to the document.

        Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first that is 'Scheduled' on. That is, if control scheme 1 is not 'on' and control scheme 2 is -- then control scheme 2 is selected. Only plant equipment should be listed on a Control Scheme for this item.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationschemes
        """

class GeneratorCombustionTurbine_v9_3_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_power_output: float | None = ...,
        electric_circuit_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        part_load_based_fuel_input_curve_name: str | None = ...,
        temperature_based_fuel_input_curve_name: str | None = ...,
        exhaust_flow_curve_name: str | None = ...,
        part_load_based_exhaust_temperature_curve_name: str | None = ...,
        temperature_based_exhaust_temperature_curve_name: str | None = ...,
        heat_recovery_lube_energy_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        design_air_inlet_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        fuel_type: Literal[
            "", "Diesel", "FuelOilNo1", "FuelOilNo2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ]
        | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        outdoor_air_inlet_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:CombustionTurbine`` and add it to the document.

        This generator model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Generator performance curves are generated by fitting catalog data to second order polynomial equations. Three sets of coefficients are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-electric-load-center-generator/#generatorcombustionturbine
        """

class ZoneHVACWaterToAirHeatPump_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit", "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit", "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_time_constant: float | None = 60,
        fraction_of_on_cycle_power_use: float | None = 0.01,
        heat_pump_fan_delay_time: float | None = 60,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:WaterToAirHeatPump`` and add it to the document.

        Water-to-air heat pump. Forced-convection heating-cooling unit with supply fan, water-to-air cooling and heating coils, supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-zone-forced-air-units/#zonehvacwatertoairheatpump
        """

class ControllerOutdoorAir_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        relief_air_outlet_node_name: str,
        return_air_node_name: str,
        mixed_air_node_name: str,
        actuator_node_name: str,
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        economizer_control_type: Literal[
            "",
            "DifferentialDryBulb",
            "DifferentialDryBulbAndEnthalpy",
            "DifferentialEnthalpy",
            "ElectronicEnthalpy",
            "FixedDewPointAndDryBulb",
            "FixedDryBulb",
            "FixedEnthalpy",
            "NoEconomizer",
        ]
        | None = "NoEconomizer",
        economizer_control_action_type: Literal["", "MinimumFlowWithBypass", "ModulateFlow"] | None = "ModulateFlow",
        economizer_maximum_limit_dry_bulb_temperature: float | None = ...,
        economizer_maximum_limit_enthalpy: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        electronic_enthalpy_limit_curve_name: str | None = ...,
        economizer_minimum_limit_dry_bulb_temperature: float | None = ...,
        lockout_type: Literal["", "LockoutWithCompressor", "LockoutWithHeating", "NoLockout"] | None = "NoLockout",
        minimum_limit_type: Literal["", "FixedMinimum", "ProportionalMinimum"] | None = "ProportionalMinimum",
        minimum_outdoor_air_schedule_name: str | None = ...,
        minimum_fraction_of_outdoor_air_schedule_name: str | None = ...,
        maximum_fraction_of_outdoor_air_schedule_name: str | None = ...,
        mechanical_ventilation_controller_name: str | None = ...,
        time_of_day_economizer_control_schedule_name: str | None = ...,
        high_humidity_control: Literal["", "No", "Yes"] | None = "No",
        humidistat_control_zone_name: str | None = ...,
        high_humidity_outdoor_air_flow_ratio: float | None = 1,
        control_high_indoor_humidity_based_on_outdoor_humidity_ratio: Literal["", "No", "Yes"] | None = "Yes",
        heat_recovery_bypass_control_type: Literal[
            "", "BypassWhenOAFlowGreaterThanMinimum", "BypassWhenWithinEconomizerLimits"
        ]
        | None = "BypassWhenWithinEconomizerLimits",
    ) -> None:
        """Create a new ``Controller:OutdoorAir`` and add it to the document.

        Controller to set the outdoor air flow rate for an air loop. Control options include fixed, proportional, scheduled, economizer, and demand-controlled ventilation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-controllers/#controlleroutdoorair
        """

class LifeCycleCostUsePriceEscalation_v9_3_to_v22_1:
    def __call__(
        self,
        /,
        *,
        lcc_price_escalation_name: str,
        resource: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ],
        escalation_start_year: float | None = ...,
        escalation_start_month: Literal[
            "",
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        escalations: list[_g.LifeCycleCostUsePriceEscalationEscalationsItem] = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:UsePriceEscalation`` and add it to the document.

        Life cycle cost escalation factors. The values for this object may be found in the annual supplement to NIST Handbook 135 in Tables Ca-1 to Ca-5 and are included in an EnergyPlus dataset file.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/energyplus-economics/lifecyclecost-usepriceescalation/#lifecyclecostusepriceescalation
        """

class RefrigerationSecondarySystem_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        refrigerated_case_or_walkin_or_caseandwalkinlist_name: str,
        circulating_fluid_type: Literal["FluidAlwaysLiquid", "FluidPhaseChange"],
        circulating_fluid_name: str,
        evaporator_evaporating_temperature: float,
        evaporator_approach_temperature_difference: float,
        evaporator_capacity: float | None = ...,
        evaporator_flow_rate_for_secondary_fluid: float | None = ...,
        evaporator_range_temperature_difference: float | None = ...,
        number_of_pumps_in_loop: float | None = 1,
        total_pump_flow_rate: float | None = ...,
        total_pump_power: float | None = ...,
        total_pump_head: float | None = ...,
        phasechange_circulating_rate: float | None = 2.5,
        pump_drive_type: Literal["", "Constant", "Variable"] | None = "Constant",
        variable_speed_pump_cubic_curve_name: str | None = ...,
        pump_motor_heat_to_fluid: float | None = 0.85,
        sum_ua_distribution_piping: float | None = 0,
        distribution_piping_zone_name: str | None = ...,
        sum_ua_receiver_separator_shell: float | None = 0,
        receiver_separator_zone_name: str | None = ...,
        evaporator_refrigerant_inventory: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Refrigeration:SecondarySystem`` and add it to the document.

        Works in conjunction with refrigerated cases and walkins to simulate the performance of a secondary loop supermarket refrigeration system. Heat from the refrigeration loads served by the secondary loop is absorbed by a primary refrigeration system (Refrigeration:System). The SecondarySystem object simulates a heat exchanger that is an evaporator, or refrigeration load, on the primary refrigeration system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-refrigeration/#refrigerationsecondarysystem
        """

class HVACTemplateSystemVRF_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_outdoor_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_temperature_in_cooling_mode: float | None = 43,
        gross_rated_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_outdoor_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_temperature_in_heating_mode: float | None = 16,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "", "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["", "No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = 30,
        vertical_height_used_for_piping_correction_factor: float | None = 10,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = 30,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: float | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        water_condenser_volume_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: Literal[
            "",
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "Electricity",
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -15,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 45,
    ) -> None:
        """Create a new ``HVACTemplate:System:VRF`` and add it to the document.

        Variable refrigerant flow (VRF) heat pump condensing unit. Serves one or more VRF zone terminal units (HVACTemplate:Zone:VRF).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemvrf
        """

class ComfortViewFactorAngles_v24_1_to_v25_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        surface_1_name: str | None = ...,
        angle_factor_1: float | None = ...,
        surface_2_name: str | None = ...,
        angle_factor_2: float | None = ...,
        surface_3_name: str | None = ...,
        angle_factor_3: float | None = ...,
        surface_4_name: str | None = ...,
        angle_factor_4: float | None = ...,
        surface_5_name: str | None = ...,
        angle_factor_5: float | None = ...,
        surface_6_name: str | None = ...,
        angle_factor_6: float | None = ...,
        surface_7_name: str | None = ...,
        angle_factor_7: float | None = ...,
        surface_8_name: str | None = ...,
        angle_factor_8: float | None = ...,
        surface_9_name: str | None = ...,
        angle_factor_9: float | None = ...,
        surface_10_name: str | None = ...,
        angle_factor_10: float | None = ...,
        surface_11_name: str | None = ...,
        angle_factor_11: float | None = ...,
        surface_12_name: str | None = ...,
        angle_factor_12: float | None = ...,
        surface_13_name: str | None = ...,
        angle_factor_13: float | None = ...,
        surface_14_name: str | None = ...,
        angle_factor_14: float | None = ...,
        surface_15_name: str | None = ...,
        angle_factor_15: float | None = ...,
        surface_16_name: str | None = ...,
        angle_factor_16: float | None = ...,
        surface_17_name: str | None = ...,
        angle_factor_17: float | None = ...,
        surface_18_name: str | None = ...,
        angle_factor_18: float | None = ...,
        surface_19_name: str | None = ...,
        angle_factor_19: float | None = ...,
        surface_20_name: str | None = ...,
        angle_factor_20: float | None = ...,
        surface_21_name: str | None = ...,
        angle_factor_21: float | None = ...,
        surface_22_name: str | None = ...,
        angle_factor_22: float | None = ...,
        surface_23_name: str | None = ...,
        angle_factor_23: float | None = ...,
        surface_24_name: str | None = ...,
        angle_factor_24: float | None = ...,
        surface_25_name: str | None = ...,
        angle_factor_25: float | None = ...,
        surface_26_name: str | None = ...,
        angle_factor_26: float | None = ...,
        surface_27_name: str | None = ...,
        angle_factor_27: float | None = ...,
        surface_28_name: str | None = ...,
        angle_factor_28: float | None = ...,
        surface_29_name: str | None = ...,
        angle_factor_29: float | None = ...,
        surface_30_name: str | None = ...,
        angle_factor_30: float | None = ...,
        surface_31_name: str | None = ...,
        angle_factor_31: float | None = ...,
        surface_32_name: str | None = ...,
        angle_factor_32: float | None = ...,
        surface_33_name: str | None = ...,
        angle_factor_33: float | None = ...,
        surface_34_name: str | None = ...,
        angle_factor_34: float | None = ...,
        surface_35_name: str | None = ...,
        angle_factor_35: float | None = ...,
        surface_36_name: str | None = ...,
        angle_factor_36: float | None = ...,
        surface_37_name: str | None = ...,
        angle_factor_37: float | None = ...,
        surface_38_name: str | None = ...,
        angle_factor_38: float | None = ...,
        surface_39_name: str | None = ...,
        angle_factor_39: float | None = ...,
        surface_40_name: str | None = ...,
        angle_factor_40: float | None = ...,
        surface_41_name: str | None = ...,
        angle_factor_41: float | None = ...,
        surface_42_name: str | None = ...,
        angle_factor_42: float | None = ...,
        surface_43_name: str | None = ...,
        angle_factor_43: float | None = ...,
        surface_44_name: str | None = ...,
        angle_factor_44: float | None = ...,
        surface_45_name: str | None = ...,
        angle_factor_45: float | None = ...,
        surface_46_name: str | None = ...,
        angle_factor_46: float | None = ...,
        surface_47_name: str | None = ...,
        angle_factor_47: float | None = ...,
        surface_48_name: str | None = ...,
        angle_factor_48: float | None = ...,
        surface_49_name: str | None = ...,
        angle_factor_49: float | None = ...,
        surface_50_name: str | None = ...,
        angle_factor_50: float | None = ...,
        surface_51_name: str | None = ...,
        angle_factor_51: float | None = ...,
        surface_52_name: str | None = ...,
        angle_factor_52: float | None = ...,
        surface_53_name: str | None = ...,
        angle_factor_53: float | None = ...,
        surface_54_name: str | None = ...,
        angle_factor_54: float | None = ...,
        surface_55_name: str | None = ...,
        angle_factor_55: float | None = ...,
        surface_56_name: str | None = ...,
        angle_factor_56: float | None = ...,
        surface_57_name: str | None = ...,
        angle_factor_57: float | None = ...,
        surface_58_name: str | None = ...,
        angle_factor_58: float | None = ...,
        surface_59_name: str | None = ...,
        angle_factor_59: float | None = ...,
        surface_60_name: str | None = ...,
        angle_factor_60: float | None = ...,
        surface_61_name: str | None = ...,
        angle_factor_61: float | None = ...,
        surface_62_name: str | None = ...,
        angle_factor_62: float | None = ...,
        surface_63_name: str | None = ...,
        angle_factor_63: float | None = ...,
        surface_64_name: str | None = ...,
        angle_factor_64: float | None = ...,
        surface_65_name: str | None = ...,
        angle_factor_65: float | None = ...,
        surface_66_name: str | None = ...,
        angle_factor_66: float | None = ...,
        surface_67_name: str | None = ...,
        angle_factor_67: float | None = ...,
        surface_68_name: str | None = ...,
        angle_factor_68: float | None = ...,
        surface_69_name: str | None = ...,
        angle_factor_69: float | None = ...,
        surface_70_name: str | None = ...,
        angle_factor_70: float | None = ...,
        surface_71_name: str | None = ...,
        angle_factor_71: float | None = ...,
        surface_72_name: str | None = ...,
        angle_factor_72: float | None = ...,
        surface_73_name: str | None = ...,
        angle_factor_73: float | None = ...,
        surface_74_name: str | None = ...,
        angle_factor_74: float | None = ...,
        surface_75_name: str | None = ...,
        angle_factor_75: float | None = ...,
        surface_76_name: str | None = ...,
        angle_factor_76: float | None = ...,
        surface_77_name: str | None = ...,
        angle_factor_77: float | None = ...,
        surface_78_name: str | None = ...,
        angle_factor_78: float | None = ...,
        surface_79_name: str | None = ...,
        angle_factor_79: float | None = ...,
        surface_80_name: str | None = ...,
        angle_factor_80: float | None = ...,
        surface_81_name: str | None = ...,
        angle_factor_81: float | None = ...,
        surface_82_name: str | None = ...,
        angle_factor_82: float | None = ...,
        surface_83_name: str | None = ...,
        angle_factor_83: float | None = ...,
        surface_84_name: str | None = ...,
        angle_factor_84: float | None = ...,
        surface_85_name: str | None = ...,
        angle_factor_85: float | None = ...,
        surface_86_name: str | None = ...,
        angle_factor_86: float | None = ...,
        surface_87_name: str | None = ...,
        angle_factor_87: float | None = ...,
        surface_88_name: str | None = ...,
        angle_factor_88: float | None = ...,
        surface_89_name: str | None = ...,
        angle_factor_89: float | None = ...,
        surface_90_name: str | None = ...,
        angle_factor_90: float | None = ...,
        surface_91_name: str | None = ...,
        angle_factor_91: float | None = ...,
        surface_92_name: str | None = ...,
        angle_factor_92: float | None = ...,
        surface_93_name: str | None = ...,
        angle_factor_93: float | None = ...,
        surface_94_name: str | None = ...,
        angle_factor_94: float | None = ...,
        surface_95_name: str | None = ...,
        angle_factor_95: float | None = ...,
        surface_96_name: str | None = ...,
        angle_factor_96: float | None = ...,
        surface_97_name: str | None = ...,
        angle_factor_97: float | None = ...,
        surface_98_name: str | None = ...,
        angle_factor_98: float | None = ...,
        surface_99_name: str | None = ...,
        angle_factor_99: float | None = ...,
        surface_100_name: str | None = ...,
        angle_factor_100: float | None = ...,
    ) -> None:
        """Create a new ``ComfortViewFactorAngles`` and add it to the document.

        Used to specify radiant view factors for thermal comfort calculations. Note that the following angle factor fractions must sum up to 1.0 All surfaces must be in the same enclosure.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-internal-gains-people-lights-other/#comfortviewfactorangles
        """

class MeterCustom_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Water",
        ]
        | None = ...,
        variable_details: list[_g.MeterCustomVariableDetailsItem] = ...,
    ) -> None:
        """Create a new ``Meter:Custom`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:Custom cannot reference another Meter:Custom.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-simulation-parameters/#metercustom
        """

class HeatPumpWaterToWaterEIRCooling_v9_1_to_v9_2:
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
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EIR:Cooling`` and add it to the document.

        An EIR formulated water to water heat pump model, cooling operation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.
        """

class CoilCoolingDXCurveFitOperatingMode_v22_2_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        speed_1_name: str,
        rated_gross_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_evaporator_air_flow_rate: float | Literal["Autosize"] | None = ...,
        rated_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        apply_latent_degradation_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        nominal_evaporative_condenser_pump_power: float | Literal["", "Autosize"] | None = 0,
        nominal_speed_number: int | None = ...,
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

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitoperatingmode
        """

class HeatPumpPlantLoopEIRCooling_v9_3_to_v23_1:
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
        condenser_type: Literal["", "AirSource", "WaterSource"] | None = "WaterSource",
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``HeatPump:PlantLoop:EIR:Cooling`` and add it to the document.

        An EIR formulated water to water heat pump model, cooling operation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-plant-equipment/#heatpumpplantloopeircooling
        """
