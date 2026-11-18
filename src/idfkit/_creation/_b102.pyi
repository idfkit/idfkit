"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class WindowMaterialBlindEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        slat_width: float,
        slat_separation: float,
        front_side_slat_beam_diffuse_solar_reflectance: float,
        back_side_slat_beam_diffuse_solar_reflectance: float,
        front_side_slat_diffuse_diffuse_solar_reflectance: float,
        back_side_slat_diffuse_diffuse_solar_reflectance: float,
        slat_orientation: Literal["Horizontal", "Vertical"] | None = "Horizontal",
        slat_crown: float | None = 0.0015,
        slat_angle: float | None = 45,
        front_side_slat_beam_diffuse_solar_transmittance: float | None = 0,
        back_side_slat_beam_diffuse_solar_transmittance: float | None = 0,
        front_side_slat_beam_diffuse_visible_transmittance: float | None = 0,
        back_side_slat_beam_diffuse_visible_transmittance: float | None = 0,
        front_side_slat_beam_diffuse_visible_reflectance: float | None = ...,
        back_side_slat_beam_diffuse_visible_reflectance: float | None = ...,
        slat_diffuse_diffuse_solar_transmittance: float | None = 0,
        slat_diffuse_diffuse_visible_transmittance: float | None = ...,
        front_side_slat_diffuse_diffuse_visible_reflectance: float | None = ...,
        back_side_slat_diffuse_diffuse_visible_reflectance: float | None = ...,
        slat_infrared_transmittance: float | None = 0,
        front_side_slat_infrared_emissivity: float | None = 0.9,
        back_side_slat_infrared_emissivity: float | None = 0.9,
        slat_angle_control: Literal["BlockBeamSolar", "FixedSlatAngle", "MaximizeSolar"] | None = "FixedSlatAngle",
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowMaterial:Blind:EquivalentLayer`` and add it to the document.

        Window equivalent layer blind slat optical and thermal properties. The model assumes that slats are thin and flat, applies correction empirical correlation to account for curvature effect. Slats are assumed to transmit and reflect diffusely.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialblindequivalentlayer
        """

class AnyLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_level_calculation_method: Literal["LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        fraction_replaceable: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_fraction_calculated_from_plenum_temperature: Literal["No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
        return_air_heat_gain_node_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Lights`` and add it to the document.

        Sets internal gains for lights in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#lights
        """

