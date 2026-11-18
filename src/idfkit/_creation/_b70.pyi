"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class RunPeriodControlDaylightSavingTime:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        start_date: str,
        end_date: str,
        validate: bool = True,
    ) -> None:
        """Create a new ``RunPeriodControl:DaylightSavingTime`` and add it to the document.

        This object sets up the daylight saving time period for any RunPeriod. Ignores any daylight saving time period on the weather file and uses this definition. These are not used with SizingPeriod:DesignDay objects. Use with SizingPeriod:WeatherFileDays object can be controlled in that object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#runperiodcontroldaylightsavingtime
        """

class ZoneList:
    def __call__(
        self,
        name: str,
        /,
        *,
        zones: Sequence[_g.ZoneListZonesItem | _g.ZoneListZonesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneList`` and add it to the document.

        Defines a list of thermal zones which can be referenced as a group. The ZoneList name may be used elsewhere in the input to apply a parameter to all zones in the list. ZoneLists can be used effectively with the following objects: People, Lights, ElectricEquipment, GasEquipment, HotWaterEquipment, ZoneInfiltration:DesignFlowRate, ZoneVentilation:DesignFlowRate, Sizing:Zone, ZoneControl:Thermostat, and others.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#zonelist
        """

class AnyElectricEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_level_calculation_method: Literal["EquipmentLevel", "Watts/Area", "Watts/Person"]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        watts_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``ElectricEquipment`` and add it to the document.

        Sets internal gains for electric equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#electricequipment
        """

class HVACTemplatePlantTower:
    def __call__(
        self,
        name: str,
        /,
        *,
        tower_type: Literal["SingleSpeed", "TwoSpeed"],
        high_speed_nominal_capacity: float | Literal["Autosize"] | None = "Autosize",
        high_speed_fan_power: float | Literal["Autosize"] | None = "Autosize",
        low_speed_nominal_capacity: float | Literal["Autosize"] | None = "Autosize",
        low_speed_fan_power: float | Literal["Autosize"] | None = "Autosize",
        free_convection_capacity: float | Literal["Autosize"] | None = "Autosize",
        priority: str | None = ...,
        sizing_factor: float | None = 1,
        template_plant_loop_type: Literal["ChilledWater", "MixedWater"] | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Tower`` and add it to the document.

        This object adds a cooling tower to an HVACTemplate:Plant:ChilledWaterLoop or MixedWaterLoop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplanttower
        """

class AirTerminalSingleDuctParallelPIUReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        maximum_secondary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
        fan_on_flow_fraction: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_inlet_node_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        fan_control_type: Literal["ConstantSpeed", "VariableSpeed"] | None = "ConstantSpeed",
        minimum_fan_turn_down_ratio: float | None = 0.3,
        heating_control_type: Literal["Modulated", "Staged"] | None = ...,
        design_heating_discharge_air_temperature: float | None = 32.1,
        high_limit_heating_discharge_air_temperature: float | None = 37.7,
        backdraft_damper_leakage_fraction_curve_name: str | None = ...,
        backdraft_damper_leakage_zone_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ParallelPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, parallel powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductparallelpiureheat
        """

class FanSystemModel:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        design_maximum_air_flow_rate: float | Literal["Autosize"],
        design_pressure_rise: float,
        availability_schedule_name: str | None = ...,
        speed_control_method: Literal["Continuous", "Discrete"] | None = "Discrete",
        electric_power_minimum_flow_rate_fraction: float | None = 0.2,
        motor_efficiency: float | None = 0.9,
        motor_in_air_stream_fraction: float | None = 1,
        design_electric_power_consumption: float | Literal["Autosize"] | None = "Autosize",
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure", "TotalEfficiencyAndPressure"]
        | None = "PowerPerFlowPerPressure",
        electric_power_per_unit_flow_rate: float | None = ...,
        electric_power_per_unit_flow_rate_per_unit_pressure: float | None = 1.66667,
        fan_total_efficiency: float | None = 0.7,
        electric_power_function_of_flow_fraction_curve_name: str | None = ...,
        night_ventilation_mode_pressure_rise: float | None = ...,
        night_ventilation_mode_flow_fraction: float | None = ...,
        motor_loss_zone_name: str | None = ...,
        motor_loss_radiative_fraction: float | None = ...,
        end_use_subcategory: str | None = "General",
        number_of_speeds: int | None = 1,
        speed_fractions: Sequence[_g.FanSystemModelSpeedFractionsItem | _g.FanSystemModelSpeedFractionsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Fan:SystemModel`` and add it to the document.

        Versatile simple fan that can be used in variable air volume, constant volume, on-off cycling, two-speed or multi-speed applications. Performance at different flow rates, or speed levels, is determined using separate performance curve or table or prescribed power fractions at discrete speed levels for two-speed or multi-speed fans.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fansystemmodel
        """

class ThermalStorageIceDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        capacity: float | Literal["Autosize"],
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
        thermal_storage_sizing_object_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ThermalStorage:Ice:Detailed`` and add it to the document.

        This input syntax is intended to describe a thermal storage system that includes smaller containers filled with water that are placed in a larger tank or series of tanks. The model uses polynomial equations to describe the system performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstorageicedetailed
        """

class AnyPlantEquipmentList:
    def __call__(self, name: str, /, *, validate: bool = True) -> None:
        """Create a new ``PlantEquipmentList`` and add it to the document.

        List plant equipment in order of operating priority, 1st in list will be used 1st, etc Use only plant equipment in this list. If no equipment object types and equipment names are specified, then the corresponding PlantEquipmentOperation:* object will assume all available plant equipment for the loop should be OFF (not operate) within the specified lower/upper limit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentlist
        """

class AvailabilityManagerLowTemperatureTurnOff:
    def __call__(
        self,
        name: str,
        /,
        *,
        sensor_node_name: str,
        temperature: float,
        applicability_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AvailabilityManager:LowTemperatureTurnOff`` and add it to the document.

        Overrides fan/pump schedules depending on temperature at sensor node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerlowtemperatureturnoff
        """

class OutputTableSummaryReports:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        reports: Sequence[_g.OutputTableSummaryReportsReportsItem | _g.OutputTableSummaryReportsReportsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Table:SummaryReports`` and add it to the document.

        This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object and appear in the same files as the tabular reports. The entries for this object is a list of the predefined reports that should appear in the tabular report output file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-summaryreports/#outputtablesummaryreports
        """
