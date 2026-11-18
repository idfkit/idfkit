"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ShadingSiteDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        transmittance_schedule_name: str | None = ...,
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.ShadingSiteDetailedVerticesItem | _g.ShadingSiteDetailedVerticesGroup] = ...,
    ) -> None:
        """Create a new ``Shading:Site:Detailed`` and add it to the document.

        used for shading elements such as trees these items are fixed in space and would not move with relative geometry

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zones-and-surfaces/#shadingsitedetailed
        """

class PeopleDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_people_calculation_method: Literal["Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        people_per_floor_area: float | None = ...,
        floor_area_per_person: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["AngleFactor", "EnclosureAveraged", "SurfaceWeighted"]
        | None = "EnclosureAveraged",
        thermal_comfort_model_1_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_2_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_3_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_4_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_5_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_6_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_7_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
    ) -> None:
        """Create a new ``People:Definition`` and add it to the document.

        Defines the physical characteristics (number of people, heat gain fractions, CO2 generation rate and thermal comfort model selections) for occupants. Referenced by one or more People:Instance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#peopledefinition
        """

class AirflowNetworkMultiZoneWindPressureCoefficientValues:
    def __call__(
        self,
        name: str,
        /,
        *,
        airflownetwork_multizone_windpressurecoefficientarray_name: str,
        wind_pressure_coefficient_value_1: float,
        wind_pressure_coefficient_value_2: float,
        wind_pressure_coefficient_value_3: float | None = ...,
        wind_pressure_coefficient_value_4: float | None = ...,
        wind_pressure_coefficient_value_5: float | None = ...,
        wind_pressure_coefficient_value_6: float | None = ...,
        wind_pressure_coefficient_value_7: float | None = ...,
        wind_pressure_coefficient_value_8: float | None = ...,
        wind_pressure_coefficient_value_9: float | None = ...,
        wind_pressure_coefficient_value_10: float | None = ...,
        wind_pressure_coefficient_value_11: float | None = ...,
        wind_pressure_coefficient_value_12: float | None = ...,
        wind_pressure_coefficient_value_13: float | None = ...,
        wind_pressure_coefficient_value_14: float | None = ...,
        wind_pressure_coefficient_value_15: float | None = ...,
        wind_pressure_coefficient_value_16: float | None = ...,
        wind_pressure_coefficient_value_17: float | None = ...,
        wind_pressure_coefficient_value_18: float | None = ...,
        wind_pressure_coefficient_value_19: float | None = ...,
        wind_pressure_coefficient_value_20: float | None = ...,
        wind_pressure_coefficient_value_21: float | None = ...,
        wind_pressure_coefficient_value_22: float | None = ...,
        wind_pressure_coefficient_value_23: float | None = ...,
        wind_pressure_coefficient_value_24: float | None = ...,
        wind_pressure_coefficient_value_25: float | None = ...,
        wind_pressure_coefficient_value_26: float | None = ...,
        wind_pressure_coefficient_value_27: float | None = ...,
        wind_pressure_coefficient_value_28: float | None = ...,
        wind_pressure_coefficient_value_29: float | None = ...,
        wind_pressure_coefficient_value_30: float | None = ...,
        wind_pressure_coefficient_value_31: float | None = ...,
        wind_pressure_coefficient_value_32: float | None = ...,
        wind_pressure_coefficient_value_33: float | None = ...,
        wind_pressure_coefficient_value_34: float | None = ...,
        wind_pressure_coefficient_value_35: float | None = ...,
        wind_pressure_coefficient_value_36: float | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:WindPressureCoefficientValues`` and add it to the document.

        Used only if Wind Pressure Coefficient (WPC) Type = INPUT in the AirflowNetwork:SimulationControl object. The number of WPC numeric inputs must correspond to the number of wind direction inputs in the AirflowNetwork:Multizone:WindPressureCoefficientArray object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonewindpressurecoefficientvalues
        """

class HVACTemplatePlantBoiler:
    def __call__(
        self,
        name: str,
        /,
        *,
        boiler_type: Literal["CondensingHotWaterBoiler", "DistrictHotWater", "HotWaterBoiler"],
        capacity: float | Literal["Autosize"] | None = "Autosize",
        efficiency: float | None = 0.8,
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
        ]
        | None = ...,
        priority: str | None = ...,
        sizing_factor: float | None = 1,
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1.1,
        optimum_part_load_ratio: float | None = 1,
        water_outlet_upper_temperature_limit: float | None = 100,
        template_plant_loop_type: Literal["HotWater", "MixedWater"] | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Boiler`` and add it to the document.

        This object adds a boiler to an HVACTemplate:Plant:HotWaterLoop or MixedWaterLoop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantboiler
        """

class ZoneHVACBaseboardRadiantConvectiveSteamDesign:
    def __call__(
        self,
        name: str,
        /,
        *,
        fraction_radiant: float,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        convergence_tolerance: float | None = 0.001,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Steam:Design`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivesteamdesign
        """

class AnyCoilHeatingDesuperheater:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        availability_schedule_name: str | None = ...,
        heat_reclaim_recovery_efficiency: float | None = ...,
        temperature_setpoint_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as a unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdesuperheater
        """

class EvaporativeCoolerIndirectCelDekPad:
    def __call__(
        self,
        name: str,
        /,
        *,
        recirculating_water_pump_power_consumption: float,
        secondary_air_fan_flow_rate: float,
        secondary_air_fan_delta_pressure: float,
        indirect_heat_exchanger_effectiveness: float,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        direct_pad_area: float | Literal["Autosize"] | None = "Autosize",
        direct_pad_depth: float | Literal["Autosize"] | None = "Autosize",
        secondary_air_fan_total_efficiency: float | None = ...,
        control_type: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
    ) -> None:
        """Create a new ``EvaporativeCooler:Indirect:CelDekPad`` and add it to the document.

        Indirect evaporative cooler with rigid media evaporative pad, recirculating water pump, and secondary air fan. This model has no controls other than its availability schedule.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-evaporative-coolers/#evaporativecoolerindirectceldekpad
        """

class EnergyManagementSystemMeteredOutputVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        ems_variable_name: str,
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "MainsWaterSupply",
            "NaturalGas",
            "OnSiteWaterProduced",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "RainWaterCollected",
            "SolarAirHeating",
            "SolarWaterHeating",
            "WaterUse",
            "WellWaterDrawn",
        ],
        group_type: Literal["Building", "HVAC", "Plant", "System"],
        end_use_category: Literal[
            "Baseboard",
            "Boilers",
            "Chillers",
            "Cooling",
            "CoolingCoils",
            "ExteriorEquipment",
            "ExteriorLights",
            "Fans",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "Heating",
            "HeatingCoils",
            "Humidifier",
            "InteriorEquipment",
            "InteriorLights",
            "OnSiteGeneration",
            "Pumps",
            "Refrigeration",
            "WaterSystems",
        ],
        ems_program_or_subroutine_name: str | None = ...,
        end_use_subcategory: str | None = ...,
        units: str | None = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:MeteredOutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from an Erl variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemmeteredoutputvariable
        """

class FluidPropertiesConcentration:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        fluid_name: str | None = ...,
        fluid_property_type: Literal["Conductivity", "Density", "SpecificHeat", "Viscosity"] | None = ...,
        temperature_values_name: str | None = ...,
        concentration: float | None = ...,
        property_value_1: float | None = ...,
        property_value_2: float | None = ...,
        property_value_3: float | None = ...,
        property_value_4: float | None = ...,
        property_value_5: float | None = ...,
        property_value_6: float | None = ...,
        property_value_7: float | None = ...,
        property_value_8: float | None = ...,
        property_value_9: float | None = ...,
        property_value_10: float | None = ...,
        property_value_11: float | None = ...,
        property_value_12: float | None = ...,
        property_value_13: float | None = ...,
        property_value_14: float | None = ...,
        property_value_15: float | None = ...,
        property_value_16: float | None = ...,
        property_value_17: float | None = ...,
        property_value_18: float | None = ...,
        property_value_19: float | None = ...,
        property_value_20: float | None = ...,
        property_value_21: float | None = ...,
        property_value_22: float | None = ...,
        property_value_23: float | None = ...,
        property_value_24: float | None = ...,
        property_value_25: float | None = ...,
        property_value_26: float | None = ...,
        property_value_27: float | None = ...,
        property_value_28: float | None = ...,
        property_value_29: float | None = ...,
        property_value_30: float | None = ...,
        property_value_31: float | None = ...,
        property_value_32: float | None = ...,
        property_value_33: float | None = ...,
        property_value_34: float | None = ...,
        property_value_35: float | None = ...,
        property_value_36: float | None = ...,
        property_value_37: float | None = ...,
        property_value_38: float | None = ...,
        property_value_39: float | None = ...,
        property_value_40: float | None = ...,
        property_value_41: float | None = ...,
        property_value_42: float | None = ...,
        property_value_43: float | None = ...,
        property_value_44: float | None = ...,
        property_value_45: float | None = ...,
        property_value_46: float | None = ...,
        property_value_47: float | None = ...,
        property_value_48: float | None = ...,
        property_value_49: float | None = ...,
        property_value_50: float | None = ...,
        property_value_51: float | None = ...,
        property_value_52: float | None = ...,
        property_value_53: float | None = ...,
        property_value_54: float | None = ...,
        property_value_55: float | None = ...,
        property_value_56: float | None = ...,
        property_value_57: float | None = ...,
        property_value_58: float | None = ...,
        property_value_59: float | None = ...,
        property_value_60: float | None = ...,
        property_value_61: float | None = ...,
        property_value_62: float | None = ...,
        property_value_63: float | None = ...,
        property_value_64: float | None = ...,
        property_value_65: float | None = ...,
        property_value_66: float | None = ...,
        property_value_67: float | None = ...,
        property_value_68: float | None = ...,
        property_value_69: float | None = ...,
        property_value_70: float | None = ...,
        property_value_71: float | None = ...,
        property_value_72: float | None = ...,
        property_value_73: float | None = ...,
        property_value_74: float | None = ...,
        property_value_75: float | None = ...,
        property_value_76: float | None = ...,
        property_value_77: float | None = ...,
        property_value_78: float | None = ...,
        property_value_79: float | None = ...,
        property_value_80: float | None = ...,
        property_value_81: float | None = ...,
        property_value_82: float | None = ...,
        property_value_83: float | None = ...,
        property_value_84: float | None = ...,
        property_value_85: float | None = ...,
        property_value_86: float | None = ...,
        property_value_87: float | None = ...,
        property_value_88: float | None = ...,
        property_value_89: float | None = ...,
        property_value_90: float | None = ...,
        property_value_91: float | None = ...,
        property_value_92: float | None = ...,
        property_value_93: float | None = ...,
        property_value_94: float | None = ...,
        property_value_95: float | None = ...,
        property_value_96: float | None = ...,
        property_value_97: float | None = ...,
        property_value_98: float | None = ...,
        property_value_99: float | None = ...,
        property_value_100: float | None = ...,
        property_value_101: float | None = ...,
        property_value_102: float | None = ...,
        property_value_103: float | None = ...,
        property_value_104: float | None = ...,
        property_value_105: float | None = ...,
        property_value_106: float | None = ...,
        property_value_107: float | None = ...,
        property_value_108: float | None = ...,
        property_value_109: float | None = ...,
        property_value_110: float | None = ...,
        property_value_111: float | None = ...,
        property_value_112: float | None = ...,
        property_value_113: float | None = ...,
        property_value_114: float | None = ...,
        property_value_115: float | None = ...,
        property_value_116: float | None = ...,
        property_value_117: float | None = ...,
        property_value_118: float | None = ...,
        property_value_119: float | None = ...,
        property_value_120: float | None = ...,
        property_value_121: float | None = ...,
        property_value_122: float | None = ...,
        property_value_123: float | None = ...,
        property_value_124: float | None = ...,
        property_value_125: float | None = ...,
        property_value_126: float | None = ...,
        property_value_127: float | None = ...,
        property_value_128: float | None = ...,
        property_value_129: float | None = ...,
        property_value_130: float | None = ...,
        property_value_131: float | None = ...,
        property_value_132: float | None = ...,
        property_value_133: float | None = ...,
        property_value_134: float | None = ...,
        property_value_135: float | None = ...,
        property_value_136: float | None = ...,
        property_value_137: float | None = ...,
        property_value_138: float | None = ...,
        property_value_139: float | None = ...,
        property_value_140: float | None = ...,
        property_value_141: float | None = ...,
        property_value_142: float | None = ...,
        property_value_143: float | None = ...,
        property_value_144: float | None = ...,
        property_value_145: float | None = ...,
        property_value_146: float | None = ...,
        property_value_147: float | None = ...,
        property_value_148: float | None = ...,
        property_value_149: float | None = ...,
        property_value_150: float | None = ...,
        property_value_151: float | None = ...,
        property_value_152: float | None = ...,
        property_value_153: float | None = ...,
        property_value_154: float | None = ...,
        property_value_155: float | None = ...,
        property_value_156: float | None = ...,
        property_value_157: float | None = ...,
        property_value_158: float | None = ...,
        property_value_159: float | None = ...,
        property_value_160: float | None = ...,
        property_value_161: float | None = ...,
        property_value_162: float | None = ...,
        property_value_163: float | None = ...,
        property_value_164: float | None = ...,
        property_value_165: float | None = ...,
        property_value_166: float | None = ...,
        property_value_167: float | None = ...,
        property_value_168: float | None = ...,
        property_value_169: float | None = ...,
        property_value_170: float | None = ...,
        property_value_171: float | None = ...,
        property_value_172: float | None = ...,
        property_value_173: float | None = ...,
        property_value_174: float | None = ...,
        property_value_175: float | None = ...,
        property_value_176: float | None = ...,
        property_value_177: float | None = ...,
        property_value_178: float | None = ...,
        property_value_179: float | None = ...,
        property_value_180: float | None = ...,
        property_value_181: float | None = ...,
        property_value_182: float | None = ...,
        property_value_183: float | None = ...,
        property_value_184: float | None = ...,
        property_value_185: float | None = ...,
        property_value_186: float | None = ...,
        property_value_187: float | None = ...,
        property_value_188: float | None = ...,
        property_value_189: float | None = ...,
        property_value_190: float | None = ...,
        property_value_191: float | None = ...,
        property_value_192: float | None = ...,
        property_value_193: float | None = ...,
        property_value_194: float | None = ...,
        property_value_195: float | None = ...,
        property_value_196: float | None = ...,
        property_value_197: float | None = ...,
        property_value_198: float | None = ...,
        property_value_199: float | None = ...,
        property_value_200: float | None = ...,
        property_value_201: float | None = ...,
        property_value_202: float | None = ...,
        property_value_203: float | None = ...,
        property_value_204: float | None = ...,
        property_value_205: float | None = ...,
        property_value_206: float | None = ...,
        property_value_207: float | None = ...,
        property_value_208: float | None = ...,
        property_value_209: float | None = ...,
        property_value_210: float | None = ...,
        property_value_211: float | None = ...,
        property_value_212: float | None = ...,
        property_value_213: float | None = ...,
        property_value_214: float | None = ...,
        property_value_215: float | None = ...,
        property_value_216: float | None = ...,
        property_value_217: float | None = ...,
        property_value_218: float | None = ...,
        property_value_219: float | None = ...,
        property_value_220: float | None = ...,
        property_value_221: float | None = ...,
        property_value_222: float | None = ...,
        property_value_223: float | None = ...,
        property_value_224: float | None = ...,
        property_value_225: float | None = ...,
        property_value_226: float | None = ...,
        property_value_227: float | None = ...,
        property_value_228: float | None = ...,
        property_value_229: float | None = ...,
        property_value_230: float | None = ...,
        property_value_231: float | None = ...,
        property_value_232: float | None = ...,
        property_value_233: float | None = ...,
        property_value_234: float | None = ...,
        property_value_235: float | None = ...,
        property_value_236: float | None = ...,
        property_value_237: float | None = ...,
        property_value_238: float | None = ...,
        property_value_239: float | None = ...,
        property_value_240: float | None = ...,
        property_value_241: float | None = ...,
        property_value_242: float | None = ...,
        property_value_243: float | None = ...,
        property_value_244: float | None = ...,
        property_value_245: float | None = ...,
        property_value_246: float | None = ...,
        property_value_247: float | None = ...,
        property_value_248: float | None = ...,
        property_value_249: float | None = ...,
        property_value_250: float | None = ...,
    ) -> None:
        """Create a new ``FluidProperties:Concentration`` and add it to the document.

        fluid properties for water/other fluid mixtures

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fluid-properties/#fluidpropertiesconcentration
        """
