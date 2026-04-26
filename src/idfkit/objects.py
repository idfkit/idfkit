"""
Core object classes for IDF representation.

IDFObject: Thin wrapper around a dict with attribute access.
IDFCollection: Indexed collection of IDFObjects with O(1) lookup.
"""

from __future__ import annotations

import re
import warnings
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

from ._compat_object import EppyObjectMixin
from .exceptions import InvalidFieldError

__all__ = [
    "ExtensibleGroup",
    "ExtensibleList",
    "IDFCollection",
    "IDFObject",
    "parse_extensible_index",
    "to_python_name",
]

if TYPE_CHECKING:
    from .document import IDFDocument

# Field name conversion patterns
_FIELD_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9]+")

# Matches a numbered extensible field like "vertex_1_x_coordinate" -> "vertex_x_coordinate"
_EXTENSIBLE_NUMBER_PATTERN = re.compile(r"^(.+?)_(\d+)_(.+)$")


def parse_extensible_index(field_name: str, extensibles: frozenset[str]) -> tuple[str | None, int]:
    """Extract the base name and 1-based group index from an extensible field name.

    Handles both naming conventions:
    - ``field_1`` / ``field_2`` (user style, base ``field``)
    - ``vertex_1_x_coordinate`` / ``vertex_2_x_coordinate`` (user style)
    - ``field`` / ``field_2`` (schema style, first group has no number)
    - ``vertex_x_coordinate`` / ``vertex_x_coordinate_2`` (schema style)

    Returns ``(base_name, group_index)`` or ``(None, 0)`` if not extensible.
    """
    if field_name in extensibles:
        return field_name, 1

    last_underscore = field_name.rfind("_")
    if last_underscore > 0 and field_name[last_underscore + 1 :].isdigit():
        base = field_name[:last_underscore]
        num = int(field_name[last_underscore + 1 :])
        if base in extensibles:
            return base, num

    m = _EXTENSIBLE_NUMBER_PATTERN.match(field_name)
    if m:
        base = f"{m.group(1)}_{m.group(3)}"
        if base in extensibles:
            return base, int(m.group(2))

    return None, 0


