# AGENTS.md

Instructions for AI agents and CI environments working with this repository.

## Installing EnergyPlus

EnergyPlus is required to run integration tests (`pytest -m integration`) and
to verify simulation tutorials. The project supports EnergyPlus versions 8.9.0
through 25.2.0.

### Download

EnergyPlus releases are hosted on GitHub under the **NatLabRockies** organization
(formerly NREL):

```
https://github.com/NatLabRockies/EnergyPlus/releases
```

Pick a version that matches a bundled schema (see `src/idfkit/schemas/` for
available versions). Version **24.2.0** is recommended for testing as it is
the latest in the 24.x series used by most tutorials.

### Linux (Ubuntu) Installation

```bash
# 1. Download the tar.gz for your Ubuntu version (22.04 or 24.04)
wget https://github.com/NatLabRockies/EnergyPlus/releases/download/v24.2.0/EnergyPlus-24.2.0-e7ecb2d53b-Linux-Ubuntu24.04-x86_64.tar.gz -O /tmp/energyplus.tar.gz

# 2. Extract to the standard installation directory
mkdir -p /usr/local/EnergyPlus-24-2-0
tar xzf /tmp/energyplus.tar.gz -C /usr/local/EnergyPlus-24-2-0 --strip-components=1

# 3. Verify
/usr/local/EnergyPlus-24-2-0/energyplus --version
```

For Ubuntu 22.04, replace `Ubuntu24.04` with `Ubuntu22.04` in the URL.

### Setting the Environment Variable

Set `ENERGYPLUS_DIR` so idfkit can discover the installation:

```bash
export ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0
```

### How idfkit Discovers EnergyPlus

idfkit searches for EnergyPlus in this order (see `src/idfkit/simulation/config.py`):

1. Explicit `path` argument to `find_energyplus(path=...)`
2. `ENERGYPLUS_DIR` environment variable
3. `energyplus` on system `PATH`
4. Platform default directories (newest version first):
   - Linux: `~/.local/EnergyPlus-*`, `~/EnergyPlus-*`, `/usr/local/EnergyPlus-*`, `/opt/EnergyPlus-*`
   - macOS: `~/Applications/EnergyPlus-*`, `/Applications/EnergyPlus-*`
   - Windows: `%ProgramFiles%/EnergyPlus-*`

### Verifying the Installation

```bash
uv run python -c "
from idfkit.simulation import find_energyplus
config = find_energyplus()
print(f'EnergyPlus {config.version[0]}.{config.version[1]}.{config.version[2]}')
print(f'Executable: {config.executable}')
"
```

### Running Integration Tests

```bash
# Run only integration tests (requires EnergyPlus)
ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0 uv run pytest -m integration -v

# Run all tests including integration
ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0 uv run pytest -v
```

### Version Compatibility

The `src/idfkit/versions.py` file lists all supported versions. Each version
has a bundled epJSON schema under `src/idfkit/schemas/V{major}-{minor}-{patch}/`.

| Version Range | Notes |
|---|---|
| 24.1.0 - 24.2.0 | Used in most tutorials and examples |
| 25.1.0 - 25.2.0 | Latest supported |
| 8.9.0 - 9.6.0 | Legacy versions |

### Bundled Files

An EnergyPlus installation includes:
- `energyplus` executable
- `Energy+.idd` (schema definition)
- `ExampleFiles/` directory with sample IDF models
- `WeatherData/` directory with sample EPW weather files

The example files are used by `tests/test_simulation_e2e.py` for integration testing.
