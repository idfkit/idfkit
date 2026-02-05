# Batch API

Parallel simulation execution with thread-pool parallelism.

## simulate_batch

::: idfkit.simulation.batch.simulate_batch
    options:
      show_root_heading: true
      show_source: true

## SimulationJob

::: idfkit.simulation.batch.SimulationJob
    options:
      show_root_heading: true
      show_source: true
      members:
        - model
        - weather
        - label
        - output_dir
        - expand_objects
        - annual
        - design_day
        - output_prefix
        - output_suffix
        - readvars
        - timeout
        - extra_args

## BatchResult

::: idfkit.simulation.batch.BatchResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - results
        - total_runtime_seconds
        - succeeded
        - failed
        - all_succeeded
