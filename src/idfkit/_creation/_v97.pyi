"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class HVACTemplatePlantBoiler_v8_9_to_v9_2:
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
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantboiler
        """

class AirTerminalSingleDuctUserDefined_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        number_of_plant_loop_connections: float,
        plant_connection_1_inlet_node_name: str,
        plant_connection_1_outlet_node_name: str,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        model_setup_and_sizing_program_calling_manager_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        secondary_air_outlet_node_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:UserDefined`` and add it to the document.

        Defines a generic single duct air terminal unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-user-defined-hvac-and-plant-component/#airterminalsingleductuserdefined
        """

class ZoneHVACHybridUnitaryHVAC_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        return_air_node_name: str,
        outdoor_air_node_name: str,
        supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        minimum_supply_air_temperature_schedule_name: str | None = ...,
        maximum_supply_air_temperature_schedule_name: str | None = ...,
        minimum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        maximum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        method_to_choose_controlled_inputs_and_part_runtime_fraction: Literal["Automatic", "User Defined"]
        | None = "Automatic",
        relief_node_name: str | None = ...,
        system_maximum_supply_air_flow_rate: float | None = ...,
        external_static_pressure_at_system_maximum_supply_air_flow_rate: float | None = ...,
        scaling_factor: float | None = 1,
        number_of_operating_modes: float | None = 1,
        minimum_time_between_mode_change: float | None = 10,
        first_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = "Electricity",
        second_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = "None",
        third_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = "None",
        objective_function_to_minimize: Literal["Electricity Use", "Second Fuel Use", "Third Fuel Use", "Water Use"]
        | None = "Electricity Use",
        design_specification_outdoor_air_object_name: str | None = ...,
        mode_0_name: str | None = ...,
        mode_0_supply_air_temperature_lookup_table_name: str | None = ...,
        mode_0_supply_air_humidity_ratio_lookup_table_name: str | None = ...,
        mode_0_system_electric_power_lookup_table_name: str | None = ...,
        mode_0_supply_fan_electric_power_lookup_table_name: str | None = ...,
        mode_0_external_static_pressure_lookup_table_name: str | None = ...,
        mode_0_system_second_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_third_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_water_use_lookup_table_name: str | None = ...,
        mode_0_outdoor_air_fraction: float | None = 0,
        mode_0_supply_air_mass_flow_rate_ratio: float | None = 0,
        modes: Sequence[_g.ZoneHVACHybridUnitaryHVACModesItem | _g.ZoneHVACHybridUnitaryHVACModesGroup] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:HybridUnitaryHVAC`` and add it to the document.

        Hybrid Unitary HVAC. A black box model for multi-mode packaged forced air equipment. Independent variables include outdoor air conditions and indoor air conditions. Controlled inputs include operating mode, supply air flow rate, and outdoor air faction. Emperical lookup tables are required to map supply air temperature supply air humidity, electricity use, fuel uses, water use, fan electricity use, and external static pressure as a function of each indpednent varaible and each controlled input. In each timestep the model will choose one or more combinations of settings for mode, supply air flow rate, outdoor air faction, and part runtime fraction so as to satisfy zone requests for sensible cooling, heating, ventilation, and/or dehumidification with the least resource consumption. Equipment in this class may consume electricity, water, and up to two additional fuel types.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-zone-forced-air-units/#zonehvachybridunitaryhvac
        """

class OutputTableSummaryReports_v9_4:
    def __call__(
        self,
        /,
        *,
        reports: Sequence[
            _vd.OutputTableSummaryReportsReportsItem_v9_4 | _vd.OutputTableSummaryReportsReportsGroup_v9_4
        ] = ...,
    ) -> None:
        """Create a new ``Output:Table:SummaryReports`` and add it to the document.

        This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object and appear in the same files as the tabular reports. The entries for this object is a list of the predefined reports that should appear in the tabular report output file. There should be as many fields (A) in this object as there are keys in the following (minus AllSummary+AllMonthly+AllSummaryAndMonthly)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/standard-output-reports/output-table-summaryreports/#outputtablesummaryreports
        """
