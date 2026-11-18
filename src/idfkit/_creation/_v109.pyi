"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class WaterHeaterSizing_v8_9_to_v22_1:
    def __call__(
        self,
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
        number_of_bedrooms: float | None = ...,
        number_of_bathrooms: float | None = ...,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-water-heaters/#waterheatersizing
        """

class ZoneHVACLowTemperatureRadiantVariableFlow_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_inside_diameter: float | None = 0.013,
        hydronic_tubing_length: float | Literal["", "Autosize"] | None = "Autosize",
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
        ]
        | None = "MeanAirTemperature",
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        maximum_hot_water_flow: float | Literal["Autosize"] | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_control_throttling_range: float | None = 0.5,
        heating_control_temperature_schedule_name: str | None = ...,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        maximum_cold_water_flow: float | Literal["Autosize"] | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:VariableFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water flow to the unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantvariableflow
        """
