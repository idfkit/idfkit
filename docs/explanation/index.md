# Explanation

Explanation is the discussion of a topic: how idfkit works under the hood, why
it was designed the way it is, and how the pieces relate. These pages are worth
reading away from the keyboard, when you want to understand rather than to do.

They deliberately don't tell you which buttons to press — that's the job of the
[How-to guides](../how-to/index.md) — and they don't exhaustively list options,
which is the [Reference](../reference/index.md)'s job.

## Architecture & design

- [Simulation architecture](../concepts/simulation-architecture.md) — why
  simulations run in subprocesses on a copy of your model.
- [Weather data pipeline](../concepts/weather-pipeline.md) — how station search,
  downloads, and design days fit together.
- [Caching strategy](../concepts/caching.md) — what idfkit caches, and why.
- [Schedule evaluator design](../design/schedule-evaluator.md) — the design of
  the pure-Python schedule engine.

## Working effectively

- [Type-safe development](../concepts/type-safety.md) — how the generated type
  stubs give you autocomplete and catch typos.
- [Performance & benchmarks](../benchmarks.md) — how idfkit compares to eppy and
  other tools, and how those numbers were measured.
