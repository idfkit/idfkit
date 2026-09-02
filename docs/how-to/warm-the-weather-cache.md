# How to warm the weather cache for an offline run

Some environments cannot reach the internet when they run: a hardened CI
runner, an air-gapped cluster, a container whose egress is closed by policy.
idfkit is built to work in them, but weather files are the one thing it cannot
invent, so they have to be put on disk while a network is still available.

This guide covers the build-time warm-up: what to pre-download, where to put
it, and the two settings that decide whether the isolated run is silent or
spends five minutes discovering it is offline.

Everything here is Python. There is no equivalent procedure in JavaScript
because there is nothing there to warm: that library keeps no cache directory,
so its offline story is decided at install time rather than at build time.

{{ parity("weather-index") }}

## What needs warming, and what does not

Only the weather **files** need warming. The station index does not.

| Asset | Ships with the package | Needs the network |
|-------|------------------------|-------------------|
| Station index (about 70,000 stations) | yes, as `stations.json.gz` | no |
| EPW and DDY files | no | yes, once per station |
| IP geolocation (`ipgeo.json`) | no | yes, and do not warm it: see below |
| Schemas, validation, introspection, documentation URLs | yes | no |

`StationIndex.load()` reads the bundled index straight off disk. Searching it,
resolving a station, and reading its metadata are all local. Only
`WeatherDownloader.download()` reaches for anything.

!!! note "`StationIndex.refresh()` is optional"
    `refresh()` re-downloads the upstream KML indexes and rebuilds the cached
    index. It is a **freshness update, not a required fetch**. A run that never
    calls it still gets a full station index, just the one that shipped with
    the installed version of idfkit. Do not put `refresh()` in a warm-up script
    unless you specifically want a newer index than the release carries.

## 1. Choose a cache location the isolated run can read

