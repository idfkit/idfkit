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

## ESOColumn

::: idfkit.simulation.parsers.eso.ESOColumn
    options:
      show_root_heading: true
      show_source: true

## ESOVariable

::: idfkit.simulation.parsers.eso.ESOVariable
    options:
      show_root_heading: true
      show_source: true

## ESOEnvironment

::: idfkit.simulation.parsers.eso.ESOEnvironment
    options:
      show_root_heading: true
      show_source: true
