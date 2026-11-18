"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class ZoneHVACTerminalUnitVariableRefrigerantFlow_v9_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        terminal_unit_air_inlet_node_name: str,
        terminal_unit_air_outlet_node_name: str,
        supply_air_fan_operating_mode_schedule_name: str,
        supply_air_fan_object_name: str,
        terminal_unit_availability_schedule: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"]
        | None = "Fan:ConstantVolume",
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
    ) -> None:
        """Create a new ``ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`` and add it to the document.

        Zone terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air heat pump). The VRF terminal units are served by an AirConditioner:VariableRefrigerantFlow or AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:* system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-zone-forced-air-units/#zonehvacterminalunitvariablerefrigerantflow
        """

class OutputSQLite_v9_5_to_v23_2:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        option_type: Literal["Simple", "SimpleAndTabular"] | None = ...,
        unit_conversion_for_tabular_data: Literal[
            "InchPound", "JtoGJ", "JtoKWH", "JtoMJ", "None", "UseOutputControlTableStyle"
        ]
        | None = "UseOutputControlTableStyle",
    ) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/input-for-output/#outputsqlite
        """

class InternalMass_v24_2_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        surface_area: float,
        zone_or_zonelist_name: str | None = ...,
        space_or_spacelist_name: str | None = ...,
    ) -> None:
        """Create a new ``InternalMass`` and add it to the document.

        Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList. Likewise for SpaceList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-thermal-zone-description-geometry/#internalmass
        """
