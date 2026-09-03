---
title: Browser simulation
description: Why a WebAssembly build of EnergyPlus exists, what it can do, and what it cannot.
---

# Why EnergyPlus runs in a browser

Every other page on this site treats simulation as something that happens
elsewhere. You build a model, write it out, and hand it to EnergyPlus. In
JavaScript there is a third option: EnergyPlus itself, compiled to WebAssembly,
running in the page.

{{ parity("browser-simulation") }}

This page explains why that build exists, what it is good for, and the several
things it is not. The task itself is [How to run a simulation in the
browser](../how-to/run-a-simulation-in-the-browser.md).

## What it is

EnergyPlus is Fortran and C++. `@idfkit/engine` is that source compiled to
WebAssembly, plus a thin JavaScript facade that hands it an IDF string and a
weather file and gives back its output files parsed. The binary and its
supporting data ship separately as `@idfkit/engine-assets`, about 51 MB, and
are versioned by the EnergyPlus release they carry.

It is a different package from everything else on this site, built in a
different repository, and it is not reachable through the shared install name.
That is deliberate and it is not going to change: 51 MB pinned to one
EnergyPlus release is not something `npm install idfkit` may quietly acquire
(FR-070).

## Why bother

Because the alternative to a browser is a server, and a server is a different
kind of project.

A model editor that can simulate needs somewhere to run EnergyPlus. Without a
browser build that means an upload endpoint, a queue, a worker pool with
EnergyPlus installed, a results store, and an answer to what happens when
somebody uploads a model that runs for four hours. All of that is ordinary
infrastructure work and none of it is about buildings.

Running in the page removes the whole category. The model never leaves the
machine it was made on, which also settles the question of who is holding
somebody's building data. A teaching tool, a sensitivity slider, a
configurator that shows the load change as you drag a window bigger: each is a
static page.

## What it cannot do

**It is not faster.** WebAssembly runs EnergyPlus at roughly half native speed.
An annual simulation that takes twenty seconds locally takes about forty here.
For one run that is nothing; for a thousand-run parametric sweep it is the
difference between an afternoon and a day, and the sweep belongs
[on a machine with EnergyPlus installed](../simulation/running.md).

**It is one release.** The asset package carries a single EnergyPlus version.
Supporting several means shipping several 51 MB packages, so a model written for
another release has to be migrated first. The Python library, which drives a
locally installed EnergyPlus, runs whichever versions are installed.

**Memory is the real ceiling.** A browser tab has far less address space than a
workstation, and a large model with fine timesteps and many output variables
will exhaust it. The failure is a dead tab, not a diagnostic.

**Reading results is the engine's job, not this library's.** `@idfkit/core` has
no output-reading API and is not planning one. The engine returns its own
parsed structures.

## Why the Python library has no equivalent, permanently

The parity ledger records local simulation as permanently absent from
JavaScript and browser simulation as permanently absent from Python, and both
entries mean it.

Python already runs on a machine that can install EnergyPlus, so a WebAssembly
build there would be a slower way to do something the language can do directly.
The reverse is stronger still: a browser cannot start a subprocess. These are
not two implementations of one capability with one side unfinished. They are
two capabilities, and the ledger holds them as separate entries so that neither
language reads as deficient for lacking the other's (FR-068).

## What this site does and does not check

The example on the how-to page is compiled in CI against `@idfkit/engine`'s
published type declarations, so renaming a method on the engine breaks the
documentation checks (SC-030). That is a real check and it caught a real thing:
the interface is `EnergyPlusEngine`, not `EnergyPlus`, and a hand-written
stand-in for it had the name wrong.

What is not checked is whether the example *works*. Nothing in this
repository's CI runs EnergyPlus in a browser, so a change that type-checks and
produces wrong output would ship. The live runner embedded on the how-to page
executes the same source the type-check reads, which means a reader can see for
themselves; it is a demonstration, not a test, and this site does not claim
otherwise.

## See also

- [How to run a simulation in the browser](../how-to/run-a-simulation-in-the-browser.md)
- [How to run a simulation](../simulation/running.md), the Python path
- [Capability parity](parity.md), where both simulation entries are recorded
- [A synchronous core with async edges](sync-core-async-edge.md), which is why
  the seam between the two libraries is plain IDF text
