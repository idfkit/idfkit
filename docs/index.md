---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# idfkit

<p class="hero-tagline">
EnergyPlus IDF and epJSON tooling for Python and TypeScript. One API surface,
one vocabulary, one site.
</p>

<div class="badges" markdown>

[![Release](https://img.shields.io/github/v/release/idfkit/idfkit)](https://img.shields.io/github/v/release/idfkit/idfkit)
[![Build status](https://img.shields.io/github/actions/workflow/status/idfkit/idfkit/main.yml?branch=main)](https://github.com/idfkit/idfkit/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/idfkit/idfkit)](https://img.shields.io/github/commit-activity/m/idfkit/idfkit)
[![License](https://img.shields.io/github/license/idfkit/idfkit)](https://img.shields.io/github/license/idfkit/idfkit)

</div>

<div class="hero-buttons" markdown>

[Build your first model :material-arrow-right:](tutorials/first-model.md){ .md-button .md-button--primary }
[How-to guides](how-to/index.md){ .md-button }
[Reference](reference/index.md){ .md-button }

</div>

</div>

<div class="feature-chips" markdown>

<span class="chip">:material-language-python: Python</span>
<span class="chip">:material-language-typescript: TypeScript</span>
<span class="chip">:material-history: v8.9 to v26.1, 17 versions</span>
<span class="chip">:material-speedometer: O(1) lookups</span>
<span class="chip">:material-graph-outline: Reference tracking</span>
<span class="chip">:material-file-swap-outline: IDF + epJSON</span>
<span class="chip">:material-shield-check-outline: Schema validation</span>
<span class="chip">:material-package-variant-closed: No third-party runtime dependencies</span>

</div>

!!! warning "Status"

    The Python library is released on PyPI: `pip install idfkit`. The
    TypeScript library is not yet published under the shared `idfkit` install
    name and its API is not stable, so the names on these pages can still
    change under it. Follow the TypeScript tabs by all means; pin nothing to
    them yet.

---

## Read a model, change it, write it back

=== "Python"

    ```python
    --8<-- "docs/snippets/index/quick_example.py:example"
    ```

=== "TypeScript"

    ```ts
    import { loadIdf, saveIdf } from '@idfkit/core/node';

    // Load an existing IDF file
    const doc = await loadIdf('in.idf');

    // Query objects with O(1) lookups
    const zone = doc.require('Zone', 'Office');
    console.log(zone.x_origin, zone.y_origin);

    // Modify a field
    zone.x_origin = 10;

    // See what references the zone
    for (const obj of doc.references.referencingObjects('Office')) {
      console.log(obj.typeName, obj.name);
    }

    // Write back to IDF (or epJSON)
    await saveIdf(doc, 'out.idf');
    ```

The two programs read as one lesson because they are. Names are decided once for
both languages and diverge only where the languages force it: a subscript
against a method, a synchronous call against an awaited one. [The naming
map](explanation/naming-map.md) records every pair and the reason for each
difference, and [What each language has](explanation/parity.md) records the
capabilities one of them does not carry yet.

---

## Explore the docs

<div class="grid cards" markdown>

-   :material-school:{ .lg .middle } **Tutorials**

    ---

    Learning-oriented lessons: build your first model from an empty document,
    step by step, in either language.

    [:octicons-arrow-right-24: Tutorials](tutorials/index.md)

-   :material-map-marker-path:{ .lg .middle } **How-to guides**

    ---

    Goal-oriented recipes: run simulations, work with weather data, parse in
    the browser, scale out.

    [:octicons-arrow-right-24: How-to guides](how-to/index.md)

-   :material-api:{ .lg .middle } **Reference**

    ---

    The complete API, CLI, and configuration, generated from the source.

    [:octicons-arrow-right-24: Reference](reference/index.md)

-   :material-lightbulb-on:{ .lg .middle } **Explanation**

    ---

    Understanding-oriented discussion: architecture, caching, and the design
    decisions behind both libraries.

    [:octicons-arrow-right-24: Explanation](explanation/index.md)

</div>

## More resources

| Page | Description |
|------|-------------|
| [What each language has](explanation/parity.md) | Capability by capability, what Python and TypeScript carry today |
| [The naming map](explanation/naming-map.md) | Every shared name, and why the two libraries spell a few of them differently |
| [How conformance is established](explanation/conformance.md) | How both libraries are proved against the IDF files EnergyPlus ships |
| [Core Tutorial](getting-started/core-tutorial.ipynb) | Interactive Python notebook covering basic, advanced, and expert usage |
| [How to migrate from eppy](migration.md) | Side-by-side comparison of eppy and idfkit APIs |
| [How to migrate models between EnergyPlus versions](simulation/migrating-versions.md) | Forward-migrate IDF models across EnergyPlus releases |
| [Benchmarks](benchmarks.md) | Performance comparison against eppy and other tools |
| [Troubleshooting](troubleshooting/errors.md) | Common errors and solutions |
