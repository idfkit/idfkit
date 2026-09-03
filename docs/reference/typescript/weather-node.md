---
title: '@idfkit/weather/node'
---

# `@idfkit/weather/node`

Node-only conveniences: loading the bundled station index from disk with no
network call, and writing downloaded weather files to disk. This is the
asynchronous edge, kept separate so the portable surface never has to touch
`node:fs`.

```ts
import { loadBundledIndex, saveWeatherFiles } from '@idfkit/weather/node';
```

::: idfkit-js::@idfkit/weather.node
    handler: typescript
