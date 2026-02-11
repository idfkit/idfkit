"""
IDFDocument - The main container for an EnergyPlus model.

Provides:
- Typed access to object collections
- Reference tracking for O(1) dependency lookups
- On-demand validation
- Support for both IDF and epJSON formats
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .exceptions import ValidationFailedError
from .introspection import ObjectDescription, describe_object_type
from .objects import IDFCollection, IDFObject
from .references import ReferenceGraph
from .validation import validate_object
from .versions import LATEST_VERSION

if TYPE_CHECKING:
    from .schema import EpJSONSchema
    from .simulation.config import EnergyPlusConfig


# Common object type mappings for attribute access
_PYTHON_TO_IDF = {
    "zones": "Zone",
    "materials": "Material",
    "material_nomass": "Material:NoMass",
    "material_airgap": "Material:AirGap",
    "constructions": "Construction",
    "building_surfaces": "BuildingSurface:Detailed",
    "fenestration_surfaces": "FenestrationSurface:Detailed",
    "internal_mass": "InternalMass",
    "shading_surfaces": "Shading:Site:Detailed",
    "shading_building": "Shading:Building:Detailed",
    "shading_zone": "Shading:Zone:Detailed",
    "schedules_compact": "Schedule:Compact",
    "schedules_constant": "Schedule:Constant",
    "schedules_file": "Schedule:File",
    "schedules_year": "Schedule:Year",
    "schedules_week_daily": "Schedule:Week:Daily",
    "schedules_day_interval": "Schedule:Day:Interval",
    "schedules_day_hourly": "Schedule:Day:Hourly",
    "schedules_day_list": "Schedule:Day:List",
    "schedule_type_limits": "ScheduleTypeLimits",
    "people": "People",
    "lights": "Lights",
    "electric_equipment": "ElectricEquipment",
    "gas_equipment": "GasEquipment",
    "hot_water_equipment": "HotWaterEquipment",
    "infiltration": "ZoneInfiltration:DesignFlowRate",
    "ventilation": "ZoneVentilation:DesignFlowRate",
    "thermostats": "ThermostatSetpoint:DualSetpoint",
    "hvac_templates": "HVACTemplate:Zone:IdealLoadsAirSystem",
    "ideal_loads": "ZoneHVAC:IdealLoadsAirSystem",
    "sizing_zone": "Sizing:Zone",
    "sizing_system": "Sizing:System",
    "output_variables": "Output:Variable",
    "output_meters": "Output:Meter",
    "output_table_summary": "Output:Table:SummaryReports",
    "simulation_control": "SimulationControl",
    "run_period": "RunPeriod",
    "building": "Building",
    "global_geometry_rules": "GlobalGeometryRules",
    "site_location": "Site:Location",
    "sizing_parameters": "Sizing:Parameters",
    "timestep": "Timestep",
    "version": "Version",
    "window_material_simple": "WindowMaterial:SimpleGlazingSystem",
    "window_material_glazing": "WindowMaterial:Glazing",
    "window_material_gas": "WindowMaterial:Gas",
    "construction_window": "Construction",
}

# Inverse mapping
_IDF_TO_PYTHON = {v.upper(): k for k, v in _PYTHON_TO_IDF.items()}


class IDFDocument:
    """
    Main container for an EnergyPlus model.

    Attributes:
        version: The EnergyPlus version tuple (major, minor, patch)
        filepath: Path to the source file (if loaded from file)
        _collections: Dict of object_type -> IDFCollection
        _schema: EpJSONSchema for validation and field info
        _references: ReferenceGraph for dependency tracking
    """

    __slots__ = (
        "_collections",
        "_references",
        "_schedules_cache",
        "_schema",
        "filepath",
        "version",
    )

    version: tuple[int, int, int]
    filepath: Path | None
    _collections: dict[str, IDFCollection]
    _schema: EpJSONSchema | None
    _references: ReferenceGraph
    _schedules_cache: dict[str, IDFObject] | None

    def __init__(
        self,
        version: tuple[int, int, int] | None = None,
        schema: EpJSONSchema | None = None,
        filepath: Path | str | None = None,
    ) -> None:
        """
        Initialize an IDFDocument.

        Args:
            version: EnergyPlus version tuple
            schema: EpJSONSchema for validation
            filepath: Source file path
        """
        self.version = version or LATEST_VERSION
        self.filepath = Path(filepath) if filepath else None
        self._schema = schema
        self._collections: dict[str, IDFCollection] = {}
        self._references = ReferenceGraph()
        self._schedules_cache: dict[str, IDFObject] | None = None

    @property
    def schema(self) -> EpJSONSchema | None:
        """The EpJSON schema for validation and field info."""
        return self._schema

    @property
    def collections(self) -> dict[str, IDFCollection]:
        """Dict of object_type -> IDFCollection."""
        return self._collections

    @property
    def references(self) -> ReferenceGraph:
        """The reference graph for dependency tracking."""
        return self._references

    # -------------------------------------------------------------------------
    # Collection Access
    # -------------------------------------------------------------------------

    def __getitem__(self, obj_type: str) -> IDFCollection:
        """
        Get collection by object type name.

        Returns an empty collection if no objects of that type exist yet.

        Examples:
            Access all zones in the model:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> model.add("Zone", "Core_ZN")  # doctest: +ELLIPSIS
            Zone('Core_ZN')
            >>> len(model["Zone"])
            2

            Look up a specific zone by name (O(1)):

            >>> model["Zone"]["Perimeter_ZN_1"].name
            'Perimeter_ZN_1'
        """
        key = obj_type
        if key not in self._collections:
            self._collections[key] = IDFCollection(obj_type)
        return self._collections[key]

    def __getattr__(self, name: str) -> IDFCollection:
        """
        Get collection by Python-style attribute name.

        Convenient shorthand names are mapped to their IDF equivalents
        (e.g. ``zones`` -> ``Zone``, ``building_surfaces`` ->
        ``BuildingSurface:Detailed``).

        Examples:
            Use shorthand attribute names for common object types:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> len(model.zones)
            1
            >>> model.zones[0].name
            'Perimeter_ZN_1'

        Raises:
            AttributeError: If the attribute is not a known collection mapping.
        """
        if name.startswith("_"):
            raise AttributeError(name)

        # Check the mapping
        obj_type = _PYTHON_TO_IDF.get(name)
        if obj_type:
            return self[obj_type]

        # Try as-is with different cases
        for key in self._collections:
            if key.lower().replace(":", "_").replace(" ", "_") == name.lower():
                return self._collections[key]

        # Raise AttributeError for unknown attributes
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")  # noqa: TRY003

    def __contains__(self, obj_type: str) -> bool:
        """Check if document has objects of a type.

        Examples:
            Check whether the model contains any zones or materials:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> "Zone" in model
            True
            >>> "Material" in model
            False
        """
        return obj_type in self._collections and len(self._collections[obj_type]) > 0

    def __iter__(self) -> Iterator[str]:
        """Iterate over object type names."""
        return iter(self._collections)

    def __len__(self) -> int:
        """Return total number of objects."""
        return sum(len(c) for c in self._collections.values())

    def keys(self) -> list[str]:
        """Return list of object type names that have objects.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> model.keys()
            ['Zone']
        """
        return [k for k, v in self._collections.items() if v]

    def values(self) -> list[IDFCollection]:
        """Return list of non-empty collections.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> len(model.values())
            1
        """
        return [v for v in self._collections.values() if v]

    def items(self) -> list[tuple[str, IDFCollection]]:
        """Return list of (object_type, collection) pairs for non-empty collections.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> [(t, len(c)) for t, c in model.items()]
            [('Zone', 1)]
        """
        return [(k, v) for k, v in self._collections.items() if v]

    # -------------------------------------------------------------------------
    # Object Access (eppy compatibility)
    # -------------------------------------------------------------------------

    @property
    def idfobjects(self) -> _IDFObjectsView:
        """
        Dict-like access to all object collections (eppy compatibility).

        Returns a view that allows access like idf.idfobjects["ZONE"]
        """
        return _IDFObjectsView(self)

    def getobject(self, obj_type: str, name: str) -> IDFObject | None:
        """
        Get a specific object by type and name.

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
        """Get dict of object groups (eppy compatibility)."""
        # This would require IDD group info from schema
        # For now, return a simplified version
        groups: dict[str, list[str]] = {}
        for obj_type in self._collections:
            # Simple grouping by first part of name
            parts = obj_type.split(":")
            group = parts[0] if len(parts) > 1 else "Miscellaneous"
            if group not in groups:
                groups[group] = []
            groups[group].append(obj_type)
        return groups

    def describe(self, obj_type: str) -> ObjectDescription:
        """
        Get detailed field information for an object type.

        Returns a description of the object type including all fields,
        their types, defaults, constraints, and whether they are required.

        This is useful for discovering what fields are available when
        creating new objects.

        Args:
            obj_type: Object type name (e.g., "Zone", "Material")

        Returns:
            ObjectDescription with detailed field information

        Raises:
            ValueError: If no schema is loaded
            KeyError: If the object type is not found in the schema

        Examples:
            Discover which fields are needed for a new Material:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> mat_desc = model.describe("Material")
            >>> mat_desc.required_fields
            ['roughness', 'thickness', 'conductivity', 'density', 'specific_heat']

            Explore Zone fields:

            >>> zone_desc = model.describe("Zone")
            >>> zone_desc.obj_type
            'Zone'
            >>> len(zone_desc.fields) > 0
            True
        """
        if self._schema is None:
            msg = "No schema loaded - cannot describe object types"
            raise ValueError(msg)
        return describe_object_type(self._schema, obj_type)

    # -------------------------------------------------------------------------
    # Object Manipulation
    # -------------------------------------------------------------------------

    def add(
        self,
        obj_type: str,
        name: str = "",
        data: dict[str, Any] | None = None,
        *,
        validate: bool = True,
        **kwargs: Any,
    ) -> IDFObject:
        """
        Add a new object to the document.

        Args:
            obj_type: Object type (e.g., "Zone")
            name: Object name (optional for object types without a name field,
                such as Timestep, SimulationControl, GlobalGeometryRules)
            data: Field data as dict
            validate: If True (default), validate the object against schema before adding.
                Raises ValidationFailedError if validation fails. Set to False for
                bulk operations where performance matters.
            **kwargs: Additional field values

        Returns:
            The created IDFObject

        Raises:
            ValidationFailedError: If validation fails (unknown fields, missing
                required fields, invalid values)

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()

            Create a thermal zone for a south-facing perimeter office:

            >>> zone = model.add("Zone", "Perimeter_ZN_South",
            ...     x_origin=0.0, y_origin=0.0, z_origin=0.0)
            >>> zone.name
            'Perimeter_ZN_South'

            Define a concrete wall material (200 mm, k=1.4 W/m-K):

            >>> concrete = model.add("Material", "Concrete_200mm",
            ...     roughness="MediumRough", thickness=0.2,
            ...     conductivity=1.4, density=2240.0, specific_heat=900.0)
            >>> concrete.conductivity
            1.4

            Build a construction and assign it to a surface:

            >>> wall = model.add("Construction", "Ext_Wall",
            ...     outside_layer="Concrete_200mm", validate=False)

            Disable validation for bulk loading (e.g., importing from
            another tool):

            >>> for i in range(3):
            ...     _ = model.add("Zone", f"Floor{i+1}_Core", validate=False)
            >>> len(model["Zone"])
            4
        """
        # Merge data and kwargs
        field_data = dict(data) if data else {}
        field_data.update(kwargs)

        # Get schema info
        obj_schema: dict[str, Any] | None = None
        field_order: list[str] | None = None
        ref_fields: frozenset[str] | None = None
        if self._schema:
            obj_schema = self._schema.get_object_schema(obj_type)
            if self._schema.has_name(obj_type):
                field_order = self._schema.get_field_names(obj_type)
            else:
                field_order = self._schema.get_all_field_names(obj_type)
            ref_fields = self._compute_ref_fields(self._schema, obj_type)

        # Create object
        obj = IDFObject(
            obj_type=obj_type,
            name=name,
            data=field_data,
            schema=obj_schema,
            document=self,
            field_order=field_order,
            ref_fields=ref_fields,
        )

        # Validate if requested
        if validate and self._schema:
            errors = validate_object(obj, self._schema)
            if errors:
                raise ValidationFailedError(errors)

        # Add to collection
        self[obj_type].add(obj)

        # Index references
        self._index_object_references(obj)

        # Invalidate schedules cache
        if obj_type.upper().startswith("SCHEDULE"):
            self._schedules_cache = None

        return obj

    def newidfobject(self, obj_type: str, **kwargs: Any) -> IDFObject:
        """
        Create a new object (eppy compatibility).

        The 'Name' kwarg becomes the object name if provided.
        """
        name = kwargs.pop("Name", kwargs.pop("name", ""))
        return self.add(obj_type, name, **kwargs)

    def addidfobject(self, obj: IDFObject) -> IDFObject:
        """Add an existing IDFObject to the document."""
        # Set document reference
        object.__setattr__(obj, "_document", self)

        # Compute ref_fields if not already set
        if object.__getattribute__(obj, "_ref_fields") is None and self._schema:
            object.__setattr__(obj, "_ref_fields", self._compute_ref_fields(self._schema, obj.obj_type))

        # Add to collection
        self[obj.obj_type].add(obj)

        # Index references
        self._index_object_references(obj)

        return obj

    def addidfobjects(self, objects: list[IDFObject]) -> list[IDFObject]:
        """Add multiple objects to the document."""
        return [self.addidfobject(obj) for obj in objects]

    def removeidfobject(self, obj: IDFObject) -> None:
        """Remove an object from the document."""
        obj_type = obj.obj_type

        if obj_type in self._collections:
            self._collections[obj_type].remove(obj)

        # Remove from reference graph
        self._references.unregister(obj)

        # Invalidate caches
        if obj_type.upper().startswith("SCHEDULE"):
            self._schedules_cache = None

    def popidfobject(self, obj_type: str, index: int) -> IDFObject:
        """Remove and return an object by type and index (eppy compatibility).

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
        """Remove multiple objects from the document."""
        for obj in objects:
            self.removeidfobject(obj)

    def copyidfobject(self, obj: IDFObject, new_name: str | None = None) -> IDFObject:
        """Create a copy of an object with optional new name."""
        new_obj = obj.copy()
        if new_name:
            new_obj.name = new_name
        return self.addidfobject(new_obj)

    def update(self, updates: dict[str, Any]) -> None:
        """Apply batch field updates using dot-separated key paths.

        Mirrors eppy's ``json_functions.updateidf`` for parametric
        sweeps and bulk modifications.

        Each key has the form ``"ObjectType.ObjectName.field_name"``
        and the value is the new field value.  The object must already
        exist in the document.

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

    def rename(self, obj_type: str, old_name: str, new_name: str) -> None:
        """
        Rename an object and update all references.

        All objects that reference the old name are automatically updated
        to point to the new name via the reference graph.

        Args:
            obj_type: Object type
            old_name: Current name
            new_name: New name

        Examples:
            Rename a zone -- all referencing surfaces, people, lights,
            etc. are updated automatically via the reference graph:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "THERMAL ZONE 1")  # doctest: +ELLIPSIS
            Zone('THERMAL ZONE 1')
            >>> model.rename("Zone", "THERMAL ZONE 1", "Perimeter_ZN_South")
            >>> model.getobject("Zone", "THERMAL ZONE 1") is None
            True
            >>> model.getobject("Zone", "Perimeter_ZN_South").name
            'Perimeter_ZN_South'
        """
        obj = self.getobject(obj_type, old_name)
        if not obj:
            raise KeyError(f"No {obj_type} named '{old_name}'")  # noqa: TRY003

        # Setting the name triggers _set_name -> _on_name_change which handles
        # collection index, referencing objects, and graph updates.
        obj.name = new_name

    # -------------------------------------------------------------------------
    # Reference Graph
    # -------------------------------------------------------------------------

    @staticmethod
    def _compute_ref_fields(schema: EpJSONSchema, obj_type: str) -> frozenset[str]:
        """Return frozenset of reference field names (python-style) for an object type."""
        field_names = schema.get_field_names(obj_type)
        return frozenset(f for f in field_names if schema.is_reference_field(obj_type, f))

    def notify_name_change(self, obj: IDFObject, old_name: str, new_name: str) -> None:
        """Called by IDFObject._set_name when a name changes."""
        # 1. Update collection index
        obj_type = obj.obj_type
        if obj_type in self._collections:
            collection = self._collections[obj_type]
            old_key = old_name.upper()
            if old_key in collection.by_name:
                del collection.by_name[old_key]
            new_key = new_name.upper()
            if new_name:
                collection.by_name[new_key] = obj

        # 2. Update referencing objects' _data directly (bypass _set_field to avoid recursion)
        referencing = self._references.get_referencing_with_fields(old_name)
        for ref_obj, field_name in referencing:
            current = ref_obj.data.get(field_name, "")
            if isinstance(current, str) and current.upper() == old_name.upper():
                ref_obj.data[field_name] = new_name

        # 3. Update graph indexes
        self._references.rename_target(old_name, new_name)

        # 4. Invalidate schedules cache if needed
        if obj_type.upper().startswith("SCHEDULE"):
            self._schedules_cache = None

    def notify_reference_change(self, obj: IDFObject, field_name: str, old_value: Any, new_value: Any) -> None:
        """Called by IDFObject._set_field when a reference field changes."""
        old_str = old_value if isinstance(old_value, str) else None
        new_str = new_value if isinstance(new_value, str) else None
        self._references.update_reference(obj, field_name, old_str, new_str)

    def _index_object_references(self, obj: IDFObject) -> None:
        """Index all references in an object using schema information."""
        if not self._schema:
            return  # Schema required for reference indexing

        obj_type = obj.obj_type
        field_names = self._schema.get_field_names(obj_type)

        for field_name in field_names:
            if self._schema.is_reference_field(obj_type, field_name):
                value = obj.data.get(field_name)
                if value and isinstance(value, str) and value.strip():
                    self._references.register(obj, field_name, value)

    def get_referencing(self, name: str) -> set[IDFObject]:
        """Get all objects that reference a given name.

        Uses the reference graph for O(1) lookup.  This is the primary
        way to find all surfaces in a zone, all objects using a schedule,
        or all surfaces assigned to a construction.

        Examples:
            Find every surface that belongs to a zone:

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
            >>> refs = model.get_referencing("Perimeter_ZN_1")
            >>> len(refs)
            1
        """
        return self._references.get_referencing(name)

    def get_references(self, obj: IDFObject) -> set[str]:
        """Get all names that an object references.

        Useful for understanding the dependency chain of a surface
        (which zone and construction does it point to?).

        Examples:
            Inspect what a wall surface depends on:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> wall = model.add("BuildingSurface:Detailed", "South_Wall",
            ...     surface_type="Wall", construction_name="",
            ...     zone_name="Perimeter_ZN_1",
            ...     outside_boundary_condition="Outdoors",
            ...     sun_exposure="SunExposed", wind_exposure="WindExposed",
            ...     validate=False)
            >>> refs = model.get_references(wall)
            >>> "PERIMETER_ZN_1" in refs
            True
        """
        return self._references.get_references(obj)

    # -------------------------------------------------------------------------
    # Schedules (common access pattern)
    # -------------------------------------------------------------------------

    @property
    def schedules_dict(self) -> dict[str, IDFObject]:
        """
        Get dict mapping schedule names to schedule objects.

        This is a cached property for fast schedule lookup.
        """
        if self._schedules_cache is None:
            self._schedules_cache = self._build_schedules_dict()
        return self._schedules_cache

    def _build_schedules_dict(self) -> dict[str, IDFObject]:
        """Build the schedules lookup dict."""
        schedules: dict[str, IDFObject] = {}
        schedule_types = [
            "Schedule:Year",
            "Schedule:Compact",
            "Schedule:File",
            "Schedule:Constant",
            "Schedule:Day:Hourly",
            "Schedule:Day:Interval",
            "Schedule:Day:List",
            "Schedule:Week:Daily",
            "Schedule:Week:Compact",
        ]

        for sched_type in schedule_types:
            if sched_type in self._collections:
                for sched in self._collections[sched_type]:
                    if sched.name:
                        schedules[sched.name.upper()] = sched

        return schedules

    def get_schedule(self, name: str) -> IDFObject | None:
        """Get a schedule by name (case-insensitive)."""
        return self.schedules_dict.get(name.upper())

    def get_used_schedules(self) -> set[str]:
        """
        Get names of schedules actually used in the model.

        Uses the reference graph for O(1) lookup per schedule.
        """
        used: set[str] = set()
        for name in self.schedules_dict:
            if self._references.is_referenced(name):
                used.add(name)
        return used

    # -------------------------------------------------------------------------
    # Surfaces (common access pattern)
    # -------------------------------------------------------------------------

    def getsurfaces(self, surface_type: str | None = None) -> list[IDFObject]:
        """
        Get building surfaces, optionally filtered by type.

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
        surfaces = list(self["BuildingSurface:Detailed"])

        if surface_type:
            surface_type_upper = surface_type.upper()
            surfaces = [s for s in surfaces if (getattr(s, "surface_type", None) or "").upper() == surface_type_upper]

        return surfaces

    def get_zone_surfaces(self, zone_name: str) -> list[IDFObject]:
        """Get all surfaces belonging to a zone."""
        return list(self._references.get_referencing(zone_name))

    # -------------------------------------------------------------------------
    # Iteration
    # -------------------------------------------------------------------------

    @property
    def all_objects(self) -> Iterator[IDFObject]:
        """Iterate over all objects in the document."""
        for collection in self._collections.values():
            yield from collection

    def objects_by_type(self) -> Iterator[tuple[str, IDFCollection]]:
        """Iterate over (type, collection) pairs."""
        for obj_type, collection in self._collections.items():
            if collection:
                yield obj_type, collection

    # -------------------------------------------------------------------------
    # Expansion
    # -------------------------------------------------------------------------

    def expand(
        self,
        *,
        energyplus: EnergyPlusConfig | None = None,
        timeout: float = 120.0,
    ) -> IDFDocument:
        """Run the EnergyPlus *ExpandObjects* preprocessor on this document.

        This replaces ``HVACTemplate:*`` objects with their fully specified
        low-level HVAC equivalents and returns a **new** document.  The
        current document is not mutated.

        If the document contains no expandable objects, a copy is returned
        immediately without invoking the preprocessor.

        Args:
            energyplus: Pre-configured EnergyPlus installation.  If ``None``,
                auto-discovery is used.
            timeout: Maximum time in seconds to wait for the preprocessor
                (default 120).

        Returns:
            A new :class:`IDFDocument` with all template objects expanded.

        Raises:
            EnergyPlusNotFoundError: If no EnergyPlus installation is found.
            ExpandObjectsError: If the preprocessor fails.

        Examples:
            Expand HVACTemplate objects into low-level HVAC components
            so you can inspect or modify the resulting system::

                model = load_idf("5ZoneAirCooled_HVACTemplate.idf")
                expanded = model.expand()
                for ideal in expanded["ZoneHVAC:IdealLoadsAirSystem"]:
                    print(ideal.name, ideal.cooling_limit)

            Point to a specific EnergyPlus installation::

                from idfkit.simulation import find_energyplus
                ep = find_energyplus(version=(24, 1, 0))
                expanded = model.expand(energyplus=ep)
        """
        from .simulation.expand import expand_objects

        return expand_objects(self, energyplus=energyplus, timeout=timeout)

    # -------------------------------------------------------------------------
    # Copying
    # -------------------------------------------------------------------------

    def copy(self) -> IDFDocument:
        """Create a deep copy of the document.

        The copy is independent -- modifying the copy does not affect
        the original.

        Examples:
            Create a copy for parametric comparison (e.g., testing
            different insulation strategies without altering the baseline):

            >>> from idfkit import new_document
            >>> baseline = new_document()
            >>> baseline.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> variant = baseline.copy()
            >>> len(variant)
            1
            >>> variant.add("Zone", "Server_Room")  # doctest: +ELLIPSIS
            Zone('Server_Room')
            >>> len(baseline)
            1
            >>> len(variant)
            2
        """
        new_doc = IDFDocument(
            version=self.version,
            schema=self._schema,
            filepath=self.filepath,
        )

        for obj in self.all_objects:
            new_obj = obj.copy()
            new_doc.addidfobject(new_obj)

        return new_doc

    # -------------------------------------------------------------------------
    # File I/O (eppy compatibility)
    # -------------------------------------------------------------------------

    def save(self, filepath: str | Path | None = None, encoding: str = "latin-1") -> None:
        """Save the document to its current filepath (eppy compatibility).

        Args:
            filepath: Explicit path override.  If ``None``, uses
                ``self.filepath``.
            encoding: Output encoding (default ``latin-1``).

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
        write_idf(self, target, encoding=encoding)
        self.filepath = target

    def saveas(self, filepath: str | Path, encoding: str = "latin-1") -> None:
        """Save to a new path and update ``self.filepath`` (eppy compatibility).

        After saving, ``self.filepath`` is updated to the new path so
        subsequent :meth:`save` calls write to it.

        Args:
            filepath: Destination path.
            encoding: Output encoding.

        Examples:
            Save under a new name and continue editing there::

                model = load_idf("Baseline.idf")
                model.saveas("HighInsulation_Variant.idf")
                model.save()   # now writes to HighInsulation_Variant.idf
        """
        from .writers import write_idf

        target = Path(filepath)
        write_idf(self, target, encoding=encoding)
        self.filepath = target

    def savecopy(self, filepath: str | Path, encoding: str = "latin-1") -> None:
        """Save a copy without changing ``self.filepath`` (eppy compatibility).

        Unlike :meth:`saveas`, the document's ``filepath`` remains
        unchanged.

        Args:
            filepath: Destination path.
            encoding: Output encoding.

        Examples:
            Create a snapshot before running a parametric sweep::

                model = load_idf("Baseline.idf")
                model.savecopy("Baseline_backup.idf")
                # ... modify model ...
                model.save()   # still writes to Baseline.idf
        """
        from .writers import write_idf

        write_idf(self, Path(filepath), encoding=encoding)

    # -------------------------------------------------------------------------
    # String Representation
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        version_str = f"{self.version[0]}.{self.version[1]}.{self.version[2]}"
        return f"IDFDocument(version={version_str}, objects={len(self)})"

    def __str__(self) -> str:
        lines = [repr(self), ""]
        for obj_type, collection in sorted(self._collections.items()):
            if collection:
                lines.append(f"  {obj_type}: {len(collection)} objects")
        return "\n".join(lines)


class _IDFObjectsView:
    """
    Dict-like view for idfobjects access (eppy compatibility).

    Allows: idf.idfobjects["ZONE"], idf.idfobjects["Zone"], etc.
    """

    __slots__ = ("_doc",)

    def __init__(self, doc: IDFDocument) -> None:
        self._doc = doc

    def __getitem__(self, key: str) -> IDFCollection:
        collections = self._doc.collections
        # Try exact match first
        if key in collections:
            return collections[key]

        # Try case-insensitive match
        key_upper = key.upper()
        for obj_type, collection in collections.items():
            if obj_type.upper() == key_upper:
                return collection

        # Return empty collection
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
        return list(self._doc.collections.keys())

    def values(self) -> list[IDFCollection]:
        return list(self._doc.collections.values())

    def items(self) -> list[tuple[str, IDFCollection]]:
        return list(self._doc.collections.items())