class ExtensibleGroup:
    """One row of an extensible array (e.g. a single vertex inside ``vertices``).

    Holds a back-reference to the owning :class:`IDFObject` and the group's
    1-based index so attribute reads/writes route into
    ``obj.data[wrapper_key][group_index - 1]``. Equality compares against
    plain dicts; ``as_dict()`` snapshots the underlying values.
    """

    __slots__ = ("_group_index", "_inner_names", "_owner", "_wrapper_key")

    _owner: IDFObject
    _wrapper_key: str
    _group_index: int
    _inner_names: tuple[str, ...]

    def __init__(self, owner: IDFObject, wrapper_key: str, group_index: int, inner_names: tuple[str, ...]) -> None:
        object.__setattr__(self, "_owner", owner)
        object.__setattr__(self, "_wrapper_key", wrapper_key)
        object.__setattr__(self, "_group_index", group_index)
        object.__setattr__(self, "_inner_names", inner_names)

    @property
    def group_index(self) -> int:
        """1-based position of this group within the wrapper array."""
        return self._group_index

    def _slot(self) -> dict[str, Any]:
        """Return the underlying dict for this group, creating it if necessary."""
        items = self._owner.data.setdefault(self._wrapper_key, [])
        while len(items) < self._group_index:
            items.append({})
        return cast("dict[str, Any]", items[self._group_index - 1])

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name not in self._inner_names:
            raise AttributeError(  # noqa: TRY003
                f"{name!r} is not an extensible field of {self._owner.obj_type}.{self._wrapper_key}"
            )
        items = self._owner.data.get(self._wrapper_key)
        if not items or self._group_index > len(items):
            return None
        return cast("dict[str, Any]", items[self._group_index - 1]).get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        if name not in self._inner_names:
            raise AttributeError(  # noqa: TRY003
                f"{name!r} is not an extensible field of {self._owner.obj_type}.{self._wrapper_key}"
            )
        self._slot()[name] = value
        self._owner._bump_version()  # pyright: ignore[reportPrivateUsage]

    def __getitem__(self, key: str) -> Any:
        return self.__getattr__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__setattr__(key, value)

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and key in self._inner_names

    def __iter__(self) -> Iterator[str]:
        return iter(self._inner_names)

    def keys(self) -> tuple[str, ...]:
        """Return the inner field names defined by the schema for this group."""
        return self._inner_names

    def values(self) -> list[Any]:
        """Return the values for each inner field, in schema order."""
        return [self.__getattr__(n) for n in self._inner_names]

    def items(self) -> list[tuple[str, Any]]:
        """Return ``(field_name, value)`` pairs for the inner fields."""
        return [(n, self.__getattr__(n)) for n in self._inner_names]

    def as_dict(self) -> dict[str, Any]:
        """Snapshot the group as a plain dict (does not track future mutations)."""
        items = self._owner.data.get(self._wrapper_key)
        if not items or self._group_index > len(items):
            return {}
        return dict(cast("dict[str, Any]", items[self._group_index - 1]))

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Update one or more inner fields atomically (matches dict.update)."""
        if len(args) > 1:
            raise TypeError(f"update expected at most 1 positional argument, got {len(args)}")  # noqa: TRY003
        merged: dict[str, Any] = {}
        if args:
            src = args[0]
            if isinstance(src, dict):
                merged.update(cast("dict[str, Any]", src))
            else:
                for k, v in src:
                    merged[k] = v
        merged.update(kwargs)
        for k in merged:
            if k not in self._inner_names:
                raise AttributeError(  # noqa: TRY003
                    f"{k!r} is not an extensible field of {self._owner.obj_type}.{self._wrapper_key}"
                )
        slot = self._slot()
        slot.update(merged)
        self._owner._bump_version()  # pyright: ignore[reportPrivateUsage]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ExtensibleGroup):
            return self.as_dict() == other.as_dict()
        if isinstance(other, dict):
            other_dict = cast("dict[str, Any]", other)
            return self.as_dict() == other_dict
        return NotImplemented

    def __hash__(self) -> int:
        return id(self)

    def __repr__(self) -> str:
        return (
            f"ExtensibleGroup({self._owner.obj_type}.{self._wrapper_key}[{self._group_index - 1}], {self.as_dict()!r})"
        )


GroupT_co = TypeVar("GroupT_co", bound=ExtensibleGroup, covariant=True)


class ExtensibleList(Generic[GroupT_co]):
    """List-like view over the canonical wrapper array ``obj.data[wrapper_key]``.

    Holds a reference to the owning :class:`IDFObject` and the wrapper key;
    indexing, iteration, append, insert, delete, pop, clear, extend, equality,
    and bulk replace all operate on the canonical list of dicts. Items are
    yielded as :class:`ExtensibleGroup` instances bound to the underlying dicts.

    The ``Generic[GroupT_co]`` parameter lets generated stubs narrow the item
    type per object — e.g. ``surface.vertices`` is typed as
    ``ExtensibleList[BuildingSurfaceVertex]`` so IDEs autocomplete the
    inner ``vertex_x_coordinate`` etc. on each indexed item.

    Mutations bump the owner's mutation version. Reference-graph notification
    for fields inside extensible groups is handled separately by the document
    when it walks ``ref_fields`` recursively.
    """

    __slots__ = ("_inner_names", "_owner", "_wrapper_key")

    _owner: IDFObject
    _wrapper_key: str
    _inner_names: tuple[str, ...]

    def __init__(self, owner: IDFObject, wrapper_key: str, inner_names: tuple[str, ...]) -> None:
        self._owner = owner
        self._wrapper_key = wrapper_key
        self._inner_names = inner_names

    def _items_or_empty(self) -> list[dict[str, Any]]:
        """Return the underlying canonical list (empty list if absent)."""
        return cast("list[dict[str, Any]]", self._owner.data.get(self._wrapper_key, []))

    def _items_for_write(self) -> list[dict[str, Any]]:
        """Return the underlying canonical list, creating it if absent."""
        return cast("list[dict[str, Any]]", self._owner.data.setdefault(self._wrapper_key, []))

    def __len__(self) -> int:
        return len(self._items_or_empty())

    def _resolve_index(self, index: int) -> int:
        n = len(self)
        if index < 0:
            index += n
        if index < 0 or index >= n:
            raise IndexError(f"{self._wrapper_key} index {index} out of range (length {n})")  # noqa: TRY003
        return index

    def __getitem__(self, index: int) -> GroupT_co:
        idx = self._resolve_index(index)
        return cast("GroupT_co", ExtensibleGroup(self._owner, self._wrapper_key, idx + 1, self._inner_names))

    def __iter__(self) -> Iterator[GroupT_co]:
        for i in range(len(self)):
            yield cast(
                "GroupT_co",
                ExtensibleGroup(self._owner, self._wrapper_key, i + 1, self._inner_names),
            )

    def __delitem__(self, index: int) -> None:
        idx = self._resolve_index(index)
        items = self._items_for_write()
        del items[idx]
        if not items:
            self._owner.data.pop(self._wrapper_key, None)
        self._owner._bump_version()  # pyright: ignore[reportPrivateUsage]

    def _coerce_item(self, item: Any, kwargs: dict[str, Any]) -> dict[str, Any]:
        if item is not None and kwargs:
            raise TypeError("pass either a dict/group OR keyword arguments, not both")  # noqa: TRY003
        if isinstance(item, ExtensibleGroup):
            return item.as_dict()
        if isinstance(item, dict):
            return dict(cast("dict[str, Any]", item))
        if item is None:
            return dict(kwargs)
        raise TypeError(f"expected dict, ExtensibleGroup, or kwargs; got {type(item).__name__}")  # noqa: TRY003

    def _validate_inner(self, item: dict[str, Any]) -> None:
        unknown = [k for k in item if k not in self._inner_names]
        if unknown:
            raise ValueError(  # noqa: TRY003
                f"{self._owner.obj_type}.{self._wrapper_key}: unknown extensible field(s) "
                f"{unknown!r}; expected subset of {list(self._inner_names)}"
            )

    def append(self, item: Any = None, /, **kwargs: Any) -> GroupT_co:
        """Append a new group. Accepts a dict, another :class:`ExtensibleGroup`, or kwargs."""
        merged = self._coerce_item(item, kwargs)
        self._validate_inner(merged)
        items = self._items_for_write()
        items.append(merged)
        self._owner._bump_version()  # pyright: ignore[reportPrivateUsage]
        return cast("GroupT_co", ExtensibleGroup(self._owner, self._wrapper_key, len(items), self._inner_names))

    def insert(self, index: int, item: Any = None, /, **kwargs: Any) -> GroupT_co:
        """Insert a new group at *index*. Existing groups at and after *index* shift up."""
        merged = self._coerce_item(item, kwargs)
        self._validate_inner(merged)
        items = self._items_for_write()
        n = len(items)
        if index < 0:
            index = max(0, n + index)
        index = min(index, n)
        items.insert(index, merged)
        self._owner._bump_version()  # pyright: ignore[reportPrivateUsage]
        return cast(
            "GroupT_co",
            ExtensibleGroup(self._owner, self._wrapper_key, index + 1, self._inner_names),
        )

    def extend(self, items: Any) -> None:
        """Append every group from *items* (any iterable of dicts or groups)."""
        for it in items:
            self.append(it)

    def clear(self) -> None:
        """Remove all groups."""
        if self._wrapper_key in self._owner.data:
            del self._owner.data[self._wrapper_key]
            self._owner._bump_version()  # pyright: ignore[reportPrivateUsage]

    def pop(self, index: int = -1) -> dict[str, Any]:
        """Remove and return the group at *index* as a plain dict."""
        idx = self._resolve_index(index)
        items = self._items_for_write()
        snapshot = dict(items[idx])
        del items[idx]
        if not items:
            self._owner.data.pop(self._wrapper_key, None)
        self._owner._bump_version()  # pyright: ignore[reportPrivateUsage]
        return snapshot

    def replace(self, items: list[Any]) -> None:
        """Replace the entire wrapper contents with *items* (each a dict or group)."""
        coerced = [self._coerce_item(it, {}) for it in items]
        for it in coerced:
            self._validate_inner(it)
        self.clear()
        for it in coerced:
            self.append(it)

    def as_list(self) -> list[dict[str, Any]]:
        """Snapshot the wrapper as a plain list of plain dicts."""
        return [g.as_dict() for g in self]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ExtensibleList):
            return self.as_list() == other.as_list()
        if isinstance(other, list):
            return self.as_list() == [
                (g.as_dict() if isinstance(g, ExtensibleGroup) else g) for g in cast("list[Any]", other)
            ]
        return NotImplemented

    def __hash__(self) -> int:
        return id(self)

    def __repr__(self) -> str:
        return f"ExtensibleList({self._owner.obj_type}.{self._wrapper_key}, {self.as_list()!r})"


def to_python_name(idf_name: str) -> str:
    """Convert IDF field name to Python-friendly name.

    'Direction of Relative North' -> 'direction_of_relative_north'
    'X Origin' -> 'x_origin'
    """
    return _FIELD_NAME_PATTERN.sub("_", idf_name.lower()).strip("_")


def to_idf_name(python_name: str) -> str:
    """Convert Python name back to IDF-style name.

    'direction_of_relative_north' -> 'Direction of Relative North'
    """
    return " ".join(word.capitalize() for word in python_name.split("_"))


class IDFObject(EppyObjectMixin):
    """
    Lightweight wrapper around a dict representing an EnergyPlus object.

    Uses __slots__ for memory efficiency - each object is ~200 bytes.
    Provides attribute access to fields via __getattr__/__setattr__.

    Examples:
        Create a rigid insulation material and access its properties:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> insulation = model.add("Material", "XPS_50mm",
        ...     roughness="Rough", thickness=0.05,
        ...     conductivity=0.034, density=35.0, specific_heat=1400.0)

        Read thermal properties as attributes:

        >>> insulation.conductivity
        0.034
        >>> insulation.thickness
        0.05

        Modify for parametric analysis (double the insulation):

        >>> insulation.thickness = 0.1
        >>> insulation.thickness
        0.1

        Export to a dictionary for use with external tools:

        >>> d = insulation.to_dict()
        >>> d["conductivity"]
        0.034

    Attributes:
        _type: The IDF object type (e.g., "Zone", "Material")
        _name: The object's name (first field)
        _data: Dict of field_name -> value
        _schema: Optional schema dict for validation
        _document: Reference to parent document (for reference resolution)
        _field_order: Ordered list of field names from schema
    """

    __slots__ = (
        "__weakref__",
        "_data",
        "_document",
        "_ext_inner_names",
        "_extensibles",
        "_field_order",
        "_name",
        "_ref_fields",
        "_schema",
        "_source_text",
        "_type",
        "_version",
        "_wrapper_key",
    )

    _type: str
    _name: str
    _data: dict[str, Any]
    _schema: dict[str, Any] | None
    _document: IDFDocument[bool] | None
    _field_order: list[str] | None
    _ref_fields: frozenset[str] | None
    _source_text: str | None
    _wrapper_key: str | None
    _ext_inner_names: tuple[str, ...]

    def __init__(
        self,
        obj_type: str,
        name: str,
        data: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
        document: IDFDocument[bool] | None = None,
        field_order: list[str] | None = None,
        ref_fields: frozenset[str] | None = None,
        source_text: str | None = None,
        extensibles: frozenset[str] | None = None,
        wrapper_key: str | None = None,
        ext_inner_names: tuple[str, ...] = (),
    ) -> None:
        object.__setattr__(self, "_type", obj_type)
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_data", data if data is not None else {})
        object.__setattr__(self, "_schema", schema)
        object.__setattr__(self, "_document", document)
        object.__setattr__(self, "_extensibles", extensibles or frozenset())
        object.__setattr__(self, "_field_order", field_order)
        object.__setattr__(self, "_ref_fields", ref_fields)
        object.__setattr__(self, "_source_text", source_text)
        object.__setattr__(self, "_version", 0)
        object.__setattr__(self, "_wrapper_key", wrapper_key)
        object.__setattr__(self, "_ext_inner_names", ext_inner_names)

    @property
    def obj_type(self) -> str:
        """The IDF object type (e.g., 'Zone', 'Material')."""
        return self._type

    @property
    def mutation_version(self) -> int:
        """Monotonically increasing counter bumped on every field write.

        Useful for caches that need to detect whether an object has been
        modified since a cached value was computed.
        """
        return self._version

    @property
    def data(self) -> dict[str, Any]:
        """The field data dictionary."""
        return self._data

    @property
    def schema_dict(self) -> dict[str, Any] | None:
        """The schema dict for this object type."""
        return self._schema

    @property
    def source_text(self) -> str | None:
        """Original source text from parsing, or ``None`` if the object was mutated or created programmatically."""
        return self._source_text

    @property
    def field_order(self) -> list[str] | None:
        """Ordered list of field names from schema."""
        return self._field_order

    def extensible_items(self, wrapper_key: str | None = None) -> list[dict[str, Any]]:
        """Return the canonical list of extensible items (empty if absent).

        For an extensible type (e.g. ``BuildingSurface:Detailed``) this
        returns ``obj.data[wrapper_key]`` typed as ``list[dict[str, Any]]``.
        If *wrapper_key* is omitted, the schema's wrapper key is used.
        Returns an empty list if the wrapper isn't present or the type
        isn't extensible — never ``None``.
        """
        key = wrapper_key if wrapper_key is not None else self._wrapper_key
        if key is None:
            return []
        items = self._data.get(key)
        if not isinstance(items, list):
            return []
        return cast("list[dict[str, Any]]", items)

    def _is_known_field(self, python_key: str, field_order: list[str]) -> bool:
        """Check whether *python_key* is a valid field name for this object.

        Returns ``True`` if the key is in *field_order* OR if it is a
        legacy flat-extensible alias (``vertex_3_x_coordinate``,
        ``vertex_x_coordinate_3``, ``field_42``) for one of this type's
        extensible fields.
        """
        if python_key in field_order:
            return True
        extensibles = self._extensibles
        if not extensibles:
            return False
        base, _ = parse_extensible_index(python_key, extensibles)
        return base is not None

    @property
    def name(self) -> str:
        """The object's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the object's name."""
        self._set_name(value)

    def __getattr__(self, key: str) -> Any:  # noqa: C901
        """Get field value by attribute name.

        When the parent document has ``strict=True``, accessing a field
        name that is neither present in the data dict nor recognised by
        the schema raises ``AttributeError`` instead of returning
        ``None``.  This catches typos during migration.
        """
        if key.startswith("_"):
            raise AttributeError(key)

        # Canonical extensible-wrapper access (e.g. surface.vertices,
        # schedule.data, branchlist.branches). Returns a list-like view
        # bound to the schema's wrapper key.
        wrapper_key = object.__getattribute__(self, "_wrapper_key")
        if wrapper_key is not None and (key == wrapper_key or to_python_name(key) == wrapper_key):
            inner = object.__getattribute__(self, "_ext_inner_names")
            return ExtensibleList[ExtensibleGroup](self, wrapper_key, inner)

        # Try exact match first
        data = object.__getattribute__(self, "_data")
        if key in data:
            return data[key]

        # Try lowercase version
        key_lower = key.lower()
        if key_lower in data:
            return data[key_lower]

        # Try python name conversion
        python_key = to_python_name(key)
        if python_key in data:
            return data[python_key]

        # Eppy-compat: legacy flat extensible field access
        # (vertex_3_x_coordinate, vertex_x_coordinate_3, time_2, ...).
        # Translates to the canonical wrapper position with a deprecation
        # warning. Scheduled for removal in a future release.
        extensibles = object.__getattribute__(self, "_extensibles")
        if extensibles:
            base, group_idx = parse_extensible_index(python_key, extensibles)
            if base is not None:
                wrapper_key = object.__getattribute__(self, "_wrapper_key")
                if wrapper_key is not None:
                    items_any: Any = data.get(wrapper_key)
                    if isinstance(items_any, list):
                        items_typed = cast("list[dict[str, Any]]", items_any)
                        if 0 < group_idx <= len(items_typed):
                            warnings.warn(
                                f"{key!r} flat-extensible access is deprecated; "
                                f"use {self._type}.{wrapper_key}[{group_idx - 1}].{base}",
                                DeprecationWarning,
                                stacklevel=2,
                            )
                            return items_typed[group_idx - 1].get(base)

        # Field not found — check strict mode
        doc = object.__getattribute__(self, "_document")
        if doc is not None and getattr(doc, "_strict", False):
            # In strict mode, only allow known schema fields
            field_order = object.__getattribute__(self, "_field_order")
            if field_order is not None and not self._is_known_field(python_key, field_order):
                obj_type = object.__getattribute__(self, "_type")
                ver: tuple[int, int, int] | None = object.__getattribute__(doc, "version")
                raise InvalidFieldError(
                    obj_type,
                    key,
                    available_fields=list(field_order),
                    version=ver,
                    extensible_fields=object.__getattribute__(self, "_extensibles"),
                )

        # Default: return None (eppy behaviour)
        return None

    def __setattr__(self, key: str, value: Any) -> None:
        """Set field value by attribute name.

        Extensible field names are normalized to the epJSON schema convention
        (``field``, ``field_2``; ``vertex_x_coordinate``, ``vertex_x_coordinate_2``).
        """
        if key.startswith("_"):
            object.__setattr__(self, key, value)
            return
        if key.lower() == "name":
            self._set_name(value)
            return
        # Canonical extensible-wrapper bulk replace (e.g. surface.vertices = [...]).
        wrapper_key = self._wrapper_key
        if wrapper_key is not None and (key == wrapper_key or to_python_name(key) == wrapper_key):
            if not isinstance(value, list):
                raise TypeError(  # noqa: TRY003
                    f"{self._type}.{wrapper_key} must be a list of dicts; got {type(value).__name__}"
                )
            view = ExtensibleList[ExtensibleGroup](self, wrapper_key, self._ext_inner_names)
            view.replace(cast("list[Any]", value))
            return
        # Normalize key to python style
        python_key = to_python_name(key)

        # Eppy-compat: legacy flat extensible field write
        # (surface.vertex_3_x_coordinate = 5.0). Routes to the canonical
        # wrapper slot with a deprecation warning.
        if self._extensibles:
            base, group_idx = parse_extensible_index(python_key, self._extensibles)
            if base is not None and self._wrapper_key is not None:
                warnings.warn(
                    f"{key!r} flat-extensible assignment is deprecated; "
                    f"use {self._type}.{self._wrapper_key}[{group_idx - 1}].{base} = ...",
                    DeprecationWarning,
                    stacklevel=2,
                )
                items = self._data.setdefault(self._wrapper_key, [])
                while len(items) < group_idx:
                    items.append({})
                cast("list[dict[str, Any]]", items)[group_idx - 1][base] = value
                self._bump_version()
                return

        # Validate in strict mode
        doc = self._document
        if doc is not None and getattr(doc, "_strict", False):
            field_order = self._field_order
            if field_order is not None and not self._is_known_field(python_key, field_order):
                ver: tuple[int, int, int] | None = object.__getattribute__(doc, "version")
                raise InvalidFieldError(
                    self._type,
                    key,
                    available_fields=list(field_order),
                    version=ver,
                    extensible_fields=self._extensibles,
                )
        self._set_field(python_key, value)

    def __getitem__(self, key: str | int) -> Any:
        """Get field value by name or index.

        For the schema's extensible wrapper key (``"vertices"``, ``"data"``,
        ``"branches"``, …), returns an :class:`ExtensibleList` view of the
        wrapper. This is the only access path for types whose wrapper key
        collides with the ``data`` property (Schedule:Day:Interval,
        Schedule:Compact); for other types it is equivalent to attribute
        access.
        """
        if isinstance(key, int):
            if key == 0:
                return self._name
            if self._field_order and 0 < key <= len(self._field_order):
                field_name = self._field_order[key - 1]
                return self._data.get(field_name)
            raise IndexError(f"Field index {key} out of range")  # noqa: TRY003
        if self._wrapper_key is not None and key == self._wrapper_key:
            return ExtensibleList[ExtensibleGroup](self, self._wrapper_key, self._ext_inner_names)
        return getattr(self, key)

    def __setitem__(self, key: str | int, value: Any) -> None:
        """Set field value by name or index.

        For the schema's extensible wrapper key, *value* must be a list of
        dicts (or :class:`ExtensibleGroup` instances) and replaces the entire
        wrapper contents.
        """
        if isinstance(key, int):
            if key == 0:
                self._set_name(value)
            elif self._field_order and 0 < key <= len(self._field_order):
                field_name = self._field_order[key - 1]
                self._set_field(field_name, value)
            else:
                raise IndexError(f"Field index {key} out of range")  # noqa: TRY003
            return
        if self._wrapper_key is not None and key == self._wrapper_key:
            if not isinstance(value, list):
                raise TypeError(  # noqa: TRY003
                    f"{self._type}[{key!r}] must be a list of dicts; got {type(value).__name__}"
                )
            ExtensibleList[ExtensibleGroup](self, self._wrapper_key, self._ext_inner_names).replace(
                cast("list[Any]", value)
            )
            return
        setattr(self, key, value)

    def __repr__(self) -> str:
        return f"{self._type}('{self._name}')"

    def __str__(self) -> str:
        return f"{self._type}: {self._name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IDFObject):
            return NotImplemented
        return self._type == other._type and self._name == other._name and self._data == other._data

    def __hash__(self) -> int:
        return id(self)

    def _set_name(self, value: str) -> None:
        """Centralized name-change logic with document notification."""
        old = self._name
        if old == value:
            return
        object.__setattr__(self, "_name", value)
        object.__setattr__(self, "_version", self._version + 1)
        object.__setattr__(self, "_source_text", None)
        doc = self._document
        if doc is not None:
            doc.notify_name_change(self, old, value)

    def _bump_version(self) -> None:
        """Mark the object as mutated.

        Bumps :attr:`mutation_version` and invalidates the cached IDF source
        text so the writer regenerates output for this object. Used by
        :class:`ExtensibleList`/:class:`ExtensibleGroup` after mutating the
        canonical wrapper array directly (without going through
        :meth:`_set_field`).
        """
        object.__setattr__(self, "_version", self._version + 1)
        object.__setattr__(self, "_source_text", None)

    def _set_field(self, python_key: str, value: Any) -> None:
        """Centralized data-field write with reference graph notification."""
        doc = self._document
        ref_fields = self._ref_fields
        if doc is not None and ref_fields is not None and python_key in ref_fields:
            old = self._data.get(python_key)
            self._data[python_key] = value
            if old != value:
                doc.notify_reference_change(self, python_key, old, value)
        else:
            self._data[python_key] = value

        object.__setattr__(self, "_version", self._version + 1)
        object.__setattr__(self, "_source_text", None)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Useful for serializing EnergyPlus objects to JSON, CSV, or
        DataFrames for post-processing.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> mat = model.add("Material", "Concrete_200mm",
            ...     roughness="MediumRough", thickness=0.2,
            ...     conductivity=1.4, density=2240.0, specific_heat=900.0)
            >>> d = mat.to_dict()
            >>> d["name"], d["thickness"], d["conductivity"]
            ('Concrete_200mm', 0.2, 1.4)
        """
        return {"name": self._name, **self._data}

    def get(self, key: str, default: Any = None) -> Any:
        """Get field value with default.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> mat = model.add("Material", "Concrete_200mm",
            ...     roughness="MediumRough", thickness=0.2,
            ...     conductivity=1.4, density=2240.0, specific_heat=900.0)
            >>> mat.get("conductivity")
            1.4
            >>> mat.get("thermal_absorptance", 0.9)
            0.9
        """
        value = getattr(self, key)
        return value if value is not None else default

    def copy(self) -> IDFObject:
        """Create a copy of this object."""
        return IDFObject(
            obj_type=self._type,
            name=self._name,
            data=dict(self._data),
            schema=self._schema,
            document=None,  # Don't copy document reference
            field_order=list(self._field_order) if self._field_order is not None else None,
            ref_fields=self._ref_fields,
            source_text=None,  # copy is a new object; don't carry over verbatim text
            extensibles=self._extensibles,
        )

    def __dir__(self) -> list[str]:
        """Return attributes for tab completion (includes schema field names)."""
        attrs = [
            "obj_type",
            "name",
            "data",
            "key",
            "Name",
            "fieldnames",
            "fieldvalues",
            "theidf",
            "schema_dict",
            "field_order",
            "to_dict",
            "get",
            "copy",
            "get_field_idd",
            "get_referenced_object",
            "getfieldidd",
            "getfieldidd_item",
            "getrange",
            "checkrange",
            "getreferingobjs",
        ]
        field_order = object.__getattribute__(self, "_field_order")
        if field_order:
            attrs.extend(field_order)
        else:
            data = object.__getattribute__(self, "_data")
            attrs.extend(data.keys())
        return attrs

    def _repr_svg_(self) -> str | None:
        """Return SVG representation for Jupyter/IPython display.

        Currently supports Construction objects, rendering a cross-section
        diagram showing layer sequence, thicknesses, and thermal properties.

        Returns:
            SVG string for Construction objects, None for other types.
        """
        if self._type != "Construction":
            return None

        if self._document is None:
            # Need document to resolve material references
            return None

        try:
            from .visualization.svg import construction_to_svg

            return construction_to_svg(self)
        except Exception:
            # Fail gracefully - fall back to text repr
            return None


