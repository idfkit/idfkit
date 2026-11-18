"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class Lights:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal["LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        fraction_replaceable: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_fraction_calculated_from_plenum_temperature: Literal["No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
        return_air_heat_gain_node_name: str | None = ...,
        exhaust_air_heat_gain_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Lights`` and add it to the document.

        Sets internal gains for lights in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#lights
        """

class CoilHeatingSteam:
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
        maximum_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        degree_of_subcooling: float | None = ...,
        degree_of_loop_subcooling: float | None = 20,
        coil_control_type: Literal["TemperatureSetpointControl", "ZoneLoadControl"] | None = ...,
        temperature_setpoint_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Steam`` and add it to the document.

        Steam heating coil. Condenses and sub-cools steam at loop pressure and discharges condensate through steam traps to low pressure condensate line.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingsteam
        """

class FluidCoolerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_entering_water_temperature: float,
        design_entering_air_temperature: float,
        design_entering_air_wetbulb_temperature: float,
        design_water_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate_fan_power: float | Literal["Autosize"],
        performance_input_method: Literal["NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "NominalCapacity",
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        nominal_capacity: float | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
    ) -> None:
        """Create a new ``FluidCooler:SingleSpeed`` and add it to the document.

        The fluid cooler is modeled as a cross flow heat exchanger (both streams unmixed) with single-speed fans (induced draft configuration).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#fluidcoolersinglespeed
        """

class AnyGroundHeatExchangerResponseFactors:
    def __call__(
        self,
        name: str,
        /,
        *,
        ghe_vertical_properties_object_name: str,
        number_of_boreholes: int,
        g_function_reference_ratio: float | None = 0.0005,
        g_functions: Sequence[
            _g.GroundHeatExchangerResponseFactorsGFunctionsItem | _g.GroundHeatExchangerResponseFactorsGFunctionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:ResponseFactors`` and add it to the document.

        Response factor definitions from third-party tool, commonly referred to a 'g-functions'

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerresponsefactors
        """
