"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ScheduleDayList:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        interpolate_to_timestep: Literal["Average", "Linear", "No"] | None = "No",
        minutes_per_item: int | None = ...,
        extensions: Sequence[_g.ScheduleDayListExtensionsItem | _g.ScheduleDayListExtensionsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Schedule:Day:List`` and add it to the document.

        Schedule:Day:List will allow the user to list 24 hours worth of values, which can be sub-hourly in nature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduledaylist
        """

class MaterialNoMass:
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
        thermal_absorptance_inside_face: float | None = ...,
        solar_absorptance_inside_face: float | None = ...,
        visible_absorptance_inside_face: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Material:NoMass`` and add it to the document.

        Regular materials properties described whose principal description is R (Thermal Resistance)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialnomass
        """

class AnyWallExterior:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Wall:Exterior`` and add it to the document.

        Allows for simplified entry of exterior walls. View Factor to Ground is automatically calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#wallexterior
        """

class AnyCeilingAdiabatic:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Ceiling:Adiabatic`` and add it to the document.

        Allows for simplified entry of interior ceilings.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#ceilingadiabatic
        """

class FenestrationSurfaceDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal[
            "Door",
            "FixedWindow",
            "GlassDoor",
            "OperableWindow",
            "OverheadDoor",
            "Skylight",
            "TubularDaylightDiffuser",
            "TubularDaylightDome",
            "Window",
        ],
        building_surface_name: str,
        vertex_1_x_coordinate: float,
        vertex_1_y_coordinate: float,
        vertex_1_z_coordinate: float,
        vertex_2_x_coordinate: float,
        vertex_2_y_coordinate: float,
        vertex_2_z_coordinate: float,
        vertex_3_x_coordinate: float,
        vertex_3_y_coordinate: float,
        vertex_3_z_coordinate: float,
        construction_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        view_factor_to_ground: float | Literal["Autocalculate"] | None = "Autocalculate",
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertex_4_x_coordinate: float | None = ...,
        vertex_4_y_coordinate: float | None = ...,
        vertex_4_z_coordinate: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``FenestrationSurface:Detailed`` and add it to the document.

        Allows for detailed entry of subsurfaces (windows, doors, glass doors, tubular daylighting devices).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#fenestrationsurfacedetailed
        """

class ThermostatSetpointThermalComfortFangerSingleHeating:
    def __call__(self, name: str, /, *, fanger_thermal_comfort_schedule_name: str, validate: bool = True) -> None:
        """Create a new ``ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating`` and add it to the document.

        Used for heating only thermal comfort control. The PMV setpoint can be scheduled and varied throughout the simulation but only heating is allowed with this control type.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointthermalcomfortfangersingleheating
        """

class AnyGroundHeatExchangerHorizontalTrench:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        trench_length_in_pipe_axial_direction: float | None = 50,
        number_of_trenches: int | None = 1,
        horizontal_spacing_between_pipes: float | None = 1,
        pipe_inner_diameter: float | None = 0.016,
        pipe_outer_diameter: float | None = 0.026,
        burial_depth: float | None = 1.5,
        soil_thermal_conductivity: float | None = 1.08,
        soil_density: float | None = 962,
        soil_specific_heat: float | None = 2576,
        pipe_thermal_conductivity: float | None = 0.3895,
        pipe_density: float | None = 641,
        pipe_specific_heat: float | None = 2405,
        soil_moisture_content_percent: float | None = 30,
        soil_moisture_content_percent_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:HorizontalTrench`` and add it to the document.

        This models a horizontal heat exchanger placed in a series of trenches The model uses the PipingSystem:Underground underlying algorithms, but provides a more usable input interface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerhorizontaltrench
        """

class AnyOutputTableAnnual:
    def __call__(
        self,
        name: str,
        /,
        *,
        filter: str | None = ...,
        schedule_name: str | None = ...,
        variable_details: Sequence[
            _g.AnyOutputTableAnnualVariableDetailsItem | _g.AnyOutputTableAnnualVariableDetailsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Table:Annual`` and add it to the document.

        Provides a generic method of setting up tables of annual results with one row per object. The report has multiple columns that are each defined using a repeated group of fields for any number of columns. A single Output:Table:Annual produces a single table in the output.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-annual/#outputtableannual
        """
