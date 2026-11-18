"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ZoneHVACTerminalUnitVariableRefrigerantFlow_v8_9_to_v9_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        terminal_unit_air_inlet_node_name: str,
        terminal_unit_air_outlet_node_name: str,
        supply_air_fan_operating_mode_schedule_name: str,
        supply_air_fan_object_name: str,
        terminal_unit_availability_schedule: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"]
        | None = "Fan:ConstantVolume",
        outside_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outside_air_mixer_object_name: str | None = ...,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:VariableRefrigerantFlow", "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        cooling_coil_object_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:VariableRefrigerantFlow", "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        heating_coil_object_name: str | None = ...,
        zone_terminal_unit_on_parasitic_electric_energy_use: float | None = 0,
        zone_terminal_unit_off_parasitic_electric_energy_use: float | None = 0,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`` and add it to the document.

        Zone terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air heat pump). The VRF terminal units are served by an AirConditioner:VariableRefrigerantFlow system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-zone-forced-air-units/#zonehvacterminalunitvariablerefrigerantflow
        """

class WaterHeaterStratified_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float | Literal["Autosize"],
        tank_height: float | Literal["Autosize"],
        heater_1_setpoint_temperature_schedule_name: str,
        heater_2_setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        end_use_subcategory: str | None = "General",
        tank_shape: Literal["HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        heater_priority_control: Literal["MasterSlave", "Simultaneous"] | None = "MasterSlave",
        heater_1_deadband_temperature_difference: float | None = 0,
        heater_1_capacity: float | Literal["Autosize"] | None = ...,
        heater_1_height: float | None = ...,
        heater_2_deadband_temperature_difference: float | None = 0,
        heater_2_capacity: float | None = ...,
        heater_2_height: float | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        off_cycle_parasitic_height: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_height: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        skin_loss_fraction_to_zone: float | None = 1,
        off_cycle_flue_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_flue_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        use_side_inlet_height: float | None = 0,
        use_side_outlet_height: float | Literal["Autocalculate"] | None = "Autocalculate",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        source_side_inlet_height: float | Literal["Autocalculate"] | None = "Autocalculate",
        source_side_outlet_height: float | None = 0,
        inlet_mode: Literal["Fixed", "Seeking"] | None = "Fixed",
        use_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        number_of_nodes: float | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
        node_11_additional_loss_coefficient: float | None = 0,
        node_12_additional_loss_coefficient: float | None = 0,
        source_side_flow_control_mode: Literal[
            "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``WaterHeater:Stratified`` and add it to the document.

        Water heater with stratified, multi-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:*.)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-water-heaters/#waterheaterstratified
        """

class HybridModelZone_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_measured_air_temperature_schedule_name: str,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        calculate_zone_internal_thermal_mass: Literal["No", "Yes"] | None = "No",
        calculate_zone_air_infiltration_rate: Literal["No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``HybridModel:Zone`` and add it to the document.

        Zones with measured air temperature data and a range of dates. If the range of temperature measurement dates includes a leap day, the weather data should include a leap day.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-hybrid-model/#hybridmodelzone
        """

class AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"],
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:Electric:MultiStage",
            "Coil:Heating:Gas:MultiStage",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:MultiSpeed"],
        cooling_coil_name: str,
        number_of_speeds_for_heating: float,
        number_of_speeds_for_cooling: float,
        heating_speed_1_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_speed_1_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_speed_2_supply_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        auxiliary_on_cycle_electric_power: float | None = 0,
        auxiliary_off_cycle_electric_power: float | None = 0,
        design_heat_recovery_water_flow_rate: float | None = 0,
        maximum_temperature_for_heat_recovery: float | None = 80,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_2_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_3_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_4_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_speed_3_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_speed_4_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed`` and add it to the document.

        Unitary system, heating and cooling, multi-speed with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (DX air-to-air heat pump, gas, electric, hot water, or steam), and supplemental heating coil (gas, electric, hot water, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoairmultispeed
        """

class ZoneHVACLowTemperatureRadiantConstantFlow_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_inside_diameter: float | None = 0.013,
        hydronic_tubing_length: float | Literal["Autosize"] | None = "Autosize",
        temperature_control_type: Literal[
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
        ]
        | None = "MeanAirTemperature",
        rated_flow_rate: float | Literal["Autosize"] | None = ...,
        pump_flow_rate_schedule_name: str | None = ...,
        rated_pump_head: float | None = 179352,
        rated_power_consumption: float | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_high_water_temperature_schedule_name: str | None = ...,
        heating_low_water_temperature_schedule_name: str | None = ...,
        heating_high_control_temperature_schedule_name: str | None = ...,
        heating_low_control_temperature_schedule_name: str | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_high_water_temperature_schedule_name: str | None = ...,
        cooling_low_water_temperature_schedule_name: str | None = ...,
        cooling_high_control_temperature_schedule_name: str | None = ...,
        cooling_low_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        number_of_circuits: Literal["CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water temperature circulating through the unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantconstantflow
        """

class IndoorLivingWall_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        schedule_name: str,
        evapotranspiration_calculation_method: Literal["Penman-Monteith", "Stanghellini"] | None = "Penman-Monteith",
        lighting_method: Literal["Daylight", "LED", "LED-Daylight"] | None = ...,
        led_intensity_schedule_name_: str | None = ...,
        daylighting_control_name: str | None = ...,
        led_daylight_targeted_lighting_intensity_schedule_name: str | None = ...,
        total_leaf_area: float | None = ...,
        led_nominal_intensity_: float | None = ...,
        led_nominal_power: float | None = ...,
        radiant_fraction_of_led_lights: float | None = 0.6,
    ) -> None:
        """Create a new ``IndoorLivingWall`` and add it to the document.

        Indoor greenery systems such as indoor living walls are panels of plants, which grow hydroponically or from substrates. The living wall structures can be either free-standing or attached to walls. The IndoorLivingWall module directly connects with inside surface heat balance, zone air heat balance, and zone air moisture balance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-internal-gains-people-lights-other/#indoorlivingwall
        """

class ZoneHVACHighTemperatureRadiant_v8_9_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        fuel_type: Literal["Electricity", "NaturalGas"],
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        combustion_efficiency: float | None = 0.9,
        fraction_of_input_converted_to_radiant_energy: float | None = 0.7,
        fraction_of_input_converted_to_latent_energy: float | None = 0,
        fraction_of_input_that_is_lost: float | None = 0,
        temperature_control_type: Literal[
            "MeanAirTemperature",
            "MeanAirTemperatureSetpoint",
            "MeanRadiantTemperature",
            "MeanRadiantTemperatureSetpoint",
            "OperativeTemperature",
            "OperativeTemperatureSetpoint",
        ]
        | None = "OperativeTemperature",
        heating_throttling_range: float | None = 2,
        heating_setpoint_temperature_schedule_name: str | None = ...,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: Sequence[
            _g.ZoneHVACHighTemperatureRadiantSurfaceFractionsItem
            | _g.ZoneHVACHighTemperatureRadiantSurfaceFractionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:HighTemperatureRadiant`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-radiative-convective-units/#zonehvachightemperatureradiant
        """
