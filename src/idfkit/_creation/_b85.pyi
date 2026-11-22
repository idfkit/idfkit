"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class WindowMaterialSimpleGlazingSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        u_factor: float,
        solar_heat_gain_coefficient: float,
        visible_transmittance: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowMaterial:SimpleGlazingSystem`` and add it to the document.

        Alternate method of describing windows This window material object is used to define an entire glazing system using simple performance parameters.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialsimpleglazingsystem
        """

class ExteriorFuelEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_use_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ],
        schedule_name: str,
        design_level: float,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Exterior:FuelEquipment`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-exterior-energy-use-equipment/#exteriorfuelequipment
        """

class ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling:
    def __call__(self, name: str, /, *, fanger_thermal_comfort_schedule_name: str, validate: bool = True) -> None:
        """Create a new ``ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling`` and add it to the document.

        Used for heating and cooling thermal comfort control with a single setpoint. The PMV setpoint can be scheduled and varied throughout the simulation for both heating and cooling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointthermalcomfortfangersingleheatingorcooling
        """

class ZoneHVACBaseboardRadiantConvectiveElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        fraction_radiant: float,
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        efficiency: float | None = 1,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: Sequence[
            _g.ZoneHVACBaseboardRadiantConvectiveElectricSurfaceFractionsItem
            | _g.ZoneHVACBaseboardRadiantConvectiveElectricSurfaceFractionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Electric`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        ``surface_fractions`` takes the extensible groups in order, one dict per group:

        ```python
        doc["ZoneHVAC:Baseboard:RadiantConvective:Electric"].add(
            "ZoneHVAC Baseboard RadiantConvective Electric 1",
            fraction_radiant=0.0,
            surface_fractions=[
                {"surface_name": "Surface 1", "fraction_of_radiant_energy_to_surface": 0.0},
                {"surface_name": "Surface 2", "fraction_of_radiant_energy_to_surface": 0.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectiveelectric
        """

class CoilCoolingWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        design_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_inlet_water_temperature: float | Literal["Autosize"] | None = "Autosize",
        design_inlet_air_temperature: float | Literal["Autosize"] | None = "Autosize",
        design_outlet_air_temperature: float | Literal["Autosize"] | None = "Autosize",
        design_inlet_air_humidity_ratio: float | Literal["Autosize"] | None = "Autosize",
        design_outlet_air_humidity_ratio: float | Literal["Autosize"] | None = "Autosize",
        type_of_analysis: Literal["DetailedAnalysis", "SimpleAnalysis"] | None = "SimpleAnalysis",
        heat_exchanger_configuration: Literal["CounterFlow", "CrossFlow"] | None = "CounterFlow",
        condensate_collection_water_storage_tank_name: str | None = ...,
        design_water_temperature_difference: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:Water`` and add it to the document.

        Chilled water cooling coil, NTU-effectiveness model, with inputs for design entering and leaving conditions.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwater
        """

class AnyEvaporativeFluidCoolerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate_fan_power: float | Literal["Autosize"],
        design_spray_water_flow_rate: float,
        performance_input_method: Literal[
            "StandardDesignCapacity", "UFactorTimesAreaAndDesignWaterFlowRate", "UserSpecifiedDesignCapacity"
        ],
        outdoor_air_inlet_node_name: str | None = ...,
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        standard_design_capacity: float | None = ...,
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        user_specified_design_capacity: float | None = ...,
        design_entering_water_temperature: float | None = ...,
        design_entering_air_temperature: float | None = ...,
        design_entering_air_wet_bulb_temperature: float | None = ...,
        capacity_control: Literal["FanCycling", "FluidBypass"] | None = "FanCycling",
        sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``EvaporativeFluidCooler:SingleSpeed`` and add it to the document.

        This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#evaporativefluidcoolersinglespeed
        """

class PlantEquipmentOperationOutdoorWetBulb:
    def __call__(
        self,
        name: str,
        /,
        *,
        wet_bulb_temperature_range_1_lower_limit: float,
        wet_bulb_temperature_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        wet_bulb_temperature_range_2_lower_limit: float | None = ...,
        wet_bulb_temperature_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_3_lower_limit: float | None = ...,
        wet_bulb_temperature_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_4_lower_limit: float | None = ...,
        wet_bulb_temperature_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_5_lower_limit: float | None = ...,
        wet_bulb_temperature_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_6_lower_limit: float | None = ...,
        wet_bulb_temperature_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_7_lower_limit: float | None = ...,
        wet_bulb_temperature_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_8_lower_limit: float | None = ...,
        wet_bulb_temperature_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_9_lower_limit: float | None = ...,
        wet_bulb_temperature_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        wet_bulb_temperature_range_10_lower_limit: float | None = ...,
        wet_bulb_temperature_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:OutdoorWetBulb`` and add it to the document.

        Plant equipment operation scheme for outdoor wet-bulb temperature range operation. Specifies one or more groups of equipment which are available to operate for successive outdoor wet-bulb temperature ranges.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationoutdoorwetbulb
        """

class RefrigerationCompressorRack:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_rack_cop_function_of_temperature_curve_name: str,
        heat_rejection_location: Literal["Outdoors", "Zone"] | None = "Outdoors",
        design_compressor_rack_cop: float | None = 2,
        design_condenser_fan_power: float | None = 250,
        condenser_fan_power_function_of_temperature_curve_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        water_cooled_condenser_inlet_node_name: str | None = ...,
        water_cooled_condenser_outlet_node_name: str | None = ...,
        water_cooled_loop_flow_type: Literal["ConstantFlow", "VariableFlow"] | None = "VariableFlow",
        water_cooled_condenser_outlet_temperature_schedule_name: str | None = ...,
        water_cooled_condenser_design_flow_rate: float | None = ...,
        water_cooled_condenser_maximum_flow_rate: float | None = ...,
        water_cooled_condenser_maximum_water_outlet_temperature: float | None = 55,
        water_cooled_condenser_minimum_water_inlet_temperature: float | None = 10,
        evaporative_condenser_availability_schedule_name: str | None = ...,
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autocalculate"] | None = "Autocalculate",
        basin_heater_capacity: float | None = 200,
        basin_heater_setpoint_temperature: float | None = 2,
        design_evaporative_condenser_water_pump_power: float | Literal["Autocalculate"] | None = 1000,
        evaporative_water_supply_tank_name: str | None = ...,
        condenser_air_inlet_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        refrigeration_case_name_or_walkin_name_or_caseandwalkinlist_name: str | None = ...,
        heat_rejection_zone_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:CompressorRack`` and add it to the document.

        Works in conjunction with the refrigeration case and walk-in objects to simulate the performance of a refrigerated case system. This object models the electric consumption of the rack compressors and the condenser fans. Heat can be rejected either outdoors or to a zone. Compressor rack waste heat can also be reclaimed for use by an optional air- or water-heating coil (Coil:Heating:Desuperheater and Coil:WaterHeating:Desuperheater).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcompressorrack
        """
