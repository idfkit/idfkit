"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SiteGroundTemperatureUndisturbedKusudaAchenbach:
    def __call__(
        self,
        name: str,
        /,
        *,
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        average_soil_surface_temperature: float | None = ...,
        average_amplitude_of_surface_temperature: float | None = ...,
        phase_shift_of_minimum_surface_temperature: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Site:GroundTemperature:Undisturbed:KusudaAchenbach`` and add it to the document.

        Undisturbed ground temperature object using the Kusuda-Achenbach 1965 correlation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperatureundisturbedkusudaachenbach
        """

class SurfacePropertyExposedFoundationPerimeter:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        surface_name: str,
        exposed_perimeter_calculation_method: Literal["BySegment", "ExposedPerimeterFraction", "TotalExposedPerimeter"],
        total_exposed_perimeter: float | None = ...,
        exposed_perimeter_fraction: float | None = ...,
        surfaces: Sequence[
            _g.SurfacePropertyExposedFoundationPerimeterSurfacesItem
            | _g.SurfacePropertyExposedFoundationPerimeterSurfacesGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SurfaceProperty:ExposedFoundationPerimeter`` and add it to the document.

        Defines the perimeter of a foundation floor that is exposed to the exterior environment through the floor. User may either define the total exposed perimeter, fraction of perimeter exposed or individually define which segments of the floor surface perimeter are exposed.

        ``surfaces`` takes the extensible groups in order, one dict per group:

        ```python
        doc["SurfaceProperty:ExposedFoundationPerimeter"].add(
            surface_name="Surface 1",
            exposed_perimeter_calculation_method="BySegment",
            surfaces=[
                {"surface_segment_exposed": "Yes"},
                {"surface_segment_exposed": "Yes"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyexposedfoundationperimeter
        """

class SurfaceConvectionAlgorithmInsideUserCurve:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        reference_temperature_for_convection_heat_transfer: Literal[
            "AdjacentAirTemperature", "MeanAirTemperature", "SupplyAirTemperature"
        ]
        | None = ...,
        hc_function_of_temperature_difference_curve_name: str | None = ...,
        hc_function_of_temperature_difference_divided_by_height_curve_name: str | None = ...,
        hc_function_of_air_change_rate_curve_name: str | None = ...,
        hc_function_of_air_system_volume_flow_rate_divided_by_zone_perimeter_length_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Inside:UserCurve`` and add it to the document.

        Used to describe a custom model equation for surface convection heat transfer coefficient If more than one curve is referenced they are all used and added together.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfaceconvectionalgorithminsideusercurve
        """

class DaylightingReferencePoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        x_coordinate_of_reference_point: float,
        y_coordinate_of_reference_point: float,
        z_coordinate_of_reference_point: float | None = 0.8,
        validate: bool = True,
    ) -> None:
        """Create a new ``Daylighting:ReferencePoint`` and add it to the document.

        Used by Daylighting:Controls to identify the reference point coordinates for each sensor. Reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingreferencepoint
        """

class OutputDaylightFactors:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        reporting_days: Literal["AllShadowCalculationDays", "SizingDays"],
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:DaylightFactors`` and add it to the document.

        Reports hourly daylight factors for each exterior window for four sky types (clear, turbid clear, intermediate, and overcast).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputdaylightfactors
        """

class HVACTemplatePlantBoilerObjectReference:
    def __call__(
        self,
        name: str,
        /,
        *,
        boiler_name: str,
        boiler_object_type: Literal["Boiler:HotWater"] | None = "Boiler:HotWater",
        priority: float | None = ...,
        template_plant_loop_type: Literal["HotWater", "MixedWater"] | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Boiler:ObjectReference`` and add it to the document.

        This object references a detailed boiler object and adds it to an HVACTemplate:Plant:HotWaterLoop or MixedWaterLoop. The user must create a complete detailed boiler object with all required curve or performance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantboilerobjectreference
        """

class AnyCoilHeatingDXSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_capacity_function_of_temperature_curve_name: str,
        heating_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = 0,
        region_number_for_calculating_hspf: int | None = 4,
        evaporator_air_inlet_node_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Heating:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric compressor and outdoor fan), single-speed, with defrost controls.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxsinglespeed
        """

class SetpointManagerColdest:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["Temperature"] | None = "Temperature",
        minimum_setpoint_temperature: float | None = 20,
        maximum_setpoint_temperature: float | None = 50,
        strategy: Literal["MinimumTemperature"] | None = "MinimumTemperature",
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:Coldest`` and add it to the document.

        This SetpointManager is used in dual duct systems to reset the setpoint temperature of the air in the heating supply duct. Usually it is used in conjunction with a SetpointManager:Warmest resetting the temperature of the air in the cooling supply duct.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagercoldest
        """

class RefrigerationCaseAndWalkInList:
    def __call__(
        self,
        name: str,
        /,
        *,
        cases_and_walkins: Sequence[
            _g.RefrigerationCaseAndWalkInListCasesAndWalkinsItem | _g.RefrigerationCaseAndWalkInListCasesAndWalkinsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:CaseAndWalkInList`` and add it to the document.

        Provides a list of all the refrigerated cases, walk in coolers, or air chillers cooled by a single refrigeration system. Note that the names of all cases, walk-ins ,air chillers, and CaseAndWalkInLists must be unique. That is, you cannot give a list the same name as one of list items. This list may contain a combination of case and walk-in names OR a list of air chiller names. Air chillers may not be included in any list that also includes cases or walk-ins.

        ``cases_and_walkins`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Refrigeration:CaseAndWalkInList"].add(
            "Refrigeration CaseAndWalkInList 1",
            cases_and_walkins=[
                {"case_or_walkin_name": "Case or WalkIn 1"},
                {"case_or_walkin_name": "Case or WalkIn 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcaseandwalkinlist
        """

class TableIndependentVariableList:
    def __call__(
        self,
        name: str,
        /,
        *,
        independent_variables: Sequence[
            _g.TableIndependentVariableListIndependentVariablesItem
            | _g.TableIndependentVariableListIndependentVariablesGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Table:IndependentVariableList`` and add it to the document.

        A sorted list of independent variables used by one or more Table:Lookup objects.

        ``independent_variables`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Table:IndependentVariableList"].add(
            "Table IndependentVariableList 1",
            independent_variables=[
                {"independent_variable_name": "Independent Variable 1"},
                {"independent_variable_name": "Independent Variable 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-tables/#tableindependentvariablelist
        """