_T = TypeVar("_T", bound=IDFObject)


class IDFCollection(Generic[_T]):
    """
    Indexed collection of IDFObjects with O(1) lookup by name.

    Provides list-like iteration and dict-like access by name.

    Examples:
        >>> from idfkit import new_document
        >>> model = new_document()
        >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
        Zone('Perimeter_ZN_1')
        >>> model.add("Zone", "Core_ZN")  # doctest: +ELLIPSIS
        Zone('Core_ZN')
        >>> zones = model["Zone"]
        >>> len(zones)
        2

        O(1) lookup by name:

        >>> zones["Perimeter_ZN_1"].name
        'Perimeter_ZN_1'
        >>> zones[0].name
        'Perimeter_ZN_1'

    Attributes:
        _type: The object type this collection holds
        _by_name: Dict mapping uppercase names to objects
        _items: Ordered list of objects
    """

    __slots__ = ("_by_name", "_items", "_type")

    _type: str
    _by_name: dict[str, _T]
    _items: list[_T]

    def __init__(self, obj_type: str) -> None:
        self._type = obj_type
        self._by_name: dict[str, _T] = {}
        self._items: list[_T] = []

    @property
    def obj_type(self) -> str:
        """The object type this collection holds."""
        return self._type

    @property
    def by_name(self) -> dict[str, _T]:
        """Dict mapping uppercase names to objects."""
        return self._by_name

    def add(self, obj: _T) -> _T:
        """
        Add an object to the collection.

        Args:
            obj: The IDFObject to add

        Returns:
            The added object

        Raises:
            DuplicateObjectError: If an object with the same name exists
        """
        from .exceptions import DuplicateObjectError

        key = obj.name.upper() if obj.name else ""
        if key and key in self._by_name:
            raise DuplicateObjectError(self._type, obj.name)

        if key:
            self._by_name[key] = obj
        self._items.append(obj)
        return obj

    def remove(self, obj: _T) -> None:
        """Remove an object from the collection."""
        key = obj.name.upper() if obj.name else ""
        if key in self._by_name:
            del self._by_name[key]
        if obj in self._items:
            self._items.remove(obj)

    def __getitem__(self, key: str | int) -> _T:
        """Get object by name or index."""
        if isinstance(key, int):
            return self._items[key]
        if not key:
            # Unnamed/singleton objects are not indexed in _by_name;
            # fall back to the first item in the ordered list.
            if self._items:
                return self._items[0]
            raise KeyError(f"No {self._type} with name '{key}'")  # noqa: TRY003
        result = self._by_name.get(key.upper())
        if result is None:
            raise KeyError(f"No {self._type} with name '{key}'")  # noqa: TRY003
        return result

    def __iter__(self) -> Iterator[_T]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, key: str | _T) -> bool:
        if isinstance(key, IDFObject):
            return key in self._items
        if not key:
            # Unnamed/singleton objects: check if any items exist
            return len(self._items) > 0
        return key.upper() in self._by_name

    def __bool__(self) -> bool:
        return len(self._items) > 0

    def __repr__(self) -> str:
        return f"IDFCollection({self._type}, count={len(self._items)})"

    def get(self, name: str, default: _T | None = None) -> _T | None:
        """Get object by name with default.

        For unnamed/singleton object types (e.g. SimulationControl), pass an
        empty string to retrieve the first object in the collection.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model["Zone"].get("Perimeter_ZN_1").name
            'Perimeter_ZN_1'
            >>> model["Zone"].get("NonExistent") is None
            True
            >>> model["SimulationControl"].get("") is not None
            True
        """
        if not name:
            return self._items[0] if self._items else default
        return self._by_name.get(name.upper(), default)

    def first(self) -> _T | None:
        """Get the first object or None.

        Examples:
            Quickly grab a singleton like Building or SimulationControl:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Core_ZN")  # doctest: +ELLIPSIS
            Zone('Core_ZN')
            >>> model["Zone"].first().name
            'Core_ZN'
            >>> model["Material"].first() is None
            True
        """
        return self._items[0] if self._items else None

    def to_list(self) -> list[_T]:
        """Convert to list.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model.add("Zone", "Core_ZN")  # doctest: +ELLIPSIS
            Zone('Core_ZN')
            >>> [z.name for z in model["Zone"].to_list()]
            ['Perimeter_ZN_1', 'Core_ZN']
        """
        return list(self._items)

    def to_dict(self) -> list[dict[str, Any]]:
        """Convert all objects to list of dicts (eppy compatibility).

        Useful for feeding zone/material data into pandas or other
        analysis tools.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1", x_origin=0.0)  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> dicts = model["Zone"].to_dict()
            >>> dicts[0]["name"]
            'Perimeter_ZN_1'
        """
        return [obj.to_dict() for obj in self._items]

    def filter(self, predicate: Callable[[_T], bool]) -> list[_T]:
        """Filter objects by predicate function.

        Examples:
            Find zones on upper floors of a multi-story building:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Ground_Office", z_origin=0.0)  # doctest: +ELLIPSIS
            Zone('Ground_Office')
            >>> model.add("Zone", "Floor2_Office", z_origin=3.5)  # doctest: +ELLIPSIS
            Zone('Floor2_Office')
            >>> upper = model["Zone"].filter(lambda z: (z.z_origin or 0) > 0)
            >>> [z.name for z in upper]
            ['Floor2_Office']
        """
        return [obj for obj in self._items if predicate(obj)]
