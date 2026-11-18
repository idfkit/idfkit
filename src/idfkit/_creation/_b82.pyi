"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class SizingPeriodWeatherFileDays:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
        day_of_week_for_start_day: Literal[
            "",
            "CustomDay1",
            "CustomDay2",
            "Friday",
            "Monday",
            "Saturday",
            "SummerDesignDay",
            "Sunday",
            "Thursday",
            "Tuesday",
            "Wednesday",
            "WinterDesignDay",
        ]
        | None = "Monday",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_rain_and_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``SizingPeriod:WeatherFileDays`` and add it to the document.

        Use a weather file period for design sizing calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sizingperiodweatherfiledays
        """

class AnyWallInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Interzone`` and add it to the document.

        Allows for simplified entry of interzone walls (walls between zones).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#wallinterzone
        """

class RoomAirSettingsThreeNodeDisplacementVentilation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        gain_distribution_schedule_name: str,
        number_of_plumes_per_occupant: float | None = 1,
        thermostat_height: float | None = 1.1,
        comfort_height: float | None = 1.1,
        temperature_difference_threshold_for_reporting: float | None = 0.4,
    ) -> None:
        """Create a new ``RoomAirSettings:ThreeNodeDisplacementVentilation`` and add it to the document.

        The UCSD model for Displacement Ventilation

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairsettingsthreenodedisplacementventilation
        """

class SizingParameters:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        heating_sizing_factor: float | None = 1,
        cooling_sizing_factor: float | None = 1,
        timesteps_in_averaging_window: int | None = ...,
    ) -> None:
        """Create a new ``Sizing:Parameters`` and add it to the document.

        Specifies global heating and cooling sizing factors/ratios. These ratios are applied at the zone level to all of the zone heating and cooling loads and air flow rates. Then these new loads and air flow rates are used to calculate the system level flow rates and capacities and are used in all component sizing calculations. Specifies the width (in load timesteps) of a moving average window which is used to smooth the peak load across more than one timestep.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingparameters
        """

class ZoneHVACLowTemperatureRadiantVariableFlowDesign:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        fluid_to_radiant_surface_heat_transfer_model: Literal["", "ConvectionOnly", "ISOStandard"]
        | None = "ConvectionOnly",
        hydronic_tubing_inside_diameter: float | None = 0.013,
        hydronic_tubing_outside_diameter: float | None = 0.016,
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
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        heating_control_throttling_range: float | None = 0.5,
        heating_control_temperature_schedule_name: str | None = ...,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        changeover_delay_time_period_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantvariableflowdesign
        """

class AnyPlantEquipmentOperationThermalEnergyStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        on_peak_schedule: str,
        charging_availability_schedule: str,
        non_charging_chilled_water_temperature: float,
        charging_chilled_water_temperature: float,
        component_1_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ],
        component_1_name: str,
        component_1_demand_calculation_node_name: str,
        component_1_setpoint_node_name: str,
        component_1_flow_rate: float | Literal["Autosize"],
        component_1_operation_type: Literal["Cooling", "Dual", "Heating"],
        component_2_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_2_demand_calculation_node_name: str | None = ...,
        component_2_setpoint_node_name: str | None = ...,
        component_2_flow_rate: float | Literal["Autosize"] | None = ...,
        component_2_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_3_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_3_demand_calculation_node_name: str | None = ...,
        component_3_setpoint_node_name: str | None = ...,
        component_3_flow_rate: float | Literal["Autosize"] | None = ...,
        component_3_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_4_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_4_demand_calculation_node_name: str | None = ...,
        component_4_setpoint_node_name: str | None = ...,
        component_4_flow_rate: float | Literal["Autosize"] | None = ...,
        component_4_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_5_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_5_demand_calculation_node_name: str | None = ...,
        component_5_setpoint_node_name: str | None = ...,
        component_5_flow_rate: float | Literal["Autosize"] | None = ...,
        component_5_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_6_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_6_demand_calculation_node_name: str | None = ...,
        component_6_setpoint_node_name: str | None = ...,
        component_6_flow_rate: float | Literal["Autosize"] | None = ...,
        component_6_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_7_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_7_demand_calculation_node_name: str | None = ...,
        component_7_setpoint_node_name: str | None = ...,
        component_7_flow_rate: float | Literal["Autosize"] | None = ...,
        component_7_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_8_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_8_name: str | None = ...,
        component_8_demand_calculation_node_name: str | None = ...,
        component_8_setpoint_node_name: str | None = ...,
        component_8_flow_rate: float | Literal["Autosize"] | None = ...,
        component_8_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_9_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_9_name: str | None = ...,
        component_9_demand_calculation_node_name: str | None = ...,
        component_9_setpoint_node_name: str | None = ...,
        component_9_flow_rate: float | Literal["Autosize"] | None = ...,
        component_9_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_10_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_10_name: str | None = ...,
        component_10_demand_calculation_node_name: str | None = ...,
        component_10_setpoint_node_name: str | None = ...,
        component_10_flow_rate: float | Literal["Autosize"] | None = ...,
        component_10_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:ThermalEnergyStorage`` and add it to the document.

        Plant equipment operation scheme for simpler input to control thermal (ice) energy storage systems. It replaces a host of setpoint managers with simple, single input values. For more complex controls, use the ComponentSetpoint scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationthermalenergystorage
        """

class GeneratorMicroCHP:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        performance_parameters_name: str | None = ...,
        zone_name: str | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        generator_fuel_supply_name: str | None = ...,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:MicroCHP`` and add it to the document.

        Small-scale combined heat and power (micro CHP) electric generator using the model developed by IEA/ECBCS Annex 42 see www.cogen-sim.net. The model was developed for both internal combustion and Stirling cycle engines, but might be used for other types of residential CHP devices.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatormicrochp
        """
