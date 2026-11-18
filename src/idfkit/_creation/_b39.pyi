"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class WindowsCalculationEngine:
    def __call__(
        self,
        /,
        *,
        windows_engine: Literal["BuiltInWindowsModel", "ExternalWindowsModel"] | None = "BuiltInWindowsModel",
    ) -> None:
        """Create a new ``WindowsCalculationEngine`` and add it to the document.

        Describes which window model will be used in calculations. Built in windows model will use algorithms that are part of EnergyPlus, while ExternalWindowsModel will use Windows-CalcEngine library to perform optical and thermal performances of windows and doors.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowscalculationengine
        """

class WallUnderground:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Underground`` and add it to the document.

        Allows for simplified entry of underground walls.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#wallunderground
        """

class AirflowNetworkMultiZoneComponentHorizontalOpening:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_opening_is_closed: float,
        discharge_coefficient: float,
        air_mass_flow_exponent_when_opening_is_closed: float | None = 0.65,
        sloping_plane_angle: float | None = 90,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Component:HorizontalOpening`` and add it to the document.

        This object specifies the properties of air flow through a horizontal opening

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonecomponenthorizontalopening
        """

class SetpointManagerOutdoorAirReset:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_at_outdoor_low_temperature: float,
        outdoor_low_temperature: float,
        setpoint_at_outdoor_high_temperature: float,
        outdoor_high_temperature: float,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["MaximumTemperature", "MinimumTemperature", "Temperature"] | None = "Temperature",
        schedule_name: str | None = ...,
        setpoint_at_outdoor_low_temperature_2: float | None = ...,
        outdoor_low_temperature_2: float | None = ...,
        setpoint_at_outdoor_high_temperature_2: float | None = ...,
        outdoor_high_temperature_2: float | None = ...,
    ) -> None:
        """Create a new ``SetpointManager:OutdoorAirReset`` and add it to the document.

        This Setpoint Manager is used to place a setpoint temperature on system node according to the outdoor air temperature using a reset rule. The outdoor air temperature is obtained from the weather information during the simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanageroutdoorairreset
        """

class GeneratorPVWatts:
    def __call__(
        self,
        name: str,
        /,
        *,
        dc_system_capacity: float,
        module_type: Literal["Premium", "Standard", "ThinFilm"],
        array_type: Literal["FixedOpenRack", "FixedRoofMounted", "OneAxis", "OneAxisBacktracking", "TwoAxis"],
        pvwatts_version: Literal["5"] | None = ...,
        system_losses: float | None = 0.14,
        array_geometry_type: Literal["Surface", "TiltAzimuth"] | None = "TiltAzimuth",
        tilt_angle: float | None = 20,
        azimuth_angle: float | None = 180,
        surface_name: str | None = ...,
        ground_coverage_ratio: float | None = 0.4,
    ) -> None:
        """Create a new ``Generator:PVWatts`` and add it to the document.

        Describes a simple set of inputs for an array of photovoltaic (PV) modules as described in the PVWatts software. A series of different PVWatts arrays can be connected to a single electric load center (preferably through an ElectricLoadCenter:Inverter:PVWatts). Array tilt and azimuth can be either specified on this object or taken from a referenced building surface or shading surface. If a surface is specified, the array participates normally in all shading calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorpvwatts
        """

class AnyTableLookup:
    def __call__(
        self,
        name: str,
        /,
        *,
        independent_variable_list_name: str,
        normalization_method: Literal["AutomaticWithDivisor", "DivisorOnly", "None"] | None = "None",
        normalization_divisor: float | None = 1,
        minimum_output: float | None = ...,
        maximum_output: float | None = ...,
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: int | None = ...,
        external_file_starting_row_number: int | None = ...,
        values: Sequence[_g.TableLookupValuesItem | _g.TableLookupValuesGroup] = ...,
    ) -> None:
        """Create a new ``Table:Lookup`` and add it to the document.

        Lookup tables are used in place of curves and can represent any number of independent variables (defined as Table:IndependentVariable objects in a Table:IndependentVariableList). Output values are interpolated within the bounds defined by each independent variable and extrapolated beyond the bounds according to the interpolation/extrapolation methods defined by each independent variable.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-tables/#tablelookup
        """
