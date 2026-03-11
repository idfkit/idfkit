"""Auto-generated type stubs for EnergyPlus 25.2.0 object types.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs 25.2.0
"""

from .objects import IDFObject

# =========================================================================
# Typed object classes (one per EnergyPlus object type)
# =========================================================================

class Version(IDFObject): ...

class SimulationControl(IDFObject):
    do_system_sizing_calculation: str | None
    do_plant_sizing_calculation: str | None
    run_simulation_for_sizing_periods: str | None
    run_simulation_for_weather_file_run_periods: str | None
    do_hvac_sizing_simulation_for_sizing_periods: str | None
    maximum_number_of_hvac_sizing_simulation_passes: int | None

class PerformancePrecisionTradeoffs(IDFObject):
    zone_radiant_exchange_algorithm: str | None
    override_mode: str | None
    maxzonetempdiff: float | None
    maxalloweddeltemp: float | None
    use_representative_surfaces_for_calculations: str | None

class Building(IDFObject):
    north_axis: float | None
    terrain: str | None
    loads_convergence_tolerance_value: float | None
    temperature_convergence_tolerance_value: float | None
    solar_distribution: str | None
    maximum_number_of_warmup_days: int | None
    minimum_number_of_warmup_days: int | None

class ShadowCalculation(IDFObject):
    shading_calculation_update_frequency_method: str | None
    shading_calculation_update_frequency: int | None
    maximum_figures_in_shadow_overlap_calculations: int | None
    polygon_clipping_algorithm: str | None
    pixel_counting_resolution: int | None
    sky_diffuse_modeling_algorithm: str | None
    output_external_shading_calculation_results: str | None
    disable_self_shading_within_shading_zone_groups: str | None
    disable_self_shading_from_shading_zone_groups_to_other_zones: str | None
    shading_zone_group_zonelist_name: str | None

class SurfaceConvectionAlgorithmInside(IDFObject): ...
class SurfaceConvectionAlgorithmOutside(IDFObject): ...

class HeatBalanceAlgorithm(IDFObject):
    surface_temperature_upper_limit: float | None
    minimum_surface_convection_heat_transfer_coefficient_value: float | None
    maximum_surface_convection_heat_transfer_coefficient_value: float | None

class HeatBalanceSettingsConductionFiniteDifference(IDFObject):
    space_discretization_constant: float | None
    relaxation_factor: float | None
    inside_face_surface_temperature_convergence_criteria: float | None

class ZoneAirHeatBalanceAlgorithm(IDFObject):
    do_space_heat_balance_for_sizing: str | None
    do_space_heat_balance_for_simulation: str | None

class ZoneAirContaminantBalance(IDFObject):
    outdoor_carbon_dioxide_schedule_name: str | None
    generic_contaminant_concentration: str | None
    outdoor_generic_contaminant_schedule_name: str | None

class ZoneAirMassFlowConservation(IDFObject):
    infiltration_balancing_method: str | None
    infiltration_balancing_zones: str | None

class ZoneCapacitanceMultiplierResearchSpecial(IDFObject):
    zone_or_zonelist_name: str | None
    temperature_capacity_multiplier: float | None
    humidity_capacity_multiplier: float | None
    carbon_dioxide_capacity_multiplier: float | None
    generic_contaminant_capacity_multiplier: float | None

class Timestep(IDFObject): ...

class ConvergenceLimits(IDFObject):
    maximum_hvac_iterations: int | None
    minimum_plant_iterations: int | None
    maximum_plant_iterations: int | None

class HVACSystemRootFindingAlgorithm(IDFObject):
    number_of_iterations_before_algorithm_switch: int | None

class ComplianceBuilding(IDFObject): ...

class SiteLocation(IDFObject):
    latitude: float | None
    longitude: float | None
    time_zone: float | None
    elevation: float | None
    keep_site_location_information: str | None

class SiteVariableLocation(IDFObject):
    building_location_latitude_schedule: str | None
    building_location_longitude_schedule: str | None
    building_location_orientation_schedule: str | None

class SizingPeriodDesignDay(IDFObject):
    month: int | None
    day_of_month: int | None
    day_type: str | None
    maximum_dry_bulb_temperature: float | None
    daily_dry_bulb_temperature_range: float | None
    dry_bulb_temperature_range_modifier_type: str | None
    dry_bulb_temperature_range_modifier_day_schedule_name: str | None
    humidity_condition_type: str | None
    wetbulb_or_dewpoint_at_maximum_dry_bulb: float | None
    humidity_condition_day_schedule_name: str | None
    humidity_ratio_at_maximum_dry_bulb: float | None
    enthalpy_at_maximum_dry_bulb: float | None
    daily_wet_bulb_temperature_range: float | None
    barometric_pressure: float | None
    wind_speed: float | None
    wind_direction: float | None
    rain_indicator: str | None
    snow_indicator: str | None
    daylight_saving_time_indicator: str | None
    solar_model_indicator: str | None
    beam_solar_day_schedule_name: str | None
    diffuse_solar_day_schedule_name: str | None
    ashrae_clear_sky_optical_depth_for_beam_irradiance_taub_: float | None
    ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud_: float | None
    sky_clearness: float | None
    maximum_number_warmup_days: int | None
    begin_environment_reset_mode: str | None

class SizingPeriodWeatherFileDays(IDFObject):
    begin_month: int | None
    begin_day_of_month: int | None
    end_month: int | None
    end_day_of_month: int | None
    day_of_week_for_start_day: str | None
    use_weather_file_daylight_saving_period: str | None
    use_weather_file_rain_and_snow_indicators: str | None

class SizingPeriodWeatherFileConditionType(IDFObject):
    period_selection: str | None
    day_of_week_for_start_day: str | None
    use_weather_file_daylight_saving_period: str | None
    use_weather_file_rain_and_snow_indicators: str | None

class RunPeriod(IDFObject):
    begin_month: int | None
    begin_day_of_month: int | None
    begin_year: float | None
    end_month: int | None
    end_day_of_month: int | None
    end_year: float | None
    day_of_week_for_start_day: str | None
    use_weather_file_holidays_and_special_days: str | None
    use_weather_file_daylight_saving_period: str | None
    apply_weekend_holiday_rule: str | None
    use_weather_file_rain_indicators: str | None
    use_weather_file_snow_indicators: str | None
    treat_weather_as_actual: str | None
    first_hour_interpolation_starting_values: str | None

class RunPeriodControlSpecialDays(IDFObject):
    start_date: str | None
    duration: float | None
    special_day_type: str | None

class RunPeriodControlDaylightSavingTime(IDFObject):
    end_date: str | None

class WeatherPropertySkyTemperature(IDFObject):
    calculation_type: str | None
    schedule_name: str | None
    use_weather_file_horizontal_ir: str | None

class SiteWeatherStation(IDFObject):
    wind_speed_profile_exponent: float | None
    wind_speed_profile_boundary_layer_thickness: float | None
    air_temperature_sensor_height_above_ground: float | None

class SiteHeightVariation(IDFObject):
    wind_speed_profile_boundary_layer_thickness: float | None
    air_temperature_gradient_coefficient: float | None

class SiteGroundTemperatureBuildingSurface(IDFObject):
    february_ground_temperature: float | None
    march_ground_temperature: float | None
    april_ground_temperature: float | None
    may_ground_temperature: float | None
    june_ground_temperature: float | None
    july_ground_temperature: float | None
    august_ground_temperature: float | None
    september_ground_temperature: float | None
    october_ground_temperature: float | None
    november_ground_temperature: float | None
    december_ground_temperature: float | None

class SiteGroundTemperatureFCfactorMethod(IDFObject):
    february_ground_temperature: float | None
    march_ground_temperature: float | None
    april_ground_temperature: float | None
    may_ground_temperature: float | None
    june_ground_temperature: float | None
    july_ground_temperature: float | None
    august_ground_temperature: float | None
    september_ground_temperature: float | None
    october_ground_temperature: float | None
    november_ground_temperature: float | None
    december_ground_temperature: float | None

class SiteGroundTemperatureShallow(IDFObject):
    february_surface_ground_temperature: float | None
    march_surface_ground_temperature: float | None
    april_surface_ground_temperature: float | None
    may_surface_ground_temperature: float | None
    june_surface_ground_temperature: float | None
    july_surface_ground_temperature: float | None
    august_surface_ground_temperature: float | None
    september_surface_ground_temperature: float | None
    october_surface_ground_temperature: float | None
    november_surface_ground_temperature: float | None
    december_surface_ground_temperature: float | None

class SiteGroundTemperatureDeep(IDFObject):
    february_deep_ground_temperature: float | None
    march_deep_ground_temperature: float | None
    april_deep_ground_temperature: float | None
    may_deep_ground_temperature: float | None
    june_deep_ground_temperature: float | None
    july_deep_ground_temperature: float | None
    august_deep_ground_temperature: float | None
    september_deep_ground_temperature: float | None
    october_deep_ground_temperature: float | None
    november_deep_ground_temperature: float | None
    december_deep_ground_temperature: float | None

class SiteGroundTemperatureUndisturbedFiniteDifference(IDFObject):
    soil_thermal_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    soil_moisture_content_volume_fraction: float | None
    soil_moisture_content_volume_fraction_at_saturation: float | None
    evapotranspiration_ground_cover_parameter: float | None

class SiteGroundTemperatureUndisturbedKusudaAchenbach(IDFObject):
    soil_thermal_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    average_soil_surface_temperature: float | None
    average_amplitude_of_surface_temperature: float | None
    phase_shift_of_minimum_surface_temperature: float | None

class SiteGroundTemperatureUndisturbedXing(IDFObject):
    soil_thermal_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    average_soil_surface_temperature: float | None
    soil_surface_temperature_amplitude_1: float | None
    soil_surface_temperature_amplitude_2: float | None
    phase_shift_of_temperature_amplitude_1: float | None
    phase_shift_of_temperature_amplitude_2: float | None

class SiteGroundDomainSlab(IDFObject):
    ground_domain_depth: float | None
    aspect_ratio: float | None
    perimeter_offset: float | None
    soil_thermal_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    soil_moisture_content_volume_fraction: float | None
    soil_moisture_content_volume_fraction_at_saturation: float | None
    undisturbed_ground_temperature_model_type: str | None
    undisturbed_ground_temperature_model_name: str | None
    evapotranspiration_ground_cover_parameter: float | None
    slab_boundary_condition_model_name: str | None
    slab_location: str | None
    slab_material_name: str | None
    horizontal_insulation: str | None
    horizontal_insulation_material_name: str | None
    horizontal_insulation_extents: str | None
    perimeter_insulation_width: float | None
    vertical_insulation: str | None
    vertical_insulation_material_name: str | None
    vertical_insulation_depth: float | None
    simulation_timestep: str | None
    geometric_mesh_coefficient: float | None
    mesh_density_parameter: int | None

class SiteGroundDomainBasement(IDFObject):
    ground_domain_depth: float | None
    aspect_ratio: float | None
    perimeter_offset: float | None
    soil_thermal_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    soil_moisture_content_volume_fraction: float | None
    soil_moisture_content_volume_fraction_at_saturation: float | None
    undisturbed_ground_temperature_model_type: str | None
    undisturbed_ground_temperature_model_name: str | None
    evapotranspiration_ground_cover_parameter: float | None
    basement_floor_boundary_condition_model_name: str | None
    horizontal_insulation: str | None
    horizontal_insulation_material_name: str | None
    horizontal_insulation_extents: str | None
    perimeter_horizontal_insulation_width: float | None
    basement_wall_depth: float | None
    basement_wall_boundary_condition_model_name: str | None
    vertical_insulation: str | None
    basement_wall_vertical_insulation_material_name: str | None
    vertical_insulation_depth: float | None
    simulation_timestep: str | None
    mesh_density_parameter: int | None

class SiteGroundReflectance(IDFObject):
    february_ground_reflectance: float | None
    march_ground_reflectance: float | None
    april_ground_reflectance: float | None
    may_ground_reflectance: float | None
    june_ground_reflectance: float | None
    july_ground_reflectance: float | None
    august_ground_reflectance: float | None
    september_ground_reflectance: float | None
    october_ground_reflectance: float | None
    november_ground_reflectance: float | None
    december_ground_reflectance: float | None

class SiteGroundReflectanceSnowModifier(IDFObject):
    daylighting_ground_reflected_solar_modifier: float | None

class SiteWaterMainsTemperature(IDFObject):
    temperature_schedule_name: str | None
    annual_average_outdoor_air_temperature: float | None
    maximum_difference_in_monthly_average_outdoor_air_temperatures: float | None
    temperature_multiplier: float | None
    temperature_offset: float | None

class SitePrecipitation(IDFObject):
    design_level_for_total_annual_precipitation: float | None
    precipitation_rates_schedule_name: str | None
    average_total_annual_precipitation: float | None

class RoofIrrigation(IDFObject):
    irrigation_rate_schedule_name: str | None
    irrigation_maximum_saturation_threshold: float | None

class SiteSolarAndVisibleSpectrum(IDFObject):
    spectrum_data_method: str | None
    solar_spectrum_data_object_name: str | None
    visible_spectrum_data_object_name: str | None

class SiteSpectrumData(IDFObject):
    spectrum_data_type: str | None
    wavelength: float | None
    spectrum: float | None
    wavelength_1: float | None
    spectrum_2: float | None

class ScheduleTypeLimits(IDFObject):
    lower_limit_value: float | None
    upper_limit_value: float | None
    numeric_type: str | None
    unit_type: str | None

class ScheduleDayHourly(IDFObject):
    schedule_type_limits_name: str | None
    hour_1: float | None
    hour_2: float | None
    hour_3: float | None
    hour_4: float | None
    hour_5: float | None
    hour_6: float | None
    hour_7: float | None
    hour_8: float | None
    hour_9: float | None
    hour_10: float | None
    hour_11: float | None
    hour_12: float | None
    hour_13: float | None
    hour_14: float | None
    hour_15: float | None
    hour_16: float | None
    hour_17: float | None
    hour_18: float | None
    hour_19: float | None
    hour_20: float | None
    hour_21: float | None
    hour_22: float | None
    hour_23: float | None
    hour_24: float | None

class ScheduleDayInterval(IDFObject):
    schedule_type_limits_name: str | None
    interpolate_to_timestep: str | None
    time: str | None
    value_until_time: float | None

class ScheduleDayList(IDFObject):
    schedule_type_limits_name: str | None
    interpolate_to_timestep: str | None
    minutes_per_item: int | None
    value: float | None

class ScheduleWeekDaily(IDFObject):
    sunday_schedule_day_name: str | None
    monday_schedule_day_name: str | None
    tuesday_schedule_day_name: str | None
    wednesday_schedule_day_name: str | None
    thursday_schedule_day_name: str | None
    friday_schedule_day_name: str | None
    saturday_schedule_day_name: str | None
    holiday_schedule_day_name: str | None
    summerdesignday_schedule_day_name: str | None
    winterdesignday_schedule_day_name: str | None
    customday1_schedule_day_name: str | None
    customday2_schedule_day_name: str | None

class ScheduleWeekCompact(IDFObject):
    daytype_list: str | None
    schedule_day_name: str | None

class ScheduleYear(IDFObject):
    schedule_type_limits_name: str | None
    schedule_week_name: str | None
    start_month: float | None
    start_day: float | None
    end_month: float | None
    end_day: float | None

class ScheduleCompact(IDFObject):
    schedule_type_limits_name: str | None
    field: str | None

class ScheduleConstant(IDFObject):
    schedule_type_limits_name: str | None
    hourly_value: float | None

class ScheduleFileShading(IDFObject): ...

class ScheduleFile(IDFObject):
    schedule_type_limits_name: str | None
    file_name: str | None
    column_number: int | None
    rows_to_skip_at_top: int | None
    number_of_hours_of_data: float | None
    column_separator: str | None
    interpolate_to_timestep: str | None
    minutes_per_item: int | None
    adjust_schedule_for_daylight_savings: str | None

class Material(IDFObject):
    roughness: str | None
    thickness: float | None
    conductivity: float | None
    density: float | None
    specific_heat: float | None
    thermal_absorptance: float | None
    solar_absorptance: float | None
    visible_absorptance: float | None

class MaterialNoMass(IDFObject):
    roughness: str | None
    thermal_resistance: float | None
    thermal_absorptance: float | None
    solar_absorptance: float | None
    visible_absorptance: float | None

class MaterialInfraredTransparent(IDFObject): ...

class MaterialAirGap(IDFObject):
    thermal_resistance: float | None

class MaterialRoofVegetation(IDFObject):
    height_of_plants: float | None
    leaf_area_index: float | None
    leaf_reflectivity: float | None
    leaf_emissivity: float | None
    minimum_stomatal_resistance: float | None
    soil_layer_name: str | None
    roughness: str | None
    thickness: float | None
    conductivity_of_dry_soil: float | None
    density_of_dry_soil: float | None
    specific_heat_of_dry_soil: float | None
    thermal_absorptance: float | None
    solar_absorptance: float | None
    visible_absorptance: float | None
    saturation_volumetric_moisture_content_of_the_soil_layer: float | None
    residual_volumetric_moisture_content_of_the_soil_layer: float | None
    initial_volumetric_moisture_content_of_the_soil_layer: float | None
    moisture_diffusion_calculation_method: str | None

class WindowMaterialSimpleGlazingSystem(IDFObject):
    u_factor: float | None
    solar_heat_gain_coefficient: float | None
    visible_transmittance: float | None

class WindowMaterialGlazing(IDFObject):
    optical_data_type: str | None
    window_glass_spectral_data_set_name: str | None
    thickness: float | None
    solar_transmittance_at_normal_incidence: float | None
    front_side_solar_reflectance_at_normal_incidence: float | None
    back_side_solar_reflectance_at_normal_incidence: float | None
    visible_transmittance_at_normal_incidence: float | None
    front_side_visible_reflectance_at_normal_incidence: float | None
    back_side_visible_reflectance_at_normal_incidence: float | None
    infrared_transmittance_at_normal_incidence: float | None
    front_side_infrared_hemispherical_emissivity: float | None
    back_side_infrared_hemispherical_emissivity: float | None
    conductivity: float | None
    dirt_correction_factor_for_solar_and_visible_transmittance: float | None
    solar_diffusing: str | None
    young_s_modulus: float | None
    poisson_s_ratio: float | None
    window_glass_spectral_and_incident_angle_transmittance_data_set_table_name: str | None
    window_glass_spectral_and_incident_angle_front_reflectance_data_set_table_name: str | None
    window_glass_spectral_and_incident_angle_back_reflectance_data_set_table_name: str | None

class WindowMaterialGlazingGroupThermochromic(IDFObject):
    optical_data_temperature: float | None
    window_material_glazing_name: str | None

class WindowMaterialGlazingRefractionExtinctionMethod(IDFObject):
    thickness: float | None
    solar_index_of_refraction: float | None
    solar_extinction_coefficient: float | None
    visible_index_of_refraction: float | None
    visible_extinction_coefficient: float | None
    infrared_transmittance_at_normal_incidence: float | None
    infrared_hemispherical_emissivity: float | None
    conductivity: float | None
    dirt_correction_factor_for_solar_and_visible_transmittance: float | None
    solar_diffusing: str | None

class WindowMaterialGas(IDFObject):
    gas_type: str | None
    thickness: float | None
    conductivity_coefficient_a: float | None
    conductivity_coefficient_b: float | None
    conductivity_coefficient_c: float | None
    viscosity_coefficient_a: float | None
    viscosity_coefficient_b: float | None
    viscosity_coefficient_c: float | None
    specific_heat_coefficient_a: float | None
    specific_heat_coefficient_b: float | None
    specific_heat_coefficient_c: float | None
    molecular_weight: float | None
    specific_heat_ratio: float | None

class WindowGapSupportPillar(IDFObject):
    spacing: float | None
    radius: float | None

class WindowGapDeflectionState(IDFObject):
    deflected_thickness: float | None
    initial_temperature: float | None
    initial_pressure: float | None

class WindowMaterialGasMixture(IDFObject):
    thickness: float | None
    number_of_gases_in_mixture: int | None
    gas_1_type: str | None
    gas_1_fraction: float | None
    gas_2_type: str | None
    gas_2_fraction: float | None
    gas_3_type: str | None
    gas_3_fraction: float | None
    gas_4_type: str | None
    gas_4_fraction: float | None

class WindowMaterialGap(IDFObject):
    thickness: float | None
    gas_or_gas_mixture_: str | None
    pressure: float | None
    deflection_state: str | None
    support_pillar: str | None

class WindowMaterialShade(IDFObject):
    solar_transmittance: float | None
    solar_reflectance: float | None
    visible_transmittance: float | None
    visible_reflectance: float | None
    infrared_hemispherical_emissivity: float | None
    infrared_transmittance: float | None
    thickness: float | None
    conductivity: float | None
    shade_to_glass_distance: float | None
    top_opening_multiplier: float | None
    bottom_opening_multiplier: float | None
    left_side_opening_multiplier: float | None
    right_side_opening_multiplier: float | None
    airflow_permeability: float | None

class WindowMaterialComplexShade(IDFObject):
    layer_type: str | None
    thickness: float | None
    conductivity: float | None
    ir_transmittance: float | None
    front_emissivity: float | None
    back_emissivity: float | None
    top_opening_multiplier: float | None
    bottom_opening_multiplier: float | None
    left_side_opening_multiplier: float | None
    right_side_opening_multiplier: float | None
    front_opening_multiplier: float | None
    slat_width: float | None
    slat_spacing: float | None
    slat_thickness: float | None
    slat_angle: float | None
    slat_conductivity: float | None
    slat_curve: float | None

class WindowMaterialBlind(IDFObject):
    slat_orientation: str | None
    slat_width: float | None
    slat_separation: float | None
    slat_thickness: float | None
    slat_angle: float | None
    slat_conductivity: float | None
    slat_beam_solar_transmittance: float | None
    front_side_slat_beam_solar_reflectance: float | None
    back_side_slat_beam_solar_reflectance: float | None
    slat_diffuse_solar_transmittance: float | None
    front_side_slat_diffuse_solar_reflectance: float | None
    back_side_slat_diffuse_solar_reflectance: float | None
    slat_beam_visible_transmittance: float | None
    front_side_slat_beam_visible_reflectance: float | None
    back_side_slat_beam_visible_reflectance: float | None
    slat_diffuse_visible_transmittance: float | None
    front_side_slat_diffuse_visible_reflectance: float | None
    back_side_slat_diffuse_visible_reflectance: float | None
    slat_infrared_hemispherical_transmittance: float | None
    front_side_slat_infrared_hemispherical_emissivity: float | None
    back_side_slat_infrared_hemispherical_emissivity: float | None
    blind_to_glass_distance: float | None
    blind_top_opening_multiplier: float | None
    blind_bottom_opening_multiplier: float | None
    blind_left_side_opening_multiplier: float | None
    blind_right_side_opening_multiplier: float | None
    minimum_slat_angle: float | None
    maximum_slat_angle: float | None

class WindowMaterialScreen(IDFObject):
    reflected_beam_transmittance_accounting_method: str | None
    diffuse_solar_reflectance: float | None
    diffuse_visible_reflectance: float | None
    thermal_hemispherical_emissivity: float | None
    conductivity: float | None
    screen_material_spacing: float | None
    screen_material_diameter: float | None
    screen_to_glass_distance: float | None
    top_opening_multiplier: float | None
    bottom_opening_multiplier: float | None
    left_side_opening_multiplier: float | None
    right_side_opening_multiplier: float | None
    angle_of_resolution_for_screen_transmittance_output_map: float | str | None

class WindowMaterialShadeEquivalentLayer(IDFObject):
    shade_beam_beam_solar_transmittance: float | None
    front_side_shade_beam_diffuse_solar_transmittance: float | None
    back_side_shade_beam_diffuse_solar_transmittance: float | None
    front_side_shade_beam_diffuse_solar_reflectance: float | None
    back_side_shade_beam_diffuse_solar_reflectance: float | None
    shade_beam_beam_visible_transmittance_at_normal_incidence: float | None
    shade_beam_diffuse_visible_transmittance_at_normal_incidence: float | None
    shade_beam_diffuse_visible_reflectance_at_normal_incidence: float | None
    shade_material_infrared_transmittance: float | None
    front_side_shade_material_infrared_emissivity: float | None
    back_side_shade_material_infrared_emissivity: float | None

class WindowMaterialDrapeEquivalentLayer(IDFObject):
    drape_beam_beam_solar_transmittance_at_normal_incidence: float | None
    front_side_drape_beam_diffuse_solar_transmittance: float | None
    back_side_drape_beam_diffuse_solar_transmittance: float | None
    front_side_drape_beam_diffuse_solar_reflectance: float | None
    back_side_drape_beam_diffuse_solar_reflectance: float | None
    drape_beam_beam_visible_transmittance: float | None
    drape_beam_diffuse_visible_transmittance: float | None
    drape_beam_diffuse_visible_reflectance: float | None
    drape_material_infrared_transmittance: float | None
    front_side_drape_material_infrared_emissivity: float | None
    back_side_drape_material_infrared_emissivity: float | None
    width_of_pleated_fabric: float | None
    length_of_pleated_fabric: float | None

class WindowMaterialBlindEquivalentLayer(IDFObject):
    slat_orientation: str | None
    slat_width: float | None
    slat_separation: float | None
    slat_crown: float | None
    slat_angle: float | None
    front_side_slat_beam_diffuse_solar_transmittance: float | None
    back_side_slat_beam_diffuse_solar_transmittance: float | None
    front_side_slat_beam_diffuse_solar_reflectance: float | None
    back_side_slat_beam_diffuse_solar_reflectance: float | None
    front_side_slat_beam_diffuse_visible_transmittance: float | None
    back_side_slat_beam_diffuse_visible_transmittance: float | None
    front_side_slat_beam_diffuse_visible_reflectance: float | None
    back_side_slat_beam_diffuse_visible_reflectance: float | None
    slat_diffuse_diffuse_solar_transmittance: float | None
    front_side_slat_diffuse_diffuse_solar_reflectance: float | None
    back_side_slat_diffuse_diffuse_solar_reflectance: float | None
    slat_diffuse_diffuse_visible_transmittance: float | None
    front_side_slat_diffuse_diffuse_visible_reflectance: float | None
    back_side_slat_diffuse_diffuse_visible_reflectance: float | None
    slat_infrared_transmittance: float | None
    front_side_slat_infrared_emissivity: float | None
    back_side_slat_infrared_emissivity: float | None
    slat_angle_control: str | None

class WindowMaterialScreenEquivalentLayer(IDFObject):
    screen_beam_beam_solar_transmittance: float | str | None
    screen_beam_diffuse_solar_transmittance: float | None
    screen_beam_diffuse_solar_reflectance: float | None
    screen_beam_beam_visible_transmittance: float | None
    screen_beam_diffuse_visible_transmittance: float | None
    screen_beam_diffuse_visible_reflectance: float | None
    screen_infrared_transmittance: float | None
    screen_infrared_emissivity: float | None
    screen_wire_spacing: float | None
    screen_wire_diameter: float | None

class WindowMaterialGlazingEquivalentLayer(IDFObject):
    optical_data_type: str | None
    window_glass_spectral_data_set_name: str | None
    front_side_beam_beam_solar_transmittance: float | None
    back_side_beam_beam_solar_transmittance: float | None
    front_side_beam_beam_solar_reflectance: float | None
    back_side_beam_beam_solar_reflectance: float | None
    front_side_beam_beam_visible_solar_transmittance: float | None
    back_side_beam_beam_visible_solar_transmittance: float | None
    front_side_beam_beam_visible_solar_reflectance: float | None
    back_side_beam_beam_visible_solar_reflectance: float | None
    front_side_beam_diffuse_solar_transmittance: float | None
    back_side_beam_diffuse_solar_transmittance: float | None
    front_side_beam_diffuse_solar_reflectance: float | None
    back_side_beam_diffuse_solar_reflectance: float | None
    front_side_beam_diffuse_visible_solar_transmittance: float | None
    back_side_beam_diffuse_visible_solar_transmittance: float | None
    front_side_beam_diffuse_visible_solar_reflectance: float | None
    back_side_beam_diffuse_visible_solar_reflectance: float | None
    diffuse_diffuse_solar_transmittance: float | str | None
    front_side_diffuse_diffuse_solar_reflectance: float | str | None
    back_side_diffuse_diffuse_solar_reflectance: float | str | None
    diffuse_diffuse_visible_solar_transmittance: float | str | None
    front_side_diffuse_diffuse_visible_solar_reflectance: float | str | None
    back_side_diffuse_diffuse_visible_solar_reflectance: float | str | None
    infrared_transmittance_applies_to_front_and_back_: float | None
    front_side_infrared_emissivity: float | None
    back_side_infrared_emissivity: float | None
    thermal_resistance: float | None

class WindowMaterialGapEquivalentLayer(IDFObject):
    gas_type: str | None
    thickness: float | None
    gap_vent_type: str | None
    conductivity_coefficient_a: float | None
    conductivity_coefficient_b: float | None
    conductivity_coefficient_c: float | None
    viscosity_coefficient_a: float | None
    viscosity_coefficient_b: float | None
    viscosity_coefficient_c: float | None
    specific_heat_coefficient_a: float | None
    specific_heat_coefficient_b: float | None
    specific_heat_coefficient_c: float | None
    molecular_weight: float | None
    specific_heat_ratio: float | None

class MaterialPropertyMoisturePenetrationDepthSettings(IDFObject):
    water_vapor_diffusion_resistance_factor: float | None
    moisture_equation_coefficient_a: float | None
    moisture_equation_coefficient_b: float | None
    moisture_equation_coefficient_c: float | None
    moisture_equation_coefficient_d: float | None
    surface_layer_penetration_depth: float | str | None
    deep_layer_penetration_depth: float | str | None
    coating_layer_thickness: float | None
    coating_layer_water_vapor_diffusion_resistance_factor: float | None

class MaterialPropertyPhaseChange(IDFObject):
    temperature_coefficient_for_thermal_conductivity: float | None
    temperature: float | None
    enthalpy: float | None

class MaterialPropertyPhaseChangeHysteresis(IDFObject):
    latent_heat_during_the_entire_phase_change_process: float | None
    liquid_state_thermal_conductivity: float | None
    liquid_state_density: float | None
    liquid_state_specific_heat: float | None
    high_temperature_difference_of_melting_curve: float | None
    peak_melting_temperature: float | None
    low_temperature_difference_of_melting_curve: float | None
    solid_state_thermal_conductivity: float | None
    solid_state_density: float | None
    solid_state_specific_heat: float | None
    high_temperature_difference_of_freezing_curve: float | None
    peak_freezing_temperature: float | None
    low_temperature_difference_of_freezing_curve: float | None

class MaterialPropertyVariableThermalConductivity(IDFObject):
    temperature: float | None
    thermal_conductivity: float | None

class MaterialPropertyVariableAbsorptance(IDFObject):
    reference_material_name: str | None
    control_signal: str | None
    thermal_absorptance_function_name: str | None
    thermal_absorptance_schedule_name: str | None
    solar_absorptance_function_name: str | None
    solar_absorptance_schedule_name: str | None

class MaterialPropertyHeatAndMoistureTransferSettings(IDFObject):
    porosity: float | None
    initial_water_content_ratio: float | None

class MaterialPropertyHeatAndMoistureTransferSorptionIsotherm(IDFObject):
    number_of_isotherm_coordinates: int | None
    relative_humidity_fraction_1: float | None
    moisture_content_1: float | None
    relative_humidity_fraction_2: float | None
    moisture_content_2: float | None
    relative_humidity_fraction_3: float | None
    moisture_content_3: float | None
    relative_humidity_fraction_4: float | None
    moisture_content_4: float | None
    relative_humidity_fraction_5: float | None
    moisture_content_5: float | None
    relative_humidity_fraction_6: float | None
    moisture_content_6: float | None
    relative_humidity_fraction_7: float | None
    moisture_content_7: float | None
    relative_humidity_fraction_8: float | None
    moisture_content_8: float | None
    relative_humidity_fraction_9: float | None
    moisture_content_9: float | None
    relative_humidity_fraction_10: float | None
    moisture_content_10: float | None
    relative_humidity_fraction_11: float | None
    moisture_content_11: float | None
    relative_humidity_fraction_12: float | None
    moisture_content_12: float | None
    relative_humidity_fraction_13: float | None
    moisture_content_13: float | None
    relative_humidity_fraction_14: float | None
    moisture_content_14: float | None
    relative_humidity_fraction_15: float | None
    moisture_content_15: float | None
    relative_humidity_fraction_16: float | None
    moisture_content_16: float | None
    relative_humidity_fraction_17: float | None
    moisture_content_17: float | None
    relative_humidity_fraction_18: float | None
    moisture_content_18: float | None
    relative_humidity_fraction_19: float | None
    moisture_content_19: float | None
    relative_humidity_fraction_20: float | None
    moisture_content_20: float | None
    relative_humidity_fraction_21: float | None
    moisture_content_21: float | None
    relative_humidity_fraction_22: float | None
    moisture_content_22: float | None
    relative_humidity_fraction_23: float | None
    moisture_content_23: float | None
    relative_humidity_fraction_24: float | None
    moisture_content_24: float | None
    relative_humidity_fraction_25: float | None
    moisture_content_25: float | None

class MaterialPropertyHeatAndMoistureTransferSuction(IDFObject):
    number_of_suction_points: int | None
    moisture_content_1: float | None
    liquid_transport_coefficient_1: float | None
    moisture_content_2: float | None
    liquid_transport_coefficient_2: float | None
    moisture_content_3: float | None
    liquid_transport_coefficient_3: float | None
    moisture_content_4: float | None
    liquid_transport_coefficient_4: float | None
    moisture_content_5: float | None
    liquid_transport_coefficient_5: float | None
    moisture_content_6: float | None
    liquid_transport_coefficient_6: float | None
    moisture_content_7: float | None
    liquid_transport_coefficient_7: float | None
    moisture_content_8: float | None
    liquid_transport_coefficient_8: float | None
    moisture_content_9: float | None
    liquid_transport_coefficient_9: float | None
    moisture_content_10: float | None
    liquid_transport_coefficient_10: float | None
    moisture_content_11: float | None
    liquid_transport_coefficient_11: float | None
    moisture_content_12: float | None
    liquid_transport_coefficient_12: float | None
    moisture_content_13: float | None
    liquid_transport_coefficient_13: float | None
    moisture_content_14: float | None
    liquid_transport_coefficient_14: float | None
    moisture_content_15: float | None
    liquid_transport_coefficient_15: float | None
    moisture_content_16: float | None
    liquid_transport_coefficient_16: float | None
    moisture_content_17: float | None
    liquid_transport_coefficient_17: float | None
    moisture_content_18: float | None
    liquid_transport_coefficient_18: float | None
    moisture_content_19: float | None
    liquid_transport_coefficient_19: float | None
    moisture_content_20: float | None
    liquid_transport_coefficient_20: float | None
    moisture_content_21: float | None
    liquid_transport_coefficient_21: float | None
    moisture_content_22: float | None
    liquid_transport_coefficient_22: float | None
    moisture_content_23: float | None
    liquid_transport_coefficient_23: float | None
    moisture_content_24: float | None
    liquid_transport_coefficient_24: float | None
    moisture_content_25: float | None
    liquid_transport_coefficient_25: float | None

class MaterialPropertyHeatAndMoistureTransferRedistribution(IDFObject):
    number_of_redistribution_points: int | None
    moisture_content_1: float | None
    liquid_transport_coefficient_1: float | None
    moisture_content_2: float | None
    liquid_transport_coefficient_2: float | None
    moisture_content_3: float | None
    liquid_transport_coefficient_3: float | None
    moisture_content_4: float | None
    liquid_transport_coefficient_4: float | None
    moisture_content_5: float | None
    liquid_transport_coefficient_5: float | None
    moisture_content_6: float | None
    liquid_transport_coefficient_6: float | None
    moisture_content_7: float | None
    liquid_transport_coefficient_7: float | None
    moisture_content_8: float | None
    liquid_transport_coefficient_8: float | None
    moisture_content_9: float | None
    liquid_transport_coefficient_9: float | None
    moisture_content_10: float | None
    liquid_transport_coefficient_10: float | None
    moisture_content_11: float | None
    liquid_transport_coefficient_11: float | None
    moisture_content_12: float | None
    liquid_transport_coefficient_12: float | None
    moisture_content_13: float | None
    liquid_transport_coefficient_13: float | None
    moisture_content_14: float | None
    liquid_transport_coefficient_14: float | None
    moisture_content_15: float | None
    liquid_transport_coefficient_15: float | None
    moisture_content_16: float | None
    liquid_transport_coefficient_16: float | None
    moisture_content_17: float | None
    liquid_transport_coefficient_17: float | None
    moisture_content_18: float | None
    liquid_transport_coefficient_18: float | None
    moisture_content_19: float | None
    liquid_transport_coefficient_19: float | None
    moisture_content_20: float | None
    liquid_transport_coefficient_20: float | None
    moisture_content_21: float | None
    liquid_transport_coefficient_21: float | None
    moisture_content_22: float | None
    liquid_transport_coefficient_22: float | None
    moisture_content_23: float | None
    liquid_transport_coefficient_23: float | None
    moisture_content_24: float | None
    liquid_transport_coefficient_24: float | None
    moisture_content_25: float | None
    liquid_transport_coefficient_25: float | None

class MaterialPropertyHeatAndMoistureTransferDiffusion(IDFObject):
    number_of_data_pairs: int | None
    relative_humidity_fraction_1: float | None
    water_vapor_diffusion_resistance_factor_1: float | None
    relative_humidity_fraction_2: float | None
    water_vapor_diffusion_resistance_factor_2: float | None
    relative_humidity_fraction_3: float | None
    water_vapor_diffusion_resistance_factor_3: float | None
    relative_humidity_fraction_4: float | None
    water_vapor_diffusion_resistance_factor_4: float | None
    relative_humidity_fraction_5: float | None
    water_vapor_diffusion_resistance_factor_5: float | None
    relative_humidity_fraction_6: float | None
    water_vapor_diffusion_resistance_factor_6: float | None
    relative_humidity_fraction_7: float | None
    water_vapor_diffusion_resistance_factor_7: float | None
    relative_humidity_fraction_8: float | None
    water_vapor_diffusion_resistance_factor_8: float | None
    relative_humidity_fraction_9: float | None
    water_vapor_diffusion_resistance_factor_9: float | None
    relative_humidity_fraction_10: float | None
    water_vapor_diffusion_resistance_factor_10: float | None
    relative_humidity_fraction_11: float | None
    water_vapor_diffusion_resistance_factor_11: float | None
    relative_humidity_fraction_12: float | None
    water_vapor_diffusion_resistance_factor_12: float | None
    relative_humidity_fraction_13: float | None
    water_vapor_diffusion_resistance_factor_13: float | None
    relative_humidity_fraction_14: float | None
    water_vapor_diffusion_resistance_factor_14: float | None
    relative_humidity_fraction_15: float | None
    water_vapor_diffusion_resistance_factor_15: float | None
    relative_humidity_fraction_16: float | None
    water_vapor_diffusion_resistance_factor_16: float | None
    relative_humidity_fraction_17: float | None
    water_vapor_diffusion_resistance_factor_17: float | None
    relative_humidity_fraction_18: float | None
    water_vapor_diffusion_resistance_factor_18: float | None
    relative_humidity_fraction_19: float | None
    water_vapor_diffusion_resistance_factor_19: float | None
    relative_humidity_fraction_20: float | None
    water_vapor_diffusion_resistance_factor_20: float | None
    relative_humidity_fraction_21: float | None
    water_vapor_diffusion_resistance_factor_21: float | None
    relative_humidity_fraction_22: float | None
    water_vapor_diffusion_resistance_factor_22: float | None
    relative_humidity_fraction_23: float | None
    water_vapor_diffusion_resistance_factor_23: float | None
    relative_humidity_fraction_24: float | None
    water_vapor_diffusion_resistance_factor_24: float | None
    relative_humidity_fraction_25: float | None
    water_vapor_diffusion_resistance_factor_25: float | None

class MaterialPropertyHeatAndMoistureTransferThermalConductivity(IDFObject):
    number_of_thermal_coordinates: int | None
    moisture_content_1: float | None
    thermal_conductivity_1: float | None
    moisture_content_2: float | None
    thermal_conductivity_2: float | None
    moisture_content_3: float | None
    thermal_conductivity_3: float | None
    moisture_content_4: float | None
    thermal_conductivity_4: float | None
    moisture_content_5: float | None
    thermal_conductivity_5: float | None
    moisture_content_6: float | None
    thermal_conductivity_6: float | None
    moisture_content_7: float | None
    thermal_conductivity_7: float | None
    moisture_content_8: float | None
    thermal_conductivity_8: float | None
    moisture_content_9: float | None
    thermal_conductivity_9: float | None
    moisture_content_10: float | None
    thermal_conductivity_10: float | None
    moisture_content_11: float | None
    thermal_conductivity_11: float | None
    moisture_content_12: float | None
    thermal_conductivity_12: float | None
    moisture_content_13: float | None
    thermal_conductivity_13: float | None
    moisture_content_14: float | None
    thermal_conductivity_14: float | None
    moisture_content_15: float | None
    thermal_conductivity_15: float | None
    moisture_content_16: float | None
    thermal_conductivity_16: float | None
    moisture_content_17: float | None
    thermal_conductivity_17: float | None
    moisture_content_18: float | None
    thermal_conductivity_18: float | None
    moisture_content_19: float | None
    thermal_conductivity_19: float | None
    moisture_content_20: float | None
    thermal_conductivity_20: float | None
    moisture_content_21: float | None
    thermal_conductivity_21: float | None
    moisture_content_22: float | None
    thermal_conductivity_22: float | None
    moisture_content_23: float | None
    thermal_conductivity_23: float | None
    moisture_content_24: float | None
    thermal_conductivity_24: float | None
    moisture_content_25: float | None
    thermal_conductivity_25: float | None

class MaterialPropertyGlazingSpectralData(IDFObject):
    wavelength_1: float | None
    transmittance_1: float | None
    front_reflectance_1: float | None
    back_reflectance_1: float | None
    wavelength_2: float | None
    transmittance_2: float | None
    front_reflectance_2: float | None
    back_reflectance_2: float | None
    wavelength_3: float | None
    transmittance_3: float | None
    front_reflectance_3: float | None
    back_reflectance_3: float | None
    wavelength_4: float | None
    transmittance_4: float | None
    front_reflectance_4: float | None
    back_reflectance_4: float | None
    wavelength: float | None
    transmittance: float | None
    front_reflectance: float | None
    back_reflectance: float | None

class Construction(IDFObject):
    outside_layer: str | None
    layer_2: str | None
    layer_3: str | None
    layer_4: str | None
    layer_5: str | None
    layer_6: str | None
    layer_7: str | None
    layer_8: str | None
    layer_9: str | None
    layer_10: str | None

class ConstructionCfactorUndergroundWall(IDFObject):
    c_factor: float | None
    height: float | None

class ConstructionFfactorGroundFloor(IDFObject):
    f_factor: float | None
    area: float | None
    perimeterexposed: float | None

class ConstructionPropertyInternalHeatSource(IDFObject):
    construction_name: str | None
    thermal_source_present_after_layer_number: int | None
    temperature_calculation_requested_after_layer_number: int | None
    dimensions_for_the_ctf_calculation: int | None
    tube_spacing: float | None
    two_dimensional_temperature_calculation_position: float | None

class ConstructionAirBoundary(IDFObject):
    air_exchange_method: str | None
    simple_mixing_air_changes_per_hour: float | None
    simple_mixing_schedule_name: str | None

class WindowThermalModelParams(IDFObject):
    standard: str | None
    thermal_model: str | None
    sdscalar: float | None
    deflection_model: str | None
    vacuum_pressure_limit: float | None
    initial_temperature: float | None
    initial_pressure: float | None

class WindowsCalculationEngine(IDFObject): ...

class ConstructionComplexFenestrationState(IDFObject):
    basis_type: str | None
    basis_symmetry_type: str | None
    window_thermal_model: str | None
    basis_matrix_name: str | None
    solar_optical_complex_front_transmittance_matrix_name: str | None
    solar_optical_complex_back_reflectance_matrix_name: str | None
    visible_optical_complex_front_transmittance_matrix_name: str | None
    visible_optical_complex_back_transmittance_matrix_name: str | None
    outside_layer_name: str | None
    outside_layer_directional_front_absorptance_matrix_name: str | None
    outside_layer_directional_back_absorptance_matrix_name: str | None
    gap_1_name: str | None
    cfs_gap_1_directional_front_absorptance_matrix_name: str | None
    cfs_gap_1_directional_back_absorptance_matrix_name: str | None
    layer_2_name: str | None
    layer_2_directional_front_absorptance_matrix_name: str | None
    layer_2_directional_back_absorptance_matrix_name: str | None
    gap_2_name: str | None
    gap_2_directional_front_absorptance_matrix_name: str | None
    gap_2_directional_back_absorptance_matrix_name: str | None
    layer_3_name: str | None
    layer_3_directional_front_absorptance_matrix_name: str | None
    layer_3_directional_back_absorptance_matrix_name: str | None
    gap_3_name: str | None
    gap_3_directional_front_absorptance_matrix_name: str | None
    gap_3_directional_back_absorptance_matrix_name: str | None
    layer_4_name: str | None
    layer_4_directional_front_absorptance_matrix_name: str | None
    layer_4_directional_back_absorptance_matrix_name: str | None
    gap_4_name: str | None
    gap_4_directional_front_absorptance_matrix_name: str | None
    gap_4_directional_back_absorptance_matrix_name: str | None
    layer_5_name: str | None
    layer_5_directional_front_absorptance_matrix_name: str | None
    layer_5_directional_back_absorptance_matrix_name: str | None

class ConstructionWindowEquivalentLayer(IDFObject):
    outside_layer: str | None
    layer_2: str | None
    layer_3: str | None
    layer_4: str | None
    layer_5: str | None
    layer_6: str | None
    layer_7: str | None
    layer_8: str | None
    layer_9: str | None
    layer_10: str | None
    layer_11: str | None

class ConstructionWindowDataFile(IDFObject):
    file_name: str | None

class GlobalGeometryRules(IDFObject):
    vertex_entry_direction: str | None
    coordinate_system: str | None
    daylighting_reference_point_coordinate_system: str | None
    rectangular_surface_coordinate_system: str | None

class GeometryTransform(IDFObject):
    current_aspect_ratio: float | None
    new_aspect_ratio: float | None

class Space(IDFObject):
    zone_name: str | None
    ceiling_height: float | str | None
    volume: float | str | None
    floor_area: float | str | None
    space_type: str | None
    tag: str | None

class SpaceList(IDFObject):
    space_name: str | None

class Zone(IDFObject):
    direction_of_relative_north: float | None
    x_origin: float | None
    y_origin: float | None
    z_origin: float | None
    type: int | None
    multiplier: int | None
    ceiling_height: float | str | None
    volume: float | str | None
    floor_area: float | str | None
    zone_inside_convection_algorithm: str | None
    zone_outside_convection_algorithm: str | None
    part_of_total_floor_area: str | None

class ZoneList(IDFObject):
    zone_name: str | None

class ZoneGroup(IDFObject):
    zone_list_name: str | None
    zone_list_multiplier: int | None

class BuildingSurfaceDetailed(IDFObject):
    surface_type: str | None
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    outside_boundary_condition: str | None
    outside_boundary_condition_object: str | None
    sun_exposure: str | None
    wind_exposure: str | None
    view_factor_to_ground: float | str | None
    number_of_vertices: float | str | None
    vertex_x_coordinate: float | None
    vertex_y_coordinate: float | None
    vertex_z_coordinate: float | None

class WallDetailed(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    outside_boundary_condition: str | None
    outside_boundary_condition_object: str | None
    sun_exposure: str | None
    wind_exposure: str | None
    view_factor_to_ground: float | str | None
    number_of_vertices: float | str | None
    vertex_x_coordinate: float | None
    vertex_y_coordinate: float | None
    vertex_z_coordinate: float | None

class RoofCeilingDetailed(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    outside_boundary_condition: str | None
    outside_boundary_condition_object: str | None
    sun_exposure: str | None
    wind_exposure: str | None
    view_factor_to_ground: float | str | None
    number_of_vertices: float | str | None
    vertex_x_coordinate: float | None
    vertex_y_coordinate: float | None
    vertex_z_coordinate: float | None

class FloorDetailed(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    outside_boundary_condition: str | None
    outside_boundary_condition_object: str | None
    sun_exposure: str | None
    wind_exposure: str | None
    view_factor_to_ground: float | str | None
    number_of_vertices: float | str | None
    vertex_x_coordinate: float | None
    vertex_y_coordinate: float | None
    vertex_z_coordinate: float | None

class WallExterior(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class WallAdiabatic(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class WallUnderground(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class WallInterzone(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    outside_boundary_condition_object: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class Roof(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    width: float | None

class CeilingAdiabatic(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    width: float | None

class CeilingInterzone(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    outside_boundary_condition_object: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    width: float | None

class FloorGroundContact(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    width: float | None

class FloorAdiabatic(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    width: float | None

class FloorInterzone(IDFObject):
    construction_name: str | None
    zone_name: str | None
    space_name: str | None
    outside_boundary_condition_object: str | None
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    width: float | None

class FenestrationSurfaceDetailed(IDFObject):
    surface_type: str | None
    construction_name: str | None
    building_surface_name: str | None
    outside_boundary_condition_object: str | None
    view_factor_to_ground: float | str | None
    frame_and_divider_name: str | None
    multiplier: float | None
    number_of_vertices: float | str | None
    vertex_1_x_coordinate: float | None
    vertex_1_y_coordinate: float | None
    vertex_1_z_coordinate: float | None
    vertex_2_x_coordinate: float | None
    vertex_2_y_coordinate: float | None
    vertex_2_z_coordinate: float | None
    vertex_3_x_coordinate: float | None
    vertex_3_y_coordinate: float | None
    vertex_3_z_coordinate: float | None
    vertex_4_x_coordinate: float | None
    vertex_4_y_coordinate: float | None
    vertex_4_z_coordinate: float | None

class Window(IDFObject):
    construction_name: str | None
    building_surface_name: str | None
    frame_and_divider_name: str | None
    multiplier: float | None
    starting_x_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class Door(IDFObject):
    construction_name: str | None
    building_surface_name: str | None
    multiplier: float | None
    starting_x_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class GlazedDoor(IDFObject):
    construction_name: str | None
    building_surface_name: str | None
    frame_and_divider_name: str | None
    multiplier: float | None
    starting_x_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class WindowInterzone(IDFObject):
    construction_name: str | None
    building_surface_name: str | None
    outside_boundary_condition_object: str | None
    multiplier: float | None
    starting_x_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class DoorInterzone(IDFObject):
    construction_name: str | None
    building_surface_name: str | None
    outside_boundary_condition_object: str | None
    multiplier: float | None
    starting_x_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class GlazedDoorInterzone(IDFObject):
    construction_name: str | None
    building_surface_name: str | None
    outside_boundary_condition_object: str | None
    multiplier: float | None
    starting_x_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class WindowShadingControl(IDFObject):
    zone_name: str | None
    shading_control_sequence_number: int | None
    shading_type: str | None
    construction_with_shading_name: str | None
    shading_control_type: str | None
    schedule_name: str | None
    setpoint: float | None
    shading_control_is_scheduled: str | None
    glare_control_is_active: str | None
    shading_device_material_name: str | None
    type_of_slat_angle_control_for_blinds: str | None
    slat_angle_schedule_name: str | None
    setpoint_2: float | None
    daylighting_control_object_name: str | None
    multiple_surface_control_type: str | None
    fenestration_surface_name: str | None

class WindowPropertyFrameAndDivider(IDFObject):
    frame_width: float | None
    frame_outside_projection: float | None
    frame_inside_projection: float | None
    frame_conductance: float | None
    ratio_of_frame_edge_glass_conductance_to_center_of_glass_conductance: float | None
    frame_solar_absorptance: float | None
    frame_visible_absorptance: float | None
    frame_thermal_hemispherical_emissivity: float | None
    divider_type: str | None
    divider_width: float | None
    number_of_horizontal_dividers: float | None
    number_of_vertical_dividers: float | None
    divider_outside_projection: float | None
    divider_inside_projection: float | None
    divider_conductance: float | None
    ratio_of_divider_edge_glass_conductance_to_center_of_glass_conductance: float | None
    divider_solar_absorptance: float | None
    divider_visible_absorptance: float | None
    divider_thermal_hemispherical_emissivity: float | None
    outside_reveal_solar_absorptance: float | None
    inside_sill_depth: float | None
    inside_sill_solar_absorptance: float | None
    inside_reveal_depth: float | None
    inside_reveal_solar_absorptance: float | None
    nfrc_product_type_for_assembly_calculations: str | None

class WindowPropertyAirflowControl(IDFObject):
    airflow_source: str | None
    airflow_destination: str | None
    maximum_flow_rate: float | None
    airflow_control_type: str | None
    airflow_is_scheduled: str | None
    airflow_multiplier_schedule_name: str | None
    airflow_return_air_node_name: str | None

class WindowPropertyStormWindow(IDFObject):
    storm_glass_layer_name: str | None
    distance_between_storm_glass_layer_and_adjacent_glass: float | None
    month_that_storm_glass_layer_is_put_on: int | None
    day_of_month_that_storm_glass_layer_is_put_on: int | None
    month_that_storm_glass_layer_is_taken_off: int | None
    day_of_month_that_storm_glass_layer_is_taken_off: int | None

class InternalMass(IDFObject):
    construction_name: str | None
    zone_or_zonelist_name: str | None
    space_or_spacelist_name: str | None
    surface_area: float | None

class ShadingSite(IDFObject):
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class ShadingBuilding(IDFObject):
    azimuth_angle: float | None
    tilt_angle: float | None
    starting_x_coordinate: float | None
    starting_y_coordinate: float | None
    starting_z_coordinate: float | None
    length: float | None
    height: float | None

class ShadingSiteDetailed(IDFObject):
    transmittance_schedule_name: str | None
    number_of_vertices: float | str | None
    vertex_x_coordinate: float | None
    vertex_y_coordinate: float | None
    vertex_z_coordinate: float | None

class ShadingBuildingDetailed(IDFObject):
    transmittance_schedule_name: str | None
    number_of_vertices: float | str | None
    vertex_x_coordinate: float | None
    vertex_y_coordinate: float | None
    vertex_z_coordinate: float | None

class ShadingOverhang(IDFObject):
    window_or_door_name: str | None
    height_above_window_or_door: float | None
    tilt_angle_from_window_door: float | None
    left_extension_from_window_door_width: float | None
    right_extension_from_window_door_width: float | None
    depth: float | None

class ShadingOverhangProjection(IDFObject):
    window_or_door_name: str | None
    height_above_window_or_door: float | None
    tilt_angle_from_window_door: float | None
    left_extension_from_window_door_width: float | None
    right_extension_from_window_door_width: float | None
    depth_as_fraction_of_window_door_height: float | None

class ShadingFin(IDFObject):
    window_or_door_name: str | None
    left_extension_from_window_door: float | None
    left_distance_above_top_of_window: float | None
    left_distance_below_bottom_of_window: float | None
    left_tilt_angle_from_window_door: float | None
    left_depth: float | None
    right_extension_from_window_door: float | None
    right_distance_above_top_of_window: float | None
    right_distance_below_bottom_of_window: float | None
    right_tilt_angle_from_window_door: float | None
    right_depth: float | None

class ShadingFinProjection(IDFObject):
    window_or_door_name: str | None
    left_extension_from_window_door: float | None
    left_distance_above_top_of_window: float | None
    left_distance_below_bottom_of_window: float | None
    left_tilt_angle_from_window_door: float | None
    left_depth_as_fraction_of_window_door_width: float | None
    right_extension_from_window_door: float | None
    right_distance_above_top_of_window: float | None
    right_distance_below_bottom_of_window: float | None
    right_tilt_angle_from_window_door: float | None
    right_depth_as_fraction_of_window_door_width: float | None

class ShadingZoneDetailed(IDFObject):
    base_surface_name: str | None
    transmittance_schedule_name: str | None
    number_of_vertices: float | str | None
    vertex_x_coordinate: float | None
    vertex_y_coordinate: float | None
    vertex_z_coordinate: float | None

class ShadingPropertyReflectance(IDFObject):
    diffuse_solar_reflectance_of_unglazed_part_of_shading_surface: float | None
    diffuse_visible_reflectance_of_unglazed_part_of_shading_surface: float | None
    fraction_of_shading_surface_that_is_glazed: float | None
    glazing_construction_name: str | None

class SurfacePropertyHeatTransferAlgorithm(IDFObject):
    algorithm: str | None

class SurfacePropertyHeatTransferAlgorithmMultipleSurface(IDFObject):
    surface_type: str | None
    algorithm: str | None

class SurfacePropertyHeatTransferAlgorithmSurfaceList(IDFObject):
    algorithm: str | None
    surface_name: str | None

class SurfacePropertyHeatTransferAlgorithmConstruction(IDFObject):
    algorithm: str | None
    construction_name: str | None

class SurfacePropertyHeatBalanceSourceTerm(IDFObject):
    inside_face_heat_source_term_schedule_name: str | None
    outside_face_heat_source_term_schedule_name: str | None

class SurfaceControlMovableInsulation(IDFObject):
    surface_name: str | None
    material_name: str | None
    schedule_name: str | None

class SurfacePropertyOtherSideCoefficients(IDFObject):
    combined_convective_radiative_film_coefficient: float | None
    constant_temperature: float | None
    constant_temperature_coefficient: float | None
    external_dry_bulb_temperature_coefficient: float | None
    ground_temperature_coefficient: float | None
    wind_speed_coefficient: float | None
    zone_air_temperature_coefficient: float | None
    constant_temperature_schedule_name: str | None
    sinusoidal_variation_of_constant_temperature_coefficient: str | None
    period_of_sinusoidal_variation: float | None
    previous_other_side_temperature_coefficient: float | None
    minimum_other_side_temperature_limit: float | None
    maximum_other_side_temperature_limit: float | None

class SurfacePropertyOtherSideConditionsModel(IDFObject):
    type_of_modeling: str | None

class SurfacePropertyUnderwater(IDFObject):
    distance_from_surface_centroid_to_leading_edge_of_boundary_layer: float | None
    free_stream_water_temperature_schedule: str | None
    free_stream_water_velocity_schedule: str | None

class FoundationKiva(IDFObject):
    initial_indoor_air_temperature: float | None
    interior_horizontal_insulation_material_name: str | None
    interior_horizontal_insulation_depth: float | None
    interior_horizontal_insulation_width: float | None
    interior_vertical_insulation_material_name: str | None
    interior_vertical_insulation_depth: float | None
    exterior_horizontal_insulation_material_name: str | None
    exterior_horizontal_insulation_depth: float | None
    exterior_horizontal_insulation_width: float | None
    exterior_vertical_insulation_material_name: str | None
    exterior_vertical_insulation_depth: float | None
    wall_height_above_grade: float | None
    wall_depth_below_slab: float | None
    footing_wall_construction_name: str | None
    footing_material_name: str | None
    footing_depth: float | None
    custom_block_material_name: str | None
    custom_block_depth: float | None
    custom_block_x_position: float | None
    custom_block_z_position: float | None

class FoundationKivaSettings(IDFObject):
    soil_density: float | None
    soil_specific_heat: float | None
    ground_solar_absorptivity: float | None
    ground_thermal_absorptivity: float | None
    ground_surface_roughness: float | None
    far_field_width: float | None
    deep_ground_boundary_condition: str | None
    deep_ground_depth: float | str | None
    minimum_cell_dimension: float | None
    maximum_cell_growth_coefficient: float | None
    simulation_timestep: str | None

class SurfacePropertyExposedFoundationPerimeter(IDFObject):
    exposed_perimeter_calculation_method: str | None
    total_exposed_perimeter: float | None
    exposed_perimeter_fraction: float | None
    surface_segment_exposed: str | None

class SurfaceConvectionAlgorithmInsideAdaptiveModelSelections(IDFObject):
    simple_buoyancy_vertical_wall_equation_source: str | None
    simple_buoyancy_vertical_wall_user_curve_name: str | None
    simple_buoyancy_stable_horizontal_equation_source: str | None
    simple_buoyancy_stable_horizontal_equation_user_curve_name: str | None
    simple_buoyancy_unstable_horizontal_equation_source: str | None
    simple_buoyancy_unstable_horizontal_equation_user_curve_name: str | None
    simple_buoyancy_stable_tilted_equation_source: str | None
    simple_buoyancy_stable_tilted_equation_user_curve_name: str | None
    simple_buoyancy_unstable_tilted_equation_source: str | None
    simple_buoyancy_unstable_tilted_equation_user_curve_name: str | None
    simple_buoyancy_windows_equation_source: str | None
    simple_buoyancy_windows_equation_user_curve_name: str | None
    floor_heat_ceiling_cool_vertical_wall_equation_source: str | None
    floor_heat_ceiling_cool_vertical_wall_equation_user_curve_name: str | None
    floor_heat_ceiling_cool_stable_horizontal_equation_source: str | None
    floor_heat_ceiling_cool_stable_horizontal_equation_user_curve_name: str | None
    floor_heat_ceiling_cool_unstable_horizontal_equation_source: str | None
    floor_heat_ceiling_cool_unstable_horizontal_equation_user_curve_name: str | None
    floor_heat_ceiling_cool_heated_floor_equation_source: str | None
    floor_heat_ceiling_cool_heated_floor_equation_user_curve_name: str | None
    floor_heat_ceiling_cool_chilled_ceiling_equation_source: str | None
    floor_heat_ceiling_cool_chilled_ceiling_equation_user_curve_name: str | None
    floor_heat_ceiling_cool_stable_tilted_equation_source: str | None
    floor_heat_ceiling_cool_stable_tilted_equation_user_curve_name: str | None
    floor_heat_ceiling_cool_unstable_tilted_equation_source: str | None
    floor_heat_ceiling_cool_unstable_tilted_equation_user_curve_name: str | None
    floor_heat_ceiling_cool_window_equation_source: str | None
    floor_heat_ceiling_cool_window_equation_user_curve_name: str | None
    wall_panel_heating_vertical_wall_equation_source: str | None
    wall_panel_heating_vertical_wall_equation_user_curve_name: str | None
    wall_panel_heating_heated_wall_equation_source: str | None
    wall_panel_heating_heated_wall_equation_user_curve_name: str | None
    wall_panel_heating_stable_horizontal_equation_source: str | None
    wall_panel_heating_stable_horizontal_equation_user_curve_name: str | None
    wall_panel_heating_unstable_horizontal_equation_source: str | None
    wall_panel_heating_unstable_horizontal_equation_user_curve_name: str | None
    wall_panel_heating_stable_tilted_equation_source: str | None
    wall_panel_heating_stable_tilted_equation_user_curve_name: str | None
    wall_panel_heating_unstable_tilted_equation_source: str | None
    wall_panel_heating_unstable_tilted_equation_user_curve_name: str | None
    wall_panel_heating_window_equation_source: str | None
    wall_panel_heating_window_equation_user_curve_name: str | None
    convective_zone_heater_vertical_wall_equation_source: str | None
    convective_zone_heater_vertical_wall_equation_user_curve_name: str | None
    convective_zone_heater_vertical_walls_near_heater_equation_source: str | None
    convective_zone_heater_vertical_walls_near_heater_equation_user_curve_name: str | None
    convective_zone_heater_stable_horizontal_equation_source: str | None
    convective_zone_heater_stable_horizontal_equation_user_curve_name: str | None
    convective_zone_heater_unstable_horizontal_equation_source: str | None
    convective_zone_heater_unstable_horizontal_equation_user_curve_name: str | None
    convective_zone_heater_stable_tilted_equation_source: str | None
    convective_zone_heater_stable_tilted_equation_user_curve_name: str | None
    convective_zone_heater_unstable_tilted_equation_source: str | None
    convective_zone_heater_unstable_tilted_equation_user_curve_name: str | None
    convective_zone_heater_windows_equation_source: str | None
    convective_zone_heater_windows_equation_user_curve_name: str | None
    central_air_diffuser_wall_equation_source: str | None
    central_air_diffuser_wall_equation_user_curve_name: str | None
    central_air_diffuser_ceiling_equation_source: str | None
    central_air_diffuser_ceiling_equation_user_curve_name: str | None
    central_air_diffuser_floor_equation_source: str | None
    central_air_diffuser_floor_equation_user_curve_name: str | None
    central_air_diffuser_window_equation_source: str | None
    central_air_diffuser_window_equation_user_curve_name: str | None
    mechanical_zone_fan_circulation_vertical_wall_equation_source: str | None
    mechanical_zone_fan_circulation_vertical_wall_equation_user_curve_name: str | None
    mechanical_zone_fan_circulation_stable_horizontal_equation_source: str | None
    mechanical_zone_fan_circulation_stable_horizontal_equation_user_curve_name: str | None
    mechanical_zone_fan_circulation_unstable_horizontal_equation_source: str | None
    mechanical_zone_fan_circulation_unstable_horizontal_equation_user_curve_name: str | None
    mechanical_zone_fan_circulation_stable_tilted_equation_source: str | None
    mechanical_zone_fan_circulation_stable_tilted_equation_user_curve_name: str | None
    mechanical_zone_fan_circulation_unstable_tilted_equation_source: str | None
    mechanical_zone_fan_circulation_unstable_tilted_equation_user_curve_name: str | None
    mechanical_zone_fan_circulation_window_equation_source: str | None
    mechanical_zone_fan_circulation_window_equation_user_curve_name: str | None
    mixed_regime_buoyancy_assisting_flow_on_walls_equation_source: str | None
    mixed_regime_buoyancy_assisting_flow_on_walls_equation_user_curve_name: str | None
    mixed_regime_buoyancy_opposing_flow_on_walls_equation_source: str | None
    mixed_regime_buoyancy_opposing_flow_on_walls_equation_user_curve_name: str | None
    mixed_regime_stable_floor_equation_source: str | None
    mixed_regime_stable_floor_equation_user_curve_name: str | None
    mixed_regime_unstable_floor_equation_source: str | None
    mixed_regime_unstable_floor_equation_user_curve_name: str | None
    mixed_regime_stable_ceiling_equation_source: str | None
    mixed_regime_stable_ceiling_equation_user_curve_name: str | None
    mixed_regime_unstable_ceiling_equation_source: str | None
    mixed_regime_unstable_ceiling_equation_user_curve_name: str | None
    mixed_regime_window_equation_source: str | None
    mixed_regime_window_equation_user_curve_name: str | None

class SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections(IDFObject):
    wind_convection_windward_vertical_wall_equation_source: str | None
    wind_convection_windward_equation_vertical_wall_user_curve_name: str | None
    wind_convection_leeward_vertical_wall_equation_source: str | None
    wind_convection_leeward_vertical_wall_equation_user_curve_name: str | None
    wind_convection_horizontal_roof_equation_source: str | None
    wind_convection_horizontal_roof_user_curve_name: str | None
    natural_convection_vertical_wall_equation_source: str | None
    natural_convection_vertical_wall_equation_user_curve_name: str | None
    natural_convection_stable_horizontal_equation_source: str | None
    natural_convection_stable_horizontal_equation_user_curve_name: str | None
    natural_convection_unstable_horizontal_equation_source: str | None
    natural_convection_unstable_horizontal_equation_user_curve_name: str | None

class SurfaceConvectionAlgorithmInsideUserCurve(IDFObject):
    reference_temperature_for_convection_heat_transfer: str | None
    hc_function_of_temperature_difference_curve_name: str | None
    hc_function_of_temperature_difference_divided_by_height_curve_name: str | None
    hc_function_of_air_change_rate_curve_name: str | None
    hc_function_of_air_system_volume_flow_rate_divided_by_zone_perimeter_length_curve_name: str | None

class SurfaceConvectionAlgorithmOutsideUserCurve(IDFObject):
    wind_speed_type_for_curve: str | None
    hf_function_of_wind_speed_curve_name: str | None
    hn_function_of_temperature_difference_curve_name: str | None
    hn_function_of_temperature_difference_divided_by_height_curve_name: str | None

class SurfacePropertyConvectionCoefficients(IDFObject):
    convection_coefficient_1_location: str | None
    convection_coefficient_1_type: str | None
    convection_coefficient_1: float | None
    convection_coefficient_1_schedule_name: str | None
    convection_coefficient_1_user_curve_name: str | None
    convection_coefficient_2_location: str | None
    convection_coefficient_2_type: str | None
    convection_coefficient_2: float | None
    convection_coefficient_2_schedule_name: str | None
    convection_coefficient_2_user_curve_name: str | None

class SurfacePropertyConvectionCoefficientsMultipleSurface(IDFObject):
    convection_coefficient_1_location: str | None
    convection_coefficient_1_type: str | None
    convection_coefficient_1: float | None
    convection_coefficient_1_schedule_name: str | None
    convection_coefficient_1_user_curve_name: str | None
    convection_coefficient_2_location: str | None
    convection_coefficient_2_type: str | None
    convection_coefficient_2: float | None
    convection_coefficient_2_schedule_name: str | None
    convection_coefficient_2_user_curve_name: str | None

class SurfacePropertiesVaporCoefficients(IDFObject):
    constant_external_vapor_transfer_coefficient: str | None
    external_vapor_coefficient_value: float | None
    constant_internal_vapor_transfer_coefficient: str | None
    internal_vapor_coefficient_value: float | None

class SurfacePropertyExteriorNaturalVentedCavity(IDFObject):
    boundary_conditions_model_name: str | None
    area_fraction_of_openings: float | None
    thermal_emissivity_of_exterior_baffle_material: float | None
    solar_absorbtivity_of_exterior_baffle: float | None
    height_scale_for_buoyancy_driven_ventilation: float | None
    effective_thickness_of_cavity_behind_exterior_baffle: float | None
    ratio_of_actual_surface_area_to_projected_surface_area: float | None
    roughness_of_exterior_surface: str | None
    effectiveness_for_perforations_with_respect_to_wind: float | None
    discharge_coefficient_for_openings_with_respect_to_buoyancy_driven_flow: float | None
    surface_name: str | None

class SurfacePropertySolarIncidentInside(IDFObject):
    surface_name: str | None
    construction_name: str | None
    inside_surface_incident_sun_solar_radiation_schedule_name: str | None

class SurfacePropertyIncidentSolarMultiplier(IDFObject):
    incident_solar_multiplier: float | None
    incident_solar_multiplier_schedule_name: str | None

class SurfacePropertyLocalEnvironment(IDFObject):
    exterior_surface_name: str | None
    sunlit_fraction_schedule_name: str | None
    surrounding_surfaces_object_name: str | None
    outdoor_air_node_name: str | None
    ground_surfaces_object_name: str | None

class ZonePropertyLocalEnvironment(IDFObject):
    zone_name: str | None
    outdoor_air_node_name: str | None

class SurfacePropertySurroundingSurfaces(IDFObject):
    sky_view_factor: float | None
    sky_temperature_schedule_name: str | None
    ground_view_factor: float | None
    ground_temperature_schedule_name: str | None
    surrounding_surface_name: str | None
    surrounding_surface_view_factor: float | None
    surrounding_surface_temperature_schedule_name: str | None

class SurfacePropertyGroundSurfaces(IDFObject):
    ground_surface_name: str | None
    ground_surface_view_factor: float | None
    ground_surface_temperature_schedule_name: str | None
    ground_surface_reflectance_schedule_name: str | None

class ComplexFenestrationPropertySolarAbsorbedLayers(IDFObject):
    fenestration_surface: str | None
    construction_name: str | None
    layer_1_solar_radiation_absorbed_schedule_name: str | None
    layer_2_solar_radiation_absorbed_schedule_name: str | None
    layer_3_solar_radiation_absorbed_schedule_name: str | None
    layer_4_solar_radiation_absorbed_schedule_name: str | None
    layer_5_solar_radiation_absorbed_schedule_name: str | None

class ZonePropertyUserViewFactorsBySurfaceName(IDFObject):
    from_surface: str | None
    to_surface: str | None
    view_factor: float | None

class GroundHeatTransferControl(IDFObject):
    run_basement_preprocessor: str | None
    run_slab_preprocessor: str | None

class GroundHeatTransferSlabMaterials(IDFObject):
    albedo_surface_albedo_no_snow: float | None
    albedo_surface_albedo_snow: float | None
    epslw_surface_emissivity_no_snow: float | None
    epslw_surface_emissivity_snow: float | None
    z0_surface_roughness_no_snow: float | None
    z0_surface_roughness_snow: float | None
    hin_indoor_hconv_downward_flow: float | None
    hin_indoor_hconv_upward: float | None

class GroundHeatTransferSlabMatlProps(IDFObject):
    rho_soil_density: float | None
    cp_slab_cp: float | None
    cp_soil_cp: float | None
    tcon_slab_k: float | None
    tcon_soil_k: float | None

class GroundHeatTransferSlabBoundConds(IDFObject):
    fixbc_is_the_lower_boundary_at_a_fixed_temperature: str | None
    tdeepin: float | None
    usrhflag_is_the_ground_surface_h_specified_by_the_user_: str | None
    userh_user_specified_ground_surface_heat_transfer_coefficient: float | None

class GroundHeatTransferSlabBldgProps(IDFObject):
    shape_slab_shape: float | None
    hbldg_building_height: float | None
    tin1_january_indoor_average_temperature_setpoint: float | None
    tin2_february_indoor_average_temperature_setpoint: float | None
    tin3_march_indoor_average_temperature_setpoint: float | None
    tin4_april_indoor_average_temperature_setpoint: float | None
    tin5_may_indoor_average_temperature_setpoint: float | None
    tin6_june_indoor_average_temperature_setpoint: float | None
    tin7_july_indoor_average_temperature_setpoint: float | None
    tin8_august_indoor_average_temperature_setpoint: float | None
    tin9_september_indoor_average_temperature_setpoint: float | None
    tin10_october_indoor_average_temperature_setpoint: float | None
    tin11_november_indoor_average_temperature_setpoint: float | None
    tin12_december_indoor_average_temperature_setpoint: float | None
    tinamp_daily_indoor_sine_wave_variation_amplitude: float | None
    convtol_convergence_tolerance: float | None

class GroundHeatTransferSlabInsulation(IDFObject):
    dins_width_of_strip_of_under_slab_insulation: float | None
    rvins_r_value_of_vertical_insulation: float | None
    zvins_depth_of_vertical_insulation: float | None
    ivins_flag_is_there_vertical_insulation: float | str | None

class GroundHeatTransferSlabEquivalentSlab(IDFObject):
    slabdepth_thickness_of_slab_on_grade: float | None
    clearance_distance_from_edge_of_slab_to_domain_edge: float | None
    zclearance_distance_from_bottom_of_slab_to_domain_bottom: float | None

class GroundHeatTransferSlabAutoGrid(IDFObject):
    slaby_y_dimension_of_the_building_slab: float | None
    slabdepth_thickness_of_slab_on_grade: float | None
    clearance_distance_from_edge_of_slab_to_domain_edge: float | None
    zclearance_distance_from_bottom_of_slab_to_domain_bottom: float | None

class GroundHeatTransferSlabManualGrid(IDFObject):
    ny_number_of_cells_in_the_y_direction: float | None
    nz_number_of_cells_in_the_z_direction: float | None
    ibox_x_direction_cell_indicator_of_slab_edge: float | None
    jbox_y_direction_cell_indicator_of_slab_edge: float | None

class GroundHeatTransferSlabXFACE(IDFObject): ...
class GroundHeatTransferSlabYFACE(IDFObject): ...
class GroundHeatTransferSlabZFACE(IDFObject): ...

class GroundHeatTransferBasementSimParameters(IDFObject):
    iyrs_maximum_number_of_yearly_iterations_: float | None

class GroundHeatTransferBasementMatlProps(IDFObject):
    density_for_foundation_wall: float | None
    density_for_floor_slab: float | None
    density_for_ceiling: float | None
    density_for_soil: float | None
    density_for_gravel: float | None
    density_for_wood: float | None
    specific_heat_for_foundation_wall: float | None
    specific_heat_for_floor_slab: float | None
    specific_heat_for_ceiling: float | None
    specific_heat_for_soil: float | None
    specific_heat_for_gravel: float | None
    specific_heat_for_wood: float | None
    thermal_conductivity_for_foundation_wall: float | None
    thermal_conductivity_for_floor_slab: float | None
    thermal_conductivity_for_ceiling: float | None
    thermal_conductivity_for_soil: float | None
    thermal_conductivity_for_gravel: float | None
    thermal_conductivity_for_wood: float | None

class GroundHeatTransferBasementInsulation(IDFObject):
    insfull_flag_is_the_wall_fully_insulated_: str | None

class GroundHeatTransferBasementSurfaceProps(IDFObject):
    albedo_surface_albedo_for_snow_conditions: float | None
    epsln_surface_emissivity_no_snow: float | None
    epsln_surface_emissivity_with_snow: float | None
    veght_surface_roughness_no_snow_conditions: float | None
    veght_surface_roughness_snow_conditions: float | None
    pet_flag_potential_evapotranspiration_on_: str | None

class GroundHeatTransferBasementBldgData(IDFObject):
    dslab_floor_slab_thickness: float | None
    dgravxy_width_of_gravel_pit_beside_basement_wall: float | None
    dgravzn_gravel_depth_extending_above_the_floor_slab: float | None
    dgravzp_gravel_depth_below_the_floor_slab: float | None

class GroundHeatTransferBasementInterior(IDFObject):
    hin_downward_convection_only_heat_transfer_coefficient: float | None
    hin_upward_convection_only_heat_transfer_coefficient: float | None
    hin_horizontal_convection_only_heat_transfer_coefficient: float | None
    hin_downward_combined_convection_and_radiation_heat_transfer_coefficient: float | None
    hin_upward_combined_convection_and_radiation_heat_transfer_coefficient: float | None
    hin_horizontal_combined_convection_and_radiation_heat_transfer_coefficient: float | None

class GroundHeatTransferBasementComBldg(IDFObject):
    february_average_temperature: float | None
    march_average_temperature: float | None
    april_average_temperature: float | None
    may_average_temperature: float | None
    june_average_temperature: float | None
    july_average_temperature: float | None
    august_average_temperature: float | None
    september_average_temperature: float | None
    october_average_temperature: float | None
    november_average_temperature: float | None
    december_average_temperature: float | None
    daily_variation_sine_wave_amplitude: float | None

class GroundHeatTransferBasementEquivSlab(IDFObject):
    equivsizing_flag: str | None

class GroundHeatTransferBasementEquivAutoGrid(IDFObject):
    slabdepth_thickness_of_the_floor_slab: float | None
    basedepth_depth_of_the_basement_wall_below_grade: float | None

class GroundHeatTransferBasementAutoGrid(IDFObject):
    slabx_x_dimension_of_the_building_slab: float | None
    slaby_y_dimension_of_the_building_slab: float | None
    concagheight_height_of_the_foundation_wall_above_grade: float | None
    slabdepth_thickness_of_the_floor_slab: float | None
    basedepth_depth_of_the_basement_wall_below_grade: float | None

class GroundHeatTransferBasementManualGrid(IDFObject):
    ny_number_of_cells_in_the_y_direction_20_: float | None
    nzag_number_of_cells_in_the_z_direction_above_grade_4_always_: float | None
    nzbg_number_of_cells_in_z_direction_below_grade_10_35_: float | None
    ibase_x_direction_cell_indicator_of_slab_edge_5_20_: float | None
    jbase_y_direction_cell_indicator_of_slab_edge_5_20_: float | None
    kbase_z_direction_cell_indicator_of_the_top_of_the_floor_slab_5_20_: float | None

class GroundHeatTransferBasementXFACE(IDFObject): ...
class GroundHeatTransferBasementYFACE(IDFObject): ...
class GroundHeatTransferBasementZFACE(IDFObject): ...

class RoomAirModelType(IDFObject):
    zone_name: str | None
    room_air_modeling_type: str | None
    air_temperature_coupling_strategy: str | None

class RoomAirTemperaturePatternUserDefined(IDFObject):
    zone_name: str | None
    availability_schedule_name: str | None
    pattern_control_schedule_name: str | None

class RoomAirTemperaturePatternConstantGradient(IDFObject):
    control_integer_for_pattern_control_schedule_name: int | None
    thermostat_offset: float | None
    return_air_offset: float | None
    exhaust_air_offset: float | None
    temperature_gradient: float | None

class RoomAirTemperaturePatternTwoGradient(IDFObject):
    control_integer_for_pattern_control_schedule_name: int | None
    thermostat_height: float | None
    return_air_height: float | None
    exhaust_air_height: float | None
    temperature_gradient_lower_bound: float | None
    temperature_gradient_upper_bound: float | None
    gradient_interpolation_mode: str | None
    upper_temperature_bound: float | None
    lower_temperature_bound: float | None
    upper_heat_rate_bound: float | None
    lower_heat_rate_bound: float | None

class RoomAirTemperaturePatternNondimensionalHeight(IDFObject):
    control_integer_for_pattern_control_schedule_name: int | None
    thermostat_offset: float | None
    return_air_offset: float | None
    exhaust_air_offset: float | None
    pair_zeta_nondimensional_height: float | None
    pair_delta_adjacent_air_temperature: float | None

class RoomAirTemperaturePatternSurfaceMapping(IDFObject):
    control_integer_for_pattern_control_schedule_name: int | None
    thermostat_offset: float | None
    return_air_offset: float | None
    exhaust_air_offset: float | None
    surface_name_pair: str | None
    delta_adjacent_air_temperature_pair: float | None

class RoomAirNode(IDFObject):
    node_type: str | None
    zone_name: str | None
    height_of_nodal_control_volume_center: float | None
    surface_1_name: str | None
    surface_2_name: str | None
    surface_3_name: str | None
    surface_4_name: str | None
    surface_5_name: str | None
    surface_6_name: str | None
    surface_7_name: str | None
    surface_8_name: str | None
    surface_9_name: str | None
    surface_10_name: str | None
    surface_11_name: str | None
    surface_12_name: str | None
    surface_13_name: str | None
    surface_14_name: str | None
    surface_15_name: str | None
    surface_16_name: str | None
    surface_17_name: str | None
    surface_18_name: str | None
    surface_19_name: str | None
    surface_20_name: str | None
    surface_21_name: str | None

class RoomAirSettingsOneNodeDisplacementVentilation(IDFObject):
    fraction_of_convective_internal_loads_added_to_floor_air: float | None
    fraction_of_infiltration_internal_loads_added_to_floor_air: float | None

class RoomAirSettingsThreeNodeDisplacementVentilation(IDFObject):
    gain_distribution_schedule_name: str | None
    number_of_plumes_per_occupant: float | None
    thermostat_height: float | None
    comfort_height: float | None
    temperature_difference_threshold_for_reporting: float | None

class RoomAirSettingsCrossVentilation(IDFObject):
    gain_distribution_schedule_name: str | None
    airflow_region_used_for_thermal_comfort_evaluation: str | None

class RoomAirSettingsUnderFloorAirDistributionInterior(IDFObject):
    number_of_diffusers: float | str | None
    power_per_plume: float | str | None
    design_effective_area_of_diffuser: float | str | None
    diffuser_slot_angle_from_vertical: float | str | None
    thermostat_height: float | None
    comfort_height: float | None
    temperature_difference_threshold_for_reporting: float | None
    floor_diffuser_type: str | None
    transition_height: float | str | None
    coefficient_a: float | str | None
    coefficient_b: float | str | None
    coefficient_c: float | str | None
    coefficient_d: float | str | None
    coefficient_e: float | str | None

class RoomAirSettingsUnderFloorAirDistributionExterior(IDFObject):
    number_of_diffusers_per_zone: float | str | None
    power_per_plume: float | str | None
    design_effective_area_of_diffuser: float | str | None
    diffuser_slot_angle_from_vertical: float | str | None
    thermostat_height: float | None
    comfort_height: float | None
    temperature_difference_threshold_for_reporting: float | None
    floor_diffuser_type: str | None
    transition_height: float | str | None
    coefficient_a_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float | str | None
    coefficient_b_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float | str | None
    coefficient_c_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float | str | None
    coefficient_d_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float | str | None
    coefficient_e_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float | str | None

class RoomAirNodeAirflowNetwork(IDFObject):
    zone_name: str | None
    fraction_of_zone_air_volume: float | None
    roomair_node_airflownetwork_adjacentsurfacelist_name: str | None
    roomair_node_airflownetwork_internalgains_name: str | None
    roomair_node_airflownetwork_hvacequipment_name: str | None

class RoomAirNodeAirflowNetworkAdjacentSurfaceList(IDFObject):
    surface_name: str | None

class RoomAirNodeAirflowNetworkInternalGains(IDFObject):
    internal_gain_object_type: str | None
    internal_gain_object_name: str | None
    fraction_of_gains_to_node: float | None

class RoomAirNodeAirflowNetworkHVACEquipment(IDFObject):
    zonehvac_or_air_terminal_equipment_object_type: str | None
    zonehvac_or_air_terminal_equipment_object_name: str | None
    fraction_of_output_or_supply_air_from_hvac_equipment: float | None
    fraction_of_input_or_return_air_to_hvac_equipment: float | None

class RoomAirSettingsAirflowNetwork(IDFObject):
    zone_name: str | None
    control_point_roomairflownetwork_node_name: str | None
    roomairflownetwork_node_name: str | None

class People(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    number_of_people_schedule_name: str | None
    number_of_people_calculation_method: str | None
    number_of_people: float | None
    people_per_floor_area: float | None
    floor_area_per_person: float | None
    fraction_radiant: float | None
    sensible_heat_fraction: float | str | None
    activity_level_schedule_name: str | None
    carbon_dioxide_generation_rate: float | None
    enable_ashrae_55_comfort_warnings: str | None
    mean_radiant_temperature_calculation_type: str | None
    surface_name_angle_factor_list_name: str | None
    work_efficiency_schedule_name: str | None
    clothing_insulation_calculation_method: str | None
    clothing_insulation_calculation_method_schedule_name: str | None
    clothing_insulation_schedule_name: str | None
    air_velocity_schedule_name: str | None
    thermal_comfort_model_1_type: str | None
    thermal_comfort_model_2_type: str | None
    thermal_comfort_model_3_type: str | None
    thermal_comfort_model_4_type: str | None
    thermal_comfort_model_5_type: str | None
    thermal_comfort_model_6_type: str | None
    thermal_comfort_model_7_type: str | None
    ankle_level_air_velocity_schedule_name: str | None
    cold_stress_temperature_threshold: float | None
    heat_stress_temperature_threshold: float | None

class ComfortViewFactorAngles(IDFObject):
    surface_name: str | None
    angle_factor: float | None

class Lights(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    design_level_calculation_method: str | None
    lighting_level: float | None
    watts_per_floor_area: float | None
    watts_per_person: float | None
    return_air_fraction: float | None
    fraction_radiant: float | None
    fraction_visible: float | None
    fraction_replaceable: float | None
    end_use_subcategory: str | None
    return_air_fraction_calculated_from_plenum_temperature: str | None
    return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None
    return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None
    return_air_heat_gain_node_name: str | None
    exhaust_air_heat_gain_node_name: str | None

class ElectricEquipment(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    design_level_calculation_method: str | None
    design_level: float | None
    watts_per_floor_area: float | None
    watts_per_person: float | None
    fraction_latent: float | None
    fraction_radiant: float | None
    fraction_lost: float | None
    end_use_subcategory: str | None

class GasEquipment(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    design_level_calculation_method: str | None
    design_level: float | None
    power_per_floor_area: float | None
    power_per_person: float | None
    fraction_latent: float | None
    fraction_radiant: float | None
    fraction_lost: float | None
    carbon_dioxide_generation_rate: float | None
    end_use_subcategory: str | None

class HotWaterEquipment(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    design_level_calculation_method: str | None
    design_level: float | None
    power_per_floor_area: float | None
    power_per_person: float | None
    fraction_latent: float | None
    fraction_radiant: float | None
    fraction_lost: float | None
    end_use_subcategory: str | None

class SteamEquipment(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    design_level_calculation_method: str | None
    design_level: float | None
    power_per_floor_area: float | None
    power_per_person: float | None
    fraction_latent: float | None
    fraction_radiant: float | None
    fraction_lost: float | None
    end_use_subcategory: str | None

class OtherEquipment(IDFObject):
    fuel_type: str | None
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    design_level_calculation_method: str | None
    design_level: float | None
    power_per_floor_area: float | None
    power_per_person: float | None
    fraction_latent: float | None
    fraction_radiant: float | None
    fraction_lost: float | None
    carbon_dioxide_generation_rate: float | None
    end_use_subcategory: str | None

class IndoorLivingWall(IDFObject):
    surface_name: str | None
    schedule_name: str | None
    evapotranspiration_calculation_method: str | None
    lighting_method: str | None
    led_intensity_schedule_name: str | None
    daylighting_control_name: str | None
    led_daylight_targeted_lighting_intensity_schedule_name: str | None
    total_leaf_area: float | None
    led_nominal_intensity: float | None
    led_nominal_power: float | None
    radiant_fraction_of_led_lights: float | None

class ElectricEquipmentITEAirCooled(IDFObject):
    zone_or_space_name: str | None
    air_flow_calculation_method: str | None
    design_power_input_calculation_method: str | None
    watts_per_unit: float | None
    number_of_units: float | None
    watts_per_floor_area: float | None
    design_power_input_schedule_name: str | None
    cpu_loading_schedule_name: str | None
    cpu_power_input_function_of_loading_and_air_temperature_curve_name: str | None
    design_fan_power_input_fraction: float | None
    design_fan_air_flow_rate_per_power_input: float | None
    air_flow_function_of_loading_and_air_temperature_curve_name: str | None
    fan_power_input_function_of_flow_curve_name: str | None
    design_entering_air_temperature: float | None
    environmental_class: str | None
    air_inlet_connection_type: str | None
    air_inlet_room_air_model_node_name: str | None
    air_outlet_room_air_model_node_name: str | None
    supply_air_node_name: str | None
    design_recirculation_fraction: float | None
    recirculation_function_of_loading_and_supply_temperature_curve_name: str | None
    design_electric_power_supply_efficiency: float | None
    electric_power_supply_efficiency_function_of_part_load_ratio_curve_name: str | None
    fraction_of_electric_power_supply_losses_to_zone: float | None
    cpu_end_use_subcategory: str | None
    fan_end_use_subcategory: str | None
    electric_power_supply_end_use_subcategory: str | None
    supply_temperature_difference: float | None
    supply_temperature_difference_schedule: str | None
    return_temperature_difference: float | None
    return_temperature_difference_schedule: str | None

class ZoneBaseboardOutdoorTemperatureControlled(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    capacity_at_low_temperature: float | None
    low_temperature: float | None
    capacity_at_high_temperature: float | None
    high_temperature: float | None
    fraction_radiant: float | None
    end_use_subcategory: str | None

class SwimmingPoolIndoor(IDFObject):
    surface_name: str | None
    average_depth: float | None
    activity_factor_schedule_name: str | None
    make_up_water_supply_schedule_name: str | None
    cover_schedule_name: str | None
    cover_evaporation_factor: float | None
    cover_convection_factor: float | None
    cover_short_wavelength_radiation_factor: float | None
    cover_long_wavelength_radiation_factor: float | None
    pool_water_inlet_node: str | None
    pool_water_outlet_node: str | None
    pool_heating_system_maximum_water_flow_rate: float | None
    pool_miscellaneous_equipment_power: float | None
    setpoint_temperature_schedule: str | None
    maximum_number_of_people: float | None
    people_schedule: str | None
    people_heat_gain_schedule: str | None

class ZoneContaminantSourceAndSinkCarbonDioxide(IDFObject):
    zone_name: str | None
    design_generation_rate: float | None
    schedule_name: str | None

class ZoneContaminantSourceAndSinkGenericConstant(IDFObject):
    zone_name: str | None
    design_generation_rate: float | None
    generation_schedule_name: str | None
    design_removal_coefficient: float | None
    removal_schedule_name: str | None

class SurfaceContaminantSourceAndSinkGenericPressureDriven(IDFObject):
    surface_name: str | None
    design_generation_rate_coefficient: float | None
    generation_schedule_name: str | None
    generation_exponent: float | None

class ZoneContaminantSourceAndSinkGenericCutoffModel(IDFObject):
    zone_name: str | None
    design_generation_rate_coefficient: float | None
    schedule_name: str | None
    cutoff_generic_contaminant_at_which_emission_ceases: float | None

class ZoneContaminantSourceAndSinkGenericDecaySource(IDFObject):
    zone_name: str | None
    initial_emission_rate: float | None
    schedule_name: str | None
    delay_time_constant: float | None

class SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion(IDFObject):
    surface_name: str | None
    mass_transfer_coefficient: float | None
    schedule_name: str | None
    henry_adsorption_constant_or_partition_coefficient: float | None

class SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink(IDFObject):
    surface_name: str | None
    deposition_velocity: float | None
    schedule_name: str | None

class ZoneContaminantSourceAndSinkGenericDepositionRateSink(IDFObject):
    zone_name: str | None
    deposition_rate: float | None
    schedule_name: str | None

class DaylightingControls(IDFObject):
    zone_or_space_name: str | None
    daylighting_method: str | None
    availability_schedule_name: str | None
    lighting_control_type: str | None
    minimum_input_power_fraction_for_continuous_or_continuousoff_dimming_control: float | None
    minimum_light_output_fraction_for_continuous_or_continuousoff_dimming_control: float | None
    number_of_stepped_control_steps: int | None
    probability_lighting_will_be_reset_when_needed_in_manual_stepped_control: float | None
    glare_calculation_daylighting_reference_point_name: str | None
    glare_calculation_azimuth_angle_of_view_direction_clockwise_from_zone_y_axis: float | None
    maximum_allowable_discomfort_glare_index: float | None
    delight_gridding_resolution: float | None
    daylighting_reference_point_name: str | None
    fraction_of_lights_controlled_by_reference_point: float | None
    illuminance_setpoint_at_reference_point: float | None

class DaylightingReferencePoint(IDFObject):
    zone_or_space_name: str | None
    x_coordinate_of_reference_point: float | None
    y_coordinate_of_reference_point: float | None
    z_coordinate_of_reference_point: float | None

class DaylightingDELightComplexFenestration(IDFObject):
    complex_fenestration_type: str | None
    building_surface_name: str | None
    window_name: str | None
    fenestration_rotation: float | None

class DaylightingDeviceTubular(IDFObject):
    dome_name: str | None
    diffuser_name: str | None
    construction_name: str | None
    diameter: float | None
    total_length: float | None
    effective_thermal_resistance: float | None
    transition_zone_name: str | None
    transition_zone_length: float | None

class DaylightingDeviceShelf(IDFObject):
    window_name: str | None
    inside_shelf_name: str | None
    outside_shelf_name: str | None
    outside_shelf_construction_name: str | None
    view_factor_to_outside_shelf: float | None

class DaylightingDeviceLightWell(IDFObject):
    height_of_well: float | None
    perimeter_of_bottom_of_well: float | None
    area_of_bottom_of_well: float | None
    visible_reflectance_of_well_walls: float | None

class OutputDaylightFactors(IDFObject): ...

class OutputIlluminanceMap(IDFObject):
    zone_or_space_name: str | None
    z_height: float | None
    x_minimum_coordinate: float | None
    x_maximum_coordinate: float | None
    number_of_x_grid_points: int | None
    y_minimum_coordinate: float | None
    y_maximum_coordinate: float | None
    number_of_y_grid_points: int | None

class OutputControlIlluminanceMapStyle(IDFObject): ...

class ZoneInfiltrationDesignFlowRate(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    design_flow_rate_calculation_method: str | None
    design_flow_rate: float | None
    flow_rate_per_floor_area: float | None
    flow_rate_per_exterior_surface_area: float | None
    air_changes_per_hour: float | None
    constant_term_coefficient: float | None
    temperature_term_coefficient: float | None
    velocity_term_coefficient: float | None
    velocity_squared_term_coefficient: float | None
    density_basis: str | None

class ZoneInfiltrationEffectiveLeakageArea(IDFObject):
    zone_or_space_name: str | None
    schedule_name: str | None
    effective_air_leakage_area: float | None
    stack_coefficient: float | None
    wind_coefficient: float | None

class ZoneInfiltrationFlowCoefficient(IDFObject):
    zone_or_space_name: str | None
    schedule_name: str | None
    flow_coefficient: float | None
    stack_coefficient: float | None
    pressure_exponent: float | None
    wind_coefficient: float | None
    shelter_factor: float | None

class ZoneVentilationDesignFlowRate(IDFObject):
    zone_or_zonelist_or_space_or_spacelist_name: str | None
    schedule_name: str | None
    design_flow_rate_calculation_method: str | None
    design_flow_rate: float | None
    flow_rate_per_floor_area: float | None
    flow_rate_per_person: float | None
    air_changes_per_hour: float | None
    ventilation_type: str | None
    fan_pressure_rise: float | None
    fan_total_efficiency: float | None
    constant_term_coefficient: float | None
    temperature_term_coefficient: float | None
    velocity_term_coefficient: float | None
    velocity_squared_term_coefficient: float | None
    minimum_indoor_temperature: float | None
    minimum_indoor_temperature_schedule_name: str | None
    maximum_indoor_temperature: float | None
    maximum_indoor_temperature_schedule_name: str | None
    delta_temperature: float | None
    delta_temperature_schedule_name: str | None
    minimum_outdoor_temperature: float | None
    minimum_outdoor_temperature_schedule_name: str | None
    maximum_outdoor_temperature: float | None
    maximum_outdoor_temperature_schedule_name: str | None
    maximum_wind_speed: float | None
    density_basis: str | None

class ZoneVentilationWindandStackOpenArea(IDFObject):
    zone_or_space_name: str | None
    opening_area: float | None
    opening_area_fraction_schedule_name: str | None
    opening_effectiveness: float | str | None
    effective_angle: float | None
    height_difference: float | None
    discharge_coefficient_for_opening: float | str | None
    minimum_indoor_temperature: float | None
    minimum_indoor_temperature_schedule_name: str | None
    maximum_indoor_temperature: float | None
    maximum_indoor_temperature_schedule_name: str | None
    delta_temperature: float | None
    delta_temperature_schedule_name: str | None
    minimum_outdoor_temperature: float | None
    minimum_outdoor_temperature_schedule_name: str | None
    maximum_outdoor_temperature: float | None
    maximum_outdoor_temperature_schedule_name: str | None
    maximum_wind_speed: float | None

class ZoneAirBalanceOutdoorAir(IDFObject):
    zone_name: str | None
    air_balance_method: str | None
    induced_outdoor_air_due_to_unbalanced_duct_leakage: float | None
    induced_outdoor_air_schedule_name: str | None

class ZoneMixing(IDFObject):
    zone_or_space_name: str | None
    schedule_name: str | None
    design_flow_rate_calculation_method: str | None
    design_flow_rate: float | None
    flow_rate_per_floor_area: float | None
    flow_rate_per_person: float | None
    air_changes_per_hour: float | None
    source_zone_or_space_name: str | None
    delta_temperature: float | None
    delta_temperature_schedule_name: str | None
    minimum_receiving_temperature_schedule_name: str | None
    maximum_receiving_temperature_schedule_name: str | None
    minimum_source_temperature_schedule_name: str | None
    maximum_source_temperature_schedule_name: str | None
    minimum_outdoor_temperature_schedule_name: str | None
    maximum_outdoor_temperature_schedule_name: str | None

class ZoneCrossMixing(IDFObject):
    zone_or_space_name: str | None
    schedule_name: str | None
    design_flow_rate_calculation_method: str | None
    design_flow_rate: float | None
    flow_rate_per_floor_area: float | None
    flow_rate_per_person: float | None
    air_changes_per_hour: float | None
    source_zone_or_space_name: str | None
    delta_temperature: float | None
    delta_temperature_schedule_name: str | None
    minimum_receiving_temperature_schedule_name: str | None
    maximum_receiving_temperature_schedule_name: str | None
    minimum_source_temperature_schedule_name: str | None
    maximum_source_temperature_schedule_name: str | None
    minimum_outdoor_temperature_schedule_name: str | None
    maximum_outdoor_temperature_schedule_name: str | None

class ZoneRefrigerationDoorMixing(IDFObject):
    zone_or_space_name_1: str | None
    zone_or_space_name_2: str | None
    schedule_name: str | None
    door_height: float | None
    door_area: float | None
    door_protection_type: str | None

class ZoneEarthtube(IDFObject):
    schedule_name: str | None
    design_flow_rate: float | None
    minimum_zone_temperature_when_cooling: float | None
    maximum_zone_temperature_when_heating: float | None
    delta_temperature: float | None
    earthtube_type: str | None
    fan_pressure_rise: float | None
    fan_total_efficiency: float | None
    pipe_radius: float | None
    pipe_thickness: float | None
    pipe_length: float | None
    pipe_thermal_conductivity: float | None
    pipe_depth_under_ground_surface: float | None
    soil_condition: str | None
    average_soil_surface_temperature: float | None
    amplitude_of_soil_surface_temperature: float | None
    phase_constant_of_soil_surface_temperature: float | None
    constant_term_flow_coefficient: float | None
    temperature_term_flow_coefficient: float | None
    velocity_term_flow_coefficient: float | None
    velocity_squared_term_flow_coefficient: float | None
    earth_tube_model_type: str | None
    earth_tube_model_parameters: str | None

class ZoneEarthtubeParameters(IDFObject):
    nodes_above_earth_tube: int | None
    nodes_below_earth_tube: int | None
    earth_tube_dimensionless_boundary_above: float | None
    earth_tube_dimensionless_boundary_below: float | None
    earth_tube_solution_space_width: float | None

class ZoneCoolTowerShower(IDFObject):
    availability_schedule_name: str | None
    zone_or_space_name: str | None
    water_supply_storage_tank_name: str | None
    flow_control_type: str | None
    pump_flow_rate_schedule_name: str | None
    maximum_water_flow_rate: float | None
    effective_tower_height: float | None
    airflow_outlet_area: float | None
    maximum_air_flow_rate: float | None
    minimum_indoor_temperature: float | None
    fraction_of_water_loss: float | None
    fraction_of_flow_schedule: float | None
    rated_power_consumption: float | None

class ZoneThermalChimney(IDFObject):
    zone_name: str | None
    availability_schedule_name: str | None
    width_of_the_absorber_wall: float | None
    cross_sectional_area_of_air_channel_outlet: float | None
    discharge_coefficient: float | None
    zone_or_space_name_1: str | None
    distance_from_top_of_thermal_chimney_to_inlet_1: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_1: float | None
    cross_sectional_areas_of_air_channel_inlet_1: float | None
    zone_or_space_name_2: str | None
    distance_from_top_of_thermal_chimney_to_inlet_2: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_2: float | None
    cross_sectional_areas_of_air_channel_inlet_2: float | None
    zone_or_space_name_3: str | None
    distance_from_top_of_thermal_chimney_to_inlet_3: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_3: float | None
    cross_sectional_areas_of_air_channel_inlet_3: float | None
    zone_or_space_name_4: str | None
    distance_from_top_of_thermal_chimney_to_inlet_4: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_4: float | None
    cross_sectional_areas_of_air_channel_inlet_4: float | None
    zone_or_space_name_5: str | None
    distance_from_top_of_thermal_chimney_to_inlet_5: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_5: float | None
    cross_sectional_areas_of_air_channel_inlet_5: float | None
    zone_or_space_name_6: str | None
    distance_from_top_of_thermal_chimney_to_inlet_6: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_6: float | None
    cross_sectional_areas_of_air_channel_inlet_6: float | None
    zone_or_space_name_7: str | None
    distance_from_top_of_thermal_chimney_to_inlet_7: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_7: float | None
    cross_sectional_areas_of_air_channel_inlet_7: float | None
    zone_or_space_name_8: str | None
    distance_from_top_of_thermal_chimney_to_inlet_8: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_8: float | None
    cross_sectional_areas_of_air_channel_inlet_8: float | None
    zone_or_space_name_9: str | None
    distance_from_top_of_thermal_chimney_to_inlet_9: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_9: float | None
    cross_sectional_areas_of_air_channel_inlet_9: float | None
    zone_or_space_name_10: str | None
    distance_from_top_of_thermal_chimney_to_inlet_10: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_10: float | None
    cross_sectional_areas_of_air_channel_inlet_10: float | None
    zone_or_space_name_11: str | None
    distance_from_top_of_thermal_chimney_to_inlet_11: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_11: float | None
    cross_sectional_areas_of_air_channel_inlet_11: float | None
    zone_or_space_name_12: str | None
    distance_from_top_of_thermal_chimney_to_inlet_12: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_12: float | None
    cross_sectional_areas_of_air_channel_inlet_12: float | None
    zone_or_space_name_13: str | None
    distance_from_top_of_thermal_chimney_to_inlet_13: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_13: float | None
    cross_sectional_areas_of_air_channel_inlet_13: float | None
    zone_or_space_name_14: str | None
    distance_from_top_of_thermal_chimney_to_inlet_14: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_14: float | None
    cross_sectional_areas_of_air_channel_inlet_14: float | None
    zone_or_space_name_15: str | None
    distance_from_top_of_thermal_chimney_to_inlet_15: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_15: float | None
    cross_sectional_areas_of_air_channel_inlet_15: float | None
    zone_or_space_name_16: str | None
    distance_from_top_of_thermal_chimney_to_inlet_16: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_16: float | None
    cross_sectional_areas_of_air_channel_inlet_16: float | None
    zone_or_space_name_17: str | None
    distance_from_top_of_thermal_chimney_to_inlet_17: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_17: float | None
    cross_sectional_areas_of_air_channel_inlet_17: float | None
    zone_or_space_name_18: str | None
    distance_from_top_of_thermal_chimney_to_inlet_18: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_18: float | None
    cross_sectional_areas_of_air_channel_inlet_18: float | None
    zone_or_space_name_19: str | None
    distance_from_top_of_thermal_chimney_to_inlet_19: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_19: float | None
    cross_sectional_areas_of_air_channel_inlet_19: float | None
    zone_or_space_name_20: str | None
    distance_from_top_of_thermal_chimney_to_inlet_20: float | None
    relative_ratios_of_air_flow_rates_passing_through_inlet_20: float | None
    cross_sectional_areas_of_air_channel_inlet_20: float | None

class AirflowNetworkSimulationControl(IDFObject):
    airflownetwork_control: str | None
    wind_pressure_coefficient_type: str | None
    height_selection_for_local_wind_pressure_calculation: str | None
    building_type: str | None
    maximum_number_of_iterations: int | None
    initialization_type: str | None
    relative_airflow_convergence_tolerance: float | None
    absolute_airflow_convergence_tolerance: float | None
    convergence_acceleration_limit: float | None
    azimuth_angle_of_long_axis_of_building: float | None
    ratio_of_building_width_along_short_axis_to_width_along_long_axis: float | None
    height_dependence_of_external_node_temperature: str | None
    solver: str | None
    allow_unsupported_zone_equipment: str | None
    do_distribution_duct_sizing_calculation: str | None

class AirflowNetworkMultiZoneZone(IDFObject):
    ventilation_control_mode: str | None
    ventilation_control_zone_temperature_setpoint_schedule_name: str | None
    minimum_venting_open_factor: float | None
    indoor_and_outdoor_temperature_difference_lower_limit_for_maximum_venting_open_factor: float | None
    indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor: float | None
    indoor_and_outdoor_enthalpy_difference_lower_limit_for_maximum_venting_open_factor: float | None
    indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor: float | None
    venting_availability_schedule_name: str | None
    single_sided_wind_pressure_coefficient_algorithm: str | None
    facade_width: float | None
    occupant_ventilation_control_name: str | None

class AirflowNetworkMultiZoneSurface(IDFObject):
    leakage_component_name: str | None
    external_node_name: str | None
    window_door_opening_factor_or_crack_factor: float | None
    ventilation_control_mode: str | None
    ventilation_control_zone_temperature_setpoint_schedule_name: str | None
    minimum_venting_open_factor: float | None
    indoor_and_outdoor_temperature_difference_lower_limit_for_maximum_venting_open_factor: float | None
    indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor: float | None
    indoor_and_outdoor_enthalpy_difference_lower_limit_for_maximum_venting_open_factor: float | None
    indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor: float | None
    venting_availability_schedule_name: str | None
    occupant_ventilation_control_name: str | None
    equivalent_rectangle_method: str | None
    equivalent_rectangle_aspect_ratio: float | None

class AirflowNetworkMultiZoneReferenceCrackConditions(IDFObject):
    reference_temperature: float | None
    reference_barometric_pressure: float | None
    reference_humidity_ratio: float | None

class AirflowNetworkMultiZoneSurfaceCrack(IDFObject):
    air_mass_flow_coefficient_at_reference_conditions: float | None
    air_mass_flow_exponent: float | None
    reference_crack_conditions: str | None

class AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea(IDFObject):
    effective_leakage_area: float | None
    discharge_coefficient: float | None
    reference_pressure_difference: float | None
    air_mass_flow_exponent: float | None

class AirflowNetworkMultiZoneSpecifiedFlowRate(IDFObject):
    air_flow_value: float | None
    air_flow_units: str | None

class AirflowNetworkMultiZoneComponentDetailedOpening(IDFObject):
    air_mass_flow_coefficient_when_opening_is_closed: float | None
    air_mass_flow_exponent_when_opening_is_closed: float | None
    type_of_rectangular_large_vertical_opening_lvo_: str | None
    extra_crack_length_or_height_of_pivoting_axis: float | None
    number_of_sets_of_opening_factor_data: int | None
    opening_factor_1: float | None
    discharge_coefficient_for_opening_factor_1: float | None
    width_factor_for_opening_factor_1: float | None
    height_factor_for_opening_factor_1: float | None
    start_height_factor_for_opening_factor_1: float | None
    opening_factor_2: float | None
    discharge_coefficient_for_opening_factor_2: float | None
    width_factor_for_opening_factor_2: float | None
    height_factor_for_opening_factor_2: float | None
    start_height_factor_for_opening_factor_2: float | None
    opening_factor_3: float | None
    discharge_coefficient_for_opening_factor_3: float | None
    width_factor_for_opening_factor_3: float | None
    height_factor_for_opening_factor_3: float | None
    start_height_factor_for_opening_factor_3: float | None
    opening_factor_4: float | None
    discharge_coefficient_for_opening_factor_4: float | None
    width_factor_for_opening_factor_4: float | None
    height_factor_for_opening_factor_4: float | None
    start_height_factor_for_opening_factor_4: float | None

class AirflowNetworkMultiZoneComponentSimpleOpening(IDFObject):
    air_mass_flow_coefficient_when_opening_is_closed: float | None
    air_mass_flow_exponent_when_opening_is_closed: float | None
    minimum_density_difference_for_two_way_flow: float | None
    discharge_coefficient: float | None

class AirflowNetworkMultiZoneComponentHorizontalOpening(IDFObject):
    air_mass_flow_coefficient_when_opening_is_closed: float | None
    air_mass_flow_exponent_when_opening_is_closed: float | None
    sloping_plane_angle: float | None
    discharge_coefficient: float | None

class AirflowNetworkMultiZoneComponentZoneExhaustFan(IDFObject):
    air_mass_flow_coefficient_when_the_zone_exhaust_fan_is_off_at_reference_conditions: float | None
    air_mass_flow_exponent_when_the_zone_exhaust_fan_is_off: float | None
    reference_crack_conditions: str | None

class AirflowNetworkMultiZoneExternalNode(IDFObject):
    external_node_height: float | None
    wind_pressure_coefficient_curve_name: str | None
    symmetric_wind_pressure_coefficient_curve: str | None
    wind_angle_type: str | None

class AirflowNetworkMultiZoneWindPressureCoefficientArray(IDFObject):
    wind_direction_1: float | None
    wind_direction_2: float | None
    wind_direction_3: float | None
    wind_direction_4: float | None
    wind_direction_5: float | None
    wind_direction_6: float | None
    wind_direction_7: float | None
    wind_direction_8: float | None
    wind_direction_9: float | None
    wind_direction_10: float | None
    wind_direction_11: float | None
    wind_direction_12: float | None
    wind_direction_13: float | None
    wind_direction_14: float | None
    wind_direction_15: float | None
    wind_direction_16: float | None
    wind_direction_17: float | None
    wind_direction_18: float | None
    wind_direction_19: float | None
    wind_direction_20: float | None
    wind_direction_21: float | None
    wind_direction_22: float | None
    wind_direction_23: float | None
    wind_direction_24: float | None
    wind_direction_25: float | None
    wind_direction_26: float | None
    wind_direction_27: float | None
    wind_direction_28: float | None
    wind_direction_29: float | None
    wind_direction_30: float | None
    wind_direction_31: float | None
    wind_direction_32: float | None
    wind_direction_33: float | None
    wind_direction_34: float | None
    wind_direction_35: float | None
    wind_direction_36: float | None

class AirflowNetworkMultiZoneWindPressureCoefficientValues(IDFObject):
    airflownetwork_multizone_windpressurecoefficientarray_name: str | None
    wind_pressure_coefficient_value_1: float | None
    wind_pressure_coefficient_value_2: float | None
    wind_pressure_coefficient_value_3: float | None
    wind_pressure_coefficient_value_4: float | None
    wind_pressure_coefficient_value_5: float | None
    wind_pressure_coefficient_value_6: float | None
    wind_pressure_coefficient_value_7: float | None
    wind_pressure_coefficient_value_8: float | None
    wind_pressure_coefficient_value_9: float | None
    wind_pressure_coefficient_value_10: float | None
    wind_pressure_coefficient_value_11: float | None
    wind_pressure_coefficient_value_12: float | None
    wind_pressure_coefficient_value_13: float | None
    wind_pressure_coefficient_value_14: float | None
    wind_pressure_coefficient_value_15: float | None
    wind_pressure_coefficient_value_16: float | None
    wind_pressure_coefficient_value_17: float | None
    wind_pressure_coefficient_value_18: float | None
    wind_pressure_coefficient_value_19: float | None
    wind_pressure_coefficient_value_20: float | None
    wind_pressure_coefficient_value_21: float | None
    wind_pressure_coefficient_value_22: float | None
    wind_pressure_coefficient_value_23: float | None
    wind_pressure_coefficient_value_24: float | None
    wind_pressure_coefficient_value_25: float | None
    wind_pressure_coefficient_value_26: float | None
    wind_pressure_coefficient_value_27: float | None
    wind_pressure_coefficient_value_28: float | None
    wind_pressure_coefficient_value_29: float | None
    wind_pressure_coefficient_value_30: float | None
    wind_pressure_coefficient_value_31: float | None
    wind_pressure_coefficient_value_32: float | None
    wind_pressure_coefficient_value_33: float | None
    wind_pressure_coefficient_value_34: float | None
    wind_pressure_coefficient_value_35: float | None
    wind_pressure_coefficient_value_36: float | None

class AirflowNetworkZoneControlPressureController(IDFObject):
    control_zone_name: str | None
    control_object_type: str | None
    control_object_name: str | None
    pressure_control_availability_schedule_name: str | None
    pressure_setpoint_schedule_name: str | None

class AirflowNetworkDistributionNode(IDFObject):
    component_name_or_node_name: str | None
    component_object_type_or_node_type: str | None
    node_height: float | None

class AirflowNetworkDistributionComponentLeak(IDFObject):
    air_mass_flow_coefficient: float | None
    air_mass_flow_exponent: float | None

class AirflowNetworkDistributionComponentLeakageRatio(IDFObject):
    effective_leakage_ratio: float | None
    maximum_flow_rate: float | None
    reference_pressure_difference: float | None
    air_mass_flow_exponent: float | None

class AirflowNetworkDistributionComponentDuct(IDFObject):
    duct_length: float | None
    hydraulic_diameter: float | None
    cross_section_area: float | None
    surface_roughness: float | None
    coefficient_for_local_dynamic_loss_due_to_fitting: float | None
    heat_transmittance_coefficient_u_factor_for_duct_wall_construction: float | None
    overall_moisture_transmittance_coefficient_from_air_to_air: float | None
    outside_convection_coefficient: float | None
    inside_convection_coefficient: float | None

class AirflowNetworkDistributionComponentFan(IDFObject):
    supply_fan_object_type: str | None

class AirflowNetworkDistributionComponentCoil(IDFObject):
    coil_object_type: str | None
    air_path_length: float | None
    air_path_hydraulic_diameter: float | None

class AirflowNetworkDistributionComponentHeatExchanger(IDFObject):
    heatexchanger_object_type: str | None
    air_path_length: float | None
    air_path_hydraulic_diameter: float | None

class AirflowNetworkDistributionComponentTerminalUnit(IDFObject):
    terminal_unit_object_type: str | None
    air_path_length: float | None
    air_path_hydraulic_diameter: float | None

class AirflowNetworkDistributionComponentConstantPressureDrop(IDFObject):
    pressure_difference_across_the_component: float | None

class AirflowNetworkDistributionComponentOutdoorAirFlow(IDFObject):
    outdoor_air_mixer_name: str | None
    air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float | None
    air_mass_flow_exponent_when_no_outdoor_air_flow: float | None
    reference_crack_conditions: str | None

class AirflowNetworkDistributionComponentReliefAirFlow(IDFObject):
    outdoor_air_mixer_name: str | None
    air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float | None
    air_mass_flow_exponent_when_no_outdoor_air_flow: float | None
    reference_crack_conditions: str | None

class AirflowNetworkDistributionLinkage(IDFObject):
    node_1_name: str | None
    node_2_name: str | None
    component_name: str | None
    thermal_zone_name: str | None

class AirflowNetworkDistributionDuctViewFactors(IDFObject):
    duct_surface_exposure_fraction: float | None
    duct_surface_emittance: float | None
    surface_name: str | None
    surface_view_factor: float | None

class AirflowNetworkDistributionDuctSizing(IDFObject):
    duct_sizing_method: str | None
    duct_sizing_factor: float | None
    maximum_airflow_velocity: float | None
    total_pressure_loss_across_supply_trunk: float | None
    total_pressure_loss_across_supply_branch: float | None
    total_pressure_loss_across_return_trunk: float | None
    total_pressure_loss_across_return_branch: float | None

class AirflowNetworkOccupantVentilationControl(IDFObject):
    minimum_opening_time: float | None
    minimum_closing_time: float | None
    thermal_comfort_low_temperature_curve_name: str | None
    thermal_comfort_temperature_boundary_point: float | None
    thermal_comfort_high_temperature_curve_name: str | None
    maximum_threshold_for_persons_dissatisfied_ppd: float | None
    occupancy_check: str | None
    opening_probability_schedule_name: str | None
    closing_probability_schedule_name: str | None

class AirflowNetworkIntraZoneNode(IDFObject):
    roomair_node_airflownetwork_name: str | None
    zone_name: str | None
    node_height: float | None

class AirflowNetworkIntraZoneLinkage(IDFObject):
    node_1_name: str | None
    node_2_name: str | None
    component_name: str | None
    airflownetwork_multizone_surface_name: str | None

class DuctLossConduction(IDFObject):
    airloophvac_name: str | None
    airflownetwork_distribution_linkage_name: str | None
    environment_type: str | None
    ambient_zone_name: str | None
    ambient_temperature_schedule_name: str | None
    ambient_humidity_ratio_schedule_name: str | None

class DuctLossLeakage(IDFObject):
    airloophvac_name: str | None
    airflownetwork_distribution_linkage_name: str | None

class DuctLossMakeupAir(IDFObject):
    airloophvac_name: str | None
    airflownetwork_distribution_linkage_name: str | None

class ExteriorLights(IDFObject):
    schedule_name: str | None
    design_level: float | None
    control_option: str | None
    end_use_subcategory: str | None

class ExteriorFuelEquipment(IDFObject):
    fuel_use_type: str | None
    schedule_name: str | None
    design_level: float | None
    end_use_subcategory: str | None

class ExteriorWaterEquipment(IDFObject):
    fuel_use_type: str | None
    schedule_name: str | None
    design_level: float | None
    end_use_subcategory: str | None

class HVACTemplateThermostat(IDFObject):
    heating_setpoint_schedule_name: str | None
    constant_heating_setpoint: float | None
    cooling_setpoint_schedule_name: str | None
    constant_cooling_setpoint: float | None

class HVACTemplateZoneIdealLoadsAirSystem(IDFObject):
    template_thermostat_name: str | None
    system_availability_schedule_name: str | None
    maximum_heating_supply_air_temperature: float | None
    minimum_cooling_supply_air_temperature: float | None
    maximum_heating_supply_air_humidity_ratio: float | None
    minimum_cooling_supply_air_humidity_ratio: float | None
    heating_limit: str | None
    maximum_heating_air_flow_rate: float | str | None
    maximum_sensible_heating_capacity: float | str | None
    cooling_limit: str | None
    maximum_cooling_air_flow_rate: float | str | None
    maximum_total_cooling_capacity: float | str | None
    heating_availability_schedule_name: str | None
    cooling_availability_schedule_name: str | None
    dehumidification_control_type: str | None
    cooling_sensible_heat_ratio: float | None
    dehumidification_setpoint: float | None
    humidification_control_type: str | None
    humidification_setpoint: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    design_specification_outdoor_air_object_name: str | None
    demand_controlled_ventilation_type: str | None
    outdoor_air_economizer_type: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None

class HVACTemplateZoneBaseboardHeat(IDFObject):
    template_thermostat_name: str | None
    zone_heating_sizing_factor: float | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    dedicated_outdoor_air_system_name: str | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None

class HVACTemplateZoneFanCoil(IDFObject):
    template_thermostat_name: str | None
    supply_air_maximum_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    system_availability_schedule_name: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    supply_fan_motor_in_air_stream_fraction: float | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_design_setpoint: float | None
    heating_coil_type: str | None
    heating_coil_availability_schedule_name: str | None
    heating_coil_design_setpoint: float | None
    dedicated_outdoor_air_system_name: str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature_difference: float | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None
    capacity_control_method: str | None
    low_speed_supply_air_flow_ratio: float | None
    medium_speed_supply_air_flow_ratio: float | None
    outdoor_air_schedule_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None

class HVACTemplateZonePTAC(IDFObject):
    template_thermostat_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    system_availability_schedule_name: str | None
    supply_fan_operating_mode_schedule_name: str | None
    supply_fan_placement: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_gross_rated_total_capacity: float | str | None
    cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    cooling_coil_gross_rated_cooling_cop: float | None
    heating_coil_type: str | None
    heating_coil_availability_schedule_name: str | None
    heating_coil_capacity: float | str | None
    gas_heating_coil_efficiency: float | None
    gas_heating_coil_parasitic_electric_load: float | None
    dedicated_outdoor_air_system_name: str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    capacity_control_method: str | None

class HVACTemplateZonePTHP(IDFObject):
    template_thermostat_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    system_availability_schedule_name: str | None
    supply_fan_operating_mode_schedule_name: str | None
    supply_fan_placement: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_gross_rated_total_capacity: float | str | None
    cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    cooling_coil_gross_rated_cop: float | None
    heat_pump_heating_coil_type: str | None
    heat_pump_heating_coil_availability_schedule_name: str | None
    heat_pump_heating_coil_gross_rated_capacity: float | str | None
    heat_pump_heating_coil_gross_rated_cop: float | None
    heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None
    heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None
    heat_pump_defrost_strategy: str | None
    heat_pump_defrost_control: str | None
    heat_pump_defrost_time_period_fraction: float | None
    supplemental_heating_coil_type: str | None
    supplemental_heating_coil_availability_schedule_name: str | None
    supplemental_heating_coil_capacity: float | str | None
    supplemental_heating_coil_maximum_outdoor_dry_bulb_temperature: float | None
    supplemental_gas_heating_coil_efficiency: float | None
    supplemental_gas_heating_coil_parasitic_electric_load: float | None
    dedicated_outdoor_air_system_name: str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    capacity_control_method: str | None

class HVACTemplateZoneWaterToAirHeatPump(IDFObject):
    template_thermostat_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    system_availability_schedule_name: str | None
    supply_fan_operating_mode_schedule_name: str | None
    supply_fan_placement: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    cooling_coil_type: str | None
    cooling_coil_gross_rated_total_capacity: float | str | None
    cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    cooling_coil_gross_rated_cop: float | None
    heat_pump_heating_coil_type: str | None
    heat_pump_heating_coil_gross_rated_capacity: float | str | None
    heat_pump_heating_coil_gross_rated_cop: float | None
    supplemental_heating_coil_availability_schedule_name: str | None
    supplemental_heating_coil_capacity: float | str | None
    maximum_cycling_rate: float | None
    latent_capacity_time_constant: float | None
    heat_pump_fan_delay_time: float | None
    dedicated_outdoor_air_system_name: str | None
    supplemental_heating_coil_type: str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None
    heat_pump_coil_water_flow_mode: str | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None

class HVACTemplateZoneVRF(IDFObject):
    template_vrf_system_name: str | None
    template_thermostat_name: str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    rated_total_heating_capacity_sizing_ratio: float | None
    cooling_supply_air_flow_rate: float | str | None
    no_cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_heating_supply_air_flow_rate: float | str | None
    cooling_outdoor_air_flow_rate: float | str | None
    heating_outdoor_air_flow_rate: float | str | None
    no_load_outdoor_air_flow_rate: float | str | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None
    system_availability_schedule_name: str | None
    supply_fan_operating_mode_schedule_name: str | None
    supply_air_fan_placement: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_gross_rated_total_capacity: float | str | None
    cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    heat_pump_heating_coil_type: str | None
    heat_pump_heating_coil_availability_schedule_name: str | None
    heat_pump_heating_coil_gross_rated_capacity: float | str | None
    zone_terminal_unit_on_parasitic_electric_energy_use: float | None
    zone_terminal_unit_off_parasitic_electric_energy_use: float | None
    dedicated_outdoor_air_system_name: str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None

class HVACTemplateZoneUnitary(IDFObject):
    template_unitary_system_name: str | None
    template_thermostat_name: str | None
    supply_air_maximum_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None

class HVACTemplateZoneVAV(IDFObject):
    template_vav_system_name: str | None
    template_thermostat_name: str | None
    supply_air_maximum_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    zone_minimum_air_flow_input_method: str | None
    constant_minimum_air_flow_fraction: float | None
    fixed_minimum_air_flow_rate: float | None
    minimum_air_flow_fraction_schedule_name: str | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    reheat_coil_type: str | None
    reheat_coil_availability_schedule_name: str | None
    damper_heating_action: str | None
    maximum_flow_per_zone_floor_area_during_reheat: float | str | None
    maximum_flow_fraction_during_reheat: float | str | None
    maximum_reheat_air_temperature: float | None
    design_specification_outdoor_air_object_name_for_control: str | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None
    design_specification_outdoor_air_object_name_for_sizing: str | None
    design_specification_zone_air_distribution_object_name: str | None

class HVACTemplateZoneVAVFanPowered(IDFObject):
    template_vav_system_name: str | None
    template_thermostat_name: str | None
    primary_supply_air_maximum_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    primary_supply_air_minimum_flow_fraction: float | str | None
    secondary_supply_air_maximum_flow_rate: float | str | None
    flow_type: str | None
    parallel_fan_on_flow_fraction: float | str | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    reheat_coil_type: str | None
    reheat_coil_availability_schedule_name: str | None
    fan_total_efficiency: float | None
    fan_delta_pressure: float | None
    fan_motor_efficiency: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None
    zone_piu_fan_schedule_name: str | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None

class HVACTemplateZoneVAVHeatAndCool(IDFObject):
    template_vav_system_name: str | None
    template_thermostat_name: str | None
    supply_air_maximum_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    constant_minimum_air_flow_fraction: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    design_specification_outdoor_air_object_name_for_sizing: str | None
    design_specification_zone_air_distribution_object_name: str | None
    reheat_coil_type: str | None
    reheat_coil_availability_schedule_name: str | None
    maximum_reheat_air_temperature: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None

class HVACTemplateZoneConstantVolume(IDFObject):
    template_constant_volume_system_name: str | None
    template_thermostat_name: str | None
    supply_air_maximum_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None
    reheat_coil_type: str | None
    reheat_coil_availability_schedule_name: str | None
    maximum_reheat_air_temperature: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None

class HVACTemplateZoneDualDuct(IDFObject):
    template_dual_duct_system_name: str | None
    template_thermostat_name: str | None
    supply_air_maximum_flow_rate: float | str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    zone_minimum_air_flow_fraction: float | None
    outdoor_air_method: str | None
    outdoor_air_flow_rate_per_person: float | None
    outdoor_air_flow_rate_per_zone_floor_area: float | None
    outdoor_air_flow_rate_per_zone: float | None
    design_specification_outdoor_air_object_name_for_sizing: str | None
    design_specification_zone_air_distribution_object_name: str | None
    design_specification_outdoor_air_object_name_for_control: str | None
    cold_supply_plenum_name: str | None
    hot_supply_plenum_name: str | None
    return_plenum_name: str | None
    baseboard_heating_type: str | None
    baseboard_heating_availability_schedule_name: str | None
    baseboard_heating_capacity: float | str | None
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None

class HVACTemplateSystemVRF(IDFObject):
    system_availability_schedule_name: str | None
    gross_rated_total_cooling_capacity: float | str | None
    gross_rated_cooling_cop: float | None
    minimum_outdoor_temperature_in_cooling_mode: float | None
    maximum_outdoor_temperature_in_cooling_mode: float | None
    gross_rated_heating_capacity: float | str | None
    rated_heating_capacity_sizing_ratio: float | None
    gross_rated_heating_cop: float | None
    minimum_outdoor_temperature_in_heating_mode: float | None
    maximum_outdoor_temperature_in_heating_mode: float | None
    minimum_heat_pump_part_load_ratio: float | None
    zone_name_for_master_thermostat_location: str | None
    master_thermostat_priority_control_type: str | None
    thermostat_priority_schedule_name: str | None
    heat_pump_waste_heat_recovery: str | None
    equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None
    vertical_height_used_for_piping_correction_factor: float | None
    equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None
    crankcase_heater_power_per_compressor: float | None
    number_of_compressors: int | None
    ratio_of_compressor_size_to_total_compressor_capacity: float | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None
    defrost_strategy: str | None
    defrost_control: str | None
    defrost_time_period_fraction: float | None
    resistive_defrost_heater_capacity: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    condenser_type: str | None
    water_condenser_volume_flow_rate: float | str | None
    evaporative_condenser_effectiveness: float | None
    evaporative_condenser_air_flow_rate: float | str | None
    evaporative_condenser_pump_rated_power_consumption: float | str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    fuel_type: str | None
    minimum_outdoor_temperature_in_heat_recovery_mode: float | None
    maximum_outdoor_temperature_in_heat_recovery_mode: float | None

class HVACTemplateSystemUnitary(IDFObject):
    system_availability_schedule_name: str | None
    control_zone_or_thermostat_location_name: str | None
    supply_fan_maximum_flow_rate: float | str | None
    supply_fan_operating_mode_schedule_name: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    supply_fan_motor_in_air_stream_fraction: float | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_design_supply_air_temperature: float | None
    cooling_coil_gross_rated_total_capacity: float | str | None
    cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    cooling_coil_gross_rated_cop: float | None
    heating_coil_type: str | None
    heating_coil_availability_schedule_name: str | None
    heating_design_supply_air_temperature: float | None
    heating_coil_capacity: float | str | None
    gas_heating_coil_efficiency: float | None
    gas_heating_coil_parasitic_electric_load: float | None
    maximum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_schedule_name: str | None
    economizer_type: str | None
    economizer_lockout: str | None
    economizer_upper_temperature_limit: float | None
    economizer_lower_temperature_limit: float | None
    economizer_upper_enthalpy_limit: float | None
    economizer_maximum_limit_dewpoint_temperature: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    supply_fan_placement: str | None
    night_cycle_control: str | None
    night_cycle_control_zone_name: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None
    dehumidification_control_type: str | None
    dehumidification_setpoint: float | None
    humidifier_type: str | None
    humidifier_availability_schedule_name: str | None
    humidifier_rated_capacity: float | None
    humidifier_rated_electric_power: float | str | None
    humidifier_control_zone_name: str | None
    humidifier_setpoint: float | None
    return_fan: str | None
    return_fan_total_efficiency: float | None
    return_fan_delta_pressure: float | None
    return_fan_motor_efficiency: float | None
    return_fan_motor_in_air_stream_fraction: float | None

class HVACTemplateSystemUnitaryHeatPumpAirToAir(IDFObject):
    system_availability_schedule_name: str | None
    control_zone_or_thermostat_location_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    supply_fan_operating_mode_schedule_name: str | None
    supply_fan_placement: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    supply_fan_motor_in_air_stream_fraction: float | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_design_supply_air_temperature: float | None
    cooling_coil_gross_rated_total_capacity: float | str | None
    cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    cooling_coil_gross_rated_cop: float | None
    heat_pump_heating_coil_type: str | None
    heat_pump_heating_coil_availability_schedule_name: str | None
    heating_design_supply_air_temperature: float | None
    heat_pump_heating_coil_gross_rated_capacity: float | str | None
    heat_pump_heating_coil_rated_cop: float | None
    heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None
    heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None
    heat_pump_defrost_strategy: str | None
    heat_pump_defrost_control: str | None
    heat_pump_defrost_time_period_fraction: float | None
    supplemental_heating_coil_type: str | None
    supplemental_heating_coil_availability_schedule_name: str | None
    supplemental_heating_coil_capacity: float | str | None
    supplemental_heating_coil_maximum_outdoor_dry_bulb_temperature: float | None
    supplemental_gas_heating_coil_efficiency: float | None
    supplemental_gas_heating_coil_parasitic_electric_load: float | None
    maximum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_schedule_name: str | None
    economizer_type: str | None
    economizer_lockout: str | None
    economizer_maximum_limit_dry_bulb_temperature: float | None
    economizer_maximum_limit_enthalpy: float | None
    economizer_maximum_limit_dewpoint_temperature: float | None
    economizer_minimum_limit_dry_bulb_temperature: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    night_cycle_control: str | None
    night_cycle_control_zone_name: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None
    humidifier_type: str | None
    humidifier_availability_schedule_name: str | None
    humidifier_rated_capacity: float | None
    humidifier_rated_electric_power: float | str | None
    humidifier_control_zone_name: str | None
    humidifier_setpoint: float | None
    return_fan: str | None
    return_fan_total_efficiency: float | None
    return_fan_delta_pressure: float | None
    return_fan_motor_efficiency: float | None
    return_fan_motor_in_air_stream_fraction: float | None

class HVACTemplateSystemUnitarySystem(IDFObject):
    system_availability_schedule_name: str | None
    control_type: str | None
    control_zone_or_thermostat_location_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    supply_fan_operating_mode_schedule_name: str | None
    supply_fan_placement: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    supply_fan_motor_in_air_stream_fraction: float | None
    cooling_coil_type: str | None
    number_of_speeds_for_cooling: int | None
    cooling_coil_availability_schedule_name: str | None
    cooling_design_supply_air_temperature: float | None
    dx_cooling_coil_gross_rated_total_capacity: float | str | None
    dx_cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    dx_cooling_coil_gross_rated_cop: float | None
    heating_coil_type: str | None
    number_of_speeds_or_stages_for_heating: int | None
    heating_coil_availability_schedule_name: str | None
    heating_design_supply_air_temperature: float | None
    heating_coil_gross_rated_capacity: float | str | None
    gas_heating_coil_efficiency: float | None
    gas_heating_coil_parasitic_electric_load: float | None
    heat_pump_heating_coil_gross_rated_cop: float | None
    heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None
    heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None
    heat_pump_defrost_strategy: str | None
    heat_pump_defrost_control: str | None
    heat_pump_defrost_time_period_fraction: float | None
    supplemental_heating_or_reheat_coil_type: str | None
    supplemental_heating_or_reheat_coil_availability_schedule_name: str | None
    supplemental_heating_or_reheat_coil_capacity: float | str | None
    supplemental_heating_or_reheat_coil_maximum_outdoor_dry_bulb_temperature: float | None
    supplemental_gas_heating_or_reheat_coil_efficiency: float | None
    supplemental_gas_heating_or_reheat_coil_parasitic_electric_load: float | None
    maximum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_schedule_name: str | None
    economizer_type: str | None
    economizer_lockout: str | None
    economizer_maximum_limit_dry_bulb_temperature: float | None
    economizer_maximum_limit_enthalpy: float | None
    economizer_maximum_limit_dewpoint_temperature: float | None
    economizer_minimum_limit_dry_bulb_temperature: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None
    heat_recovery_heat_exchanger_type: str | None
    heat_recovery_frost_control_type: str | None
    dehumidification_control_type: str | None
    dehumidification_relative_humidity_setpoint: float | None
    dehumidification_relative_humidity_setpoint_schedule_name: str | None
    humidifier_type: str | None
    humidifier_availability_schedule_name: str | None
    humidifier_rated_capacity: float | None
    humidifier_rated_electric_power: float | str | None
    humidifier_control_zone_name: str | None
    humidifier_relative_humidity_setpoint: float | None
    humidifier_relative_humidity_setpoint_schedule_name: str | None
    sizing_option: str | None
    return_fan: str | None
    return_fan_total_efficiency: float | None
    return_fan_delta_pressure: float | None
    return_fan_motor_efficiency: float | None
    return_fan_motor_in_air_stream_fraction: float | None

class HVACTemplateSystemVAV(IDFObject):
    system_availability_schedule_name: str | None
    supply_fan_maximum_flow_rate: float | str | None
    supply_fan_minimum_flow_rate: float | str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    supply_fan_motor_in_air_stream_fraction: float | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_setpoint_schedule_name: str | None
    cooling_coil_design_setpoint: float | None
    heating_coil_type: str | None
    heating_coil_availability_schedule_name: str | None
    heating_coil_setpoint_schedule_name: str | None
    heating_coil_design_setpoint: float | None
    gas_heating_coil_efficiency: float | None
    gas_heating_coil_parasitic_electric_load: float | None
    preheat_coil_type: str | None
    preheat_coil_availability_schedule_name: str | None
    preheat_coil_setpoint_schedule_name: str | None
    preheat_coil_design_setpoint: float | None
    gas_preheat_coil_efficiency: float | None
    gas_preheat_coil_parasitic_electric_load: float | None
    maximum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_control_type: str | None
    minimum_outdoor_air_schedule_name: str | None
    economizer_type: str | None
    economizer_lockout: str | None
    economizer_upper_temperature_limit: float | None
    economizer_lower_temperature_limit: float | None
    economizer_upper_enthalpy_limit: float | None
    economizer_maximum_limit_dewpoint_temperature: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    supply_fan_placement: str | None
    supply_fan_part_load_power_coefficients: str | None
    night_cycle_control: str | None
    night_cycle_control_zone_name: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None
    cooling_coil_setpoint_reset_type: str | None
    heating_coil_setpoint_reset_type: str | None
    dehumidification_control_type: str | None
    dehumidification_control_zone_name: str | None
    dehumidification_setpoint: float | None
    humidifier_type: str | None
    humidifier_availability_schedule_name: str | None
    humidifier_rated_capacity: float | None
    humidifier_rated_electric_power: float | str | None
    humidifier_control_zone_name: str | None
    humidifier_setpoint: float | None
    sizing_option: str | None
    return_fan: str | None
    return_fan_total_efficiency: float | None
    return_fan_delta_pressure: float | None
    return_fan_motor_efficiency: float | None
    return_fan_motor_in_air_stream_fraction: float | None
    return_fan_part_load_power_coefficients: str | None

class HVACTemplateSystemPackagedVAV(IDFObject):
    system_availability_schedule_name: str | None
    supply_fan_maximum_flow_rate: float | str | None
    supply_fan_minimum_flow_rate: float | str | None
    supply_fan_placement: str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    supply_fan_motor_in_air_stream_fraction: float | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_setpoint_schedule_name: str | None
    cooling_coil_design_setpoint: float | None
    cooling_coil_gross_rated_total_capacity: float | str | None
    cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    cooling_coil_gross_rated_cop: float | None
    heating_coil_type: str | None
    heating_coil_availability_schedule_name: str | None
    heating_coil_setpoint_schedule_name: str | None
    heating_coil_design_setpoint: float | None
    heating_coil_capacity: float | str | None
    gas_heating_coil_efficiency: float | None
    gas_heating_coil_parasitic_electric_load: float | None
    maximum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_control_type: str | None
    minimum_outdoor_air_schedule_name: str | None
    economizer_type: str | None
    economizer_lockout: str | None
    economizer_maximum_limit_dry_bulb_temperature: float | None
    economizer_maximum_limit_enthalpy: float | None
    economizer_maximum_limit_dewpoint_temperature: float | None
    economizer_minimum_limit_dry_bulb_temperature: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    supply_fan_part_load_power_coefficients: str | None
    night_cycle_control: str | None
    night_cycle_control_zone_name: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None
    cooling_coil_setpoint_reset_type: str | None
    heating_coil_setpoint_reset_type: str | None
    dehumidification_control_type: str | None
    dehumidification_control_zone_name: str | None
    dehumidification_setpoint: float | None
    humidifier_type: str | None
    humidifier_availability_schedule_name: str | None
    humidifier_rated_capacity: float | None
    humidifier_rated_electric_power: float | str | None
    humidifier_control_zone_name: str | None
    humidifier_setpoint: float | None
    sizing_option: str | None
    return_fan: str | None
    return_fan_total_efficiency: float | None
    return_fan_delta_pressure: float | None
    return_fan_motor_efficiency: float | None
    return_fan_motor_in_air_stream_fraction: float | None
    return_fan_part_load_power_coefficients: str | None

class HVACTemplateSystemConstantVolume(IDFObject):
    system_availability_schedule_name: str | None
    supply_fan_maximum_flow_rate: float | str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    supply_fan_motor_in_air_stream_fraction: float | None
    supply_fan_placement: str | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_setpoint_control_type: str | None
    cooling_coil_control_zone_name: str | None
    cooling_coil_design_setpoint_temperature: float | None
    cooling_coil_setpoint_schedule_name: str | None
    cooling_coil_setpoint_at_outdoor_dry_bulb_low: float | None
    cooling_coil_reset_outdoor_dry_bulb_low: float | None
    cooling_coil_setpoint_at_outdoor_dry_bulb_high: float | None
    cooling_coil_reset_outdoor_dry_bulb_high: float | None
    heating_coil_type: str | None
    heating_coil_availability_schedule_name: str | None
    heating_coil_setpoint_control_type: str | None
    heating_coil_control_zone_name: str | None
    heating_coil_design_setpoint: float | None
    heating_coil_setpoint_schedule_name: str | None
    heating_coil_setpoint_at_outdoor_dry_bulb_low: float | None
    heating_coil_reset_outdoor_dry_bulb_low: float | None
    heating_coil_setpoint_at_outdoor_dry_bulb_high: float | None
    heating_coil_reset_outdoor_dry_bulb_high: float | None
    heating_coil_capacity: float | str | None
    gas_heating_coil_efficiency: float | None
    gas_heating_coil_parasitic_electric_load: float | None
    preheat_coil_type: str | None
    preheat_coil_availability_schedule_name: str | None
    preheat_coil_design_setpoint: float | None
    preheat_coil_setpoint_schedule_name: str | None
    gas_preheat_coil_efficiency: float | None
    gas_preheat_coil_parasitic_electric_load: float | None
    maximum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_schedule_name: str | None
    economizer_type: str | None
    economizer_upper_temperature_limit: float | None
    economizer_lower_temperature_limit: float | None
    economizer_upper_enthalpy_limit: float | None
    economizer_maximum_limit_dewpoint_temperature: float | None
    supply_plenum_name: str | None
    return_plenum_name: str | None
    night_cycle_control: str | None
    night_cycle_control_zone_name: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None
    heat_recovery_heat_exchanger_type: str | None
    heat_recovery_frost_control_type: str | None
    dehumidification_control_type: str | None
    dehumidification_control_zone_name: str | None
    dehumidification_relative_humidity_setpoint: float | None
    dehumidification_relative_humidity_setpoint_schedule_name: str | None
    humidifier_type: str | None
    humidifier_availability_schedule_name: str | None
    humidifier_rated_capacity: float | None
    humidifier_rated_electric_power: float | str | None
    humidifier_control_zone_name: str | None
    humidifier_relative_humidity_setpoint: float | None
    humidifier_relative_humidity_setpoint_schedule_name: str | None
    return_fan: str | None
    return_fan_total_efficiency: float | None
    return_fan_delta_pressure: float | None
    return_fan_motor_efficiency: float | None
    return_fan_motor_in_air_stream_fraction: float | None

class HVACTemplateSystemDualDuct(IDFObject):
    system_availability_schedule_name: str | None
    system_configuration_type: str | None
    main_supply_fan_maximum_flow_rate: float | str | None
    main_supply_fan_minimum_flow_fraction: float | None
    main_supply_fan_total_efficiency: float | None
    main_supply_fan_delta_pressure: float | None
    main_supply_fan_motor_efficiency: float | None
    main_supply_fan_motor_in_air_stream_fraction: float | None
    main_supply_fan_part_load_power_coefficients: str | None
    cold_duct_supply_fan_maximum_flow_rate: float | str | None
    cold_duct_supply_fan_minimum_flow_fraction: float | None
    cold_duct_supply_fan_total_efficiency: float | None
    cold_duct_supply_fan_delta_pressure: float | None
    cold_duct_supply_fan_motor_efficiency: float | None
    cold_duct_supply_fan_motor_in_air_stream_fraction: float | None
    cold_duct_supply_fan_part_load_power_coefficients: str | None
    cold_duct_supply_fan_placement: str | None
    hot_duct_supply_fan_maximum_flow_rate: float | str | None
    hot_duct_supply_fan_minimum_flow_fraction: float | None
    hot_duct_supply_fan_total_efficiency: float | None
    hot_duct_supply_fan_delta_pressure: float | None
    hot_duct_supply_fan_motor_efficiency: float | None
    hot_duct_supply_fan_motor_in_air_stream_fraction: float | None
    hot_duct_supply_fan_part_load_power_coefficients: str | None
    hot_duct_supply_fan_placement: str | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_setpoint_control_type: str | None
    cooling_coil_design_setpoint_temperature: float | None
    cooling_coil_setpoint_schedule_name: str | None
    cooling_coil_setpoint_at_outdoor_dry_bulb_low: float | None
    cooling_coil_reset_outdoor_dry_bulb_low: float | None
    cooling_coil_setpoint_at_outdoor_dry_bulb_high: float | None
    cooling_coil_reset_outdoor_dry_bulb_high: float | None
    heating_coil_type: str | None
    heating_coil_availability_schedule_name: str | None
    heating_coil_setpoint_control_type: str | None
    heating_coil_design_setpoint: float | None
    heating_coil_setpoint_schedule_name: str | None
    heating_coil_setpoint_at_outdoor_dry_bulb_low: float | None
    heating_coil_reset_outdoor_dry_bulb_low: float | None
    heating_coil_setpoint_at_outdoor_dry_bulb_high: float | None
    heating_coil_reset_outdoor_dry_bulb_high: float | None
    heating_coil_capacity: float | str | None
    gas_heating_coil_efficiency: float | None
    gas_heating_coil_parasitic_electric_load: float | None
    preheat_coil_type: str | None
    preheat_coil_availability_schedule_name: str | None
    preheat_coil_design_setpoint: float | None
    preheat_coil_setpoint_schedule_name: str | None
    gas_preheat_coil_efficiency: float | None
    gas_preheat_coil_parasitic_electric_load: float | None
    maximum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_control_type: str | None
    minimum_outdoor_air_schedule_name: str | None
    economizer_type: str | None
    economizer_lockout: str | None
    economizer_upper_temperature_limit: float | None
    economizer_lower_temperature_limit: float | None
    economizer_upper_enthalpy_limit: float | None
    economizer_maximum_limit_dewpoint_temperature: float | None
    cold_supply_plenum_name: str | None
    hot_supply_plenum_name: str | None
    return_plenum_name: str | None
    night_cycle_control: str | None
    night_cycle_control_zone_name: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None
    heat_recovery_heat_exchanger_type: str | None
    heat_recovery_frost_control_type: str | None
    dehumidification_control_type: str | None
    dehumidification_control_zone_name: str | None
    dehumidification_relative_humidity_setpoint: float | None
    dehumidification_relative_humidity_setpoint_schedule_name: str | None
    humidifier_type: str | None
    humidifier_availability_schedule_name: str | None
    humidifier_rated_capacity: float | None
    humidifier_rated_electric_power: float | str | None
    humidifier_control_zone_name: str | None
    humidifier_relative_humidity_setpoint: float | None
    humidifier_relative_humidity_setpoint_schedule_name: str | None
    sizing_option: str | None
    return_fan: str | None
    return_fan_total_efficiency: float | None
    return_fan_delta_pressure: float | None
    return_fan_motor_efficiency: float | None
    return_fan_motor_in_air_stream_fraction: float | None
    return_fan_part_load_power_coefficients: str | None

class HVACTemplateSystemDedicatedOutdoorAir(IDFObject):
    system_availability_schedule_name: str | None
    air_outlet_type: str | None
    supply_fan_flow_rate: float | str | None
    supply_fan_total_efficiency: float | None
    supply_fan_delta_pressure: float | None
    supply_fan_motor_efficiency: float | None
    supply_fan_motor_in_air_stream_fraction: float | None
    supply_fan_placement: str | None
    cooling_coil_type: str | None
    cooling_coil_availability_schedule_name: str | None
    cooling_coil_setpoint_control_type: str | None
    cooling_coil_design_setpoint: float | None
    cooling_coil_setpoint_schedule_name: str | None
    cooling_coil_setpoint_at_outdoor_dry_bulb_low: float | None
    cooling_coil_reset_outdoor_dry_bulb_low: float | None
    cooling_coil_setpoint_at_outdoor_dry_bulb_high: float | None
    cooling_coil_reset_outdoor_dry_bulb_high: float | None
    dx_cooling_coil_gross_rated_total_capacity: float | str | None
    dx_cooling_coil_gross_rated_sensible_heat_ratio: float | str | None
    dx_cooling_coil_gross_rated_cop: float | None
    heating_coil_type: str | None
    heating_coil_availability_schedule_name: str | None
    heating_coil_setpoint_control_type: str | None
    heating_coil_design_setpoint: float | None
    heating_coil_setpoint_schedule_name: str | None
    heating_coil_setpoint_at_outdoor_dry_bulb_low: float | None
    heating_coil_reset_outdoor_dry_bulb_low: float | None
    heating_coil_setpoint_at_outdoor_dry_bulb_high: float | None
    heating_coil_reset_outdoor_dry_bulb_high: float | None
    gas_heating_coil_efficiency: float | None
    gas_heating_coil_parasitic_electric_load: float | None
    heat_recovery_type: str | None
    heat_recovery_sensible_effectiveness: float | None
    heat_recovery_latent_effectiveness: float | None
    heat_recovery_heat_exchanger_type: str | None
    heat_recovery_frost_control_type: str | None
    dehumidification_control_type: str | None
    dehumidification_setpoint: float | None
    humidifier_type: str | None
    humidifier_availability_schedule_name: str | None
    humidifier_rated_capacity: float | None
    humidifier_rated_electric_power: float | str | None
    humidifier_constant_setpoint: float | None
    dehumidification_setpoint_schedule_name: str | None
    humidifier_setpoint_schedule_name: str | None

class HVACTemplatePlantChilledWaterLoop(IDFObject):
    pump_schedule_name: str | None
    pump_control_type: str | None
    chiller_plant_operation_scheme_type: str | None
    chiller_plant_equipment_operation_schemes_name: str | None
    chilled_water_setpoint_schedule_name: str | None
    chilled_water_design_setpoint: float | None
    chilled_water_pump_configuration: str | None
    primary_chilled_water_pump_rated_head: float | None
    secondary_chilled_water_pump_rated_head: float | None
    condenser_plant_operation_scheme_type: str | None
    condenser_equipment_operation_schemes_name: str | None
    condenser_water_temperature_control_type: str | None
    condenser_water_setpoint_schedule_name: str | None
    condenser_water_design_setpoint: float | None
    condenser_water_pump_rated_head: float | None
    chilled_water_setpoint_reset_type: str | None
    chilled_water_setpoint_at_outdoor_dry_bulb_low: float | None
    chilled_water_reset_outdoor_dry_bulb_low: float | None
    chilled_water_setpoint_at_outdoor_dry_bulb_high: float | None
    chilled_water_reset_outdoor_dry_bulb_high: float | None
    chilled_water_primary_pump_type: str | None
    chilled_water_secondary_pump_type: str | None
    condenser_water_pump_type: str | None
    chilled_water_supply_side_bypass_pipe: str | None
    chilled_water_demand_side_bypass_pipe: str | None
    condenser_water_supply_side_bypass_pipe: str | None
    condenser_water_demand_side_bypass_pipe: str | None
    fluid_type: str | None
    loop_design_delta_temperature: float | None
    minimum_outdoor_dry_bulb_temperature: float | None
    chilled_water_load_distribution_scheme: str | None
    condenser_water_load_distribution_scheme: str | None

class HVACTemplatePlantChiller(IDFObject):
    chiller_type: str | None
    capacity: float | str | None
    nominal_cop: float | None
    condenser_type: str | None
    priority: str | None
    sizing_factor: float | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    minimum_unloading_ratio: float | None
    leaving_chilled_water_lower_temperature_limit: float | None

class HVACTemplatePlantChillerObjectReference(IDFObject):
    chiller_object_type: str | None
    chiller_name: str | None
    priority: float | None

class HVACTemplatePlantTower(IDFObject):
    tower_type: str | None
    high_speed_nominal_capacity: float | str | None
    high_speed_fan_power: float | str | None
    low_speed_nominal_capacity: float | str | None
    low_speed_fan_power: float | str | None
    free_convection_capacity: float | str | None
    priority: str | None
    sizing_factor: float | None
    template_plant_loop_type: str | None

class HVACTemplatePlantTowerObjectReference(IDFObject):
    cooling_tower_object_type: str | None
    cooling_tower_name: str | None
    priority: float | None
    template_plant_loop_type: str | None

class HVACTemplatePlantHotWaterLoop(IDFObject):
    pump_schedule_name: str | None
    pump_control_type: str | None
    hot_water_plant_operation_scheme_type: str | None
    hot_water_plant_equipment_operation_schemes_name: str | None
    hot_water_setpoint_schedule_name: str | None
    hot_water_design_setpoint: float | None
    hot_water_pump_configuration: str | None
    hot_water_pump_rated_head: float | None
    hot_water_setpoint_reset_type: str | None
    hot_water_setpoint_at_outdoor_dry_bulb_low: float | None
    hot_water_reset_outdoor_dry_bulb_low: float | None
    hot_water_setpoint_at_outdoor_dry_bulb_high: float | None
    hot_water_reset_outdoor_dry_bulb_high: float | None
    hot_water_pump_type: str | None
    supply_side_bypass_pipe: str | None
    demand_side_bypass_pipe: str | None
    fluid_type: str | None
    loop_design_delta_temperature: float | None
    maximum_outdoor_dry_bulb_temperature: float | None
    load_distribution_scheme: str | None

class HVACTemplatePlantBoiler(IDFObject):
    boiler_type: str | None
    capacity: float | str | None
    efficiency: float | None
    fuel_type: str | None
    priority: str | None
    sizing_factor: float | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    water_outlet_upper_temperature_limit: float | None
    template_plant_loop_type: str | None

class HVACTemplatePlantBoilerObjectReference(IDFObject):
    boiler_object_type: str | None
    boiler_name: str | None
    priority: float | None
    template_plant_loop_type: str | None

class HVACTemplatePlantMixedWaterLoop(IDFObject):
    pump_schedule_name: str | None
    pump_control_type: str | None
    operation_scheme_type: str | None
    equipment_operation_schemes_name: str | None
    high_temperature_setpoint_schedule_name: str | None
    high_temperature_design_setpoint: float | None
    low_temperature_setpoint_schedule_name: str | None
    low_temperature_design_setpoint: float | None
    water_pump_configuration: str | None
    water_pump_rated_head: float | None
    water_pump_type: str | None
    supply_side_bypass_pipe: str | None
    demand_side_bypass_pipe: str | None
    fluid_type: str | None
    loop_design_delta_temperature: float | None
    load_distribution_scheme: str | None

class DesignSpecificationOutdoorAir(IDFObject):
    outdoor_air_method: str | None
    outdoor_air_flow_per_person: float | None
    outdoor_air_flow_per_zone_floor_area: float | None
    outdoor_air_flow_per_zone: float | None
    outdoor_air_flow_air_changes_per_hour: float | None
    outdoor_air_schedule_name: str | None
    proportional_control_minimum_outdoor_air_flow_rate_schedule_name: str | None

class DesignSpecificationOutdoorAirSpaceList(IDFObject):
    space_name: str | None
    space_design_specification_outdoor_air_object_name: str | None

class DesignSpecificationZoneAirDistribution(IDFObject):
    zone_air_distribution_effectiveness_in_cooling_mode: float | None
    zone_air_distribution_effectiveness_in_heating_mode: float | None
    zone_air_distribution_effectiveness_schedule_name: str | None
    zone_secondary_recirculation_fraction: float | None
    minimum_zone_ventilation_efficiency: float | None

class SizingParameters(IDFObject):
    cooling_sizing_factor: float | None
    timesteps_in_averaging_window: int | None

class SizingZone(IDFObject):
    zone_cooling_design_supply_air_temperature_input_method: str | None
    zone_cooling_design_supply_air_temperature: float | None
    zone_cooling_design_supply_air_temperature_difference: float | None
    zone_heating_design_supply_air_temperature_input_method: str | None
    zone_heating_design_supply_air_temperature: float | None
    zone_heating_design_supply_air_temperature_difference: float | None
    zone_cooling_design_supply_air_humidity_ratio: float | None
    zone_heating_design_supply_air_humidity_ratio: float | None
    design_specification_outdoor_air_object_name: str | None
    zone_heating_sizing_factor: float | None
    zone_cooling_sizing_factor: float | None
    cooling_design_air_flow_method: str | None
    cooling_design_air_flow_rate: float | None
    cooling_minimum_air_flow_per_zone_floor_area: float | None
    cooling_minimum_air_flow: float | None
    cooling_minimum_air_flow_fraction: float | None
    heating_design_air_flow_method: str | None
    heating_design_air_flow_rate: float | None
    heating_maximum_air_flow_per_zone_floor_area: float | None
    heating_maximum_air_flow: float | None
    heating_maximum_air_flow_fraction: float | None
    design_specification_zone_air_distribution_object_name: str | None
    account_for_dedicated_outdoor_air_system: str | None
    dedicated_outdoor_air_system_control_strategy: str | None
    dedicated_outdoor_air_low_setpoint_temperature_for_design: float | str | None
    dedicated_outdoor_air_high_setpoint_temperature_for_design: float | str | None
    zone_load_sizing_method: str | None
    zone_latent_cooling_design_supply_air_humidity_ratio_input_method: str | None
    zone_dehumidification_design_supply_air_humidity_ratio: float | None
    zone_cooling_design_supply_air_humidity_ratio_difference: float | None
    zone_latent_heating_design_supply_air_humidity_ratio_input_method: str | None
    zone_humidification_design_supply_air_humidity_ratio: float | None
    zone_humidification_design_supply_air_humidity_ratio_difference: float | None
    zone_humidistat_dehumidification_set_point_schedule_name: str | None
    zone_humidistat_humidification_set_point_schedule_name: str | None
    type_of_space_sum_to_use: str | None
    heating_coil_sizing_method: str | None
    maximum_heating_capacity_to_cooling_load_sizing_ratio: float | None

class DesignSpecificationZoneHVACSizing(IDFObject):
    cooling_supply_air_flow_rate_method: str | None
    cooling_supply_air_flow_rate: float | str | None
    cooling_supply_air_flow_rate_per_floor_area: float | None
    cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None
    cooling_supply_air_flow_rate_per_unit_cooling_capacity: float | None
    no_load_supply_air_flow_rate_method: str | None
    no_load_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate_per_floor_area: float | None
    no_load_fraction_of_cooling_supply_air_flow_rate: float | None
    no_load_fraction_of_heating_supply_air_flow_rate: float | None
    heating_supply_air_flow_rate_method: str | None
    heating_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate_per_floor_area: float | None
    heating_fraction_of_heating_supply_air_flow_rate: float | None
    heating_supply_air_flow_rate_per_unit_heating_capacity: float | None
    cooling_design_capacity_method: str | None
    cooling_design_capacity: float | str | None
    cooling_design_capacity_per_floor_area: float | None
    fraction_of_autosized_cooling_design_capacity: float | None
    heating_design_capacity_method: str | None
    heating_design_capacity: float | str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None

class DesignSpecificationAirTerminalSizing(IDFObject):
    fraction_of_design_cooling_load: float | None
    cooling_design_supply_air_temperature_difference_ratio: float | None
    fraction_of_design_heating_load: float | None
    heating_design_supply_air_temperature_difference_ratio: float | None
    fraction_of_minimum_outdoor_air_flow: float | None

class SizingSystem(IDFObject):
    type_of_load_to_size_on: str | None
    design_outdoor_air_flow_rate: float | str | None
    central_heating_maximum_system_air_flow_ratio: float | str | None
    preheat_design_temperature: float | None
    preheat_design_humidity_ratio: float | None
    precool_design_temperature: float | None
    precool_design_humidity_ratio: float | None
    central_cooling_design_supply_air_temperature: float | None
    central_heating_design_supply_air_temperature: float | None
    type_of_zone_sum_to_use: str | None
    central_cooling_design_supply_air_humidity_ratio: float | None
    central_heating_design_supply_air_humidity_ratio: float | None
    cooling_supply_air_flow_rate_method: str | None
    cooling_supply_air_flow_rate: float | None
    cooling_supply_air_flow_rate_per_floor_area: float | None
    cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None
    cooling_supply_air_flow_rate_per_unit_cooling_capacity: float | None
    heating_supply_air_flow_rate_method: str | None
    heating_supply_air_flow_rate: float | None
    heating_supply_air_flow_rate_per_floor_area: float | None
    heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None
    heating_fraction_of_autosized_cooling_supply_air_flow_rate: float | None
    heating_supply_air_flow_rate_per_unit_heating_capacity: float | None
    system_outdoor_air_method: str | None
    zone_maximum_outdoor_air_fraction: float | None
    cooling_design_capacity_method: str | None
    cooling_design_capacity: float | str | None
    cooling_design_capacity_per_floor_area: float | None
    fraction_of_autosized_cooling_design_capacity: float | None
    heating_design_capacity_method: str | None
    heating_design_capacity: float | str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    central_cooling_capacity_control_method: str | None
    occupant_diversity: float | str | None
    heating_coil_sizing_method: str | None
    maximum_heating_capacity_to_cooling_capacity_sizing_ratio: float | None

class SizingPlant(IDFObject):
    loop_type: str | None
    design_loop_exit_temperature: float | None
    loop_design_temperature_difference: float | None
    sizing_option: str | None
    zone_timesteps_in_averaging_window: int | None
    coincident_sizing_factor_mode: str | None

class OutputControlSizingStyle(IDFObject): ...

class ZoneControlHumidistat(IDFObject):
    zone_name: str | None
    humidifying_relative_humidity_setpoint_schedule_name: str | None
    dehumidifying_relative_humidity_setpoint_schedule_name: str | None

class ZoneControlThermostat(IDFObject):
    zone_or_zonelist_name: str | None
    control_type_schedule_name: str | None
    control_1_object_type: str | None
    control_1_name: str | None
    control_2_object_type: str | None
    control_2_name: str | None
    control_3_object_type: str | None
    control_3_name: str | None
    control_4_object_type: str | None
    control_4_name: str | None
    temperature_difference_between_cutout_and_setpoint: float | None

class ZoneControlThermostatOperativeTemperature(IDFObject):
    radiative_fraction_input_mode: str | None
    fixed_radiative_fraction: float | None
    radiative_fraction_schedule_name: str | None
    adaptive_comfort_model_type: str | None

class ZoneControlThermostatThermalComfort(IDFObject):
    zone_or_zonelist_name: str | None
    averaging_method: str | None
    specific_people_name: str | None
    minimum_dry_bulb_temperature_setpoint: float | None
    maximum_dry_bulb_temperature_setpoint: float | None
    thermal_comfort_control_type_schedule_name: str | None
    thermal_comfort_control_1_object_type: str | None
    thermal_comfort_control_1_name: str | None
    thermal_comfort_control_2_object_type: str | None
    thermal_comfort_control_2_name: str | None
    thermal_comfort_control_3_object_type: str | None
    thermal_comfort_control_3_name: str | None
    thermal_comfort_control_4_object_type: str | None
    thermal_comfort_control_4_name: str | None

class ZoneControlThermostatTemperatureAndHumidity(IDFObject):
    dehumidifying_relative_humidity_setpoint_schedule_name: str | None
    dehumidification_control_type: str | None
    overcool_range_input_method: str | None
    overcool_constant_range: float | None
    overcool_range_schedule_name: str | None
    overcool_control_ratio: float | None

class ThermostatSetpointSingleHeating(IDFObject):
    setpoint_temperature_schedule_name: str | None

class ThermostatSetpointSingleCooling(IDFObject):
    setpoint_temperature_schedule_name: str | None

class ThermostatSetpointSingleHeatingOrCooling(IDFObject):
    setpoint_temperature_schedule_name: str | None

class ThermostatSetpointDualSetpoint(IDFObject):
    heating_setpoint_temperature_schedule_name: str | None
    cooling_setpoint_temperature_schedule_name: str | None

class ThermostatSetpointThermalComfortFangerSingleHeating(IDFObject):
    fanger_thermal_comfort_schedule_name: str | None

class ThermostatSetpointThermalComfortFangerSingleCooling(IDFObject):
    fanger_thermal_comfort_schedule_name: str | None

class ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling(IDFObject):
    fanger_thermal_comfort_schedule_name: str | None

class ThermostatSetpointThermalComfortFangerDualSetpoint(IDFObject):
    fanger_thermal_comfort_heating_schedule_name: str | None
    fanger_thermal_comfort_cooling_schedule_name: str | None

class ZoneControlThermostatStagedDualSetpoint(IDFObject):
    zone_or_zonelist_name: str | None
    number_of_heating_stages: int | None
    heating_temperature_setpoint_schedule_name: str | None
    heating_throttling_temperature_range: float | None
    stage_1_heating_temperature_offset: float | None
    stage_2_heating_temperature_offset: float | None
    stage_3_heating_temperature_offset: float | None
    stage_4_heating_temperature_offset: float | None
    number_of_cooling_stages: int | None
    cooling_temperature_setpoint_base_schedule_name: str | None
    cooling_throttling_temperature_range: float | None
    stage_1_cooling_temperature_offset: float | None
    stage_2_cooling_temperature_offset: float | None
    stage_3_cooling_temperature_offset: float | None
    stage_4_cooling_temperature_offset: float | None

class ZoneControlContaminantController(IDFObject):
    zone_name: str | None
    carbon_dioxide_control_availability_schedule_name: str | None
    carbon_dioxide_setpoint_schedule_name: str | None
    minimum_carbon_dioxide_concentration_schedule_name: str | None
    maximum_carbon_dioxide_concentration_schedule_name: str | None
    generic_contaminant_control_availability_schedule_name: str | None
    generic_contaminant_setpoint_schedule_name: str | None

class ZoneHVACIdealLoadsAirSystem(IDFObject):
    availability_schedule_name: str | None
    zone_supply_air_node_name: str | None
    zone_exhaust_air_node_name: str | None
    system_inlet_air_node_name: str | None
    maximum_heating_supply_air_temperature: float | None
    minimum_cooling_supply_air_temperature: float | None
    maximum_heating_supply_air_humidity_ratio: float | None
    minimum_cooling_supply_air_humidity_ratio: float | None
    heating_limit: str | None
    maximum_heating_air_flow_rate: float | str | None
    maximum_sensible_heating_capacity: float | str | None
    cooling_limit: str | None
    maximum_cooling_air_flow_rate: float | str | None
    maximum_total_cooling_capacity: float | str | None
    heating_availability_schedule_name: str | None
    cooling_availability_schedule_name: str | None
    dehumidification_control_type: str | None
    cooling_sensible_heat_ratio: float | None
    humidification_control_type: str | None
    design_specification_outdoor_air_object_name: str | None
    outdoor_air_inlet_node_name: str | None
    demand_controlled_ventilation_type: str | None
    outdoor_air_economizer_type: str | None
    heat_recovery_type: str | None
    sensible_heat_recovery_effectiveness: float | None
    latent_heat_recovery_effectiveness: float | None
    design_specification_zonehvac_sizing_object_name: str | None
    heating_fuel_efficiency_schedule_name: str | None
    heating_fuel_type: str | None
    cooling_fuel_efficiency_schedule_name: str | None
    cooling_fuel_type: str | None

class ZoneHVACFourPipeFanCoil(IDFObject):
    availability_schedule_name: str | None
    capacity_control_method: str | None
    maximum_supply_air_flow_rate: float | str | None
    low_speed_supply_air_flow_ratio: float | None
    medium_speed_supply_air_flow_ratio: float | None
    maximum_outdoor_air_flow_rate: float | str | None
    outdoor_air_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_mixer_object_type: str | None
    outdoor_air_mixer_name: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    maximum_cold_water_flow_rate: float | str | None
    minimum_cold_water_flow_rate: float | None
    cooling_convergence_tolerance: float | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    maximum_hot_water_flow_rate: float | str | None
    minimum_hot_water_flow_rate: float | None
    heating_convergence_tolerance: float | None
    availability_manager_list_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    minimum_supply_air_temperature_in_cooling_mode: float | str | None
    maximum_supply_air_temperature_in_heating_mode: float | str | None

class ZoneHVACWindowAirConditioner(IDFObject):
    availability_schedule_name: str | None
    maximum_supply_air_flow_rate: float | str | None
    maximum_outdoor_air_flow_rate: float | str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_mixer_object_type: str | None
    outdoor_air_mixer_name: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    cooling_coil_object_type: str | None
    dx_cooling_coil_name: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    fan_placement: str | None
    cooling_convergence_tolerance: float | None
    availability_manager_list_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None

class ZoneHVACPackagedTerminalAirConditioner(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_mixer_object_type: str | None
    outdoor_air_mixer_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate_control_set_to_low_speed: str | None
    cooling_outdoor_air_flow_rate: float | str | None
    heating_outdoor_air_flow_rate: float | str | None
    no_load_outdoor_air_flow_rate: float | str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    fan_placement: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    availability_manager_list_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None
    capacity_control_method: str | None
    minimum_supply_air_temperature_in_cooling_mode: float | str | None
    maximum_supply_air_temperature_in_heating_mode: float | str | None

class ZoneHVACPackagedTerminalHeatPump(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_mixer_object_type: str | None
    outdoor_air_mixer_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate_control_set_to_low_speed: str | None
    cooling_outdoor_air_flow_rate: float | str | None
    heating_outdoor_air_flow_rate: float | str | None
    no_load_outdoor_air_flow_rate: float | str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    heating_convergence_tolerance: float | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    cooling_convergence_tolerance: float | None
    supplemental_heating_coil_object_type: str | None
    supplemental_heating_coil_name: str | None
    maximum_supply_air_temperature_from_supplemental_heater: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None
    fan_placement: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    availability_manager_list_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None
    capacity_control_method: str | None
    minimum_supply_air_temperature_in_cooling_mode: float | str | None
    maximum_supply_air_temperature_in_heating_mode: float | str | None
    dx_heating_coil_sizing_ratio: float | None

class ZoneHVACWaterToAirHeatPump(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_mixer_object_type: str | None
    outdoor_air_mixer_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate_control_set_to_low_speed: str | None
    cooling_outdoor_air_flow_rate: float | str | None
    heating_outdoor_air_flow_rate: float | str | None
    no_load_outdoor_air_flow_rate: float | str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    supplemental_heating_coil_object_type: str | None
    supplemental_heating_coil_name: str | None
    maximum_supply_air_temperature_from_supplemental_heater: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None
    outdoor_dry_bulb_temperature_sensor_node_name: str | None
    fan_placement: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    availability_manager_list_name: str | None
    heat_pump_coil_water_flow_mode: str | None
    design_specification_zonehvac_sizing_object_name: str | None
    design_specification_multispeed_object_type: str | None
    design_specification_multispeed_object_name: str | None
    dx_heating_coil_sizing_ratio: float | None

class ZoneHVACDehumidifierDX(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    rated_water_removal: float | None
    rated_energy_factor: float | None
    rated_air_flow_rate: float | None
    water_removal_curve_name: str | None
    energy_factor_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None
    minimum_dry_bulb_temperature_for_dehumidifier_operation: float | None
    maximum_dry_bulb_temperature_for_dehumidifier_operation: float | None
    off_cycle_parasitic_electric_load: float | None
    condensate_collection_water_storage_tank_name: str | None

class ZoneHVACEnergyRecoveryVentilator(IDFObject):
    availability_schedule_name: str | None
    heat_exchanger_name: str | None
    supply_air_flow_rate: float | str | None
    exhaust_air_flow_rate: float | str | None
    supply_air_fan_name: str | None
    exhaust_air_fan_name: str | None
    controller_name: str | None
    ventilation_rate_per_unit_floor_area: float | None
    ventilation_rate_per_occupant: float | None
    availability_manager_list_name: str | None

class ZoneHVACEnergyRecoveryVentilatorController(IDFObject):
    temperature_high_limit: float | None
    temperature_low_limit: float | None
    enthalpy_high_limit: float | None
    dewpoint_temperature_limit: float | None
    electronic_enthalpy_limit_curve_name: str | None
    exhaust_air_temperature_limit: str | None
    exhaust_air_enthalpy_limit: str | None
    time_of_day_economizer_flow_control_schedule_name: str | None
    high_humidity_control_flag: str | None
    humidistat_control_zone_name: str | None
    high_humidity_outdoor_air_flow_ratio: float | None
    control_high_indoor_humidity_based_on_outdoor_humidity_ratio: str | None

class ZoneHVACUnitVentilator(IDFObject):
    availability_schedule_name: str | None
    maximum_supply_air_flow_rate: float | str | None
    outdoor_air_control_type: str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_schedule_name: str | None
    maximum_outdoor_air_flow_rate: float | str | None
    maximum_outdoor_air_fraction_or_temperature_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_node_name: str | None
    exhaust_air_node_name: str | None
    mixed_air_node_name: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    coil_option: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    heating_convergence_tolerance: float | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    cooling_convergence_tolerance: float | None
    availability_manager_list_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None

class ZoneHVACUnitHeater(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    maximum_supply_air_flow_rate: float | str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    supply_air_fan_operation_during_no_heating: str | None
    maximum_hot_water_or_steam_flow_rate: float | str | None
    minimum_hot_water_or_steam_flow_rate: float | None
    heating_convergence_tolerance: float | None
    availability_manager_list_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None

class ZoneHVACEvaporativeCoolerUnit(IDFObject):
    availability_schedule_name: str | None
    availability_manager_list_name: str | None
    outdoor_air_inlet_node_name: str | None
    cooler_outlet_node_name: str | None
    zone_relief_air_node_name: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    design_supply_air_flow_rate: float | str | None
    fan_placement: str | None
    cooler_unit_control_method: str | None
    throttling_range_temperature_difference: float | None
    cooling_load_control_threshold_heat_transfer_rate: float | None
    first_evaporative_cooler_object_type: str | None
    first_evaporative_cooler_object_name: str | None
    second_evaporative_cooler_object_type: str | None
    second_evaporative_cooler_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None
    shut_off_relative_humidity: float | None

class ZoneHVACHybridUnitaryHVAC(IDFObject):
    availability_schedule_name: str | None
    availability_manager_list_name: str | None
    minimum_supply_air_temperature_schedule_name: str | None
    maximum_supply_air_temperature_schedule_name: str | None
    minimum_supply_air_humidity_ratio_schedule_name: str | None
    maximum_supply_air_humidity_ratio_schedule_name: str | None
    method_to_choose_controlled_inputs_and_part_runtime_fraction: str | None
    return_air_node_name: str | None
    outdoor_air_node_name: str | None
    supply_air_node_name: str | None
    relief_node_name: str | None
    system_maximum_supply_air_flow_rate: float | None
    external_static_pressure_at_system_maximum_supply_air_flow_rate: float | None
    fan_heat_included_in_lookup_tables: str | None
    fan_heat_gain_location: str | None
    fan_heat_in_air_stream_fraction: float | None
    scaling_factor: float | None
    minimum_time_between_mode_change: float | None
    first_fuel_type: str | None
    second_fuel_type: str | None
    third_fuel_type: str | None
    objective_function_to_minimize: str | None
    design_specification_outdoor_air_object_name: str | None
    mode_0_name: str | None
    mode_0_supply_air_temperature_lookup_table_name: str | None
    mode_0_supply_air_humidity_ratio_lookup_table_name: str | None
    mode_0_system_electric_power_lookup_table_name: str | None
    mode_0_supply_fan_electric_power_lookup_table_name: str | None
    mode_0_external_static_pressure_lookup_table_name: str | None
    mode_0_system_second_fuel_consumption_lookup_table_name: str | None
    mode_0_system_third_fuel_consumption_lookup_table_name: str | None
    mode_0_system_water_use_lookup_table_name: str | None
    mode_0_outdoor_air_fraction: float | None
    mode_0_supply_air_mass_flow_rate_ratio: float | None
    mode_name: str | None
    mode_supply_air_temperature_lookup_table_name: str | None
    mode_supply_air_humidity_ratio_lookup_table_name: str | None
    mode_system_electric_power_lookup_table_name: str | None
    mode_supply_fan_electric_power_lookup_table_name: str | None
    mode_external_static_pressure_lookup_table_name: str | None
    mode_system_second_fuel_consumption_lookup_table_name: str | None
    mode_system_third_fuel_consumption_lookup_table_name: str | None
    mode_system_water_use_lookup_table_name: str | None
    mode_minimum_outdoor_air_temperature: float | None
    mode_maximum_outdoor_air_temperature: float | None
    mode_minimum_outdoor_air_humidity_ratio: float | None
    mode_maximum_outdoor_air_humidity_ratio: float | None
    mode_minimum_outdoor_air_relative_humidity: float | None
    mode_maximum_outdoor_air_relative_humidity: float | None
    mode_minimum_return_air_temperature: float | None
    mode_maximum_return_air_temperature: float | None
    mode_minimum_return_air_humidity_ratio: float | None
    mode_maximum_return_air_humidity_ratio: float | None
    mode_minimum_return_air_relative_humidity: float | None
    mode_maximum_return_air_relative_humidity: float | None
    mode_minimum_outdoor_air_fraction: float | None
    mode_maximum_outdoor_air_fraction: float | None
    mode_minimum_supply_air_mass_flow_rate_ratio: float | None
    mode_maximum_supply_air_mass_flow_rate_ratio: float | None

class ZoneHVACOutdoorAirUnit(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    outdoor_air_flow_rate: float | str | None
    outdoor_air_schedule_name: str | None
    supply_fan_name: str | None
    supply_fan_placement: str | None
    exhaust_fan_name: str | None
    exhaust_air_flow_rate: float | str | None
    exhaust_air_schedule_name: str | None
    unit_control_type: str | None
    high_air_control_temperature_schedule_name: str | None
    low_air_control_temperature_schedule_name: str | None
    outdoor_air_node_name: str | None
    airoutlet_node_name: str | None
    airinlet_node_name: str | None
    supply_fanoutlet_node_name: str | None
    outdoor_air_unit_list_name: str | None
    availability_manager_list_name: str | None

class ZoneHVACOutdoorAirUnitEquipmentList(IDFObject):
    component_1_object_type: str | None
    component_1_name: str | None
    component_2_object_type: str | None
    component_2_name: str | None
    component_3_object_type: str | None
    component_3_name: str | None
    component_4_object_type: str | None
    component_4_name: str | None
    component_5_object_type: str | None
    component_5_name: str | None
    component_6_object_type: str | None
    component_6_name: str | None
    component_7_object_type: str | None
    component_7_name: str | None
    component_8_object_type: str | None
    component_8_name: str | None

class ZoneHVACTerminalUnitVariableRefrigerantFlow(IDFObject):
    terminal_unit_availability_schedule: str | None
    terminal_unit_air_inlet_node_name: str | None
    terminal_unit_air_outlet_node_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    no_cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_heating_supply_air_flow_rate: float | str | None
    cooling_outdoor_air_flow_rate: float | str | None
    heating_outdoor_air_flow_rate: float | str | None
    no_load_outdoor_air_flow_rate: float | str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    supply_air_fan_placement: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_object_name: str | None
    outside_air_mixer_object_type: str | None
    outside_air_mixer_object_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_object_name: str | None
    heating_coil_object_type: str | None
    heating_coil_object_name: str | None
    zone_terminal_unit_on_parasitic_electric_energy_use: float | None
    zone_terminal_unit_off_parasitic_electric_energy_use: float | None
    rated_heating_capacity_sizing_ratio: float | None
    availability_manager_list_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None
    supplemental_heating_coil_object_type: str | None
    supplemental_heating_coil_name: str | None
    maximum_supply_air_temperature_from_supplemental_heater: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None
    controlling_zone_or_thermostat_location: str | None
    design_specification_multispeed_object_type: str | None
    design_specification_multispeed_object_name: str | None

class ZoneHVACBaseboardRadiantConvectiveWaterDesign(IDFObject):
    heating_design_capacity_method: str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    convergence_tolerance: float | None
    fraction_radiant: float | None
    fraction_of_radiant_energy_incident_on_people: float | None

class ZoneHVACBaseboardRadiantConvectiveWater(IDFObject):
    design_object: str | None
    availability_schedule_name: str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    rated_average_water_temperature: float | None
    rated_water_mass_flow_rate: float | None
    heating_design_capacity: float | str | None
    maximum_water_flow_rate: float | str | None
    surface_name: str | None
    fraction_of_radiant_energy_to_surface: float | None

class ZoneHVACBaseboardRadiantConvectiveSteamDesign(IDFObject):
    heating_design_capacity_method: str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    convergence_tolerance: float | None
    fraction_radiant: float | None
    fraction_of_radiant_energy_incident_on_people: float | None

class ZoneHVACBaseboardRadiantConvectiveSteam(IDFObject):
    design_object: str | None
    availability_schedule_name: str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    heating_design_capacity: float | str | None
    degree_of_subcooling: float | None
    maximum_steam_flow_rate: float | str | None
    surface_name: str | None
    fraction_of_radiant_energy_to_surface: float | None

class ZoneHVACBaseboardRadiantConvectiveElectric(IDFObject):
    availability_schedule_name: str | None
    heating_design_capacity_method: str | None
    heating_design_capacity: float | str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    efficiency: float | None
    fraction_radiant: float | None
    fraction_of_radiant_energy_incident_on_people: float | None
    surface_name: str | None
    fraction_of_radiant_energy_to_surface: float | None

class ZoneHVACCoolingPanelRadiantConvectiveWater(IDFObject):
    availability_schedule_name: str | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    rated_inlet_water_temperature: float | None
    rated_inlet_space_temperature: float | None
    rated_water_mass_flow_rate: float | None
    cooling_design_capacity_method: str | None
    cooling_design_capacity: float | str | None
    cooling_design_capacity_per_floor_area: float | None
    fraction_of_autosized_cooling_design_capacity: float | None
    maximum_chilled_water_flow_rate: float | str | None
    control_type: str | None
    cooling_control_throttling_range: float | None
    cooling_control_temperature_schedule_name: str | None
    condensation_control_type: str | None
    condensation_control_dewpoint_offset: float | None
    fraction_radiant: float | None
    fraction_of_radiant_energy_incident_on_people: float | None
    surface_name: str | None
    fraction_of_radiant_energy_to_surface: float | None

class ZoneHVACBaseboardConvectiveWater(IDFObject):
    availability_schedule_name: str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    heating_design_capacity_method: str | None
    heating_design_capacity: float | str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    u_factor_times_area_value: float | str | None
    maximum_water_flow_rate: float | str | None
    convergence_tolerance: float | None

class ZoneHVACBaseboardConvectiveElectric(IDFObject):
    availability_schedule_name: str | None
    heating_design_capacity_method: str | None
    heating_design_capacity: float | str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    efficiency: float | None

class ZoneHVACLowTemperatureRadiantVariableFlow(IDFObject):
    design_object: str | None
    availability_schedule_name: str | None
    zone_name: str | None
    surface_name_or_radiant_surface_group_name: str | None
    hydronic_tubing_length: float | str | None
    heating_design_capacity: float | str | None
    maximum_hot_water_flow: float | str | None
    heating_water_inlet_node_name: str | None
    heating_water_outlet_node_name: str | None
    cooling_design_capacity: float | str | None
    maximum_cold_water_flow: float | str | None
    cooling_water_inlet_node_name: str | None
    cooling_water_outlet_node_name: str | None
    number_of_circuits: str | None
    circuit_length: float | None

class ZoneHVACLowTemperatureRadiantVariableFlowDesign(IDFObject):
    fluid_to_radiant_surface_heat_transfer_model: str | None
    hydronic_tubing_inside_diameter: float | None
    hydronic_tubing_outside_diameter: float | None
    hydronic_tubing_conductivity: float | None
    temperature_control_type: str | None
    setpoint_control_type: str | None
    heating_design_capacity_method: str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    heating_control_throttling_range: float | None
    heating_control_temperature_schedule_name: str | None
    cooling_design_capacity_method: str | None
    cooling_design_capacity_per_floor_area: float | None
    fraction_of_autosized_cooling_design_capacity: float | None
    cooling_control_throttling_range: float | None
    cooling_control_temperature_schedule_name: str | None
    condensation_control_type: str | None
    condensation_control_dewpoint_offset: float | None
    changeover_delay_time_period_schedule: str | None

class ZoneHVACLowTemperatureRadiantConstantFlow(IDFObject):
    design_object: str | None
    availability_schedule_name: str | None
    zone_name: str | None
    surface_name_or_radiant_surface_group_name: str | None
    hydronic_tubing_length: float | str | None
    rated_flow_rate: float | str | None
    pump_flow_rate_schedule_name: str | None
    rated_pump_head: float | None
    rated_power_consumption: float | None
    heating_water_inlet_node_name: str | None
    heating_water_outlet_node_name: str | None
    heating_high_water_temperature_schedule_name: str | None
    heating_low_water_temperature_schedule_name: str | None
    heating_high_control_temperature_schedule_name: str | None
    heating_low_control_temperature_schedule_name: str | None
    cooling_water_inlet_node_name: str | None
    cooling_water_outlet_node_name: str | None
    cooling_high_water_temperature_schedule_name: str | None
    cooling_low_water_temperature_schedule_name: str | None
    cooling_high_control_temperature_schedule_name: str | None
    cooling_low_control_temperature_schedule_name: str | None
    number_of_circuits: str | None
    circuit_length: float | None

class ZoneHVACLowTemperatureRadiantConstantFlowDesign(IDFObject):
    fluid_to_radiant_surface_heat_transfer_model: str | None
    hydronic_tubing_inside_diameter: float | None
    hydronic_tubing_outside_diameter: float | None
    hydronic_tubing_conductivity: float | None
    temperature_control_type: str | None
    running_mean_outdoor_dry_bulb_temperature_weighting_factor: float | None
    motor_efficiency: float | None
    fraction_of_motor_inefficiencies_to_fluid_stream: float | None
    condensation_control_type: str | None
    condensation_control_dewpoint_offset: float | None
    changeover_delay_time_period_schedule: str | None

class ZoneHVACLowTemperatureRadiantElectric(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    surface_name_or_radiant_surface_group_name: str | None
    heating_design_capacity_method: str | None
    heating_design_capacity: float | str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    temperature_control_type: str | None
    setpoint_control_type: str | None
    heating_throttling_range: float | None
    heating_setpoint_temperature_schedule_name: str | None

class ZoneHVACLowTemperatureRadiantSurfaceGroup(IDFObject):
    surface_name: str | None
    flow_fraction_for_surface: float | None

class ZoneHVACHighTemperatureRadiant(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    heating_design_capacity_method: str | None
    heating_design_capacity: float | str | None
    heating_design_capacity_per_floor_area: float | None
    fraction_of_autosized_heating_design_capacity: float | None
    fuel_type: str | None
    combustion_efficiency: float | None
    fraction_of_input_converted_to_radiant_energy: float | None
    fraction_of_input_converted_to_latent_energy: float | None
    fraction_of_input_that_is_lost: float | None
    temperature_control_type: str | None
    heating_throttling_range: float | None
    heating_setpoint_temperature_schedule_name: str | None
    fraction_of_radiant_energy_incident_on_people: float | None
    surface_name: str | None
    fraction_of_radiant_energy_to_surface: float | None

class ZoneHVACVentilatedSlab(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    surface_name_or_radiant_surface_group_name: str | None
    maximum_air_flow_rate: float | str | None
    outdoor_air_control_type: str | None
    minimum_outdoor_air_flow_rate: float | str | None
    minimum_outdoor_air_schedule_name: str | None
    maximum_outdoor_air_flow_rate: float | str | None
    maximum_outdoor_air_fraction_or_temperature_schedule_name: str | None
    system_configuration_type: str | None
    hollow_core_inside_diameter: float | None
    hollow_core_length: float | None
    number_of_cores: float | None
    temperature_control_type: str | None
    heating_high_air_temperature_schedule_name: str | None
    heating_low_air_temperature_schedule_name: str | None
    heating_high_control_temperature_schedule_name: str | None
    heating_low_control_temperature_schedule_name: str | None
    cooling_high_air_temperature_schedule_name: str | None
    cooling_low_air_temperature_schedule_name: str | None
    cooling_high_control_temperature_schedule_name: str | None
    cooling_low_control_temperature_schedule_name: str | None
    return_air_node_name: str | None
    slab_in_node_name: str | None
    zone_supply_air_node_name: str | None
    outdoor_air_node_name: str | None
    relief_air_node_name: str | None
    outdoor_air_mixer_outlet_node_name: str | None
    fan_outlet_node_name: str | None
    fan_name: str | None
    coil_option_type: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    hot_water_or_steam_inlet_node_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    cold_water_inlet_node_name: str | None
    availability_manager_list_name: str | None
    design_specification_zonehvac_sizing_object_name: str | None

class ZoneHVACVentilatedSlabSlabGroup(IDFObject):
    zone_name: str | None
    surface_name: str | None
    core_diameter_for_surface: float | None
    core_length_for_surface: float | None
    core_numbers_for_surface: float | None
    slab_inlet_node_name_for_surface: str | None
    slab_outlet_node_name_for_surface: str | None

class AirTerminalSingleDuctConstantVolumeReheat(IDFObject):
    availability_schedule_name: str | None
    air_outlet_node_name: str | None
    air_inlet_node_name: str | None
    maximum_air_flow_rate: float | str | None
    reheat_coil_object_type: str | None
    reheat_coil_name: str | None
    maximum_hot_water_or_steam_flow_rate: float | str | None
    minimum_hot_water_or_steam_flow_rate: float | None
    convergence_tolerance: float | None
    maximum_reheat_air_temperature: float | None

class AirTerminalSingleDuctConstantVolumeNoReheat(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    maximum_air_flow_rate: float | str | None
    design_specification_outdoor_air_object_name: str | None
    per_person_ventilation_rate_mode: str | None

class AirTerminalSingleDuctVAVNoReheat(IDFObject):
    availability_schedule_name: str | None
    air_outlet_node_name: str | None
    air_inlet_node_name: str | None
    maximum_air_flow_rate: float | str | None
    zone_minimum_air_flow_input_method: str | None
    constant_minimum_air_flow_fraction: float | str | None
    fixed_minimum_air_flow_rate: float | str | None
    minimum_air_flow_fraction_schedule_name: str | None
    design_specification_outdoor_air_object_name: str | None
    minimum_air_flow_turndown_schedule_name: str | None

class AirTerminalSingleDuctVAVReheat(IDFObject):
    availability_schedule_name: str | None
    damper_air_outlet_node_name: str | None
    air_inlet_node_name: str | None
    maximum_air_flow_rate: float | str | None
    zone_minimum_air_flow_input_method: str | None
    constant_minimum_air_flow_fraction: float | str | None
    fixed_minimum_air_flow_rate: float | str | None
    minimum_air_flow_fraction_schedule_name: str | None
    reheat_coil_object_type: str | None
    reheat_coil_name: str | None
    maximum_hot_water_or_steam_flow_rate: float | str | None
    minimum_hot_water_or_steam_flow_rate: float | None
    air_outlet_node_name: str | None
    convergence_tolerance: float | None
    damper_heating_action: str | None
    maximum_flow_per_zone_floor_area_during_reheat: float | str | None
    maximum_flow_fraction_during_reheat: float | str | None
    maximum_reheat_air_temperature: float | None
    design_specification_outdoor_air_object_name: str | None
    minimum_air_flow_turndown_schedule_name: str | None

class AirTerminalSingleDuctVAVReheatVariableSpeedFan(IDFObject):
    availability_schedule_name: str | None
    maximum_cooling_air_flow_rate: float | str | None
    maximum_heating_air_flow_rate: float | str | None
    zone_minimum_air_flow_fraction: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    fan_object_type: str | None
    fan_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    maximum_hot_water_or_steam_flow_rate: float | str | None
    minimum_hot_water_or_steam_flow_rate: float | None
    heating_convergence_tolerance: float | None
    minimum_air_flow_turndown_schedule_name: str | None

class AirTerminalSingleDuctVAVHeatAndCoolNoReheat(IDFObject):
    availability_schedule_name: str | None
    air_outlet_node_name: str | None
    air_inlet_node_name: str | None
    maximum_air_flow_rate: float | str | None
    zone_minimum_air_flow_fraction: float | None
    minimum_air_flow_turndown_schedule_name: str | None

class AirTerminalSingleDuctVAVHeatAndCoolReheat(IDFObject):
    availability_schedule_name: str | None
    damper_air_outlet_node_name: str | None
    air_inlet_node_name: str | None
    maximum_air_flow_rate: float | str | None
    zone_minimum_air_flow_fraction: float | None
    reheat_coil_object_type: str | None
    reheat_coil_name: str | None
    maximum_hot_water_or_steam_flow_rate: float | str | None
    minimum_hot_water_or_steam_flow_rate: float | None
    air_outlet_node_name: str | None
    convergence_tolerance: float | None
    maximum_reheat_air_temperature: float | None
    minimum_air_flow_turndown_schedule_name: str | None

class AirTerminalSingleDuctSeriesPIUReheat(IDFObject):
    availability_schedule_name: str | None
    maximum_air_flow_rate: float | str | None
    maximum_primary_air_flow_rate: float | str | None
    minimum_primary_air_flow_fraction: float | str | None
    supply_air_inlet_node_name: str | None
    secondary_air_inlet_node_name: str | None
    outlet_node_name: str | None
    reheat_coil_air_inlet_node_name: str | None
    zone_mixer_name: str | None
    fan_name: str | None
    reheat_coil_object_type: str | None
    reheat_coil_name: str | None
    maximum_hot_water_or_steam_flow_rate: float | str | None
    minimum_hot_water_or_steam_flow_rate: float | None
    convergence_tolerance: float | None
    fan_control_type: str | None
    minimum_fan_turn_down_ratio: float | None
    heating_control_type: str | None
    design_heating_discharge_air_temperature: float | None
    high_limit_heating_discharge_air_temperature: float | None

class AirTerminalSingleDuctParallelPIUReheat(IDFObject):
    availability_schedule_name: str | None
    maximum_primary_air_flow_rate: float | str | None
    maximum_secondary_air_flow_rate: float | str | None
    minimum_primary_air_flow_fraction: float | str | None
    fan_on_flow_fraction: float | str | None
    supply_air_inlet_node_name: str | None
    secondary_air_inlet_node_name: str | None
    outlet_node_name: str | None
    reheat_coil_air_inlet_node_name: str | None
    zone_mixer_name: str | None
    fan_name: str | None
    reheat_coil_object_type: str | None
    reheat_coil_name: str | None
    maximum_hot_water_or_steam_flow_rate: float | str | None
    minimum_hot_water_or_steam_flow_rate: float | None
    convergence_tolerance: float | None
    fan_control_type: str | None
    minimum_fan_turn_down_ratio: float | None
    heating_control_type: str | None
    design_heating_discharge_air_temperature: float | None
    high_limit_heating_discharge_air_temperature: float | None

class AirTerminalSingleDuctConstantVolumeFourPipeInduction(IDFObject):
    availability_schedule_name: str | None
    maximum_total_air_flow_rate: float | str | None
    induction_ratio: float | None
    supply_air_inlet_node_name: str | None
    induced_air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    maximum_hot_water_flow_rate: float | str | None
    minimum_hot_water_flow_rate: float | None
    heating_convergence_tolerance: float | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    maximum_cold_water_flow_rate: float | str | None
    minimum_cold_water_flow_rate: float | None
    cooling_convergence_tolerance: float | None
    zone_mixer_name: str | None

class AirTerminalSingleDuctConstantVolumeFourPipeBeam(IDFObject):
    primary_air_availability_schedule_name: str | None
    cooling_availability_schedule_name: str | None
    heating_availability_schedule_name: str | None
    primary_air_inlet_node_name: str | None
    primary_air_outlet_node_name: str | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    hot_water_inlet_node_name: str | None
    hot_water_outlet_node_name: str | None
    design_primary_air_volume_flow_rate: float | str | None
    design_chilled_water_volume_flow_rate: float | str | None
    design_hot_water_volume_flow_rate: float | str | None
    zone_total_beam_length: float | str | None
    rated_primary_air_flow_rate_per_beam_length: float | None
    beam_rated_cooling_capacity_per_beam_length: float | None
    beam_rated_cooling_room_air_chilled_water_temperature_difference: float | None
    beam_rated_chilled_water_volume_flow_rate_per_beam_length: float | None
    beam_cooling_capacity_temperature_difference_modification_factor_curve_name: str | None
    beam_cooling_capacity_air_flow_modification_factor_curve_name: str | None
    beam_cooling_capacity_chilled_water_flow_modification_factor_curve_name: str | None
    beam_rated_heating_capacity_per_beam_length: float | None
    beam_rated_heating_room_air_hot_water_temperature_difference: float | None
    beam_rated_hot_water_volume_flow_rate_per_beam_length: float | None
    beam_heating_capacity_temperature_difference_modification_factor_curve_name: str | None
    beam_heating_capacity_air_flow_modification_factor_curve_name: str | None
    beam_heating_capacity_hot_water_flow_modification_factor_curve_name: str | None

class AirTerminalSingleDuctConstantVolumeCooledBeam(IDFObject):
    availability_schedule_name: str | None
    cooled_beam_type: str | None
    supply_air_inlet_node_name: str | None
    supply_air_outlet_node_name: str | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    supply_air_volumetric_flow_rate: float | str | None
    maximum_total_chilled_water_volumetric_flow_rate: float | str | None
    number_of_beams: int | str | None
    beam_length: float | str | None
    design_inlet_water_temperature: float | None
    design_outlet_water_temperature: float | None
    coil_surface_area_per_coil_length: float | None
    model_parameter_a: float | None
    model_parameter_n1: float | None
    model_parameter_n2: float | None
    model_parameter_n3: float | None
    model_parameter_a0: float | None
    model_parameter_k1: float | None
    model_parameter_n: float | None
    coefficient_of_induction_kin: float | str | None
    leaving_pipe_inside_diameter: float | None

class AirTerminalSingleDuctMixer(IDFObject):
    zonehvac_unit_object_type: str | None
    zonehvac_unit_object_name: str | None
    mixer_outlet_node_name: str | None
    mixer_primary_air_inlet_node_name: str | None
    mixer_secondary_air_inlet_node_name: str | None
    mixer_connection_type: str | None
    design_specification_outdoor_air_object_name: str | None
    per_person_ventilation_rate_mode: str | None

class AirTerminalDualDuctConstantVolume(IDFObject):
    availability_schedule_name: str | None
    air_outlet_node_name: str | None
    hot_air_inlet_node_name: str | None
    cold_air_inlet_node_name: str | None
    maximum_air_flow_rate: float | str | None

class AirTerminalDualDuctVAV(IDFObject):
    availability_schedule_name: str | None
    air_outlet_node_name: str | None
    hot_air_inlet_node_name: str | None
    cold_air_inlet_node_name: str | None
    maximum_damper_air_flow_rate: float | str | None
    zone_minimum_air_flow_fraction: float | None
    design_specification_outdoor_air_object_name: str | None
    minimum_air_flow_turndown_schedule_name: str | None

class AirTerminalDualDuctVAVOutdoorAir(IDFObject):
    availability_schedule_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_inlet_node_name: str | None
    recirculated_air_inlet_node_name: str | None
    maximum_terminal_air_flow_rate: float | str | None
    design_specification_outdoor_air_object_name: str | None
    per_person_ventilation_rate_mode: str | None

class ZoneHVACAirDistributionUnit(IDFObject):
    air_distribution_unit_outlet_node_name: str | None
    air_terminal_object_type: str | None
    air_terminal_name: str | None
    nominal_upstream_leakage_fraction: float | None
    constant_downstream_leakage_fraction: float | None
    design_specification_air_terminal_sizing_object_name: str | None

class ZoneHVACExhaustControl(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    design_exhaust_flow_rate: float | str | None
    flow_control_type: str | None
    exhaust_flow_fraction_schedule_name: str | None
    supply_node_or_nodelist_name: str | None
    minimum_zone_temperature_limit_schedule_name: str | None
    minimum_exhaust_flow_fraction_schedule_name: str | None
    balanced_exhaust_fraction_schedule_name: str | None

class ZoneHVACEquipmentList(IDFObject):
    load_distribution_scheme: str | None
    zone_equipment_object_type: str | None
    zone_equipment_name: str | None
    zone_equipment_cooling_sequence: float | None
    zone_equipment_heating_or_no_load_sequence: float | None
    zone_equipment_sequential_cooling_fraction_schedule_name: str | None
    zone_equipment_sequential_heating_fraction_schedule_name: str | None

class ZoneHVACEquipmentConnections(IDFObject):
    zone_conditioning_equipment_list_name: str | None
    zone_air_inlet_node_or_nodelist_name: str | None
    zone_air_exhaust_node_or_nodelist_name: str | None
    zone_air_node_name: str | None
    zone_return_air_node_or_nodelist_name: str | None
    zone_return_air_node_1_flow_rate_fraction_schedule_name: str | None
    zone_return_air_node_1_flow_rate_basis_node_or_nodelist_name: str | None

class SpaceHVACEquipmentConnections(IDFObject):
    space_air_inlet_node_or_nodelist_name: str | None
    space_air_exhaust_node_or_nodelist_name: str | None
    space_air_node_name: str | None
    space_return_air_node_or_nodelist_name: str | None
    space_return_air_node_1_flow_rate_fraction_schedule_name: str | None
    space_return_air_node_1_flow_rate_basis_node_or_nodelist_name: str | None

class SpaceHVACZoneEquipmentSplitter(IDFObject):
    zone_name: str | None
    zone_equipment_object_type: str | None
    zone_equipment_name: str | None
    zone_equipment_outlet_node_name: str | None
    thermostat_control_method: str | None
    control_space_name: str | None
    space_fraction_method: str | None
    space_name: str | None
    space_fraction: float | None
    space_supply_node_name: str | None

class SpaceHVACZoneEquipmentMixer(IDFObject):
    zone_name: str | None
    zone_equipment_inlet_node_name: str | None
    space_fraction_method: str | None
    space_name: str | None
    space_fraction: float | None
    space_node_name: str | None

class SpaceHVACZoneReturnMixer(IDFObject):
    zone_name: str | None
    zone_return_air_node_name: str | None
    space_name: str | None
    space_return_air_node_name: str | None

class FanSystemModel(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    design_maximum_air_flow_rate: float | str | None
    speed_control_method: str | None
    electric_power_minimum_flow_rate_fraction: float | None
    design_pressure_rise: float | None
    motor_efficiency: float | None
    motor_in_air_stream_fraction: float | None
    design_electric_power_consumption: float | str | None
    design_power_sizing_method: str | None
    electric_power_per_unit_flow_rate: float | None
    electric_power_per_unit_flow_rate_per_unit_pressure: float | None
    fan_total_efficiency: float | None
    electric_power_function_of_flow_fraction_curve_name: str | None
    night_ventilation_mode_pressure_rise: float | None
    night_ventilation_mode_flow_fraction: float | None
    motor_loss_zone_name: str | None
    motor_loss_radiative_fraction: float | None
    end_use_subcategory: str | None
    number_of_speeds: int | None
    speed_flow_fraction: float | None
    speed_electric_power_fraction: float | None

class FanConstantVolume(IDFObject):
    availability_schedule_name: str | None
    fan_total_efficiency: float | None
    pressure_rise: float | None
    maximum_flow_rate: float | str | None
    motor_efficiency: float | None
    motor_in_airstream_fraction: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    end_use_subcategory: str | None

class FanVariableVolume(IDFObject):
    availability_schedule_name: str | None
    fan_total_efficiency: float | None
    pressure_rise: float | None
    maximum_flow_rate: float | str | None
    fan_power_minimum_flow_rate_input_method: str | None
    fan_power_minimum_flow_fraction: float | None
    fan_power_minimum_air_flow_rate: float | None
    motor_efficiency: float | None
    motor_in_airstream_fraction: float | None
    fan_power_coefficient_1: float | None
    fan_power_coefficient_2: float | None
    fan_power_coefficient_3: float | None
    fan_power_coefficient_4: float | None
    fan_power_coefficient_5: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    end_use_subcategory: str | None

class FanOnOff(IDFObject):
    availability_schedule_name: str | None
    fan_total_efficiency: float | None
    pressure_rise: float | None
    maximum_flow_rate: float | str | None
    motor_efficiency: float | None
    motor_in_airstream_fraction: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    fan_power_ratio_function_of_speed_ratio_curve_name: str | None
    fan_efficiency_ratio_function_of_speed_ratio_curve_name: str | None
    end_use_subcategory: str | None

class FanZoneExhaust(IDFObject):
    availability_schedule_name: str | None
    fan_total_efficiency: float | None
    pressure_rise: float | None
    maximum_flow_rate: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    end_use_subcategory: str | None
    flow_fraction_schedule_name: str | None
    system_availability_manager_coupling_mode: str | None
    minimum_zone_temperature_limit_schedule_name: str | None
    balanced_exhaust_fraction_schedule_name: str | None

class FanPerformanceNightVentilation(IDFObject):
    fan_total_efficiency: float | None
    pressure_rise: float | None
    maximum_flow_rate: float | str | None
    motor_efficiency: float | None
    motor_in_airstream_fraction: float | None

class FanComponentModel(IDFObject):
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    availability_schedule_name: str | None
    maximum_flow_rate: float | str | None
    minimum_flow_rate: float | str | None
    fan_sizing_factor: float | None
    fan_wheel_diameter: float | None
    fan_outlet_area: float | None
    maximum_fan_static_efficiency: float | None
    euler_number_at_maximum_fan_static_efficiency: float | None
    maximum_dimensionless_fan_airflow: float | None
    motor_fan_pulley_ratio: float | str | None
    belt_maximum_torque: float | str | None
    belt_sizing_factor: float | None
    belt_fractional_torque_transition: float | None
    motor_maximum_speed: float | None
    maximum_motor_output_power: float | str | None
    motor_sizing_factor: float | None
    motor_in_airstream_fraction: float | None
    vfd_efficiency_type: str | None
    maximum_vfd_output_power: float | str | None
    vfd_sizing_factor: float | None
    fan_pressure_rise_curve_name: str | None
    duct_static_pressure_reset_curve_name: str | None
    normalized_fan_static_efficiency_curve_name_non_stall_region: str | None
    normalized_fan_static_efficiency_curve_name_stall_region: str | None
    normalized_dimensionless_airflow_curve_name_non_stall_region: str | None
    normalized_dimensionless_airflow_curve_name_stall_region: str | None
    maximum_belt_efficiency_curve_name: str | None
    normalized_belt_efficiency_curve_name_region_1: str | None
    normalized_belt_efficiency_curve_name_region_2: str | None
    normalized_belt_efficiency_curve_name_region_3: str | None
    maximum_motor_efficiency_curve_name: str | None
    normalized_motor_efficiency_curve_name: str | None
    vfd_efficiency_curve_name: str | None
    end_use_subcategory: str | None

class CoilCoolingWater(IDFObject):
    availability_schedule_name: str | None
    design_water_flow_rate: float | str | None
    design_air_flow_rate: float | str | None
    design_inlet_water_temperature: float | str | None
    design_inlet_air_temperature: float | str | None
    design_outlet_air_temperature: float | str | None
    design_inlet_air_humidity_ratio: float | str | None
    design_outlet_air_humidity_ratio: float | str | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    type_of_analysis: str | None
    heat_exchanger_configuration: str | None
    condensate_collection_water_storage_tank_name: str | None
    design_water_temperature_difference: float | None

class CoilCoolingWaterDetailedGeometry(IDFObject):
    availability_schedule_name: str | None
    maximum_water_flow_rate: float | str | None
    tube_outside_surface_area: float | str | None
    total_tube_inside_area: float | str | None
    fin_surface_area: float | str | None
    minimum_airflow_area: float | str | None
    coil_depth: float | str | None
    fin_diameter: float | str | None
    fin_thickness: float | None
    tube_inside_diameter: float | None
    tube_outside_diameter: float | None
    tube_thermal_conductivity: float | None
    fin_thermal_conductivity: float | None
    fin_spacing: float | None
    tube_depth_spacing: float | None
    number_of_tube_rows: float | None
    number_of_tubes_per_row: float | str | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    condensate_collection_water_storage_tank_name: str | None
    design_water_temperature_difference: float | None
    design_inlet_water_temperature: float | str | None

class CoilSystemCoolingWater(IDFObject):
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    availability_schedule_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    dehumidification_control_type: str | None
    run_on_sensible_load: str | None
    run_on_latent_load: str | None
    minimum_air_to_water_temperature_offset: float | None
    economizer_lockout: str | None
    minimum_water_loop_temperature_for_heat_recovery: float | None
    companion_coil_used_for_heat_recovery: str | None

class CoilCoolingDX(IDFObject):
    evaporator_inlet_node_name: str | None
    evaporator_outlet_node_name: str | None
    availability_schedule_name: str | None
    condenser_zone_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    performance_object_name: str | None
    condensate_collection_water_storage_tank_name: str | None
    evaporative_condenser_supply_water_storage_tank_name: str | None

class CoilCoolingDXCurveFitPerformance(IDFObject):
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None
    unit_internal_static_air_pressure: float | None
    capacity_control_method: str | None
    evaporative_condenser_basin_heater_capacity: float | None
    evaporative_condenser_basin_heater_setpoint_temperature: float | None
    evaporative_condenser_basin_heater_operating_schedule_name: str | None
    compressor_fuel_type: str | None
    base_operating_mode: str | None
    alternative_operating_mode_1: str | None
    alternative_operating_mode_2: str | None

class CoilCoolingDXCurveFitOperatingMode(IDFObject):
    rated_gross_total_cooling_capacity: float | str | None
    rated_evaporator_air_flow_rate: float | str | None
    rated_condenser_air_flow_rate: float | str | None
    maximum_cycling_rate: float | None
    ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    latent_capacity_time_constant: float | None
    nominal_time_for_condensate_removal_to_begin: float | None
    apply_latent_degradation_to_speeds_greater_than_1: str | None
    condenser_type: str | None
    nominal_evaporative_condenser_pump_power: float | str | None
    nominal_speed_number: int | None
    speed_1_name: str | None
    speed_2_name: str | None
    speed_3_name: str | None
    speed_4_name: str | None
    speed_5_name: str | None
    speed_6_name: str | None
    speed_7_name: str | None
    speed_8_name: str | None
    speed_9_name: str | None
    speed_10_name: str | None

class CoilCoolingDXCurveFitSpeed(IDFObject):
    gross_total_cooling_capacity_fraction: float | None
    evaporator_air_flow_rate_fraction: float | None
    condenser_air_flow_rate_fraction: float | None
    gross_sensible_heat_ratio: float | str | None
    gross_cooling_cop: float | None
    active_fraction_of_coil_face_area: float | None
    evaporative_condenser_pump_power_fraction: float | None
    evaporative_condenser_effectiveness: float | None
    total_cooling_capacity_modifier_function_of_temperature_curve_name: str | None
    total_cooling_capacity_modifier_function_of_air_flow_fraction_curve_name: str | None
    energy_input_ratio_modifier_function_of_temperature_curve_name: str | None
    energy_input_ratio_modifier_function_of_air_flow_fraction_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None
    rated_waste_heat_fraction_of_power_input: float | None
    waste_heat_modifier_function_of_temperature_curve_name: str | None
    sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None
    sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None

class CoilDXASHRAE205Performance(IDFObject):
    representation_file_name: str | None
    performance_interpolation_method: str | None
    rated_total_cooling_capacity: float | str | None
    rated_steady_state_heating_capacity: float | str | None

class CoilCoolingDXSingleSpeed(IDFObject):
    availability_schedule_name: str | None
    gross_rated_total_cooling_capacity: float | str | None
    gross_rated_sensible_heat_ratio: float | str | None
    gross_rated_cooling_cop: float | None
    rated_air_flow_rate: float | str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    total_cooling_capacity_function_of_temperature_curve_name: str | None
    total_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    energy_input_ratio_function_of_temperature_curve_name: str | None
    energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    nominal_time_for_condensate_removal_to_begin: float | None
    ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    maximum_cycling_rate: float | None
    latent_capacity_time_constant: float | None
    condenser_air_inlet_node_name: str | None
    condenser_type: str | None
    evaporative_condenser_effectiveness: float | None
    evaporative_condenser_air_flow_rate: float | str | None
    evaporative_condenser_pump_rated_power_consumption: float | str | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None
    supply_water_storage_tank_name: str | None
    condensate_collection_water_storage_tank_name: str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    sensible_heat_ratio_function_of_temperature_curve_name: str | None
    sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None
    report_ashrae_standard_127_performance_ratings: str | None
    zone_name_for_condenser_placement: str | None

class CoilCoolingDXTwoSpeed(IDFObject):
    availability_schedule_name: str | None
    high_speed_gross_rated_total_cooling_capacity: float | str | None
    high_speed_rated_sensible_heat_ratio: float | str | None
    high_speed_gross_rated_cooling_cop: float | None
    high_speed_rated_air_flow_rate: float | str | None
    high_speed_2017_rated_evaporator_fan_power_per_volume_flow_rate: float | None
    high_speed_2023_rated_evaporator_fan_power_per_volume_flow_rate: float | None
    unit_internal_static_air_pressure: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    total_cooling_capacity_function_of_temperature_curve_name: str | None
    total_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    energy_input_ratio_function_of_temperature_curve_name: str | None
    energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None
    low_speed_gross_rated_total_cooling_capacity: float | str | None
    low_speed_gross_rated_sensible_heat_ratio: float | str | None
    low_speed_gross_rated_cooling_cop: float | None
    low_speed_rated_air_flow_rate: float | str | None
    low_speed_2017_rated_evaporator_fan_power_per_volume_flow_rate: float | None
    low_speed_2023_rated_evaporator_fan_power_per_volume_flow_rate: float | None
    low_speed_total_cooling_capacity_function_of_temperature_curve_name: str | None
    low_speed_energy_input_ratio_function_of_temperature_curve_name: str | None
    condenser_air_inlet_node_name: str | None
    condenser_type: str | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    high_speed_evaporative_condenser_effectiveness: float | None
    high_speed_evaporative_condenser_air_flow_rate: float | str | None
    high_speed_evaporative_condenser_pump_rated_power_consumption: float | str | None
    low_speed_evaporative_condenser_effectiveness: float | None
    low_speed_evaporative_condenser_air_flow_rate: float | str | None
    low_speed_evaporative_condenser_pump_rated_power_consumption: float | str | None
    supply_water_storage_tank_name: str | None
    condensate_collection_water_storage_tank_name: str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    sensible_heat_ratio_function_of_temperature_curve_name: str | None
    sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None
    low_speed_sensible_heat_ratio_function_of_temperature_curve_name: str | None
    low_speed_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None
    zone_name_for_condenser_placement: str | None

class CoilCoolingDXMultiSpeed(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    condenser_air_inlet_node_name: str | None
    condenser_type: str | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    supply_water_storage_tank_name: str | None
    condensate_collection_water_storage_tank_name: str | None
    apply_part_load_fraction_to_speeds_greater_than_1: str | None
    apply_latent_degradation_to_speeds_greater_than_1: str | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    fuel_type: str | None
    number_of_speeds: int | None
    speed_1_gross_rated_total_cooling_capacity: float | str | None
    speed_1_gross_rated_sensible_heat_ratio: float | str | None
    speed_1_gross_rated_cooling_cop: float | None
    speed_1_rated_air_flow_rate: float | str | None
    speed_1_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_1_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    speed_1_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    speed_1_part_load_fraction_correlation_curve_name: str | None
    speed_1_nominal_time_for_condensate_removal_to_begin: float | None
    speed_1_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    speed_1_maximum_cycling_rate: float | None
    speed_1_latent_capacity_time_constant: float | None
    speed_1_rated_waste_heat_fraction_of_power_input: float | None
    speed_1_waste_heat_function_of_temperature_curve_name: str | None
    speed_1_evaporative_condenser_effectiveness: float | None
    speed_1_evaporative_condenser_air_flow_rate: float | str | None
    speed_1_rated_evaporative_condenser_pump_power_consumption: float | str | None
    speed_2_gross_rated_total_cooling_capacity: float | str | None
    speed_2_gross_rated_sensible_heat_ratio: float | str | None
    speed_2_gross_rated_cooling_cop: float | None
    speed_2_rated_air_flow_rate: float | str | None
    speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_2_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    speed_2_part_load_fraction_correlation_curve_name: str | None
    speed_2_nominal_time_for_condensate_removal_to_begin: float | None
    speed_2_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    speed_2_maximum_cycling_rate: float | None
    speed_2_latent_capacity_time_constant: float | None
    speed_2_rated_waste_heat_fraction_of_power_input: float | None
    speed_2_waste_heat_function_of_temperature_curve_name: str | None
    speed_2_evaporative_condenser_effectiveness: float | None
    speed_2_evaporative_condenser_air_flow_rate: float | str | None
    speed_2_rated_evaporative_condenser_pump_power_consumption: float | str | None
    speed_3_gross_rated_total_cooling_capacity: float | str | None
    speed_3_gross_rated_sensible_heat_ratio: float | str | None
    speed_3_gross_rated_cooling_cop: float | None
    speed_3_rated_air_flow_rate: float | str | None
    speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_3_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    speed_3_part_load_fraction_correlation_curve_name: str | None
    speed_3_nominal_time_for_condensate_removal_to_begin: float | None
    speed_3_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    speed_3_maximum_cycling_rate: float | None
    speed_3_latent_capacity_time_constant: float | None
    speed_3_rated_waste_heat_fraction_of_power_input: float | None
    speed_3_waste_heat_function_of_temperature_curve_name: str | None
    speed_3_evaporative_condenser_effectiveness: float | None
    speed_3_evaporative_condenser_air_flow_rate: float | str | None
    speed_3_rated_evaporative_condenser_pump_power_consumption: float | str | None
    speed_4_gross_rated_total_cooling_capacity: float | str | None
    speed_4_gross_rated_sensible_heat_ratio: float | str | None
    speed_4_gross_rated_cooling_cop: float | None
    speed_4_rated_air_flow_rate: float | str | None
    speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_4_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    speed_4_part_load_fraction_correlation_curve_name: str | None
    speed_4_nominal_time_for_condensate_removal_to_begin: float | None
    speed_4_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    speed_4_maximum_cycling_rate: float | None
    speed_4_latent_capacity_time_constant: float | None
    speed_4_rated_waste_heat_fraction_of_power_input: float | None
    speed_4_waste_heat_function_of_temperature_curve_name: str | None
    speed_4_evaporative_condenser_effectiveness: float | None
    speed_4_evaporative_condenser_air_flow_rate: float | str | None
    speed_4_rated_evaporative_condenser_pump_power_consumption: float | str | None
    zone_name_for_condenser_placement: str | None

class CoilCoolingDXVariableSpeed(IDFObject):
    availability_schedule_name: str | None
    indoor_air_inlet_node_name: str | None
    indoor_air_outlet_node_name: str | None
    number_of_speeds: int | None
    nominal_speed_level: int | None
    gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float | str | None
    rated_air_flow_rate_at_selected_nominal_speed_level: float | str | None
    nominal_time_for_condensate_to_begin_leaving_the_coil: float | None
    initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None
    maximum_cycling_rate: float | None
    latent_capacity_time_constant: float | None
    fan_delay_time: float | None
    energy_part_load_fraction_curve_name: str | None
    condenser_air_inlet_node_name: str | None
    condenser_type: str | None
    evaporative_condenser_pump_rated_power_consumption: float | str | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    supply_water_storage_tank_name: str | None
    condensate_collection_water_storage_tank_name: str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    speed_1_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_1_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_1_reference_unit_gross_rated_cooling_cop: float | None
    speed_1_reference_unit_rated_air_flow_rate: float | None
    speed_1_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_1_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_1_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_1_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_2_reference_unit_gross_rated_cooling_cop: float | None
    speed_2_reference_unit_rated_air_flow_rate: float | None
    speed_2_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_2_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_3_reference_unit_gross_rated_cooling_cop: float | None
    speed_3_reference_unit_rated_air_flow_rate: float | None
    speed_3_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_3_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_4_reference_unit_gross_rated_cooling_cop: float | None
    speed_4_reference_unit_rated_air_flow_rate: float | None
    speed_4_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_4_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_5_reference_unit_gross_rated_cooling_cop: float | None
    speed_5_reference_unit_rated_air_flow_rate: float | None
    speed_5_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_5_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_6_reference_unit_gross_rated_cooling_cop: float | None
    speed_6_reference_unit_rated_air_flow_rate: float | None
    speed_6_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_6_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_7_reference_unit_gross_rated_cooling_cop: float | None
    speed_7_reference_unit_rated_air_flow_rate: float | None
    speed_7_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_7_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_8_reference_unit_gross_rated_cooling_cop: float | None
    speed_8_reference_unit_rated_air_flow_rate: float | None
    speed_8_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_8_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_9_reference_unit_gross_rated_cooling_cop: float | None
    speed_9_reference_unit_rated_air_flow_rate: float | None
    speed_9_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_9_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_10_reference_unit_gross_rated_cooling_cop: float | None
    speed_10_reference_unit_rated_air_flow_rate: float | None
    speed_10_reference_unit_rated_condenser_air_flow_rate: float | None
    speed_10_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None
    speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None

class CoilCoolingDXTwoStageWithHumidityControlMode(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None
    number_of_capacity_stages: int | None
    number_of_enhanced_dehumidification_modes: int | None
    normal_mode_stage_1_coil_performance_object_type: str | None
    normal_mode_stage_1_coil_performance_name: str | None
    normal_mode_stage_1_2_coil_performance_object_type: str | None
    normal_mode_stage_1_2_coil_performance_name: str | None
    dehumidification_mode_1_stage_1_coil_performance_object_type: str | None
    dehumidification_mode_1_stage_1_coil_performance_name: str | None
    dehumidification_mode_1_stage_1_2_coil_performance_object_type: str | None
    dehumidification_mode_1_stage_1_2_coil_performance_name: str | None
    supply_water_storage_tank_name: str | None
    condensate_collection_water_storage_tank_name: str | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None

class CoilPerformanceDXCooling(IDFObject):
    gross_rated_total_cooling_capacity: float | str | None
    gross_rated_sensible_heat_ratio: float | str | None
    gross_rated_cooling_cop: float | None
    rated_air_flow_rate: float | str | None
    fraction_of_air_flow_bypassed_around_coil: float | None
    total_cooling_capacity_function_of_temperature_curve_name: str | None
    total_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    energy_input_ratio_function_of_temperature_curve_name: str | None
    energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None
    nominal_time_for_condensate_removal_to_begin: float | None
    ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    maximum_cycling_rate: float | None
    latent_capacity_time_constant: float | None
    condenser_air_inlet_node_name: str | None
    condenser_type: str | None
    evaporative_condenser_effectiveness: float | None
    evaporative_condenser_air_flow_rate: float | str | None
    evaporative_condenser_pump_rated_power_consumption: float | str | None
    sensible_heat_ratio_function_of_temperature_curve_name: str | None
    sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None

class CoilCoolingDXVariableRefrigerantFlow(IDFObject):
    availability_schedule_name: str | None
    gross_rated_total_cooling_capacity: float | str | None
    gross_rated_sensible_heat_ratio: float | str | None
    rated_air_flow_rate: float | str | None
    cooling_capacity_ratio_modifier_function_of_temperature_curve_name: str | None
    cooling_capacity_modifier_curve_function_of_flow_fraction_name: str | None
    coil_air_inlet_node: str | None
    coil_air_outlet_node: str | None
    name_of_water_storage_tank_for_condensate_collection: str | None

class CoilHeatingDXVariableRefrigerantFlow(IDFObject):
    availability_schedule: str | None
    gross_rated_heating_capacity: float | str | None
    rated_air_flow_rate: float | str | None
    coil_air_inlet_node: str | None
    coil_air_outlet_node: str | None
    heating_capacity_ratio_modifier_function_of_temperature_curve_name: str | None
    heating_capacity_modifier_function_of_flow_fraction_curve_name: str | None

class CoilCoolingDXVariableRefrigerantFlowFluidTemperatureControl(IDFObject):
    availability_schedule_name: str | None
    coil_air_inlet_node: str | None
    coil_air_outlet_node: str | None
    rated_total_cooling_capacity: float | str | None
    rated_sensible_heat_ratio: float | str | None
    indoor_unit_reference_superheating: float | None
    indoor_unit_evaporating_temperature_function_of_superheating_curve_name: str | None
    name_of_water_storage_tank_for_condensate_collection: str | None

class CoilHeatingDXVariableRefrigerantFlowFluidTemperatureControl(IDFObject):
    availability_schedule: str | None
    coil_air_inlet_node: str | None
    coil_air_outlet_node: str | None
    rated_total_heating_capacity: float | str | None
    indoor_unit_reference_subcooling: float | None
    indoor_unit_condensing_temperature_function_of_subcooling_curve_name: str | None

class CoilHeatingWater(IDFObject):
    availability_schedule_name: str | None
    u_factor_times_area_value: float | str | None
    maximum_water_flow_rate: float | str | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    performance_input_method: str | None
    rated_capacity: float | str | None
    rated_inlet_water_temperature: float | None
    rated_inlet_air_temperature: float | None
    rated_outlet_water_temperature: float | None
    rated_outlet_air_temperature: float | None
    rated_ratio_for_air_and_water_convection: float | None
    design_water_temperature_difference: float | None

class CoilHeatingSteam(IDFObject):
    availability_schedule_name: str | None
    maximum_steam_flow_rate: float | str | None
    degree_of_subcooling: float | None
    degree_of_loop_subcooling: float | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    coil_control_type: str | None
    temperature_setpoint_node_name: str | None

class CoilHeatingElectric(IDFObject):
    availability_schedule_name: str | None
    efficiency: float | None
    nominal_capacity: float | str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    temperature_setpoint_node_name: str | None

class CoilHeatingElectricMultiStage(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    temperature_setpoint_node_name: str | None
    number_of_stages: int | None
    stage_1_efficiency: float | None
    stage_1_nominal_capacity: float | str | None
    stage_2_efficiency: float | None
    stage_2_nominal_capacity: float | str | None
    stage_3_efficiency: float | None
    stage_3_nominal_capacity: float | str | None
    stage_4_efficiency: float | None
    stage_4_nominal_capacity: float | str | None

class CoilHeatingFuel(IDFObject):
    availability_schedule_name: str | None
    fuel_type: str | None
    burner_efficiency: float | None
    nominal_capacity: float | str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    temperature_setpoint_node_name: str | None
    on_cycle_parasitic_electric_load: float | None
    part_load_fraction_correlation_curve_name: str | None
    off_cycle_parasitic_fuel_load: float | None

class CoilHeatingGasMultiStage(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    temperature_setpoint_node_name: str | None
    part_load_fraction_correlation_curve_name: str | None
    off_cycle_parasitic_gas_load: float | None
    number_of_stages: int | None
    stage_1_gas_burner_efficiency: float | None
    stage_1_nominal_capacity: float | str | None
    stage_1_on_cycle_parasitic_electric_load: float | None
    stage_2_gas_burner_efficiency: float | None
    stage_2_nominal_capacity: float | str | None
    stage_2_on_cycle_parasitic_electric_load: float | None
    stage_3_gas_burner_efficiency: float | None
    stage_3_nominal_capacity: float | str | None
    stage_3_on_cycle_parasitic_electric_load: float | None
    stage_4_gas_burner_efficiency: float | None
    stage_4_nominal_capacity: float | str | None
    stage_4_on_cycle_parasitic_electric_load: float | None

class CoilHeatingDesuperheater(IDFObject):
    availability_schedule_name: str | None
    heat_reclaim_recovery_efficiency: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    heating_source_object_type: str | None
    heating_source_name: str | None
    temperature_setpoint_node_name: str | None
    on_cycle_parasitic_electric_load: float | None

class CoilHeatingDXSingleSpeed(IDFObject):
    availability_schedule_name: str | None
    gross_rated_heating_capacity: float | str | None
    gross_rated_heating_cop: float | None
    rated_air_flow_rate: float | str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    heating_capacity_function_of_temperature_curve_name: str | None
    heating_capacity_function_of_flow_fraction_curve_name: str | None
    energy_input_ratio_function_of_temperature_curve_name: str | None
    energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None
    defrost_energy_input_ratio_function_of_temperature_curve_name: str | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None
    defrost_strategy: str | None
    defrost_control: str | None
    defrost_time_period_fraction: float | None
    resistive_defrost_heater_capacity: float | str | None
    region_number_for_calculating_hspf: int | None
    evaporator_air_inlet_node_name: str | None
    zone_name_for_evaporator_placement: str | None
    secondary_coil_air_flow_rate: float | str | None
    secondary_coil_fan_flow_scaling_factor: float | None
    nominal_sensible_heat_ratio_of_secondary_coil: float | None
    sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None
    sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None

class CoilHeatingDXMultiSpeed(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None
    defrost_energy_input_ratio_function_of_temperature_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    defrost_strategy: str | None
    defrost_control: str | None
    defrost_time_period_fraction: float | None
    resistive_defrost_heater_capacity: float | str | None
    apply_part_load_fraction_to_speeds_greater_than_1: str | None
    fuel_type: str | None
    region_number_for_calculating_hspf: int | None
    number_of_speeds: int | None
    speed_1_gross_rated_heating_capacity: float | str | None
    speed_1_gross_rated_heating_cop: float | None
    speed_1_rated_air_flow_rate: float | str | None
    speed_1_heating_capacity_function_of_temperature_curve_name: str | None
    speed_1_heating_capacity_function_of_flow_fraction_curve_name: str | None
    speed_1_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    speed_1_part_load_fraction_correlation_curve_name: str | None
    speed_1_rated_waste_heat_fraction_of_power_input: float | None
    speed_1_waste_heat_function_of_temperature_curve_name: str | None
    speed_2_gross_rated_heating_capacity: float | str | None
    speed_2_gross_rated_heating_cop: float | None
    speed_2_rated_air_flow_rate: float | str | None
    speed_2_heating_capacity_function_of_temperature_curve_name: str | None
    speed_2_heating_capacity_function_of_flow_fraction_curve_name: str | None
    speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    speed_2_part_load_fraction_correlation_curve_name: str | None
    speed_2_rated_waste_heat_fraction_of_power_input: float | None
    speed_2_waste_heat_function_of_temperature_curve_name: str | None
    speed_3_gross_rated_heating_capacity: float | str | None
    speed_3_gross_rated_heating_cop: float | None
    speed_3_rated_air_flow_rate: float | str | None
    speed_3_heating_capacity_function_of_temperature_curve_name: str | None
    speed_3_heating_capacity_function_of_flow_fraction_curve_name: str | None
    speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    speed_3_part_load_fraction_correlation_curve_name: str | None
    speed_3_rated_waste_heat_fraction_of_power_input: float | None
    speed_3_waste_heat_function_of_temperature_curve_name: str | None
    speed_4_gross_rated_heating_capacity: float | str | None
    speed_4_gross_rated_heating_cop: float | None
    speed_4_rated_air_flow_rate: float | str | None
    speed_4_heating_capacity_function_of_temperature_curve_name: str | None
    speed_4_heating_capacity_function_of_flow_fraction_curve_name: str | None
    speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    speed_4_part_load_fraction_correlation_curve_name: str | None
    speed_4_rated_waste_heat_fraction_of_power_input: float | None
    speed_4_waste_heat_function_of_temperature_curve_name: str | None
    zone_name_for_evaporator_placement: str | None
    speed_1_secondary_coil_air_flow_rate: float | str | None
    speed_1_secondary_coil_fan_flow_scaling_factor: float | None
    speed_1_nominal_sensible_heat_ratio_of_secondary_coil: float | None
    speed_1_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None
    speed_1_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None
    speed_2_secondary_coil_air_flow_rate: float | str | None
    speed_2_secondary_coil_fan_flow_scaling_factor: float | None
    speed_2_nominal_sensible_heat_ratio_of_secondary_coil: float | None
    speed_2_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None
    speed_2_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None
    speed_3_secondary_coil_air_flow_rate: float | str | None
    speed_3_secondary_coil_fan_flow_scaling_factor: float | None
    speed_3_nominal_sensible_heat_ratio_of_secondary_coil: float | None
    speed_3_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None
    speed_3_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None
    speed_4_secondary_coil_air_flow_rate: float | str | None
    speed_4_secondary_coil_fan_flow_scaling_factor: float | None
    speed_4_nominal_sensible_heat_ratio_of_secondary_coil: float | None
    speed_4_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None
    speed_4_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None

class CoilHeatingDXVariableSpeed(IDFObject):
    availability_schedule_name: str | None
    indoor_air_inlet_node_name: str | None
    indoor_air_outlet_node_name: str | None
    number_of_speeds: int | None
    nominal_speed_level: int | None
    rated_heating_capacity_at_selected_nominal_speed_level: float | str | None
    rated_air_flow_rate_at_selected_nominal_speed_level: float | str | None
    energy_part_load_fraction_curve_name: str | None
    defrost_energy_input_ratio_function_of_temperature_curve_name: str | None
    minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None
    outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None
    defrost_strategy: str | None
    defrost_control: str | None
    defrost_time_period_fraction: float | None
    resistive_defrost_heater_capacity: float | str | None
    speed_1_reference_unit_gross_rated_heating_capacity: float | None
    speed_1_reference_unit_gross_rated_heating_cop: float | None
    speed_1_reference_unit_rated_air_flow_rate: float | None
    speed_1_heating_capacity_function_of_temperature_curve_name: str | None
    speed_1_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_1_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_2_reference_unit_gross_rated_heating_capacity: float | None
    speed_2_reference_unit_gross_rated_heating_cop: float | None
    speed_2_reference_unit_rated_air_flow_rate: float | None
    speed_2_heating_capacity_function_of_temperature_curve_name: str | None
    speed_2_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_3_reference_unit_gross_rated_heating_capacity: float | None
    speed_3_reference_unit_gross_rated_heating_cop: float | None
    speed_3_reference_unit_rated_air_flow_rate: float | None
    speed_3_heating_capacity_function_of_temperature_curve_name: str | None
    speed_3_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_4_reference_unit_gross_rated_heating_capacity: float | None
    speed_4_reference_unit_gross_rated_heating_cop: float | None
    speed_4_reference_unit_rated_air_flow_rate: float | None
    speed_4_heating_capacity_function_of_temperature_curve_name: str | None
    speed_4_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_5_reference_unit_gross_rated_heating_capacity: float | None
    speed_5_reference_unit_gross_rated_heating_cop: float | None
    speed_5_reference_unit_rated_air_flow_rate: float | None
    speed_5_heating_capacity_function_of_temperature_curve_name: str | None
    speed_5_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_6_reference_unit_gross_rated_heating_capacity: float | None
    speed_6_reference_unit_gross_rated_heating_cop: float | None
    speed_6_reference_unit_rated_air_flow_rate: float | None
    speed_6_heating_capacity_function_of_temperature_curve_name: str | None
    speed_6_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_7_reference_unit_gross_rated_heating_capacity: float | None
    speed_7_reference_unit_gross_rated_heating_cop: float | None
    speed_7_reference_unit_rated_air_flow_rate: float | None
    speed_7_heating_capacity_function_of_temperature_curve_name: str | None
    speed_7_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_8_reference_unit_gross_rated_heating_capacity: float | None
    speed_8_reference_unit_gross_rated_heating_cop: float | None
    speed_8_reference_unit_rated_air_flow_rate: float | None
    speed_8_heating_capacity_function_of_temperature_curve_name: str | None
    speed_8_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_9_reference_unit_gross_rated_heating_capacity: float | None
    speed_9_reference_unit_gross_rated_heating_cop: float | None
    speed_9_reference_unit_rated_air_flow_rate: float | None
    speed_9_heating_capacity_function_of_temperature_curve_name: str | None
    speed_9_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_10_reference_unit_gross_rated_heating_capacity: float | None
    speed_10_reference_unit_gross_rated_heating_cop: float | None
    speed_10_reference_unit_rated_air_flow_rate: float | None
    speed_10_heating_capacity_function_of_temperature_curve_name: str | None
    speed_10_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None

class CoilCoolingWaterToAirHeatPumpParameterEstimation(IDFObject):
    availability_schedule_name: str | None
    compressor_type: str | None
    refrigerant_type: str | None
    design_source_side_flow_rate: float | None
    nominal_cooling_coil_capacity: float | None
    nominal_time_for_condensate_removal_to_begin: float | None
    ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    high_pressure_cutoff: float | None
    low_pressure_cutoff: float | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    load_side_total_heat_transfer_coefficient: float | None
    load_side_outside_surface_heat_transfer_coefficient: float | None
    superheat_temperature_at_the_evaporator_outlet: float | None
    compressor_power_losses: float | None
    compressor_efficiency: float | None
    compressor_piston_displacement: float | None
    compressor_suction_discharge_pressure_drop: float | None
    compressor_clearance_factor: float | None
    refrigerant_volume_flow_rate: float | None
    volume_ratio: float | None
    leak_rate_coefficient: float | None
    source_side_heat_transfer_coefficient: float | None
    source_side_heat_transfer_resistance1: float | None
    source_side_heat_transfer_resistance2: float | None
    part_load_fraction_correlation_curve_name: str | None
    maximum_cycling_rate: float | None
    latent_capacity_time_constant: float | None
    fan_delay_time: float | None

class CoilHeatingWaterToAirHeatPumpParameterEstimation(IDFObject):
    availability_schedule_name: str | None
    compressor_type: str | None
    refrigerant_type: str | None
    design_source_side_flow_rate: float | None
    gross_rated_heating_capacity: float | None
    high_pressure_cutoff: float | None
    low_pressure_cutoff: float | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    load_side_total_heat_transfer_coefficient: float | None
    superheat_temperature_at_the_evaporator_outlet: float | None
    compressor_power_losses: float | None
    compressor_efficiency: float | None
    compressor_piston_displacement: float | None
    compressor_suction_discharge_pressure_drop: float | None
    compressor_clearance_factor: float | None
    refrigerant_volume_flow_rate: float | None
    volume_ratio: float | None
    leak_rate_coefficient: float | None
    source_side_heat_transfer_coefficient: float | None
    source_side_heat_transfer_resistance1: float | None
    source_side_heat_transfer_resistance2: float | None
    part_load_fraction_correlation_curve_name: str | None

class CoilCoolingWaterToAirHeatPumpEquationFit(IDFObject):
    availability_schedule_name: str | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    rated_air_flow_rate: float | str | None
    rated_water_flow_rate: float | str | None
    gross_rated_total_cooling_capacity: float | str | None
    gross_rated_sensible_cooling_capacity: float | str | None
    gross_rated_cooling_cop: float | None
    rated_entering_water_temperature: float | None
    rated_entering_air_dry_bulb_temperature: float | None
    rated_entering_air_wet_bulb_temperature: float | None
    total_cooling_capacity_curve_name: str | None
    sensible_cooling_capacity_curve_name: str | None
    cooling_power_consumption_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None
    nominal_time_for_condensate_removal_to_begin: float | None
    ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None
    maximum_cycling_rate: float | None
    latent_capacity_time_constant: float | None
    fan_delay_time: float | None

class CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit(IDFObject):
    availability_schedule_name: str | None
    water_to_refrigerant_hx_water_inlet_node_name: str | None
    water_to_refrigerant_hx_water_outlet_node_name: str | None
    indoor_air_inlet_node_name: str | None
    indoor_air_outlet_node_name: str | None
    number_of_speeds: int | None
    nominal_speed_level: int | None
    gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float | str | None
    rated_air_flow_rate_at_selected_nominal_speed_level: float | str | None
    rated_water_flow_rate_at_selected_nominal_speed_level: float | str | None
    nominal_time_for_condensate_to_begin_leaving_the_coil: float | None
    initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None
    maximum_cycling_rate: float | None
    latent_capacity_time_constant: float | None
    fan_delay_time: float | None
    flag_for_using_hot_gas_reheat_0_or_1: float | None
    energy_part_load_fraction_curve_name: str | None
    speed_1_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_1_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_1_reference_unit_gross_rated_cooling_cop: float | None
    speed_1_reference_unit_rated_air_flow_rate: float | None
    speed_1_reference_unit_rated_water_flow_rate: float | None
    speed_1_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_1_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_1_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_1_waste_heat_function_of_temperature_curve_name: str | None
    speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_2_reference_unit_gross_rated_cooling_cop: float | None
    speed_2_reference_unit_rated_air_flow_rate: float | None
    speed_2_reference_unit_rated_water_flow_rate: float | None
    speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_2_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_2_waste_heat_function_of_temperature_curve_name: str | None
    speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_3_reference_unit_gross_rated_cooling_cop: float | None
    speed_3_reference_unit_rated_air_flow_rate: float | None
    speed_3_reference_unit_rated_water_flow_rate: float | None
    speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_3_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_3_waste_heat_function_of_temperature_curve_name: str | None
    speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_4_reference_unit_gross_rated_cooling_cop: float | None
    speed_4_reference_unit_rated_air_flow_rate: float | None
    speed_4_reference_unit_rated_water_flow_rate: float | None
    speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_4_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_4_waste_heat_function_of_temperature_curve_name: str | None
    speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_5_reference_unit_gross_rated_cooling_cop: float | None
    speed_5_reference_unit_rated_air_flow_rate: float | None
    speed_5_reference_unit_rated_water_flow_rate: float | None
    speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_5_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_5_waste_heat_function_of_temperature_curve_name: str | None
    speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_6_reference_unit_gross_rated_cooling_cop: float | None
    speed_6_reference_unit_rated_air_flow_rate: float | None
    speed_6_reference_unit_rated_water_flow_rate: float | None
    speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_6_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_6_waste_heat_function_of_temperature_curve_name: str | None
    speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_7_reference_unit_gross_rated_cooling_cop: float | None
    speed_7_reference_unit_rated_air_flow_rate: float | None
    speed_7_reference_unit_rated_water_flow_rate: float | None
    speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_7_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_7_waste_heat_function_of_temperature_curve_name: str | None
    speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_8_reference_unit_gross_rated_cooling_cop: float | None
    speed_8_reference_unit_rated_air_flow_rate: float | None
    speed_8_reference_unit_rated_water_flow_rate: float | None
    speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_8_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_8_waste_heat_function_of_temperature_curve_name: str | None
    speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_9_reference_unit_gross_rated_cooling_cop: float | None
    speed_9_reference_unit_rated_air_flow_rate: float | None
    speed_9_reference_unit_rated_water_flow_rate: float | None
    speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_9_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_9_waste_heat_function_of_temperature_curve_name: str | None
    speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None
    speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None
    speed_10_reference_unit_gross_rated_cooling_cop: float | None
    speed_10_reference_unit_rated_air_flow_rate: float | None
    speed_10_reference_unit_rated_water_flow_rate: float | None
    speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None
    speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_10_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_10_waste_heat_function_of_temperature_curve_name: str | None

class CoilHeatingWaterToAirHeatPumpEquationFit(IDFObject):
    availability_schedule_name: str | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    rated_air_flow_rate: float | str | None
    rated_water_flow_rate: float | str | None
    gross_rated_heating_capacity: float | str | None
    gross_rated_heating_cop: float | None
    rated_entering_water_temperature: float | None
    rated_entering_air_dry_bulb_temperature: float | None
    ratio_of_rated_heating_capacity_to_rated_cooling_capacity: float | None
    heating_capacity_curve_name: str | None
    heating_power_consumption_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None

class CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit(IDFObject):
    availability_schedule_name: str | None
    water_to_refrigerant_hx_water_inlet_node_name: str | None
    water_to_refrigerant_hx_water_outlet_node_name: str | None
    indoor_air_inlet_node_name: str | None
    indoor_air_outlet_node_name: str | None
    number_of_speeds: int | None
    nominal_speed_level: int | None
    rated_heating_capacity_at_selected_nominal_speed_level: float | str | None
    rated_air_flow_rate_at_selected_nominal_speed_level: float | str | None
    rated_water_flow_rate_at_selected_nominal_speed_level: float | str | None
    energy_part_load_fraction_curve_name: str | None
    speed_1_reference_unit_gross_rated_heating_capacity: float | None
    speed_1_reference_unit_gross_rated_heating_cop: float | None
    speed_1_reference_unit_rated_air_flow_rate: float | None
    speed_1_reference_unit_rated_water_flow_rate: float | None
    speed_1_heating_capacity_function_of_temperature_curve_name: str | None
    speed_1_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_1_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_1_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_1_waste_heat_function_of_temperature_curve_name: str | None
    speed_2_reference_unit_gross_rated_heating_capacity: float | None
    speed_2_reference_unit_gross_rated_heating_cop: float | None
    speed_2_reference_unit_rated_air_flow_rate: float | None
    speed_2_reference_unit_rated_water_flow_rate: float | None
    speed_2_heating_capacity_function_of_temperature_curve_name: str | None
    speed_2_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_2_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_2_waste_heat_function_of_temperature_curve_name: str | None
    speed_3_reference_unit_gross_rated_heating_capacity: float | None
    speed_3_reference_unit_gross_rated_heating_cop: float | None
    speed_3_reference_unit_rated_air_flow_rate: float | None
    speed_3_reference_unit_rated_water_flow_rate: float | None
    speed_3_heating_capacity_function_of_temperature_curve_name: str | None
    speed_3_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_3_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_3_waste_heat_function_of_temperature_curve_name: str | None
    speed_4_reference_unit_gross_rated_heating_capacity: float | None
    speed_4_reference_unit_gross_rated_heating_cop: float | None
    speed_4_reference_unit_rated_air_flow_rate: float | None
    speed_4_reference_unit_rated_water_flow_rate: float | None
    speed_4_heating_capacity_function_of_temperature_curve_name: str | None
    speed_4_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_4_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_4_waste_heat_function_of_temperature_curve_name: str | None
    speed_5_reference_unit_gross_rated_heating_capacity: float | None
    speed_5_reference_unit_gross_rated_heating_cop: float | None
    speed_5_reference_unit_rated_air_flow_rate: float | None
    speed_5_reference_unit_rated_water_flow_rate: float | None
    speed_5_heating_capacity_function_of_temperature_curve_name: str | None
    speed_5_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_5_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_5_waste_heat_function_of_temperature_curve_name: str | None
    speed_6_reference_unit_gross_rated_heating_capacity: float | None
    speed_6_reference_unit_gross_rated_heating_cop: float | None
    speed_6_reference_unit_rated_air_flow_rate: float | None
    speed_6_reference_unit_rated_water_flow_rate: float | None
    speed_6_heating_capacity_function_of_temperature_curve_name: str | None
    speed_6_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_6_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_6_waste_heat_function_of_temperature_curve_name: str | None
    speed_7_reference_unit_gross_rated_heating_capacity: float | None
    speed_7_reference_unit_gross_rated_heating_cop: float | None
    speed_7_reference_unit_rated_air_flow_rate: float | None
    speed_7_reference_unit_rated_water_flow_rate: float | None
    speed_7_heating_capacity_function_of_temperature_curve_name: str | None
    speed_7_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_7_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_7_waste_heat_function_of_temperature_curve_name: str | None
    speed_8_reference_unit_gross_rated_heating_capacity: float | None
    speed_8_reference_unit_gross_rated_heating_cop: float | None
    speed_8_reference_unit_rated_air_flow_rate: float | None
    speed_8_reference_unit_rated_water_flow_rate: float | None
    speed_8_heating_capacity_function_of_temperature_curve_name: str | None
    speed_8_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_8_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_8_waste_heat_function_of_temperature_curve_name: str | None
    speed_9_reference_unit_gross_rated_heating_capacity: float | None
    speed_9_reference_unit_gross_rated_heating_cop: float | None
    speed_9_reference_unit_rated_air_flow_rate: float | None
    speed_9_reference_unit_rated_water_flow_rate: float | None
    speed_9_heating_capacity_function_of_temperature_curve_name: str | None
    speed_9_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_9_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_9_waste_heat_function_of_temperature_curve_name: str | None
    speed_10_reference_unit_gross_rated_heating_capacity: float | None
    speed_10_reference_unit_gross_rated_heating_cop: float | None
    speed_10_reference_unit_rated_air_flow_rate: float | None
    speed_10_reference_unit_rated_water_flow_rate: float | None
    speed_10_heating_capacity_function_of_temperature_curve_name: str | None
    speed_10_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_10_heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None
    speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None
    speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None
    speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None
    speed_10_waste_heat_function_of_temperature_curve_name: str | None

class CoilWaterHeatingAirToWaterHeatPumpPumped(IDFObject):
    availability_schedule_name: str | None
    rated_heating_capacity: float | None
    rated_cop: float | None
    rated_sensible_heat_ratio: float | None
    rated_evaporator_inlet_air_dry_bulb_temperature: float | None
    rated_evaporator_inlet_air_wet_bulb_temperature: float | None
    rated_condenser_inlet_water_temperature: float | None
    rated_evaporator_air_flow_rate: float | str | None
    rated_condenser_water_flow_rate: float | str | None
    evaporator_fan_power_included_in_rated_cop: str | None
    condenser_pump_power_included_in_rated_cop: str | None
    condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: str | None
    condenser_water_pump_power: float | None
    fraction_of_condenser_pump_heat_to_water: float | None
    evaporator_air_inlet_node_name: str | None
    evaporator_air_outlet_node_name: str | None
    condenser_water_inlet_node_name: str | None
    condenser_water_outlet_node_name: str | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_ambient_temperature_for_crankcase_heater_operation: float | None
    evaporator_air_temperature_type_for_curve_objects: str | None
    heating_capacity_function_of_temperature_curve_name: str | None
    heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    heating_capacity_function_of_water_flow_fraction_curve_name: str | None
    heating_cop_function_of_temperature_curve_name: str | None
    heating_cop_function_of_air_flow_fraction_curve_name: str | None
    heating_cop_function_of_water_flow_fraction_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None

class CoilWaterHeatingAirToWaterHeatPumpWrapped(IDFObject):
    availability_schedule_name: str | None
    rated_heating_capacity: float | None
    rated_cop: float | None
    rated_sensible_heat_ratio: float | None
    rated_evaporator_inlet_air_dry_bulb_temperature: float | None
    rated_evaporator_inlet_air_wet_bulb_temperature: float | None
    rated_condenser_water_temperature: float | None
    rated_evaporator_air_flow_rate: float | str | None
    evaporator_fan_power_included_in_rated_cop: str | None
    evaporator_air_inlet_node_name: str | None
    evaporator_air_outlet_node_name: str | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_ambient_temperature_for_crankcase_heater_operation: float | None
    evaporator_air_temperature_type_for_curve_objects: str | None
    heating_capacity_function_of_temperature_curve_name: str | None
    heating_capacity_function_of_air_flow_fraction_curve_name: str | None
    heating_cop_function_of_temperature_curve_name: str | None
    heating_cop_function_of_air_flow_fraction_curve_name: str | None
    part_load_fraction_correlation_curve_name: str | None

class CoilWaterHeatingAirToWaterHeatPumpVariableSpeed(IDFObject):
    availability_schedule_name: str | None
    number_of_speeds: int | None
    nominal_speed_level: int | None
    rated_water_heating_capacity: float | None
    rated_evaporator_inlet_air_dry_bulb_temperature: float | None
    rated_evaporator_inlet_air_wet_bulb_temperature: float | None
    rated_condenser_inlet_water_temperature: float | None
    rated_evaporator_air_flow_rate: float | str | None
    rated_condenser_water_flow_rate: float | str | None
    evaporator_fan_power_included_in_rated_cop: str | None
    condenser_pump_power_included_in_rated_cop: str | None
    condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: str | None
    fraction_of_condenser_pump_heat_to_water: float | None
    evaporator_air_inlet_node_name: str | None
    evaporator_air_outlet_node_name: str | None
    condenser_water_inlet_node_name: str | None
    condenser_water_outlet_node_name: str | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_ambient_temperature_for_crankcase_heater_operation: float | None
    evaporator_air_temperature_type_for_curve_objects: str | None
    part_load_fraction_correlation_curve_name: str | None
    speed_1_rated_water_heating_capacity: float | None
    speed_1_rated_water_heating_cop: float | None
    speed_1_rated_sensible_heat_ratio: float | None
    speed_1_reference_unit_rated_air_flow_rate: float | None
    speed_1_reference_unit_rated_water_flow_rate: float | None
    speed_1_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_1_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_1_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_1_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_1_cop_function_of_temperature_curve_name: str | None
    speed_1_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_1_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_2_rated_water_heating_capacity: float | None
    speed_2_rated_water_heating_cop: float | None
    speed_2_rated_sensible_heat_ratio: float | None
    speed_2_reference_unit_rated_air_flow_rate: float | None
    speed_2_reference_unit_rated_water_flow_rate: float | None
    speed_2_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_2_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_2_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_2_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_2_cop_function_of_temperature_curve_name: str | None
    speed_2_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_2_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_3_rated_water_heating_capacity: float | None
    speed_3_rated_water_heating_cop: float | None
    speed_3_rated_sensible_heat_ratio: float | None
    speed_3_reference_unit_rated_air_flow_rate: float | None
    speed_3_reference_unit_rated_water_flow_rate: float | None
    speed_3_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_3_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_3_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_3_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_3_cop_function_of_temperature_curve_name: str | None
    speed_3_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_3_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_4_rated_water_heating_capacity: float | None
    speed_4_rated_water_heating_cop: float | None
    speed_4_rated_sensible_heat_ratio: float | None
    speed_4_reference_unit_rated_air_flow_rate: float | None
    speed_4_reference_unit_rated_water_flow_rate: float | None
    speed_4_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_4_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_4_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_4_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_4_cop_function_of_temperature_curve_name: str | None
    speed_4_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_4_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_5_rated_water_heating_capacity: float | None
    speed_5_rated_water_heating_cop: float | None
    speed_5_rated_sensible_heat_ratio: float | None
    speed_5_reference_unit_rated_air_flow_rate: float | None
    speed_5_reference_unit_rated_water_flow_rate: float | None
    speed_5_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_5_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_5_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_5_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_5_cop_function_of_temperature_curve_name: str | None
    speed_5_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_5_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_6_rated_water_heating_capacity: float | None
    speed_6_rated_water_heating_cop: float | None
    speed_6_rated_sensible_heat_ratio: float | None
    speed_6_reference_unit_rated_air_flow_rate: float | None
    speed_6_reference_unit_rated_water_flow_rate: float | None
    speed_6_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_6_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_6_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_6_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_6_cop_function_of_temperature_curve_name: str | None
    speed_6_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_6_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_7_rated_water_heating_capacity: float | None
    speed_7_rated_water_heating_cop: float | None
    speed_7_rated_sensible_heat_ratio: float | None
    speed_7_reference_unit_rated_air_flow_rate: float | None
    speed_7_reference_unit_rated_water_flow_rate: float | None
    speed_7_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_7_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_7_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_7_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_7_cop_function_of_temperature_curve_name: str | None
    speed_7_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_7_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_8_rated_water_heating_capacity: float | None
    speed_8_rated_water_heating_cop: float | None
    speed_8_rated_sensible_heat_ratio: float | None
    speed_8_reference_unit_rated_air_flow_rate: float | None
    speed_8_reference_unit_rated_water_flow_rate: float | None
    speed_8_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_8_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_8_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_8_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_8_cop_function_of_temperature_curve_name: str | None
    speed_8_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_8_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_9_rated_water_heating_capacity: float | None
    speed_9_rated_water_heating_cop: float | None
    speed_9_rated_sensible_heat_ratio: float | None
    speed_9_reference_unit_rated_air_flow_rate: float | None
    speed_9_reference_unit_rated_water_flow_rate: float | None
    speed_9_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_9_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_9_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_9_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_9_cop_function_of_temperature_curve_name: str | None
    speed_9_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_9_cop_function_of_water_flow_fraction_curve_name: str | None
    speed_10_rated_water_heating_capacity: float | None
    speed_10_rated_water_heating_cop: float | None
    speed_10_rated_sensible_heat_ratio: float | None
    speed_10_reference_unit_rated_air_flow_rate: float | None
    speed_10_reference_unit_rated_water_flow_rate: float | None
    speed_10_reference_unit_water_pump_input_power_at_rated_conditions: float | None
    speed_10_total_wh_capacity_function_of_temperature_curve_name: str | None
    speed_10_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None
    speed_10_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None
    speed_10_cop_function_of_temperature_curve_name: str | None
    speed_10_cop_function_of_air_flow_fraction_curve_name: str | None
    speed_10_cop_function_of_water_flow_fraction_curve_name: str | None

class CoilWaterHeatingDesuperheater(IDFObject):
    availability_schedule_name: str | None
    setpoint_temperature_schedule_name: str | None
    dead_band_temperature_difference: float | None
    rated_heat_reclaim_recovery_efficiency: float | None
    rated_inlet_water_temperature: float | None
    rated_outdoor_air_temperature: float | None
    maximum_inlet_water_temperature_for_heat_reclaim: float | None
    heat_reclaim_efficiency_function_of_temperature_curve_name: str | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    tank_object_type: str | None
    tank_name: str | None
    heating_source_object_type: str | None
    heating_source_name: str | None
    water_flow_rate: float | None
    water_pump_power: float | None
    fraction_of_pump_heat_to_water: float | None
    on_cycle_parasitic_electric_load: float | None
    off_cycle_parasitic_electric_load: float | None

class CoilSystemCoolingDX(IDFObject):
    availability_schedule_name: str | None
    dx_cooling_coil_system_inlet_node_name: str | None
    dx_cooling_coil_system_outlet_node_name: str | None
    dx_cooling_coil_system_sensor_node_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    dehumidification_control_type: str | None
    run_on_sensible_load: str | None
    run_on_latent_load: str | None
    use_outdoor_air_dx_cooling_coil: str | None
    outdoor_air_dx_cooling_coil_leaving_minimum_air_temperature: float | None

class CoilSystemHeatingDX(IDFObject):
    availability_schedule_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None

class CoilSystemCoolingWaterHeatExchangerAssisted(IDFObject):
    heat_exchanger_object_type: str | None
    heat_exchanger_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None

class CoilSystemCoolingDXHeatExchangerAssisted(IDFObject):
    heat_exchanger_object_type: str | None
    heat_exchanger_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None

class CoilSystemIntegratedHeatPumpAirSource(IDFObject):
    supply_hot_water_flow_sensor_node_name: str | None
    space_cooling_coil_name: str | None
    space_heating_coil_name: str | None
    dedicated_water_heating_coil_name: str | None
    scwh_coil_name: str | None
    scdwh_cooling_coil_name: str | None
    scdwh_water_heating_coil_name: str | None
    shdwh_heating_coil_name: str | None
    shdwh_water_heating_coil_name: str | None
    indoor_temperature_limit_for_scwh_mode: float | None
    ambient_temperature_limit_for_scwh_mode: float | None
    indoor_temperature_above_which_wh_has_higher_priority: float | None
    ambient_temperature_above_which_wh_has_higher_priority: float | None
    flag_to_indicate_load_control_in_scwh_mode: int | None
    minimum_speed_level_for_scwh_mode: int | None
    maximum_water_flow_volume_before_switching_from_scdwh_to_scwh_mode: float | None
    minimum_speed_level_for_scdwh_mode: int | None
    maximum_running_time_before_allowing_electric_resistance_heat_use_during_shdwh_mode: float | None
    minimum_speed_level_for_shdwh_mode: int | None

class CoilCoolingDXSingleSpeedThermalStorage(IDFObject):
    availability_schedule_name: str | None
    operating_mode_control_method: str | None
    operation_mode_control_schedule_name: str | None
    storage_type: str | None
    user_defined_fluid_type: str | None
    fluid_storage_volume: float | str | None
    ice_storage_capacity: float | str | None
    storage_capacity_sizing_factor: float | None
    storage_tank_ambient_temperature_node_name: str | None
    storage_tank_to_ambient_u_value_times_area_heat_transfer_coefficient: float | None
    fluid_storage_tank_rating_temperature: float | None
    rated_evaporator_air_flow_rate: float | str | None
    evaporator_air_inlet_node_name: str | None
    evaporator_air_outlet_node_name: str | None
    cooling_only_mode_available: str | None
    cooling_only_mode_rated_total_evaporator_cooling_capacity: float | str | None
    cooling_only_mode_rated_sensible_heat_ratio: float | None
    cooling_only_mode_rated_cop: float | None
    cooling_only_mode_total_evaporator_cooling_capacity_function_of_temperature_curve_name: str | None
    cooling_only_mode_total_evaporator_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    cooling_only_mode_energy_input_ratio_function_of_temperature_curve_name: str | None
    cooling_only_mode_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    cooling_only_mode_part_load_fraction_correlation_curve_name: str | None
    cooling_only_mode_sensible_heat_ratio_function_of_temperature_curve_name: str | None
    cooling_only_mode_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None
    cooling_and_charge_mode_available: str | None
    cooling_and_charge_mode_rated_total_evaporator_cooling_capacity: float | str | None
    cooling_and_charge_mode_capacity_sizing_factor: float | None
    cooling_and_charge_mode_rated_storage_charging_capacity: float | str | None
    cooling_and_charge_mode_storage_capacity_sizing_factor: float | None
    cooling_and_charge_mode_rated_sensible_heat_ratio: float | None
    cooling_and_charge_mode_cooling_rated_cop: float | None
    cooling_and_charge_mode_charging_rated_cop: float | None
    cooling_and_charge_mode_total_evaporator_cooling_capacity_function_of_temperature_curve_name: str | None
    cooling_and_charge_mode_total_evaporator_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    cooling_and_charge_mode_evaporator_energy_input_ratio_function_of_temperature_curve_name: str | None
    cooling_and_charge_mode_evaporator_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    cooling_and_charge_mode_evaporator_part_load_fraction_correlation_curve_name: str | None
    cooling_and_charge_mode_storage_charge_capacity_function_of_temperature_curve_name: str | None
    cooling_and_charge_mode_storage_charge_capacity_function_of_total_evaporator_plr_curve_name: str | None
    cooling_and_charge_mode_storage_energy_input_ratio_function_of_temperature_curve_name: str | None
    cooling_and_charge_mode_storage_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    cooling_and_charge_mode_storage_energy_part_load_fraction_correlation_curve_name: str | None
    cooling_and_charge_mode_sensible_heat_ratio_function_of_temperature_curve_name: str | None
    cooling_and_charge_mode_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None
    cooling_and_discharge_mode_available: str | None
    cooling_and_discharge_mode_rated_total_evaporator_cooling_capacity: float | str | None
    cooling_and_discharge_mode_evaporator_capacity_sizing_factor: float | None
    cooling_and_discharge_mode_rated_storage_discharging_capacity: float | str | None
    cooling_and_discharge_mode_storage_discharge_capacity_sizing_factor: float | None
    cooling_and_discharge_mode_rated_sensible_heat_ratio: float | None
    cooling_and_discharge_mode_cooling_rated_cop: float | None
    cooling_and_discharge_mode_discharging_rated_cop: float | None
    cooling_and_discharge_mode_total_evaporator_cooling_capacity_function_of_temperature_curve_name: str | None
    cooling_and_discharge_mode_total_evaporator_cooling_capacity_function_of_flow_fraction_curve_name: str | None
    cooling_and_discharge_mode_evaporator_energy_input_ratio_function_of_temperature_curve_name: str | None
    cooling_and_discharge_mode_evaporator_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    cooling_and_discharge_mode_evaporator_part_load_fraction_correlation_curve_name: str | None
    cooling_and_discharge_mode_storage_discharge_capacity_function_of_temperature_curve_name: str | None
    cooling_and_discharge_mode_storage_discharge_capacity_function_of_flow_fraction_curve_name: str | None
    cooling_and_discharge_mode_storage_discharge_capacity_function_of_total_evaporator_plr_curve_name: str | None
    cooling_and_discharge_mode_storage_energy_input_ratio_function_of_temperature_curve_name: str | None
    cooling_and_discharge_mode_storage_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    cooling_and_discharge_mode_storage_energy_part_load_fraction_correlation_curve_name: str | None
    cooling_and_discharge_mode_sensible_heat_ratio_function_of_temperature_curve_name: str | None
    cooling_and_discharge_mode_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None
    charge_only_mode_available: str | None
    charge_only_mode_rated_storage_charging_capacity: float | str | None
    charge_only_mode_capacity_sizing_factor: float | None
    charge_only_mode_charging_rated_cop: float | None
    charge_only_mode_storage_charge_capacity_function_of_temperature_curve_name: str | None
    charge_only_mode_storage_energy_input_ratio_function_of_temperature_curve_name: str | None
    discharge_only_mode_available: str | None
    discharge_only_mode_rated_storage_discharging_capacity: float | str | None
    discharge_only_mode_capacity_sizing_factor: float | None
    discharge_only_mode_rated_sensible_heat_ratio: float | None
    discharge_only_mode_rated_cop: float | None
    discharge_only_mode_storage_discharge_capacity_function_of_temperature_curve_name: str | None
    discharge_only_mode_storage_discharge_capacity_function_of_flow_fraction_curve_name: str | None
    discharge_only_mode_energy_input_ratio_function_of_temperature_curve_name: str | None
    discharge_only_mode_energy_input_ratio_function_of_flow_fraction_curve_name: str | None
    discharge_only_mode_part_load_fraction_correlation_curve_name: str | None
    discharge_only_mode_sensible_heat_ratio_function_of_temperature_curve_name: str | None
    discharge_only_mode_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None
    ancillary_electric_power: float | None
    cold_weather_operation_minimum_outdoor_air_temperature: float | None
    cold_weather_operation_ancillary_power: float | None
    condenser_air_inlet_node_name: str | None
    condenser_air_outlet_node_name: str | None
    condenser_design_air_flow_rate: float | str | None
    condenser_air_flow_sizing_factor: float | None
    condenser_type: str | None
    evaporative_condenser_effectiveness: float | None
    evaporative_condenser_pump_rated_power_consumption: float | str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_availability_schedule_name: str | None
    supply_water_storage_tank_name: str | None
    condensate_collection_water_storage_tank_name: str | None
    storage_tank_plant_connection_inlet_node_name: str | None
    storage_tank_plant_connection_outlet_node_name: str | None
    storage_tank_plant_connection_design_flow_rate: float | None
    storage_tank_plant_connection_heat_transfer_effectiveness: float | None
    storage_tank_minimum_operating_limit_fluid_temperature: float | None
    storage_tank_maximum_operating_limit_fluid_temperature: float | None

class EvaporativeCoolerDirectCelDekPad(IDFObject):
    availability_schedule_name: str | None
    direct_pad_area: float | str | None
    direct_pad_depth: float | str | None
    recirculating_water_pump_power_consumption: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    control_type: str | None
    water_supply_storage_tank_name: str | None

class EvaporativeCoolerIndirectCelDekPad(IDFObject):
    availability_schedule_name: str | None
    direct_pad_area: float | str | None
    direct_pad_depth: float | str | None
    recirculating_water_pump_power_consumption: float | None
    secondary_air_fan_flow_rate: float | None
    secondary_air_fan_total_efficiency: float | None
    secondary_air_fan_delta_pressure: float | None
    indirect_heat_exchanger_effectiveness: float | None
    primary_air_inlet_node_name: str | None
    primary_air_outlet_node_name: str | None
    control_type: str | None
    water_supply_storage_tank_name: str | None
    secondary_air_inlet_node_name: str | None

class EvaporativeCoolerIndirectWetCoil(IDFObject):
    availability_schedule_name: str | None
    coil_maximum_efficiency: float | None
    coil_flow_ratio: float | None
    recirculating_water_pump_power_consumption: float | None
    secondary_air_fan_flow_rate: float | None
    secondary_air_fan_total_efficiency: float | None
    secondary_air_fan_delta_pressure: float | None
    primary_air_inlet_node_name: str | None
    primary_air_outlet_node_name: str | None
    control_type: str | None
    water_supply_storage_tank_name: str | None
    secondary_air_inlet_node_name: str | None

class EvaporativeCoolerIndirectResearchSpecial(IDFObject):
    availability_schedule_name: str | None
    cooler_wetbulb_design_effectiveness: float | None
    wetbulb_effectiveness_flow_ratio_modifier_curve_name: str | None
    cooler_drybulb_design_effectiveness: float | None
    drybulb_effectiveness_flow_ratio_modifier_curve_name: str | None
    recirculating_water_pump_design_power: float | str | None
    water_pump_power_sizing_factor: float | None
    water_pump_power_modifier_curve_name: str | None
    secondary_air_design_flow_rate: float | str | None
    secondary_air_flow_scaling_factor: float | None
    secondary_air_fan_design_power: float | str | None
    secondary_air_fan_sizing_specific_power: float | None
    secondary_air_fan_power_modifier_curve_name: str | None
    primary_air_inlet_node_name: str | None
    primary_air_outlet_node_name: str | None
    primary_air_design_flow_rate: float | str | None
    dewpoint_effectiveness_factor: float | None
    secondary_air_inlet_node_name: str | None
    secondary_air_outlet_node_name: str | None
    sensor_node_name: str | None
    relief_air_inlet_node_name: str | None
    water_supply_storage_tank_name: str | None
    drift_loss_fraction: float | None
    blowdown_concentration_ratio: float | None
    evaporative_operation_minimum_limit_secondary_air_drybulb_temperature: float | None
    evaporative_operation_maximum_limit_outdoor_wetbulb_temperature: float | None
    dry_operation_maximum_limit_outdoor_drybulb_temperature: float | None

class EvaporativeCoolerDirectResearchSpecial(IDFObject):
    availability_schedule_name: str | None
    cooler_design_effectiveness: float | None
    effectiveness_flow_ratio_modifier_curve_name: str | None
    primary_air_design_flow_rate: float | str | None
    recirculating_water_pump_design_power: float | str | None
    water_pump_power_sizing_factor: float | None
    water_pump_power_modifier_curve_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    sensor_node_name: str | None
    water_supply_storage_tank_name: str | None
    drift_loss_fraction: float | None
    blowdown_concentration_ratio: float | None
    evaporative_operation_minimum_drybulb_temperature: float | None
    evaporative_operation_maximum_limit_wetbulb_temperature: float | None
    evaporative_operation_maximum_limit_drybulb_temperature: float | None

class HumidifierSteamElectric(IDFObject):
    availability_schedule_name: str | None
    rated_capacity: float | str | None
    rated_power: float | str | None
    rated_fan_power: float | None
    standby_power: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    water_storage_tank_name: str | None

class HumidifierSteamGas(IDFObject):
    availability_schedule_name: str | None
    rated_capacity: float | str | None
    rated_gas_use_rate: float | str | None
    thermal_efficiency: float | None
    thermal_efficiency_modifier_curve_name: str | None
    rated_fan_power: float | None
    auxiliary_electric_power: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    water_storage_tank_name: str | None
    inlet_water_temperature_option: str | None

class DehumidifierDesiccantNoFans(IDFObject):
    availability_schedule_name: str | None
    process_air_inlet_node_name: str | None
    process_air_outlet_node_name: str | None
    regeneration_air_inlet_node_name: str | None
    regeneration_fan_inlet_node_name: str | None
    control_type: str | None
    leaving_maximum_humidity_ratio_setpoint: float | None
    nominal_process_air_flow_rate: float | None
    nominal_process_air_velocity: float | None
    rotor_power: float | None
    regeneration_coil_object_type: str | None
    regeneration_coil_name: str | None
    regeneration_fan_object_type: str | None
    regeneration_fan_name: str | None
    performance_model_type: str | None
    leaving_dry_bulb_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None
    leaving_dry_bulb_function_of_air_velocity_curve_name: str | None
    leaving_humidity_ratio_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None
    leaving_humidity_ratio_function_of_air_velocity_curve_name: str | None
    regeneration_energy_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None
    regeneration_energy_function_of_air_velocity_curve_name: str | None
    regeneration_velocity_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None
    regeneration_velocity_function_of_air_velocity_curve_name: str | None
    nominal_regeneration_temperature: float | None

class DehumidifierDesiccantSystem(IDFObject):
    availability_schedule_name: str | None
    desiccant_heat_exchanger_object_type: str | None
    desiccant_heat_exchanger_name: str | None
    sensor_node_name: str | None
    regeneration_air_fan_object_type: str | None
    regeneration_air_fan_name: str | None
    regeneration_air_fan_placement: str | None
    regeneration_air_heater_object_type: str | None
    regeneration_air_heater_name: str | None
    regeneration_inlet_air_setpoint_temperature: float | None
    companion_cooling_coil_object_type: str | None
    companion_cooling_coil_name: str | None
    companion_cooling_coil_upstream_of_dehumidifier_process_inlet: str | None
    companion_coil_regeneration_air_heating: str | None
    exhaust_fan_maximum_flow_rate: float | None
    exhaust_fan_maximum_power: float | None
    exhaust_fan_power_curve_name: str | None

class HeatExchangerAirToAirFlatPlate(IDFObject):
    availability_schedule_name: str | None
    flow_arrangement_type: str | None
    economizer_lockout: str | None
    ratio_of_supply_to_secondary_ha_values: float | None
    nominal_supply_air_flow_rate: float | str | None
    nominal_supply_air_inlet_temperature: float | None
    nominal_supply_air_outlet_temperature: float | None
    nominal_secondary_air_flow_rate: float | str | None
    nominal_secondary_air_inlet_temperature: float | None
    nominal_electric_power: float | None
    supply_air_inlet_node_name: str | None
    supply_air_outlet_node_name: str | None
    secondary_air_inlet_node_name: str | None
    secondary_air_outlet_node_name: str | None

class HeatExchangerAirToAirSensibleAndLatent(IDFObject):
    availability_schedule_name: str | None
    nominal_supply_air_flow_rate: float | str | None
    sensible_effectiveness_at_100_heating_air_flow: float | None
    latent_effectiveness_at_100_heating_air_flow: float | None
    sensible_effectiveness_at_100_cooling_air_flow: float | None
    latent_effectiveness_at_100_cooling_air_flow: float | None
    supply_air_inlet_node_name: str | None
    supply_air_outlet_node_name: str | None
    exhaust_air_inlet_node_name: str | None
    exhaust_air_outlet_node_name: str | None
    nominal_electric_power: float | None
    supply_air_outlet_temperature_control: str | None
    heat_exchanger_type: str | None
    frost_control_type: str | None
    threshold_temperature: float | None
    initial_defrost_time_fraction: float | None
    rate_of_defrost_time_fraction_increase: float | None
    economizer_lockout: str | None
    sensible_effectiveness_of_heating_air_flow_curve_name: str | None
    latent_effectiveness_of_heating_air_flow_curve_name: str | None
    sensible_effectiveness_of_cooling_air_flow_curve_name: str | None
    latent_effectiveness_of_cooling_air_flow_curve_name: str | None

class HeatExchangerDesiccantBalancedFlow(IDFObject):
    availability_schedule_name: str | None
    regeneration_air_inlet_node_name: str | None
    regeneration_air_outlet_node_name: str | None
    process_air_inlet_node_name: str | None
    process_air_outlet_node_name: str | None
    heat_exchanger_performance_object_type: str | None
    heat_exchanger_performance_name: str | None
    economizer_lockout: str | None

class HeatExchangerDesiccantBalancedFlowPerformanceDataType1(IDFObject):
    nominal_air_flow_rate: float | str | None
    nominal_air_face_velocity: float | str | None
    nominal_electric_power: float | None
    temperature_equation_coefficient_1: float | None
    temperature_equation_coefficient_2: float | None
    temperature_equation_coefficient_3: float | None
    temperature_equation_coefficient_4: float | None
    temperature_equation_coefficient_5: float | None
    temperature_equation_coefficient_6: float | None
    temperature_equation_coefficient_7: float | None
    temperature_equation_coefficient_8: float | None
    minimum_regeneration_inlet_air_humidity_ratio_for_temperature_equation: float | None
    maximum_regeneration_inlet_air_humidity_ratio_for_temperature_equation: float | None
    minimum_regeneration_inlet_air_temperature_for_temperature_equation: float | None
    maximum_regeneration_inlet_air_temperature_for_temperature_equation: float | None
    minimum_process_inlet_air_humidity_ratio_for_temperature_equation: float | None
    maximum_process_inlet_air_humidity_ratio_for_temperature_equation: float | None
    minimum_process_inlet_air_temperature_for_temperature_equation: float | None
    maximum_process_inlet_air_temperature_for_temperature_equation: float | None
    minimum_regeneration_air_velocity_for_temperature_equation: float | None
    maximum_regeneration_air_velocity_for_temperature_equation: float | None
    minimum_regeneration_outlet_air_temperature_for_temperature_equation: float | None
    maximum_regeneration_outlet_air_temperature_for_temperature_equation: float | None
    minimum_regeneration_inlet_air_relative_humidity_for_temperature_equation: float | None
    maximum_regeneration_inlet_air_relative_humidity_for_temperature_equation: float | None
    minimum_process_inlet_air_relative_humidity_for_temperature_equation: float | None
    maximum_process_inlet_air_relative_humidity_for_temperature_equation: float | None
    humidity_ratio_equation_coefficient_1: float | None
    humidity_ratio_equation_coefficient_2: float | None
    humidity_ratio_equation_coefficient_3: float | None
    humidity_ratio_equation_coefficient_4: float | None
    humidity_ratio_equation_coefficient_5: float | None
    humidity_ratio_equation_coefficient_6: float | None
    humidity_ratio_equation_coefficient_7: float | None
    humidity_ratio_equation_coefficient_8: float | None
    minimum_regeneration_inlet_air_humidity_ratio_for_humidity_ratio_equation: float | None
    maximum_regeneration_inlet_air_humidity_ratio_for_humidity_ratio_equation: float | None
    minimum_regeneration_inlet_air_temperature_for_humidity_ratio_equation: float | None
    maximum_regeneration_inlet_air_temperature_for_humidity_ratio_equation: float | None
    minimum_process_inlet_air_humidity_ratio_for_humidity_ratio_equation: float | None
    maximum_process_inlet_air_humidity_ratio_for_humidity_ratio_equation: float | None
    minimum_process_inlet_air_temperature_for_humidity_ratio_equation: float | None
    maximum_process_inlet_air_temperature_for_humidity_ratio_equation: float | None
    minimum_regeneration_air_velocity_for_humidity_ratio_equation: float | None
    maximum_regeneration_air_velocity_for_humidity_ratio_equation: float | None
    minimum_regeneration_outlet_air_humidity_ratio_for_humidity_ratio_equation: float | None
    maximum_regeneration_outlet_air_humidity_ratio_for_humidity_ratio_equation: float | None
    minimum_regeneration_inlet_air_relative_humidity_for_humidity_ratio_equation: float | None
    maximum_regeneration_inlet_air_relative_humidity_for_humidity_ratio_equation: float | None
    minimum_process_inlet_air_relative_humidity_for_humidity_ratio_equation: float | None
    maximum_process_inlet_air_relative_humidity_for_humidity_ratio_equation: float | None

class AirLoopHVACUnitarySystem(IDFObject):
    control_type: str | None
    controlling_zone_or_thermostat_location: str | None
    dehumidification_control_type: str | None
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    supply_fan_object_type: str | None
    supply_fan_name: str | None
    fan_placement: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    dx_heating_coil_sizing_ratio: float | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    use_doas_dx_cooling_coil: str | None
    minimum_supply_air_temperature: float | str | None
    latent_load_control: str | None
    supplemental_heating_coil_object_type: str | None
    supplemental_heating_coil_name: str | None
    cooling_supply_air_flow_rate_method: str | None
    cooling_supply_air_flow_rate: float | str | None
    cooling_supply_air_flow_rate_per_floor_area: float | None
    cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None
    cooling_supply_air_flow_rate_per_unit_of_capacity: float | None
    heating_supply_air_flow_rate_method: str | None
    heating_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate_per_floor_area: float | None
    heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None
    heating_supply_air_flow_rate_per_unit_of_capacity: float | None
    no_load_supply_air_flow_rate_method: str | None
    no_load_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate_per_floor_area: float | None
    no_load_fraction_of_autosized_cooling_supply_air_flow_rate: float | None
    no_load_fraction_of_autosized_heating_supply_air_flow_rate: float | None
    no_load_supply_air_flow_rate_per_unit_of_capacity_during_cooling_operation: float | None
    no_load_supply_air_flow_rate_per_unit_of_capacity_during_heating_operation: float | None
    no_load_supply_air_flow_rate_control_set_to_low_speed: str | None
    maximum_supply_air_temperature: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None
    outdoor_dry_bulb_temperature_sensor_node_name: str | None
    ancillary_on_cycle_electric_power: float | None
    ancillary_off_cycle_electric_power: float | None
    design_heat_recovery_water_flow_rate: float | None
    maximum_temperature_for_heat_recovery: float | None
    heat_recovery_water_inlet_node_name: str | None
    heat_recovery_water_outlet_node_name: str | None
    design_specification_multispeed_object_type: str | None
    design_specification_multispeed_object_name: str | None

class UnitarySystemPerformanceMultispeed(IDFObject):
    number_of_speeds_for_heating: int | None
    number_of_speeds_for_cooling: int | None
    single_mode_operation: str | None
    no_load_supply_air_flow_rate_ratio: float | None
    heating_speed_supply_air_flow_ratio: float | None
    cooling_speed_supply_air_flow_ratio: float | None

class AirLoopHVACUnitaryFurnaceHeatOnly(IDFObject):
    availability_schedule_name: str | None
    furnace_air_inlet_node_name: str | None
    furnace_air_outlet_node_name: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    maximum_supply_air_temperature: float | str | None
    heating_supply_air_flow_rate: float | str | None
    controlling_zone_or_thermostat_location: str | None
    supply_fan_object_type: str | None
    supply_fan_name: str | None
    fan_placement: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None

class AirLoopHVACUnitaryFurnaceHeatCool(IDFObject):
    availability_schedule_name: str | None
    furnace_air_inlet_node_name: str | None
    furnace_air_outlet_node_name: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    maximum_supply_air_temperature: float | str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    controlling_zone_or_thermostat_location: str | None
    supply_fan_object_type: str | None
    supply_fan_name: str | None
    fan_placement: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    dehumidification_control_type: str | None
    reheat_coil_object_type: str | None
    reheat_coil_name: str | None

class AirLoopHVACUnitaryHeatOnly(IDFObject):
    availability_schedule_name: str | None
    unitary_system_air_inlet_node_name: str | None
    unitary_system_air_outlet_node_name: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    maximum_supply_air_temperature: float | str | None
    heating_supply_air_flow_rate: float | str | None
    controlling_zone_or_thermostat_location: str | None
    supply_fan_object_type: str | None
    supply_fan_name: str | None
    fan_placement: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None

class AirLoopHVACUnitaryHeatCool(IDFObject):
    availability_schedule_name: str | None
    unitary_system_air_inlet_node_name: str | None
    unitary_system_air_outlet_node_name: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    maximum_supply_air_temperature: float | str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    controlling_zone_or_thermostat_location: str | None
    supply_fan_object_type: str | None
    supply_fan_name: str | None
    fan_placement: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    dehumidification_control_type: str | None
    reheat_coil_object_type: str | None
    reheat_coil_name: str | None

class AirLoopHVACUnitaryHeatPumpAirToAir(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    controlling_zone_or_thermostat_location: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    supplemental_heating_coil_object_type: str | None
    supplemental_heating_coil_name: str | None
    maximum_supply_air_temperature_from_supplemental_heater: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None
    fan_placement: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    dehumidification_control_type: str | None
    dx_heating_coil_sizing_ratio: float | None

class AirLoopHVACUnitaryHeatPumpWaterToAir(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    supply_air_flow_rate: float | str | None
    controlling_zone_or_thermostat_location: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    heating_convergence: float | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    cooling_convergence: float | None
    supplemental_heating_coil_object_type: str | None
    supplemental_heating_coil_name: str | None
    maximum_supply_air_temperature_from_supplemental_heater: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None
    outdoor_dry_bulb_temperature_sensor_node_name: str | None
    fan_placement: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    dehumidification_control_type: str | None
    heat_pump_coil_water_flow_mode: str | None
    dx_heating_coil_sizing_ratio: float | None

class AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass(IDFObject):
    availability_schedule_name: str | None
    cooling_supply_air_flow_rate: float | str | None
    heating_supply_air_flow_rate: float | str | None
    no_load_supply_air_flow_rate: float | str | None
    cooling_outdoor_air_flow_rate: float | str | None
    heating_outdoor_air_flow_rate: float | str | None
    no_load_outdoor_air_flow_rate: float | str | None
    outdoor_air_flow_rate_multiplier_schedule_name: str | None
    air_inlet_node_name: str | None
    bypass_duct_mixer_node_name: str | None
    bypass_duct_splitter_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_mixer_object_type: str | None
    outdoor_air_mixer_name: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    supply_air_fan_placement: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    priority_control_mode: str | None
    minimum_outlet_air_temperature_during_cooling_operation: float | None
    maximum_outlet_air_temperature_during_heating_operation: float | None
    dehumidification_control_type: str | None
    plenum_or_mixer_inlet_node_name: str | None
    minimum_runtime_before_operating_mode_change: float | None

class AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed(IDFObject):
    availability_schedule_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    controlling_zone_or_thermostat_location: str | None
    supply_air_fan_object_type: str | None
    supply_air_fan_name: str | None
    supply_air_fan_placement: str | None
    supply_air_fan_operating_mode_schedule_name: str | None
    heating_coil_object_type: str | None
    heating_coil_name: str | None
    dx_heating_coil_sizing_ratio: float | None
    cooling_coil_object_type: str | None
    cooling_coil_name: str | None
    supplemental_heating_coil_object_type: str | None
    supplemental_heating_coil_name: str | None
    maximum_supply_air_temperature_from_supplemental_heater: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None
    auxiliary_on_cycle_electric_power: float | None
    auxiliary_off_cycle_electric_power: float | None
    design_heat_recovery_water_flow_rate: float | None
    maximum_temperature_for_heat_recovery: float | None
    heat_recovery_water_inlet_node_name: str | None
    heat_recovery_water_outlet_node_name: str | None
    no_load_supply_air_flow_rate: float | str | None
    number_of_speeds_for_heating: int | None
    number_of_speeds_for_cooling: int | None
    heating_speed_1_supply_air_flow_rate: float | str | None
    heating_speed_2_supply_air_flow_rate: float | str | None
    heating_speed_3_supply_air_flow_rate: float | str | None
    heating_speed_4_supply_air_flow_rate: float | str | None
    cooling_speed_1_supply_air_flow_rate: float | str | None
    cooling_speed_2_supply_air_flow_rate: float | str | None
    cooling_speed_3_supply_air_flow_rate: float | str | None
    cooling_speed_4_supply_air_flow_rate: float | str | None

class AirConditionerVariableRefrigerantFlow(IDFObject):
    availability_schedule_name: str | None
    gross_rated_total_cooling_capacity: float | str | None
    gross_rated_cooling_cop: float | None
    minimum_condenser_inlet_node_temperature_in_cooling_mode: float | None
    maximum_condenser_inlet_node_temperature_in_cooling_mode: float | None
    cooling_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None
    cooling_capacity_ratio_boundary_curve_name: str | None
    cooling_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None
    cooling_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None
    cooling_energy_input_ratio_boundary_curve_name: str | None
    cooling_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None
    cooling_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None
    cooling_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None
    cooling_combination_ratio_correction_factor_curve_name: str | None
    cooling_part_load_fraction_correlation_curve_name: str | None
    gross_rated_heating_capacity: float | str | None
    rated_heating_capacity_sizing_ratio: float | None
    gross_rated_heating_cop: float | None
    minimum_condenser_inlet_node_temperature_in_heating_mode: float | None
    maximum_condenser_inlet_node_temperature_in_heating_mode: float | None
    heating_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None
    heating_capacity_ratio_boundary_curve_name: str | None
    heating_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None
    heating_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None
    heating_energy_input_ratio_boundary_curve_name: str | None
    heating_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None
    heating_performance_curve_outdoor_temperature_type: str | None
    heating_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None
    heating_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None
    heating_combination_ratio_correction_factor_curve_name: str | None
    heating_part_load_fraction_correlation_curve_name: str | None
    minimum_heat_pump_part_load_ratio: float | None
    zone_name_for_master_thermostat_location: str | None
    master_thermostat_priority_control_type: str | None
    thermostat_priority_schedule_name: str | None
    zone_terminal_unit_list_name: str | None
    heat_pump_waste_heat_recovery: str | None
    equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None
    vertical_height_used_for_piping_correction_factor: float | None
    piping_correction_factor_for_length_in_cooling_mode_curve_name: str | None
    piping_correction_factor_for_height_in_cooling_mode_coefficient: float | None
    equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None
    piping_correction_factor_for_length_in_heating_mode_curve_name: str | None
    piping_correction_factor_for_height_in_heating_mode_coefficient: float | None
    crankcase_heater_power_per_compressor: float | None
    number_of_compressors: int | None
    ratio_of_compressor_size_to_total_compressor_capacity: float | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None
    defrost_strategy: str | None
    defrost_control: str | None
    defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None
    defrost_time_period_fraction: float | None
    resistive_defrost_heater_capacity: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    condenser_type: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    water_condenser_volume_flow_rate: float | str | None
    evaporative_condenser_effectiveness: float | None
    evaporative_condenser_air_flow_rate: float | str | None
    evaporative_condenser_pump_rated_power_consumption: float | str | None
    supply_water_storage_tank_name: str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    fuel_type: str | None
    minimum_condenser_inlet_node_temperature_in_heat_recovery_mode: float | None
    maximum_condenser_inlet_node_temperature_in_heat_recovery_mode: float | None
    heat_recovery_cooling_capacity_modifier_curve_name: str | None
    initial_heat_recovery_cooling_capacity_fraction: float | None
    heat_recovery_cooling_capacity_time_constant: float | None
    heat_recovery_cooling_energy_modifier_curve_name: str | None
    initial_heat_recovery_cooling_energy_fraction: float | None
    heat_recovery_cooling_energy_time_constant: float | None
    heat_recovery_heating_capacity_modifier_curve_name: str | None
    initial_heat_recovery_heating_capacity_fraction: float | None
    heat_recovery_heating_capacity_time_constant: float | None
    heat_recovery_heating_energy_modifier_curve_name: str | None
    initial_heat_recovery_heating_energy_fraction: float | None
    heat_recovery_heating_energy_time_constant: float | None

class AirConditionerVariableRefrigerantFlowFluidTemperatureControl(IDFObject):
    availability_schedule_name: str | None
    zone_terminal_unit_list_name: str | None
    refrigerant_type: str | None
    rated_evaporative_capacity: float | str | None
    rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None
    minimum_outdoor_air_temperature_in_cooling_mode: float | None
    maximum_outdoor_air_temperature_in_cooling_mode: float | None
    minimum_outdoor_air_temperature_in_heating_mode: float | None
    maximum_outdoor_air_temperature_in_heating_mode: float | None
    reference_outdoor_unit_superheating: float | None
    reference_outdoor_unit_subcooling: float | None
    refrigerant_temperature_control_algorithm_for_indoor_unit: str | None
    reference_evaporating_temperature_for_indoor_unit: float | None
    reference_condensing_temperature_for_indoor_unit: float | None
    variable_evaporating_temperature_minimum_for_indoor_unit: float | None
    variable_evaporating_temperature_maximum_for_indoor_unit: float | None
    variable_condensing_temperature_minimum_for_indoor_unit: float | None
    variable_condensing_temperature_maximum_for_indoor_unit: float | None
    outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None
    outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None
    outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str | None
    outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str | None
    diameter_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None
    length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None
    equivalent_length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None
    height_difference_between_outdoor_unit_and_indoor_units: float | None
    main_pipe_insulation_thickness: float | None
    main_pipe_insulation_thermal_conductivity: float | None
    crankcase_heater_power_per_compressor: float | None
    number_of_compressors: int | None
    ratio_of_compressor_size_to_total_compressor_capacity: float | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None
    defrost_strategy: str | None
    defrost_control: str | None
    defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None
    defrost_time_period_fraction: float | None
    resistive_defrost_heater_capacity: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    compressor_maximum_delta_pressure: float | None
    number_of_compressor_loading_index_entries: int | None
    compressor_speed_at_loading_index: float | None
    loading_index_evaporative_capacity_multiplier_function_of_temperature_curve_name: str | None
    loading_index_compressor_power_multiplier_function_of_temperature_curve_name: str | None

class AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR(IDFObject):
    availability_schedule_name: str | None
    zone_terminal_unit_list_name: str | None
    refrigerant_type: str | None
    rated_evaporative_capacity: float | str | None
    rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None
    minimum_outdoor_air_temperature_in_cooling_only_mode: float | None
    maximum_outdoor_air_temperature_in_cooling_only_mode: float | None
    minimum_outdoor_air_temperature_in_heating_only_mode: float | None
    maximum_outdoor_air_temperature_in_heating_only_mode: float | None
    minimum_outdoor_temperature_in_heat_recovery_mode: float | None
    maximum_outdoor_temperature_in_heat_recovery_mode: float | None
    refrigerant_temperature_control_algorithm_for_indoor_unit: str | None
    reference_evaporating_temperature_for_indoor_unit: float | None
    reference_condensing_temperature_for_indoor_unit: float | None
    variable_evaporating_temperature_minimum_for_indoor_unit: float | None
    variable_evaporating_temperature_maximum_for_indoor_unit: float | None
    variable_condensing_temperature_minimum_for_indoor_unit: float | None
    variable_condensing_temperature_maximum_for_indoor_unit: float | None
    outdoor_unit_evaporator_reference_superheating: float | None
    outdoor_unit_condenser_reference_subcooling: float | None
    outdoor_unit_evaporator_rated_bypass_factor: float | None
    outdoor_unit_condenser_rated_bypass_factor: float | None
    difference_between_outdoor_unit_evaporating_temperature_and_outdoor_air_temperature_in_heat_recovery_mode: (
        float | None
    )
    outdoor_unit_heat_exchanger_capacity_ratio: float | None
    outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None
    outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None
    outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str | None
    outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str | None
    diameter_of_main_pipe_for_suction_gas: float | None
    diameter_of_main_pipe_for_discharge_gas: float | None
    length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None
    equivalent_length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None
    height_difference_between_outdoor_unit_and_indoor_units: float | None
    main_pipe_insulation_thickness: float | None
    main_pipe_insulation_thermal_conductivity: float | None
    crankcase_heater_power_per_compressor: float | None
    number_of_compressors: int | None
    ratio_of_compressor_size_to_total_compressor_capacity: float | None
    maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None
    defrost_strategy: str | None
    defrost_control: str | None
    defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None
    defrost_time_period_fraction: float | None
    resistive_defrost_heater_capacity: float | str | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    initial_heat_recovery_cooling_capacity_fraction: float | None
    heat_recovery_cooling_capacity_time_constant: float | None
    initial_heat_recovery_cooling_energy_fraction: float | None
    heat_recovery_cooling_energy_time_constant: float | None
    initial_heat_recovery_heating_capacity_fraction: float | None
    heat_recovery_heating_capacity_time_constant: float | None
    initial_heat_recovery_heating_energy_fraction: float | None
    heat_recovery_heating_energy_time_constant: float | None
    compressor_maximum_delta_pressure: float | None
    compressor_inverter_efficiency: float | None
    compressor_evaporative_capacity_correction_factor: float | None
    number_of_compressor_loading_index_entries: int | None
    compressor_speed_at_loading_index: float | None
    loading_index_evaporative_capacity_multiplier_function_of_temperature_curve_name: str | None
    loading_index_compressor_power_multiplier_function_of_temperature_curve_name: str | None

class ZoneTerminalUnitList(IDFObject):
    zone_terminal_unit_name: str | None

class ControllerWaterCoil(IDFObject):
    control_variable: str | None
    action: str | None
    actuator_variable: str | None
    sensor_node_name: str | None
    actuator_node_name: str | None
    controller_convergence_tolerance: float | str | None
    maximum_actuated_flow: float | str | None
    minimum_actuated_flow: float | None

class ControllerOutdoorAir(IDFObject):
    relief_air_outlet_node_name: str | None
    return_air_node_name: str | None
    mixed_air_node_name: str | None
    actuator_node_name: str | None
    minimum_outdoor_air_flow_rate: float | str | None
    maximum_outdoor_air_flow_rate: float | str | None
    economizer_control_type: str | None
    economizer_control_action_type: str | None
    economizer_maximum_limit_dry_bulb_temperature: float | None
    economizer_maximum_limit_enthalpy: float | None
    economizer_maximum_limit_dewpoint_temperature: float | None
    electronic_enthalpy_limit_curve_name: str | None
    economizer_minimum_limit_dry_bulb_temperature: float | None
    lockout_type: str | None
    minimum_limit_type: str | None
    minimum_outdoor_air_schedule_name: str | None
    minimum_fraction_of_outdoor_air_schedule_name: str | None
    maximum_fraction_of_outdoor_air_schedule_name: str | None
    mechanical_ventilation_controller_name: str | None
    time_of_day_economizer_control_schedule_name: str | None
    high_humidity_control: str | None
    humidistat_control_zone_name: str | None
    high_humidity_outdoor_air_flow_ratio: float | None
    control_high_indoor_humidity_based_on_outdoor_humidity_ratio: str | None
    heat_recovery_bypass_control_type: str | None
    economizer_operation_staging: str | None

class ControllerMechanicalVentilation(IDFObject):
    availability_schedule_name: str | None
    demand_controlled_ventilation: str | None
    system_outdoor_air_method: str | None
    zone_maximum_outdoor_air_fraction: float | None
    zone_or_zonelist_name: str | None
    design_specification_outdoor_air_object_name: str | None
    design_specification_zone_air_distribution_object_name: str | None

class AirLoopHVACControllerList(IDFObject):
    controller_1_object_type: str | None
    controller_1_name: str | None
    controller_2_object_type: str | None
    controller_2_name: str | None
    controller_3_object_type: str | None
    controller_3_name: str | None
    controller_4_object_type: str | None
    controller_4_name: str | None
    controller_5_object_type: str | None
    controller_5_name: str | None
    controller_6_object_type: str | None
    controller_6_name: str | None
    controller_7_object_type: str | None
    controller_7_name: str | None
    controller_8_object_type: str | None
    controller_8_name: str | None

class AirLoopHVAC(IDFObject):
    controller_list_name: str | None
    availability_manager_list_name: str | None
    design_supply_air_flow_rate: float | str | None
    branch_list_name: str | None
    connector_list_name: str | None
    supply_side_inlet_node_name: str | None
    demand_side_outlet_node_name: str | None
    demand_side_inlet_node_names: str | None
    supply_side_outlet_node_names: str | None
    design_return_air_flow_fraction_of_supply_air_flow: float | None

class AirLoopHVACOutdoorAirSystemEquipmentList(IDFObject):
    component_1_object_type: str | None
    component_1_name: str | None
    component_2_object_type: str | None
    component_2_name: str | None
    component_3_object_type: str | None
    component_3_name: str | None
    component_4_object_type: str | None
    component_4_name: str | None
    component_5_object_type: str | None
    component_5_name: str | None
    component_6_object_type: str | None
    component_6_name: str | None
    component_7_object_type: str | None
    component_7_name: str | None
    component_8_object_type: str | None
    component_8_name: str | None
    component_9_object_type: str | None
    component_9_name: str | None

class AirLoopHVACOutdoorAirSystem(IDFObject):
    controller_list_name: str | None
    outdoor_air_equipment_list_name: str | None

class OutdoorAirMixer(IDFObject):
    mixed_air_node_name: str | None
    outdoor_air_stream_node_name: str | None
    relief_air_stream_node_name: str | None
    return_air_stream_node_name: str | None

class AirLoopHVACZoneSplitter(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None

class AirLoopHVACSupplyPlenum(IDFObject):
    zone_name: str | None
    zone_node_name: str | None
    inlet_node_name: str | None
    outlet_node_name: str | None

class AirLoopHVACSupplyPath(IDFObject):
    supply_air_path_inlet_node_name: str | None
    component_object_type: str | None
    component_name: str | None

class AirLoopHVACZoneMixer(IDFObject):
    outlet_node_name: str | None
    inlet_node_name: str | None

class AirLoopHVACReturnPlenum(IDFObject):
    zone_name: str | None
    zone_node_name: str | None
    outlet_node_name: str | None
    induced_air_outlet_node_or_nodelist_name: str | None
    inlet_node_name: str | None

class AirLoopHVACReturnPath(IDFObject):
    return_air_path_outlet_node_name: str | None
    component_object_type: str | None
    component_name: str | None

class AirLoopHVACExhaustSystem(IDFObject):
    zone_mixer_name: str | None
    fan_object_type: str | None
    fan_name: str | None

class AirLoopHVACDedicatedOutdoorAirSystem(IDFObject):
    airloophvac_outdoorairsystem_name: str | None
    availability_schedule_name: str | None
    airloophvac_mixer_name: str | None
    airloophvac_splitter_name: str | None
    preheat_design_temperature: float | None
    preheat_design_humidity_ratio: float | None
    precool_design_temperature: float | None
    precool_design_humidity_ratio: float | None
    number_of_airloophvac: int | None
    airloophvac_name: str | None

class AirLoopHVACMixer(IDFObject):
    outlet_node_name: str | None
    inlet_node_name: str | None

class AirLoopHVACSplitter(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None

class Branch(IDFObject):
    pressure_drop_curve_name: str | None
    component_object_type: str | None
    component_name: str | None
    component_inlet_node_name: str | None
    component_outlet_node_name: str | None

class BranchList(IDFObject):
    branch_name: str | None

class ConnectorSplitter(IDFObject):
    inlet_branch_name: str | None
    outlet_branch_name: str | None

class ConnectorMixer(IDFObject):
    outlet_branch_name: str | None
    inlet_branch_name: str | None

class ConnectorList(IDFObject):
    connector_1_object_type: str | None
    connector_1_name: str | None
    connector_2_object_type: str | None
    connector_2_name: str | None

class NodeList(IDFObject):
    node_name: str | None

class OutdoorAirNode(IDFObject):
    height_above_ground: float | None
    drybulb_temperature_schedule_name: str | None
    wetbulb_temperature_schedule_name: str | None
    wind_speed_schedule_name: str | None
    wind_direction_schedule_name: str | None
    wind_pressure_coefficient_curve_name: str | None
    symmetric_wind_pressure_coefficient_curve: str | None
    wind_angle_type: str | None

class OutdoorAirNodeList(IDFObject):
    node_or_nodelist_name: str | None

class PipeAdiabatic(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None

class PipeAdiabaticSteam(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None

class PipeIndoor(IDFObject):
    construction_name: str | None
    fluid_inlet_node_name: str | None
    fluid_outlet_node_name: str | None
    environment_type: str | None
    ambient_temperature_zone_name: str | None
    ambient_temperature_schedule_name: str | None
    ambient_air_velocity_schedule_name: str | None
    pipe_inside_diameter: float | None
    pipe_length: float | None

class PipeOutdoor(IDFObject):
    construction_name: str | None
    fluid_inlet_node_name: str | None
    fluid_outlet_node_name: str | None
    ambient_temperature_outdoor_air_node_name: str | None
    pipe_inside_diameter: float | None
    pipe_length: float | None

class PipeUnderground(IDFObject):
    construction_name: str | None
    fluid_inlet_node_name: str | None
    fluid_outlet_node_name: str | None
    sun_exposure: str | None
    pipe_inside_diameter: float | None
    pipe_length: float | None
    soil_material_name: str | None
    undisturbed_ground_temperature_model_type: str | None
    undisturbed_ground_temperature_model_name: str | None

class PipingSystemUndergroundDomain(IDFObject):
    xmax: float | None
    ymax: float | None
    zmax: float | None
    x_direction_mesh_density_parameter: int | None
    x_direction_mesh_type: str | None
    x_direction_geometric_coefficient: float | None
    y_direction_mesh_density_parameter: int | None
    y_direction_mesh_type: str | None
    y_direction_geometric_coefficient: float | None
    z_direction_mesh_density_parameter: int | None
    z_direction_mesh_type: str | None
    z_direction_geometric_coefficient: float | None
    soil_thermal_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    soil_moisture_content_volume_fraction: float | None
    soil_moisture_content_volume_fraction_at_saturation: float | None
    undisturbed_ground_temperature_model_type: str | None
    undisturbed_ground_temperature_model_name: str | None
    this_domain_includes_basement_surface_interaction: str | None
    width_of_basement_floor_in_ground_domain: float | None
    depth_of_basement_wall_in_ground_domain: float | None
    shift_pipe_x_coordinates_by_basement_width: str | None
    name_of_basement_wall_boundary_condition_model: str | None
    name_of_basement_floor_boundary_condition_model: str | None
    convergence_criterion_for_the_outer_cartesian_domain_iteration_loop: float | None
    maximum_iterations_in_the_outer_cartesian_domain_iteration_loop: int | None
    evapotranspiration_ground_cover_parameter: float | None
    number_of_pipe_circuits_entered_for_this_domain: int | None
    pipe_circuit: str | None

class PipingSystemUndergroundPipeCircuit(IDFObject):
    pipe_thermal_conductivity: float | None
    pipe_density: float | None
    pipe_specific_heat: float | None
    pipe_inner_diameter: float | None
    pipe_outer_diameter: float | None
    design_flow_rate: float | None
    circuit_inlet_node: str | None
    circuit_outlet_node: str | None
    convergence_criterion_for_the_inner_radial_iteration_loop: float | None
    maximum_iterations_in_the_inner_radial_iteration_loop: int | None
    number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region: int | None
    radial_thickness_of_inner_radial_near_pipe_mesh_region: float | None
    number_of_pipe_segments_entered_for_this_pipe_circuit: int | None
    pipe_segment: str | None

class PipingSystemUndergroundPipeSegment(IDFObject):
    x_position: float | None
    y_position: float | None
    flow_direction: str | None

class Duct(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None

class PumpVariableSpeed(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    design_maximum_flow_rate: float | str | None
    design_pump_head: float | None
    design_power_consumption: float | str | None
    motor_efficiency: float | None
    fraction_of_motor_inefficiencies_to_fluid_stream: float | None
    coefficient_1_of_the_part_load_performance_curve: float | None
    coefficient_2_of_the_part_load_performance_curve: float | None
    coefficient_3_of_the_part_load_performance_curve: float | None
    coefficient_4_of_the_part_load_performance_curve: float | None
    design_minimum_flow_rate: float | str | None
    pump_control_type: str | None
    pump_flow_rate_schedule_name: str | None
    pump_curve_name: str | None
    impeller_diameter: float | None
    vfd_control_type: str | None
    pump_rpm_schedule_name: str | None
    minimum_pressure_schedule: str | None
    maximum_pressure_schedule: str | None
    minimum_rpm_schedule: str | None
    maximum_rpm_schedule: str | None
    zone_name: str | None
    skin_loss_radiative_fraction: float | None
    design_power_sizing_method: str | None
    design_electric_power_per_unit_flow_rate: float | None
    design_shaft_power_per_unit_flow_rate_per_unit_head: float | None
    design_minimum_flow_rate_fraction: float | None
    end_use_subcategory: str | None

class PumpConstantSpeed(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    design_flow_rate: float | str | None
    design_pump_head: float | None
    design_power_consumption: float | str | None
    motor_efficiency: float | None
    fraction_of_motor_inefficiencies_to_fluid_stream: float | None
    pump_control_type: str | None
    pump_flow_rate_schedule_name: str | None
    pump_curve_name: str | None
    impeller_diameter: float | None
    rotational_speed: float | None
    zone_name: str | None
    skin_loss_radiative_fraction: float | None
    design_power_sizing_method: str | None
    design_electric_power_per_unit_flow_rate: float | None
    design_shaft_power_per_unit_flow_rate_per_unit_head: float | None
    end_use_subcategory: str | None

class PumpVariableSpeedCondensate(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    design_steam_volume_flow_rate: float | str | None
    design_pump_head: float | None
    design_power_consumption: float | str | None
    motor_efficiency: float | None
    fraction_of_motor_inefficiencies_to_fluid_stream: float | None
    coefficient_1_of_the_part_load_performance_curve: float | None
    coefficient_2_of_the_part_load_performance_curve: float | None
    coefficient_3_of_the_part_load_performance_curve: float | None
    coefficient_4_of_the_part_load_performance_curve: float | None
    pump_flow_rate_schedule_name: str | None
    zone_name: str | None
    skin_loss_radiative_fraction: float | None
    design_power_sizing_method: str | None
    design_electric_power_per_unit_flow_rate: float | None
    design_shaft_power_per_unit_flow_rate_per_unit_head: float | None
    end_use_subcategory: str | None

class HeaderedPumpsConstantSpeed(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    total_design_flow_rate: float | str | None
    number_of_pumps_in_bank: int | None
    flow_sequencing_control_scheme: str | None
    design_pump_head: float | None
    design_power_consumption: float | str | None
    motor_efficiency: float | None
    fraction_of_motor_inefficiencies_to_fluid_stream: float | None
    pump_control_type: str | None
    pump_flow_rate_schedule_name: str | None
    zone_name: str | None
    skin_loss_radiative_fraction: float | None
    design_power_sizing_method: str | None
    design_electric_power_per_unit_flow_rate: float | None
    design_shaft_power_per_unit_flow_rate_per_unit_head: float | None
    end_use_subcategory: str | None

class HeaderedPumpsVariableSpeed(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    total_design_flow_rate: float | str | None
    number_of_pumps_in_bank: int | None
    flow_sequencing_control_scheme: str | None
    design_pump_head: float | None
    design_power_consumption: float | str | None
    motor_efficiency: float | None
    fraction_of_motor_inefficiencies_to_fluid_stream: float | None
    coefficient_1_of_the_part_load_performance_curve: float | None
    coefficient_2_of_the_part_load_performance_curve: float | None
    coefficient_3_of_the_part_load_performance_curve: float | None
    coefficient_4_of_the_part_load_performance_curve: float | None
    minimum_flow_rate_fraction: float | None
    pump_control_type: str | None
    pump_flow_rate_schedule_name: str | None
    zone_name: str | None
    skin_loss_radiative_fraction: float | None
    design_power_sizing_method: str | None
    design_electric_power_per_unit_flow_rate: float | None
    design_shaft_power_per_unit_flow_rate_per_unit_head: float | None
    end_use_subcategory: str | None

class TemperingValve(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    stream_2_source_node_name: str | None
    temperature_setpoint_node_name: str | None
    pump_outlet_node_name: str | None

class LoadProfilePlant(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    load_schedule_name: str | None
    peak_flow_rate: float | None
    flow_rate_fraction_schedule_name: str | None
    plant_loop_fluid_type: str | None
    degree_of_subcooling: float | None
    degree_of_loop_subcooling: float | None

class SolarCollectorPerformanceFlatPlate(IDFObject):
    gross_area: float | None
    test_fluid: str | None
    test_flow_rate: float | None
    test_correlation_type: str | None
    coefficient_1_of_efficiency_equation: float | None
    coefficient_2_of_efficiency_equation: float | None
    coefficient_3_of_efficiency_equation: float | None
    coefficient_2_of_incident_angle_modifier: float | None
    coefficient_3_of_incident_angle_modifier: float | None

class SolarCollectorFlatPlateWater(IDFObject):
    solarcollectorperformance_name: str | None
    surface_name: str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    maximum_flow_rate: float | None

class SolarCollectorFlatPlatePhotovoltaicThermal(IDFObject):
    surface_name: str | None
    photovoltaic_thermal_model_performance_name: str | None
    photovoltaic_name: str | None
    thermal_working_fluid_type: str | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    design_flow_rate: float | str | None

class SolarCollectorPerformancePhotovoltaicThermalSimple(IDFObject):
    fraction_of_surface_area_with_active_thermal_collector: float | None
    thermal_conversion_efficiency_input_mode_type: str | None
    value_for_thermal_conversion_efficiency_if_fixed: float | None
    thermal_conversion_efficiency_schedule_name: str | None
    front_surface_emittance: float | None

class SolarCollectorPerformancePhotovoltaicThermalBIPVT(IDFObject):
    boundary_conditions_model_name: str | None
    availability_schedule_name: str | None
    effective_plenum_gap_thickness_behind_pv_modules: float | None
    pv_cell_normal_transmittance_absorptance_product: float | None
    backing_material_normal_transmittance_absorptance_product: float | None
    cladding_normal_transmittance_absorptance_product: float | None
    fraction_of_collector_gross_area_covered_by_pv_module: float | None
    fraction_of_pv_cell_area_to_pv_module_area: float | None
    pv_module_top_thermal_resistance: float | None
    pv_module_bottom_thermal_resistance: float | None
    pv_module_front_longwave_emissivity: float | None
    pv_module_back_longwave_emissivity: float | None
    glass_thickness: float | None
    glass_refraction_index: float | None
    glass_extinction_coefficient: float | None

class SolarCollectorIntegralCollectorStorage(IDFObject):
    integralcollectorstorageparameters_name: str | None
    surface_name: str | None
    bottom_surface_boundary_conditions_type: str | None
    boundary_condition_model_name: str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    maximum_flow_rate: float | None

class SolarCollectorPerformanceIntegralCollectorStorage(IDFObject):
    ics_collector_type: str | None
    gross_area: float | None
    collector_water_volume: float | None
    bottom_heat_loss_conductance: float | None
    side_heat_loss_conductance: float | None
    aspect_ratio: float | None
    collector_side_height: float | None
    thermal_mass_of_absorber_plate: float | None
    number_of_covers: int | None
    cover_spacing: float | None
    refractive_index_of_outer_cover: float | None
    extinction_coefficient_times_thickness_of_outer_cover: float | None
    emissivity_of_outer_cover: float | None
    refractive_index_of_inner_cover: float | None
    extinction_coefficient_times_thickness_of_the_inner_cover: float | None
    emissivity_of_inner_cover: float | None
    absorptance_of_absorber_plate: float | None
    emissivity_of_absorber_plate: float | None

class SolarCollectorUnglazedTranspired(IDFObject):
    boundary_conditions_model_name: str | None
    availability_schedule_name: str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    setpoint_node_name: str | None
    zone_node_name: str | None
    free_heating_setpoint_schedule_name: str | None
    diameter_of_perforations_in_collector: float | None
    distance_between_perforations_in_collector: float | None
    thermal_emissivity_of_collector_surface: float | None
    solar_absorbtivity_of_collector_surface: float | None
    effective_overall_height_of_collector: float | None
    effective_gap_thickness_of_plenum_behind_collector: float | None
    effective_cross_section_area_of_plenum_behind_collector: float | None
    hole_layout_pattern_for_pitch: str | None
    heat_exchange_effectiveness_correlation: str | None
    ratio_of_actual_collector_surface_area_to_projected_surface_area: float | None
    roughness_of_collector: str | None
    collector_thickness: float | None
    effectiveness_for_perforations_with_respect_to_wind: float | None
    discharge_coefficient_for_openings_with_respect_to_buoyancy_driven_flow: float | None
    surface_name: str | None

class SolarCollectorUnglazedTranspiredMultisystem(IDFObject):
    outdoor_air_system_collector_inlet_node: str | None
    outdoor_air_system_collector_outlet_node: str | None
    outdoor_air_system_mixed_air_node: str | None
    outdoor_air_system_zone_node: str | None

class BoilerHotWater(IDFObject):
    fuel_type: str | None
    nominal_capacity: float | str | None
    nominal_thermal_efficiency: float | None
    efficiency_curve_temperature_evaluation_variable: str | None
    normalized_boiler_efficiency_curve_name: str | None
    design_water_flow_rate: float | str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    boiler_water_inlet_node_name: str | None
    boiler_water_outlet_node_name: str | None
    water_outlet_upper_temperature_limit: float | None
    boiler_flow_mode: str | None
    on_cycle_parasitic_electric_load: float | None
    sizing_factor: float | None
    end_use_subcategory: str | None
    off_cycle_parasitic_fuel_load: float | None

class BoilerSteam(IDFObject):
    fuel_type: str | None
    maximum_operating_pressure: float | None
    theoretical_efficiency: float | None
    design_outlet_steam_temperature: float | None
    nominal_capacity: float | str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    coefficient_1_of_fuel_use_function_of_part_load_ratio_curve: float | None
    coefficient_2_of_fuel_use_function_of_part_load_ratio_curve: float | None
    coefficient_3_of_fuel_use_function_of_part_load_ratio_curve: float | None
    water_inlet_node_name: str | None
    steam_outlet_node_name: str | None
    sizing_factor: float | None
    end_use_subcategory: str | None

class ChillerElectricASHRAE205(IDFObject):
    representation_file_name: str | None
    performance_interpolation_method: str | None
    rated_capacity: float | str | None
    sizing_factor: float | None
    ambient_temperature_indicator: str | None
    ambient_temperature_schedule_name: str | None
    ambient_temperature_zone_name: str | None
    ambient_temperature_outdoor_air_node_name: str | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    chilled_water_maximum_requested_flow_rate: float | str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    condenser_maximum_requested_flow_rate: float | str | None
    chiller_flow_mode: str | None
    oil_cooler_inlet_node_name: str | None
    oil_cooler_outlet_node_name: str | None
    oil_cooler_design_flow_rate: float | None
    auxiliary_inlet_node_name: str | None
    auxiliary_outlet_node_name: str | None
    auxiliary_cooling_design_flow_rate: float | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    end_use_subcategory: str | None

class ChillerElectricEIR(IDFObject):
    reference_capacity: float | str | None
    reference_cop: float | None
    reference_leaving_chilled_water_temperature: float | None
    reference_entering_condenser_fluid_temperature: float | None
    reference_chilled_water_flow_rate: float | str | None
    reference_condenser_fluid_flow_rate: float | str | None
    cooling_capacity_function_of_temperature_curve_name: str | None
    electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None
    electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    minimum_unloading_ratio: float | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    condenser_type: str | None
    condenser_fan_power_ratio: float | None
    fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None
    leaving_chilled_water_lower_temperature_limit: float | None
    chiller_flow_mode: str | None
    design_heat_recovery_water_flow_rate: float | str | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    sizing_factor: float | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    condenser_heat_recovery_relative_capacity_fraction: float | None
    heat_recovery_inlet_high_temperature_limit_schedule_name: str | None
    heat_recovery_leaving_temperature_setpoint_node_name: str | None
    end_use_subcategory: str | None
    condenser_flow_control: str | None
    condenser_loop_flow_rate_fraction_function_of_loop_part_load_ratio_curve_name: str | None
    temperature_difference_across_condenser_schedule_name: str | None
    condenser_minimum_flow_fraction: float | None
    thermosiphon_capacity_fraction_curve_name: str | None
    thermosiphon_minimum_temperature_difference: float | None

class ChillerElectricReformulatedEIR(IDFObject):
    reference_capacity: float | str | None
    reference_cop: float | None
    reference_leaving_chilled_water_temperature: float | None
    reference_leaving_condenser_water_temperature: float | None
    reference_chilled_water_flow_rate: float | str | None
    reference_condenser_water_flow_rate: float | str | None
    cooling_capacity_function_of_temperature_curve_name: str | None
    electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None
    electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_type: str | None
    electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    minimum_unloading_ratio: float | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None
    leaving_chilled_water_lower_temperature_limit: float | None
    chiller_flow_mode_type: str | None
    design_heat_recovery_water_flow_rate: float | str | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    sizing_factor: float | None
    condenser_heat_recovery_relative_capacity_fraction: float | None
    heat_recovery_inlet_high_temperature_limit_schedule_name: str | None
    heat_recovery_leaving_temperature_setpoint_node_name: str | None
    end_use_subcategory: str | None
    condenser_flow_control: str | None
    condenser_loop_flow_rate_fraction_function_of_loop_part_load_ratio_curve_name: str | None
    temperature_difference_across_condenser_schedule_name: str | None
    condenser_minimum_flow_fraction: float | None
    thermosiphon_capacity_fraction_curve_name: str | None
    thermosiphon_minimum_temperature_difference: float | None

class ChillerElectric(IDFObject):
    condenser_type: str | None
    nominal_capacity: float | str | None
    nominal_cop: float | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    design_condenser_inlet_temperature: float | None
    temperature_rise_coefficient: float | None
    design_chilled_water_outlet_temperature: float | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_fluid_flow_rate: float | str | None
    coefficient_1_of_capacity_ratio_curve: float | None
    coefficient_2_of_capacity_ratio_curve: float | None
    coefficient_3_of_capacity_ratio_curve: float | None
    coefficient_1_of_power_ratio_curve: float | None
    coefficient_2_of_power_ratio_curve: float | None
    coefficient_3_of_power_ratio_curve: float | None
    coefficient_1_of_full_load_ratio_curve: float | None
    coefficient_2_of_full_load_ratio_curve: float | None
    coefficient_3_of_full_load_ratio_curve: float | None
    chilled_water_outlet_temperature_lower_limit: float | None
    chiller_flow_mode: str | None
    design_heat_recovery_water_flow_rate: float | str | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    sizing_factor: float | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    condenser_heat_recovery_relative_capacity_fraction: float | None
    heat_recovery_inlet_high_temperature_limit_schedule_name: str | None
    heat_recovery_leaving_temperature_setpoint_node_name: str | None
    end_use_subcategory: str | None
    thermosiphon_capacity_fraction_curve_name: str | None
    thermosiphon_minimum_temperature_difference: float | None

class ChillerAbsorptionIndirect(IDFObject):
    nominal_capacity: float | str | None
    nominal_pumping_power: float | str | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    design_condenser_inlet_temperature: float | None
    condenser_inlet_temperature_lower_limit: float | None
    chilled_water_outlet_temperature_lower_limit: float | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_water_flow_rate: float | str | None
    chiller_flow_mode: str | None
    generator_heat_input_function_of_part_load_ratio_curve_name: str | None
    pump_electric_input_function_of_part_load_ratio_curve_name: str | None
    generator_inlet_node_name: str | None
    generator_outlet_node_name: str | None
    capacity_correction_function_of_condenser_temperature_curve_name: str | None
    capacity_correction_function_of_chilled_water_temperature_curve_name: str | None
    capacity_correction_function_of_generator_temperature_curve_name: str | None
    generator_heat_input_correction_function_of_condenser_temperature_curve_name: str | None
    generator_heat_input_correction_function_of_chilled_water_temperature_curve_name: str | None
    generator_heat_source_type: str | None
    design_generator_fluid_flow_rate: float | str | None
    temperature_lower_limit_generator_inlet: float | None
    degree_of_subcooling_in_steam_generator: float | None
    degree_of_subcooling_in_steam_condensate_loop: float | None
    sizing_factor: float | None

class ChillerAbsorption(IDFObject):
    nominal_capacity: float | str | None
    nominal_pumping_power: float | str | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    design_condenser_inlet_temperature: float | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_water_flow_rate: float | str | None
    coefficient_1_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None
    coefficient_2_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None
    coefficient_3_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None
    coefficient_1_of_the_pump_electric_use_part_load_ratio_curve: float | None
    coefficient_2_of_the_pump_electric_use_part_load_ratio_curve: float | None
    coefficient_3_of_the_pump_electric_use_part_load_ratio_curve: float | None
    chilled_water_outlet_temperature_lower_limit: float | None
    generator_inlet_node_name: str | None
    generator_outlet_node_name: str | None
    chiller_flow_mode: str | None
    generator_heat_source_type: str | None
    design_generator_fluid_flow_rate: float | str | None
    degree_of_subcooling_in_steam_generator: float | None
    sizing_factor: float | None

class ChillerConstantCOP(IDFObject):
    nominal_capacity: float | str | None
    nominal_cop: float | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_water_flow_rate: float | str | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    condenser_type: str | None
    chiller_flow_mode: str | None
    sizing_factor: float | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    thermosiphon_capacity_fraction_curve_name: str | None
    thermosiphon_minimum_temperature_difference: float | None

class ChillerEngineDriven(IDFObject):
    condenser_type: str | None
    nominal_capacity: float | str | None
    nominal_cop: float | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    design_condenser_inlet_temperature: float | None
    temperature_rise_coefficient: float | None
    design_chilled_water_outlet_temperature: float | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_water_flow_rate: float | str | None
    coefficient_1_of_capacity_ratio_curve: float | None
    coefficient_2_of_capacity_ratio_curve: float | None
    coefficient_3_of_capacity_ratio_curve: float | None
    coefficient_1_of_power_ratio_curve: float | None
    coefficient_2_of_power_ratio_curve: float | None
    coefficient_3_of_power_ratio_curve: float | None
    coefficient_1_of_full_load_ratio_curve: float | None
    coefficient_2_of_full_load_ratio_curve: float | None
    coefficient_3_of_full_load_ratio_curve: float | None
    chilled_water_outlet_temperature_lower_limit: float | None
    fuel_use_curve_name: str | None
    jacket_heat_recovery_curve_name: str | None
    lube_heat_recovery_curve_name: str | None
    total_exhaust_energy_curve_name: str | None
    exhaust_temperature_curve_name: str | None
    coefficient_1_of_u_factor_times_area_curve: float | None
    coefficient_2_of_u_factor_times_area_curve: float | None
    maximum_exhaust_flow_per_unit_of_power_output: float | None
    design_minimum_exhaust_temperature: float | None
    fuel_type: str | None
    fuel_higher_heating_value: float | None
    design_heat_recovery_water_flow_rate: float | str | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    chiller_flow_mode: str | None
    maximum_temperature_for_heat_recovery_at_heat_recovery_outlet_node: float | None
    sizing_factor: float | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    condenser_heat_recovery_relative_capacity_fraction: float | None

class ChillerCombustionTurbine(IDFObject):
    condenser_type: str | None
    nominal_capacity: float | str | None
    nominal_cop: float | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    design_condenser_inlet_temperature: float | None
    temperature_rise_coefficient: float | None
    design_chilled_water_outlet_temperature: float | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_water_flow_rate: float | str | None
    coefficient_1_of_capacity_ratio_curve: float | None
    coefficient_2_of_capacity_ratio_curve: float | None
    coefficient_3_of_capacity_ratio_curve: float | None
    coefficient_1_of_power_ratio_curve: float | None
    coefficient_2_of_power_ratio_curve: float | None
    coefficient_3_of_power_ratio_curve: float | None
    coefficient_1_of_full_load_ratio_curve: float | None
    coefficient_2_of_full_load_ratio_curve: float | None
    coefficient_3_of_full_load_ratio_curve: float | None
    chilled_water_outlet_temperature_lower_limit: float | None
    coefficient_1_of_fuel_input_curve: float | None
    coefficient_2_of_fuel_input_curve: float | None
    coefficient_3_of_fuel_input_curve: float | None
    coefficient_1_of_temperature_based_fuel_input_curve: float | None
    coefficient_2_of_temperature_based_fuel_input_curve: float | None
    coefficient_3_of_temperature_based_fuel_input_curve: float | None
    coefficient_1_of_exhaust_flow_curve: float | None
    coefficient_2_of_exhaust_flow_curve: float | None
    coefficient_3_of_exhaust_flow_curve: float | None
    coefficient_1_of_exhaust_gas_temperature_curve: float | None
    coefficient_2_of_exhaust_gas_temperature_curve: float | None
    coefficient_3_of_exhaust_gas_temperature_curve: float | None
    coefficient_1_of_temperature_based_exhaust_gas_temperature_curve: float | None
    coefficient_2_of_temperature_based_exhaust_gas_temperature_curve: float | None
    coefficient_3_of_temperature_based_exhaust_gas_temperature_curve: float | None
    coefficient_1_of_recovery_lube_heat_curve: float | None
    coefficient_2_of_recovery_lube_heat_curve: float | None
    coefficient_3_of_recovery_lube_heat_curve: float | None
    coefficient_1_of_u_factor_times_area_curve: float | None
    coefficient_2_of_u_factor_times_area_curve: float | None
    gas_turbine_engine_capacity: float | str | None
    maximum_exhaust_flow_per_unit_of_power_output: float | None
    design_steam_saturation_temperature: float | None
    fuel_higher_heating_value: float | None
    design_heat_recovery_water_flow_rate: float | str | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    chiller_flow_mode: str | None
    fuel_type: str | None
    heat_recovery_maximum_temperature: float | None
    sizing_factor: float | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    condenser_heat_recovery_relative_capacity_fraction: float | None
    turbine_engine_efficiency: float | None

class ChillerHeaterAbsorptionDirectFired(IDFObject):
    nominal_cooling_capacity: float | str | None
    heating_to_cooling_capacity_ratio: float | None
    fuel_input_to_cooling_output_ratio: float | None
    fuel_input_to_heating_output_ratio: float | None
    electric_input_to_cooling_output_ratio: float | None
    electric_input_to_heating_output_ratio: float | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    hot_water_inlet_node_name: str | None
    hot_water_outlet_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    design_entering_condenser_water_temperature: float | None
    design_leaving_chilled_water_temperature: float | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_water_flow_rate: float | str | None
    design_hot_water_flow_rate: float | str | None
    cooling_capacity_function_of_temperature_curve_name: str | None
    fuel_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None
    fuel_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None
    electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None
    electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None
    heating_capacity_function_of_cooling_capacity_curve_name: str | None
    fuel_input_to_heat_output_ratio_during_heating_only_operation_curve_name: str | None
    temperature_curve_input_variable: str | None
    condenser_type: str | None
    chilled_water_temperature_lower_limit: float | None
    fuel_higher_heating_value: float | None
    fuel_type: str | None
    sizing_factor: float | None

class ChillerHeaterAbsorptionDoubleEffect(IDFObject):
    nominal_cooling_capacity: float | str | None
    heating_to_cooling_capacity_ratio: float | None
    thermal_energy_input_to_cooling_output_ratio: float | None
    thermal_energy_input_to_heating_output_ratio: float | None
    electric_input_to_cooling_output_ratio: float | None
    electric_input_to_heating_output_ratio: float | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    condenser_inlet_node_name: str | None
    condenser_outlet_node_name: str | None
    hot_water_inlet_node_name: str | None
    hot_water_outlet_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    design_entering_condenser_water_temperature: float | None
    design_leaving_chilled_water_temperature: float | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_water_flow_rate: float | str | None
    design_hot_water_flow_rate: float | str | None
    cooling_capacity_function_of_temperature_curve_name: str | None
    fuel_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None
    fuel_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None
    electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None
    electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None
    heating_capacity_function_of_cooling_capacity_curve_name: str | None
    fuel_input_to_heat_output_ratio_during_heating_only_operation_curve_name: str | None
    temperature_curve_input_variable: str | None
    condenser_type: str | None
    chilled_water_temperature_lower_limit: float | None
    exhaust_source_object_type: str | None
    exhaust_source_object_name: str | None
    sizing_factor: float | None

class HeatPumpPlantLoopEIRCooling(IDFObject):
    load_side_inlet_node_name: str | None
    load_side_outlet_node_name: str | None
    condenser_type: str | None
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    companion_heat_pump_name: str | None
    load_side_reference_flow_rate: float | str | None
    source_side_reference_flow_rate: float | str | None
    heat_recovery_reference_flow_rate: float | str | None
    reference_capacity: float | str | None
    reference_coefficient_of_performance: float | None
    sizing_factor: float | None
    capacity_modifier_function_of_temperature_curve_name: str | None
    electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str | None
    electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str | None
    control_type: str | None
    flow_mode: str | None
    minimum_part_load_ratio: float | None
    minimum_source_inlet_temperature: float | None
    maximum_source_inlet_temperature: float | None
    minimum_supply_water_temperature_curve_name: str | None
    maximum_supply_water_temperature_curve_name: str | None
    maximum_heat_recovery_outlet_temperature: float | None
    heat_recovery_capacity_modifier_function_of_temperature_curve_name: str | None
    heat_recovery_electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str | None
    thermosiphon_capacity_fraction_curve_name: str | None
    thermosiphon_minimum_temperature_difference: float | None

class HeatPumpPlantLoopEIRHeating(IDFObject):
    load_side_inlet_node_name: str | None
    load_side_outlet_node_name: str | None
    condenser_type: str | None
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    companion_heat_pump_name: str | None
    load_side_reference_flow_rate: float | str | None
    source_side_reference_flow_rate: float | str | None
    heat_recovery_reference_flow_rate: float | str | None
    reference_capacity: float | str | None
    reference_coefficient_of_performance: float | None
    sizing_factor: float | None
    capacity_modifier_function_of_temperature_curve_name: str | None
    electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str | None
    electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str | None
    heating_to_cooling_capacity_sizing_ratio: float | None
    heat_pump_sizing_method: str | None
    control_type: str | None
    flow_mode: str | None
    minimum_part_load_ratio: float | None
    minimum_source_inlet_temperature: float | None
    maximum_source_inlet_temperature: float | None
    minimum_supply_water_temperature_curve_name: str | None
    maximum_supply_water_temperature_curve_name: str | None
    dry_outdoor_correction_factor_curve_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    heat_pump_defrost_control: str | None
    heat_pump_defrost_time_period_fraction: float | None
    defrost_energy_input_ratio_function_of_temperature_curve_name: str | None
    timed_empirical_defrost_frequency_curve_name: str | None
    timed_empirical_defrost_heat_load_penalty_curve_name: str | None
    timed_empirical_defrost_heat_input_energy_fraction_curve_name: str | None
    minimum_heat_recovery_outlet_temperature: float | None
    heat_recovery_capacity_modifier_function_of_temperature_curve_name: str | None
    heat_recovery_electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str | None

class HeatPumpAirToWaterFuelFiredHeating(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_source_node_name: str | None
    companion_cooling_heat_pump_name: str | None
    fuel_type: str | None
    end_use_subcategory: str | None
    nominal_heating_capacity: float | str | None
    nominal_cop: float | None
    design_flow_rate: float | str | None
    design_supply_temperature: float | None
    design_temperature_lift: float | str | None
    sizing_factor: float | None
    flow_mode: str | None
    outdoor_air_temperature_curve_input_variable: str | None
    water_temperature_curve_input_variable: str | None
    normalized_capacity_function_of_temperature_curve_name: str | None
    fuel_energy_input_ratio_function_of_temperature_curve_name: str | None
    fuel_energy_input_ratio_function_of_plr_curve_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    defrost_control_type: str | None
    defrost_operation_time_fraction: float | None
    fuel_energy_input_ratio_defrost_adjustment_curve_name: str | None
    resistive_defrost_heater_capacity: float | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    cycling_ratio_factor_curve_name: str | None
    nominal_auxiliary_electric_power: float | None
    auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None
    auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None
    standby_electric_power: float | None
    minimum_unloading_ratio: float | None

class HeatPumpAirToWaterFuelFiredCooling(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    air_source_node_name: str | None
    companion_heating_heat_pump_name: str | None
    fuel_type: str | None
    end_use_subcategory: str | None
    nominal_cooling_capacity: float | str | None
    nominal_cop: float | None
    design_flow_rate: float | str | None
    design_supply_temperature: float | None
    design_temperature_lift: float | str | None
    sizing_factor: float | None
    flow_mode: str | None
    outdoor_air_temperature_curve_input_variable: str | None
    water_temperature_curve_input_variable: str | None
    normalized_capacity_function_of_temperature_curve_name: str | None
    fuel_energy_input_ratio_function_of_temperature_curve_name: str | None
    fuel_energy_input_ratio_function_of_plr_curve_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    cycling_ratio_factor_curve_name: str | None
    nominal_auxiliary_electric_power: float | None
    auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None
    auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None
    standby_electric_power: float | None
    minimum_unloading_ratio: float | None

class HeatPumpAirToWater(IDFObject):
    availability_schedule_name_heating: str | None
    availability_schedule_name_cooling: str | None
    operating_mode_control_method: str | None
    operating_mode_control_option_for_multiple_unit: str | None
    operating_mode_control_schedule_name: str | None
    minimum_part_load_ratio: float | None
    rated_inlet_air_temperature_in_heating_mode: float | None
    rated_air_flow_rate_in_heating_mode: float | str | None
    rated_leaving_water_temperature_in_heating_mode: float | None
    rated_water_flow_rate_in_heating_mode: float | str | None
    minimum_outdoor_air_temperature_in_heating_mode: float | None
    maximum_outdoor_air_temperature_in_heating_mode: float | None
    minimum_leaving_water_temperature_curve_name_in_heating_mode: str | None
    maximum_leaving_water_temperature_curve_name_in_heating_mode: str | None
    sizing_factor_for_heating: float | None
    rated_inlet_air_temperature_in_cooling_mode: float | None
    rated_air_flow_rate_in_cooling_mode: float | str | None
    rated_leaving_water_temperature_in_cooling_mode: float | None
    rated_water_flow_rate_in_cooling_mode: float | str | None
    minimum_outdoor_air_temperature_in_cooling_mode: float | None
    maximum_outdoor_air_temperature_in_cooling_mode: float | None
    minimum_leaving_water_temperature_curve_name_in_cooling_mode: str | None
    maximum_leaving_water_temperature_curve_name_in_cooling_mode: str | None
    sizing_factor_for_cooling: float | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    hot_water_inlet_node_name: str | None
    hot_water_outlet_node_name: str | None
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None
    heat_pump_defrost_control: str | None
    heat_pump_defrost_time_period_fraction: float | None
    resistive_defrost_heater_capacity: float | None
    defrost_energy_input_ratio_function_of_temperature_curve_name: str | None
    heat_pump_multiplier: int | None
    control_type: str | None
    crankcase_heater_capacity: float | None
    crankcase_heater_capacity_function_of_temperature_curve_name: str | None
    maximum_ambient_temperature_for_crankcase_heater_operation: float | None
    number_of_speeds_for_heating: int | None
    rated_heating_capacity_at_speed_1: float | str | None
    rated_cop_for_heating_at_speed_1: float | None
    normalized_heating_capacity_function_of_temperature_curve_name_at_speed_1: str | None
    heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_1: str | None
    heating_energy_input_ratio_function_of_plr_curve_name_at_speed_1: str | None
    rated_heating_capacity_at_speed_2: float | str | None
    rated_cop_for_heating_at_speed_2: float | None
    normalized_heating_capacity_function_of_temperature_curve_name_at_speed_2: str | None
    heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_2: str | None
    heating_energy_input_ratio_function_of_plr_curve_name_at_speed_2: str | None
    rated_heating_capacity_at_speed_3: float | str | None
    rated_cop_for_heating_at_speed_3: float | None
    normalized_heating_capacity_function_of_temperature_curve_name_at_speed_3: str | None
    heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_3: str | None
    heating_energy_input_ratio_function_of_plr_curve_name_at_speed_3: str | None
    rated_heating_capacity_at_speed_4: float | str | None
    rated_cop_for_heating_at_speed_4: float | None
    normalized_heating_capacity_function_of_temperature_curve_name_at_speed_4: str | None
    heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_4: str | None
    heating_energy_input_ratio_function_of_plr_curve_name_at_speed_4: str | None
    rated_heating_capacity_at_speed_5: float | str | None
    rated_cop_for_heating_at_speed_5: float | None
    normalized_heating_capacity_function_of_temperature_curve_name_at_speed_5: str | None
    heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_5: str | None
    heating_energy_input_ratio_function_of_plr_curve_name_at_speed_5: str | None
    booster_mode_on_heating: str | None
    rated_heating_capacity_in_booster_mode: float | None
    rated_heating_cop_in_booster_mode: float | None
    normalized_heating_capacity_function_of_temperature_curve_name_in_booster_mode: str | None
    heating_energy_input_ratio_function_of_temperature_curve_name_in_booster_mode: str | None
    heating_energy_input_ratio_function_of_plr_curve_name_in_booster_mode: str | None
    number_of_speeds_for_cooling: int | None
    rated_cooling_capacity_at_speed_1: float | str | None
    rated_cop_for_cooling_at_speed_1: float | None
    normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_1: str | None
    cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_1: str | None
    cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_1: str | None
    rated_cooling_capacity_at_speed_2: float | str | None
    rated_cop_for_cooling_at_speed_2: float | None
    normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_2: str | None
    cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_2: str | None
    cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_2: str | None
    rated_cooling_capacity_at_speed_3: float | str | None
    rated_cop_for_cooling_at_speed_3: float | None
    normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_3: str | None
    cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_3: str | None
    cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_3: str | None
    rated_cooling_capacity_at_speed_4: float | str | None
    rated_cop_for_cooling_at_speed_4: float | None
    normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_4: str | None
    cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_4: str | None
    cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_4: str | None
    rated_cooling_capacity_at_speed_5: float | str | None
    rated_cop_for_cooling_at_speed_5: float | None
    normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_5: str | None
    cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_5: str | None
    cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_5: str | None
    booster_mode_on_cooling: str | None
    rated_cooling_capacity_in_booster_mode: float | None
    rated_cooling_cop_in_booster_mode: float | None
    normalized_cooling_capacity_function_of_temperature_curve_name_in_booster_mode: str | None
    cooling_energy_input_ratio_function_of_temperature_curve_name_in_booster_mode: str | None
    cooling_energy_input_ratio_function_of_plr_curve_name_in_booster_mode: str | None

class HeatPumpWaterToWaterEquationFitHeating(IDFObject):
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    load_side_inlet_node_name: str | None
    load_side_outlet_node_name: str | None
    reference_load_side_flow_rate: float | str | None
    reference_source_side_flow_rate: float | str | None
    reference_heating_capacity: float | str | None
    reference_heating_power_consumption: float | str | None
    heating_capacity_curve_name: str | None
    heating_compressor_power_curve_name: str | None
    reference_coefficient_of_performance: float | None
    sizing_factor: float | None
    companion_cooling_heat_pump_name: str | None

class HeatPumpWaterToWaterEquationFitCooling(IDFObject):
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    load_side_inlet_node_name: str | None
    load_side_outlet_node_name: str | None
    reference_load_side_flow_rate: float | str | None
    reference_source_side_flow_rate: float | str | None
    reference_cooling_capacity: float | str | None
    reference_cooling_power_consumption: float | str | None
    cooling_capacity_curve_name: str | None
    cooling_compressor_power_curve_name: str | None
    reference_coefficient_of_performance: float | None
    sizing_factor: float | None
    companion_heating_heat_pump_name: str | None

class HeatPumpWaterToWaterParameterEstimationCooling(IDFObject):
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    load_side_inlet_node_name: str | None
    load_side_outlet_node_name: str | None
    nominal_cop: float | None
    nominal_capacity: float | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    load_side_flow_rate: float | None
    source_side_flow_rate: float | None
    load_side_heat_transfer_coefficient: float | None
    source_side_heat_transfer_coefficient: float | None
    piston_displacement: float | None
    compressor_clearance_factor: float | None
    compressor_suction_and_discharge_pressure_drop: float | None
    superheating: float | None
    constant_part_of_electromechanical_power_losses: float | None
    loss_factor: float | None
    high_pressure_cut_off: float | None
    low_pressure_cut_off: float | None

class HeatPumpWaterToWaterParameterEstimationHeating(IDFObject):
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    load_side_inlet_node_name: str | None
    load_side_outlet_node_name: str | None
    nominal_cop: float | None
    nominal_capacity: float | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    load_side_flow_rate: float | None
    source_side_flow_rate: float | None
    load_side_heat_transfer_coefficient: float | None
    source_side_heat_transfer_coefficient: float | None
    piston_displacement: float | None
    compressor_clearance_factor: float | None
    compressor_suction_and_discharge_pressure_drop: float | None
    superheating: float | None
    constant_part_of_electromechanical_power_losses: float | None
    loss_factor: float | None
    high_pressure_cut_off: float | None
    low_pressure_cut_off: float | None

class DistrictCooling(IDFObject):
    chilled_water_inlet_node_name: str | None
    chilled_water_outlet_node_name: str | None
    nominal_capacity: float | str | None
    capacity_fraction_schedule_name: str | None

class DistrictHeatingWater(IDFObject):
    hot_water_inlet_node_name: str | None
    hot_water_outlet_node_name: str | None
    nominal_capacity: float | str | None
    capacity_fraction_schedule_name: str | None

class DistrictHeatingSteam(IDFObject):
    steam_inlet_node_name: str | None
    steam_outlet_node_name: str | None
    nominal_capacity: float | str | None
    capacity_fraction_schedule_name: str | None

class PlantComponentTemperatureSource(IDFObject):
    inlet_node: str | None
    outlet_node: str | None
    design_volume_flow_rate: float | str | None
    temperature_specification_type: str | None
    source_temperature: float | None
    source_temperature_schedule_name: str | None

class CentralHeatPumpSystem(IDFObject):
    control_method: str | None
    cooling_loop_inlet_node_name: str | None
    cooling_loop_outlet_node_name: str | None
    source_loop_inlet_node_name: str | None
    source_loop_outlet_node_name: str | None
    heating_loop_inlet_node_name: str | None
    heating_loop_outlet_node_name: str | None
    ancillary_power: float | None
    ancillary_operation_schedule_name: str | None
    chiller_heater_modules_performance_component_object_type_1: str | None
    chiller_heater_modules_performance_component_name_1: str | None
    chiller_heater_modules_control_schedule_name_1: str | None
    number_of_chiller_heater_modules_1: int | None
    chiller_heater_modules_performance_component_object_type_2: str | None
    chiller_heater_modules_performance_component_name_2: str | None
    chiller_heater_modules_control_schedule_name_2: str | None
    number_of_chiller_heater_modules_2: int | None
    chiller_heater_performance_component_object_type_3: str | None
    chiller_heater_performance_component_name_3: str | None
    chiller_heater_modules_control_schedule_name_3: str | None
    number_of_chiller_heater_modules_3: int | None
    chiller_heater_modules_performance_component_object_type_4: str | None
    chiller_heater_modules_performance_component_name_4: str | None
    chiller_heater_modules_control_schedule_name_4: str | None
    number_of_chiller_heater_modules_4: int | None
    chiller_heater_modules_performance_component_object_type_5: str | None
    chiller_heater_models_performance_component_name_5: str | None
    chiller_heater_modules_control_schedule_name_5: str | None
    number_of_chiller_heater_modules_5: int | None
    chiller_heater_modules_performance_component_object_type_6: str | None
    chiller_heater_modules_performance_component_name_6: str | None
    chiller_heater_modules_control_schedule_name_6: str | None
    number_of_chiller_heater_modules_6: int | None
    chiller_heater_modules_performance_component_object_type_7: str | None
    chiller_heater_modules_performance_component_name_7: str | None
    chiller_heater_modules_control_schedule_name_7: str | None
    number_of_chiller_heater_modules_7: int | None
    chiller_heater_modules_performance_component_object_type_8: str | None
    chiller_heater_modules_performance_component_name_8: str | None
    chiller_heater_modules_control_schedule_name_8: str | None
    number_of_chiller_heater_modules_8: int | None
    chiller_heater_modules_performance_component_object_type_9: str | None
    chiller_heater_modules_performance_component_name_9: str | None
    chiller_heater_modules_control_schedule_name_9: str | None
    number_of_chiller_heater_modules_9: int | None
    chiller_heater_modules_performance_component_object_type_10: str | None
    chiller_heater_modules_performance_component_name_10: str | None
    chiller_heater_modules_control_schedule_name_10: str | None
    number_of_chiller_heater_modules_10: int | None
    chiller_heater_modules_performance_component_object_type_11: str | None
    chiller_heater_modules_performance_component_name_11: str | None
    chiller_heater_module_control_schedule_name_11: str | None
    number_of_chiller_heater_modules_11: int | None
    chiller_heater_modules_performance_component_object_type_12: str | None
    chiller_heater_modules_performance_component_name_12: str | None
    chiller_heater_modules_control_schedule_name_12: str | None
    number_of_chiller_heater_modules_12: int | None
    chiller_heater_modules_performance_component_object_type_13: str | None
    chiller_heater_modules_performance_component_name_13: str | None
    chiller_heater_modules_control_schedule_name_13: str | None
    number_of_chiller_heater_modules_13: int | None
    chiller_heater_modules_performance_component_object_type_14: str | None
    chiller_heater_modules_performance_component_name_14: str | None
    chiller_heater_modules_control_schedule_name_14: str | None
    number_of_chiller_heater_modules_14: int | None
    chiller_heater_modules_performance_component_object_type_15: str | None
    chiller_heater_modules_performance_component_name_15: str | None
    chiller_heater_modules_control_schedule_name_15: str | None
    number_of_chiller_heater_modules_15: int | None
    chiller_heater_modules_performance_component_object_type_16: str | None
    chiller_heater_modules_performance_component_name_16: str | None
    chiller_heater_modules_control_schedule_name_16: str | None
    number_of_chiller_heater_modules_16: int | None
    chiller_heater_modules_performance_component_object_type_17: str | None
    chiller_heater_modules_performance_component_name_17: str | None
    chiller_heater_modules_control_schedule_name_17: str | None
    number_of_chiller_heater_modules_17: int | None
    chiller_heater_modules_performance_component_object_type_18: str | None
    chiller_heater_modules_performance_component_name_18: str | None
    chiller_heater_modules_control_control_schedule_name_18: str | None
    number_of_chiller_heater_modules_18: int | None
    chiller_heater_modules_performance_component_object_type_19: str | None
    chiller_heater_modules_performance_component_name_19: str | None
    chiller_heater_modules_control_schedule_name_19: str | None
    number_of_chiller_heater_modules_19: int | None
    chiller_heater_modules_performance_component_object_type_20: str | None
    chiller_heater_modules_performance_component_name_20: str | None
    chiller_heater_modules_control_schedule_name_20: str | None
    number_of_chiller_heater_modules_20: int | None

class ChillerHeaterPerformanceElectricEIR(IDFObject):
    reference_cooling_mode_evaporator_capacity: float | str | None
    reference_cooling_mode_cop: float | None
    reference_cooling_mode_leaving_chilled_water_temperature: float | None
    reference_cooling_mode_entering_condenser_fluid_temperature: float | None
    reference_cooling_mode_leaving_condenser_water_temperature: float | None
    reference_heating_mode_cooling_capacity_ratio: float | None
    reference_heating_mode_cooling_power_input_ratio: float | None
    reference_heating_mode_leaving_chilled_water_temperature: float | None
    reference_heating_mode_leaving_condenser_water_temperature: float | None
    reference_heating_mode_entering_condenser_fluid_temperature: float | None
    heating_mode_entering_chilled_water_temperature_low_limit: float | None
    chilled_water_flow_mode_type: str | None
    design_chilled_water_flow_rate: float | str | None
    design_condenser_water_flow_rate: float | str | None
    design_hot_water_flow_rate: float | None
    compressor_motor_efficiency: float | None
    condenser_type: str | None
    cooling_mode_temperature_curve_condenser_water_independent_variable: str | None
    cooling_mode_cooling_capacity_function_of_temperature_curve_name: str | None
    cooling_mode_electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None
    cooling_mode_electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None
    cooling_mode_cooling_capacity_optimum_part_load_ratio: float | None
    heating_mode_temperature_curve_condenser_water_independent_variable: str | None
    heating_mode_cooling_capacity_function_of_temperature_curve_name: str | None
    heating_mode_electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None
    heating_mode_electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None
    heating_mode_cooling_capacity_optimum_part_load_ratio: float | None
    sizing_factor: float | None

class CoolingTowerSingleSpeed(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    design_water_flow_rate: float | str | None
    design_air_flow_rate: float | str | None
    design_fan_power: float | str | None
    design_u_factor_times_area_value: float | str | None
    free_convection_regime_air_flow_rate: float | str | None
    free_convection_regime_air_flow_rate_sizing_factor: float | None
    free_convection_regime_u_factor_times_area_value: float | str | None
    free_convection_u_factor_times_area_value_sizing_factor: float | None
    performance_input_method: str | None
    heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None
    nominal_capacity: float | None
    free_convection_capacity: float | str | None
    free_convection_nominal_capacity_sizing_factor: float | None
    design_inlet_air_dry_bulb_temperature: float | None
    design_inlet_air_wet_bulb_temperature: float | None
    design_approach_temperature: float | str | None
    design_range_temperature: float | str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    evaporation_loss_mode: str | None
    evaporation_loss_factor: float | None
    drift_loss_percent: float | None
    blowdown_calculation_mode: str | None
    blowdown_concentration_ratio: float | None
    blowdown_makeup_water_usage_schedule_name: str | None
    supply_water_storage_tank_name: str | None
    outdoor_air_inlet_node_name: str | None
    capacity_control: str | None
    number_of_cells: int | None
    cell_control: str | None
    cell_minimum_water_flow_rate_fraction: float | None
    cell_maximum_water_flow_rate_fraction: float | None
    sizing_factor: float | None
    end_use_subcategory: str | None

class CoolingTowerTwoSpeed(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    design_water_flow_rate: float | str | None
    high_fan_speed_air_flow_rate: float | str | None
    high_fan_speed_fan_power: float | str | None
    high_fan_speed_u_factor_times_area_value: float | str | None
    low_fan_speed_air_flow_rate: float | str | None
    low_fan_speed_air_flow_rate_sizing_factor: float | None
    low_fan_speed_fan_power: float | str | None
    low_fan_speed_fan_power_sizing_factor: float | None
    low_fan_speed_u_factor_times_area_value: float | str | None
    low_fan_speed_u_factor_times_area_sizing_factor: float | None
    free_convection_regime_air_flow_rate: float | str | None
    free_convection_regime_air_flow_rate_sizing_factor: float | None
    free_convection_regime_u_factor_times_area_value: float | str | None
    free_convection_u_factor_times_area_value_sizing_factor: float | None
    performance_input_method: str | None
    heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None
    high_speed_nominal_capacity: float | None
    low_speed_nominal_capacity: float | str | None
    low_speed_nominal_capacity_sizing_factor: float | None
    free_convection_nominal_capacity: float | str | None
    free_convection_nominal_capacity_sizing_factor: float | None
    design_inlet_air_dry_bulb_temperature: float | None
    design_inlet_air_wet_bulb_temperature: float | None
    design_approach_temperature: float | str | None
    design_range_temperature: float | str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    evaporation_loss_mode: str | None
    evaporation_loss_factor: float | None
    drift_loss_percent: float | None
    blowdown_calculation_mode: str | None
    blowdown_concentration_ratio: float | None
    blowdown_makeup_water_usage_schedule_name: str | None
    supply_water_storage_tank_name: str | None
    outdoor_air_inlet_node_name: str | None
    number_of_cells: int | None
    cell_control: str | None
    cell_minimum_water_flow_rate_fraction: float | None
    cell_maximum_water_flow_rate_fraction: float | None
    sizing_factor: float | None
    end_use_subcategory: str | None

class CoolingTowerVariableSpeedMerkel(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    performance_input_method: str | None
    heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None
    nominal_capacity: float | str | None
    free_convection_nominal_capacity: float | str | None
    free_convection_nominal_capacity_sizing_factor: float | None
    design_water_flow_rate: float | str | None
    design_water_flow_rate_per_unit_of_nominal_capacity: float | None
    design_air_flow_rate: float | str | None
    design_air_flow_rate_per_unit_of_nominal_capacity: float | None
    minimum_air_flow_rate_ratio: float | None
    design_fan_power: float | str | None
    design_fan_power_per_unit_of_nominal_capacity: float | None
    fan_power_modifier_function_of_air_flow_rate_ratio_curve_name: str | None
    free_convection_regime_air_flow_rate: float | str | None
    free_convection_regime_air_flow_rate_sizing_factor: float | None
    design_air_flow_rate_u_factor_times_area_value: float | str | None
    free_convection_regime_u_factor_times_area_value: float | str | None
    free_convection_u_factor_times_area_value_sizing_factor: float | None
    u_factor_times_area_modifier_function_of_air_flow_ratio_curve_name: str | None
    u_factor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name: str | None
    u_factor_times_area_modifier_function_of_water_flow_ratio_curve_name: str | None
    design_inlet_air_dry_bulb_temperature: float | None
    design_inlet_air_wet_bulb_temperature: float | None
    design_approach_temperature: float | str | None
    design_range_temperature: float | str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    evaporation_loss_mode: str | None
    evaporation_loss_factor: float | None
    drift_loss_percent: float | None
    blowdown_calculation_mode: str | None
    blowdown_concentration_ratio: float | None
    blowdown_makeup_water_usage_schedule_name: str | None
    supply_water_storage_tank_name: str | None
    outdoor_air_inlet_node_name: str | None
    number_of_cells: int | None
    cell_control: str | None
    cell_minimum_water_flow_rate_fraction: float | None
    cell_maximum_water_flow_rate_fraction: float | None
    sizing_factor: float | None
    end_use_subcategory: str | None

class CoolingTowerVariableSpeed(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    model_type: str | None
    model_coefficient_name: str | None
    design_inlet_air_wet_bulb_temperature: float | None
    design_approach_temperature: float | None
    design_range_temperature: float | None
    design_water_flow_rate: float | str | None
    design_air_flow_rate: float | str | None
    design_fan_power: float | str | None
    fan_power_ratio_function_of_air_flow_rate_ratio_curve_name: str | None
    minimum_air_flow_rate_ratio: float | None
    fraction_of_tower_capacity_in_free_convection_regime: float | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    basin_heater_operating_schedule_name: str | None
    evaporation_loss_mode: str | None
    evaporation_loss_factor: float | None
    drift_loss_percent: float | None
    blowdown_calculation_mode: str | None
    blowdown_concentration_ratio: float | None
    blowdown_makeup_water_usage_schedule_name: str | None
    supply_water_storage_tank_name: str | None
    outdoor_air_inlet_node_name: str | None
    number_of_cells: int | None
    cell_control: str | None
    cell_minimum_water_flow_rate_fraction: float | None
    cell_maximum_water_flow_rate_fraction: float | None
    sizing_factor: float | None
    end_use_subcategory: str | None

class CoolingTowerPerformanceCoolTools(IDFObject):
    minimum_inlet_air_wet_bulb_temperature: float | None
    maximum_inlet_air_wet_bulb_temperature: float | None
    minimum_range_temperature: float | None
    maximum_range_temperature: float | None
    minimum_approach_temperature: float | None
    maximum_approach_temperature: float | None
    minimum_water_flow_rate_ratio: float | None
    maximum_water_flow_rate_ratio: float | None
    coefficient_1: float | None
    coefficient_2: float | None
    coefficient_3: float | None
    coefficient_4: float | None
    coefficient_5: float | None
    coefficient_6: float | None
    coefficient_7: float | None
    coefficient_8: float | None
    coefficient_9: float | None
    coefficient_10: float | None
    coefficient_11: float | None
    coefficient_12: float | None
    coefficient_13: float | None
    coefficient_14: float | None
    coefficient_15: float | None
    coefficient_16: float | None
    coefficient_17: float | None
    coefficient_18: float | None
    coefficient_19: float | None
    coefficient_20: float | None
    coefficient_21: float | None
    coefficient_22: float | None
    coefficient_23: float | None
    coefficient_24: float | None
    coefficient_25: float | None
    coefficient_26: float | None
    coefficient_27: float | None
    coefficient_28: float | None
    coefficient_29: float | None
    coefficient_30: float | None
    coefficient_31: float | None
    coefficient_32: float | None
    coefficient_33: float | None
    coefficient_34: float | None
    coefficient_35: float | None

class CoolingTowerPerformanceYorkCalc(IDFObject):
    minimum_inlet_air_wet_bulb_temperature: float | None
    maximum_inlet_air_wet_bulb_temperature: float | None
    minimum_range_temperature: float | None
    maximum_range_temperature: float | None
    minimum_approach_temperature: float | None
    maximum_approach_temperature: float | None
    minimum_water_flow_rate_ratio: float | None
    maximum_water_flow_rate_ratio: float | None
    maximum_liquid_to_gas_ratio: float | None
    coefficient_1: float | None
    coefficient_2: float | None
    coefficient_3: float | None
    coefficient_4: float | None
    coefficient_5: float | None
    coefficient_6: float | None
    coefficient_7: float | None
    coefficient_8: float | None
    coefficient_9: float | None
    coefficient_10: float | None
    coefficient_11: float | None
    coefficient_12: float | None
    coefficient_13: float | None
    coefficient_14: float | None
    coefficient_15: float | None
    coefficient_16: float | None
    coefficient_17: float | None
    coefficient_18: float | None
    coefficient_19: float | None
    coefficient_20: float | None
    coefficient_21: float | None
    coefficient_22: float | None
    coefficient_23: float | None
    coefficient_24: float | None
    coefficient_25: float | None
    coefficient_26: float | None
    coefficient_27: float | None

class EvaporativeFluidCoolerSingleSpeed(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    design_air_flow_rate: float | str | None
    design_air_flow_rate_fan_power: float | str | None
    design_spray_water_flow_rate: float | None
    performance_input_method: str | None
    outdoor_air_inlet_node_name: str | None
    heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None
    standard_design_capacity: float | None
    design_air_flow_rate_u_factor_times_area_value: float | str | None
    design_water_flow_rate: float | str | None
    user_specified_design_capacity: float | None
    design_entering_water_temperature: float | str | None
    design_entering_air_temperature: float | None
    design_entering_air_wet_bulb_temperature: float | None
    capacity_control: str | None
    sizing_factor: float | None
    evaporation_loss_mode: str | None
    evaporation_loss_factor: float | None
    drift_loss_percent: float | None
    blowdown_calculation_mode: str | None
    blowdown_concentration_ratio: float | None
    blowdown_makeup_water_usage_schedule_name: str | None
    supply_water_storage_tank_name: str | None

class EvaporativeFluidCoolerTwoSpeed(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    high_fan_speed_air_flow_rate: float | str | None
    high_fan_speed_fan_power: float | str | None
    low_fan_speed_air_flow_rate: float | str | None
    low_fan_speed_air_flow_rate_sizing_factor: float | None
    low_fan_speed_fan_power: float | str | None
    low_fan_speed_fan_power_sizing_factor: float | None
    design_spray_water_flow_rate: float | None
    performance_input_method: str | None
    outdoor_air_inlet_node_name: str | None
    heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None
    high_speed_standard_design_capacity: float | None
    low_speed_standard_design_capacity: float | str | None
    low_speed_standard_capacity_sizing_factor: float | None
    high_fan_speed_u_factor_times_area_value: float | str | None
    low_fan_speed_u_factor_times_area_value: float | str | None
    low_fan_speed_u_factor_times_area_sizing_factor: float | None
    design_water_flow_rate: float | str | None
    high_speed_user_specified_design_capacity: float | None
    low_speed_user_specified_design_capacity: float | str | None
    low_speed_user_specified_design_capacity_sizing_factor: float | None
    design_entering_water_temperature: float | str | None
    design_entering_air_temperature: float | None
    design_entering_air_wet_bulb_temperature: float | None
    high_speed_sizing_factor: float | None
    evaporation_loss_mode: str | None
    evaporation_loss_factor: float | None
    drift_loss_percent: float | None
    blowdown_calculation_mode: str | None
    blowdown_concentration_ratio: float | None
    blowdown_makeup_water_usage_schedule_name: str | None
    supply_water_storage_tank_name: str | None

class FluidCoolerSingleSpeed(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    performance_input_method: str | None
    design_air_flow_rate_u_factor_times_area_value: float | str | None
    nominal_capacity: float | None
    design_entering_water_temperature: float | None
    design_entering_air_temperature: float | None
    design_entering_air_wetbulb_temperature: float | None
    design_water_flow_rate: float | str | None
    design_air_flow_rate: float | str | None
    design_air_flow_rate_fan_power: float | str | None
    outdoor_air_inlet_node_name: str | None

class FluidCoolerTwoSpeed(IDFObject):
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    performance_input_method: str | None
    high_fan_speed_u_factor_times_area_value: float | str | None
    low_fan_speed_u_factor_times_area_value: float | str | None
    low_fan_speed_u_factor_times_area_sizing_factor: float | None
    high_speed_nominal_capacity: float | None
    low_speed_nominal_capacity: float | str | None
    low_speed_nominal_capacity_sizing_factor: float | None
    design_entering_water_temperature: float | None
    design_entering_air_temperature: float | None
    design_entering_air_wet_bulb_temperature: float | None
    design_water_flow_rate: float | str | None
    high_fan_speed_air_flow_rate: float | str | None
    high_fan_speed_fan_power: float | str | None
    low_fan_speed_air_flow_rate: float | str | None
    low_fan_speed_air_flow_rate_sizing_factor: float | None
    low_fan_speed_fan_power: float | str | None
    low_fan_speed_fan_power_sizing_factor: float | None
    outdoor_air_inlet_node_name: str | None

class GroundHeatExchangerSystem(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    design_flow_rate: float | None
    undisturbed_ground_temperature_model_type: str | None
    undisturbed_ground_temperature_model_name: str | None
    ground_thermal_conductivity: float | None
    ground_thermal_heat_capacity: float | None
    ghe_vertical_responsefactors_object_name: str | None
    g_function_calculation_method: str | None
    ghe_vertical_sizing_object_type: str | None
    ghe_vertical_sizing_object_name: str | None
    ghe_vertical_array_object_name: str | None
    ghe_vertical_single_object_name: str | None

class GroundHeatExchangerVerticalSizingRectangle(IDFObject):
    sizingperiod_weatherfiledays_name: str | None
    design_flow_rate_per_borehole: float | None
    available_borehole_field_length: float | None
    available_borehole_field_width: float | None
    maximum_number_of_boreholes: float | None
    minimum_borehole_spacing: float | None
    maximum_borehole_spacing: float | None
    minimum_borehole_vertical_length: float | None
    maximum_borehole_vertical_length: float | None
    minimum_exiting_fluid_temperature_for_sizing: float | None
    maximum_exiting_fluid_temperature_for_sizing: float | None

class GroundHeatExchangerVerticalProperties(IDFObject):
    depth_of_top_of_borehole: float | None
    borehole_length: float | None
    borehole_diameter: float | None
    grout_thermal_conductivity: float | None
    grout_thermal_heat_capacity: float | None
    pipe_thermal_conductivity: float | None
    pipe_thermal_heat_capacity: float | None
    pipe_outer_diameter: float | None
    pipe_thickness: float | None
    u_tube_distance: float | None

class GroundHeatExchangerVerticalArray(IDFObject):
    ghe_vertical_properties_object_name: str | None
    number_of_boreholes_in_x_direction: int | None
    number_of_boreholes_in_y_direction: int | None
    borehole_spacing: float | None

class GroundHeatExchangerVerticalSingle(IDFObject):
    ghe_vertical_properties_object_name: str | None
    x_location: float | None
    y_location: float | None

class GroundHeatExchangerResponseFactors(IDFObject):
    ghe_vertical_properties_object_name: str | None
    number_of_boreholes: int | None
    g_function_reference_ratio: float | None
    g_function_ln_t_ts_value: float | None
    g_function_g_value: float | None

class GroundHeatExchangerPond(IDFObject):
    fluid_inlet_node_name: str | None
    fluid_outlet_node_name: str | None
    pond_depth: float | None
    pond_area: float | None
    hydronic_tubing_inside_diameter: float | None
    hydronic_tubing_outside_diameter: float | None
    hydronic_tubing_thermal_conductivity: float | None
    ground_thermal_conductivity: float | None
    number_of_tubing_circuits: int | None
    length_of_each_tubing_circuit: float | None

class GroundHeatExchangerSurface(IDFObject):
    construction_name: str | None
    fluid_inlet_node_name: str | None
    fluid_outlet_node_name: str | None
    hydronic_tubing_inside_diameter: float | None
    number_of_tubing_circuits: int | None
    hydronic_tube_spacing: float | None
    surface_length: float | None
    surface_width: float | None
    lower_surface_environment: str | None

class GroundHeatExchangerHorizontalTrench(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    design_flow_rate: float | None
    trench_length_in_pipe_axial_direction: float | None
    number_of_trenches: int | None
    horizontal_spacing_between_pipes: float | None
    pipe_inner_diameter: float | None
    pipe_outer_diameter: float | None
    burial_depth: float | None
    soil_thermal_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    pipe_thermal_conductivity: float | None
    pipe_density: float | None
    pipe_specific_heat: float | None
    soil_moisture_content_percent: float | None
    soil_moisture_content_percent_at_saturation: float | None
    undisturbed_ground_temperature_model_type: str | None
    undisturbed_ground_temperature_model_name: str | None
    evapotranspiration_ground_cover_parameter: float | None

class GroundHeatExchangerSlinky(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    design_flow_rate: float | None
    soil_thermal_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    pipe_thermal_conductivity: float | None
    pipe_density: float | None
    pipe_specific_heat: float | None
    pipe_outer_diameter: float | None
    pipe_thickness: float | None
    heat_exchanger_configuration: str | None
    coil_diameter: float | None
    coil_pitch: float | None
    trench_depth: float | None
    trench_length: float | None
    number_of_trenches: int | None
    horizontal_spacing_between_pipes: float | None
    undisturbed_ground_temperature_model_type: str | None
    undisturbed_ground_temperature_model_name: str | None
    maximum_length_of_simulation: float | None

class HeatExchangerFluidToFluid(IDFObject):
    availability_schedule_name: str | None
    loop_demand_side_inlet_node_name: str | None
    loop_demand_side_outlet_node_name: str | None
    loop_demand_side_design_flow_rate: float | str | None
    loop_supply_side_inlet_node_name: str | None
    loop_supply_side_outlet_node_name: str | None
    loop_supply_side_design_flow_rate: float | str | None
    heat_exchange_model_type: str | None
    heat_exchanger_u_factor_times_area_value: float | str | None
    control_type: str | None
    heat_exchanger_setpoint_node_name: str | None
    minimum_temperature_difference_to_activate_heat_exchanger: float | None
    heat_transfer_metering_end_use_type: str | None
    component_override_loop_supply_side_inlet_node_name: str | None
    component_override_loop_demand_side_inlet_node_name: str | None
    component_override_cooling_control_temperature_mode: str | None
    sizing_factor: float | None
    operation_minimum_temperature_limit: float | None
    operation_maximum_temperature_limit: float | None

class WaterHeaterMixed(IDFObject):
    tank_volume: float | str | None
    setpoint_temperature_schedule_name: str | None
    deadband_temperature_difference: float | None
    maximum_temperature_limit: float | None
    heater_control_type: str | None
    heater_maximum_capacity: float | str | None
    heater_minimum_capacity: float | None
    heater_ignition_minimum_flow_rate: float | None
    heater_ignition_delay: float | None
    heater_fuel_type: str | None
    heater_thermal_efficiency: float | None
    part_load_factor_curve_name: str | None
    off_cycle_parasitic_fuel_consumption_rate: float | None
    off_cycle_parasitic_fuel_type: str | None
    off_cycle_parasitic_heat_fraction_to_tank: float | None
    on_cycle_parasitic_fuel_consumption_rate: float | None
    on_cycle_parasitic_fuel_type: str | None
    on_cycle_parasitic_heat_fraction_to_tank: float | None
    ambient_temperature_indicator: str | None
    ambient_temperature_schedule_name: str | None
    ambient_temperature_zone_name: str | None
    ambient_temperature_outdoor_air_node_name: str | None
    off_cycle_loss_coefficient_to_ambient_temperature: float | None
    off_cycle_loss_fraction_to_zone: float | None
    on_cycle_loss_coefficient_to_ambient_temperature: float | None
    on_cycle_loss_fraction_to_zone: float | None
    peak_use_flow_rate: float | None
    use_flow_rate_fraction_schedule_name: str | None
    cold_water_supply_temperature_schedule_name: str | None
    use_side_inlet_node_name: str | None
    use_side_outlet_node_name: str | None
    use_side_effectiveness: float | None
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    source_side_effectiveness: float | None
    use_side_design_flow_rate: float | str | None
    source_side_design_flow_rate: float | str | None
    indirect_water_heating_recovery_time: float | None
    source_side_flow_control_mode: str | None
    indirect_alternate_setpoint_temperature_schedule_name: str | None
    end_use_subcategory: str | None

class WaterHeaterStratified(IDFObject):
    end_use_subcategory: str | None
    tank_volume: float | str | None
    tank_height: float | str | None
    tank_shape: str | None
    tank_perimeter: float | None
    maximum_temperature_limit: float | None
    heater_priority_control: str | None
    heater_1_setpoint_temperature_schedule_name: str | None
    heater_1_deadband_temperature_difference: float | None
    heater_1_capacity: float | str | None
    heater_1_height: float | None
    heater_2_setpoint_temperature_schedule_name: str | None
    heater_2_deadband_temperature_difference: float | None
    heater_2_capacity: float | None
    heater_2_height: float | None
    heater_fuel_type: str | None
    heater_thermal_efficiency: float | None
    off_cycle_parasitic_fuel_consumption_rate: float | None
    off_cycle_parasitic_fuel_type: str | None
    off_cycle_parasitic_heat_fraction_to_tank: float | None
    off_cycle_parasitic_height: float | None
    on_cycle_parasitic_fuel_consumption_rate: float | None
    on_cycle_parasitic_fuel_type: str | None
    on_cycle_parasitic_heat_fraction_to_tank: float | None
    on_cycle_parasitic_height: float | None
    ambient_temperature_indicator: str | None
    ambient_temperature_schedule_name: str | None
    ambient_temperature_zone_name: str | None
    ambient_temperature_outdoor_air_node_name: str | None
    uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None
    skin_loss_fraction_to_zone: float | None
    off_cycle_flue_loss_coefficient_to_ambient_temperature: float | None
    off_cycle_flue_loss_fraction_to_zone: float | None
    peak_use_flow_rate: float | None
    use_flow_rate_fraction_schedule_name: str | None
    cold_water_supply_temperature_schedule_name: str | None
    use_side_inlet_node_name: str | None
    use_side_outlet_node_name: str | None
    use_side_effectiveness: float | None
    use_side_inlet_height: float | None
    use_side_outlet_height: float | str | None
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    source_side_effectiveness: float | None
    source_side_inlet_height: float | str | None
    source_side_outlet_height: float | None
    inlet_mode: str | None
    use_side_design_flow_rate: float | str | None
    source_side_design_flow_rate: float | str | None
    indirect_water_heating_recovery_time: float | None
    number_of_nodes: int | None
    additional_destratification_conductivity: float | None
    node_1_additional_loss_coefficient: float | None
    node_2_additional_loss_coefficient: float | None
    node_3_additional_loss_coefficient: float | None
    node_4_additional_loss_coefficient: float | None
    node_5_additional_loss_coefficient: float | None
    node_6_additional_loss_coefficient: float | None
    node_7_additional_loss_coefficient: float | None
    node_8_additional_loss_coefficient: float | None
    node_9_additional_loss_coefficient: float | None
    node_10_additional_loss_coefficient: float | None
    node_11_additional_loss_coefficient: float | None
    node_12_additional_loss_coefficient: float | None
    source_side_flow_control_mode: str | None
    indirect_alternate_setpoint_temperature_schedule_name: str | None

class WaterHeaterSizing(IDFObject):
    design_mode: str | None
    time_storage_can_meet_peak_draw: float | None
    time_for_tank_recovery: float | None
    nominal_tank_volume_for_autosizing_plant_connections: float | None
    number_of_bedrooms: int | None
    number_of_bathrooms: int | None
    storage_capacity_per_person: float | None
    recovery_capacity_per_person: float | None
    storage_capacity_per_floor_area: float | None
    recovery_capacity_per_floor_area: float | None
    number_of_units: float | None
    storage_capacity_per_unit: float | None
    recovery_capacity_perunit: float | None
    storage_capacity_per_collector_area: float | None
    height_aspect_ratio: float | None

class WaterHeaterHeatPumpPumpedCondenser(IDFObject):
    availability_schedule_name: str | None
    compressor_setpoint_temperature_schedule_name: str | None
    dead_band_temperature_difference: float | None
    condenser_water_inlet_node_name: str | None
    condenser_water_outlet_node_name: str | None
    condenser_water_flow_rate: float | str | None
    evaporator_air_flow_rate: float | str | None
    inlet_air_configuration: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_node_name: str | None
    exhaust_air_node_name: str | None
    inlet_air_temperature_schedule_name: str | None
    inlet_air_humidity_schedule_name: str | None
    inlet_air_zone_name: str | None
    tank_object_type: str | None
    tank_name: str | None
    tank_use_side_inlet_node_name: str | None
    tank_use_side_outlet_node_name: str | None
    dx_coil_object_type: str | None
    dx_coil_name: str | None
    minimum_inlet_air_temperature_for_compressor_operation: float | None
    maximum_inlet_air_temperature_for_compressor_operation: float | None
    compressor_location: str | None
    compressor_ambient_temperature_schedule_name: str | None
    fan_object_type: str | None
    fan_name: str | None
    fan_placement: str | None
    on_cycle_parasitic_electric_load: float | None
    off_cycle_parasitic_electric_load: float | None
    parasitic_heat_rejection_location: str | None
    inlet_air_mixer_node_name: str | None
    outlet_air_splitter_node_name: str | None
    inlet_air_mixer_schedule_name: str | None
    tank_element_control_logic: str | None
    control_sensor_1_height_in_stratified_tank: float | None
    control_sensor_1_weight: float | None
    control_sensor_2_height_in_stratified_tank: float | None

class WaterHeaterHeatPumpWrappedCondenser(IDFObject):
    availability_schedule_name: str | None
    compressor_setpoint_temperature_schedule_name: str | None
    dead_band_temperature_difference: float | None
    condenser_bottom_location: float | None
    condenser_top_location: float | None
    evaporator_air_flow_rate: float | str | None
    inlet_air_configuration: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    outdoor_air_node_name: str | None
    exhaust_air_node_name: str | None
    inlet_air_temperature_schedule_name: str | None
    inlet_air_humidity_schedule_name: str | None
    inlet_air_zone_name: str | None
    tank_object_type: str | None
    tank_name: str | None
    tank_use_side_inlet_node_name: str | None
    tank_use_side_outlet_node_name: str | None
    dx_coil_object_type: str | None
    dx_coil_name: str | None
    minimum_inlet_air_temperature_for_compressor_operation: float | None
    maximum_inlet_air_temperature_for_compressor_operation: float | None
    compressor_location: str | None
    compressor_ambient_temperature_schedule_name: str | None
    fan_object_type: str | None
    fan_name: str | None
    fan_placement: str | None
    on_cycle_parasitic_electric_load: float | None
    off_cycle_parasitic_electric_load: float | None
    parasitic_heat_rejection_location: str | None
    inlet_air_mixer_node_name: str | None
    outlet_air_splitter_node_name: str | None
    inlet_air_mixer_schedule_name: str | None
    tank_element_control_logic: str | None
    control_sensor_1_height_in_stratified_tank: float | None
    control_sensor_1_weight: float | None
    control_sensor_2_height_in_stratified_tank: float | None

class ThermalStorageIceSimple(IDFObject):
    ice_storage_type: str | None
    capacity: float | str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    thermal_storage_sizing_object_name: str | None

class ThermalStorageIceDetailed(IDFObject):
    availability_schedule_name: str | None
    capacity: float | str | None
    inlet_node_name: str | None
    outlet_node_name: str | None
    discharging_curve_variable_specifications: str | None
    discharging_curve_name: str | None
    charging_curve_variable_specifications: str | None
    charging_curve_name: str | None
    timestep_of_the_curve_data: float | None
    parasitic_electric_load_during_discharging: float | None
    parasitic_electric_load_during_charging: float | None
    tank_loss_coefficient: float | None
    freezing_temperature_of_storage_medium: float | None
    thaw_process_indicator: str | None
    thermal_storage_sizing_object_name: str | None

class ThermalStorageChilledWaterMixed(IDFObject):
    tank_volume: float | None
    setpoint_temperature_schedule_name: str | None
    deadband_temperature_difference: float | None
    minimum_temperature_limit: float | None
    nominal_cooling_capacity: float | None
    ambient_temperature_indicator: str | None
    ambient_temperature_schedule_name: str | None
    ambient_temperature_zone_name: str | None
    ambient_temperature_outdoor_air_node_name: str | None
    heat_gain_coefficient_from_ambient_temperature: float | None
    use_side_inlet_node_name: str | None
    use_side_outlet_node_name: str | None
    use_side_heat_transfer_effectiveness: float | None
    use_side_availability_schedule_name: str | None
    use_side_design_flow_rate: float | str | None
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    source_side_heat_transfer_effectiveness: float | None
    source_side_availability_schedule_name: str | None
    source_side_design_flow_rate: float | str | None
    tank_recovery_time: float | None

class ThermalStorageChilledWaterStratified(IDFObject):
    tank_volume: float | None
    tank_height: float | None
    tank_shape: str | None
    tank_perimeter: float | None
    setpoint_temperature_schedule_name: str | None
    deadband_temperature_difference: float | None
    temperature_sensor_height: float | None
    minimum_temperature_limit: float | None
    nominal_cooling_capacity: float | str | None
    ambient_temperature_indicator: str | None
    ambient_temperature_schedule_name: str | None
    ambient_temperature_zone_name: str | None
    ambient_temperature_outdoor_air_node_name: str | None
    uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None
    use_side_inlet_node_name: str | None
    use_side_outlet_node_name: str | None
    use_side_heat_transfer_effectiveness: float | None
    use_side_availability_schedule_name: str | None
    use_side_inlet_height: float | str | None
    use_side_outlet_height: float | None
    use_side_design_flow_rate: float | str | None
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    source_side_heat_transfer_effectiveness: float | None
    source_side_availability_schedule_name: str | None
    source_side_inlet_height: float | None
    source_side_outlet_height: float | str | None
    source_side_design_flow_rate: float | str | None
    tank_recovery_time: float | None
    inlet_mode: str | None
    number_of_nodes: int | None
    additional_destratification_conductivity: float | None
    node_1_additional_loss_coefficient: float | None
    node_2_additional_loss_coefficient: float | None
    node_3_additional_loss_coefficient: float | None
    node_4_additional_loss_coefficient: float | None
    node_5_additional_loss_coefficient: float | None
    node_6_additional_loss_coefficient: float | None
    node_7_additional_loss_coefficient: float | None
    node_8_additional_loss_coefficient: float | None
    node_9_additional_loss_coefficient: float | None
    node_10_additional_loss_coefficient: float | None

class ThermalStorageHotWaterStratified(IDFObject):
    tank_volume: float | None
    tank_height: float | None
    tank_shape: str | None
    tank_perimeter: float | None
    top_setpoint_temperature_schedule_name: str | None
    bottom_setpoint_temperature_schedule_name: str | None
    deadband_temperature_difference: float | None
    top_temperature_sensor_height: float | None
    bottom_temperature_sensor_height: float | None
    maximum_temperature_limit: float | None
    nominal_heating_capacity: float | str | None
    ambient_temperature_indicator: str | None
    ambient_temperature_schedule_name: str | None
    ambient_temperature_zone_name: str | None
    ambient_temperature_outdoor_air_node_name: str | None
    uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None
    use_side_inlet_node_name: str | None
    use_side_outlet_node_name: str | None
    use_side_flow_direction_schedule: str | None
    use_side_heat_transfer_effectiveness: float | None
    use_side_availability_schedule_name: str | None
    use_side_inlet_height: float | str | None
    use_side_outlet_height: float | None
    use_side_design_flow_rate: float | str | None
    source_side_inlet_node_name: str | None
    source_side_outlet_node_name: str | None
    source_side_flow_direction_schedule: str | None
    source_side_heat_transfer_effectiveness: float | None
    source_side_availability_schedule_name: str | None
    source_side_inlet_height: float | None
    source_side_outlet_height: float | str | None
    source_side_design_flow_rate: float | str | None
    tank_recovery_time: float | None
    inlet_mode: str | None
    number_of_nodes: int | None
    additional_destratification_conductivity: float | None
    node_1_additional_loss_coefficient: float | None
    node_2_additional_loss_coefficient: float | None
    node_3_additional_loss_coefficient: float | None
    node_4_additional_loss_coefficient: float | None
    node_5_additional_loss_coefficient: float | None
    node_6_additional_loss_coefficient: float | None
    node_7_additional_loss_coefficient: float | None
    node_8_additional_loss_coefficient: float | None
    node_9_additional_loss_coefficient: float | None
    node_10_additional_loss_coefficient: float | None

class ThermalStoragePCM(IDFObject):
    availability_schedule_name: str | None
    plant_side_inlet_node_name: str | None
    plant_side_outlet_node_name: str | None
    use_side_inlet_node_name: str | None
    use_side_outlet_node_name: str | None
    pcm_material_name: str | None
    tank_capacity: float | str | None
    heat_loss_rate: float | None
    use_side_design_flow_rate: float | str | None
    plant_side_design_flow_rate: float | str | None

class ThermalStorageSizing(IDFObject):
    on_peak_period_start_time: float | None
    on_peak_period_end_time: float | None
    sizing_factor: float | None

class PlantLoop(IDFObject):
    fluid_type: str | None
    user_defined_fluid_type: str | None
    plant_equipment_operation_scheme_name: str | None
    loop_temperature_setpoint_node_name: str | None
    maximum_loop_temperature: float | None
    minimum_loop_temperature: float | None
    maximum_loop_flow_rate: float | str | None
    minimum_loop_flow_rate: float | None
    plant_loop_volume: float | str | None
    plant_side_inlet_node_name: str | None
    plant_side_outlet_node_name: str | None
    plant_side_branch_list_name: str | None
    plant_side_connector_list_name: str | None
    demand_side_inlet_node_name: str | None
    demand_side_outlet_node_name: str | None
    demand_side_branch_list_name: str | None
    demand_side_connector_list_name: str | None
    load_distribution_scheme: str | None
    availability_manager_list_name: str | None
    plant_loop_demand_calculation_scheme: str | None
    common_pipe_simulation: str | None
    pressure_simulation_type: str | None
    loop_circulation_time: float | None

class CondenserLoop(IDFObject):
    fluid_type: str | None
    user_defined_fluid_type: str | None
    condenser_equipment_operation_scheme_name: str | None
    condenser_loop_temperature_setpoint_node_name: str | None
    maximum_loop_temperature: float | None
    minimum_loop_temperature: float | None
    maximum_loop_flow_rate: float | str | None
    minimum_loop_flow_rate: float | None
    condenser_loop_volume: float | str | None
    condenser_side_inlet_node_name: str | None
    condenser_side_outlet_node_name: str | None
    condenser_side_branch_list_name: str | None
    condenser_side_connector_list_name: str | None
    demand_side_inlet_node_name: str | None
    demand_side_outlet_node_name: str | None
    condenser_demand_side_branch_list_name: str | None
    condenser_demand_side_connector_list_name: str | None
    load_distribution_scheme: str | None
    pressure_simulation_type: str | None
    loop_circulation_time: float | None

class PlantEquipmentList(IDFObject):
    equipment_object_type: str | None
    equipment_name: str | None

class CondenserEquipmentList(IDFObject):
    equipment_object_type: str | None
    equipment_name: str | None

class PlantEquipmentOperationUncontrolled(IDFObject):
    equipment_list_name: str | None

class PlantEquipmentOperationCoolingLoad(IDFObject):
    load_range_1_lower_limit: float | None
    load_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    load_range_2_lower_limit: float | None
    load_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    load_range_3_lower_limit: float | None
    load_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    load_range_4_lower_limit: float | None
    load_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    load_range_5_lower_limit: float | None
    load_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    load_range_6_lower_limit: float | None
    load_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    load_range_7_lower_limit: float | None
    load_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    load_range_8_lower_limit: float | None
    load_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    load_range_9_lower_limit: float | None
    load_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    load_range_10_lower_limit: float | None
    load_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationHeatingLoad(IDFObject):
    load_range_1_lower_limit: float | None
    load_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    load_range_2_lower_limit: float | None
    load_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    load_range_3_lower_limit: float | None
    load_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    load_range_4_lower_limit: float | None
    load_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    load_range_5_lower_limit: float | None
    load_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    load_range_6_lower_limit: float | None
    load_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    load_range_7_lower_limit: float | None
    load_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    load_range_8_lower_limit: float | None
    load_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    load_range_9_lower_limit: float | None
    load_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    load_range_10_lower_limit: float | None
    load_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationOutdoorDryBulb(IDFObject):
    dry_bulb_temperature_range_1_lower_limit: float | None
    dry_bulb_temperature_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    dry_bulb_temperature_range_2_lower_limit: float | None
    dry_bulb_temperature_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    dry_bulb_temperature_range_3_lower_limit: float | None
    dry_bulb_temperature_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    dry_bulb_temperature_range_4_lower_limit: float | None
    dry_bulb_temperature_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    dry_bulb_temperature_range_5_lower_limit: float | None
    dry_bulb_temperature_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    dry_bulb_temperature_range_6_lower_limit: float | None
    dry_bulb_temperature_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    dry_bulb_temperature_range_7_lower_limit: float | None
    dry_bulb_temperature_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    dry_bulb_temperature_range_8_lower_limit: float | None
    dry_bulb_temperature_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    dry_bulb_temperature_range_9_lower_limit: float | None
    dry_bulb_temperature_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    dry_bulb_temperature_range_10_lower_limit: float | None
    dry_bulb_temperature_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationOutdoorWetBulb(IDFObject):
    wet_bulb_temperature_range_1_lower_limit: float | None
    wet_bulb_temperature_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    wet_bulb_temperature_range_2_lower_limit: float | None
    wet_bulb_temperature_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    wet_bulb_temperature_range_3_lower_limit: float | None
    wet_bulb_temperature_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    wet_bulb_temperature_range_4_lower_limit: float | None
    wet_bulb_temperature_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    wet_bulb_temperature_range_5_lower_limit: float | None
    wet_bulb_temperature_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    wet_bulb_temperature_range_6_lower_limit: float | None
    wet_bulb_temperature_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    wet_bulb_temperature_range_7_lower_limit: float | None
    wet_bulb_temperature_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    wet_bulb_temperature_range_8_lower_limit: float | None
    wet_bulb_temperature_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    wet_bulb_temperature_range_9_lower_limit: float | None
    wet_bulb_temperature_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    wet_bulb_temperature_range_10_lower_limit: float | None
    wet_bulb_temperature_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationOutdoorRelativeHumidity(IDFObject):
    relative_humidity_range_1_lower_limit: float | None
    relative_humidity_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    relative_humidity_range_2_lower_limit: float | None
    relative_humidity_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    relative_humidity_range_3_lower_limit: float | None
    relative_humidity_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    relative_humidity_range_4_lower_limit: float | None
    relative_humidity_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    relative_humidity_range_5_lower_limit: float | None
    relative_humidity_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    relative_humidity_range_6_lower_limit: float | None
    relative_humidity_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    relative_humidity_range_7_lower_limit: float | None
    relative_humidity_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    relative_humidity_range_8_lower_limit: float | None
    relative_humidity_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    relative_humidity_range_9_lower_limit: float | None
    relative_humidity_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    relative_humidity_range_10_lower_limit: float | None
    relative_humidity_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationOutdoorDewpoint(IDFObject):
    dewpoint_temperature_range_1_lower_limit: float | None
    dewpoint_temperature_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    dewpoint_temperature_range_2_lower_limit: float | None
    dewpoint_temperature_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    dewpoint_temperature_range_3_lower_limit: float | None
    dewpoint_temperature_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    dewpoint_temperature_range_4_lower_limit: float | None
    dewpoint_temperature_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    dewpoint_temperature_range_5_lower_limit: float | None
    dewpoint_temperature_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    dewpoint_temperature_range_6_lower_limit: float | None
    dewpoint_temperature_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    dewpoint_temperature_range_7_lower_limit: float | None
    dewpoint_temperature_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    dewpoint_temperature_range_8_lower_limit: float | None
    dewpoint_temperature_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    dewpoint_temperature_range_9_lower_limit: float | None
    dewpoint_temperature_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    dewpoint_temperature_range_10_lower_limit: float | None
    dewpoint_temperature_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationComponentSetpoint(IDFObject):
    equipment_1_object_type: str | None
    equipment_1_name: str | None
    demand_calculation_1_node_name: str | None
    setpoint_1_node_name: str | None
    component_1_flow_rate: float | str | None
    operation_1_type: str | None
    equipment_2_object_type: str | None
    equipment_2_name: str | None
    demand_calculation_2_node_name: str | None
    setpoint_2_node_name: str | None
    component_2_flow_rate: float | str | None
    operation_2_type: str | None
    equipment_3_object_type: str | None
    equipment_3_name: str | None
    demand_calculation_3_node_name: str | None
    setpoint_3_node_name: str | None
    component_3_flow_rate: float | str | None
    operation_3_type: str | None
    equipment_4_object_type: str | None
    equipment_4_name: str | None
    demand_calculation_4_node_name: str | None
    setpoint_4_node_name: str | None
    component_4_flow_rate: float | str | None
    operation_4_type: str | None
    equipment_5_object_type: str | None
    equipment_5_name: str | None
    demand_calculation_5_node_name: str | None
    setpoint_5_node_name: str | None
    component_5_flow_rate: float | str | None
    operation_5_type: str | None
    equipment_6_object_type: str | None
    equipment_6_name: str | None
    demand_calculation_6_node_name: str | None
    setpoint_6_node_name: str | None
    component_6_flow_rate: float | str | None
    operation_6_type: str | None
    equipment_7_object_type: str | None
    equipment_7_name: str | None
    demand_calculation_7_node_name: str | None
    setpoint_7_node_name: str | None
    component_7_flow_rate: float | str | None
    operation_7_type: str | None
    equipment_8_object_type: str | None
    equipment_8_name: str | None
    demand_calculation_8_node_name: str | None
    setpoint_8_node_name: str | None
    component_8_flow_rate: float | str | None
    operation_8_type: str | None
    equipment_9_object_type: str | None
    equipment_9_name: str | None
    demand_calculation_9_node_name: str | None
    setpoint_9_node_name: str | None
    component_9_flow_rate: float | str | None
    operation_9_type: str | None
    equipment_10_object_type: str | None
    equipment_10_name: str | None
    demand_calculation_10_node_name: str | None
    setpoint_10_node_name: str | None
    component_10_flow_rate: float | str | None
    operation_10_type: str | None

class PlantEquipmentOperationThermalEnergyStorage(IDFObject):
    on_peak_schedule: str | None
    charging_availability_schedule: str | None
    non_charging_chilled_water_temperature: float | None
    charging_chilled_water_temperature: float | None
    component_1_object_type: str | None
    component_1_name: str | None
    component_1_demand_calculation_node_name: str | None
    component_1_setpoint_node_name: str | None
    component_1_flow_rate: float | str | None
    component_1_operation_type: str | None
    component_2_object_type: str | None
    component_2_name: str | None
    component_2_demand_calculation_node_name: str | None
    component_2_setpoint_node_name: str | None
    component_2_flow_rate: float | str | None
    component_2_operation_type: str | None
    component_3_object_type: str | None
    component_3_name: str | None
    component_3_demand_calculation_node_name: str | None
    component_3_setpoint_node_name: str | None
    component_3_flow_rate: float | str | None
    component_3_operation_type: str | None
    component_4_object_type: str | None
    component_4_name: str | None
    component_4_demand_calculation_node_name: str | None
    component_4_setpoint_node_name: str | None
    component_4_flow_rate: float | str | None
    component_4_operation_type: str | None
    component_5_object_type: str | None
    component_5_name: str | None
    component_5_demand_calculation_node_name: str | None
    component_5_setpoint_node_name: str | None
    component_5_flow_rate: float | str | None
    component_5_operation_type: str | None
    component_6_object_type: str | None
    component_6_name: str | None
    component_6_demand_calculation_node_name: str | None
    component_6_setpoint_node_name: str | None
    component_6_flow_rate: float | str | None
    component_6_operation_type: str | None
    component_7_object_type: str | None
    component_7_name: str | None
    component_7_demand_calculation_node_name: str | None
    component_7_setpoint_node_name: str | None
    component_7_flow_rate: float | str | None
    component_7_operation_type: str | None
    component_8_object_type: str | None
    component_8_name: str | None
    component_8_demand_calculation_node_name: str | None
    component_8_setpoint_node_name: str | None
    component_8_flow_rate: float | str | None
    component_8_operation_type: str | None
    component_9_object_type: str | None
    component_9_name: str | None
    component_9_demand_calculation_node_name: str | None
    component_9_setpoint_node_name: str | None
    component_9_flow_rate: float | str | None
    component_9_operation_type: str | None
    component_10_object_type: str | None
    component_10_name: str | None
    component_10_demand_calculation_node_name: str | None
    component_10_setpoint_node_name: str | None
    component_10_flow_rate: float | str | None
    component_10_operation_type: str | None

class PlantEquipmentOperationOutdoorDryBulbDifference(IDFObject):
    reference_temperature_node_name: str | None
    dry_bulb_temperature_difference_range_1_lower_limit: float | None
    dry_bulb_temperature_difference_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_2_lower_limit: float | None
    dry_bulb_temperature_difference_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_3_lower_limit: float | None
    dry_bulb_temperature_difference_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_4_lower_limit: float | None
    dry_bulb_temperature_difference_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_5_lower_limit: float | None
    dry_bulb_temperature_difference_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_6_lower_limit: float | None
    dry_bulb_temperature_difference_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_7_lower_limit: float | None
    dry_bulb_temperature_difference_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_8_lower_limit: float | None
    dry_bulb_temperature_difference_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_9_lower_limit: float | None
    dry_bulb_temperature_difference_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    dry_bulb_temperature_difference_range_10_lower_limit: float | None
    dry_bulb_temperature_difference_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationOutdoorWetBulbDifference(IDFObject):
    reference_temperature_node_name: str | None
    wet_bulb_temperature_difference_range_1_lower_limit: float | None
    wet_bulb_temperature_difference_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_2_lower_limit: float | None
    wet_bulb_temperature_difference_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_3_lower_limit: float | None
    wet_bulb_temperature_difference_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_4_lower_limit: float | None
    wet_bulb_temperature_difference_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_5_lower_limit: float | None
    wet_bulb_temperature_difference_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_6_lower_limit: float | None
    wet_bulb_temperature_difference_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_7_lower_limit: float | None
    wet_bulb_temperature_difference_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_8_lower_limit: float | None
    wet_bulb_temperature_difference_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_9_lower_limit: float | None
    wet_bulb_temperature_difference_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    wet_bulb_temperature_difference_range_10_lower_limit: float | None
    wet_bulb_temperature_difference_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationOutdoorDewpointDifference(IDFObject):
    reference_temperature_node_name: str | None
    dewpoint_temperature_difference_range_1_lower_limit: float | None
    dewpoint_temperature_difference_range_1_upper_limit: float | None
    range_1_equipment_list_name: str | None
    dewpoint_temperature_difference_range_2_lower_limit: float | None
    dewpoint_temperature_difference_range_2_upper_limit: float | None
    range_2_equipment_list_name: str | None
    dewpoint_temperature_difference_range_3_lower_limit: float | None
    dewpoint_temperature_difference_range_3_upper_limit: float | None
    range_3_equipment_list_name: str | None
    dewpoint_temperature_difference_range_4_lower_limit: float | None
    dewpoint_temperature_difference_range_4_upper_limit: float | None
    range_4_equipment_list_name: str | None
    dewpoint_temperature_difference_range_5_lower_limit: float | None
    dewpoint_temperature_difference_range_5_upper_limit: float | None
    range_5_equipment_list_name: str | None
    dewpoint_temperature_difference_range_6_lower_limit: float | None
    dewpoint_temperature_difference_range_6_upper_limit: float | None
    range_6_equipment_list_name: str | None
    dewpoint_temperature_difference_range_7_lower_limit: float | None
    dewpoint_temperature_difference_range_7_upper_limit: float | None
    range_7_equipment_list_name: str | None
    dewpoint_temperature_difference_range_8_lower_limit: float | None
    dewpoint_temperature_difference_range_8_upper_limit: float | None
    range_8_equipment_list_name: str | None
    dewpoint_temperature_difference_range_9_lower_limit: float | None
    dewpoint_temperature_difference_range_9_upper_limit: float | None
    range_9_equipment_list_name: str | None
    dewpoint_temperature_difference_range_10_lower_limit: float | None
    dewpoint_temperature_difference_range_10_upper_limit: float | None
    range_10_equipment_list_name: str | None

class PlantEquipmentOperationChillerHeaterChangeover(IDFObject):
    primary_cooling_plant_setpoint_temperature: float | None
    secondary_distribution_cooling_plant_setpoint_temperature: float | None
    primary_heating_plant_setpoint_at_outdoor_high_temperature: float | None
    outdoor_high_temperature: float | None
    primary_heating_plant_setpoint_at_outdoor_low_temperature: float | None
    outdoor_low_temperature: float | None
    secondary_distribution_heating_plant_setpoint_temperature: float | None
    zone_load_polling_zonelist_name: str | None
    cooling_only_load_plant_equipment_operation_cooling_load_name: str | None
    heating_only_load_plant_equipment_operation_heating_load_name: str | None
    simultaneous_cooling_and_heating_plant_equipment_operation_cooling_load_name: str | None
    simultaneous_cooling_and_heating_plant_equipment_operation_heating_load_name: str | None
    dedicated_chilled_water_return_recovery_heat_pump_name: str | None
    dedicated_hot_water_return_recovery_heat_pump_name: str | None
    boiler_setpoint_temperature_offset: float | None
    primary_heating_plant_setpoint_at_backup_outdoor_low_temperature: float | None
    backup_outdoor_low_temperature: float | None

class PlantEquipmentOperationSchemes(IDFObject):
    control_scheme_1_object_type: str | None
    control_scheme_1_name: str | None
    control_scheme_1_schedule_name: str | None
    control_scheme_2_object_type: str | None
    control_scheme_2_name: str | None
    control_scheme_2_schedule_name: str | None
    control_scheme_3_object_type: str | None
    control_scheme_3_name: str | None
    control_scheme_3_schedule_name: str | None
    control_scheme_4_object_type: str | None
    control_scheme_4_name: str | None
    control_scheme_4_schedule_name: str | None
    control_scheme_5_object_type: str | None
    control_scheme_5_name: str | None
    control_scheme_5_schedule_name: str | None
    control_scheme_6_object_type: str | None
    control_scheme_6_name: str | None
    control_scheme_6_schedule_name: str | None
    control_scheme_7_object_type: str | None
    control_scheme_7_name: str | None
    control_scheme_7_schedule_name: str | None
    control_scheme_8_object_type: str | None
    control_scheme_8_name: str | None
    control_scheme_8_schedule_name: str | None

class CondenserEquipmentOperationSchemes(IDFObject):
    control_scheme_1_object_type: str | None
    control_scheme_1_name: str | None
    control_scheme_1_schedule_name: str | None
    control_scheme_2_object_type: str | None
    control_scheme_2_name: str | None
    control_scheme_2_schedule_name: str | None
    control_scheme_3_object_type: str | None
    control_scheme_3_name: str | None
    control_scheme_3_schedule_name: str | None
    control_scheme_4_object_type: str | None
    control_scheme_4_name: str | None
    control_scheme_4_schedule_name: str | None
    control_scheme_5_object_type: str | None
    control_scheme_5_name: str | None
    control_scheme_5_schedule_name: str | None
    control_scheme_6_object_type: str | None
    control_scheme_6_name: str | None
    control_scheme_6_schedule_name: str | None
    control_scheme_7_object_type: str | None
    control_scheme_7_name: str | None
    control_scheme_7_schedule_name: str | None
    control_scheme_8_object_type: str | None
    control_scheme_8_name: str | None
    control_scheme_8_schedule_name: str | None

class EnergyManagementSystemSensor(IDFObject):
    output_variable_or_output_meter_index_key_name: str | None
    output_variable_or_output_meter_name: str | None

class EnergyManagementSystemActuator(IDFObject):
    actuated_component_unique_name: str | None
    actuated_component_type: str | None
    actuated_component_control_type: str | None

class EnergyManagementSystemProgramCallingManager(IDFObject):
    energyplus_model_calling_point: str | None
    program_name: str | None

class EnergyManagementSystemProgram(IDFObject):
    program_line: str | None

class EnergyManagementSystemSubroutine(IDFObject):
    program_line: str | None

class EnergyManagementSystemGlobalVariable(IDFObject):
    erl_variable_name: str | None

class EnergyManagementSystemOutputVariable(IDFObject):
    ems_variable_name: str | None
    type_of_data_in_variable: str | None
    update_frequency: str | None
    ems_program_or_subroutine_name: str | None
    units: str | None

class EnergyManagementSystemMeteredOutputVariable(IDFObject):
    ems_variable_name: str | None
    update_frequency: str | None
    ems_program_or_subroutine_name: str | None
    resource_type: str | None
    group_type: str | None
    end_use_category: str | None
    end_use_subcategory: str | None
    units: str | None

class EnergyManagementSystemTrendVariable(IDFObject):
    ems_variable_name: str | None
    number_of_timesteps_to_be_logged: int | None

class EnergyManagementSystemInternalVariable(IDFObject):
    internal_data_index_key_name: str | None
    internal_data_type: str | None

class EnergyManagementSystemCurveOrTableIndexVariable(IDFObject):
    curve_or_table_object_name: str | None

class EnergyManagementSystemConstructionIndexVariable(IDFObject):
    construction_object_name: str | None

class ExternalInterface(IDFObject): ...

class ExternalInterfaceSchedule(IDFObject):
    schedule_type_limits_name: str | None
    initial_value: float | None

class ExternalInterfaceVariable(IDFObject):
    initial_value: float | None

class ExternalInterfaceActuator(IDFObject):
    actuated_component_unique_name: str | None
    actuated_component_type: str | None
    actuated_component_control_type: str | None
    optional_initial_value: float | None

class ExternalInterfaceFunctionalMockupUnitImport(IDFObject):
    fmu_timeout: float | None
    fmu_loggingon: int | None

class ExternalInterfaceFunctionalMockupUnitImportFromVariable(IDFObject):
    output_variable_name: str | None
    fmu_file_name: str | None
    fmu_instance_name: str | None
    fmu_variable_name: str | None

class ExternalInterfaceFunctionalMockupUnitImportToSchedule(IDFObject):
    schedule_type_limits_names: str | None
    fmu_file_name: str | None
    fmu_instance_name: str | None
    fmu_variable_name: str | None
    initial_value: float | None

class ExternalInterfaceFunctionalMockupUnitImportToActuator(IDFObject):
    actuated_component_unique_name: str | None
    actuated_component_type: str | None
    actuated_component_control_type: str | None
    fmu_file_name: str | None
    fmu_instance_name: str | None
    fmu_variable_name: str | None
    initial_value: float | None

class ExternalInterfaceFunctionalMockupUnitImportToVariable(IDFObject):
    fmu_file_name: str | None
    fmu_instance_name: str | None
    fmu_variable_name: str | None
    initial_value: float | None

class ExternalInterfaceFunctionalMockupUnitExportFromVariable(IDFObject):
    output_variable_name: str | None
    fmu_variable_name: str | None

class ExternalInterfaceFunctionalMockupUnitExportToSchedule(IDFObject):
    schedule_type_limits_names: str | None
    fmu_variable_name: str | None
    initial_value: float | None

class ExternalInterfaceFunctionalMockupUnitExportToActuator(IDFObject):
    actuated_component_unique_name: str | None
    actuated_component_type: str | None
    actuated_component_control_type: str | None
    fmu_variable_name: str | None
    initial_value: float | None

class ExternalInterfaceFunctionalMockupUnitExportToVariable(IDFObject):
    fmu_variable_name: str | None
    initial_value: float | None

class ZoneHVACForcedAirUserDefined(IDFObject):
    overall_model_simulation_program_calling_manager_name: str | None
    model_setup_and_sizing_program_calling_manager_name: str | None
    primary_air_inlet_node_name: str | None
    primary_air_outlet_node_name: str | None
    secondary_air_inlet_node_name: str | None
    secondary_air_outlet_node_name: str | None
    number_of_plant_loop_connections: int | None
    plant_connection_1_inlet_node_name: str | None
    plant_connection_1_outlet_node_name: str | None
    plant_connection_2_inlet_node_name: str | None
    plant_connection_2_outlet_node_name: str | None
    plant_connection_3_inlet_node_name: str | None
    plant_connection_3_outlet_node_name: str | None
    supply_inlet_water_storage_tank_name: str | None
    collection_outlet_water_storage_tank_name: str | None
    ambient_zone_name: str | None

class AirTerminalSingleDuctUserDefined(IDFObject):
    overall_model_simulation_program_calling_manager_name: str | None
    model_setup_and_sizing_program_calling_manager_name: str | None
    primary_air_inlet_node_name: str | None
    primary_air_outlet_node_name: str | None
    secondary_air_inlet_node_name: str | None
    secondary_air_outlet_node_name: str | None
    number_of_plant_loop_connections: int | None
    plant_connection_1_inlet_node_name: str | None
    plant_connection_1_outlet_node_name: str | None
    plant_connection_2_inlet_node_name: str | None
    plant_connection_2_outlet_node_name: str | None
    supply_inlet_water_storage_tank_name: str | None
    collection_outlet_water_storage_tank_name: str | None
    ambient_zone_name: str | None

class CoilUserDefined(IDFObject):
    overall_model_simulation_program_calling_manager_name: str | None
    model_setup_and_sizing_program_calling_manager_name: str | None
    number_of_air_connections: int | None
    air_connection_1_inlet_node_name: str | None
    air_connection_1_outlet_node_name: str | None
    air_connection_2_inlet_node_name: str | None
    air_connection_2_outlet_node_name: str | None
    plant_connection_is_used: str | None
    plant_connection_inlet_node_name: str | None
    plant_connection_outlet_node_name: str | None
    supply_inlet_water_storage_tank_name: str | None
    collection_outlet_water_storage_tank_name: str | None
    ambient_zone_name: str | None

class PlantComponentUserDefined(IDFObject):
    main_model_program_calling_manager_name: str | None
    number_of_plant_loop_connections: int | None
    plant_connection_1_inlet_node_name: str | None
    plant_connection_1_outlet_node_name: str | None
    plant_connection_1_loading_mode: str | None
    plant_connection_1_loop_flow_request_mode: str | None
    plant_connection_1_initialization_program_calling_manager_name: str | None
    plant_connection_1_simulation_program_calling_manager_name: str | None
    plant_connection_2_inlet_node_name: str | None
    plant_connection_2_outlet_node_name: str | None
    plant_connection_2_loading_mode: str | None
    plant_connection_2_loop_flow_request_mode: str | None
    plant_connection_2_initialization_program_calling_manager_name: str | None
    plant_connection_2_simulation_program_calling_manager_name: str | None
    plant_connection_3_inlet_node_name: str | None
    plant_connection_3_outlet_node_name: str | None
    plant_connection_3_loading_mode: str | None
    plant_connection_3_loop_flow_request_mode: str | None
    plant_connection_3_initialization_program_calling_manager_name: str | None
    plant_connection_3_simulation_program_calling_manager_name: str | None
    plant_connection_4_inlet_node_name: str | None
    plant_connection_4_outlet_node_name: str | None
    plant_connection_4_loading_mode: str | None
    plant_connection_4_loop_flow_request_mode: str | None
    plant_connection_4_initialization_program_calling_manager_name: str | None
    plant_connection_4_simulation_program_calling_manager_name: str | None
    air_connection_inlet_node_name: str | None
    air_connection_outlet_node_name: str | None
    supply_inlet_water_storage_tank_name: str | None
    collection_outlet_water_storage_tank_name: str | None
    ambient_zone_name: str | None

class PlantEquipmentOperationUserDefined(IDFObject):
    main_model_program_calling_manager_name: str | None
    initialization_program_calling_manager_name: str | None
    equipment_1_object_type: str | None
    equipment_1_name: str | None
    equipment_2_object_type: str | None
    equipment_2_name: str | None
    equipment_3_object_type: str | None
    equipment_3_name: str | None
    equipment_4_object_type: str | None
    equipment_4_name: str | None
    equipment_5_object_type: str | None
    equipment_5_name: str | None
    equipment_6_object_type: str | None
    equipment_6_name: str | None
    equipment_7_object_type: str | None
    equipment_7_name: str | None
    equipment_8_object_type: str | None
    equipment_8_name: str | None
    equipment_9_object_type: str | None
    equipment_9_name: str | None
    equipment_10_object_type: str | None
    equipment_10_name: str | None

class AvailabilityManagerScheduled(IDFObject):
    schedule_name: str | None

class AvailabilityManagerScheduledOn(IDFObject):
    schedule_name: str | None

class AvailabilityManagerScheduledOff(IDFObject):
    schedule_name: str | None

class AvailabilityManagerOptimumStart(IDFObject):
    applicability_schedule_name: str | None
    fan_schedule_name: str | None
    control_type: str | None
    control_zone_name: str | None
    zone_list_name: str | None
    maximum_value_for_optimum_start_time: float | None
    control_algorithm: str | None
    constant_temperature_gradient_during_cooling: float | None
    constant_temperature_gradient_during_heating: float | None
    initial_temperature_gradient_during_cooling: float | None
    initial_temperature_gradient_during_heating: float | None
    constant_start_time: float | None
    number_of_previous_days: int | None

class AvailabilityManagerNightCycle(IDFObject):
    applicability_schedule_name: str | None
    fan_schedule_name: str | None
    control_type: str | None
    thermostat_tolerance: float | None
    cycling_run_time_control_type: str | None
    cycling_run_time: float | None
    control_zone_or_zone_list_name: str | None
    cooling_control_zone_or_zone_list_name: str | None
    heating_control_zone_or_zone_list_name: str | None
    heating_zone_fans_only_zone_or_zone_list_name: str | None

class AvailabilityManagerDifferentialThermostat(IDFObject):
    hot_node_name: str | None
    cold_node_name: str | None
    temperature_difference_on_limit: float | None
    temperature_difference_off_limit: float | None

class AvailabilityManagerHighTemperatureTurnOff(IDFObject):
    sensor_node_name: str | None
    temperature: float | None

class AvailabilityManagerHighTemperatureTurnOn(IDFObject):
    sensor_node_name: str | None
    temperature: float | None

class AvailabilityManagerLowTemperatureTurnOff(IDFObject):
    sensor_node_name: str | None
    temperature: float | None
    applicability_schedule_name: str | None

class AvailabilityManagerLowTemperatureTurnOn(IDFObject):
    sensor_node_name: str | None
    temperature: float | None

class AvailabilityManagerNightVentilation(IDFObject):
    applicability_schedule_name: str | None
    fan_schedule_name: str | None
    ventilation_temperature_schedule_name: str | None
    ventilation_temperature_difference: float | None
    ventilation_temperature_low_limit: float | None
    night_venting_flow_fraction: float | None
    control_zone_name: str | None

class AvailabilityManagerHybridVentilation(IDFObject):
    hvac_air_loop_name: str | None
    control_zone_name: str | None
    ventilation_control_mode_schedule_name: str | None
    use_weather_file_rain_indicators: str | None
    maximum_wind_speed: float | None
    minimum_outdoor_temperature: float | None
    maximum_outdoor_temperature: float | None
    minimum_outdoor_enthalpy: float | None
    maximum_outdoor_enthalpy: float | None
    minimum_outdoor_dewpoint: float | None
    maximum_outdoor_dewpoint: float | None
    minimum_outdoor_ventilation_air_schedule_name: str | None
    opening_factor_function_of_wind_speed_curve_name: str | None
    airflownetwork_control_type_schedule_name: str | None
    simple_airflow_control_type_schedule_name: str | None
    zoneventilation_object_name: str | None
    minimum_hvac_operation_time: float | None
    minimum_ventilation_time: float | None

class AvailabilityManagerAssignmentList(IDFObject):
    availability_manager_object_type: str | None
    availability_manager_name: str | None

class SetpointManagerScheduled(IDFObject):
    control_variable: str | None
    schedule_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerScheduledDualSetpoint(IDFObject):
    control_variable: str | None
    high_setpoint_schedule_name: str | None
    low_setpoint_schedule_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerOutdoorAirReset(IDFObject):
    control_variable: str | None
    setpoint_at_outdoor_low_temperature: float | None
    outdoor_low_temperature: float | None
    setpoint_at_outdoor_high_temperature: float | None
    outdoor_high_temperature: float | None
    setpoint_node_or_nodelist_name: str | None
    schedule_name: str | None
    setpoint_at_outdoor_low_temperature_2: float | None
    outdoor_low_temperature_2: float | None
    setpoint_at_outdoor_high_temperature_2: float | None
    outdoor_high_temperature_2: float | None

class SetpointManagerSingleZoneReheat(IDFObject):
    control_variable: str | None
    minimum_supply_air_temperature: float | None
    maximum_supply_air_temperature: float | None
    control_zone_name: str | None
    zone_node_name: str | None
    zone_inlet_node_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerSingleZoneHeating(IDFObject):
    control_variable: str | None
    minimum_supply_air_temperature: float | None
    maximum_supply_air_temperature: float | None
    control_zone_name: str | None
    zone_node_name: str | None
    zone_inlet_node_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerSingleZoneCooling(IDFObject):
    control_variable: str | None
    minimum_supply_air_temperature: float | None
    maximum_supply_air_temperature: float | None
    control_zone_name: str | None
    zone_node_name: str | None
    zone_inlet_node_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerSingleZoneHumidityMinimum(IDFObject):
    setpoint_node_or_nodelist_name: str | None
    control_zone_air_node_name: str | None

class SetpointManagerSingleZoneHumidityMaximum(IDFObject):
    setpoint_node_or_nodelist_name: str | None
    control_zone_air_node_name: str | None

class SetpointManagerMixedAir(IDFObject):
    control_variable: str | None
    reference_setpoint_node_name: str | None
    fan_inlet_node_name: str | None
    fan_outlet_node_name: str | None
    setpoint_node_or_nodelist_name: str | None
    cooling_coil_inlet_node_name: str | None
    cooling_coil_outlet_node_name: str | None
    minimum_temperature_at_cooling_coil_outlet_node: float | None

class SetpointManagerOutdoorAirPretreat(IDFObject):
    control_variable: str | None
    minimum_setpoint_temperature: float | None
    maximum_setpoint_temperature: float | None
    minimum_setpoint_humidity_ratio: float | None
    maximum_setpoint_humidity_ratio: float | None
    reference_setpoint_node_name: str | None
    mixed_air_stream_node_name: str | None
    outdoor_air_stream_node_name: str | None
    return_air_stream_node_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerWarmest(IDFObject):
    control_variable: str | None
    hvac_air_loop_name: str | None
    minimum_setpoint_temperature: float | None
    maximum_setpoint_temperature: float | None
    strategy: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerColdest(IDFObject):
    control_variable: str | None
    hvac_air_loop_name: str | None
    minimum_setpoint_temperature: float | None
    maximum_setpoint_temperature: float | None
    strategy: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerReturnAirBypassFlow(IDFObject):
    control_variable: str | None
    hvac_air_loop_name: str | None
    temperature_setpoint_schedule_name: str | None

class SetpointManagerWarmestTemperatureFlow(IDFObject):
    control_variable: str | None
    hvac_air_loop_name: str | None
    minimum_setpoint_temperature: float | None
    maximum_setpoint_temperature: float | None
    strategy: str | None
    setpoint_node_or_nodelist_name: str | None
    minimum_turndown_ratio: float | None

class SetpointManagerMultiZoneHeatingAverage(IDFObject):
    hvac_air_loop_name: str | None
    minimum_setpoint_temperature: float | None
    maximum_setpoint_temperature: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerMultiZoneCoolingAverage(IDFObject):
    hvac_air_loop_name: str | None
    minimum_setpoint_temperature: float | None
    maximum_setpoint_temperature: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerMultiZoneMinimumHumidityAverage(IDFObject):
    hvac_air_loop_name: str | None
    minimum_setpoint_humidity_ratio: float | None
    maximum_setpoint_humidity_ratio: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerMultiZoneMaximumHumidityAverage(IDFObject):
    hvac_air_loop_name: str | None
    minimum_setpoint_humidity_ratio: float | None
    maximum_setpoint_humidity_ratio: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerMultiZoneHumidityMinimum(IDFObject):
    hvac_air_loop_name: str | None
    minimum_setpoint_humidity_ratio: float | None
    maximum_setpoint_humidity_ratio: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerMultiZoneHumidityMaximum(IDFObject):
    hvac_air_loop_name: str | None
    minimum_setpoint_humidity_ratio: float | None
    maximum_setpoint_humidity_ratio: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerFollowOutdoorAirTemperature(IDFObject):
    control_variable: str | None
    reference_temperature_type: str | None
    offset_temperature_difference: float | None
    maximum_setpoint_temperature: float | None
    minimum_setpoint_temperature: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerFollowSystemNodeTemperature(IDFObject):
    control_variable: str | None
    reference_node_name: str | None
    reference_temperature_type: str | None
    offset_temperature_difference: float | None
    maximum_limit_setpoint_temperature: float | None
    minimum_limit_setpoint_temperature: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerFollowGroundTemperature(IDFObject):
    control_variable: str | None
    reference_ground_temperature_object_type: str | None
    offset_temperature_difference: float | None
    maximum_setpoint_temperature: float | None
    minimum_setpoint_temperature: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerCondenserEnteringReset(IDFObject):
    control_variable: str | None
    default_condenser_entering_water_temperature_schedule_name: str | None
    minimum_design_wetbulb_temperature_curve_name: str | None
    minimum_outside_air_wetbulb_temperature_curve_name: str | None
    optimized_cond_entering_water_temperature_curve_name: str | None
    minimum_lift: float | None
    maximum_condenser_entering_water_temperature: float | None
    cooling_tower_design_inlet_air_wet_bulb_temperature: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerCondenserEnteringResetIdeal(IDFObject):
    control_variable: str | None
    minimum_lift: float | None
    maximum_condenser_entering_water_temperature: float | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerSingleZoneOneStageCooling(IDFObject):
    cooling_stage_on_supply_air_setpoint_temperature: float | None
    cooling_stage_off_supply_air_setpoint_temperature: float | None
    control_zone_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerSingleZoneOneStageHeating(IDFObject):
    heating_stage_on_supply_air_setpoint_temperature: float | None
    heating_stage_off_supply_air_setpoint_temperature: float | None
    control_zone_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerReturnTemperatureChilledWater(IDFObject):
    plant_loop_supply_outlet_node: str | None
    plant_loop_supply_inlet_node: str | None
    minimum_supply_temperature_setpoint: float | None
    maximum_supply_temperature_setpoint: float | None
    return_temperature_setpoint_input_type: str | None
    return_temperature_setpoint_constant_value: float | None
    return_temperature_setpoint_schedule_name: str | None

class SetpointManagerReturnTemperatureHotWater(IDFObject):
    plant_loop_supply_outlet_node: str | None
    plant_loop_supply_inlet_node: str | None
    minimum_supply_temperature_setpoint: float | None
    maximum_supply_temperature_setpoint: float | None
    return_temperature_setpoint_input_type: str | None
    return_temperature_setpoint_constant_value: float | None
    return_temperature_setpoint_schedule_name: str | None

class SetpointManagerSystemNodeResetTemperature(IDFObject):
    control_variable: str | None
    setpoint_at_low_reference_temperature: float | None
    setpoint_at_high_reference_temperature: float | None
    low_reference_temperature: float | None
    high_reference_temperature: float | None
    reference_node_name: str | None
    setpoint_node_or_nodelist_name: str | None

class SetpointManagerSystemNodeResetHumidity(IDFObject):
    control_variable: str | None
    setpoint_at_low_reference_humidity_ratio: float | None
    setpoint_at_high_reference_humidity_ratio: float | None
    low_reference_humidity_ratio: float | None
    high_reference_humidity_ratio: float | None
    reference_node_name: str | None
    setpoint_node_or_nodelist_name: str | None

class RefrigerationCase(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    rated_ambient_temperature: float | None
    rated_ambient_relative_humidity: float | None
    rated_total_cooling_capacity_per_unit_length: float | None
    rated_latent_heat_ratio: float | None
    rated_runtime_fraction: float | None
    case_length: float | None
    case_operating_temperature: float | None
    latent_case_credit_curve_type: str | None
    latent_case_credit_curve_name: str | None
    standard_case_fan_power_per_unit_length: float | None
    operating_case_fan_power_per_unit_length: float | None
    standard_case_lighting_power_per_unit_length: float | None
    installed_case_lighting_power_per_unit_length: float | None
    case_lighting_schedule_name: str | None
    fraction_of_lighting_energy_to_case: float | None
    case_anti_sweat_heater_power_per_unit_length: float | None
    minimum_anti_sweat_heater_power_per_unit_length: float | None
    anti_sweat_heater_control_type: str | None
    humidity_at_zero_anti_sweat_heater_energy: float | None
    case_height: float | None
    fraction_of_anti_sweat_heater_energy_to_case: float | None
    case_defrost_power_per_unit_length: float | None
    case_defrost_type: str | None
    case_defrost_schedule_name: str | None
    case_defrost_drip_down_schedule_name: str | None
    defrost_energy_correction_curve_type: str | None
    defrost_energy_correction_curve_name: str | None
    under_case_hvac_return_air_fraction: float | None
    refrigerated_case_restocking_schedule_name: str | None
    case_credit_fraction_schedule_name: str | None
    design_evaporator_temperature_or_brine_inlet_temperature: float | None
    average_refrigerant_charge_inventory: float | None
    under_case_hvac_return_air_node_name: str | None

class RefrigerationCompressorRack(IDFObject):
    heat_rejection_location: str | None
    design_compressor_rack_cop: float | None
    compressor_rack_cop_function_of_temperature_curve_name: str | None
    design_condenser_fan_power: float | None
    condenser_fan_power_function_of_temperature_curve_name: str | None
    condenser_type: str | None
    water_cooled_condenser_inlet_node_name: str | None
    water_cooled_condenser_outlet_node_name: str | None
    water_cooled_loop_flow_type: str | None
    water_cooled_condenser_outlet_temperature_schedule_name: str | None
    water_cooled_condenser_design_flow_rate: float | None
    water_cooled_condenser_maximum_flow_rate: float | None
    water_cooled_condenser_maximum_water_outlet_temperature: float | None
    water_cooled_condenser_minimum_water_inlet_temperature: float | None
    evaporative_condenser_availability_schedule_name: str | None
    evaporative_condenser_effectiveness: float | None
    evaporative_condenser_air_flow_rate: float | str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    design_evaporative_condenser_water_pump_power: float | str | None
    evaporative_water_supply_tank_name: str | None
    condenser_air_inlet_node_name: str | None
    end_use_subcategory: str | None
    refrigeration_case_name_or_walkin_name_or_caseandwalkinlist_name: str | None
    heat_rejection_zone_name: str | None

class RefrigerationCaseAndWalkInList(IDFObject):
    case_or_walkin_name: str | None

class RefrigerationCondenserAirCooled(IDFObject):
    rated_effective_total_heat_rejection_rate_curve_name: str | None
    rated_subcooling_temperature_difference: float | None
    condenser_fan_speed_control_type: str | None
    rated_fan_power: float | None
    minimum_fan_air_flow_ratio: float | None
    air_inlet_node_name_or_zone_name: str | None
    end_use_subcategory: str | None
    condenser_refrigerant_operating_charge_inventory: float | None
    condensate_receiver_refrigerant_inventory: float | None
    condensate_piping_refrigerant_inventory: float | None

class RefrigerationCondenserEvaporativeCooled(IDFObject):
    rated_effective_total_heat_rejection_rate: float | None
    rated_subcooling_temperature_difference: float | None
    fan_speed_control_type: str | None
    rated_fan_power: float | None
    minimum_fan_air_flow_ratio: float | None
    approach_temperature_constant_term: float | None
    approach_temperature_coefficient_2: float | None
    approach_temperature_coefficient_3: float | None
    approach_temperature_coefficient_4: float | None
    minimum_capacity_factor: float | None
    maximum_capacity_factor: float | None
    air_inlet_node_name: str | None
    rated_air_flow_rate: float | str | None
    basin_heater_capacity: float | None
    basin_heater_setpoint_temperature: float | None
    rated_water_pump_power: float | str | None
    evaporative_water_supply_tank_name: str | None
    evaporative_condenser_availability_schedule_name: str | None
    end_use_subcategory: str | None
    condenser_refrigerant_operating_charge_inventory: float | None
    condensate_receiver_refrigerant_inventory: float | None
    condensate_piping_refrigerant_inventory: float | None

class RefrigerationCondenserWaterCooled(IDFObject):
    rated_effective_total_heat_rejection_rate: float | None
    rated_condensing_temperature: float | None
    rated_subcooling_temperature_difference: float | None
    rated_water_inlet_temperature: float | None
    water_inlet_node_name: str | None
    water_outlet_node_name: str | None
    water_cooled_loop_flow_type: str | None
    water_outlet_temperature_schedule_name: str | None
    water_design_flow_rate: float | None
    water_maximum_flow_rate: float | None
    water_maximum_water_outlet_temperature: float | None
    water_minimum_water_inlet_temperature: float | None
    end_use_subcategory: str | None
    condenser_refrigerant_operating_charge_inventory: float | None
    condensate_receiver_refrigerant_inventory: float | None
    condensate_piping_refrigerant_inventory: float | None

class RefrigerationCondenserCascade(IDFObject):
    rated_condensing_temperature: float | None
    rated_approach_temperature_difference: float | None
    rated_effective_total_heat_rejection_rate: float | None
    condensing_temperature_control_type: str | None
    condenser_refrigerant_operating_charge_inventory: float | None
    condensate_receiver_refrigerant_inventory: float | None
    condensate_piping_refrigerant_inventory: float | None

class RefrigerationGasCoolerAirCooled(IDFObject):
    rated_total_heat_rejection_rate_curve_name: str | None
    gas_cooler_fan_speed_control_type: str | None
    rated_fan_power: float | None
    minimum_fan_air_flow_ratio: float | None
    transition_temperature: float | None
    transcritical_approach_temperature: float | None
    subcritical_temperature_difference: float | None
    minimum_condensing_temperature: float | None
    air_inlet_node_name: str | None
    end_use_subcategory: str | None
    gas_cooler_refrigerant_operating_charge_inventory: float | None
    gas_cooler_receiver_refrigerant_inventory: float | None
    gas_cooler_outlet_piping_refrigerant_inventory: float | None

class RefrigerationTransferLoadList(IDFObject):
    cascade_condenser_name_or_secondary_system_name: str | None

class RefrigerationSubcooler(IDFObject):
    subcooler_type: str | None
    liquid_suction_design_subcooling_temperature_difference: float | None
    design_liquid_inlet_temperature: float | None
    design_vapor_inlet_temperature: float | None
    capacity_providing_system: str | None
    outlet_control_temperature: float | None

class RefrigerationCompressor(IDFObject):
    refrigeration_compressor_power_curve_name: str | None
    refrigeration_compressor_capacity_curve_name: str | None
    rated_superheat: float | None
    rated_return_gas_temperature: float | None
    rated_liquid_temperature: float | None
    rated_subcooling: float | None
    end_use_subcategory: str | None
    mode_of_operation: str | None
    transcritical_compressor_power_curve_name: str | None
    transcritical_compressor_capacity_curve_name: str | None

class RefrigerationCompressorList(IDFObject):
    refrigeration_compressor_name: str | None

class RefrigerationSystem(IDFObject):
    refrigerated_case_or_walkin_or_caseandwalkinlist_name: str | None
    refrigeration_transfer_load_or_transferload_list_name: str | None
    refrigeration_condenser_name: str | None
    compressor_or_compressorlist_name: str | None
    minimum_condensing_temperature: float | None
    refrigeration_system_working_fluid_type: str | None
    suction_temperature_control_type: str | None
    mechanical_subcooler_name: str | None
    liquid_suction_heat_exchanger_subcooler_name: str | None
    sum_ua_suction_piping: float | None
    suction_piping_zone_name: str | None
    end_use_subcategory: str | None
    number_of_compressor_stages: float | str | None
    intercooler_type: str | None
    shell_and_coil_intercooler_effectiveness: float | None
    high_stage_compressor_or_compressorlist_name: str | None

class RefrigerationTranscriticalSystem(IDFObject):
    system_type: str | None
    medium_temperature_refrigerated_case_or_walkin_or_caseandwalkinlist_name: str | None
    low_temperature_refrigerated_case_or_walkin_or_caseandwalkinlist_name: str | None
    refrigeration_gas_cooler_name: str | None
    high_pressure_compressor_or_compressorlist_name: str | None
    low_pressure_compressor_or_compressorlist_name: str | None
    receiver_pressure: float | None
    subcooler_effectiveness: float | None
    refrigeration_system_working_fluid_type: str | None
    sum_ua_suction_piping_for_medium_temperature_loads: float | None
    medium_temperature_suction_piping_zone_name: str | None
    sum_ua_suction_piping_for_low_temperature_loads: float | None
    low_temperature_suction_piping_zone_name: str | None
    end_use_subcategory: str | None

class RefrigerationSecondarySystem(IDFObject):
    refrigerated_case_or_walkin_or_caseandwalkinlist_name: str | None
    circulating_fluid_type: str | None
    circulating_fluid_name: str | None
    evaporator_capacity: float | None
    evaporator_flow_rate_for_secondary_fluid: float | None
    evaporator_evaporating_temperature: float | None
    evaporator_approach_temperature_difference: float | None
    evaporator_range_temperature_difference: float | None
    number_of_pumps_in_loop: int | None
    total_pump_flow_rate: float | None
    total_pump_power: float | None
    total_pump_head: float | None
    phasechange_circulating_rate: float | None
    pump_drive_type: str | None
    variable_speed_pump_cubic_curve_name: str | None
    pump_motor_heat_to_fluid: float | None
    sum_ua_distribution_piping: float | None
    distribution_piping_zone_name: str | None
    sum_ua_receiver_separator_shell: float | None
    receiver_separator_zone_name: str | None
    evaporator_refrigerant_inventory: float | None
    end_use_subcategory: str | None

class RefrigerationWalkIn(IDFObject):
    availability_schedule_name: str | None
    rated_coil_cooling_capacity: float | None
    operating_temperature: float | None
    rated_cooling_source_temperature: float | None
    rated_total_heating_power: float | None
    heating_power_schedule_name: str | None
    rated_cooling_coil_fan_power: float | None
    rated_circulation_fan_power: float | None
    rated_total_lighting_power: float | None
    lighting_schedule_name: str | None
    defrost_type: str | None
    defrost_control_type: str | None
    defrost_schedule_name: str | None
    defrost_drip_down_schedule_name: str | None
    defrost_power: float | None
    temperature_termination_defrost_fraction_to_ice: float | None
    restocking_schedule_name: str | None
    average_refrigerant_charge_inventory: float | None
    insulated_floor_surface_area: float | None
    insulated_floor_u_value: float | None
    zone_name: str | None
    total_insulated_surface_area_facing_zone: float | None
    insulated_surface_u_value_facing_zone: float | None
    area_of_glass_reach_in_doors_facing_zone: float | None
    height_of_glass_reach_in_doors_facing_zone: float | None
    glass_reach_in_door_u_value_facing_zone: float | None
    glass_reach_in_door_opening_schedule_name_facing_zone: str | None
    area_of_stocking_doors_facing_zone: float | None
    height_of_stocking_doors_facing_zone: float | None
    stocking_door_u_value_facing_zone: float | None
    stocking_door_opening_schedule_name_facing_zone: str | None
    stocking_door_opening_protection_type_facing_zone: str | None

class RefrigerationAirChiller(IDFObject):
    availability_schedule_name: str | None
    capacity_rating_type: str | None
    rated_unit_load_factor: float | None
    rated_capacity: float | None
    rated_relative_humidity: float | None
    rated_cooling_source_temperature: float | None
    rated_temperature_difference_dt1: float | None
    maximum_temperature_difference_between_inlet_air_and_evaporating_temperature: float | None
    coil_material_correction_factor: float | None
    refrigerant_correction_factor: float | None
    capacity_correction_curve_type: str | None
    capacity_correction_curve_name: str | None
    shr60_correction_factor: float | None
    rated_total_heating_power: float | None
    heating_power_schedule_name: str | None
    fan_speed_control_type: str | None
    rated_fan_power: float | None
    rated_air_flow: float | None
    minimum_fan_air_flow_ratio: float | None
    defrost_type: str | None
    defrost_control_type: str | None
    defrost_schedule_name: str | None
    defrost_drip_down_schedule_name: str | None
    defrost_power: float | None
    temperature_termination_defrost_fraction_to_ice: float | None
    vertical_location: str | None
    average_refrigerant_charge_inventory: float | None

class ZoneHVACRefrigerationChillerSet(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    air_chiller_name: str | None

class DemandManagerAssignmentList(IDFObject):
    meter_name: str | None
    demand_limit_schedule_name: str | None
    demand_limit_safety_fraction: float | None
    billing_period_schedule_name: str | None
    peak_period_schedule_name: str | None
    demand_window_length: int | None
    demand_manager_priority: str | None
    demandmanager_object_type: str | None
    demandmanager_name: str | None

class DemandManagerExteriorLights(IDFObject):
    availability_schedule_name: str | None
    limit_control: str | None
    minimum_limit_duration: int | None
    maximum_limit_fraction: float | None
    limit_step_change: float | None
    selection_control: str | None
    rotation_duration: int | None
    exterior_lights_name: str | None

class DemandManagerLights(IDFObject):
    availability_schedule_name: str | None
    limit_control: str | None
    minimum_limit_duration: int | None
    maximum_limit_fraction: float | None
    limit_step_change: float | None
    selection_control: str | None
    rotation_duration: int | None
    lights_name: str | None

class DemandManagerElectricEquipment(IDFObject):
    availability_schedule_name: str | None
    limit_control: str | None
    minimum_limit_duration: int | None
    maximum_limit_fraction: float | None
    limit_step_change: float | None
    selection_control: str | None
    rotation_duration: int | None
    electric_equipment_name: str | None

class DemandManagerThermostats(IDFObject):
    availability_schedule_name: str | None
    reset_control: str | None
    minimum_reset_duration: int | None
    maximum_heating_setpoint_reset: float | None
    maximum_cooling_setpoint_reset: float | None
    reset_step_change: float | None
    selection_control: str | None
    rotation_duration: int | None
    thermostat_name: str | None

class DemandManagerVentilation(IDFObject):
    availability_schedule_name: str | None
    limit_control: str | None
    minimum_limit_duration: int | None
    fixed_rate: float | None
    reduction_ratio: float | None
    limit_step_change: float | None
    selection_control: str | None
    rotation_duration: int | None
    controller_outdoor_air_name: str | None

class GeneratorInternalCombustionEngine(IDFObject):
    rated_power_output: float | None
    electric_circuit_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    shaft_power_curve_name: str | None
    jacket_heat_recovery_curve_name: str | None
    lube_heat_recovery_curve_name: str | None
    total_exhaust_energy_curve_name: str | None
    exhaust_temperature_curve_name: str | None
    coefficient_1_of_u_factor_times_area_curve: float | None
    coefficient_2_of_u_factor_times_area_curve: float | None
    maximum_exhaust_flow_per_unit_of_power_output: float | None
    design_minimum_exhaust_temperature: float | None
    fuel_higher_heating_value: float | None
    design_heat_recovery_water_flow_rate: float | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    fuel_type: str | None
    heat_recovery_maximum_temperature: float | None

class GeneratorCombustionTurbine(IDFObject):
    rated_power_output: float | None
    electric_circuit_node_name: str | None
    minimum_part_load_ratio: float | None
    maximum_part_load_ratio: float | None
    optimum_part_load_ratio: float | None
    part_load_based_fuel_input_curve_name: str | None
    temperature_based_fuel_input_curve_name: str | None
    exhaust_flow_curve_name: str | None
    part_load_based_exhaust_temperature_curve_name: str | None
    temperature_based_exhaust_temperature_curve_name: str | None
    heat_recovery_lube_energy_curve_name: str | None
    coefficient_1_of_u_factor_times_area_curve: float | None
    coefficient_2_of_u_factor_times_area_curve: float | None
    maximum_exhaust_flow_per_unit_of_power_output: float | None
    design_minimum_exhaust_temperature: float | None
    design_air_inlet_temperature: float | None
    fuel_higher_heating_value: float | None
    design_heat_recovery_water_flow_rate: float | None
    heat_recovery_inlet_node_name: str | None
    heat_recovery_outlet_node_name: str | None
    fuel_type: str | None
    heat_recovery_maximum_temperature: float | None
    outdoor_air_inlet_node_name: str | None

class GeneratorMicroTurbine(IDFObject):
    reference_electrical_power_output: float | None
    minimum_full_load_electrical_power_output: float | None
    maximum_full_load_electrical_power_output: float | None
    reference_electrical_efficiency_using_lower_heating_value: float | None
    reference_combustion_air_inlet_temperature: float | None
    reference_combustion_air_inlet_humidity_ratio: float | None
    reference_elevation: float | None
    electrical_power_function_of_temperature_and_elevation_curve_name: str | None
    electrical_efficiency_function_of_temperature_curve_name: str | None
    electrical_efficiency_function_of_part_load_ratio_curve_name: str | None
    fuel_type: str | None
    fuel_higher_heating_value: float | None
    fuel_lower_heating_value: float | None
    standby_power: float | None
    ancillary_power: float | None
    ancillary_power_function_of_fuel_input_curve_name: str | None
    heat_recovery_water_inlet_node_name: str | None
    heat_recovery_water_outlet_node_name: str | None
    reference_thermal_efficiency_using_lower_heat_value: float | None
    reference_inlet_water_temperature: float | None
    heat_recovery_water_flow_operating_mode: str | None
    reference_heat_recovery_water_flow_rate: float | None
    heat_recovery_water_flow_rate_function_of_temperature_and_power_curve_name: str | None
    thermal_efficiency_function_of_temperature_and_elevation_curve_name: str | None
    heat_recovery_rate_function_of_part_load_ratio_curve_name: str | None
    heat_recovery_rate_function_of_inlet_water_temperature_curve_name: str | None
    heat_recovery_rate_function_of_water_flow_rate_curve_name: str | None
    minimum_heat_recovery_water_flow_rate: float | None
    maximum_heat_recovery_water_flow_rate: float | None
    maximum_heat_recovery_water_temperature: float | None
    combustion_air_inlet_node_name: str | None
    combustion_air_outlet_node_name: str | None
    reference_exhaust_air_mass_flow_rate: float | None
    exhaust_air_flow_rate_function_of_temperature_curve_name: str | None
    exhaust_air_flow_rate_function_of_part_load_ratio_curve_name: str | None
    nominal_exhaust_air_outlet_temperature: float | None
    exhaust_air_temperature_function_of_temperature_curve_name: str | None
    exhaust_air_temperature_function_of_part_load_ratio_curve_name: str | None

class GeneratorPhotovoltaic(IDFObject):
    surface_name: str | None
    photovoltaic_performance_object_type: str | None
    module_performance_name: str | None
    heat_transfer_integration_mode: str | None
    number_of_series_strings_in_parallel: float | None
    number_of_modules_in_series: float | None

class PhotovoltaicPerformanceSimple(IDFObject):
    fraction_of_surface_area_with_active_solar_cells: float | None
    conversion_efficiency_input_mode: str | None
    value_for_cell_efficiency_if_fixed: float | None
    efficiency_schedule_name: str | None

class PhotovoltaicPerformanceEquivalentOneDiode(IDFObject):
    cell_type: str | None
    number_of_cells_in_series: int | None
    active_area: float | None
    transmittance_absorptance_product: float | None
    semiconductor_bandgap: float | None
    shunt_resistance: float | None
    short_circuit_current: float | None
    open_circuit_voltage: float | None
    reference_temperature: float | None
    reference_insolation: float | None
    module_current_at_maximum_power: float | None
    module_voltage_at_maximum_power: float | None
    temperature_coefficient_of_short_circuit_current: float | None
    temperature_coefficient_of_open_circuit_voltage: float | None
    nominal_operating_cell_temperature_test_ambient_temperature: float | None
    nominal_operating_cell_temperature_test_cell_temperature: float | None
    nominal_operating_cell_temperature_test_insolation: float | None
    module_heat_loss_coefficient: float | None
    total_heat_capacity: float | None

class PhotovoltaicPerformanceSandia(IDFObject):
    active_area: float | None
    number_of_cells_in_series: int | None
    number_of_cells_in_parallel: int | None
    short_circuit_current: float | None
    open_circuit_voltage: float | None
    current_at_maximum_power_point: float | None
    voltage_at_maximum_power_point: float | None
    sandia_database_parameter_aisc: float | None
    sandia_database_parameter_aimp: float | None
    sandia_database_parameter_c0: float | None
    sandia_database_parameter_c1: float | None
    sandia_database_parameter_bvoc0: float | None
    sandia_database_parameter_mbvoc: float | None
    sandia_database_parameter_bvmp0: float | None
    sandia_database_parameter_mbvmp: float | None
    diode_factor: float | None
    sandia_database_parameter_c2: float | None
    sandia_database_parameter_c3: float | None
    sandia_database_parameter_a0: float | None
    sandia_database_parameter_a1: float | None
    sandia_database_parameter_a2: float | None
    sandia_database_parameter_a3: float | None
    sandia_database_parameter_a4: float | None
    sandia_database_parameter_b0: float | None
    sandia_database_parameter_b1: float | None
    sandia_database_parameter_b2: float | None
    sandia_database_parameter_b3: float | None
    sandia_database_parameter_b4: float | None
    sandia_database_parameter_b5: float | None
    sandia_database_parameter_delta_tc_: float | None
    sandia_database_parameter_fd: float | None
    sandia_database_parameter_a: float | None
    sandia_database_parameter_b: float | None
    sandia_database_parameter_c4: float | None
    sandia_database_parameter_c5: float | None
    sandia_database_parameter_ix0: float | None
    sandia_database_parameter_ixx0: float | None
    sandia_database_parameter_c6: float | None
    sandia_database_parameter_c7: float | None

class GeneratorPVWatts(IDFObject):
    pvwatts_version: str | None
    dc_system_capacity: float | None
    module_type: str | None
    array_type: str | None
    system_losses: float | None
    array_geometry_type: str | None
    tilt_angle: float | None
    azimuth_angle: float | None
    surface_name: str | None
    ground_coverage_ratio: float | None

class ElectricLoadCenterInverterPVWatts(IDFObject):
    dc_to_ac_size_ratio: float | None
    inverter_efficiency: float | None

class GeneratorFuelCell(IDFObject):
    power_module_name: str | None
    air_supply_name: str | None
    fuel_supply_name: str | None
    water_supply_name: str | None
    auxiliary_heater_name: str | None
    heat_exchanger_name: str | None
    electrical_storage_name: str | None
    inverter_name: str | None
    stack_cooler_name: str | None

class GeneratorFuelCellPowerModule(IDFObject):
    efficiency_curve_mode: str | None
    efficiency_curve_name: str | None
    nominal_efficiency: float | None
    nominal_electrical_power: float | None
    number_of_stops_at_start_of_simulation: float | None
    cycling_performance_degradation_coefficient: float | None
    number_of_run_hours_at_beginning_of_simulation: float | None
    accumulated_run_time_degradation_coefficient: float | None
    run_time_degradation_initiation_time_threshold: float | None
    power_up_transient_limit: float | None
    power_down_transient_limit: float | None
    start_up_time: float | None
    start_up_fuel: float | None
    start_up_electricity_consumption: float | None
    start_up_electricity_produced: float | None
    shut_down_time: float | None
    shut_down_fuel: float | None
    shut_down_electricity_consumption: float | None
    ancillary_electricity_constant_term: float | None
    ancillary_electricity_linear_term: float | None
    skin_loss_calculation_mode: str | None
    zone_name: str | None
    skin_loss_radiative_fraction: float | None
    constant_skin_loss_rate: float | None
    skin_loss_u_factor_times_area_term: float | None
    skin_loss_quadratic_curve_name: str | None
    dilution_air_flow_rate: float | None
    stack_heat_loss_to_dilution_air: float | None
    dilution_inlet_air_node_name: str | None
    dilution_outlet_air_node_name: str | None
    minimum_operating_point: float | None
    maximum_operating_point: float | None

class GeneratorFuelCellAirSupply(IDFObject):
    air_inlet_node_name: str | None
    blower_power_curve_name: str | None
    blower_heat_loss_factor: float | None
    air_supply_rate_calculation_mode: str | None
    stoichiometric_ratio: float | None
    air_rate_function_of_electric_power_curve_name: str | None
    air_rate_air_temperature_coefficient: float | None
    air_rate_function_of_fuel_rate_curve_name: str | None
    air_intake_heat_recovery_mode: str | None
    air_supply_constituent_mode: str | None
    number_of_userdefined_constituents: float | None
    constituent_name: str | None
    molar_fraction: float | None

class GeneratorFuelCellWaterSupply(IDFObject):
    reformer_water_flow_rate_function_of_fuel_rate_curve_name: str | None
    reformer_water_pump_power_function_of_fuel_rate_curve_name: str | None
    pump_heat_loss_factor: float | None
    water_temperature_modeling_mode: str | None
    water_temperature_reference_node_name: str | None
    water_temperature_schedule_name: str | None

class GeneratorFuelCellAuxiliaryHeater(IDFObject):
    excess_air_ratio: float | None
    ancillary_power_constant_term: float | None
    ancillary_power_linear_term: float | None
    skin_loss_u_factor_times_area_value: float | None
    skin_loss_destination: str | None
    zone_name_to_receive_skin_losses: str | None
    heating_capacity_units: str | None
    maximum_heating_capacity_in_watts: float | None
    minimum_heating_capacity_in_watts: float | None
    maximum_heating_capacity_in_kmol_per_second: float | None
    minimum_heating_capacity_in_kmol_per_second: float | None

class GeneratorFuelCellExhaustGasToWaterHeatExchanger(IDFObject):
    heat_recovery_water_inlet_node_name: str | None
    heat_recovery_water_outlet_node_name: str | None
    heat_recovery_water_maximum_flow_rate: float | None
    exhaust_outlet_air_node_name: str | None
    heat_exchanger_calculation_method: str | None
    method_1_heat_exchanger_effectiveness: float | None
    method_2_parameter_hxs0: float | None
    method_2_parameter_hxs1: float | None
    method_2_parameter_hxs2: float | None
    method_2_parameter_hxs3: float | None
    method_2_parameter_hxs4: float | None
    method_3_h0gas_coefficient: float | None
    method_3_ndotgasref_coefficient: float | None
    method_3_n_coefficient: float | None
    method_3_gas_area: float | None
    method_3_h0_water_coefficient: float | None
    method_3_n_dot_water_ref_coefficient: float | None
    method_3_m_coefficient: float | None
    method_3_water_area: float | None
    method_3_f_adjustment_factor: float | None
    method_4_hxl1_coefficient: float | None
    method_4_hxl2_coefficient: float | None
    method_4_condensation_threshold: float | None

class GeneratorFuelCellElectricalStorage(IDFObject):
    choice_of_model: str | None
    nominal_charging_energetic_efficiency: float | None
    nominal_discharging_energetic_efficiency: float | None
    simple_maximum_capacity: float | None
    simple_maximum_power_draw: float | None
    simple_maximum_power_store: float | None
    initial_charge_state: float | None

class GeneratorFuelCellInverter(IDFObject):
    inverter_efficiency_calculation_mode: str | None
    inverter_efficiency: float | None
    efficiency_function_of_dc_power_curve_name: str | None

class GeneratorFuelCellStackCooler(IDFObject):
    heat_recovery_water_inlet_node_name: str | None
    heat_recovery_water_outlet_node_name: str | None
    nominal_stack_temperature: float | None
    actual_stack_temperature: float | None
    coefficient_r0: float | None
    coefficient_r1: float | None
    coefficient_r2: float | None
    coefficient_r3: float | None
    stack_coolant_flow_rate: float | None
    stack_cooler_u_factor_times_area_value: float | None
    fs_cogen_adjustment_factor: float | None
    stack_cogeneration_exchanger_area: float | None
    stack_cogeneration_exchanger_nominal_flow_rate: float | None
    stack_cogeneration_exchanger_nominal_heat_transfer_coefficient: float | None
    stack_cogeneration_exchanger_nominal_heat_transfer_coefficient_exponent: float | None
    stack_cooler_pump_power: float | None
    stack_cooler_pump_heat_loss_fraction: float | None
    stack_air_cooler_fan_coefficient_f0: float | None
    stack_air_cooler_fan_coefficient_f1: float | None
    stack_air_cooler_fan_coefficient_f2: float | None

class GeneratorMicroCHP(IDFObject):
    performance_parameters_name: str | None
    zone_name: str | None
    cooling_water_inlet_node_name: str | None
    cooling_water_outlet_node_name: str | None
    air_inlet_node_name: str | None
    air_outlet_node_name: str | None
    generator_fuel_supply_name: str | None
    availability_schedule_name: str | None

class GeneratorMicroCHPNonNormalizedParameters(IDFObject):
    maximum_electric_power: float | None
    minimum_electric_power: float | None
    minimum_cooling_water_flow_rate: float | None
    maximum_cooling_water_temperature: float | None
    electrical_efficiency_curve_name: str | None
    thermal_efficiency_curve_name: str | None
    cooling_water_flow_rate_mode: str | None
    cooling_water_flow_rate_curve_name: str | None
    air_flow_rate_curve_name: str | None
    maximum_net_electrical_power_rate_of_change: float | None
    maximum_fuel_flow_rate_of_change: float | None
    heat_exchanger_u_factor_times_area_value: float | None
    skin_loss_u_factor_times_area_value: float | None
    skin_loss_radiative_fraction: float | None
    aggregated_thermal_mass_of_energy_conversion_portion_of_generator: float | None
    aggregated_thermal_mass_of_heat_recovery_portion_of_generator: float | None
    standby_power: float | None
    warm_up_mode: str | None
    warm_up_fuel_flow_rate_coefficient: float | None
    nominal_engine_operating_temperature: float | None
    warm_up_power_coefficient: float | None
    warm_up_fuel_flow_rate_limit_ratio: float | None
    warm_up_delay_time: float | None
    cool_down_power: float | None
    cool_down_delay_time: float | None
    restart_mode: str | None

class GeneratorFuelSupply(IDFObject):
    fuel_temperature_modeling_mode: str | None
    fuel_temperature_reference_node_name: str | None
    fuel_temperature_schedule_name: str | None
    compressor_power_multiplier_function_of_fuel_rate_curve_name: str | None
    compressor_heat_loss_factor: float | None
    fuel_type: str | None
    liquid_generic_fuel_lower_heating_value: float | None
    liquid_generic_fuel_higher_heating_value: float | None
    liquid_generic_fuel_molecular_weight: float | None
    liquid_generic_fuel_co2_emission_factor: float | None
    number_of_constituents_in_gaseous_constituent_fuel_supply: float | None
    constituent_1_name: str | None
    constituent_1_molar_fraction: float | None
    constituent_2_name: str | None
    constituent_2_molar_fraction: float | None
    constituent_3_name: str | None
    constituent_3_molar_fraction: float | None
    constituent_4_name: str | None
    constituent_4_molar_fraction: float | None
    constituent_5_name: str | None
    constituent_5_molar_fraction: float | None
    constituent_6_name: str | None
    constituent_6_molar_fraction: float | None
    constituent_7_name: str | None
    constituent_7_molar_fraction: float | None
    constituent_8_name: str | None
    constituent_8_molar_fraction: float | None
    constituent_9_name: str | None
    constituent_9_molar_fraction: float | None
    constituent_10_name: str | None
    constituent_10_molar_fraction: float | None
    constituent_11_name: str | None
    constituent_11_molar_fraction: float | None
    constituent_12_name: str | None
    constituent_12_molar_fraction: float | None

class GeneratorWindTurbine(IDFObject):
    availability_schedule_name: str | None
    rotor_type: str | None
    power_control: str | None
    rated_rotor_speed: float | None
    rotor_diameter: float | None
    overall_height: float | None
    number_of_blades: float | None
    rated_power: float | None
    rated_wind_speed: float | None
    cut_in_wind_speed: float | None
    cut_out_wind_speed: float | None
    fraction_system_efficiency: float | None
    maximum_tip_speed_ratio: float | None
    maximum_power_coefficient: float | None
    annual_local_average_wind_speed: float | None
    height_for_local_average_wind_speed: float | None
    blade_chord_area: float | None
    blade_drag_coefficient: float | None
    blade_lift_coefficient: float | None
    power_coefficient_c1: float | None
    power_coefficient_c2: float | None
    power_coefficient_c3: float | None
    power_coefficient_c4: float | None
    power_coefficient_c5: float | None
    power_coefficient_c6: float | None

class ElectricLoadCenterGenerators(IDFObject):
    generator_name: str | None
    generator_object_type: str | None
    generator_rated_electric_power_output: float | None
    generator_availability_schedule_name: str | None
    generator_rated_thermal_to_electrical_power_ratio: float | None

class ElectricLoadCenterInverterSimple(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    radiative_fraction: float | None
    inverter_efficiency: float | None

class ElectricLoadCenterInverterFunctionOfPower(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    radiative_fraction: float | None
    efficiency_function_of_power_curve_name: str | None
    rated_maximum_continuous_input_power: float | None
    minimum_efficiency: float | None
    maximum_efficiency: float | None
    minimum_power_output: float | None
    maximum_power_output: float | None
    ancillary_power_consumed_in_standby: float | None

class ElectricLoadCenterInverterLookUpTable(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    radiative_fraction: float | None
    rated_maximum_continuous_output_power: float | None
    night_tare_loss_power: float | None
    nominal_voltage_input: float | None
    efficiency_at_10_power_and_nominal_voltage: float | None
    efficiency_at_20_power_and_nominal_voltage: float | None
    efficiency_at_30_power_and_nominal_voltage: float | None
    efficiency_at_50_power_and_nominal_voltage: float | None
    efficiency_at_75_power_and_nominal_voltage: float | None
    efficiency_at_100_power_and_nominal_voltage: float | None

class ElectricLoadCenterStorageSimple(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    radiative_fraction_for_zone_heat_gains: float | None
    nominal_energetic_efficiency_for_charging: float | None
    nominal_discharging_energetic_efficiency: float | None
    maximum_storage_capacity: float | None
    maximum_power_for_discharging: float | None
    maximum_power_for_charging: float | None
    initial_state_of_charge: float | None

class ElectricLoadCenterStorageBattery(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    radiative_fraction: float | None
    number_of_battery_modules_in_parallel: int | None
    number_of_battery_modules_in_series: int | None
    maximum_module_capacity: float | None
    initial_fractional_state_of_charge: float | None
    fraction_of_available_charge_capacity: float | None
    change_rate_from_bound_charge_to_available_charge: float | None
    fully_charged_module_open_circuit_voltage: float | None
    fully_discharged_module_open_circuit_voltage: float | None
    voltage_change_curve_name_for_charging: str | None
    voltage_change_curve_name_for_discharging: str | None
    module_internal_electrical_resistance: float | None
    maximum_module_discharging_current: float | None
    module_cut_off_voltage: float | None
    module_charge_rate_limit: float | None
    battery_life_calculation: str | None
    number_of_cycle_bins: int | None
    battery_life_curve_name: str | None

class ElectricLoadCenterStorageLiIonNMCBattery(IDFObject):
    availability_schedule_name: str | None
    zone_name: str | None
    radiative_fraction: float | None
    lifetime_model: str | None
    number_of_cells_in_series: int | None
    number_of_strings_in_parallel: int | None
    initial_fractional_state_of_charge: float | None
    dc_to_dc_charging_efficiency: float | None
    battery_mass: float | None
    battery_surface_area: float | None
    battery_specific_heat_capacity: float | None
    heat_transfer_coefficient_between_battery_and_ambient: float | None
    fully_charged_cell_voltage: float | None
    cell_voltage_at_end_of_exponential_zone: float | None
    cell_voltage_at_end_of_nominal_zone: float | None
    default_nominal_cell_voltage: float | None
    fully_charged_cell_capacity: float | None
    fraction_of_cell_capacity_removed_at_the_end_of_exponential_zone: float | None
    fraction_of_cell_capacity_removed_at_the_end_of_nominal_zone: float | None
    charge_rate_at_which_voltage_vs_capacity_curve_was_generated: float | None
    battery_cell_internal_electrical_resistance: float | None

class ElectricLoadCenterTransformer(IDFObject):
    availability_schedule_name: str | None
    transformer_usage: str | None
    zone_name: str | None
    radiative_fraction: float | None
    rated_capacity: float | None
    phase: float | str | None
    conductor_material: str | None
    full_load_temperature_rise: float | None
    fraction_of_eddy_current_losses: float | None
    performance_input_method: str | None
    rated_no_load_loss: float | None
    rated_load_loss: float | None
    nameplate_efficiency: float | None
    per_unit_load_for_nameplate_efficiency: float | None
    reference_temperature_for_nameplate_efficiency: float | None
    per_unit_load_for_maximum_efficiency: float | None
    consider_transformer_loss_for_utility_cost: str | None
    meter_name: str | None

class ElectricLoadCenterDistribution(IDFObject):
    generator_list_name: str | None
    generator_operation_scheme_type: str | None
    generator_demand_limit_scheme_purchased_electric_demand_limit: float | None
    generator_track_schedule_name_scheme_schedule_name: str | None
    generator_track_meter_scheme_meter_name: str | None
    electrical_buss_type: str | None
    inverter_name: str | None
    electrical_storage_object_name: str | None
    transformer_object_name: str | None
    storage_operation_scheme: str | None
    storage_control_track_meter_name: str | None
    storage_converter_object_name: str | None
    maximum_storage_state_of_charge_fraction: float | None
    minimum_storage_state_of_charge_fraction: float | None
    design_storage_control_charge_power: float | None
    storage_charge_power_fraction_schedule_name: str | None
    design_storage_control_discharge_power: float | None
    storage_discharge_power_fraction_schedule_name: str | None
    storage_control_utility_demand_target: float | None
    storage_control_utility_demand_target_fraction_schedule_name: str | None

class ElectricLoadCenterStorageConverter(IDFObject):
    availability_schedule_name: str | None
    power_conversion_efficiency_method: str | None
    simple_fixed_efficiency: float | None
    design_maximum_continuous_input_power: float | None
    efficiency_function_of_power_curve_name: str | None
    ancillary_power_consumed_in_standby: float | None
    zone_name: str | None
    radiative_fraction: float | None

class WaterUseEquipment(IDFObject):
    end_use_subcategory: str | None
    peak_flow_rate: float | None
    flow_rate_fraction_schedule_name: str | None
    target_temperature_schedule_name: str | None
    hot_water_supply_temperature_schedule_name: str | None
    cold_water_supply_temperature_schedule_name: str | None
    zone_name: str | None
    sensible_fraction_schedule_name: str | None
    latent_fraction_schedule_name: str | None

class WaterUseConnections(IDFObject):
    inlet_node_name: str | None
    outlet_node_name: str | None
    supply_water_storage_tank_name: str | None
    reclamation_water_storage_tank_name: str | None
    hot_water_supply_temperature_schedule_name: str | None
    cold_water_supply_temperature_schedule_name: str | None
    drain_water_heat_exchanger_type: str | None
    drain_water_heat_exchanger_destination: str | None
    drain_water_heat_exchanger_u_factor_times_area: float | None
    water_use_equipment_name: str | None

class WaterUseStorage(IDFObject):
    water_quality_subcategory: str | None
    maximum_capacity: float | None
    initial_volume: float | None
    design_in_flow_rate: float | None
    design_out_flow_rate: float | None
    overflow_destination: str | None
    type_of_supply_controlled_by_float_valve: str | None
    float_valve_on_capacity: float | None
    float_valve_off_capacity: float | None
    backup_mains_capacity: float | None
    other_tank_name: str | None
    water_thermal_mode: str | None
    water_temperature_schedule_name: str | None
    ambient_temperature_indicator: str | None
    ambient_temperature_schedule_name: str | None
    zone_name: str | None
    tank_surface_area: float | None
    tank_u_value: float | None
    tank_outside_surface_material_name: str | None

class WaterUseWell(IDFObject):
    storage_tank_name: str | None
    pump_depth: float | None
    pump_rated_flow_rate: float | None
    pump_rated_head: float | None
    pump_rated_power_consumption: float | None
    pump_efficiency: float | None
    well_recovery_rate: float | None
    nominal_well_storage_volume: float | None
    water_table_depth_mode: str | None
    water_table_depth: float | None
    water_table_depth_schedule_name: str | None

class WaterUseRainCollector(IDFObject):
    storage_tank_name: str | None
    loss_factor_mode: str | None
    collection_loss_factor: float | None
    collection_loss_factor_schedule_name: str | None
    maximum_collection_rate: float | None
    collection_surface_name: str | None

class FaultModelTemperatureSensorOffsetOutdoorAir(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    controller_object_type: str | None
    controller_object_name: str | None
    temperature_sensor_offset: float | None

class FaultModelHumiditySensorOffsetOutdoorAir(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    controller_object_type: str | None
    controller_object_name: str | None
    humidity_sensor_offset: float | None

class FaultModelEnthalpySensorOffsetOutdoorAir(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    controller_object_type: str | None
    controller_object_name: str | None
    enthalpy_sensor_offset: float | None

class FaultModelTemperatureSensorOffsetReturnAir(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    controller_object_type: str | None
    controller_object_name: str | None
    temperature_sensor_offset: float | None

class FaultModelEnthalpySensorOffsetReturnAir(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    controller_object_type: str | None
    controller_object_name: str | None
    enthalpy_sensor_offset: float | None

class FaultModelTemperatureSensorOffsetChillerSupplyWater(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    chiller_object_type: str | None
    chiller_object_name: str | None
    reference_sensor_offset: float | None

class FaultModelTemperatureSensorOffsetCoilSupplyAir(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    coil_object_type: str | None
    coil_object_name: str | None
    water_coil_controller_name: str | None
    reference_sensor_offset: float | None

class FaultModelTemperatureSensorOffsetCondenserSupplyWater(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    cooling_tower_object_type: str | None
    cooling_tower_object_name: str | None
    reference_sensor_offset: float | None

class FaultModelThermostatOffset(IDFObject):
    thermostat_name: str | None
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    reference_thermostat_offset: float | None

class FaultModelHumidistatOffset(IDFObject):
    humidistat_name: str | None
    humidistat_offset_type: str | None
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    reference_humidistat_offset: float | None
    related_thermostat_offset_fault_name: str | None

class FaultModelFoulingAirFilter(IDFObject):
    fan_object_type: str | None
    fan_name: str | None
    availability_schedule_name: str | None
    pressure_fraction_schedule_name: str | None
    fan_curve_name: str | None

class FaultModelFoulingBoiler(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    boiler_object_type: str | None
    boiler_object_name: str | None
    fouling_factor: float | None

class FaultModelFoulingEvaporativeCooler(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    evaporative_cooler_object_type: str | None
    evaporative_cooler_object_name: str | None
    fouling_factor: float | None

class FaultModelFoulingChiller(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    chiller_object_type: str | None
    chiller_object_name: str | None
    fouling_factor: float | None

class FaultModelFoulingCoolingTower(IDFObject):
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    cooling_tower_object_type: str | None
    cooling_tower_object_name: str | None
    reference_ua_reduction_factor: float | None

class FaultModelFoulingCoil(IDFObject):
    coil_name: str | None
    availability_schedule_name: str | None
    severity_schedule_name: str | None
    fouling_input_method: str | None
    uafouled: float | None
    water_side_fouling_factor: float | None
    air_side_fouling_factor: float | None
    outside_coil_surface_area: float | None
    inside_to_outside_coil_surface_area_ratio: float | None

class MatrixTwoDimension(IDFObject):
    number_of_rows: int | None
    number_of_columns: int | None
    value: float | None

class HybridModelZone(IDFObject):
    zone_name: str | None
    calculate_zone_internal_thermal_mass: str | None
    calculate_zone_air_infiltration_rate: str | None
    calculate_zone_people_count: str | None
    zone_measured_air_temperature_schedule_name: str | None
    zone_measured_air_humidity_ratio_schedule_name: str | None
    zone_measured_air_co2_concentration_schedule_name: str | None
    zone_input_people_activity_schedule_name: str | None
    zone_input_people_sensible_heat_fraction_schedule_name: str | None
    zone_input_people_radiant_heat_fraction_schedule_name: str | None
    zone_input_people_co2_generation_rate_schedule_name: str | None
    zone_input_supply_air_temperature_schedule_name: str | None
    zone_input_supply_air_mass_flow_rate_schedule_name: str | None
    zone_input_supply_air_humidity_ratio_schedule_name: str | None
    zone_input_supply_air_co2_concentration_schedule_name: str | None
    begin_month: int | None
    begin_day_of_month: int | None
    end_month: int | None
    end_day_of_month: int | None

class CurveLinear(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveQuadLinear(IDFObject):
    coefficient1_constant: float | None
    coefficient2_w: float | None
    coefficient3_x: float | None
    coefficient4_y: float | None
    coefficient5_z: float | None
    minimum_value_of_w: float | None
    maximum_value_of_w: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_value_of_y: float | None
    maximum_value_of_y: float | None
    minimum_value_of_z: float | None
    maximum_value_of_z: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_w: str | None
    input_unit_type_for_x: str | None
    input_unit_type_for_y: str | None
    input_unit_type_for_z: str | None

class CurveQuintLinear(IDFObject):
    coefficient1_constant: float | None
    coefficient2_v: float | None
    coefficient3_w: float | None
    coefficient4_x: float | None
    coefficient5_y: float | None
    coefficient6_z: float | None
    minimum_value_of_v: float | None
    maximum_value_of_v: float | None
    minimum_value_of_w: float | None
    maximum_value_of_w: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_value_of_y: float | None
    maximum_value_of_y: float | None
    minimum_value_of_z: float | None
    maximum_value_of_z: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_v: str | None
    input_unit_type_for_w: str | None
    input_unit_type_for_x: str | None
    input_unit_type_for_y: str | None
    input_unit_type_for_z: str | None

class CurveQuadratic(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x: float | None
    coefficient3_x_2: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveCubic(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x: float | None
    coefficient3_x_2: float | None
    coefficient4_x_3: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveQuartic(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x: float | None
    coefficient3_x_2: float | None
    coefficient4_x_3: float | None
    coefficient5_x_4: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveExponent(IDFObject):
    coefficient1_constant: float | None
    coefficient2_constant: float | None
    coefficient3_constant: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveBicubic(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x: float | None
    coefficient3_x_2: float | None
    coefficient4_y: float | None
    coefficient5_y_2: float | None
    coefficient6_x_y: float | None
    coefficient7_x_3: float | None
    coefficient8_y_3: float | None
    coefficient9_x_2_y: float | None
    coefficient10_x_y_2: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_value_of_y: float | None
    maximum_value_of_y: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    input_unit_type_for_y: str | None
    output_unit_type: str | None

class CurveBiquadratic(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x: float | None
    coefficient3_x_2: float | None
    coefficient4_y: float | None
    coefficient5_y_2: float | None
    coefficient6_x_y: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_value_of_y: float | None
    maximum_value_of_y: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    input_unit_type_for_y: str | None
    output_unit_type: str | None

class CurveQuadraticLinear(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x: float | None
    coefficient3_x_2: float | None
    coefficient4_y: float | None
    coefficient5_x_y: float | None
    coefficient6_x_2_y: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_value_of_y: float | None
    maximum_value_of_y: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    input_unit_type_for_y: str | None
    output_unit_type: str | None

class CurveCubicLinear(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x: float | None
    coefficient3_x_2: float | None
    coefficient4_x_3: float | None
    coefficient5_y: float | None
    coefficient6_x_y: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_value_of_y: float | None
    maximum_value_of_y: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    input_unit_type_for_y: str | None
    output_unit_type: str | None

class CurveTriquadratic(IDFObject):
    coefficient1_constant: float | None
    coefficient2_x_2: float | None
    coefficient3_x: float | None
    coefficient4_y_2: float | None
    coefficient5_y: float | None
    coefficient6_z_2: float | None
    coefficient7_z: float | None
    coefficient8_x_2_y_2: float | None
    coefficient9_x_y: float | None
    coefficient10_x_y_2: float | None
    coefficient11_x_2_y: float | None
    coefficient12_x_2_z_2: float | None
    coefficient13_x_z: float | None
    coefficient14_x_z_2: float | None
    coefficient15_x_2_z: float | None
    coefficient16_y_2_z_2: float | None
    coefficient17_y_z: float | None
    coefficient18_y_z_2: float | None
    coefficient19_y_2_z: float | None
    coefficient20_x_2_y_2_z_2: float | None
    coefficient21_x_2_y_2_z: float | None
    coefficient22_x_2_y_z_2: float | None
    coefficient23_x_y_2_z_2: float | None
    coefficient24_x_2_y_z: float | None
    coefficient25_x_y_2_z: float | None
    coefficient26_x_y_z_2: float | None
    coefficient27_x_y_z: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_value_of_y: float | None
    maximum_value_of_y: float | None
    minimum_value_of_z: float | None
    maximum_value_of_z: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    input_unit_type_for_y: str | None
    input_unit_type_for_z: str | None
    output_unit_type: str | None

class CurveFunctionalPressureDrop(IDFObject):
    diameter: float | None
    minor_loss_coefficient: float | None
    length: float | None
    roughness: float | None
    fixed_friction_factor: float | None

class CurveFanPressureRise(IDFObject):
    coefficient1_c1: float | None
    coefficient2_c2: float | None
    coefficient3_c3: float | None
    coefficient4_c4: float | None
    minimum_value_of_qfan: float | None
    maximum_value_of_qfan: float | None
    minimum_value_of_psm: float | None
    maximum_value_of_psm: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None

class CurveExponentialSkewNormal(IDFObject):
    coefficient1_c1: float | None
    coefficient2_c2: float | None
    coefficient3_c3: float | None
    coefficient4_c4: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveSigmoid(IDFObject):
    coefficient1_c1: float | None
    coefficient2_c2: float | None
    coefficient3_c3: float | None
    coefficient4_c4: float | None
    coefficient5_c5: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveRectangularHyperbola1(IDFObject):
    coefficient1_c1: float | None
    coefficient2_c2: float | None
    coefficient3_c3: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveRectangularHyperbola2(IDFObject):
    coefficient1_c1: float | None
    coefficient2_c2: float | None
    coefficient3_c3: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveExponentialDecay(IDFObject):
    coefficient1_c1: float | None
    coefficient2_c2: float | None
    coefficient3_c3: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveDoubleExponentialDecay(IDFObject):
    coefficient1_c1: float | None
    coefficient2_c2: float | None
    coefficient3_c3: float | None
    coefficient4_c4: float | None
    coefficient5_c5: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    output_unit_type: str | None

class CurveChillerPartLoadWithLift(IDFObject):
    coefficient1_c1: float | None
    coefficient2_c2: float | None
    coefficient3_c3: float | None
    coefficient4_c4: float | None
    coefficient5_c5: float | None
    coefficient6_c6: float | None
    coefficient7_c7: float | None
    coefficient8_c8: float | None
    coefficient9_c9: float | None
    coefficient10_c10: float | None
    coefficient11_c11: float | None
    coefficient12_c12: float | None
    minimum_value_of_x: float | None
    maximum_value_of_x: float | None
    minimum_value_of_y: float | None
    maximum_value_of_y: float | None
    minimum_value_of_z: float | None
    maximum_value_of_z: float | None
    minimum_curve_output: float | None
    maximum_curve_output: float | None
    input_unit_type_for_x: str | None
    input_unit_type_for_y: str | None
    input_unit_type_for_z: str | None
    output_unit_type: str | None

class TableIndependentVariable(IDFObject):
    interpolation_method: str | None
    extrapolation_method: str | None
    minimum_value: float | None
    maximum_value: float | None
    normalization_reference_value: float | None
    unit_type: str | None
    external_file_name: str | None
    external_file_column_number: int | None
    external_file_starting_row_number: int | None
    value: float | None

class TableIndependentVariableList(IDFObject):
    independent_variable_name: str | None

class TableLookup(IDFObject):
    independent_variable_list_name: str | None
    normalization_method: str | None
    normalization_divisor: float | None
    minimum_output: float | None
    maximum_output: float | None
    output_unit_type: str | None
    external_file_name: str | None
    external_file_column_number: int | None
    external_file_starting_row_number: int | None
    output_value: float | None

class FluidPropertiesName(IDFObject):
    fluid_type: str | None

class FluidPropertiesGlycolConcentration(IDFObject):
    glycol_type: str | None
    user_defined_glycol_name: str | None
    glycol_concentration: float | None

class FluidPropertiesTemperatures(IDFObject):
    temperature_1: float | None
    temperature_2: float | None
    temperature_3: float | None
    temperature_4: float | None
    temperature_5: float | None
    temperature_6: float | None
    temperature_7: float | None
    temperature_8: float | None
    temperature_9: float | None
    temperature_10: float | None
    temperature_11: float | None
    temperature_12: float | None
    temperature_13: float | None
    temperature_14: float | None
    temperature_15: float | None
    temperature_16: float | None
    temperature_17: float | None
    temperature_18: float | None
    temperature_19: float | None
    temperature_20: float | None
    temperature_21: float | None
    temperature_22: float | None
    temperature_23: float | None
    temperature_24: float | None
    temperature_25: float | None
    temperature_26: float | None
    temperature_27: float | None
    temperature_28: float | None
    temperature_29: float | None
    temperature_30: float | None
    temperature_31: float | None
    temperature_32: float | None
    temperature_33: float | None
    temperature_34: float | None
    temperature_35: float | None
    temperature_36: float | None
    temperature_37: float | None
    temperature_38: float | None
    temperature_39: float | None
    temperature_40: float | None
    temperature_41: float | None
    temperature_42: float | None
    temperature_43: float | None
    temperature_44: float | None
    temperature_45: float | None
    temperature_46: float | None
    temperature_47: float | None
    temperature_48: float | None
    temperature_49: float | None
    temperature_50: float | None
    temperature_51: float | None
    temperature_52: float | None
    temperature_53: float | None
    temperature_54: float | None
    temperature_55: float | None
    temperature_56: float | None
    temperature_57: float | None
    temperature_58: float | None
    temperature_59: float | None
    temperature_60: float | None
    temperature_61: float | None
    temperature_62: float | None
    temperature_63: float | None
    temperature_64: float | None
    temperature_65: float | None
    temperature_66: float | None
    temperature_67: float | None
    temperature_68: float | None
    temperature_69: float | None
    temperature_70: float | None
    temperature_71: float | None
    temperature_72: float | None
    temperature_73: float | None
    temperature_74: float | None
    temperature_75: float | None
    temperature_76: float | None
    temperature_77: float | None
    temperature_78: float | None
    temperature_79: float | None
    temperature_80: float | None
    temperature_81: float | None
    temperature_82: float | None
    temperature_83: float | None
    temperature_84: float | None
    temperature_85: float | None
    temperature_86: float | None
    temperature_87: float | None
    temperature_88: float | None
    temperature_89: float | None
    temperature_90: float | None
    temperature_91: float | None
    temperature_92: float | None
    temperature_93: float | None
    temperature_94: float | None
    temperature_95: float | None
    temperature_96: float | None
    temperature_97: float | None
    temperature_98: float | None
    temperature_99: float | None
    temperature_100: float | None
    temperature_101: float | None
    temperature_102: float | None
    temperature_103: float | None
    temperature_104: float | None
    temperature_105: float | None
    temperature_106: float | None
    temperature_107: float | None
    temperature_108: float | None
    temperature_109: float | None
    temperature_110: float | None
    temperature_111: float | None
    temperature_112: float | None
    temperature_113: float | None
    temperature_114: float | None
    temperature_115: float | None
    temperature_116: float | None
    temperature_117: float | None
    temperature_118: float | None
    temperature_119: float | None
    temperature_120: float | None
    temperature_121: float | None
    temperature_122: float | None
    temperature_123: float | None
    temperature_124: float | None
    temperature_125: float | None
    temperature_126: float | None
    temperature_127: float | None
    temperature_128: float | None
    temperature_129: float | None
    temperature_130: float | None
    temperature_131: float | None
    temperature_132: float | None
    temperature_133: float | None
    temperature_134: float | None
    temperature_135: float | None
    temperature_136: float | None
    temperature_137: float | None
    temperature_138: float | None
    temperature_139: float | None
    temperature_140: float | None
    temperature_141: float | None
    temperature_142: float | None
    temperature_143: float | None
    temperature_144: float | None
    temperature_145: float | None
    temperature_146: float | None
    temperature_147: float | None
    temperature_148: float | None
    temperature_149: float | None
    temperature_150: float | None
    temperature_151: float | None
    temperature_152: float | None
    temperature_153: float | None
    temperature_154: float | None
    temperature_155: float | None
    temperature_156: float | None
    temperature_157: float | None
    temperature_158: float | None
    temperature_159: float | None
    temperature_160: float | None
    temperature_161: float | None
    temperature_162: float | None
    temperature_163: float | None
    temperature_164: float | None
    temperature_165: float | None
    temperature_166: float | None
    temperature_167: float | None
    temperature_168: float | None
    temperature_169: float | None
    temperature_170: float | None
    temperature_171: float | None
    temperature_172: float | None
    temperature_173: float | None
    temperature_174: float | None
    temperature_175: float | None
    temperature_176: float | None
    temperature_177: float | None
    temperature_178: float | None
    temperature_179: float | None
    temperature_180: float | None
    temperature_181: float | None
    temperature_182: float | None
    temperature_183: float | None
    temperature_184: float | None
    temperature_185: float | None
    temperature_186: float | None
    temperature_187: float | None
    temperature_188: float | None
    temperature_189: float | None
    temperature_190: float | None
    temperature_191: float | None
    temperature_192: float | None
    temperature_193: float | None
    temperature_194: float | None
    temperature_195: float | None
    temperature_196: float | None
    temperature_197: float | None
    temperature_198: float | None
    temperature_199: float | None
    temperature_200: float | None
    temperature_201: float | None
    temperature_202: float | None
    temperature_203: float | None
    temperature_204: float | None
    temperature_205: float | None
    temperature_206: float | None
    temperature_207: float | None
    temperature_208: float | None
    temperature_209: float | None
    temperature_210: float | None
    temperature_211: float | None
    temperature_212: float | None
    temperature_213: float | None
    temperature_214: float | None
    temperature_215: float | None
    temperature_216: float | None
    temperature_217: float | None
    temperature_218: float | None
    temperature_219: float | None
    temperature_220: float | None
    temperature_221: float | None
    temperature_222: float | None
    temperature_223: float | None
    temperature_224: float | None
    temperature_225: float | None
    temperature_226: float | None
    temperature_227: float | None
    temperature_228: float | None
    temperature_229: float | None
    temperature_230: float | None
    temperature_231: float | None
    temperature_232: float | None
    temperature_233: float | None
    temperature_234: float | None
    temperature_235: float | None
    temperature_236: float | None
    temperature_237: float | None
    temperature_238: float | None
    temperature_239: float | None
    temperature_240: float | None
    temperature_241: float | None
    temperature_242: float | None
    temperature_243: float | None
    temperature_244: float | None
    temperature_245: float | None
    temperature_246: float | None
    temperature_247: float | None
    temperature_248: float | None
    temperature_249: float | None
    temperature_250: float | None

class FluidPropertiesSaturated(IDFObject):
    fluid_property_type: str | None
    fluid_phase: str | None
    temperature_values_name: str | None
    property_value_1: float | None
    property_value_2: float | None
    property_value_3: float | None
    property_value_4: float | None
    property_value_5: float | None
    property_value_6: float | None
    property_value_7: float | None
    property_value_8: float | None
    property_value_9: float | None
    property_value_10: float | None
    property_value_11: float | None
    property_value_12: float | None
    property_value_13: float | None
    property_value_14: float | None
    property_value_15: float | None
    property_value_16: float | None
    property_value_17: float | None
    property_value_18: float | None
    property_value_19: float | None
    property_value_20: float | None
    property_value_21: float | None
    property_value_22: float | None
    property_value_23: float | None
    property_value_24: float | None
    property_value_25: float | None
    property_value_26: float | None
    property_value_27: float | None
    property_value_28: float | None
    property_value_29: float | None
    property_value_30: float | None
    property_value_31: float | None
    property_value_32: float | None
    property_value_33: float | None
    property_value_34: float | None
    property_value_35: float | None
    property_value_36: float | None
    property_value_37: float | None
    property_value_38: float | None
    property_value_39: float | None
    property_value_40: float | None
    property_value_41: float | None
    property_value_42: float | None
    property_value_43: float | None
    property_value_44: float | None
    property_value_45: float | None
    property_value_46: float | None
    property_value_47: float | None
    property_value_48: float | None
    property_value_49: float | None
    property_value_50: float | None
    property_value_51: float | None
    property_value_52: float | None
    property_value_53: float | None
    property_value_54: float | None
    property_value_55: float | None
    property_value_56: float | None
    property_value_57: float | None
    property_value_58: float | None
    property_value_59: float | None
    property_value_60: float | None
    property_value_61: float | None
    property_value_62: float | None
    property_value_63: float | None
    property_value_64: float | None
    property_value_65: float | None
    property_value_66: float | None
    property_value_67: float | None
    property_value_68: float | None
    property_value_69: float | None
    property_value_70: float | None
    property_value_71: float | None
    property_value_72: float | None
    property_value_73: float | None
    property_value_74: float | None
    property_value_75: float | None
    property_value_76: float | None
    property_value_77: float | None
    property_value_78: float | None
    property_value_79: float | None
    property_value_80: float | None
    property_value_81: float | None
    property_value_82: float | None
    property_value_83: float | None
    property_value_84: float | None
    property_value_85: float | None
    property_value_86: float | None
    property_value_87: float | None
    property_value_88: float | None
    property_value_89: float | None
    property_value_90: float | None
    property_value_91: float | None
    property_value_92: float | None
    property_value_93: float | None
    property_value_94: float | None
    property_value_95: float | None
    property_value_96: float | None
    property_value_97: float | None
    property_value_98: float | None
    property_value_99: float | None
    property_value_100: float | None
    property_value_101: float | None
    property_value_102: float | None
    property_value_103: float | None
    property_value_104: float | None
    property_value_105: float | None
    property_value_106: float | None
    property_value_107: float | None
    property_value_108: float | None
    property_value_109: float | None
    property_value_110: float | None
    property_value_111: float | None
    property_value_112: float | None
    property_value_113: float | None
    property_value_114: float | None
    property_value_115: float | None
    property_value_116: float | None
    property_value_117: float | None
    property_value_118: float | None
    property_value_119: float | None
    property_value_120: float | None
    property_value_121: float | None
    property_value_122: float | None
    property_value_123: float | None
    property_value_124: float | None
    property_value_125: float | None
    property_value_126: float | None
    property_value_127: float | None
    property_value_128: float | None
    property_value_129: float | None
    property_value_130: float | None
    property_value_131: float | None
    property_value_132: float | None
    property_value_133: float | None
    property_value_134: float | None
    property_value_135: float | None
    property_value_136: float | None
    property_value_137: float | None
    property_value_138: float | None
    property_value_139: float | None
    property_value_140: float | None
    property_value_141: float | None
    property_value_142: float | None
    property_value_143: float | None
    property_value_144: float | None
    property_value_145: float | None
    property_value_146: float | None
    property_value_147: float | None
    property_value_148: float | None
    property_value_149: float | None
    property_value_150: float | None
    property_value_151: float | None
    property_value_152: float | None
    property_value_153: float | None
    property_value_154: float | None
    property_value_155: float | None
    property_value_156: float | None
    property_value_157: float | None
    property_value_158: float | None
    property_value_159: float | None
    property_value_160: float | None
    property_value_161: float | None
    property_value_162: float | None
    property_value_163: float | None
    property_value_164: float | None
    property_value_165: float | None
    property_value_166: float | None
    property_value_167: float | None
    property_value_168: float | None
    property_value_169: float | None
    property_value_170: float | None
    property_value_171: float | None
    property_value_172: float | None
    property_value_173: float | None
    property_value_174: float | None
    property_value_175: float | None
    property_value_176: float | None
    property_value_177: float | None
    property_value_178: float | None
    property_value_179: float | None
    property_value_180: float | None
    property_value_181: float | None
    property_value_182: float | None
    property_value_183: float | None
    property_value_184: float | None
    property_value_185: float | None
    property_value_186: float | None
    property_value_187: float | None
    property_value_188: float | None
    property_value_189: float | None
    property_value_190: float | None
    property_value_191: float | None
    property_value_192: float | None
    property_value_193: float | None
    property_value_194: float | None
    property_value_195: float | None
    property_value_196: float | None
    property_value_197: float | None
    property_value_198: float | None
    property_value_199: float | None
    property_value_200: float | None
    property_value_201: float | None
    property_value_202: float | None
    property_value_203: float | None
    property_value_204: float | None
    property_value_205: float | None
    property_value_206: float | None
    property_value_207: float | None
    property_value_208: float | None
    property_value_209: float | None
    property_value_210: float | None
    property_value_211: float | None
    property_value_212: float | None
    property_value_213: float | None
    property_value_214: float | None
    property_value_215: float | None
    property_value_216: float | None
    property_value_217: float | None
    property_value_218: float | None
    property_value_219: float | None
    property_value_220: float | None
    property_value_221: float | None
    property_value_222: float | None
    property_value_223: float | None
    property_value_224: float | None
    property_value_225: float | None
    property_value_226: float | None
    property_value_227: float | None
    property_value_228: float | None
    property_value_229: float | None
    property_value_230: float | None
    property_value_231: float | None
    property_value_232: float | None
    property_value_233: float | None
    property_value_234: float | None
    property_value_235: float | None
    property_value_236: float | None
    property_value_237: float | None
    property_value_238: float | None
    property_value_239: float | None
    property_value_240: float | None
    property_value_241: float | None
    property_value_242: float | None
    property_value_243: float | None
    property_value_244: float | None
    property_value_245: float | None
    property_value_246: float | None
    property_value_247: float | None
    property_value_248: float | None
    property_value_249: float | None
    property_value_250: float | None

class FluidPropertiesSuperheated(IDFObject):
    fluid_property_type: str | None
    temperature_values_name: str | None
    pressure: float | None
    property_value_1: float | None
    property_value_2: float | None
    property_value_3: float | None
    property_value_4: float | None
    property_value_5: float | None
    property_value_6: float | None
    property_value_7: float | None
    property_value_8: float | None
    property_value_9: float | None
    property_value_10: float | None
    property_value_11: float | None
    property_value_12: float | None
    property_value_13: float | None
    property_value_14: float | None
    property_value_15: float | None
    property_value_16: float | None
    property_value_17: float | None
    property_value_18: float | None
    property_value_19: float | None
    property_value_20: float | None
    property_value_21: float | None
    property_value_22: float | None
    property_value_23: float | None
    property_value_24: float | None
    property_value_25: float | None
    property_value_26: float | None
    property_value_27: float | None
    property_value_28: float | None
    property_value_29: float | None
    property_value_30: float | None
    property_value_31: float | None
    property_value_32: float | None
    property_value_33: float | None
    property_value_34: float | None
    property_value_35: float | None
    property_value_36: float | None
    property_value_37: float | None
    property_value_38: float | None
    property_value_39: float | None
    property_value_40: float | None
    property_value_41: float | None
    property_value_42: float | None
    property_value_43: float | None
    property_value_44: float | None
    property_value_45: float | None
    property_value_46: float | None
    property_value_47: float | None
    property_value_48: float | None
    property_value_49: float | None
    property_value_50: float | None
    property_value_51: float | None
    property_value_52: float | None
    property_value_53: float | None
    property_value_54: float | None
    property_value_55: float | None
    property_value_56: float | None
    property_value_57: float | None
    property_value_58: float | None
    property_value_59: float | None
    property_value_60: float | None
    property_value_61: float | None
    property_value_62: float | None
    property_value_63: float | None
    property_value_64: float | None
    property_value_65: float | None
    property_value_66: float | None
    property_value_67: float | None
    property_value_68: float | None
    property_value_69: float | None
    property_value_70: float | None
    property_value_71: float | None
    property_value_72: float | None
    property_value_73: float | None
    property_value_74: float | None
    property_value_75: float | None
    property_value_76: float | None
    property_value_77: float | None
    property_value_78: float | None
    property_value_79: float | None
    property_value_80: float | None
    property_value_81: float | None
    property_value_82: float | None
    property_value_83: float | None
    property_value_84: float | None
    property_value_85: float | None
    property_value_86: float | None
    property_value_87: float | None
    property_value_88: float | None
    property_value_89: float | None
    property_value_90: float | None
    property_value_91: float | None
    property_value_92: float | None
    property_value_93: float | None
    property_value_94: float | None
    property_value_95: float | None
    property_value_96: float | None
    property_value_97: float | None
    property_value_98: float | None
    property_value_99: float | None
    property_value_100: float | None
    property_value_101: float | None
    property_value_102: float | None
    property_value_103: float | None
    property_value_104: float | None
    property_value_105: float | None
    property_value_106: float | None
    property_value_107: float | None
    property_value_108: float | None
    property_value_109: float | None
    property_value_110: float | None
    property_value_111: float | None
    property_value_112: float | None
    property_value_113: float | None
    property_value_114: float | None
    property_value_115: float | None
    property_value_116: float | None
    property_value_117: float | None
    property_value_118: float | None
    property_value_119: float | None
    property_value_120: float | None
    property_value_121: float | None
    property_value_122: float | None
    property_value_123: float | None
    property_value_124: float | None
    property_value_125: float | None
    property_value_126: float | None
    property_value_127: float | None
    property_value_128: float | None
    property_value_129: float | None
    property_value_130: float | None
    property_value_131: float | None
    property_value_132: float | None
    property_value_133: float | None
    property_value_134: float | None
    property_value_135: float | None
    property_value_136: float | None
    property_value_137: float | None
    property_value_138: float | None
    property_value_139: float | None
    property_value_140: float | None
    property_value_141: float | None
    property_value_142: float | None
    property_value_143: float | None
    property_value_144: float | None
    property_value_145: float | None
    property_value_146: float | None
    property_value_147: float | None
    property_value_148: float | None
    property_value_149: float | None
    property_value_150: float | None
    property_value_151: float | None
    property_value_152: float | None
    property_value_153: float | None
    property_value_154: float | None
    property_value_155: float | None
    property_value_156: float | None
    property_value_157: float | None
    property_value_158: float | None
    property_value_159: float | None
    property_value_160: float | None
    property_value_161: float | None
    property_value_162: float | None
    property_value_163: float | None
    property_value_164: float | None
    property_value_165: float | None
    property_value_166: float | None
    property_value_167: float | None
    property_value_168: float | None
    property_value_169: float | None
    property_value_170: float | None
    property_value_171: float | None
    property_value_172: float | None
    property_value_173: float | None
    property_value_174: float | None
    property_value_175: float | None
    property_value_176: float | None
    property_value_177: float | None
    property_value_178: float | None
    property_value_179: float | None
    property_value_180: float | None
    property_value_181: float | None
    property_value_182: float | None
    property_value_183: float | None
    property_value_184: float | None
    property_value_185: float | None
    property_value_186: float | None
    property_value_187: float | None
    property_value_188: float | None
    property_value_189: float | None
    property_value_190: float | None
    property_value_191: float | None
    property_value_192: float | None
    property_value_193: float | None
    property_value_194: float | None
    property_value_195: float | None
    property_value_196: float | None
    property_value_197: float | None
    property_value_198: float | None
    property_value_199: float | None
    property_value_200: float | None
    property_value_201: float | None
    property_value_202: float | None
    property_value_203: float | None
    property_value_204: float | None
    property_value_205: float | None
    property_value_206: float | None
    property_value_207: float | None
    property_value_208: float | None
    property_value_209: float | None
    property_value_210: float | None
    property_value_211: float | None
    property_value_212: float | None
    property_value_213: float | None
    property_value_214: float | None
    property_value_215: float | None
    property_value_216: float | None
    property_value_217: float | None
    property_value_218: float | None
    property_value_219: float | None
    property_value_220: float | None
    property_value_221: float | None
    property_value_222: float | None
    property_value_223: float | None
    property_value_224: float | None
    property_value_225: float | None
    property_value_226: float | None
    property_value_227: float | None
    property_value_228: float | None
    property_value_229: float | None
    property_value_230: float | None
    property_value_231: float | None
    property_value_232: float | None
    property_value_233: float | None
    property_value_234: float | None
    property_value_235: float | None
    property_value_236: float | None
    property_value_237: float | None
    property_value_238: float | None
    property_value_239: float | None
    property_value_240: float | None
    property_value_241: float | None
    property_value_242: float | None
    property_value_243: float | None
    property_value_244: float | None
    property_value_245: float | None
    property_value_246: float | None
    property_value_247: float | None
    property_value_248: float | None
    property_value_249: float | None
    property_value_250: float | None

class FluidPropertiesConcentration(IDFObject):
    fluid_property_type: str | None
    temperature_values_name: str | None
    concentration: float | None
    property_value_1: float | None
    property_value_2: float | None
    property_value_3: float | None
    property_value_4: float | None
    property_value_5: float | None
    property_value_6: float | None
    property_value_7: float | None
    property_value_8: float | None
    property_value_9: float | None
    property_value_10: float | None
    property_value_11: float | None
    property_value_12: float | None
    property_value_13: float | None
    property_value_14: float | None
    property_value_15: float | None
    property_value_16: float | None
    property_value_17: float | None
    property_value_18: float | None
    property_value_19: float | None
    property_value_20: float | None
    property_value_21: float | None
    property_value_22: float | None
    property_value_23: float | None
    property_value_24: float | None
    property_value_25: float | None
    property_value_26: float | None
    property_value_27: float | None
    property_value_28: float | None
    property_value_29: float | None
    property_value_30: float | None
    property_value_31: float | None
    property_value_32: float | None
    property_value_33: float | None
    property_value_34: float | None
    property_value_35: float | None
    property_value_36: float | None
    property_value_37: float | None
    property_value_38: float | None
    property_value_39: float | None
    property_value_40: float | None
    property_value_41: float | None
    property_value_42: float | None
    property_value_43: float | None
    property_value_44: float | None
    property_value_45: float | None
    property_value_46: float | None
    property_value_47: float | None
    property_value_48: float | None
    property_value_49: float | None
    property_value_50: float | None
    property_value_51: float | None
    property_value_52: float | None
    property_value_53: float | None
    property_value_54: float | None
    property_value_55: float | None
    property_value_56: float | None
    property_value_57: float | None
    property_value_58: float | None
    property_value_59: float | None
    property_value_60: float | None
    property_value_61: float | None
    property_value_62: float | None
    property_value_63: float | None
    property_value_64: float | None
    property_value_65: float | None
    property_value_66: float | None
    property_value_67: float | None
    property_value_68: float | None
    property_value_69: float | None
    property_value_70: float | None
    property_value_71: float | None
    property_value_72: float | None
    property_value_73: float | None
    property_value_74: float | None
    property_value_75: float | None
    property_value_76: float | None
    property_value_77: float | None
    property_value_78: float | None
    property_value_79: float | None
    property_value_80: float | None
    property_value_81: float | None
    property_value_82: float | None
    property_value_83: float | None
    property_value_84: float | None
    property_value_85: float | None
    property_value_86: float | None
    property_value_87: float | None
    property_value_88: float | None
    property_value_89: float | None
    property_value_90: float | None
    property_value_91: float | None
    property_value_92: float | None
    property_value_93: float | None
    property_value_94: float | None
    property_value_95: float | None
    property_value_96: float | None
    property_value_97: float | None
    property_value_98: float | None
    property_value_99: float | None
    property_value_100: float | None
    property_value_101: float | None
    property_value_102: float | None
    property_value_103: float | None
    property_value_104: float | None
    property_value_105: float | None
    property_value_106: float | None
    property_value_107: float | None
    property_value_108: float | None
    property_value_109: float | None
    property_value_110: float | None
    property_value_111: float | None
    property_value_112: float | None
    property_value_113: float | None
    property_value_114: float | None
    property_value_115: float | None
    property_value_116: float | None
    property_value_117: float | None
    property_value_118: float | None
    property_value_119: float | None
    property_value_120: float | None
    property_value_121: float | None
    property_value_122: float | None
    property_value_123: float | None
    property_value_124: float | None
    property_value_125: float | None
    property_value_126: float | None
    property_value_127: float | None
    property_value_128: float | None
    property_value_129: float | None
    property_value_130: float | None
    property_value_131: float | None
    property_value_132: float | None
    property_value_133: float | None
    property_value_134: float | None
    property_value_135: float | None
    property_value_136: float | None
    property_value_137: float | None
    property_value_138: float | None
    property_value_139: float | None
    property_value_140: float | None
    property_value_141: float | None
    property_value_142: float | None
    property_value_143: float | None
    property_value_144: float | None
    property_value_145: float | None
    property_value_146: float | None
    property_value_147: float | None
    property_value_148: float | None
    property_value_149: float | None
    property_value_150: float | None
    property_value_151: float | None
    property_value_152: float | None
    property_value_153: float | None
    property_value_154: float | None
    property_value_155: float | None
    property_value_156: float | None
    property_value_157: float | None
    property_value_158: float | None
    property_value_159: float | None
    property_value_160: float | None
    property_value_161: float | None
    property_value_162: float | None
    property_value_163: float | None
    property_value_164: float | None
    property_value_165: float | None
    property_value_166: float | None
    property_value_167: float | None
    property_value_168: float | None
    property_value_169: float | None
    property_value_170: float | None
    property_value_171: float | None
    property_value_172: float | None
    property_value_173: float | None
    property_value_174: float | None
    property_value_175: float | None
    property_value_176: float | None
    property_value_177: float | None
    property_value_178: float | None
    property_value_179: float | None
    property_value_180: float | None
    property_value_181: float | None
    property_value_182: float | None
    property_value_183: float | None
    property_value_184: float | None
    property_value_185: float | None
    property_value_186: float | None
    property_value_187: float | None
    property_value_188: float | None
    property_value_189: float | None
    property_value_190: float | None
    property_value_191: float | None
    property_value_192: float | None
    property_value_193: float | None
    property_value_194: float | None
    property_value_195: float | None
    property_value_196: float | None
    property_value_197: float | None
    property_value_198: float | None
    property_value_199: float | None
    property_value_200: float | None
    property_value_201: float | None
    property_value_202: float | None
    property_value_203: float | None
    property_value_204: float | None
    property_value_205: float | None
    property_value_206: float | None
    property_value_207: float | None
    property_value_208: float | None
    property_value_209: float | None
    property_value_210: float | None
    property_value_211: float | None
    property_value_212: float | None
    property_value_213: float | None
    property_value_214: float | None
    property_value_215: float | None
    property_value_216: float | None
    property_value_217: float | None
    property_value_218: float | None
    property_value_219: float | None
    property_value_220: float | None
    property_value_221: float | None
    property_value_222: float | None
    property_value_223: float | None
    property_value_224: float | None
    property_value_225: float | None
    property_value_226: float | None
    property_value_227: float | None
    property_value_228: float | None
    property_value_229: float | None
    property_value_230: float | None
    property_value_231: float | None
    property_value_232: float | None
    property_value_233: float | None
    property_value_234: float | None
    property_value_235: float | None
    property_value_236: float | None
    property_value_237: float | None
    property_value_238: float | None
    property_value_239: float | None
    property_value_240: float | None
    property_value_241: float | None
    property_value_242: float | None
    property_value_243: float | None
    property_value_244: float | None
    property_value_245: float | None
    property_value_246: float | None
    property_value_247: float | None
    property_value_248: float | None
    property_value_249: float | None
    property_value_250: float | None

class CurrencyType(IDFObject): ...

class ComponentCostAdjustments(IDFObject):
    design_and_engineering_fees: float | None
    contractor_fee: float | None
    contingency: float | None
    permits_bonding_and_insurance: float | None
    commissioning_fee: float | None
    regional_adjustment_factor: float | None

class ComponentCostReference(IDFObject):
    reference_building_miscellaneous_cost_per_conditioned_area: float | None
    reference_building_design_and_engineering_fees: float | None
    reference_building_contractor_fee: float | None
    reference_building_contingency: float | None
    reference_building_permits_bonding_and_insurance: float | None
    reference_building_commissioning_fee: float | None
    reference_building_regional_adjustment_factor: float | None

class ComponentCostLineItem(IDFObject):
    type: str | None
    line_item_type: str | None
    item_name: str | None
    object_end_use_key: str | None
    cost_per_each: float | None
    cost_per_area: float | None
    cost_per_unit_of_output_capacity: float | None
    cost_per_unit_of_output_capacity_per_cop: float | None
    cost_per_volume: float | None
    cost_per_volume_rate: float | None
    cost_per_energy_per_temperature_difference: float | None
    quantity: float | None

class UtilityCostTariff(IDFObject):
    output_meter_name: str | None
    conversion_factor_choice: str | None
    energy_conversion_factor: float | None
    demand_conversion_factor: float | None
    time_of_use_period_schedule_name: str | None
    season_schedule_name: str | None
    month_schedule_name: str | None
    demand_window_length: str | None
    monthly_charge_or_variable_name: float | str | None
    minimum_monthly_charge_or_variable_name: float | str | None
    real_time_pricing_charge_schedule_name: str | None
    customer_baseline_load_schedule_name: str | None
    group_name: str | None
    buy_or_sell: str | None

class UtilityCostQualify(IDFObject):
    tariff_name: str | None
    variable_name: str | None
    qualify_type: str | None
    threshold_value_or_variable_name: float | str | None
    season: str | None
    threshold_test: str | None
    number_of_months: float | None

class UtilityCostChargeSimple(IDFObject):
    tariff_name: str | None
    source_variable: str | None
    season: str | None
    category_variable_name: str | None
    cost_per_unit_value_or_variable_name: float | str | None

class UtilityCostChargeBlock(IDFObject):
    tariff_name: str | None
    source_variable: str | None
    season: str | None
    category_variable_name: str | None
    remaining_into_variable: str | None
    block_size_multiplier_value_or_variable_name: float | str | None
    block_size_1_value_or_variable_name: float | str | None
    block_1_cost_per_unit_value_or_variable_name: float | str | None
    block_size_2_value_or_variable_name: float | str | None
    block_2_cost_per_unit_value_or_variable_name: float | str | None
    block_size_3_value_or_variable_name: float | str | None
    block_3_cost_per_unit_value_or_variable_name: float | str | None
    block_size_4_value_or_variable_name: float | str | None
    block_4_cost_per_unit_value_or_variable_name: float | str | None
    block_size_5_value_or_variable_name: float | str | None
    block_5_cost_per_unit_value_or_variable_name: float | str | None
    block_size_6_value_or_variable_name: float | str | None
    block_6_cost_per_unit_value_or_variable_name: float | str | None
    block_size_7_value_or_variable_name: float | str | None
    block_7_cost_per_unit_value_or_variable_name: float | str | None
    block_size_8_value_or_variable_name: float | str | None
    block_8_cost_per_unit_value_or_variable_name: float | str | None
    block_size_9_value_or_variable_name: float | str | None
    block_9_cost_per_unit_value_or_variable_name: float | str | None
    block_size_10_value_or_variable_name: float | str | None
    block_10_cost_per_unit_value_or_variable_name: float | str | None
    block_size_11_value_or_variable_name: float | str | None
    block_11_cost_per_unit_value_or_variable_name: float | str | None
    block_size_12_value_or_variable_name: float | str | None
    block_12_cost_per_unit_value_or_variable_name: float | str | None
    block_size_13_value_or_variable_name: float | str | None
    block_13_cost_per_unit_value_or_variable_name: float | str | None
    block_size_14_value_or_variable_name: float | str | None
    block_14_cost_per_unit_value_or_variable_name: float | str | None
    block_size_15_value_or_variable_name: float | str | None
    block_15_cost_per_unit_value_or_variable_name: float | str | None

class UtilityCostRatchet(IDFObject):
    tariff_name: str | None
    baseline_source_variable: str | None
    adjustment_source_variable: str | None
    season_from: str | None
    season_to: str | None
    multiplier_value_or_variable_name: float | str | None
    offset_value_or_variable_name: float | str | None

class UtilityCostVariable(IDFObject):
    tariff_name: str | None
    variable_type: str | None
    january_value: float | None
    february_value: float | None
    march_value: float | None
    april_value: float | None
    may_value: float | None
    june_value: float | None
    july_value: float | None
    august_value: float | None
    september_value: float | None
    october_value: float | None
    november_value: float | None
    december_value: float | None

class UtilityCostComputation(IDFObject):
    tariff_name: str | None
    compute_step_1: str | None
    compute_step_2: str | None
    compute_step_3: str | None
    compute_step_4: str | None
    compute_step_5: str | None
    compute_step_6: str | None
    compute_step_7: str | None
    compute_step_8: str | None
    compute_step_9: str | None
    compute_step_10: str | None
    compute_step_11: str | None
    compute_step_12: str | None
    compute_step_13: str | None
    compute_step_14: str | None
    compute_step_15: str | None
    compute_step_16: str | None
    compute_step_17: str | None
    compute_step_18: str | None
    compute_step_19: str | None
    compute_step_20: str | None
    compute_step_21: str | None
    compute_step_22: str | None
    compute_step_23: str | None
    compute_step_24: str | None
    compute_step_25: str | None
    compute_step_26: str | None
    compute_step_27: str | None
    compute_step_28: str | None
    compute_step_29: str | None
    compute_step_30: str | None

class LifeCycleCostParameters(IDFObject):
    discounting_convention: str | None
    inflation_approach: str | None
    real_discount_rate: float | None
    nominal_discount_rate: float | None
    inflation: float | None
    base_date_month: str | None
    base_date_year: int | None
    service_date_month: str | None
    service_date_year: int | None
    length_of_study_period_in_years: int | None
    tax_rate: float | None
    depreciation_method: str | None

class LifeCycleCostRecurringCosts(IDFObject):
    category: str | None
    cost: float | None
    start_of_costs: str | None
    years_from_start: int | None
    months_from_start: int | None
    repeat_period_years: int | None
    repeat_period_months: int | None
    annual_escalation_rate: float | None

class LifeCycleCostNonrecurringCost(IDFObject):
    category: str | None
    cost: float | None
    start_of_costs: str | None
    years_from_start: int | None
    months_from_start: int | None

class LifeCycleCostUsePriceEscalation(IDFObject):
    resource: str | None
    escalation_start_year: int | None
    escalation_start_month: str | None
    year_escalation: float | None

class LifeCycleCostUseAdjustment(IDFObject):
    resource: str | None
    year_multiplier: float | None

class ParametricSetValueForRun(IDFObject):
    value_for_run: str | None

class ParametricLogic(IDFObject):
    parametric_logic_line: str | None

class ParametricRunControl(IDFObject):
    perform_run: str | None

class ParametricFileNameSuffix(IDFObject):
    suffix_for_file_name_in_run: str | None

class OutputVariableDictionary(IDFObject):
    sort_option: str | None

class OutputSurfacesList(IDFObject):
    report_specifications: str | None

class OutputSurfacesDrawing(IDFObject):
    report_specifications_1: str | None
    report_specifications_2: str | None

class OutputSchedules(IDFObject): ...

class OutputConstructions(IDFObject):
    details_type_2: str | None

class OutputEnergyManagementSystem(IDFObject):
    internal_variable_availability_dictionary_reporting: str | None
    ems_runtime_language_debug_output_level: str | None

class OutputControlSurfaceColorScheme(IDFObject):
    drawing_element_1_type: str | None
    color_for_drawing_element_1: int | None
    drawing_element_2_type: str | None
    color_for_drawing_element_2: int | None
    drawing_element_3_type: str | None
    color_for_drawing_element_3: int | None
    drawing_element_4_type: str | None
    color_for_drawing_element_4: int | None
    drawing_element_5_type: str | None
    color_for_drawing_element_5: int | None
    drawing_element_6_type: str | None
    color_for_drawing_element_6: int | None
    drawing_element_7_type: str | None
    color_for_drawing_element_7: int | None
    drawing_element_8_type: str | None
    color_for_drawing_element_8: int | None
    drawing_element_9_type: str | None
    color_for_drawing_element_9: int | None
    drawing_element_10_type: str | None
    color_for_drawing_element_10: int | None
    drawing_element_11_type: str | None
    color_for_drawing_element_11: int | None
    drawing_element_12_type: str | None
    color_for_drawing_element_12: int | None
    drawing_element_13_type: str | None
    color_for_drawing_element_13: int | None
    drawing_element_14_type: str | None
    color_for_drawing_element_14: int | None
    drawing_element_15_type: str | None
    color_for_drawing_element_15: int | None

class OutputTableSummaryReports(IDFObject):
    report_name: str | None

class OutputTableTimeBins(IDFObject):
    variable_name: str | None
    interval_start: float | None
    interval_size: float | None
    interval_count: int | None
    schedule_name: str | None
    variable_type: str | None

class OutputTableMonthly(IDFObject):
    digits_after_decimal: int | None
    variable_or_meter_name: str | None
    aggregation_type_for_variable_or_meter: str | None

class OutputTableAnnual(IDFObject):
    filter: str | None
    schedule_name: str | None
    variable_or_meter_or_ems_variable_or_field_name: str | None
    aggregation_type_for_variable_or_meter: str | None
    digits_after_decimal: float | None

class OutputTableReportPeriod(IDFObject):
    report_name: str | None
    begin_year: int | None
    begin_month: int | None
    begin_day_of_month: int | None
    begin_hour_of_day: int | None
    end_year: int | None
    end_month: int | None
    end_day_of_month: int | None
    end_hour_of_day: int | None

class OutputControlTableStyle(IDFObject):
    unit_conversion: str | None
    format_numeric_values: str | None

class OutputControlReportingTolerances(IDFObject):
    tolerance_for_time_cooling_setpoint_not_met: float | None

class OutputControlResilienceSummaries(IDFObject): ...

class OutputVariable(IDFObject):
    variable_name: str | None
    reporting_frequency: str | None
    schedule_name: str | None

class OutputMeter(IDFObject):
    reporting_frequency: str | None

class OutputMeterMeterFileOnly(IDFObject):
    reporting_frequency: str | None

class OutputMeterCumulative(IDFObject):
    reporting_frequency: str | None

class OutputMeterCumulativeMeterFileOnly(IDFObject):
    reporting_frequency: str | None

class MeterCustom(IDFObject):
    resource_type: str | None
    key_name: str | None
    output_variable_or_meter_name: str | None

class MeterCustomDecrement(IDFObject):
    resource_type: str | None
    source_meter_name: str | None
    key_name: str | None
    output_variable_or_meter_name: str | None

class OutputControlFiles(IDFObject):
    output_mtr: str | None
    output_eso: str | None
    output_eio: str | None
    output_tabular: str | None
    output_sqlite: str | None
    output_json: str | None
    output_audit: str | None
    output_space_sizing: str | None
    output_zone_sizing: str | None
    output_system_sizing: str | None
    output_dxf: str | None
    output_bnd: str | None
    output_rdd: str | None
    output_mdd: str | None
    output_mtd: str | None
    output_end: str | None
    output_shd: str | None
    output_dfs: str | None
    output_glhe: str | None
    output_delightin: str | None
    output_delighteldmp: str | None
    output_delightdfdmp: str | None
    output_edd: str | None
    output_dbg: str | None
    output_perflog: str | None
    output_sln: str | None
    output_sci: str | None
    output_wrl: str | None
    output_screen: str | None
    output_extshd: str | None
    output_tarcog: str | None
    output_plant_component_sizing: str | None

class OutputControlTimestamp(IDFObject):
    timestamp_at_beginning_of_interval: str | None

class OutputJSON(IDFObject):
    output_json: str | None
    output_cbor: str | None
    output_messagepack: str | None
    unit_conversion_for_tabular_data: str | None
    format_numeric_values_for_tabular_data: str | None

class OutputSQLite(IDFObject):
    unit_conversion_for_tabular_data: str | None
    format_numeric_values_for_tabular_data: str | None

class OutputEnvironmentalImpactFactors(IDFObject): ...

class EnvironmentalImpactFactors(IDFObject):
    district_cooling_cop: float | None
    district_heating_steam_conversion_efficiency: float | None
    total_carbon_equivalent_emission_factor_from_n2o: float | None
    total_carbon_equivalent_emission_factor_from_ch4: float | None
    total_carbon_equivalent_emission_factor_from_co2: float | None

class FuelFactors(IDFObject):
    source_energy_factor: float | None
    source_energy_schedule_name: str | None
    co2_emission_factor: float | None
    co2_emission_factor_schedule_name: str | None
    co_emission_factor: float | None
    co_emission_factor_schedule_name: str | None
    ch4_emission_factor: float | None
    ch4_emission_factor_schedule_name: str | None
    nox_emission_factor: float | None
    nox_emission_factor_schedule_name: str | None
    n2o_emission_factor: float | None
    n2o_emission_factor_schedule_name: str | None
    so2_emission_factor: float | None
    so2_emission_factor_schedule_name: str | None
    pm_emission_factor: float | None
    pm_emission_factor_schedule_name: str | None
    pm10_emission_factor: float | None
    pm10_emission_factor_schedule_name: str | None
    pm2_5_emission_factor: float | None
    pm2_5_emission_factor_schedule_name: str | None
    nh3_emission_factor: float | None
    nh3_emission_factor_schedule_name: str | None
    nmvoc_emission_factor: float | None
    nmvoc_emission_factor_schedule_name: str | None
    hg_emission_factor: float | None
    hg_emission_factor_schedule_name: str | None
    pb_emission_factor: float | None
    pb_emission_factor_schedule_name: str | None
    water_emission_factor: float | None
    water_emission_factor_schedule_name: str | None
    nuclear_high_level_emission_factor: float | None
    nuclear_high_level_emission_factor_schedule_name: str | None
    nuclear_low_level_emission_factor: float | None
    nuclear_low_level_emission_factor_schedule_name: str | None

class OutputDiagnostics(IDFObject):
    key: str | None

class OutputDebuggingData(IDFObject):
    report_during_warmup: str | None

class OutputPreprocessorMessage(IDFObject):
    error_severity: str | None
    message_line_1: str | None
    message_line_2: str | None
    message_line_3: str | None
    message_line_4: str | None
    message_line_5: str | None
    message_line_6: str | None
    message_line_7: str | None
    message_line_8: str | None
    message_line_9: str | None
    message_line_10: str | None

class PythonPluginSearchPaths(IDFObject):
    add_current_working_directory_to_search_path: str | None
    add_input_file_directory_to_search_path: str | None
    add_epin_environment_variable_to_search_path: str | None
    search_path: str | None

class PythonPluginInstance(IDFObject):
    run_during_warmup_days: str | None
    python_module_name: str | None
    plugin_class_name: str | None

class PythonPluginVariables(IDFObject):
    variable_name: str | None

class PythonPluginTrendVariable(IDFObject):
    name_of_a_python_plugin_variable: str | None
    number_of_timesteps_to_be_logged: int | None

class PythonPluginOutputVariable(IDFObject):
    python_plugin_variable_name: str | None
    type_of_data_in_variable: str | None
    update_frequency: str | None
    units: str | None
    resource_type: str | None
    group_type: str | None
    end_use_category: str | None
    end_use_subcategory: str | None
