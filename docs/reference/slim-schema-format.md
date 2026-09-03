# Slim schema format

`@idfkit/schemas` does not ship the raw epJSON schemas. It ships a reduced form
carrying everything needed to parse, write, and resolve references, with the
documentation metadata removed. This page describes that form; see
[Content-addressed schemas](../explanation/content-addressed-schemas.md) for why
it exists. The format is specific to the TypeScript packages: Python reads the
epJSON schemas EnergyPlus publishes, one gzipped file per release, and has no
slim form.

Keys are single letters. This file is parsed on every cold start, and in a
browser that start is a page load.

## Bundle layout

```
data/
  index.json.gz              versions, and the manifest file for each
  types.json.gz              every unique type definition, keyed by content hash
  manifest-26-1-0.json.gz    type name -> hash, for one version
  manifest-25-2-0.json.gz
  ...
```

`index.json` is `BundleIndex`: a `versions` array, oldest first, and a
`manifests` record mapping version string to manifest file name. A manifest is a
flat `Record<typeName, hash>`. `types.json` is a flat `Record<hash, SlimType>`,
shared by every version.

Files are gzipped and inflated by the source. `httpSource` uses
`DecompressionStream` so the payload stays around 1 MB. It sniffs the gzip magic
bytes first, so it works whether the server leaves `Content-Encoding` unset or
sets it for the `.gz` extension, where the client inflates the body itself.

## `SlimType`

One object type, e.g. `Zone`.

| Key    | Meaning                                                                  |
| ------ | ------------------------------------------------------------------------ |
| `f`    | All field names in IDF positional order, from `legacy_idd.fields`        |
| `p`    | Field definitions, keyed by epJSON field name                            |
| `r`    | Required field names                                                     |
| `nref` | Reference lists the object's _name_ contributes to                       |
| `nreq` | `1` when the name is required                                            |
| `s`    | `1` when the object is a singleton, e.g. `Version`, `Building`           |
| `anon` | `1` when the object has no name field at all, e.g. `GlobalGeometryRules` |
| `x`    | Extensible group definition, if the type has one                         |
| `g`    | IDD group, e.g. `Thermal Zones and Surfaces`                             |

`f` is the load-bearing one: IDF is positional, and this array is the only thing
that says which slot a value belongs to.

## `SlimField`

| Key    | Meaning                                                                                    |
| ------ | ------------------------------------------------------------------------------------------ |
| `t`    | Storage class, see below                                                                   |
| `auto` | `1` when the field is an `anyOf` of a numeric branch and a string branch                   |
| `se`   | String literals that `anyOf` string branch accepts, see below                              |
| `ol`   | Reference lists this field points _into_: it is a foreign key                             |
| `ref`  | Reference lists this field contributes _to_: it is a key                                  |
| `e`    | Permitted values, for a choice field. Numbers on the fields that state choices numerically |
| `d`    | Schema default, applied on write when the field is absent                                  |
| `min`  | Inclusive minimum                                                                          |
| `max`  | Inclusive maximum                                                                          |
| `xmin` | Exclusive minimum, or `true` on a draft-04 version, see below                              |
| `xmax` | Exclusive maximum, or `true` on a draft-04 version, see below                              |
| `u`    | SI units, e.g. `m`                                                                         |
| `rc`   | `1` when the value is case-sensitive and must not be normalized                            |

`ol` and `ref` together are what the [reference
graph](../explanation/index.md) is built from: `ref` says a name enters a list,
`ol` says a field reads from one.

### `auto` and `se`, the two branches of an `anyOf`

13060 fields across the 17 bundled versions are declared `anyOf: [{number},
{string}]`: a capacity is a number, or the word that asks EnergyPlus to size it.
The bundle hoists the numeric branch onto the record, so `t`, `e`, `min`, `max`,
`xmin` and `xmax` all describe that branch, and sets `auto`. What survives of the
string branch is `se`, its enum, verbatim.

`se` is absent when the string branch declared no enum, and any string is legal
there. 646 fields have that shape, `Schedule:Compact`'s extensible `field` among
them. That is why the empty string is kept in `se` rather than filtered out the
way it is filtered out of `e`: `se: [""]` and no `se` at all are opposite claims.

Nothing about the sentinel can be assumed. 10565 fields take `Autosize` and 1781
take `Autocalculate`, and a consumer that accepts either everywhere accepts a
value EnergyPlus rejects.

### `xmin` and `xmax`, in two JSON Schema dialects

From 9.6.0 the schemas are draft-06 or later, where `exclusiveMinimum` carries
the bound itself, and `xmin` is a number. For 8.9.0 through 9.5.0 they are
draft-04, where the keyword is a boolean qualifying the sibling `minimum`, and
`xmin` is `true`. No version mixes the two. Branch on the type of the value, not
on the version: comparing a value against `true` silently compares it against 1.

## `FieldKind`

The `t` key. It records how a value must be formatted on the way back out, which
JavaScript cannot recover on its own: `3` and `3.0` are the same number at
runtime.

| Value   | Meaning                                       |
| ------- | --------------------------------------------- |
| `'a'`   | Alpha. Written verbatim.                      |
| `'n'`   | Real. Written with a decimal point preserved. |
| `'i'`   | Integer. Written without a decimal point.     |
| `'arr'` | Extensible array wrapper.                     |

## `SlimExtensible`

The `x` key on a type that has repeating field groups.

| Key      | Meaning                                                  |
| -------- | -------------------------------------------------------- |
| `key`    | epJSON key holding the array, e.g. `vertices`            |
| `fields` | Field names inside each repeat group, in IDF order       |
| `p`      | Definitions for the inner fields, from the array's items |

## What is dropped

`note`, `memo`, `ip-units`, and `field_info`. That is documentation metadata,
it is most of the weight, and it sits on the critical path of every parse.
Tooling that renders EnergyPlus documentation should read the source schemas
directly, or use [idfkit-docs](https://docs.idfkit.com).

## Reading a definition

```ts
import { localBundle } from '@idfkit/schemas/node';

const schema = await localBundle().load('26.1.0');

schema.resolve('ZONE'); // 'Zone'. IDF type names are case-insensitive
schema.get('Zone'); // the SlimType
schema.field('Zone', 'x_origin'); // { t: 'n', u: 'm', d: 0 }
```

Definitions are frozen and shared by identity across versions with the same
content hash, so they must not be mutated.
