"""``IDFDocumentV26_1``: an ``IDFDocument`` typed for EnergyPlus 26.1.0 (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs

Import it from :mod:`idfkit.versioned`.
"""

from __future__ import annotations

from typing import Literal, overload

from typing_extensions import Never

from .. import _generated_types as _g
from .. import versioned as _v
from ..document import IDFDocumentAllVersions, Strict
from ..objects import IDFCollection

class _NotAnObjectTypeOfEnergyPlus26_1:
    """Not a name of an object type EnergyPlus 26.1.0 has: indexing a document with one is a type error.

    The last ``__getitem__`` overload of a document type takes this class, which no string is, so
    a type checker that finds no overload for an object type name reports it against this type.
    """

class IDFDocumentV26_1(
    _v._Accessors_v8_9_to_v26_1,
    _v._Accessors_v8_9_to_v26_2,
    _v._Accessors_v9_0_to_v26_1,
    _v._Accessors_v9_0_to_v26_2,
    _v._Accessors_v9_1_to_v26_2,
    _v._Accessors_v9_2_to_v26_2,
    _v._Accessors_v9_3_to_v26_2,
    _v._Accessors_v9_4_to_v26_2,
    _v._Accessors_v9_5_to_v26_2,
    _v._Accessors_v9_6_to_v26_1,
    _v._Accessors_v9_6_to_v26_2,
    _v._Accessors_v22_1_to_v26_1,
    _v._Accessors_v22_1_to_v26_2,
    _v._Accessors_v22_2_to_v26_1,
    _v._Accessors_v22_2_to_v26_2,
    _v._Accessors_v23_1_to_v26_1,
    _v._Accessors_v23_1_to_v26_2,
    _v._Accessors_v23_2_to_v26_2,
    _v._Accessors_v24_1_to_v26_2,
    _v._Accessors_v24_2_to_v26_1,
    _v._Accessors_v24_2_to_v26_2,
    _v._Accessors_v25_1_to_v26_1,
    _v._Accessors_v25_1_to_v26_2,
    _v._Accessors_v25_2_to_v26_2,
    _v._Accessors_v26_1_to_v26_2,
    IDFDocumentAllVersions[Strict],
):
    """An :class:`~idfkit.document.IDFDocument` typed for EnergyPlus 26.1.0."""

    @overload
    def __getitem__(self, obj_type: Literal["Version"], /) -> IDFCollection[_g.Version]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SimulationControl"], /) -> IDFCollection[_g.SimulationControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PerformancePrecisionTradeoffs"], /
    ) -> IDFCollection[_g.PerformancePrecisionTradeoffs]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Building"], /) -> IDFCollection[_v.Building_v22_2_to_v26_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ShadowCalculation"], /) -> IDFCollection[_g.ShadowCalculation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmInside]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmOutside]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HeatBalanceAlgorithm"], /) -> IDFCollection[_g.HeatBalanceAlgorithm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatBalanceSettings:ConductionFiniteDifference"], /
    ) -> IDFCollection[_g.HeatBalanceSettingsConductionFiniteDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirHeatBalanceAlgorithm"], /
    ) -> IDFCollection[_g.ZoneAirHeatBalanceAlgorithm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirContaminantBalance"], /
    ) -> IDFCollection[_g.ZoneAirContaminantBalance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirMassFlowConservation"], /
    ) -> IDFCollection[_g.ZoneAirMassFlowConservation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneCapacitanceMultiplier:ResearchSpecial"], /
    ) -> IDFCollection[_g.ZoneCapacitanceMultiplierResearchSpecial]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Timestep"], /) -> IDFCollection[_g.Timestep]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ConvergenceLimits"], /) -> IDFCollection[_g.ConvergenceLimits]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACSystemRootFindingAlgorithm"], /
    ) -> IDFCollection[_g.HVACSystemRootFindingAlgorithm]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Compliance:Building"], /) -> IDFCollection[_g.ComplianceBuilding]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:Location"], /) -> IDFCollection[_g.SiteLocation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:VariableLocation"], /) -> IDFCollection[_g.SiteVariableLocation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SizingPeriod:DesignDay"], /
    ) -> IDFCollection[_g.SizingPeriodDesignDay]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SizingPeriod:WeatherFileDays"], /
    ) -> IDFCollection[_g.SizingPeriodWeatherFileDays]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SizingPeriod:WeatherFileConditionType"], /
    ) -> IDFCollection[_g.SizingPeriodWeatherFileConditionType]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RunPeriod"], /) -> IDFCollection[_g.RunPeriod]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RunPeriodControl:SpecialDays"], /
    ) -> IDFCollection[_g.RunPeriodControlSpecialDays]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RunPeriodControl:DaylightSavingTime"], /
    ) -> IDFCollection[_g.RunPeriodControlDaylightSavingTime]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WeatherProperty:SkyTemperature"], /
    ) -> IDFCollection[_g.WeatherPropertySkyTemperature]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:WeatherStation"], /) -> IDFCollection[_g.SiteWeatherStation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:HeightVariation"], /) -> IDFCollection[_g.SiteHeightVariation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:BuildingSurface"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureBuildingSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:FCfactorMethod"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureFCfactorMethod]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Shallow"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureShallow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Deep"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureDeep]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:FiniteDifference"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureUndisturbedFiniteDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:KusudaAchenbach"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureUndisturbedKusudaAchenbach]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:Xing"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureUndisturbedXing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:GroundDomain:Slab"], /) -> IDFCollection[_g.SiteGroundDomainSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundDomain:Basement"], /
    ) -> IDFCollection[_g.SiteGroundDomainBasement]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundReflectance"], /
    ) -> IDFCollection[_g.SiteGroundReflectance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundReflectance:SnowModifier"], /
    ) -> IDFCollection[_g.SiteGroundReflectanceSnowModifier]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:WaterMainsTemperature"], /
    ) -> IDFCollection[_g.SiteWaterMainsTemperature]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:Precipitation"], /) -> IDFCollection[_g.SitePrecipitation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoofIrrigation"], /) -> IDFCollection[_g.RoofIrrigation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:SolarAndVisibleSpectrum"], /
    ) -> IDFCollection[_g.SiteSolarAndVisibleSpectrum]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:SpectrumData"], /) -> IDFCollection[_g.SiteSpectrumData]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ScheduleTypeLimits"], /) -> IDFCollection[_g.ScheduleTypeLimits]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Day:Hourly"], /) -> IDFCollection[_g.ScheduleDayHourly]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Day:Interval"], /) -> IDFCollection[_g.ScheduleDayInterval]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Day:List"], /) -> IDFCollection[_g.ScheduleDayList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Week:Daily"], /) -> IDFCollection[_g.ScheduleWeekDaily]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Week:Compact"], /) -> IDFCollection[_g.ScheduleWeekCompact]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Year"], /) -> IDFCollection[_g.ScheduleYear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Compact"], /) -> IDFCollection[_g.ScheduleCompact]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Constant"], /) -> IDFCollection[_g.ScheduleConstant]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:File:Shading"], /) -> IDFCollection[_g.ScheduleFileShading]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:File"], /) -> IDFCollection[_g.ScheduleFile]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Material"], /) -> IDFCollection[_v.Material_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Material:NoMass"], /
    ) -> IDFCollection[_v.MaterialNoMass_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Material:InfraredTransparent"], /
    ) -> IDFCollection[_g.MaterialInfraredTransparent]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Material:AirGap"], /) -> IDFCollection[_g.MaterialAirGap]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Material:RoofVegetation"], /
    ) -> IDFCollection[_g.MaterialRoofVegetation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:SimpleGlazingSystem"], /
    ) -> IDFCollection[_g.WindowMaterialSimpleGlazingSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Glazing"], /
    ) -> IDFCollection[_g.WindowMaterialGlazing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:GlazingGroup:Thermochromic"], /
    ) -> IDFCollection[_g.WindowMaterialGlazingGroupThermochromic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Glazing:RefractionExtinctionMethod"], /
    ) -> IDFCollection[_g.WindowMaterialGlazingRefractionExtinctionMethod]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Gas"], /) -> IDFCollection[_g.WindowMaterialGas]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowGap:SupportPillar"], /
    ) -> IDFCollection[_g.WindowGapSupportPillar]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowGap:DeflectionState"], /
    ) -> IDFCollection[_g.WindowGapDeflectionState]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:GasMixture"], /
    ) -> IDFCollection[_g.WindowMaterialGasMixture]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Gap"], /) -> IDFCollection[_g.WindowMaterialGap]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Shade"], /) -> IDFCollection[_g.WindowMaterialShade]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:ComplexShade"], /
    ) -> IDFCollection[_g.WindowMaterialComplexShade]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Blind"], /) -> IDFCollection[_g.WindowMaterialBlind]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Screen"], /) -> IDFCollection[_g.WindowMaterialScreen]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Shade:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialShadeEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Drape:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialDrapeEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Blind:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialBlindEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Screen:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialScreenEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Glazing:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialGlazingEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Gap:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialGapEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:MoisturePenetrationDepth:Settings"], /
    ) -> IDFCollection[_g.MaterialPropertyMoisturePenetrationDepthSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:PhaseChange"], /
    ) -> IDFCollection[_g.MaterialPropertyPhaseChange]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:PhaseChangeHysteresis"], /
    ) -> IDFCollection[_g.MaterialPropertyPhaseChangeHysteresis]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:VariableThermalConductivity"], /
    ) -> IDFCollection[_g.MaterialPropertyVariableThermalConductivity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:VariableAbsorptance"], /
    ) -> IDFCollection[_v.MaterialPropertyVariableAbsorptance_v23_1_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Settings"], /
    ) -> IDFCollection[_g.MaterialPropertyHeatAndMoistureTransferSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:SorptionIsotherm"], /
    ) -> IDFCollection[_g.MaterialPropertyHeatAndMoistureTransferSorptionIsotherm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Suction"], /
    ) -> IDFCollection[_g.MaterialPropertyHeatAndMoistureTransferSuction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Redistribution"], /
    ) -> IDFCollection[_g.MaterialPropertyHeatAndMoistureTransferRedistribution]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Diffusion"], /
    ) -> IDFCollection[_g.MaterialPropertyHeatAndMoistureTransferDiffusion]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:ThermalConductivity"], /
    ) -> IDFCollection[_g.MaterialPropertyHeatAndMoistureTransferThermalConductivity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:GlazingSpectralData"], /
    ) -> IDFCollection[_g.MaterialPropertyGlazingSpectralData]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Construction"], /) -> IDFCollection[_g.Construction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:CfactorUndergroundWall"], /
    ) -> IDFCollection[_g.ConstructionCfactorUndergroundWall]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:FfactorGroundFloor"], /
    ) -> IDFCollection[_g.ConstructionFfactorGroundFloor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ConstructionProperty:InternalHeatSource"], /
    ) -> IDFCollection[_g.ConstructionPropertyInternalHeatSource]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:AirBoundary"], /
    ) -> IDFCollection[_g.ConstructionAirBoundary]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowThermalModel:Params"], /
    ) -> IDFCollection[_g.WindowThermalModelParams]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowsCalculationEngine"], /
    ) -> IDFCollection[_g.WindowsCalculationEngine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:ComplexFenestrationState"], /
    ) -> IDFCollection[_g.ConstructionComplexFenestrationState]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:WindowEquivalentLayer"], /
    ) -> IDFCollection[_g.ConstructionWindowEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:WindowDataFile"], /
    ) -> IDFCollection[_g.ConstructionWindowDataFile]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GlobalGeometryRules"], /) -> IDFCollection[_g.GlobalGeometryRules]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GeometryTransform"], /) -> IDFCollection[_g.GeometryTransform]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Space"], /) -> IDFCollection[_v.Space_v22_2_to_v26_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SpaceList"], /) -> IDFCollection[_g.SpaceList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Zone"], /) -> IDFCollection[_g.Zone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneList"], /) -> IDFCollection[_g.ZoneList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneGroup"], /) -> IDFCollection[_g.ZoneGroup]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["BuildingSurface:Detailed"], /
    ) -> IDFCollection[_v.BuildingSurfaceDetailed_v25_1_to_v26_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Detailed"], /) -> IDFCollection[_g.WallDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoofCeiling:Detailed"], /) -> IDFCollection[_g.RoofCeilingDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Detailed"], /) -> IDFCollection[_g.FloorDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Exterior"], /) -> IDFCollection[_g.WallExterior]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Adiabatic"], /) -> IDFCollection[_g.WallAdiabatic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Underground"], /) -> IDFCollection[_g.WallUnderground]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Interzone"], /) -> IDFCollection[_g.WallInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Roof"], /) -> IDFCollection[_g.Roof]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Ceiling:Adiabatic"], /) -> IDFCollection[_g.CeilingAdiabatic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Ceiling:Interzone"], /) -> IDFCollection[_g.CeilingInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:GroundContact"], /) -> IDFCollection[_g.FloorGroundContact]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Adiabatic"], /) -> IDFCollection[_g.FloorAdiabatic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Interzone"], /) -> IDFCollection[_g.FloorInterzone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FenestrationSurface:Detailed"], /
    ) -> IDFCollection[_v.FenestrationSurfaceDetailed_v9_0_to_v26_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Window"], /) -> IDFCollection[_g.Window]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Door"], /) -> IDFCollection[_g.Door]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GlazedDoor"], /) -> IDFCollection[_g.GlazedDoor]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Window:Interzone"], /) -> IDFCollection[_g.WindowInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Door:Interzone"], /) -> IDFCollection[_g.DoorInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GlazedDoor:Interzone"], /) -> IDFCollection[_g.GlazedDoorInterzone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowShadingControl"], /) -> IDFCollection[_g.WindowShadingControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:FrameAndDivider"], /
    ) -> IDFCollection[_v.WindowPropertyFrameAndDivider_v22_1_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:AirflowControl"], /
    ) -> IDFCollection[_g.WindowPropertyAirflowControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:StormWindow"], /
    ) -> IDFCollection[_g.WindowPropertyStormWindow]: ...
    @overload
    def __getitem__(self, obj_type: Literal["InternalMass"], /) -> IDFCollection[_v.InternalMass_v24_2_to_v26_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Site"], /) -> IDFCollection[_g.ShadingSite]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Building"], /) -> IDFCollection[_g.ShadingBuilding]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Site:Detailed"], /) -> IDFCollection[_g.ShadingSiteDetailed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Shading:Building:Detailed"], /
    ) -> IDFCollection[_g.ShadingBuildingDetailed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Overhang"], /) -> IDFCollection[_g.ShadingOverhang]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Shading:Overhang:Projection"], /
    ) -> IDFCollection[_g.ShadingOverhangProjection]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Fin"], /) -> IDFCollection[_g.ShadingFin]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Fin:Projection"], /) -> IDFCollection[_g.ShadingFinProjection]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Zone:Detailed"], /) -> IDFCollection[_g.ShadingZoneDetailed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ShadingProperty:Reflectance"], /
    ) -> IDFCollection[_g.ShadingPropertyReflectance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatTransferAlgorithm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:MultipleSurface"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatTransferAlgorithmMultipleSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:SurfaceList"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatTransferAlgorithmSurfaceList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:Construction"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatTransferAlgorithmConstruction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatBalanceSourceTerm"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatBalanceSourceTerm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceControl:MovableInsulation"], /
    ) -> IDFCollection[_g.SurfaceControlMovableInsulation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:OtherSideCoefficients"], /
    ) -> IDFCollection[_g.SurfacePropertyOtherSideCoefficients]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:OtherSideConditionsModel"], /
    ) -> IDFCollection[_g.SurfacePropertyOtherSideConditionsModel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:Underwater"], /
    ) -> IDFCollection[_g.SurfacePropertyUnderwater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Foundation:Kiva"], /) -> IDFCollection[_g.FoundationKiva]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Foundation:Kiva:Settings"], /
    ) -> IDFCollection[_g.FoundationKivaSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ExposedFoundationPerimeter"], /
    ) -> IDFCollection[_g.SurfacePropertyExposedFoundationPerimeter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside:AdaptiveModelSelections"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmInsideAdaptiveModelSelections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside:AdaptiveModelSelections"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside:UserCurve"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmInsideUserCurve]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside:UserCurve"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmOutsideUserCurve]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ConvectionCoefficients"], /
    ) -> IDFCollection[_g.SurfacePropertyConvectionCoefficients]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ConvectionCoefficients:MultipleSurface"], /
    ) -> IDFCollection[_g.SurfacePropertyConvectionCoefficientsMultipleSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperties:VaporCoefficients"], /
    ) -> IDFCollection[_g.SurfacePropertiesVaporCoefficients]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ExteriorNaturalVentedCavity"], /
    ) -> IDFCollection[_g.SurfacePropertyExteriorNaturalVentedCavity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:SolarIncidentInside"], /
    ) -> IDFCollection[_g.SurfacePropertySolarIncidentInside]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:IncidentSolarMultiplier"], /
    ) -> IDFCollection[_g.SurfacePropertyIncidentSolarMultiplier]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:LocalEnvironment"], /
    ) -> IDFCollection[_g.SurfacePropertyLocalEnvironment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneProperty:LocalEnvironment"], /
    ) -> IDFCollection[_g.ZonePropertyLocalEnvironment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:SurroundingSurfaces"], /
    ) -> IDFCollection[_v.SurfacePropertySurroundingSurfaces_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:GroundSurfaces"], /
    ) -> IDFCollection[_g.SurfacePropertyGroundSurfaces]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComplexFenestrationProperty:SolarAbsorbedLayers"], /
    ) -> IDFCollection[_g.ComplexFenestrationPropertySolarAbsorbedLayers]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneProperty:UserViewFactors:BySurfaceName"], /
    ) -> IDFCollection[_g.ZonePropertyUserViewFactorsBySurfaceName]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Control"], /
    ) -> IDFCollection[_g.GroundHeatTransferControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:Materials"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabMaterials]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:MatlProps"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabMatlProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:BoundConds"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabBoundConds]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:BldgProps"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabBldgProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:Insulation"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabInsulation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:EquivalentSlab"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabEquivalentSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:AutoGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabAutoGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:ManualGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabManualGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:XFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabXFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:YFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabYFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:ZFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabZFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:SimParameters"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementSimParameters]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:MatlProps"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementMatlProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:Insulation"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementInsulation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:SurfaceProps"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementSurfaceProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:BldgData"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementBldgData]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:Interior"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementInterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ComBldg"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementComBldg]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:EquivSlab"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementEquivSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:EquivAutoGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementEquivAutoGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:AutoGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementAutoGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ManualGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementManualGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:XFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementXFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:YFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementYFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ZFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementZFACE]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoomAirModelType"], /) -> IDFCollection[_g.RoomAirModelType]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:UserDefined"], /
    ) -> IDFCollection[_g.RoomAirTemperaturePatternUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:ConstantGradient"], /
    ) -> IDFCollection[_g.RoomAirTemperaturePatternConstantGradient]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:TwoGradient"], /
    ) -> IDFCollection[_g.RoomAirTemperaturePatternTwoGradient]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:NondimensionalHeight"], /
    ) -> IDFCollection[_g.RoomAirTemperaturePatternNondimensionalHeight]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:SurfaceMapping"], /
    ) -> IDFCollection[_g.RoomAirTemperaturePatternSurfaceMapping]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoomAir:Node"], /) -> IDFCollection[_g.RoomAirNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:OneNodeDisplacementVentilation"], /
    ) -> IDFCollection[_g.RoomAirSettingsOneNodeDisplacementVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:ThreeNodeDisplacementVentilation"], /
    ) -> IDFCollection[_g.RoomAirSettingsThreeNodeDisplacementVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:CrossVentilation"], /
    ) -> IDFCollection[_g.RoomAirSettingsCrossVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:UnderFloorAirDistributionInterior"], /
    ) -> IDFCollection[_g.RoomAirSettingsUnderFloorAirDistributionInterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:UnderFloorAirDistributionExterior"], /
    ) -> IDFCollection[_g.RoomAirSettingsUnderFloorAirDistributionExterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork"], /
    ) -> IDFCollection[_g.RoomAirNodeAirflowNetwork]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:AdjacentSurfaceList"], /
    ) -> IDFCollection[_g.RoomAirNodeAirflowNetworkAdjacentSurfaceList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:InternalGains"], /
    ) -> IDFCollection[_g.RoomAirNodeAirflowNetworkInternalGains]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:HVACEquipment"], /
    ) -> IDFCollection[_g.RoomAirNodeAirflowNetworkHVACEquipment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:AirflowNetwork"], /
    ) -> IDFCollection[_g.RoomAirSettingsAirflowNetwork]: ...
    @overload
    def __getitem__(self, obj_type: Literal["People"], /) -> IDFCollection[_g.People]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComfortViewFactorAngles"], /
    ) -> IDFCollection[_g.ComfortViewFactorAngles]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Lights"], /) -> IDFCollection[_g.Lights]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ElectricEquipment"], /) -> IDFCollection[_g.ElectricEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GasEquipment"], /) -> IDFCollection[_g.GasEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HotWaterEquipment"], /) -> IDFCollection[_g.HotWaterEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SteamEquipment"], /) -> IDFCollection[_g.SteamEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OtherEquipment"], /) -> IDFCollection[_g.OtherEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["IndoorLivingWall"], /) -> IDFCollection[_g.IndoorLivingWall]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricEquipment:ITE:AirCooled"], /
    ) -> IDFCollection[_g.ElectricEquipmentITEAirCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneBaseboard:OutdoorTemperatureControlled"], /
    ) -> IDFCollection[_v.ZoneBaseboardOutdoorTemperatureControlled_v9_6_to_v26_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SwimmingPool:Indoor"], /) -> IDFCollection[_g.SwimmingPoolIndoor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:CarbonDioxide"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkCarbonDioxide]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:Constant"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkGenericConstant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:PressureDriven"], /
    ) -> IDFCollection[_g.SurfaceContaminantSourceAndSinkGenericPressureDriven]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:CutoffModel"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkGenericCutoffModel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:DecaySource"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkGenericDecaySource]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:BoundaryLayerDiffusion"], /
    ) -> IDFCollection[_g.SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:DepositionVelocitySink"], /
    ) -> IDFCollection[_g.SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:DepositionRateSink"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkGenericDepositionRateSink]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Daylighting:Controls"], /) -> IDFCollection[_g.DaylightingControls]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Daylighting:ReferencePoint"], /
    ) -> IDFCollection[_g.DaylightingReferencePoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Daylighting:DELight:ComplexFenestration"], /
    ) -> IDFCollection[_g.DaylightingDELightComplexFenestration]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DaylightingDevice:Tubular"], /
    ) -> IDFCollection[_g.DaylightingDeviceTubular]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DaylightingDevice:Shelf"], /
    ) -> IDFCollection[_g.DaylightingDeviceShelf]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DaylightingDevice:LightWell"], /
    ) -> IDFCollection[_g.DaylightingDeviceLightWell]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:DaylightFactors"], /
    ) -> IDFCollection[_g.OutputDaylightFactors]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:IlluminanceMap"], /) -> IDFCollection[_g.OutputIlluminanceMap]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:IlluminanceMap:Style"], /
    ) -> IDFCollection[_g.OutputControlIlluminanceMapStyle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:DesignFlowRate"], /
    ) -> IDFCollection[_g.ZoneInfiltrationDesignFlowRate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:EffectiveLeakageArea"], /
    ) -> IDFCollection[_g.ZoneInfiltrationEffectiveLeakageArea]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:FlowCoefficient"], /
    ) -> IDFCollection[_g.ZoneInfiltrationFlowCoefficient]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneVentilation:DesignFlowRate"], /
    ) -> IDFCollection[_g.ZoneVentilationDesignFlowRate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneVentilation:WindandStackOpenArea"], /
    ) -> IDFCollection[_g.ZoneVentilationWindandStackOpenArea]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirBalance:OutdoorAir"], /
    ) -> IDFCollection[_g.ZoneAirBalanceOutdoorAir]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneMixing"], /) -> IDFCollection[_g.ZoneMixing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneCrossMixing"], /) -> IDFCollection[_g.ZoneCrossMixing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneRefrigerationDoorMixing"], /
    ) -> IDFCollection[_g.ZoneRefrigerationDoorMixing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneEarthtube"], /) -> IDFCollection[_g.ZoneEarthtube]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneEarthtube:Parameters"], /
    ) -> IDFCollection[_g.ZoneEarthtubeParameters]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneCoolTower:Shower"], /) -> IDFCollection[_g.ZoneCoolTowerShower]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneThermalChimney"], /) -> IDFCollection[_g.ZoneThermalChimney]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:SimulationControl"], /
    ) -> IDFCollection[_g.AirflowNetworkSimulationControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Zone"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneZone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:ReferenceCrackConditions"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneReferenceCrackConditions]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface:Crack"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneSurfaceCrack]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface:EffectiveLeakageArea"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:SpecifiedFlowRate"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneSpecifiedFlowRate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:DetailedOpening"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneComponentDetailedOpening]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:SimpleOpening"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneComponentSimpleOpening]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:HorizontalOpening"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneComponentHorizontalOpening]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:ZoneExhaustFan"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneComponentZoneExhaustFan]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:ExternalNode"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneExternalNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:WindPressureCoefficientArray"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneWindPressureCoefficientArray]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:WindPressureCoefficientValues"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneWindPressureCoefficientValues]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:ZoneControl:PressureController"], /
    ) -> IDFCollection[_g.AirflowNetworkZoneControlPressureController]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Node"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Leak"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentLeak]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:LeakageRatio"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentLeakageRatio]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Duct"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentDuct]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Fan"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentFan]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Coil"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:HeatExchanger"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentHeatExchanger]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:TerminalUnit"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentTerminalUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:ConstantPressureDrop"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentConstantPressureDrop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:OutdoorAirFlow"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentOutdoorAirFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:ReliefAirFlow"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentReliefAirFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Linkage"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionLinkage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:DuctViewFactors"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionDuctViewFactors]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:DuctSizing"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionDuctSizing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:OccupantVentilationControl"], /
    ) -> IDFCollection[_g.AirflowNetworkOccupantVentilationControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:IntraZone:Node"], /
    ) -> IDFCollection[_g.AirflowNetworkIntraZoneNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:IntraZone:Linkage"], /
    ) -> IDFCollection[_g.AirflowNetworkIntraZoneLinkage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct:Loss:Conduction"], /) -> IDFCollection[_g.DuctLossConduction]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct:Loss:Leakage"], /) -> IDFCollection[_g.DuctLossLeakage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct:Loss:MakeupAir"], /) -> IDFCollection[_g.DuctLossMakeupAir]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Exterior:Lights"], /) -> IDFCollection[_g.ExteriorLights]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Exterior:FuelEquipment"], /
    ) -> IDFCollection[_g.ExteriorFuelEquipment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Exterior:WaterEquipment"], /
    ) -> IDFCollection[_g.ExteriorWaterEquipment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Thermostat"], /
    ) -> IDFCollection[_g.HVACTemplateThermostat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:IdealLoadsAirSystem"], /
    ) -> IDFCollection[_g.HVACTemplateZoneIdealLoadsAirSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:BaseboardHeat"], /
    ) -> IDFCollection[_g.HVACTemplateZoneBaseboardHeat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:FanCoil"], /
    ) -> IDFCollection[_g.HVACTemplateZoneFanCoil]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:PTAC"], /) -> IDFCollection[_g.HVACTemplateZonePTAC]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:PTHP"], /) -> IDFCollection[_g.HVACTemplateZonePTHP]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:WaterToAirHeatPump"], /
    ) -> IDFCollection[_g.HVACTemplateZoneWaterToAirHeatPump]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:VRF"], /) -> IDFCollection[_g.HVACTemplateZoneVRF]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:Unitary"], /
    ) -> IDFCollection[_g.HVACTemplateZoneUnitary]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:VAV"], /) -> IDFCollection[_g.HVACTemplateZoneVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:VAV:FanPowered"], /
    ) -> IDFCollection[_g.HVACTemplateZoneVAVFanPowered]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:VAV:HeatAndCool"], /
    ) -> IDFCollection[_g.HVACTemplateZoneVAVHeatAndCool]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:ConstantVolume"], /
    ) -> IDFCollection[_g.HVACTemplateZoneConstantVolume]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:DualDuct"], /
    ) -> IDFCollection[_g.HVACTemplateZoneDualDuct]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:VRF"], /
    ) -> IDFCollection[_g.HVACTemplateSystemVRF]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:Unitary"], /
    ) -> IDFCollection[_g.HVACTemplateSystemUnitary]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:UnitaryHeatPump:AirToAir"], /
    ) -> IDFCollection[_g.HVACTemplateSystemUnitaryHeatPumpAirToAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:UnitarySystem"], /
    ) -> IDFCollection[_g.HVACTemplateSystemUnitarySystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:VAV"], /
    ) -> IDFCollection[_g.HVACTemplateSystemVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:PackagedVAV"], /
    ) -> IDFCollection[_g.HVACTemplateSystemPackagedVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:ConstantVolume"], /
    ) -> IDFCollection[_g.HVACTemplateSystemConstantVolume]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:DualDuct"], /
    ) -> IDFCollection[_g.HVACTemplateSystemDualDuct]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:DedicatedOutdoorAir"], /
    ) -> IDFCollection[_g.HVACTemplateSystemDedicatedOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:ChilledWaterLoop"], /
    ) -> IDFCollection[_g.HVACTemplatePlantChilledWaterLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Chiller"], /
    ) -> IDFCollection[_g.HVACTemplatePlantChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Chiller:ObjectReference"], /
    ) -> IDFCollection[_g.HVACTemplatePlantChillerObjectReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Tower"], /
    ) -> IDFCollection[_g.HVACTemplatePlantTower]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Tower:ObjectReference"], /
    ) -> IDFCollection[_g.HVACTemplatePlantTowerObjectReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:HotWaterLoop"], /
    ) -> IDFCollection[_g.HVACTemplatePlantHotWaterLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Boiler"], /
    ) -> IDFCollection[_g.HVACTemplatePlantBoiler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Boiler:ObjectReference"], /
    ) -> IDFCollection[_g.HVACTemplatePlantBoilerObjectReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:MixedWaterLoop"], /
    ) -> IDFCollection[_g.HVACTemplatePlantMixedWaterLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:OutdoorAir"], /
    ) -> IDFCollection[_g.DesignSpecificationOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:OutdoorAir:SpaceList"], /
    ) -> IDFCollection[_g.DesignSpecificationOutdoorAirSpaceList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:ZoneAirDistribution"], /
    ) -> IDFCollection[_g.DesignSpecificationZoneAirDistribution]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:Parameters"], /) -> IDFCollection[_g.SizingParameters]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:Zone"], /) -> IDFCollection[_g.SizingZone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:ZoneHVAC:Sizing"], /
    ) -> IDFCollection[_g.DesignSpecificationZoneHVACSizing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:AirTerminal:Sizing"], /
    ) -> IDFCollection[_g.DesignSpecificationAirTerminalSizing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:System"], /) -> IDFCollection[_g.SizingSystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:Plant"], /) -> IDFCollection[_g.SizingPlant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:Sizing:Style"], /
    ) -> IDFCollection[_g.OutputControlSizingStyle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Humidistat"], /
    ) -> IDFCollection[_v.ZoneControlHumidistat_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat"], /
    ) -> IDFCollection[_g.ZoneControlThermostat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:OperativeTemperature"], /
    ) -> IDFCollection[_g.ZoneControlThermostatOperativeTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:ThermalComfort"], /
    ) -> IDFCollection[_g.ZoneControlThermostatThermalComfort]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:TemperatureAndHumidity"], /
    ) -> IDFCollection[_g.ZoneControlThermostatTemperatureAndHumidity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleHeating"], /
    ) -> IDFCollection[_g.ThermostatSetpointSingleHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleCooling"], /
    ) -> IDFCollection[_g.ThermostatSetpointSingleCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleHeatingOrCooling"], /
    ) -> IDFCollection[_g.ThermostatSetpointSingleHeatingOrCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:DualSetpoint"], /
    ) -> IDFCollection[_g.ThermostatSetpointDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating"], /
    ) -> IDFCollection[_g.ThermostatSetpointThermalComfortFangerSingleHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling"], /
    ) -> IDFCollection[_g.ThermostatSetpointThermalComfortFangerSingleCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling"], /
    ) -> IDFCollection[_g.ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint"], /
    ) -> IDFCollection[_g.ThermostatSetpointThermalComfortFangerDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:StagedDualSetpoint"], /
    ) -> IDFCollection[_g.ZoneControlThermostatStagedDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:ContaminantController"], /
    ) -> IDFCollection[_v.ZoneControlContaminantController_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:IdealLoadsAirSystem"], /
    ) -> IDFCollection[_g.ZoneHVACIdealLoadsAirSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:FourPipeFanCoil"], /
    ) -> IDFCollection[_g.ZoneHVACFourPipeFanCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:WindowAirConditioner"], /
    ) -> IDFCollection[_g.ZoneHVACWindowAirConditioner]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:PackagedTerminalAirConditioner"], /
    ) -> IDFCollection[_g.ZoneHVACPackagedTerminalAirConditioner]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:PackagedTerminalHeatPump"], /
    ) -> IDFCollection[_g.ZoneHVACPackagedTerminalHeatPump]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:WaterToAirHeatPump"], /
    ) -> IDFCollection[_g.ZoneHVACWaterToAirHeatPump]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Dehumidifier:DX"], /
    ) -> IDFCollection[_g.ZoneHVACDehumidifierDX]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EnergyRecoveryVentilator"], /
    ) -> IDFCollection[_g.ZoneHVACEnergyRecoveryVentilator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EnergyRecoveryVentilator:Controller"], /
    ) -> IDFCollection[_g.ZoneHVACEnergyRecoveryVentilatorController]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:UnitVentilator"], /
    ) -> IDFCollection[_g.ZoneHVACUnitVentilator]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:UnitHeater"], /) -> IDFCollection[_g.ZoneHVACUnitHeater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EvaporativeCoolerUnit"], /
    ) -> IDFCollection[_g.ZoneHVACEvaporativeCoolerUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:HybridUnitaryHVAC"], /
    ) -> IDFCollection[_g.ZoneHVACHybridUnitaryHVAC]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:OutdoorAirUnit"], /
    ) -> IDFCollection[_g.ZoneHVACOutdoorAirUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:OutdoorAirUnit:EquipmentList"], /
    ) -> IDFCollection[_g.ZoneHVACOutdoorAirUnitEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:TerminalUnit:VariableRefrigerantFlow"], /
    ) -> IDFCollection[_g.ZoneHVACTerminalUnitVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Water:Design"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardRadiantConvectiveWaterDesign]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Water"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardRadiantConvectiveWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Steam:Design"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardRadiantConvectiveSteamDesign]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Steam"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardRadiantConvectiveSteam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Electric"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardRadiantConvectiveElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:CoolingPanel:RadiantConvective:Water"], /
    ) -> IDFCollection[_g.ZoneHVACCoolingPanelRadiantConvectiveWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:Convective:Water"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardConvectiveWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:Convective:Electric"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardConvectiveElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:VariableFlow"], /
    ) -> IDFCollection[_g.ZoneHVACLowTemperatureRadiantVariableFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design"], /
    ) -> IDFCollection[_g.ZoneHVACLowTemperatureRadiantVariableFlowDesign]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:ConstantFlow"], /
    ) -> IDFCollection[_g.ZoneHVACLowTemperatureRadiantConstantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design"], /
    ) -> IDFCollection[_g.ZoneHVACLowTemperatureRadiantConstantFlowDesign]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:Electric"], /
    ) -> IDFCollection[_g.ZoneHVACLowTemperatureRadiantElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:SurfaceGroup"], /
    ) -> IDFCollection[_g.ZoneHVACLowTemperatureRadiantSurfaceGroup]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:HighTemperatureRadiant"], /
    ) -> IDFCollection[_g.ZoneHVACHighTemperatureRadiant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:VentilatedSlab"], /
    ) -> IDFCollection[_g.ZoneHVACVentilatedSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:VentilatedSlab:SlabGroup"], /
    ) -> IDFCollection[_g.ZoneHVACVentilatedSlabSlabGroup]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:Reheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:NoReheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeNoReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:NoReheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctVAVNoReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:Reheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctVAVReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctVAVReheatVariableSpeedFan]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctVAVHeatAndCoolNoReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctVAVHeatAndCoolReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:SeriesPIU:Reheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctSeriesPIUReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ParallelPIU:Reheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctParallelPIUReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeFourPipeInduction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeFourPipeBeam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:CooledBeam"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeCooledBeam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:Mixer"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:DualDuct:ConstantVolume"], /
    ) -> IDFCollection[_g.AirTerminalDualDuctConstantVolume]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:DualDuct:VAV"], /
    ) -> IDFCollection[_g.AirTerminalDualDuctVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:DualDuct:VAV:OutdoorAir"], /
    ) -> IDFCollection[_g.AirTerminalDualDuctVAVOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:AirDistributionUnit"], /
    ) -> IDFCollection[_g.ZoneHVACAirDistributionUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:ExhaustControl"], /
    ) -> IDFCollection[_g.ZoneHVACExhaustControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EquipmentList"], /
    ) -> IDFCollection[_g.ZoneHVACEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EquipmentConnections"], /
    ) -> IDFCollection[_g.ZoneHVACEquipmentConnections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SpaceHVAC:EquipmentConnections"], /
    ) -> IDFCollection[_g.SpaceHVACEquipmentConnections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SpaceHVAC:ZoneEquipmentSplitter"], /
    ) -> IDFCollection[_g.SpaceHVACZoneEquipmentSplitter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SpaceHVAC:ZoneEquipmentMixer"], /
    ) -> IDFCollection[_g.SpaceHVACZoneEquipmentMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SpaceHVAC:ZoneReturnMixer"], /
    ) -> IDFCollection[_g.SpaceHVACZoneReturnMixer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:SystemModel"], /) -> IDFCollection[_g.FanSystemModel]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ConstantVolume"], /) -> IDFCollection[_g.FanConstantVolume]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:VariableVolume"], /) -> IDFCollection[_g.FanVariableVolume]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:OnOff"], /) -> IDFCollection[_g.FanOnOff]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ZoneExhaust"], /) -> IDFCollection[_g.FanZoneExhaust]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FanPerformance:NightVentilation"], /
    ) -> IDFCollection[_g.FanPerformanceNightVentilation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ComponentModel"], /) -> IDFCollection[_g.FanComponentModel]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Cooling:Water"], /) -> IDFCollection[_g.CoilCoolingWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:Water:DetailedGeometry"], /
    ) -> IDFCollection[_g.CoilCoolingWaterDetailedGeometry]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:Cooling:Water"], /
    ) -> IDFCollection[_g.CoilSystemCoolingWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Cooling:DX"], /) -> IDFCollection[_g.CoilCoolingDX]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:CurveFit:Performance"], /
    ) -> IDFCollection[_g.CoilCoolingDXCurveFitPerformance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:CurveFit:OperatingMode"], /
    ) -> IDFCollection[_v.CoilCoolingDXCurveFitOperatingMode_v22_2_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:CurveFit:Speed"], /
    ) -> IDFCollection[_g.CoilCoolingDXCurveFitSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:DX:ASHRAE205:Performance"], /
    ) -> IDFCollection[_g.CoilDXASHRAE205Performance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:SingleSpeed"], /
    ) -> IDFCollection[_g.CoilCoolingDXSingleSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:TwoSpeed"], /
    ) -> IDFCollection[_g.CoilCoolingDXTwoSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:MultiSpeed"], /
    ) -> IDFCollection[_g.CoilCoolingDXMultiSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableSpeed"], /
    ) -> IDFCollection[_g.CoilCoolingDXVariableSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:TwoStageWithHumidityControlMode"], /
    ) -> IDFCollection[_g.CoilCoolingDXTwoStageWithHumidityControlMode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilPerformance:DX:Cooling"], /
    ) -> IDFCollection[_g.CoilPerformanceDXCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableRefrigerantFlow"], /
    ) -> IDFCollection[_g.CoilCoolingDXVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableRefrigerantFlow"], /
    ) -> IDFCollection[_g.CoilHeatingDXVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"], /
    ) -> IDFCollection[_g.CoilCoolingDXVariableRefrigerantFlowFluidTemperatureControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"], /
    ) -> IDFCollection[_g.CoilHeatingDXVariableRefrigerantFlowFluidTemperatureControl]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Water"], /) -> IDFCollection[_g.CoilHeatingWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Steam"], /) -> IDFCollection[_g.CoilHeatingSteam]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Electric"], /) -> IDFCollection[_g.CoilHeatingElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Electric:MultiStage"], /
    ) -> IDFCollection[_g.CoilHeatingElectricMultiStage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Fuel"], /) -> IDFCollection[_g.CoilHeatingFuel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Gas:MultiStage"], /
    ) -> IDFCollection[_g.CoilHeatingGasMultiStage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Desuperheater"], /
    ) -> IDFCollection[_g.CoilHeatingDesuperheater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:SingleSpeed"], /
    ) -> IDFCollection[_g.CoilHeatingDXSingleSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:MultiSpeed"], /
    ) -> IDFCollection[_g.CoilHeatingDXMultiSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableSpeed"], /
    ) -> IDFCollection[_g.CoilHeatingDXVariableSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:ParameterEstimation"], /
    ) -> IDFCollection[_g.CoilCoolingWaterToAirHeatPumpParameterEstimation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:ParameterEstimation"], /
    ) -> IDFCollection[_g.CoilHeatingWaterToAirHeatPumpParameterEstimation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:EquationFit"], /
    ) -> IDFCollection[_g.CoilCoolingWaterToAirHeatPumpEquationFit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"], /
    ) -> IDFCollection[_g.CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:EquationFit"], /
    ) -> IDFCollection[_g.CoilHeatingWaterToAirHeatPumpEquationFit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"], /
    ) -> IDFCollection[_g.CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:Pumped"], /
    ) -> IDFCollection[_g.CoilWaterHeatingAirToWaterHeatPumpPumped]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:Wrapped"], /
    ) -> IDFCollection[_g.CoilWaterHeatingAirToWaterHeatPumpWrapped]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed"], /
    ) -> IDFCollection[_g.CoilWaterHeatingAirToWaterHeatPumpVariableSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:Desuperheater"], /
    ) -> IDFCollection[_g.CoilWaterHeatingDesuperheater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoilSystem:Cooling:DX"], /) -> IDFCollection[_g.CoilSystemCoolingDX]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoilSystem:Heating:DX"], /) -> IDFCollection[_g.CoilSystemHeatingDX]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:Cooling:Water:HeatExchangerAssisted"], /
    ) -> IDFCollection[_g.CoilSystemCoolingWaterHeatExchangerAssisted]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:Cooling:DX:HeatExchangerAssisted"], /
    ) -> IDFCollection[_g.CoilSystemCoolingDXHeatExchangerAssisted]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:IntegratedHeatPump:AirSource"], /
    ) -> IDFCollection[_g.CoilSystemIntegratedHeatPumpAirSource]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:SingleSpeed:ThermalStorage"], /
    ) -> IDFCollection[_g.CoilCoolingDXSingleSpeedThermalStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Direct:CelDekPad"], /
    ) -> IDFCollection[_g.EvaporativeCoolerDirectCelDekPad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:CelDekPad"], /
    ) -> IDFCollection[_g.EvaporativeCoolerIndirectCelDekPad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:WetCoil"], /
    ) -> IDFCollection[_g.EvaporativeCoolerIndirectWetCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:ResearchSpecial"], /
    ) -> IDFCollection[_g.EvaporativeCoolerIndirectResearchSpecial]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Direct:ResearchSpecial"], /
    ) -> IDFCollection[_g.EvaporativeCoolerDirectResearchSpecial]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Humidifier:Steam:Electric"], /
    ) -> IDFCollection[_g.HumidifierSteamElectric]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Humidifier:Steam:Gas"], /) -> IDFCollection[_g.HumidifierSteamGas]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Dehumidifier:Desiccant:NoFans"], /
    ) -> IDFCollection[_g.DehumidifierDesiccantNoFans]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Dehumidifier:Desiccant:System"], /
    ) -> IDFCollection[_g.DehumidifierDesiccantSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:AirToAir:FlatPlate"], /
    ) -> IDFCollection[_g.HeatExchangerAirToAirFlatPlate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:AirToAir:SensibleAndLatent"], /
    ) -> IDFCollection[_g.HeatExchangerAirToAirSensibleAndLatent]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:Desiccant:BalancedFlow"], /
    ) -> IDFCollection[_g.HeatExchangerDesiccantBalancedFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:Desiccant:BalancedFlow:PerformanceDataType1"], /
    ) -> IDFCollection[_g.HeatExchangerDesiccantBalancedFlowPerformanceDataType1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitarySystem"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitarySystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UnitarySystemPerformance:Multispeed"], /
    ) -> IDFCollection[_g.UnitarySystemPerformanceMultispeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:Unitary:Furnace:HeatOnly"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryFurnaceHeatOnly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:Unitary:Furnace:HeatCool"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryFurnaceHeatCool]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatOnly"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryHeatOnly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatCool"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryHeatCool]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:AirToAir"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryHeatPumpAirToAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:WaterToAir"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryHeatPumpWaterToAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow"], /
    ) -> IDFCollection[_g.AirConditionerVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl"], /
    ) -> IDFCollection[_g.AirConditionerVariableRefrigerantFlowFluidTemperatureControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR"], /
    ) -> IDFCollection[_g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneTerminalUnitList"], /) -> IDFCollection[_g.ZoneTerminalUnitList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Controller:WaterCoil"], /) -> IDFCollection[_g.ControllerWaterCoil]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Controller:OutdoorAir"], /) -> IDFCollection[_g.ControllerOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Controller:MechanicalVentilation"], /
    ) -> IDFCollection[_g.ControllerMechanicalVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ControllerList"], /
    ) -> IDFCollection[_g.AirLoopHVACControllerList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC"], /) -> IDFCollection[_g.AirLoopHVAC]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:OutdoorAirSystem:EquipmentList"], /
    ) -> IDFCollection[_g.AirLoopHVACOutdoorAirSystemEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:OutdoorAirSystem"], /
    ) -> IDFCollection[_g.AirLoopHVACOutdoorAirSystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:Mixer"], /) -> IDFCollection[_g.OutdoorAirMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ZoneSplitter"], /
    ) -> IDFCollection[_g.AirLoopHVACZoneSplitter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:SupplyPlenum"], /
    ) -> IDFCollection[_g.AirLoopHVACSupplyPlenum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:SupplyPath"], /
    ) -> IDFCollection[_g.AirLoopHVACSupplyPath]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:ZoneMixer"], /) -> IDFCollection[_g.AirLoopHVACZoneMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ReturnPlenum"], /
    ) -> IDFCollection[_g.AirLoopHVACReturnPlenum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ReturnPath"], /
    ) -> IDFCollection[_g.AirLoopHVACReturnPath]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ExhaustSystem"], /
    ) -> IDFCollection[_g.AirLoopHVACExhaustSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:DedicatedOutdoorAirSystem"], /
    ) -> IDFCollection[_g.AirLoopHVACDedicatedOutdoorAirSystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:Mixer"], /) -> IDFCollection[_g.AirLoopHVACMixer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:Splitter"], /) -> IDFCollection[_g.AirLoopHVACSplitter]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Branch"], /) -> IDFCollection[_g.Branch]: ...
    @overload
    def __getitem__(self, obj_type: Literal["BranchList"], /) -> IDFCollection[_g.BranchList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Connector:Splitter"], /) -> IDFCollection[_g.ConnectorSplitter]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Connector:Mixer"], /) -> IDFCollection[_g.ConnectorMixer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ConnectorList"], /) -> IDFCollection[_g.ConnectorList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["NodeList"], /) -> IDFCollection[_g.NodeList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:Node"], /) -> IDFCollection[_g.OutdoorAirNode]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:NodeList"], /) -> IDFCollection[_g.OutdoorAirNodeList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Adiabatic"], /) -> IDFCollection[_g.PipeAdiabatic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Adiabatic:Steam"], /) -> IDFCollection[_g.PipeAdiabaticSteam]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Indoor"], /) -> IDFCollection[_g.PipeIndoor]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Outdoor"], /) -> IDFCollection[_g.PipeOutdoor]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Underground"], /) -> IDFCollection[_g.PipeUnderground]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:Domain"], /
    ) -> IDFCollection[_g.PipingSystemUndergroundDomain]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:PipeCircuit"], /
    ) -> IDFCollection[_g.PipingSystemUndergroundPipeCircuit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:PipeSegment"], /
    ) -> IDFCollection[_g.PipingSystemUndergroundPipeSegment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct"], /) -> IDFCollection[_g.Duct]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pump:VariableSpeed"], /) -> IDFCollection[_g.PumpVariableSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pump:ConstantSpeed"], /) -> IDFCollection[_g.PumpConstantSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Pump:VariableSpeed:Condensate"], /
    ) -> IDFCollection[_g.PumpVariableSpeedCondensate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeaderedPumps:ConstantSpeed"], /
    ) -> IDFCollection[_g.HeaderedPumpsConstantSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeaderedPumps:VariableSpeed"], /
    ) -> IDFCollection[_g.HeaderedPumpsVariableSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["TemperingValve"], /) -> IDFCollection[_g.TemperingValve]: ...
    @overload
    def __getitem__(self, obj_type: Literal["LoadProfile:Plant"], /) -> IDFCollection[_g.LoadProfilePlant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:FlatPlate"], /
    ) -> IDFCollection[_g.SolarCollectorPerformanceFlatPlate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:FlatPlate:Water"], /
    ) -> IDFCollection[_g.SolarCollectorFlatPlateWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:FlatPlate:PhotovoltaicThermal"], /
    ) -> IDFCollection[_g.SolarCollectorFlatPlatePhotovoltaicThermal]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:PhotovoltaicThermal:Simple"], /
    ) -> IDFCollection[_g.SolarCollectorPerformancePhotovoltaicThermalSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:PhotovoltaicThermal:BIPVT"], /
    ) -> IDFCollection[_g.SolarCollectorPerformancePhotovoltaicThermalBIPVT]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:IntegralCollectorStorage"], /
    ) -> IDFCollection[_g.SolarCollectorIntegralCollectorStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:IntegralCollectorStorage"], /
    ) -> IDFCollection[_g.SolarCollectorPerformanceIntegralCollectorStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:UnglazedTranspired"], /
    ) -> IDFCollection[_g.SolarCollectorUnglazedTranspired]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:UnglazedTranspired:Multisystem"], /
    ) -> IDFCollection[_g.SolarCollectorUnglazedTranspiredMultisystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Boiler:HotWater"], /) -> IDFCollection[_g.BoilerHotWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Boiler:Steam"], /) -> IDFCollection[_g.BoilerSteam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Electric:ASHRAE205"], /
    ) -> IDFCollection[_g.ChillerElectricASHRAE205]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:Electric:EIR"], /) -> IDFCollection[_g.ChillerElectricEIR]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Electric:ReformulatedEIR"], /
    ) -> IDFCollection[_g.ChillerElectricReformulatedEIR]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:Electric"], /) -> IDFCollection[_g.ChillerElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Absorption:Indirect"], /
    ) -> IDFCollection[_g.ChillerAbsorptionIndirect]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:Absorption"], /) -> IDFCollection[_g.ChillerAbsorption]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:ConstantCOP"], /) -> IDFCollection[_g.ChillerConstantCOP]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:EngineDriven"], /) -> IDFCollection[_g.ChillerEngineDriven]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:CombustionTurbine"], /
    ) -> IDFCollection[_g.ChillerCombustionTurbine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeater:Absorption:DirectFired"], /
    ) -> IDFCollection[_g.ChillerHeaterAbsorptionDirectFired]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeater:Absorption:DoubleEffect"], /
    ) -> IDFCollection[_g.ChillerHeaterAbsorptionDoubleEffect]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:PlantLoop:EIR:Cooling"], /
    ) -> IDFCollection[_g.HeatPumpPlantLoopEIRCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:PlantLoop:EIR:Heating"], /
    ) -> IDFCollection[_g.HeatPumpPlantLoopEIRHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:AirToWater:FuelFired:Heating"], /
    ) -> IDFCollection[_g.HeatPumpAirToWaterFuelFiredHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:AirToWater:FuelFired:Cooling"], /
    ) -> IDFCollection[_g.HeatPumpAirToWaterFuelFiredCooling]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HeatPump:AirToWater"], /) -> IDFCollection[_g.HeatPumpAirToWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:EquationFit:Heating"], /
    ) -> IDFCollection[_g.HeatPumpWaterToWaterEquationFitHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:EquationFit:Cooling"], /
    ) -> IDFCollection[_g.HeatPumpWaterToWaterEquationFitCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:ParameterEstimation:Cooling"], /
    ) -> IDFCollection[_g.HeatPumpWaterToWaterParameterEstimationCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:ParameterEstimation:Heating"], /
    ) -> IDFCollection[_g.HeatPumpWaterToWaterParameterEstimationHeating]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DistrictCooling"], /) -> IDFCollection[_g.DistrictCooling]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DistrictHeating:Water"], /) -> IDFCollection[_g.DistrictHeatingWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DistrictHeating:Steam"], /) -> IDFCollection[_g.DistrictHeatingSteam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantComponent:TemperatureSource"], /
    ) -> IDFCollection[_g.PlantComponentTemperatureSource]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CentralHeatPumpSystem"], /
    ) -> IDFCollection[_v.CentralHeatPumpSystem_v22_2_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeaterPerformance:Electric:EIR"], /
    ) -> IDFCollection[_v.ChillerHeaterPerformanceElectricEIR_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:SingleSpeed"], /
    ) -> IDFCollection[_g.CoolingTowerSingleSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoolingTower:TwoSpeed"], /) -> IDFCollection[_g.CoolingTowerTwoSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:VariableSpeed:Merkel"], /
    ) -> IDFCollection[_g.CoolingTowerVariableSpeedMerkel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:VariableSpeed"], /
    ) -> IDFCollection[_g.CoolingTowerVariableSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTowerPerformance:CoolTools"], /
    ) -> IDFCollection[_g.CoolingTowerPerformanceCoolTools]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTowerPerformance:YorkCalc"], /
    ) -> IDFCollection[_g.CoolingTowerPerformanceYorkCalc]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeFluidCooler:SingleSpeed"], /
    ) -> IDFCollection[_g.EvaporativeFluidCoolerSingleSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeFluidCooler:TwoSpeed"], /
    ) -> IDFCollection[_g.EvaporativeFluidCoolerTwoSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidCooler:SingleSpeed"], /
    ) -> IDFCollection[_g.FluidCoolerSingleSpeed]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FluidCooler:TwoSpeed"], /) -> IDFCollection[_g.FluidCoolerTwoSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:System"], /
    ) -> IDFCollection[_g.GroundHeatExchangerSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Sizing:Rectangle"], /
    ) -> IDFCollection[_g.GroundHeatExchangerVerticalSizingRectangle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Properties"], /
    ) -> IDFCollection[_g.GroundHeatExchangerVerticalProperties]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Array"], /
    ) -> IDFCollection[_g.GroundHeatExchangerVerticalArray]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Single"], /
    ) -> IDFCollection[_g.GroundHeatExchangerVerticalSingle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:ResponseFactors"], /
    ) -> IDFCollection[_g.GroundHeatExchangerResponseFactors]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Pond"], /
    ) -> IDFCollection[_g.GroundHeatExchangerPond]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Surface"], /
    ) -> IDFCollection[_g.GroundHeatExchangerSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:HorizontalTrench"], /
    ) -> IDFCollection[_g.GroundHeatExchangerHorizontalTrench]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Slinky"], /
    ) -> IDFCollection[_g.GroundHeatExchangerSlinky]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:FluidToFluid"], /
    ) -> IDFCollection[_g.HeatExchangerFluidToFluid]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterHeater:Mixed"], /) -> IDFCollection[_g.WaterHeaterMixed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:Stratified"], /
    ) -> IDFCollection[_g.WaterHeaterStratified]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterHeater:Sizing"], /) -> IDFCollection[_g.WaterHeaterSizing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:HeatPump:PumpedCondenser"], /
    ) -> IDFCollection[_g.WaterHeaterHeatPumpPumpedCondenser]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:HeatPump:WrappedCondenser"], /
    ) -> IDFCollection[_g.WaterHeaterHeatPumpWrappedCondenser]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:Ice:Simple"], /
    ) -> IDFCollection[_g.ThermalStorageIceSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:Ice:Detailed"], /
    ) -> IDFCollection[_g.ThermalStorageIceDetailed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:ChilledWater:Mixed"], /
    ) -> IDFCollection[_g.ThermalStorageChilledWaterMixed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:ChilledWater:Stratified"], /
    ) -> IDFCollection[_g.ThermalStorageChilledWaterStratified]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:HotWater:Stratified"], /
    ) -> IDFCollection[_g.ThermalStorageHotWaterStratified]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ThermalStorage:PCM"], /) -> IDFCollection[_g.ThermalStoragePCM]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ThermalStorage:Sizing"], /) -> IDFCollection[_g.ThermalStorageSizing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PlantLoop"], /) -> IDFCollection[_g.PlantLoop]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CondenserLoop"], /) -> IDFCollection[_g.CondenserLoop]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PlantEquipmentList"], /) -> IDFCollection[_g.PlantEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CondenserEquipmentList"], /
    ) -> IDFCollection[_g.CondenserEquipmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:Uncontrolled"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationUncontrolled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:CoolingLoad"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationCoolingLoad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:HeatingLoad"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationHeatingLoad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDryBulb"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorDryBulb]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorWetBulb"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorWetBulb]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorRelativeHumidity"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorRelativeHumidity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDewpoint"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorDewpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:ComponentSetpoint"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationComponentSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:ThermalEnergyStorage"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationThermalEnergyStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDryBulbDifference"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorDryBulbDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorWetBulbDifference"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorWetBulbDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDewpointDifference"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorDewpointDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:ChillerHeaterChangeover"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationChillerHeaterChangeover]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperationSchemes"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationSchemes]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CondenserEquipmentOperationSchemes"], /
    ) -> IDFCollection[_g.CondenserEquipmentOperationSchemes]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Sensor"], /
    ) -> IDFCollection[_g.EnergyManagementSystemSensor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Actuator"], /
    ) -> IDFCollection[_g.EnergyManagementSystemActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:ProgramCallingManager"], /
    ) -> IDFCollection[_g.EnergyManagementSystemProgramCallingManager]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Program"], /
    ) -> IDFCollection[_g.EnergyManagementSystemProgram]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Subroutine"], /
    ) -> IDFCollection[_g.EnergyManagementSystemSubroutine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:GlobalVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemGlobalVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:OutputVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemOutputVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:MeteredOutputVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemMeteredOutputVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:TrendVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemTrendVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:InternalVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemInternalVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:CurveOrTableIndexVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemCurveOrTableIndexVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:ConstructionIndexVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemConstructionIndexVariable]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ExternalInterface"], /) -> IDFCollection[_g.ExternalInterface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Schedule"], /
    ) -> IDFCollection[_g.ExternalInterfaceSchedule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Actuator"], /
    ) -> IDFCollection[_g.ExternalInterfaceActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImport]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:From:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImportFromVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Schedule"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImportToSchedule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Actuator"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImportToActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImportToVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:From:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitExportFromVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Schedule"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitExportToSchedule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Actuator"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitExportToActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitExportToVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:ForcedAir:UserDefined"], /
    ) -> IDFCollection[_g.ZoneHVACForcedAirUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:UserDefined"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctUserDefined]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:UserDefined"], /) -> IDFCollection[_g.CoilUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantComponent:UserDefined"], /
    ) -> IDFCollection[_g.PlantComponentUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:UserDefined"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:Scheduled"], /
    ) -> IDFCollection[_g.AvailabilityManagerScheduled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:ScheduledOn"], /
    ) -> IDFCollection[_g.AvailabilityManagerScheduledOn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:ScheduledOff"], /
    ) -> IDFCollection[_g.AvailabilityManagerScheduledOff]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:OptimumStart"], /
    ) -> IDFCollection[_g.AvailabilityManagerOptimumStart]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:NightCycle"], /
    ) -> IDFCollection[_g.AvailabilityManagerNightCycle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:DifferentialThermostat"], /
    ) -> IDFCollection[_g.AvailabilityManagerDifferentialThermostat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HighTemperatureTurnOff"], /
    ) -> IDFCollection[_g.AvailabilityManagerHighTemperatureTurnOff]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HighTemperatureTurnOn"], /
    ) -> IDFCollection[_g.AvailabilityManagerHighTemperatureTurnOn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:LowTemperatureTurnOff"], /
    ) -> IDFCollection[_g.AvailabilityManagerLowTemperatureTurnOff]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:LowTemperatureTurnOn"], /
    ) -> IDFCollection[_g.AvailabilityManagerLowTemperatureTurnOn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:NightVentilation"], /
    ) -> IDFCollection[_g.AvailabilityManagerNightVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HybridVentilation"], /
    ) -> IDFCollection[_g.AvailabilityManagerHybridVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManagerAssignmentList"], /
    ) -> IDFCollection[_g.AvailabilityManagerAssignmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Scheduled"], /
    ) -> IDFCollection[_g.SetpointManagerScheduled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Scheduled:DualSetpoint"], /
    ) -> IDFCollection[_g.SetpointManagerScheduledDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:OutdoorAirReset"], /
    ) -> IDFCollection[_g.SetpointManagerOutdoorAirReset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Reheat"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Heating"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Cooling"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Humidity:Minimum"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneHumidityMinimum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Humidity:Maximum"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneHumidityMaximum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MixedAir"], /
    ) -> IDFCollection[_g.SetpointManagerMixedAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:OutdoorAirPretreat"], /
    ) -> IDFCollection[_g.SetpointManagerOutdoorAirPretreat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Warmest"], /
    ) -> IDFCollection[_g.SetpointManagerWarmest]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Coldest"], /
    ) -> IDFCollection[_g.SetpointManagerColdest]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnAirBypassFlow"], /
    ) -> IDFCollection[_g.SetpointManagerReturnAirBypassFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:WarmestTemperatureFlow"], /
    ) -> IDFCollection[_g.SetpointManagerWarmestTemperatureFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Heating:Average"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneHeatingAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Cooling:Average"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneCoolingAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:MinimumHumidity:Average"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneMinimumHumidityAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:MaximumHumidity:Average"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneMaximumHumidityAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Humidity:Minimum"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneHumidityMinimum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Humidity:Maximum"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneHumidityMaximum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowOutdoorAirTemperature"], /
    ) -> IDFCollection[_g.SetpointManagerFollowOutdoorAirTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowSystemNodeTemperature"], /
    ) -> IDFCollection[_g.SetpointManagerFollowSystemNodeTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowGroundTemperature"], /
    ) -> IDFCollection[_g.SetpointManagerFollowGroundTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:CondenserEnteringReset"], /
    ) -> IDFCollection[_g.SetpointManagerCondenserEnteringReset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:CondenserEnteringReset:Ideal"], /
    ) -> IDFCollection[_g.SetpointManagerCondenserEnteringResetIdeal]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:OneStageCooling"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneOneStageCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:OneStageHeating"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneOneStageHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnTemperature:ChilledWater"], /
    ) -> IDFCollection[_g.SetpointManagerReturnTemperatureChilledWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnTemperature:HotWater"], /
    ) -> IDFCollection[_g.SetpointManagerReturnTemperatureHotWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SystemNodeReset:Temperature"], /
    ) -> IDFCollection[_g.SetpointManagerSystemNodeResetTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SystemNodeReset:Humidity"], /
    ) -> IDFCollection[_g.SetpointManagerSystemNodeResetHumidity]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:Case"], /) -> IDFCollection[_g.RefrigerationCase]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CompressorRack"], /
    ) -> IDFCollection[_g.RefrigerationCompressorRack]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CaseAndWalkInList"], /
    ) -> IDFCollection[_g.RefrigerationCaseAndWalkInList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:AirCooled"], /
    ) -> IDFCollection[_g.RefrigerationCondenserAirCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:EvaporativeCooled"], /
    ) -> IDFCollection[_g.RefrigerationCondenserEvaporativeCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:WaterCooled"], /
    ) -> IDFCollection[_g.RefrigerationCondenserWaterCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:Cascade"], /
    ) -> IDFCollection[_g.RefrigerationCondenserCascade]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:GasCooler:AirCooled"], /
    ) -> IDFCollection[_g.RefrigerationGasCoolerAirCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:TransferLoadList"], /
    ) -> IDFCollection[_g.RefrigerationTransferLoadList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Subcooler"], /
    ) -> IDFCollection[_g.RefrigerationSubcooler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Compressor"], /
    ) -> IDFCollection[_g.RefrigerationCompressor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CompressorList"], /
    ) -> IDFCollection[_g.RefrigerationCompressorList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:System"], /) -> IDFCollection[_g.RefrigerationSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:TranscriticalSystem"], /
    ) -> IDFCollection[_g.RefrigerationTranscriticalSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:SecondarySystem"], /
    ) -> IDFCollection[_g.RefrigerationSecondarySystem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:WalkIn"], /) -> IDFCollection[_g.RefrigerationWalkIn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:AirChiller"], /
    ) -> IDFCollection[_g.RefrigerationAirChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:RefrigerationChillerSet"], /
    ) -> IDFCollection[_g.ZoneHVACRefrigerationChillerSet]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManagerAssignmentList"], /
    ) -> IDFCollection[_g.DemandManagerAssignmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:ExteriorLights"], /
    ) -> IDFCollection[_g.DemandManagerExteriorLights]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DemandManager:Lights"], /) -> IDFCollection[_g.DemandManagerLights]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:ElectricEquipment"], /
    ) -> IDFCollection[_g.DemandManagerElectricEquipment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:Thermostats"], /
    ) -> IDFCollection[_g.DemandManagerThermostats]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:Ventilation"], /
    ) -> IDFCollection[_g.DemandManagerVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:InternalCombustionEngine"], /
    ) -> IDFCollection[_g.GeneratorInternalCombustionEngine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:CombustionTurbine"], /
    ) -> IDFCollection[_g.GeneratorCombustionTurbine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:MicroTurbine"], /
    ) -> IDFCollection[_g.GeneratorMicroTurbine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:Photovoltaic"], /
    ) -> IDFCollection[_g.GeneratorPhotovoltaic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:Simple"], /
    ) -> IDFCollection[_g.PhotovoltaicPerformanceSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:EquivalentOne-Diode"], /
    ) -> IDFCollection[_g.PhotovoltaicPerformanceEquivalentOneDiode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:Sandia"], /
    ) -> IDFCollection[_g.PhotovoltaicPerformanceSandia]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:PVWatts"], /) -> IDFCollection[_g.GeneratorPVWatts]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:PVWatts"], /
    ) -> IDFCollection[_g.ElectricLoadCenterInverterPVWatts]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:FuelCell"], /) -> IDFCollection[_g.GeneratorFuelCell]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:PowerModule"], /
    ) -> IDFCollection[_g.GeneratorFuelCellPowerModule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:AirSupply"], /
    ) -> IDFCollection[_g.GeneratorFuelCellAirSupply]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:WaterSupply"], /
    ) -> IDFCollection[_g.GeneratorFuelCellWaterSupply]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:AuxiliaryHeater"], /
    ) -> IDFCollection[_g.GeneratorFuelCellAuxiliaryHeater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:ExhaustGasToWaterHeatExchanger"], /
    ) -> IDFCollection[_g.GeneratorFuelCellExhaustGasToWaterHeatExchanger]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:ElectricalStorage"], /
    ) -> IDFCollection[_g.GeneratorFuelCellElectricalStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:Inverter"], /
    ) -> IDFCollection[_g.GeneratorFuelCellInverter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:StackCooler"], /
    ) -> IDFCollection[_g.GeneratorFuelCellStackCooler]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:MicroCHP"], /) -> IDFCollection[_g.GeneratorMicroCHP]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:MicroCHP:NonNormalizedParameters"], /
    ) -> IDFCollection[_g.GeneratorMicroCHPNonNormalizedParameters]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:FuelSupply"], /) -> IDFCollection[_g.GeneratorFuelSupply]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:WindTurbine"], /) -> IDFCollection[_g.GeneratorWindTurbine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Generators"], /
    ) -> IDFCollection[_g.ElectricLoadCenterGenerators]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:Simple"], /
    ) -> IDFCollection[_g.ElectricLoadCenterInverterSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:FunctionOfPower"], /
    ) -> IDFCollection[_g.ElectricLoadCenterInverterFunctionOfPower]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:LookUpTable"], /
    ) -> IDFCollection[_g.ElectricLoadCenterInverterLookUpTable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Simple"], /
    ) -> IDFCollection[_g.ElectricLoadCenterStorageSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Battery"], /
    ) -> IDFCollection[_g.ElectricLoadCenterStorageBattery]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:LiIonNMCBattery"], /
    ) -> IDFCollection[_g.ElectricLoadCenterStorageLiIonNMCBattery]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Transformer"], /
    ) -> IDFCollection[_g.ElectricLoadCenterTransformer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Distribution"], /
    ) -> IDFCollection[_g.ElectricLoadCenterDistribution]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Converter"], /
    ) -> IDFCollection[_g.ElectricLoadCenterStorageConverter]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Equipment"], /) -> IDFCollection[_g.WaterUseEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Connections"], /) -> IDFCollection[_g.WaterUseConnections]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Storage"], /) -> IDFCollection[_g.WaterUseStorage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Well"], /) -> IDFCollection[_g.WaterUseWell]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterUse:RainCollector"], /
    ) -> IDFCollection[_g.WaterUseRainCollector]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:OutdoorAir"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:HumiditySensorOffset:OutdoorAir"], /
    ) -> IDFCollection[_g.FaultModelHumiditySensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:EnthalpySensorOffset:OutdoorAir"], /
    ) -> IDFCollection[_g.FaultModelEnthalpySensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:ReturnAir"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetReturnAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:EnthalpySensorOffset:ReturnAir"], /
    ) -> IDFCollection[_g.FaultModelEnthalpySensorOffsetReturnAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:ChillerSupplyWater"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetChillerSupplyWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:CoilSupplyAir"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetCoilSupplyAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:CondenserSupplyWater"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetCondenserSupplyWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:ThermostatOffset"], /
    ) -> IDFCollection[_g.FaultModelThermostatOffset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:HumidistatOffset"], /
    ) -> IDFCollection[_g.FaultModelHumidistatOffset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:AirFilter"], /
    ) -> IDFCollection[_g.FaultModelFoulingAirFilter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:Boiler"], /
    ) -> IDFCollection[_g.FaultModelFoulingBoiler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:EvaporativeCooler"], /
    ) -> IDFCollection[_g.FaultModelFoulingEvaporativeCooler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:Chiller"], /
    ) -> IDFCollection[_g.FaultModelFoulingChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:CoolingTower"], /
    ) -> IDFCollection[_g.FaultModelFoulingCoolingTower]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:Coil"], /
    ) -> IDFCollection[_g.FaultModelFoulingCoil]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Matrix:TwoDimension"], /) -> IDFCollection[_g.MatrixTwoDimension]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HybridModel:Zone"], /) -> IDFCollection[_g.HybridModelZone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Linear"], /) -> IDFCollection[_g.CurveLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:QuadLinear"], /) -> IDFCollection[_g.CurveQuadLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:QuintLinear"], /) -> IDFCollection[_g.CurveQuintLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Quadratic"], /) -> IDFCollection[_g.CurveQuadratic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Cubic"], /) -> IDFCollection[_g.CurveCubic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Quartic"], /) -> IDFCollection[_g.CurveQuartic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Exponent"], /) -> IDFCollection[_g.CurveExponent]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Bicubic"], /) -> IDFCollection[_g.CurveBicubic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Biquadratic"], /) -> IDFCollection[_g.CurveBiquadratic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:QuadraticLinear"], /) -> IDFCollection[_g.CurveQuadraticLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:CubicLinear"], /) -> IDFCollection[_g.CurveCubicLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Triquadratic"], /) -> IDFCollection[_g.CurveTriquadratic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:Functional:PressureDrop"], /
    ) -> IDFCollection[_g.CurveFunctionalPressureDrop]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:FanPressureRise"], /) -> IDFCollection[_g.CurveFanPressureRise]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:ExponentialSkewNormal"], /
    ) -> IDFCollection[_g.CurveExponentialSkewNormal]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Sigmoid"], /) -> IDFCollection[_g.CurveSigmoid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:RectangularHyperbola1"], /
    ) -> IDFCollection[_g.CurveRectangularHyperbola1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:RectangularHyperbola2"], /
    ) -> IDFCollection[_g.CurveRectangularHyperbola2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:ExponentialDecay"], /
    ) -> IDFCollection[_g.CurveExponentialDecay]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:DoubleExponentialDecay"], /
    ) -> IDFCollection[_g.CurveDoubleExponentialDecay]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:ChillerPartLoadWithLift"], /
    ) -> IDFCollection[_g.CurveChillerPartLoadWithLift]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Table:IndependentVariable"], /
    ) -> IDFCollection[_g.TableIndependentVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Table:IndependentVariableList"], /
    ) -> IDFCollection[_g.TableIndependentVariableList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Table:Lookup"], /) -> IDFCollection[_g.TableLookup]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FluidProperties:Name"], /) -> IDFCollection[_g.FluidPropertiesName]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:GlycolConcentration"], /
    ) -> IDFCollection[_g.FluidPropertiesGlycolConcentration]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Temperatures"], /
    ) -> IDFCollection[_g.FluidPropertiesTemperatures]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Saturated"], /
    ) -> IDFCollection[_g.FluidPropertiesSaturated]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Superheated"], /
    ) -> IDFCollection[_g.FluidPropertiesSuperheated]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Concentration"], /
    ) -> IDFCollection[_g.FluidPropertiesConcentration]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CurrencyType"], /) -> IDFCollection[_g.CurrencyType]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComponentCost:Adjustments"], /
    ) -> IDFCollection[_g.ComponentCostAdjustments]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComponentCost:Reference"], /
    ) -> IDFCollection[_g.ComponentCostReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComponentCost:LineItem"], /
    ) -> IDFCollection[_g.ComponentCostLineItem]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Tariff"], /) -> IDFCollection[_g.UtilityCostTariff]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Qualify"], /) -> IDFCollection[_g.UtilityCostQualify]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UtilityCost:Charge:Simple"], /
    ) -> IDFCollection[_g.UtilityCostChargeSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UtilityCost:Charge:Block"], /
    ) -> IDFCollection[_g.UtilityCostChargeBlock]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Ratchet"], /) -> IDFCollection[_g.UtilityCostRatchet]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Variable"], /) -> IDFCollection[_g.UtilityCostVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UtilityCost:Computation"], /
    ) -> IDFCollection[_g.UtilityCostComputation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:Parameters"], /
    ) -> IDFCollection[_g.LifeCycleCostParameters]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:RecurringCosts"], /
    ) -> IDFCollection[_g.LifeCycleCostRecurringCosts]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:NonrecurringCost"], /
    ) -> IDFCollection[_g.LifeCycleCostNonrecurringCost]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:UsePriceEscalation"], /
    ) -> IDFCollection[_g.LifeCycleCostUsePriceEscalation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:UseAdjustment"], /
    ) -> IDFCollection[_g.LifeCycleCostUseAdjustment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Parametric:SetValueForRun"], /
    ) -> IDFCollection[_g.ParametricSetValueForRun]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Parametric:Logic"], /) -> IDFCollection[_g.ParametricLogic]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Parametric:RunControl"], /) -> IDFCollection[_g.ParametricRunControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Parametric:FileNameSuffix"], /
    ) -> IDFCollection[_g.ParametricFileNameSuffix]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:VariableDictionary"], /
    ) -> IDFCollection[_g.OutputVariableDictionary]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Surfaces:List"], /) -> IDFCollection[_g.OutputSurfacesList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Surfaces:Drawing"], /
    ) -> IDFCollection[_g.OutputSurfacesDrawing]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Schedules"], /) -> IDFCollection[_g.OutputSchedules]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Constructions"], /) -> IDFCollection[_g.OutputConstructions]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:EnergyManagementSystem"], /
    ) -> IDFCollection[_g.OutputEnergyManagementSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:SurfaceColorScheme"], /
    ) -> IDFCollection[_g.OutputControlSurfaceColorScheme]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Table:SummaryReports"], /
    ) -> IDFCollection[_g.OutputTableSummaryReports]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Table:TimeBins"], /) -> IDFCollection[_g.OutputTableTimeBins]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Table:Monthly"], /) -> IDFCollection[_g.OutputTableMonthly]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Table:Annual"], /) -> IDFCollection[_g.OutputTableAnnual]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Table:ReportPeriod"], /
    ) -> IDFCollection[_g.OutputTableReportPeriod]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:Table:Style"], /
    ) -> IDFCollection[_g.OutputControlTableStyle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:ReportingTolerances"], /
    ) -> IDFCollection[_g.OutputControlReportingTolerances]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:ResilienceSummaries"], /
    ) -> IDFCollection[_g.OutputControlResilienceSummaries]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Variable"], /) -> IDFCollection[_g.OutputVariable]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Meter"], /) -> IDFCollection[_g.OutputMeter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Meter:MeterFileOnly"], /
    ) -> IDFCollection[_g.OutputMeterMeterFileOnly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Meter:Cumulative"], /
    ) -> IDFCollection[_g.OutputMeterCumulative]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Meter:Cumulative:MeterFileOnly"], /
    ) -> IDFCollection[_g.OutputMeterCumulativeMeterFileOnly]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Meter:Custom"], /) -> IDFCollection[_g.MeterCustom]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Meter:CustomDecrement"], /) -> IDFCollection[_g.MeterCustomDecrement]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutputControl:Files"], /) -> IDFCollection[_g.OutputControlFiles]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:Timestamp"], /
    ) -> IDFCollection[_g.OutputControlTimestamp]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:JSON"], /) -> IDFCollection[_g.OutputJSON]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:SQLite"], /) -> IDFCollection[_g.OutputSQLite]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:EnvironmentalImpactFactors"], /
    ) -> IDFCollection[_g.OutputEnvironmentalImpactFactors]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnvironmentalImpactFactors"], /
    ) -> IDFCollection[_g.EnvironmentalImpactFactors]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FuelFactors"], /) -> IDFCollection[_g.FuelFactors]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Diagnostics"], /) -> IDFCollection[_g.OutputDiagnostics]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:DebuggingData"], /) -> IDFCollection[_g.OutputDebuggingData]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:PreprocessorMessage"], /
    ) -> IDFCollection[_g.OutputPreprocessorMessage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PythonPlugin:SearchPaths"], /
    ) -> IDFCollection[_g.PythonPluginSearchPaths]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PythonPlugin:Instance"], /) -> IDFCollection[_g.PythonPluginInstance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PythonPlugin:Variables"], /
    ) -> IDFCollection[_g.PythonPluginVariables]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PythonPlugin:TrendVariable"], /
    ) -> IDFCollection[_g.PythonPluginTrendVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PythonPlugin:OutputVariable"], /
    ) -> IDFCollection[_g.PythonPluginOutputVariable]: ...
    @overload
    def __getitem__(self, obj_type: _NotAnObjectTypeOfEnergyPlus26_1, /) -> Never: ...
