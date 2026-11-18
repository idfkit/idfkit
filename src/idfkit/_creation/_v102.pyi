"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class WindowMaterialGlazingEquivalentLayer_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        front_side_beam_beam_solar_transmittance: float,
        back_side_beam_beam_solar_transmittance: float,
        front_side_beam_beam_solar_reflectance: float,
        back_side_beam_beam_solar_reflectance: float,
        optical_data_type: Literal["Spectral", "SpectralAverage"] | None = "SpectralAverage",
        window_glass_spectral_data_set_name: str | None = ...,
        front_side_beam_beam_visible_solar_transmittance: float | None = ...,
        back_side_beam_beam_visible_solar_transmittance: float | None = ...,
        front_side_beam_beam_visible_solar_reflectance: float | None = ...,
        back_side_beam_beam_visible_solar_reflectance: float | None = ...,
        front_side_beam_diffuse_solar_transmittance: float | None = 0,
        back_side_beam_diffuse_solar_transmittance: float | None = 0,
        front_side_beam_diffuse_solar_reflectance: float | None = 0,
        back_side_beam_diffuse_solar_reflectance: float | None = 0,
        front_side_beam_diffuse_visible_solar_transmittance: float | None = 0,
        back_side_beam_diffuse_visible_solar_transmittance: float | None = 0,
        front_side_beam_diffuse_visible_solar_reflectance: float | None = 0,
        back_side_beam_diffuse_visible_solar_reflectance: float | None = 0,
        diffuse_diffuse_solar_transmittance: float | Literal["Autocalculate"] | None = "Autocalculate",
        front_side_diffuse_diffuse_solar_reflectance: float | Literal["Autocalculate"] | None = "Autocalculate",
        back_side_diffuse_diffuse_solar_reflectance: float | Literal["Autocalculate"] | None = "Autocalculate",
        diffuse_diffuse_visible_solar_transmittance: float | Literal["Autocalculate"] | None = "Autocalculate",
        front_side_diffuse_diffuse_visible_solar_reflectance: float | Literal["Autocalculate"] | None = "Autocalculate",
        back_side_diffuse_diffuse_visible_solar_reflectance: float | Literal["Autocalculate"] | None = "Autocalculate",
        infrared_transmittance_applies_to_front_and_back_: float | None = 0,
        front_side_infrared_emissivity: float | None = 0.84,
        back_side_infrared_emissivity: float | None = 0.84,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowMaterial:Glazing:EquivalentLayer`` and add it to the document.

        Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-surface-construction-elements/#windowmaterialglazingequivalentlayer
        """

class AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        bypass_duct_mixer_node_name: str,
        bypass_duct_splitter_node_name: str,
        air_outlet_node_name: str,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"],
        outdoor_air_mixer_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"],
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:DX:VariableSpeed",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        outdoor_air_flow_rate_multiplier_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        priority_control_mode: Literal["CoolingPriority", "HeatingPriority", "ZonePriority"] | None = "ZonePriority",
        minimum_outlet_air_temperature_during_cooling_operation: float | None = 8,
        maximum_outlet_air_temperature_during_heating_operation: float | None = 50,
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        validate: bool = True,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, steam, or DX air-to-air heat pump) and bypass damper for variable volume flow to terminal units. Used with AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat or AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatcoolvavchangeoverbypass
        """

class AirflowNetworkDistributionComponentReliefAirFlow_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:ReliefAirFlow`` and add it to the document.

        This object allows variation of air flow rate to perform pressure.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentreliefairflow
        """

class InternalMass_v8_9_to_v9_1:
    def __call__(
        self, name: str, /, *, construction_name: str, zone_name: str, surface_area: float, validate: bool = True
    ) -> None:
        """Create a new ``InternalMass`` and add it to the document.

        Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-thermal-zone-description-geometry/#internalmass
        """
