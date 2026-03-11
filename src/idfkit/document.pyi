"""Auto-generated type stub for IDFDocument (EnergyPlus 25.2.0).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs 25.2.0
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any, Generic, Literal, TypeVar, overload

from ._compat import EppyDocumentMixin
from ._generated_types import *  # noqa: F403
from .introspection import ObjectDescription
from .objects import IDFCollection, IDFObject
from .references import ReferenceGraph
from .schema import EpJSONSchema
from .simulation.config import EnergyPlusConfig

Strict = TypeVar("Strict", bound=bool, default=bool)

_PYTHON_TO_IDF: dict[str, str]
_IDF_TO_PYTHON: dict[str, str]

class IDFDocument(EppyDocumentMixin, Generic[Strict]):
    version: tuple[int, int, int]
    filepath: Path | None

    def __init__(
        self,
        version: tuple[int, int, int] | None = ...,
        schema: EpJSONSchema | None = ...,
        filepath: Path | str | None = ...,
        *,
        strict: Strict = ...,  # type: ignore[assignment]
    ) -> None: ...
    @property
    def strict(self) -> Strict: ...
    @property
    def schema(self) -> EpJSONSchema | None: ...
    @property
    def collections(self) -> dict[str, IDFCollection[IDFObject]]: ...
    @property
    def references(self) -> ReferenceGraph: ...
    @overload
    def __getitem__(self, obj_type: Literal["Version"]) -> IDFCollection[Version]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SimulationControl"]) -> IDFCollection[SimulationControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PerformancePrecisionTradeoffs"]
    ) -> IDFCollection[PerformancePrecisionTradeoffs]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Building"]) -> IDFCollection[Building]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ShadowCalculation"]) -> IDFCollection[ShadowCalculation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside"]
    ) -> IDFCollection[SurfaceConvectionAlgorithmInside]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside"]
    ) -> IDFCollection[SurfaceConvectionAlgorithmOutside]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HeatBalanceAlgorithm"]) -> IDFCollection[HeatBalanceAlgorithm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatBalanceSettings:ConductionFiniteDifference"]
    ) -> IDFCollection[HeatBalanceSettingsConductionFiniteDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirHeatBalanceAlgorithm"]
    ) -> IDFCollection[ZoneAirHeatBalanceAlgorithm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirContaminantBalance"]
    ) -> IDFCollection[ZoneAirContaminantBalance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirMassFlowConservation"]
    ) -> IDFCollection[ZoneAirMassFlowConservation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneCapacitanceMultiplier:ResearchSpecial"]
    ) -> IDFCollection[ZoneCapacitanceMultiplierResearchSpecial]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Timestep"]) -> IDFCollection[Timestep]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ConvergenceLimits"]) -> IDFCollection[ConvergenceLimits]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACSystemRootFindingAlgorithm"]
    ) -> IDFCollection[HVACSystemRootFindingAlgorithm]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Compliance:Building"]) -> IDFCollection[ComplianceBuilding]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:Location"]) -> IDFCollection[SiteLocation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:VariableLocation"]) -> IDFCollection[SiteVariableLocation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SizingPeriod:DesignDay"]) -> IDFCollection[SizingPeriodDesignDay]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SizingPeriod:WeatherFileDays"]
    ) -> IDFCollection[SizingPeriodWeatherFileDays]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SizingPeriod:WeatherFileConditionType"]
    ) -> IDFCollection[SizingPeriodWeatherFileConditionType]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RunPeriod"]) -> IDFCollection[RunPeriod]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RunPeriodControl:SpecialDays"]
    ) -> IDFCollection[RunPeriodControlSpecialDays]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RunPeriodControl:DaylightSavingTime"]
    ) -> IDFCollection[RunPeriodControlDaylightSavingTime]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WeatherProperty:SkyTemperature"]
    ) -> IDFCollection[WeatherPropertySkyTemperature]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:WeatherStation"]) -> IDFCollection[SiteWeatherStation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:HeightVariation"]) -> IDFCollection[SiteHeightVariation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:BuildingSurface"]
    ) -> IDFCollection[SiteGroundTemperatureBuildingSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:FCfactorMethod"]
    ) -> IDFCollection[SiteGroundTemperatureFCfactorMethod]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Shallow"]
    ) -> IDFCollection[SiteGroundTemperatureShallow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Deep"]
    ) -> IDFCollection[SiteGroundTemperatureDeep]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:FiniteDifference"]
    ) -> IDFCollection[SiteGroundTemperatureUndisturbedFiniteDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:KusudaAchenbach"]
    ) -> IDFCollection[SiteGroundTemperatureUndisturbedKusudaAchenbach]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:Xing"]
    ) -> IDFCollection[SiteGroundTemperatureUndisturbedXing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:GroundDomain:Slab"]) -> IDFCollection[SiteGroundDomainSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundDomain:Basement"]
    ) -> IDFCollection[SiteGroundDomainBasement]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:GroundReflectance"]) -> IDFCollection[SiteGroundReflectance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundReflectance:SnowModifier"]
    ) -> IDFCollection[SiteGroundReflectanceSnowModifier]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:WaterMainsTemperature"]
    ) -> IDFCollection[SiteWaterMainsTemperature]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:Precipitation"]) -> IDFCollection[SitePrecipitation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoofIrrigation"]) -> IDFCollection[RoofIrrigation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:SolarAndVisibleSpectrum"]
    ) -> IDFCollection[SiteSolarAndVisibleSpectrum]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:SpectrumData"]) -> IDFCollection[SiteSpectrumData]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ScheduleTypeLimits"]) -> IDFCollection[ScheduleTypeLimits]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Day:Hourly"]) -> IDFCollection[ScheduleDayHourly]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Day:Interval"]) -> IDFCollection[ScheduleDayInterval]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Day:List"]) -> IDFCollection[ScheduleDayList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Week:Daily"]) -> IDFCollection[ScheduleWeekDaily]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Week:Compact"]) -> IDFCollection[ScheduleWeekCompact]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Year"]) -> IDFCollection[ScheduleYear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Compact"]) -> IDFCollection[ScheduleCompact]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Constant"]) -> IDFCollection[ScheduleConstant]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:File:Shading"]) -> IDFCollection[ScheduleFileShading]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:File"]) -> IDFCollection[ScheduleFile]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Material"]) -> IDFCollection[Material]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Material:NoMass"]) -> IDFCollection[MaterialNoMass]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Material:InfraredTransparent"]
    ) -> IDFCollection[MaterialInfraredTransparent]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Material:AirGap"]) -> IDFCollection[MaterialAirGap]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Material:RoofVegetation"]) -> IDFCollection[MaterialRoofVegetation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:SimpleGlazingSystem"]
    ) -> IDFCollection[WindowMaterialSimpleGlazingSystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Glazing"]) -> IDFCollection[WindowMaterialGlazing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:GlazingGroup:Thermochromic"]
    ) -> IDFCollection[WindowMaterialGlazingGroupThermochromic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Glazing:RefractionExtinctionMethod"]
    ) -> IDFCollection[WindowMaterialGlazingRefractionExtinctionMethod]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Gas"]) -> IDFCollection[WindowMaterialGas]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowGap:SupportPillar"]) -> IDFCollection[WindowGapSupportPillar]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowGap:DeflectionState"]
    ) -> IDFCollection[WindowGapDeflectionState]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:GasMixture"]
    ) -> IDFCollection[WindowMaterialGasMixture]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Gap"]) -> IDFCollection[WindowMaterialGap]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Shade"]) -> IDFCollection[WindowMaterialShade]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:ComplexShade"]
    ) -> IDFCollection[WindowMaterialComplexShade]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Blind"]) -> IDFCollection[WindowMaterialBlind]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Screen"]) -> IDFCollection[WindowMaterialScreen]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Shade:EquivalentLayer"]
    ) -> IDFCollection[WindowMaterialShadeEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Drape:EquivalentLayer"]
    ) -> IDFCollection[WindowMaterialDrapeEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Blind:EquivalentLayer"]
    ) -> IDFCollection[WindowMaterialBlindEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Screen:EquivalentLayer"]
    ) -> IDFCollection[WindowMaterialScreenEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Glazing:EquivalentLayer"]
    ) -> IDFCollection[WindowMaterialGlazingEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Gap:EquivalentLayer"]
    ) -> IDFCollection[WindowMaterialGapEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:MoisturePenetrationDepth:Settings"]
    ) -> IDFCollection[MaterialPropertyMoisturePenetrationDepthSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:PhaseChange"]
    ) -> IDFCollection[MaterialPropertyPhaseChange]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:PhaseChangeHysteresis"]
    ) -> IDFCollection[MaterialPropertyPhaseChangeHysteresis]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:VariableThermalConductivity"]
    ) -> IDFCollection[MaterialPropertyVariableThermalConductivity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:VariableAbsorptance"]
    ) -> IDFCollection[MaterialPropertyVariableAbsorptance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Settings"]
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:SorptionIsotherm"]
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferSorptionIsotherm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Suction"]
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferSuction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Redistribution"]
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferRedistribution]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Diffusion"]
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferDiffusion]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:ThermalConductivity"]
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferThermalConductivity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:GlazingSpectralData"]
    ) -> IDFCollection[MaterialPropertyGlazingSpectralData]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Construction"]) -> IDFCollection[Construction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:CfactorUndergroundWall"]
    ) -> IDFCollection[ConstructionCfactorUndergroundWall]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:FfactorGroundFloor"]
    ) -> IDFCollection[ConstructionFfactorGroundFloor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ConstructionProperty:InternalHeatSource"]
    ) -> IDFCollection[ConstructionPropertyInternalHeatSource]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Construction:AirBoundary"]) -> IDFCollection[ConstructionAirBoundary]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowThermalModel:Params"]
    ) -> IDFCollection[WindowThermalModelParams]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowsCalculationEngine"]) -> IDFCollection[WindowsCalculationEngine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:ComplexFenestrationState"]
    ) -> IDFCollection[ConstructionComplexFenestrationState]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:WindowEquivalentLayer"]
    ) -> IDFCollection[ConstructionWindowEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:WindowDataFile"]
    ) -> IDFCollection[ConstructionWindowDataFile]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GlobalGeometryRules"]) -> IDFCollection[GlobalGeometryRules]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GeometryTransform"]) -> IDFCollection[GeometryTransform]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Space"]) -> IDFCollection[Space]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SpaceList"]) -> IDFCollection[SpaceList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Zone"]) -> IDFCollection[Zone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneList"]) -> IDFCollection[ZoneList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneGroup"]) -> IDFCollection[ZoneGroup]: ...
    @overload
    def __getitem__(self, obj_type: Literal["BuildingSurface:Detailed"]) -> IDFCollection[BuildingSurfaceDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Detailed"]) -> IDFCollection[WallDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoofCeiling:Detailed"]) -> IDFCollection[RoofCeilingDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Detailed"]) -> IDFCollection[FloorDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Exterior"]) -> IDFCollection[WallExterior]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Adiabatic"]) -> IDFCollection[WallAdiabatic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Underground"]) -> IDFCollection[WallUnderground]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Interzone"]) -> IDFCollection[WallInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Roof"]) -> IDFCollection[Roof]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Ceiling:Adiabatic"]) -> IDFCollection[CeilingAdiabatic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Ceiling:Interzone"]) -> IDFCollection[CeilingInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:GroundContact"]) -> IDFCollection[FloorGroundContact]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Adiabatic"]) -> IDFCollection[FloorAdiabatic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Interzone"]) -> IDFCollection[FloorInterzone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FenestrationSurface:Detailed"]
    ) -> IDFCollection[FenestrationSurfaceDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Window"]) -> IDFCollection[Window]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Door"]) -> IDFCollection[Door]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GlazedDoor"]) -> IDFCollection[GlazedDoor]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Window:Interzone"]) -> IDFCollection[WindowInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Door:Interzone"]) -> IDFCollection[DoorInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GlazedDoor:Interzone"]) -> IDFCollection[GlazedDoorInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowShadingControl"]) -> IDFCollection[WindowShadingControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:FrameAndDivider"]
    ) -> IDFCollection[WindowPropertyFrameAndDivider]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:AirflowControl"]
    ) -> IDFCollection[WindowPropertyAirflowControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:StormWindow"]
    ) -> IDFCollection[WindowPropertyStormWindow]: ...
    @overload
    def __getitem__(self, obj_type: Literal["InternalMass"]) -> IDFCollection[InternalMass]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Site"]) -> IDFCollection[ShadingSite]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Building"]) -> IDFCollection[ShadingBuilding]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Site:Detailed"]) -> IDFCollection[ShadingSiteDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Building:Detailed"]) -> IDFCollection[ShadingBuildingDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Overhang"]) -> IDFCollection[ShadingOverhang]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Shading:Overhang:Projection"]
    ) -> IDFCollection[ShadingOverhangProjection]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Fin"]) -> IDFCollection[ShadingFin]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Fin:Projection"]) -> IDFCollection[ShadingFinProjection]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Zone:Detailed"]) -> IDFCollection[ShadingZoneDetailed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ShadingProperty:Reflectance"]
    ) -> IDFCollection[ShadingPropertyReflectance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm"]
    ) -> IDFCollection[SurfacePropertyHeatTransferAlgorithm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:MultipleSurface"]
    ) -> IDFCollection[SurfacePropertyHeatTransferAlgorithmMultipleSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:SurfaceList"]
    ) -> IDFCollection[SurfacePropertyHeatTransferAlgorithmSurfaceList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:Construction"]
    ) -> IDFCollection[SurfacePropertyHeatTransferAlgorithmConstruction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatBalanceSourceTerm"]
    ) -> IDFCollection[SurfacePropertyHeatBalanceSourceTerm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceControl:MovableInsulation"]
    ) -> IDFCollection[SurfaceControlMovableInsulation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:OtherSideCoefficients"]
    ) -> IDFCollection[SurfacePropertyOtherSideCoefficients]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:OtherSideConditionsModel"]
    ) -> IDFCollection[SurfacePropertyOtherSideConditionsModel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:Underwater"]
    ) -> IDFCollection[SurfacePropertyUnderwater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Foundation:Kiva"]) -> IDFCollection[FoundationKiva]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Foundation:Kiva:Settings"]) -> IDFCollection[FoundationKivaSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ExposedFoundationPerimeter"]
    ) -> IDFCollection[SurfacePropertyExposedFoundationPerimeter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside:AdaptiveModelSelections"]
    ) -> IDFCollection[SurfaceConvectionAlgorithmInsideAdaptiveModelSelections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside:AdaptiveModelSelections"]
    ) -> IDFCollection[SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside:UserCurve"]
    ) -> IDFCollection[SurfaceConvectionAlgorithmInsideUserCurve]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside:UserCurve"]
    ) -> IDFCollection[SurfaceConvectionAlgorithmOutsideUserCurve]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ConvectionCoefficients"]
    ) -> IDFCollection[SurfacePropertyConvectionCoefficients]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ConvectionCoefficients:MultipleSurface"]
    ) -> IDFCollection[SurfacePropertyConvectionCoefficientsMultipleSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperties:VaporCoefficients"]
    ) -> IDFCollection[SurfacePropertiesVaporCoefficients]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ExteriorNaturalVentedCavity"]
    ) -> IDFCollection[SurfacePropertyExteriorNaturalVentedCavity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:SolarIncidentInside"]
    ) -> IDFCollection[SurfacePropertySolarIncidentInside]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:IncidentSolarMultiplier"]
    ) -> IDFCollection[SurfacePropertyIncidentSolarMultiplier]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:LocalEnvironment"]
    ) -> IDFCollection[SurfacePropertyLocalEnvironment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneProperty:LocalEnvironment"]
    ) -> IDFCollection[ZonePropertyLocalEnvironment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:SurroundingSurfaces"]
    ) -> IDFCollection[SurfacePropertySurroundingSurfaces]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:GroundSurfaces"]
    ) -> IDFCollection[SurfacePropertyGroundSurfaces]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComplexFenestrationProperty:SolarAbsorbedLayers"]
    ) -> IDFCollection[ComplexFenestrationPropertySolarAbsorbedLayers]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneProperty:UserViewFactors:BySurfaceName"]
    ) -> IDFCollection[ZonePropertyUserViewFactorsBySurfaceName]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Control"]
    ) -> IDFCollection[GroundHeatTransferControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:Materials"]
    ) -> IDFCollection[GroundHeatTransferSlabMaterials]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:MatlProps"]
    ) -> IDFCollection[GroundHeatTransferSlabMatlProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:BoundConds"]
    ) -> IDFCollection[GroundHeatTransferSlabBoundConds]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:BldgProps"]
    ) -> IDFCollection[GroundHeatTransferSlabBldgProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:Insulation"]
    ) -> IDFCollection[GroundHeatTransferSlabInsulation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:EquivalentSlab"]
    ) -> IDFCollection[GroundHeatTransferSlabEquivalentSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:AutoGrid"]
    ) -> IDFCollection[GroundHeatTransferSlabAutoGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:ManualGrid"]
    ) -> IDFCollection[GroundHeatTransferSlabManualGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:XFACE"]
    ) -> IDFCollection[GroundHeatTransferSlabXFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:YFACE"]
    ) -> IDFCollection[GroundHeatTransferSlabYFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:ZFACE"]
    ) -> IDFCollection[GroundHeatTransferSlabZFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:SimParameters"]
    ) -> IDFCollection[GroundHeatTransferBasementSimParameters]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:MatlProps"]
    ) -> IDFCollection[GroundHeatTransferBasementMatlProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:Insulation"]
    ) -> IDFCollection[GroundHeatTransferBasementInsulation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:SurfaceProps"]
    ) -> IDFCollection[GroundHeatTransferBasementSurfaceProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:BldgData"]
    ) -> IDFCollection[GroundHeatTransferBasementBldgData]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:Interior"]
    ) -> IDFCollection[GroundHeatTransferBasementInterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ComBldg"]
    ) -> IDFCollection[GroundHeatTransferBasementComBldg]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:EquivSlab"]
    ) -> IDFCollection[GroundHeatTransferBasementEquivSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:EquivAutoGrid"]
    ) -> IDFCollection[GroundHeatTransferBasementEquivAutoGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:AutoGrid"]
    ) -> IDFCollection[GroundHeatTransferBasementAutoGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ManualGrid"]
    ) -> IDFCollection[GroundHeatTransferBasementManualGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:XFACE"]
    ) -> IDFCollection[GroundHeatTransferBasementXFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:YFACE"]
    ) -> IDFCollection[GroundHeatTransferBasementYFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ZFACE"]
    ) -> IDFCollection[GroundHeatTransferBasementZFACE]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoomAirModelType"]) -> IDFCollection[RoomAirModelType]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:UserDefined"]
    ) -> IDFCollection[RoomAirTemperaturePatternUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:ConstantGradient"]
    ) -> IDFCollection[RoomAirTemperaturePatternConstantGradient]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:TwoGradient"]
    ) -> IDFCollection[RoomAirTemperaturePatternTwoGradient]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:NondimensionalHeight"]
    ) -> IDFCollection[RoomAirTemperaturePatternNondimensionalHeight]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:SurfaceMapping"]
    ) -> IDFCollection[RoomAirTemperaturePatternSurfaceMapping]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoomAir:Node"]) -> IDFCollection[RoomAirNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:OneNodeDisplacementVentilation"]
    ) -> IDFCollection[RoomAirSettingsOneNodeDisplacementVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:ThreeNodeDisplacementVentilation"]
    ) -> IDFCollection[RoomAirSettingsThreeNodeDisplacementVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:CrossVentilation"]
    ) -> IDFCollection[RoomAirSettingsCrossVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:UnderFloorAirDistributionInterior"]
    ) -> IDFCollection[RoomAirSettingsUnderFloorAirDistributionInterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:UnderFloorAirDistributionExterior"]
    ) -> IDFCollection[RoomAirSettingsUnderFloorAirDistributionExterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork"]
    ) -> IDFCollection[RoomAirNodeAirflowNetwork]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:AdjacentSurfaceList"]
    ) -> IDFCollection[RoomAirNodeAirflowNetworkAdjacentSurfaceList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:InternalGains"]
    ) -> IDFCollection[RoomAirNodeAirflowNetworkInternalGains]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:HVACEquipment"]
    ) -> IDFCollection[RoomAirNodeAirflowNetworkHVACEquipment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:AirflowNetwork"]
    ) -> IDFCollection[RoomAirSettingsAirflowNetwork]: ...
    @overload
    def __getitem__(self, obj_type: Literal["People"]) -> IDFCollection[People]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ComfortViewFactorAngles"]) -> IDFCollection[ComfortViewFactorAngles]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Lights"]) -> IDFCollection[Lights]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ElectricEquipment"]) -> IDFCollection[ElectricEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GasEquipment"]) -> IDFCollection[GasEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HotWaterEquipment"]) -> IDFCollection[HotWaterEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SteamEquipment"]) -> IDFCollection[SteamEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OtherEquipment"]) -> IDFCollection[OtherEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["IndoorLivingWall"]) -> IDFCollection[IndoorLivingWall]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricEquipment:ITE:AirCooled"]
    ) -> IDFCollection[ElectricEquipmentITEAirCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneBaseboard:OutdoorTemperatureControlled"]
    ) -> IDFCollection[ZoneBaseboardOutdoorTemperatureControlled]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SwimmingPool:Indoor"]) -> IDFCollection[SwimmingPoolIndoor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:CarbonDioxide"]
    ) -> IDFCollection[ZoneContaminantSourceAndSinkCarbonDioxide]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:Constant"]
    ) -> IDFCollection[ZoneContaminantSourceAndSinkGenericConstant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:PressureDriven"]
    ) -> IDFCollection[SurfaceContaminantSourceAndSinkGenericPressureDriven]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:CutoffModel"]
    ) -> IDFCollection[ZoneContaminantSourceAndSinkGenericCutoffModel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:DecaySource"]
    ) -> IDFCollection[ZoneContaminantSourceAndSinkGenericDecaySource]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:BoundaryLayerDiffusion"]
    ) -> IDFCollection[SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:DepositionVelocitySink"]
    ) -> IDFCollection[SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:DepositionRateSink"]
    ) -> IDFCollection[ZoneContaminantSourceAndSinkGenericDepositionRateSink]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Daylighting:Controls"]) -> IDFCollection[DaylightingControls]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Daylighting:ReferencePoint"]
    ) -> IDFCollection[DaylightingReferencePoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Daylighting:DELight:ComplexFenestration"]
    ) -> IDFCollection[DaylightingDELightComplexFenestration]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DaylightingDevice:Tubular"]
    ) -> IDFCollection[DaylightingDeviceTubular]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DaylightingDevice:Shelf"]) -> IDFCollection[DaylightingDeviceShelf]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DaylightingDevice:LightWell"]
    ) -> IDFCollection[DaylightingDeviceLightWell]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:DaylightFactors"]) -> IDFCollection[OutputDaylightFactors]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:IlluminanceMap"]) -> IDFCollection[OutputIlluminanceMap]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:IlluminanceMap:Style"]
    ) -> IDFCollection[OutputControlIlluminanceMapStyle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:DesignFlowRate"]
    ) -> IDFCollection[ZoneInfiltrationDesignFlowRate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:EffectiveLeakageArea"]
    ) -> IDFCollection[ZoneInfiltrationEffectiveLeakageArea]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:FlowCoefficient"]
    ) -> IDFCollection[ZoneInfiltrationFlowCoefficient]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneVentilation:DesignFlowRate"]
    ) -> IDFCollection[ZoneVentilationDesignFlowRate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneVentilation:WindandStackOpenArea"]
    ) -> IDFCollection[ZoneVentilationWindandStackOpenArea]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirBalance:OutdoorAir"]
    ) -> IDFCollection[ZoneAirBalanceOutdoorAir]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneMixing"]) -> IDFCollection[ZoneMixing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneCrossMixing"]) -> IDFCollection[ZoneCrossMixing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneRefrigerationDoorMixing"]
    ) -> IDFCollection[ZoneRefrigerationDoorMixing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneEarthtube"]) -> IDFCollection[ZoneEarthtube]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneEarthtube:Parameters"]) -> IDFCollection[ZoneEarthtubeParameters]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneCoolTower:Shower"]) -> IDFCollection[ZoneCoolTowerShower]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneThermalChimney"]) -> IDFCollection[ZoneThermalChimney]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:SimulationControl"]
    ) -> IDFCollection[AirflowNetworkSimulationControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Zone"]
    ) -> IDFCollection[AirflowNetworkMultiZoneZone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface"]
    ) -> IDFCollection[AirflowNetworkMultiZoneSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:ReferenceCrackConditions"]
    ) -> IDFCollection[AirflowNetworkMultiZoneReferenceCrackConditions]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface:Crack"]
    ) -> IDFCollection[AirflowNetworkMultiZoneSurfaceCrack]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface:EffectiveLeakageArea"]
    ) -> IDFCollection[AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:SpecifiedFlowRate"]
    ) -> IDFCollection[AirflowNetworkMultiZoneSpecifiedFlowRate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:DetailedOpening"]
    ) -> IDFCollection[AirflowNetworkMultiZoneComponentDetailedOpening]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:SimpleOpening"]
    ) -> IDFCollection[AirflowNetworkMultiZoneComponentSimpleOpening]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:HorizontalOpening"]
    ) -> IDFCollection[AirflowNetworkMultiZoneComponentHorizontalOpening]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:ZoneExhaustFan"]
    ) -> IDFCollection[AirflowNetworkMultiZoneComponentZoneExhaustFan]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:ExternalNode"]
    ) -> IDFCollection[AirflowNetworkMultiZoneExternalNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:WindPressureCoefficientArray"]
    ) -> IDFCollection[AirflowNetworkMultiZoneWindPressureCoefficientArray]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:WindPressureCoefficientValues"]
    ) -> IDFCollection[AirflowNetworkMultiZoneWindPressureCoefficientValues]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:ZoneControl:PressureController"]
    ) -> IDFCollection[AirflowNetworkZoneControlPressureController]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Node"]
    ) -> IDFCollection[AirflowNetworkDistributionNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Leak"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentLeak]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:LeakageRatio"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentLeakageRatio]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Duct"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentDuct]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Fan"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentFan]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Coil"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:HeatExchanger"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentHeatExchanger]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:TerminalUnit"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentTerminalUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:ConstantPressureDrop"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentConstantPressureDrop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:OutdoorAirFlow"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentOutdoorAirFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:ReliefAirFlow"]
    ) -> IDFCollection[AirflowNetworkDistributionComponentReliefAirFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Linkage"]
    ) -> IDFCollection[AirflowNetworkDistributionLinkage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:DuctViewFactors"]
    ) -> IDFCollection[AirflowNetworkDistributionDuctViewFactors]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:DuctSizing"]
    ) -> IDFCollection[AirflowNetworkDistributionDuctSizing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:OccupantVentilationControl"]
    ) -> IDFCollection[AirflowNetworkOccupantVentilationControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:IntraZone:Node"]
    ) -> IDFCollection[AirflowNetworkIntraZoneNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:IntraZone:Linkage"]
    ) -> IDFCollection[AirflowNetworkIntraZoneLinkage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct:Loss:Conduction"]) -> IDFCollection[DuctLossConduction]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct:Loss:Leakage"]) -> IDFCollection[DuctLossLeakage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct:Loss:MakeupAir"]) -> IDFCollection[DuctLossMakeupAir]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Exterior:Lights"]) -> IDFCollection[ExteriorLights]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Exterior:FuelEquipment"]) -> IDFCollection[ExteriorFuelEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Exterior:WaterEquipment"]) -> IDFCollection[ExteriorWaterEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Thermostat"]) -> IDFCollection[HVACTemplateThermostat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:IdealLoadsAirSystem"]
    ) -> IDFCollection[HVACTemplateZoneIdealLoadsAirSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:BaseboardHeat"]
    ) -> IDFCollection[HVACTemplateZoneBaseboardHeat]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:FanCoil"]) -> IDFCollection[HVACTemplateZoneFanCoil]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:PTAC"]) -> IDFCollection[HVACTemplateZonePTAC]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:PTHP"]) -> IDFCollection[HVACTemplateZonePTHP]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:WaterToAirHeatPump"]
    ) -> IDFCollection[HVACTemplateZoneWaterToAirHeatPump]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:VRF"]) -> IDFCollection[HVACTemplateZoneVRF]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:Unitary"]) -> IDFCollection[HVACTemplateZoneUnitary]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:VAV"]) -> IDFCollection[HVACTemplateZoneVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:VAV:FanPowered"]
    ) -> IDFCollection[HVACTemplateZoneVAVFanPowered]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:VAV:HeatAndCool"]
    ) -> IDFCollection[HVACTemplateZoneVAVHeatAndCool]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:ConstantVolume"]
    ) -> IDFCollection[HVACTemplateZoneConstantVolume]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:DualDuct"]
    ) -> IDFCollection[HVACTemplateZoneDualDuct]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:System:VRF"]) -> IDFCollection[HVACTemplateSystemVRF]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:Unitary"]
    ) -> IDFCollection[HVACTemplateSystemUnitary]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:UnitaryHeatPump:AirToAir"]
    ) -> IDFCollection[HVACTemplateSystemUnitaryHeatPumpAirToAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:UnitarySystem"]
    ) -> IDFCollection[HVACTemplateSystemUnitarySystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:System:VAV"]) -> IDFCollection[HVACTemplateSystemVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:PackagedVAV"]
    ) -> IDFCollection[HVACTemplateSystemPackagedVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:ConstantVolume"]
    ) -> IDFCollection[HVACTemplateSystemConstantVolume]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:DualDuct"]
    ) -> IDFCollection[HVACTemplateSystemDualDuct]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:DedicatedOutdoorAir"]
    ) -> IDFCollection[HVACTemplateSystemDedicatedOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:ChilledWaterLoop"]
    ) -> IDFCollection[HVACTemplatePlantChilledWaterLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Chiller"]
    ) -> IDFCollection[HVACTemplatePlantChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Chiller:ObjectReference"]
    ) -> IDFCollection[HVACTemplatePlantChillerObjectReference]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Plant:Tower"]) -> IDFCollection[HVACTemplatePlantTower]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Tower:ObjectReference"]
    ) -> IDFCollection[HVACTemplatePlantTowerObjectReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:HotWaterLoop"]
    ) -> IDFCollection[HVACTemplatePlantHotWaterLoop]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Plant:Boiler"]) -> IDFCollection[HVACTemplatePlantBoiler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Boiler:ObjectReference"]
    ) -> IDFCollection[HVACTemplatePlantBoilerObjectReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:MixedWaterLoop"]
    ) -> IDFCollection[HVACTemplatePlantMixedWaterLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:OutdoorAir"]
    ) -> IDFCollection[DesignSpecificationOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:OutdoorAir:SpaceList"]
    ) -> IDFCollection[DesignSpecificationOutdoorAirSpaceList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:ZoneAirDistribution"]
    ) -> IDFCollection[DesignSpecificationZoneAirDistribution]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:Parameters"]) -> IDFCollection[SizingParameters]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:Zone"]) -> IDFCollection[SizingZone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:ZoneHVAC:Sizing"]
    ) -> IDFCollection[DesignSpecificationZoneHVACSizing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:AirTerminal:Sizing"]
    ) -> IDFCollection[DesignSpecificationAirTerminalSizing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:System"]) -> IDFCollection[SizingSystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:Plant"]) -> IDFCollection[SizingPlant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:Sizing:Style"]
    ) -> IDFCollection[OutputControlSizingStyle]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneControl:Humidistat"]) -> IDFCollection[ZoneControlHumidistat]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneControl:Thermostat"]) -> IDFCollection[ZoneControlThermostat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:OperativeTemperature"]
    ) -> IDFCollection[ZoneControlThermostatOperativeTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:ThermalComfort"]
    ) -> IDFCollection[ZoneControlThermostatThermalComfort]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:TemperatureAndHumidity"]
    ) -> IDFCollection[ZoneControlThermostatTemperatureAndHumidity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleHeating"]
    ) -> IDFCollection[ThermostatSetpointSingleHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleCooling"]
    ) -> IDFCollection[ThermostatSetpointSingleCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleHeatingOrCooling"]
    ) -> IDFCollection[ThermostatSetpointSingleHeatingOrCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:DualSetpoint"]
    ) -> IDFCollection[ThermostatSetpointDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating"]
    ) -> IDFCollection[ThermostatSetpointThermalComfortFangerSingleHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling"]
    ) -> IDFCollection[ThermostatSetpointThermalComfortFangerSingleCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling"]
    ) -> IDFCollection[ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint"]
    ) -> IDFCollection[ThermostatSetpointThermalComfortFangerDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:StagedDualSetpoint"]
    ) -> IDFCollection[ZoneControlThermostatStagedDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:ContaminantController"]
    ) -> IDFCollection[ZoneControlContaminantController]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:IdealLoadsAirSystem"]
    ) -> IDFCollection[ZoneHVACIdealLoadsAirSystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:FourPipeFanCoil"]) -> IDFCollection[ZoneHVACFourPipeFanCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:WindowAirConditioner"]
    ) -> IDFCollection[ZoneHVACWindowAirConditioner]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:PackagedTerminalAirConditioner"]
    ) -> IDFCollection[ZoneHVACPackagedTerminalAirConditioner]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:PackagedTerminalHeatPump"]
    ) -> IDFCollection[ZoneHVACPackagedTerminalHeatPump]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:WaterToAirHeatPump"]
    ) -> IDFCollection[ZoneHVACWaterToAirHeatPump]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:Dehumidifier:DX"]) -> IDFCollection[ZoneHVACDehumidifierDX]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EnergyRecoveryVentilator"]
    ) -> IDFCollection[ZoneHVACEnergyRecoveryVentilator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EnergyRecoveryVentilator:Controller"]
    ) -> IDFCollection[ZoneHVACEnergyRecoveryVentilatorController]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:UnitVentilator"]) -> IDFCollection[ZoneHVACUnitVentilator]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:UnitHeater"]) -> IDFCollection[ZoneHVACUnitHeater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EvaporativeCoolerUnit"]
    ) -> IDFCollection[ZoneHVACEvaporativeCoolerUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:HybridUnitaryHVAC"]
    ) -> IDFCollection[ZoneHVACHybridUnitaryHVAC]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:OutdoorAirUnit"]) -> IDFCollection[ZoneHVACOutdoorAirUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:OutdoorAirUnit:EquipmentList"]
    ) -> IDFCollection[ZoneHVACOutdoorAirUnitEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:TerminalUnit:VariableRefrigerantFlow"]
    ) -> IDFCollection[ZoneHVACTerminalUnitVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Water:Design"]
    ) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveWaterDesign]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Water"]
    ) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Steam:Design"]
    ) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveSteamDesign]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Steam"]
    ) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveSteam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Electric"]
    ) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:CoolingPanel:RadiantConvective:Water"]
    ) -> IDFCollection[ZoneHVACCoolingPanelRadiantConvectiveWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:Convective:Water"]
    ) -> IDFCollection[ZoneHVACBaseboardConvectiveWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:Convective:Electric"]
    ) -> IDFCollection[ZoneHVACBaseboardConvectiveElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:VariableFlow"]
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantVariableFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design"]
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantVariableFlowDesign]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:ConstantFlow"]
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantConstantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design"]
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantConstantFlowDesign]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:Electric"]
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:SurfaceGroup"]
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantSurfaceGroup]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:HighTemperatureRadiant"]
    ) -> IDFCollection[ZoneHVACHighTemperatureRadiant]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:VentilatedSlab"]) -> IDFCollection[ZoneHVACVentilatedSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:VentilatedSlab:SlabGroup"]
    ) -> IDFCollection[ZoneHVACVentilatedSlabSlabGroup]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:Reheat"]
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:NoReheat"]
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeNoReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:NoReheat"]
    ) -> IDFCollection[AirTerminalSingleDuctVAVNoReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:Reheat"]
    ) -> IDFCollection[AirTerminalSingleDuctVAVReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan"]
    ) -> IDFCollection[AirTerminalSingleDuctVAVReheatVariableSpeedFan]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat"]
    ) -> IDFCollection[AirTerminalSingleDuctVAVHeatAndCoolNoReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat"]
    ) -> IDFCollection[AirTerminalSingleDuctVAVHeatAndCoolReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:SeriesPIU:Reheat"]
    ) -> IDFCollection[AirTerminalSingleDuctSeriesPIUReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ParallelPIU:Reheat"]
    ) -> IDFCollection[AirTerminalSingleDuctParallelPIUReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction"]
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeFourPipeInduction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam"]
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeFourPipeBeam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:CooledBeam"]
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeCooledBeam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:Mixer"]
    ) -> IDFCollection[AirTerminalSingleDuctMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:DualDuct:ConstantVolume"]
    ) -> IDFCollection[AirTerminalDualDuctConstantVolume]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirTerminal:DualDuct:VAV"]) -> IDFCollection[AirTerminalDualDuctVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:DualDuct:VAV:OutdoorAir"]
    ) -> IDFCollection[AirTerminalDualDuctVAVOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:AirDistributionUnit"]
    ) -> IDFCollection[ZoneHVACAirDistributionUnit]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:ExhaustControl"]) -> IDFCollection[ZoneHVACExhaustControl]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:EquipmentList"]) -> IDFCollection[ZoneHVACEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EquipmentConnections"]
    ) -> IDFCollection[ZoneHVACEquipmentConnections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SpaceHVAC:EquipmentConnections"]
    ) -> IDFCollection[SpaceHVACEquipmentConnections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SpaceHVAC:ZoneEquipmentSplitter"]
    ) -> IDFCollection[SpaceHVACZoneEquipmentSplitter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SpaceHVAC:ZoneEquipmentMixer"]
    ) -> IDFCollection[SpaceHVACZoneEquipmentMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SpaceHVAC:ZoneReturnMixer"]
    ) -> IDFCollection[SpaceHVACZoneReturnMixer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:SystemModel"]) -> IDFCollection[FanSystemModel]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ConstantVolume"]) -> IDFCollection[FanConstantVolume]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:VariableVolume"]) -> IDFCollection[FanVariableVolume]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:OnOff"]) -> IDFCollection[FanOnOff]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ZoneExhaust"]) -> IDFCollection[FanZoneExhaust]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FanPerformance:NightVentilation"]
    ) -> IDFCollection[FanPerformanceNightVentilation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ComponentModel"]) -> IDFCollection[FanComponentModel]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Cooling:Water"]) -> IDFCollection[CoilCoolingWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:Water:DetailedGeometry"]
    ) -> IDFCollection[CoilCoolingWaterDetailedGeometry]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoilSystem:Cooling:Water"]) -> IDFCollection[CoilSystemCoolingWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Cooling:DX"]) -> IDFCollection[CoilCoolingDX]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:CurveFit:Performance"]
    ) -> IDFCollection[CoilCoolingDXCurveFitPerformance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:CurveFit:OperatingMode"]
    ) -> IDFCollection[CoilCoolingDXCurveFitOperatingMode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:CurveFit:Speed"]
    ) -> IDFCollection[CoilCoolingDXCurveFitSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:DX:ASHRAE205:Performance"]
    ) -> IDFCollection[CoilDXASHRAE205Performance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:SingleSpeed"]
    ) -> IDFCollection[CoilCoolingDXSingleSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Cooling:DX:TwoSpeed"]) -> IDFCollection[CoilCoolingDXTwoSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:MultiSpeed"]
    ) -> IDFCollection[CoilCoolingDXMultiSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableSpeed"]
    ) -> IDFCollection[CoilCoolingDXVariableSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:TwoStageWithHumidityControlMode"]
    ) -> IDFCollection[CoilCoolingDXTwoStageWithHumidityControlMode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilPerformance:DX:Cooling"]
    ) -> IDFCollection[CoilPerformanceDXCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableRefrigerantFlow"]
    ) -> IDFCollection[CoilCoolingDXVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableRefrigerantFlow"]
    ) -> IDFCollection[CoilHeatingDXVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"]
    ) -> IDFCollection[CoilCoolingDXVariableRefrigerantFlowFluidTemperatureControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"]
    ) -> IDFCollection[CoilHeatingDXVariableRefrigerantFlowFluidTemperatureControl]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Water"]) -> IDFCollection[CoilHeatingWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Steam"]) -> IDFCollection[CoilHeatingSteam]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Electric"]) -> IDFCollection[CoilHeatingElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Electric:MultiStage"]
    ) -> IDFCollection[CoilHeatingElectricMultiStage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Fuel"]) -> IDFCollection[CoilHeatingFuel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Gas:MultiStage"]
    ) -> IDFCollection[CoilHeatingGasMultiStage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Desuperheater"]
    ) -> IDFCollection[CoilHeatingDesuperheater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:SingleSpeed"]
    ) -> IDFCollection[CoilHeatingDXSingleSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:MultiSpeed"]
    ) -> IDFCollection[CoilHeatingDXMultiSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableSpeed"]
    ) -> IDFCollection[CoilHeatingDXVariableSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:ParameterEstimation"]
    ) -> IDFCollection[CoilCoolingWaterToAirHeatPumpParameterEstimation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:ParameterEstimation"]
    ) -> IDFCollection[CoilHeatingWaterToAirHeatPumpParameterEstimation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:EquationFit"]
    ) -> IDFCollection[CoilCoolingWaterToAirHeatPumpEquationFit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"]
    ) -> IDFCollection[CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:EquationFit"]
    ) -> IDFCollection[CoilHeatingWaterToAirHeatPumpEquationFit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"]
    ) -> IDFCollection[CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:Pumped"]
    ) -> IDFCollection[CoilWaterHeatingAirToWaterHeatPumpPumped]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:Wrapped"]
    ) -> IDFCollection[CoilWaterHeatingAirToWaterHeatPumpWrapped]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed"]
    ) -> IDFCollection[CoilWaterHeatingAirToWaterHeatPumpVariableSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:Desuperheater"]
    ) -> IDFCollection[CoilWaterHeatingDesuperheater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoilSystem:Cooling:DX"]) -> IDFCollection[CoilSystemCoolingDX]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoilSystem:Heating:DX"]) -> IDFCollection[CoilSystemHeatingDX]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:Cooling:Water:HeatExchangerAssisted"]
    ) -> IDFCollection[CoilSystemCoolingWaterHeatExchangerAssisted]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:Cooling:DX:HeatExchangerAssisted"]
    ) -> IDFCollection[CoilSystemCoolingDXHeatExchangerAssisted]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:IntegratedHeatPump:AirSource"]
    ) -> IDFCollection[CoilSystemIntegratedHeatPumpAirSource]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:SingleSpeed:ThermalStorage"]
    ) -> IDFCollection[CoilCoolingDXSingleSpeedThermalStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Direct:CelDekPad"]
    ) -> IDFCollection[EvaporativeCoolerDirectCelDekPad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:CelDekPad"]
    ) -> IDFCollection[EvaporativeCoolerIndirectCelDekPad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:WetCoil"]
    ) -> IDFCollection[EvaporativeCoolerIndirectWetCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:ResearchSpecial"]
    ) -> IDFCollection[EvaporativeCoolerIndirectResearchSpecial]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Direct:ResearchSpecial"]
    ) -> IDFCollection[EvaporativeCoolerDirectResearchSpecial]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Humidifier:Steam:Electric"]) -> IDFCollection[HumidifierSteamElectric]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Humidifier:Steam:Gas"]) -> IDFCollection[HumidifierSteamGas]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Dehumidifier:Desiccant:NoFans"]
    ) -> IDFCollection[DehumidifierDesiccantNoFans]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Dehumidifier:Desiccant:System"]
    ) -> IDFCollection[DehumidifierDesiccantSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:AirToAir:FlatPlate"]
    ) -> IDFCollection[HeatExchangerAirToAirFlatPlate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:AirToAir:SensibleAndLatent"]
    ) -> IDFCollection[HeatExchangerAirToAirSensibleAndLatent]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:Desiccant:BalancedFlow"]
    ) -> IDFCollection[HeatExchangerDesiccantBalancedFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:Desiccant:BalancedFlow:PerformanceDataType1"]
    ) -> IDFCollection[HeatExchangerDesiccantBalancedFlowPerformanceDataType1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitarySystem"]
    ) -> IDFCollection[AirLoopHVACUnitarySystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UnitarySystemPerformance:Multispeed"]
    ) -> IDFCollection[UnitarySystemPerformanceMultispeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:Unitary:Furnace:HeatOnly"]
    ) -> IDFCollection[AirLoopHVACUnitaryFurnaceHeatOnly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:Unitary:Furnace:HeatCool"]
    ) -> IDFCollection[AirLoopHVACUnitaryFurnaceHeatCool]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatOnly"]
    ) -> IDFCollection[AirLoopHVACUnitaryHeatOnly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatCool"]
    ) -> IDFCollection[AirLoopHVACUnitaryHeatCool]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:AirToAir"]
    ) -> IDFCollection[AirLoopHVACUnitaryHeatPumpAirToAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:WaterToAir"]
    ) -> IDFCollection[AirLoopHVACUnitaryHeatPumpWaterToAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass"]
    ) -> IDFCollection[AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed"]
    ) -> IDFCollection[AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow"]
    ) -> IDFCollection[AirConditionerVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl"]
    ) -> IDFCollection[AirConditionerVariableRefrigerantFlowFluidTemperatureControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR"]
    ) -> IDFCollection[AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneTerminalUnitList"]) -> IDFCollection[ZoneTerminalUnitList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Controller:WaterCoil"]) -> IDFCollection[ControllerWaterCoil]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Controller:OutdoorAir"]) -> IDFCollection[ControllerOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Controller:MechanicalVentilation"]
    ) -> IDFCollection[ControllerMechanicalVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ControllerList"]
    ) -> IDFCollection[AirLoopHVACControllerList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC"]) -> IDFCollection[AirLoopHVAC]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:OutdoorAirSystem:EquipmentList"]
    ) -> IDFCollection[AirLoopHVACOutdoorAirSystemEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:OutdoorAirSystem"]
    ) -> IDFCollection[AirLoopHVACOutdoorAirSystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:Mixer"]) -> IDFCollection[OutdoorAirMixer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:ZoneSplitter"]) -> IDFCollection[AirLoopHVACZoneSplitter]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:SupplyPlenum"]) -> IDFCollection[AirLoopHVACSupplyPlenum]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:SupplyPath"]) -> IDFCollection[AirLoopHVACSupplyPath]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:ZoneMixer"]) -> IDFCollection[AirLoopHVACZoneMixer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:ReturnPlenum"]) -> IDFCollection[AirLoopHVACReturnPlenum]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:ReturnPath"]) -> IDFCollection[AirLoopHVACReturnPath]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ExhaustSystem"]
    ) -> IDFCollection[AirLoopHVACExhaustSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:DedicatedOutdoorAirSystem"]
    ) -> IDFCollection[AirLoopHVACDedicatedOutdoorAirSystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:Mixer"]) -> IDFCollection[AirLoopHVACMixer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:Splitter"]) -> IDFCollection[AirLoopHVACSplitter]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Branch"]) -> IDFCollection[Branch]: ...
    @overload
    def __getitem__(self, obj_type: Literal["BranchList"]) -> IDFCollection[BranchList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Connector:Splitter"]) -> IDFCollection[ConnectorSplitter]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Connector:Mixer"]) -> IDFCollection[ConnectorMixer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ConnectorList"]) -> IDFCollection[ConnectorList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["NodeList"]) -> IDFCollection[NodeList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:Node"]) -> IDFCollection[OutdoorAirNode]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:NodeList"]) -> IDFCollection[OutdoorAirNodeList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Adiabatic"]) -> IDFCollection[PipeAdiabatic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Adiabatic:Steam"]) -> IDFCollection[PipeAdiabaticSteam]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Indoor"]) -> IDFCollection[PipeIndoor]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Outdoor"]) -> IDFCollection[PipeOutdoor]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Underground"]) -> IDFCollection[PipeUnderground]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:Domain"]
    ) -> IDFCollection[PipingSystemUndergroundDomain]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:PipeCircuit"]
    ) -> IDFCollection[PipingSystemUndergroundPipeCircuit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:PipeSegment"]
    ) -> IDFCollection[PipingSystemUndergroundPipeSegment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct"]) -> IDFCollection[Duct]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pump:VariableSpeed"]) -> IDFCollection[PumpVariableSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pump:ConstantSpeed"]) -> IDFCollection[PumpConstantSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Pump:VariableSpeed:Condensate"]
    ) -> IDFCollection[PumpVariableSpeedCondensate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeaderedPumps:ConstantSpeed"]
    ) -> IDFCollection[HeaderedPumpsConstantSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeaderedPumps:VariableSpeed"]
    ) -> IDFCollection[HeaderedPumpsVariableSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["TemperingValve"]) -> IDFCollection[TemperingValve]: ...
    @overload
    def __getitem__(self, obj_type: Literal["LoadProfile:Plant"]) -> IDFCollection[LoadProfilePlant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:FlatPlate"]
    ) -> IDFCollection[SolarCollectorPerformanceFlatPlate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:FlatPlate:Water"]
    ) -> IDFCollection[SolarCollectorFlatPlateWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:FlatPlate:PhotovoltaicThermal"]
    ) -> IDFCollection[SolarCollectorFlatPlatePhotovoltaicThermal]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:PhotovoltaicThermal:Simple"]
    ) -> IDFCollection[SolarCollectorPerformancePhotovoltaicThermalSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:PhotovoltaicThermal:BIPVT"]
    ) -> IDFCollection[SolarCollectorPerformancePhotovoltaicThermalBIPVT]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:IntegralCollectorStorage"]
    ) -> IDFCollection[SolarCollectorIntegralCollectorStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:IntegralCollectorStorage"]
    ) -> IDFCollection[SolarCollectorPerformanceIntegralCollectorStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:UnglazedTranspired"]
    ) -> IDFCollection[SolarCollectorUnglazedTranspired]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:UnglazedTranspired:Multisystem"]
    ) -> IDFCollection[SolarCollectorUnglazedTranspiredMultisystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Boiler:HotWater"]) -> IDFCollection[BoilerHotWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Boiler:Steam"]) -> IDFCollection[BoilerSteam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Electric:ASHRAE205"]
    ) -> IDFCollection[ChillerElectricASHRAE205]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:Electric:EIR"]) -> IDFCollection[ChillerElectricEIR]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Electric:ReformulatedEIR"]
    ) -> IDFCollection[ChillerElectricReformulatedEIR]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:Electric"]) -> IDFCollection[ChillerElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Absorption:Indirect"]
    ) -> IDFCollection[ChillerAbsorptionIndirect]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:Absorption"]) -> IDFCollection[ChillerAbsorption]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:ConstantCOP"]) -> IDFCollection[ChillerConstantCOP]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:EngineDriven"]) -> IDFCollection[ChillerEngineDriven]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:CombustionTurbine"]
    ) -> IDFCollection[ChillerCombustionTurbine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeater:Absorption:DirectFired"]
    ) -> IDFCollection[ChillerHeaterAbsorptionDirectFired]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeater:Absorption:DoubleEffect"]
    ) -> IDFCollection[ChillerHeaterAbsorptionDoubleEffect]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:PlantLoop:EIR:Cooling"]
    ) -> IDFCollection[HeatPumpPlantLoopEIRCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:PlantLoop:EIR:Heating"]
    ) -> IDFCollection[HeatPumpPlantLoopEIRHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:AirToWater:FuelFired:Heating"]
    ) -> IDFCollection[HeatPumpAirToWaterFuelFiredHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:AirToWater:FuelFired:Cooling"]
    ) -> IDFCollection[HeatPumpAirToWaterFuelFiredCooling]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HeatPump:AirToWater"]) -> IDFCollection[HeatPumpAirToWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:EquationFit:Heating"]
    ) -> IDFCollection[HeatPumpWaterToWaterEquationFitHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:EquationFit:Cooling"]
    ) -> IDFCollection[HeatPumpWaterToWaterEquationFitCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:ParameterEstimation:Cooling"]
    ) -> IDFCollection[HeatPumpWaterToWaterParameterEstimationCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:ParameterEstimation:Heating"]
    ) -> IDFCollection[HeatPumpWaterToWaterParameterEstimationHeating]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DistrictCooling"]) -> IDFCollection[DistrictCooling]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DistrictHeating:Water"]) -> IDFCollection[DistrictHeatingWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DistrictHeating:Steam"]) -> IDFCollection[DistrictHeatingSteam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantComponent:TemperatureSource"]
    ) -> IDFCollection[PlantComponentTemperatureSource]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CentralHeatPumpSystem"]) -> IDFCollection[CentralHeatPumpSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeaterPerformance:Electric:EIR"]
    ) -> IDFCollection[ChillerHeaterPerformanceElectricEIR]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoolingTower:SingleSpeed"]) -> IDFCollection[CoolingTowerSingleSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoolingTower:TwoSpeed"]) -> IDFCollection[CoolingTowerTwoSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:VariableSpeed:Merkel"]
    ) -> IDFCollection[CoolingTowerVariableSpeedMerkel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:VariableSpeed"]
    ) -> IDFCollection[CoolingTowerVariableSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTowerPerformance:CoolTools"]
    ) -> IDFCollection[CoolingTowerPerformanceCoolTools]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTowerPerformance:YorkCalc"]
    ) -> IDFCollection[CoolingTowerPerformanceYorkCalc]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeFluidCooler:SingleSpeed"]
    ) -> IDFCollection[EvaporativeFluidCoolerSingleSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeFluidCooler:TwoSpeed"]
    ) -> IDFCollection[EvaporativeFluidCoolerTwoSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FluidCooler:SingleSpeed"]) -> IDFCollection[FluidCoolerSingleSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FluidCooler:TwoSpeed"]) -> IDFCollection[FluidCoolerTwoSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:System"]
    ) -> IDFCollection[GroundHeatExchangerSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Sizing:Rectangle"]
    ) -> IDFCollection[GroundHeatExchangerVerticalSizingRectangle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Properties"]
    ) -> IDFCollection[GroundHeatExchangerVerticalProperties]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Array"]
    ) -> IDFCollection[GroundHeatExchangerVerticalArray]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Single"]
    ) -> IDFCollection[GroundHeatExchangerVerticalSingle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:ResponseFactors"]
    ) -> IDFCollection[GroundHeatExchangerResponseFactors]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GroundHeatExchanger:Pond"]) -> IDFCollection[GroundHeatExchangerPond]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Surface"]
    ) -> IDFCollection[GroundHeatExchangerSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:HorizontalTrench"]
    ) -> IDFCollection[GroundHeatExchangerHorizontalTrench]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Slinky"]
    ) -> IDFCollection[GroundHeatExchangerSlinky]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:FluidToFluid"]
    ) -> IDFCollection[HeatExchangerFluidToFluid]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterHeater:Mixed"]) -> IDFCollection[WaterHeaterMixed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterHeater:Stratified"]) -> IDFCollection[WaterHeaterStratified]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterHeater:Sizing"]) -> IDFCollection[WaterHeaterSizing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:HeatPump:PumpedCondenser"]
    ) -> IDFCollection[WaterHeaterHeatPumpPumpedCondenser]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:HeatPump:WrappedCondenser"]
    ) -> IDFCollection[WaterHeaterHeatPumpWrappedCondenser]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ThermalStorage:Ice:Simple"]) -> IDFCollection[ThermalStorageIceSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:Ice:Detailed"]
    ) -> IDFCollection[ThermalStorageIceDetailed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:ChilledWater:Mixed"]
    ) -> IDFCollection[ThermalStorageChilledWaterMixed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:ChilledWater:Stratified"]
    ) -> IDFCollection[ThermalStorageChilledWaterStratified]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:HotWater:Stratified"]
    ) -> IDFCollection[ThermalStorageHotWaterStratified]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ThermalStorage:PCM"]) -> IDFCollection[ThermalStoragePCM]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ThermalStorage:Sizing"]) -> IDFCollection[ThermalStorageSizing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PlantLoop"]) -> IDFCollection[PlantLoop]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CondenserLoop"]) -> IDFCollection[CondenserLoop]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PlantEquipmentList"]) -> IDFCollection[PlantEquipmentList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CondenserEquipmentList"]) -> IDFCollection[CondenserEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:Uncontrolled"]
    ) -> IDFCollection[PlantEquipmentOperationUncontrolled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:CoolingLoad"]
    ) -> IDFCollection[PlantEquipmentOperationCoolingLoad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:HeatingLoad"]
    ) -> IDFCollection[PlantEquipmentOperationHeatingLoad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDryBulb"]
    ) -> IDFCollection[PlantEquipmentOperationOutdoorDryBulb]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorWetBulb"]
    ) -> IDFCollection[PlantEquipmentOperationOutdoorWetBulb]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorRelativeHumidity"]
    ) -> IDFCollection[PlantEquipmentOperationOutdoorRelativeHumidity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDewpoint"]
    ) -> IDFCollection[PlantEquipmentOperationOutdoorDewpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:ComponentSetpoint"]
    ) -> IDFCollection[PlantEquipmentOperationComponentSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:ThermalEnergyStorage"]
    ) -> IDFCollection[PlantEquipmentOperationThermalEnergyStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDryBulbDifference"]
    ) -> IDFCollection[PlantEquipmentOperationOutdoorDryBulbDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorWetBulbDifference"]
    ) -> IDFCollection[PlantEquipmentOperationOutdoorWetBulbDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDewpointDifference"]
    ) -> IDFCollection[PlantEquipmentOperationOutdoorDewpointDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:ChillerHeaterChangeover"]
    ) -> IDFCollection[PlantEquipmentOperationChillerHeaterChangeover]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperationSchemes"]
    ) -> IDFCollection[PlantEquipmentOperationSchemes]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CondenserEquipmentOperationSchemes"]
    ) -> IDFCollection[CondenserEquipmentOperationSchemes]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Sensor"]
    ) -> IDFCollection[EnergyManagementSystemSensor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Actuator"]
    ) -> IDFCollection[EnergyManagementSystemActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:ProgramCallingManager"]
    ) -> IDFCollection[EnergyManagementSystemProgramCallingManager]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Program"]
    ) -> IDFCollection[EnergyManagementSystemProgram]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Subroutine"]
    ) -> IDFCollection[EnergyManagementSystemSubroutine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:GlobalVariable"]
    ) -> IDFCollection[EnergyManagementSystemGlobalVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:OutputVariable"]
    ) -> IDFCollection[EnergyManagementSystemOutputVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:MeteredOutputVariable"]
    ) -> IDFCollection[EnergyManagementSystemMeteredOutputVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:TrendVariable"]
    ) -> IDFCollection[EnergyManagementSystemTrendVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:InternalVariable"]
    ) -> IDFCollection[EnergyManagementSystemInternalVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:CurveOrTableIndexVariable"]
    ) -> IDFCollection[EnergyManagementSystemCurveOrTableIndexVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:ConstructionIndexVariable"]
    ) -> IDFCollection[EnergyManagementSystemConstructionIndexVariable]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ExternalInterface"]) -> IDFCollection[ExternalInterface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Schedule"]
    ) -> IDFCollection[ExternalInterfaceSchedule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Variable"]
    ) -> IDFCollection[ExternalInterfaceVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Actuator"]
    ) -> IDFCollection[ExternalInterfaceActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImport]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:From:Variable"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImportFromVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Schedule"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImportToSchedule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Actuator"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImportToActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Variable"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImportToVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:From:Variable"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitExportFromVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Schedule"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitExportToSchedule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Actuator"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitExportToActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Variable"]
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitExportToVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:ForcedAir:UserDefined"]
    ) -> IDFCollection[ZoneHVACForcedAirUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:UserDefined"]
    ) -> IDFCollection[AirTerminalSingleDuctUserDefined]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:UserDefined"]) -> IDFCollection[CoilUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantComponent:UserDefined"]
    ) -> IDFCollection[PlantComponentUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:UserDefined"]
    ) -> IDFCollection[PlantEquipmentOperationUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:Scheduled"]
    ) -> IDFCollection[AvailabilityManagerScheduled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:ScheduledOn"]
    ) -> IDFCollection[AvailabilityManagerScheduledOn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:ScheduledOff"]
    ) -> IDFCollection[AvailabilityManagerScheduledOff]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:OptimumStart"]
    ) -> IDFCollection[AvailabilityManagerOptimumStart]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:NightCycle"]
    ) -> IDFCollection[AvailabilityManagerNightCycle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:DifferentialThermostat"]
    ) -> IDFCollection[AvailabilityManagerDifferentialThermostat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HighTemperatureTurnOff"]
    ) -> IDFCollection[AvailabilityManagerHighTemperatureTurnOff]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HighTemperatureTurnOn"]
    ) -> IDFCollection[AvailabilityManagerHighTemperatureTurnOn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:LowTemperatureTurnOff"]
    ) -> IDFCollection[AvailabilityManagerLowTemperatureTurnOff]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:LowTemperatureTurnOn"]
    ) -> IDFCollection[AvailabilityManagerLowTemperatureTurnOn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:NightVentilation"]
    ) -> IDFCollection[AvailabilityManagerNightVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HybridVentilation"]
    ) -> IDFCollection[AvailabilityManagerHybridVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManagerAssignmentList"]
    ) -> IDFCollection[AvailabilityManagerAssignmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Scheduled"]
    ) -> IDFCollection[SetpointManagerScheduled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Scheduled:DualSetpoint"]
    ) -> IDFCollection[SetpointManagerScheduledDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:OutdoorAirReset"]
    ) -> IDFCollection[SetpointManagerOutdoorAirReset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Reheat"]
    ) -> IDFCollection[SetpointManagerSingleZoneReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Heating"]
    ) -> IDFCollection[SetpointManagerSingleZoneHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Cooling"]
    ) -> IDFCollection[SetpointManagerSingleZoneCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Humidity:Minimum"]
    ) -> IDFCollection[SetpointManagerSingleZoneHumidityMinimum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Humidity:Maximum"]
    ) -> IDFCollection[SetpointManagerSingleZoneHumidityMaximum]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SetpointManager:MixedAir"]) -> IDFCollection[SetpointManagerMixedAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:OutdoorAirPretreat"]
    ) -> IDFCollection[SetpointManagerOutdoorAirPretreat]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SetpointManager:Warmest"]) -> IDFCollection[SetpointManagerWarmest]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SetpointManager:Coldest"]) -> IDFCollection[SetpointManagerColdest]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnAirBypassFlow"]
    ) -> IDFCollection[SetpointManagerReturnAirBypassFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:WarmestTemperatureFlow"]
    ) -> IDFCollection[SetpointManagerWarmestTemperatureFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Heating:Average"]
    ) -> IDFCollection[SetpointManagerMultiZoneHeatingAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Cooling:Average"]
    ) -> IDFCollection[SetpointManagerMultiZoneCoolingAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:MinimumHumidity:Average"]
    ) -> IDFCollection[SetpointManagerMultiZoneMinimumHumidityAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:MaximumHumidity:Average"]
    ) -> IDFCollection[SetpointManagerMultiZoneMaximumHumidityAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Humidity:Minimum"]
    ) -> IDFCollection[SetpointManagerMultiZoneHumidityMinimum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Humidity:Maximum"]
    ) -> IDFCollection[SetpointManagerMultiZoneHumidityMaximum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowOutdoorAirTemperature"]
    ) -> IDFCollection[SetpointManagerFollowOutdoorAirTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowSystemNodeTemperature"]
    ) -> IDFCollection[SetpointManagerFollowSystemNodeTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowGroundTemperature"]
    ) -> IDFCollection[SetpointManagerFollowGroundTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:CondenserEnteringReset"]
    ) -> IDFCollection[SetpointManagerCondenserEnteringReset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:CondenserEnteringReset:Ideal"]
    ) -> IDFCollection[SetpointManagerCondenserEnteringResetIdeal]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:OneStageCooling"]
    ) -> IDFCollection[SetpointManagerSingleZoneOneStageCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:OneStageHeating"]
    ) -> IDFCollection[SetpointManagerSingleZoneOneStageHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnTemperature:ChilledWater"]
    ) -> IDFCollection[SetpointManagerReturnTemperatureChilledWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnTemperature:HotWater"]
    ) -> IDFCollection[SetpointManagerReturnTemperatureHotWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SystemNodeReset:Temperature"]
    ) -> IDFCollection[SetpointManagerSystemNodeResetTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SystemNodeReset:Humidity"]
    ) -> IDFCollection[SetpointManagerSystemNodeResetHumidity]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:Case"]) -> IDFCollection[RefrigerationCase]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CompressorRack"]
    ) -> IDFCollection[RefrigerationCompressorRack]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CaseAndWalkInList"]
    ) -> IDFCollection[RefrigerationCaseAndWalkInList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:AirCooled"]
    ) -> IDFCollection[RefrigerationCondenserAirCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:EvaporativeCooled"]
    ) -> IDFCollection[RefrigerationCondenserEvaporativeCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:WaterCooled"]
    ) -> IDFCollection[RefrigerationCondenserWaterCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:Cascade"]
    ) -> IDFCollection[RefrigerationCondenserCascade]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:GasCooler:AirCooled"]
    ) -> IDFCollection[RefrigerationGasCoolerAirCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:TransferLoadList"]
    ) -> IDFCollection[RefrigerationTransferLoadList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:Subcooler"]) -> IDFCollection[RefrigerationSubcooler]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:Compressor"]) -> IDFCollection[RefrigerationCompressor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CompressorList"]
    ) -> IDFCollection[RefrigerationCompressorList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:System"]) -> IDFCollection[RefrigerationSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:TranscriticalSystem"]
    ) -> IDFCollection[RefrigerationTranscriticalSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:SecondarySystem"]
    ) -> IDFCollection[RefrigerationSecondarySystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:WalkIn"]) -> IDFCollection[RefrigerationWalkIn]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:AirChiller"]) -> IDFCollection[RefrigerationAirChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:RefrigerationChillerSet"]
    ) -> IDFCollection[ZoneHVACRefrigerationChillerSet]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManagerAssignmentList"]
    ) -> IDFCollection[DemandManagerAssignmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:ExteriorLights"]
    ) -> IDFCollection[DemandManagerExteriorLights]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DemandManager:Lights"]) -> IDFCollection[DemandManagerLights]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:ElectricEquipment"]
    ) -> IDFCollection[DemandManagerElectricEquipment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:Thermostats"]
    ) -> IDFCollection[DemandManagerThermostats]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:Ventilation"]
    ) -> IDFCollection[DemandManagerVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:InternalCombustionEngine"]
    ) -> IDFCollection[GeneratorInternalCombustionEngine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:CombustionTurbine"]
    ) -> IDFCollection[GeneratorCombustionTurbine]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:MicroTurbine"]) -> IDFCollection[GeneratorMicroTurbine]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:Photovoltaic"]) -> IDFCollection[GeneratorPhotovoltaic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:Simple"]
    ) -> IDFCollection[PhotovoltaicPerformanceSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:EquivalentOne-Diode"]
    ) -> IDFCollection[PhotovoltaicPerformanceEquivalentOneDiode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:Sandia"]
    ) -> IDFCollection[PhotovoltaicPerformanceSandia]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:PVWatts"]) -> IDFCollection[GeneratorPVWatts]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:PVWatts"]
    ) -> IDFCollection[ElectricLoadCenterInverterPVWatts]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:FuelCell"]) -> IDFCollection[GeneratorFuelCell]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:PowerModule"]
    ) -> IDFCollection[GeneratorFuelCellPowerModule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:AirSupply"]
    ) -> IDFCollection[GeneratorFuelCellAirSupply]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:WaterSupply"]
    ) -> IDFCollection[GeneratorFuelCellWaterSupply]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:AuxiliaryHeater"]
    ) -> IDFCollection[GeneratorFuelCellAuxiliaryHeater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:ExhaustGasToWaterHeatExchanger"]
    ) -> IDFCollection[GeneratorFuelCellExhaustGasToWaterHeatExchanger]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:ElectricalStorage"]
    ) -> IDFCollection[GeneratorFuelCellElectricalStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:Inverter"]
    ) -> IDFCollection[GeneratorFuelCellInverter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:StackCooler"]
    ) -> IDFCollection[GeneratorFuelCellStackCooler]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:MicroCHP"]) -> IDFCollection[GeneratorMicroCHP]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:MicroCHP:NonNormalizedParameters"]
    ) -> IDFCollection[GeneratorMicroCHPNonNormalizedParameters]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:FuelSupply"]) -> IDFCollection[GeneratorFuelSupply]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:WindTurbine"]) -> IDFCollection[GeneratorWindTurbine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Generators"]
    ) -> IDFCollection[ElectricLoadCenterGenerators]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:Simple"]
    ) -> IDFCollection[ElectricLoadCenterInverterSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:FunctionOfPower"]
    ) -> IDFCollection[ElectricLoadCenterInverterFunctionOfPower]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:LookUpTable"]
    ) -> IDFCollection[ElectricLoadCenterInverterLookUpTable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Simple"]
    ) -> IDFCollection[ElectricLoadCenterStorageSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Battery"]
    ) -> IDFCollection[ElectricLoadCenterStorageBattery]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:LiIonNMCBattery"]
    ) -> IDFCollection[ElectricLoadCenterStorageLiIonNMCBattery]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Transformer"]
    ) -> IDFCollection[ElectricLoadCenterTransformer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Distribution"]
    ) -> IDFCollection[ElectricLoadCenterDistribution]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Converter"]
    ) -> IDFCollection[ElectricLoadCenterStorageConverter]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Equipment"]) -> IDFCollection[WaterUseEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Connections"]) -> IDFCollection[WaterUseConnections]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Storage"]) -> IDFCollection[WaterUseStorage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Well"]) -> IDFCollection[WaterUseWell]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:RainCollector"]) -> IDFCollection[WaterUseRainCollector]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:OutdoorAir"]
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:HumiditySensorOffset:OutdoorAir"]
    ) -> IDFCollection[FaultModelHumiditySensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:EnthalpySensorOffset:OutdoorAir"]
    ) -> IDFCollection[FaultModelEnthalpySensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:ReturnAir"]
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetReturnAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:EnthalpySensorOffset:ReturnAir"]
    ) -> IDFCollection[FaultModelEnthalpySensorOffsetReturnAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:ChillerSupplyWater"]
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetChillerSupplyWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:CoilSupplyAir"]
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetCoilSupplyAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:CondenserSupplyWater"]
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetCondenserSupplyWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:ThermostatOffset"]
    ) -> IDFCollection[FaultModelThermostatOffset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:HumidistatOffset"]
    ) -> IDFCollection[FaultModelHumidistatOffset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:AirFilter"]
    ) -> IDFCollection[FaultModelFoulingAirFilter]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FaultModel:Fouling:Boiler"]) -> IDFCollection[FaultModelFoulingBoiler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:EvaporativeCooler"]
    ) -> IDFCollection[FaultModelFoulingEvaporativeCooler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:Chiller"]
    ) -> IDFCollection[FaultModelFoulingChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:CoolingTower"]
    ) -> IDFCollection[FaultModelFoulingCoolingTower]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FaultModel:Fouling:Coil"]) -> IDFCollection[FaultModelFoulingCoil]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Matrix:TwoDimension"]) -> IDFCollection[MatrixTwoDimension]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HybridModel:Zone"]) -> IDFCollection[HybridModelZone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Linear"]) -> IDFCollection[CurveLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:QuadLinear"]) -> IDFCollection[CurveQuadLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:QuintLinear"]) -> IDFCollection[CurveQuintLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Quadratic"]) -> IDFCollection[CurveQuadratic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Cubic"]) -> IDFCollection[CurveCubic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Quartic"]) -> IDFCollection[CurveQuartic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Exponent"]) -> IDFCollection[CurveExponent]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Bicubic"]) -> IDFCollection[CurveBicubic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Biquadratic"]) -> IDFCollection[CurveBiquadratic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:QuadraticLinear"]) -> IDFCollection[CurveQuadraticLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:CubicLinear"]) -> IDFCollection[CurveCubicLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Triquadratic"]) -> IDFCollection[CurveTriquadratic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:Functional:PressureDrop"]
    ) -> IDFCollection[CurveFunctionalPressureDrop]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:FanPressureRise"]) -> IDFCollection[CurveFanPressureRise]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:ExponentialSkewNormal"]
    ) -> IDFCollection[CurveExponentialSkewNormal]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Sigmoid"]) -> IDFCollection[CurveSigmoid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:RectangularHyperbola1"]
    ) -> IDFCollection[CurveRectangularHyperbola1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:RectangularHyperbola2"]
    ) -> IDFCollection[CurveRectangularHyperbola2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:ExponentialDecay"]) -> IDFCollection[CurveExponentialDecay]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:DoubleExponentialDecay"]
    ) -> IDFCollection[CurveDoubleExponentialDecay]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:ChillerPartLoadWithLift"]
    ) -> IDFCollection[CurveChillerPartLoadWithLift]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Table:IndependentVariable"]
    ) -> IDFCollection[TableIndependentVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Table:IndependentVariableList"]
    ) -> IDFCollection[TableIndependentVariableList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Table:Lookup"]) -> IDFCollection[TableLookup]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FluidProperties:Name"]) -> IDFCollection[FluidPropertiesName]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:GlycolConcentration"]
    ) -> IDFCollection[FluidPropertiesGlycolConcentration]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Temperatures"]
    ) -> IDFCollection[FluidPropertiesTemperatures]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Saturated"]
    ) -> IDFCollection[FluidPropertiesSaturated]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Superheated"]
    ) -> IDFCollection[FluidPropertiesSuperheated]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Concentration"]
    ) -> IDFCollection[FluidPropertiesConcentration]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CurrencyType"]) -> IDFCollection[CurrencyType]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComponentCost:Adjustments"]
    ) -> IDFCollection[ComponentCostAdjustments]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ComponentCost:Reference"]) -> IDFCollection[ComponentCostReference]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ComponentCost:LineItem"]) -> IDFCollection[ComponentCostLineItem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Tariff"]) -> IDFCollection[UtilityCostTariff]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Qualify"]) -> IDFCollection[UtilityCostQualify]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Charge:Simple"]) -> IDFCollection[UtilityCostChargeSimple]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Charge:Block"]) -> IDFCollection[UtilityCostChargeBlock]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Ratchet"]) -> IDFCollection[UtilityCostRatchet]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Variable"]) -> IDFCollection[UtilityCostVariable]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Computation"]) -> IDFCollection[UtilityCostComputation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["LifeCycleCost:Parameters"]) -> IDFCollection[LifeCycleCostParameters]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:RecurringCosts"]
    ) -> IDFCollection[LifeCycleCostRecurringCosts]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:NonrecurringCost"]
    ) -> IDFCollection[LifeCycleCostNonrecurringCost]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:UsePriceEscalation"]
    ) -> IDFCollection[LifeCycleCostUsePriceEscalation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:UseAdjustment"]
    ) -> IDFCollection[LifeCycleCostUseAdjustment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Parametric:SetValueForRun"]
    ) -> IDFCollection[ParametricSetValueForRun]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Parametric:Logic"]) -> IDFCollection[ParametricLogic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Parametric:RunControl"]) -> IDFCollection[ParametricRunControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Parametric:FileNameSuffix"]
    ) -> IDFCollection[ParametricFileNameSuffix]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:VariableDictionary"]
    ) -> IDFCollection[OutputVariableDictionary]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Surfaces:List"]) -> IDFCollection[OutputSurfacesList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Surfaces:Drawing"]) -> IDFCollection[OutputSurfacesDrawing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Schedules"]) -> IDFCollection[OutputSchedules]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Constructions"]) -> IDFCollection[OutputConstructions]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:EnergyManagementSystem"]
    ) -> IDFCollection[OutputEnergyManagementSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:SurfaceColorScheme"]
    ) -> IDFCollection[OutputControlSurfaceColorScheme]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Table:SummaryReports"]
    ) -> IDFCollection[OutputTableSummaryReports]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Table:TimeBins"]) -> IDFCollection[OutputTableTimeBins]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Table:Monthly"]) -> IDFCollection[OutputTableMonthly]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Table:Annual"]) -> IDFCollection[OutputTableAnnual]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Table:ReportPeriod"]) -> IDFCollection[OutputTableReportPeriod]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutputControl:Table:Style"]) -> IDFCollection[OutputControlTableStyle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:ReportingTolerances"]
    ) -> IDFCollection[OutputControlReportingTolerances]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:ResilienceSummaries"]
    ) -> IDFCollection[OutputControlResilienceSummaries]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Variable"]) -> IDFCollection[OutputVariable]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Meter"]) -> IDFCollection[OutputMeter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Meter:MeterFileOnly"]
    ) -> IDFCollection[OutputMeterMeterFileOnly]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Meter:Cumulative"]) -> IDFCollection[OutputMeterCumulative]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Meter:Cumulative:MeterFileOnly"]
    ) -> IDFCollection[OutputMeterCumulativeMeterFileOnly]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Meter:Custom"]) -> IDFCollection[MeterCustom]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Meter:CustomDecrement"]) -> IDFCollection[MeterCustomDecrement]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutputControl:Files"]) -> IDFCollection[OutputControlFiles]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutputControl:Timestamp"]) -> IDFCollection[OutputControlTimestamp]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:JSON"]) -> IDFCollection[OutputJSON]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:SQLite"]) -> IDFCollection[OutputSQLite]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:EnvironmentalImpactFactors"]
    ) -> IDFCollection[OutputEnvironmentalImpactFactors]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnvironmentalImpactFactors"]
    ) -> IDFCollection[EnvironmentalImpactFactors]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FuelFactors"]) -> IDFCollection[FuelFactors]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Diagnostics"]) -> IDFCollection[OutputDiagnostics]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:DebuggingData"]) -> IDFCollection[OutputDebuggingData]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:PreprocessorMessage"]
    ) -> IDFCollection[OutputPreprocessorMessage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PythonPlugin:SearchPaths"]) -> IDFCollection[PythonPluginSearchPaths]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PythonPlugin:Instance"]) -> IDFCollection[PythonPluginInstance]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PythonPlugin:Variables"]) -> IDFCollection[PythonPluginVariables]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PythonPlugin:TrendVariable"]
    ) -> IDFCollection[PythonPluginTrendVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PythonPlugin:OutputVariable"]
    ) -> IDFCollection[PythonPluginOutputVariable]: ...
    @overload
    def __getitem__(self, obj_type: str) -> IDFCollection[IDFObject]: ...
    def __getitem__(self, obj_type: str) -> IDFCollection[IDFObject]: ...
    def __getattr__(self, name: str) -> IDFCollection[IDFObject]: ...
    def __contains__(self, obj_type: str) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def keys(self) -> list[str]: ...
    def values(self) -> list[IDFCollection[IDFObject]]: ...
    def items(self) -> list[tuple[str, IDFCollection[IDFObject]]]: ...
    def describe(self, obj_type: str) -> ObjectDescription: ...
    @overload
    def add(
        self,
        obj_type: Literal["Version"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Version: ...
    @overload
    def add(
        self,
        obj_type: Literal["SimulationControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SimulationControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["PerformancePrecisionTradeoffs"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PerformancePrecisionTradeoffs: ...
    @overload
    def add(
        self,
        obj_type: Literal["Building"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Building: ...
    @overload
    def add(
        self,
        obj_type: Literal["ShadowCalculation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadowCalculation: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceConvectionAlgorithm:Inside"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceConvectionAlgorithmInside: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceConvectionAlgorithm:Outside"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceConvectionAlgorithmOutside: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatBalanceAlgorithm"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatBalanceAlgorithm: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatBalanceSettings:ConductionFiniteDifference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatBalanceSettingsConductionFiniteDifference: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneAirHeatBalanceAlgorithm"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneAirHeatBalanceAlgorithm: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneAirContaminantBalance"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneAirContaminantBalance: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneAirMassFlowConservation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneAirMassFlowConservation: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneCapacitanceMultiplier:ResearchSpecial"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneCapacitanceMultiplierResearchSpecial: ...
    @overload
    def add(
        self,
        obj_type: Literal["Timestep"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Timestep: ...
    @overload
    def add(
        self,
        obj_type: Literal["ConvergenceLimits"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConvergenceLimits: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACSystemRootFindingAlgorithm"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACSystemRootFindingAlgorithm: ...
    @overload
    def add(
        self,
        obj_type: Literal["Compliance:Building"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ComplianceBuilding: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:Location"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteLocation: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:VariableLocation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteVariableLocation: ...
    @overload
    def add(
        self,
        obj_type: Literal["SizingPeriod:DesignDay"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SizingPeriodDesignDay: ...
    @overload
    def add(
        self,
        obj_type: Literal["SizingPeriod:WeatherFileDays"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SizingPeriodWeatherFileDays: ...
    @overload
    def add(
        self,
        obj_type: Literal["SizingPeriod:WeatherFileConditionType"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SizingPeriodWeatherFileConditionType: ...
    @overload
    def add(
        self,
        obj_type: Literal["RunPeriod"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RunPeriod: ...
    @overload
    def add(
        self,
        obj_type: Literal["RunPeriodControl:SpecialDays"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RunPeriodControlSpecialDays: ...
    @overload
    def add(
        self,
        obj_type: Literal["RunPeriodControl:DaylightSavingTime"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RunPeriodControlDaylightSavingTime: ...
    @overload
    def add(
        self,
        obj_type: Literal["WeatherProperty:SkyTemperature"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WeatherPropertySkyTemperature: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:WeatherStation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteWeatherStation: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:HeightVariation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteHeightVariation: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundTemperature:BuildingSurface"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundTemperatureBuildingSurface: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundTemperature:FCfactorMethod"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundTemperatureFCfactorMethod: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundTemperature:Shallow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundTemperatureShallow: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundTemperature:Deep"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundTemperatureDeep: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundTemperature:Undisturbed:FiniteDifference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundTemperatureUndisturbedFiniteDifference: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundTemperature:Undisturbed:KusudaAchenbach"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundTemperatureUndisturbedKusudaAchenbach: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundTemperature:Undisturbed:Xing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundTemperatureUndisturbedXing: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundDomain:Slab"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundDomainSlab: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundDomain:Basement"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundDomainBasement: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundReflectance"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundReflectance: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:GroundReflectance:SnowModifier"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteGroundReflectanceSnowModifier: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:WaterMainsTemperature"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteWaterMainsTemperature: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:Precipitation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SitePrecipitation: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoofIrrigation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoofIrrigation: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:SolarAndVisibleSpectrum"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteSolarAndVisibleSpectrum: ...
    @overload
    def add(
        self,
        obj_type: Literal["Site:SpectrumData"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SiteSpectrumData: ...
    @overload
    def add(
        self,
        obj_type: Literal["ScheduleTypeLimits"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleTypeLimits: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:Day:Hourly"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleDayHourly: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:Day:Interval"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleDayInterval: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:Day:List"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleDayList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:Week:Daily"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleWeekDaily: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:Week:Compact"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleWeekCompact: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:Year"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleYear: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:Compact"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleCompact: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:Constant"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleConstant: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:File:Shading"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleFileShading: ...
    @overload
    def add(
        self,
        obj_type: Literal["Schedule:File"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ScheduleFile: ...
    @overload
    def add(
        self,
        obj_type: Literal["Material"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Material: ...
    @overload
    def add(
        self,
        obj_type: Literal["Material:NoMass"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialNoMass: ...
    @overload
    def add(
        self,
        obj_type: Literal["Material:InfraredTransparent"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialInfraredTransparent: ...
    @overload
    def add(
        self,
        obj_type: Literal["Material:AirGap"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialAirGap: ...
    @overload
    def add(
        self,
        obj_type: Literal["Material:RoofVegetation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialRoofVegetation: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:SimpleGlazingSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialSimpleGlazingSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Glazing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialGlazing: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:GlazingGroup:Thermochromic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialGlazingGroupThermochromic: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Glazing:RefractionExtinctionMethod"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialGlazingRefractionExtinctionMethod: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Gas"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialGas: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowGap:SupportPillar"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowGapSupportPillar: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowGap:DeflectionState"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowGapDeflectionState: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:GasMixture"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialGasMixture: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Gap"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialGap: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Shade"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialShade: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:ComplexShade"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialComplexShade: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Blind"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialBlind: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Screen"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialScreen: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Shade:EquivalentLayer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialShadeEquivalentLayer: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Drape:EquivalentLayer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialDrapeEquivalentLayer: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Blind:EquivalentLayer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialBlindEquivalentLayer: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Screen:EquivalentLayer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialScreenEquivalentLayer: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Glazing:EquivalentLayer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialGlazingEquivalentLayer: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowMaterial:Gap:EquivalentLayer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowMaterialGapEquivalentLayer: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:MoisturePenetrationDepth:Settings"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyMoisturePenetrationDepthSettings: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:PhaseChange"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyPhaseChange: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:PhaseChangeHysteresis"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyPhaseChangeHysteresis: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:VariableThermalConductivity"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyVariableThermalConductivity: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:VariableAbsorptance"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyVariableAbsorptance: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Settings"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyHeatAndMoistureTransferSettings: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:SorptionIsotherm"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyHeatAndMoistureTransferSorptionIsotherm: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Suction"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyHeatAndMoistureTransferSuction: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Redistribution"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyHeatAndMoistureTransferRedistribution: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Diffusion"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyHeatAndMoistureTransferDiffusion: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:ThermalConductivity"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyHeatAndMoistureTransferThermalConductivity: ...
    @overload
    def add(
        self,
        obj_type: Literal["MaterialProperty:GlazingSpectralData"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MaterialPropertyGlazingSpectralData: ...
    @overload
    def add(
        self,
        obj_type: Literal["Construction"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Construction: ...
    @overload
    def add(
        self,
        obj_type: Literal["Construction:CfactorUndergroundWall"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConstructionCfactorUndergroundWall: ...
    @overload
    def add(
        self,
        obj_type: Literal["Construction:FfactorGroundFloor"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConstructionFfactorGroundFloor: ...
    @overload
    def add(
        self,
        obj_type: Literal["ConstructionProperty:InternalHeatSource"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConstructionPropertyInternalHeatSource: ...
    @overload
    def add(
        self,
        obj_type: Literal["Construction:AirBoundary"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConstructionAirBoundary: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowThermalModel:Params"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowThermalModelParams: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowsCalculationEngine"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowsCalculationEngine: ...
    @overload
    def add(
        self,
        obj_type: Literal["Construction:ComplexFenestrationState"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConstructionComplexFenestrationState: ...
    @overload
    def add(
        self,
        obj_type: Literal["Construction:WindowEquivalentLayer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConstructionWindowEquivalentLayer: ...
    @overload
    def add(
        self,
        obj_type: Literal["Construction:WindowDataFile"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConstructionWindowDataFile: ...
    @overload
    def add(
        self,
        obj_type: Literal["GlobalGeometryRules"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GlobalGeometryRules: ...
    @overload
    def add(
        self,
        obj_type: Literal["GeometryTransform"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeometryTransform: ...
    @overload
    def add(
        self,
        obj_type: Literal["Space"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Space: ...
    @overload
    def add(
        self,
        obj_type: Literal["SpaceList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SpaceList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Zone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Zone: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneList: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneGroup"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneGroup: ...
    @overload
    def add(
        self,
        obj_type: Literal["BuildingSurface:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> BuildingSurfaceDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Wall:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WallDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoofCeiling:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoofCeilingDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Floor:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FloorDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Wall:Exterior"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WallExterior: ...
    @overload
    def add(
        self,
        obj_type: Literal["Wall:Adiabatic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WallAdiabatic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Wall:Underground"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WallUnderground: ...
    @overload
    def add(
        self,
        obj_type: Literal["Wall:Interzone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WallInterzone: ...
    @overload
    def add(
        self,
        obj_type: Literal["Roof"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Roof: ...
    @overload
    def add(
        self,
        obj_type: Literal["Ceiling:Adiabatic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CeilingAdiabatic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Ceiling:Interzone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CeilingInterzone: ...
    @overload
    def add(
        self,
        obj_type: Literal["Floor:GroundContact"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FloorGroundContact: ...
    @overload
    def add(
        self,
        obj_type: Literal["Floor:Adiabatic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FloorAdiabatic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Floor:Interzone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FloorInterzone: ...
    @overload
    def add(
        self,
        obj_type: Literal["FenestrationSurface:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FenestrationSurfaceDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Window"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Window: ...
    @overload
    def add(
        self,
        obj_type: Literal["Door"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Door: ...
    @overload
    def add(
        self,
        obj_type: Literal["GlazedDoor"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GlazedDoor: ...
    @overload
    def add(
        self,
        obj_type: Literal["Window:Interzone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowInterzone: ...
    @overload
    def add(
        self,
        obj_type: Literal["Door:Interzone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DoorInterzone: ...
    @overload
    def add(
        self,
        obj_type: Literal["GlazedDoor:Interzone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GlazedDoorInterzone: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowShadingControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowShadingControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowProperty:FrameAndDivider"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowPropertyFrameAndDivider: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowProperty:AirflowControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowPropertyAirflowControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["WindowProperty:StormWindow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WindowPropertyStormWindow: ...
    @overload
    def add(
        self,
        obj_type: Literal["InternalMass"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> InternalMass: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Site"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingSite: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Building"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingBuilding: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Site:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingSiteDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Building:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingBuildingDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Overhang"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingOverhang: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Overhang:Projection"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingOverhangProjection: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Fin"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingFin: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Fin:Projection"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingFinProjection: ...
    @overload
    def add(
        self,
        obj_type: Literal["Shading:Zone:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingZoneDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["ShadingProperty:Reflectance"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ShadingPropertyReflectance: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyHeatTransferAlgorithm: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:MultipleSurface"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyHeatTransferAlgorithmMultipleSurface: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:SurfaceList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyHeatTransferAlgorithmSurfaceList: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:Construction"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyHeatTransferAlgorithmConstruction: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:HeatBalanceSourceTerm"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyHeatBalanceSourceTerm: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceControl:MovableInsulation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceControlMovableInsulation: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:OtherSideCoefficients"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyOtherSideCoefficients: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:OtherSideConditionsModel"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyOtherSideConditionsModel: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:Underwater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyUnderwater: ...
    @overload
    def add(
        self,
        obj_type: Literal["Foundation:Kiva"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FoundationKiva: ...
    @overload
    def add(
        self,
        obj_type: Literal["Foundation:Kiva:Settings"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FoundationKivaSettings: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:ExposedFoundationPerimeter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyExposedFoundationPerimeter: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceConvectionAlgorithm:Inside:AdaptiveModelSelections"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceConvectionAlgorithmInsideAdaptiveModelSelections: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceConvectionAlgorithm:Outside:AdaptiveModelSelections"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceConvectionAlgorithm:Inside:UserCurve"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceConvectionAlgorithmInsideUserCurve: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceConvectionAlgorithm:Outside:UserCurve"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceConvectionAlgorithmOutsideUserCurve: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:ConvectionCoefficients"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyConvectionCoefficients: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:ConvectionCoefficients:MultipleSurface"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyConvectionCoefficientsMultipleSurface: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperties:VaporCoefficients"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertiesVaporCoefficients: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:ExteriorNaturalVentedCavity"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyExteriorNaturalVentedCavity: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:SolarIncidentInside"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertySolarIncidentInside: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:IncidentSolarMultiplier"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyIncidentSolarMultiplier: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:LocalEnvironment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyLocalEnvironment: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneProperty:LocalEnvironment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZonePropertyLocalEnvironment: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:SurroundingSurfaces"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertySurroundingSurfaces: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceProperty:GroundSurfaces"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfacePropertyGroundSurfaces: ...
    @overload
    def add(
        self,
        obj_type: Literal["ComplexFenestrationProperty:SolarAbsorbedLayers"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ComplexFenestrationPropertySolarAbsorbedLayers: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneProperty:UserViewFactors:BySurfaceName"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZonePropertyUserViewFactorsBySurfaceName: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Control"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:Materials"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabMaterials: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:MatlProps"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabMatlProps: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:BoundConds"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabBoundConds: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:BldgProps"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabBldgProps: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:Insulation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabInsulation: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:EquivalentSlab"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabEquivalentSlab: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:AutoGrid"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabAutoGrid: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:ManualGrid"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabManualGrid: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:XFACE"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabXFACE: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:YFACE"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabYFACE: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Slab:ZFACE"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferSlabZFACE: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:SimParameters"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementSimParameters: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:MatlProps"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementMatlProps: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:Insulation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementInsulation: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:SurfaceProps"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementSurfaceProps: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:BldgData"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementBldgData: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:Interior"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementInterior: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:ComBldg"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementComBldg: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:EquivSlab"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementEquivSlab: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:EquivAutoGrid"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementEquivAutoGrid: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:AutoGrid"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementAutoGrid: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:ManualGrid"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementManualGrid: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:XFACE"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementXFACE: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:YFACE"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementYFACE: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatTransfer:Basement:ZFACE"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatTransferBasementZFACE: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAirModelType"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirModelType: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:TemperaturePattern:UserDefined"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirTemperaturePatternUserDefined: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:TemperaturePattern:ConstantGradient"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirTemperaturePatternConstantGradient: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:TemperaturePattern:TwoGradient"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirTemperaturePatternTwoGradient: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:TemperaturePattern:NondimensionalHeight"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirTemperaturePatternNondimensionalHeight: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:TemperaturePattern:SurfaceMapping"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirTemperaturePatternSurfaceMapping: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:Node"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirNode: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAirSettings:OneNodeDisplacementVentilation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirSettingsOneNodeDisplacementVentilation: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAirSettings:ThreeNodeDisplacementVentilation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirSettingsThreeNodeDisplacementVentilation: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAirSettings:CrossVentilation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirSettingsCrossVentilation: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAirSettings:UnderFloorAirDistributionInterior"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirSettingsUnderFloorAirDistributionInterior: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAirSettings:UnderFloorAirDistributionExterior"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirSettingsUnderFloorAirDistributionExterior: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:Node:AirflowNetwork"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirNodeAirflowNetwork: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:Node:AirflowNetwork:AdjacentSurfaceList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirNodeAirflowNetworkAdjacentSurfaceList: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:Node:AirflowNetwork:InternalGains"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirNodeAirflowNetworkInternalGains: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAir:Node:AirflowNetwork:HVACEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirNodeAirflowNetworkHVACEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["RoomAirSettings:AirflowNetwork"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RoomAirSettingsAirflowNetwork: ...
    @overload
    def add(
        self,
        obj_type: Literal["People"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> People: ...
    @overload
    def add(
        self,
        obj_type: Literal["ComfortViewFactorAngles"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ComfortViewFactorAngles: ...
    @overload
    def add(
        self,
        obj_type: Literal["Lights"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Lights: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["GasEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GasEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["HotWaterEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HotWaterEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["SteamEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SteamEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["OtherEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OtherEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["IndoorLivingWall"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> IndoorLivingWall: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricEquipment:ITE:AirCooled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricEquipmentITEAirCooled: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneBaseboard:OutdoorTemperatureControlled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneBaseboardOutdoorTemperatureControlled: ...
    @overload
    def add(
        self,
        obj_type: Literal["SwimmingPool:Indoor"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SwimmingPoolIndoor: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneContaminantSourceAndSink:CarbonDioxide"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneContaminantSourceAndSinkCarbonDioxide: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneContaminantSourceAndSink:Generic:Constant"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneContaminantSourceAndSinkGenericConstant: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:PressureDriven"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceContaminantSourceAndSinkGenericPressureDriven: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneContaminantSourceAndSink:Generic:CutoffModel"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneContaminantSourceAndSinkGenericCutoffModel: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneContaminantSourceAndSink:Generic:DecaySource"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneContaminantSourceAndSinkGenericDecaySource: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:BoundaryLayerDiffusion"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion: ...
    @overload
    def add(
        self,
        obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:DepositionVelocitySink"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneContaminantSourceAndSink:Generic:DepositionRateSink"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneContaminantSourceAndSinkGenericDepositionRateSink: ...
    @overload
    def add(
        self,
        obj_type: Literal["Daylighting:Controls"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DaylightingControls: ...
    @overload
    def add(
        self,
        obj_type: Literal["Daylighting:ReferencePoint"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DaylightingReferencePoint: ...
    @overload
    def add(
        self,
        obj_type: Literal["Daylighting:DELight:ComplexFenestration"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DaylightingDELightComplexFenestration: ...
    @overload
    def add(
        self,
        obj_type: Literal["DaylightingDevice:Tubular"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DaylightingDeviceTubular: ...
    @overload
    def add(
        self,
        obj_type: Literal["DaylightingDevice:Shelf"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DaylightingDeviceShelf: ...
    @overload
    def add(
        self,
        obj_type: Literal["DaylightingDevice:LightWell"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DaylightingDeviceLightWell: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:DaylightFactors"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputDaylightFactors: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:IlluminanceMap"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputIlluminanceMap: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutputControl:IlluminanceMap:Style"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputControlIlluminanceMapStyle: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneInfiltration:DesignFlowRate"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneInfiltrationDesignFlowRate: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneInfiltration:EffectiveLeakageArea"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneInfiltrationEffectiveLeakageArea: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneInfiltration:FlowCoefficient"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneInfiltrationFlowCoefficient: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneVentilation:DesignFlowRate"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneVentilationDesignFlowRate: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneVentilation:WindandStackOpenArea"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneVentilationWindandStackOpenArea: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneAirBalance:OutdoorAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneAirBalanceOutdoorAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneMixing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneMixing: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneCrossMixing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneCrossMixing: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneRefrigerationDoorMixing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneRefrigerationDoorMixing: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneEarthtube"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneEarthtube: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneEarthtube:Parameters"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneEarthtubeParameters: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneCoolTower:Shower"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneCoolTowerShower: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneThermalChimney"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneThermalChimney: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:SimulationControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkSimulationControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:Zone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneZone: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:Surface"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneSurface: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:ReferenceCrackConditions"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneReferenceCrackConditions: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:Surface:Crack"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneSurfaceCrack: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:Surface:EffectiveLeakageArea"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:SpecifiedFlowRate"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneSpecifiedFlowRate: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:Component:DetailedOpening"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneComponentDetailedOpening: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:Component:SimpleOpening"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneComponentSimpleOpening: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:Component:HorizontalOpening"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneComponentHorizontalOpening: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:Component:ZoneExhaustFan"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneComponentZoneExhaustFan: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:ExternalNode"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneExternalNode: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:WindPressureCoefficientArray"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneWindPressureCoefficientArray: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:MultiZone:WindPressureCoefficientValues"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkMultiZoneWindPressureCoefficientValues: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:ZoneControl:PressureController"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkZoneControlPressureController: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Node"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionNode: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:Leak"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentLeak: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:LeakageRatio"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentLeakageRatio: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:Duct"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentDuct: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:Fan"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentFan: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:Coil"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentCoil: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:HeatExchanger"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentHeatExchanger: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:TerminalUnit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentTerminalUnit: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:ConstantPressureDrop"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentConstantPressureDrop: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:OutdoorAirFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentOutdoorAirFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Component:ReliefAirFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionComponentReliefAirFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:Linkage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionLinkage: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:DuctViewFactors"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionDuctViewFactors: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:Distribution:DuctSizing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkDistributionDuctSizing: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:OccupantVentilationControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkOccupantVentilationControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:IntraZone:Node"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkIntraZoneNode: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirflowNetwork:IntraZone:Linkage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirflowNetworkIntraZoneLinkage: ...
    @overload
    def add(
        self,
        obj_type: Literal["Duct:Loss:Conduction"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DuctLossConduction: ...
    @overload
    def add(
        self,
        obj_type: Literal["Duct:Loss:Leakage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DuctLossLeakage: ...
    @overload
    def add(
        self,
        obj_type: Literal["Duct:Loss:MakeupAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DuctLossMakeupAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["Exterior:Lights"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExteriorLights: ...
    @overload
    def add(
        self,
        obj_type: Literal["Exterior:FuelEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExteriorFuelEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["Exterior:WaterEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExteriorWaterEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Thermostat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateThermostat: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:IdealLoadsAirSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneIdealLoadsAirSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:BaseboardHeat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneBaseboardHeat: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:FanCoil"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneFanCoil: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:PTAC"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZonePTAC: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:PTHP"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZonePTHP: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:WaterToAirHeatPump"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneWaterToAirHeatPump: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:VRF"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneVRF: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:Unitary"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneUnitary: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:VAV"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneVAV: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:VAV:FanPowered"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneVAVFanPowered: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:VAV:HeatAndCool"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneVAVHeatAndCool: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:ConstantVolume"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneConstantVolume: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Zone:DualDuct"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateZoneDualDuct: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:VRF"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemVRF: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:Unitary"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemUnitary: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:UnitaryHeatPump:AirToAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemUnitaryHeatPumpAirToAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:UnitarySystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemUnitarySystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:VAV"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemVAV: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:PackagedVAV"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemPackagedVAV: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:ConstantVolume"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemConstantVolume: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:DualDuct"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemDualDuct: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:System:DedicatedOutdoorAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplateSystemDedicatedOutdoorAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:ChilledWaterLoop"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantChilledWaterLoop: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:Chiller"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantChiller: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:Chiller:ObjectReference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantChillerObjectReference: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:Tower"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantTower: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:Tower:ObjectReference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantTowerObjectReference: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:HotWaterLoop"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantHotWaterLoop: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:Boiler"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantBoiler: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:Boiler:ObjectReference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantBoilerObjectReference: ...
    @overload
    def add(
        self,
        obj_type: Literal["HVACTemplate:Plant:MixedWaterLoop"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HVACTemplatePlantMixedWaterLoop: ...
    @overload
    def add(
        self,
        obj_type: Literal["DesignSpecification:OutdoorAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DesignSpecificationOutdoorAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["DesignSpecification:OutdoorAir:SpaceList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DesignSpecificationOutdoorAirSpaceList: ...
    @overload
    def add(
        self,
        obj_type: Literal["DesignSpecification:ZoneAirDistribution"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DesignSpecificationZoneAirDistribution: ...
    @overload
    def add(
        self,
        obj_type: Literal["Sizing:Parameters"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SizingParameters: ...
    @overload
    def add(
        self,
        obj_type: Literal["Sizing:Zone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SizingZone: ...
    @overload
    def add(
        self,
        obj_type: Literal["DesignSpecification:ZoneHVAC:Sizing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DesignSpecificationZoneHVACSizing: ...
    @overload
    def add(
        self,
        obj_type: Literal["DesignSpecification:AirTerminal:Sizing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DesignSpecificationAirTerminalSizing: ...
    @overload
    def add(
        self,
        obj_type: Literal["Sizing:System"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SizingSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["Sizing:Plant"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SizingPlant: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutputControl:Sizing:Style"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputControlSizingStyle: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneControl:Humidistat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneControlHumidistat: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneControl:Thermostat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneControlThermostat: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneControl:Thermostat:OperativeTemperature"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneControlThermostatOperativeTemperature: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneControl:Thermostat:ThermalComfort"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneControlThermostatThermalComfort: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneControl:Thermostat:TemperatureAndHumidity"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneControlThermostatTemperatureAndHumidity: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermostatSetpoint:SingleHeating"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermostatSetpointSingleHeating: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermostatSetpoint:SingleCooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermostatSetpointSingleCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermostatSetpoint:SingleHeatingOrCooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermostatSetpointSingleHeatingOrCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermostatSetpoint:DualSetpoint"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermostatSetpointDualSetpoint: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermostatSetpointThermalComfortFangerSingleHeating: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermostatSetpointThermalComfortFangerSingleCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermostatSetpointThermalComfortFangerDualSetpoint: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneControl:Thermostat:StagedDualSetpoint"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneControlThermostatStagedDualSetpoint: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneControl:ContaminantController"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneControlContaminantController: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:IdealLoadsAirSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACIdealLoadsAirSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:FourPipeFanCoil"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACFourPipeFanCoil: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:WindowAirConditioner"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACWindowAirConditioner: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:PackagedTerminalAirConditioner"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACPackagedTerminalAirConditioner: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:PackagedTerminalHeatPump"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACPackagedTerminalHeatPump: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:WaterToAirHeatPump"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACWaterToAirHeatPump: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:Dehumidifier:DX"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACDehumidifierDX: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:EnergyRecoveryVentilator"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACEnergyRecoveryVentilator: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:EnergyRecoveryVentilator:Controller"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACEnergyRecoveryVentilatorController: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:UnitVentilator"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACUnitVentilator: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:UnitHeater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACUnitHeater: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:EvaporativeCoolerUnit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACEvaporativeCoolerUnit: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:HybridUnitaryHVAC"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACHybridUnitaryHVAC: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:OutdoorAirUnit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACOutdoorAirUnit: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:OutdoorAirUnit:EquipmentList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACOutdoorAirUnitEquipmentList: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:TerminalUnit:VariableRefrigerantFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACTerminalUnitVariableRefrigerantFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Water:Design"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACBaseboardRadiantConvectiveWaterDesign: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Water"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACBaseboardRadiantConvectiveWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Steam:Design"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACBaseboardRadiantConvectiveSteamDesign: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Steam"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACBaseboardRadiantConvectiveSteam: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Electric"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACBaseboardRadiantConvectiveElectric: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:CoolingPanel:RadiantConvective:Water"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACCoolingPanelRadiantConvectiveWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:Baseboard:Convective:Water"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACBaseboardConvectiveWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:Baseboard:Convective:Electric"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACBaseboardConvectiveElectric: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:VariableFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACLowTemperatureRadiantVariableFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACLowTemperatureRadiantVariableFlowDesign: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:ConstantFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACLowTemperatureRadiantConstantFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACLowTemperatureRadiantConstantFlowDesign: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:Electric"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACLowTemperatureRadiantElectric: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:SurfaceGroup"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACLowTemperatureRadiantSurfaceGroup: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:HighTemperatureRadiant"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACHighTemperatureRadiant: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:VentilatedSlab"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACVentilatedSlab: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:VentilatedSlab:SlabGroup"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACVentilatedSlabSlabGroup: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:Reheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctConstantVolumeReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:NoReheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctConstantVolumeNoReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:VAV:NoReheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctVAVNoReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:VAV:Reheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctVAVReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctVAVReheatVariableSpeedFan: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctVAVHeatAndCoolNoReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctVAVHeatAndCoolReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:SeriesPIU:Reheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctSeriesPIUReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:ParallelPIU:Reheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctParallelPIUReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctConstantVolumeFourPipeInduction: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctConstantVolumeFourPipeBeam: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:CooledBeam"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctConstantVolumeCooledBeam: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:Mixer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctMixer: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:DualDuct:ConstantVolume"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalDualDuctConstantVolume: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:DualDuct:VAV"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalDualDuctVAV: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:DualDuct:VAV:OutdoorAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalDualDuctVAVOutdoorAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:AirDistributionUnit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACAirDistributionUnit: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:ExhaustControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACExhaustControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:EquipmentList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACEquipmentList: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:EquipmentConnections"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACEquipmentConnections: ...
    @overload
    def add(
        self,
        obj_type: Literal["SpaceHVAC:EquipmentConnections"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SpaceHVACEquipmentConnections: ...
    @overload
    def add(
        self,
        obj_type: Literal["SpaceHVAC:ZoneEquipmentSplitter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SpaceHVACZoneEquipmentSplitter: ...
    @overload
    def add(
        self,
        obj_type: Literal["SpaceHVAC:ZoneEquipmentMixer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SpaceHVACZoneEquipmentMixer: ...
    @overload
    def add(
        self,
        obj_type: Literal["SpaceHVAC:ZoneReturnMixer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SpaceHVACZoneReturnMixer: ...
    @overload
    def add(
        self,
        obj_type: Literal["Fan:SystemModel"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FanSystemModel: ...
    @overload
    def add(
        self,
        obj_type: Literal["Fan:ConstantVolume"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FanConstantVolume: ...
    @overload
    def add(
        self,
        obj_type: Literal["Fan:VariableVolume"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FanVariableVolume: ...
    @overload
    def add(
        self,
        obj_type: Literal["Fan:OnOff"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FanOnOff: ...
    @overload
    def add(
        self,
        obj_type: Literal["Fan:ZoneExhaust"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FanZoneExhaust: ...
    @overload
    def add(
        self,
        obj_type: Literal["FanPerformance:NightVentilation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FanPerformanceNightVentilation: ...
    @overload
    def add(
        self,
        obj_type: Literal["Fan:ComponentModel"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FanComponentModel: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:Water"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:Water:DetailedGeometry"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingWaterDetailedGeometry: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoilSystem:Cooling:Water"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilSystemCoolingWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDX: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:CurveFit:Performance"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXCurveFitPerformance: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:CurveFit:OperatingMode"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXCurveFitOperatingMode: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:CurveFit:Speed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXCurveFitSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:DX:ASHRAE205:Performance"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilDXASHRAE205Performance: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:SingleSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXSingleSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:TwoSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXTwoSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:MultiSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXMultiSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:VariableSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXVariableSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:TwoStageWithHumidityControlMode"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXTwoStageWithHumidityControlMode: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoilPerformance:DX:Cooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilPerformanceDXCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:VariableRefrigerantFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXVariableRefrigerantFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:DX:VariableRefrigerantFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingDXVariableRefrigerantFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXVariableRefrigerantFlowFluidTemperatureControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingDXVariableRefrigerantFlowFluidTemperatureControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:Water"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:Steam"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingSteam: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:Electric"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingElectric: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:Electric:MultiStage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingElectricMultiStage: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:Fuel"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingFuel: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:Gas:MultiStage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingGasMultiStage: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:Desuperheater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingDesuperheater: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:DX:SingleSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingDXSingleSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:DX:MultiSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingDXMultiSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:DX:VariableSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingDXVariableSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:ParameterEstimation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingWaterToAirHeatPumpParameterEstimation: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:WaterToAirHeatPump:ParameterEstimation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingWaterToAirHeatPumpParameterEstimation: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:EquationFit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingWaterToAirHeatPumpEquationFit: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:WaterToAirHeatPump:EquationFit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingWaterToAirHeatPumpEquationFit: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:Pumped"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilWaterHeatingAirToWaterHeatPumpPumped: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:Wrapped"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilWaterHeatingAirToWaterHeatPumpWrapped: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilWaterHeatingAirToWaterHeatPumpVariableSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:WaterHeating:Desuperheater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilWaterHeatingDesuperheater: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoilSystem:Cooling:DX"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilSystemCoolingDX: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoilSystem:Heating:DX"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilSystemHeatingDX: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoilSystem:Cooling:Water:HeatExchangerAssisted"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilSystemCoolingWaterHeatExchangerAssisted: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoilSystem:Cooling:DX:HeatExchangerAssisted"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilSystemCoolingDXHeatExchangerAssisted: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoilSystem:IntegratedHeatPump:AirSource"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilSystemIntegratedHeatPumpAirSource: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:Cooling:DX:SingleSpeed:ThermalStorage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilCoolingDXSingleSpeedThermalStorage: ...
    @overload
    def add(
        self,
        obj_type: Literal["EvaporativeCooler:Direct:CelDekPad"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EvaporativeCoolerDirectCelDekPad: ...
    @overload
    def add(
        self,
        obj_type: Literal["EvaporativeCooler:Indirect:CelDekPad"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EvaporativeCoolerIndirectCelDekPad: ...
    @overload
    def add(
        self,
        obj_type: Literal["EvaporativeCooler:Indirect:WetCoil"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EvaporativeCoolerIndirectWetCoil: ...
    @overload
    def add(
        self,
        obj_type: Literal["EvaporativeCooler:Indirect:ResearchSpecial"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EvaporativeCoolerIndirectResearchSpecial: ...
    @overload
    def add(
        self,
        obj_type: Literal["EvaporativeCooler:Direct:ResearchSpecial"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EvaporativeCoolerDirectResearchSpecial: ...
    @overload
    def add(
        self,
        obj_type: Literal["Humidifier:Steam:Electric"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HumidifierSteamElectric: ...
    @overload
    def add(
        self,
        obj_type: Literal["Humidifier:Steam:Gas"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HumidifierSteamGas: ...
    @overload
    def add(
        self,
        obj_type: Literal["Dehumidifier:Desiccant:NoFans"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DehumidifierDesiccantNoFans: ...
    @overload
    def add(
        self,
        obj_type: Literal["Dehumidifier:Desiccant:System"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DehumidifierDesiccantSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatExchanger:AirToAir:FlatPlate"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatExchangerAirToAirFlatPlate: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatExchanger:AirToAir:SensibleAndLatent"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatExchangerAirToAirSensibleAndLatent: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatExchanger:Desiccant:BalancedFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatExchangerDesiccantBalancedFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatExchanger:Desiccant:BalancedFlow:PerformanceDataType1"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatExchangerDesiccantBalancedFlowPerformanceDataType1: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:UnitarySystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitarySystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["UnitarySystemPerformance:Multispeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> UnitarySystemPerformanceMultispeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:Unitary:Furnace:HeatOnly"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitaryFurnaceHeatOnly: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:Unitary:Furnace:HeatCool"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitaryFurnaceHeatCool: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:UnitaryHeatOnly"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitaryHeatOnly: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:UnitaryHeatCool"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitaryHeatCool: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:AirToAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitaryHeatPumpAirToAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:WaterToAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitaryHeatPumpWaterToAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirConditioner:VariableRefrigerantFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirConditionerVariableRefrigerantFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirConditionerVariableRefrigerantFlowFluidTemperatureControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneTerminalUnitList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneTerminalUnitList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Controller:WaterCoil"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ControllerWaterCoil: ...
    @overload
    def add(
        self,
        obj_type: Literal["Controller:OutdoorAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ControllerOutdoorAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["Controller:MechanicalVentilation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ControllerMechanicalVentilation: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:ControllerList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACControllerList: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVAC: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:OutdoorAirSystem:EquipmentList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACOutdoorAirSystemEquipmentList: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:OutdoorAirSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACOutdoorAirSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutdoorAir:Mixer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutdoorAirMixer: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:ZoneSplitter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACZoneSplitter: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:SupplyPlenum"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACSupplyPlenum: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:SupplyPath"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACSupplyPath: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:ZoneMixer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACZoneMixer: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:ReturnPlenum"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACReturnPlenum: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:ReturnPath"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACReturnPath: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:ExhaustSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACExhaustSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:DedicatedOutdoorAirSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACDedicatedOutdoorAirSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:Mixer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACMixer: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirLoopHVAC:Splitter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirLoopHVACSplitter: ...
    @overload
    def add(
        self,
        obj_type: Literal["Branch"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Branch: ...
    @overload
    def add(
        self,
        obj_type: Literal["BranchList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> BranchList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Connector:Splitter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConnectorSplitter: ...
    @overload
    def add(
        self,
        obj_type: Literal["Connector:Mixer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConnectorMixer: ...
    @overload
    def add(
        self,
        obj_type: Literal["ConnectorList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ConnectorList: ...
    @overload
    def add(
        self,
        obj_type: Literal["NodeList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> NodeList: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutdoorAir:Node"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutdoorAirNode: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutdoorAir:NodeList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutdoorAirNodeList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Pipe:Adiabatic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PipeAdiabatic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Pipe:Adiabatic:Steam"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PipeAdiabaticSteam: ...
    @overload
    def add(
        self,
        obj_type: Literal["Pipe:Indoor"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PipeIndoor: ...
    @overload
    def add(
        self,
        obj_type: Literal["Pipe:Outdoor"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PipeOutdoor: ...
    @overload
    def add(
        self,
        obj_type: Literal["Pipe:Underground"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PipeUnderground: ...
    @overload
    def add(
        self,
        obj_type: Literal["PipingSystem:Underground:Domain"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PipingSystemUndergroundDomain: ...
    @overload
    def add(
        self,
        obj_type: Literal["PipingSystem:Underground:PipeCircuit"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PipingSystemUndergroundPipeCircuit: ...
    @overload
    def add(
        self,
        obj_type: Literal["PipingSystem:Underground:PipeSegment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PipingSystemUndergroundPipeSegment: ...
    @overload
    def add(
        self,
        obj_type: Literal["Duct"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> Duct: ...
    @overload
    def add(
        self,
        obj_type: Literal["Pump:VariableSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PumpVariableSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Pump:ConstantSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PumpConstantSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["Pump:VariableSpeed:Condensate"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PumpVariableSpeedCondensate: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeaderedPumps:ConstantSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeaderedPumpsConstantSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeaderedPumps:VariableSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeaderedPumpsVariableSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["TemperingValve"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> TemperingValve: ...
    @overload
    def add(
        self,
        obj_type: Literal["LoadProfile:Plant"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> LoadProfilePlant: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollectorPerformance:FlatPlate"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorPerformanceFlatPlate: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollector:FlatPlate:Water"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorFlatPlateWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollector:FlatPlate:PhotovoltaicThermal"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorFlatPlatePhotovoltaicThermal: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollectorPerformance:PhotovoltaicThermal:Simple"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorPerformancePhotovoltaicThermalSimple: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollectorPerformance:PhotovoltaicThermal:BIPVT"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorPerformancePhotovoltaicThermalBIPVT: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollector:IntegralCollectorStorage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorIntegralCollectorStorage: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollectorPerformance:IntegralCollectorStorage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorPerformanceIntegralCollectorStorage: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollector:UnglazedTranspired"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorUnglazedTranspired: ...
    @overload
    def add(
        self,
        obj_type: Literal["SolarCollector:UnglazedTranspired:Multisystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SolarCollectorUnglazedTranspiredMultisystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["Boiler:HotWater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> BoilerHotWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["Boiler:Steam"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> BoilerSteam: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:Electric:ASHRAE205"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerElectricASHRAE205: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:Electric:EIR"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerElectricEIR: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:Electric:ReformulatedEIR"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerElectricReformulatedEIR: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:Electric"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerElectric: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:Absorption:Indirect"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerAbsorptionIndirect: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:Absorption"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerAbsorption: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:ConstantCOP"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerConstantCOP: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:EngineDriven"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerEngineDriven: ...
    @overload
    def add(
        self,
        obj_type: Literal["Chiller:CombustionTurbine"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerCombustionTurbine: ...
    @overload
    def add(
        self,
        obj_type: Literal["ChillerHeater:Absorption:DirectFired"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerHeaterAbsorptionDirectFired: ...
    @overload
    def add(
        self,
        obj_type: Literal["ChillerHeater:Absorption:DoubleEffect"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerHeaterAbsorptionDoubleEffect: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:PlantLoop:EIR:Cooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpPlantLoopEIRCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:PlantLoop:EIR:Heating"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpPlantLoopEIRHeating: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:AirToWater:FuelFired:Heating"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpAirToWaterFuelFiredHeating: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:AirToWater:FuelFired:Cooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpAirToWaterFuelFiredCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:AirToWater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpAirToWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:WaterToWater:EquationFit:Heating"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpWaterToWaterEquationFitHeating: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:WaterToWater:EquationFit:Cooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpWaterToWaterEquationFitCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:WaterToWater:ParameterEstimation:Cooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpWaterToWaterParameterEstimationCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatPump:WaterToWater:ParameterEstimation:Heating"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatPumpWaterToWaterParameterEstimationHeating: ...
    @overload
    def add(
        self,
        obj_type: Literal["DistrictCooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DistrictCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["DistrictHeating:Water"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DistrictHeatingWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["DistrictHeating:Steam"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DistrictHeatingSteam: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantComponent:TemperatureSource"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantComponentTemperatureSource: ...
    @overload
    def add(
        self,
        obj_type: Literal["CentralHeatPumpSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CentralHeatPumpSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["ChillerHeaterPerformance:Electric:EIR"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ChillerHeaterPerformanceElectricEIR: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoolingTower:SingleSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoolingTowerSingleSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoolingTower:TwoSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoolingTowerTwoSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoolingTower:VariableSpeed:Merkel"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoolingTowerVariableSpeedMerkel: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoolingTower:VariableSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoolingTowerVariableSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoolingTowerPerformance:CoolTools"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoolingTowerPerformanceCoolTools: ...
    @overload
    def add(
        self,
        obj_type: Literal["CoolingTowerPerformance:YorkCalc"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoolingTowerPerformanceYorkCalc: ...
    @overload
    def add(
        self,
        obj_type: Literal["EvaporativeFluidCooler:SingleSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EvaporativeFluidCoolerSingleSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["EvaporativeFluidCooler:TwoSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EvaporativeFluidCoolerTwoSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["FluidCooler:SingleSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FluidCoolerSingleSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["FluidCooler:TwoSpeed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FluidCoolerTwoSpeed: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:System"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:Vertical:Sizing:Rectangle"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerVerticalSizingRectangle: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:Vertical:Properties"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerVerticalProperties: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:Vertical:Array"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerVerticalArray: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:Vertical:Single"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerVerticalSingle: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:ResponseFactors"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerResponseFactors: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:Pond"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerPond: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:Surface"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerSurface: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:HorizontalTrench"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerHorizontalTrench: ...
    @overload
    def add(
        self,
        obj_type: Literal["GroundHeatExchanger:Slinky"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GroundHeatExchangerSlinky: ...
    @overload
    def add(
        self,
        obj_type: Literal["HeatExchanger:FluidToFluid"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HeatExchangerFluidToFluid: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterHeater:Mixed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterHeaterMixed: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterHeater:Stratified"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterHeaterStratified: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterHeater:Sizing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterHeaterSizing: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterHeater:HeatPump:PumpedCondenser"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterHeaterHeatPumpPumpedCondenser: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterHeater:HeatPump:WrappedCondenser"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterHeaterHeatPumpWrappedCondenser: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermalStorage:Ice:Simple"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermalStorageIceSimple: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermalStorage:Ice:Detailed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermalStorageIceDetailed: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermalStorage:ChilledWater:Mixed"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermalStorageChilledWaterMixed: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermalStorage:ChilledWater:Stratified"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermalStorageChilledWaterStratified: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermalStorage:HotWater:Stratified"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermalStorageHotWaterStratified: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermalStorage:PCM"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermalStoragePCM: ...
    @overload
    def add(
        self,
        obj_type: Literal["ThermalStorage:Sizing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ThermalStorageSizing: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantLoop"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantLoop: ...
    @overload
    def add(
        self,
        obj_type: Literal["CondenserLoop"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CondenserLoop: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentList: ...
    @overload
    def add(
        self,
        obj_type: Literal["CondenserEquipmentList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CondenserEquipmentList: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:Uncontrolled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationUncontrolled: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:CoolingLoad"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationCoolingLoad: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:HeatingLoad"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationHeatingLoad: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:OutdoorDryBulb"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationOutdoorDryBulb: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:OutdoorWetBulb"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationOutdoorWetBulb: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:OutdoorRelativeHumidity"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationOutdoorRelativeHumidity: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:OutdoorDewpoint"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationOutdoorDewpoint: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:ComponentSetpoint"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationComponentSetpoint: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:ThermalEnergyStorage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationThermalEnergyStorage: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:OutdoorDryBulbDifference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationOutdoorDryBulbDifference: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:OutdoorWetBulbDifference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationOutdoorWetBulbDifference: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:OutdoorDewpointDifference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationOutdoorDewpointDifference: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:ChillerHeaterChangeover"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationChillerHeaterChangeover: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperationSchemes"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationSchemes: ...
    @overload
    def add(
        self,
        obj_type: Literal["CondenserEquipmentOperationSchemes"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CondenserEquipmentOperationSchemes: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:Sensor"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemSensor: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:Actuator"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemActuator: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:ProgramCallingManager"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemProgramCallingManager: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:Program"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemProgram: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:Subroutine"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemSubroutine: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:GlobalVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemGlobalVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:OutputVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemOutputVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:MeteredOutputVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemMeteredOutputVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:TrendVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemTrendVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:InternalVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemInternalVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:CurveOrTableIndexVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemCurveOrTableIndexVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnergyManagementSystem:ConstructionIndexVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnergyManagementSystemConstructionIndexVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterface: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:Schedule"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceSchedule: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:Variable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:Actuator"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceActuator: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitImport: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:From:Variable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitImportFromVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Schedule"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitImportToSchedule: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Actuator"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitImportToActuator: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Variable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitImportToVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:From:Variable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitExportFromVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Schedule"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitExportToSchedule: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Actuator"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitExportToActuator: ...
    @overload
    def add(
        self,
        obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Variable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ExternalInterfaceFunctionalMockupUnitExportToVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:ForcedAir:UserDefined"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACForcedAirUserDefined: ...
    @overload
    def add(
        self,
        obj_type: Literal["AirTerminal:SingleDuct:UserDefined"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AirTerminalSingleDuctUserDefined: ...
    @overload
    def add(
        self,
        obj_type: Literal["Coil:UserDefined"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CoilUserDefined: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantComponent:UserDefined"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantComponentUserDefined: ...
    @overload
    def add(
        self,
        obj_type: Literal["PlantEquipmentOperation:UserDefined"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PlantEquipmentOperationUserDefined: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:Scheduled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerScheduled: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:ScheduledOn"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerScheduledOn: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:ScheduledOff"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerScheduledOff: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:OptimumStart"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerOptimumStart: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:NightCycle"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerNightCycle: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:DifferentialThermostat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerDifferentialThermostat: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:HighTemperatureTurnOff"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerHighTemperatureTurnOff: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:HighTemperatureTurnOn"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerHighTemperatureTurnOn: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:LowTemperatureTurnOff"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerLowTemperatureTurnOff: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:LowTemperatureTurnOn"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerLowTemperatureTurnOn: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:NightVentilation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerNightVentilation: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManager:HybridVentilation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerHybridVentilation: ...
    @overload
    def add(
        self,
        obj_type: Literal["AvailabilityManagerAssignmentList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> AvailabilityManagerAssignmentList: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:Scheduled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerScheduled: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:Scheduled:DualSetpoint"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerScheduledDualSetpoint: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:OutdoorAirReset"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerOutdoorAirReset: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SingleZone:Reheat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSingleZoneReheat: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SingleZone:Heating"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSingleZoneHeating: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SingleZone:Cooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSingleZoneCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SingleZone:Humidity:Minimum"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSingleZoneHumidityMinimum: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SingleZone:Humidity:Maximum"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSingleZoneHumidityMaximum: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:MixedAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerMixedAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:OutdoorAirPretreat"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerOutdoorAirPretreat: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:Warmest"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerWarmest: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:Coldest"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerColdest: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:ReturnAirBypassFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerReturnAirBypassFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:WarmestTemperatureFlow"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerWarmestTemperatureFlow: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:MultiZone:Heating:Average"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerMultiZoneHeatingAverage: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:MultiZone:Cooling:Average"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerMultiZoneCoolingAverage: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:MultiZone:MinimumHumidity:Average"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerMultiZoneMinimumHumidityAverage: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:MultiZone:MaximumHumidity:Average"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerMultiZoneMaximumHumidityAverage: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:MultiZone:Humidity:Minimum"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerMultiZoneHumidityMinimum: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:MultiZone:Humidity:Maximum"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerMultiZoneHumidityMaximum: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:FollowOutdoorAirTemperature"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerFollowOutdoorAirTemperature: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:FollowSystemNodeTemperature"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerFollowSystemNodeTemperature: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:FollowGroundTemperature"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerFollowGroundTemperature: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:CondenserEnteringReset"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerCondenserEnteringReset: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:CondenserEnteringReset:Ideal"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerCondenserEnteringResetIdeal: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SingleZone:OneStageCooling"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSingleZoneOneStageCooling: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SingleZone:OneStageHeating"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSingleZoneOneStageHeating: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:ReturnTemperature:ChilledWater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerReturnTemperatureChilledWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:ReturnTemperature:HotWater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerReturnTemperatureHotWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SystemNodeReset:Temperature"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSystemNodeResetTemperature: ...
    @overload
    def add(
        self,
        obj_type: Literal["SetpointManager:SystemNodeReset:Humidity"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> SetpointManagerSystemNodeResetHumidity: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:Case"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCase: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:CompressorRack"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCompressorRack: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:CaseAndWalkInList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCaseAndWalkInList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:Condenser:AirCooled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCondenserAirCooled: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:Condenser:EvaporativeCooled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCondenserEvaporativeCooled: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:Condenser:WaterCooled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCondenserWaterCooled: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:Condenser:Cascade"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCondenserCascade: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:GasCooler:AirCooled"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationGasCoolerAirCooled: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:TransferLoadList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationTransferLoadList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:Subcooler"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationSubcooler: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:Compressor"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCompressor: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:CompressorList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationCompressorList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:System"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:TranscriticalSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationTranscriticalSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:SecondarySystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationSecondarySystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:WalkIn"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationWalkIn: ...
    @overload
    def add(
        self,
        obj_type: Literal["Refrigeration:AirChiller"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> RefrigerationAirChiller: ...
    @overload
    def add(
        self,
        obj_type: Literal["ZoneHVAC:RefrigerationChillerSet"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ZoneHVACRefrigerationChillerSet: ...
    @overload
    def add(
        self,
        obj_type: Literal["DemandManagerAssignmentList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DemandManagerAssignmentList: ...
    @overload
    def add(
        self,
        obj_type: Literal["DemandManager:ExteriorLights"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DemandManagerExteriorLights: ...
    @overload
    def add(
        self,
        obj_type: Literal["DemandManager:Lights"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DemandManagerLights: ...
    @overload
    def add(
        self,
        obj_type: Literal["DemandManager:ElectricEquipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DemandManagerElectricEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["DemandManager:Thermostats"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DemandManagerThermostats: ...
    @overload
    def add(
        self,
        obj_type: Literal["DemandManager:Ventilation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> DemandManagerVentilation: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:InternalCombustionEngine"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorInternalCombustionEngine: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:CombustionTurbine"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorCombustionTurbine: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:MicroTurbine"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorMicroTurbine: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:Photovoltaic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorPhotovoltaic: ...
    @overload
    def add(
        self,
        obj_type: Literal["PhotovoltaicPerformance:Simple"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PhotovoltaicPerformanceSimple: ...
    @overload
    def add(
        self,
        obj_type: Literal["PhotovoltaicPerformance:EquivalentOne-Diode"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PhotovoltaicPerformanceEquivalentOneDiode: ...
    @overload
    def add(
        self,
        obj_type: Literal["PhotovoltaicPerformance:Sandia"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PhotovoltaicPerformanceSandia: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:PVWatts"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorPVWatts: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Inverter:PVWatts"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterInverterPVWatts: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCell: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell:PowerModule"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCellPowerModule: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell:AirSupply"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCellAirSupply: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell:WaterSupply"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCellWaterSupply: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell:AuxiliaryHeater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCellAuxiliaryHeater: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell:ExhaustGasToWaterHeatExchanger"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCellExhaustGasToWaterHeatExchanger: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell:ElectricalStorage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCellElectricalStorage: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell:Inverter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCellInverter: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelCell:StackCooler"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelCellStackCooler: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:MicroCHP"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorMicroCHP: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:MicroCHP:NonNormalizedParameters"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorMicroCHPNonNormalizedParameters: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:FuelSupply"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorFuelSupply: ...
    @overload
    def add(
        self,
        obj_type: Literal["Generator:WindTurbine"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> GeneratorWindTurbine: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Generators"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterGenerators: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Inverter:Simple"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterInverterSimple: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Inverter:FunctionOfPower"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterInverterFunctionOfPower: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Inverter:LookUpTable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterInverterLookUpTable: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Storage:Simple"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterStorageSimple: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Storage:Battery"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterStorageBattery: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Storage:LiIonNMCBattery"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterStorageLiIonNMCBattery: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Transformer"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterTransformer: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Distribution"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterDistribution: ...
    @overload
    def add(
        self,
        obj_type: Literal["ElectricLoadCenter:Storage:Converter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ElectricLoadCenterStorageConverter: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterUse:Equipment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterUseEquipment: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterUse:Connections"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterUseConnections: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterUse:Storage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterUseStorage: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterUse:Well"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterUseWell: ...
    @overload
    def add(
        self,
        obj_type: Literal["WaterUse:RainCollector"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> WaterUseRainCollector: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:TemperatureSensorOffset:OutdoorAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelTemperatureSensorOffsetOutdoorAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:HumiditySensorOffset:OutdoorAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelHumiditySensorOffsetOutdoorAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:EnthalpySensorOffset:OutdoorAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelEnthalpySensorOffsetOutdoorAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:TemperatureSensorOffset:ReturnAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelTemperatureSensorOffsetReturnAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:EnthalpySensorOffset:ReturnAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelEnthalpySensorOffsetReturnAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:TemperatureSensorOffset:ChillerSupplyWater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelTemperatureSensorOffsetChillerSupplyWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:TemperatureSensorOffset:CoilSupplyAir"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelTemperatureSensorOffsetCoilSupplyAir: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:TemperatureSensorOffset:CondenserSupplyWater"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelTemperatureSensorOffsetCondenserSupplyWater: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:ThermostatOffset"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelThermostatOffset: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:HumidistatOffset"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelHumidistatOffset: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:Fouling:AirFilter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelFoulingAirFilter: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:Fouling:Boiler"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelFoulingBoiler: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:Fouling:EvaporativeCooler"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelFoulingEvaporativeCooler: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:Fouling:Chiller"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelFoulingChiller: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:Fouling:CoolingTower"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelFoulingCoolingTower: ...
    @overload
    def add(
        self,
        obj_type: Literal["FaultModel:Fouling:Coil"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FaultModelFoulingCoil: ...
    @overload
    def add(
        self,
        obj_type: Literal["Matrix:TwoDimension"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MatrixTwoDimension: ...
    @overload
    def add(
        self,
        obj_type: Literal["HybridModel:Zone"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> HybridModelZone: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Linear"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveLinear: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:QuadLinear"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveQuadLinear: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:QuintLinear"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveQuintLinear: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Quadratic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveQuadratic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Cubic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveCubic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Quartic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveQuartic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Exponent"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveExponent: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Bicubic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveBicubic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Biquadratic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveBiquadratic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:QuadraticLinear"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveQuadraticLinear: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:CubicLinear"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveCubicLinear: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Triquadratic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveTriquadratic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Functional:PressureDrop"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveFunctionalPressureDrop: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:FanPressureRise"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveFanPressureRise: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:ExponentialSkewNormal"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveExponentialSkewNormal: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:Sigmoid"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveSigmoid: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:RectangularHyperbola1"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveRectangularHyperbola1: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:RectangularHyperbola2"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveRectangularHyperbola2: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:ExponentialDecay"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveExponentialDecay: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:DoubleExponentialDecay"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveDoubleExponentialDecay: ...
    @overload
    def add(
        self,
        obj_type: Literal["Curve:ChillerPartLoadWithLift"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurveChillerPartLoadWithLift: ...
    @overload
    def add(
        self,
        obj_type: Literal["Table:IndependentVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> TableIndependentVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["Table:IndependentVariableList"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> TableIndependentVariableList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Table:Lookup"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> TableLookup: ...
    @overload
    def add(
        self,
        obj_type: Literal["FluidProperties:Name"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FluidPropertiesName: ...
    @overload
    def add(
        self,
        obj_type: Literal["FluidProperties:GlycolConcentration"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FluidPropertiesGlycolConcentration: ...
    @overload
    def add(
        self,
        obj_type: Literal["FluidProperties:Temperatures"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FluidPropertiesTemperatures: ...
    @overload
    def add(
        self,
        obj_type: Literal["FluidProperties:Saturated"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FluidPropertiesSaturated: ...
    @overload
    def add(
        self,
        obj_type: Literal["FluidProperties:Superheated"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FluidPropertiesSuperheated: ...
    @overload
    def add(
        self,
        obj_type: Literal["FluidProperties:Concentration"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FluidPropertiesConcentration: ...
    @overload
    def add(
        self,
        obj_type: Literal["CurrencyType"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> CurrencyType: ...
    @overload
    def add(
        self,
        obj_type: Literal["ComponentCost:Adjustments"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ComponentCostAdjustments: ...
    @overload
    def add(
        self,
        obj_type: Literal["ComponentCost:Reference"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ComponentCostReference: ...
    @overload
    def add(
        self,
        obj_type: Literal["ComponentCost:LineItem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ComponentCostLineItem: ...
    @overload
    def add(
        self,
        obj_type: Literal["UtilityCost:Tariff"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> UtilityCostTariff: ...
    @overload
    def add(
        self,
        obj_type: Literal["UtilityCost:Qualify"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> UtilityCostQualify: ...
    @overload
    def add(
        self,
        obj_type: Literal["UtilityCost:Charge:Simple"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> UtilityCostChargeSimple: ...
    @overload
    def add(
        self,
        obj_type: Literal["UtilityCost:Charge:Block"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> UtilityCostChargeBlock: ...
    @overload
    def add(
        self,
        obj_type: Literal["UtilityCost:Ratchet"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> UtilityCostRatchet: ...
    @overload
    def add(
        self,
        obj_type: Literal["UtilityCost:Variable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> UtilityCostVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["UtilityCost:Computation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> UtilityCostComputation: ...
    @overload
    def add(
        self,
        obj_type: Literal["LifeCycleCost:Parameters"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> LifeCycleCostParameters: ...
    @overload
    def add(
        self,
        obj_type: Literal["LifeCycleCost:RecurringCosts"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> LifeCycleCostRecurringCosts: ...
    @overload
    def add(
        self,
        obj_type: Literal["LifeCycleCost:NonrecurringCost"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> LifeCycleCostNonrecurringCost: ...
    @overload
    def add(
        self,
        obj_type: Literal["LifeCycleCost:UsePriceEscalation"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> LifeCycleCostUsePriceEscalation: ...
    @overload
    def add(
        self,
        obj_type: Literal["LifeCycleCost:UseAdjustment"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> LifeCycleCostUseAdjustment: ...
    @overload
    def add(
        self,
        obj_type: Literal["Parametric:SetValueForRun"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ParametricSetValueForRun: ...
    @overload
    def add(
        self,
        obj_type: Literal["Parametric:Logic"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ParametricLogic: ...
    @overload
    def add(
        self,
        obj_type: Literal["Parametric:RunControl"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ParametricRunControl: ...
    @overload
    def add(
        self,
        obj_type: Literal["Parametric:FileNameSuffix"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> ParametricFileNameSuffix: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:VariableDictionary"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputVariableDictionary: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Surfaces:List"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputSurfacesList: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Surfaces:Drawing"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputSurfacesDrawing: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Schedules"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputSchedules: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Constructions"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputConstructions: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:EnergyManagementSystem"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputEnergyManagementSystem: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutputControl:SurfaceColorScheme"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputControlSurfaceColorScheme: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Table:SummaryReports"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputTableSummaryReports: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Table:TimeBins"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputTableTimeBins: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Table:Monthly"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputTableMonthly: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Table:Annual"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputTableAnnual: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Table:ReportPeriod"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputTableReportPeriod: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutputControl:Table:Style"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputControlTableStyle: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutputControl:ReportingTolerances"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputControlReportingTolerances: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutputControl:ResilienceSummaries"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputControlResilienceSummaries: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Variable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Meter"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputMeter: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Meter:MeterFileOnly"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputMeterMeterFileOnly: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Meter:Cumulative"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputMeterCumulative: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Meter:Cumulative:MeterFileOnly"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputMeterCumulativeMeterFileOnly: ...
    @overload
    def add(
        self,
        obj_type: Literal["Meter:Custom"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MeterCustom: ...
    @overload
    def add(
        self,
        obj_type: Literal["Meter:CustomDecrement"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> MeterCustomDecrement: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutputControl:Files"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputControlFiles: ...
    @overload
    def add(
        self,
        obj_type: Literal["OutputControl:Timestamp"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputControlTimestamp: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:JSON"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputJSON: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:SQLite"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputSQLite: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:EnvironmentalImpactFactors"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputEnvironmentalImpactFactors: ...
    @overload
    def add(
        self,
        obj_type: Literal["EnvironmentalImpactFactors"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> EnvironmentalImpactFactors: ...
    @overload
    def add(
        self,
        obj_type: Literal["FuelFactors"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> FuelFactors: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:Diagnostics"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputDiagnostics: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:DebuggingData"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputDebuggingData: ...
    @overload
    def add(
        self,
        obj_type: Literal["Output:PreprocessorMessage"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> OutputPreprocessorMessage: ...
    @overload
    def add(
        self,
        obj_type: Literal["PythonPlugin:SearchPaths"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PythonPluginSearchPaths: ...
    @overload
    def add(
        self,
        obj_type: Literal["PythonPlugin:Instance"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PythonPluginInstance: ...
    @overload
    def add(
        self,
        obj_type: Literal["PythonPlugin:Variables"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PythonPluginVariables: ...
    @overload
    def add(
        self,
        obj_type: Literal["PythonPlugin:TrendVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PythonPluginTrendVariable: ...
    @overload
    def add(
        self,
        obj_type: Literal["PythonPlugin:OutputVariable"],
        name: str = ...,
        data: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> PythonPluginOutputVariable: ...
    @overload
    def add(
        self, obj_type: str, name: str = ..., data: dict[str, Any] | None = ..., *, validate: bool = ..., **kwargs: Any
    ) -> IDFObject: ...
    def add(
        self, obj_type: str, name: str = ..., data: dict[str, Any] | None = ..., *, validate: bool = ..., **kwargs: Any
    ) -> IDFObject: ...
    def removeidfobject(self, obj: IDFObject) -> None: ...
    def rename(self, obj_type: str, old_name: str, new_name: str) -> None: ...
    def notify_name_change(self, obj: IDFObject, old_name: str, new_name: str) -> None: ...
    def notify_reference_change(self, obj: IDFObject, field_name: str, old_value: Any, new_value: Any) -> None: ...
    def get_referencing(self, name: str) -> set[IDFObject]: ...
    def get_references(self, obj: IDFObject) -> set[str]: ...
    @property
    def schedules_dict(self) -> dict[str, IDFObject]: ...
    def get_schedule(self, name: str) -> IDFObject | None: ...
    def get_used_schedules(self) -> set[str]: ...
    def get_zone_surfaces(self, zone_name: str) -> list[IDFObject]: ...
    @property
    def all_objects(self) -> Iterator[IDFObject]: ...
    def objects_by_type(self) -> Iterator[tuple[str, IDFCollection[IDFObject]]]: ...
    def expand(self, *, energyplus: EnergyPlusConfig | None = ..., timeout: float = ...) -> IDFDocument[Strict]: ...
    def copy(self) -> IDFDocument[Strict]: ...
    @property
    def zones(self) -> IDFCollection[Zone]: ...
    @property
    def materials(self) -> IDFCollection[Material]: ...
    @property
    def material_nomass(self) -> IDFCollection[MaterialNoMass]: ...
    @property
    def material_airgap(self) -> IDFCollection[MaterialAirGap]: ...
    @property
    def constructions(self) -> IDFCollection[Construction]: ...
    @property
    def building_surfaces(self) -> IDFCollection[BuildingSurfaceDetailed]: ...
    @property
    def fenestration_surfaces(self) -> IDFCollection[FenestrationSurfaceDetailed]: ...
    @property
    def internal_mass(self) -> IDFCollection[InternalMass]: ...
    @property
    def shading_surfaces(self) -> IDFCollection[ShadingSiteDetailed]: ...
    @property
    def shading_building(self) -> IDFCollection[ShadingBuildingDetailed]: ...
    @property
    def shading_zone(self) -> IDFCollection[ShadingZoneDetailed]: ...
    @property
    def schedules_compact(self) -> IDFCollection[ScheduleCompact]: ...
    @property
    def schedules_constant(self) -> IDFCollection[ScheduleConstant]: ...
    @property
    def schedules_file(self) -> IDFCollection[ScheduleFile]: ...
    @property
    def schedules_year(self) -> IDFCollection[ScheduleYear]: ...
    @property
    def schedules_week_daily(self) -> IDFCollection[ScheduleWeekDaily]: ...
    @property
    def schedules_day_interval(self) -> IDFCollection[ScheduleDayInterval]: ...
    @property
    def schedules_day_hourly(self) -> IDFCollection[ScheduleDayHourly]: ...
    @property
    def schedules_day_list(self) -> IDFCollection[ScheduleDayList]: ...
    @property
    def schedule_type_limits(self) -> IDFCollection[ScheduleTypeLimits]: ...
    @property
    def people(self) -> IDFCollection[People]: ...
    @property
    def lights(self) -> IDFCollection[Lights]: ...
    @property
    def electric_equipment(self) -> IDFCollection[ElectricEquipment]: ...
    @property
    def gas_equipment(self) -> IDFCollection[GasEquipment]: ...
    @property
    def hot_water_equipment(self) -> IDFCollection[HotWaterEquipment]: ...
    @property
    def infiltration(self) -> IDFCollection[ZoneInfiltrationDesignFlowRate]: ...
    @property
    def ventilation(self) -> IDFCollection[ZoneVentilationDesignFlowRate]: ...
    @property
    def thermostats(self) -> IDFCollection[ThermostatSetpointDualSetpoint]: ...
    @property
    def hvac_templates(self) -> IDFCollection[HVACTemplateZoneIdealLoadsAirSystem]: ...
    @property
    def ideal_loads(self) -> IDFCollection[ZoneHVACIdealLoadsAirSystem]: ...
    @property
    def sizing_zone(self) -> IDFCollection[SizingZone]: ...
    @property
    def sizing_system(self) -> IDFCollection[SizingSystem]: ...
    @property
    def output_variables(self) -> IDFCollection[OutputVariable]: ...
    @property
    def output_meters(self) -> IDFCollection[OutputMeter]: ...
    @property
    def output_table_summary(self) -> IDFCollection[OutputTableSummaryReports]: ...
    @property
    def simulation_control(self) -> IDFCollection[SimulationControl]: ...
    @property
    def run_period(self) -> IDFCollection[RunPeriod]: ...
    @property
    def building(self) -> IDFCollection[Building]: ...
    @property
    def global_geometry_rules(self) -> IDFCollection[GlobalGeometryRules]: ...
    @property
    def site_location(self) -> IDFCollection[SiteLocation]: ...
    @property
    def sizing_parameters(self) -> IDFCollection[SizingParameters]: ...
    @property
    def timestep(self) -> IDFCollection[Timestep]: ...
    @property
    def window_material_simple(self) -> IDFCollection[WindowMaterialSimpleGlazingSystem]: ...
    @property
    def window_material_glazing(self) -> IDFCollection[WindowMaterialGlazing]: ...
    @property
    def window_material_gas(self) -> IDFCollection[WindowMaterialGas]: ...
    @property
    def construction_window(self) -> IDFCollection[Construction]: ...
