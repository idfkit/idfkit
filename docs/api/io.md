# I/O -- Parsers & Writers

Functions and classes for reading and writing EnergyPlus models in IDF
(text) and epJSON (JSON) formats.

## Convenience Loaders

Top-level convenience functions:

- `load_idf(path, version=None, *, strict=True, strict_fields=False, preserve_formatting=False)` for IDF files. Strict parsing
  is on by default.
- `load_epjson(path, version=None, *, strict_fields=False, preserve_formatting=False)` for epJSON files.

::: idfkit.load_idf

::: idfkit.load_epjson

## IDF Parser

::: idfkit.idf_parser

## epJSON Parser

::: idfkit.epjson_parser

## Writers

::: idfkit.writers
