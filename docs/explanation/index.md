# Explanation

idfkit is two libraries, one in Python and one in TypeScript, over one pair of
EnergyPlus formats. Most of what either does is obvious once you know why it was
built that way, and surprising until then: why a field is called
`ceiling_height`, why a blank name is not the same as no name, why the
TypeScript parser refuses to read a file for you, and why a capability that
exists in one language may be deliberately absent from the other.

These pages answer the why. None of them is needed to get work done, and each
one is behind behaviour you will eventually meet. They are worth reading away
from the keyboard.

They deliberately do not tell you which buttons to press, which is the job of
the [how-to guides](../how-to/index.md), and they do not list options
exhaustively, which is the [reference](../reference/index.md)'s job.

## What the formats do to any library over them

Two pages here are about EnergyPlus, not about idfkit. They apply whichever
language you work in.

- [The hazards of a positional format](positional-format-hazards.md): the two
  rules that exist because breaking them corrupts a model in silence.
- [Why field names come from epJSON](epjson-field-names.md): why it is
  `zone_name` and not a converted form, in both languages.

## How the two libraries relate

- [About capability parity](parity.md): every public capability, its
  availability in each language, and whether an absence is temporary or
  permanent.
- [The naming map](naming-map.md): which name a concept carries in each
  language, and which surfaces are excluded from alignment.
- [How conformance is established](conformance.md): why the evidence that the
  two libraries agree lives outside both of them.

## How a model is represented

- [Type-safe development](../concepts/type-safety.md): how the generated stubs
  give you completion and catch typos, in Python.
- [Static types generated from the schema](generated-types.md): how a misspelled
  field name becomes a compile error, in TypeScript.
- [Why accessors and not a `Proxy`](accessors-not-proxies.md): why
  `zone.ceiling_height` is a real property, in TypeScript.
- [Content-addressed schemas](content-addressed-schemas.md): how 17 versions of
  the schema fit in about 1 MB for the browser.

## How work gets done and where it happens

- [A synchronous core with async edges](sync-core-async-edge.md): why `parseIdf`
  takes a string and never a path, in TypeScript.
- [Simulation architecture](../concepts/simulation-architecture.md): why
  simulations run in subprocesses on a copy of your model, in Python.
- [Weather data pipeline](../concepts/weather-pipeline.md): how station search,
  downloads, and design days fit together.
- [Caching strategy](../concepts/caching.md): what idfkit caches, and why.
- [Geocoding and IP location](geocoding.md): the free services behind address
  and "near me" lookup, and their accuracy and privacy trade-offs.
- [How the schedule evaluator works](../design/schedule-evaluator.md): how the
  pure-Python schedule engine resolves the Year, Week, and Day hierarchy.
- [Performance and benchmarks](../benchmarks.md): how idfkit compares to eppy
  and other tools, and how those numbers were measured.
