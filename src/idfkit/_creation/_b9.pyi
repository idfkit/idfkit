"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnySiteGroundDomainBasement:
    def __call__(
        self,
        name: str,
        /,
        *,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        basement_floor_boundary_condition_model_name: str,
        basement_wall_boundary_condition_model_name: str,
        ground_domain_depth: float | None = 10,
        aspect_ratio: float | None = 1,
        perimeter_offset: float | None = 5,
        soil_thermal_conductivity: float | None = 1.5,
        soil_density: float | None = 2800,
        soil_specific_heat: float | None = 850,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        horizontal_insulation: Literal["No", "Yes"] | None = "No",
        horizontal_insulation_material_name: str | None = ...,
        horizontal_insulation_extents: Literal["Full", "Perimeter"] | None = "Full",
        perimeter_horizontal_insulation_width: float | None = ...,
        basement_wall_depth: float | None = ...,
        vertical_insulation: Literal["No", "Yes"] | None = "No",
        basement_wall_vertical_insulation_material_name: str | None = ...,
        vertical_insulation_depth: float | None = ...,
        simulation_timestep: Literal["Hourly", "Timestep"] | None = "Hourly",
        mesh_density_parameter: int | None = 4,
    ) -> None:
        """Create a new ``Site:GroundDomain:Basement`` and add it to the document.

        Ground-coupled basement model for simulating basements or other underground zones.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegrounddomainbasement
        """

class GroundHeatTransferSlabEquivalentSlab:
    def __call__(
        self,
        /,
        *,
        apratio_the_area_to_perimeter_ratio_for_this_slab: float,
        slabdepth_thickness_of_slab_on_grade: float | None = 0.1,
        clearance_distance_from_edge_of_slab_to_domain_edge: float | None = 15,
        zclearance_distance_from_bottom_of_slab_to_domain_bottom: float | None = 15,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:EquivalentSlab`` and add it to the document.

        Using an equivalent slab allows non-rectangular shapes to be modeled accurately. Object uses the area - perimeter (area/perimeter) ratio to determine the size of an equivalent rectangular slab. EnergyPlus users normally use this option.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabequivalentslab
        """

class ZoneHVACUnitHeater:
    def __call__(
        self,
        name: str,
        /,
        *,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"],
        supply_air_fan_name: str,
        maximum_supply_air_flow_rate: float | Literal["Autosize"],
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        supply_air_fan_operation_during_no_heating: Literal["No", "Yes"],
        availability_schedule_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:UnitHeater`` and add it to the document.

        Unit heater. Forced-convection heating-only unit with supply fan, heating coil (gas, electric, hot water, or steam) and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacunitheater
        """

class ControllerMechanicalVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        demand_controlled_ventilation: Literal["No", "Yes"] | None = "No",
        system_outdoor_air_method: Literal[
            "IndoorAirQualityProcedure",
            "IndoorAirQualityProcedureCombined",
            "IndoorAirQualityProcedureGenericContaminant",
            "ProportionalControlBasedOnDesignOARate",
            "ProportionalControlBasedOnDesignOccupancy",
            "ProportionalControlBasedOnOccupancySchedule",
            "Standard62.1VentilationRateProcedure",
            "Standard62.1VentilationRateProcedureWithLimit",
            "ZoneSum",
        ]
        | None = "Standard62.1VentilationRateProcedure",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        zone_specifications: Sequence[
            _g.ControllerMechanicalVentilationZoneSpecificationsItem
            | _g.ControllerMechanicalVentilationZoneSpecificationsGroup
        ] = ...,
    ) -> None:
        """Create a new ``Controller:MechanicalVentilation`` and add it to the document.

        This object is used in conjunction with Controller:OutdoorAir to specify outdoor ventilation air based on outdoor air specified in the DesignSpecification:OutdoorAir object The Controller:OutdoorAir object is associated with a specific air loop, so the outdoor air flow rates specified in Controller:MechanicalVentilation correspond to the zones attached to that specific air loop. Duplicate groups of Zone name, Design Specification Outdoor Air Object Name, and Design Specification Zone Air Distribution Object Name to increase allowable number of entries

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-controllers/#controllermechanicalventilation
        """

class SetpointManagerWarmest:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["Temperature"] | None = "Temperature",
        minimum_setpoint_temperature: float | None = 12,
        maximum_setpoint_temperature: float | None = 18,
        strategy: Literal["MaximumTemperature"] | None = "MaximumTemperature",
    ) -> None:
        """Create a new ``SetpointManager:Warmest`` and add it to the document.

        This SetpointManager resets the cooling supply air temperature of a central forced air HVAC system according to the cooling demand of the warmest zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerwarmest
        """

class ElectricLoadCenterStorageSimple:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction_for_zone_heat_gains: float | None = ...,
        nominal_energetic_efficiency_for_charging: float | None = ...,
        nominal_discharging_energetic_efficiency: float | None = ...,
        maximum_storage_capacity: float | None = ...,
        maximum_power_for_discharging: float | None = ...,
        maximum_power_for_charging: float | None = ...,
        initial_state_of_charge: float | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:Simple`` and add it to the document.

        Used to model storage of electricity in an electric load center. This is a simple model that does not attempt to represent any of the characteristics of a real storage device such as a battery. The type of power, AC or DC, depends on the configuration chosen as the Electrical Buss Type in the ElectricLoadCenter:Distribution object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstoragesimple
        """

class ElectricLoadCenterStorageConverter:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        power_conversion_efficiency_method: Literal["FunctionOfPower", "SimpleFixed"] | None = "SimpleFixed",
        simple_fixed_efficiency: float | None = 0.95,
        design_maximum_continuous_input_power: float | None = ...,
        efficiency_function_of_power_curve_name: str | None = ...,
        ancillary_power_consumed_in_standby: float | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:Converter`` and add it to the document.

        This model is for converting AC to DC for grid-supplied charging of DC storage

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstorageconverter
        """

class OutputSQLite:
    def __call__(
        self,
        /,
        *,
        option_type: Literal["Simple", "SimpleAndTabular"] | None = ...,
        unit_conversion_for_tabular_data: Literal[
            "InchPound", "InchPoundExceptElectricity", "JtoGJ", "JtoKWH", "JtoMJ", "None", "UseOutputControlTableStyle"
        ]
        | None = "UseOutputControlTableStyle",
        format_numeric_values_for_tabular_data: Literal["No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputsqlite
        """
