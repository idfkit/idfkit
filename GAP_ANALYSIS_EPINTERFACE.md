# Gap Analysis: idfkit vs eppy/archetypal for epinterface

This document evaluates what is missing in **idfkit** to fully replace **eppy** and **archetypal** as used by the [epinterface](https://github.com/szvsw/epinterface) project.

## Executive Summary

epinterface uses archetypal (which wraps eppy and geomeppy) as its sole EnergyPlus interface layer. The dependency is deep: `archetypal.idfclass.IDF` is imported in 15+ files, `archetypal.schedule.Schedule` in 6+ files, `archetypal.idfclass.sql.Sql` in 4 files, and `geomeppy` geometry primitives in 1 file.

idfkit already covers **most** of what epinterface needs. The core IDF manipulation, simulation execution, SQL result parsing, geometry operations, and eppy-compatible API are all present. However, there are **6 gaps** ranging from minor API parity issues to significant missing features (primarily around high-level schedule creation and shoebox geometry generation).

---

## Capability Matrix

| Capability | epinterface needs | idfkit status | Gap? |
|---|---|---|---|
| Load/create IDF files | `IDF(filepath)`, `IDF(prep_outputs=True)` | `load_idf()`, `new_document()` | No |
| Create objects | `idf.newidfobject(key, **fields)` | `doc.newidfobject()` (compat) / `doc.add()` | No |
| Access objects by type | `idf.idfobjects["ZONE"]` | `doc.idfobjects["ZONE"]` (compat) / `doc["Zone"]` | No |
| Get object by type+name | `idf.getobject(type, name)` | `doc.getobject(type, name)` (compat) | No |
| Remove single object | `idf.removeidfobject(obj)` | `doc.removeidfobject(obj)` | No |
| Remove all objects of type | `idf.removeallidfobjects(key)` | Not implemented | **YES** |
| Add existing object | `idf.addidfobject(obj)` | `doc.addidfobject(obj)` (compat) | No |
| Add multiple objects | `idf.addidfobjects(objs)` | `doc.addidfobjects(objs)` (compat) | No |
| Copy object | `idf.copyidfobject(obj)` | `doc.copyidfobject(obj)` (compat) | No |
| Object `.to_dict()` | `obj.to_dict()` | `obj.to_dict()` | No |
| Object field access | `obj.Name`, `obj.Zone_Name` | `obj.name`, `obj.zone_name` | Naming convention differs (see below) |
| Save IDF | `idf.saveas(filepath)` | `doc.saveas(filepath)` (compat) | No |
| Run simulation | `idf.simulate()` | `doc.run()` (compat) / `simulate()` | No |
| SQL time series | `Sql(path).timeseries_by_name(...)` | `SQLResult(path).get_timeseries(...)` | API differs (see below) |
| SQL tabular data | `Sql(path).tabular_data_by_name(...)` | `SQLResult(path).get_tabular_data(...)` | API differs (see below) |
| Constant schedule creation | `Schedule.constant_schedule(Name=..., value=...)` | Not implemented | **YES** |
| Schedule from 8760 values | `Schedule.from_values(Name=..., Values=..., Type=...)` | Not implemented | **YES** |
| Schedule decompose to Year/Week/Day | `schedule.to_year_week_day()` | Not implemented | **YES** |
| Schedule write to IDF | `year_schedule.to_epbunch(idf)` | Not implemented | **YES** |
| ScheduleTypeLimits creation | `ScheduleTypeLimits(Name=..., ...)` | Manual `doc.add("ScheduleTypeLimits", ...)` | Partial (no high-level API) |
| Add building block | `idf.add_block(name, coords, height, stories)` | Not implemented | **YES** |
| Add shading block | `idf.add_shading_block(name, coords, height)` | Not implemented | **YES** |
| Scale geometry | `idf.scale(factor, anchor, axes)` | Not implemented | **YES** |
| Bounding box | `idf.bounding_box()` | Not implemented | **YES** |
| Intersect & match surfaces | `idf.intersect_match()` | `intersect_match(doc)` | **Partial** (no surface splitting) |
| Set WWR | `idf.set_wwr(wwr, construction)` | `set_wwr(doc, wwr, ...)` | No |
| Translate building | `idf.translate(vector)` | `translate_building(doc, offset)` | No |
| Rotate building | `idf.rotate(angle)` | `rotate_building(doc, angle)` | No |
| Set default constructions | `idf.set_default_constructions()` | Not implemented | **YES** |
| Surface `.coords` access | `srf.coords` (returns coordinate tuples) | `get_surface_coords(srf)` | Function vs property |
| Surface `.setcoords()` | `srf.setcoords(coords)` | `set_surface_coords(srf, poly)` | Function vs method |
| Polygon3D (geomeppy) | `from geomeppy.geom.polygons import Polygon3D` | `from idfkit.geometry import Polygon3D` | No |
| Vector2D (geomeppy) | `from geomeppy.geom.vectors import Vector2D` | Not implemented (Vector3D only) | **Minor** |
| DDY file parsing | `IDF(ddy_path, as_version="9.2.0")` | `load_idf(ddy_path)` via DesignDayManager | No |
| DDY injection | Extract design days from DDY, inject to model | `DesignDayManager`, `apply_ashrae_sizing()` | No |
| EPW parsing | `from ladybug.epw import EPW` | Not in scope (ladybug separate dep) | N/A |

---

## Detailed Gap Analysis

### Gap 1: `removeallidfobjects(key)` [LOW effort]

**What epinterface does:**
```python
idf.removeallidfobjects("SizingPeriod:DesignDay")
```
Used in `ddy_injector_bayes.py` to clear all existing design days before injecting new ones.

**idfkit status:** The compat layer has `removeidfobject()` (single) and `removeidfobjects()` (list), but no `removeallidfobjects(type)` that clears an entire collection by type.

**Recommendation:** Add `removeallidfobjects(obj_type: str)` to `EppyDocumentMixin`. Implementation is trivial:
```python
def removeallidfobjects(self, obj_type: str) -> None:
    for obj in list(self[obj_type]):
        self.removeidfobject(obj)
```

---

### Gap 2: High-Level Schedule Creation API [HIGH effort]

**What epinterface does:**
```python
from archetypal.schedule import Schedule, ScheduleTypeLimits

# Create a constant schedule
sched = Schedule.constant_schedule(Name="Always On", value=1.0)

# Create from 8760 hourly values
sched = Schedule.from_values(Name="Occupancy", Values=hourly_array, Type="Fractional")

# Decompose into Year/Week/Day hierarchy
year_sched, week_scheds, day_scheds = sched.to_year_week_day()

# Write all components to IDF
year_sched.to_epbunch(idf)

# Access properties
sched.MonthlyAverageValues
sched.bounds  # (min, max)
```

This is the **most heavily used archetypal feature** in epinterface (6+ files). The lifecycle is:
1. Create a `Schedule` object from constant value or 8760 hourly array
2. Decompose it into the EnergyPlus `Schedule:Year` / `Schedule:Week:Daily` / `Schedule:Day:Hourly` hierarchy
3. Write all resulting IDF objects into the model

**idfkit status:** idfkit has a schedule **evaluation** engine (read schedules from existing IDF and compute values at given times), but no schedule **creation** API. There is no way to:
- Create a schedule from an array of 8760 values
- Automatically decompose a schedule into Year/Week/Day IDF objects
- Create constant schedules as first-class objects

**Recommendation:** Implement a `ScheduleBuilder` module in `idfkit.schedules` with:
- `create_constant_schedule(doc, name, value, type_limits=None) -> IDFObject`
- `create_schedule_from_values(doc, name, values, type_limits=None) -> IDFObject` (8760 array -> Year/Week/Day decomposition)
- `create_schedule_type_limits(doc, name, lower=0, upper=1, numeric_type="Continuous")` convenience

This is the largest gap because the decomposition algorithm (grouping 8760 hourly values into unique day profiles, then week profiles, then annual periods) is non-trivial.

---

### Gap 3: Shoebox Geometry Generation [MEDIUM effort]

**What epinterface does:**
```python
idf.add_block(name="block1", coordinates=[(x1,y1), (x2,y2), ...], height=3.0, num_stories=2)
idf.add_shading_block(name="neighbor", coordinates=[(x1,y1), ...], height=15.0)
idf.set_default_constructions()
idf.bounding_box()
idf.scale(factor=2.0, anchor=Vector2D(0, 0))
```

These geomeppy methods are used in `epinterface/geometry.py` to construct shoebox building models:
- `add_block()` generates zones with complete surface geometry (walls, floor, ceiling) from a 2D footprint, height, and story count
- `add_shading_block()` generates `Shading:Site:Detailed` surfaces from a 2D footprint and height
- `set_default_constructions()` assigns placeholder constructions to all surfaces that lack one
- `bounding_box()` returns the 2D bounding polygon of the building
- `scale()` scales all geometry around an anchor point

**idfkit status:** idfkit has `translate_building()`, `rotate_building()`, `set_wwr()`, `intersect_match()`, and low-level coordinate manipulation (`get_surface_coords`, `set_surface_coords`). But it has **no** high-level block/shoebox generation.

**Recommendation:** Add a `idfkit.geometry.builders` module with:
- `add_block(doc, name, footprint, height, num_stories=1)` - Creates Zone + BuildingSurface:Detailed objects from 2D footprint
- `add_shading_block(doc, name, footprint, height)` - Creates Shading:Site:Detailed surfaces
- `set_default_constructions(doc)` - Assigns stub constructions
- `bounding_box(doc) -> Polygon3D` - Computes 2D bounding envelope
- `scale_building(doc, factor, anchor=None)` - Scales all geometry

---

### Gap 4: `intersect_match` Partial Intersection [LOW-MEDIUM effort]

**What epinterface does:**
```python
idf.intersect_match()  # Full geomeppy intersection including surface splitting
```
geomeppy's `intersect_match()` can **split** partially overlapping surfaces at their intersection boundary, creating new sub-surfaces. epinterface relies on this for multi-zone shoebox models where adjacent walls may not be perfectly aligned.

**idfkit status:** `intersect_match(doc)` exists and handles the common case of **full-overlap matching** (same-size surfaces on opposite sides of a shared wall). It explicitly notes that "partial intersection and surface splitting are **not** implemented."

**Impact:** For simple shoebox models where `add_block()` generates aligned surfaces, full-overlap matching is sufficient. But if epinterface ever produces non-aligned zone boundaries, the partial split would be needed.

**Recommendation:** For the initial migration this is likely acceptable as-is, since `add_block()` would generate aligned surfaces. Document the limitation and add surface splitting as a future enhancement.

---

### Gap 5: SQL Result API Differences [LOW effort]

**What epinterface does:**
```python
from archetypal.idfclass.sql import Sql

sql = Sql(sql_file_path)
ts = sql.timeseries_by_name(
    KeyValue="",
    Name="Zone Ideal Loads Supply Air Total Heating Energy",
    EnvType=3,  # annual run period
    Frequency="Hourly"
)
tab = sql.tabular_data_by_name(
    ReportName="AnnualBuildingUtilityPerformanceSummary",
    ReportForString="Entire Facility",
    TableName="End Uses",
    ColumnName="Electricity",
    RowName="Total End Uses",
    Units="GJ"
)
```

**idfkit status:** `SQLResult` provides equivalent functionality but with different method signatures:
- `get_timeseries(variable_name, key_value, frequency, environment)` - Equivalent but uses `environment="annual"|"sizing"` instead of integer env types
- `get_tabular_data(report_name, table_name)` - Returns all matching rows; no per-column/per-row filtering in the query (must be filtered client-side)

**Differences:**
1. `timeseries_by_name()` uses `EnvType=3` integer; idfkit uses `environment="annual"` string
2. `tabular_data_by_name()` filters by 6 dimensions in archetypal; idfkit only filters by `report_name` and `table_name`, requiring client-side filtering for `row_name`, `column_name`, `report_for`, and `units`
3. Return types differ: archetypal returns pandas Series/DataFrames; idfkit returns `TimeSeriesResult` / `list[TabularRow]` (with `.to_dataframe()` available)

**Recommendation:** Two options:
1. **Minimal:** Add optional `row_name`, `column_name`, `report_for` filter parameters to `get_tabular_data()`. Add `timeseries_by_name()` and `tabular_data_by_name()` compatibility aliases.
2. **Full compat:** Add a thin `Sql` compatibility wrapper that translates archetypal's API to idfkit's `SQLResult`.

---

### Gap 6: `IDF()` Constructor Options [LOW effort]

**What epinterface does:**
```python
idf = IDF(
    filepath,
    epw="weather.epw",
    output_directory="./output",
    prep_outputs=True,      # auto-add Output:SQLite etc.
    as_version="9.2.0",     # version override
    file_version="9.2.0",   # explicit file version
)
```

**idfkit status:**
- `load_idf(path, version=None)` covers `filepath` + `as_version`/`file_version`
- `epw` and `output_directory` are simulation-time options in `simulate()`
- `prep_outputs=True` (auto-injecting Output:SQLite, Output:Table:SummaryReports, etc.) has no equivalent

**Recommendation:** Add a `prep_outputs(doc)` utility that adds standard output objects if not present:
- `Output:SQLite` with `SimpleAndTabular`
- `Output:Table:SummaryReports` with common reports
- `Output:VariableDictionary` with `Regular`

---

## Non-Gaps (Already Covered)

These capabilities are fully or adequately covered by idfkit:

| Feature | Notes |
|---|---|
| **IDF parsing/writing** | Full support for both IDF and epJSON |
| **Object CRUD** | `add()`, `removeidfobject()`, `copyidfobject()`, bracket access |
| **Eppy compat layer** | `_compat.py` covers `newidfobject`, `getobject`, `idfobjects[]`, `saveas`, `run`, etc. |
| **Reference graph** | Auto-tracking of cross-object references, rename cascading |
| **WWR setting** | `set_wwr()` with orientation filtering |
| **Building translate/rotate** | `translate_building()`, `rotate_building()` |
| **Surface coordinate access** | `get_surface_coords()`, `set_surface_coords()` |
| **Simulation execution** | `simulate()` with full options, async, batch |
| **SQL result parsing** | `SQLResult` with time series, tabular, variable listing |
| **DDY parsing/injection** | `DesignDayManager`, `apply_ashrae_sizing()` |
| **Weather station search** | `StationIndex` with 55k+ stations |
| **Weather file download** | `WeatherDownloader` with caching |
| **Schedule evaluation** | All 8 schedule types, hourly values, pandas Series |
| **Thermal properties** | R-value, U-value, SHGC calculations |
| **Geometry primitives** | `Vector3D`, `Polygon3D` with full operations |
| **3D visualization** | SVG construction diagrams, building model views |
| **Validation** | Schema-driven validation with error/warning levels |

---

## Migration Effort Estimate

### Priority Order (for epinterface migration)

1. **`removeallidfobjects`** - Trivial addition to compat layer (a few lines)
2. **`prep_outputs` utility** - Small utility function
3. **SQL compat aliases** - Thin wrapper or additional filter params
4. **High-level schedule creation** - The most impactful gap; requires implementing 8760-to-Year/Week/Day decomposition algorithm
5. **Shoebox geometry generation** - `add_block()`, `add_shading_block()`, `scale_building()`, `bounding_box()`, `set_default_constructions()`
6. **Partial surface intersection** - Enhancement to existing `intersect_match()`

### Field Name Convention Note

epinterface accesses EnergyPlus fields using the original IDF names (`obj.Name`, `obj.Zone_Name`, `obj.Construction_Name`), while idfkit uses Python-style names (`obj.name`, `obj.zone_name`, `obj.construction_name`). This is not a gap in idfkit itself but means epinterface code would need refactoring for field access. The `EppyObjectMixin` in `_compat_object.py` may already handle some of this mapping.

### Summary Table

| Gap | Effort | Impact | Priority |
|---|---|---|---|
| `removeallidfobjects()` | Trivial | Medium | P0 |
| Schedule creation API | High | Critical | P0 |
| `prep_outputs()` utility | Low | Medium | P1 |
| SQL compat layer | Low | Medium | P1 |
| Shoebox geometry builders | Medium | High | P1 |
| `set_default_constructions()` | Low | Medium | P2 |
| `bounding_box()` | Low | Low | P2 |
| `scale_building()` | Low | Medium | P2 |
| Partial surface intersection | Medium | Low | P3 |
| `Vector2D` class | Trivial | Low | P3 |
