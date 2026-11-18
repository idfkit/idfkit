"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyFloorInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Floor:Interzone`` and add it to the document.

        Allows for simplified entry of floors using adjacent zone (interzone) heat transfer - adjacent surface should be a ceiling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#floorinterzone
        """

class ShadingFin:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        left_extension_from_window_door: float | None = ...,
        left_distance_above_top_of_window: float | None = ...,
        left_distance_below_bottom_of_window: float | None = ...,
        left_tilt_angle_from_window_door: float | None = 90,
        left_depth: float | None = ...,
        right_extension_from_window_door: float | None = ...,
        right_distance_above_top_of_window: float | None = ...,
        right_distance_below_bottom_of_window: float | None = ...,
        right_tilt_angle_from_window_door: float | None = 90,
        right_depth: float | None = ...,
    ) -> None:
        """Create a new ``Shading:Fin`` and add it to the document.

        Fins are usually shading surfaces that are perpendicular to a window or door.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#shadingfin
        """

class AirflowNetworkDistributionLinkage:
    def __call__(
        self,
        name: str,
        /,
        *,
        node_1_name: str,
        node_2_name: str,
        component_name: str,
        thermal_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Linkage`` and add it to the document.

        This object defines the connection between two nodes and a component.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributionlinkage
        """

class PlantEquipmentOperationOutdoorWetBulbDifference:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_temperature_node_name: str,
        wet_bulb_temperature_difference_range_1_lower_limit: float,
        wet_bulb_temperature_difference_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        wet_bulb_temperature_difference_range_2_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_3_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_4_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_5_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_6_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_7_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_8_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_9_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        wet_bulb_temperature_difference_range_10_lower_limit: float | None = ...,
        wet_bulb_temperature_difference_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:OutdoorWetBulbDifference`` and add it to the document.

        Plant equipment operation scheme for outdoor wet-bulb temperature difference operation. Specifies one or more groups of equipment which are available to operate for successive ranges based the difference between a reference node temperature and the outdoor wet-bulb temperature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationoutdoorwetbulbdifference
        """

class AnyDemandManagerAssignmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        meter_name: str,
        demand_limit_safety_fraction: float,
        demand_window_length: int,
        demand_manager_priority: Literal["All", "Sequential"],
        demand_limit_schedule_name: str | None = ...,
        billing_period_schedule_name: str | None = ...,
        peak_period_schedule_name: str | None = ...,
        manager_data: Sequence[
            _g.DemandManagerAssignmentListManagerDataItem | _g.DemandManagerAssignmentListManagerDataGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManagerAssignmentList`` and add it to the document.

        A high level control that makes demand limiting decisions based on a list of possible demand limiting strategies.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerassignmentlist
        """

class UtilityCostVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        tariff_name: str,
        variable_type: Literal["", "Currency", "Demand", "Dimensionless", "Energy"] | None = "Dimensionless",
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

class LifeCycleCostUsePriceEscalation:
    def __call__(
        self,
        /,
        *,
        lcc_price_escalation_name: str,
        resource: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
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
