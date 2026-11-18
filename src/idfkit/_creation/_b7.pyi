"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ZoneHVACCoolingPanelRadiantConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        maximum_chilled_water_flow_rate: float | Literal["Autosize"],
        fraction_radiant: float,
        rated_inlet_water_temperature: float | None = 5,
        rated_inlet_space_temperature: float | None = 24,
        rated_water_mass_flow_rate: float | None = 0.063,
        cooling_design_capacity_method: Literal[
            "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        control_type: Literal[
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "ZoneConvectiveLoad",
            "ZoneTotalLoad",
        ]
        | None = "MeanAirTemperature",
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: Sequence[
            _g.ZoneHVACCoolingPanelRadiantConvectiveWaterSurfaceFractionsItem
            | _g.ZoneHVACCoolingPanelRadiantConvectiveWaterSurfaceFractionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:CoolingPanel:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaccoolingpanelradiantconvectivewater
        """

class PipingSystemUndergroundPipeSegment:
    def __call__(
        self,
        name: str,
        /,
        *,
        x_position: float,
        y_position: float,
        flow_direction: Literal["DecreasingZ", "IncreasingZ"],
        validate: bool = True,
    ) -> None:
        """Create a new ``PipingSystem:Underground:PipeSegment`` and add it to the document.

        The pipe segment to be used in an underground piping system This object represents a single pipe leg positioned axially in the local z-direction, at a given x, y location in the domain

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipingsystemundergroundpipesegment
        """

class AnyEnvironmentalImpactFactors:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        district_cooling_cop: float | None = 3,
        total_carbon_equivalent_emission_factor_from_n2o: float | None = 80.7272,
        total_carbon_equivalent_emission_factor_from_ch4: float | None = 6.2727,
        total_carbon_equivalent_emission_factor_from_co2: float | None = 0.2727,
        validate: bool = True,
    ) -> None:
        """Create a new ``EnvironmentalImpactFactors`` and add it to the document.

        Used to help convert district and ideal energy use to a fuel type and provide total carbon equivalent with coefficients Also used in Source=>Site conversions.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#environmentalimpactfactors
        """

class EnvironmentalImpactFactors:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        district_heating_water_efficiency: float | None = 0.3,
        district_cooling_cop: float | None = 3,
        district_heating_steam_conversion_efficiency: float | None = 0.25,
        total_carbon_equivalent_emission_factor_from_n2o: float | None = 80.7272,
        total_carbon_equivalent_emission_factor_from_ch4: float | None = 6.2727,
        total_carbon_equivalent_emission_factor_from_co2: float | None = 0.2727,
        validate: bool = True,
    ) -> None:
        """Create a new ``EnvironmentalImpactFactors`` and add it to the document.

        Used to help convert district and ideal energy use to a fuel type and provide total carbon equivalent with coefficients Also used in Source=>Site conversions.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#environmentalimpactfactors
        """
