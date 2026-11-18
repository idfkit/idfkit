"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ConvergenceLimits:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        minimum_system_timestep: int | None = ...,
        maximum_hvac_iterations: int | None = 20,
        minimum_plant_iterations: int | None = 2,
        maximum_plant_iterations: int | None = 8,
        validate: bool = True,
    ) -> None:
        """Create a new ``ConvergenceLimits`` and add it to the document.

        Specifies limits on HVAC system simulation timesteps and iterations. This item is an advanced feature that should be used only with caution.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#convergencelimits
        """

class Space:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        ceiling_height: float | Literal["Autocalculate"] | None = "Autocalculate",
        volume: float | Literal["Autocalculate"] | None = "Autocalculate",
        floor_area: float | Literal["Autocalculate"] | None = "Autocalculate",
        space_type: str | None = "General",
        construction_assignment_set_name: str | None = ...,
        tags: Sequence[_g.SpaceTagsItem | _g.SpaceTagsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Space`` and add it to the document.

        Defines a space (room) in the building. All Spaces are part of a Zone. Every Zone contains one or more spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will be created. If some surfaces in a Zone are assigned to a space and some are not, then a default Space named <Zone Name>-Remainder will be created. Input references to Space Names must have a matching Space object (default space names may not be referenced except in output variable keys).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#space
        """

class GroundHeatTransferSlabMaterials:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        nmat_number_of_materials: float,
        albedo_surface_albedo_no_snow: float | None = 0.16,
        albedo_surface_albedo_snow: float | None = 0.4,
        epslw_surface_emissivity_no_snow: float | None = 0.94,
        epslw_surface_emissivity_snow: float | None = 0.86,
        z0_surface_roughness_no_snow: float | None = 0.75,
        z0_surface_roughness_snow: float | None = 0.25,
        hin_indoor_hconv_downward_flow: float | None = 6.13,
        hin_indoor_hconv_upward: float | None = 9.26,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:Materials`` and add it to the document.

        Object gives an overall description of the slab ground heat transfer model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabmaterials
        """

class RoomAirNodeAirflowNetworkHVACEquipment:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        equipment_fractions: Sequence[
            _g.RoomAirNodeAirflowNetworkHVACEquipmentEquipmentFractionsItem
            | _g.RoomAirNodeAirflowNetworkHVACEquipmentEquipmentFractionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork:HVACEquipment`` and add it to the document.

        define the zone equipment associated with one particular RoomAir:Node

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetworkhvacequipment
        """

class AnySizingPlant:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        plant_or_condenser_loop_name: str,
        loop_type: Literal["Condenser", "Cooling", "Heating", "Steam"],
        design_loop_exit_temperature: float,
        loop_design_temperature_difference: float,
        sizing_option: Literal["Coincident", "NonCoincident"] | None = "NonCoincident",
        zone_timesteps_in_averaging_window: int | None = 1,
        coincident_sizing_factor_mode: Literal[
            "GlobalCoolingSizingFactor", "GlobalHeatingSizingFactor", "LoopComponentSizingFactor", "None"
        ]
        | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Sizing:Plant`` and add it to the document.

        Specifies the input needed to autosize plant loop flow rates and equipment capacities. This information is initially used by components that use water for heating or cooling such as hot or chilled water coils to calculate their maximum water flow rates. These flow rates are then summed for use in calculating the Plant Loop flow rates.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingplant
        """

class ZoneHVACOutdoorAirUnitEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_1_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
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
            "AirLoopHVAC:UnitarySystem",
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
            "AirLoopHVAC:UnitarySystem",
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
            "AirLoopHVAC:UnitarySystem",
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
            "AirLoopHVAC:UnitarySystem",
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
            "AirLoopHVAC:UnitarySystem",
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
            "AirLoopHVAC:UnitarySystem",
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
            "AirLoopHVAC:UnitarySystem",
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
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:OutdoorAirUnit:EquipmentList`` and add it to the document.

        Equipment list for components in a ZoneHVAC:OutdoorAirUnit. Components are simulated sequentially in the order given in the equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacoutdoorairunitequipmentlist
        """

class ZoneHVACBaseboardConvectiveElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        efficiency: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:Convective:Electric`` and add it to the document.

        Electric baseboard heater, convection-only. Natural convection electric heating unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardconvectiveelectric
        """

class CoilPerformanceDXCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        gross_rated_cooling_cop: float | None = 3,
        fraction_of_air_flow_bypassed_around_coil: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = 0,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``CoilPerformance:DX:Cooling`` and add it to the document.

        Used to specify DX cooling coil performance for one mode of operation for a Coil:Cooling:DX:TwoStageWithHumidityControlMode object which may reference one to four CoilPerformance:DX:Cooling objects depending on the specified number of stages and dehumidification modes. In nearly all cases, the Rated Air Flow Rate will be the same for all performance objects associated with a given coil. If bypass is specified, the Rated Air Flow Rate includes both the bypassed flow and the flow through the active part of the coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilperformancedxcooling
        """

class SolarCollectorPerformanceFlatPlate:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_area: float,
        test_flow_rate: float,
        test_correlation_type: Literal["Average", "Inlet", "Outlet"],
        coefficient_1_of_efficiency_equation: float,
        coefficient_2_of_efficiency_equation: float,
        test_fluid: Literal["Water"] | None = "Water",
        coefficient_3_of_efficiency_equation: float | None = ...,
        coefficient_2_of_incident_angle_modifier: float | None = ...,
        coefficient_3_of_incident_angle_modifier: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:FlatPlate`` and add it to the document.

        Thermal and optical performance parameters for a single flat plate solar collector module. These parameters are based on the testing methodologies described in ASHRAE Standards 93 and 96 which are used Solar Rating and Certification Corporation (SRCC) Directory of SRCC Certified Solar Collector Ratings. See EnergyPlus DataSets file SolarCollectors.idf.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformanceflatplate
        """

class AnyCoolingTowerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_fan_power: float | Literal["Autosize"],
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        nominal_capacity: float | None = ...,
        free_convection_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        capacity_control: Literal["FanCycling", "FluidBypass"] | None = "FanCycling",
        number_of_cells: int | None = 1,
        cell_control: Literal["MaximalCell", "MinimalCell"] | None = ...,
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``CoolingTower:SingleSpeed`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a single-speed fan drawing air through the tower (induced-draft configuration). Added fluid bypass as an additional capacity control. 8/2008. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowersinglespeed
        """
