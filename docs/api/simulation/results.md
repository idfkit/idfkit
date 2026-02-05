# Results API

Simulation result container and output file access.

## SimulationResult

::: idfkit.simulation.result.SimulationResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - run_dir
        - success
        - exit_code
        - stdout
        - stderr
        - runtime_seconds
        - output_prefix
        - errors
        - sql
        - variables
        - csv
        - sql_path
        - err_path
        - eso_path
        - csv_path
        - html_path
        - rdd_path
        - mdd_path
        - from_directory

## ErrorReport

::: idfkit.simulation.parsers.err.ErrorReport
    options:
      show_root_heading: true
      show_source: true
      members:
        - messages
        - fatal
        - severe
        - warnings
        - fatal_count
        - severe_count
        - warning_count
        - has_fatal
        - has_severe
        - summary
        - from_file
        - from_string

## ErrorMessage

::: idfkit.simulation.parsers.err.ErrorMessage
    options:
      show_root_heading: true
      show_source: true
