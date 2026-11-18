"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class WindowGapSupportPillar:
    def __call__(self, name: str, /, *, spacing: float | None = 0.04, radius: float | None = 0.0004) -> None:
        """Create a new ``WindowGap:SupportPillar`` and add it to the document.

        used to define pillar geometry for support pillars

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowgapsupportpillar
        """

class CeilingAdiabatic:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Ceiling:Adiabatic`` and add it to the document.

        Allows for simplified entry of interior ceilings.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#ceilingadiabatic
        """

class SurfacePropertyHeatTransferAlgorithm:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        algorithm: Literal[
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
    ) -> None:
        """Create a new ``SurfaceProperty:HeatTransferAlgorithm`` and add it to the document.

        Determines which Heat Balance Algorithm will be used for a specific surface Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions). Advanced/Research Usage: CondFD (Conduction Finite Difference) Advanced/Research Usage: HAMT (Combined Heat And Moisture Finite Element)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheattransferalgorithm
        """

class AnyElectricLoadCenterStorageLiIonNMCBattery:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_cells_in_series: int,
        number_of_strings_in_parallel: int,
        battery_mass: float,
        battery_surface_area: float,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        lifetime_model: Literal["KandlerSmith", "None"] | None = "KandlerSmith",
        initial_fractional_state_of_charge: float | None = 0.5,
        dc_to_dc_charging_efficiency: float | None = 0.95,
        battery_specific_heat_capacity: float | None = 1500,
        heat_transfer_coefficient_between_battery_and_ambient: float | None = 7.5,
        fully_charged_cell_voltage: float | None = 4.2,
        cell_voltage_at_end_of_exponential_zone: float | None = 3.53,
        cell_voltage_at_end_of_nominal_zone: float | None = 3.342,
        default_nominal_cell_voltage: float | None = 3.342,
        fully_charged_cell_capacity: float | None = 3.2,
        fraction_of_cell_capacity_removed_at_the_end_of_exponential_zone: float | None = 0.8075,
        fraction_of_cell_capacity_removed_at_the_end_of_nominal_zone: float | None = 0.976875,
        charge_rate_at_which_voltage_vs_capacity_curve_was_generated: float | None = 1,
        battery_cell_internal_electrical_resistance: float | None = 0.09,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:LiIonNMCBattery`` and add it to the document.

        Uses Lithium Ion NMC model to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstorageliionnmcbattery
        """
