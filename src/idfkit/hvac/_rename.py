"""Rename one node everywhere it is used (internal; called by :meth:`IDFDocument.rename_node`)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from idfkit._graph_common import ObjectKey
from idfkit.hvac.topology import HVACTopology
from idfkit.hvac.types import NodeRenameResult

if TYPE_CHECKING:
    from idfkit.document import IDFDocument
    from idfkit.objects import IDFObject

_Write = tuple["IDFObject", Callable[[], None], Callable[[], None]]
"""``(object, apply, undo)``."""

_NOT_FIELDS = frozenset({"CONNECTOR:SPLITTER", "CONNECTOR:MIXER"})
"""Types the view gives node uses that no field of theirs spells: they name branches."""


def _matches(value: object, old: str) -> bool:
    return isinstance(value, str) and value.upper() == old


def _field_writes(doc: IDFDocument, obj: IDFObject, field: str, old: str, new: str) -> list[_Write]:
    """The writes that point one node field of *obj* (top level or ``group.key``) at *new*."""
    if "." not in field:
        original = obj.data.get(field)
        if not _matches(original, old):
            return []
        if field == "name":  # an OutdoorAir:Node declares its node by its own name
            obj_type, spelled = obj.obj_type, str(original)
            return [
                (obj, lambda: doc.rename(obj_type, spelled, new), lambda: doc.rename(obj_type, new, spelled)),
            ]

        def put(value: object) -> Callable[[], None]:
            return lambda: obj.__setitem__(field, value)

        return [(obj, put(new), put(original))]
    wrapper, key = field.split(".", 1)
    groups: Any = getattr(obj, wrapper)
    writes: list[_Write] = []
    for index, item in enumerate(obj.extensible_items(wrapper)):
        original = item.get(key)
        if _matches(original, old):
            group = groups[index]

            def put_group(value: object, group: Any = group) -> Callable[[], None]:
                return lambda: setattr(group, key, value)

            writes.append((obj, put_group(new), put_group(original)))
    return writes


def _check_new(topo: HVACTopology, old: str, new: str) -> None:
    if not new.strip():
        msg = "The new node name must not be empty"
        raise ValueError(msg)
    if new.upper() == old.upper():
        msg = f"The new node name {new!r} is the old one"
        raise ValueError(msg)
    if new.upper() in {n.upper() for n in topo.nodes()}:
        msg = f"{new!r} is already a node in the model; rename_node never merges two nodes"
        raise ValueError(msg)


def _apply(writes: list[_Write]) -> None:
    """Apply every write, or none: on a failure the writes made are undone and the error raised."""
    applied: list[_Write] = []
    try:
        for write in writes:
            write[1]()
            applied.append(write)
    except BaseException:
        for _, _, undo in reversed(applied):
            undo()
        raise


def rename_node(doc: IDFDocument, old: str, new: str) -> NodeRenameResult:
    """See :meth:`IDFDocument.rename_node`."""
    topo = HVACTopology.from_document(doc)
    uses = topo._node_fields(old)  # pyright: ignore[reportPrivateUsage]  # KeyError when no field names it
    spelled = uses[0][1].node if uses else old
    _check_new(topo, old, new)
    key_old = old.upper()
    writes: list[_Write] = []
    done: set[tuple[int, str]] = set()
    keys: dict[int, ObjectKey] = {}
    for obj, use in uses:
        keys.setdefault(id(obj), use.object)
        if use.via_nodelist is not None or obj.obj_type.upper() in _NOT_FIELDS:
            continue
        if (id(obj), use.field) in done:
            continue
        done.add((id(obj), use.field))
        writes.extend(_field_writes(doc, obj, use.field, key_old, new))
    if "NodeList" in doc:
        for node_list in doc.get_collection("NodeList"):
            writes.extend(_field_writes(doc, node_list, "nodes.node_name", key_old, new))
    _apply(writes)
    objects = tuple(dict.fromkeys(keys.get(id(o)) or ObjectKey(o.obj_type, o.name) for o, _, _ in writes))
    return NodeRenameResult(old=spelled, new=new, fields_updated=len(writes), objects=objects)
