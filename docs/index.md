---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# idfkit

<p class="hero-tagline">
A fast, modern EnergyPlus IDF/epJSON toolkit for Python — with O(1) lookups,
automatic reference tracking, and built-in simulation support.
</p>

<div class="badges" markdown>

[![Release](https://img.shields.io/github/v/release/samuelduchesne/idfkit)](https://img.shields.io/github/v/release/samuelduchesne/idfkit)
[![Build status](https://img.shields.io/github/actions/workflow/status/samuelduchesne/idfkit/main.yml?branch=main)](https://github.com/samuelduchesne/idfkit/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/samuelduchesne/idfkit)](https://img.shields.io/github/commit-activity/m/samuelduchesne/idfkit)
[![License](https://img.shields.io/github/license/samuelduchesne/idfkit)](https://img.shields.io/github/license/samuelduchesne/idfkit)

</div>

<div class="hero-buttons" markdown>

[Get Started :material-arrow-right:](getting-started/installation.md){ .md-button .md-button--primary }
[API Reference](api/document.md){ .md-button }

</div>

</div>

<div class="install-cmd" markdown>

```bash
pip install idfkit
```

</div>

<div class="feature-chips" markdown>

<span class="chip">:material-speedometer: O(1) lookups</span>
<span class="chip">:material-graph-outline: Reference tracking</span>
<span class="chip">:material-file-swap-outline: IDF + epJSON</span>
<span class="chip">:material-shield-check-outline: Schema validation</span>
<span class="chip">:material-cube-outline: 3-D geometry</span>
<span class="chip">:material-play-circle-outline: Simulation</span>
<span class="chip">:material-weather-cloudy: Weather data</span>
<span class="chip">:material-history: v8.9 -- v25.2</span>

</div>

---

## Quick Example

```python
--8<-- "docs/snippets/index/quick_example.py:example"
```

## Run Simulations

```python
--8<-- "docs/snippets/index/run_simulations.py:example"
```

## Find Weather Stations

```python
--8<-- "docs/snippets/index/find_weather_stations.py:example"
```

---

## Explore the Docs

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Get Started**

    ---

    Installation, quick start guide, and interactive tutorial.

    [:octicons-arrow-right-24: Get Started](getting-started/installation.md)

-   :material-school:{ .lg .middle } **Concepts**

    ---

    Architecture decisions, caching strategy, and design principles.

    [:octicons-arrow-right-24: Concepts](concepts/simulation-architecture.md)

-   :material-play-circle:{ .lg .middle } **Simulation**

    ---

    Run EnergyPlus, parse results, batch processing, and caching.

    [:octicons-arrow-right-24: Simulation Guide](simulation/index.md)

-   :material-weather-cloudy:{ .lg .middle } **Weather**

    ---

    Station search, downloads, design days, and geocoding.

    [:octicons-arrow-right-24: Weather Guide](weather/index.md)

-   :material-flask:{ .lg .middle } **Examples**

    ---

    Parametric studies, sizing workflows, and cloud simulations.

    [:octicons-arrow-right-24: Examples](examples/parametric-study.ipynb)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete API documentation for all modules.

    [:octicons-arrow-right-24: API Reference](api/document.md)

</div>

## More Resources

| Page | Description |
|------|-------------|
| [Core Tutorial](getting-started/core-tutorial.ipynb) | Interactive notebook covering basic, advanced, and expert usage |
| [Migrating from eppy](migration.md) | Side-by-side comparison of eppy and idfkit APIs |
| [Benchmarks](benchmarks.md) | Performance comparison against eppy and other tools |
| [Troubleshooting](troubleshooting/errors.md) | Common errors and solutions |
