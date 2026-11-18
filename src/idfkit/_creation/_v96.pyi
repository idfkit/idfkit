"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class OutputControlTableStyle_v24_1_to_v25_1:
    def __call__(
        self,
        /,
        *,
        column_separator: Literal[
            "All", "Comma", "CommaAndHTML", "CommaAndXML", "Fixed", "HTML", "Tab", "TabAndHTML", "XML", "XMLandHTML"
        ]
        | None = "Comma",
        unit_conversion: Literal["InchPound", "InchPoundExceptElectricity", "JtoGJ", "JtoKWH", "JtoMJ", "None"]
        | None = "None",
    ) -> None:
        """Create a new ``OutputControl:Table:Style`` and add it to the document.

        default style for the OutputControl:Table:Style is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may be a better choice. fixed puts spaces between the 'columns'. HTML produces tables in HTML. XML produces an XML file. note - if no OutputControl:Table:Style is included, the defaults are comma and None.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/standard-output-reports/outputcontrol-table-style/#outputcontroltablestyle
        """

class AirLoopHVACOutdoorAirSystem_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_list_name: str,
        outdoor_air_equipment_list_name: str,
        availability_manager_list_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:OutdoorAirSystem`` and add it to the document.

        Outdoor air subsystem for an AirLoopHVAC. Includes an outdoor air mixing box and optional outdoor air conditioning equipment such as heat recovery, preheat, and precool coils. From the perspective of the primary air loop the outdoor air system is treated as a single component.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-air-distribution/#airloophvacoutdoorairsystem
        """

class CoilSystemCoolingDX_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        dx_cooling_coil_system_inlet_node_name: str,
        dx_cooling_coil_system_outlet_node_name: str,
        dx_cooling_coil_system_sensor_node_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        run_on_sensible_load: Literal["No", "Yes"] | None = "Yes",
        run_on_latent_load: Literal["No", "Yes"] | None = "No",
        use_outdoor_air_dx_cooling_coil: Literal["No", "Yes"] | None = "No",
        outdoor_air_dx_cooling_coil_leaving_minimum_air_temperature: float | None = 2,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX`` and add it to the document.

        Virtual container component that consists of a DX cooling coil and its associated controls. This control object supports several different types of DX cooling coils and may be placed directly in an air loop branch or outdoor air equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdx
        """

class DemandManagerVentilation_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["FixedRate", "Off", "ReductionRatio"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: float | None = ...,
        fixed_rate: float | None = ...,
        reduction_ratio: float | None = ...,
        limit_step_change: float | None = ...,
        selection_control: Literal["All", "RotateMany", "RotateOne"] | None = "All",
        rotation_duration: float | None = ...,
        controllers: Sequence[
            _g.DemandManagerVentilationControllersItem | _g.DemandManagerVentilationControllersGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManager:Ventilation`` and add it to the document.

        used for demand limiting Controller:OutdoorAir objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-demand-limiting-controls/#demandmanagerventilation
        """

class EnergyManagementSystemProgram_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        lines: Sequence[_g.EnergyManagementSystemProgramLinesItem | _g.EnergyManagementSystemProgramLinesGroup] = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:Program`` and add it to the document.

        This input defines an Erl program Each field after the name is a line of EMS Runtime Language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemprogram
        """

class ZoneHVACBaseboardRadiantConvectiveWater_v9_5_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_water_flow_rate: float | Literal["Autosize"],
        design_object: str | None = ...,
        availability_schedule_name: str | None = ...,
        rated_average_water_temperature: float | None = 87.78,
        rated_water_mass_flow_rate: float | None = 0.063,
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        surface_fractions: Sequence[
            _g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsItem
            | _g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivewater
        """
