"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class ZoneGroup:
    def __call__(self, name: str, /, *, zone_list_name: str, zone_list_multiplier: int | None = 1) -> None:
        """Create a new ``ZoneGroup`` and add it to the document.

        Adds a multiplier to a ZoneList. This can be used to reduce the amount of input necessary for simulating repetitive structures, such as the identical floors of a multi-story building.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#zonegroup
        """

class AnyWindowPropertyStormWindow:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        window_name: str,
        storm_glass_layer_name: str,
        month_that_storm_glass_layer_is_put_on: int,
        day_of_month_that_storm_glass_layer_is_put_on: int,
        month_that_storm_glass_layer_is_taken_off: int,
        day_of_month_that_storm_glass_layer_is_taken_off: int,
        distance_between_storm_glass_layer_and_adjacent_glass: float | None = 0.05,
    ) -> None:
        """Create a new ``WindowProperty:StormWindow`` and add it to the document.

        This is a movable exterior glass layer that is usually applied in the winter and removed in the summer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertystormwindow
        """

class AnyZoneHVACPackagedTerminalAirConditioner:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["", "None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalAirConditioner`` and add it to the document.

        Packaged terminal air conditioner (PTAC). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam) and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalairconditioner
        """

class AnyCoilCoolingDXCurveFitOperatingMode:
    def __call__(
        self,
        name: str,
        /,
        *,
        speed_1_name: str,
        rated_gross_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_evaporator_air_flow_rate: float | Literal["Autosize"] | None = ...,
        rated_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        apply_latent_degradation_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        nominal_evaporative_condenser_pump_power: float | Literal["", "Autosize"] | None = 0,
        nominal_speed_number: int | None = ...,
        speed_2_name: str | None = ...,
        speed_3_name: str | None = ...,
        speed_4_name: str | None = ...,
        speed_5_name: str | None = ...,
        speed_6_name: str | None = ...,
        speed_7_name: str | None = ...,
        speed_8_name: str | None = ...,
        speed_9_name: str | None = ...,
        speed_10_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:OperatingMode`` and add it to the document.

        DX cooling coil performance for a single operating mode which may have one or more speeds.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitoperatingmode
        """

class AnyCoilHeatingGasMultiStage:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: int,
        stage_1_gas_burner_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        stage_2_gas_burner_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_gas_burner_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_gas_burner_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Gas:MultiStage`` and add it to the document.

        Gas heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatinggasmultistage
        """

class HeatPumpWaterToWaterParameterEstimationCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        nominal_cop: float | None = ...,
        nominal_capacity: float | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        load_side_flow_rate: float | None = ...,
        source_side_flow_rate: float | None = ...,
        load_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        piston_displacement: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        compressor_suction_and_discharge_pressure_drop: float | None = ...,
        superheating: float | None = ...,
        constant_part_of_electromechanical_power_losses: float | None = ...,
        loss_factor: float | None = ...,
        high_pressure_cut_off: float | None = 500000000,
        low_pressure_cut_off: float | None = 0,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:ParameterEstimation:Cooling`` and add it to the document.

        OSU parameter estimation model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterparameterestimationcooling
        """

class SetpointManagerSingleZoneHumidityMaximum:
    def __call__(self, name: str, /, *, setpoint_node_or_nodelist_name: str, control_zone_air_node_name: str) -> None:
        """Create a new ``SetpointManager:SingleZone:Humidity:Maximum`` and add it to the document.

        The Single Zone Maximum Humidity Setpoint Manager allows the control of a single zone maximum humidity level. This setpoint manager can be used in conjunction with object ZoneControl:Humidistat to detect humidity levels.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersinglezonehumiditymaximum
        """

class OutputSurfacesDrawing:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        report_type: Literal["DXF", "DXF:WireFrame", "VRML"],
        report_specifications_1: Literal["", "RegularPolyline", "ThickPolyline", "Triangulate3DFace"]
        | None = "Triangulate3DFace",
        report_specifications_2: str | None = ...,
    ) -> None:
        """Create a new ``Output:Surfaces:Drawing`` and add it to the document.

        Produces reports/files that are capable of rendering graphically or being imported into other programs. Rendering does not alter the actual inputs/surfaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputsurfacesdrawing
        """
