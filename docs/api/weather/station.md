# Station API

Weather station index, search, and geocoding.

## StationIndex

::: idfkit.weather.index.StationIndex
    options:
      show_root_heading: true
      show_source: true
      members:
        - load
        - refresh
        - check_for_updates
        - search
        - nearest
        - filter
        - get_by_wmo
        - countries

## WeatherStation

::: idfkit.weather.station.WeatherStation
    options:
      show_root_heading: true
      show_source: true
      members:
        - city
        - state
        - country
        - wmo
        - source_data
        - latitude
        - longitude
        - time_zone
        - elevation
        - url
        - display_name

## SearchResult

::: idfkit.weather.station.SearchResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - station
        - score

## SpatialResult

::: idfkit.weather.station.SpatialResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - station
        - distance_km

## geocode

::: idfkit.weather.geocode.geocode
    options:
      show_root_heading: true
      show_source: true

## GeocodingError

::: idfkit.weather.geocode.GeocodingError
    options:
      show_root_heading: true
      show_source: true
