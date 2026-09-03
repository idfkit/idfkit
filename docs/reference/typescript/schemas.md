---
title: '@idfkit/schemas'
---

# `@idfkit/schemas`

EnergyPlus epJSON schemas for all 17 supported versions, content-addressed so
that the whole set is around 1 MB gzipped rather than 11.9 MB. See
[Content-addressed schemas](../../explanation/content-addressed-schemas.md) for why,
and [Slim schema format](../slim-schema-format.md) for what a definition contains.

```bash
npm install @idfkit/schemas
```

`@idfkit/core` re-exports `Schema`, `SchemaBundle`, `httpSource`, and the slim
type definitions, so most applications never import this package directly.

## Portable surface

::: @idfkit/schemas
    handler: typescript

## Node

::: idfkit-js::@idfkit/schemas.node
    handler: typescript
