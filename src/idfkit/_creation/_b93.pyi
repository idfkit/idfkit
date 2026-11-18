"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ZonePropertyUserViewFactorsBySurfaceName:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str | None = ...,
        view_factors: Sequence[
            _g.ZonePropertyUserViewFactorsBySurfaceNameViewFactorsItem
            | _g.ZonePropertyUserViewFactorsBySurfaceNameViewFactorsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneProperty:UserViewFactors:BySurfaceName`` and add it to the document.

        View factors for Surface to Surface in a zone. (Number of Surfaces)**2 are expected. Any omitted surface pairs will be assumed to have a view factor of zero.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#zonepropertyuserviewfactorsbysurfacename
        """

class AnyHVACTemplateZonePTAC:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cooling_cop: float | None = 3,
        heating_coil_type: Literal["Electric", "Gas", "HotWater"] | None = "Electric",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:PTAC`` and add it to the document.

        Packaged Terminal Air Conditioner

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezoneptac
        """

class CoilHeatingWaterToAirHeatPumpEquationFit:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        heating_capacity_curve_name: str,
        heating_power_consumption_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        rated_entering_water_temperature: float | None = 20,
        rated_entering_air_dry_bulb_temperature: float | None = 20,
        ratio_of_rated_heating_capacity_to_rated_cooling_capacity: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpequationfit
        """

class AnyLoadProfilePlant:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        load_schedule_name: str,
        peak_flow_rate: float,
        flow_rate_fraction_schedule_name: str,
        validate: bool = True,
    ) -> None:
        """Create a new ``LoadProfile:Plant`` and add it to the document.

        Used to simulate a scheduled plant loop demand profile. Load and flow rate are specified using schedules. Positive values are heating loads, and negative values are cooling loads. The actual load met is dependent on the performance of the supply loop components. Optional inputs for steam loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-non-zone-equipment/#loadprofileplant
        """

class ThermalStorageChilledWaterMixed:
    def __call__(
        self,
        name: str,
        /,
        *,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_volume: float | None = 0.1,
        setpoint_temperature_schedule_name: str | None = ...,
        deadband_temperature_difference: float | None = 0.5,
        minimum_temperature_limit: float | None = ...,
        nominal_cooling_capacity: float | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        heat_gain_coefficient_from_ambient_temperature: float | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_heat_transfer_effectiveness: float | None = 1,
        use_side_availability_schedule_name: str | None = ...,
        use_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_heat_transfer_effectiveness: float | None = 1,
        source_side_availability_schedule_name: str | None = ...,
        source_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        tank_recovery_time: float | None = 4,
        validate: bool = True,
    ) -> None:
        """Create a new ``ThermalStorage:ChilledWater:Mixed`` and add it to the document.

        Chilled water storage with a well-mixed, single-node tank. The chilled water is 'used' by drawing from the 'Use Side' of the water tank. The tank is indirectly charged by circulating cold water through the 'Source Side' of the water tank.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragechilledwatermixed
        """

class AnyAvailabilityManagerOptimumStart:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_type: Literal["ControlZone", "MaximumofZoneList", "StayOff"] | None = "ControlZone",
        control_zone_name: str | None = ...,
        zone_list_name: str | None = ...,
        maximum_value_for_optimum_start_time: float | None = 6,
        control_algorithm: Literal[
            "AdaptiveASHRAE", "AdaptiveTemperatureGradient", "ConstantStartTime", "ConstantTemperatureGradient"
        ]
        | None = "AdaptiveASHRAE",
        constant_temperature_gradient_during_cooling: float | None = ...,
        constant_temperature_gradient_during_heating: float | None = ...,
        initial_temperature_gradient_during_cooling: float | None = ...,
        initial_temperature_gradient_during_heating: float | None = ...,
        constant_start_time: float | None = ...,
        number_of_previous_days: int | None = 2,
        validate: bool = True,
    ) -> None:
        """Create a new ``AvailabilityManager:OptimumStart`` and add it to the document.

        Determines the optimal start of HVAC systems before occupancy.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanageroptimumstart
        """
