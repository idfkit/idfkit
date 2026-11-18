"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class SiteVariableLocation:
    def __call__(
        self,
        name: str,
        /,
        *,
        building_location_latitude_schedule: str | None = ...,
        building_location_longitude_schedule: str | None = ...,
        building_location_orientation_schedule: str | None = ...,
    ) -> None:
        """Create a new ``Site:VariableLocation`` and add it to the document.

        Captures the scheduling of a moving/reorienting building, or more likely a vessel

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitevariablelocation
        """

class AnyFloorGroundContact:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Floor:GroundContact`` and add it to the document.

        Allows for simplified entry of exterior floors with ground contact. View Factors to Ground is automatically calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#floorgroundcontact
        """

class AnyZoneMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        delta_temperature: float | None = 0,
        delta_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneMixing`` and add it to the document.

        ZoneMixing is a simple air exchange from one zone or space to another. Note that this statement only affects the energy balance of the 'receiving' zone or space and will not produce any effect on the 'source' zone. Mixing statements can be complementary and include multiple zones, but the balancing of flows between zones is left to the user's discretion.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonemixing
        """

class ZoneHVACWindowAirConditioner:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_supply_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"],
        outdoor_air_mixer_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        dx_cooling_coil_name: str,
        fan_placement: Literal["BlowThrough", "DrawThrough"],
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        cooling_convergence_tolerance: float | None = 0.001,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:WindowAirConditioner`` and add it to the document.

        Window air conditioner. Forced-convection cooling-only unit with supply fan, direct expansion (DX) cooling coil, and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacwindowairconditioner
        """

class WaterHeaterSizing:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        waterheater_name: str,
        design_mode: Literal[
            "PeakDraw", "PerFloorArea", "PerPerson", "PerSolarCollectorArea", "PerUnit", "ResidentialHUD-FHAMinimum"
        ]
        | None = ...,
        time_storage_can_meet_peak_draw: float | None = ...,
        time_for_tank_recovery: float | None = ...,
        nominal_tank_volume_for_autosizing_plant_connections: float | None = ...,
        number_of_bedrooms: int | None = ...,
        number_of_bathrooms: int | None = ...,
        storage_capacity_per_person: float | None = ...,
        recovery_capacity_per_person: float | None = ...,
        storage_capacity_per_floor_area: float | None = ...,
        recovery_capacity_per_floor_area: float | None = ...,
        number_of_units: float | None = ...,
        storage_capacity_per_unit: float | None = ...,
        recovery_capacity_perunit: float | None = ...,
        storage_capacity_per_collector_area: float | None = ...,
        height_aspect_ratio: float | None = ...,
    ) -> None:
        """Create a new ``WaterHeater:Sizing`` and add it to the document.

        This input object is used with WaterHeater:Mixed or with WaterHeater:Stratified to autosize tank volume and heater capacity This object is not needed if water heaters are not autosized.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#waterheatersizing
        """

class SetpointManagerSingleZoneCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        zone_node_name: str,
        zone_inlet_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        minimum_supply_air_temperature: float | None = -99,
        maximum_supply_air_temperature: float | None = 99,
    ) -> None:
        """Create a new ``SetpointManager:SingleZone:Cooling`` and add it to the document.

        This setpoint manager detects the control zone load to meet the current cooling setpoint, zone inlet node flow rate, and zone node temperature, and calculates a setpoint temperature for the supply air that will satisfy the zone cooling load for the control zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersinglezonecooling
        """

class SetpointManagerMixedAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_setpoint_node_name: str,
        fan_inlet_node_name: str,
        fan_outlet_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        cooling_coil_inlet_node_name: str | None = ...,
        cooling_coil_outlet_node_name: str | None = ...,
        minimum_temperature_at_cooling_coil_outlet_node: float | None = 7.2,
    ) -> None:
        """Create a new ``SetpointManager:MixedAir`` and add it to the document.

        The Mixed Air Setpoint Manager is meant to be used in conjunction with a Controller:OutdoorAir object. This setpoint manager is used to establish a temperature setpoint at the mixed air node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagermixedair
        """

class CurveQuadLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_w: float,
        coefficient3_x: float,
        coefficient4_y: float,
        coefficient5_z: float,
        minimum_value_of_w: float,
        maximum_value_of_w: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_value_of_z: float,
        maximum_value_of_z: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_w: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_x: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_z: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:QuadLinear`` and add it to the document.

        Linear curve with four independent variables. Input for the linear curve consists of a curve name, the two coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*w + C3*x + C4*y + C5*z

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvequadlinear
        """

class OutputVariableDictionary:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        key_field: Literal["", "IDF", "regular"] | None = "regular",
        sort_option: Literal["Name", "Unsorted"] | None = ...,
    ) -> None:
        """Create a new ``Output:VariableDictionary`` and add it to the document.

        Produces a list summarizing the output variables and meters that are available for reporting for the model being simulated (rdd output file). The list varies depending on the types of objects present in the idf file. For example, variables related to lights will only appear if a Lights object is present. The IDF option generates complete Output:Variable objects to simplify adding the desired output to the idf file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputvariabledictionary
        """
