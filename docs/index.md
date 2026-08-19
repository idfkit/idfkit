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

[![Release](https://img.shields.io/github/v/release/idfkit/idfkit)](https://img.shields.io/github/v/release/idfkit/idfkit)
[![Build status](https://img.shields.io/github/actions/workflow/status/idfkit/idfkit/main.yml?branch=main)](https://github.com/idfkit/idfkit/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/idfkit/idfkit)](https://img.shields.io/github/commit-activity/m/idfkit/idfkit)
[![License](https://img.shields.io/github/license/idfkit/idfkit)](https://img.shields.io/github/license/idfkit/idfkit)

</div>

<div class="hero-buttons" markdown>

[Get Started :material-arrow-right:](tutorials/index.md){ .md-button .md-button--primary }
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
<span class="chip">:material-history: v8.9 -- v26.1</span>
<span class="chip">:material-update: Version migration</span>
<span class="chip">:material-console: CLI</span>

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

-   :material-school:{ .lg .middle } **Tutorials**

    ---

    Learning-oriented lessons: install idfkit and build your first model,
    step by step.

    [:octicons-arrow-right-24: Tutorials](tutorials/index.md)

-   :material-map-marker-path:{ .lg .middle } **How-to guides**

    ---

    Goal-oriented recipes: run simulations, work with weather data, scale
    out, and more.

    [:octicons-arrow-right-24: How-to guides](how-to/index.md)

-   :material-api:{ .lg .middle } **Reference**

    ---

    The complete API, CLI, and configuration — generated from the source.

    [:octicons-arrow-right-24: Reference](reference/index.md)

-   :material-lightbulb-on:{ .lg .middle } **Explanation**

    ---

    Understanding-oriented discussion: architecture, caching, and design
    decisions.

    [:octicons-arrow-right-24: Explanation](explanation/index.md)

</div>

## More Resources

| Page | Description |
|------|-------------|
| [Core Tutorial](getting-started/core-tutorial.ipynb) | Interactive notebook covering basic, advanced, and expert usage |
| [How to migrate from eppy](migration.md) | Side-by-side comparison of eppy and idfkit APIs |
| [How to migrate models between EnergyPlus versions](simulation/migrating-versions.md) | Forward-migrate IDF models across EnergyPlus releases |
| [Benchmarks](benchmarks.md) | Performance comparison against eppy and other tools |
| [Troubleshooting](troubleshooting/errors.md) | Common errors and solutions |
