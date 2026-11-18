"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class OutputTableTimeBins_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        variable_name: str,
        key_value: str | None = "*",
        interval_start: float | None = ...,
        interval_size: float | None = ...,
        interval_count: float | None = ...,
        schedule_name: str | None = ...,
        variable_type: Literal["Energy", "Power", "Temperature", "VolumetricFlow"] | None = ...,
    ) -> None:
        """Create a new ``Output:Table:TimeBins`` and add it to the document.

        Produces a bin report in the table output file which shows the amount of time in hours that occurs in different bins for a single specific output variable or meter. Two different types of binning are reported: by month and by hour of the day.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/standard-output-reports/output-table-timebins/#outputtabletimebins
        """

class OutputControlSurfaceColorScheme_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        drawing_element_1_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_1: float | None = ...,
        drawing_element_2_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_2: float | None = ...,
        drawing_element_3_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_3: float | None = ...,
        drawing_element_4_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_4: float | None = ...,
        drawing_element_5_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_5: float | None = ...,
        drawing_element_6_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_6: float | None = ...,
        drawing_element_7_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_7: float | None = ...,
        drawing_element_8_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_8: float | None = ...,
        drawing_element_9_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_9: float | None = ...,
        drawing_element_10_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_10: float | None = ...,
        drawing_element_11_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_11: float | None = ...,
        drawing_element_12_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_12: float | None = ...,
        drawing_element_13_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_13: float | None = ...,
        drawing_element_14_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_14: float | None = ...,
        drawing_element_15_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_15: float | None = ...,
    ) -> None:
        """Create a new ``OutputControl:SurfaceColorScheme`` and add it to the document.

        This object is used to set colors for reporting on various building elements particularly for the DXF reports. We know the user can enter 0 to 255 and the color map is available in DXF output. Therefore, we are limiting the colors in that range. You can extend by editing the IDD but you do so on your own. Colors not changed in any scheme will remain as the default scheme uses.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/input-for-output/#outputcontrolsurfacecolorscheme
        """

class TableTwoIndependentVariables_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        curve_type: Literal["BiQuadratic", "QuadraticLinear"],
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
