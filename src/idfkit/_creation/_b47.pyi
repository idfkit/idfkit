"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyMaterialPropertyVariableAbsorptance:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_material_name: str,
        control_signal: Literal[
            "Scheduled", "SpaceHeatingCoolingMode", "SurfaceReceivedSolarRadiation", "SurfaceTemperature"
        ]
        | None = "SurfaceTemperature",
        thermal_absorptance_function_name: str | None = ...,
        thermal_absorptance_schedule_name: str | None = ...,
        solar_absorptance_function_name: str | None = ...,
        solar_absorptance_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:VariableAbsorptance`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyvariableabsorptance
        """

class SpaceList:
    def __call__(
        self, name: str, /, *, spaces: Sequence[_g.SpaceListSpacesItem | _g.SpaceListSpacesGroup] = ...
    ) -> None:
        """Create a new ``SpaceList`` and add it to the document.

        Defines a list of Spaces which can be referenced as a group. The SpaceList name may be used elsewhere in the input to apply a parameter to all Spaces in the list. SpaceLists can be used effectively with the following objects: InternalMass, People, Lights, ElectricEquipment, GasEquipment, HotWaterEquipment, and others.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#spacelist
        """

class ZoneVentilationDesignFlowRate:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str | None = ...,
        design_flow_rate_calculation_method: Literal["AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        ventilation_type: Literal["Balanced", "Exhaust", "Intake", "Natural"] | None = "Natural",
        fan_pressure_rise: float | None = 0,
        fan_total_efficiency: float | None = 1,
        constant_term_coefficient: float | None = 1,
        temperature_term_coefficient: float | None = 0,
        velocity_term_coefficient: float | None = 0,
        velocity_squared_term_coefficient: float | None = 0,
        minimum_indoor_temperature: float | None = -100,
        minimum_indoor_temperature_schedule_name: str | None = ...,
        maximum_indoor_temperature: float | None = 100,
        maximum_indoor_temperature_schedule_name: str | None = ...,
        delta_temperature: float | None = -100,
        delta_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature: float | None = -100,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature: float | None = 100,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_wind_speed: float | None = 40,
        density_basis: Literal["Indoor", "Outdoor", "Standard"] | None = "Outdoor",
    ) -> None:
        """Create a new ``ZoneVentilation:DesignFlowRate`` and add it to the document.

        Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneventilationdesignflowrate
        """

class ZoneControlHumidistat:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        humidifying_setpoint_schedule_name: str,
        dehumidifying_setpoint_schedule_name: str | None = ...,
        control_variable: Literal["Dewpoint", "RelativeHumidity"] | None = "RelativeHumidity",
    ) -> None:
        """Create a new ``ZoneControl:Humidistat`` and add it to the document.

        Specifies zone relative humidity setpoint schedules for humidifying and dehumidifying.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolhumidistat
        """

class CoilHeatingWaterToAirHeatPumpParameterEstimation:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_type: Literal["Reciprocating", "Rotary", "Scroll"],
        design_source_side_flow_rate: float,
        gross_rated_heating_capacity: float,
        high_pressure_cutoff: float,
        low_pressure_cutoff: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        load_side_total_heat_transfer_coefficient: float,
        superheat_temperature_at_the_evaporator_outlet: float,
        compressor_power_losses: float,
        compressor_efficiency: float,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R22",
        compressor_piston_displacement: float | None = ...,
        compressor_suction_discharge_pressure_drop: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        refrigerant_volume_flow_rate: float | None = ...,
        volume_ratio: float | None = ...,
        leak_rate_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_resistance1: float | None = ...,
        source_side_heat_transfer_resistance2: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:ParameterEstimation`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Parameter estimation model is a deterministic model that requires a consistent set of parameters to describe the operating conditions of the heat pump components.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpparameterestimation
        """

class AnyAirLoopHVACUnitarySystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        control_type: Literal["Load", "SetPoint", "SingleZoneVAV"] | None = "Load",
        controlling_zone_or_thermostat_location: str | None = ...,
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        availability_schedule_name: str | None = ...,
        supply_fan_object_type: Literal[
            "Fan:ComponentModel", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ]
        | None = ...,
        supply_fan_name: str | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:DX:VariableSpeed",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Electric:MultiStage",
            "Coil:Heating:Fuel",
            "Coil:Heating:Gas:MultiStage",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "Coil:Heating:WaterToAirHeatPump:EquationFit",
            "Coil:Heating:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Coil:UserDefined",
        ]
        | None = ...,
        heating_coil_name: str | None = ...,
        dx_heating_coil_sizing_ratio: float | None = 1,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Coil:UserDefined",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ]
        | None = ...,
        cooling_coil_name: str | None = ...,
        use_doas_dx_cooling_coil: Literal["No", "Yes"] | None = "No",
        minimum_supply_air_temperature: float | Literal["Autosize"] | None = 2,
        latent_load_control: Literal[
            "LatentOnlyLoadControl",
            "LatentOrSensibleLoadControl",
            "LatentWithSensibleLoadControl",
            "SensibleOnlyLoadControl",
        ]
        | None = "SensibleOnlyLoadControl",
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "Coil:UserDefined",
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        cooling_supply_air_flow_rate_method: Literal[
            "FlowPerCoolingCapacity", "FlowPerFloorArea", "FractionOfAutosizedCoolingValue", "None", "SupplyAirFlowRate"
        ]
        | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_of_capacity: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "FlowPerFloorArea", "FlowPerHeatingCapacity", "FractionOfAutosizedHeatingValue", "None", "SupplyAirFlowRate"
        ]
        | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_of_capacity: float | None = ...,
        no_load_supply_air_flow_rate_method: Literal[
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedCoolingValue",
            "FractionOfAutosizedHeatingValue",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_per_floor_area: float | None = ...,
        no_load_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        no_load_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        no_load_supply_air_flow_rate_per_unit_of_capacity_during_cooling_operation: float | None = ...,
        no_load_supply_air_flow_rate_per_unit_of_capacity_during_heating_operation: float | None = ...,
        maximum_supply_air_temperature: float | Literal["Autosize"] | None = 80,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        ancillary_on_cycle_electric_power: float | None = 0,
        ancillary_off_cycle_electric_power: float | None = 0,
        design_heat_recovery_water_flow_rate: float | None = 0,
        maximum_temperature_for_heat_recovery: float | None = 80,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        design_specification_multispeed_object_type: Literal["UnitarySystemPerformance:Multispeed"] | None = ...,
        design_specification_multispeed_object_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitarySystem`` and add it to the document.

        AirloopHVAC:UnitarySystem is a generic HVAC system type that allows any configuration of coils and/or fan. This object is a replacement of other AirloopHVAC objects. This object can be used in outdoor air systems, outdoor air units, air loops, and as zone equipment if desired.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitarysystem
        """

class AirLoopHVACMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        outlet_node_name: str,
        nodes: Sequence[_g.AirLoopHVACMixerNodesItem | _g.AirLoopHVACMixerNodesGroup] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:Mixer`` and add it to the document.

        Mix N inlet air streams from Relief Air Stream Node in OutdoorAir:Mixer objects served by AirLoopHVAC objects listed in AirLoopHVAC:DedicatedOutdoorAirSystem into one (currently 10 as default, but extensible). Node names cannot be duplicated within a single mixer list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacmixer
        """

class GeneratorFuelCellAirSupply:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_supply_rate_calculation_mode: Literal[
            "AirRatiobyStoics", "QuadraticFunctionofElectricPower", "QuadraticFunctionofFuelRate"
        ],
        air_intake_heat_recovery_mode: Literal[
            "NoRecovery",
            "RecoverAuxiliaryBurner",
            "RecoverBurnerInverterStorage",
            "RecoverElectricalStorage",
            "RecoverInverter",
            "RecoverInverterandStorage",
        ],
        air_supply_constituent_mode: Literal["AmbientAir", "UserDefinedConstituents"],
        air_inlet_node_name: str | None = ...,
        blower_power_curve_name: str | None = ...,
        blower_heat_loss_factor: float | None = ...,
        stoichiometric_ratio: float | None = ...,
        air_rate_function_of_electric_power_curve_name: str | None = ...,
        air_rate_air_temperature_coefficient: float | None = ...,
        air_rate_function_of_fuel_rate_curve_name: str | None = ...,
        number_of_userdefined_constituents: float | None = ...,
        constituent_fractions: Sequence[
            _g.GeneratorFuelCellAirSupplyConstituentFractionsItem
            | _g.GeneratorFuelCellAirSupplyConstituentFractionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:AirSupply`` and add it to the document.

        Used to define details of the air supply subsystem for a fuel cell power generator.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellairsupply
        """

class CurveCubic:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        coefficient4_x_3: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Cubic`` and add it to the document.

        Cubic curve with one independent variable. Input for a cubic curve consists of the curve name, the 4 coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x + C3*x**2 + C4*x**3

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvecubic
        """

class CurveDoubleExponentialDecay:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient4_c4: float,
        coefficient5_c5: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:DoubleExponentialDecay`` and add it to the document.

        Double exponential decay curve with one independent variable. Input consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1+C2*exp(C3*x)+C4*exp(C5*x)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvedoubleexponentialdecay
        """
