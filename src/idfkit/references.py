"""
Reference graph for tracking object dependencies.

Provides O(1) lookups for:
- What objects reference a given name?
- What names does an object reference?
- Validation of reference integrity
"""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, cast

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .objects import IDFObject


class ReferenceGraph:
    """
    Tracks object references for instant dependency queries.

    The graph maintains two indexes:
    - _referenced_by: name -> set of objects that reference it
    - _references: object -> set of names it references

    This enables O(1) lookups for common operations like:
    - Finding all surfaces in a zone
    - Finding all objects using a construction
    - Detecting dangling references

    The reference graph is automatically maintained by
    [IDFDocument][idfkit.document.IDFDocument] when objects are added,
    removed, or when reference fields are modified.

    Examples:
        The reference graph automatically tracks which objects point
        to which names.  For instance, when a surface references a
        zone, that link is available for instant queries:

        >>> from idfkit import new_document
        >>> model = new_document()
        >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
        Zone('Perimeter_ZN_1')
        >>> model.add("BuildingSurface:Detailed", "South_Wall",
        ...     surface_type="Wall", construction_name="",
        ...     zone_name="Perimeter_ZN_1",
        ...     outside_boundary_condition="Outdoors",
        ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
        ...     validate=False)  # doctest: +ELLIPSIS
        BuildingSurface:Detailed('South_Wall')
        >>> model.references.is_referenced("Perimeter_ZN_1")
        True
        >>> stats = model.references.stats()
        >>> stats["total_references"] >= 1
        True
    """

    __slots__ = ("_object_lists", "_referenced_by", "_references")

    def __init__(self) -> None:
        # An edge carries a group index alongside the field name. ``None`` means an ordinary
        # top-level field; an int is the 0-based repeat inside an extensible group, which is
        # what keeps two groups of the same object pointing at the same name from collapsing
        # into one edge. The public accessors drop the index again, so callers still see the
        # (object, field) and (name, field) pairs they always have.
        #
        # name (uppercase) -> set of (object, field_name, group_index) edges that reference it
        self._referenced_by: dict[str, set[tuple[IDFObject, str, int | None]]] = defaultdict(set)
        # object -> set of (name_uppercase, field_name, group_index) edges it references
        self._references: dict[IDFObject, set[tuple[str, str, int | None]]] = defaultdict(set)
        # object_list name -> set of object types that provide names for it
        self._object_lists: dict[str, set[str]] = defaultdict(set)

    def register_object_list(self, list_name: str, obj_type: str) -> None:
        """Register that an object type provides names for an object-list."""
        self._object_lists[list_name].add(obj_type)

    def register(self, obj: IDFObject, field_name: str, referenced_name: str, group_index: int | None = None) -> None:
        """
        Register that an object references another name.

        Args:
            obj: The object that contains the reference
            field_name: The field that contains the reference
            referenced_name: The name being referenced
            group_index: 0-based repeat index when *field_name* lives inside an
                extensible group; ``None`` for an ordinary top-level field.
        """
        if not referenced_name:
            return

        name_upper = referenced_name.upper()
        self._referenced_by[name_upper].add((obj, field_name, group_index))
        self._references[obj].add((name_upper, field_name, group_index))

    def reindex_extensible(self, obj: IDFObject, wrapper_key: str, ref_fields: frozenset[str]) -> None:
        """Rebuild the edges for *obj*'s extensible reference fields.

        Extensible data lives in ``obj.data[wrapper_key]`` as one dict per repeat group, and
        the reference fields inside those groups carry ``object_list`` exactly as a top-level
        field does. They are re-indexed wholesale rather than per field, because the groups are
        mutated through the extensible view (which writes into the wrapper array directly)
        rather than through the per-field setter that keeps top-level edges current.

        Args:
            obj: The object whose extensible groups should be re-indexed
            wrapper_key: The data key holding the list of repeat groups
            ref_fields: Inner field names inside a group that are reference fields
        """
        if not ref_fields:
            return

        self._drop_extensible_edges(obj)
        groups = obj.data.get(wrapper_key)
        if not isinstance(groups, list):
            return
        for group_index, group in enumerate(cast("list[Any]", groups)):
            if not isinstance(group, dict):
                continue
            for field_name in ref_fields:
                value = cast("dict[str, Any]", group).get(field_name)
                if isinstance(value, str) and value.strip():
                    self.register(obj, field_name, value, group_index)

    def _drop_extensible_edges(self, obj: IDFObject) -> None:
        """Remove every edge of *obj* that carries a group index."""
        obj_refs = self._references.get(obj)
        if not obj_refs:
            return
        for name_upper, field_name, group_index in [e for e in obj_refs if e[2] is not None]:
            obj_refs.discard((name_upper, field_name, group_index))
            referrers = self._referenced_by.get(name_upper)
            if referrers is None:
                continue
            referrers.discard((obj, field_name, group_index))
            if not referrers:
                del self._referenced_by[name_upper]

    def unregister(self, obj: IDFObject) -> None:
        """Remove all reference tracking for an object."""
        if obj in self._references:
            # Remove from referenced_by
            for name_upper, field_name, group_index in self._references[obj]:
                if name_upper in self._referenced_by:
                    self._referenced_by[name_upper].discard((obj, field_name, group_index))
                    if not self._referenced_by[name_upper]:
                        del self._referenced_by[name_upper]
            del self._references[obj]

        # Also remove any references TO this object
        obj_name_upper = obj.name.upper() if obj.name else ""
        if obj_name_upper in self._referenced_by:
            del self._referenced_by[obj_name_upper]

    def get_referencing(self, name: str) -> set[IDFObject]:
        """
        O(1): Get all objects that reference a given name.

        Args:
            name: The name to look up

        Returns:
            Set of IDFObjects that reference this name

        Examples:
            Find all surfaces assigned to a zone (O(1)):

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model.add("BuildingSurface:Detailed", "South_Wall",
            ...     surface_type="Wall", construction_name="",
            ...     zone_name="Perimeter_ZN_1",
            ...     outside_boundary_condition="Outdoors",
            ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
            ...     validate=False)  # doctest: +ELLIPSIS
            BuildingSurface:Detailed('South_Wall')
            >>> len(model.references.get_referencing("Perimeter_ZN_1"))
            1
        """
        refs = self._referenced_by.get(name.upper(), set())
        return {obj for obj, _, _ in refs}

    def get_referencing_with_fields(self, name: str) -> set[tuple[IDFObject, str]]:
        """
        O(1): Get all (object, field_name) pairs that reference a given name.

        Args:
            name: The name to look up

        Returns:
            Set of (IDFObject, field_name) tuples
        """
        return {(obj, field_name) for obj, field_name, _ in self._referenced_by.get(name.upper(), set())}

    def get_referencing_edges(self, name: str) -> set[tuple[IDFObject, str, int | None]]:
        """Get all (object, field_name, group_index) edges that reference a given name.

        Same as [get_referencing_with_fields][idfkit.references.ReferenceGraph.get_referencing_with_fields]
        but keeps the extensible group index, so a caller that has to rewrite the underlying
        value knows whether it lives at the top level or inside a repeat group.
        """
        return self._referenced_by.get(name.upper(), set()).copy()

    def get_references(self, obj: IDFObject) -> set[str]:
        """
        O(1): Get all names that an object references.

        Args:
            obj: The object to look up

        Returns:
            Set of names (uppercase) that this object references
        """
        refs = self._references.get(obj, set())
        return {name for name, _, _ in refs}

    def get_references_with_fields(self, obj: IDFObject) -> set[tuple[str, str]]:
        """
        O(1): Get all (name, field_name) pairs that an object references.

        Args:
            obj: The object to look up

        Returns:
            Set of (name, field_name) tuples
        """
        return {(name, field_name) for name, field_name, _ in self._references.get(obj, set())}

    def is_referenced(self, name: str) -> bool:
        """Check if a name is referenced by any object.

        Examples:
            Check whether a zone is used by any surface before deleting it:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model.references.is_referenced("Perimeter_ZN_1")
            False
            >>> model.add("BuildingSurface:Detailed", "South_Wall",
            ...     surface_type="Wall", construction_name="",
            ...     zone_name="Perimeter_ZN_1",
            ...     outside_boundary_condition="Outdoors",
            ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
            ...     validate=False)  # doctest: +ELLIPSIS
            BuildingSurface:Detailed('South_Wall')
            >>> model.references.is_referenced("Perimeter_ZN_1")
            True
        """
        return name.upper() in self._referenced_by

    def get_dangling_references(self, valid_names: set[str]) -> Iterator[tuple[IDFObject, str, str]]:
        """
        Find all references to non-existent objects.

        Args:
            valid_names: Set of valid object names (uppercase)

        Yields:
            Tuples of (source_object, field_name, referenced_name)
        """
        valid_upper = {n.upper() for n in valid_names}

        for obj, refs in self._references.items():
            for name_upper, field_name, _group_index in refs:
                if name_upper not in valid_upper:
                    yield (obj, field_name, name_upper)

    def rename_target(self, old_name: str, new_name: str) -> None:
        """
        Update indexes when a referenced target is renamed.

        Moves _referenced_by[OLD] -> _referenced_by[NEW] and updates
        corresponding _references entries for all affected objects.

        Args:
            old_name: The old target name
            new_name: The new target name
        """
        old_upper = old_name.upper()
        new_upper = new_name.upper()
        if old_upper == new_upper:
            return

        referrers = self._referenced_by.pop(old_upper, set())
        if not referrers:
            return

        # Update _references for each referring object
        for obj, field_name, group_index in referrers:
            obj_refs = self._references.get(obj)
            if obj_refs is not None:
                obj_refs.discard((old_upper, field_name, group_index))
                obj_refs.add((new_upper, field_name, group_index))

        # Merge into new key (there may already be refs to new_name)
        if new_upper in self._referenced_by:
            self._referenced_by[new_upper].update(referrers)
        else:
            self._referenced_by[new_upper] = referrers

    def update_reference(self, obj: IDFObject, field_name: str, old_value: str | None, new_value: str | None) -> None:
        """
        Update indexes when an object's reference field changes.

        Removes the old entry from both indexes and adds the new entry.

        Args:
            obj: The object whose field changed
            field_name: The field that changed
            old_value: The previous referenced name (or None)
            new_value: The new referenced name (or None)
        """
        # Remove old
        if old_value:
            old_upper = old_value.upper()
            refs_set = self._referenced_by.get(old_upper)
            if refs_set is not None:
                refs_set.discard((obj, field_name, None))
                if not refs_set:
                    del self._referenced_by[old_upper]
            obj_refs = self._references.get(obj)
            if obj_refs is not None:
                obj_refs.discard((old_upper, field_name, None))

        # Add new
        if new_value and new_value.strip():
            new_upper = new_value.upper()
            self._referenced_by[new_upper].add((obj, field_name, None))
            self._references[obj].add((new_upper, field_name, None))

    def clear(self) -> None:
        """Clear all reference tracking."""
        self._referenced_by.clear()
        self._references.clear()
        self._object_lists.clear()

    def __len__(self) -> int:
        """Return total number of references tracked."""
        return sum(len(refs) for refs in self._references.values())

    def stats(self) -> dict[str, int]:
        """Return statistics about the reference graph."""
        return {
            "total_references": len(self),
            "objects_with_references": len(self._references),
            "names_referenced": len(self._referenced_by),
            "object_lists": len(self._object_lists),
        }
