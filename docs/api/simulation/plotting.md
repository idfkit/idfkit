# Plotting API

Pluggable plotting backends for result visualization.

## PlotBackend Protocol

::: idfkit.simulation.plotting.PlotBackend
    options:
      show_root_heading: true
      show_source: true

## get_default_backend

::: idfkit.simulation.plotting.get_default_backend
    options:
      show_root_heading: true
      show_source: true

## Built-in Visualizations

### plot_temperature_profile

::: idfkit.simulation.plotting.visualizations.plot_temperature_profile
    options:
      show_root_heading: true
      show_source: true

### plot_energy_balance

::: idfkit.simulation.plotting.visualizations.plot_energy_balance
    options:
      show_root_heading: true
      show_source: true

### plot_comfort_hours

::: idfkit.simulation.plotting.visualizations.plot_comfort_hours
    options:
      show_root_heading: true
      show_source: true

## Backend Implementations

### MatplotlibBackend

::: idfkit.simulation.plotting.matplotlib.MatplotlibBackend
    options:
      show_root_heading: true
      show_source: true

### PlotlyBackend

::: idfkit.simulation.plotting.plotly.PlotlyBackend
    options:
      show_root_heading: true
      show_source: true
