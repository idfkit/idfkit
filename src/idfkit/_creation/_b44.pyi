"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyFoundationKiva:
    def __call__(
        self,
        name: str,
        /,
        *,
        interior_horizontal_insulation_material_name: str | None = ...,
        interior_horizontal_insulation_depth: float | None = 0,
        interior_horizontal_insulation_width: float | None = ...,
        interior_vertical_insulation_material_name: str | None = ...,
        interior_vertical_insulation_depth: float | None = ...,
        exterior_horizontal_insulation_material_name: str | None = ...,
        exterior_horizontal_insulation_depth: float | None = ...,
        exterior_horizontal_insulation_width: float | None = 0,
        exterior_vertical_insulation_material_name: str | None = ...,
        exterior_vertical_insulation_depth: float | None = ...,
        wall_height_above_grade: float | None = 0.2,
        wall_depth_below_slab: float | None = 0,
        footing_wall_construction_name: str | None = ...,
        footing_material_name: str | None = ...,
        footing_depth: float | None = 0.3,
        blocks: Sequence[_g.FoundationKivaBlocksItem | _g.FoundationKivaBlocksGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Foundation:Kiva`` and add it to the document.

        Refined definition of the foundation surface construction used to inform two-dimensional heat transfer calculated using the Kiva ground heat transfer methodology.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#foundationkiva
        """

class AnyZonePropertyUserViewFactorsBySurfaceName:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        view_factors: Sequence[
            _g.ZonePropertyUserViewFactorsBySurfaceNameViewFactorsItem
            | _g.ZonePropertyUserViewFactorsBySurfaceNameViewFactorsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneProperty:UserViewFactors:BySurfaceName`` and add it to the document.

        View factors for Surface to Surface in a zone. (Number of Surfaces)**2 are expected. Any omitted surface pairs will be assumed to have a view factor of zero.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#zonepropertyuserviewfactorsbysurfacename
        """

class ZoneHVACTerminalUnitVariableRefrigerantFlow:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        terminal_unit_air_inlet_node_name: str,
        terminal_unit_air_outlet_node_name: str,
        terminal_unit_availability_schedule: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"]
        | None = "Fan:ConstantVolume",
        supply_air_fan_object_name: str | None = ...,
        outside_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outside_air_mixer_object_name: str | None = ...,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:VariableRefrigerantFlow", "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        cooling_coil_object_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:VariableRefrigerantFlow", "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        heating_coil_object_name: str | None = ...,
        zone_terminal_unit_on_parasitic_electric_energy_use: float | None = 0,
        zone_terminal_unit_off_parasitic_electric_energy_use: float | None = 0,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        controlling_zone_or_thermostat_location: str | None = ...,
        design_specification_multispeed_object_type: Literal["UnitarySystemPerformance:Multispeed"] | None = ...,
        design_specification_multispeed_object_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`` and add it to the document.

        A terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air heat pump). The VRF terminal units are served by an AirConditioner:VariableRefrigerantFlow or AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:* system. Terminal units can be configured as zone, air loop or outside air system equipment.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacterminalunitvariablerefrigerantflow
        """

class ZoneHVACHighTemperatureRadiant:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        fuel_type: Literal["Electricity", "NaturalGas"],
        heating_setpoint_temperature_schedule_name: str,
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        combustion_efficiency: float | None = 0.9,
        fraction_of_input_converted_to_radiant_energy: float | None = 0.7,
        fraction_of_input_converted_to_latent_energy: float | None = 0,
        fraction_of_input_that_is_lost: float | None = 0,
        temperature_control_type: Literal[
            "MeanAirTemperature",
            "MeanAirTemperatureSetpoint",
            "MeanRadiantTemperature",
            "MeanRadiantTemperatureSetpoint",
            "OperativeTemperature",
            "OperativeTemperatureSetpoint",
        ]
        | None = "OperativeTemperature",
        heating_throttling_range: float | None = 2,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: Sequence[
            _g.ZoneHVACHighTemperatureRadiantSurfaceFractionsItem
            | _g.ZoneHVACHighTemperatureRadiantSurfaceFractionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:HighTemperatureRadiant`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvachightemperatureradiant
        """

class AnyCoilHeatingWaterToAirHeatPumpEquationFit:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump performance.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpequationfit
        """

class CoilSystemIntegratedHeatPumpAirSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        supply_hot_water_flow_sensor_node_name: str,
        space_cooling_coil_name: str,
        space_heating_coil_name: str | None = ...,
        dedicated_water_heating_coil_name: str | None = ...,
        scwh_coil_name: str | None = ...,
        scdwh_cooling_coil_name: str | None = ...,
        scdwh_water_heating_coil_name: str | None = ...,
        shdwh_heating_coil_name: str | None = ...,
        shdwh_water_heating_coil_name: str | None = ...,
        indoor_temperature_limit_for_scwh_mode: float | None = 20,
        ambient_temperature_limit_for_scwh_mode: float | None = 27,
        indoor_temperature_above_which_wh_has_higher_priority: float | None = 20,
        ambient_temperature_above_which_wh_has_higher_priority: float | None = 20,
        flag_to_indicate_load_control_in_scwh_mode: int | None = 0,
        minimum_speed_level_for_scwh_mode: int | None = 1,
        maximum_water_flow_volume_before_switching_from_scdwh_to_scwh_mode: float | None = 0,
        minimum_speed_level_for_scdwh_mode: int | None = 1,
        maximum_running_time_before_allowing_electric_resistance_heat_use_during_shdwh_mode: float | None = 360,
        minimum_speed_level_for_shdwh_mode: int | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``CoilSystem:IntegratedHeatPump:AirSource`` and add it to the document.

        This object is used for air-source integrated heat pump, a collection of its working modes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemintegratedheatpumpairsource
        """

class AnyChillerHeaterAbsorptionDirectFired:
    def __call__(
        self,
        name: str,
        /,
        *,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        nominal_cooling_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_to_cooling_capacity_ratio: float | None = 0.8,
        fuel_input_to_cooling_output_ratio: float | None = 0.97,
        fuel_input_to_heating_output_ratio: float | None = 1.25,
        electric_input_to_cooling_output_ratio: float | None = 0.01,
        electric_input_to_heating_output_ratio: float | None = 0,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        design_entering_condenser_water_temperature: float | None = 29,
        design_leaving_chilled_water_temperature: float | None = 7,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_hot_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        heating_capacity_function_of_cooling_capacity_curve_name: str | None = ...,
        fuel_input_to_heat_output_ratio_during_heating_only_operation_curve_name: str | None = ...,
        temperature_curve_input_variable: Literal["EnteringCondenser", "LeavingCondenser"] | None = "EnteringCondenser",
        condenser_type: Literal["AirCooled", "WaterCooled"] | None = "WaterCooled",
        chilled_water_temperature_lower_limit: float | None = 2,
        fuel_higher_heating_value: float | None = 0,
        fuel_type: Literal["Diesel", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"] | None = "NaturalGas",
        sizing_factor: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``ChillerHeater:Absorption:DirectFired`` and add it to the document.

        Direct fired gas absorption chiller-heater using performance curves similar to DOE-2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerheaterabsorptiondirectfired
        """

class PlantEquipmentOperationHeatingLoad:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_range_1_lower_limit: float,
        load_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        load_range_2_lower_limit: float | None = ...,
        load_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        load_range_3_lower_limit: float | None = ...,
        load_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        load_range_4_lower_limit: float | None = ...,
        load_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        load_range_5_lower_limit: float | None = ...,
        load_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        load_range_6_lower_limit: float | None = ...,
        load_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        load_range_7_lower_limit: float | None = ...,
        load_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        load_range_8_lower_limit: float | None = ...,
        load_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        load_range_9_lower_limit: float | None = ...,
        load_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        load_range_10_lower_limit: float | None = ...,
        load_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:HeatingLoad`` and add it to the document.

        Plant equipment operation scheme for heating load range operation. Specifies one or more groups of equipment which are available to operate for successive heating load ranges.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationheatingload
        """

class ExternalInterfaceFunctionalMockupUnitImport:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        fmu_file_name: str,
        fmu_timeout: float | None = 0,
        fmu_loggingon: int | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitImport`` and add it to the document.

        This object declares an FMU

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitimport
        """

class FluidPropertiesTemperatures:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        temperature_1: float | None = ...,
        temperature_2: float | None = ...,
        temperature_3: float | None = ...,
        temperature_4: float | None = ...,
        temperature_5: float | None = ...,
        temperature_6: float | None = ...,
        temperature_7: float | None = ...,
        temperature_8: float | None = ...,
        temperature_9: float | None = ...,
        temperature_10: float | None = ...,
        temperature_11: float | None = ...,
        temperature_12: float | None = ...,
        temperature_13: float | None = ...,
        temperature_14: float | None = ...,
        temperature_15: float | None = ...,
        temperature_16: float | None = ...,
        temperature_17: float | None = ...,
        temperature_18: float | None = ...,
        temperature_19: float | None = ...,
        temperature_20: float | None = ...,
        temperature_21: float | None = ...,
        temperature_22: float | None = ...,
        temperature_23: float | None = ...,
        temperature_24: float | None = ...,
        temperature_25: float | None = ...,
        temperature_26: float | None = ...,
        temperature_27: float | None = ...,
        temperature_28: float | None = ...,
        temperature_29: float | None = ...,
        temperature_30: float | None = ...,
        temperature_31: float | None = ...,
        temperature_32: float | None = ...,
        temperature_33: float | None = ...,
        temperature_34: float | None = ...,
        temperature_35: float | None = ...,
        temperature_36: float | None = ...,
        temperature_37: float | None = ...,
        temperature_38: float | None = ...,
        temperature_39: float | None = ...,
        temperature_40: float | None = ...,
        temperature_41: float | None = ...,
        temperature_42: float | None = ...,
        temperature_43: float | None = ...,
        temperature_44: float | None = ...,
        temperature_45: float | None = ...,
        temperature_46: float | None = ...,
        temperature_47: float | None = ...,
        temperature_48: float | None = ...,
        temperature_49: float | None = ...,
        temperature_50: float | None = ...,
        temperature_51: float | None = ...,
        temperature_52: float | None = ...,
        temperature_53: float | None = ...,
        temperature_54: float | None = ...,
        temperature_55: float | None = ...,
        temperature_56: float | None = ...,
        temperature_57: float | None = ...,
        temperature_58: float | None = ...,
        temperature_59: float | None = ...,
        temperature_60: float | None = ...,
        temperature_61: float | None = ...,
        temperature_62: float | None = ...,
        temperature_63: float | None = ...,
        temperature_64: float | None = ...,
        temperature_65: float | None = ...,
        temperature_66: float | None = ...,
        temperature_67: float | None = ...,
        temperature_68: float | None = ...,
        temperature_69: float | None = ...,
        temperature_70: float | None = ...,
        temperature_71: float | None = ...,
        temperature_72: float | None = ...,
        temperature_73: float | None = ...,
        temperature_74: float | None = ...,
        temperature_75: float | None = ...,
        temperature_76: float | None = ...,
        temperature_77: float | None = ...,
        temperature_78: float | None = ...,
        temperature_79: float | None = ...,
        temperature_80: float | None = ...,
        temperature_81: float | None = ...,
        temperature_82: float | None = ...,
        temperature_83: float | None = ...,
        temperature_84: float | None = ...,
        temperature_85: float | None = ...,
        temperature_86: float | None = ...,
        temperature_87: float | None = ...,
        temperature_88: float | None = ...,
        temperature_89: float | None = ...,
        temperature_90: float | None = ...,
        temperature_91: float | None = ...,
        temperature_92: float | None = ...,
        temperature_93: float | None = ...,
        temperature_94: float | None = ...,
        temperature_95: float | None = ...,
        temperature_96: float | None = ...,
        temperature_97: float | None = ...,
        temperature_98: float | None = ...,
        temperature_99: float | None = ...,
        temperature_100: float | None = ...,
        temperature_101: float | None = ...,
        temperature_102: float | None = ...,
        temperature_103: float | None = ...,
        temperature_104: float | None = ...,
        temperature_105: float | None = ...,
        temperature_106: float | None = ...,
        temperature_107: float | None = ...,
        temperature_108: float | None = ...,
        temperature_109: float | None = ...,
        temperature_110: float | None = ...,
        temperature_111: float | None = ...,
        temperature_112: float | None = ...,
        temperature_113: float | None = ...,
        temperature_114: float | None = ...,
        temperature_115: float | None = ...,
        temperature_116: float | None = ...,
        temperature_117: float | None = ...,
        temperature_118: float | None = ...,
        temperature_119: float | None = ...,
        temperature_120: float | None = ...,
        temperature_121: float | None = ...,
        temperature_122: float | None = ...,
        temperature_123: float | None = ...,
        temperature_124: float | None = ...,
        temperature_125: float | None = ...,
        temperature_126: float | None = ...,
        temperature_127: float | None = ...,
        temperature_128: float | None = ...,
        temperature_129: float | None = ...,
        temperature_130: float | None = ...,
        temperature_131: float | None = ...,
        temperature_132: float | None = ...,
        temperature_133: float | None = ...,
        temperature_134: float | None = ...,
        temperature_135: float | None = ...,
        temperature_136: float | None = ...,
        temperature_137: float | None = ...,
        temperature_138: float | None = ...,
        temperature_139: float | None = ...,
        temperature_140: float | None = ...,
        temperature_141: float | None = ...,
        temperature_142: float | None = ...,
        temperature_143: float | None = ...,
        temperature_144: float | None = ...,
        temperature_145: float | None = ...,
        temperature_146: float | None = ...,
        temperature_147: float | None = ...,
        temperature_148: float | None = ...,
        temperature_149: float | None = ...,
        temperature_150: float | None = ...,
        temperature_151: float | None = ...,
        temperature_152: float | None = ...,
        temperature_153: float | None = ...,
        temperature_154: float | None = ...,
        temperature_155: float | None = ...,
        temperature_156: float | None = ...,
        temperature_157: float | None = ...,
        temperature_158: float | None = ...,
        temperature_159: float | None = ...,
        temperature_160: float | None = ...,
        temperature_161: float | None = ...,
        temperature_162: float | None = ...,
        temperature_163: float | None = ...,
        temperature_164: float | None = ...,
        temperature_165: float | None = ...,
        temperature_166: float | None = ...,
        temperature_167: float | None = ...,
        temperature_168: float | None = ...,
        temperature_169: float | None = ...,
        temperature_170: float | None = ...,
        temperature_171: float | None = ...,
        temperature_172: float | None = ...,
        temperature_173: float | None = ...,
        temperature_174: float | None = ...,
        temperature_175: float | None = ...,
        temperature_176: float | None = ...,
        temperature_177: float | None = ...,
        temperature_178: float | None = ...,
        temperature_179: float | None = ...,
        temperature_180: float | None = ...,
        temperature_181: float | None = ...,
        temperature_182: float | None = ...,
        temperature_183: float | None = ...,
        temperature_184: float | None = ...,
        temperature_185: float | None = ...,
        temperature_186: float | None = ...,
        temperature_187: float | None = ...,
        temperature_188: float | None = ...,
        temperature_189: float | None = ...,
        temperature_190: float | None = ...,
        temperature_191: float | None = ...,
        temperature_192: float | None = ...,
        temperature_193: float | None = ...,
        temperature_194: float | None = ...,
        temperature_195: float | None = ...,
        temperature_196: float | None = ...,
        temperature_197: float | None = ...,
        temperature_198: float | None = ...,
        temperature_199: float | None = ...,
        temperature_200: float | None = ...,
        temperature_201: float | None = ...,
        temperature_202: float | None = ...,
        temperature_203: float | None = ...,
        temperature_204: float | None = ...,
        temperature_205: float | None = ...,
        temperature_206: float | None = ...,
        temperature_207: float | None = ...,
        temperature_208: float | None = ...,
        temperature_209: float | None = ...,
        temperature_210: float | None = ...,
        temperature_211: float | None = ...,
        temperature_212: float | None = ...,
        temperature_213: float | None = ...,
        temperature_214: float | None = ...,
        temperature_215: float | None = ...,
        temperature_216: float | None = ...,
        temperature_217: float | None = ...,
        temperature_218: float | None = ...,
        temperature_219: float | None = ...,
        temperature_220: float | None = ...,
        temperature_221: float | None = ...,
        temperature_222: float | None = ...,
        temperature_223: float | None = ...,
        temperature_224: float | None = ...,
        temperature_225: float | None = ...,
        temperature_226: float | None = ...,
        temperature_227: float | None = ...,
        temperature_228: float | None = ...,
        temperature_229: float | None = ...,
        temperature_230: float | None = ...,
        temperature_231: float | None = ...,
        temperature_232: float | None = ...,
        temperature_233: float | None = ...,
        temperature_234: float | None = ...,
        temperature_235: float | None = ...,
        temperature_236: float | None = ...,
        temperature_237: float | None = ...,
        temperature_238: float | None = ...,
        temperature_239: float | None = ...,
        temperature_240: float | None = ...,
        temperature_241: float | None = ...,
        temperature_242: float | None = ...,
        temperature_243: float | None = ...,
        temperature_244: float | None = ...,
        temperature_245: float | None = ...,
        temperature_246: float | None = ...,
        temperature_247: float | None = ...,
        temperature_248: float | None = ...,
        temperature_249: float | None = ...,
        temperature_250: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``FluidProperties:Temperatures`` and add it to the document.

        property values for fluid properties list of up to 250 temperatures, note that number of property values must match the number of properties in other words, there must be a one-to-one correspondence between the property values in this list and the actual properties list in other syntax degrees C (for all temperature inputs)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fluid-properties/#fluidpropertiestemperatures
        """
