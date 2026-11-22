"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import versioned as _vd

class OutputTableAnnual_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        filter: str | None = ...,
        schedule_name: str | None = ...,
        variable_details: Sequence[
            _vd.OutputTableAnnualVariableDetailsItem_v8_9_to_v22_1
            | _vd.OutputTableAnnualVariableDetailsGroup_v8_9_to_v22_1
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Table:Annual`` and add it to the document.

        Provides a generic method of setting up tables of annual results with one row per object. The report has multiple columns that are each defined using a repeated group of fields for any number of columns. A single Output:Table:Annual produces a single table in the output.

        ``variable_details`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Output:Table:Annual"].add(
            "Output Table Annual 1",
            variable_details=[
                {
                    "variable_or_meter_or_ems_variable_or_field_name": "Variable or Meter or EMS Variable or Field 1",
                    "aggregation_type_for_variable_or_meter": "HourInTenBinsMinToMax",
                    "digits_after_decimal": 2.0,
                },
                {
                    "variable_or_meter_or_ems_variable_or_field_name": "Variable or Meter or EMS Variable or Field 2",
                    "aggregation_type_for_variable_or_meter": "HourInTenBinsMinToZero",
                    "digits_after_decimal": 2.0,
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/standard-output-reports/output-table-annual/#outputtableannual
        """

class GroundHeatExchangerHorizontalTrench_v8_9_to_v22_1:
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
        number_of_trenches: float | None = 1,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#groundheatexchangerhorizontaltrench
        """
