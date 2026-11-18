"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class AnySurfaceConvectionAlgorithmInside:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        algorithm: Literal["", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP"] | None = "TARP",
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Inside`` and add it to the document.

        Default indoor surface heat transfer convection algorithm to be used for all zones

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#surfaceconvectionalgorithminside
        """

class SiteLocation:
    def __call__(
        self,
        name: str,
        /,
        *,
        latitude: float | None = 0,
        longitude: float | None = 0,
        time_zone: float | None = 0,
        elevation: float | None = 0,
        keep_site_location_information: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``Site:Location`` and add it to the document.

        Specifies the building's location. Only one location is allowed. Weather data file location, if it exists, will override this object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitelocation
        """

class MaterialPropertyHeatAndMoistureTransferDiffusion:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        material_name: str,
        number_of_data_pairs: int,
        relative_humidity_fraction_1: float,
        water_vapor_diffusion_resistance_factor_1: float,
        relative_humidity_fraction_2: float | None = ...,
        water_vapor_diffusion_resistance_factor_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        water_vapor_diffusion_resistance_factor_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        water_vapor_diffusion_resistance_factor_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        water_vapor_diffusion_resistance_factor_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        water_vapor_diffusion_resistance_factor_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        water_vapor_diffusion_resistance_factor_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        water_vapor_diffusion_resistance_factor_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        water_vapor_diffusion_resistance_factor_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        water_vapor_diffusion_resistance_factor_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        water_vapor_diffusion_resistance_factor_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        water_vapor_diffusion_resistance_factor_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        water_vapor_diffusion_resistance_factor_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        water_vapor_diffusion_resistance_factor_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        water_vapor_diffusion_resistance_factor_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        water_vapor_diffusion_resistance_factor_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        water_vapor_diffusion_resistance_factor_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        water_vapor_diffusion_resistance_factor_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        water_vapor_diffusion_resistance_factor_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        water_vapor_diffusion_resistance_factor_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        water_vapor_diffusion_resistance_factor_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        water_vapor_diffusion_resistance_factor_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        water_vapor_diffusion_resistance_factor_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        water_vapor_diffusion_resistance_factor_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        water_vapor_diffusion_resistance_factor_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Diffusion`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between water vapor diffusion and relative humidity fraction Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferdiffusion
        """

class AnyWallUnderground:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Underground`` and add it to the document.

        Allows for simplified entry of underground walls.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#wallunderground
        """

class AnyWindow:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Window`` and add it to the document.

        Allows for simplified entry of Windows.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#window
        """

class GroundHeatTransferBasementInterior:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        cond_flag_is_the_basement_conditioned_: Literal["", "FALSE", "TRUE"] | None = "TRUE",
        hin_downward_convection_only_heat_transfer_coefficient: float | None = 0.92,
        hin_upward_convection_only_heat_transfer_coefficient: float | None = 4.04,
        hin_horizontal_convection_only_heat_transfer_coefficient: float | None = 3.08,
        hin_downward_combined_convection_and_radiation_heat_transfer_coefficient: float | None = 6.13,
        hin_upward_combined_convection_and_radiation_heat_transfer_coefficient: float | None = 9.26,
        hin_horizontal_combined_convection_and_radiation_heat_transfer_coefficient: float | None = 8.29,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:Interior`` and add it to the document.

        Provides the information needed to simulate the inside boundary conditions for the Basement preprocessor ground heat transfer simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementinterior
        """

class DesignSpecificationAirTerminalSizing:
    def __call__(
        self,
        name: str,
        /,
        *,
        fraction_of_design_cooling_load: float | None = 1,
        cooling_design_supply_air_temperature_difference_ratio: float | None = 1,
        fraction_of_design_heating_load: float | None = 1,
        heating_design_supply_air_temperature_difference_ratio: float | None = 1,
        fraction_of_minimum_outdoor_air_flow: float | None = 1,
    ) -> None:
        """Create a new ``DesignSpecification:AirTerminal:Sizing`` and add it to the document.

        This object is used to scale the sizing of air terminal units.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#designspecificationairterminalsizing
        """

class EvaporativeCoolerIndirectResearchSpecial:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        cooler_wetbulb_design_effectiveness: float,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        secondary_air_inlet_node_name: str,
        secondary_air_outlet_node_name: str,
        sensor_node_name: str,
        availability_schedule_name: str | None = ...,
        wetbulb_effectiveness_flow_ratio_modifier_curve_name: str | None = ...,
        cooler_drybulb_design_effectiveness: float | None = ...,
        drybulb_effectiveness_flow_ratio_modifier_curve_name: str | None = ...,
        recirculating_water_pump_design_power: float | Literal["", "Autosize"] | None = "Autosize",
        water_pump_power_sizing_factor: float | None = 90,
        water_pump_power_modifier_curve_name: str | None = ...,
        secondary_air_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        secondary_air_flow_scaling_factor: float | None = 1,
        secondary_air_fan_design_power: float | Literal["", "Autosize"] | None = "Autosize",
        secondary_air_fan_sizing_specific_power: float | None = 250,
        secondary_air_fan_power_modifier_curve_name: str | None = ...,
        primary_air_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        dewpoint_effectiveness_factor: float | None = ...,
        relief_air_inlet_node_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        drift_loss_fraction: float | None = 0,
        blowdown_concentration_ratio: float | None = ...,
        evaporative_operation_minimum_limit_secondary_air_drybulb_temperature: float | None = ...,
        evaporative_operation_maximum_limit_outdoor_wetbulb_temperature: float | None = ...,
        dry_operation_maximum_limit_outdoor_drybulb_temperature: float | None = ...,
    ) -> None:
        """Create a new ``EvaporativeCooler:Indirect:ResearchSpecial`` and add it to the document.

        Indirect evaporative cooler with user-specified effectiveness (can represent rigid pad or wetted coil), recirculating water pump, and secondary air fan. This model is controlled to meet the primary air outlet temperature setpoint.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-evaporative-coolers/#evaporativecoolerindirectresearchspecial
        """

class EnergyManagementSystemSensor:
    def __call__(
        self,
        name: str,
        /,
        *,
        output_variable_or_output_meter_name: str,
        output_variable_or_output_meter_index_key_name: str | None = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:Sensor`` and add it to the document.

        Declares EMS variable as a sensor a list of output variables and meters that can be reported are available after a run on the report (.rdd) or meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemsensor
        """

class EnergyManagementSystemActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
    ) -> None:
        """Create a new ``EnergyManagementSystem:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemactuator
        """

class AnyExternalInterfaceFunctionalMockupUnitExportToSchedule:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        schedule_name: str,
        fmu_variable_name: str,
        initial_value: float,
        schedule_type_limits_names: str | None = ...,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitExport:To:Schedule`` and add it to the document.

        This objects contains only one value, which is used during the first call of EnergyPlus

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitexporttoschedule
        """

class FaultModelHumiditySensorOffsetOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        humidity_sensor_offset: float | None = 0,
    ) -> None:
        """Create a new ``FaultModel:HumiditySensorOffset:OutdoorAir`` and add it to the document.

        This object describes outdoor air humidity sensor offset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelhumiditysensoroffsetoutdoorair
        """
