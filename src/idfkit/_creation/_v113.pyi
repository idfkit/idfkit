"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class HVACSystemRootFindingAlgorithm_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        algorithm: Literal[
            "", "Alternation", "Bisection", "BisectionThenRegulaFalsi", "RegulaFalsi", "RegulaFalsiThenBisection"
        ]
        | None = "RegulaFalsi",
        number_of_iterations_before_algorithm_switch: float | None = 5,
    ) -> None:
        """Create a new ``HVACSystemRootFindingAlgorithm`` and add it to the document.

        Specifies a HVAC system solver algorithm to find a root

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-simulation-parameters/#hvacsystemrootfindingalgorithm
        """

class ZoneAirMassFlowConservation_v8_9_to_v9_4:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        adjust_zone_mixing_for_zone_air_mass_flow_balance: Literal["", "No", "Yes"] | None = "No",
        infiltration_balancing_method: Literal["", "AddInfiltrationFlow", "AdjustInfiltrationFlow", "None"]
        | None = "AddInfiltrationFlow",
        infiltration_balancing_zones: Literal["", "AllZones", "MixingSourceZonesOnly"] | None = "MixingSourceZonesOnly",
    ) -> None:
        """Create a new ``ZoneAirMassFlowConservation`` and add it to the document.

        Enforces the zone air mass flow balance by adjusting zone mixing object and/or infiltration object mass flow rates. If either mixing or infiltration is active, then the zone air mass flow balance calculation will attempt to enforce conservation of mass for each zone. If mixing is 'No' and infiltration is 'None', then the zone air mass flow calculation defaults to assume self-balanced simple flow mixing and infiltration objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-airflow/#zoneairmassflowconservation
        """

class Zone_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        direction_of_relative_north: float | None = 0,
        x_origin: float | None = 0,
        y_origin: float | None = 0,
        z_origin: float | None = 0,
        type: float | None = 1,
        multiplier: float | None = 1,
        ceiling_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        volume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        floor_area: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        zone_inside_convection_algorithm: Literal[
            "", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP", "TrombeWall"
        ]
        | None = ...,
        zone_outside_convection_algorithm: Literal[
            "", "AdaptiveConvectionAlgorithm", "DOE-2", "MoWiTT", "SimpleCombined", "TARP"
        ]
        | None = ...,
        part_of_total_floor_area: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Zone`` and add it to the document.

        Defines a thermal zone of the building.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-thermal-zone-description-geometry/#zone
        """

class ConstructionInternalSource_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_present_after_layer_number: float,
        temperature_calculation_requested_after_layer_number: float,
        dimensions_for_the_ctf_calculation: float,
        tube_spacing: float,
        outside_layer: str,
        layer_2: str | None = ...,
        layer_3: str | None = ...,
        layer_4: str | None = ...,
        layer_5: str | None = ...,
        layer_6: str | None = ...,
        layer_7: str | None = ...,
        layer_8: str | None = ...,
        layer_9: str | None = ...,
        layer_10: str | None = ...,
    ) -> None:
        """Create a new ``Construction:InternalSource`` and add it to the document.

        Start with outside layer and work your way to the inside Layer Up to 10 layers total, 8 for windows Enter the material name for each layer
        """

class WindowShadingControl_v9_0_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        shading_type: Literal[
            "BetweenGlassBlind",
            "BetweenGlassShade",
            "ExteriorBlind",
            "ExteriorScreen",
            "ExteriorShade",
            "InteriorBlind",
            "InteriorShade",
            "SwitchableGlazing",
        ],
        shading_control_type: Literal[
            "AlwaysOff",
            "AlwaysOn",
            "MeetDaylightIlluminanceSetpoint",
            "OffNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnIfHighGlare",
            "OnIfHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighSolarOnWindow",
            "OnIfHighOutdoorAirTemperature",
            "OnIfHighSolarOnWindow",
            "OnIfHighZoneAirTempAndHighHorizontalSolar",
            "OnIfHighZoneAirTempAndHighSolarOnWindow",
            "OnIfHighZoneAirTemperature",
            "OnIfHighZoneCooling",
            "OnIfScheduleAllows",
            "OnNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnNightIfHeatingAndOffDay",
            "OnNightIfHeatingAndOnDayIfCooling",
            "OnNightIfLowInsideTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOnDayIfCooling",
        ],
        shading_control_sequence_number: float | None = 1,
        construction_with_shading_name_: str | None = ...,
        schedule_name: str | None = ...,
        setpoint: float | None = ...,
        shading_control_is_scheduled: Literal["", "No", "Yes"] | None = "No",
        glare_control_is_active: Literal["", "No", "Yes"] | None = "No",
        shading_device_material_name: str | None = ...,
        type_of_slat_angle_control_for_blinds: Literal["", "BlockBeamSolar", "FixedSlatAngle", "ScheduledSlatAngle"]
        | None = "FixedSlatAngle",
        slat_angle_schedule_name: str | None = ...,
        setpoint_2: float | None = ...,
        daylighting_control_object_name: str | None = ...,
        multiple_surface_control_type: Literal["", "Group", "Sequential"] | None = "Sequential",
        fenestration_surfaces: Sequence[
            _g.WindowShadingControlFenestrationSurfacesItem | _g.WindowShadingControlFenestrationSurfacesGroup
        ] = ...,
    ) -> None:
        """Create a new ``WindowShadingControl`` and add it to the document.

        Specifies the type, location, and controls for window shades, window blinds, and switchable glazing. Referencing the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-thermal-zone-description-geometry/#windowshadingcontrol
        """

class EvaporativeFluidCoolerSingleSpeed_v8_9_to_v22_1:
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
        ]
        | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        standard_design_capacity: float | None = ...,
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        user_specified_design_capacity: float | None = ...,
        design_entering_water_temperature: float | None = ...,
        design_entering_air_temperature: float | None = ...,
        design_entering_air_wet_bulb_temperature: float | None = ...,
        capacity_control: Literal["", "FanCycling", "FluidBypass"] | None = "FanCycling",
        sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``EvaporativeFluidCooler:SingleSpeed`` and add it to the document.

        This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#evaporativefluidcoolersinglespeed
        """
