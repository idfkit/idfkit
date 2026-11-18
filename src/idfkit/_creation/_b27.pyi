"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SiteWaterMainsTemperature:
    def __call__(
        self,
        /,
        *,
        calculation_method: Literal["Correlation", "CorrelationFromWeatherFile", "Schedule"]
        | None = "CorrelationFromWeatherFile",
        temperature_schedule_name: str | None = ...,
        annual_average_outdoor_air_temperature: float | None = ...,
        maximum_difference_in_monthly_average_outdoor_air_temperatures: float | None = ...,
        temperature_multiplier: float | None = 1,
        temperature_offset: float | None = 0,
    ) -> None:
        """Create a new ``Site:WaterMainsTemperature`` and add it to the document.

        Used to calculate water mains temperatures delivered by underground water main pipes. Water mains temperatures are a function of outdoor climate conditions and vary with time of year.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitewatermainstemperature
        """

class ScheduleDayInterval:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        interpolate_to_timestep: Literal["Average", "Linear", "No"] | None = "No",
        data: Sequence[_g.ScheduleDayIntervalDataItem | _g.ScheduleDayIntervalDataGroup] = ...,
    ) -> None:
        """Create a new ``Schedule:Day:Interval`` and add it to the document.

        A Schedule:Day:Interval contains a full day of values with specified end times for each value Currently, is set up to allow for 10 minute intervals for an entire day.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduledayinterval
        """

class InternalMass:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_area: float,
        construction_name: str | None = ...,
        zone_or_zonelist_name: str | None = ...,
        space_or_spacelist_name: str | None = ...,
    ) -> None:
        """Create a new ``InternalMass`` and add it to the document.

        Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList. Likewise for SpaceList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#internalmass
        """

class GroundHeatTransferSlabYFACE:
    def __call__(self, /) -> None:
        """Create a new ``GroundHeatTransfer:Slab:YFACE`` and add it to the document.

        This is only needed when using manual gridding (not recommended) YFACE: Y Direction cell face coordinates: m,

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabyface
        """

class AnyComfortViewFactorAngles:
    def __call__(self, name: str = "", /) -> None:
        """Create a new ``ComfortViewFactorAngles`` and add it to the document.

        Used to specify radiant view factors for thermal comfort calculations. Note that the following angle factor fractions must sum up to 1.0 All surfaces must be in the same enclosure.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#comfortviewfactorangles
        """

class GasEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        gas_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``GasEquipment:Instance`` and add it to the document.

        Sets internal gains and contaminant rates for gas equipment in the zone. The physical characteristics are given by the referenced GasEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#gasequipmentinstance
        """

class AnyIndoorLivingWall:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        schedule_name: str,
        evapotranspiration_calculation_method: Literal["Penman-Monteith", "Stanghellini"] | None = "Penman-Monteith",
        lighting_method: Literal["Daylight", "LED", "LED-Daylight"] | None = ...,
        daylighting_control_name: str | None = ...,
        led_daylight_targeted_lighting_intensity_schedule_name: str | None = ...,
        total_leaf_area: float | None = ...,
        led_nominal_power: float | None = ...,
        radiant_fraction_of_led_lights: float | None = 0.6,
    ) -> None:
        """Create a new ``IndoorLivingWall`` and add it to the document.

        Indoor greenery systems such as indoor living walls are panels of plants, which grow hydroponically or from substrates. The living wall structures can be either free-standing or attached to walls. The IndoorLivingWall module directly connects with inside surface heat balance, zone air heat balance, and zone air moisture balance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#indoorlivingwall
        """

class AirflowNetworkDistributionComponentConstantPressureDrop:
    def __call__(self, name: str, /, *, pressure_difference_across_the_component: float) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:ConstantPressureDrop`` and add it to the document.

        This object defines the characteristics of a constant pressure drop component (e.g. filter). Each node connected to this object can not be a node of mixer, splitter, a node of air primary loop, or zone equipment loop. It is recommended to connect to a duct component at both ends.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentconstantpressuredrop
        """

class ThermostatSetpointThermalComfortFangerDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        fanger_thermal_comfort_heating_schedule_name: str,
        fanger_thermal_comfort_cooling_schedule_name: str,
    ) -> None:
        """Create a new ``ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint`` and add it to the document.

        Used for heating and cooling thermal comfort control with dual setpoints. The PMV setpoints can be scheduled and varied throughout the simulation for both heating and cooling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointthermalcomfortfangerdualsetpoint
        """

class FanConstantVolume:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_rise: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.7,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        motor_in_airstream_fraction: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Fan:ConstantVolume`` and add it to the document.

        Constant volume fan that is intended to operate continuously based on a time schedule. This fan will not cycle on and off based on cooling/heating load or other control signals.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fanconstantvolume
        """

class UtilityCostRatchet:
    def __call__(
        self,
        name: str,
        /,
        *,
        tariff_name: str,
        baseline_source_variable: str,
        adjustment_source_variable: str,
        season_from: Literal["Annual", "Fall", "Monthly", "Spring", "Summer", "Winter"] | None = ...,
        season_to: Literal["Annual", "Fall", "Spring", "Summer", "Winter"] | None = ...,
        multiplier_value_or_variable_name: float | str | None = ...,
        offset_value_or_variable_name: float | str | None = ...,
    ) -> None:
        """Create a new ``UtilityCost:Ratchet`` and add it to the document.

        Allows the modeling of tariffs that include some type of seasonal ratcheting. Ratchets are most common when used with electric demand charges. A ratchet is when a utility requires that the demand charge for a month with a low demand may be increased to be more consistent with a month that set a higher demand charge.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-ratchet/#utilitycostratchet
        """

class AnyOutputMeter:
    def __call__(
        self,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
    ) -> None:
        """Create a new ``Output:Meter`` and add it to the document.

        Each Output:Meter command picks meters to be put onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. A list of meters that can be reported are available after a run on the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-output-reporting/#outputmeter
        """
