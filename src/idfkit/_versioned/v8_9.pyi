"""``IDFDocumentV8_9``: an ``IDFDocument`` typed for EnergyPlus 8.9.0 (stub only).

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

class _NotAnObjectTypeOfEnergyPlus8_9:
    """Not a name of an object type EnergyPlus 8.9.0 has: indexing a document with one is a type error.

    The last ``__getitem__`` overload of a document type takes this class, which no string is, so
    a type checker that finds no overload for an object type name reports it against this type.
    """

class IDFDocumentV8_9(
    _v._Accessors_v8_9,
    _v._Accessors_v8_9_to_v9_0,
    _v._Accessors_v8_9_to_v9_1,
    _v._Accessors_v8_9_to_v9_2,
    _v._Accessors_v8_9_to_v9_3,
    _v._Accessors_v8_9_to_v9_4,
    _v._Accessors_v8_9_to_v9_5,
    _v._Accessors_v8_9_to_v9_6,
    _v._Accessors_v8_9_to_v22_1,
    _v._Accessors_v8_9_to_v22_2,
    _v._Accessors_v8_9_to_v23_1,
    _v._Accessors_v8_9_to_v23_2,
    _v._Accessors_v8_9_to_v24_1,
    _v._Accessors_v8_9_to_v25_1,
    _v._Accessors_v8_9_to_v25_2,
    _v._Accessors_v8_9_to_v26_1,
    _v._Accessors_v8_9_to_v26_2,
    IDFDocumentAllVersions[Strict],
):
    """An :class:`~idfkit.document.IDFDocument` typed for EnergyPlus 8.9.0."""

    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:KusudaAchenbach"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureUndisturbedKusudaAchenbach]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ManualGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementManualGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat"], /
    ) -> IDFCollection[_g.ZoneControlThermostat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Boiler"], /
    ) -> IDFCollection[_v.HVACTemplatePlantBoiler_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:CoolingTower"], /
    ) -> IDFCollection[_g.FaultModelFoulingCoolingTower]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:File"], /) -> IDFCollection[_v.ScheduleFile_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:LookUpTable"], /
    ) -> IDFCollection[_g.ElectricLoadCenterInverterLookUpTable]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:QuadraticLinear"], /) -> IDFCollection[_g.CurveQuadraticLinear]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:From:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitExportFromVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Array"], /
    ) -> IDFCollection[_v.GroundHeatExchangerVerticalArray_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:VariableVolume"], /) -> IDFCollection[_g.FanVariableVolume]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Scheduled:DualSetpoint"], /
    ) -> IDFCollection[_g.SetpointManagerScheduledDualSetpoint]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Outdoor"], /) -> IDFCollection[_g.PipeOutdoor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:InternalVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemInternalVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:OptimumStart"], /
    ) -> IDFCollection[_v.AvailabilityManagerOptimumStart_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GasEquipment"], /) -> IDFCollection[_v.GasEquipment_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Exterior:FuelEquipment"], /
    ) -> IDFCollection[_v.ExteriorFuelEquipment_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:UserDefined"], /
    ) -> IDFCollection[_g.RoomAirTemperaturePatternUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterUse:RainCollector"], /
    ) -> IDFCollection[_g.WaterUseRainCollector]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:DualDuct:ConstantVolume"], /
    ) -> IDFCollection[_g.AirTerminalDualDuctConstantVolume]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneHVAC:UnitHeater"], /) -> IDFCollection[_g.ZoneHVACUnitHeater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:EquationFit:Heating"], /
    ) -> IDFCollection[_v.HeatPumpWaterToWaterEquationFitHeating_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Ceiling:Adiabatic"], /
    ) -> IDFCollection[_v.CeilingAdiabatic_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:DualSetpoint"], /
    ) -> IDFCollection[_g.ThermostatSetpointDualSetpoint]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GlazedDoor:Interzone"], /) -> IDFCollection[_g.GlazedDoorInterzone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:TransferLoadList"], /
    ) -> IDFCollection[_g.RefrigerationTransferLoadList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorWetBulbDifference"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorWetBulbDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:SingleSpeed"], /
    ) -> IDFCollection[_v.CoilCoolingDXSingleSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SimulationControl"], /
    ) -> IDFCollection[_v.SimulationControl_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:FiniteDifference"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureUndisturbedFiniteDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:EngineDriven"], /
    ) -> IDFCollection[_v.ChillerEngineDriven_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:WindowEquivalentLayer"], /
    ) -> IDFCollection[_g.ConstructionWindowEquivalentLayer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:SystemModel"], /) -> IDFCollection[_v.FanSystemModel_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:WalkIn"], /) -> IDFCollection[_g.RefrigerationWalkIn]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:Location"], /) -> IDFCollection[_v.SiteLocation_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:InternalCombustionEngine"], /
    ) -> IDFCollection[_v.GeneratorInternalCombustionEngine_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:SolarAndVisibleSpectrum"], /
    ) -> IDFCollection[_g.SiteSolarAndVisibleSpectrum]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Foundation:Kiva"], /) -> IDFCollection[_v.FoundationKiva_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FanPerformance:NightVentilation"], /
    ) -> IDFCollection[_g.FanPerformanceNightVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Material:NoMass"], /
    ) -> IDFCollection[_v.MaterialNoMass_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:FuelCell"], /) -> IDFCollection[_g.GeneratorFuelCell]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:OtherSideConditionsModel"], /
    ) -> IDFCollection[_g.SurfacePropertyOtherSideConditionsModel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Warmest"], /
    ) -> IDFCollection[_g.SetpointManagerWarmest]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Fan"], /
    ) -> IDFCollection[_v.AirflowNetworkDistributionComponentFan_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Parametric:Logic"], /) -> IDFCollection[_g.ParametricLogic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:Photovoltaic"], /
    ) -> IDFCollection[_g.GeneratorPhotovoltaic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleHeating"], /
    ) -> IDFCollection[_g.ThermostatSetpointSingleHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:LowTemperatureTurnOn"], /
    ) -> IDFCollection[_g.AvailabilityManagerLowTemperatureTurnOn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork"], /
    ) -> IDFCollection[_g.RoomAirNodeAirflowNetwork]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneThermalChimney"], /
    ) -> IDFCollection[_v.ZoneThermalChimney_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:UserDefined"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctUserDefined_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatCool"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryHeatCool]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Zone:Detailed"], /) -> IDFCollection[_g.ShadingZoneDetailed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Node"], /
    ) -> IDFCollection[_v.AirflowNetworkDistributionNode_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:OccupantVentilationControl"], /
    ) -> IDFCollection[_g.AirflowNetworkOccupantVentilationControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Table:Monthly"], /
    ) -> IDFCollection[_v.OutputTableMonthly_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Thermostat"], /
    ) -> IDFCollection[_g.HVACTemplateThermostat]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Version"], /) -> IDFCollection[_v.Version_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:MoisturePenetrationDepth:Settings"], /
    ) -> IDFCollection[_g.MaterialPropertyMoisturePenetrationDepthSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:HotWaterLoop"], /
    ) -> IDFCollection[_g.HVACTemplatePlantHotWaterLoop]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoofIrrigation"], /) -> IDFCollection[_g.RoofIrrigation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:Desiccant:BalancedFlow"], /
    ) -> IDFCollection[_v.HeatExchangerDesiccantBalancedFlow_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Linkage"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionLinkage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport"], /
    ) -> IDFCollection[_v.ExternalInterfaceFunctionalMockupUnitImport_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Blind:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialBlindEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:ParameterEstimation"], /
    ) -> IDFCollection[_v.CoilCoolingWaterToAirHeatPumpParameterEstimation_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Ceiling:Interzone"], /
    ) -> IDFCollection[_v.CeilingInterzone_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricEquipment:ITE:AirCooled"], /
    ) -> IDFCollection[_v.ElectricEquipmentITEAirCooled_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:PowerModule"], /
    ) -> IDFCollection[_g.GeneratorFuelCellPowerModule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:SurfaceList"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatTransferAlgorithmSurfaceList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:VariableLocation"], /) -> IDFCollection[_g.SiteVariableLocation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:VAV:FanPowered"], /
    ) -> IDFCollection[_g.HVACTemplateZoneVAVFanPowered]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DistrictHeating"], /
    ) -> IDFCollection[_v.DistrictHeating_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:Case"], /) -> IDFCollection[_g.RefrigerationCase]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:OutdoorAirReset"], /
    ) -> IDFCollection[_g.SetpointManagerOutdoorAirReset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:TwoSpeed"], /
    ) -> IDFCollection[_v.CoolingTowerTwoSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneList"], /) -> IDFCollection[_g.ZoneList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:VAV:HeatAndCool"], /
    ) -> IDFCollection[_g.HVACTemplateZoneVAVHeatAndCool]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoomAirModelType"], /) -> IDFCollection[_g.RoomAirModelType]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ZoneSplitter"], /
    ) -> IDFCollection[_g.AirLoopHVACZoneSplitter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WeatherProperty:SkyTemperature"], /
    ) -> IDFCollection[_v.WeatherPropertySkyTemperature_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Parametric:RunControl"], /) -> IDFCollection[_g.ParametricRunControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:Boiler"], /
    ) -> IDFCollection[_g.FaultModelFoulingBoiler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Controller:WaterCoil"], /
    ) -> IDFCollection[_v.ControllerWaterCoil_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Glazing:EquivalentLayer"], /
    ) -> IDFCollection[_v.WindowMaterialGlazingEquivalentLayer_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ReturnPath"], /
    ) -> IDFCollection[_g.AirLoopHVACReturnPath]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:UnitVentilator"], /
    ) -> IDFCollection[_g.ZoneHVACUnitVentilator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl"], /
    ) -> IDFCollection[_v.AirConditionerVariableRefrigerantFlowFluidTemperatureControl_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:OutdoorAir"], /
    ) -> IDFCollection[_v.DesignSpecificationOutdoorAir_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirBalance:OutdoorAir"], /
    ) -> IDFCollection[_g.ZoneAirBalanceOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["BuildingSurface:Detailed"], /
    ) -> IDFCollection[_v.BuildingSurfaceDetailed_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Undisturbed:Xing"], /
    ) -> IDFCollection[_v.SiteGroundTemperatureUndisturbedXing_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:MultipleSurface"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatTransferAlgorithmMultipleSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:Unitary:Furnace:HeatCool"], /
    ) -> IDFCollection[_v.AirLoopHVACUnitaryFurnaceHeatCool_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Simple"], /
    ) -> IDFCollection[_g.ElectricLoadCenterStorageSimple]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:FanPressureRise"], /) -> IDFCollection[_g.CurveFanPressureRise]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC:ZoneMixer"], /) -> IDFCollection[_g.AirLoopHVACZoneMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Steam"], /
    ) -> IDFCollection[_v.ZoneHVACBaseboardRadiantConvectiveSteam_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:Zone"], /) -> IDFCollection[_v.SizingZone_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FluidCooler:TwoSpeed"], /) -> IDFCollection[_g.FluidCoolerTwoSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:DifferentialThermostat"], /
    ) -> IDFCollection[_g.AvailabilityManagerDifferentialThermostat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ShadingProperty:Reflectance"], /
    ) -> IDFCollection[_g.ShadingPropertyReflectance]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OtherEquipment"], /) -> IDFCollection[_v.OtherEquipment_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:DualDuct:VAV"], /
    ) -> IDFCollection[_v.AirTerminalDualDuctVAV_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Parametric:SetValueForRun"], /
    ) -> IDFCollection[_g.ParametricSetValueForRun]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"], /
    ) -> IDFCollection[_g.CoilCoolingDXVariableRefrigerantFlowFluidTemperatureControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ConvectionCoefficients"], /
    ) -> IDFCollection[_v.SurfacePropertyConvectionCoefficients_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatBalanceSettings:ConductionFiniteDifference"], /
    ) -> IDFCollection[_g.HeatBalanceSettingsConductionFiniteDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:ThermalConductivity"], /
    ) -> IDFCollection[_v.MaterialPropertyHeatAndMoistureTransferThermalConductivity_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:ProgramCallingManager"], /
    ) -> IDFCollection[_v.EnergyManagementSystemProgramCallingManager_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:FCfactorMethod"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureFCfactorMethod]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Boiler:HotWater"], /) -> IDFCollection[_v.BoilerHotWater_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Pump:VariableSpeed:Condensate"], /
    ) -> IDFCollection[_v.PumpVariableSpeedCondensate_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:BuildingSurface"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureBuildingSurface]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Site:Detailed"], /) -> IDFCollection[_g.ShadingSiteDetailed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:ConstantGradient"], /
    ) -> IDFCollection[_v.RoomAirTemperaturePatternConstantGradient_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:IdealLoadsAirSystem"], /
    ) -> IDFCollection[_v.ZoneHVACIdealLoadsAirSystem_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:Scheduled"], /
    ) -> IDFCollection[_g.AvailabilityManagerScheduled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundDomain:Basement"], /
    ) -> IDFCollection[_v.SiteGroundDomainBasement_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Indoor"], /) -> IDFCollection[_g.PipeIndoor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:TemperatureAndHumidity"], /
    ) -> IDFCollection[_g.ZoneControlThermostatTemperatureAndHumidity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:Convective:Electric"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardConvectiveElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:MaximumHumidity:Average"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneMaximumHumidityAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:Materials"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabMaterials]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RunPeriodControl:DaylightSavingTime"], /
    ) -> IDFCollection[_g.RunPeriodControlDaylightSavingTime]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:CombustionTurbine"], /
    ) -> IDFCollection[_v.ChillerCombustionTurbine_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ExternalInterface"], /) -> IDFCollection[_g.ExternalInterface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:SimpleOpening"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneComponentSimpleOpening]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Table:TimeBins"], /
    ) -> IDFCollection[_v.OutputTableTimeBins_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:SorptionIsotherm"], /
    ) -> IDFCollection[_v.MaterialPropertyHeatAndMoistureTransferSorptionIsotherm_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Boiler:Steam"], /) -> IDFCollection[_v.BoilerSteam_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:CoolingPanel:RadiantConvective:Water"], /
    ) -> IDFCollection[_v.ZoneHVACCoolingPanelRadiantConvectiveWater_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LoadProfile:Plant"], /
    ) -> IDFCollection[_v.LoadProfilePlant_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:ThermostatOffset"], /
    ) -> IDFCollection[_g.FaultModelThermostatOffset]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:Cooling:DX:HeatExchangerAssisted"], /
    ) -> IDFCollection[_v.CoilSystemCoolingDXHeatExchangerAssisted_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:Parameters"], /
    ) -> IDFCollection[_v.LifeCycleCostParameters_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACSystemRootFindingAlgorithm"], /
    ) -> IDFCollection[_v.HVACSystemRootFindingAlgorithm_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:OutdoorAirUnit:EquipmentList"], /
    ) -> IDFCollection[_v.ZoneHVACOutdoorAirUnitEquipmentList_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Reheat"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:PhaseChange"], /
    ) -> IDFCollection[_v.MaterialPropertyPhaseChange_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Building"], /) -> IDFCollection[_g.ShadingBuilding]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableRefrigerantFlow"], /
    ) -> IDFCollection[_g.CoilHeatingDXVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Screen:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialScreenEquivalentLayer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Tariff"], /) -> IDFCollection[_g.UtilityCostTariff]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ComponentModel"], /) -> IDFCollection[_g.FanComponentModel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EnergyRecoveryVentilator"], /
    ) -> IDFCollection[_g.ZoneHVACEnergyRecoveryVentilator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ConvectionCoefficients:MultipleSurface"], /
    ) -> IDFCollection[_v.SurfacePropertyConvectionCoefficientsMultipleSurface_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneProperty:LocalEnvironment"], /
    ) -> IDFCollection[_g.ZonePropertyLocalEnvironment]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:ConstructionIndexVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemConstructionIndexVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeFluidCooler:TwoSpeed"], /
    ) -> IDFCollection[_v.EvaporativeFluidCoolerTwoSpeed_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:SimParameters"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementSimParameters]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UtilityCost:Charge:Block"], /
    ) -> IDFCollection[_v.UtilityCostChargeBlock_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:AirTerminal:Sizing"], /
    ) -> IDFCollection[_g.DesignSpecificationAirTerminalSizing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:EquivalentSlab"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabEquivalentSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Electric"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardRadiantConvectiveElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:MinimumHumidity:Average"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneMinimumHumidityAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:TranscriticalSystem"], /
    ) -> IDFCollection[_g.RefrigerationTranscriticalSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneRefrigerationDoorMixing"], /
    ) -> IDFCollection[_v.ZoneRefrigerationDoorMixing_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:ConstantCOP"], /
    ) -> IDFCollection[_v.ChillerConstantCOP_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SizingPeriod:WeatherFileConditionType"], /
    ) -> IDFCollection[_g.SizingPeriodWeatherFileConditionType]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Shade"], /) -> IDFCollection[_g.WindowMaterialShade]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:WindowAirConditioner"], /
    ) -> IDFCollection[_g.ZoneHVACWindowAirConditioner]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:PackagedVAV"], /
    ) -> IDFCollection[_g.HVACTemplateSystemPackagedVAV]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ConnectorList"], /) -> IDFCollection[_g.ConnectorList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ExteriorNaturalVentedCavity"], /
    ) -> IDFCollection[_g.SurfacePropertyExteriorNaturalVentedCavity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:Sandia"], /
    ) -> IDFCollection[_v.PhotovoltaicPerformanceSandia_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:NoReheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeNoReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Schedule"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImportToSchedule]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Floor:GroundContact"], /
    ) -> IDFCollection[_v.FloorGroundContact_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:BaseboardHeat"], /
    ) -> IDFCollection[_g.HVACTemplateZoneBaseboardHeat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatBalanceSourceTerm"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatBalanceSourceTerm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow"], /
    ) -> IDFCollection[_v.AirConditionerVariableRefrigerantFlow_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:OnOff"], /) -> IDFCollection[_g.FanOnOff]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Year"], /) -> IDFCollection[_v.ScheduleYear_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Humidistat"], /
    ) -> IDFCollection[_v.ZoneControlHumidistat_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:VentilatedSlab:SlabGroup"], /
    ) -> IDFCollection[_g.ZoneHVACVentilatedSlabSlabGroup]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:IdealLoadsAirSystem"], /
    ) -> IDFCollection[_g.HVACTemplateZoneIdealLoadsAirSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Humidity:Maximum"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneHumidityMaximum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EquipmentConnections"], /
    ) -> IDFCollection[_g.ZoneHVACEquipmentConnections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:Mixed"], /
    ) -> IDFCollection[_v.WaterHeaterMixed_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:ZFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabZFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:FfactorGroundFloor"], /
    ) -> IDFCollection[_g.ConstructionFfactorGroundFloor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:OneStageCooling"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneOneStageCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:Cooling:Water:HeatExchangerAssisted"], /
    ) -> IDFCollection[_g.CoilSystemCoolingWaterHeatExchangerAssisted]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:OtherSideCoefficients"], /
    ) -> IDFCollection[_g.SurfacePropertyOtherSideCoefficients]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnTemperature:ChilledWater"], /
    ) -> IDFCollection[_g.SetpointManagerReturnTemperatureChilledWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:HybridUnitaryHVAC"], /
    ) -> IDFCollection[_v.ZoneHVACHybridUnitaryHVAC_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:ReferenceCrackConditions"], /
    ) -> IDFCollection[_v.AirflowNetworkMultiZoneReferenceCrackConditions_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Daylighting:Controls"], /
    ) -> IDFCollection[_v.DaylightingControls_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Saturated"], /
    ) -> IDFCollection[_g.FluidPropertiesSaturated]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:IntegralCollectorStorage"], /
    ) -> IDFCollection[_g.SolarCollectorIntegralCollectorStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:WindPressureCoefficientValues"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneWindPressureCoefficientValues]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Leak"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentLeak]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Humidity:Maximum"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneHumidityMaximum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm:Construction"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatTransferAlgorithmConstruction]: ...
    @overload
    def __getitem__(self, obj_type: Literal["NodeList"], /) -> IDFCollection[_g.NodeList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Overhang"], /) -> IDFCollection[_g.ShadingOverhang]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:DualDuct"], /
    ) -> IDFCollection[_g.HVACTemplateSystemDualDuct]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Adiabatic:Steam"], /) -> IDFCollection[_g.PipeAdiabaticSteam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:AuxiliaryHeater"], /
    ) -> IDFCollection[_g.GeneratorFuelCellAuxiliaryHeater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:Ice:Detailed"], /
    ) -> IDFCollection[_v.ThermalStorageIceDetailed_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:EvaporativeCooler"], /
    ) -> IDFCollection[_g.FaultModelFoulingEvaporativeCooler]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Triquadratic"], /) -> IDFCollection[_g.CurveTriquadratic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:EquivSlab"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementEquivSlab]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:CurveOrTableIndexVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemCurveOrTableIndexVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:ExteriorLights"], /
    ) -> IDFCollection[_v.DemandManagerExteriorLights_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:TerminalUnit:VariableRefrigerantFlow"], /
    ) -> IDFCollection[_v.ZoneHVACTerminalUnitVariableRefrigerantFlow_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:Insulation"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabInsulation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UtilityCost:Computation"], /
    ) -> IDFCollection[_g.UtilityCostComputation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:GlobalVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemGlobalVariable]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Qualify"], /) -> IDFCollection[_g.UtilityCostQualify]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ControllerList"], /
    ) -> IDFCollection[_g.AirLoopHVACControllerList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Parametric:FileNameSuffix"], /
    ) -> IDFCollection[_g.ParametricFileNameSuffix]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:ChilledWater:Mixed"], /
    ) -> IDFCollection[_g.ThermalStorageChilledWaterMixed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Single"], /
    ) -> IDFCollection[_g.GroundHeatExchangerVerticalSingle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:FlatPlate:PhotovoltaicThermal"], /
    ) -> IDFCollection[_g.SolarCollectorFlatPlatePhotovoltaicThermal]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:YFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabYFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Table:Annual"], /
    ) -> IDFCollection[_v.OutputTableAnnual_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:CoilSupplyAir"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetCoilSupplyAir]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Exponent"], /) -> IDFCollection[_g.CurveExponent]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowGap:SupportPillar"], /
    ) -> IDFCollection[_g.WindowGapSupportPillar]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:AdjacentSurfaceList"], /
    ) -> IDFCollection[_g.RoomAirNodeAirflowNetworkAdjacentSurfaceList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:FlatPlate"], /
    ) -> IDFCollection[_g.SolarCollectorPerformanceFlatPlate]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Scheduled"], /
    ) -> IDFCollection[_g.SetpointManagerScheduled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:GasMixture"], /
    ) -> IDFCollection[_v.WindowMaterialGasMixture_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirMassFlowConservation"], /
    ) -> IDFCollection[_v.ZoneAirMassFlowConservation_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:DualDuct"], /
    ) -> IDFCollection[_g.HVACTemplateZoneDualDuct]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:AutoGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementAutoGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnvironmentalImpactFactors"], /
    ) -> IDFCollection[_v.EnvironmentalImpactFactors_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ZoneExhaust"], /) -> IDFCollection[_g.FanZoneExhaust]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:Coldest"], /
    ) -> IDFCollection[_g.SetpointManagerColdest]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HybridVentilation"], /
    ) -> IDFCollection[_g.AvailabilityManagerHybridVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:ChilledWaterLoop"], /
    ) -> IDFCollection[_g.HVACTemplatePlantChilledWaterLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:ZoneAirDistribution"], /
    ) -> IDFCollection[_g.DesignSpecificationZoneAirDistribution]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:ScheduledOn"], /
    ) -> IDFCollection[_g.AvailabilityManagerScheduledOn]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:ThermalEnergyStorage"], /
    ) -> IDFCollection[_v.PlantEquipmentOperationThermalEnergyStorage_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:File:Shading"], /) -> IDFCollection[_g.ScheduleFileShading]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:HorizontalTrench"], /
    ) -> IDFCollection[_v.GroundHeatExchangerHorizontalTrench_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Site"], /) -> IDFCollection[_g.ShadingSite]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass"], /
    ) -> IDFCollection[_v.AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDewpointDifference"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorDewpointDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Schedule"], /
    ) -> IDFCollection[_g.ExternalInterfaceSchedule]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Compact"], /) -> IDFCollection[_g.ScheduleCompact]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Meter:Cumulative"], /
    ) -> IDFCollection[_g.OutputMeterCumulative]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Actuator"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImportToActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:EnergyManagementSystem"], /
    ) -> IDFCollection[_g.OutputEnergyManagementSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Material:InfraredTransparent"], /
    ) -> IDFCollection[_g.MaterialInfraredTransparent]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:VariableDictionary"], /
    ) -> IDFCollection[_g.OutputVariableDictionary]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:WaterToAir"], /
    ) -> IDFCollection[_v.AirLoopHVACUnitaryHeatPumpWaterToAir_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneCoolTower:Shower"], /
    ) -> IDFCollection[_v.ZoneCoolTowerShower_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:System"], /) -> IDFCollection[_v.SizingSystem_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Humidity:Minimum"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneHumidityMinimum]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Connections"], /) -> IDFCollection[_g.WaterUseConnections]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Zone"], /) -> IDFCollection[_v.Zone_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:OutdoorAirUnit"], /
    ) -> IDFCollection[_g.ZoneHVACOutdoorAirUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Shallow"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureShallow]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RunPeriod"], /) -> IDFCollection[_v.RunPeriod_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:PTHP"], /
    ) -> IDFCollection[_v.HVACTemplateZonePTHP_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:PhotovoltaicThermal:Simple"], /
    ) -> IDFCollection[_g.SolarCollectorPerformancePhotovoltaicThermalSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:Sizing"], /
    ) -> IDFCollection[_v.WaterHeaterSizing_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:EnthalpySensorOffset:ReturnAir"], /
    ) -> IDFCollection[_g.FaultModelEnthalpySensorOffsetReturnAir]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:Precipitation"], /) -> IDFCollection[_g.SitePrecipitation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:ReliefAirFlow"], /
    ) -> IDFCollection[_v.AirflowNetworkDistributionComponentReliefAirFlow_v8_9]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Linear"], /) -> IDFCollection[_g.CurveLinear]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:Table:Style"], /
    ) -> IDFCollection[_v.OutputControlTableStyle_v8_9_to_v23_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Material"], /) -> IDFCollection[_v.Material_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComponentCost:LineItem"], /
    ) -> IDFCollection[_v.ComponentCostLineItem_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Construction"], /) -> IDFCollection[_g.Construction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:ThreeNodeDisplacementVentilation"], /
    ) -> IDFCollection[_g.RoomAirSettingsThreeNodeDisplacementVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Boiler:ObjectReference"], /
    ) -> IDFCollection[_g.HVACTemplatePlantBoilerObjectReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDryBulb"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorDryBulb]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:Unitary"], /
    ) -> IDFCollection[_g.HVACTemplateSystemUnitary]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneGroup"], /) -> IDFCollection[_v.ZoneGroup_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:TwoSpeed"], /
    ) -> IDFCollection[_v.CoilCoolingDXTwoSpeed_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Wall:Underground"], /
    ) -> IDFCollection[_v.WallUnderground_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:AirToAir:SensibleAndLatent"], /
    ) -> IDFCollection[_v.HeatExchangerAirToAirSensibleAndLatent_v8_9_to_v23_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:EquationFit"], /
    ) -> IDFCollection[_v.CoilHeatingWaterToAirHeatPumpEquationFit_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Tower"], /
    ) -> IDFCollection[_g.HVACTemplatePlantTower]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Electric:ReformulatedEIR"], /
    ) -> IDFCollection[_v.ChillerElectricReformulatedEIR_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Dehumidifier:Desiccant:System"], /
    ) -> IDFCollection[_g.DehumidifierDesiccantSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:XFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabXFACE]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ScheduleTypeLimits"], /) -> IDFCollection[_g.ScheduleTypeLimits]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:GlazingGroup:Thermochromic"], /
    ) -> IDFCollection[_g.WindowMaterialGlazingGroupThermochromic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SizingPeriod:WeatherFileDays"], /
    ) -> IDFCollection[_v.SizingPeriodWeatherFileDays_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:Coil"], /
    ) -> IDFCollection[_g.FaultModelFoulingCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:HumiditySensorOffset:OutdoorAir"], /
    ) -> IDFCollection[_g.FaultModelHumiditySensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(self, obj_type: Literal["People"], /) -> IDFCollection[_v.People_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Subcooler"], /
    ) -> IDFCollection[_g.RefrigerationSubcooler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Foundation:Kiva:Settings"], /
    ) -> IDFCollection[_g.FoundationKivaSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:DualDuct:VAV:OutdoorAir"], /
    ) -> IDFCollection[_g.AirTerminalDualDuctVAVOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:BoundConds"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabBoundConds]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:WeatherStation"], /) -> IDFCollection[_g.SiteWeatherStation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Coil"], /
    ) -> IDFCollection[_v.AirflowNetworkDistributionComponentCoil_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Humidifier:Steam:Electric"], /
    ) -> IDFCollection[_g.HumidifierSteamElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:UseAdjustment"], /
    ) -> IDFCollection[_v.LifeCycleCostUseAdjustment_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:SingleSpeed:ThermalStorage"], /
    ) -> IDFCollection[_g.CoilCoolingDXSingleSpeedThermalStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:BldgProps"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabBldgProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitExportToVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneProperty:UserViewFactors:bySurfaceName"], /
    ) -> IDFCollection[_v.ZonePropertyUserViewFactorsbySurfaceName_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:ForcedAir:UserDefined"], /
    ) -> IDFCollection[_v.ZoneHVACForcedAirUserDefined_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:VariableFlow"], /
    ) -> IDFCollection[_v.ZoneHVACLowTemperatureRadiantVariableFlow_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:GlycolConcentration"], /
    ) -> IDFCollection[_g.FluidPropertiesGlycolConcentration]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:ScheduledOff"], /
    ) -> IDFCollection[_g.AvailabilityManagerScheduledOff]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Concentration"], /
    ) -> IDFCollection[_g.FluidPropertiesConcentration]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Cooling:Water"], /) -> IDFCollection[_g.CoilCoolingWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComponentCost:Reference"], /
    ) -> IDFCollection[_g.ComponentCostReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleCooling"], /
    ) -> IDFCollection[_g.ThermostatSetpointSingleCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:OperativeTemperature"], /
    ) -> IDFCollection[_g.ZoneControlThermostatOperativeTemperature]: ...
    @overload
    def __getitem__(self, obj_type: Literal["DistrictCooling"], /) -> IDFCollection[_g.DistrictCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Direct:CelDekPad"], /
    ) -> IDFCollection[_g.EvaporativeCoolerDirectCelDekPad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:ContaminantController"], /
    ) -> IDFCollection[_v.ZoneControlContaminantController_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Fin"], /) -> IDFCollection[_g.ShadingFin]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:ComponentSetpoint"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationComponentSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:Insulation"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementInsulation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CurrencyType"], /) -> IDFCollection[_g.CurrencyType]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:ComplexFenestrationState"], /
    ) -> IDFCollection[_v.ConstructionComplexFenestrationState_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint"], /
    ) -> IDFCollection[_g.ThermostatSetpointThermalComfortFangerDualSetpoint]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HighTemperatureTurnOff"], /
    ) -> IDFCollection[_g.AvailabilityManagerHighTemperatureTurnOff]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Electric:MultiStage"], /
    ) -> IDFCollection[_v.CoilHeatingElectricMultiStage_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Humidifier:Steam:Gas"], /) -> IDFCollection[_g.HumidifierSteamGas]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:AirChiller"], /
    ) -> IDFCollection[_g.RefrigerationAirChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Surface"], /
    ) -> IDFCollection[_v.GroundHeatExchangerSurface_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Material:RoofVegetation"], /
    ) -> IDFCollection[_g.MaterialRoofVegetation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:FlatPlate:Water"], /
    ) -> IDFCollection[_g.SolarCollectorFlatPlateWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RunPeriodControl:SpecialDays"], /
    ) -> IDFCollection[_g.RunPeriodControlSpecialDays]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:EquivAutoGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementEquivAutoGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RunPeriod:CustomRange"], /
    ) -> IDFCollection[_v.RunPeriodCustomRange_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Vertical:Properties"], /
    ) -> IDFCollection[_g.GroundHeatExchangerVerticalProperties]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:CondenserEnteringReset"], /
    ) -> IDFCollection[_g.SetpointManagerCondenserEnteringReset]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Day:Interval"], /) -> IDFCollection[_g.ScheduleDayInterval]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:SingleSpeed"], /
    ) -> IDFCollection[_v.CoilHeatingDXSingleSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Pump:ConstantSpeed"], /
    ) -> IDFCollection[_v.PumpConstantSpeed_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:CelDekPad"], /
    ) -> IDFCollection[_g.EvaporativeCoolerIndirectCelDekPad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UtilityCost:Charge:Simple"], /
    ) -> IDFCollection[_g.UtilityCostChargeSimple]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:Duct"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentDuct]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:Simple"], /
    ) -> IDFCollection[_g.ElectricLoadCenterInverterSimple]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Compliance:Building"], /) -> IDFCollection[_g.ComplianceBuilding]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Shading:Building:Detailed"], /
    ) -> IDFCollection[_g.ShadingBuildingDetailed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:PTAC"], /
    ) -> IDFCollection[_v.HVACTemplateZonePTAC_v8_9]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Underground"], /) -> IDFCollection[_g.PipeUnderground]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:VAV"], /) -> IDFCollection[_g.HVACTemplateZoneVAV]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Quadratic"], /) -> IDFCollection[_g.CurveQuadratic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableSpeed"], /
    ) -> IDFCollection[_v.CoilHeatingDXVariableSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Duct"], /) -> IDFCollection[_g.Duct]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceControl:MovableInsulation"], /
    ) -> IDFCollection[_g.SurfaceControlMovableInsulation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeFourPipeBeam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManagerAssignmentList"], /
    ) -> IDFCollection[_g.AvailabilityManagerAssignmentList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:AirCooled"], /
    ) -> IDFCollection[_g.RefrigerationCondenserAirCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneVentilation:WindandStackOpenArea"], /
    ) -> IDFCollection[_v.ZoneVentilationWindandStackOpenArea_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowSystemNodeTemperature"], /
    ) -> IDFCollection[_g.SetpointManagerFollowSystemNodeTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeaderedPumps:ConstantSpeed"], /
    ) -> IDFCollection[_v.HeaderedPumpsConstantSpeed_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:PVWatts"], /
    ) -> IDFCollection[_g.ElectricLoadCenterInverterPVWatts]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:Desiccant:BalancedFlow:PerformanceDataType1"], /
    ) -> IDFCollection[_g.HeatExchangerDesiccantBalancedFlowPerformanceDataType1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Sizing:Parameters"], /
    ) -> IDFCollection[_v.SizingParameters_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FuelFactors"], /) -> IDFCollection[_v.FuelFactors_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Variable"], /) -> IDFCollection[_g.OutputVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:WaterToAirHeatPump"], /
    ) -> IDFCollection[_v.HVACTemplateZoneWaterToAirHeatPump_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:SurroundingSurfaces"], /
    ) -> IDFCollection[_v.SurfacePropertySurroundingSurfaces_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTowerPerformance:CoolTools"], /
    ) -> IDFCollection[_g.CoolingTowerPerformanceCoolTools]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeFourPipeInduction]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside:UserCurve"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmOutsideUserCurve]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:LeakageRatio"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentLeakageRatio]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:CrossVentilation"], /
    ) -> IDFCollection[_g.RoomAirSettingsCrossVentilation]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Window"], /) -> IDFCollection[_v.Window_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ShadowCalculation"], /
    ) -> IDFCollection[_v.ShadowCalculation_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:SurfaceColorScheme"], /
    ) -> IDFCollection[_v.OutputControlSurfaceColorScheme_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Pipe:Adiabatic"], /) -> IDFCollection[_g.PipeAdiabatic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Electric:EIR"], /
    ) -> IDFCollection[_v.ChillerElectricEIR_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:MicroCHP:NonNormalizedParameters"], /
    ) -> IDFCollection[_g.GeneratorMicroCHPNonNormalizedParameters]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Actuator"], /
    ) -> IDFCollection[_v.ExternalInterfaceFunctionalMockupUnitExportToActuator_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Detailed"], /) -> IDFCollection[_v.WallDetailed_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:IlluminanceMap"], /
    ) -> IDFCollection[_v.OutputIlluminanceMap_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:ReportingTolerances"], /
    ) -> IDFCollection[_g.OutputControlReportingTolerances]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:UserDefined"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationUserDefined]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Slinky"], /
    ) -> IDFCollection[_v.GroundHeatExchangerSlinky_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FenestrationSurface:Detailed"], /
    ) -> IDFCollection[_v.FenestrationSurfaceDetailed_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:TerminalUnit"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentTerminalUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CompressorRack"], /
    ) -> IDFCollection[_g.RefrigerationCompressorRack]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Program"], /
    ) -> IDFCollection[_v.EnergyManagementSystemProgram_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:VentilatedSlab"], /
    ) -> IDFCollection[_g.ZoneHVACVentilatedSlab]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:Node"], /) -> IDFCollection[_g.OutdoorAirNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:RefrigerationChillerSet"], /
    ) -> IDFCollection[_g.ZoneHVACRefrigerationChillerSet]: ...
    @overload
    def __getitem__(self, obj_type: Literal["InternalMass"], /) -> IDFCollection[_v.InternalMass_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside:AdaptiveModelSelections"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmInsideAdaptiveModelSelections]: ...
    @overload
    def __getitem__(self, obj_type: Literal["SteamEquipment"], /) -> IDFCollection[_v.SteamEquipment_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Table:SummaryReports"], /
    ) -> IDFCollection[_v.OutputTableSummaryReports_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:DuctViewFactors"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionDuctViewFactors]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:IntegratedHeatPump:AirSource"], /
    ) -> IDFCollection[_v.CoilSystemIntegratedHeatPumpAirSource_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:NightVentilation"], /
    ) -> IDFCollection[_g.AvailabilityManagerNightVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Daylighting:ReferencePoint"], /
    ) -> IDFCollection[_v.DaylightingReferencePoint_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Compressor"], /
    ) -> IDFCollection[_g.RefrigerationCompressor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:PressureSensorOffset:OutdoorAir"], /
    ) -> IDFCollection[_v.FaultModelPressureSensorOffsetOutdoorAir_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:Stratified"], /
    ) -> IDFCollection[_v.WaterHeaterStratified_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:ParameterEstimation:Cooling"], /
    ) -> IDFCollection[_g.HeatPumpWaterToWaterParameterEstimationCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:AirSupply"], /
    ) -> IDFCollection[_g.GeneratorFuelCellAirSupply]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:ReturnPlenum"], /
    ) -> IDFCollection[_g.AirLoopHVACReturnPlenum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:WindowDataFile"], /
    ) -> IDFCollection[_g.ConstructionWindowDataFile]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UtilityCost:Variable"], /
    ) -> IDFCollection[_v.UtilityCostVariable_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Diffusion"], /
    ) -> IDFCollection[_v.MaterialPropertyHeatAndMoistureTransferDiffusion_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:LowTemperatureTurnOff"], /
    ) -> IDFCollection[_g.AvailabilityManagerLowTemperatureTurnOff]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Cubic"], /) -> IDFCollection[_g.CurveCubic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:WetCoil"], /
    ) -> IDFCollection[_g.EvaporativeCoolerIndirectWetCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DaylightingDevice:LightWell"], /
    ) -> IDFCollection[_g.DaylightingDeviceLightWell]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneCrossMixing"], /
    ) -> IDFCollection[_v.ZoneCrossMixing_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:PressureDriven"], /
    ) -> IDFCollection[_g.SurfaceContaminantSourceAndSinkGenericPressureDriven]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:Simple"], /
    ) -> IDFCollection[_v.PhotovoltaicPerformanceSimple_v8_9_to_v25_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GeometryTransform"], /) -> IDFCollection[_g.GeometryTransform]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Drape:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialDrapeEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:UnderFloorAirDistributionInterior"], /
    ) -> IDFCollection[_g.RoomAirSettingsUnderFloorAirDistributionInterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:EffectiveLeakageArea"], /
    ) -> IDFCollection[_v.ZoneInfiltrationEffectiveLeakageArea_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Adiabatic"], /) -> IDFCollection[_v.FloorAdiabatic_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SwimmingPool:Indoor"], /
    ) -> IDFCollection[_v.SwimmingPoolIndoor_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:OutdoorAirSystem"], /
    ) -> IDFCollection[_v.AirLoopHVACOutdoorAirSystem_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Meter:CustomDecrement"], /
    ) -> IDFCollection[_v.MeterCustomDecrement_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeater:Absorption:DirectFired"], /
    ) -> IDFCollection[_v.ChillerHeaterAbsorptionDirectFired_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ComBldg"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementComBldg]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Meter:Cumulative:MeterFileOnly"], /
    ) -> IDFCollection[_g.OutputMeterCumulativeMeterFileOnly]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:WindTurbine"], /) -> IDFCollection[_g.GeneratorWindTurbine]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CoilSystem:Heating:DX"], /) -> IDFCollection[_g.CoilSystemHeatingDX]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:VariableSpeed:Merkel"], /
    ) -> IDFCollection[_v.CoolingTowerVariableSpeedMerkel_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:SurfaceMapping"], /
    ) -> IDFCollection[_v.RoomAirTemperaturePatternSurfaceMapping_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:Inverter"], /
    ) -> IDFCollection[_g.GeneratorFuelCellInverter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Desuperheater"], /
    ) -> IDFCollection[_v.CoilHeatingDesuperheater_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PhotovoltaicPerformance:EquivalentOne-Diode"], /
    ) -> IDFCollection[_v.PhotovoltaicPerformanceEquivalentOneDiode_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:SolarIncidentInside"], /
    ) -> IDFCollection[_g.SurfacePropertySolarIncidentInside]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:ResponseFactors"], /
    ) -> IDFCollection[_v.GroundHeatExchangerResponseFactors_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Connector:Splitter"], /) -> IDFCollection[_g.ConnectorSplitter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:AirflowNetwork"], /
    ) -> IDFCollection[_g.RoomAirSettingsAirflowNetwork]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Transformer"], /
    ) -> IDFCollection[_g.ElectricLoadCenterTransformer]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:QuadLinear"], /) -> IDFCollection[_g.CurveQuadLinear]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Door:Interzone"], /) -> IDFCollection[_g.DoorInterzone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:AirToAir"], /
    ) -> IDFCollection[_v.AirLoopHVACUnitaryHeatPumpAirToAir_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Interzone"], /) -> IDFCollection[_v.WallInterzone_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:ConstantVolume"], /
    ) -> IDFCollection[_g.HVACTemplateSystemConstantVolume]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Indirect:ResearchSpecial"], /
    ) -> IDFCollection[_g.EvaporativeCoolerIndirectResearchSpecial]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:OutdoorAir"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilSystem:Cooling:DX"], /
    ) -> IDFCollection[_v.CoilSystemCoolingDX_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed"], /
    ) -> IDFCollection[_v.CoilWaterHeatingAirToWaterHeatPumpVariableSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:LocalEnvironment"], /
    ) -> IDFCollection[_v.SurfacePropertyLocalEnvironment_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:RectangularHyperbola2"], /
    ) -> IDFCollection[_g.CurveRectangularHyperbola2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:Uncontrolled"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctUncontrolled_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:StagedDualSetpoint"], /
    ) -> IDFCollection[_v.ZoneControlThermostatStagedDualSetpoint_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Shading:Overhang:Projection"], /
    ) -> IDFCollection[_g.ShadingOverhangProjection]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:BoundaryLayerDiffusion"], /
    ) -> IDFCollection[_g.SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricEquipment"], /
    ) -> IDFCollection[_v.ElectricEquipment_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:UserDefined"], /
    ) -> IDFCollection[_v.CoilUserDefined_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:HorizontalOpening"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneComponentHorizontalOpening]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:FanCoil"], /
    ) -> IDFCollection[_v.HVACTemplateZoneFanCoil_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:HighTemperatureTurnOn"], /
    ) -> IDFCollection[_g.AvailabilityManagerHighTemperatureTurnOn]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:SQLite"], /) -> IDFCollection[_v.OutputSQLite_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Generators"], /
    ) -> IDFCollection[_g.ElectricLoadCenterGenerators]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:SpectrumData"], /) -> IDFCollection[_g.SiteSpectrumData]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:ExposedFoundationPerimeter"], /
    ) -> IDFCollection[_v.SurfacePropertyExposedFoundationPerimeter_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:ChillerSupplyWater"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetChillerSupplyWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeFluidCooler:SingleSpeed"], /
    ) -> IDFCollection[_v.EvaporativeFluidCoolerSingleSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneTerminalUnitList"], /) -> IDFCollection[_g.ZoneTerminalUnitList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:Mixer"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CondenserEquipmentOperationSchemes"], /
    ) -> IDFCollection[_g.CondenserEquipmentOperationSchemes]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:Reheat"], /
    ) -> IDFCollection[_g.AirTerminalSingleDuctConstantVolumeReheat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Sensor"], /
    ) -> IDFCollection[_g.EnergyManagementSystemSensor]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:MicroTurbine"], /
    ) -> IDFCollection[_v.GeneratorMicroTurbine_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ParallelPIU:Reheat"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctParallelPIUReheat_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableRefrigerantFlow"], /
    ) -> IDFCollection[_g.CoilCoolingDXVariableRefrigerantFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:Ice:Simple"], /
    ) -> IDFCollection[_v.ThermalStorageIceSimple_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Refrigeration:System"], /) -> IDFCollection[_g.RefrigerationSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:DaylightFactors"], /
    ) -> IDFCollection[_g.OutputDaylightFactors]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:System"], /
    ) -> IDFCollection[_v.GroundHeatExchangerSystem_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Dehumidifier:Desiccant:NoFans"], /
    ) -> IDFCollection[_g.DehumidifierDesiccantNoFans]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Site:HeightVariation"], /) -> IDFCollection[_g.SiteHeightVariation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:HighTemperatureRadiant"], /
    ) -> IDFCollection[_v.ZoneHVACHighTemperatureRadiant_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Storage"], /) -> IDFCollection[_g.WaterUseStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:OneNodeDisplacementVentilation"], /
    ) -> IDFCollection[_g.RoomAirSettingsOneNodeDisplacementVentilation]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:RecurringCosts"], /
    ) -> IDFCollection[_v.LifeCycleCostRecurringCosts_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:TwoGradient"], /
    ) -> IDFCollection[_v.RoomAirTemperaturePatternTwoGradient_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirContaminantBalance"], /
    ) -> IDFCollection[_g.ZoneAirContaminantBalance]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneMixing"], /) -> IDFCollection[_v.ZoneMixing_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneSurface]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoilPerformance:DX:Cooling"], /
    ) -> IDFCollection[_g.CoilPerformanceDXCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:MultiSpeed"], /
    ) -> IDFCollection[_v.CoilHeatingDXMultiSpeed_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneVentilation:DesignFlowRate"], /
    ) -> IDFCollection[_v.ZoneVentilationDesignFlowRate_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:StormWindow"], /
    ) -> IDFCollection[_v.WindowPropertyStormWindow_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:SurfaceProps"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementSurfaceProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:WaterMainsTemperature"], /
    ) -> IDFCollection[_v.SiteWaterMainsTemperature_v8_9]: ...
    @overload
    def __getitem__(self, obj_type: Literal["CondenserLoop"], /) -> IDFCollection[_g.CondenserLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AvailabilityManager:NightCycle"], /
    ) -> IDFCollection[_g.AvailabilityManagerNightCycle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:Uncontrolled"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationUncontrolled]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Constant"], /) -> IDFCollection[_g.ScheduleConstant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Suction"], /
    ) -> IDFCollection[_v.MaterialPropertyHeatAndMoistureTransferSuction_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Diagnostics"], /
    ) -> IDFCollection[_v.OutputDiagnostics_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:PipeCircuit"], /
    ) -> IDFCollection[_v.PipingSystemUndergroundPipeCircuit_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundReflectance:SnowModifier"], /
    ) -> IDFCollection[_g.SiteGroundReflectanceSnowModifier]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Absorption:Indirect"], /
    ) -> IDFCollection[_g.ChillerAbsorptionIndirect]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GlobalGeometryRules"], /
    ) -> IDFCollection[_v.GlobalGeometryRules_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:DedicatedOutdoorAir"], /
    ) -> IDFCollection[_g.HVACTemplateSystemDedicatedOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Settings"], /
    ) -> IDFCollection[_g.MaterialPropertyHeatAndMoistureTransferSettings]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollectorPerformance:IntegralCollectorStorage"], /
    ) -> IDFCollection[_v.SolarCollectorPerformanceIntegralCollectorStorage_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundDomain:Slab"], /
    ) -> IDFCollection[_v.SiteGroundDomainSlab_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:ManualGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabManualGrid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Daylighting:DELight:ComplexFenestration"], /
    ) -> IDFCollection[_g.DaylightingDELightComplexFenestration]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CondenserEquipmentList"], /
    ) -> IDFCollection[_v.CondenserEquipmentList_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:ZoneExhaustFan"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneComponentZoneExhaustFan]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComplexFenestrationProperty:SolarAbsorbedLayers"], /
    ) -> IDFCollection[_g.ComplexFenestrationPropertySolarAbsorbedLayers]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating"], /
    ) -> IDFCollection[_g.ThermostatSetpointThermalComfortFangerSingleHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:OutdoorAirPretreat"], /
    ) -> IDFCollection[_g.SetpointManagerOutdoorAirPretreat]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:ElectricalStorage"], /
    ) -> IDFCollection[_g.GeneratorFuelCellElectricalStorage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Tower:ObjectReference"], /
    ) -> IDFCollection[_g.HVACTemplatePlantTowerObjectReference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:FlowCoefficient"], /
    ) -> IDFCollection[_v.ZoneInfiltrationFlowCoefficient_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:ComplexShade"], /
    ) -> IDFCollection[_v.WindowMaterialComplexShade_v8_9]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Lights"], /) -> IDFCollection[_v.Lights_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:WarmestTemperatureFlow"], /
    ) -> IDFCollection[_g.SetpointManagerWarmestTemperatureFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeaderedPumps:VariableSpeed"], /
    ) -> IDFCollection[_v.HeaderedPumpsVariableSpeed_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Electric"], /) -> IDFCollection[_g.CoilHeatingElectric]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:SurfaceGroup"], /
    ) -> IDFCollection[_g.ZoneHVACLowTemperatureRadiantSurfaceGroup]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:PackagedTerminalAirConditioner"], /
    ) -> IDFCollection[_v.ZoneHVACPackagedTerminalAirConditioner_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Bicubic"], /) -> IDFCollection[_g.CurveBicubic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowThermalModel:Params"], /
    ) -> IDFCollection[_g.WindowThermalModelParams]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:OutdoorAirSystem:EquipmentList"], /
    ) -> IDFCollection[_g.AirLoopHVACOutdoorAirSystemEquipmentList]: ...
    @overload
    def __getitem__(self, obj_type: Literal["BranchList"], /) -> IDFCollection[_g.BranchList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:EnthalpySensorOffset:OutdoorAir"], /
    ) -> IDFCollection[_g.FaultModelEnthalpySensorOffsetOutdoorAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceContaminantSourceAndSink:Generic:DepositionVelocitySink"], /
    ) -> IDFCollection[_g.SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SizingPeriod:DesignDay"], /
    ) -> IDFCollection[_v.SizingPeriodDesignDay_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidCooler:SingleSpeed"], /
    ) -> IDFCollection[_g.FluidCoolerSingleSpeed]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside:AdaptiveModelSelections"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Control"], /
    ) -> IDFCollection[_g.GroundHeatTransferControl]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:FuelSupply"], /) -> IDFCollection[_g.GeneratorFuelSupply]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:PipeSegment"], /
    ) -> IDFCollection[_g.PipingSystemUndergroundPipeSegment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Schedules"], /) -> IDFCollection[_g.OutputSchedules]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:EquationFit"], /
    ) -> IDFCollection[_v.CoilCoolingWaterToAirHeatPumpEquationFit_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:RadiantConvective:Water"], /
    ) -> IDFCollection[_v.ZoneHVACBaseboardRadiantConvectiveWater_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:Unitary"], /
    ) -> IDFCollection[_g.HVACTemplateZoneUnitary]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:SupplyPath"], /
    ) -> IDFCollection[_g.AirLoopHVACSupplyPath]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:AirFilter"], /
    ) -> IDFCollection[_g.FaultModelFoulingAirFilter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CompressorList"], /
    ) -> IDFCollection[_g.RefrigerationCompressorList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneInfiltration:DesignFlowRate"], /
    ) -> IDFCollection[_v.ZoneInfiltrationDesignFlowRate_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:PVWatts"], /) -> IDFCollection[_g.GeneratorPVWatts]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:ElectricEquipment"], /
    ) -> IDFCollection[_v.DemandManagerElectricEquipment_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Glazing"], /
    ) -> IDFCollection[_g.WindowMaterialGlazing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:VariableSpeed"], /
    ) -> IDFCollection[_v.CoolingTowerVariableSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Exterior:WaterEquipment"], /
    ) -> IDFCollection[_g.ExteriorWaterEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["ZoneEarthtube"], /) -> IDFCollection[_v.ZoneEarthtube_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Dehumidifier:DX"], /
    ) -> IDFCollection[_g.ZoneHVACDehumidifierDX]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnTemperature:HotWater"], /
    ) -> IDFCollection[_g.SetpointManagerReturnTemperatureHotWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneControl:Thermostat:ThermalComfort"], /
    ) -> IDFCollection[_g.ZoneControlThermostatThermalComfort]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:RectangularHyperbola1"], /
    ) -> IDFCollection[_g.CurveRectangularHyperbola1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:Mixer"], /) -> IDFCollection[_g.OutdoorAirMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundTemperature:Deep"], /
    ) -> IDFCollection[_g.SiteGroundTemperatureDeep]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HotWaterEquipment"], /
    ) -> IDFCollection[_v.HotWaterEquipment_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Steam"], /) -> IDFCollection[_g.CoilHeatingSteam]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PipingSystem:Underground:Domain"], /
    ) -> IDFCollection[_v.PipingSystemUndergroundDomain_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:CaseAndWalkInList"], /
    ) -> IDFCollection[_g.RefrigerationCaseAndWalkInList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:To:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImportToVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:PackagedTerminalHeatPump"], /
    ) -> IDFCollection[_v.ZoneHVACPackagedTerminalHeatPump_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"], /
    ) -> IDFCollection[_g.CoilHeatingDXVariableRefrigerantFlowFluidTemperatureControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Heating"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctVAVHeatAndCoolReheat_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Controller:MechanicalVentilation"], /
    ) -> IDFCollection[_v.ControllerMechanicalVentilation_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:VAV"], /
    ) -> IDFCollection[_g.HVACTemplateSystemVAV]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:AirToAir:FlatPlate"], /
    ) -> IDFCollection[_g.HeatExchangerAirToAirFlatPlate]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Constructions"], /) -> IDFCollection[_g.OutputConstructions]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DesignSpecification:ZoneHVAC:Sizing"], /
    ) -> IDFCollection[_g.DesignSpecificationZoneHVACSizing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:NonrecurringCost"], /
    ) -> IDFCollection[_v.LifeCycleCostNonrecurringCost_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:Constant"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkGenericConstant]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DaylightingDevice:Tubular"], /
    ) -> IDFCollection[_g.DaylightingDeviceTubular]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperationSchemes"], /
    ) -> IDFCollection[_v.PlantEquipmentOperationSchemes_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR"], /
    ) -> IDFCollection[_v.AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:WindPressureCoefficientArray"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneWindPressureCoefficientArray]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Heating:Average"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneHeatingAverage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:MatlProps"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabMatlProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatOnly"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryHeatOnly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:MeteredOutputVariable"], /
    ) -> IDFCollection[_v.EnergyManagementSystemMeteredOutputVariable_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:CfactorUndergroundWall"], /
    ) -> IDFCollection[_g.ConstructionCfactorUndergroundWall]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Table:OneIndependentVariable"], /
    ) -> IDFCollection[_v.TableOneIndependentVariable_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Chiller:Electric"], /
    ) -> IDFCollection[_v.ChillerElectric_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneCapacitanceMultiplier:ResearchSpecial"], /
    ) -> IDFCollection[_g.ZoneCapacitanceMultiplierResearchSpecial]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Week:Compact"], /) -> IDFCollection[_g.ScheduleWeekCompact]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTower:SingleSpeed"], /
    ) -> IDFCollection[_v.CoolingTowerSingleSpeed_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Roof"], /) -> IDFCollection[_v.Roof_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:DebuggingData"], /
    ) -> IDFCollection[_v.OutputDebuggingData_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:CombustionTurbine"], /
    ) -> IDFCollection[_v.GeneratorCombustionTurbine_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Pump:VariableSpeed"], /
    ) -> IDFCollection[_v.PumpVariableSpeed_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Humidity:Minimum"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneHumidityMinimum]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Week:Daily"], /) -> IDFCollection[_g.ScheduleWeekDaily]: ...
    @overload
    def __getitem__(self, obj_type: Literal["TemperingValve"], /) -> IDFCollection[_g.TemperingValve]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComponentCost:Adjustments"], /
    ) -> IDFCollection[_g.ComponentCostAdjustments]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Gas:MultiStage"], /
    ) -> IDFCollection[_v.CoilHeatingGasMultiStage_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDryBulbDifference"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorDryBulbDifference]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:IntraZone:Node"], /
    ) -> IDFCollection[_g.AirflowNetworkIntraZoneNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctVAVReheatVariableSpeedFan_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"], /
    ) -> IDFCollection[_v.CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Site:GroundReflectance"], /
    ) -> IDFCollection[_g.SiteGroundReflectance]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:ConstantVolume:CooledBeam"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctConstantVolumeCooledBeam_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ConvergenceLimits"], /
    ) -> IDFCollection[_v.ConvergenceLimits_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:AirDistributionUnit"], /
    ) -> IDFCollection[_g.ZoneHVACAirDistributionUnit]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:StackCooler"], /
    ) -> IDFCollection[_g.GeneratorFuelCellStackCooler]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MultiZone:Cooling:Average"], /
    ) -> IDFCollection[_g.SetpointManagerMultiZoneCoolingAverage]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Chiller:Absorption"], /) -> IDFCollection[_g.ChillerAbsorption]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:ShadingControl"], /
    ) -> IDFCollection[_v.WindowPropertyShadingControl_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:OneStageHeating"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneOneStageHeating]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Branch"], /) -> IDFCollection[_g.Branch]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorRelativeHumidity"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorRelativeHumidity]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Schedule:Day:List"], /
    ) -> IDFCollection[_v.ScheduleDayList_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:ParameterEstimation:Heating"], /
    ) -> IDFCollection[_g.HeatPumpWaterToWaterParameterEstimationHeating]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:Interior"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementInterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:MixedAir"], /
    ) -> IDFCollection[_g.SetpointManagerMixedAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentList"], /
    ) -> IDFCollection[_v.PlantEquipmentList_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Coil:Heating:Water"], /) -> IDFCollection[_g.CoilHeatingWater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Window:Interzone"], /) -> IDFCollection[_g.WindowInterzone]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:GasCooler:AirCooled"], /
    ) -> IDFCollection[_g.RefrigerationGasCoolerAirCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAirSettings:UnderFloorAirDistributionExterior"], /
    ) -> IDFCollection[_g.RoomAirSettingsUnderFloorAirDistributionExterior]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctVAVHeatAndCoolNoReheat_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HybridModel:Zone"], /
    ) -> IDFCollection[_v.HybridModelZone_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Sigmoid"], /) -> IDFCollection[_g.CurveSigmoid]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:Desuperheater"], /
    ) -> IDFCollection[_v.CoilWaterHeatingDesuperheater_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:SeriesPIU:Reheat"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctSeriesPIUReheat_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:IntraZone:Linkage"], /
    ) -> IDFCollection[_g.AirflowNetworkIntraZoneLinkage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatPump:WaterToWater:EquationFit:Cooling"], /
    ) -> IDFCollection[_v.HeatPumpWaterToWaterEquationFitCooling_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Fan:ConstantVolume"], /) -> IDFCollection[_g.FanConstantVolume]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Building"], /) -> IDFCollection[_v.Building_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Generator:MicroCHP"], /) -> IDFCollection[_g.GeneratorMicroCHP]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Superheated"], /
    ) -> IDFCollection[_g.FluidPropertiesSuperheated]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Actuator"], /
    ) -> IDFCollection[_g.ExternalInterfaceActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:SingleZone:Cooling"], /
    ) -> IDFCollection[_g.SetpointManagerSingleZoneCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:WaterCooled"], /
    ) -> IDFCollection[_g.RefrigerationCondenserWaterCooled]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Blind"], /) -> IDFCollection[_g.WindowMaterialBlind]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CentralHeatPumpSystem"], /
    ) -> IDFCollection[_v.CentralHeatPumpSystem_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:CondenserSupplyWater"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetCondenserSupplyWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:ZoneControl:PressureController"], /
    ) -> IDFCollection[_g.AirflowNetworkZoneControlPressureController]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:Cascade"], /
    ) -> IDFCollection[_g.RefrigerationCondenserCascade]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:DepositionRateSink"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkGenericDepositionRateSink]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EquipmentList"], /
    ) -> IDFCollection[_v.ZoneHVACEquipmentList_v8_9_to_v9_0]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:FrameAndDivider"], /
    ) -> IDFCollection[_v.WindowPropertyFrameAndDivider_v8_9_to_v9_6]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:VariableSpeed"], /
    ) -> IDFCollection[_v.CoilCoolingDXVariableSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatExchanger:Pond"], /
    ) -> IDFCollection[_v.GroundHeatExchangerPond_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Table:MultiVariableLookup"], /
    ) -> IDFCollection[_v.TableMultiVariableLookup_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantComponent:TemperatureSource"], /
    ) -> IDFCollection[_g.PlantComponentTemperatureSource]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:IlluminanceMap:Style"], /
    ) -> IDFCollection[_g.OutputControlIlluminanceMapStyle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:SingleHeatingOrCooling"], /
    ) -> IDFCollection[_g.ThermostatSetpointSingleHeatingOrCooling]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Screen"], /) -> IDFCollection[_g.WindowMaterialScreen]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:WaterToAirHeatPump"], /
    ) -> IDFCollection[_v.ZoneHVACWaterToAirHeatPump_v8_9_to_v9_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EnergyRecoveryVentilator:Controller"], /
    ) -> IDFCollection[_g.ZoneHVACEnergyRecoveryVentilatorController]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Detailed"], /) -> IDFCollection[_v.FloorDetailed_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperties:VaporCoefficients"], /
    ) -> IDFCollection[_g.SurfacePropertiesVaporCoefficients]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HeatExchanger:FluidToFluid"], /
    ) -> IDFCollection[_v.HeatExchangerFluidToFluid_v8_9_to_v25_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitarySystem"], /
    ) -> IDFCollection[_v.AirLoopHVACUnitarySystem_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:TrendVariable"], /
    ) -> IDFCollection[_v.EnergyManagementSystemTrendVariable_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:UnitarySystem"], /
    ) -> IDFCollection[_v.HVACTemplateSystemUnitarySystem_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FluidProperties:Temperatures"], /
    ) -> IDFCollection[_g.FluidPropertiesTemperatures]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:MultiSpeed"], /
    ) -> IDFCollection[_v.CoilCoolingDXMultiSpeed_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Shading:Fin:Projection"], /) -> IDFCollection[_g.ShadingFinProjection]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Matrix:TwoDimension"], /
    ) -> IDFCollection[_v.MatrixTwoDimension_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Gas"], /) -> IDFCollection[_g.WindowMaterialGas]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Exterior"], /) -> IDFCollection[_v.WallExterior_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WindowMaterial:Gap"], /) -> IDFCollection[_g.WindowMaterialGap]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:HumidistatOffset"], /
    ) -> IDFCollection[_g.FaultModelHumidistatOffset]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:CubicLinear"], /) -> IDFCollection[_g.CurveCubicLinear]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManagerAssignmentList"], /
    ) -> IDFCollection[_v.DemandManagerAssignmentList_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeaterPerformance:Electric:EIR"], /
    ) -> IDFCollection[_v.ChillerHeaterPerformanceElectricEIR_v8_9_to_v26_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermalStorage:ChilledWater:Stratified"], /
    ) -> IDFCollection[_v.ThermalStorageChilledWaterStratified_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Controller:OutdoorAir"], /
    ) -> IDFCollection[_v.ControllerOutdoorAir_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:Lights"], /
    ) -> IDFCollection[_v.DemandManagerLights_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Construction:InternalSource"], /
    ) -> IDFCollection[_v.ConstructionInternalSource_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:DecaySource"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkGenericDecaySource]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:ExhaustGasToWaterHeatExchanger"], /
    ) -> IDFCollection[_g.GeneratorFuelCellExhaustGasToWaterHeatExchanger]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface:Crack"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneSurfaceCrack]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HVACTemplate:Zone:VRF"], /) -> IDFCollection[_g.HVACTemplateZoneVRF]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:ReturnAirBypassFlow"], /
    ) -> IDFCollection[_g.SetpointManagerReturnAirBypassFlow]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:Baseboard:Convective:Water"], /
    ) -> IDFCollection[_g.ZoneHVACBaseboardConvectiveWater]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:TemperatureSensorOffset:ReturnAir"], /
    ) -> IDFCollection[_g.FaultModelTemperatureSensorOffsetReturnAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:Condenser:EvaporativeCooled"], /
    ) -> IDFCollection[_g.RefrigerationCondenserEvaporativeCooled]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:UnitaryHeatPump:AirToAir"], /
    ) -> IDFCollection[_g.HVACTemplateSystemUnitaryHeatPumpAirToAir]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Meter:MeterFileOnly"], /
    ) -> IDFCollection[_g.OutputMeterMeterFileOnly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitImport:From:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceFunctionalMockupUnitImportFromVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:HeatAndMoistureTransfer:Redistribution"], /
    ) -> IDFCollection[_v.MaterialPropertyHeatAndMoistureTransferRedistribution_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:OutdoorAirFlow"], /
    ) -> IDFCollection[_v.AirflowNetworkDistributionComponentOutdoorAirFlow_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:Variable"], /
    ) -> IDFCollection[_g.ExternalInterfaceVariable]: ...
    @overload
    def __getitem__(self, obj_type: Literal["PlantLoop"], /) -> IDFCollection[_g.PlantLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:XFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementXFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:CoolingLoad"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationCoolingLoad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorWetBulb"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorWetBulb]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoofCeiling:Detailed"], /
    ) -> IDFCollection[_v.RoofCeilingDetailed_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:FourPipeFanCoil"], /
    ) -> IDFCollection[_g.ZoneHVACFourPipeFanCoil]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:GlazingSpectralData"], /
    ) -> IDFCollection[_g.MaterialPropertyGlazingSpectralData]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Biquadratic"], /) -> IDFCollection[_g.CurveBiquadratic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:EvaporativeCoolerUnit"], /
    ) -> IDFCollection[_v.ZoneHVACEvaporativeCoolerUnit_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:BldgData"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementBldgData]: ...
    @overload
    def __getitem__(self, obj_type: Literal["OutdoorAir:NodeList"], /) -> IDFCollection[_g.OutdoorAirNodeList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:HeatingLoad"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationHeatingLoad]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:ExponentialDecay"], /
    ) -> IDFCollection[_g.CurveExponentialDecay]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:HeatExchanger"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentHeatExchanger]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowGroundTemperature"], /
    ) -> IDFCollection[_g.SetpointManagerFollowGroundTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["LifeCycleCost:UsePriceEscalation"], /
    ) -> IDFCollection[_v.LifeCycleCostUsePriceEscalation_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Actuator"], /
    ) -> IDFCollection[_g.EnergyManagementSystemActuator]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Shade:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialShadeEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Chiller:ObjectReference"], /
    ) -> IDFCollection[_g.HVACTemplatePlantChillerObjectReference]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Surfaces:List"], /) -> IDFCollection[_g.OutputSurfacesList]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:PreprocessorMessage"], /
    ) -> IDFCollection[_g.OutputPreprocessorMessage]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:Water:DetailedGeometry"], /
    ) -> IDFCollection[_v.CoilCoolingWaterDetailedGeometry_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(self, obj_type: Literal["HeatBalanceAlgorithm"], /) -> IDFCollection[_g.HeatBalanceAlgorithm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:HeatTransferAlgorithm"], /
    ) -> IDFCollection[_g.SurfacePropertyHeatTransferAlgorithm]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:Chiller"], /
    ) -> IDFCollection[_g.HVACTemplatePlantChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Table:TwoIndependentVariables"], /
    ) -> IDFCollection[_v.TableTwoIndependentVariables_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Plant:MixedWaterLoop"], /
    ) -> IDFCollection[_g.HVACTemplatePlantMixedWaterLoop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Zone"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneZone]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Well"], /) -> IDFCollection[_g.WaterUseWell]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Outside"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmOutside]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:Reheat"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctVAVReheat_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Converter"], /
    ) -> IDFCollection[_g.ElectricLoadCenterStorageConverter]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Refrigeration:SecondarySystem"], /
    ) -> IDFCollection[_v.RefrigerationSecondarySystem_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:Surfaces:Drawing"], /
    ) -> IDFCollection[_g.OutputSurfacesDrawing]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneAirHeatBalanceAlgorithm"], /
    ) -> IDFCollection[_v.ZoneAirHeatBalanceAlgorithm_v8_9_to_v22_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:ExponentialSkewNormal"], /
    ) -> IDFCollection[_g.CurveExponentialSkewNormal]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:Ventilation"], /
    ) -> IDFCollection[_v.DemandManagerVentilation_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DaylightingDevice:Shelf"], /
    ) -> IDFCollection[_g.DaylightingDeviceShelf]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside:UserCurve"], /
    ) -> IDFCollection[_g.SurfaceConvectionAlgorithmInsideUserCurve]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Connector:Mixer"], /) -> IDFCollection[_g.ConnectorMixer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:System:VRF"], /
    ) -> IDFCollection[_v.HVACTemplateSystemVRF_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:UnglazedTranspired:Multisystem"], /
    ) -> IDFCollection[_g.SolarCollectorUnglazedTranspiredMultisystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:SupplyPlenum"], /
    ) -> IDFCollection[_g.AirLoopHVACSupplyPlenum]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling"], /
    ) -> IDFCollection[_g.ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling]: ...
    @overload
    def __getitem__(self, obj_type: Literal["UtilityCost:Ratchet"], /) -> IDFCollection[_g.UtilityCostRatchet]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Storage:Battery"], /
    ) -> IDFCollection[_v.ElectricLoadCenterStorageBattery_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantEquipmentOperation:OutdoorDewpoint"], /
    ) -> IDFCollection[_g.PlantEquipmentOperationOutdoorDewpoint]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Sizing:Plant"], /) -> IDFCollection[_v.SizingPlant_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirTerminal:SingleDuct:VAV:NoReheat"], /
    ) -> IDFCollection[_v.AirTerminalSingleDuctVAVNoReheat_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:ExternalNode"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneExternalNode]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Exterior:Lights"], /) -> IDFCollection[_g.ExteriorLights]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["FaultModel:Fouling:Chiller"], /
    ) -> IDFCollection[_g.FaultModelFoulingChiller]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:CondenserEnteringReset:Ideal"], /
    ) -> IDFCollection[_g.SetpointManagerCondenserEnteringResetIdeal]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Surface:EffectiveLeakageArea"], /
    ) -> IDFCollection[_g.AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed"], /
    ) -> IDFCollection[_v.AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Glazing:RefractionExtinctionMethod"], /
    ) -> IDFCollection[_g.WindowMaterialGlazingRefractionExtinctionMethod]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Material:AirGap"], /) -> IDFCollection[_g.MaterialAirGap]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Timestep"], /) -> IDFCollection[_v.Timestep_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:DX:TwoStageWithHumidityControlMode"], /
    ) -> IDFCollection[_v.CoilCoolingDXTwoStageWithHumidityControlMode_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Floor:Interzone"], /) -> IDFCollection[_v.FloorInterzone_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ComfortViewFactorAngles"], /
    ) -> IDFCollection[_v.ComfortViewFactorAngles_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Wall:Adiabatic"], /) -> IDFCollection[_v.WallAdiabatic_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(self, obj_type: Literal["RoomAir:Node"], /) -> IDFCollection[_g.RoomAirNode]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ExternalInterface:FunctionalMockupUnitExport:To:Schedule"], /
    ) -> IDFCollection[_v.ExternalInterfaceFunctionalMockupUnitExportToSchedule_v8_9_to_v25_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceProperty:Underwater"], /
    ) -> IDFCollection[_g.SurfacePropertyUnderwater]: ...
    @overload
    def __getitem__(self, obj_type: Literal["AirLoopHVAC"], /) -> IDFCollection[_g.AirLoopHVAC]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Output:Meter"], /) -> IDFCollection[_v.OutputMeter_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["DemandManager:Thermostats"], /
    ) -> IDFCollection[_v.DemandManagerThermostats_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["HVACTemplate:Zone:ConstantVolume"], /
    ) -> IDFCollection[_g.HVACTemplateZoneConstantVolume]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowProperty:AirflowControl"], /
    ) -> IDFCollection[_g.WindowPropertyAirflowControl]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:ZFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementZFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Inverter:FunctionOfPower"], /
    ) -> IDFCollection[_g.ElectricLoadCenterInverterFunctionOfPower]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Generator:FuelCell:WaterSupply"], /
    ) -> IDFCollection[_g.GeneratorFuelCellWaterSupply]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["PlantComponent:UserDefined"], /
    ) -> IDFCollection[_v.PlantComponentUserDefined_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:Wrapped"], /
    ) -> IDFCollection[_v.CoilWaterHeatingAirToWaterHeatPumpWrapped_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:HVACEquipment"], /
    ) -> IDFCollection[_v.RoomAirNodeAirflowNetworkHVACEquipment_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(self, obj_type: Literal["FluidProperties:Name"], /) -> IDFCollection[_g.FluidPropertiesName]: ...
    @overload
    def __getitem__(self, obj_type: Literal["GlazedDoor"], /) -> IDFCollection[_v.GlazedDoor_v8_9]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:VariableThermalConductivity"], /
    ) -> IDFCollection[_v.MaterialPropertyVariableThermalConductivity_v8_9_to_v24_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SolarCollector:UnglazedTranspired"], /
    ) -> IDFCollection[_g.SolarCollectorUnglazedTranspired]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:OutputVariable"], /
    ) -> IDFCollection[_g.EnergyManagementSystemOutputVariable]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:HeatPump:WrappedCondenser"], /
    ) -> IDFCollection[_g.WaterHeaterHeatPumpWrappedCondenser]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EvaporativeCooler:Direct:ResearchSpecial"], /
    ) -> IDFCollection[_g.EvaporativeCoolerDirectResearchSpecial]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["MaterialProperty:PhaseChangeHysteresis"], /
    ) -> IDFCollection[_g.MaterialPropertyPhaseChangeHysteresis]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:YFACE"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementYFACE]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:ChillerPartLoadWithLift"], /
    ) -> IDFCollection[_g.CurveChillerPartLoadWithLift]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Schedule:Day:Hourly"], /) -> IDFCollection[_g.ScheduleDayHourly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ChillerHeater:Absorption:DoubleEffect"], /
    ) -> IDFCollection[_g.ChillerHeaterAbsorptionDoubleEffect]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ElectricLoadCenter:Distribution"], /
    ) -> IDFCollection[_g.ElectricLoadCenterDistribution]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:Generic:CutoffModel"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkGenericCutoffModel]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:SimulationControl"], /
    ) -> IDFCollection[_v.AirflowNetworkSimulationControl_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling"], /
    ) -> IDFCollection[_g.ThermostatSetpointThermalComfortFangerSingleCooling]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Output:EnvironmentalImpactFactors"], /
    ) -> IDFCollection[_g.OutputEnvironmentalImpactFactors]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:WaterHeating:AirToWaterHeatPump:Pumped"], /
    ) -> IDFCollection[_v.CoilWaterHeatingAirToWaterHeatPumpPumped_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["EnergyManagementSystem:Subroutine"], /
    ) -> IDFCollection[_g.EnergyManagementSystemSubroutine]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:Fuel"], /
    ) -> IDFCollection[_v.CoilHeatingFuel_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneBaseboard:OutdoorTemperatureControlled"], /
    ) -> IDFCollection[_v.ZoneBaseboardOutdoorTemperatureControlled_v8_9_to_v9_5]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:SimpleGlazingSystem"], /
    ) -> IDFCollection[_g.WindowMaterialSimpleGlazingSystem]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:Functional:PressureDrop"], /
    ) -> IDFCollection[_g.CurveFunctionalPressureDrop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:Electric"], /
    ) -> IDFCollection[_v.ZoneHVACLowTemperatureRadiantElectric_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SetpointManager:FollowOutdoorAirTemperature"], /
    ) -> IDFCollection[_g.SetpointManagerFollowOutdoorAirTemperature]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WaterHeater:HeatPump:PumpedCondenser"], /
    ) -> IDFCollection[_g.WaterHeaterHeatPumpPumpedCondenser]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Curve:Quartic"], /) -> IDFCollection[_g.CurveQuartic]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["OutputControl:Sizing:Style"], /
    ) -> IDFCollection[_g.OutputControlSizingStyle]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowMaterial:Gap:EquivalentLayer"], /
    ) -> IDFCollection[_g.WindowMaterialGapEquivalentLayer]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["WindowGap:DeflectionState"], /
    ) -> IDFCollection[_g.WindowGapDeflectionState]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["CoolingTowerPerformance:YorkCalc"], /
    ) -> IDFCollection[_g.CoolingTowerPerformanceYorkCalc]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Slab:AutoGrid"], /
    ) -> IDFCollection[_g.GroundHeatTransferSlabAutoGrid]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Door"], /) -> IDFCollection[_g.Door]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneHVAC:LowTemperatureRadiant:ConstantFlow"], /
    ) -> IDFCollection[_v.ZoneHVACLowTemperatureRadiantConstantFlow_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["ZoneContaminantSourceAndSink:CarbonDioxide"], /
    ) -> IDFCollection[_g.ZoneContaminantSourceAndSinkCarbonDioxide]: ...
    @overload
    def __getitem__(self, obj_type: Literal["WaterUse:Equipment"], /) -> IDFCollection[_g.WaterUseEquipment]: ...
    @overload
    def __getitem__(self, obj_type: Literal["Meter:Custom"], /) -> IDFCollection[_v.MeterCustom_v8_9_to_v9_2]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:Distribution:Component:ConstantPressureDrop"], /
    ) -> IDFCollection[_g.AirflowNetworkDistributionComponentConstantPressureDrop]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["UnitarySystemPerformance:Multispeed"], /
    ) -> IDFCollection[_v.UnitarySystemPerformanceMultispeed_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirLoopHVAC:Unitary:Furnace:HeatOnly"], /
    ) -> IDFCollection[_g.AirLoopHVACUnitaryFurnaceHeatOnly]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:TemperaturePattern:NondimensionalHeight"], /
    ) -> IDFCollection[_v.RoomAirTemperaturePatternNondimensionalHeight_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["GroundHeatTransfer:Basement:MatlProps"], /
    ) -> IDFCollection[_g.GroundHeatTransferBasementMatlProps]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Heating:WaterToAirHeatPump:ParameterEstimation"], /
    ) -> IDFCollection[_v.CoilHeatingWaterToAirHeatPumpParameterEstimation_v8_9_to_v23_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Curve:DoubleExponentialDecay"], /
    ) -> IDFCollection[_v.CurveDoubleExponentialDecay_v8_9_to_v9_3]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"], /
    ) -> IDFCollection[_v.CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["AirflowNetwork:MultiZone:Component:DetailedOpening"], /
    ) -> IDFCollection[_v.AirflowNetworkMultiZoneComponentDetailedOpening_v8_9_to_v22_1]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["RoomAir:Node:AirflowNetwork:InternalGains"], /
    ) -> IDFCollection[_v.RoomAirNodeAirflowNetworkInternalGains_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(
        self, obj_type: Literal["SurfaceConvectionAlgorithm:Inside"], /
    ) -> IDFCollection[_v.SurfaceConvectionAlgorithmInside_v8_9_to_v9_4]: ...
    @overload
    def __getitem__(self, obj_type: _NotAnObjectTypeOfEnergyPlus8_9, /) -> Never: ...
