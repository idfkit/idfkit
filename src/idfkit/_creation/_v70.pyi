"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ThermalStorageIceDetailed_v9_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        capacity: float,
        inlet_node_name: str,
        outlet_node_name: str,
        discharging_curve_variable_specifications: Literal[
            "FractionChargedLMTD", "FractionDischargedLMTD", "LMTDFractionCharged", "LMTDMassFlow"
        ],
        discharging_curve_name: str,
        charging_curve_variable_specifications: Literal[
            "FractionChargedLMTD", "FractionDischargedLMTD", "LMTDFractionCharged", "LMTDMassFlow"
        ],
        charging_curve_name: str,
        availability_schedule_name: str | None = ...,
        timestep_of_the_curve_data: float | None = ...,
        parasitic_electric_load_during_discharging: float | None = ...,
        parasitic_electric_load_during_charging: float | None = ...,
        tank_loss_coefficient: float | None = ...,
        freezing_temperature_of_storage_medium: float | None = 0,
        thaw_process_indicator: Literal["InsideMelt", "OutsideMelt"] | None = "OutsideMelt",
    ) -> None:
        """Create a new ``ThermalStorage:Ice:Detailed`` and add it to the document.

        This input syntax is intended to describe a thermal storage system that includes smaller containers filled with water that are placed in a larger tank or series of tanks. The model uses polynomial equations to describe the system performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-water-heaters/#thermalstorageicedetailed
        """

class OutputSQLite_v8_9_to_v9_4:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        option_type: Literal["Simple", "SimpleAndTabular"] | None = ...,
    ) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/input-for-output/#outputsqlite
        """

class CoilCoolingWaterToAirHeatPumpEquationFit_v9_5_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_cooling_capacity: float | Literal["Autosize"],
        gross_rated_cooling_cop: float,
        total_cooling_capacity_curve_name: str,
        sensible_cooling_capacity_curve_name: str,
        cooling_power_consumption_curve_name: str,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """

class AirflowNetworkSimulationControl_v9_5_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        airflownetwork_control: Literal[
            "MultizoneWithDistribution",
            "MultizoneWithDistributionOnlyDuringFanOperation",
            "MultizoneWithoutDistribution",
            "NoMultizoneOrDistribution",
        ]
        | None = "NoMultizoneOrDistribution",
        wind_pressure_coefficient_type: Literal["Input", "SurfaceAverageCalculation"]
        | None = "SurfaceAverageCalculation",
        height_selection_for_local_wind_pressure_calculation: Literal["ExternalNode", "OpeningHeight"]
        | None = "OpeningHeight",
        building_type: Literal["HighRise", "LowRise"] | None = "LowRise",
        maximum_number_of_iterations: float | None = 500,
        initialization_type: Literal["LinearInitializationMethod", "ZeroNodePressures"] | None = "ZeroNodePressures",
        relative_airflow_convergence_tolerance: float | None = 0.0001,
        absolute_airflow_convergence_tolerance: float | None = ...,
        convergence_acceleration_limit: float | None = -0.5,
        azimuth_angle_of_long_axis_of_building: float | None = 0,
        ratio_of_building_width_along_short_axis_to_width_along_long_axis: float | None = 1,
        height_dependence_of_external_node_temperature: Literal["No", "Yes"] | None = "No",
        solver: Literal["ConjugateGradient", "SkylineLU"] | None = "SkylineLU",
        allow_unsupported_zone_equipment: Literal["No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``AirflowNetwork:SimulationControl`` and add it to the document.

        This object defines the global parameters used in an Airflow Network simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow-network/#airflownetworksimulationcontrol
        """

class ZonePropertyUserViewFactorsBySurfaceName_v9_4_to_v9_5:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_or_zonelist_name: str | None = ...,
        view_factors: Sequence[
            _g.ZonePropertyUserViewFactorsBySurfaceNameViewFactorsItem
            | _g.ZonePropertyUserViewFactorsBySurfaceNameViewFactorsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ZoneProperty:UserViewFactors:BySurfaceName`` and add it to the document.

        View factors for Surface to Surface in a zone. (Number of Surfaces)**2 are expected. Any omitted surface pairs will be assumed to have a view factor of zero.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-advanced-surface-concepts/#zonepropertyuserviewfactorsbysurfacename
        """
