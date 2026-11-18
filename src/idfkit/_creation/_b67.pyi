"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class Material:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thickness: float,
        conductivity: float,
        density: float,
        specific_heat: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
        thermal_absorptance_inside_face: float | None = ...,
        solar_absorptance_inside_face: float | None = ...,
        visible_absorptance_inside_face: float | None = ...,
    ) -> None:
        """Create a new ``Material`` and add it to the document.

        Regular materials described with full set of thermal properties

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#material
        """

class AnyInternalMass:
    def __call__(
        self, name: str, /, *, narrow_with_as_version_first: Never, construction_name: str, surface_area: float
    ) -> None:
        """Create a new ``InternalMass`` and add it to the document.

        Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList. Likewise for SpaceList.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#internalmass
        """

class AirflowNetworkDistributionDuctViewFactors:
    def __call__(
        self,
        /,
        *,
        linkage_name: str,
        duct_surface_exposure_fraction: float | None = 0,
        duct_surface_emittance: float | None = 0.9,
        surfaces: Sequence[
            _g.AirflowNetworkDistributionDuctViewFactorsSurfacesItem
            | _g.AirflowNetworkDistributionDuctViewFactorsSurfacesGroup
        ] = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:DuctViewFactors`` and add it to the document.

        This object is used to allow user-defined view factors to be used for duct-surface radiation calculations. All surfaces must be in the same enclosure.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributionductviewfactors
        """

class AirLoopHVACReturnPath:
    def __call__(
        self,
        name: str,
        /,
        *,
        return_air_path_outlet_node_name: str,
        components: Sequence[_g.AirLoopHVACReturnPathComponentsItem | _g.AirLoopHVACReturnPathComponentsGroup] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:ReturnPath`` and add it to the document.

        A return air path can only contain one AirLoopHVAC:ZoneMixer and one or more AirLoopHVAC:ReturnPlenum objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacreturnpath
        """

class WaterUseRainCollector:
    def __call__(
        self,
        name: str,
        /,
        *,
        storage_tank_name: str,
        loss_factor_mode: Literal["Constant", "Scheduled"] | None = ...,
        collection_loss_factor: float | None = ...,
        collection_loss_factor_schedule_name: str | None = ...,
        maximum_collection_rate: float | None = ...,
        surfaces: Sequence[_g.WaterUseRainCollectorSurfacesItem | _g.WaterUseRainCollectorSurfacesGroup] = ...,
    ) -> None:
        """Create a new ``WaterUse:RainCollector`` and add it to the document.

        Used for harvesting rainwater falling on building surfaces. The rainwater is sent to a WaterUse:Storage object. In versions up till Version 9.6, it is necessary to also include a Site:Precipitation object to describe the rates of rainfall, in order to use this object. In later versions, if the Site:Precipitation is not present, precipitation depth in the weather input .epw will be used instead. When this is the case, please make sure the precipitation in the .epw is accurate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-systems/#wateruseraincollector
        """

class OutputMeterCumulative:
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
        """Create a new ``Output:Meter:Cumulative`` and add it to the document.

        Each Output:Meter:Cumulative command picks meters to be reported cumulatively onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. a list of meters that can be reported are available after a run on the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-output-reporting/#outputmetercumulative
        """
