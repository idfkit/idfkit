# How-to guides

Each guide here takes one task and walks it to a result. They assume you know
what you want and are looking for the shortest correct route; if you are still
learning the shape of the library, start with the
[Tutorials](../tutorials/index.md) instead.

For exact signatures, options, and return types, see the
[Reference](../reference/index.md). For why something works the way it does,
see [Explanation](../explanation/index.md).

Most guides show the same task in both languages, one tab each. Where a task
exists in only one of them, the guide says so on its first screen.

## Getting set up

- [Common tasks](../getting-started/quick-start.md): quick recipes for load,
  query, modify, simulate, and round-trip
- [How to install idfkit](../getting-started/installation.md)
- [How to migrate from eppy](../migration.md)

## Reading and editing models

- [How to collect diagnostics instead of throwing](collect-diagnostics.md):
  what an editor, a language server, or a batch job needs from a bad file
- [How to edit extensible groups](edit-extensible-groups.md): vertices, branch
  lists, and anything else that repeats
- [How to compare two EnergyPlus versions](compare-versions.md): what changed
  between two releases, and whether a model survives the move

## In the browser

These two are TypeScript only, because there is no Python browser runtime.

- [How to parse in the browser](parse-in-the-browser.md): serve the schema
  bundle and keep the parse synchronous
- [How to run a simulation in the browser](run-a-simulation-in-the-browser.md):
  hand a model to `@idfkit/engine` and read the results back

## Working with simulations

Running EnergyPlus locally is Python only, and needs an EnergyPlus
installation on the machine.

- [Simulation overview](../simulation/index.md)
- [How to run a simulation](../simulation/running.md)
- [How to run simulations asynchronously](../simulation/async.md)
- [How to access simulation results](../simulation/results.md)
- [How to query simulation SQL output](../simulation/sql-queries.md)
- [How to run batch simulations](../simulation/batch.md)
- [How to track simulation progress](../simulation/progress.md)
- [How to cache simulation results](../simulation/caching.md)
- [How to plot simulation results](../simulation/plotting.md)
- [How to discover output variables](../simulation/output-discovery.md)
- [How to handle simulation errors](../simulation/errors.md)
- [How to migrate models between EnergyPlus versions](../simulation/migrating-versions.md)
- [Design-day sizing workflow](../examples/sizing-workflow.ipynb)
- [Run a parametric study](../examples/parametric-study.ipynb)

## Weather data

- [Weather overview](../weather/index.md)
- [How to search for weather stations](../weather/station-search.md)
- [How to download weather files](../weather/downloads.md)
- [How to apply design days](../weather/design-days.md)
- [How to geocode addresses](../weather/geocoding.md)
- [How to warm the weather cache for an offline run](warm-the-weather-cache.md)

## Schedules

- [How to evaluate schedules](../schedules/index.md)

## Scaling out

- [How to use cloud and remote storage](../concepts/cloud-storage.md)
- [How to store simulation results in S3](../examples/cloud-simulations.md)
- [How to run simulations as Celery tasks](../examples/celery-integration.md)
- [How to run distributed simulations with Scythe](../examples/scythe.md)

## Configuring and operating

- [How to configure logging](../concepts/logging.md)
- [How to check version compatibility](../concepts/version-compatibility.md)

## When things go wrong

- [Common errors](../troubleshooting/errors.md)
- [EnergyPlus issues](../troubleshooting/energyplus.md)
