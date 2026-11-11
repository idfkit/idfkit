"""Generate ``idfkit.hvac._node_fields``: which fields of which object types name a fluid node.

WHY GENERATED

The schema says *that* a field names a node in only one place: the ``"data_type": "node"`` tag,
which EnergyPlus's epJSON generator emits from 26.2 on. The seventeen older bundled schemas carry
no tag at all. Field names are stable across versions (97 to 98% overlap), so the 26.2 tags carry back
to older schemas by ``(type, field)``, and the field-name rule ``node(_or_nodelist)?_names?$``
catches the fields the tags miss, in every version (research R-03).

The table is the union, over every bundled schema, of the fields that are tagged in 26.2 or match
the rule, minus the "nodes" that are not fluid nodes: AirflowNetwork and RoomAir nodes, room-air
model nodes and electric circuit nodes.

A generated table is reviewable in a diff, which a table computed at import time is not, and the
older schemas have nothing to compute it from. ``make check-node-fields`` regenerates and diffs it.

Usage::

    python -m idfkit.codegen.generate_node_fields
"""

from __future__ import annotations

import re
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any, Final, cast

from idfkit.schema import get_schema_manager, load_schema_json

_OUTPUT_PATH: Final = Path(__file__).resolve().parents[1] / "hvac" / "_node_fields.py"
_TAGGED_VERSION: Final = "V26-2-0"
_SCHEMA_FILE: Final = "Energy+.schema.epJSON.gz"

NODE_FIELD_RULE: Final = re.compile(r"node(_or_nodelist)?_names?$")
"""The field-name rule that marks a node field in every version."""

_EXCLUDED_TYPE_PREFIXES: Final = ("AirflowNetwork", "RoomAir")
"""Types whose "nodes" are airflow-network or room-air nodes, not HVAC fluid nodes."""

_EXCLUDED_FIELD_RULE: Final = re.compile(r"(^|_)electric_circuit_node_name$|room_air_model_node_name$")
"""Fields that are named like nodes but are electric circuit or room-air model nodes."""


def _iter_fields(type_schema: Mapping[str, Any]) -> Iterator[tuple[bool, str, Mapping[str, Any]]]:
    """Yield ``(is_extensible, field_name, field_schema)`` for every field of one object type."""
    pattern = cast("Mapping[str, Any] | None", type_schema.get("patternProperties"))
    if pattern:
        inner = cast("Mapping[str, Any]", next(iter(pattern.values())))
        props = cast("Mapping[str, Any]", inner.get("properties", {}))
    else:
        props = cast("Mapping[str, Any]", type_schema.get("properties", {}))
    for name, field in props.items():
        field_map = cast("Mapping[str, Any]", field)
        items = field_map.get("items")
        if field_map.get("type") == "array" and isinstance(items, dict):
            sub = cast("Mapping[str, Any]", cast("Mapping[str, Any]", items).get("properties", {}))
            for sub_name, sub_field in sub.items():
                yield True, sub_name, cast("Mapping[str, Any]", sub_field)
        else:
            yield False, name, field_map


def _load_properties(version_dir: Path) -> Mapping[str, Any]:
    data = load_schema_json(version_dir / _SCHEMA_FILE)
    return cast("Mapping[str, Any]", data["properties"])


def _is_excluded(object_type: str, field: str) -> bool:
    return object_type.startswith(_EXCLUDED_TYPE_PREFIXES) or bool(_EXCLUDED_FIELD_RULE.search(field))


def collect_node_fields(bundled_dir: Path) -> dict[str, tuple[tuple[str, ...], tuple[str, ...]]]:
    """Return ``object type -> (top-level node fields, extensible node fields)`` over every bundled schema.

    Field order follows the schema of the latest version that has the field, so the table reads in
    the order the IDF editor shows the fields.
    """
    tagged_props = _load_properties(bundled_dir / _TAGGED_VERSION)
    tagged = {
        (object_type, field)
        for object_type, type_schema in tagged_props.items()
        for _, field, field_schema in _iter_fields(cast("Mapping[str, Any]", type_schema))
        if field_schema.get("data_type") == "node"
    }

    # Latest version first, so a field's position comes from the newest schema that has it.
    version_dirs = sorted(
        (d for d in bundled_dir.iterdir() if d.is_dir() and (d / _SCHEMA_FILE).exists()),
        key=lambda d: tuple(int(p) for p in d.name[1:].split("-")),
        reverse=True,
    )
    top: dict[str, list[str]] = {}
    ext: dict[str, list[str]] = {}
    for version_dir in version_dirs:
        for object_type, type_schema in _load_properties(version_dir).items():
            for is_ext, field, _ in _iter_fields(cast("Mapping[str, Any]", type_schema)):
                if _is_excluded(object_type, field):
                    continue
                if (object_type, field) not in tagged and not NODE_FIELD_RULE.search(field):
                    continue
                bucket = ext if is_ext else top
                fields = bucket.setdefault(object_type, [])
                if field not in fields:
                    fields.append(field)
    return {
        object_type: (tuple(top.get(object_type, ())), tuple(ext.get(object_type, ())))
        for object_type in sorted(set(top) | set(ext))
    }


_HEADER: Final = '''"""Auto-generated table of fluid node fields per object type.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_node_fields

Each entry maps an object type to ``(top-level node fields, extensible node fields)``: the union,
over every bundled schema, of the fields tagged ``"data_type": "node"`` in the 26.2 schema or named
like ``node(_or_nodelist)?_names?``, without AirflowNetwork, RoomAir, room-air model and electric
circuit nodes. A field listed here may be absent from an older schema; callers intersect with the
document's own schema.
"""

from __future__ import annotations

from typing import Final

NODE_FIELDS: Final[dict[str, tuple[tuple[str, ...], tuple[str, ...]]]] = {
'''


def render(table: Mapping[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> str:
    """Render the table as the module source written to ``_node_fields.py``."""
    lines = [_HEADER]
    for object_type, (top, ext) in table.items():
        lines.append(f"    {_quote(object_type)}: (\n")
        lines.append(f"        {_render_tuple(top)},\n")
        lines.append(f"        {_render_tuple(ext)},\n")
        lines.append("    ),\n")
    lines.append("}\n")
    return "".join(lines)


def _render_tuple(items: tuple[str, ...]) -> str:
    # One item per line with a trailing comma, so `ruff format` leaves the file as written.
    if not items:
        return "()"
    if len(items) == 1:
        return f"({_quote(items[0])},)"
    body = "".join(f"            {_quote(i)},\n" for i in items)
    return f"(\n{body}        )"


def _quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    """Regenerate ``src/idfkit/hvac/_node_fields.py`` from the bundled schemas."""
    table = collect_node_fields(get_schema_manager().bundled_dir)
    _OUTPUT_PATH.write_text(render(table), encoding="utf-8")
    fields = sum(len(top) + len(ext) for top, ext in table.values())
    print(f"Wrote {_OUTPUT_PATH.name}: {len(table)} object types, {fields} node fields")


if __name__ == "__main__":
    main()
