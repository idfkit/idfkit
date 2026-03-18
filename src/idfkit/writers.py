"""
Writers for IDF and epJSON formats.

Provides serialization of IDFDocument to both formats.

The [write_idf][idfkit.writers.write_idf] function accepts an *output_type* parameter that
mirrors eppy's ``idf.outputtype`` options:

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


def _resolve_version_identifier(doc: IDFDocument[bool]) -> str:
    """Resolve version identifier from Version object, falling back to document metadata."""
    for obj_type, collection in doc.collections.items():
        if obj_type.upper() != "VERSION" or not collection:
            continue
        version_obj = collection.first()
        if version_obj is None:
            continue
        version_identifier = version_obj.data.get("version_identifier")
        if isinstance(version_identifier, str):
            version_identifier = version_identifier.strip()
            if version_identifier:
                return version_identifier
        elif version_identifier is not None:
            return str(version_identifier)

    version = doc.version
    return f"{version[0]}.{version[1]}"


def write_idf(
    doc: IDFDocument[bool],
    filepath: Path | str | None = None,
    encoding: str = "latin-1",
    output_type: OutputType = "standard",
    *,
    preserve_formatting: bool | None = None,
) -> str | None:
    """
    Write document to IDF format.

    Args:
        doc: The document to write.
        filepath: Output path (if ``None``, returns a string).
        encoding: Output encoding.
        output_type: Output formatting mode — ``"standard"`` (with
            comments), ``"nocomment"`` (no comments), or
            ``"compressed"`` (single-line objects).  Mirrors eppy's
            ``idf.outputtype``.  Ignored when *preserve_formatting* is
            active.
        preserve_formatting: If ``True``, reproduce the original source
            text for unmodified objects and apply standard formatting only
            to objects that were mutated or added after parsing.  Requires
            the document to have been parsed with
            ``preserve_formatting=True``.  When ``None`` (the default),
            automatically uses lossless output if a CST is available.

    Returns:
        IDF string if *filepath* is ``None``, otherwise ``None``.

    Examples:
        Serialize the model to an IDF string for inspection:

        >>> from idfkit import new_document, write_idf
        >>> model = new_document()
        >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
        Zone('Perimeter_ZN_1')
        >>> idf_str = write_idf(model)
        >>> "Zone," in idf_str
        True

        Write to disk for EnergyPlus simulation:

            ```python
            write_idf(model, "in.idf")
            ```

        Use compressed format for batch parametric runs:

        >>> compressed = write_idf(model, output_type="compressed")
        >>> "\\n" not in compressed.split("Zone")[1].split(";")[0]
        True

        Lossless round-trip:

            ```python
            from idfkit import load_idf, write_idf
            model = load_idf("building.idf", preserve_formatting=True)
            write_idf(model, "building_copy.idf")  # byte-identical
            ```
    """
    use_preserve = preserve_formatting if preserve_formatting is not None else doc.cst is not None

    if use_preserve and doc.cst is not None:
        content = _write_idf_lossless(doc)
    else:
        writer = IDFWriter(doc, output_type=output_type)
        content = writer.to_string()

    if filepath:
        filepath = Path(filepath)
        with open(filepath, "w", encoding=encoding) as f:
            f.write(content)
        logger.info("Wrote IDF (%d objects) to %s", len(doc), filepath)
        return None

    logger.debug("Serialized IDF (%d objects) to string", len(doc))
    return content


def write_epjson(
    doc: IDFDocument[bool],
    filepath: Path | str | None = None,
    indent: int = 2,
    *,
    preserve_formatting: bool | None = None,
) -> str | None:
    """
    Write document to epJSON format.

    Args:
        doc: The document to write
        filepath: Output path (if None, returns string)
        indent: JSON indentation
        preserve_formatting: If ``True``, return the original JSON text
            verbatim when no objects have been modified.  When ``None``
            (the default), automatically uses lossless output if raw text
            is available and no objects were mutated.

    Returns:
        JSON string if filepath is None, otherwise None

    Examples:
        Serialize the model to epJSON for use with EnergyPlus v9.3+:

        >>> from idfkit import new_document, write_epjson
        >>> model = new_document()
        >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
        Zone('Perimeter_ZN_1')
        >>> json_str = write_epjson(model)
        >>> '"Zone"' in json_str
        True

        Write to disk:

            ```python
            write_epjson(model, "in.epJSON")
            ```
    """
    use_preserve = preserve_formatting if preserve_formatting is not None else doc.raw_text is not None

    # If preserve_formatting and we have raw text, check whether any object
    # was mutated.  If not, emit the original text verbatim.
    if use_preserve and doc.raw_text is not None:
        all_clean = all(obj.source_text is not None for obj in doc.all_objects)
        if all_clean:
            content = doc.raw_text
            if filepath:
                filepath = Path(filepath)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info("Wrote epJSON (%d objects, lossless) to %s", len(doc), filepath)
                return None
            logger.debug("Serialized epJSON (%d objects, lossless) to string", len(doc))
            return content

    # Fall back to standard writer.
    writer = EpJSONWriter(doc)
    data = writer.to_dict()

    if filepath:
        filepath = Path(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
        logger.info("Wrote epJSON (%d objects) to %s", len(doc), filepath)
        return None

    logger.debug("Serialized epJSON (%d objects) to string", len(doc))
    return json.dumps(data, indent=indent)


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

    def __init__(self, doc: IDFDocument, output_type: OutputType = "standard"):
        self._doc = doc
        self._output_type = output_type

    def to_string(self) -> str:
        """Convert document to IDF string."""
        lines: list[str] = []

        if self._output_type != "compressed":
            # Write header comment
            lines.append("!-Generator archetypal")
            lines.append("!-Option SortedOrder")
            lines.append("")

        # Write Version first
        version_identifier = _resolve_version_identifier(self._doc)
        if self._output_type == "compressed":
            lines.append(f"Version,{version_identifier};")
        else:
            lines.append("Version,")
            if self._output_type == "standard":
                lines.append(f"  {version_identifier};                    !- Version Identifier")
            else:
                lines.append(f"  {version_identifier};")
            lines.append("")

        # Write objects grouped by type
        for obj_type in sorted(self._doc.collections.keys()):
            if obj_type.upper() == "VERSION":
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

    def _get_field_values_and_comments(self, obj: IDFObject) -> tuple[list[str], list[str]]:
        """Get the ordered field values and comment labels for *obj*."""
        obj_type = obj.obj_type
        schema = self._doc.schema

        obj_has_name = True
        if schema:
            obj_has_name = schema.has_name(obj_type)

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

        for field_name in field_names:
            if field_name == "name":
                values.append(obj.name or "")
                comments.append("Name")
            else:
                value = obj.data.get(field_name)
                values.append(self._format_value(value))
                comment = field_name.replace("_", " ").title()
                comments.append(comment)

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

            if self._output_type == "standard":
                field_str = f"  {value}{terminator}"
                field_str = field_str.ljust(30)
                field_str += f"!- {comment}"
            else:
                # nocomment
                field_str = f"  {value}{terminator}"

            lines.append(field_str)

        return "\n".join(lines)

    def _format_value(self, value: Any) -> str:
        """Format a field value for IDF output."""
        if value is None:
            return ""
        if isinstance(value, bool):
            return "Yes" if value else "No"
        if isinstance(value, float):
            # Avoid scientific notation for small numbers
            abs_val = abs(value)
            if abs_val < 1e-10:
                return "0"
            if abs_val >= 1e10 or abs_val < 0.0001:
                return f"{value:.6e}"
            return f"{value:g}"
        if isinstance(value, list):
            # Handle vertex lists etc.
            items = cast(list[Any], value)
            return ", ".join(str(v) for v in items)
        return str(value)

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
            nameless_counter = 0
            for obj in collection:
                obj_data = self._object_to_dict(obj)
                if obj.name:
                    key = obj.name
                else:
                    # Generate unique key for nameless objects (e.g. Output:Variable)
                    nameless_counter += 1
                    key = f"{obj_type} {nameless_counter}"
                result[obj_type][key] = obj_data

        return result

    def _object_to_dict(self, obj: IDFObject) -> dict[str, Any]:
        """Convert object to epJSON dict (excluding name)."""
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
    write_epjson(doc, epjson_path)

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
    write_idf(doc, idf_path)

    return idf_path
