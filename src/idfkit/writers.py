"""
Writers for IDF and epJSON formats.

Provides serialization of IDFDocument to both formats. Each format has two entry points:
``write_*`` serializes to a string and never touches the disk, and ``save_*`` serializes and
writes the result to a path.

The [write_idf][idfkit.writers.write_idf] and [save_idf][idfkit.writers.save_idf] functions
accept an *output_type* parameter that mirrors eppy's ``idf.outputtype`` options:

- ``"standard"`` (default): field comments included (``!- Field Name``).
- ``"nocomment"``: no field comments, one field per line.
- ``"compressed"``: entire object on a single line (minimal whitespace).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, cast

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .cst import CSTNode
    from .document import IDFDocument
    from .objects import IDFObject

OutputType = Literal["standard", "nocomment", "compressed"]

#: How the writer orders objects.
#:
#: An enumeration rather than a boolean, because three behaviours exist today across the two
#: languages and two formats and a flag cannot express three things: this library's IDF writer
#: sorts by type name with Version pinned first, its epJSON writer keeps collection order with
#: Version first, and the other language keeps insertion order in both formats. A `sorted`/`source`
#: pair names what each of those is, and leaves room for the third to be named if it ever needs to
#: be reached from here.
#:
#: `"sorted"` is the default for this library's IDF writer and does not move (FR-017).
Ordering = Literal["sorted", "source"]

#: The two-space indent this writer has always used. The other language uses four.
DEFAULT_INDENT = 2

#: The column field comments are padded to. The same 30 in both languages, and the one default of
#: the six that already agrees.
DEFAULT_COMMENT_COLUMN = 30


def _resolve_version_identifier(doc: IDFDocument[bool]) -> str:
    """Read version_identifier from the Version object, falling back to doc.version."""
    version_coll = doc.collections.get("Version")
    if version_coll:
        obj = version_coll.first()
        if obj is not None:
            vi = obj.data.get("version_identifier")
            if isinstance(vi, str) and vi.strip():
                return vi.strip()
    v = doc.version
    return f"{v[0]}.{v[1]}"


def write_idf(
    doc: IDFDocument[bool],
    output_type: OutputType = "standard",
    *,
    preserve_formatting: bool | None = None,
    indent: int = DEFAULT_INDENT,
    comment_column: int = DEFAULT_COMMENT_COLUMN,
    ordering: Ordering = "sorted",
    version_first: bool = True,
) -> str:
    """
    Serialize a document to IDF text.

    Returns the text; it never touches the disk. Use
    [save_idf][idfkit.writers.save_idf] to put the text on disk.

    Args:
        doc: The document to serialize.
        output_type: Output formatting mode, ``"standard"`` (with
            comments), ``"nocomment"`` (no comments), or
            ``"compressed"`` (single-line objects). Mirrors eppy's
            ``idf.outputtype``. An output type other than ``"standard"``
            takes precedence over *preserve_formatting*, including over an
            explicit ``True``: a different output form is a different
            artifact, which the original text was never going to express.
        preserve_formatting: If ``True``, reproduce the original source
            text for unmodified objects and apply standard formatting only
            to objects that were mutated or added after parsing. Requires
            the document to have been parsed with
            ``preserve_formatting=True``. When ``None`` (the default),
            automatically uses lossless output if a CST is available and
            *output_type* is ``"standard"``.
        indent: Spaces before each field line. Defaults to the two this
            writer has always used.
        comment_column: Column the ``!-`` field comments are padded to.
            Defaults to 30. A value longer than the column pushes its
            comment right rather than being truncated.
        ordering: ``"sorted"`` to write object types in alphabetical order,
            which is the default and what the ``!-Option SortedOrder``
            header declares, or ``"source"`` to keep the document's own
            collection order, which writes ``!-Option OriginalOrderTop``
            instead. An enumeration rather than a boolean because three
            orderings exist across the two libraries and two formats.

    Returns:
        The IDF text.

    Raises:
        ValueError: If *preserve_formatting* is explicitly ``True`` on a
            document that carries a CST while *indent*, *comment_column*,
            *ordering* or *version_first* is away from its default.
            Reproducing the original text and reformatting it are
            contradictory requests.

    Examples:
        Serialize the model to an IDF string for inspection:

        >>> from idfkit import new_document, write_idf
        >>> model = new_document()
        >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
        Zone('Perimeter_ZN_1')
        >>> idf_str = write_idf(model)
        >>> "Zone," in idf_str
        True

        Use compressed format for batch parametric runs:

        >>> compressed = write_idf(model, output_type="compressed")
        >>> "\\n" not in compressed.split("Zone")[1].split(";")[0]
        True
    """
    # An explicitly requested output FORM wins over preservation, including over an explicit
    # `preserve_formatting=True`. A form is a different artifact, which the original text was never
    # going to express, so producing it is honest; granting preservation instead drops the request
    # in silence, which is what this did until the other language's decision table was written down
    # beside it and the two were compared.
    if output_type != "standard":
        use_preserve = False
    elif preserve_formatting is not None:
        use_preserve = preserve_formatting
    else:
        use_preserve = doc.cst is not None

    # A control that is not at its default asks for output the original text does not have, so the
    # lossless path cannot honour it. Reproducing the file byte for byte and indenting to three
    # spaces are contradictory requests, and silently doing the first would be the wrong answer.
    #
    # `version_first` belongs in this set and was missing from it, so asking to move the version
    # statement while preserving was granted silently: the file came back with the statement where
    # the author left it and no word about the request. It is a reformatting control like the other
    # three, because moving a statement is a change to how the text is laid out.
    #
    # Away from its default is a REQUEST TO FORMAT on the default path too, which is what the
    # `not formatting_requested` clause below says: a caller who names a control and does not name
    # preservation gets the control, not a silent drop of it.
    #
    # The conflict is only real when the lossless path would actually be taken. `preserve_formatting=True`
    # on a document that carries no CST has always fallen back to this writer, and asking for a control at
    # the same time must not turn that quiet fallback into an error.
    formatting_requested = (
        indent != DEFAULT_INDENT
        or comment_column != DEFAULT_COMMENT_COLUMN
        or ordering != "sorted"
        or version_first is not True
    )
    if formatting_requested and use_preserve and preserve_formatting and doc.cst is not None:
        msg = (
            "preserve_formatting reproduces the original text, so it cannot also apply indent, "
            "comment_column, ordering or version_first. Pass one or the other."
        )
        raise ValueError(msg)

    if use_preserve and doc.cst is not None and not formatting_requested:
        content = _write_idf_lossless(doc)
    else:
        writer = IDFWriter(
            doc,
            output_type=output_type,
            indent=indent,
            comment_column=comment_column,
            ordering=ordering,
            version_first=version_first,
        )
        content = writer.to_string()

    logger.debug("Serialized IDF (%d objects) to string", len(doc))
    return content


def save_idf(
    doc: IDFDocument[bool],
    path: Path | str,
    encoding: str = "latin-1",
    output_type: OutputType = "standard",
    *,
    preserve_formatting: bool | None = None,
    indent: int = DEFAULT_INDENT,
    comment_column: int = DEFAULT_COMMENT_COLUMN,
    ordering: Ordering = "sorted",
    version_first: bool = True,
) -> None:
    """
    Serialize a document to IDF text and write it to *path*.

    The disk-writing counterpart of [write_idf][idfkit.writers.write_idf].

    Args:
        doc: The document to save.
        path: Output path.
        encoding: Output encoding.
        output_type: Output formatting mode, as for
            [write_idf][idfkit.writers.write_idf].
        preserve_formatting: Lossless output control, as for
            [write_idf][idfkit.writers.write_idf].
        indent: Field-line indent, as for
            [write_idf][idfkit.writers.write_idf].
        comment_column: Comment column, as for
            [write_idf][idfkit.writers.write_idf].
        ordering: Object ordering, as for
            [write_idf][idfkit.writers.write_idf].

    Examples:
        Write to disk for EnergyPlus simulation:

            ```python
            save_idf(model, "in.idf")
            ```

        Lossless round-trip:

            ```python
            from idfkit import load_idf, save_idf
            model = load_idf("building.idf", preserve_formatting=True)
            save_idf(model, "building_copy.idf")  # byte-identical
            ```
    """
    content = write_idf(
        doc,
        output_type,
        preserve_formatting=preserve_formatting,
        indent=indent,
        comment_column=comment_column,
        ordering=ordering,
        version_first=version_first,
    )
    path = Path(path)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)
    logger.info("Wrote IDF (%d objects) to %s", len(doc), path)


def write_epjson(
    doc: IDFDocument[bool],
    indent: int = 2,
    *,
    preserve_formatting: bool | None = None,
) -> str:
    """
    Serialize a document to epJSON text.

    Returns the text; it never touches the disk. Use
    [save_epjson][idfkit.writers.save_epjson] to put the text on disk.

    Args:
        doc: The document to serialize.
        indent: JSON indentation.
        preserve_formatting: If ``True``, return the original JSON text
            verbatim when no objects have been modified. When ``None``
            (the default), automatically uses lossless output if raw text
            is available and no objects were mutated.

    Returns:
        The epJSON text.

    Examples:
        Serialize the model to epJSON for use with EnergyPlus v9.3+:

        >>> from idfkit import new_document, write_epjson
        >>> model = new_document()
        >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
        Zone('Perimeter_ZN_1')
        >>> json_str = write_epjson(model)
        >>> '"Zone"' in json_str
        True
    """
    # Note: epJSON preservation is all-or-nothing (any mutation or addition
    # falls back to the standard JSON writer), unlike IDF which has per-object
    # granularity via CST nodes.
    use_preserve = preserve_formatting if preserve_formatting is not None else doc.raw_text is not None

    # If preserve_formatting and we have raw text, check whether the document is
    # still the one that text describes: nothing touched, nothing added, nothing
    # removed.
    #
    # The count is the half that asking the survivors cannot supply. Every object
    # left after a removal is still pristine, so `all_clean` alone reproduced the
    # original text with the removed object still in it: a file that loads and
    # misrepresents the model. An addition is caught by the same comparison from
    # the other side, since a new object carries no sentinel and fails
    # `all_clean` anyway.
    if use_preserve and doc.raw_text is not None:
        # `# pyright: ignore` for the same reason `epjson_parser` needs one when it sets this:
        # the generated stub answers every name it does not declare with a collection, and it
        # declares no internal attribute, so reading one types as `IDFCollection` here.
        count_at_read = cast("int | None", doc._count_at_read)
        unchanged = count_at_read == len(doc) and all(obj.source_text is not None for obj in doc.all_objects)
        if unchanged:
            logger.debug("Serialized epJSON (%d objects, lossless) to string", len(doc))
            return doc.raw_text

    # Fall back to standard writer.
    writer = EpJSONWriter(doc)
    data = writer.to_dict()

    logger.debug("Serialized epJSON (%d objects) to string", len(doc))
    return json.dumps(data, indent=indent)


def save_epjson(
    doc: IDFDocument[bool],
    path: Path | str,
    indent: int = 2,
    *,
    preserve_formatting: bool | None = None,
) -> None:
    """
    Serialize a document to epJSON text and write it to *path*.

    The disk-writing counterpart of
    [write_epjson][idfkit.writers.write_epjson].

    Args:
        doc: The document to save.
        path: Output path.
        indent: JSON indentation.
        preserve_formatting: Lossless output control, as for
            [write_epjson][idfkit.writers.write_epjson].

    Examples:
        Write to disk:

            ```python
            save_epjson(model, "in.epJSON")
            ```
    """
    content = write_epjson(doc, indent, preserve_formatting=preserve_formatting)
    path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info("Wrote epJSON (%d objects) to %s", len(doc), path)


def _emit_cst_node(
    node: CSTNode,
    formatter: IDFWriter,
    parts: list[str],
    emitted: set[int],
    live_ids: set[int],
) -> None:
    """Emit a single CST node — verbatim for clean objects, reformatted for dirty ones."""
    if node.obj is None:
        parts.append(node.text)
        return

    obj = node.obj
    if id(obj) not in live_ids:
        return  # removed — skip

    emitted.add(id(obj))

    if obj.source_text is not None:
        parts.append(obj.source_text)
    else:
        parts.append(formatter.format_object(obj))
        parts.append("\n\n")


def _write_idf_lossless(doc: IDFDocument[bool]) -> str:
    """Produce IDF output that preserves original formatting via the CST.

    Unmodified objects are emitted verbatim.  Mutated or new objects use
    the standard :class:`IDFWriter` formatter.  Removed objects are dropped.
    """
    cst = doc.cst
    if cst is None:
        msg = "Document has no CST — parse with preserve_formatting=True"
        raise ValueError(msg)

    parts: list[str] = []
    formatter = IDFWriter(doc, output_type="standard")
    emitted: set[int] = set()
    live_ids = {id(o) for o in doc.all_objects}

    for node in cst.nodes:
        _emit_cst_node(node, formatter, parts, emitted, live_ids)

    # Append objects added after parsing (not in any CST node).
    new_objs = [formatter.format_object(o) for o in doc.all_objects if id(o) not in emitted]
    if new_objs:
        tail = parts[-1] if parts else ""
        if tail and not tail.endswith("\n"):
            parts.append("\n")
        for obj_str in new_objs:
            parts.append(obj_str)
            parts.append("\n\n")

    return "".join(parts)


class IDFWriter:
    """
    Writes IDFDocument to IDF text format.

    The IDF format is:
    ```
    ObjectType,
      field1,    !- Field 1 Name
      field2,    !- Field 2 Name
      field3;    !- Field 3 Name
    ```

    Supports three *output_type* modes mirroring eppy's
    ``idf.outputtype``:

    - ``"standard"`` — full comments (default).
    - ``"nocomment"`` — no field comments, one field per line.
    - ``"compressed"`` — each object on a single line.
    """

    def __init__(
        self,
        doc: IDFDocument,
        output_type: OutputType = "standard",
        *,
        indent: int = DEFAULT_INDENT,
        comment_column: int = DEFAULT_COMMENT_COLUMN,
        ordering: Ordering = "sorted",
        version_first: bool = True,
    ):
        self._doc = doc
        self._output_type = output_type
        self._indent = indent
        self._comment_column = comment_column
        self._ordering = ordering
        self._version_first = version_first

    def _header_lines(self) -> list[str]:
        """The generator header, or nothing in compressed output.

        The `!-Option` directive states the order the file is actually in. IDFEditor reads it, so
        writing `SortedOrder` over source-ordered objects would announce an order the file does not
        have. `sorted` is the default, so the default header does not move.
        """
        if self._output_type == "compressed":
            return []

        from . import __version__

        directive = "SortedOrder" if self._ordering == "sorted" else "OriginalOrderTop"
        return [f"!-Generator idfkit v{__version__}", f"!-Option {directive}", ""]

    def _version_lines(self) -> list[str]:
        """The Version object, written by hand rather than through the field loop."""
        version_identifier = _resolve_version_identifier(self._doc)
        pad = " " * self._indent

        if self._output_type == "compressed":
            return [f"Version,{version_identifier};"]
        if self._output_type == "standard":
            # Its comment lands at column 27 at the default indent rather than at `comment_column`.
            # The literal run of spaces is kept so that default output is unchanged; only the indent
            # moves when the caller moves it.
            return ["Version,", f"{pad}{version_identifier};                    !- Version Identifier", ""]
        return ["Version,", f"{pad}{version_identifier};", ""]

    def to_string(self) -> str:
        """Convert document to IDF string."""
        lines: list[str] = self._header_lines()

        def write_version() -> None:
            lines.extend(self._version_lines())

        # Version ahead of everything else, which is what this writer has always done and what
        # `version_first` defaults to, so the default does not move (FR-017). Turning it off leaves
        # Version in whichever position the chosen ordering puts it, which is what a caller wants
        # when the output is going to be diffed against a source file that did not lead with it.
        if self._version_first:
            write_version()

        # Write objects grouped by type.
        #
        # `sorted` is this writer's default and does not move. `source` keeps the document's own
        # collection order, which is what the other language does and what a caller wants when the
        # output is going to be diffed against an input rather than against another writer.
        type_order = (
            sorted(self._doc.collections.keys()) if self._ordering == "sorted" else list(self._doc.collections.keys())
        )
        for obj_type in type_order:
            if obj_type.upper() == "VERSION":
                if not self._version_first:
                    write_version()
                continue
            collection = self._doc.collections[obj_type]
            if not collection:
                continue

            for obj in collection:
                obj_str = self.format_object(obj)
                lines.append(obj_str)
                if self._output_type != "compressed":
                    lines.append("")

        return "\n".join(lines)

    def _get_field_values_and_comments(self, obj: IDFObject) -> tuple[list[str], list[str]]:  # noqa: C901
        """Get the ordered field values and comment labels for *obj*.

        Storage is canonical: extensible groups live as a list of dicts under
        the wrapper key (e.g. ``obj.data["vertices"]``). For IDF output we
        flatten them into the legacy positional sequence with comment labels
        synthesised on the fly (``Vertex X Coordinate 2`` for the second
        ``vertex_x_coordinate`` token, etc.).
        """
        obj_type = obj.obj_type
        schema = self._doc.schema

        obj_has_name = True
        pc = None
        if schema:
            obj_has_name = schema.has_name(obj_type)
            pc = schema.get_parsing_cache(obj_type)

        if obj.field_order:
            if obj_has_name:
                field_names: list[str] = ["name", *list(obj.field_order)]
            else:
                field_names = list(obj.field_order)
        elif schema:
            field_names = schema.get_all_field_names(obj_type)
        else:
            field_names = ["name", *list(obj.data.keys())] if obj_has_name else list(obj.data.keys())

        values: list[str] = []
        comments: list[str] = []
        wrapper_key = pc.ext_wrapper_key if pc and pc.extensible else None

        for field_name in field_names:
            if field_name == "name":
                values.append(obj.name or "")
                comments.append("Name")
            elif field_name == wrapper_key:
                # Skip — handled below as positional extensible expansion.
                continue
            else:
                value = obj.data.get(field_name)
                values.append(self._format_value(value))
                comment = field_name.replace("_", " ").title()
                comments.append(comment)

        # Append extensible groups as positional tokens (legacy IDF layout).
        if wrapper_key and pc and pc.ext_field_names:
            inner_names = pc.ext_field_names
            ext_items_raw: Any = obj.data.get(wrapper_key) or []
            if isinstance(ext_items_raw, list):
                ext_items: list[dict[str, Any]] = cast("list[dict[str, Any]]", ext_items_raw)
                for group_idx, item in enumerate(ext_items, start=1):
                    suffix = "" if group_idx == 1 else f" {group_idx}"
                    for inner in inner_names:
                        values.append(self._format_value(item.get(inner)))
                        comments.append(f"{inner.replace('_', ' ').title()}{suffix}")

        # Trim trailing empty fields
        while len(values) > 1 and values[-1] == "":
            values.pop()
            comments.pop()

        return values, comments

    def format_object(self, obj: IDFObject) -> str:
        """Convert a single object to IDF string."""
        values, comments = self._get_field_values_and_comments(obj)
        obj_type = obj.obj_type

        if self._output_type == "compressed":
            parts = ",".join(values)
            return f"{obj_type},{parts};"

        lines: list[str] = [f"{obj_type},"]
        for i, (value, comment) in enumerate(zip(values, comments, strict=False)):
            is_last = i == len(values) - 1
            terminator = ";" if is_last else ","

            pad = " " * self._indent
            if self._output_type == "standard":
                field_str = f"{pad}{value}{terminator}"
                field_str = field_str.ljust(self._comment_column)
                field_str += f"!- {comment}"
            else:
                # nocomment
                field_str = f"{pad}{value}{terminator}"

            lines.append(field_str)

        return "\n".join(lines)

    def _format_value(self, value: Any) -> str:
        """Format a field value for IDF output."""
        if value is None:
            return ""
        if isinstance(value, bool):
            return "Yes" if value else "No"
        if isinstance(value, float):
            if value == 0.0:
                return "0"
            abs_val = abs(value)
            if abs_val >= 1e10 or abs_val < 0.0001:
                return f"{value:.6e}"
            return f"{value:g}"
        if isinstance(value, list):
            # Handle vertex lists etc.
            items = cast(list[Any], value)
            return ", ".join(str(v) for v in items)
        text = str(value)
        if any(ch in text for ch in (",", ";", "!")):
            logger.warning(
                "Field value %r contains IDF delimiter characters (comma, semicolon, or exclamation mark) "
                "that will produce invalid IDF output",
                text,
            )
        return text

    def write_to_file(self, filepath: Path | str, encoding: str = "latin-1") -> None:
        """Write to file."""
        content = self.to_string()
        with open(filepath, "w", encoding=encoding) as f:
            f.write(content)


class EpJSONWriter:
    """
    Writes IDFDocument to epJSON format.

    The epJSON format is:
    ```json
    {
      "Version": {
        "Version 1": {
          "version_identifier": "23.2"
        }
      },
      "Zone": {
        "Zone 1": {
          "direction_of_relative_north": 0.0,
          ...
        }
      }
    }
    ```
    """

    def __init__(self, doc: IDFDocument):
        self._doc = doc

    def to_dict(self) -> dict[str, Any]:
        """Convert document to epJSON dict."""
        result: dict[str, Any] = {}

        # Add Version
        result["Version"] = {"Version 1": {"version_identifier": _resolve_version_identifier(self._doc)}}

        # Add objects by type
        for obj_type, collection in self._doc.collections.items():
            if obj_type.upper() == "VERSION":
                continue
            if not collection:
                continue

            result[obj_type] = {}
            # A blank Name is not an absent Name. Only a type that declares no Name field at all
            # gets the synthetic "<Type> N" key, numbered 1-based in file order. A type whose Name
            # field is optional and left blank keeps the blank verbatim, so its key is "". Keying a
            # blank Name as "<Type> N" manufactures a name into a namespace the writer does not own,
            # and any object the user genuinely named "<Type> N" is then silently overwritten.
            type_has_name = self._type_has_name(obj_type, collection.first())
            nameless_counter = 0
            for obj in collection:
                obj_data = self._object_to_dict(obj)
                if type_has_name:
                    key = obj.name
                else:
                    # Generate unique key for nameless objects (e.g. Output:Variable)
                    nameless_counter += 1
                    key = f"{obj_type} {nameless_counter}"
                result[obj_type][key] = obj_data

        return result

    def _type_has_name(self, obj_type: str, sample: IDFObject | None) -> bool:
        """Whether *obj_type* declares a Name field.

        Answered from the document schema when one is loaded, otherwise from the schema dict carried
        by the objects themselves. With no schema information at all the answer is ``True``, which
        matches what the IDF parser assumes when it has no parsing cache for a type: the first field
        is the name.
        """
        schema = self._doc.schema
        if schema is not None:
            return schema.has_name(obj_type)
        if sample is not None and sample.schema_dict is not None:
            return "name" in sample.schema_dict
        return True

    def _object_to_dict(self, obj: IDFObject) -> dict[str, Any]:
        """Convert object to epJSON dict (excluding name).

        Storage is canonical, so this is a pass-through that drops empty
        scalars and routes each value through ``_format_value`` for normal
        type handling. The wrapper-key list (if any) is emitted verbatim —
        each item is already a dict matching the schema's items.properties.
        """

        result: dict[str, Any] = {}
        for field_name, value in obj.data.items():
            if value is not None and value != "":
                result[field_name] = self._format_value(value)
        return result

    def _format_value(self, value: Any) -> Any:
        """Format a field value for epJSON output."""
        # epJSON uses native JSON types
        if isinstance(value, str):
            # Check for special values
            lower = value.lower()
            if lower == "autocalculate":
                return "Autocalculate"
            if lower == "autosize":
                return "Autosize"
            if lower == "yes":
                return "Yes"
            if lower == "no":
                return "No"
        return value

    def write_to_file(self, filepath: Path | str, indent: int = 2) -> None:
        """Write to file."""
        data = self.to_dict()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)


def convert_idf_to_epjson(
    idf_path: Path | str,
    epjson_path: Path | str | None = None,
) -> Path:
    """
    Convert an IDF file to epJSON format.

    Args:
        idf_path: Input IDF file path
        epjson_path: Output epJSON path (default: same name with .epJSON extension)

    Returns:
        Path to the output file

    Examples:
        Convert an IDF model to native JSON format:

            ```python
            output = convert_idf_to_epjson("5ZoneAirCooled.idf")
            # Creates 5ZoneAirCooled.epJSON

            convert_idf_to_epjson("legacy_model.idf", "modern_model.epJSON")
            ```
    """
    from .idf_parser import parse_idf

    idf_path = Path(idf_path)

    epjson_path = idf_path.with_suffix(".epJSON") if epjson_path is None else Path(epjson_path)

    doc = parse_idf(idf_path)
    save_epjson(doc, epjson_path)

    return epjson_path


def convert_epjson_to_idf(
    epjson_path: Path | str,
    idf_path: Path | str | None = None,
) -> Path:
    """
    Convert an epJSON file to IDF format.

    Args:
        epjson_path: Input epJSON file path
        idf_path: Output IDF path (default: same name with .idf extension)

    Returns:
        Path to the output file

    Examples:
        Convert an epJSON model back to classic IDF format:

            ```python
            output = convert_epjson_to_idf("5ZoneAirCooled.epJSON")
            # Creates 5ZoneAirCooled.idf

            convert_epjson_to_idf("modern_model.epJSON", "classic_model.idf")
            ```
    """
    from .epjson_parser import parse_epjson

    epjson_path = Path(epjson_path)

    idf_path = epjson_path.with_suffix(".idf") if idf_path is None else Path(idf_path)

    doc = parse_epjson(epjson_path)
    save_idf(doc, idf_path)

    return idf_path
