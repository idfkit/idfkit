"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class SurfacePropertyLocalEnvironment_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        exterior_surface_name: str | None = ...,
        external_shading_fraction_schedule_name: str | None = ...,
        surrounding_surfaces_object_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
        ground_surfaces_object_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:LocalEnvironment`` and add it to the document.

        This object defines the local environment properties of an exterior surface. One or more environment properties have to be defined and linked to the exterior surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-advanced-surface-concepts/#surfacepropertylocalenvironment
        """

class ControllerMechanicalVentilation_v8_9_to_v9_2:
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
            "ProportionalControlBasedonOccupancySchedule",
            "VentilationRateProcedure",
            "ZoneSum",
        ]
        | None = "VentilationRateProcedure",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        zone_specifications: Sequence[
            _vd.ControllerMechanicalVentilationZoneSpecificationsItem_v8_9_to_v9_2
            | _vd.ControllerMechanicalVentilationZoneSpecificationsGroup_v8_9_to_v9_2
        ] = ...,
    ) -> None:
        """Create a new ``Controller:MechanicalVentilation`` and add it to the document.

        This object is used in conjunction with Controller:OutdoorAir to specify outdoor ventilation air based on outdoor air specified in the DesignSpecification:OutdoorAir object The Controller:OutdoorAir object is associated with a specific air loop, so the outdoor air flow rates specified in Controller:MechanicalVentilation correspond to the zones attached to that specific air loop. Duplicate groups of Zone name, Design Specification Outdoor Air Object Name, and Design Specification Zone Air Distribution Object Name to increase allowable number of entries

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-controllers/#controllermechanicalventilation
        """

class ControllerMechanicalVentilation_v9_5:
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
            "VentilationRateProcedure",
            "ZoneSum",
        ]
        | None = "VentilationRateProcedure",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        zone_specifications: Sequence[
            _vd.ControllerMechanicalVentilationZoneSpecificationsItem_v9_5
            | _vd.ControllerMechanicalVentilationZoneSpecificationsGroup_v9_5
        ] = ...,
    ) -> None:
        """Create a new ``Controller:MechanicalVentilation`` and add it to the document.

        This object is used in conjunction with Controller:OutdoorAir to specify outdoor ventilation air based on outdoor air specified in the DesignSpecification:OutdoorAir object The Controller:OutdoorAir object is associated with a specific air loop, so the outdoor air flow rates specified in Controller:MechanicalVentilation correspond to the zones attached to that specific air loop. Duplicate groups of Zone name, Design Specification Outdoor Air Object Name, and Design Specification Zone Air Distribution Object Name to increase allowable number of entries

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-controllers/#controllermechanicalventilation
        """

class Space_v9_6_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        floor_area: float | Literal["Autocalculate"] | None = "Autocalculate",
        space_type: str | None = "General",
        tags: Sequence[_g.SpaceTagsItem | _g.SpaceTagsGroup] = ...,
    ) -> None:
        """Create a new ``Space`` and add it to the document.

        Defines a space (room) in the building. All Spaces are part of a Zone. Every Zone contains one or more spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will be created. If some surfaces in a Zone are assigned to a space and some are not, then a default Space named <Zone Name>-Remainder will be created. Input references to Space Names must have a matching Space object (default space names may not be referenced except in output variable keys).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-thermal-zone-description-geometry/#space
        """

class AirflowNetworkMultiZoneReferenceCrackConditions_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_temperature: float | None = 20,
        reference_barometric_pressure: float | None = 101325,
        reference_humidity_ratio: float | None = 0,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:ReferenceCrackConditions`` and add it to the document.

        This object specifies the conditions under which the air mass flow coefficient was measured.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-airflow-network/#airflownetworkmultizonereferencecrackconditions
        """

class SwimmingPoolIndoor_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        average_depth: float,
        activity_factor_schedule_name: str,
        make_up_water_supply_schedule_name: str,
        cover_schedule_name: str,
        pool_water_inlet_node: str,
        pool_water_outlet_node: str,
        setpoint_temperature_schedule: str,
        maximum_number_of_people: float,
        cover_evaporation_factor: float | None = 0,
        cover_convection_factor: float | None = 0,
        cover_short_wavelength_radiation_factor: float | None = 0,
        cover_long_wavelength_radiation_factor: float | None = 0,
        pool_heating_system_maximum_water_flow_rate: float | None = ...,
        pool_miscellaneous_equipment_power: float | None = ...,
        people_schedule: str | None = ...,
        people_heat_gain_schedule: str | None = ...,
    ) -> None:
        """Create a new ``SwimmingPool:Indoor`` and add it to the document.

        Specifies an indoor swimming pools linked to a floor surface. The pool is assumed to cover the entire floor to which it is linked.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-internal-gains-people-lights-other/#swimmingpoolindoor
        """
