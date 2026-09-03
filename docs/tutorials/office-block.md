# Simulate an office block

By the end of this you will have raised a two-storey office block from a
rectangle, split every floor into a core and four perimeter zones, wrapped it in
an insulated envelope, pulled Chicago's winter design weather off the network,
and asked a local EnergyPlus how much heating the block needs on the coldest day
of its year. The last step prints that number, and you will have got it out of
the results database yourself rather than read it here.

Allow about twenty minutes. Most of that is one weather download and a
simulation that finishes in under a second.

This tutorial is Python only. The four capabilities it is built on, generating
zoned blocks from a footprint, building and transforming geometry, applying
ASHRAE design days, and driving a locally installed EnergyPlus, are all recorded
on the parity ledger as present in Python and absent in JavaScript. The last of
them is absent permanently, because a library that targets the browser cannot
launch a native simulation engine:

{{ parity("local-simulation") }}

The other three are tracked gaps rather than boundaries:
[generating zoned blocks](../explanation/parity.md#zoning), [building and
transforming geometry](../explanation/parity.md#geometry-authoring), and
[design days and ASHRAE sizing
conditions](../explanation/parity.md#design-day-sizing). When they are ported,
this page grows TypeScript tabs; until then it says so here rather than leaving
you to discover it at the first import.

## What this needs

- **idfkit**, from `pip install idfkit`. [How to install
  idfkit](../getting-started/installation.md) covers the extras.
- **EnergyPlus**, 8.9 or newer, installed where idfkit can find it. Step 1 is
  the one that fails immediately if it cannot.
- **A network connection**, once. Step 4 downloads a weather file and its
  design-day companion, then caches both, so every later run is offline.

You do not need [Build your first model](first-model.md) first, though it is
shorter and it teaches the object model this page leans on. Keep the code in one
file, `office_block.py`, and re-run it after each step: every step builds on the
document the step before it left behind.

## Step 1: Pin the model to the EnergyPlus you have

A model carries the EnergyPlus version it was written for, and a simulation is
the moment that choice stops being cosmetic. So the run begins with a question
rather than an assumption: find the installed EnergyPlus, then pin the document
to it.

```python
--8<-- "docs/snippets/tutorials/office-block.py:pin"
```

```
26.1.0
26.1.0
```

Two lines, and they agree. `find_energyplus()` searches the usual installation
locations and returns a config carrying the version it found;
`find_closest_version()` maps that onto a schema idfkit actually ships. They
agree here because idfkit carries a schema for 26.1.0. If you run a release it
has no schema for, the second line is the nearest one it has, which is exactly
the fact you want in front of you before you build anything. It returns `None`
only when nothing is close at all, which is why `LATEST_VERSION` stands behind
it as a floor.

If there is no EnergyPlus on the machine, `find_energyplus()` raises
`EnergyPlusNotFoundError` here rather than at step 6, after you have built a
model you cannot run. That is the point of doing it first.

## Step 2: Raise the block from a footprint

You could place all sixty surfaces by hand. Instead, hand `create_block()` a
footprint, a floor-to-floor height, a storey count, and a zoning scheme, and let
it work out the geometry.

```python
--8<-- "docs/snippets/tutorials/office-block.py:block"
```

```
10 zones, 60 surfaces
Office Story 1 Perimeter_South
Office Story 1 Perimeter_East
Office Story 1 Perimeter_North
Office Story 1 Perimeter_West
Office Story 1 Core
Office Story 2 Perimeter_South
Office Story 2 Perimeter_East
Office Story 2 Perimeter_North
Office Story 2 Perimeter_West
Office Story 2 Core
```

Ten zones from four numbers. `ZoningScheme.CORE_PERIMETER` is the reason there
are five per storey rather than one: it insets the footprint by
`perimeter_depth` and cuts the ring into four zones, one per orientation, around
a core that touches no outside wall. That division is what lets step 7 tell you
which part of the building is losing the heat, and it is why a whole-floor zone
would have had nothing interesting to say.

The surfaces came with it, already named, already pointing at their zones,
already carrying vertices in the winding order `GlobalGeometryRules` declares.
Floors between storeys were matched to each other, so storey 1's ceiling and
storey 2's floor are one interface rather than two guesses.

## Step 3: Wrap it in an envelope

Those sixty surfaces name constructions that do not exist yet, and a
construction is a stack of material layers. Build two stacks, one opaque and one
transparent, then hand them out.

```python
--8<-- "docs/snippets/tutorials/office-block.py:envelope"
```

```
8 windows, 60 opaque surfaces
```

`Insulated Wall` is two layers deep: `outside_layer` is the concrete,
`layer_2` is the insulation behind it. Layers run outside to inside, and the
100 mm of insulation is what keeps step 7's answer plausible. Take it out and
the block asks for roughly four times the heat.

Order matters in the two calls that follow. `set_wwr()` punches windows into the
exterior walls at a 40 percent window-to-wall ratio and gives each one the
glazing construction, so those eight surfaces already have theirs.
`set_default_constructions()` then fills in every surface that still lacks one.
Run them the other way round and the fill step would have claimed the windows
first.

## Step 4: Bring in the design weather

A design day is a synthetic worst case: the conditions a system has to cope with
rather than the ones it usually sees. ASHRAE publishes them per station, and
EnergyPlus reads them out of a `.ddy` file that ships beside the weather file.
idfkit finds the station, downloads both, and injects the design day into the
model.

```python
--8<-- "docs/snippets/tutorials/office-block.py:weather"
```

```
Chicago-Meigs.Field-Northerly.Island (3.2 km away)
Chicago-Meigs.Field-Northerly Ann Htg 99.6% Condns DB
```

`nearest()` searched a station index that ships inside the package, so that part
needed no network. `download()` did, once: it fetched the weather file and its
design-day companion and cached them, so re-running this step is instant from
here on.

`heating="99.6%"` picks the winter day the station's design conditions are
stated for, meaning the outdoor temperature that Chicago stays above for 99.6
percent of the year. `apply_to_model()` added it as a `SizingPeriod:DesignDay`
and moved the model's `Site:Location` onto the station's coordinates, so the
building is now standing where the weather is.

Only one day came back. That is the file being honest: this station's `.ddy`
carries heating and dehumidification days but no dry-bulb cooling day, so a
summer sizing run would have nothing to size against. The rest of this tutorial
is a winter question, which is the one the data can answer.

## Step 5: Give every zone a thermostat

An unconditioned block just tracks the outdoor temperature, and asking how much
heat it needs is meaningless until something is trying to hold it at a
temperature. `HVACTemplate` objects are the short way to say that: one
thermostat shared by every zone, and one ideal loads system per zone that
delivers whatever the thermostat asks for.

```python
--8<-- "docs/snippets/tutorials/office-block.py:condition"
```

```
10
```

An ideal loads system is a measuring instrument rather than a machine. It has no
fan, no coil, and no capacity limit, so it always meets the setpoint and reports
exactly what that cost. That is what makes it the right thing for a sizing
question: the number in step 7 is the building's demand, uncontaminated by the
efficiency of any particular equipment you might buy to meet it.

The two `HVACTemplate` objects expand, at simulation time, into the dozens of
`ZoneHVAC`, node, and controller objects EnergyPlus actually solves. You will
see them in the run directory in step 6.

## Step 6: Run the design day

Ask for the one output variable this tutorial needs, check the model, and run
it.

```python
--8<-- "docs/snippets/tutorials/office-block.py:run"
```

```
0
True
```

Zero validation errors means every required field is present and every name the
model refers to resolves to an object that exists. Sixty surfaces naming
constructions, ten templates naming zones and a thermostat: nothing dangles.

`design_day=True` is what makes this fast. It tells EnergyPlus to simulate only
the sizing periods, so it runs the one winter day rather than 8760 hours, and it
finishes in a fraction of a second. Passing `energyplus=energyplus` reuses the
installation step 1 already located instead of searching again.

Look inside `office-sizing/` now. `model.idf` is what idfkit wrote,
`eplus.expidf` is that file after the templates expanded, `eplus.err` is
EnergyPlus's own account of the run, and `eplus.sql` is the results database the
next step reads. Reading `eplus.err` after a run is a habit worth forming: a
model can succeed and still be warning you about something.

## Step 7: Read the load out of the results

The results are an SQLite database, and idfkit hands you the series rather than
the schema. Pull one per zone, add them hour by hour, and take the worst hour.

```python
--8<-- "docs/snippets/tutorials/office-block.py:read"
```

```
10 zones, 24 hours
peak 30.6 kW at 00:00, 28.3 W/m2
Office Story 2 Perimeter_North         5.1 kW
Office Story 2 Perimeter_South         5.1 kW
Office Story 1 Perimeter_North         3.6 kW
Office Story 1 Perimeter_South         3.6 kW
Office Story 2 Perimeter_East          2.9 kW
Office Story 2 Perimeter_West          2.9 kW
Office Story 2 Core                    2.7 kW
Office Story 1 Perimeter_West          2.1 kW
Office Story 1 Perimeter_East          2.1 kW
Office Story 1 Core                    0.4 kW
```

There it is. The block you drew as a rectangle needs about **30.6 kW of heating**
at its worst hour, which is 28.3 watts for every square metre of floor.

Your numbers will differ a little. The weather file is periodically re-issued,
the design conditions travel with it, and EnergyPlus changes between releases,
so treat these as the shape of the answer rather than a fixture to match.

The ranking is the interesting part, and every line of it follows from the
geometry you chose:

- **North and south lead** because the footprint is 30 m by 18 m, so those
  facades are longer, carry more wall and more glazing, and lose more through
  both.
- **Storey 2 beats storey 1 everywhere** because it has the roof. The roof took
  the same construction as the walls, and it is exposed to a sky that is colder
  than the air.
- **Storey 2's core outranks four perimeter zones**, which looks wrong until you
  remember it has no exterior wall at all. Its entire load is that roof.
- **Storey 1's core asks for 0.4 kW**, close to nothing, because it is enclosed
  on all six sides by conditioned space and ground.
- **The peak lands at midnight**, not at dawn. This is a heating design day: no
  sun, no occupants, no equipment, no internal gains of any kind, and a constant
  outdoor temperature. Nothing about it varies by hour except the building's own
  thermal mass settling, so the load is nearly flat and the first hour wins.

## What the block told you

You went from four numbers to a heating load, through geometry you never placed
by hand, weather you never went looking for, and an HVAC system you described in
two objects. Along the way:

- `create_block()` with a `ZoningScheme` turned a footprint into zones and
  surfaces, and the zoning choice decided what step 7 could see.
- Constructions stack materials outside to inside, and `set_wwr()` before
  `set_default_constructions()` is the order that leaves nothing overwritten.
- `StationIndex` searches locally, `WeatherDownloader` fetches once and caches,
  and `DesignDayManager` turns a `.ddy` file into a sizing period plus a
  location.
- `HVACTemplate` objects expand into real HVAC at run time, and ideal loads is
  how you ask what a building needs rather than what a machine would do.
- `design_day=True` is the difference between a run you wait for and a run you
  iterate on.
- `result.sql` gives you the series, and the arithmetic that turns ten series
  into one answer is ordinary Python.

## Where to take it next

- Change one thing and re-run. Delete the insulation layer, or set `wwr=0.2`,
  and watch the number move. A sizing run is fast enough that this is a
  conversation rather than an errand.
- [How to run a simulation](../simulation/running.md) for the full-year run,
  the other `simulate()` options, and what else comes back in a result.
- [How to apply design days](../weather/design-days.md) for cooling days,
  ASHRAE 90.1 presets, and stations whose `.ddy` carries more than this one did.
- [How to query simulation SQL output](../simulation/sql-queries.md) for the
  tabular reports, meters, and environments this page never touched.
- [What each language has](../explanation/parity.md) before you plan work around
  anything on this page.
