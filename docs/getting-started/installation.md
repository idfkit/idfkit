# How to install idfkit

idfkit is one library under one name in two ecosystems: `idfkit` on PyPI and
`idfkit` on npm. This guide installs it, adds the optional pieces, and points
EnergyPlus at your simulations.

The two ecosystems package the same surface differently, and the difference
shows up twice below. Python gates optional features behind extras, which are
dependencies rather than files, so weather support and its station index arrive
whether or not you asked for them. JavaScript gates them behind separate
packages, so weather is a second install and stays off disk until you make it.

!!! warning "The npm side of this page describes the intended install"
    `pip install idfkit` works today. The npm commands do not, and not because
    npm is empty: `@idfkit/core`, `@idfkit/schemas` and `@idfkit/weather` are
    published at 0.1.0. That release predates the renames these pages document,
    so installing it gets you an API this site does not describe. It still
    exports `IDFDocument` rather than `IdfDocument`, and `IdfDocument.collection()`
    is public there and withdrawn here. The shared `idfkit` name is not published
    at all. Read the TypeScript tabs as the destination, and do not pin to 0.1.0
    expecting the names on these pages.

## Install the library

=== "Python"

    ```bash
    pip install idfkit
    # or, with uv
    uv add idfkit
    ```

=== "TypeScript"

    ```bash
    # Not yet published. This is the intended install.
    npm install idfkit
    ```

That gives you, in both languages:

- Loading and writing IDF and epJSON files
- O(1) object lookups and reference tracking
- Schema validation for all 17 supported EnergyPlus versions
- Object and field introspection

Beyond that the two diverge, because they run in different places. Python adds
3D geometry, EnergyPlus simulation, weather, and the `idfkit` command-line tool,
with subcommands [`check`](../concepts/version-compatibility.md) (lint),
[`migrate`](../simulation/migrating-versions.md) (upgrade IDFs), and
[`tmy`](../cli/tmy.md) (weather data). TypeScript adds nothing to the base
install and ships no CLI; it parses, edits, and writes, in Node, a browser, a
worker, or an edge runtime.

On npm the name `idfkit` is a facade over three packages, each of which stays
published under its own name: `@idfkit/core` behind `idfkit` and `idfkit/node`,
`@idfkit/schemas` behind `idfkit/schemas`, and `@idfkit/weather` behind
`idfkit/weather`. The first two are ordinary dependencies and come with the
install. The third does not.

## Weather is a separate install in JavaScript

`pip install idfkit` installs weather support and the 1.7 MB station index
unconditionally. `npm install idfkit` installs neither. `@idfkit/weather` is
declared as an optional peer dependency of `idfkit`, so npm leaves it out by
default and nobody who never asks for weather pays for the index.

=== "Python"

    ```bash
    # Nothing to do. Weather ships with idfkit.
    pip install idfkit
    ```

=== "TypeScript"

    ```bash
    # Not yet published. This is the intended install.
    npm install idfkit @idfkit/weather
    ```

Import `idfkit/weather` without installing `@idfkit/weather` and the failure
names the package to install rather than reporting an unresolved module. A
project that never touches that subpath is unaffected, and a package of your own
that depends on `idfkit` and needs weather should declare `@idfkit/weather`
itself.

See [How to download weather files](../weather/downloads.md) for what the two
weather surfaces do with what they return.

## Optional Python extras

Python's optional features are extras on the one package.

### DataFrame support

Convert simulation results to pandas DataFrames:

```bash
pip install idfkit[dataframes]
# or
uv add idfkit[dataframes]
```

### Plotting

Visualize simulation results with matplotlib or plotly:

```bash
pip install idfkit[plot]     # Matplotlib backend
pip install idfkit[plotly]   # Plotly backend
```

### Progress bars

Show tqdm progress bars during batch simulations:

```bash
pip install idfkit[progress]
```

### Cloud storage (S3)

Store simulation results in Amazon S3:

```bash
pip install idfkit[s3]
```

### Everything at once

```bash
pip install idfkit[all]
```

## Generated types in TypeScript

The base install is typed, but object types and field names are only as specific
as the schema you tell it about. Add the generated type map for the EnergyPlus
version you work in to get autocompletion and compile-time checking on both:

```bash
# Not yet published. This is the intended install.
npm install --save-dev @idfkit/types-v26-1
```

Each type map declares `@idfkit/core` as a peer dependency and carries no code,
so it costs nothing at runtime. There is no Python counterpart: Python resolves
field names against the schema at runtime instead.

## EnergyPlus Installation

Running simulations needs EnergyPlus itself, installed on the machine that runs
them. This applies to Python only; the TypeScript packages do not simulate.

### Automatic discovery

idfkit discovers EnergyPlus using this priority:

1. **Explicit path** passed to `find_energyplus(path=...)`
2. **Environment variable** `ENERGYPLUS_DIR`
3. **System PATH** (looks for the `energyplus` executable)
4. **`/opt/eplus`** (standard install location in Claude Code web sessions)
5. **Platform defaults**:
    - macOS: `/Applications/EnergyPlus-*/`
    - Linux: `/usr/local/EnergyPlus-*/`
    - Windows: `C:\EnergyPlusV*/`

### Download EnergyPlus

Download from the official site: [EnergyPlus
Downloads](https://energyplus.net/downloads).

### Verify the install

```python
--8<-- "docs/snippets/getting-started/installation/verify_installation.py:example"
```

## Requirements

| | Python | TypeScript |
|---|---|---|
| Runtime | Python 3.10 or later | Node 20 or later, or any modern browser |
| EnergyPlus | 8.9 or later, for simulation | not used |

## Install from source to contribute

=== "Python"

    ```bash
    git clone https://github.com/idfkit/idfkit.git
    cd idfkit
    uv sync
    make test    # run the test suite
    make check   # run all quality checks
    ```

=== "TypeScript"

    ```bash
    git clone https://github.com/idfkit/idfkit-js.git
    cd idfkit-js
    npm install
    npm test
    ```

## Next steps

- [Build your first model](../tutorials/first-model.md), from an empty document
  to a running simulation
- [Common tasks](quick-start.md), quick recipes for everyday operations
- [Core Tutorial](core-tutorial.ipynb), the in-depth interactive walkthrough
- [How to parse in the browser](../how-to/parse-in-the-browser.md), if
  TypeScript is where you are headed
