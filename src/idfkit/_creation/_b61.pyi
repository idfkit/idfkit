"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class MaterialPropertyPhaseChange:
    def __call__(
        self,
        name: str,
        /,
        *,
        temperature_coefficient_for_thermal_conductivity: float | None = 0,
        values: Sequence[_g.MaterialPropertyPhaseChangeValuesItem | _g.MaterialPropertyPhaseChangeValuesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``MaterialProperty:PhaseChange`` and add it to the document.

        Additional properties for temperature dependent thermal conductivity and enthalpy for Phase Change Materials (PCM) Name and temperature coefficient are followed by up to 100 sets of temperature-enthalpy pairs. HeatBalanceAlgorithm = CondFD(ConductionFiniteDifference) solution algorithm only. Constructions with this should use the detailed CondFD process. Has no effect with other HeatBalanceAlgorithm solution algorithms

        ``values`` takes the extensible groups in order, one dict per group:

        ```python
        doc["MaterialProperty:PhaseChange"].add(
            "MaterialProperty PhaseChange 1",
            values=[
                {"temperature": 0.0, "enthalpy": 0.0},
                {"temperature": 0.0, "enthalpy": 0.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyphasechange
        """

class MaterialPropertyHeatAndMoistureTransferSettings:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        material_name: str,
        porosity: float,
        initial_water_content_ratio: float | None = 0.2,
        validate: bool = True,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Settings`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Additional material properties for surfaces. Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransfersettings
        """

class SteamEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``SteamEquipment`` and add it to the document.

        Sets internal gains for steam equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#steamequipment
        """

class AirLoopHVACReturnPlenum:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_node_name: str,
        outlet_node_name: str,
        induced_air_outlet_node_or_nodelist_name: str | None = ...,
        nodes: Sequence[_g.AirLoopHVACReturnPlenumNodesItem | _g.AirLoopHVACReturnPlenumNodesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirLoopHVAC:ReturnPlenum`` and add it to the document.

        Connects N zone inlet air streams, through zone return plenum, to outlet (currently 500 per air loop) Node names cannot be duplicated within a single plenum list.

        ``nodes`` takes the extensible groups in order, one dict per group:

        ```python
        doc["AirLoopHVAC:ReturnPlenum"].add(
            "AirLoopHVAC ReturnPlenum 1",
            zone_name="Zone 1",
            zone_node_name="Zone Node Name",
            outlet_node_name="Outlet Node Name",
            nodes=[
                {"inlet_node_name": "Inlet Node Name"},
                {"inlet_node_name": "Inlet Node Name"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacreturnplenum
        """

class ExternalInterfaceFunctionalMockupUnitExportToVariable:
    def __call__(self, name: str, /, *, fmu_variable_name: str, initial_value: float, validate: bool = True) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitExport:To:Variable`` and add it to the document.

        Declares Erl variable as having global scope No spaces allowed in names used for Erl variables

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitexporttovariable
        """

class SetpointManagerFollowOutdoorAirTemperature:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["MaximumTemperature", "MinimumTemperature", "Temperature"] | None = "Temperature",
        reference_temperature_type: Literal["OutdoorAirDryBulb", "OutdoorAirWetBulb"] | None = "OutdoorAirWetBulb",
        offset_temperature_difference: float | None = ...,
        maximum_setpoint_temperature: float | None = ...,
        minimum_setpoint_temperature: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:FollowOutdoorAirTemperature`` and add it to the document.

        This setpoint manager is used to place a temperature setpoint on a system node that is derived from the current outdoor air environmental conditions. The outdoor air conditions are obtained from the weather information during the simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerfollowoutdoorairtemperature
        """

class WaterUseStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_temperature_schedule_name: str,
        water_quality_subcategory: str | None = ...,
        maximum_capacity: float | None = ...,
        initial_volume: float | None = ...,
        design_in_flow_rate: float | None = ...,
        design_out_flow_rate: float | None = ...,
        overflow_destination: str | None = ...,
        type_of_supply_controlled_by_float_valve: Literal["GroundwaterWell", "Mains", "None", "OtherTank"] | None = ...,
        float_valve_on_capacity: float | None = ...,
        float_valve_off_capacity: float | None = ...,
        backup_mains_capacity: float | None = ...,
        other_tank_name: str | None = ...,
        water_thermal_mode: Literal["ScheduledTemperature", "ThermalModel"] | None = ...,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"] | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        tank_surface_area: float | None = ...,
        tank_u_value: float | None = ...,
        tank_outside_surface_material_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WaterUse:Storage`` and add it to the document.

        A water storage tank. If the building model is to include any on-site water collection, wells, or storing and reuse of graywater, then a WaterUse:Storage object is needed. Each WaterUse:Storage can serve as a central node and make connections to numerous sources of supply or numerous components with demand. If a maximum capacity is not specified, the tank is assumed to have unlimited capacity.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-systems/#waterusestorage
        """

class FaultModelTemperatureSensorOffsetCondenserSupplyWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_tower_object_type: Literal[
            "CoolingTower:SingleSpeed",
            "CoolingTower:TwoSpeed",
            "CoolingTower:VariableSpeed",
            "CoolingTower:VariableSpeed:MERKEL",
        ],
        cooling_tower_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_sensor_offset: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``FaultModel:TemperatureSensorOffset:CondenserSupplyWater`` and add it to the document.

        This object describes fault of condenser supply water temperature sensor offset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodeltemperaturesensoroffsetcondensersupplywater
        """