Set [`IDFKIT_CACHE_DIR`](../concepts/environment-variables.md#idfkit_cache_dir)
to a path you control, in both the warming environment and the isolated one.
Without it, idfkit uses a platform location that a build container and its
runtime almost never share.

```bash
export IDFKIT_CACHE_DIR=/opt/idfkit-cache
```

An explicit `IDFKIT_CACHE_DIR` is never silently relocated. If the path turns
out to be unwritable, the write fails and names the path you chose, rather than
quietly moving your downloads somewhere the later run will not look.

## 2. Pre-download the stations the run will need

```python
--8<-- "docs/snippets/how-to/warm-the-weather-cache/warm_up.py:example"
```

`only={".epw", ".ddy"}` skips extracting the STAT, CLM, WEA, PVSYST, and RAIN
members of the upstream bundle, none of which a simulation reads. It saves
disk, not bandwidth: the archive is downloaded whole either way and kept, so
the transfer is identical. For Chicago O'Hare the full extraction occupies
2.9 MB against 2.1 MB for the EPW and DDY alone, the 384 KB archive included in
both. Worth having across a few hundred stations, not worth contorting a build
for.

Fail the build on a station that does not resolve. A warm-up that quietly skips
a miss produces a cache that looks complete and fails hours later, in the one
environment that cannot fix it.

## 3. Turn off the freshness nudge in the isolated run

This is the step that is easy to miss, and warming the cache alone does not
cover it.

`StationIndex.load()` fires a throttled freshness check: at most once every 24
hours it sends a HEAD request for each of the 10 upstream index files, warns if
the loaded index is behind, and records the check under the cache directory.
Offline, every one of those requests fails and is swallowed, so the call still
returns a complete index and nothing breaks. What it costs is time. Each
request carries a 30 second timeout, so on a network that drops packets rather
than refusing them, the first `StationIndex.load()` of the day can block for up
to five minutes before returning a result it already had on disk.

```bash
export IDFKIT_NO_WEATHER_UPDATE_CHECK=1
```

Measured with every socket call failing the way an offline machine fails, so
the counts are attempts made rather than requests that happened to succeed:

| Configuration | `StationIndex.load()` network attempts |
|---------------|---------------------------------------|
| Cold writable cache, nudge on | 10 |
| Cold writable cache, `IDFKIT_NO_WEATHER_UPDATE_CHECK=1` | 0 |
| Warm cache checked within the last 24 hours | 0 |
| Read-only cache | 0 |

The nudge is a convenience for interactive use, where a stale index is worth a
warning. In an environment that cannot act on the warning, it buys nothing.

## 4. Mount the cache read-only, if you like

A warm cache mounted read-only is a supported configuration and needs no extra
setting. Reads do not require write permission, and the freshness nudge stops
on its own: it cannot write its throttle timestamp, so it gives up before
reaching for the network. That is why the read-only row above reads 0 without
`IDFKIT_NO_WEATHER_UPDATE_CHECK` being set at all.

Set `IDFKIT_NO_WEATHER_UPDATE_CHECK` anyway. It makes the intent explicit
rather than relying on a permission bit to suppress a network call.

## 5. Run offline

```python
--8<-- "docs/snippets/how-to/warm-the-weather-cache/offline_run.py:example"
```

## A worked example: warming an image at build time

The whole procedure in one container. The build has a network, the run does not.

```dockerfile
FROM python:3.12-slim

ENV IDFKIT_CACHE_DIR=/opt/idfkit-cache \
    IDFKIT_NO_WEATHER_UPDATE_CHECK=1

RUN pip install --no-cache-dir idfkit

# Warm the cache while the build still has a network.
COPY warm_up.py /tmp/
RUN python /tmp/warm_up.py

COPY run.py /tmp/
CMD ["python", "/tmp/run.py"]
```

```bash
docker build -f Dockerfile.warmup -t idfkit-warmup .
docker run --rm --network none idfkit-warmup
```

Set both variables in the image rather than at `docker run` time. They have to
apply to the build stage that warms the cache and to the run stage that reads
it, and a cache warmed at one path and read from another is the single most
common way this goes wrong.

The cache does not need to be writable at run time. Running the same image as a
user who cannot write to `/opt/idfkit-cache` works unchanged, which is what
makes a read-only mount or a non-root runtime a supported configuration rather
than a thing to work around.

## Verify the warm-up before you rely on it

Run this while the network is still available. It exercises the same calls the
isolated run will make, and a warm cache turns every `download()` into a disk
read.

```python
--8<-- "docs/snippets/how-to/warm-the-weather-cache/readiness_check.py:example"
```

To prove the offline claim rather than assume it, block the network inside the
process instead of switching off an interface. Raising from the socket layer
shows that no request was even attempted, which is a stronger result than a run
that merely happened to succeed:

```python
import socket


def refuse(*args: object, **kwargs: object) -> object:
    raise socket.gaierror(8, "offline")


socket.socket.connect = refuse  # type: ignore[method-assign]
socket.create_connection = refuse  # type: ignore[assignment]
socket.getaddrinfo = refuse  # type: ignore[assignment]

# Everything below this line must still work.
```

## What still needs the network

These are the only calls that retrieve, and they fail loudly offline rather
than returning something empty:

| Call | Offline behaviour |
|------|-------------------|
| `WeatherDownloader.download()` for a station not in the cache | raises `RuntimeError` naming the URL it could not reach |
| `StationIndex.refresh()` | raises `RuntimeError` naming the index file it could not fetch |
| `StationIndex.check_for_updates()` | returns `False`, by design, because a freshness check that cannot reach upstream has learned nothing |
| `geocode()` and `detect_location()` | raise `GeocodingError` |

Geocoding is worth calling out separately. `geocode()` has no cache, so an
isolated run has to resolve its addresses to coordinates before it loses the
network, or work from coordinates directly.

!!! warning "Do not warm `detect_location()`"
    `detect_location()` does keep a disk cache, `ipgeo.json`, alongside the
    weather files, with a one hour default expiry. Warming it is worse than
    leaving it cold: it records the **build machine's** approximate location
    from its public IP, so a warmed entry would hand the isolated run the
    coordinates of your CI runner and be believed. If a run needs to know where
    it is, pass the coordinates in.

## See also

- [Environment variables](../concepts/environment-variables.md) for the full
  contract of `IDFKIT_CACHE_DIR` and `IDFKIT_NO_WEATHER_UPDATE_CHECK`
- [How to download weather files](../weather/downloads.md) for the downloader's
  full API
- [Weather data pipeline](../concepts/weather-pipeline.md) for why the index
  ships and the files do not
