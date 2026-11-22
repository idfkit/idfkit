"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class MaterialInfraredTransparent:
    def __call__(self, name: str, /, *, validate: bool = True) -> None:
        """Create a new ``Material:InfraredTransparent`` and add it to the document.

        Special infrared transparent material. Similar to a Material:Nomass with low thermal resistance. High absorptance in both wavelengths. Area will be doubled internally to make internal radiant exchange accurate. Should be only material in single layer surface construction. All thermal properties are set internally. User needs only to supply name. Cannot be used with ConductionFiniteDifference solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialinfraredtransparent
        """

class GlobalGeometryRules:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        starting_vertex_position: Literal["LowerLeftCorner", "LowerRightCorner", "UpperLeftCorner", "UpperRightCorner"],
        vertex_entry_direction: Literal["Clockwise", "Counterclockwise"],
        coordinate_system: Literal["Relative", "World"],
        daylighting_reference_point_coordinate_system: Literal["Relative", "World"] | None = "Relative",
        rectangular_surface_coordinate_system: Literal["Relative", "World"] | None = "Relative",
        validate: bool = True,
    ) -> None:
        """Create a new ``GlobalGeometryRules`` and add it to the document.

        Specifies the geometric rules used to describe the input of surface vertices and daylighting reference points.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#globalgeometryrules
        """

class AnyRoofCeilingDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Surface",
            "Zone",
        ],
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.RoofCeilingDetailedVerticesItem | _g.RoofCeilingDetailedVerticesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoofCeiling:Detailed`` and add it to the document.

        Allows for detailed entry of roof/ceiling heat transfer surfaces.

        ``vertices`` takes the extensible groups in order, one dict per group:

        ```python
        doc["RoofCeiling:Detailed"].add(
            "RoofCeiling Detailed 1",
            construction_name="Construction 1",
            zone_name="Zone 1",
            outside_boundary_condition="Outdoors",
            vertices=[
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#roofceilingdetailed
        """

class RoomAirSettingsOneNodeDisplacementVentilation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        fraction_of_convective_internal_loads_added_to_floor_air: float | None = ...,
        fraction_of_infiltration_internal_loads_added_to_floor_air: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAirSettings:OneNodeDisplacementVentilation`` and add it to the document.

        The Mundt model for displacement ventilation

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairsettingsonenodedisplacementventilation
        """

class CoilSystemCoolingWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        run_on_sensible_load: Literal["No", "Yes"] | None = "Yes",
        run_on_latent_load: Literal["No", "Yes"] | None = "No",
        minimum_air_to_water_temperature_offset: float | None = 0,
        economizer_lockout: Literal["No", "Yes"] | None = "Yes",
        minimum_water_loop_temperature_for_heat_recovery: float | None = 0,
        companion_coil_used_for_heat_recovery: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:Water`` and add it to the document.

        Virtual container component that consists of a water cooling coil and its associated controls. This control object supports the available water coil types and may be placed directly on an air loop branch or in an outdoor air equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingwater
        """

class CoilCoolingDXCurveFitOperatingMode:
    def __call__(
        self,
        name: str,
        /,
        *,
        speed_1_name: str,
        rated_gross_total_cooling_capacity: float | Literal["Autosize"] | None = "Autosize",
        rated_evaporator_air_flow_rate: float | Literal["Autosize"] | None = ...,
        rated_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["No", "Yes"] | None = "No",
        apply_latent_degradation_to_speeds_greater_than_1: Literal["No", "Yes"] | None = "No",
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        nominal_evaporative_condenser_pump_power: float | Literal["Autosize"] | None = 0,
        nominal_speed_number: int | None = ...,
        speed_2_name: str | None = ...,
        speed_3_name: str | None = ...,
        speed_4_name: str | None = ...,
        speed_5_name: str | None = ...,
        speed_6_name: str | None = ...,
        speed_7_name: str | None = ...,
        speed_8_name: str | None = ...,
        speed_9_name: str | None = ...,
        speed_10_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:OperatingMode`` and add it to the document.

        DX cooling coil performance for a single operating mode which may have one or more speeds.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitoperatingmode
        """

class AnyWaterHeaterSizing:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        waterheater_name: str,
        design_mode: Literal[
            "PeakDraw", "PerFloorArea", "PerPerson", "PerSolarCollectorArea", "PerUnit", "ResidentialHUD-FHAMinimum"
        ]
        | None = ...,
        time_storage_can_meet_peak_draw: float | None = ...,
        time_for_tank_recovery: float | None = ...,
        nominal_tank_volume_for_autosizing_plant_connections: float | None = ...,
        number_of_bedrooms: int | None = ...,
        number_of_bathrooms: int | None = ...,
        storage_capacity_per_person: float | None = ...,
        recovery_capacity_per_person: float | None = ...,
        storage_capacity_per_floor_area: float | None = ...,
        recovery_capacity_per_floor_area: float | None = ...,
        number_of_units: float | None = ...,
        storage_capacity_per_unit: float | None = ...,
        recovery_capacity_perunit: float | None = ...,
        storage_capacity_per_collector_area: float | None = ...,
        height_aspect_ratio: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WaterHeater:Sizing`` and add it to the document.

        This input object is used with WaterHeater:Mixed or with WaterHeater:Stratified to autosize tank volume and heater capacity This object is not needed if water heaters are not autosized.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#waterheatersizing
        """

class AnyTableIndependentVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        interpolation_method: Literal["Cubic", "Linear"] | None = "Linear",
        extrapolation_method: Literal["Constant", "Linear"] | None = "Constant",
        minimum_value: float | None = ...,
        maximum_value: float | None = ...,
        normalization_reference_value: float | None = ...,
        unit_type: Literal["Angle", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: int | None = ...,
        external_file_starting_row_number: int | None = ...,
        values: Sequence[_g.TableIndependentVariableValuesItem | _g.TableIndependentVariableValuesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Table:IndependentVariable`` and add it to the document.

        An independent variable representing a single dimension of a Table:Lookup object.

        ``values`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Table:IndependentVariable"].add(
            "Table IndependentVariable 1",
            values=[
                {"value": 0.0},
                {"value": 0.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-tables/#tableindependentvariable
        """

class OutputEnergyManagementSystem:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        actuator_availability_dictionary_reporting: Literal["None", "NotByUniqueKeyNames", "Verbose"] | None = "None",
        internal_variable_availability_dictionary_reporting: Literal["None", "NotByUniqueKeyNames", "Verbose"]
        | None = "None",
        ems_runtime_language_debug_output_level: Literal["ErrorsOnly", "None", "Verbose"] | None = "None",
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:EnergyManagementSystem`` and add it to the document.

        This object is used to control the output produced by the Energy Management System

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputenergymanagementsystem
        """

class OutputTableReportPeriod:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: int,
        begin_day_of_month: int,
        begin_hour_of_day: int,
        end_month: int,
        end_day_of_month: int,
        end_hour_of_day: int,
        report_name: Literal[
            "AllResilienceSummaries", "CO2ResilienceSummary", "ThermalResilienceSummary", "VisualResilienceSummary"
        ]
        | None = ...,
        begin_year: int | None = ...,
        end_year: int | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Table:ReportPeriod`` and add it to the document.

        This object allows the user to generate the resilience tabular reports over a subset of a run period. When it is defined, a series of reporting-period-specific resilience summary tables will be generated at the end of all tabular reports. Multiple reporting periods may be input.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-reportperiod/#outputtablereportperiod
        """
