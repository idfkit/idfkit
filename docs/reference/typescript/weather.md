---
title: '@idfkit/weather'
---

# `@idfkit/weather`

Browser-side EPW weather-file retrieval. Search the climate.onebuilding.org TMYx
station index, then download and unpack weather files — with no filesystem and
no dependencies, so the same code runs in Node, a browser, a worker, or an edge
runtime. Reaching the network goes through the global `fetch`, overridable per
call for a CORS proxy. Node-only conveniences live in
[`@idfkit/weather/node`](weather-node.md).

```bash
npm install @idfkit/weather
```

For a task-shaped walkthrough, see
[How to fetch a weather file](../../weather/downloads.md).

::: @idfkit/weather
    handler: typescript
