"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyZoneGroup:
    def __call__(self, name: str, /, *, zone_list_name: str, zone_list_multiplier: int | None = 1) -> None:
        """Create a new ``ZoneGroup`` and add it to the document.

        Adds a multiplier to a ZoneList. This can be used to reduce the amount of input necessary for simulating repetitive structures, such as the identical floors of a multi-story building.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#zonegroup
        """

class AnyCoilHeatingFuel:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fuel_type: Literal["Diesel", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"] | None = ...,
        burner_efficiency: float | None = 0.8,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Fuel`` and add it to the document.

        Gas or other fuel heating coil. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#coilheatingfuel
        """

class WaterHeaterStratified:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float | Literal["Autosize"],
        tank_height: float | Literal["Autosize"],
        heater_1_setpoint_temperature_schedule_name: str,
        heater_2_setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        end_use_subcategory: str | None = "General",
        tank_shape: Literal["HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        heater_priority_control: Literal["MasterSlave", "Simultaneous"] | None = "MasterSlave",
        heater_1_deadband_temperature_difference: float | None = 0,
        heater_1_capacity: float | Literal["Autosize"] | None = ...,
        heater_1_height: float | None = ...,
        heater_2_deadband_temperature_difference: float | None = 0,
        heater_2_capacity: float | None = ...,
        heater_2_height: float | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
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
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        off_cycle_parasitic_height: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
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
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_height: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        skin_loss_fraction_to_zone: float | None = 1,
        off_cycle_flue_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_flue_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        use_side_inlet_height: float | None = 0,
        use_side_outlet_height: float | Literal["Autocalculate"] | None = "Autocalculate",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        source_side_inlet_height: float | Literal["Autocalculate"] | None = "Autocalculate",
        source_side_outlet_height: float | None = 0,
        inlet_mode: Literal["Fixed", "Seeking"] | None = "Fixed",
        use_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        number_of_nodes: int | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
        node_11_additional_loss_coefficient: float | None = 0,
        node_12_additional_loss_coefficient: float | None = 0,
        source_side_flow_control_mode: Literal[
            "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``WaterHeater:Stratified`` and add it to the document.

        Water heater with stratified, multi-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:*.)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#waterheaterstratified
        """

class AnyDemandManagerLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        lights: Sequence[_g.DemandManagerLightsLightsItem | _g.DemandManagerLightsLightsGroup] = ...,
    ) -> None:
        """Create a new ``DemandManager:Lights`` and add it to the document.

        used for demand limiting Lights objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerlights
        """

class AnyOutputControlFiles:
    def __call__(
        self,
        /,
        *,
        output_csv: Literal["No", "Yes"] | None = "No",
        output_mtr: Literal["No", "Yes"] | None = "Yes",
        output_eso: Literal["No", "Yes"] | None = "Yes",
        output_eio: Literal["No", "Yes"] | None = "Yes",
        output_tabular: Literal["No", "Yes"] | None = "Yes",
        output_sqlite: Literal["No", "Yes"] | None = "Yes",
        output_json: Literal["No", "Yes"] | None = "Yes",
        output_audit: Literal["No", "Yes"] | None = "Yes",
        output_zone_sizing: Literal["No", "Yes"] | None = "Yes",
        output_system_sizing: Literal["No", "Yes"] | None = "Yes",
        output_dxf: Literal["No", "Yes"] | None = "Yes",
        output_bnd: Literal["No", "Yes"] | None = "Yes",
        output_rdd: Literal["No", "Yes"] | None = "Yes",
        output_mdd: Literal["No", "Yes"] | None = "Yes",
        output_mtd: Literal["No", "Yes"] | None = "Yes",
        output_end: Literal["No", "Yes"] | None = "Yes",
        output_shd: Literal["No", "Yes"] | None = "Yes",
        output_dfs: Literal["No", "Yes"] | None = "Yes",
        output_glhe: Literal["No", "Yes"] | None = "Yes",
        output_delightin: Literal["No", "Yes"] | None = "Yes",
        output_delighteldmp: Literal["No", "Yes"] | None = "Yes",
        output_delightdfdmp: Literal["No", "Yes"] | None = "Yes",
        output_edd: Literal["No", "Yes"] | None = "Yes",
        output_dbg: Literal["No", "Yes"] | None = "Yes",
        output_perflog: Literal["No", "Yes"] | None = "Yes",
        output_sln: Literal["No", "Yes"] | None = "Yes",
        output_sci: Literal["No", "Yes"] | None = "Yes",
        output_wrl: Literal["No", "Yes"] | None = "Yes",
        output_screen: Literal["No", "Yes"] | None = "Yes",
        output_extshd: Literal["No", "Yes"] | None = "Yes",
        output_tarcog: Literal["No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``OutputControl:Files`` and add it to the document.

        Conditionally turn on/off output from EnergyPlus.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputcontrolfiles
        """
