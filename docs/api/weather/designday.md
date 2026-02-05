# Design Days API

Design day parsing, classification, and model injection.

## DesignDayManager

::: idfkit.weather.designday.DesignDayManager
    options:
      show_root_heading: true
      show_source: true
      members:
        - annual
        - monthly
        - location
        - get
        - apply_to_model
        - summary

## DesignDayType

::: idfkit.weather.designday.DesignDayType
    options:
      show_root_heading: true
      show_source: true
      members:
        - HEATING_99_6
        - HEATING_99
        - HTG_WIND_99_6
        - HUMIDIF_99_6
        - COOLING_DB_0_4
        - COOLING_DB_1
        - COOLING_DB_2
        - COOLING_WB_0_4
        - COOLING_WB_1
        - COOLING_WB_2
        - COOLING_ENTH_0_4
        - COOLING_ENTH_1
        - COOLING_ENTH_2
        - DEHUMID_0_4
        - DEHUMID_1
        - DEHUMID_2
        - MONTHLY

## apply_ashrae_sizing

::: idfkit.weather.designday.apply_ashrae_sizing
    options:
      show_root_heading: true
      show_source: true

## NoDesignDaysError

See [`NoDesignDaysError`](../exceptions.md#idfkit.exceptions.NoDesignDaysError) in the Exceptions API.
