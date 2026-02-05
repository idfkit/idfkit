# SQL API

SQLite output database parsing and query interface.

## SQLResult

::: idfkit.simulation.parsers.sql.SQLResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - path
        - get_timeseries
        - get_tabular_data
        - get_available_variables
        - get_environments

## TimeSeriesResult

::: idfkit.simulation.parsers.sql.TimeSeriesResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - variable_name
        - key_value
        - units
        - frequency
        - timestamps
        - values
        - to_dataframe
        - plot

## TabularRow

::: idfkit.simulation.parsers.sql.TabularRow
    options:
      show_root_heading: true
      show_source: true
      members:
        - report_name
        - report_for
        - table_name
        - row_name
        - column_name
        - units
        - value

## VariableInfo

::: idfkit.simulation.parsers.sql.VariableInfo
    options:
      show_root_heading: true
      show_source: true
      members:
        - name
        - key_value
        - frequency
        - units
        - is_meter
        - variable_type

## EnvironmentInfo

::: idfkit.simulation.parsers.sql.EnvironmentInfo
    options:
      show_root_heading: true
      show_source: true
      members:
        - index
        - name
        - environment_type
