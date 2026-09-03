# How to collect diagnostics instead of throwing

Parsing is strict by default: the first problem stops the parse and nothing
comes back. That is right for a script, where a bad file should stop the run.
It is wrong for an editor, a language server, or a batch job over a directory
of models, all of which have to keep going and report everything they found.

This guide turns strict parsing off, collects what the parser could not make
sense of, and says where the two other checks live: schema validation and
reference integrity, neither of which a parse performs.

{{ parity("parse-diagnostics") }}

## Turn strict parsing off

=== "Python"

    ```python
    from idfkit import parse_idf

    model = parse_idf("model.idf", strict_parsing=False)
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/how-to/collect-diagnostics/turn_strict_parsing_off.ts:example"
    ```

You get a document either way. With strict parsing off it is the best
reconstruction the parser could manage: objects it could not read are skipped,
and everything it could read is in the document.

The Python argument is `strict_parsing`, not `strict`, and the distinction is
load-bearing. Python's `strict` is a separate setting on the document that
decides whether reading an unknown field name raises or returns `None`, and it
has nothing to do with how the file was parsed.

## Collect what was skipped

The two libraries report the recoverable findings differently, and the
difference is idiomatic rather than accidental. TypeScript returns them beside
the document, because a browser caller that gets a throw loses the partial
model it could still have shown. Python sends them to the standard library's
logging module, because a Python caller expects a failure it must handle to
arrive as an exception and everything else to arrive as a log record.

=== "Python"

    ```python
    import logging

    from idfkit import parse_idf


    class CollectDiagnostics(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            print(f"{record.name}: {record.getMessage()}")


    logging.getLogger("idfkit").addHandler(CollectDiagnostics())
    model = parse_idf("model.idf", strict_parsing=False)
    # idfkit.idf_parser: Skipped 1 unknown object type(s): Nonsense:Type
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/how-to/collect-diagnostics/collect_what_was_skipped.ts:example"
    ```

For a large batch, TypeScript's `onDiagnostic` fires as each problem is found,
so you never hold every diagnostic for every file at once. The callback fires
in addition to the array being populated, not instead of it. Python's logging
handler already works this way: it is called per record, and nothing
accumulates unless you accumulate it.

```ts
--8<-- "docs/snippets/js/how-to/collect-diagnostics/collect_what_was_skipped_2.ts:example"
```

## Read the error when you do want to stop

Strict parsing is the right default for a script, and it still tells you where
the problem is. Every diagnostic carries a message and a line, plus the object
type when the parser knew which object it was inside.

=== "Python"

    ```python
    from idfkit import parse_idf
    from idfkit.exceptions import IDFParseError

    try:
        model = parse_idf("model.idf")
    except IDFParseError as error:
        for d in error.diagnostics:
            print(f"{d.filepath}:{d.line}:{d.column} ({d.obj_type}): {d.message}")
        raise
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/how-to/collect-diagnostics/read_the_error_when_you_do_want_to_stop.ts:example"
    ```

## Keep the diagnostics when reading from a file

TypeScript's `loadIdf` returns the document directly and discards the
diagnostics with it. Use `loadIdfWithDiagnostics` when you want both.

```ts
--8<-- "docs/snippets/js/how-to/collect-diagnostics/keep_the_diagnostics_when_reading_from_a_file.ts:example"
```

Python has no equivalent pair: `parse_idf` reads from a path already, and the
recoverable findings reach you through logging whichever way you call it.

## Diagnostics are not validation

Diagnostics are parse-time only: unknown object types, malformed values, fields
that do not fit their declared kind. Required fields, ranges, and choice lists
are not checked while parsing, so a model that parses without a single
diagnostic can still be rejected by EnergyPlus. Validation is a separate call,
and it returns findings rather than raising.

=== "Python"

    ```python
    from idfkit import validate_document

    result = validate_document(model)
    for error in result.errors:
        print(error.code, error.obj_type, error.message)
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/how-to/collect-diagnostics/diagnostics_are_not_validation.ts:example"
    ```

The `code` on a finding is stable across both languages: `E001` is a missing
required field in either. The `message` is not, because number formatting and
type names differ between the two runtimes. Match on `code`.

## Reference integrity is a third check

A field can name an object that does not exist, and neither the parser nor a
per-object validation run will say so. The reference graph answers that
question directly.

=== "Python"

    ```python
    valid_names = {obj.name for obj in model.all_objects if obj.name}

    for obj, field, target in model.references.get_dangling_references(valid_names):
        print(f"{obj.obj_type} '{obj.name}'.{field} points at missing '{target}'")
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/how-to/collect-diagnostics/reference_integrity_is_a_third_check.ts:example"
    ```

A document-wide validation run makes this check for you and reports it beside
the rest, so reach for the graph directly only when dangling references are the
one thing you care about.

## See also

- [Validation API](../api/validation.md) for every check and the codes it emits
- [How to configure logging](../concepts/logging.md) for the logger names and
  levels idfkit writes to in Python
- [How to handle simulation errors](../simulation/errors.md) for what
  EnergyPlus itself reports, which is a different set of problems again
