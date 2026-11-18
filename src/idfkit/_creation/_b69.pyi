"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class GroundHeatTransferBasementMatlProps:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        nmat_number_of_materials_in_this_domain: float,
        density_for_foundation_wall: float | None = 2243,
        density_for_floor_slab: float | None = 2243,
        density_for_ceiling: float | None = 311,
        density_for_soil: float | None = 1500,
        density_for_gravel: float | None = 2000,
        density_for_wood: float | None = 449,
        specific_heat_for_foundation_wall: float | None = 880,
        specific_heat_for_floor_slab: float | None = 880,
        specific_heat_for_ceiling: float | None = 1530,
        specific_heat_for_soil: float | None = 840,
        specific_heat_for_gravel: float | None = 720,
        specific_heat_for_wood: float | None = 1530,
        thermal_conductivity_for_foundation_wall: float | None = 1.4,
        thermal_conductivity_for_floor_slab: float | None = 1.4,
        thermal_conductivity_for_ceiling: float | None = 0.09,
        thermal_conductivity_for_soil: float | None = 1.1,
        thermal_conductivity_for_gravel: float | None = 1.9,
        thermal_conductivity_for_wood: float | None = 0.12,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:MatlProps`` and add it to the document.

        Specifies the material properties for the Basement preprocessor ground heat transfer simulation. Only the Foundation Wall, Floor Slab, Soil, and Gravel properties are currently used.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementmatlprops
        """

class GroundHeatTransferBasementSurfaceProps:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        albedo_surface_albedo_for_no_snow_conditions: float | None = 0.16,
        albedo_surface_albedo_for_snow_conditions: float | None = 0.4,
        epsln_surface_emissivity_no_snow: float | None = 0.94,
        epsln_surface_emissivity_with_snow: float | None = 0.86,
        veght_surface_roughness_no_snow_conditions: float | None = 6,
        veght_surface_roughness_snow_conditions: float | None = 0.25,
        pet_flag_potential_evapotranspiration_on_: Literal["FALSE", "TRUE"] | None = "FALSE",
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:SurfaceProps`` and add it to the document.

        Specifies the soil surface properties for the Basement preprocessor ground heat transfer simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementsurfaceprops
        """

class AnyDaylightingReferencePoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        x_coordinate_of_reference_point: float,
        y_coordinate_of_reference_point: float,
        z_coordinate_of_reference_point: float | None = 0.8,
        validate: bool = True,
    ) -> None:
        """Create a new ``Daylighting:ReferencePoint`` and add it to the document.

        Used by Daylighting:Controls to identify the reference point coordinates for each sensor. Reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingreferencepoint
        """

class HVACTemplateZoneUnitary:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_unitary_system_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 12.8,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:Unitary`` and add it to the document.

        Zone terminal unit, constant volume, no controls.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezoneunitary
        """

class HVACTemplatePlantHotWaterLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        pump_schedule_name: str | None = ...,
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Intermittent",
        hot_water_plant_operation_scheme_type: Literal["Default", "UserDefined"] | None = "Default",
        hot_water_plant_equipment_operation_schemes_name: str | None = ...,
        hot_water_setpoint_schedule_name: str | None = ...,
        hot_water_design_setpoint: float | None = 82,
        hot_water_pump_configuration: Literal["ConstantFlow", "VariableFlow"] | None = "ConstantFlow",
        hot_water_pump_rated_head: float | None = 179352,
        hot_water_setpoint_reset_type: Literal["None", "OutdoorAirTemperatureReset"] | None = "None",
        hot_water_setpoint_at_outdoor_dry_bulb_low: float | None = 82.2,
        hot_water_reset_outdoor_dry_bulb_low: float | None = -6.7,
        hot_water_setpoint_at_outdoor_dry_bulb_high: float | None = 65.6,
        hot_water_reset_outdoor_dry_bulb_high: float | None = 10,
        hot_water_pump_type: Literal[
            "FiveHeaderedPumps",
            "FourHeaderedPumps",
            "PumpPerBoiler",
            "SinglePump",
            "ThreeHeaderedPumps",
            "TwoHeaderedPumps",
        ]
        | None = "SinglePump",
        supply_side_bypass_pipe: Literal["No", "Yes"] | None = "Yes",
        demand_side_bypass_pipe: Literal["No", "Yes"] | None = "Yes",
        fluid_type: Literal[
            "EthyleneGlycol30",
            "EthyleneGlycol40",
            "EthyleneGlycol50",
            "EthyleneGlycol60",
            "PropyleneGlycol30",
            "PropyleneGlycol40",
            "PropyleneGlycol50",
            "PropyleneGlycol60",
            "Water",
        ]
        | None = "Water",
        loop_design_delta_temperature: float | None = 11,
        maximum_outdoor_dry_bulb_temperature: float | None = ...,
        load_distribution_scheme: Literal[
            "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:HotWaterLoop`` and add it to the document.

        Plant loop to serve all HVACTemplate hot water coils and boilers.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplanthotwaterloop
        """

class AirTerminalSingleDuctMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        zonehvac_unit_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "ZoneHVAC:FourPipeFanCoil",
            "ZoneHVAC:PackagedTerminalAirConditioner",
            "ZoneHVAC:PackagedTerminalHeatPump",
            "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
            "ZoneHVAC:UnitVentilator",
            "ZoneHVAC:WaterToAirHeatPump",
        ],
        zonehvac_unit_object_name: str,
        mixer_outlet_node_name: str,
        mixer_primary_air_inlet_node_name: str,
        mixer_secondary_air_inlet_node_name: str,
        mixer_connection_type: Literal["InletSide", "SupplySide"],
        design_specification_outdoor_air_object_name: str | None = ...,
        per_person_ventilation_rate_mode: Literal["CurrentOccupancy", "DesignOccupancy"] | None = "CurrentOccupancy",
        validate: bool = True,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:Mixer`` and add it to the document.

        The mixer air terminal unit provides a means of supplying central system air to the air inlet or outlet side of a zoneHVAC equipment such as a four pipe fan coil unit. Normally the central air would be ventilation air from a dedicated outdoor air system (DOAS).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductmixer
        """

class LifeCycleCostNonrecurringCost:
    def __call__(
        self,
        name: str,
        /,
        *,
        category: Literal["Construction", "OtherCapital", "Salvage"] | None = "Construction",
        cost: float | None = ...,
        start_of_costs: Literal["BasePeriod", "ServicePeriod"] | None = "ServicePeriod",
        years_from_start: int | None = ...,
        months_from_start: int | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``LifeCycleCost:NonrecurringCost`` and add it to the document.

        A non-recurring cost happens only once during the study period. For costs that occur more than once during the study period on a regular schedule, use the LifeCycleCost:RecurringCost object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-nonrecurringcost/#lifecyclecostnonrecurringcost
        """
