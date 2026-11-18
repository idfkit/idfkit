"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class ExteriorFuelEquipment_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_use_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ],
        schedule_name: str,
        design_level: float,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Exterior:FuelEquipment`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-exterior-energy-use-equipment/#exteriorfuelequipment
        """

class PhotovoltaicPerformanceSandia_v8_9_to_v22_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        active_area: float | None = 1,
        number_of_cells_in_series: float | None = 1,
        number_of_cells_in_parallel: float | None = 1,
        short_circuit_current: float | None = ...,
        open_circuit_voltage: float | None = ...,
        current_at_maximum_power_point: float | None = ...,
        voltage_at_maximum_power_point: float | None = ...,
        sandia_database_parameter_aisc: float | None = ...,
        sandia_database_parameter_aimp: float | None = ...,
        sandia_database_parameter_c0: float | None = ...,
        sandia_database_parameter_c1: float | None = ...,
        sandia_database_parameter_bvoc0: float | None = ...,
        sandia_database_parameter_mbvoc: float | None = ...,
        sandia_database_parameter_bvmp0: float | None = ...,
        sandia_database_parameter_mbvmp: float | None = ...,
        diode_factor: float | None = ...,
        sandia_database_parameter_c2: float | None = ...,
        sandia_database_parameter_c3: float | None = ...,
        sandia_database_parameter_a0: float | None = ...,
        sandia_database_parameter_a1: float | None = ...,
        sandia_database_parameter_a2: float | None = ...,
        sandia_database_parameter_a3: float | None = ...,
        sandia_database_parameter_a4: float | None = ...,
        sandia_database_parameter_b0: float | None = ...,
        sandia_database_parameter_b1: float | None = ...,
        sandia_database_parameter_b2: float | None = ...,
        sandia_database_parameter_b3: float | None = ...,
        sandia_database_parameter_b4: float | None = ...,
        sandia_database_parameter_b5: float | None = ...,
        sandia_database_parameter_delta_tc_: float | None = ...,
        sandia_database_parameter_fd: float | None = ...,
        sandia_database_parameter_a: float | None = ...,
        sandia_database_parameter_b: float | None = ...,
        sandia_database_parameter_c4: float | None = ...,
        sandia_database_parameter_c5: float | None = ...,
        sandia_database_parameter_ix0: float | None = ...,
        sandia_database_parameter_ixx0: float | None = ...,
        sandia_database_parameter_c6: float | None = ...,
        sandia_database_parameter_c7: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Sandia`` and add it to the document.

        Describes performance input data needed for specific makes and models of production PV panels using the empirical coefficients assembled by Sandia National Laboratory.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesandia
        """

class FaultModelPressureSensorOffsetOutdoorAir_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        pressure_sensor_offset: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``FaultModel:PressureSensorOffset:OutdoorAir`` and add it to the document.

        This object describes outdoor air pressure sensor offset
        """

class HotWaterEquipment_v9_6_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_zone_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``HotWaterEquipment`` and add it to the document.

        Sets internal gains for hot water equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-internal-gains-people-lights-other/#hotwaterequipment
        """

class CentralHeatPumpSystem_v22_2_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_loop_inlet_node_name: str,
        cooling_loop_outlet_node_name: str,
        source_loop_inlet_node_name: str,
        source_loop_outlet_node_name: str,
        heating_loop_inlet_node_name: str,
        heating_loop_outlet_node_name: str,
        chiller_heater_modules_performance_component_object_type_1: Literal["ChillerHeaterPerformance:Electric:EIR"],
        chiller_heater_modules_performance_component_name_1: str,
        chiller_heater_modules_control_schedule_name_1: str,
        control_method: Literal["SmartMixing"] | None = "SmartMixing",
        ancillary_power: float | None = 0,
        ancillary_operation_schedule_name: str | None = ...,
        number_of_chiller_heater_modules_1: int | None = 1,
        chiller_heater_modules_performance_component_object_type_2: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_2: str | None = ...,
        chiller_heater_modules_control_schedule_name_2: str | None = ...,
        number_of_chiller_heater_modules_2: int | None = 1,
        chiller_heater_performance_component_object_type_3: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_performance_component_name_3: str | None = ...,
        chiller_heater_modules_control_schedule_name_3: str | None = ...,
        number_of_chiller_heater_modules_3: int | None = 1,
        chiller_heater_modules_performance_component_object_type_4: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_4: str | None = ...,
        chiller_heater_modules_control_schedule_name_4: str | None = ...,
        number_of_chiller_heater_modules_4: int | None = 1,
        chiller_heater_modules_performance_component_object_type_5: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_models_performance_component_name_5: str | None = ...,
        chiller_heater_modules_control_schedule_name_5: str | None = ...,
        number_of_chiller_heater_modules_5: int | None = 1,
        chiller_heater_modules_performance_component_object_type_6: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_6: str | None = ...,
        chiller_heater_modules_control_schedule_name_6: str | None = ...,
        number_of_chiller_heater_modules_6: int | None = 1,
        chiller_heater_modules_performance_component_object_type_7: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_7: str | None = ...,
        chiller_heater_modules_control_schedule_name_7: str | None = ...,
        number_of_chiller_heater_modules_7: int | None = 1,
        chiller_heater_modules_performance_component_object_type_8: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_8: str | None = ...,
        chiller_heater_modules_control_schedule_name_8: str | None = ...,
        number_of_chiller_heater_modules_8: int | None = 1,
        chiller_heater_modules_performance_component_object_type_9: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_9: str | None = ...,
        chiller_heater_modules_control_schedule_name_9: str | None = ...,
        number_of_chiller_heater_modules_9: int | None = 1,
        chiller_heater_modules_performance_component_object_type_10: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_10: str | None = ...,
        chiller_heater_modules_control_schedule_name_10: str | None = ...,
        number_of_chiller_heater_modules_10: int | None = 1,
        chiller_heater_modules_performance_component_object_type_11: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_11: str | None = ...,
        chiller_heater_module_control_schedule_name_11: str | None = ...,
        number_of_chiller_heater_modules_11: int | None = 1,
        chiller_heater_modules_performance_component_object_type_12: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_12: str | None = ...,
        chiller_heater_modules_control_schedule_name_12: str | None = ...,
        number_of_chiller_heater_modules_12: int | None = 1,
        chiller_heater_modules_performance_component_object_type_13: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_13: str | None = ...,
        chiller_heater_modules_control_schedule_name_13: str | None = ...,
        number_of_chiller_heater_modules_13: int | None = 1,
        chiller_heater_modules_performance_component_object_type_14: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_14: str | None = ...,
        chiller_heater_modules_control_schedule_name_14: str | None = ...,
        number_of_chiller_heater_modules_14: int | None = 1,
        chiller_heater_modules_performance_component_object_type_15: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_15: str | None = ...,
        chiller_heater_modules_control_schedule_name_15: str | None = ...,
        number_of_chiller_heater_modules_15: int | None = 1,
        chiller_heater_modules_performance_component_object_type_16: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_16: str | None = ...,
        chiller_heater_modules_control_schedule_name_16: str | None = ...,
        number_of_chiller_heater_modules_16: int | None = 1,
        chiller_heater_modules_performance_component_object_type_17: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_17: str | None = ...,
        chiller_heater_modules_control_schedule_name_17: str | None = ...,
        number_of_chiller_heater_modules_17: int | None = 1,
        chiller_heater_modules_performance_component_object_type_18: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_18: str | None = ...,
        chiller_heater_modules_control_control_schedule_name_18: str | None = ...,
        number_of_chiller_heater_modules_18: int | None = 1,
        chiller_heater_modules_performance_component_object_type_19: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_19: str | None = ...,
        chiller_heater_modules_control_schedule_name_19: str | None = ...,
        number_of_chiller_heater_modules_19: int | None = 1,
        chiller_heater_modules_performance_component_object_type_20: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_20: str | None = ...,
        chiller_heater_modules_control_schedule_name_20: str | None = ...,
        number_of_chiller_heater_modules_20: int | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``CentralHeatPumpSystem`` and add it to the document.

        This chiller bank can contain multiple chiller heaters and heat pump performance objects. Its function is to encapsulate the extra controls needed to turn individual modules on/off and whether they are to operate in cooling-only, heating-only or simultaneous cooling/heating mode and whether to connect the source water to the evaporator or condenser side.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-plant-equipment/#centralheatpumpsystem
        """
