# Tutorials

Tutorials are lessons. They take one controlled path from an empty file to a
working model, so you come away knowing how the pieces fit together rather than
knowing where a particular function lives. Follow them start to finish, in
order, without substitutions. You do not need to understand every line yet, only
to run the steps and watch what happens.

If you already know what you want to accomplish and just need the steps, the
[how-to guides](../how-to/index.md) are the shorter route.

## Start here

- [**Build your first model**](first-model.md) creates an EnergyPlus model from
  nothing, watches the reference graph rewrite itself when you rename a zone,
  writes the model to an IDF file, and reads it back. Python and TypeScript
  side by side, about fifteen minutes, no EnergyPlus installation needed.
- [**Simulate an office block**](office-block.md) raises a two-storey block from
  a rectangle, zones it, wraps it in an envelope, fetches design weather, and
  runs a local EnergyPlus to find out how much heating it needs on the coldest
  day. About twenty minutes, Python only, and it needs EnergyPlus installed.
- [**Core Tutorial**](../getting-started/core-tutorial.ipynb) works through the
  Python library end to end in a notebook, from basic use to the expert
  surface. Longer, and Python only.

New to the library? Start with [Build your first model](first-model.md), then
take [Simulate an office block](office-block.md) when you want to see a model
actually run. After that, the [how-to guides](../how-to/index.md) cover the
everyday operations, and [what each language has](../explanation/parity.md) says
which of them your language carries today.
