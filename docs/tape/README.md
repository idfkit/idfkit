# CLI Animations

Terminal GIF animations created with [VHS](https://github.com/charmbracelet/vhs), a tool that generates GIFs from `.tape` script files.

## Prerequisites

```bash
brew install vhs
```

The `migrate` tape additionally requires an EnergyPlus installation (any version ≥ 22.1.0) discoverable via `ENERGYPLUS_DIR`, `PATH`, or the platform default install location.

## Generating GIFs

Re-record every tape:

```bash
./tape/record.sh
```

Each tape runs in an isolated temp directory. `fixtures/` is copied into that tmpdir first so the tapes have the small IDF and Python files they reference. Generated GIFs are copied back to `tape/`.

Record a single tape manually:

```bash
vhs tape/idfkit-tmy-search.tape
```

## Tape files

| Tape | GIF | Shows |
|------|-----|-------|
| `idfkit-tmy-search.tape` | `idfkit_tmy_search.gif` | `idfkit tmy "chicago ohare"` — text search with TTY colour table |
| `idfkit-tmy-wmo-download.tape` | `idfkit_tmy_wmo_download.gif` | `idfkit tmy --wmo 725300 --variant 2009-2023 --first --download ./weather/` — filter + download |
| `idfkit-tmy-json.tape` | `idfkit_tmy_json.gif` | `idfkit tmy "london" --first --json \| jq ...` — machine-readable output piped to jq |
| `idfkit-check.tape` | `idfkit_check.gif` | `idfkit check example.py --from 24.2 --to 25.1` — static cross-version lint |
| `idfkit-migrate.tape` | `idfkit_migrate.gif` | `idfkit migrate old.idf --to 25.2` — forward-migrate an IDF |

## Fixtures

`fixtures/` contains the inputs the tapes reference:

- `example.py` — a short Python snippet using the renamed `Coil:Heating:Gas` → trips `C001` for `idfkit check`
- `old.idf` — a minimal v22.1 IDF for `idfkit migrate` to upgrade
