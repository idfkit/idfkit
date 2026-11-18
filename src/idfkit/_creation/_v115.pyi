"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import versioned as _vd

class PythonPluginVariables_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        variable_name_1: str | None = ...,
        variable_name_2: str | None = ...,
        variable_name_3: str | None = ...,
        variable_name_4: str | None = ...,
        variable_name_5: str | None = ...,
    ) -> None:
        """Create a new ``PythonPlugin:Variables`` and add it to the document.

        This object defines name identifiers for custom Python Plugin variable data that should be shared among all running Python Plugins. I will make this extensible later.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-python-plugins/#pythonpluginvariables
        """

class TableTwoIndependentVariables_v9_0_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        curve_type: Literal["BiQuadratic", "QuadraticLinear"] | None = ...,
        interpolation_method: Literal[
            "", "EvaluateCurveToLimits", "LagrangeInterpolationLinearExtrapolation", "LinearInterpolationOfTable"
        ]
        | None = "LagrangeInterpolationLinearExtrapolation",
        minimum_value_of_x: float | None = ...,
        maximum_value_of_x: float | None = ...,
        minimum_value_of_y: float | None = ...,
        maximum_value_of_y: float | None = ...,
        minimum_table_output: float | None = ...,
        maximum_table_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Angle", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow", "Wavelength"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        normalization_reference: float | None = ...,
        external_file_name: str | None = ...,
        values: Sequence[
            _vd.TableTwoIndependentVariablesValuesItem_v8_9_to_v9_1
            | _vd.TableTwoIndependentVariablesValuesGroup_v8_9_to_v9_1
        ] = ...,
    ) -> None:
        """Create a new ``Table:TwoIndependentVariables`` and add it to the document.

        Allows entry of tabular data pairs as alternate input for performance curve objects. Performance curve objects can be created using these inputs. BiQuadratic Table Equation: Output = a + bX + cX**2 + dY + eY**2 + fXY BiQuadratic solution requires a minimum of 6 data pairs QuadraticLinear Table Equation: Output = a + bX + cX**2 + dY + eXY + fX**2Y QuadraticLinear solution requires a minimum of 6 data pairs
        """
