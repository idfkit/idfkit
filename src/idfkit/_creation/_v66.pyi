"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence

from .. import _generated_types as _g
from .. import versioned as _vd

class OutputTableSummaryReports_v9_3:
    def __call__(
        self,
        /,
        *,
        reports: Sequence[
            _vd.OutputTableSummaryReportsReportsItem_v9_3 | _vd.OutputTableSummaryReportsReportsGroup_v9_3
        ] = ...,
    ) -> None:
        """Create a new ``Output:Table:SummaryReports`` and add it to the document.

        This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object and appear in the same files as the tabular reports. The entries for this object is a list of the predefined reports that should appear in the tabular report output file. There should be as many fields (A) in this object as there are keys in the following (minus AllSummary+AllMonthly+AllSummaryAndMonthly)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/standard-output-reports/output-table-summaryreports/#outputtablesummaryreports
        """

class MatrixTwoDimension_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_rows: float,
        number_of_columns: float,
        values: Sequence[_g.MatrixTwoDimensionValuesItem | _g.MatrixTwoDimensionValuesGroup] = ...,
    ) -> None:
        """Create a new ``Matrix:TwoDimension`` and add it to the document.

        matrix data in row-major order list each row keeping the columns in order number of values must equal N1 x N2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#matrixtwodimension
        """
