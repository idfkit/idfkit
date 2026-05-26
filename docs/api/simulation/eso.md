# ESO / MTR API

High-performance parser for EnergyPlus `.eso` Standard Output and `.mtr` Meter
time-series files. The data dictionary is parsed eagerly; variable data is
extracted lazily with a single targeted scan (`get_column`), or all at once with
`eager=True` / `.columns`.

## ESOResult

::: idfkit.simulation.parsers.eso.ESOResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - from_file
        - from_string
        - from_bytes
        - variables
        - environments
        - columns
        - get_variable
        - get_column
        - to_dataframe

## ESOColumn

::: idfkit.simulation.parsers.eso.ESOColumn
    options:
      show_root_heading: true
      show_source: true
      members:
        - variable
        - environment_index
        - timestamps
        - values
        - to_dataframe
        - plot

## ESOVariable

::: idfkit.simulation.parsers.eso.ESOVariable
    options:
      show_root_heading: true
      show_source: true
      members:
        - report_id
        - variable_name
        - key_value
        - units
        - frequency
        - num_values

## ESOEnvironment

::: idfkit.simulation.parsers.eso.ESOEnvironment
    options:
      show_root_heading: true
      show_source: true
      members:
        - index
        - title
        - latitude
        - longitude
        - time_zone
        - elevation
