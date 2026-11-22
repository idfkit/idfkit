"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SizingZone_v22_2_to_v24_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_or_zonelist_name: str,
        zone_cooling_design_supply_air_humidity_ratio: float,
        zone_heating_design_supply_air_humidity_ratio: float,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = ...,
        zone_cooling_design_supply_air_temperature_difference: float | None = ...,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = ...,
        zone_heating_design_supply_air_temperature_difference: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        cooling_design_air_flow_method: Literal["DesignDay", "DesignDayWithLimit", "Flow/Zone"] | None = "DesignDay",
        cooling_design_air_flow_rate: float | None = 0,
        cooling_minimum_air_flow_per_zone_floor_area: float | None = 0.000762,
        cooling_minimum_air_flow: float | None = 0,
        cooling_minimum_air_flow_fraction: float | None = 0.2,
        heating_design_air_flow_method: Literal["DesignDay", "DesignDayWithLimit", "Flow/Zone"] | None = "DesignDay",
        heating_design_air_flow_rate: float | None = 0,
        heating_maximum_air_flow_per_zone_floor_area: float | None = 0.002032,
        heating_maximum_air_flow: float | None = 0.1415762,
        heating_maximum_air_flow_fraction: float | None = 0.3,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        account_for_dedicated_outdoor_air_system: Literal["No", "Yes"] | None = "No",
        dedicated_outdoor_air_system_control_strategy: Literal[
            "ColdSupplyAir", "NeutralDehumidifiedSupplyAir", "NeutralSupplyAir"
        ]
        | None = "NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design: float | Literal["Autosize"] | None = "Autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design: float | Literal["Autosize"] | None = "Autosize",
        zone_load_sizing_method: Literal[
            "Latent Load", "Sensible And Latent Load", "Sensible Load", "Sensible Load Only No Latent Load"
        ]
        | None = "Sensible Load Only No Latent Load",
        zone_latent_cooling_design_supply_air_humidity_ratio_input_method: Literal[
            "HumidityRatioDifference", "SupplyAirHumidityRatio"
        ]
        | None = "HumidityRatioDifference",
        zone_dehumidification_design_supply_air_humidity_ratio: float | None = ...,
        zone_cooling_design_supply_air_humidity_ratio_difference: float | None = 0.005,
        zone_latent_heating_design_supply_air_humidity_ratio_input_method: Literal[
            "HumidityRatioDifference", "SupplyAirHumidityRatio"
        ]
        | None = "HumidityRatioDifference",
        zone_humidification_design_supply_air_humidity_ratio: float | None = ...,
        zone_humidification_design_supply_air_humidity_ratio_difference: float | None = 0.005,
        zone_humidistat_dehumidification_set_point_schedule_name: str | None = ...,
        zone_humidistat_humidification_set_point_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Sizing:Zone`` and add it to the document.

        Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, heating, and ventilation air flows are then saved for system level and zone component design calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-design-objects/#sizingzone
        """

class HeaderedPumpsConstantSpeed_v9_1_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: float | None = ...,
        flow_sequencing_control_scheme: Literal["Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``HeaderedPumps:ConstantSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-pumps/#headeredpumpsconstantspeed
        """

class PhotovoltaicPerformanceEquivalentOneDiode_v8_9_to_v22_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        cell_type: Literal["AmorphousSilicon", "CrystallineSilicon"] | None = ...,
        number_of_cells_in_series: float | None = 36,
        active_area: float | None = 0.89,
        transmittance_absorptance_product: float | None = 0.95,
        semiconductor_bandgap: float | None = 1.12,
        shunt_resistance: float | None = 1000000,
        short_circuit_current: float | None = 6.5,
        open_circuit_voltage: float | None = 21.6,
        reference_temperature: float | None = 25,
        reference_insolation: float | None = 1000,
        module_current_at_maximum_power: float | None = 5.9,
        module_voltage_at_maximum_power: float | None = 17,
        temperature_coefficient_of_short_circuit_current: float | None = 0.02,
        temperature_coefficient_of_open_circuit_voltage: float | None = -0.079,
        nominal_operating_cell_temperature_test_ambient_temperature: float | None = 20,
        nominal_operating_cell_temperature_test_cell_temperature: float | None = 40,
        nominal_operating_cell_temperature_test_insolation: float | None = 800,
        module_heat_loss_coefficient: float | None = 30,
        total_heat_capacity: float | None = 50000,
        validate: bool = True,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:EquivalentOne-Diode`` and add it to the document.

        Describes the performance characteristics of Photovoltaic (PV) modules to be modeled using an equivalent one-diode circuit. This model is also known as the 4- or 5-parameter TRNSYS model for photovoltaics.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformanceequivalentone-diode
        """

class WindowPropertyShadingControl_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
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
        construction_with_shading_name: str | None = ...,
        schedule_name: str | None = ...,
        setpoint: float | None = ...,
        shading_control_is_scheduled: Literal["No", "Yes"] | None = "No",
        glare_control_is_active: Literal["No", "Yes"] | None = "No",
        shading_device_material_name: str | None = ...,
        type_of_slat_angle_control_for_blinds: Literal["BlockBeamSolar", "FixedSlatAngle", "ScheduledSlatAngle"]
        | None = "FixedSlatAngle",
        slat_angle_schedule_name: str | None = ...,
        setpoint_2: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowProperty:ShadingControl`` and add it to the document.

        Specifies the type, location, and controls for window shades, window blinds, and switchable glazing. Referenced by the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).
        """

class RoomAirTemperaturePatternNondimensionalHeight_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: float,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        pairs: Sequence[
            _g.RoomAirTemperaturePatternNondimensionalHeightPairsItem
            | _g.RoomAirTemperaturePatternNondimensionalHeightPairsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:NondimensionalHeight`` and add it to the document.

        Defines a distribution pattern for air temperatures relative to the current mean air temperature as a function of height. The height, referred to as Zeta, is nondimensional by normalizing with the zone ceiling height. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        ``pairs`` takes the extensible groups in order, one dict per group:

        ```python
        doc["RoomAir:TemperaturePattern:NondimensionalHeight"].add(
            "RoomAir TemperaturePattern NondimensionalHeight 1",
            control_integer_for_pattern_control_schedule_name=0.0,
            pairs=[
                {"pair_zeta_nondimensional_height": 0.0, "pair_delta_adjacent_air_temperature": 0.0},
                {"pair_zeta_nondimensional_height": 0.0, "pair_delta_adjacent_air_temperature": 0.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-room-air-models/#roomairtemperaturepatternnondimensionalheight
        """

class ConstructionAirBoundary_v9_2_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        solar_and_daylighting_method: Literal["GroupedZones", "InteriorWindow"] | None = "GroupedZones",
        radiant_exchange_method: Literal["GroupedZones", "IRTSurface"] | None = "GroupedZones",
        air_exchange_method: Literal["None", "SimpleMixing"] | None = "None",
        simple_mixing_air_changes_per_hour: float | None = 0.5,
        simple_mixing_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Construction:AirBoundary`` and add it to the document.

        Indicates an open boundary between two zones. It may be used for base surfaces and fenestration surfaces. When this construction type is used, the Outside Boundary Condition of the surface (or the base surface of a fenestration surface) must be either Surface or Zone. A base surface with Construction:AirBoundary cannot hold any fenestration surfaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-surface-construction-elements/#constructionairboundary
        """
