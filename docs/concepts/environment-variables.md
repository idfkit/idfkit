# Environment Variables

idfkit reads a small number of environment variables to control EnergyPlus
discovery, cache locations, and a few opt-out flags. This page lists every
variable the package consults, where it is read, and the default behaviour
when the variable is not set.

## idfkit-Specific Variables

### `ENERGYPLUS_DIR`

Path to an EnergyPlus installation directory. Used by
[`find_energyplus()`](../api/simulation/runner.md) and the simulation runner
to locate the `energyplus` executable.

- **Read in:** `idfkit.simulation.config`
- **Default:** unset — discovery falls back to (in order) the `path` argument
  passed to `find_energyplus()`, the system `PATH`, then platform-specific
  default install locations.
- **Example:**

    ```bash
    export ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0
    ```

See [Installation › EnergyPlus Installation](../getting-started/installation.md#energyplus-installation)
for the full discovery order.

### `IDFKIT_NO_WEATHER_UPDATE_CHECK`

Opt-out flag that suppresses the once-per-day freshness nudge emitted when
`StationIndex.load()` notices the bundled station index may be stale.

- **Read in:** `idfkit.weather.index`
- **Default:** unset — the freshness nudge is enabled.
- **Activation:** set to any non-empty value to disable the check.
- **Example:**

    ```bash
    export IDFKIT_NO_WEATHER_UPDATE_CHECK=1
    ```

## Standard Platform Variables

idfkit honours standard OS-level variables when computing default cache
directories and discovering EnergyPlus on Windows. You generally do not need
to set these yourself — they exist on every supported platform — but
overriding them changes where idfkit reads and writes cached data.

### `XDG_CACHE_HOME` (Linux / POSIX)

Base directory for user cache data, per the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

- **Read in:** `idfkit.simulation.cache`, `idfkit.weather.index`
- **Default:** `~/.cache`
- **Effect:** Simulation cache lives at `$XDG_CACHE_HOME/idfkit/cache/simulations`;
  weather cache lives at `$XDG_CACHE_HOME/idfkit/weather`.

### `LOCALAPPDATA` (Windows)

Standard Windows variable pointing to the per-user local application data
directory.

- **Read in:** `idfkit.simulation.cache`, `idfkit.weather.index`
- **Default:** `%UserProfile%\AppData\Local`
- **Effect:** Simulation and weather caches live under
  `%LOCALAPPDATA%\idfkit\cache\`.

### `ProgramFiles`, `ProgramFiles(x86)`, `ProgramW6432` (Windows)

Standard Windows variables used to locate EnergyPlus installations under
`Program Files` directories during discovery.

- **Read in:** `idfkit.simulation.config`
- **Default:** if unset, those candidate locations are skipped.

### `SYSTEMDRIVE` (Windows)

Standard Windows variable identifying the drive that hosts the OS, used as a
fallback root when scanning for `EnergyPlusV*` installs at the drive root.

- **Read in:** `idfkit.simulation.config`
- **Default:** `C:`

## Quick Reference

| Variable                          | Purpose                                | Default                              |
|-----------------------------------|----------------------------------------|--------------------------------------|
| `ENERGYPLUS_DIR`                  | EnergyPlus install path                | unset (PATH + platform defaults)     |
| `IDFKIT_NO_WEATHER_UPDATE_CHECK`  | Disable weather index freshness nudge  | unset (check enabled)                |
| `XDG_CACHE_HOME`                  | Linux cache root                       | `~/.cache`                           |
| `LOCALAPPDATA`                    | Windows cache root                     | `%UserProfile%\AppData\Local`        |
| `ProgramFiles` / `ProgramFiles(x86)` / `ProgramW6432` | Windows EnergyPlus discovery | unset locations skipped     |
| `SYSTEMDRIVE`                     | Windows EnergyPlus discovery fallback  | `C:`                                 |

!!! note "macOS"
    On macOS, idfkit does not consult an environment variable for cache
    locations — caches live under `~/Library/Caches/idfkit/`.
