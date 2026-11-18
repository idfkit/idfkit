"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyWeatherPropertySkyTemperature:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#weatherpropertyskytemperature
        """

class AnyMaterialNoMass:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thermal_resistance: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
    ) -> None:
        """Create a new ``Material:NoMass`` and add it to the document.

        Regular materials properties described whose principal description is R (Thermal Resistance)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialnomass
        """

class AnyRoomAirNodeAirflowNetworkHVACEquipment:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        equipment_fractions: Sequence[
            _g.AnyRoomAirNodeAirflowNetworkHVACEquipmentEquipmentFractionsItem
            | _g.AnyRoomAirNodeAirflowNetworkHVACEquipmentEquipmentFractionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork:HVACEquipment`` and add it to the document.

        define the zone equipment associated with one particular RoomAir:Node

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetworkhvacequipment
        """

class SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink:
    def __call__(
        self, name: str, /, *, surface_name: str, schedule_name: str, deposition_velocity: float | None = ...
    ) -> None:
        """Create a new ``SurfaceContaminantSourceAndSink:Generic:DepositionVelocitySink`` and add it to the document.

        Simulate generic contaminant source driven by the boundary layer diffusion controlled model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#surfacecontaminantsourceandsinkgenericdepositionvelocitysink
        """

class OutputIlluminanceMap:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        z_height: float | None = 0,
        x_minimum_coordinate: float | None = 0,
        x_maximum_coordinate: float | None = 1,
        number_of_x_grid_points: int | None = 2,
        y_minimum_coordinate: float | None = 0,
        y_maximum_coordinate: float | None = 1,
        number_of_y_grid_points: int | None = 2,
    ) -> None:
        """Create a new ``Output:IlluminanceMap`` and add it to the document.

        reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#outputilluminancemap
        """

class AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea:
    def __call__(
        self,
        name: str,
        /,
        *,
        effective_leakage_area: float,
        discharge_coefficient: float | None = 1,
        reference_pressure_difference: float | None = 4,
        air_mass_flow_exponent: float | None = 0.65,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Surface:EffectiveLeakageArea`` and add it to the document.

        This object is used to define surface air leakage.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonesurfaceeffectiveleakagearea
        """

class AnyAirTerminalSingleDuctSeriesPIUReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_air_flow_rate: float | Literal["Autosize"],
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_inlet_node_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:SeriesPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, series powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductseriespiureheat
        """

class AnyCoilHeatingWaterToAirHeatPumpParameterEstimation:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        compressor_type: Literal["Reciprocating", "Rotary", "Scroll"],
        design_source_side_flow_rate: float,
        gross_rated_heating_capacity: float,
        high_pressure_cutoff: float,
        low_pressure_cutoff: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        load_side_total_heat_transfer_coefficient: float,
        superheat_temperature_at_the_evaporator_outlet: float,
        compressor_power_losses: float,
        compressor_efficiency: float,
        refrigerant_type: str | None = "R22",
        compressor_piston_displacement: float | None = ...,
        compressor_suction_discharge_pressure_drop: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        refrigerant_volume_flow_rate: float | None = ...,
        volume_ratio: float | None = ...,
        leak_rate_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_resistance1: float | None = ...,
        source_side_heat_transfer_resistance2: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:ParameterEstimation`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Parameter estimation model is a deterministic model that requires a consistent set of parameters to describe the operating conditions of the heat pump components.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpparameterestimation
        """

class AirLoopHVACOutdoorAirSystemEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_1_object_type: str,
        component_1_name: str,
        component_2_object_type: str | None = ...,
        component_2_name: str | None = ...,
        component_3_object_type: str | None = ...,
        component_3_name: str | None = ...,
        component_4_object_type: str | None = ...,
        component_4_name: str | None = ...,
        component_5_object_type: str | None = ...,
        component_5_name: str | None = ...,
        component_6_object_type: str | None = ...,
        component_6_name: str | None = ...,
        component_7_object_type: str | None = ...,
        component_7_name: str | None = ...,
        component_8_object_type: str | None = ...,
        component_8_name: str | None = ...,
        component_9_object_type: str | None = ...,
        component_9_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:OutdoorAirSystem:EquipmentList`` and add it to the document.

        List equipment in simulation order

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#airloophvacoutdoorairsystemequipmentlist
        """

class SolarCollectorUnglazedTranspired:
    def __call__(
        self,
        name: str,
        /,
        *,
        boundary_conditions_model_name: str,
        diameter_of_perforations_in_collector: float,
        distance_between_perforations_in_collector: float,
        thermal_emissivity_of_collector_surface: float,
        solar_absorbtivity_of_collector_surface: float,
        effective_overall_height_of_collector: float,
        effective_gap_thickness_of_plenum_behind_collector: float,
        effective_cross_section_area_of_plenum_behind_collector: float,
        roughness_of_collector: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        availability_schedule_name: str | None = ...,
        inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        setpoint_node_name: str | None = ...,
        zone_node_name: str | None = ...,
        free_heating_setpoint_schedule_name: str | None = ...,
        hole_layout_pattern_for_pitch: Literal["", "Square", "Triangle"] | None = "Square",
        heat_exchange_effectiveness_correlation: Literal["", "Kutscher1994", "VanDeckerHollandsBrunger2001"]
        | None = "Kutscher1994",
        ratio_of_actual_collector_surface_area_to_projected_surface_area: float | None = 1,
        collector_thickness: float | None = ...,
        effectiveness_for_perforations_with_respect_to_wind: float | None = 0.25,
        discharge_coefficient_for_openings_with_respect_to_buoyancy_driven_flow: float | None = 0.65,
        surfaces: Sequence[
            _g.SolarCollectorUnglazedTranspiredSurfacesItem | _g.SolarCollectorUnglazedTranspiredSurfacesGroup
        ] = ...,
    ) -> None:
        """Create a new ``SolarCollector:UnglazedTranspired`` and add it to the document.

        Unglazed transpired solar collector (UTSC) used to condition outdoor air. This type of collector is generally used to heat air drawn through perforated absorbers and also recover heat conducted out through the underlying surface. This object represents a single collector attached to one or more building or shading surfaces and to one or more outdoor air systems.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorunglazedtranspired
        """

class SetpointManagerMultiZoneHeatingAverage:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_temperature: float | None = 20,
        maximum_setpoint_temperature: float | None = 50,
    ) -> None:
        """Create a new ``SetpointManager:MultiZone:Heating:Average`` and add it to the document.

        This setpoint manager sets the average supply air temperature based on the heating load requirements of all controlled zones in an air loop served by a central air-conditioner.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagermultizoneheatingaverage
        """

class AnyDemandManagerThermostats:
    def __call__(
        self,
        name: str,
        /,
        *,
        reset_control: Literal["Fixed", "Off"],
        maximum_heating_setpoint_reset: float,
        maximum_cooling_setpoint_reset: float,
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_reset_duration: int | None = ...,
        reset_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        thermostats: Sequence[
            _g.DemandManagerThermostatsThermostatsItem | _g.DemandManagerThermostatsThermostatsGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManager:Thermostats`` and add it to the document.

        used for demand limiting ZoneControl:Thermostat objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerthermostats
        """
