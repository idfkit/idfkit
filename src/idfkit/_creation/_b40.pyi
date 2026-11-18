"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyPeople:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        number_of_people_calculation_method: Literal["Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["AngleFactor", "SurfaceWeighted"] | None = ...,
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        thermal_comfort_model_1_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_2_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_3_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_4_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_5_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
    ) -> None:
        """Create a new ``People`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#people
        """

class SpaceHVACZoneEquipmentMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_equipment_inlet_node_name: str,
        space_fraction_method: Literal[
            "DesignCoolingLoad", "DesignHeatingLoad", "FloorArea", "PerimeterLength", "Volume"
        ]
        | None = "DesignCoolingLoad",
        spaces: Sequence[_g.SpaceHVACZoneEquipmentMixerSpacesItem | _g.SpaceHVACZoneEquipmentMixerSpacesGroup] = ...,
    ) -> None:
        """Create a new ``SpaceHVAC:ZoneEquipmentMixer`` and add it to the document.

        Mixes the airflow from one or more Spaces into a piece of zone equipment. All spaces in the zone must also have a SpaceHVAC:EquipmentConnections object. Used only when ZoneAirHeatBalanceAlgorithm 'Do Space Heat Balance for Simulation' is Yes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#spacehvaczoneequipmentmixer
        """

class AirLoopHVACSupplyPath:
    def __call__(
        self,
        name: str,
        /,
        *,
        supply_air_path_inlet_node_name: str,
        components: Sequence[_g.AirLoopHVACSupplyPathComponentsItem | _g.AirLoopHVACSupplyPathComponentsGroup] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:SupplyPath`` and add it to the document.

        A supply path can only contain AirLoopHVAC:ZoneSplitter and AirLoopHVAC:SupplyPlenum objects which may be in series or parallel.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacsupplypath
        """
