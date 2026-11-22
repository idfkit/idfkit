"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class DemandManagerExteriorLights_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: float | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: float | None = ...,
        lights: Sequence[_g.DemandManagerExteriorLightsLightsItem | _g.DemandManagerExteriorLightsLightsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``DemandManager:ExteriorLights`` and add it to the document.

        used for demand limiting Exterior:Lights objects.

        ``lights`` takes the extensible groups in order, one dict per group:

        ```python
        doc["DemandManager:ExteriorLights"].add(
            "DemandManager ExteriorLights 1",
            limit_control="Fixed",
            selection_control="All",
            lights=[
                {"exterior_lights_name": "Exterior Lights 1"},
                {"exterior_lights_name": "Exterior Lights 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-demand-limiting-controls/#demandmanagerexteriorlights
        """

class TableMultiVariableLookup_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        interpolation_method: Literal[
            "EvaluateCurveToLimits", "LagrangeInterpolationLinearExtrapolation", "LinearInterpolationOfTable"
        ]
        | None = "LagrangeInterpolationLinearExtrapolation",
        number_of_interpolation_points: float | None = 3,
        curve_type: Literal[
            "BiCubic",
            "BiQuadratic",
            "Cubic",
            "Exponent",
            "Linear",
            "Other",
            "Quadratic",
            "QuadraticLinear",
            "Quartic",
            "TriQuadratic",
        ]
        | None = ...,
        table_data_format: Literal["SingleLineIndependentVariableWithMatrix"]
        | None = "SingleLineIndependentVariableWithMatrix",
        external_file_name: str | None = ...,
        x1_sort_order: Literal["Ascending", "Descending"] | None = "Ascending",
        x2_sort_order: Literal["Ascending", "Descending"] | None = "Ascending",
        normalization_reference: float | None = ...,
        minimum_value_of_x1: float | None = ...,
        maximum_value_of_x1: float | None = ...,
        minimum_value_of_x2: float | None = ...,
        maximum_value_of_x2: float | None = ...,
        minimum_value_of_x3: float | None = ...,
        maximum_value_of_x3: float | None = ...,
        minimum_value_of_x4: float | None = ...,
        maximum_value_of_x4: float | None = ...,
        minimum_value_of_x5: float | None = ...,
        maximum_value_of_x5: float | None = ...,
        minimum_value_of_x6: float | None = ...,
        maximum_value_of_x6: float | None = ...,
        minimum_table_output: float | None = ...,
        maximum_table_output: float | None = ...,
        input_unit_type_for_x1: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x2: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x3: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x4: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x5: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x6: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        number_of_independent_variables: float | None = ...,
        number_of_values_for_independent_variable_x1: float | None = ...,
        field_1_determined_by_the_number_of_independent_variables: float | None = ...,
        field_2_determined_by_the_number_of_independent_variables: float | None = ...,
        values: Sequence[
            _vd.TableMultiVariableLookupValuesItem_v8_9 | _vd.TableMultiVariableLookupValuesGroup_v8_9
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Table:MultiVariableLookup`` and add it to the document.

        The multi-variable lookup table can represent from 1 to 6 independent variables and can interpolate these independent variables up to a 4th order polynomial. The polynomial order is assumed to be the number of interpolation points (n) minus 1. When any independent variable value is outside the table limits, linear extrapolation is used to predict the table result and is based on the two nearest data points in the table for that particular independent variable.

        ``values`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Table:MultiVariableLookup"].add(
            "Table MultiVariableLookup 1",
            values=[
                {"field_determined_by_the_number_of_independent_variables": 0.0},
                {"field_determined_by_the_number_of_independent_variables": 0.0},
            ],
        )
        ```
        """

class CoilCoolingWaterDetailedGeometry_v8_9_to_v9_5:
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
        maximum_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        tube_outside_surface_area: float | Literal["Autosize"] | None = "Autosize",
        total_tube_inside_area: float | Literal["Autosize"] | None = "Autosize",
        fin_surface_area: float | Literal["Autosize"] | None = "Autosize",
        minimum_airflow_area: float | Literal["Autosize"] | None = "Autosize",
        coil_depth: float | Literal["Autosize"] | None = "Autosize",
        fin_diameter: float | Literal["Autosize"] | None = "Autosize",
        fin_thickness: float | None = 0.0015,
        tube_inside_diameter: float | None = 0.01445,
        tube_outside_diameter: float | None = 0.0159,
        tube_thermal_conductivity: float | None = 386,
        fin_thermal_conductivity: float | None = 204,
        fin_spacing: float | None = 0.0018,
        tube_depth_spacing: float | None = 0.026,
        number_of_tube_rows: float | None = 4,
        number_of_tubes_per_row: float | Literal["Autosize"] | None = "Autosize",
        condensate_collection_water_storage_tank_name: str | None = ...,
        design_water_temperature_difference: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:Water:DetailedGeometry`` and add it to the document.

        Chilled water cooling coil, detailed flat fin coil model for continuous plate fins, with inputs for detailed coil geometry specifications.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwaterdetailedgeometry
        """
