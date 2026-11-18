"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class WindowMaterialGasMixture_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        thickness: float,
        number_of_gases_in_mixture: float,
        gas_1_type: Literal["Air", "Argon", "Krypton", "Xenon"],
        gas_1_fraction: float,
        gas_2_type: Literal["Air", "Argon", "Krypton", "Xenon"],
        gas_2_fraction: float,
        gas_3_type: Literal["Air", "Argon", "Krypton", "Xenon"] | None = ...,
        gas_3_fraction: float | None = ...,
        gas_4_type: Literal["Air", "Argon", "Krypton", "Xenon"] | None = ...,
        gas_4_fraction: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowMaterial:GasMixture`` and add it to the document.

        Gas mixtures that are used in Windows or Glass Doors

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#windowmaterialgasmixture
        """

class GroundHeatExchangerPond_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        pond_depth: float,
        pond_area: float,
        hydronic_tubing_inside_diameter: float,
        hydronic_tubing_outside_diameter: float,
        hydronic_tubing_thermal_conductivity: float,
        ground_thermal_conductivity: float,
        number_of_tubing_circuits: float,
        length_of_each_tubing_circuit: float,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Pond`` and add it to the document.

        A model of a shallow pond with immersed pipe loops. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#groundheatexchangerpond
        """

class OutputMeter_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "Annual", "Daily", "Detailed", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Meter`` and add it to the document.

        Each Output:Meter command picks meters to be put onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. A list of meters that can be reported are available after a run on the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-output-reporting/#outputmeter
        """
