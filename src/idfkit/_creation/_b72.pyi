"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyWindowMaterialGlazingEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        front_side_beam_beam_solar_transmittance: float,
        back_side_beam_beam_solar_transmittance: float,
        front_side_beam_beam_solar_reflectance: float,
        back_side_beam_beam_solar_reflectance: float,
        optical_data_type: Literal["", "Spectral", "SpectralAverage"] | None = "SpectralAverage",
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
        diffuse_diffuse_solar_transmittance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        front_side_diffuse_diffuse_solar_reflectance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        back_side_diffuse_diffuse_solar_reflectance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        diffuse_diffuse_visible_solar_transmittance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        front_side_diffuse_diffuse_visible_solar_reflectance: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
        back_side_diffuse_diffuse_visible_solar_reflectance: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
        infrared_transmittance_applies_to_front_and_back_: float | None = 0,
        front_side_infrared_emissivity: float | None = 0.84,
        back_side_infrared_emissivity: float | None = 0.84,
    ) -> None:
        """Create a new ``WindowMaterial:Glazing:EquivalentLayer`` and add it to the document.

        Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialglazingequivalentlayer
        """

class AnyFenestrationSurfaceDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal["Door", "GlassDoor", "TubularDaylightDiffuser", "TubularDaylightDome", "Window"],
        construction_name: str,
        building_surface_name: str,
        vertex_1_x_coordinate: float,
        vertex_1_y_coordinate: float,
        vertex_1_z_coordinate: float,
        vertex_2_x_coordinate: float,
        vertex_2_y_coordinate: float,
        vertex_2_z_coordinate: float,
        vertex_3_x_coordinate: float,
        vertex_3_y_coordinate: float,
        vertex_3_z_coordinate: float,
        outside_boundary_condition_object: str | None = ...,
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertex_4_x_coordinate: float | None = ...,
        vertex_4_y_coordinate: float | None = ...,
        vertex_4_z_coordinate: float | None = ...,
    ) -> None:
        """Create a new ``FenestrationSurface:Detailed`` and add it to the document.

        Allows for detailed entry of subsurfaces (windows, doors, glass doors, tubular daylighting devices).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#fenestrationsurfacedetailed
        """

