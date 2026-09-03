# How to download weather files

You have a weather station and you need its files: the EPW for an annual run,
the DDY for design-day sizing. This guide fetches them, by station or by
canonical EPW filename, one at a time or in bulk. To choose the station in the
first place, see [How to search for weather stations](station-search.md).

One difference runs through everything below. Python downloads into a cache
directory and hands back `Path` objects. TypeScript writes nothing to disk and
hands back the file contents as text. Neither is a reduced version of the other:
a browser has no filesystem to cache into, and a Python caller is about to pass
a path to EnergyPlus.

!!! info "In JavaScript, weather is a separate install"
    `pip install idfkit` installs weather support and its station index
    unconditionally. `npm install idfkit` installs neither. `@idfkit/weather` is
    an optional peer dependency of the shared `idfkit` package, so the installer
    leaves it out by default and the 1.7 MB station index stays off disk for
    everyone who never asks for weather. Importing `idfkit/weather` without it
    fails with a message naming the package to install. See [How to install
    idfkit](../getting-started/installation.md#weather-is-a-separate-install-in-javascript),
    which also covers the fact that the npm packages are not published yet.

!!! tip "Prefer the shell?"
    The [`idfkit tmy`](../cli/tmy.md) CLI wraps the Python API for interactive
    use. Pass `--download DIR` to fetch the EPW/DDY/STAT bundle for a station
    without writing any code. There is no JavaScript equivalent.

{{ parity("weather-download") }}

## How weather is installed

=== "Python"

    Weather comes with the library. `pip install idfkit` installs the station
    index whether or not you asked for it, because a Python extra gates
    dependencies rather than files.

    ```bash
    pip install idfkit
    ```

=== "TypeScript"

    Weather is an opt-in install and the shared name does not reach it. `npm
    install idfkit` places no station index on disk and no weather code in your
    bundle; add the package by name.

    ```bash
    npm install @idfkit/weather
    ```

## Download the files for a station

Resolve a station, then ask for its files.

=== "Python"

    ```python
    --8<-- "docs/snippets/weather/downloads/basic_usage.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/weather/downloads/download_the_files_for_a_station.ts:example"
    ```

`loadBundledIndex` reads the index shipped inside the package, off disk and with
no network call, so it exists only in Node. In a browser, serve the index from
your own origin and load it with `loadStationIndex`; [How to search for weather
stations](station-search.md) covers both paths.

## Download by canonical EPW filename

When you already have the filename, skip the station lookup.

=== "Python"

    ```python
    --8<-- "docs/snippets/weather/downloads/download_by_filename.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/weather/downloads/download_by_canonical_epw_filename.ts:example"
    ```

The index does the resolving in both languages, but it arrives differently.
Python's `index` argument is optional and defaults to the bundled index, because
it can always find one on disk. TypeScript's is required, because the caller had
to obtain an index already and the function has nowhere to load one from. Either
way, a filename matching no station raises rather than returning nothing.

## Extract only the files you need

By default `download()` extracts the whole bundle and requires both an EPW and a
DDY to be present. Pass `only={".epw"}`, or any iterable of suffixes, to extract
just the members you want: useful when the EPW alone will do, or when iterating
over thousands of stations. Matching ignores case, so `".EPW"` and `"epw"` both
select `.epw`.

```python
--8<-- "docs/snippets/weather/downloads/selective_extraction.py:example"
```

There is no TypeScript counterpart, and that is not a gap. Selective extraction
is a property of writing into a cache; the JavaScript side decodes from memory
whatever the archive held, and carries the undecoded members beside it.

## What a download returns

The record carries the same station and the same three weather files in both
languages, and the fields that matter most hold different values.

| Field | Python (`WeatherFiles`) | TypeScript (`WeatherFiles`) |
|-------|-------------------------|-----------------------------|
| `epw` | `Path` to the extracted EPW | the EPW text |
| `ddy` | `Path` to the extracted DDY | the DDY text, or `null` |
| `stat` | `Path` to the STAT file, or `None` | the STAT text, or `null` |
| `zip_path` | `Path` to the downloaded ZIP archive | not present |
| `members` | not present | every archive member as bytes, by filename |
| `station` | the `WeatherStation` downloaded | the `WeatherStation` downloaded |

The names collide deliberately: `files.epw` is a path in Python and the file
contents in TypeScript, so code written from one language's documentation
against the other is wrong at runtime rather than merely awkward. [Parity with
the Python library](../explanation/parity.md) records the difference and its
cause.

```python
--8<-- "docs/snippets/weather/downloads/weatherfiles.py:example"
```

### Selective extraction returns a `PartialWeatherFiles`

`download(station, only=...)` returns a `PartialWeatherFiles` instead: the same
record with `epw`, `ddy`, and `stat` each `Path | None`. A field is `None` when
its suffix was neither requested nor already sitting in the cache from an
earlier download, so a suffix you did not ask for this time may still come back
populated.

| Attribute | Type | Description |
|-----------|------|-------------|
| `epw` | <code>Path &#124; None</code> | Path to the EPW file, or `None` if not extracted |
| `ddy` | <code>Path &#124; None</code> | Path to the DDY file, or `None` if not extracted |
| `stat` | <code>Path &#124; None</code> | Path to the STAT file, or `None` if not extracted |
| `zip_path` | `Path` | Path to the original downloaded ZIP archive |
| `station` | `WeatherStation` | The station this download corresponds to |

## Reuse the cache instead of the network

Python caches; TypeScript does not. `WeatherDownloader.download()` checks the
cache, fetches the station's ZIP only if it has to, extracts the requested
members, stores them, and returns their paths, so the second call for a station
costs no network at all. `fetchWeatherFiles` re-downloads every time, because
there is nowhere in a browser to put the result. Hold on to the text you were
given.

```python
--8<-- "docs/snippets/weather/downloads/caching.py:example"
```

### Cache location

| Platform | Default path |
|----------|--------------|
| Linux | `~/.cache/idfkit/weather/files/` |
| macOS | `~/Library/Caches/idfkit/weather/files/` |
| Windows | `%LOCALAPPDATA%\idfkit\cache\weather\files\` |

Set [`IDFKIT_CACHE_DIR`](../concepts/environment-variables.md#idfkit_cache_dir)
to override all three, or pass a directory to one downloader:

```python
--8<-- "docs/snippets/weather/downloads/custom_cache_directory.py:example"
```

### Clear the cache

```python
--8<-- "docs/snippets/weather/downloads/clear_cache.py:example"
```

## Fetch from a page: route around the missing CORS header

climate.onebuilding.org sends no `Access-Control-Allow-Origin` header, so a
direct fetch from a web page is blocked by the browser's same-origin policy.
Python and Node are unaffected; a page needs a forwarding proxy you control that
adds the header. Point `rewriteUrl` at it:

```ts
--8<-- "docs/snippets/js/weather/downloads/fetch_from_a_page_route_around_the_missing_cors_header.ts:example"
```

`rewriteUrl` only changes the URL that gets fetched, so any forwarding proxy
works. Pass your own `fetch` instead when you need to add headers or
authentication.

## Handle a failed download

Both libraries reach the network, so both fail on the things networks fail on:
no connectivity, a station URL that no longer resolves, a server that is
temporarily down.

=== "Python"

    ```python
    --8<-- "docs/snippets/weather/downloads/error_handling.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/weather/downloads/handle_a_failed_download.ts:example"
    ```

## Run offline

Cached files need no network, so pre-downloading the stations a run will use
gets you through the download itself.

```python
--8<-- "docs/snippets/weather/downloads/offline_usage.py:example"
```

!!! warning "Warming the cache is necessary but not sufficient"
    `StationIndex.load()` still fires a throttled freshness check: at most once
    every 24 hours it sends a HEAD request for each of the 10 upstream index
    files. Offline, every one of them fails slowly and silently, and the first
    load of the day can block for minutes before returning an index it already
    had. `IDFKIT_NO_WEATHER_UPDATE_CHECK=1` is what actually suppresses them,
    and the cache has to sit somewhere both the warming environment and the
    isolated run can see. [How to warm the weather cache for an offline
    run](../how-to/warm-the-weather-cache.md) covers the whole setup.

There is nothing to warm in JavaScript, because nothing is cached. That
library's offline story is settled at install time instead: install
`@idfkit/weather` and its bundled index comes with it.

## Download for many stations

```python
--8<-- "docs/snippets/weather/downloads/batch_downloads.py:example"
```

## What EPW and DDY files contain

An **EPW** holds hourly weather for a typical meteorological year: temperature,
humidity, solar radiation, wind, and the rest. It is what an annual simulation
reads.

A **DDY** holds ASHRAE design day conditions as `SizingPeriod:DesignDay`
objects. It is what HVAC sizing reads. See [How to apply design
days](design-days.md) for injecting them into a model.

## Put the files where the simulation will find them

In Python the downloaded paths go straight into `simulate()`:

```python
--8<-- "docs/snippets/weather/downloads/integration_example.py:example"
```

In TypeScript you hold text, so either hand it to an engine that takes text or
write it out first. `saveWeatherFiles` does the writing, in the Latin-1 encoding
EPW uses:

```ts
--8<-- "docs/snippets/js/weather/downloads/put_the_files_where_the_simulation_will_find_them.ts:example"
```

## See also

- [How to search for weather stations](station-search.md) for finding a station,
  and for loading or refreshing the index
- [How to apply design days](design-days.md) for using the DDY
- [How to warm the weather cache for an offline run](../how-to/warm-the-weather-cache.md)
  for air-gapped and CI environments
- [How to install idfkit](../getting-started/installation.md) for the packaging
  difference in full
- [Weather Data Pipeline](../concepts/weather-pipeline.md) for where the data
  comes from and how the index is built
