---
title: '@idfkit/core/node'
---

# `@idfkit/core/node`

Node-only conveniences: reading and writing files, and resolving a schema for a
version detected in a file. This is the asynchronous edge of the library, kept
separate so that the portable core never has to be async and browser bundles
never pull in `node:fs`.

```ts
import { loadIdf, saveIdf } from '@idfkit/core/node';
```

::: idfkit-js::@idfkit/core.node
    handler: typescript
