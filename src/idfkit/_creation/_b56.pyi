"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class SiteGroundReflectance:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        january_ground_reflectance: float | None = 0.2,
        february_ground_reflectance: float | None = 0.2,
        march_ground_reflectance: float | None = 0.2,
        april_ground_reflectance: float | None = 0.2,
        may_ground_reflectance: float | None = 0.2,
        june_ground_reflectance: float | None = 0.2,
        july_ground_reflectance: float | None = 0.2,
        august_ground_reflectance: float | None = 0.2,
        september_ground_reflectance: float | None = 0.2,
        october_ground_reflectance: float | None = 0.2,
        november_ground_reflectance: float | None = 0.2,
        december_ground_reflectance: float | None = 0.2,
    ) -> None:
        """Create a new ``Site:GroundReflectance`` and add it to the document.

        Specifies the ground reflectance values used to calculate ground reflected solar. The ground reflectance can be further modified when snow is on the ground by Site:GroundReflectance:SnowModifier.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundreflectance
        """

class ShadingOverhangProjection:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        height_above_window_or_door: float | None = ...,
        tilt_angle_from_window_door: float | None = 90,
        left_extension_from_window_door_width: float | None = ...,
        right_extension_from_window_door_width: float | None = ...,
        depth_as_fraction_of_window_door_height: float | None = ...,
    ) -> None:
        """Create a new ``Shading:Overhang:Projection`` and add it to the document.

        Overhangs are typically flat shading surfaces that reference a window or door.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#shadingoverhangprojection
        """

class SurfacePropertyHeatBalanceSourceTerm:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        surface_name: str,
        inside_face_heat_source_term_schedule_name: str | None = ...,
        outside_face_heat_source_term_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:HeatBalanceSourceTerm`` and add it to the document.

        Allows an additional heat source term to be added to the inside or outside surface boundary. A heat source can be added to either or both the inside and outside of the same surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheatbalancesourceterm
        """

class ZoneContaminantSourceAndSinkGenericDecaySource:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        initial_emission_rate: float | None = ...,
        delay_time_constant: float | None = ...,
    ) -> None:
        """Create a new ``ZoneContaminantSourceAndSink:Generic:DecaySource`` and add it to the document.

        Simulate generic contaminant source driven by the cutoff concentration model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonecontaminantsourceandsinkgenericdecaysource
        """

class AnyAirflowNetworkSimulationControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        airflownetwork_control: Literal[
            "",
            "MultizoneWithDistribution",
            "MultizoneWithDistributionOnlyDuringFanOperation",
            "MultizoneWithoutDistribution",
            "NoMultizoneOrDistribution",
        ]
        | None = "NoMultizoneOrDistribution",
        wind_pressure_coefficient_type: Literal["", "Input", "SurfaceAverageCalculation"]
        | None = "SurfaceAverageCalculation",
        height_selection_for_local_wind_pressure_calculation: Literal["", "ExternalNode", "OpeningHeight"]
        | None = "OpeningHeight",
        building_type: Literal["", "HighRise", "LowRise"] | None = "LowRise",
        maximum_number_of_iterations: int | None = 500,
        initialization_type: Literal["", "LinearInitializationMethod", "ZeroNodePressures"]
        | None = "ZeroNodePressures",
        relative_airflow_convergence_tolerance: float | None = 0.0001,
        absolute_airflow_convergence_tolerance: float | None = ...,
        convergence_acceleration_limit: float | None = -0.5,
        azimuth_angle_of_long_axis_of_building: float | None = 0,
        ratio_of_building_width_along_short_axis_to_width_along_long_axis: float | None = 1,
        height_dependence_of_external_node_temperature: Literal["", "No", "Yes"] | None = "No",
        solver: Literal["", "ConjugateGradient", "SkylineLU"] | None = "SkylineLU",
    ) -> None:
        """Create a new ``AirflowNetwork:SimulationControl`` and add it to the document.

        This object defines the global parameters used in an Airflow Network simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworksimulationcontrol
        """

class AnyHeatPumpWaterToWaterEquationFitHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_heating_capacity: float | Literal["Autosize"],
        reference_heating_power_consumption: float | Literal["Autosize"],
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
        companion_cooling_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Heating`` and add it to the document.

        simple water-water hp curve-fit model

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitheating
        """

class GroundHeatExchangerSlinky:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        design_flow_rate: float | None = 0.002,
        soil_thermal_conductivity: float | None = 1.08,
        soil_density: float | None = 962,
        soil_specific_heat: float | None = 2576,
        pipe_thermal_conductivity: float | None = 0.4,
        pipe_density: float | None = 641,
        pipe_specific_heat: float | None = 2405,
        pipe_outer_diameter: float | None = 0.02667,
        pipe_thickness: float | None = 0.002413,
        heat_exchanger_configuration: Literal["Horizontal", "Vertical"] | None = ...,
        coil_diameter: float | None = 1,
        coil_pitch: float | None = 0.2,
        trench_depth: float | None = 1.8,
        trench_length: float | None = 10,
        number_of_trenches: int | None = 1,
        horizontal_spacing_between_pipes: float | None = 2,
        maximum_length_of_simulation: float | None = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Slinky`` and add it to the document.

        This models a slinky horizontal heat exchanger placed in a series of trenches The model uses the model developed by: Xiong, Z., D.E. Fisher, and J.D. Spitler. 2015. Development and Validation of a Slinky Ground Heat Exchanger Model. Applied Energy 141: 57-69.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerslinky
        """

class ExternalInterfaceActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        optional_initial_value: float | None = ...,
    ) -> None:
        """Create a new ``ExternalInterface:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfaceactuator
        """

class GeneratorFuelCellWaterSupply:
    def __call__(
        self,
        name: str,
        /,
        *,
        reformer_water_flow_rate_function_of_fuel_rate_curve_name: str | None = ...,
        reformer_water_pump_power_function_of_fuel_rate_curve_name: str | None = ...,
        pump_heat_loss_factor: float | None = ...,
        water_temperature_modeling_mode: Literal[
            "MainsWaterTemperature", "TemperatureFromAirNode", "TemperatureFromSchedule", "TemperatureFromWaterNode"
        ]
        | None = ...,
        water_temperature_reference_node_name: str | None = ...,
        water_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:WaterSupply`` and add it to the document.

        Used to provide details of the water supply subsystem for a fuel cell power generator. This water is used for steam reforming of the fuel and is not the same as the water used for thermal heat recovery.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellwatersupply
        """

class ComponentCostAdjustments:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        miscellaneous_cost_per_conditioned_area: float | None = ...,
        design_and_engineering_fees: float | None = ...,
        contractor_fee: float | None = ...,
        contingency: float | None = ...,
        permits_bonding_and_insurance: float | None = ...,
        commissioning_fee: float | None = ...,
        regional_adjustment_factor: float | None = ...,
    ) -> None:
        """Create a new ``ComponentCost:Adjustments`` and add it to the document.

        Used to perform various modifications to the construction costs to arrive at an estimate for total project costs. This object allows extending the line item model so that the overall costs of the project will reflect various profit and fees.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#componentcostadjustments
        """
