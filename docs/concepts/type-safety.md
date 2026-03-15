# Type-Safe Development

idfkit ships auto-generated type stubs for all 858 EnergyPlus object types.
Your IDE gets autocomplete, inline documentation, and error detection out of
the box — no plugins or configuration needed.

## IDE Autocomplete and Inline Docs

Every object type has a typed attribute accessor on `IDFDocument` and typed
fields on individual objects. Your IDE will show field names, types (including
`Literal` for enumerated choices), docstrings with units, defaults, and valid
ranges.

```python
--8<-- "docs/snippets/concepts/type-safety/autocomplete.py:example"
```

For example, hovering over `zone.ceiling_height` in your IDE will show:

```
(property) ceiling_height: float | Literal["", "Autocalculate"] | None
```

## Strict Field Access

By default, accessing a misspelled field name returns `None`. Enable **strict
mode** to catch typos at runtime with an `AttributeError`:

```python
--8<-- "docs/snippets/concepts/type-safety/strict_fields.py:example"
```

| Function | Parameter |
|----------|-----------|
| `new_document()` | `strict=True` |
| `load_idf()` | `strict_fields=True` |
| `load_epjson()` | `strict_fields=True` |

!!! tip
    Strict mode is recommended during development. Disable it when loading
    third-party IDF files that may contain non-standard fields.

## Dynamic Key Access

When the object type is a string literal, `doc["Zone"]` returns a fully typed
collection. When the key comes from a variable, use `get_collection()` to get
a safely typed `IDFCollection[IDFObject]`:

```python
--8<-- "docs/snippets/concepts/type-safety/get_collection.py:example"
```

Use `doc["Zone"]` when you know the type at write time. Use
`doc.get_collection(obj_type)` in generic functions that accept any object type.

!!! note "Why `get_collection()`?"
    Under the hood, `doc["Zone"]` is typed via a `TypedDict` with all 858
    EnergyPlus object types as literal keys. This gives your type checker exact
    return types for each key — but `TypedDict` subscript access requires
    string *literals*, so a plain `str` variable won't type-check.
    An `@overload`-based approach was considered but rejected because 858
    overloads cause significant performance degradation in pyright.
    `get_collection()` is the lightweight escape hatch: it accepts any `str`
    and returns the base `IDFCollection[IDFObject]` type.

## Version Availability

Type stubs include **"Since: X.Y.Z"** annotations in docstrings for object
types and fields that were introduced after EnergyPlus 8.9.0. This helps you
avoid using features that don't exist in your target version:

```python
--8<-- "docs/snippets/concepts/type-safety/version_info.py:example"
```

Hovering over `SpaceHVACZoneReturnMixer` in your IDE shows the docstring
including "Since: 24.2.0", making it clear which minimum EnergyPlus version
is required.

## See Also

- [Version Compatibility](version-compatibility.md) — static linting for cross-version issues
- [API Reference: Document](../api/document.md) — full `IDFDocument` API
- [Quick Start](../getting-started/quick-start.md) — getting started guide
