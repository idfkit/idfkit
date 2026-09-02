# Developing with idfkit

The pages in this section are written for **AI coding assistants** writing Python
against idfkit. They are the same files idfkit ships inside its wheel as the
`developing-with-idfkit` skill, published here so you can read them yourself.

Each page is self-contained and task-oriented: a "when to use" summary, a quick
start, a core API table, then the details. The code in them comes from
`docs/snippets/agent_references/`, which is linted with ruff and type-checked
with pyright under a strict configuration, so the examples run as written.

## Why a skill and not just docs

An assistant that guesses at an API invents methods that don't exist. The skill
solves that by resolving the idfkit **installed in your project** and loading the
reference set baked into that exact version. Pin idfkit 0.13 and you get 0.13's
guidance; upgrade and the guidance upgrades with it. No version drift, and no
copy-pasted API summary in your `CLAUDE.md` going stale behind your back.

The bundle lives in the pip package at
`idfkit/.agents/skills/developing-with-idfkit/`, not in the plugin repo. Install
idfkit once and every project gets the matching docs.

## Installing the skill

The skill ships in the
[idfkit plugin](https://github.com/idfkit/idfkit-plugin). It requires **idfkit
0.13 or newer** installed in the project you're working on.

=== "Claude Code"

    Installs the skill alongside the MCP server, workflow skills, agents, and
    hooks:

    ```
    /plugin marketplace add idfkit/idfkit-plugin
    /plugin install idfkit@idfkit
    ```

=== "Any agent"

    [`skills`](https://github.com/vercel-labs/skills) is a cross-agent
    installer covering Claude Code, Cursor, Copilot, Gemini CLI, and Codex:

    ```bash
    npx skills add idfkit/idfkit-plugin -s developing-with-idfkit -g
    ```

    `-s` picks this one skill; `-g` installs it for every project. Drop `-g` to
    install into the current project's `.<agent>/skills/` instead.

=== "Copilot / Cursor"

    ```bash
    gh skill install idfkit/idfkit-plugin developing-with-idfkit --scope user
    ```

    Add `--agent cursor` for Cursor.

=== "Gemini CLI"

    ```bash
    gemini skills install https://github.com/idfkit/idfkit-plugin.git
    ```

=== "Codex"

    Run `$skill-installer` inside a Codex session and point it at
    `idfkit/idfkit-plugin`. The repo ships a `.codex-plugin/` manifest.

Once installed, the skill locates your project's interpreter (respecting
`VIRTUAL_ENV`, a local `.venv`, conda, pipenv, poetry, pdm, or uv) and reads the
bundle from there. To reach the same files directly, without the plugin:

```python
from importlib.resources import files

skill = files("idfkit") / ".agents" / "skills" / "developing-with-idfkit"
print((skill / "SKILL.md").read_text())
```

## Reference index

| Task | Reference |
| ---- | --------- |
| Build, load, query, or modify a model | [Document & Objects](document-and-objects.md) |
| Parse `.idf` / `.epJSON` files | [Parsing IDF/epJSON](parsing-idf-epjson.md) |
| Write `.idf` / `.epJSON` files | [Writing Output](writing-output.md) |
| Validate a model against the schema | [Schema & Validation](schema-and-validation.md) |
| Find or update cross-references between objects | [Reference Tracking](reference-tracking.md) |
| Compute surface area, zone volume, azimuth, WWR | [Geometry & Surfaces](geometry-and-surfaces.md) |
| Build a building footprint and zone it | [Geometry Builders & Zoning](geometry-builders-and-zoning.md) |
| Stand up an HVAC system quickly with `HVACTemplate:*` | [HVAC Templates](hvac-templates.md) |
| Hand-author `AirLoopHVAC` / `PlantLoop` / `CondenserLoop` | [HVAC Loops](hvac-loops.md) |
| Run EnergyPlus simulations (sync, async, batch) | [Simulation Execution](simulation-execution.md) |
| Parse SQL / CSV / ESO / MTR / ERR simulation output | [Result Parsing](result-parsing.md) |
| Find a weather station, download EPW/DDY, inject design days | [Weather Data](weather-data.md) |
| Evaluate `Schedule:*` objects to time series | [Schedule Evaluation](schedule-evaluation.md) |
| Compute R-value, U-value, SHGC, gas mixture properties | [Thermal Properties](thermal-properties.md) |
| Render building geometry to 3D or SVG | [Visualization](visualization.md) |
| Migrate a model forward across EnergyPlus versions | [Version Migration](version-migration.md) |

## Conventions used in every reference

- **Imports come from `idfkit` directly** unless the symbol lives in a
  sub-package (`idfkit.simulation`, `idfkit.weather`, `idfkit.schedules`,
  `idfkit.thermal`, `idfkit.visualization`).
- **Python 3.10+** syntax: `tuple[int, int, int]`, and
  `from __future__ import annotations` in real code.
- **Strict mode is the default**: unknown field names raise `InvalidFieldError`.
  Pass `strict=False` only as a tolerant migration fallback.
- **The EnergyPlus version is part of every document**: `doc.version` is a
  `tuple[int, int, int]`, and the newest supported version is
  `idfkit.LATEST_VERSION`.

## A different surface: the MCP server

Writing Python that imports idfkit is what this skill is for. Driving a model
*through* an assistant, where the agent calls `load_model` and `run_simulation`
as tools rather than writing code, is the job of the separate
[idfkit-mcp](https://github.com/idfkit/idfkit-mcp) server, which the plugin also
installs.

## See also

- [Build your first model](../tutorials/first-model.md) for the human-facing
  walkthrough of the same API.
- [Reference](../reference/index.md) for the generated API documentation.