class ComplexFenestrationPropertySolarAbsorbedLayers:
    def __call__(
        self,
        name: str,
        /,
        *,
        fenestration_surface: str,
        construction_name: str,
        layer_1_solar_radiation_absorbed_schedule_name: str,
        layer_2_solar_radiation_absorbed_schedule_name: str | None = ...,
        layer_3_solar_radiation_absorbed_schedule_name: str | None = ...,
        layer_4_solar_radiation_absorbed_schedule_name: str | None = ...,
        layer_5_solar_radiation_absorbed_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ComplexFenestrationProperty:SolarAbsorbedLayers`` and add it to the document.

        Used to provide solar radiation absorbed in fenestration layers. References surface-construction pair and if that pair is used in a simulation, then program will use value provided in schedules instead of calculating it.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#complexfenestrationpropertysolarabsorbedlayers
        """

class HVACTemplateZoneDualDuct:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_dual_duct_system_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        zone_minimum_air_flow_fraction: float | None = 0.2,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        design_specification_outdoor_air_object_name_for_sizing: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        design_specification_outdoor_air_object_name_for_control: str | None = ...,
        cold_supply_plenum_name: str | None = ...,
        hot_supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 12.8,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:DualDuct`` and add it to the document.

        Zone terminal unit, dual-duct, constant or variable volume.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonedualduct
        """

class HVACTemplatePlantChiller:
    def __call__(
        self,
        name: str,
        /,
        *,
        chiller_type: Literal[
            "DistrictChilledWater", "ElectricCentrifugalChiller", "ElectricReciprocatingChiller", "ElectricScrewChiller"
        ],
        nominal_cop: float,
        capacity: float | Literal["", "Autosize"] | None = "Autosize",
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "WaterCooled",
        priority: str | None = ...,
        sizing_factor: float | None = 1,
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        minimum_unloading_ratio: float | None = 0.25,
        leaving_chilled_water_lower_temperature_limit: float | None = 5,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Chiller`` and add it to the document.

        This object adds a chiller to an HVACTemplate:Plant:ChilledWaterLoop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantchiller
        """

class AnyZoneHVACLowTemperatureRadiantConstantFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_length: float | Literal["", "Autosize"] | None = "Autosize",
        rated_flow_rate: float | Literal["Autosize"] | None = ...,
        pump_flow_rate_schedule_name: str | None = ...,
        rated_pump_head: float | None = 179352,
        rated_power_consumption: float | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_high_water_temperature_schedule_name: str | None = ...,
        heating_low_water_temperature_schedule_name: str | None = ...,
        heating_high_control_temperature_schedule_name: str | None = ...,
        heating_low_control_temperature_schedule_name: str | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_high_water_temperature_schedule_name: str | None = ...,
        cooling_low_water_temperature_schedule_name: str | None = ...,
        cooling_high_control_temperature_schedule_name: str | None = ...,
        cooling_low_control_temperature_schedule_name: str | None = ...,
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water temperature circulating through the unit.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantconstantflow
        """

class CoilDXASHRAE205Performance:
    def __call__(
        self,
        name: str,
        /,
        *,
        representation_file_name: str,
        performance_interpolation_method: Literal["", "Cubic", "Linear"] | None = "Linear",
        rated_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_steady_state_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``Coil:DX:ASHRAE205:Performance`` and add it to the document.

        DX coil performance specification referencing an ASHRAE Standard 205 compliant representation for air-to-air direct expansion refrigerant system (Representation Specification RS0004). As RS0004 files are intended to support both heating and cooling performance, this object may referenced by the Coil:Cooling:DX and the corresponding Coil:Heating:DX object (planned for future addition).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coils/#coildxashrae205performance
        """

class HumidifierSteamGas:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        rated_capacity: float | Literal["Autosize"] | None = ...,
        rated_gas_use_rate: float | Literal["Autosize"] | None = ...,
        thermal_efficiency: float | None = 0.8,
        thermal_efficiency_modifier_curve_name: str | None = ...,
        rated_fan_power: float | None = ...,
        auxiliary_electric_power: float | None = 0,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        water_storage_tank_name: str | None = ...,
        inlet_water_temperature_option: Literal["", "FixedInletWaterTemperature", "VariableInletWaterTemperature"]
        | None = "FixedInletWaterTemperature",
    ) -> None:
        """Create a new ``Humidifier:Steam:Gas`` and add it to the document.

        Natural gas fired steam humidifier with optional blower fan.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-humidifiers-and-dehumidifiers/#humidifiersteamgas
        """

class AnyZoneHVACForcedAirUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        number_of_plant_loop_connections: int,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        model_setup_and_sizing_program_calling_manager_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        secondary_air_outlet_node_name: str | None = ...,
        plant_connection_1_inlet_node_name: str | None = ...,
        plant_connection_1_outlet_node_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        plant_connection_3_inlet_node_name: str | None = ...,
        plant_connection_3_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:ForcedAir:UserDefined`` and add it to the document.

        Defines a generic zone air unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#zonehvacforcedairuserdefined
        """

class CurveBicubic:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        coefficient4_y: float,
        coefficient5_y_2: float,
        coefficient6_x_y: float,
        coefficient7_x_3: float,
        coefficient8_y_3: float,
        coefficient9_x_2_y: float,
        coefficient10_x_y_2: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Bicubic`` and add it to the document.

        Cubic curve with two independent variables. Input consists of the curve name, the ten coefficients, and the minimum and maximum values for each of the independent variables. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x + C3*x**2 + C4*y + C5*y**2 + C6*x*y + C7*x**3 + C8*y**3 + C9*x**2*y + C10*x*y**2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvebicubic
        """

class AnyUtilityCostVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        tariff_name: str,
        variable_type: Literal["", "Currency", "Dimensionless", "Energy"] | None = "Dimensionless",
        january_value: float | None = ...,
        february_value: float | None = ...,
        march_value: float | None = ...,
        april_value: float | None = ...,
        may_value: float | None = ...,
        june_value: float | None = ...,
        july_value: float | None = ...,
        august_value: float | None = ...,
        september_value: float | None = ...,
        october_value: float | None = ...,
        november_value: float | None = ...,
        december_value: float | None = ...,
    ) -> None:
        """Create a new ``UtilityCost:Variable`` and add it to the document.

        Allows for the direct entry of monthly values into a utility tariff variable.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-variable/#utilitycostvariable
        """

class AnyLifeCycleCostUsePriceEscalation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        lcc_price_escalation_name: str,
        resource: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ],
        escalation_start_year: int | None = ...,
        escalation_start_month: Literal[
            "",
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        escalations: Sequence[
            _g.LifeCycleCostUsePriceEscalationEscalationsItem | _g.LifeCycleCostUsePriceEscalationEscalationsGroup
        ] = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:UsePriceEscalation`` and add it to the document.

        Life cycle cost escalation factors. The values for this object may be found in the annual supplement to NIST Handbook 135 in Tables Ca-1 to Ca-5 and are included in an EnergyPlus dataset file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-usepriceescalation/#lifecyclecostusepriceescalation
        """