class AnyDaylightingControls:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        daylighting_method: Literal["DElight", "SplitFlux"] | None = "SplitFlux",
        availability_schedule_name: str | None = ...,
        lighting_control_type: Literal["Continuous", "ContinuousOff", "Stepped"] | None = "Continuous",
        minimum_input_power_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.3,
        minimum_light_output_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.2,
        number_of_stepped_control_steps: int | None = 1,
        probability_lighting_will_be_reset_when_needed_in_manual_stepped_control: float | None = 1,
        glare_calculation_daylighting_reference_point_name: str | None = ...,
        glare_calculation_azimuth_angle_of_view_direction_clockwise_from_zone_y_axis: float | None = 0,
        maximum_allowable_discomfort_glare_index: float | None = 22,
        delight_gridding_resolution: float | None = ...,
        control_data: Sequence[
            _g.AnyDaylightingControlsControlDataItem | _g.AnyDaylightingControlsControlDataGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Daylighting:Controls`` and add it to the document.

        Dimming of overhead electric lighting is determined from each reference point. Glare from daylighting is also calculated.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#daylightingcontrols
        """

class DesignSpecificationOutdoorAirSpaceList:
    def __call__(
        self,
        name: str,
        /,
        *,
        space_specs: Sequence[
            _g.DesignSpecificationOutdoorAirSpaceListSpaceSpecsItem
            | _g.DesignSpecificationOutdoorAirSpaceListSpaceSpecsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``DesignSpecification:OutdoorAir:SpaceList`` and add it to the document.

        Defines a list of DesignSpecification:OutdoorAir names which can be referenced as a group. The DesignSpecification:OutdoorAir:SpaceList name may be used in Sizing:Zone and Controller:MechanicalVentilation to specify space-by-space OA requirements and anywhere else that accepts a DesignSpecification:OutdoorAir object name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#designspecificationoutdoorairspacelist
        """

class AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_terminal_unit_list_name: str,
        outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R410A",
        rated_evaporative_capacity: float | Literal["Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_only_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_only_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_only_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_only_mode: float | None = 16,
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -20,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 43,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["ConstantTemp", "VariableTemp"]
        | None = "VariableTemp",
        reference_evaporating_temperature_for_indoor_unit: float | None = 6,
        reference_condensing_temperature_for_indoor_unit: float | None = 44,
        variable_evaporating_temperature_minimum_for_indoor_unit: float | None = 4,
        variable_evaporating_temperature_maximum_for_indoor_unit: float | None = 13,
        variable_condensing_temperature_minimum_for_indoor_unit: float | None = 42,
        variable_condensing_temperature_maximum_for_indoor_unit: float | None = 46,
        outdoor_unit_evaporator_reference_superheating: float | None = 3,
        outdoor_unit_condenser_reference_subcooling: float | None = 5,
        outdoor_unit_evaporator_rated_bypass_factor: float | None = 0.4,
        outdoor_unit_condenser_rated_bypass_factor: float | None = 0.2,
        difference_between_outdoor_unit_evaporating_temperature_and_outdoor_air_temperature_in_heat_recovery_mode: float
        | None = 5,
        outdoor_unit_heat_exchanger_capacity_ratio: float | None = 0.3,
        outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None = 0.00425,
        outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None = ...,
        diameter_of_main_pipe_for_suction_gas: float | None = 0.0762,
        diameter_of_main_pipe_for_discharge_gas: float | None = 0.0762,
        length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 30,
        equivalent_length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 36,
        height_difference_between_outdoor_unit_and_indoor_units: float | None = 5,
        main_pipe_insulation_thickness: float | None = 0.02,
        main_pipe_insulation_thermal_conductivity: float | None = 0.032,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        initial_heat_recovery_cooling_capacity_fraction: float | None = 1,
        heat_recovery_cooling_capacity_time_constant: float | None = 0,
        initial_heat_recovery_cooling_energy_fraction: float | None = 1,
        heat_recovery_cooling_energy_time_constant: float | None = 0,
        initial_heat_recovery_heating_capacity_fraction: float | None = 1,
        heat_recovery_heating_capacity_time_constant: float | None = 0,
        initial_heat_recovery_heating_energy_fraction: float | None = 1,
        heat_recovery_heating_energy_time_constant: float | None = 0,
        compressor_maximum_delta_pressure: float | None = 4500000,
        compressor_inverter_efficiency: float | None = 0.95,
        compressor_evaporative_capacity_correction_factor: float | None = 1,
        number_of_compressor_loading_index_entries: int | None = 2,
        loading_indices: Sequence[
            _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlHRLoadingIndicesItem
            | _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlHRLoadingIndicesGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR`` and add it to the document.

        This is a key object in the new physics based VRF Heat Recovery (HR) model applicable for Fluid Temperature Control. It describes the VRF HR system excluding the performance of indoor units. Indoor units are modeled separately in the ZoneHVAC:TerminalUnit:VariableRefrigerantFlow object

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflowfluidtemperaturecontrolhr
        """

class EnergyManagementSystemProgramCallingManager:
    def __call__(
        self,
        name: str,
        /,
        *,
        energyplus_model_calling_point: Literal[
            "AfterComponentInputReadIn",
            "AfterNewEnvironmentWarmUpIsComplete",
            "AfterPredictorAfterHVACManagers",
            "AfterPredictorBeforeHVACManagers",
            "BeginNewEnvironment",
            "BeginTimestepBeforePredictor",
            "BeginZoneTimestepAfterInitHeatBalance",
            "BeginZoneTimestepBeforeInitHeatBalance",
            "BeginZoneTimestepBeforeSetCurrentWeather",
            "EndOfSystemSizing",
            "EndOfSystemTimestepAfterHVACReporting",
            "EndOfSystemTimestepBeforeHVACReporting",
            "EndOfZoneSizing",
            "EndOfZoneTimestepAfterZoneReporting",
            "EndOfZoneTimestepBeforeZoneReporting",
            "InsideHVACSystemIterationLoop",
            "UnitarySystemSizing",
            "UserDefinedComponentModel",
        ]
        | None = ...,
        programs: Sequence[
            _g.EnergyManagementSystemProgramCallingManagerProgramsItem
            | _g.EnergyManagementSystemProgramCallingManagerProgramsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``EnergyManagementSystem:ProgramCallingManager`` and add it to the document.

        Input EMS program. a program needs a name a description of when it should be called and then lines of program code for EMS Runtime language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemprogramcallingmanager
        """

class AnyExternalInterfaceFunctionalMockupUnitExportToActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        fmu_variable_name: str,
        initial_value: float,
        validate: bool = True,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitExport:To:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model that are dynamically updated from the FMU.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitexporttoactuator
        """

class SetpointManagerMultiZoneMinimumHumidityAverage:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_humidity_ratio: float | None = 0.005,
        maximum_setpoint_humidity_ratio: float | None = 0.012,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:MultiZone:MinimumHumidity:Average`` and add it to the document.

        This setpoint manager sets the average supply air minimum humidity ratio based on moisture load requirements of all controlled zones in an air loop served by a central air-conditioner.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagermultizoneminimumhumidityaverage
        """

class UtilityCostQualify:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        utility_cost_qualify_name: str,
        tariff_name: str,
        variable_name: str,
        threshold_value_or_variable_name: float | str,
        qualify_type: Literal["Maximum", "Minimum"] | None = "Maximum",
        season: Literal["Annual", "Fall", "Spring", "Summer", "Winter"] | None = ...,
        threshold_test: Literal["Consecutive", "Count"] | None = "Consecutive",
        number_of_months: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``UtilityCost:Qualify`` and add it to the document.

        The qualify object allows only tariffs to be selected based on limits which may apply such as maximum or minimum demand requirements. If the results of the simulation fall outside of the range of qualifications, that tariff is still calculated but the 'Qualified' entry will say 'No' and the UtilityCost:Qualify that caused its exclusion is shown. Multiple UtilityCost:Qualify objects can appear for the same tariff and they can be based on any variable.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-qualify/#utilitycostqualify
        """
