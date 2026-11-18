"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class GlazedDoorInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        outside_boundary_condition_object: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``GlazedDoor:Interzone`` and add it to the document.

        Allows for simplified entry of interzone (glass interior) doors (adjacent to other zones).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#glazeddoorinterzone
        """

class GroundHeatTransferSlabMatlProps:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        rho_slab_material_density: float | None = 2300,
        rho_soil_density: float | None = 1200,
        cp_slab_cp: float | None = 650,
        cp_soil_cp: float | None = 1200,
        tcon_slab_k: float | None = 0.9,
        tcon_soil_k: float | None = 1,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:MatlProps`` and add it to the document.

        This object contains the material properties for the materials used in the model. The fields are mostly self explanatory.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabmatlprops
        """

class HVACTemplateSystemConstantVolume:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        supply_fan_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        cooling_coil_type: Literal[
            "ChilledWater", "ChilledWaterDetailedFlatModel", "HeatExchangerAssistedChilledWater", "None"
        ]
        | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_control_type: Literal[
            "ControlZone", "FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled", "Warmest"
        ]
        | None = "FixedSetpoint",
        cooling_coil_control_zone_name: str | None = ...,
        cooling_coil_design_setpoint_temperature: float | None = 12.8,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_reset_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.8,
        cooling_coil_reset_outdoor_dry_bulb_high: float | None = 23.3,
        heating_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_control_type: Literal[
            "ControlZone", "FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled"
        ]
        | None = "FixedSetpoint",
        heating_coil_control_zone_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 10,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15,
        heating_coil_reset_outdoor_dry_bulb_low: float | None = 7.8,
        heating_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.2,
        heating_coil_reset_outdoor_dry_bulb_high: float | None = 12.2,
        heating_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        preheat_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "None",
        preheat_coil_availability_schedule_name: str | None = ...,
        preheat_coil_design_setpoint: float | None = 7.2,
        preheat_coil_setpoint_schedule_name: str | None = ...,
        gas_preheat_coil_efficiency: float | None = 0.8,
        gas_preheat_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_outdoor_air_schedule_name: str | None = ...,
        economizer_type: Literal[
            "DifferentialDryBulb",
            "DifferentialDryBulbAndEnthalpy",
            "DifferentialEnthalpy",
            "ElectronicEnthalpy",
            "FixedDewPointAndDryBulb",
            "FixedDryBulb",
            "FixedEnthalpy",
            "NoEconomizer",
        ]
        | None = "NoEconomizer",
        economizer_upper_temperature_limit: float | None = ...,
        economizer_lower_temperature_limit: float | None = ...,
        economizer_upper_enthalpy_limit: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        night_cycle_control: Literal["CycleOnAny", "CycleOnAnyZoneFansOnly", "CycleOnControlZone", "StayOff"]
        | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal["CoolReheat", "None"] | None = "None",
        dehumidification_control_zone_name: str | None = ...,
        dehumidification_relative_humidity_setpoint: float | None = 60,
        dehumidification_relative_humidity_setpoint_schedule_name: str | None = ...,
        humidifier_type: Literal["ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_relative_humidity_setpoint: float | None = 30,
        humidifier_relative_humidity_setpoint_schedule_name: str | None = ...,
        return_fan: Literal["No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 300,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
    ) -> None:
        """Create a new ``HVACTemplate:System:ConstantVolume`` and add it to the document.

        Constant Air Volume air loop with optional chilled water cooling coil, optional heating coil and optional preheat.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemconstantvolume
        """

class AnyAirLoopHVACUnitaryFurnaceHeatCool:
    def __call__(
        self,
        name: str,
        /,
        *,
        furnace_air_inlet_node_name: str,
        furnace_air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:SingleSpeed", "CoilSystem:Cooling:DX:HeatExchangerAssisted"],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["Autosize"] | None = 80,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        reheat_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ]
        | None = ...,
        reheat_coil_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:Unitary:Furnace:HeatCool`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam), and optional reheat coil for dehumidification control. Identical to AirLoopHVAC:UnitaryHeatCool.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryfurnaceheatcool
        """

class SetpointManagerSystemNodeResetHumidity:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal["HumidityRatio", "MaximumHumidityRatio", "MinimumHumidityRatio"],
        setpoint_at_low_reference_humidity_ratio: float,
        setpoint_at_high_reference_humidity_ratio: float,
        low_reference_humidity_ratio: float,
        high_reference_humidity_ratio: float,
        reference_node_name: str,
        setpoint_node_or_nodelist_name: str,
    ) -> None:
        """Create a new ``SetpointManager:SystemNodeReset:Humidity`` and add it to the document.

        This Setpoint Manager is used to place a humidity ratio setpoint on a system node according to the reference (e.g., return) humidity ratio using a reset rule. The humidity ratio setpoint is obtained by retrieving the humidity ratio of the user specified reference system node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersystemnoderesethumidity
        """

class OutputEnvironmentalImpactFactors:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        reporting_frequency: Literal["Annual", "Daily", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"]
        | None = ...,
    ) -> None:
        """Create a new ``Output:EnvironmentalImpactFactors`` and add it to the document.

        This is used to Automatically report the facility meters and turn on the Environmental Impact Report calculations for all of the Environmental Factors.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputenvironmentalimpactfactors
        """
