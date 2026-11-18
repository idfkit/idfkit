"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class SiteSpectrumData:
    def __call__(
        self,
        name: str,
        /,
        *,
        spectrum_data_type: Literal["Solar", "Visible"],
        wavelength: float | None = ...,
        spectrum: float | None = ...,
        wavelength_1: float | None = ...,
        spectrum_2: float | None = ...,
        extensions: Sequence[_g.SiteSpectrumDataExtensionsItem | _g.SiteSpectrumDataExtensionsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Site:SpectrumData`` and add it to the document.

        Spectrum Data Type is followed by up to 107 sets of normal-incidence measured values of [wavelength, spectrum] for wavelengths covering the solar (0.25 to 2.5 microns) or visible spectrum (0.38 to 0.78 microns)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitespectrumdata
        """

class ScheduleCompact:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        data: Sequence[_g.ScheduleCompactDataItem | _g.ScheduleCompactDataGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Schedule:Compact`` and add it to the document.

        Irregular object. Does not follow the usual definition for fields. Fields A3... are: Through: Date For: Applicable days (ref: Schedule:Week:Compact) Interpolate: Average/Linear/No (ref: Schedule:Day:Interval) -- optional, if not used will be 'No' Until: <Time> (ref: Schedule:Day:Interval) <numeric value> words 'Through','For','Interpolate','Until' must be included.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#schedulecompact
        """

class AnyZoneVentilationDesignFlowRate:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_flow_rate_calculation_method: Literal["AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
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
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneVentilation:DesignFlowRate`` and add it to the document.

        Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneventilationdesignflowrate
        """

class SetpointManagerFollowGroundTemperature:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["MaximumTemperature", "MinimumTemperature", "Temperature"] | None = "Temperature",
        reference_ground_temperature_object_type: Literal[
            "Site:GroundTemperature:BuildingSurface",
            "Site:GroundTemperature:Deep",
            "Site:GroundTemperature:FCfactorMethod",
            "Site:GroundTemperature:Shallow",
        ]
        | None = ...,
        offset_temperature_difference: float | None = ...,
        maximum_setpoint_temperature: float | None = ...,
        minimum_setpoint_temperature: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:FollowGroundTemperature`` and add it to the document.

        This setpoint manager is used to place a temperature setpoint on a system node that is derived from a current ground temperature. The ground temperatures are specified in different Site:GroundTemperature:* objects and used during the simulation. This setpoint manager is primarily intended for condenser or plant loops using some type of ground heat exchanger.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerfollowgroundtemperature
        """

class AnyGeneratorCombustionTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_power_output: float | None = ...,
        electric_circuit_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        part_load_based_fuel_input_curve_name: str | None = ...,
        temperature_based_fuel_input_curve_name: str | None = ...,
        exhaust_flow_curve_name: str | None = ...,
        part_load_based_exhaust_temperature_curve_name: str | None = ...,
        temperature_based_exhaust_temperature_curve_name: str | None = ...,
        heat_recovery_lube_energy_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        design_air_inlet_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        fuel_type: Literal["Diesel", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"] | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        outdoor_air_inlet_node_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Generator:CombustionTurbine`` and add it to the document.

        This generator model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Generator performance curves are generated by fitting catalog data to second order polynomial equations. Three sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorcombustionturbine
        """

class GeneratorCombustionTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_power_output: float | None = ...,
        electric_circuit_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        part_load_based_fuel_input_curve_name: str | None = ...,
        temperature_based_fuel_input_curve_name: str | None = ...,
        exhaust_flow_curve_name: str | None = ...,
        part_load_based_exhaust_temperature_curve_name: str | None = ...,
        temperature_based_exhaust_temperature_curve_name: str | None = ...,
        heat_recovery_lube_energy_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        design_air_inlet_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        outdoor_air_inlet_node_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Generator:CombustionTurbine`` and add it to the document.

        This generator model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Generator performance curves are generated by fitting catalog data to second order polynomial equations. Three sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorcombustionturbine
        """

class ElectricLoadCenterStorageLiIonNMCBattery:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_cells_in_series: int,
        number_of_strings_in_parallel: int,
        battery_mass: float,
        battery_surface_area: float,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        lifetime_model: Literal["KandlerSmith", "None"] | None = "KandlerSmith",
        initial_fractional_state_of_charge: float | None = 0.5,
        dc_to_dc_charging_efficiency: float | None = 0.95,
        battery_specific_heat_capacity: float | None = 1500,
        heat_transfer_coefficient_between_battery_and_ambient: float | None = 7.5,
        fully_charged_cell_voltage: float | None = 4.2,
        cell_voltage_at_end_of_exponential_zone: float | None = 3.53,
        cell_voltage_at_end_of_nominal_zone: float | None = 3.342,
        default_nominal_cell_voltage: float | None = 3.342,
        fully_charged_cell_capacity: float | None = 3.2,
        fraction_of_cell_capacity_removed_at_the_end_of_exponential_zone: float | None = 0.8075,
        fraction_of_cell_capacity_removed_at_the_end_of_nominal_zone: float | None = 0.976875,
        charge_rate_at_which_voltage_vs_capacity_curve_was_generated: float | None = 1,
        battery_cell_internal_electrical_resistance: float | None = 0.09,
        validate: bool = True,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:LiIonNMCBattery`` and add it to the document.

        Uses Lithium Ion NMC model to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstorageliionnmcbattery
        """

class AnyFuelFactors:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        existing_fuel_resource_name: Literal[
            "Coal",
            "Diesel",
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
        source_energy_factor: float | None = ...,
        source_energy_schedule_name: str | None = ...,
        co2_emission_factor: float | None = ...,
        co2_emission_factor_schedule_name: str | None = ...,
        co_emission_factor: float | None = ...,
        co_emission_factor_schedule_name: str | None = ...,
        ch4_emission_factor: float | None = ...,
        ch4_emission_factor_schedule_name: str | None = ...,
        nox_emission_factor: float | None = ...,
        nox_emission_factor_schedule_name: str | None = ...,
        n2o_emission_factor: float | None = ...,
        n2o_emission_factor_schedule_name: str | None = ...,
        so2_emission_factor: float | None = ...,
        so2_emission_factor_schedule_name: str | None = ...,
        pm_emission_factor: float | None = ...,
        pm_emission_factor_schedule_name: str | None = ...,
        pm10_emission_factor: float | None = ...,
        pm10_emission_factor_schedule_name: str | None = ...,
        pm2_5_emission_factor: float | None = ...,
        pm2_5_emission_factor_schedule_name: str | None = ...,
        nh3_emission_factor: float | None = ...,
        nh3_emission_factor_schedule_name: str | None = ...,
        nmvoc_emission_factor: float | None = ...,
        nmvoc_emission_factor_schedule_name: str | None = ...,
        hg_emission_factor: float | None = ...,
        hg_emission_factor_schedule_name: str | None = ...,
        pb_emission_factor: float | None = ...,
        pb_emission_factor_schedule_name: str | None = ...,
        water_emission_factor: float | None = ...,
        water_emission_factor_schedule_name: str | None = ...,
        nuclear_high_level_emission_factor: float | None = ...,
        nuclear_high_level_emission_factor_schedule_name: str | None = ...,
        nuclear_low_level_emission_factor: float | None = ...,
        nuclear_low_level_emission_factor_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``FuelFactors`` and add it to the document.

        Provides Fuel Factors for Emissions as well as Source=>Site conversions. OtherFuel1, OtherFuel2 provide options for users who want to create and use fuels that may not be mainstream (biomass, wood, pellets).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#fuelfactors
        """
