"""Eppy-compatibility helpers for :class:`~idfkit.document.IDFDocument`.

This module contains methods that exist **solely** to ease migration from
`eppy <https://github.com/santoshphilip/eppy>`_.  For each method there is
a recommended idfkit alternative noted in the docstring.

The mixin is mixed into :class:`IDFDocument` so that existing eppy code
continues to work without modification.  In a future release the mixin
may be deprecated and eventually removed.

To opt out early, avoid importing or calling any symbol from this module.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .writers import OutputType

if TYPE_CHECKING:
    from .objects import IDFCollection, IDFObject
    from .schema import EpJSONSchema
    from .simulation.result import SimulationResult


# ---------------------------------------------------------------------------
# _IDFObjectsView: case-insensitive dict-like wrapper
# ---------------------------------------------------------------------------


class _IDFObjectsView:
    """Case-insensitive view over document collections (eppy compatibility).

    Allows ``doc.idfobjects["ZONE"]`` to work the same as ``doc["Zone"]``.
    """

    __slots__ = ("_doc",)

    def __init__(self, doc: EppyDocumentMixin) -> None:
        self._doc = doc

    def __getitem__(self, key: str) -> IDFCollection:
        collections = self._doc.collections
        if key in collections:
            return collections[key]
        key_upper = key.upper()
        for obj_type, collection in collections.items():
            if obj_type.upper() == key_upper:
                return collection
        return self._doc[key]

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        collections = self._doc.collections
        key_upper = key.upper()
        for obj_type, collection in collections.items():
            if obj_type.upper() == key_upper:
                return len(collection) > 0
        return False

    def __iter__(self) -> Iterator[str]:
        return iter(self._doc.collections)

    def keys(self) -> list[str]:
        """Return object type names."""
        return list(self._doc.collections.keys())

    def values(self) -> list[IDFCollection]:
        """Return all collections."""
        return list(self._doc.collections.values())

    def items(self) -> list[tuple[str, IDFCollection]]:
        """Return (type, collection) pairs."""
        return list(self._doc.collections.items())


# ---------------------------------------------------------------------------
# Mixin
# ---------------------------------------------------------------------------


class EppyDocumentMixin:
    """Eppy-compatibility methods for :class:`~idfkit.document.IDFDocument`.

    Mixed into :class:`IDFDocument` automatically.  Each method documents
    the preferred idfkit API in a ``.. tip::`` block.
    """

    __slots__ = ()

    # -- TYPE_CHECKING interface (attributes provided by IDFDocument) ---------
    if TYPE_CHECKING:
        _collections: dict[str, IDFCollection]
        _schema: EpJSONSchema | None
        filepath: Path | None

        @property
        def collections(self) -> dict[str, IDFCollection]: ...
        def __getitem__(self, key: str) -> IDFCollection: ...
        def add(self, obj_type: str, name: str = "", **kwargs: Any) -> IDFObject: ...
        def removeidfobject(self, obj: IDFObject) -> None: ...

        @staticmethod
        def _compute_ref_fields(schema: EpJSONSchema, obj_type: str) -> frozenset[str]: ...
        def _index_object_references(self, obj: IDFObject) -> None: ...

    # -- Object access -------------------------------------------------------

    @property
    def idfobjects(self) -> _IDFObjectsView:
        """Dict-like access to all object collections (eppy compatibility).

        Returns a case-insensitive view so ``idf.idfobjects["ZONE"]``
        continues to work.

        .. tip::

            Prefer bracket access for new code::

                zones = doc["Zone"]
                zone = doc["Zone"]["Office"]
        """
        return _IDFObjectsView(self)

    def getobject(self, obj_type: str, name: str) -> IDFObject | None:
        """Get a specific object by type and name (eppy compatibility).

        .. tip::

            Prefer bracket access for new code::

                zone = doc["Zone"]["Office"]

        Args:
            obj_type: Object type (e.g., "Zone")
            name: Object name

        Returns:
            IDFObject or None if not found

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model.getobject("Zone", "Perimeter_ZN_1").name
            'Perimeter_ZN_1'
            >>> model.getobject("Zone", "NonExistent") is None
            True
        """
        collection = self._collections.get(obj_type)
        if collection:
            return collection.get(name)
        return None

    def getiddgroupdict(self) -> dict[str, list[str]]:
        """Get dict mapping IDD group names to their object types (eppy compatibility).

        Uses actual schema group metadata when a schema is loaded, so the
        returned group names match those in the EnergyPlus IDD (e.g.
        ``"Thermal Zones and Surfaces"``).

        Returns:
            Dict of ``{group_name: [object_type, ...]}`` for every object
            type present in the document.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> groups = model.getiddgroupdict()
            >>> "Office" not in groups  # groups are IDD group names, not object names
            True
        """
        groups: dict[str, list[str]] = {}
        for obj_type in self._collections:
            group: str | None = None
            if self._schema is not None:
                group = self._schema.get_group(obj_type)
            if group is None:
                group = "Miscellaneous"
            if group not in groups:
                groups[group] = []
            groups[group].append(obj_type)
        return groups

    # -- Object creation / mutation ------------------------------------------

    def newidfobject(self, obj_type: str, **kwargs: Any) -> IDFObject:
        """Create a new object (eppy compatibility).

        Provided for migration convenience.  The ``Name`` kwarg becomes
        the object name if provided.

        .. tip::

            Prefer :meth:`~idfkit.document.IDFDocument.add` for new code::

                zone = doc.add("Zone", "Office", x_origin=0.0)
        """
        name = kwargs.pop("Name", kwargs.pop("name", ""))
        return self.add(obj_type, name, **kwargs)

    def addidfobject(self, obj: IDFObject) -> IDFObject:
        """Add an existing IDFObject to the document (eppy compatibility).

        .. tip::

            Prefer :meth:`~idfkit.document.IDFDocument.add` for new code.
        """
        object.__setattr__(obj, "_document", self)

        if object.__getattribute__(obj, "_ref_fields") is None and self._schema:
            object.__setattr__(
                obj,
                "_ref_fields",
                self._compute_ref_fields(self._schema, obj.obj_type),
            )

        self[obj.obj_type].add(obj)
        self._index_object_references(obj)
        return obj

    def addidfobjects(self, objects: list[IDFObject]) -> list[IDFObject]:
        """Add multiple objects to the document (eppy compatibility).

        .. tip:: Prefer calling :meth:`~idfkit.document.IDFDocument.add` in a loop.
        """
        return [self.addidfobject(obj) for obj in objects]

    def popidfobject(self, obj_type: str, index: int) -> IDFObject:
        """Remove and return an object by type and index (eppy compatibility).

        .. tip::

            Prefer :meth:`~idfkit.document.IDFDocument.removeidfobject`
            with a direct object reference.

        Args:
            obj_type: Object type (e.g. "Zone")
            index: Zero-based index within the collection

        Returns:
            The removed IDFObject

        Raises:
            IndexError: If the index is out of range
        """
        collection = self[obj_type]
        obj = collection[index]
        self.removeidfobject(obj)
        return obj

    def removeidfobjects(self, objects: list[IDFObject]) -> None:
        """Remove multiple objects from the document (eppy compatibility).

        .. tip:: Call :meth:`~idfkit.document.IDFDocument.removeidfobject` in a loop.
        """
        for obj in objects:
            self.removeidfobject(obj)

    def removeallidfobjects(self, obj_type: str) -> None:
        """Remove all objects of a given type from the document (eppy compatibility).

        .. tip::

            For new code, iterate and remove directly::

                for obj in list(doc[obj_type]):
                    doc.removeidfobject(obj)

        Args:
            obj_type: Object type to remove all instances of (e.g. ``"Zone"``).

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "A")  # doctest: +ELLIPSIS
            Zone('A')
            >>> model.add("Zone", "B")  # doctest: +ELLIPSIS
            Zone('B')
            >>> model.removeallidfobjects("Zone")
            >>> len(model["Zone"])
            0
        """
        for obj in list(self[obj_type]):
            self.removeidfobject(obj)

    def copyidfobject(self, obj: IDFObject, new_name: str | None = None) -> IDFObject:
        """Create a copy of an object with optional new name (eppy compatibility).

        .. tip::

            Use ``obj.copy()`` to create a detached copy, then
            :meth:`addidfobject` to add it.
        """
        new_obj = obj.copy()
        if new_name:
            new_obj.name = new_name
        return self.addidfobject(new_obj)

    def update(self, updates: dict[str, Any]) -> None:
        """Apply batch field updates using dot-separated key paths (eppy compatibility).

        Mirrors eppy's ``json_functions.updateidf`` for parametric
        sweeps and bulk modifications.

        Each key has the form ``"ObjectType.ObjectName.field_name"``
        and the value is the new field value.  The object must already
        exist in the document.

        .. tip::

            For new code, modify objects directly::

                zone = doc["Zone"]["Office"]
                zone.x_origin = 10.0

        .. note::

           Object names containing literal dots are **not** supported
           because the separator is itself a dot.  For objects whose
           names may contain dots, modify fields directly via
           :meth:`getobject` instead.

        Args:
            updates: Mapping of ``"Type.Name.field"`` -> new_value.

        Raises:
            KeyError: If the referenced object does not exist or the
                key format is invalid.

        Examples:
            Batch-update fields for parametric analysis -- for instance,
            sweep insulation thickness without touching the rest of the model:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Material", "Insulation",
            ...     roughness="Rough", thickness=0.05,
            ...     conductivity=0.04, density=30.0, specific_heat=1500.0)  # doctest: +ELLIPSIS
            Material('Insulation')
            >>> model.update({"Material.Insulation.thickness": 0.1})
            >>> model.getobject("Material", "Insulation").thickness
            0.1
        """
        from .objects import to_python_name

        for dotted_key, value in updates.items():
            parts = dotted_key.split(".", 2)
            if len(parts) != 3:
                msg = f"Expected 'ObjectType.ObjectName.field_name', got '{dotted_key}'"
                raise KeyError(msg)
            obj_type, obj_name, field_name = parts
            obj = self.getobject(obj_type, obj_name)
            if obj is None:
                msg = f"No {obj_type} named '{obj_name}'"
                raise KeyError(msg)
            setattr(obj, to_python_name(field_name), value)

    # -- Surfaces (common access pattern) ------------------------------------

    def getsurfaces(self, surface_type: str | None = None) -> list[IDFObject]:
        """Get building surfaces, optionally filtered by type (eppy compatibility).

        .. tip::

            Prefer filtering directly for new code::

                walls = doc["BuildingSurface:Detailed"].filter(
                    lambda s: s.surface_type == "Wall"
                )

        Args:
            surface_type: Filter by surface type ("wall", "floor", "roof", "ceiling")

        Returns:
            List of surface objects

        Examples:
            Query the building envelope by surface type:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("BuildingSurface:Detailed", "South_Wall",
            ...     surface_type="Wall", construction_name="", zone_name="",
            ...     outside_boundary_condition="Outdoors",
            ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
            ...     validate=False)  # doctest: +ELLIPSIS
            BuildingSurface:Detailed('South_Wall')
            >>> len(model.getsurfaces())
            1
            >>> len(model.getsurfaces("wall"))
            1
            >>> len(model.getsurfaces("floor"))
            0
        """
        surfaces: list[IDFObject] = list(self["BuildingSurface:Detailed"])

        if surface_type:
            surface_type_upper = surface_type.upper()
            surfaces = [s for s in surfaces if (getattr(s, "surface_type", None) or "").upper() == surface_type_upper]

        return surfaces

    # -- I/O -----------------------------------------------------------------

    def save(
        self,
        filepath: str | Path | None = None,
        encoding: str = "latin-1",
        output_type: OutputType = "standard",
    ) -> None:
        """Save the document to its current filepath (eppy compatibility).

        .. tip::

            Also the recommended idfkit API.  For format conversion, use
            :func:`~idfkit.writers.write_idf` or
            :func:`~idfkit.writers.write_epjson` directly.

        Args:
            filepath: Explicit path override.  If ``None``, uses
                ``self.filepath``.
            encoding: Output encoding (default ``latin-1``).
            output_type: IDF formatting mode — ``"standard"`` (with field
                comments), ``"nocomment"``, or ``"compressed"`` (single-line).

        Raises:
            ValueError: If no filepath is set and none is provided.

        Examples:
            Save a modified model back to its original IDF file::

                model = load_idf("5ZoneAirCooled.idf")
                model.add("Zone", "Mech_Room")
                model.save()   # overwrites 5ZoneAirCooled.idf

            Save to a new path for archival::

                model.save("5ZoneAirCooled_v2.idf")
        """
        from .writers import write_idf

        target = Path(filepath) if filepath else self.filepath
        if target is None:
            msg = "No filepath set - pass a path or use saveas()"
            raise ValueError(msg)
        write_idf(self, target, encoding=encoding, output_type=output_type)  # type: ignore[arg-type]
        self.filepath = target

    def saveas(
        self,
        filepath: str | Path,
        encoding: str = "latin-1",
        output_type: OutputType = "standard",
    ) -> None:
        """Save to a new path and update ``self.filepath`` (eppy compatibility).

        After saving, ``self.filepath`` is updated to the new path so
        subsequent :meth:`save` calls write to it.

        .. tip::

            Also the recommended idfkit API.

        Args:
            filepath: Destination path.
            encoding: Output encoding.
            output_type: IDF formatting mode — ``"standard"`` (with field
                comments), ``"nocomment"``, or ``"compressed"`` (single-line).

        Examples:
            Save under a new name and continue editing there::

                model = load_idf("Baseline.idf")
                model.saveas("HighInsulation_Variant.idf")
                model.save()   # now writes to HighInsulation_Variant.idf
        """
        from .writers import write_idf

        target = Path(filepath)
        write_idf(self, target, encoding=encoding, output_type=output_type)  # type: ignore[arg-type]
        self.filepath = target

    def savecopy(
        self,
        filepath: str | Path,
        encoding: str = "latin-1",
        output_type: OutputType = "standard",
    ) -> None:
        """Save a copy without changing ``self.filepath`` (eppy compatibility).

        Unlike :meth:`saveas`, the document's ``filepath`` remains
        unchanged.

        .. tip::

            Also the recommended idfkit API.

        Args:
            filepath: Destination path.
            encoding: Output encoding.
            output_type: IDF formatting mode — ``"standard"`` (with field
                comments), ``"nocomment"``, or ``"compressed"`` (single-line).

        Examples:
            Create a snapshot before running a parametric sweep::

                model = load_idf("Baseline.idf")
                model.savecopy("Baseline_backup.idf")
                # ... modify model ...
                model.save()   # still writes to Baseline.idf
        """
        from .writers import write_idf

        write_idf(self, Path(filepath), encoding=encoding, output_type=output_type)  # type: ignore[arg-type]

    # -- Simulation ----------------------------------------------------------

    def run(
        self,
        weather: str | Path,
        **kwargs: Any,
    ) -> SimulationResult:
        """Run an EnergyPlus simulation (eppy-compatible convenience method).

        This is a thin wrapper around :func:`idfkit.simulation.simulate`
        provided for users migrating from eppy's ``idf.run()`` pattern.

        .. tip::

            For new code, prefer the standalone function::

                from idfkit.simulation import simulate
                result = simulate(model, "weather.epw")

            It offers the same parameters and keeps simulation concerns
            separate from document manipulation.

        Args:
            weather: Path to the EPW weather file.
            **kwargs: Forwarded to :func:`~idfkit.simulation.simulate`
                (e.g. ``output_dir``, ``annual``, ``design_day``,
                ``timeout``, ``energyplus``).

        Returns:
            :class:`~idfkit.simulation.SimulationResult` with paths to all
            output files, error reports, and SQL queries.

        Raises:
            EnergyPlusNotFoundError: If no EnergyPlus installation is found.
            SimulationError: If the simulation fails.

        Examples:
            Run a design-day simulation::

                model = load_idf("5ZoneAirCooled.idf")
                result = model.run("weather.epw", design_day=True)
                print(result.errors.summary())
        """
        from .simulation import simulate

        return simulate(self, weather, **kwargs)  # type: ignore[arg-type]
