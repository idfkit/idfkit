"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyMaterial:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thickness: float,
        conductivity: float,
        density: float,
        specific_heat: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
        validate: bool = True,
    ) -> None:
        """Create a new ``Material`` and add it to the document.

        Regular materials described with full set of thermal properties

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#material
        """

class AnyMaterialPropertyHeatAndMoistureTransferThermalConductivity:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        material_name: str,
        number_of_thermal_coordinates: int,
        moisture_content_1: float,
        thermal_conductivity_1: float,
        moisture_content_2: float | None = ...,
        thermal_conductivity_2: float | None = ...,
        moisture_content_3: float | None = ...,
        thermal_conductivity_3: float | None = ...,
        moisture_content_4: float | None = ...,
        thermal_conductivity_4: float | None = ...,
        moisture_content_5: float | None = ...,
        thermal_conductivity_5: float | None = ...,
        moisture_content_6: float | None = ...,
        thermal_conductivity_6: float | None = ...,
        moisture_content_7: float | None = ...,
        thermal_conductivity_7: float | None = ...,
        moisture_content_8: float | None = ...,
        thermal_conductivity_8: float | None = ...,
        moisture_content_9: float | None = ...,
        thermal_conductivity_9: float | None = ...,
        moisture_content_10: float | None = ...,
        thermal_conductivity_10: float | None = ...,
        moisture_content_11: float | None = ...,
        thermal_conductivity_11: float | None = ...,
        moisture_content_12: float | None = ...,
        thermal_conductivity_12: float | None = ...,
        moisture_content_13: float | None = ...,
        thermal_conductivity_13: float | None = ...,
        moisture_content_14: float | None = ...,
        thermal_conductivity_14: float | None = ...,
        moisture_content_15: float | None = ...,
        thermal_conductivity_15: float | None = ...,
        moisture_content_16: float | None = ...,
        thermal_conductivity_16: float | None = ...,
        moisture_content_17: float | None = ...,
        thermal_conductivity_17: float | None = ...,
        moisture_content_18: float | None = ...,
        thermal_conductivity_18: float | None = ...,
        moisture_content_19: float | None = ...,
        thermal_conductivity_19: float | None = ...,
        moisture_content_20: float | None = ...,
        thermal_conductivity_20: float | None = ...,
        moisture_content_21: float | None = ...,
        thermal_conductivity_21: float | None = ...,
        moisture_content_22: float | None = ...,
        thermal_conductivity_22: float | None = ...,
        moisture_content_23: float | None = ...,
        thermal_conductivity_23: float | None = ...,
        moisture_content_24: float | None = ...,
        thermal_conductivity_24: float | None = ...,
        moisture_content_25: float | None = ...,
        thermal_conductivity_25: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:ThermalConductivity`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between thermal conductivity and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferthermalconductivity
        """

class DuctLossMakeupAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_name: str,
        airflownetwork_distribution_linkage_name: str,
        validate: bool = True,
    ) -> None:
        """Create a new ``Duct:Loss:MakeupAir`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#ductlossmakeupair
        """

class AnySizingSystem:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        airloop_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        central_cooling_design_supply_air_temperature: float,
        central_heating_design_supply_air_temperature: float,
        type_of_load_to_size_on: Literal["Sensible", "Total", "VentilationRequirement"] | None = "Sensible",
        design_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        central_heating_maximum_system_air_flow_ratio: float | Literal["Autosize"] | None = "Autosize",
        type_of_zone_sum_to_use: Literal["Coincident", "NonCoincident"] | None = "NonCoincident",
        central_cooling_design_supply_air_humidity_ratio: float | None = 0.008,
        central_heating_design_supply_air_humidity_ratio: float | None = 0.008,
        cooling_supply_air_flow_rate_method: Literal[
            "DesignDay",
            "Flow/System",
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FractionOfAutosizedCoolingAirflow",
        ]
        | None = "DesignDay",
        cooling_supply_air_flow_rate: float | None = 0,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_cooling_capacity: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "DesignDay",
            "Flow/System",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedCoolingAirflow",
            "FractionOfAutosizedHeatingAirflow",
        ]
        | None = "DesignDay",
        heating_supply_air_flow_rate: float | None = 0,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        heating_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_heating_capacity: float | None = ...,
        system_outdoor_air_method: Literal["ZoneSum"] | None = "ZoneSum",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        cooling_design_capacity_method: Literal[
            "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity", "None"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = ...,
        central_cooling_capacity_control_method: Literal["Bypass", "OnOff", "VAV", "VT"] | None = "OnOff",
        validate: bool = True,
    ) -> None:
        """Create a new ``Sizing:System`` and add it to the document.

        Specifies the input needed to perform sizing calculations for a central forced air system. System design air flow, heating capacity, and cooling capacity will be calculated using this input data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingsystem
        """

class AnyZoneHVACBaseboardRadiantConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_water_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        rated_average_water_temperature: float | None = 87.78,
        rated_water_mass_flow_rate: float | None = 0.063,
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        surface_fractions: Sequence[
            _g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsItem
            | _g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        ``surface_fractions`` takes the extensible groups in order, one dict per group:

        ```python
        doc["ZoneHVAC:Baseboard:RadiantConvective:Water"].add(
            "ZoneHVAC Baseboard RadiantConvective Water 1",
            inlet_node_name="Inlet Node 1",
            outlet_node_name="Outlet Node 1",
            maximum_water_flow_rate=0.0,
            design_object="Design Object 1",
            surface_fractions=[
                {"surface_name": "Surface 1", "fraction_of_radiant_energy_to_surface": 0.0},
                {"surface_name": "Surface 2", "fraction_of_radiant_energy_to_surface": 0.0},
            ],
        )
        ```

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivewater
        """

class PipeOutdoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        pipe_inside_diameter: float | None = ...,
        pipe_length: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Pipe:Outdoor`` and add it to the document.

        Pipe model with transport delay and heat transfer to the environment.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipeoutdoor
        """

class BoilerSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ],
        maximum_operating_pressure: float | None = 160000,
        theoretical_efficiency: float | None = 0.8,
        design_outlet_steam_temperature: float | None = 100,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        coefficient_1_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        coefficient_2_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        coefficient_3_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        water_inlet_node_name: str | None = ...,
        steam_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Boiler:Steam`` and add it to the document.

        This boiler model is an adaptation of the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Boiler performance curves are generated by fitting catalog data to third order polynomial equations. A constant efficiency boiler is modeled by setting the fuel use coefficients as follows: N9=1, N10=0, N11=0

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#boilersteam
        """

class SetpointManagerWarmestTemperatureFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["Temperature"] | None = ...,
        minimum_setpoint_temperature: float | None = 12,
        maximum_setpoint_temperature: float | None = 18,
        strategy: Literal["FlowFirst", "TemperatureFirst"] | None = "TemperatureFirst",
        minimum_turndown_ratio: float | None = 0.2,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:WarmestTemperatureFlow`` and add it to the document.

        This setpoint manager sets both the supply air temperature and the supply air flow rate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerwarmesttemperatureflow
        """

class RefrigerationCompressor:
    def __call__(
        self,
        name: str,
        /,
        *,
        refrigeration_compressor_power_curve_name: str,
        refrigeration_compressor_capacity_curve_name: str,
        rated_superheat: float | None = ...,
        rated_return_gas_temperature: float | None = ...,
        rated_liquid_temperature: float | None = ...,
        rated_subcooling: float | None = ...,
        end_use_subcategory: str | None = "General",
        mode_of_operation: Literal["Subcritical", "Transcritical"] | None = "Subcritical",
        transcritical_compressor_power_curve_name: str | None = ...,
        transcritical_compressor_capacity_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:Compressor`` and add it to the document.

        Refrigeration system compressor. Data is available for many compressors in the RefrigerationCompressor.idf dataset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcompressor
        """

class OutputPreprocessorMessage:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        preprocessor_name: str | None = ...,
        error_severity: Literal["Fatal", "Information", "Severe", "Warning"] | None = ...,
        message_line_1: str | None = ...,
        message_line_2: str | None = ...,
        message_line_3: str | None = ...,
        message_line_4: str | None = ...,
        message_line_5: str | None = ...,
        message_line_6: str | None = ...,
        message_line_7: str | None = ...,
        message_line_8: str | None = ...,
        message_line_9: str | None = ...,
        message_line_10: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:PreprocessorMessage`` and add it to the document.

        This object does not come from a user input. This is generated by a pre-processor so that various conditions can be gracefully passed on by the InputProcessor.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#outputpreprocessormessage
        """
