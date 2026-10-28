"""Auto-generated type stub for IDFDocument (EnergyPlus 26.2.0).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs 26.2.0
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any, Generic, TypeVar

from ._accessors import AccessorResolver
from ._compat import EppyDocumentMixin
from ._generated_types import *  # noqa: F403
from ._generated_types import _ObjectTypeMap
from .cst import DocumentCST, SourceSpan
from .introspection import ObjectDescription
from .objects import IDFCollection, IDFObject
from .references import ReferenceGraph
from .schema import EpJSONSchema
from .simulation.config import EnergyPlusConfig
from .writers import FieldComments

Strict = TypeVar("Strict", bound=bool, default=bool, covariant=True)

_PYTHON_TO_IDF: dict[str, str]
_IDF_TO_PYTHON: dict[str, str]
_RESERVED: frozenset[str]

def _build_resolver(schema: EpJSONSchema) -> AccessorResolver: ...

class IDFDocument(_ObjectTypeMap, EppyDocumentMixin, Generic[Strict]):  # type: ignore[misc]
    """Main container for an EnergyPlus model.

    Attributes:
        version: The EnergyPlus version tuple (major, minor, patch)
        filepath: Path to the source file (if loaded from file)
        _collections: Dict of object_type -> IDFCollection
        _schema: EpJSONSchema for validation and field info
        _references: ReferenceGraph for dependency tracking
    """

    filepath: Path | None

    def __init__(
        self,
        version: tuple[int, int, int] | None = ...,
        schema: EpJSONSchema | None = ...,
        filepath: Path | str | None = ...,
        *,
        strict: Strict = ...,
    ) -> None:
        """Initialize an IDFDocument.

        Args:
            version: EnergyPlus version tuple
            schema: EpJSONSchema for validation
            filepath: Source file path
            strict: When ``True``, accessing or setting an unknown field name on any
                [IDFObject][idfkit.objects.IDFObject] owned by this document raises
                :class:`~idfkit.exceptions.InvalidFieldError` instead of returning ``None``.  This
                is useful during migration from eppy to catch field-name
                typos early.  This value is immutable after construction.
        """

    @property
    def version(self) -> tuple[int, int, int]:
        """EnergyPlus version tuple ``(major, minor, patch)``.

        Reflects the version the document was loaded or created with.  It is
        kept in sync with the ``Version`` object's ``version_identifier`` field
        at parse/add time, but direct mutation of ``version_identifier`` on the
        object after load will *not* update this value — the written output will
        change while schema operations remain coherent.
        """
    @property
    def strict(self) -> Strict:
        """Whether strict field access mode is enabled.

        When ``True``, accessing or setting an unknown field name on objects in this
        document raises :class:`~idfkit.exceptions.InvalidFieldError` instead of returning ``None``.

        This property is read-only; set it via the constructor.
        """
    @property
    def schema(self) -> EpJSONSchema | None:
        """The EpJSON schema for validation and field info."""
    @property
    def cst(self) -> DocumentCST | None:
        """The concrete syntax tree, if the document was parsed with ``preserve_formatting=True``."""
    @property
    def raw_text(self) -> str | None:
        """The original source text, if the document was parsed with ``preserve_formatting=True``."""
    @property
    def collections(self) -> dict[str, IDFCollection[IDFObject]]:
        """Dict of object_type -> IDFCollection."""
    @property
    def references(self) -> ReferenceGraph:
        """The reference graph for dependency tracking."""
    def changed_objects(self) -> Iterator[IDFObject]:
        """Every object a preserving write will write afresh rather than reproduce.

        Empty for a document read with ``preserve_formatting=True`` and not edited since. Every
        object for a document read without it, because there is nothing to reproduce.

        :attr:`raw_text` answers whether a write will preserve at all. This answers how many
        objects it will REWRITE, and it is the part a consumer cannot work out for itself: a rename
        clears the record on every object that referred to the renamed one, so counting from your
        own edit log reports one where the answer is nine.

        **It is not "everything that will differ", and a removal is the case that separates the
        two.** An object removed from the document is no longer in it to be yielded, so this can
        return nothing for a write that changes the file. A consumer treating an empty result as
        "the file is unchanged" would be wrong on every removal. To ask whether the file will
        differ at all, compare the write with :attr:`raw_text`; ask this for how much of it is
        being written afresh.

        :attr:`IDFObject.source_text` is the same record read one object at a time, and it is the
        retained TEXT rather than a flag: a reader has to know that HAVING text means unchanged.
        This asks the question directly.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> zone = model.add("Zone", "Perimeter_ZN_1")
            >>> nothing_was_read = list(model.changed_objects()) == list(model.all_objects)
            >>> nothing_was_read  # so every object is one a write has to build
            True
        """
    def region_of(self, obj: IDFObject) -> SourceSpan | None:
        """Where *obj*'s characters sit in :attr:`raw_text`, or ``None`` if they sit nowhere.

        ``None`` for an object added since the read and for a document read without
        ``preserve_formatting=True``.

        This is what makes :meth:`changed_objects` usable. Turning an edit into the smallest
        possible change to a file takes three things: WHICH objects will be rewritten, WHAT text
        each becomes, and WHERE the old one was. Without the third a consumer has to write the whole
        file and compare, which is the work :meth:`changed_objects` exists to avoid.

        The range is where the object WAS, and stays answerable after it changes. That is the case
        it is for: the objects worth locating are the ones being rewritten.

        **Where the replacement text comes from is not settled here.** A preserving write hands the
        formatter the object's own source, so text produced any other way differs from what
        :func:`~idfkit.writers.write_idf` would have produced for the same object: the author's
        units and notes come back as generated labels. A consumer that needs the two to agree takes
        the whole file from ``write_idf``. That gap is open, and it is recorded rather than papered
        over.

        The end of the range excludes whatever separated this object from the next, because that is
        what a preserving write leaves in place. It INCLUDES a comment on the terminator's own line,
        which is the last field's comment and is rewritten with it.

        Offsets rather than a line and column: a consumer wanting the rendering has the text to
        compute it from, while going the other way costs a scan.
        """
    def render_object(self, obj: IDFObject, *, field_comments: FieldComments = "preserve") -> str | None:
        """*obj*, rendered exactly as a preserving write would render it.

        The text that belongs in the range :meth:`region_of` returns, so the two compose into an
        edit that leaves the file where :func:`~idfkit.writers.write_idf` would have left it.
        ``None`` for an object the retained source does not hold, which is the same set
        :meth:`region_of` declines.

        :meth:`~idfkit.writers.IDFWriter.format_object` is not this, and that is the reason this
        exists. A preserving write hands the formatter the object's own source text, so a caller
        who does not have that text gets the author's units and notes back as generated labels:
        ``!- North Axis {deg}`` becomes ``!- North Axis``. That is a unit lost from an engineering
        model by an editor asked to save a file, and no docstring is a good enough guard against it.

        *field_comments* is the only option, because it is the only one a preserving write honours.
        ``indent``, ``comment_column``, ``ordering`` and ``version_first`` are refused by
        ``write_idf`` alongside ``preserve_formatting``, and an ``output_type`` other than
        ``"standard"`` takes precedence over preservation and sends the whole document down the
        formatting path. Accepting any of them here would render one object on terms the surrounding
        file was not written on, which is the divergence this method exists to prevent.

        No trailing line break: the range this fills ends at the terminator, or at the comment on
        that line, and what follows separates one object from the next, which a write leaves alone.
        """

    def get_collection(self, obj_type: str) -> IDFCollection[IDFObject]:
        """Get collection by type name (typed for dynamic string keys).

        Same lookup as ``model[obj_type]``, including the case-insensitive
        match and the refusal to store anything on a miss.
        """
    def __getattr__(self, name: str) -> IDFCollection[IDFObject]:
        """Get collection by Python-style attribute name.

        Every object type in the document's schema is reachable this way as its
        ``snake_case`` plural (``model.air_loop_hvacs``), which the stub types as
        ``IDFCollection`` of the generated class. Hand-written shorthands in
        ``_PYTHON_TO_IDF`` (e.g. ``building_surfaces`` -> ``BuildingSurface:Detailed``,
        ``ideal_loads`` -> ``ZoneHVAC:IdealLoadsAirSystem``) also resolve, and keep
        their meaning where one coincides with a derived name. The raw type name, with
        ``_`` in place of ``:`` and in any case (``model.Site_Location``,
        ``model.ZONE``), resolves as it did before derived names existed.

        Without a schema loaded, only the hand-written shorthands and a
        case-insensitive match against existing collections are available.

        Examples:
            Use attribute names for object types:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Perimeter_ZN_1")  # doctest: +ELLIPSIS
            Zone('Perimeter_ZN_1')
            >>> len(model.zones)
            1
            >>> model.zones[0].name
            'Perimeter_ZN_1'

        Raises:
            AttributeError: If the name resolves to no object type.  When the
                schema has a close match the message names it.
        """
    def __contains__(self, obj_type: str) -> bool:  # type: ignore[override]
        """Check if document has objects of a type.

        Matched case-insensitively and resolved against the schema, the same
        way [__getitem__][idfkit.document.IDFDocument.__getitem__] does, so
        ``"zone" in model`` and ``len(model["zone"]) > 0`` can never disagree.
        An unrecognised type name answers False rather than raising.

        Examples:
            Check whether the model contains any zones or materials:

            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> "Zone" in model
            True
            >>> "zone" in model
            True
            >>> "Material" in model
            False
            >>> "Zoen" in model
            False
        """
    def __iter__(self) -> Iterator[str]:  # type: ignore[override]
        """Iterate over object type names."""
    def __len__(self) -> int:
        """Return total number of objects."""
    def keys(self) -> list[str]:  # type: ignore[override]
        """Return list of object type names that have objects.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> "Zone" in model.keys()
            True
        """
    def values(self) -> list[IDFCollection[IDFObject]]:  # type: ignore[override]
        """Return list of non-empty collections.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> len(model.values()) >= 1
            True
        """
    def items(self) -> list[tuple[str, IDFCollection[IDFObject]]]:  # type: ignore[override]
        """Return list of (object_type, collection) pairs for non-empty collections.

        Examples:
            >>> from idfkit import new_document
            >>> model = new_document()
            >>> model.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> "Zone" in [t for t, _ in model.items()]
            True
        """
    def describe(self, obj_type: str) -> ObjectDescription:
        """Get detailed field information for an object type.

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
            UnknownObjectTypeError: If the object type is not found in the schema

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

    def add(
        self,
        obj_type: str,
        name: str = ...,
        fields: dict[str, Any] | None = ...,
        *,
        validate: bool = ...,
        **kwargs: Any,
    ) -> IDFObject:
        """Add a new object to the document.

        Args:
            obj_type: Object type (e.g., "Zone")
            name: Object name (optional for object types without a name field,
                such as Timestep, SimulationControl, GlobalGeometryRules)
            fields: Field values as a dict, useful when field names are
                computed dynamically. Equivalent to passing the same keys
                as ``**kwargs``; merged before ``kwargs`` so explicit
                kwargs win on conflict.
            validate: If True (default), validate the object against schema before adding.
                Raises ValidationFailedError if validation fails. Set to False for
                bulk operations where performance matters.
            **kwargs: Additional field values

        Returns:
            The created IDFObject

        Raises:
            UnknownObjectTypeError: If the object type is not recognised by
                the schema
            DuplicateObjectError: If a singleton object type (marked with
                schema ``maxProperties == 1``) already exists in the document
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
    def addidfobject(self, obj: IDFObject) -> IDFObject:
        """Add an existing IDFObject to the document.

        Overrides the eppy-compatibility method from
        :class:`~idfkit._compat.EppyDocumentMixin` to keep ``_version`` in sync
        when a ``Version`` object is added (e.g. during parsing or copy).
        """
    def removeidfobject(self, obj: IDFObject) -> None:
        """Remove an object from the document.

        !!! tip
            This method is also the recommended idfkit API.  Alternatively,
            use `popidfobject()` to remove by index.
        """
    def rename(self, obj_type: str, old_name: str, new_name: str) -> None:
        """Rename an object and update all references.

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
    def notify_name_change(self, obj: IDFObject, old_name: str, new_name: str) -> None:
        """Called by IDFObject._set_name when a name changes."""
    def notify_reference_change(self, obj: IDFObject, field_name: str, old_value: Any, new_value: Any) -> None:
        """Called by IDFObject._set_field when a reference field changes."""
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
    @property
    def schedules_dict(self) -> dict[str, IDFObject]:
        """Get dict mapping schedule names to schedule objects.

        This is a cached property for fast schedule lookup.
        """
    def get_schedule(self, name: str) -> IDFObject | None:
        """Get a schedule by name (case-insensitive)."""
    def get_used_schedules(self) -> set[str]:
        """Get names of schedules actually used in the model.

        Uses the reference graph for O(1) lookup per schedule.
        """
    def get_zone_surfaces(self, zone_name: str) -> list[IDFObject]:
        """Get all surfaces belonging to a zone."""
    @property
    def all_objects(self) -> Iterator[IDFObject]:
        """Iterate over all objects in the document."""
    def objects_by_type(self) -> Iterator[tuple[str, IDFCollection[IDFObject]]]:
        """Iterate over (type, collection) pairs."""
    def expand(self, *, energyplus: EnergyPlusConfig | None = ..., timeout: float = ...) -> IDFDocument[Strict]:
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
            A new [IDFDocument][idfkit.document.IDFDocument] with all template objects expanded.

        Raises:
            EnergyPlusNotFoundError: If no EnergyPlus installation is found.
            ExpandObjectsError: If the preprocessor fails.

        Examples:
            Expand HVACTemplate objects into low-level HVAC components
            so you can inspect or modify the resulting system:

                ```python
                model = load_idf("5ZoneAirCooled_HVACTemplate.idf")
                expanded = model.expand()
                for ideal in expanded["ZoneHVAC:IdealLoadsAirSystem"]:
                    print(ideal.name, ideal.cooling_limit)
                ```

            Point to a specific EnergyPlus installation:

                ```python
                from idfkit.simulation import find_energyplus
                ep = find_energyplus(version=(24, 1, 0))
                expanded = model.expand(energyplus=ep)
                ```
        """
    def copy(self) -> IDFDocument[Strict]:
        """Create a deep copy of the document.

        The copy is independent -- modifying the copy does not affect
        the original.  Strict mode is preserved, and so is the source
        formatting of a ``preserve_formatting=True`` read: the copy writes
        the same bytes the original would, and :meth:`region_of` and
        :meth:`render_object` answer for its objects.

        ``copy.deepcopy`` and ``pickle`` give the same result through the
        default machinery, which needs no hooks here: every slot of a document
        copies correctly on its own, and the schema travels by version (see
        :meth:`EpJSONSchema.__reduce__ <idfkit.schema.EpJSONSchema.__reduce__>`).
        This method is the faster of the two, as it rebuilds the model
        object by object instead of walking every field through the memo.

        Examples:
            Create a copy for parametric comparison (e.g., testing
            different insulation strategies without altering the baseline):

            >>> from idfkit import new_document
            >>> baseline = new_document()
            >>> baseline.add("Zone", "Office")  # doctest: +ELLIPSIS
            Zone('Office')
            >>> variant = baseline.copy()
            >>> len(variant) == len(baseline)
            True
            >>> variant.add("Zone", "Server_Room")  # doctest: +ELLIPSIS
            Zone('Server_Room')
            >>> len(variant) == len(baseline) + 1
            True
        """

    @property
    def air_conditioner_variable_refrigerant_flow_fluid_temperature_control_hrs(
        self,
    ) -> IDFCollection[AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR]:
        """All ``AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR`` objects in the document. This is a key object in the new physics based VRF Heat Recovery (HR) model applicable for Fluid Temperature Control. It describes the VRF HR system excluding the performance of indoor units. Indoor..."""
    @property
    def air_conditioner_variable_refrigerant_flow_fluid_temperature_controls(
        self,
    ) -> IDFCollection[AirConditionerVariableRefrigerantFlowFluidTemperatureControl]:
        """All ``AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl`` objects in the document. This is a key object in the new physics based VRF model applicable for Fluid Temperature Control It describes the Variable Refrigerant Flow system excluding the performance of indoor units Indoor u..."""
    @property
    def air_conditioner_variable_refrigerant_flows(self) -> IDFCollection[AirConditionerVariableRefrigerantFlow]:
        """All ``AirConditioner:VariableRefrigerantFlow`` objects in the document. Variable refrigerant flow (VRF) air-to-air heat pump condensing unit (includes one or more electric compressors and outdoor fan). Serves one or more VRF zone terminal units. See ZoneHVAC:TerminalUn..."""
    @property
    def air_loop_hvac_controller_lists(self) -> IDFCollection[AirLoopHVACControllerList]:
        """All ``AirLoopHVAC:ControllerList`` objects in the document. List controllers in order of control sequence"""
    @property
    def air_loop_hvac_dedicated_outdoor_air_systems(self) -> IDFCollection[AirLoopHVACDedicatedOutdoorAirSystem]:
        """All ``AirLoopHVAC:DedicatedOutdoorAirSystem`` objects in the document. Defines a central forced air system to provide dedicated outdoor air to multiple AirLoopHVACs."""
    @property
    def air_loop_hvac_exhaust_systems(self) -> IDFCollection[AirLoopHVACExhaustSystem]:
        """All ``AirLoopHVAC:ExhaustSystem`` objects in the document. Defines a general exhaust system with a central exhaust fan drawing from one or more ZoneHVAC:ExhaustControl outlet nodes via an AirLoopHVAC:ZoneMixer."""
    @property
    def air_loop_hvac_mixers(self) -> IDFCollection[AirLoopHVACMixer]:
        """All ``AirLoopHVAC:Mixer`` objects in the document. Mix N inlet air streams from Relief Air Stream Node in OutdoorAir:Mixer objects served by AirLoopHVAC objects listed in AirLoopHVAC:DedicatedOutdoorAirSystem into one (currently 10 as default, but ..."""
    @property
    def air_loop_hvac_outdoor_air_system_equipment_lists(
        self,
    ) -> IDFCollection[AirLoopHVACOutdoorAirSystemEquipmentList]:
        """All ``AirLoopHVAC:OutdoorAirSystem:EquipmentList`` objects in the document. List equipment in simulation order"""
    @property
    def air_loop_hvac_outdoor_air_systems(self) -> IDFCollection[AirLoopHVACOutdoorAirSystem]:
        """All ``AirLoopHVAC:OutdoorAirSystem`` objects in the document. Outdoor air subsystem for an AirLoopHVAC. Includes an outdoor air mixing box and optional outdoor air conditioning equipment such as heat recovery, preheat, and precool coils. From the perspective ..."""
    @property
    def air_loop_hvac_return_paths(self) -> IDFCollection[AirLoopHVACReturnPath]:
        """All ``AirLoopHVAC:ReturnPath`` objects in the document. A return air path can only contain one AirLoopHVAC:ZoneMixer and one or more AirLoopHVAC:ReturnPlenum objects."""
    @property
    def air_loop_hvac_return_plenums(self) -> IDFCollection[AirLoopHVACReturnPlenum]:
        """All ``AirLoopHVAC:ReturnPlenum`` objects in the document. Connects N zone inlet air streams, through zone return plenum, to outlet (currently 500 per air loop) Node names cannot be duplicated within a single plenum list."""
    @property
    def air_loop_hvac_splitters(self) -> IDFCollection[AirLoopHVACSplitter]:
        """All ``AirLoopHVAC:Splitter`` objects in the document. Split one air stream from AirLoopHVAC:DedicatedOutdoorAirSystem outlet node into N outlet streams (currently 10 as default, but extensible). Node names should be Outdoor Air Stream Node Name in Out..."""
    @property
    def air_loop_hvac_supply_paths(self) -> IDFCollection[AirLoopHVACSupplyPath]:
        """All ``AirLoopHVAC:SupplyPath`` objects in the document. A supply path can only contain AirLoopHVAC:ZoneSplitter and AirLoopHVAC:SupplyPlenum objects which may be in series or parallel."""
    @property
    def air_loop_hvac_supply_plenums(self) -> IDFCollection[AirLoopHVACSupplyPlenum]:
        """All ``AirLoopHVAC:SupplyPlenum`` objects in the document. Connects 1 zone inlet air stream, through zone supply plenum, to one or more outlets. Node names cannot be duplicated within a single supply plenum list."""
    @property
    def air_loop_hvac_unitary_furnace_heat_cools(self) -> IDFCollection[AirLoopHVACUnitaryFurnaceHeatCool]:
        """All ``AirLoopHVAC:Unitary:Furnace:HeatCool`` objects in the document. Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam), and optional rehe..."""
    @property
    def air_loop_hvac_unitary_furnace_heat_onlies(self) -> IDFCollection[AirLoopHVACUnitaryFurnaceHeatOnly]:
        """All ``AirLoopHVAC:Unitary:Furnace:HeatOnly`` objects in the document. Unitary system, heating-only with constant volume supply fan (continuous or cycling) and heating coil (gas, electric, hot water, or steam). Identical to AirLoopHVAC:UnitaryHeatOnly."""
    @property
    def air_loop_hvac_unitary_heat_cool_vav_changeover_bypasses(
        self,
    ) -> IDFCollection[AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass]:
        """All ``AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass`` objects in the document. Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, steam, or DX air-to-air heat..."""
    @property
    def air_loop_hvac_unitary_heat_cools(self) -> IDFCollection[AirLoopHVACUnitaryHeatCool]:
        """All ``AirLoopHVAC:UnitaryHeatCool`` objects in the document. Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam), and optional rehe..."""
    @property
    def air_loop_hvac_unitary_heat_onlies(self) -> IDFCollection[AirLoopHVACUnitaryHeatOnly]:
        """All ``AirLoopHVAC:UnitaryHeatOnly`` objects in the document. Unitary system, heating-only with constant volume supply fan (continuous or cycling) and heating coil (gas, electric, hot water, or steam). Identical to AirLoopHVAC:Unitary:Furnace:HeatOnly."""
    @property
    def air_loop_hvac_unitary_heat_pump_air_to_air_multi_speeds(
        self,
    ) -> IDFCollection[AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed]:
        """All ``AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed`` objects in the document. Unitary system, heating and cooling, multi-speed with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (DX air-to-air heat pump, gas, electric, h..."""
    @property
    def air_loop_hvac_unitary_heat_pump_air_to_airs(self) -> IDFCollection[AirLoopHVACUnitaryHeatPumpAirToAir]:
        """All ``AirLoopHVAC:UnitaryHeatPump:AirToAir`` objects in the document. Unitary heat pump system, heating and cooling, single-speed with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), and supplemental heating coil (gas, electric..."""
    @property
    def air_loop_hvac_unitary_heat_pump_water_to_airs(self) -> IDFCollection[AirLoopHVACUnitaryHeatPumpWaterToAir]:
        """All ``AirLoopHVAC:UnitaryHeatPump:WaterToAir`` objects in the document. Unitary heat pump system, heating and cooling, single-speed with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, DX heating coil (water-to-air heat pump), an..."""
    @property
    def air_loop_hvac_unitary_systems(self) -> IDFCollection[AirLoopHVACUnitarySystem]:
        """All ``AirLoopHVAC:UnitarySystem`` objects in the document. AirloopHVAC:UnitarySystem is a generic HVAC system type that allows any configuration of coils and/or fan. This object is a replacement of other AirloopHVAC objects. This object can be used in outd..."""
    @property
    def air_loop_hvac_zone_mixers(self) -> IDFCollection[AirLoopHVACZoneMixer]:
        """All ``AirLoopHVAC:ZoneMixer`` objects in the document. Mix N inlet air streams into one (currently 500 per air loop, but extensible). Node names cannot be duplicated within a single zone mixer (AirLoopHVAC:ZoneMixer) list."""
    @property
    def air_loop_hvac_zone_splitters(self) -> IDFCollection[AirLoopHVACZoneSplitter]:
        """All ``AirLoopHVAC:ZoneSplitter`` objects in the document. Split one air stream into N outlet streams (currently 500 per air loop, but extensible). Node names cannot be duplicated within a single zone splitter (AirLoopHVAC:ZoneSplitter) list."""
    @property
    def air_loop_hvacs(self) -> IDFCollection[AirLoopHVAC]:
        """All ``AirLoopHVAC`` objects in the document. Defines a central forced air system."""
    @property
    def air_terminal_dual_duct_constant_volumes(self) -> IDFCollection[AirTerminalDualDuctConstantVolume]:
        """All ``AirTerminal:DualDuct:ConstantVolume`` objects in the document. Central air system terminal unit, dual duct, constant volume."""
    @property
    def air_terminal_dual_duct_vav_outdoor_airs(self) -> IDFCollection[AirTerminalDualDuctVAVOutdoorAir]:
        """All ``AirTerminal:DualDuct:VAV:OutdoorAir`` objects in the document. Central air system terminal unit, dual duct, variable volume with special controls. One VAV duct is controlled to supply ventilation air and the other VAV duct is controlled to meet the zone coolin..."""
    @property
    def air_terminal_dual_duct_vavs(self) -> IDFCollection[AirTerminalDualDuctVAV]:
        """All ``AirTerminal:DualDuct:VAV`` objects in the document. Central air system terminal unit, dual duct, variable volume."""
    @property
    def air_terminal_single_duct_constant_volume_cooled_beams(
        self,
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeCooledBeam]:
        """All ``AirTerminal:SingleDuct:ConstantVolume:CooledBeam`` objects in the document. Central air system terminal unit, single duct, constant volume, with cooled beam (active or passive)."""
    @property
    def air_terminal_single_duct_constant_volume_four_pipe_beams(
        self,
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeFourPipeBeam]:
        """All ``AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam`` objects in the document. Central air system terminal unit, single duct, constant volume, with heating and/or cooling. Operates as two-pipe unit if heating or cooling water is omitted. Heating and/or cooling can be schedule..."""
    @property
    def air_terminal_single_duct_constant_volume_four_pipe_inductions(
        self,
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeFourPipeInduction]:
        """All ``AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction`` objects in the document. Central air system terminal unit, single duct, variable volume, induction unit with hot water reheat coil and chilled water recool coil."""
    @property
    def air_terminal_single_duct_constant_volume_no_reheats(
        self,
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeNoReheat]:
        """All ``AirTerminal:SingleDuct:ConstantVolume:NoReheat`` objects in the document. Central air system terminal unit, single duct, constant volume, without reheat coil"""
    @property
    def air_terminal_single_duct_constant_volume_reheats(
        self,
    ) -> IDFCollection[AirTerminalSingleDuctConstantVolumeReheat]:
        """All ``AirTerminal:SingleDuct:ConstantVolume:Reheat`` objects in the document. Central air system terminal unit, single duct, constant volume, with reheat coil (hot water, electric, gas, or steam)."""
    @property
    def air_terminal_single_duct_mixers(self) -> IDFCollection[AirTerminalSingleDuctMixer]:
        """All ``AirTerminal:SingleDuct:Mixer`` objects in the document. The mixer air terminal unit provides a means of supplying central system air to the air inlet or outlet side of a zoneHVAC equipment such as a four pipe fan coil unit. Normally the central air woul..."""
    @property
    def air_terminal_single_duct_parallel_piu_reheats(self) -> IDFCollection[AirTerminalSingleDuctParallelPIUReheat]:
        """All ``AirTerminal:SingleDuct:ParallelPIU:Reheat`` objects in the document. Central air system terminal unit, single duct, variable volume, parallel powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam)."""
    @property
    def air_terminal_single_duct_series_piu_reheats(self) -> IDFCollection[AirTerminalSingleDuctSeriesPIUReheat]:
        """All ``AirTerminal:SingleDuct:SeriesPIU:Reheat`` objects in the document. Central air system terminal unit, single duct, variable volume, series powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam)."""
    @property
    def air_terminal_single_duct_user_defineds(self) -> IDFCollection[AirTerminalSingleDuctUserDefined]:
        """All ``AirTerminal:SingleDuct:UserDefined`` objects in the document. Defines a generic single duct air terminal unit for custom modeling using Energy Management System or External Interface"""
    @property
    def air_terminal_single_duct_vav_heat_and_cool_no_reheats(
        self,
    ) -> IDFCollection[AirTerminalSingleDuctVAVHeatAndCoolNoReheat]:
        """All ``AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat`` objects in the document. Central air system terminal unit, single duct, variable volume for both cooling and heating, with no reheat coil."""
    @property
    def air_terminal_single_duct_vav_heat_and_cool_reheats(
        self,
    ) -> IDFCollection[AirTerminalSingleDuctVAVHeatAndCoolReheat]:
        """All ``AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat`` objects in the document. Central air system terminal unit, single duct, variable volume for both cooling and heating, with reheat coil (hot water, electric, gas, or steam)."""
    @property
    def air_terminal_single_duct_vav_no_reheats(self) -> IDFCollection[AirTerminalSingleDuctVAVNoReheat]:
        """All ``AirTerminal:SingleDuct:VAV:NoReheat`` objects in the document. Central air system terminal unit, single duct, variable volume, with no reheat coil."""
    @property
    def air_terminal_single_duct_vav_reheat_variable_speed_fans(
        self,
    ) -> IDFCollection[AirTerminalSingleDuctVAVReheatVariableSpeedFan]:
        """All ``AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan`` objects in the document. Central air system terminal unit, single duct, variable volume, with reheat coil (hot water, electric, gas, or steam) and variable-speed fan. These units are usually employed in underfloor air dist..."""
    @property
    def air_terminal_single_duct_vav_reheats(self) -> IDFCollection[AirTerminalSingleDuctVAVReheat]:
        """All ``AirTerminal:SingleDuct:VAV:Reheat`` objects in the document. Central air system terminal unit, single duct, variable volume, with reheat coil (hot water, electric, gas, or steam)."""
    @property
    def airflow_network_distribution_component_coils(self) -> IDFCollection[AirflowNetworkDistributionComponentCoil]:
        """All ``AirflowNetwork:Distribution:Component:Coil`` objects in the document. This object defines the name of a coil used in an air loop."""
    @property
    def airflow_network_distribution_component_constant_pressure_drops(
        self,
    ) -> IDFCollection[AirflowNetworkDistributionComponentConstantPressureDrop]:
        """All ``AirflowNetwork:Distribution:Component:ConstantPressureDrop`` objects in the document. This object defines the characteristics of a constant pressure drop component (e.g. filter). Each node connected to this object can not be a node of mixer, splitter, a node of air primary loop, or ..."""
    @property
    def airflow_network_distribution_component_ducts(self) -> IDFCollection[AirflowNetworkDistributionComponentDuct]:
        """All ``AirflowNetwork:Distribution:Component:Duct`` objects in the document. This object defines the relationship between pressure and air flow through the duct."""
    @property
    def airflow_network_distribution_component_fans(self) -> IDFCollection[AirflowNetworkDistributionComponentFan]:
        """All ``AirflowNetwork:Distribution:Component:Fan`` objects in the document. This object defines the name of the supply Air Fan used in an Air loop."""
    @property
    def airflow_network_distribution_component_heat_exchangers(
        self,
    ) -> IDFCollection[AirflowNetworkDistributionComponentHeatExchanger]:
        """All ``AirflowNetwork:Distribution:Component:HeatExchanger`` objects in the document. This object defines the name of an air-to-air heat exchanger used in an air loop."""
    @property
    def airflow_network_distribution_component_leakage_ratios(
        self,
    ) -> IDFCollection[AirflowNetworkDistributionComponentLeakageRatio]:
        """All ``AirflowNetwork:Distribution:Component:LeakageRatio`` objects in the document. This object is used to define supply and return air leaks with respect to the fan's maximum air flow rate."""
    @property
    def airflow_network_distribution_component_leaks(self) -> IDFCollection[AirflowNetworkDistributionComponentLeak]:
        """All ``AirflowNetwork:Distribution:Component:Leak`` objects in the document. This object defines the characteristics of a supply or return air leak."""
    @property
    def airflow_network_distribution_component_outdoor_air_flows(
        self,
    ) -> IDFCollection[AirflowNetworkDistributionComponentOutdoorAirFlow]:
        """All ``AirflowNetwork:Distribution:Component:OutdoorAirFlow`` objects in the document. This object includes the outdoor air flow rate set by the Controller:OutdoorAir object in the airflow network."""
    @property
    def airflow_network_distribution_component_relief_air_flows(
        self,
    ) -> IDFCollection[AirflowNetworkDistributionComponentReliefAirFlow]:
        """All ``AirflowNetwork:Distribution:Component:ReliefAirFlow`` objects in the document. This object allows variation of air flow rate to perform pressure."""
    @property
    def airflow_network_distribution_component_terminal_units(
        self,
    ) -> IDFCollection[AirflowNetworkDistributionComponentTerminalUnit]:
        """All ``AirflowNetwork:Distribution:Component:TerminalUnit`` objects in the document. This object defines the name of a terminal unit in an air loop."""
    @property
    def airflow_network_distribution_duct_sizings(self) -> IDFCollection[AirflowNetworkDistributionDuctSizing]:
        """All ``AirflowNetwork:Distribution:DuctSizing`` objects in the document. This object defines required parameters for duct sizing in an Airflow Network simulation. To activate duct sizing, see AirflowNetwork:SimulationControl Do Distribution Duct Sizing Calculation."""
    @property
    def airflow_network_distribution_duct_view_factors(
        self,
    ) -> IDFCollection[AirflowNetworkDistributionDuctViewFactors]:
        """All ``AirflowNetwork:Distribution:DuctViewFactors`` objects in the document. This object is used to allow user-defined view factors to be used for duct-surface radiation calculations. All surfaces must be in the same enclosure."""
    @property
    def airflow_network_distribution_linkages(self) -> IDFCollection[AirflowNetworkDistributionLinkage]:
        """All ``AirflowNetwork:Distribution:Linkage`` objects in the document. This object defines the connection between two nodes and a component."""
    @property
    def airflow_network_distribution_nodes(self) -> IDFCollection[AirflowNetworkDistributionNode]:
        """All ``AirflowNetwork:Distribution:Node`` objects in the document. This object represents an air distribution node in the AirflowNetwork model."""
    @property
    def airflow_network_intra_zone_linkages(self) -> IDFCollection[AirflowNetworkIntraZoneLinkage]:
        """All ``AirflowNetwork:IntraZone:Linkage`` objects in the document. This object defines the connection between two nodes and a component used in the combination of RoomAir and AirflowNetwork model."""
    @property
    def airflow_network_intra_zone_nodes(self) -> IDFCollection[AirflowNetworkIntraZoneNode]:
        """All ``AirflowNetwork:IntraZone:Node`` objects in the document. This object represents a node in a zone in the combination of RoomAir and AirflowNetwork model."""
    @property
    def airflow_network_multi_zone_component_detailed_openings(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneComponentDetailedOpening]:
        """All ``AirflowNetwork:MultiZone:Component:DetailedOpening`` objects in the document. This object specifies the properties of airflow through windows and doors (window, door and glass door heat transfer subsurfaces) when they are closed or open."""
    @property
    def airflow_network_multi_zone_component_horizontal_openings(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneComponentHorizontalOpening]:
        """All ``AirflowNetwork:MultiZone:Component:HorizontalOpening`` objects in the document. This object specifies the properties of air flow through a horizontal opening"""
    @property
    def airflow_network_multi_zone_component_simple_openings(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneComponentSimpleOpening]:
        """All ``AirflowNetwork:MultiZone:Component:SimpleOpening`` objects in the document. This object specifies the properties of air flow through windows and doors (window, door and glass door heat transfer subsurfaces) when they are closed or open."""
    @property
    def airflow_network_multi_zone_component_zone_exhaust_fans(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneComponentZoneExhaustFan]:
        """All ``AirflowNetwork:MultiZone:Component:ZoneExhaustFan`` objects in the document. This object specifies the additional properties for a zone exhaust fan to perform multizone airflow calculations."""
    @property
    def airflow_network_multi_zone_external_nodes(self) -> IDFCollection[AirflowNetworkMultiZoneExternalNode]:
        """All ``AirflowNetwork:MultiZone:ExternalNode`` objects in the document. This object defines outdoor environmental conditions outside of the building."""
    @property
    def airflow_network_multi_zone_reference_crack_conditions(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneReferenceCrackConditions]:
        """All ``AirflowNetwork:MultiZone:ReferenceCrackConditions`` objects in the document. This object specifies the conditions under which the air mass flow coefficient was measured."""
    @property
    def airflow_network_multi_zone_specified_flow_rates(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneSpecifiedFlowRate]:
        """All ``AirflowNetwork:MultiZone:SpecifiedFlowRate`` objects in the document. This object is used to define specified flow through a linkage."""
    @property
    def airflow_network_multi_zone_surface_cracks(self) -> IDFCollection[AirflowNetworkMultiZoneSurfaceCrack]:
        """All ``AirflowNetwork:MultiZone:Surface:Crack`` objects in the document. This object specifies the properties of airflow through a crack."""
    @property
    def airflow_network_multi_zone_surface_effective_leakage_areas(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea]:
        """All ``AirflowNetwork:MultiZone:Surface:EffectiveLeakageArea`` objects in the document. This object is used to define surface air leakage."""
    @property
    def airflow_network_multi_zone_surfaces(self) -> IDFCollection[AirflowNetworkMultiZoneSurface]:
        """All ``AirflowNetwork:MultiZone:Surface`` objects in the document. This object specifies the properties of a surface linkage through which air flows. Airflow Report: Node 1 as an inside face zone; Node 2 as an outside face zone or external node."""
    @property
    def airflow_network_multi_zone_wind_pressure_coefficient_arrays(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneWindPressureCoefficientArray]:
        """All ``AirflowNetwork:MultiZone:WindPressureCoefficientArray`` objects in the document. Used only if Wind Pressure Coefficient (WPC) Type = Input in the AirflowNetwork:SimulationControl object. Number of WPC Values in the corresponding AirflowNetwork:MultiZone:WindPressureCoefficientV..."""
    @property
    def airflow_network_multi_zone_wind_pressure_coefficient_values(
        self,
    ) -> IDFCollection[AirflowNetworkMultiZoneWindPressureCoefficientValues]:
        """All ``AirflowNetwork:MultiZone:WindPressureCoefficientValues`` objects in the document. Used only if Wind Pressure Coefficient (WPC) Type = INPUT in the AirflowNetwork:SimulationControl object. The number of WPC numeric inputs must correspond to the number of wind direction inputs in ..."""
    @property
    def airflow_network_multi_zone_zones(self) -> IDFCollection[AirflowNetworkMultiZoneZone]:
        """All ``AirflowNetwork:MultiZone:Zone`` objects in the document. This object is used to simultaneously control a thermal zone's window and door openings, both exterior and interior."""
    @property
    def airflow_network_occupant_ventilation_controls(self) -> IDFCollection[AirflowNetworkOccupantVentilationControl]:
        """All ``AirflowNetwork:OccupantVentilationControl`` objects in the document. This object is used to provide advanced thermal comfort control of window opening and closing for both exterior and interior windows."""
    @property
    def airflow_network_simulation_controls(self) -> IDFCollection[AirflowNetworkSimulationControl]:
        """All ``AirflowNetwork:SimulationControl`` objects in the document. This object defines the global parameters used in an Airflow Network simulation."""
    @property
    def airflow_network_zone_control_pressure_controllers(
        self,
    ) -> IDFCollection[AirflowNetworkZoneControlPressureController]:
        """All ``AirflowNetwork:ZoneControl:PressureController`` objects in the document. This object is used to control a zone to a specified indoor pressure using the AirflowNetwork model. The specified pressure setpoint is used to control the zone exhaust fan flow rate in a controlle..."""
    @property
    def availability_manager_assignment_lists(self) -> IDFCollection[AvailabilityManagerAssignmentList]:
        """All ``AvailabilityManagerAssignmentList`` objects in the document. Defines the applicable managers used for an AirLoopHVAC or PlantLoop. The priority of availability managers is based on a set of rules and are specific to the type of loop. The output from each ava..."""
    @property
    def availability_manager_differential_thermostats(self) -> IDFCollection[AvailabilityManagerDifferentialThermostat]:
        """All ``AvailabilityManager:DifferentialThermostat`` objects in the document. Overrides fan/pump schedules depending on temperature difference between two nodes."""
    @property
    def availability_manager_high_temperature_turn_offs(
        self,
    ) -> IDFCollection[AvailabilityManagerHighTemperatureTurnOff]:
        """All ``AvailabilityManager:HighTemperatureTurnOff`` objects in the document. Overrides fan/pump schedules depending on temperature at sensor node."""
    @property
    def availability_manager_high_temperature_turn_ons(self) -> IDFCollection[AvailabilityManagerHighTemperatureTurnOn]:
        """All ``AvailabilityManager:HighTemperatureTurnOn`` objects in the document. Overrides fan/pump schedules depending on temperature at sensor node."""
    @property
    def availability_manager_hybrid_ventilations(self) -> IDFCollection[AvailabilityManagerHybridVentilation]:
        """All ``AvailabilityManager:HybridVentilation`` objects in the document. Depending on zone and outdoor conditions overrides window/door opening controls to maximize natural ventilation and turn off an HVAC system when ventilation control conditions are met. This object ..."""
    @property
    def availability_manager_low_temperature_turn_offs(self) -> IDFCollection[AvailabilityManagerLowTemperatureTurnOff]:
        """All ``AvailabilityManager:LowTemperatureTurnOff`` objects in the document. Overrides fan/pump schedules depending on temperature at sensor node."""
    @property
    def availability_manager_low_temperature_turn_ons(self) -> IDFCollection[AvailabilityManagerLowTemperatureTurnOn]:
        """All ``AvailabilityManager:LowTemperatureTurnOn`` objects in the document. Overrides fan/pump schedules depending on temperature at sensor node."""
    @property
    def availability_manager_night_cycles(self) -> IDFCollection[AvailabilityManagerNightCycle]:
        """All ``AvailabilityManager:NightCycle`` objects in the document. Determines the availability of a loop or system: whether it is on or off. Depending on zone temperatures, overrides Schedules and forces system Fans on."""
    @property
    def availability_manager_night_ventilations(self) -> IDFCollection[AvailabilityManagerNightVentilation]:
        """All ``AvailabilityManager:NightVentilation`` objects in the document. depending on zone and outdoor conditions overrides fan schedule to do precooling with outdoor air"""
    @property
    def availability_manager_optimum_starts(self) -> IDFCollection[AvailabilityManagerOptimumStart]:
        """All ``AvailabilityManager:OptimumStart`` objects in the document. Determines the optimal start of HVAC systems before occupancy."""
    @property
    def availability_manager_scheduled_offs(self) -> IDFCollection[AvailabilityManagerScheduledOff]:
        """All ``AvailabilityManager:ScheduledOff`` objects in the document. Determines the availability of a loop or system: only controls the turn off action. Schedule overrides fan/pump schedule."""
    @property
    def availability_manager_scheduled_ons(self) -> IDFCollection[AvailabilityManagerScheduledOn]:
        """All ``AvailabilityManager:ScheduledOn`` objects in the document. Determines the availability of a loop or system: only controls the turn on action. Schedule overrides fan/pump schedule."""
    @property
    def availability_manager_scheduleds(self) -> IDFCollection[AvailabilityManagerScheduled]:
        """All ``AvailabilityManager:Scheduled`` objects in the document. Determines the availability of a loop or system: whether it is on or off. Schedule overrides fan/pump schedule."""
    @property
    def boiler_hot_waters(self) -> IDFCollection[BoilerHotWater]:
        """All ``Boiler:HotWater`` objects in the document. This boiler model is an adaptation of the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Boiler performance curves are generated by fitting catalog data to polyn..."""
    @property
    def boiler_steams(self) -> IDFCollection[BoilerSteam]:
        """All ``Boiler:Steam`` objects in the document. This boiler model is an adaptation of the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Boiler performance curves are generated by fitting catalog data to third..."""
    @property
    def branch_lists(self) -> IDFCollection[BranchList]:
        """All ``BranchList`` objects in the document. Branches MUST be listed in Flow order: Inlet branch, then parallel branches, then Outlet branch. Branches are simulated in the order listed. Branch names cannot be duplicated within a single branch..."""
    @property
    def branches(self) -> IDFCollection[Branch]:
        """All ``Branch`` objects in the document. List components on the branch in simulation and connection order Note: this should NOT include splitters or mixers which define endpoints of branches"""
    @property
    def building(self) -> IDFCollection[Building]:
        """All ``Building`` objects in the document. Describes parameters that are used during the simulation of the building. There are necessary correlations between the entries for this object and some entries in the Site:WeatherStation and Site:H..."""
    @property
    def building_surface_detaileds(self) -> IDFCollection[BuildingSurfaceDetailed]:
        """All ``BuildingSurface:Detailed`` objects in the document. Allows for detailed entry of building heat transfer surfaces. Does not include subsurfaces such as windows or doors."""
    @property
    def building_surfaces(self) -> IDFCollection[BuildingSurfaceDetailed]:
        """All ``BuildingSurface:Detailed`` objects in the document. Allows for detailed entry of building heat transfer surfaces. Does not include subsurfaces such as windows or doors."""
    @property
    def buildings(self) -> IDFCollection[Building]:
        """All ``Building`` objects in the document. Describes parameters that are used during the simulation of the building. There are necessary correlations between the entries for this object and some entries in the Site:WeatherStation and Site:H..."""
    @property
    def ceiling_adiabatics(self) -> IDFCollection[CeilingAdiabatic]:
        """All ``Ceiling:Adiabatic`` objects in the document. Allows for simplified entry of interior ceilings."""
    @property
    def ceiling_interzones(self) -> IDFCollection[CeilingInterzone]:
        """All ``Ceiling:Interzone`` objects in the document. Allows for simplified entry of ceilings using adjacent zone (interzone) heat transfer - adjacent surface should be a floor"""
    @property
    def central_heat_pump_systems(self) -> IDFCollection[CentralHeatPumpSystem]:
        """All ``CentralHeatPumpSystem`` objects in the document. This chiller bank can contain multiple chiller heaters and heat pump performance objects. Its function is to encapsulate the extra controls needed to turn individual modules on/off and whether they..."""
    @property
    def chiller_absorption_indirects(self) -> IDFCollection[ChillerAbsorptionIndirect]:
        """All ``Chiller:Absorption:Indirect`` objects in the document. This indirect absorption chiller model is an enhanced model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to th..."""
    @property
    def chiller_absorptions(self) -> IDFCollection[ChillerAbsorption]:
        """All ``Chiller:Absorption`` objects in the document. This indirect absorption chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to ..."""
    @property
    def chiller_combustion_turbines(self) -> IDFCollection[ChillerCombustionTurbine]:
        """All ``Chiller:CombustionTurbine`` objects in the document. This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomi..."""
    @property
    def chiller_constant_cops(self) -> IDFCollection[ChillerConstantCOP]:
        """All ``Chiller:ConstantCOP`` objects in the document. This constant COP chiller model provides a means of quickly specifying a Chiller where performance data is not available."""
    @property
    def chiller_electric_ashrae205s(self) -> IDFCollection[ChillerElectricASHRAE205]:
        """All ``Chiller:Electric:ASHRAE205`` objects in the document. This chiller model utilizes ASHRAE Standard 205 compliant representations for chillers (Representation Specification RS0001)."""
    @property
    def chiller_electric_eirs(self) -> IDFCollection[ChillerElectricEIR]:
        """All ``Chiller:Electric:EIR`` objects in the document. This chiller model is the empirical model from the DOE-2 building Energy simulation program. Chiller performance at off-reference conditions is modeled using three polynomial equations. Three curve..."""
    @property
    def chiller_electric_reformulated_eirs(self) -> IDFCollection[ChillerElectricReformulatedEIR]:
        """All ``Chiller:Electric:ReformulatedEIR`` objects in the document. This chiller model is an empirical model, a reformulated version of Chiller:Electric:EIR where the performance is a function of condenser leaving fluid Temperature instead of condenser entering flu..."""
    @property
    def chiller_electrics(self) -> IDFCollection[ChillerElectric]:
        """All ``Chiller:Electric`` objects in the document. This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomi..."""
    @property
    def chiller_engine_drivens(self) -> IDFCollection[ChillerEngineDriven]:
        """All ``Chiller:EngineDriven`` objects in the document. This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomi..."""
    @property
    def chiller_heater_absorption_direct_fireds(self) -> IDFCollection[ChillerHeaterAbsorptionDirectFired]:
        """All ``ChillerHeater:Absorption:DirectFired`` objects in the document. Direct fired gas absorption chiller-heater using performance curves similar to DOE-2"""
    @property
    def chiller_heater_absorption_double_effects(self) -> IDFCollection[ChillerHeaterAbsorptionDoubleEffect]:
        """All ``ChillerHeater:Absorption:DoubleEffect`` objects in the document. Exhaust fired absorption chiller-heater using performance curves similar to DOE-2"""
    @property
    def chiller_heater_performance_electric_eirs(self) -> IDFCollection[ChillerHeaterPerformanceElectricEIR]:
        """All ``ChillerHeaterPerformance:Electric:EIR`` objects in the document. This chiller model is a generic chiller-heater where the cooling mode performance is a function of condenser entering or leaving fluid temperature and the heating mode performance is typically a fu..."""
    @property
    def coil_cooling_dx_curve_fit_operating_modes(self) -> IDFCollection[CoilCoolingDXCurveFitOperatingMode]:
        """All ``Coil:Cooling:DX:CurveFit:OperatingMode`` objects in the document. DX cooling coil performance for a single operating mode which may have one or more speeds."""
    @property
    def coil_cooling_dx_curve_fit_performances(self) -> IDFCollection[CoilCoolingDXCurveFitPerformance]:
        """All ``Coil:Cooling:DX:CurveFit:Performance`` objects in the document. DX cooling coil performance specification referencing one or more operating modes. Mode 1 is always the base design operating mode. Additional modes are optional states such as subcool reheat for h..."""
    @property
    def coil_cooling_dx_curve_fit_speeds(self) -> IDFCollection[CoilCoolingDXCurveFitSpeed]:
        """All ``Coil:Cooling:DX:CurveFit:Speed`` objects in the document. DX cooling coil performance for a single speed within a single operating mode."""
    @property
    def coil_cooling_dx_multi_speeds(self) -> IDFCollection[CoilCoolingDXMultiSpeed]:
        """All ``Coil:Cooling:DX:MultiSpeed`` objects in the document. Direct expansion (DX) cooling coil and condensing unit (includes electric or engine-driven compressor and condenser fan), multi-speed (or variable-speed). Optional moisture evaporation from wet coi..."""
    @property
    def coil_cooling_dx_single_speed_thermal_storages(self) -> IDFCollection[CoilCoolingDXSingleSpeedThermalStorage]:
        """All ``Coil:Cooling:DX:SingleSpeed:ThermalStorage`` objects in the document. Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), single-speed with packaged integrated thermal storage for cooling."""
    @property
    def coil_cooling_dx_single_speeds(self) -> IDFCollection[CoilCoolingDXSingleSpeed]:
        """All ``Coil:Cooling:DX:SingleSpeed`` objects in the document. Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), single-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles ..."""
    @property
    def coil_cooling_dx_two_speeds(self) -> IDFCollection[CoilCoolingDXTwoSpeed]:
        """All ``Coil:Cooling:DX:TwoSpeed`` objects in the document. Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-speed (or variable-speed). Requires two sets of performance data and will interpolate be..."""
    @property
    def coil_cooling_dx_two_stage_with_humidity_control_modes(
        self,
    ) -> IDFCollection[CoilCoolingDXTwoStageWithHumidityControlMode]:
        """All ``Coil:Cooling:DX:TwoStageWithHumidityControlMode`` objects in the document. Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-stage with humidity control mode (e.g. sub-cool or hot gas reheat). Optional inputs for ..."""
    @property
    def coil_cooling_dx_variable_refrigerant_flow_fluid_temperature_controls(
        self,
    ) -> IDFCollection[CoilCoolingDXVariableRefrigerantFlowFluidTemperatureControl]:
        """All ``Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl`` objects in the document. This is a key object in the new physics based VRF model applicable for Fluid Temperature Control. It describes the the indoor unit coil of the system at cooling mode. Used with ZoneHVAC:TerminalUni..."""
    @property
    def coil_cooling_dx_variable_refrigerant_flows(self) -> IDFCollection[CoilCoolingDXVariableRefrigerantFlow]:
        """All ``Coil:Cooling:DX:VariableRefrigerantFlow`` objects in the document. Variable refrigerant flow (VRF) direct expansion (DX) cooling coil. Used with ZoneHVAC:TerminalUnit:VariableRefrigerantFlow. Condensing unit is modeled separately, see AirConditioner:VariableRefrig..."""
    @property
    def coil_cooling_dx_variable_speeds(self) -> IDFCollection[CoilCoolingDXVariableSpeed]:
        """All ``Coil:Cooling:DX:VariableSpeed`` objects in the document. Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), variable-speed. Optional inputs for moisture evaporation from wet coil when compressor cycle..."""
    @property
    def coil_cooling_dxes(self) -> IDFCollection[CoilCoolingDX]:
        """All ``Coil:Cooling:DX`` objects in the document. New general DX cooling coil supporting on or more speeds and one or or operating modes. Includes DX evaporator coil, compressor, and condenser. Object is currently only supported by the AIRLOOPHVAC..."""
    @property
    def coil_cooling_water_detailed_geometries(self) -> IDFCollection[CoilCoolingWaterDetailedGeometry]:
        """All ``Coil:Cooling:Water:DetailedGeometry`` objects in the document. Chilled water cooling coil, detailed flat fin coil model for continuous plate fins, with inputs for detailed coil geometry specifications."""
    @property
    def coil_cooling_water_to_air_heat_pump_equation_fits(
        self,
    ) -> IDFCollection[CoilCoolingWaterToAirHeatPumpEquationFit]:
        """All ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` objects in the document. Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compresso..."""
    @property
    def coil_cooling_water_to_air_heat_pump_parameter_estimations(
        self,
    ) -> IDFCollection[CoilCoolingWaterToAirHeatPumpParameterEstimation]:
        """All ``Coil:Cooling:WaterToAirHeatPump:ParameterEstimation`` objects in the document. Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Optional inputs for moisture evaporation from wet coil when c..."""
    @property
    def coil_cooling_water_to_air_heat_pump_variable_speed_equation_fits(
        self,
    ) -> IDFCollection[CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit]:
        """All ``Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit`` objects in the document. Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), variable-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compres..."""
    @property
    def coil_cooling_waters(self) -> IDFCollection[CoilCoolingWater]:
        """All ``Coil:Cooling:Water`` objects in the document. Chilled water cooling coil, NTU-effectiveness model, with inputs for design entering and leaving conditions."""
    @property
    def coil_dx_ashrae205_performances(self) -> IDFCollection[CoilDXASHRAE205Performance]:
        """All ``Coil:DX:ASHRAE205:Performance`` objects in the document. DX coil performance specification referencing an ASHRAE Standard 205 compliant representation for air-to-air direct expansion refrigerant system (Representation Specification RS0004). As RS0004 fil..."""
    @property
    def coil_heating_desuperheaters(self) -> IDFCollection[CoilHeatingDesuperheater]:
        """All ``Coil:Heating:Desuperheater`` objects in the document. Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor..."""
    @property
    def coil_heating_dx_multi_speeds(self) -> IDFCollection[CoilHeatingDXMultiSpeed]:
        """All ``Coil:Heating:DX:MultiSpeed`` objects in the document. Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric or engine-driven compressor and outdoor fan), multi-speed (or variable-speed), with defrost controls..."""
    @property
    def coil_heating_dx_single_speeds(self) -> IDFCollection[CoilHeatingDXSingleSpeed]:
        """All ``Coil:Heating:DX:SingleSpeed`` objects in the document. Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric compressor and outdoor fan), single-speed, with defrost controls."""
    @property
    def coil_heating_dx_variable_refrigerant_flow_fluid_temperature_controls(
        self,
    ) -> IDFCollection[CoilHeatingDXVariableRefrigerantFlowFluidTemperatureControl]:
        """All ``Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl`` objects in the document. This is a key object in the new physics based VRF model applicable for Fluid Temperature Control. It describes the the indoor unit coil of the system at heating mode. Used with ZoneHVAC:TerminalUni..."""
    @property
    def coil_heating_dx_variable_refrigerant_flows(self) -> IDFCollection[CoilHeatingDXVariableRefrigerantFlow]:
        """All ``Coil:Heating:DX:VariableRefrigerantFlow`` objects in the document. Variable refrigerant flow (VRF) direct expansion (DX) heating coil (air-to-air heat pump). Used with ZoneHVAC:TerminalUnit:VariableRefrigerantFlow. Condensing unit is modeled separately, see AirCon..."""
    @property
    def coil_heating_dx_variable_speeds(self) -> IDFCollection[CoilHeatingDXVariableSpeed]:
        """All ``Coil:Heating:DX:VariableSpeed`` objects in the document. Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric compressor and outdoor fan), variable-speed, with defrost controls. Requires two to ten sets of perf..."""
    @property
    def coil_heating_electric_multi_stages(self) -> IDFCollection[CoilHeatingElectricMultiStage]:
        """All ``Coil:Heating:Electric:MultiStage`` objects in the document. Electric heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoin..."""
    @property
    def coil_heating_electrics(self) -> IDFCollection[CoilHeatingElectric]:
        """All ``Coil:Heating:Electric`` objects in the document. Electric heating coil. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name m..."""
    @property
    def coil_heating_fuels(self) -> IDFCollection[CoilHeatingFuel]:
        """All ``Coil:Heating:Fuel`` objects in the document. Gas or other fuel heating coil. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint No..."""
    @property
    def coil_heating_gas_multi_stages(self) -> IDFCollection[CoilHeatingGasMultiStage]:
        """All ``Coil:Heating:Gas:MultiStage`` objects in the document. Gas heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Nod..."""
    @property
    def coil_heating_steams(self) -> IDFCollection[CoilHeatingSteam]:
        """All ``Coil:Heating:Steam`` objects in the document. Steam heating coil. Condenses and sub-cools steam at loop pressure and discharges condensate through steam traps to low pressure condensate line."""
    @property
    def coil_heating_water_to_air_heat_pump_equation_fits(
        self,
    ) -> IDFCollection[CoilHeatingWaterToAirHeatPumpEquationFit]:
        """All ``Coil:Heating:WaterToAirHeatPump:EquationFit`` objects in the document. Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump p..."""
    @property
    def coil_heating_water_to_air_heat_pump_parameter_estimations(
        self,
    ) -> IDFCollection[CoilHeatingWaterToAirHeatPumpParameterEstimation]:
        """All ``Coil:Heating:WaterToAirHeatPump:ParameterEstimation`` objects in the document. Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Parameter estimation model is a deterministic model that requ..."""
    @property
    def coil_heating_water_to_air_heat_pump_variable_speed_equation_fits(
        self,
    ) -> IDFCollection[CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit]:
        """All ``Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit`` objects in the document. Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), variable-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump..."""
    @property
    def coil_heating_waters(self) -> IDFCollection[CoilHeatingWater]:
        """All ``Coil:Heating:Water`` objects in the document. Hot water heating coil, NTU-effectiveness model, assumes a cross-flow heat exchanger. Two options for capacity inputs: UA and water flow rate or capacity and design temperatures."""
    @property
    def coil_performance_dx_coolings(self) -> IDFCollection[CoilPerformanceDXCooling]:
        """All ``CoilPerformance:DX:Cooling`` objects in the document. Used to specify DX cooling coil performance for one mode of operation for a Coil:Cooling:DX:TwoStageWithHumidityControlMode object which may reference one to four CoilPerformance:DX:Cooling objects..."""
    @property
    def coil_system_cooling_dx_heat_exchanger_assisteds(
        self,
    ) -> IDFCollection[CoilSystemCoolingDXHeatExchangerAssisted]:
        """All ``CoilSystem:Cooling:DX:HeatExchangerAssisted`` objects in the document. Virtual component consisting of a direct expansion (DX) cooling coil and an air-to-air heat exchanger. The air-to-air heat exchanger precools the air entering the cooling coil and reuses this energ..."""
    @property
    def coil_system_cooling_dxes(self) -> IDFCollection[CoilSystemCoolingDX]:
        """All ``CoilSystem:Cooling:DX`` objects in the document. Virtual container component that consists of a DX cooling coil and its associated controls. This control object supports several different types of DX cooling coils and may be placed directly in an..."""
    @property
    def coil_system_cooling_water_heat_exchanger_assisteds(
        self,
    ) -> IDFCollection[CoilSystemCoolingWaterHeatExchangerAssisted]:
        """All ``CoilSystem:Cooling:Water:HeatExchangerAssisted`` objects in the document. Virtual component consisting of a chilled-water cooling coil and an air-to-air heat exchanger. The air-to-air heat exchanger precools the air entering the cooling coil and reuses this energy to reh..."""
    @property
    def coil_system_cooling_waters(self) -> IDFCollection[CoilSystemCoolingWater]:
        """All ``CoilSystem:Cooling:Water`` objects in the document. Virtual container component that consists of a water cooling coil and its associated controls. This control object supports the available water coil types and may be placed directly on an air loop ..."""
    @property
    def coil_system_heating_dxes(self) -> IDFCollection[CoilSystemHeatingDX]:
        """All ``CoilSystem:Heating:DX`` objects in the document. Virtual container component that consists of a DX heating coil (heat pump) and its associated controls. This control object supports two different types of DX heating coils and may be placed direct..."""
    @property
    def coil_system_integrated_heat_pump_air_sources(self) -> IDFCollection[CoilSystemIntegratedHeatPumpAirSource]:
        """All ``CoilSystem:IntegratedHeatPump:AirSource`` objects in the document. This object is used for air-source integrated heat pump, a collection of its working modes."""
    @property
    def coil_user_defineds(self) -> IDFCollection[CoilUserDefined]:
        """All ``Coil:UserDefined`` objects in the document. Defines a generic air system component for custom modeling using Energy Management System or External Interface"""
    @property
    def coil_water_heating_air_to_water_heat_pump_pumpeds(
        self,
    ) -> IDFCollection[CoilWaterHeatingAirToWaterHeatPumpPumped]:
        """All ``Coil:WaterHeating:AirToWaterHeatPump:Pumped`` objects in the document. Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. ..."""
    @property
    def coil_water_heating_air_to_water_heat_pump_variable_speeds(
        self,
    ) -> IDFCollection[CoilWaterHeatingAirToWaterHeatPumpVariableSpeed]:
        """All ``Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed`` objects in the document. variable-speed Heat pump water heater (VSHPWH) heating coil, air-to-water direct-expansion (DX) system which includes a variable-speed water heating coil, evaporator air coil, evaporator fan, elect..."""
    @property
    def coil_water_heating_air_to_water_heat_pump_wrappeds(
        self,
    ) -> IDFCollection[CoilWaterHeatingAirToWaterHeatPumpWrapped]:
        """All ``Coil:WaterHeating:AirToWaterHeatPump:Wrapped`` objects in the document. Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. ..."""
    @property
    def coil_water_heating_desuperheaters(self) -> IDFCollection[CoilWaterHeatingDesuperheater]:
        """All ``Coil:WaterHeating:Desuperheater`` objects in the document. Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor..."""
    @property
    def comfort_view_factor_angles(self) -> IDFCollection[ComfortViewFactorAngles]:
        """All ``ComfortViewFactorAngles`` objects in the document. Used to specify radiant view factors for thermal comfort calculations. Note that the following angle factor fractions must sum up to 1.0 All surfaces must be in the same enclosure."""
    @property
    def complex_fenestration_property_solar_absorbed_layers(
        self,
    ) -> IDFCollection[ComplexFenestrationPropertySolarAbsorbedLayers]:
        """All ``ComplexFenestrationProperty:SolarAbsorbedLayers`` objects in the document. Used to provide solar radiation absorbed in fenestration layers. References surface-construction pair and if that pair is used in a simulation, then program will use value provided in schedules ins..."""
    @property
    def compliance_buildings(self) -> IDFCollection[ComplianceBuilding]:
        """All ``Compliance:Building`` objects in the document. Building level inputs related to compliance to building standards, building codes, and beyond energy code programs."""
    @property
    def component_cost_adjustments(self) -> IDFCollection[ComponentCostAdjustments]:
        """All ``ComponentCost:Adjustments`` objects in the document. Used to perform various modifications to the construction costs to arrive at an estimate for total project costs. This object allows extending the line item model so that the overall costs of the p..."""
    @property
    def component_cost_line_items(self) -> IDFCollection[ComponentCostLineItem]:
        """All ``ComponentCost:LineItem`` objects in the document. Each instance of this object creates a cost line item and will contribute to the total for a cost estimate."""
    @property
    def component_cost_references(self) -> IDFCollection[ComponentCostReference]:
        """All ``ComponentCost:Reference`` objects in the document. Used to allow comparing the current cost estimate to the results of a previous estimate for a reference building. This object parallels the ComponentCost:Adjustments object but adds a field for ent..."""
    @property
    def condenser_equipment_lists(self) -> IDFCollection[CondenserEquipmentList]:
        """All ``CondenserEquipmentList`` objects in the document. List condenser equipment in order of operating priority, 1st in list will be used 1st, etc Use only condenser equipment in this list. If no equipment object types and equipment names are specified,..."""
    @property
    def condenser_equipment_operation_schemes(self) -> IDFCollection[CondenserEquipmentOperationSchemes]:
        """All ``CondenserEquipmentOperationSchemes`` objects in the document. Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first th..."""
    @property
    def condenser_loops(self) -> IDFCollection[CondenserLoop]:
        """All ``CondenserLoop`` objects in the document. Defines a central plant condenser loop. CondenserLoop and PlantLoop are nearly identical except some components and operation schemes are applicable to only one loop type or the other."""
    @property
    def connector_lists(self) -> IDFCollection[ConnectorList]:
        """All ``ConnectorList`` objects in the document. only two connectors allowed per loop if two entered, one must be Connector:Splitter and one must be Connector:Mixer"""
    @property
    def connector_mixers(self) -> IDFCollection[ConnectorMixer]:
        """All ``Connector:Mixer`` objects in the document. Mix N inlet air/water streams into one. Branch names cannot be duplicated within a single mixer list."""
    @property
    def connector_splitters(self) -> IDFCollection[ConnectorSplitter]:
        """All ``Connector:Splitter`` objects in the document. Split one air/water stream into N outlet streams. Branch names cannot be duplicated within a single Splitter list."""
    @property
    def construction_air_boundaries(self) -> IDFCollection[ConstructionAirBoundary]:
        """All ``Construction:AirBoundary`` objects in the document. Indicates an open boundary between two zones. It may be used for base surfaces and fenestration surfaces. The two adjacent zones are grouped together for solar, daylighting and radiant exchange. Wh..."""
    @property
    def construction_assignment_sets(self) -> IDFCollection[ConstructionAssignmentSet]:
        """All ``ConstructionAssignmentSet`` objects in the document. Defines a set of construction assignments for surfaces and sub-surfaces based on their type and outside boundary condition. Can be referenced by Building or Space objects. Space-level assignments t..."""
    @property
    def construction_cfactor_underground_walls(self) -> IDFCollection[ConstructionCfactorUndergroundWall]:
        """All ``Construction:CfactorUndergroundWall`` objects in the document. Alternate method of describing underground wall constructions"""
    @property
    def construction_complex_fenestration_states(self) -> IDFCollection[ConstructionComplexFenestrationState]:
        """All ``Construction:ComplexFenestrationState`` objects in the document. Describes one state for a complex glazing system These input objects are typically generated by using WINDOW software and export to IDF syntax"""
    @property
    def construction_ffactor_ground_floors(self) -> IDFCollection[ConstructionFfactorGroundFloor]:
        """All ``Construction:FfactorGroundFloor`` objects in the document. Alternate method of describing slab-on-grade or underground floor constructions"""
    @property
    def construction_property_internal_heat_sources(self) -> IDFCollection[ConstructionPropertyInternalHeatSource]:
        """All ``ConstructionProperty:InternalHeatSource`` objects in the document. Internal heat source to be attached to a construction layer"""
    @property
    def construction_window(self) -> IDFCollection[Construction]:
        """All ``Construction`` objects in the document. Start with outside layer and work your way to the inside layer Up to 10 layers total, 8 for windows Enter the material name for each layer"""
    @property
    def construction_window_data_files(self) -> IDFCollection[ConstructionWindowDataFile]:
        """All ``Construction:WindowDataFile`` objects in the document. Initiates search of the Window data file for a window called Name."""
    @property
    def construction_window_equivalent_layers(self) -> IDFCollection[ConstructionWindowEquivalentLayer]:
        """All ``Construction:WindowEquivalentLayer`` objects in the document. Start with outside layer and work your way to the inside Layer Up to 11 layers total. Up to six solid layers and up to five gaps. Enter the material name for each layer"""
    @property
    def constructions(self) -> IDFCollection[Construction]:
        """All ``Construction`` objects in the document. Start with outside layer and work your way to the inside layer Up to 10 layers total, 8 for windows Enter the material name for each layer"""
    @property
    def controller_mechanical_ventilations(self) -> IDFCollection[ControllerMechanicalVentilation]:
        """All ``Controller:MechanicalVentilation`` objects in the document. This object is used in conjunction with Controller:OutdoorAir to specify outdoor ventilation air based on outdoor air specified in the DesignSpecification:OutdoorAir object The Controller:OutdoorAi..."""
    @property
    def controller_outdoor_airs(self) -> IDFCollection[ControllerOutdoorAir]:
        """All ``Controller:OutdoorAir`` objects in the document. Controller to set the outdoor air flow rate for an air loop. Control options include fixed, proportional, scheduled, economizer, and demand-controlled ventilation."""
    @property
    def controller_water_coils(self) -> IDFCollection[ControllerWaterCoil]:
        """All ``Controller:WaterCoil`` objects in the document. Controller for a water coil which is located directly in an air loop branch or outdoor air equipment list. Controls the coil water flow to meet the specified leaving air setpoint(s). Used with Coil..."""
    @property
    def convergence_limits(self) -> IDFCollection[ConvergenceLimits]:
        """All ``ConvergenceLimits`` objects in the document. Specifies limits on HVAC system simulation timesteps and iterations. This item is an advanced feature that should be used only with caution."""
    @property
    def cooling_tower_performance_cool_tools(self) -> IDFCollection[CoolingTowerPerformanceCoolTools]:
        """All ``CoolingTowerPerformance:CoolTools`` objects in the document. This object is used to define coefficients for the approach temperature correlation for a variable speed cooling tower when tower Model Type is specified as CoolToolsUserDefined in the object Cooli..."""
    @property
    def cooling_tower_performance_york_calcs(self) -> IDFCollection[CoolingTowerPerformanceYorkCalc]:
        """All ``CoolingTowerPerformance:YorkCalc`` objects in the document. This object is used to define coefficients for the approach temperature correlation for a variable speed cooling tower when tower Model Type is specified as YorkCalcUserDefined in the object Coolin..."""
    @property
    def cooling_tower_single_speeds(self) -> IDFCollection[CoolingTowerSingleSpeed]:
        """All ``CoolingTower:SingleSpeed`` objects in the document. This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a si..."""
    @property
    def cooling_tower_two_speeds(self) -> IDFCollection[CoolingTowerTwoSpeed]:
        """All ``CoolingTower:TwoSpeed`` objects in the document. This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a tw..."""
    @property
    def cooling_tower_variable_speed_merkels(self) -> IDFCollection[CoolingTowerVariableSpeedMerkel]:
        """All ``CoolingTower:VariableSpeed:Merkel`` objects in the document. This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a va..."""
    @property
    def cooling_tower_variable_speeds(self) -> IDFCollection[CoolingTowerVariableSpeed]:
        """All ``CoolingTower:VariableSpeed`` objects in the document. This open wet tower model is based on purely empirical algorithms derived from manufacturer's performance data or field measurements. The user can select from two existing algorithms (CoolTools or ..."""
    @property
    def currency_types(self) -> IDFCollection[CurrencyType]:
        """All ``CurrencyType`` objects in the document. If CurrencyType is not specified, it will default to USD and produce $ in the reports."""
    @property
    def curve_bicubics(self) -> IDFCollection[CurveBicubic]:
        """All ``Curve:Bicubic`` objects in the document. Cubic curve with two independent variables. Input consists of the curve name, the ten coefficients, and the minimum and maximum values for each of the independent variables. Optional inputs for cur..."""
    @property
    def curve_biquadratics(self) -> IDFCollection[CurveBiquadratic]:
        """All ``Curve:Biquadratic`` objects in the document. Quadratic curve with two independent variables. Input consists of the curve name, the six coefficients, and min and max values for each of the independent variables. Optional inputs for curve minim..."""
    @property
    def curve_chiller_part_load_with_lifts(self) -> IDFCollection[CurveChillerPartLoadWithLift]:
        """All ``Curve:ChillerPartLoadWithLift`` objects in the document. This chiller part-load performance curve has three independent variables. Input consists of the curve name, the twelve coefficients, and the maximum and minimum valid independent variable values. O..."""
    @property
    def curve_cubic_linears(self) -> IDFCollection[CurveCubicLinear]:
        """All ``Curve:CubicLinear`` objects in the document. Cubic-linear curve with two independent variables. Input consists of the curve name, the six coefficients, and min and max values for each of the independent variables. Optional inputs for curve mi..."""
    @property
    def curve_cubics(self) -> IDFCollection[CurveCubic]:
        """All ``Curve:Cubic`` objects in the document. Cubic curve with one independent variable. Input for a cubic curve consists of the curve name, the 4 coefficients, and the maximum and minimum valid independent variable values. Optional inputs for..."""
    @property
    def curve_double_exponential_decays(self) -> IDFCollection[CurveDoubleExponentialDecay]:
        """All ``Curve:DoubleExponentialDecay`` objects in the document. Double exponential decay curve with one independent variable. Input consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs..."""
    @property
    def curve_exponential_decays(self) -> IDFCollection[CurveExponentialDecay]:
        """All ``Curve:ExponentialDecay`` objects in the document. Exponential decay curve with one independent variable. Input consists of the curve name, the three coefficients, and the maximum and minimum valid independent variable values. Optional inputs for t..."""
    @property
    def curve_exponential_skew_normals(self) -> IDFCollection[CurveExponentialSkewNormal]:
        """All ``Curve:ExponentialSkewNormal`` objects in the document. Exponential-modified skew normal curve with one independent variable. Input consists of the curve name, the four coefficients, and the maximum and minimum valid independent variable values. Optiona..."""
    @property
    def curve_exponents(self) -> IDFCollection[CurveExponent]:
        """All ``Curve:Exponent`` objects in the document. Exponent curve with one independent variable. Input for a exponent curve consists of the curve name, the 3 coefficients, and the maximum and minimum valid independent variable values. Optional inpu..."""
    @property
    def curve_fan_pressure_rises(self) -> IDFCollection[CurveFanPressureRise]:
        """All ``Curve:FanPressureRise`` objects in the document. Special curve type with two independent variables. Input for the fan total pressure rise curve consists of the curve name, the four coefficients, and the maximum and minimum valid independent varia..."""
    @property
    def curve_functional_pressure_drops(self) -> IDFCollection[CurveFunctionalPressureDrop]:
        """All ``Curve:Functional:PressureDrop`` objects in the document. Sets up curve information for minor loss and/or friction calculations in plant pressure simulations Expression: DeltaP = {K + f*(L/D)} * (rho * V^2) / 2"""
    @property
    def curve_linears(self) -> IDFCollection[CurveLinear]:
        """All ``Curve:Linear`` objects in the document. Linear curve with one independent variable. Input for the linear curve consists of a curve name, the two coefficients, and the maximum and minimum valid independent variable values. Optional inputs..."""
    @property
    def curve_quad_linears(self) -> IDFCollection[CurveQuadLinear]:
        """All ``Curve:QuadLinear`` objects in the document. Linear curve with four independent variables. Input for the linear curve consists of a curve name, the two coefficients, and the maximum and minimum valid independent variable values. Optional inpu..."""
    @property
    def curve_quadratic_linears(self) -> IDFCollection[CurveQuadraticLinear]:
        """All ``Curve:QuadraticLinear`` objects in the document. Quadratic-linear curve with two independent variables. Input consists of the curve name, the six coefficients, and min and max values for each of the independent variables. Optional inputs for curv..."""
    @property
    def curve_quadratics(self) -> IDFCollection[CurveQuadratic]:
        """All ``Curve:Quadratic`` objects in the document. Quadratic curve with one independent variable. Input for a quadratic curve consists of the curve name, the three coefficients, and the maximum and minimum valid independent variable values. Optiona..."""
    @property
    def curve_quartics(self) -> IDFCollection[CurveQuartic]:
        """All ``Curve:Quartic`` objects in the document. Quartic (fourth order polynomial) curve with one independent variable. Input for a Quartic curve consists of the curve name, the five coefficients, and the maximum and minimum valid independent var..."""
    @property
    def curve_quint_linears(self) -> IDFCollection[CurveQuintLinear]:
        """All ``Curve:QuintLinear`` objects in the document. Linear curve with five independent variables. Input for the linear curve consists of a curve name, the two coefficients, and the maximum and minimum valid independent variable values. Optional inpu..."""
    @property
    def curve_rectangular_hyperbola1s(self) -> IDFCollection[CurveRectangularHyperbola1]:
        """All ``Curve:RectangularHyperbola1`` objects in the document. Rectangular hyperbola type 1 curve with one independent variable. Input consists of the curve name, the three coefficients, and the maximum and minimum valid independent variable values. Optional i..."""
    @property
    def curve_rectangular_hyperbola2s(self) -> IDFCollection[CurveRectangularHyperbola2]:
        """All ``Curve:RectangularHyperbola2`` objects in the document. Rectangular hyperbola type 2 curve with one independent variable. Input consists of the curve name, the three coefficients, and the maximum and minimum valid independent variable values. Optional i..."""
    @property
    def curve_sigmoids(self) -> IDFCollection[CurveSigmoid]:
        """All ``Curve:Sigmoid`` objects in the document. Sigmoid curve with one independent variable. Input consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve mi..."""
    @property
    def curve_triquadratics(self) -> IDFCollection[CurveTriquadratic]:
        """All ``Curve:Triquadratic`` objects in the document. Quadratic curve with three independent variables. Input consists of the curve name, the twenty seven coefficients, and min and max values for each of the independent variables. Optional inputs for ..."""
    @property
    def daylighting_controls(self) -> IDFCollection[DaylightingControls]:
        """All ``Daylighting:Controls`` objects in the document. Dimming of overhead electric lighting is determined from each reference point. Glare from daylighting is also calculated."""
    @property
    def daylighting_delight_complex_fenestrations(self) -> IDFCollection[DaylightingDELightComplexFenestration]:
        """All ``Daylighting:DELight:ComplexFenestration`` objects in the document. Used for DElight Complex Fenestration of all types"""
    @property
    def daylighting_device_light_wells(self) -> IDFCollection[DaylightingDeviceLightWell]:
        """All ``DaylightingDevice:LightWell`` objects in the document. Applies only to exterior windows in daylighting-controlled zones or in zones that share an interior window with a daylighting-controlled zone. Generally used with skylights."""
    @property
    def daylighting_device_shelfs(self) -> IDFCollection[DaylightingDeviceShelf]:
        """All ``DaylightingDevice:Shelf`` objects in the document. Defines a daylighting which can have an inside shelf, an outside shelf, or both. The inside shelf is defined as a building surface and the outside shelf is defined as a shading surface."""
    @property
    def daylighting_device_tubulars(self) -> IDFCollection[DaylightingDeviceTubular]:
        """All ``DaylightingDevice:Tubular`` objects in the document. Defines a tubular daylighting device (TDD) consisting of three components: a dome, a pipe, and a diffuser. The dome and diffuser are defined separately using the FenestrationSurface:Detailed object."""
    @property
    def daylighting_reference_points(self) -> IDFCollection[DaylightingReferencePoint]:
        """All ``Daylighting:ReferencePoint`` objects in the document. Used by Daylighting:Controls to identify the reference point coordinates for each sensor. Reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference..."""
    @property
    def dehumidifier_desiccant_no_fans(self) -> IDFCollection[DehumidifierDesiccantNoFans]:
        """All ``Dehumidifier:Desiccant:NoFans`` objects in the document. This object models a solid desiccant dehumidifier. The process air stream is the air which is dehumidified. The regeneration air stream is the air which is heated to regenerate the desiccant. This ..."""
    @property
    def dehumidifier_desiccant_systems(self) -> IDFCollection[DehumidifierDesiccantSystem]:
        """All ``Dehumidifier:Desiccant:System`` objects in the document. This compound object models a desiccant heat exchanger, an optional heater, and associated fans. The process air stream is the air which is dehumidified. The regeneration air stream is the air whic..."""
    @property
    def demand_manager_assignment_lists(self) -> IDFCollection[DemandManagerAssignmentList]:
        """All ``DemandManagerAssignmentList`` objects in the document. A high level control that makes demand limiting decisions based on a list of possible demand limiting strategies."""
    @property
    def demand_manager_electric_equipments(self) -> IDFCollection[DemandManagerElectricEquipment]:
        """All ``DemandManager:ElectricEquipment`` objects in the document. used for demand limiting ElectricEquipment objects."""
    @property
    def demand_manager_exterior_lights(self) -> IDFCollection[DemandManagerExteriorLights]:
        """All ``DemandManager:ExteriorLights`` objects in the document. used for demand limiting Exterior:Lights objects."""
    @property
    def demand_manager_lights(self) -> IDFCollection[DemandManagerLights]:
        """All ``DemandManager:Lights`` objects in the document. used for demand limiting Lights objects."""
    @property
    def demand_manager_thermostats(self) -> IDFCollection[DemandManagerThermostats]:
        """All ``DemandManager:Thermostats`` objects in the document. used for demand limiting ZoneControl:Thermostat objects."""
    @property
    def demand_manager_ventilations(self) -> IDFCollection[DemandManagerVentilation]:
        """All ``DemandManager:Ventilation`` objects in the document. used for demand limiting Controller:OutdoorAir objects."""
    @property
    def design_specification_air_terminal_sizings(self) -> IDFCollection[DesignSpecificationAirTerminalSizing]:
        """All ``DesignSpecification:AirTerminal:Sizing`` objects in the document. This object is used to scale the sizing of air terminal units."""
    @property
    def design_specification_outdoor_air_space_lists(self) -> IDFCollection[DesignSpecificationOutdoorAirSpaceList]:
        """All ``DesignSpecification:OutdoorAir:SpaceList`` objects in the document. Defines a list of DesignSpecification:OutdoorAir names which can be referenced as a group. The DesignSpecification:OutdoorAir:SpaceList name may be used in Sizing:Zone and Controller:MechanicalVent..."""
    @property
    def design_specification_outdoor_airs(self) -> IDFCollection[DesignSpecificationOutdoorAir]:
        """All ``DesignSpecification:OutdoorAir`` objects in the document. This object is used to describe general outdoor air requirements which are referenced by other objects."""
    @property
    def design_specification_zone_air_distributions(self) -> IDFCollection[DesignSpecificationZoneAirDistribution]:
        """All ``DesignSpecification:ZoneAirDistribution`` objects in the document. This object is used to describe zone air distribution in terms of air distribution effectiveness and secondary recirculation fraction. It is referenced by Sizing:Zone and Controller:MechanicalVenti..."""
    @property
    def design_specification_zone_hvac_sizings(self) -> IDFCollection[DesignSpecificationZoneHVACSizing]:
        """All ``DesignSpecification:ZoneHVAC:Sizing`` objects in the document. This object is used to describe general scalable zone HVAC equipment sizing which are referenced by other objects."""
    @property
    def district_coolings(self) -> IDFCollection[DistrictCooling]:
        """All ``DistrictCooling`` objects in the document. Centralized source of chilled water, such as a district cooling system."""
    @property
    def district_heating_steams(self) -> IDFCollection[DistrictHeatingSteam]:
        """All ``DistrictHeating:Steam`` objects in the document. Centralized source of Steam, such as a district heating system."""
    @property
    def district_heating_waters(self) -> IDFCollection[DistrictHeatingWater]:
        """All ``DistrictHeating:Water`` objects in the document. Centralized source of hot water, such as a district heating system."""
    @property
    def door_interzones(self) -> IDFCollection[DoorInterzone]:
        """All ``Door:Interzone`` objects in the document. Allows for simplified entry of interzone (opaque interior) doors (adjacent to other zones)."""
    @property
    def doors(self) -> IDFCollection[Door]:
        """All ``Door`` objects in the document. Allows for simplified entry of opaque Doors."""
    @property
    def duct_loss_conductions(self) -> IDFCollection[DuctLossConduction]:
        """All ``Duct:Loss:Conduction`` objects in the document."""
    @property
    def duct_loss_leakages(self) -> IDFCollection[DuctLossLeakage]:
        """All ``Duct:Loss:Leakage`` objects in the document."""
    @property
    def duct_loss_makeup_airs(self) -> IDFCollection[DuctLossMakeupAir]:
        """All ``Duct:Loss:MakeupAir`` objects in the document."""
    @property
    def ducts(self) -> IDFCollection[Duct]:
        """All ``Duct`` objects in the document. Passes inlet node state variables to outlet node state variables"""
    @property
    def electric_equipment(self) -> IDFCollection[ElectricEquipment]:
        """All ``ElectricEquipment`` objects in the document. Sets internal gains for electric equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and ..."""
    @property
    def electric_equipment_definitions(self) -> IDFCollection[ElectricEquipmentDefinition]:
        """All ``ElectricEquipment:Definition`` objects in the document. Defines the physical characteristics (design level and heat gain fractions) for electric equipment. Referenced by one or more ElectricEquipment:Instance objects."""
    @property
    def electric_equipment_instances(self) -> IDFCollection[ElectricEquipmentInstance]:
        """All ``ElectricEquipment:Instance`` objects in the document. Sets internal gains for electric equipment in the zone. The physical characteristics are given by the referenced ElectricEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised o..."""
    @property
    def electric_equipment_ite_air_cooled_definitions(self) -> IDFCollection[ElectricEquipmentITEAirCooledDefinition]:
        """All ``ElectricEquipment:ITE:AirCooled:Definition`` objects in the document. Performance characteristics for ElectricEquipment:ITE:AirCooled:Instance. Defines power, airflow, and efficiency as functions of loading and temperature."""
    @property
    def electric_equipment_ite_air_cooled_instances(self) -> IDFCollection[ElectricEquipmentITEAirCooledInstance]:
        """All ``ElectricEquipment:ITE:AirCooled:Instance`` objects in the document. This object describes air-cooled electric information technology equipment (ITE) which has variable power consumption as a function of loading and temperature. The performance characteristics are g..."""
    @property
    def electric_equipment_ite_air_cooleds(self) -> IDFCollection[ElectricEquipmentITEAirCooled]:
        """All ``ElectricEquipment:ITE:AirCooled`` objects in the document. This object describes air-cooled electric information technology equipment (ITE) which has variable power consumption as a function of loading and temperature. If a Zone comprised of more than one ..."""
    @property
    def electric_equipments(self) -> IDFCollection[ElectricEquipment]:
        """All ``ElectricEquipment`` objects in the document. Sets internal gains for electric equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and ..."""
    @property
    def electric_load_center_distributions(self) -> IDFCollection[ElectricLoadCenterDistribution]:
        """All ``ElectricLoadCenter:Distribution`` objects in the document. ElectricLoadCenter:Distribution objects are used to include on-site electricity generators and or storage in a simulation."""
    @property
    def electric_load_center_generators(self) -> IDFCollection[ElectricLoadCenterGenerators]:
        """All ``ElectricLoadCenter:Generators`` objects in the document. List of electric power generators to include in the simulation including the name and type of each generators along with availability schedule, rated power output, and thermal-to-electrical power r..."""
    @property
    def electric_load_center_inverter_function_of_powers(
        self,
    ) -> IDFCollection[ElectricLoadCenterInverterFunctionOfPower]:
        """All ``ElectricLoadCenter:Inverter:FunctionOfPower`` objects in the document. Electric power inverter to convert from direct current (DC) to alternating current (AC) in an electric load center that contains photovoltaic modules. This input object is for an inverter model whe..."""
    @property
    def electric_load_center_inverter_look_up_tables(self) -> IDFCollection[ElectricLoadCenterInverterLookUpTable]:
        """All ``ElectricLoadCenter:Inverter:LookUpTable`` objects in the document. California Energy Commission tests and publishes data on inverters This inverter model interpolates using CEC test data Input data are at http://www.gosolarcalifornia.org/equipment/inverter_tests/s..."""
    @property
    def electric_load_center_inverter_pv_watts(self) -> IDFCollection[ElectricLoadCenterInverterPVWatts]:
        """All ``ElectricLoadCenter:Inverter:PVWatts`` objects in the document. Electric power inverter to convert from direct current (DC) to alternating current (AC) in an electric load center that contains Generator:PVWatts objects. It implements the PVWatts inverter perfor..."""
    @property
    def electric_load_center_inverter_simples(self) -> IDFCollection[ElectricLoadCenterInverterSimple]:
        """All ``ElectricLoadCenter:Inverter:Simple`` objects in the document. Electric power inverter to convert from direct current (DC) to alternating current (AC) in an electric load center that contains photovoltaic modules. This input object is for the simplest inverter..."""
    @property
    def electric_load_center_storage_batteries(self) -> IDFCollection[ElectricLoadCenterStorageBattery]:
        """All ``ElectricLoadCenter:Storage:Battery`` objects in the document. Uses the kinetic battery model (KiBaM) to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the sur..."""
    @property
    def electric_load_center_storage_converters(self) -> IDFCollection[ElectricLoadCenterStorageConverter]:
        """All ``ElectricLoadCenter:Storage:Converter`` objects in the document. This model is for converting AC to DC for grid-supplied charging of DC storage"""
    @property
    def electric_load_center_storage_li_ion_nmc_batteries(
        self,
    ) -> IDFCollection[ElectricLoadCenterStorageLiIonNMCBattery]:
        """All ``ElectricLoadCenter:Storage:LiIonNMCBattery`` objects in the document. Uses Lithium Ion NMC model to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or defi..."""
    @property
    def electric_load_center_storage_simples(self) -> IDFCollection[ElectricLoadCenterStorageSimple]:
        """All ``ElectricLoadCenter:Storage:Simple`` objects in the document. Used to model storage of electricity in an electric load center. This is a simple model that does not attempt to represent any of the characteristics of a real storage device such as a battery. The..."""
    @property
    def electric_load_center_transformers(self) -> IDFCollection[ElectricLoadCenterTransformer]:
        """All ``ElectricLoadCenter:Transformer`` objects in the document. This object is used to model the energy losses of transformers when they are used to transfer electricity from the grid to a building (as distribution transformers) or transfer electricity from ons..."""
    @property
    def energy_management_system_actuators(self) -> IDFCollection[EnergyManagementSystemActuator]:
        """All ``EnergyManagementSystem:Actuator`` objects in the document. Hardware portion of EMS used to set up actuators in the model"""
    @property
    def energy_management_system_construction_index_variables(
        self,
    ) -> IDFCollection[EnergyManagementSystemConstructionIndexVariable]:
        """All ``EnergyManagementSystem:ConstructionIndexVariable`` objects in the document. Declares EMS variable that identifies a construction"""
    @property
    def energy_management_system_curve_or_table_index_variables(
        self,
    ) -> IDFCollection[EnergyManagementSystemCurveOrTableIndexVariable]:
        """All ``EnergyManagementSystem:CurveOrTableIndexVariable`` objects in the document. Declares EMS variable that identifies a curve or table"""
    @property
    def energy_management_system_global_variables(self) -> IDFCollection[EnergyManagementSystemGlobalVariable]:
        """All ``EnergyManagementSystem:GlobalVariable`` objects in the document. Declares Erl variable as having global scope No spaces allowed in names used for Erl variables"""
    @property
    def energy_management_system_internal_variables(self) -> IDFCollection[EnergyManagementSystemInternalVariable]:
        """All ``EnergyManagementSystem:InternalVariable`` objects in the document. Declares EMS variable as an internal data variable"""
    @property
    def energy_management_system_metered_output_variables(
        self,
    ) -> IDFCollection[EnergyManagementSystemMeteredOutputVariable]:
        """All ``EnergyManagementSystem:MeteredOutputVariable`` objects in the document. This object sets up an EnergyPlus output variable from an Erl variable"""
    @property
    def energy_management_system_output_variables(self) -> IDFCollection[EnergyManagementSystemOutputVariable]:
        """All ``EnergyManagementSystem:OutputVariable`` objects in the document. This object sets up an EnergyPlus output variable from an Erl variable"""
    @property
    def energy_management_system_program_calling_managers(
        self,
    ) -> IDFCollection[EnergyManagementSystemProgramCallingManager]:
        """All ``EnergyManagementSystem:ProgramCallingManager`` objects in the document. Input EMS program. a program needs a name a description of when it should be called and then lines of program code for EMS Runtime language"""
    @property
    def energy_management_system_programs(self) -> IDFCollection[EnergyManagementSystemProgram]:
        """All ``EnergyManagementSystem:Program`` objects in the document. This input defines an Erl program Each field after the name is a line of EMS Runtime Language"""
    @property
    def energy_management_system_sensors(self) -> IDFCollection[EnergyManagementSystemSensor]:
        """All ``EnergyManagementSystem:Sensor`` objects in the document. Declares EMS variable as a sensor a list of output variables and meters that can be reported are available after a run on the report (.rdd) or meter dictionary file (.mdd) if the Output:VariableDic..."""
    @property
    def energy_management_system_subroutines(self) -> IDFCollection[EnergyManagementSystemSubroutine]:
        """All ``EnergyManagementSystem:Subroutine`` objects in the document. This input defines an Erl program subroutine Each field after the name is a line of EMS Runtime Language"""
    @property
    def energy_management_system_trend_variables(self) -> IDFCollection[EnergyManagementSystemTrendVariable]:
        """All ``EnergyManagementSystem:TrendVariable`` objects in the document. This object sets up an EMS trend variable from an Erl variable A trend variable logs values across timesteps"""
    @property
    def environmental_impact_factors(self) -> IDFCollection[EnvironmentalImpactFactors]:
        """All ``EnvironmentalImpactFactors`` objects in the document. Used to help convert district and ideal energy use to a fuel type and provide total carbon equivalent with coefficients Also used in Source=>Site conversions."""
    @property
    def evaporative_cooler_direct_cel_dek_pads(self) -> IDFCollection[EvaporativeCoolerDirectCelDekPad]:
        """All ``EvaporativeCooler:Direct:CelDekPad`` objects in the document. Direct evaporative cooler with rigid media evaporative pad and recirculating water pump. This model has no controls other than its availability schedule."""
    @property
    def evaporative_cooler_direct_research_specials(self) -> IDFCollection[EvaporativeCoolerDirectResearchSpecial]:
        """All ``EvaporativeCooler:Direct:ResearchSpecial`` objects in the document. Direct evaporative cooler with user-specified effectiveness (can represent rigid pad or similar media), and recirculating water pump, and secondary air fan. This model is controlled to meet the pri..."""
    @property
    def evaporative_cooler_indirect_cel_dek_pads(self) -> IDFCollection[EvaporativeCoolerIndirectCelDekPad]:
        """All ``EvaporativeCooler:Indirect:CelDekPad`` objects in the document. Indirect evaporative cooler with rigid media evaporative pad, recirculating water pump, and secondary air fan. This model has no controls other than its availability schedule."""
    @property
    def evaporative_cooler_indirect_research_specials(self) -> IDFCollection[EvaporativeCoolerIndirectResearchSpecial]:
        """All ``EvaporativeCooler:Indirect:ResearchSpecial`` objects in the document. Indirect evaporative cooler with user-specified effectiveness (can represent rigid pad or wetted coil), recirculating water pump, and secondary air fan. This model is controlled to meet the primary..."""
    @property
    def evaporative_cooler_indirect_wet_coils(self) -> IDFCollection[EvaporativeCoolerIndirectWetCoil]:
        """All ``EvaporativeCooler:Indirect:WetCoil`` objects in the document. Indirect evaporative cooler with wetted coil, recirculating water pump, and secondary air fan. This model has no controls other than its availability schedule."""
    @property
    def evaporative_fluid_cooler_single_speeds(self) -> IDFCollection[EvaporativeFluidCoolerSingleSpeed]:
        """All ``EvaporativeFluidCooler:SingleSpeed`` objects in the document. This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger."""
    @property
    def evaporative_fluid_cooler_two_speeds(self) -> IDFCollection[EvaporativeFluidCoolerTwoSpeed]:
        """All ``EvaporativeFluidCooler:TwoSpeed`` objects in the document. This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger."""
    @property
    def exterior_fuel_equipments(self) -> IDFCollection[ExteriorFuelEquipment]:
        """All ``Exterior:FuelEquipment`` objects in the document. only used for Meter type reporting, does not affect building loads"""
    @property
    def exterior_lights(self) -> IDFCollection[ExteriorLights]:
        """All ``Exterior:Lights`` objects in the document. only used for Meter type reporting, does not affect building loads"""
    @property
    def exterior_water_equipments(self) -> IDFCollection[ExteriorWaterEquipment]:
        """All ``Exterior:WaterEquipment`` objects in the document. only used for Meter type reporting, does not affect building loads"""
    @property
    def external_interface_actuators(self) -> IDFCollection[ExternalInterfaceActuator]:
        """All ``ExternalInterface:Actuator`` objects in the document. Hardware portion of EMS used to set up actuators in the model"""
    @property
    def external_interface_functional_mockup_unit_export_from_variables(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitExportFromVariable]:
        """All ``ExternalInterface:FunctionalMockupUnitExport:From:Variable`` objects in the document. This object declares an FMU input variable"""
    @property
    def external_interface_functional_mockup_unit_export_to_actuators(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitExportToActuator]:
        """All ``ExternalInterface:FunctionalMockupUnitExport:To:Actuator`` objects in the document. Hardware portion of EMS used to set up actuators in the model that are dynamically updated from the FMU."""
    @property
    def external_interface_functional_mockup_unit_export_to_schedules(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitExportToSchedule]:
        """All ``ExternalInterface:FunctionalMockupUnitExport:To:Schedule`` objects in the document. This objects contains only one value, which is used during the first call of EnergyPlus"""
    @property
    def external_interface_functional_mockup_unit_export_to_variables(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitExportToVariable]:
        """All ``ExternalInterface:FunctionalMockupUnitExport:To:Variable`` objects in the document. Declares Erl variable as having global scope No spaces allowed in names used for Erl variables"""
    @property
    def external_interface_functional_mockup_unit_import_from_variables(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImportFromVariable]:
        """All ``ExternalInterface:FunctionalMockupUnitImport:From:Variable`` objects in the document. This object declares an FMU input variable"""
    @property
    def external_interface_functional_mockup_unit_import_to_actuators(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImportToActuator]:
        """All ``ExternalInterface:FunctionalMockupUnitImport:To:Actuator`` objects in the document. Hardware portion of EMS used to set up actuators in the model that are dynamically updated from the FMU."""
    @property
    def external_interface_functional_mockup_unit_import_to_schedules(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImportToSchedule]:
        """All ``ExternalInterface:FunctionalMockupUnitImport:To:Schedule`` objects in the document. This objects contains only one value, which is used during the first call of EnergyPlus"""
    @property
    def external_interface_functional_mockup_unit_import_to_variables(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImportToVariable]:
        """All ``ExternalInterface:FunctionalMockupUnitImport:To:Variable`` objects in the document. Declares Erl variable as having global scope No spaces allowed in names used for Erl variables"""
    @property
    def external_interface_functional_mockup_unit_imports(
        self,
    ) -> IDFCollection[ExternalInterfaceFunctionalMockupUnitImport]:
        """All ``ExternalInterface:FunctionalMockupUnitImport`` objects in the document. This object declares an FMU"""
    @property
    def external_interface_schedules(self) -> IDFCollection[ExternalInterfaceSchedule]:
        """All ``ExternalInterface:Schedule`` objects in the document. A ExternalInterface:Schedule contains only one value, which is used during the warm-up period and the system sizing."""
    @property
    def external_interface_variables(self) -> IDFCollection[ExternalInterfaceVariable]:
        """All ``ExternalInterface:Variable`` objects in the document. This input object is similar to EnergyManagementSystem:GlobalVariable. However, at the beginning of each zone time step, its value is set to the value received from the external interface. During t..."""
    @property
    def external_interfaces(self) -> IDFCollection[ExternalInterface]:
        """All ``ExternalInterface`` objects in the document. This object activates the external interface of EnergyPlus. If the object ExternalInterface is present, then all ExtnernalInterface:* objects will receive their values from the BCVTB interface or f..."""
    @property
    def fan_component_models(self) -> IDFCollection[FanComponentModel]:
        """All ``Fan:ComponentModel`` objects in the document. A detailed fan type for constant-air-volume (CAV) and variable-air-volume (VAV) systems. It includes inputs that describe the air-distribution system as well as the fan, drive belt (if used), motor..."""
    @property
    def fan_constant_volumes(self) -> IDFCollection[FanConstantVolume]:
        """All ``Fan:ConstantVolume`` objects in the document. Constant volume fan that is intended to operate continuously based on a time schedule. This fan will not cycle on and off based on cooling/heating load or other control signals."""
    @property
    def fan_on_offs(self) -> IDFCollection[FanOnOff]:
        """All ``Fan:OnOff`` objects in the document. Constant volume fan that is intended to cycle on and off based on cooling/heating load or other control signals. This fan can also operate continuously like Fan:ConstantVolume."""
    @property
    def fan_performance_night_ventilations(self) -> IDFCollection[FanPerformanceNightVentilation]:
        """All ``FanPerformance:NightVentilation`` objects in the document. Specifies an alternate set of performance parameters for a fan. These alternate parameters are used when a system manager (such as AvailabilityManager:NightVentilation) sets a specified flow rate. ..."""
    @property
    def fan_system_models(self) -> IDFCollection[FanSystemModel]:
        """All ``Fan:SystemModel`` objects in the document. Versatile simple fan that can be used in variable air volume, constant volume, on-off cycling, two-speed or multi-speed applications. Performance at different flow rates, or speed levels, is determ..."""
    @property
    def fan_variable_volumes(self) -> IDFCollection[FanVariableVolume]:
        """All ``Fan:VariableVolume`` objects in the document. Variable air volume fan where the electric power input varies according to a performance curve as a function of flow fraction."""
    @property
    def fan_zone_exhausts(self) -> IDFCollection[FanZoneExhaust]:
        """All ``Fan:ZoneExhaust`` objects in the document. Models a fan that exhausts air from a zone."""
    @property
    def fault_model_enthalpy_sensor_offset_outdoor_airs(
        self,
    ) -> IDFCollection[FaultModelEnthalpySensorOffsetOutdoorAir]:
        """All ``FaultModel:EnthalpySensorOffset:OutdoorAir`` objects in the document. This object describes outdoor air enthalpy sensor offset"""
    @property
    def fault_model_enthalpy_sensor_offset_return_airs(self) -> IDFCollection[FaultModelEnthalpySensorOffsetReturnAir]:
        """All ``FaultModel:EnthalpySensorOffset:ReturnAir`` objects in the document. This object describes return air enthalpy sensor offset"""
    @property
    def fault_model_fouling_air_filters(self) -> IDFCollection[FaultModelFoulingAirFilter]:
        """All ``FaultModel:Fouling:AirFilter`` objects in the document. This object describes fault of dirty air filters"""
    @property
    def fault_model_fouling_boilers(self) -> IDFCollection[FaultModelFoulingBoiler]:
        """All ``FaultModel:Fouling:Boiler`` objects in the document. This object describes the fouling fault of boilers with water-based heat exchangers"""
    @property
    def fault_model_fouling_chillers(self) -> IDFCollection[FaultModelFoulingChiller]:
        """All ``FaultModel:Fouling:Chiller`` objects in the document. This object describes the fouling fault of chillers with water-cooled condensers"""
    @property
    def fault_model_fouling_coils(self) -> IDFCollection[FaultModelFoulingCoil]:
        """All ``FaultModel:Fouling:Coil`` objects in the document. This object describes fouling water heating or cooling coils"""
    @property
    def fault_model_fouling_cooling_towers(self) -> IDFCollection[FaultModelFoulingCoolingTower]:
        """All ``FaultModel:Fouling:CoolingTower`` objects in the document. This object describes the fault of fouling cooling towers"""
    @property
    def fault_model_fouling_evaporative_coolers(self) -> IDFCollection[FaultModelFoulingEvaporativeCooler]:
        """All ``FaultModel:Fouling:EvaporativeCooler`` objects in the document. This object describes the fouling fault of the wetted coil evaporative cooler"""
    @property
    def fault_model_humidistat_offsets(self) -> IDFCollection[FaultModelHumidistatOffset]:
        """All ``FaultModel:HumidistatOffset`` objects in the document. This object describes fault of humidistat offset"""
    @property
    def fault_model_humidity_sensor_offset_outdoor_airs(
        self,
    ) -> IDFCollection[FaultModelHumiditySensorOffsetOutdoorAir]:
        """All ``FaultModel:HumiditySensorOffset:OutdoorAir`` objects in the document. This object describes outdoor air humidity sensor offset"""
    @property
    def fault_model_temperature_sensor_offset_chiller_supply_waters(
        self,
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetChillerSupplyWater]:
        """All ``FaultModel:TemperatureSensorOffset:ChillerSupplyWater`` objects in the document. This object describes fault of chiller supply water temperature sensor offset"""
    @property
    def fault_model_temperature_sensor_offset_coil_supply_airs(
        self,
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetCoilSupplyAir]:
        """All ``FaultModel:TemperatureSensorOffset:CoilSupplyAir`` objects in the document. This object describes fault of coil supply air temperature sensor offset"""
    @property
    def fault_model_temperature_sensor_offset_condenser_supply_waters(
        self,
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetCondenserSupplyWater]:
        """All ``FaultModel:TemperatureSensorOffset:CondenserSupplyWater`` objects in the document. This object describes fault of condenser supply water temperature sensor offset"""
    @property
    def fault_model_temperature_sensor_offset_outdoor_airs(
        self,
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetOutdoorAir]:
        """All ``FaultModel:TemperatureSensorOffset:OutdoorAir`` objects in the document. This object describes outdoor air temperature sensor offset"""
    @property
    def fault_model_temperature_sensor_offset_return_airs(
        self,
    ) -> IDFCollection[FaultModelTemperatureSensorOffsetReturnAir]:
        """All ``FaultModel:TemperatureSensorOffset:ReturnAir`` objects in the document. This object describes return air temperature sensor offset"""
    @property
    def fault_model_thermostat_offsets(self) -> IDFCollection[FaultModelThermostatOffset]:
        """All ``FaultModel:ThermostatOffset`` objects in the document. This object describes fault of thermostat offset"""
    @property
    def fenestration_surface_detaileds(self) -> IDFCollection[FenestrationSurfaceDetailed]:
        """All ``FenestrationSurface:Detailed`` objects in the document. Allows for detailed entry of subsurfaces (windows, doors, glass doors, tubular daylighting devices)."""
    @property
    def fenestration_surfaces(self) -> IDFCollection[FenestrationSurfaceDetailed]:
        """All ``FenestrationSurface:Detailed`` objects in the document. Allows for detailed entry of subsurfaces (windows, doors, glass doors, tubular daylighting devices)."""
    @property
    def floor_adiabatics(self) -> IDFCollection[FloorAdiabatic]:
        """All ``Floor:Adiabatic`` objects in the document. Allows for simplified entry of exterior floors ignoring ground contact or interior floors. View Factor to Ground is automatically calculated."""
    @property
    def floor_detaileds(self) -> IDFCollection[FloorDetailed]:
        """All ``Floor:Detailed`` objects in the document. Allows for detailed entry of floor heat transfer surfaces."""
    @property
    def floor_ground_contacts(self) -> IDFCollection[FloorGroundContact]:
        """All ``Floor:GroundContact`` objects in the document. Allows for simplified entry of exterior floors with ground contact. View Factors to Ground is automatically calculated."""
    @property
    def floor_interzones(self) -> IDFCollection[FloorInterzone]:
        """All ``Floor:Interzone`` objects in the document. Allows for simplified entry of floors using adjacent zone (interzone) heat transfer - adjacent surface should be a ceiling."""
    @property
    def fluid_cooler_single_speeds(self) -> IDFCollection[FluidCoolerSingleSpeed]:
        """All ``FluidCooler:SingleSpeed`` objects in the document. The fluid cooler is modeled as a cross flow heat exchanger (both streams unmixed) with single-speed fans (induced draft configuration)."""
    @property
    def fluid_cooler_two_speeds(self) -> IDFCollection[FluidCoolerTwoSpeed]:
        """All ``FluidCooler:TwoSpeed`` objects in the document. The fluid cooler is modeled as a cross flow heat exchanger (both streams unmixed) with two-speed fans (induced draft configuration)."""
    @property
    def fluid_properties_concentrations(self) -> IDFCollection[FluidPropertiesConcentration]:
        """All ``FluidProperties:Concentration`` objects in the document. fluid properties for water/other fluid mixtures"""
    @property
    def fluid_properties_glycol_concentrations(self) -> IDFCollection[FluidPropertiesGlycolConcentration]:
        """All ``FluidProperties:GlycolConcentration`` objects in the document. glycol and what concentration it is"""
    @property
    def fluid_properties_names(self) -> IDFCollection[FluidPropertiesName]:
        """All ``FluidProperties:Name`` objects in the document. potential fluid name/type in the input file repeat this object for each fluid"""
    @property
    def fluid_properties_saturateds(self) -> IDFCollection[FluidPropertiesSaturated]:
        """All ``FluidProperties:Saturated`` objects in the document. fluid properties for the saturated region"""
    @property
    def fluid_properties_superheateds(self) -> IDFCollection[FluidPropertiesSuperheated]:
        """All ``FluidProperties:Superheated`` objects in the document. fluid properties for the superheated region"""
    @property
    def fluid_properties_temperatures(self) -> IDFCollection[FluidPropertiesTemperatures]:
        """All ``FluidProperties:Temperatures`` objects in the document. property values for fluid properties list of up to 250 temperatures, note that number of property values must match the number of properties in other words, there must be a one-to-one correspondenc..."""
    @property
    def foundation_kiva_settings(self) -> IDFCollection[FoundationKivaSettings]:
        """All ``Foundation:Kiva:Settings`` objects in the document. Settings applied across all Kiva foundation calculations. Object is not required. If not defined, defaults will be applied."""
    @property
    def foundation_kivas(self) -> IDFCollection[FoundationKiva]:
        """All ``Foundation:Kiva`` objects in the document. Refined definition of the foundation surface construction used to inform two-dimensional heat transfer calculated using the Kiva ground heat transfer methodology."""
    @property
    def fuel_factors(self) -> IDFCollection[FuelFactors]:
        """All ``FuelFactors`` objects in the document. Provides Fuel Factors for Emissions as well as Source=>Site conversions. OtherFuel1, OtherFuel2 provide options for users who want to create and use fuels that may not be mainstream (biomass, wood,..."""
    @property
    def gas_equipment(self) -> IDFCollection[GasEquipment]:
        """All ``GasEquipment`` objects in the document. Sets internal gains and contaminant rates for gas equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applic..."""
    @property
    def gas_equipment_definitions(self) -> IDFCollection[GasEquipmentDefinition]:
        """All ``GasEquipment:Definition`` objects in the document. Defines the physical characteristics (design level and heat gain fractions) for gas equipment. Referenced by one or more GasEquipment:Instance objects."""
    @property
    def gas_equipment_instances(self) -> IDFCollection[GasEquipmentInstance]:
        """All ``GasEquipment:Instance`` objects in the document. Sets internal gains and contaminant rates for gas equipment in the zone. The physical characteristics are given by the referenced GasEquipment:Definition object. If a ZoneList, SpaceList, or a Zone..."""
    @property
    def gas_equipments(self) -> IDFCollection[GasEquipment]:
        """All ``GasEquipment`` objects in the document. Sets internal gains and contaminant rates for gas equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applic..."""
    @property
    def generator_combustion_turbines(self) -> IDFCollection[GeneratorCombustionTurbine]:
        """All ``Generator:CombustionTurbine`` objects in the document. This generator model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Generator performance curves are generated by fitting catalog data to second order pol..."""
    @property
    def generator_fuel_cell_air_supplies(self) -> IDFCollection[GeneratorFuelCellAirSupply]:
        """All ``Generator:FuelCell:AirSupply`` objects in the document. Used to define details of the air supply subsystem for a fuel cell power generator."""
    @property
    def generator_fuel_cell_auxiliary_heaters(self) -> IDFCollection[GeneratorFuelCellAuxiliaryHeater]:
        """All ``Generator:FuelCell:AuxiliaryHeater`` objects in the document. Intended for modeling an auxiliary heater for a fuel cell power generator, however this portion of the model is not yet available. The program still requires one of these objects be included even t..."""
    @property
    def generator_fuel_cell_electrical_storages(self) -> IDFCollection[GeneratorFuelCellElectricalStorage]:
        """All ``Generator:FuelCell:ElectricalStorage`` objects in the document. Used to describe the electrical storage subsystem for a fuel cell power generator. The electrical storage model is a very simple 'constrained bucket' model. Note that this electrical storage is emb..."""
    @property
    def generator_fuel_cell_exhaust_gas_to_water_heat_exchangers(
        self,
    ) -> IDFCollection[GeneratorFuelCellExhaustGasToWaterHeatExchanger]:
        """All ``Generator:FuelCell:ExhaustGasToWaterHeatExchanger`` objects in the document. Describes the exhaust gas heat exchanger subsystem of a fuel cell power generator used to recovery thermal energy"""
    @property
    def generator_fuel_cell_inverters(self) -> IDFCollection[GeneratorFuelCellInverter]:
        """All ``Generator:FuelCell:Inverter`` objects in the document. Used to describe the power condition unit subsystem of a fuel cell power generator. This object models an inverter system contained within a fuel cell system that converts from direct current (DC) ..."""
    @property
    def generator_fuel_cell_power_modules(self) -> IDFCollection[GeneratorFuelCellPowerModule]:
        """All ``Generator:FuelCell:PowerModule`` objects in the document. Describe the core power module subsystem of a fuel cell power generator. This includes the fuel cell stack, fuel reformer, and whatever ancillary devices are included inside. If the model has multi..."""
    @property
    def generator_fuel_cell_stack_coolers(self) -> IDFCollection[GeneratorFuelCellStackCooler]:
        """All ``Generator:FuelCell:StackCooler`` objects in the document. This object is optional and is used to define details needed to model the stack cooler on PEMFC."""
    @property
    def generator_fuel_cell_water_supplies(self) -> IDFCollection[GeneratorFuelCellWaterSupply]:
        """All ``Generator:FuelCell:WaterSupply`` objects in the document. Used to provide details of the water supply subsystem for a fuel cell power generator. This water is used for steam reforming of the fuel and is not the same as the water used for thermal heat reco..."""
    @property
    def generator_fuel_cells(self) -> IDFCollection[GeneratorFuelCell]:
        """All ``Generator:FuelCell`` objects in the document. This generator model is the FC model from IEA Annex 42"""
    @property
    def generator_fuel_supplies(self) -> IDFCollection[GeneratorFuelSupply]:
        """All ``Generator:FuelSupply`` objects in the document. Used only with Generator:FuelCell and Generator:MicroCHP"""
    @property
    def generator_internal_combustion_engines(self) -> IDFCollection[GeneratorInternalCombustionEngine]:
        """All ``Generator:InternalCombustionEngine`` objects in the document. This generator model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Engine performance curves are generated by fitting catalog data to second order polyno..."""
    @property
    def generator_micro_chp_non_normalized_parameters(self) -> IDFCollection[GeneratorMicroCHPNonNormalizedParameters]:
        """All ``Generator:MicroCHP:NonNormalizedParameters`` objects in the document. This object is referenced by a Generator:MicroCHP object and provides the non-normalized parameters for the MicroCHP generator model."""
    @property
    def generator_micro_chps(self) -> IDFCollection[GeneratorMicroCHP]:
        """All ``Generator:MicroCHP`` objects in the document. Small-scale combined heat and power (micro CHP) electric generator using the model developed by IEA/ECBCS Annex 42 see www.cogen-sim.net. The model was developed for both internal combustion and St..."""
    @property
    def generator_micro_turbines(self) -> IDFCollection[GeneratorMicroTurbine]:
        """All ``Generator:MicroTurbine`` objects in the document. MicroTurbine generators are small combustion turbines (e.g., 25kW to 500kW). The model calculates electrical power output, fuel use, standby and ancillary power. Energy recovery from exhaust air ca..."""
    @property
    def generator_photovoltaics(self) -> IDFCollection[GeneratorPhotovoltaic]:
        """All ``Generator:Photovoltaic`` objects in the document. Describes an array of photovoltaic (PV) modules. A series of different PV arrays can be connected to a single electric load center (and inverter) by listing them all in an ElectricLoadCenter:Genera..."""
    @property
    def generator_pv_watts(self) -> IDFCollection[GeneratorPVWatts]:
        """All ``Generator:PVWatts`` objects in the document. Describes a simple set of inputs for an array of photovoltaic (PV) modules as described in the PVWatts software. A series of different PVWatts arrays can be connected to a single electric load cent..."""
    @property
    def generator_wind_turbines(self) -> IDFCollection[GeneratorWindTurbine]:
        """All ``Generator:WindTurbine`` objects in the document. Wind turbine generator."""
    @property
    def geometry_transforms(self) -> IDFCollection[GeometryTransform]:
        """All ``GeometryTransform`` objects in the document. Provides a simple method of altering the footprint geometry of a model. The intent is to provide a single parameter that can be used to reshape the building description contained in the rest of the..."""
    @property
    def glazed_door_interzones(self) -> IDFCollection[GlazedDoorInterzone]:
        """All ``GlazedDoor:Interzone`` objects in the document. Allows for simplified entry of interzone (glass interior) doors (adjacent to other zones)."""
    @property
    def glazed_doors(self) -> IDFCollection[GlazedDoor]:
        """All ``GlazedDoor`` objects in the document. Allows for simplified entry of glass Doors."""
    @property
    def global_geometry_rules(self) -> IDFCollection[GlobalGeometryRules]:
        """All ``GlobalGeometryRules`` objects in the document. Specifies the geometric rules used to describe the input of surface vertices and daylighting reference points."""
    @property
    def ground_heat_exchanger_horizontal_trenches(self) -> IDFCollection[GroundHeatExchangerHorizontalTrench]:
        """All ``GroundHeatExchanger:HorizontalTrench`` objects in the document. This models a horizontal heat exchanger placed in a series of trenches The model uses the PipingSystem:Underground underlying algorithms, but provides a more usable input interface."""
    @property
    def ground_heat_exchanger_ponds(self) -> IDFCollection[GroundHeatExchangerPond]:
        """All ``GroundHeatExchanger:Pond`` objects in the document. A model of a shallow pond with immersed pipe loops. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector."""
    @property
    def ground_heat_exchanger_response_factors(self) -> IDFCollection[GroundHeatExchangerResponseFactors]:
        """All ``GroundHeatExchanger:ResponseFactors`` objects in the document. Response factor definitions from third-party tool, commonly referred to a 'g-functions'"""
    @property
    def ground_heat_exchanger_slinkies(self) -> IDFCollection[GroundHeatExchangerSlinky]:
        """All ``GroundHeatExchanger:Slinky`` objects in the document. This models a slinky horizontal heat exchanger placed in a series of trenches The model uses the model developed by: Xiong, Z., D.E. Fisher, and J.D. Spitler. 2015. Development and Validation of a ..."""
    @property
    def ground_heat_exchanger_surfaces(self) -> IDFCollection[GroundHeatExchangerSurface]:
        """All ``GroundHeatExchanger:Surface`` objects in the document. A hydronic surface/panel consisting of a multi-layer construction with embedded rows of tubes. Typically used in hybrid geothermal systems and included in the condenser loop. This component may als..."""
    @property
    def ground_heat_exchanger_systems(self) -> IDFCollection[GroundHeatExchangerSystem]:
        """All ``GroundHeatExchanger:System`` objects in the document. Models vertical ground heat exchangers systems using the response factor approach developed by Eskilson. Response factors are calculated using a finite line source model assuming uniform heat flux ..."""
    @property
    def ground_heat_exchanger_vertical_arrays(self) -> IDFCollection[GroundHeatExchangerVerticalArray]:
        """All ``GroundHeatExchanger:Vertical:Array`` objects in the document."""
    @property
    def ground_heat_exchanger_vertical_properties(self) -> IDFCollection[GroundHeatExchangerVerticalProperties]:
        """All ``GroundHeatExchanger:Vertical:Properties`` objects in the document. Properties for vertical ground heat exchanger systems"""
    @property
    def ground_heat_exchanger_vertical_singles(self) -> IDFCollection[GroundHeatExchangerVerticalSingle]:
        """All ``GroundHeatExchanger:Vertical:Single`` objects in the document."""
    @property
    def ground_heat_exchanger_vertical_sizing_rectangles(
        self,
    ) -> IDFCollection[GroundHeatExchangerVerticalSizingRectangle]:
        """All ``GroundHeatExchanger:Vertical:Sizing:Rectangle`` objects in the document. Specifies parameters to be used for Ground Heat Exchanger borehole field design and sizing."""
    @property
    def ground_heat_transfer_basement_auto_grids(self) -> IDFCollection[GroundHeatTransferBasementAutoGrid]:
        """All ``GroundHeatTransfer:Basement:AutoGrid`` objects in the document. AutoGrid only necessary when EquivSizing is false If the modeled building is not a rectangle or square, Equivalent sizing MUST be used to get accurate results"""
    @property
    def ground_heat_transfer_basement_bldg_datas(self) -> IDFCollection[GroundHeatTransferBasementBldgData]:
        """All ``GroundHeatTransfer:Basement:BldgData`` objects in the document. Specifies the surface and gravel thicknesses used for the Basement preprocessor ground heat transfer simulation."""
    @property
    def ground_heat_transfer_basement_com_bldgs(self) -> IDFCollection[GroundHeatTransferBasementComBldg]:
        """All ``GroundHeatTransfer:Basement:ComBldg`` objects in the document. ComBldg contains the monthly average temperatures (C) and possibility of daily variation amplitude"""
    @property
    def ground_heat_transfer_basement_equiv_auto_grids(self) -> IDFCollection[GroundHeatTransferBasementEquivAutoGrid]:
        """All ``GroundHeatTransfer:Basement:EquivAutoGrid`` objects in the document. EquivAutoGrid necessary when EquivSizing=TRUE, TRUE is is the normal case."""
    @property
    def ground_heat_transfer_basement_equiv_slabs(self) -> IDFCollection[GroundHeatTransferBasementEquivSlab]:
        """All ``GroundHeatTransfer:Basement:EquivSlab`` objects in the document. Using an equivalent slab allows non-rectangular shapes to be modeled accurately. The simulation default should be EquivSizing=True"""
    @property
    def ground_heat_transfer_basement_insulations(self) -> IDFCollection[GroundHeatTransferBasementInsulation]:
        """All ``GroundHeatTransfer:Basement:Insulation`` objects in the document. Describes the insulation used on an exterior basement wall for the Basement preprocessor ground heat transfer simulation."""
    @property
    def ground_heat_transfer_basement_interiors(self) -> IDFCollection[GroundHeatTransferBasementInterior]:
        """All ``GroundHeatTransfer:Basement:Interior`` objects in the document. Provides the information needed to simulate the inside boundary conditions for the Basement preprocessor ground heat transfer simulation."""
    @property
    def ground_heat_transfer_basement_manual_grids(self) -> IDFCollection[GroundHeatTransferBasementManualGrid]:
        """All ``GroundHeatTransfer:Basement:ManualGrid`` objects in the document. Manual Grid only necessary using manual gridding (not recommended)"""
    @property
    def ground_heat_transfer_basement_matl_props(self) -> IDFCollection[GroundHeatTransferBasementMatlProps]:
        """All ``GroundHeatTransfer:Basement:MatlProps`` objects in the document. Specifies the material properties for the Basement preprocessor ground heat transfer simulation. Only the Foundation Wall, Floor Slab, Soil, and Gravel properties are currently used."""
    @property
    def ground_heat_transfer_basement_sim_parameters(self) -> IDFCollection[GroundHeatTransferBasementSimParameters]:
        """All ``GroundHeatTransfer:Basement:SimParameters`` objects in the document. Specifies certain parameters that control the Basement preprocessor ground heat transfer simulation."""
    @property
    def ground_heat_transfer_basement_surface_props(self) -> IDFCollection[GroundHeatTransferBasementSurfaceProps]:
        """All ``GroundHeatTransfer:Basement:SurfaceProps`` objects in the document. Specifies the soil surface properties for the Basement preprocessor ground heat transfer simulation."""
    @property
    def ground_heat_transfer_basement_xfaces(self) -> IDFCollection[GroundHeatTransferBasementXFACE]:
        """All ``GroundHeatTransfer:Basement:XFACE`` objects in the document. This is only needed when using manual gridding (not recommended) XFACE: X Direction cell face coordinates: m"""
    @property
    def ground_heat_transfer_basement_yfaces(self) -> IDFCollection[GroundHeatTransferBasementYFACE]:
        """All ``GroundHeatTransfer:Basement:YFACE`` objects in the document. This is only needed when using manual gridding (not recommended) YFACE: Y Direction cell face coordinates: m"""
    @property
    def ground_heat_transfer_basement_zfaces(self) -> IDFCollection[GroundHeatTransferBasementZFACE]:
        """All ``GroundHeatTransfer:Basement:ZFACE`` objects in the document. This is only needed when using manual gridding (not recommended) ZFACE: Z Direction cell face coordinates: m"""
    @property
    def ground_heat_transfer_controls(self) -> IDFCollection[GroundHeatTransferControl]:
        """All ``GroundHeatTransfer:Control`` objects in the document. Object determines if the Slab and Basement preprocessors are going to be executed."""
    @property
    def ground_heat_transfer_slab_auto_grids(self) -> IDFCollection[GroundHeatTransferSlabAutoGrid]:
        """All ``GroundHeatTransfer:Slab:AutoGrid`` objects in the document. AutoGrid only necessary when EquivalentSlab option not chosen. Not normally needed by EnergyPlus users. This object permits user selection of rectangular slab dimensions. NO SLAB DIMENSIONS LESS TH..."""
    @property
    def ground_heat_transfer_slab_bldg_props(self) -> IDFCollection[GroundHeatTransferSlabBldgProps]:
        """All ``GroundHeatTransfer:Slab:BldgProps`` objects in the document. Object provides information about the building and its operating conditions Monthly Average Temperature SetPoint fields specify the average indoor building set point temperatures for each month of ..."""
    @property
    def ground_heat_transfer_slab_bound_conds(self) -> IDFCollection[GroundHeatTransferSlabBoundConds]:
        """All ``GroundHeatTransfer:Slab:BoundConds`` objects in the document. Supplies some of the boundary conditions used in the ground heat transfer calculations."""
    @property
    def ground_heat_transfer_slab_equivalent_slabs(self) -> IDFCollection[GroundHeatTransferSlabEquivalentSlab]:
        """All ``GroundHeatTransfer:Slab:EquivalentSlab`` objects in the document. Using an equivalent slab allows non-rectangular shapes to be modeled accurately. Object uses the area - perimeter (area/perimeter) ratio to determine the size of an equivalent rectangular slab. Ene..."""
    @property
    def ground_heat_transfer_slab_insulations(self) -> IDFCollection[GroundHeatTransferSlabInsulation]:
        """All ``GroundHeatTransfer:Slab:Insulation`` objects in the document. This object supplies the information about insulation used around the slab. There are two possible configurations: under the slab or vertical insulation around the slab."""
    @property
    def ground_heat_transfer_slab_manual_grids(self) -> IDFCollection[GroundHeatTransferSlabManualGrid]:
        """All ``GroundHeatTransfer:Slab:ManualGrid`` objects in the document. Manual Grid only necessary when using manual gridding (not recommended) Used only in special cases when previous two objects are not used. User must input complete gridding information."""
    @property
    def ground_heat_transfer_slab_materials(self) -> IDFCollection[GroundHeatTransferSlabMaterials]:
        """All ``GroundHeatTransfer:Slab:Materials`` objects in the document. Object gives an overall description of the slab ground heat transfer model."""
    @property
    def ground_heat_transfer_slab_matl_props(self) -> IDFCollection[GroundHeatTransferSlabMatlProps]:
        """All ``GroundHeatTransfer:Slab:MatlProps`` objects in the document. This object contains the material properties for the materials used in the model. The fields are mostly self explanatory."""
    @property
    def ground_heat_transfer_slab_xfaces(self) -> IDFCollection[GroundHeatTransferSlabXFACE]:
        """All ``GroundHeatTransfer:Slab:XFACE`` objects in the document. This is only needed when using manual gridding (not recommended) XFACE: X Direction cell face coordinates: m"""
    @property
    def ground_heat_transfer_slab_yfaces(self) -> IDFCollection[GroundHeatTransferSlabYFACE]:
        """All ``GroundHeatTransfer:Slab:YFACE`` objects in the document. This is only needed when using manual gridding (not recommended) YFACE: Y Direction cell face coordinates: m,"""
    @property
    def ground_heat_transfer_slab_zfaces(self) -> IDFCollection[GroundHeatTransferSlabZFACE]:
        """All ``GroundHeatTransfer:Slab:ZFACE`` objects in the document. This is only needed when using manual gridding (not recommended) ZFACE: Z Direction cell face coordinates: m"""
    @property
    def headered_pumps_constant_speeds(self) -> IDFCollection[HeaderedPumpsConstantSpeed]:
        """All ``HeaderedPumps:ConstantSpeed`` objects in the document. This Headered pump object describes a pump bank with more than 1 pump in parallel"""
    @property
    def headered_pumps_variable_speeds(self) -> IDFCollection[HeaderedPumpsVariableSpeed]:
        """All ``HeaderedPumps:VariableSpeed`` objects in the document. This Headered pump object describes a pump bank with more than 1 pump in parallel"""
    @property
    def heat_balance_algorithms(self) -> IDFCollection[HeatBalanceAlgorithm]:
        """All ``HeatBalanceAlgorithm`` objects in the document. Determines which Heat Balance Algorithm will be used ie. CTF (Conduction Transfer Functions), EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions). Advanced/Research Usage..."""
    @property
    def heat_balance_settings_conduction_finite_differences(
        self,
    ) -> IDFCollection[HeatBalanceSettingsConductionFiniteDifference]:
        """All ``HeatBalanceSettings:ConductionFiniteDifference`` objects in the document. Determines settings for the Conduction Finite Difference algorithm for surface heat transfer modeling."""
    @property
    def heat_exchanger_air_to_air_flat_plates(self) -> IDFCollection[HeatExchangerAirToAirFlatPlate]:
        """All ``HeatExchanger:AirToAir:FlatPlate`` objects in the document. Flat plate air-to-air heat exchanger, typically used for exhaust or relief air heat recovery."""
    @property
    def heat_exchanger_air_to_air_sensible_and_latents(self) -> IDFCollection[HeatExchangerAirToAirSensibleAndLatent]:
        """All ``HeatExchanger:AirToAir:SensibleAndLatent`` objects in the document. This object models an air-to-air heat exchanger using effectiveness relationships. The heat exchanger can transfer sensible energy, latent energy, or both between the supply (primary) and exhaust (..."""
    @property
    def heat_exchanger_desiccant_balanced_flow_performance_data_type1s(
        self,
    ) -> IDFCollection[HeatExchangerDesiccantBalancedFlowPerformanceDataType1]:
        """All ``HeatExchanger:Desiccant:BalancedFlow:PerformanceDataType1`` objects in the document. RTO = B1 + B2*RWI + B3*RTI + B4*(RWI/RTI) + B5*PWI + B6*PTI + B7*(PWI/PTI) + B8*RFV RWO = C1 + C2*RWI + C3*RTI + C4*(RWI/RTI) + C5*PWI + C6*PTI + C7*(PWI/PTI) + C8*RFV where, RTO = Dry-bulb tempera..."""
    @property
    def heat_exchanger_desiccant_balanced_flows(self) -> IDFCollection[HeatExchangerDesiccantBalancedFlow]:
        """All ``HeatExchanger:Desiccant:BalancedFlow`` objects in the document. This object models a balanced desiccant heat exchanger. The heat exchanger transfers both sensible and latent energy between the process and regeneration air streams. The air flow rate and face vel..."""
    @property
    def heat_exchanger_fluid_to_fluids(self) -> IDFCollection[HeatExchangerFluidToFluid]:
        """All ``HeatExchanger:FluidToFluid`` objects in the document. A fluid/fluid heat exchanger designed to couple the supply side of one loop to the demand side of another loop Loops can be either plant or condenser loops but no air side connections are allowed"""
    @property
    def heat_pump_air_to_water_fuel_fired_coolings(self) -> IDFCollection[HeatPumpAirToWaterFuelFiredCooling]:
        """All ``HeatPump:AirToWater:FuelFired:Cooling`` objects in the document. The object defines a fuel-fired absorption heat pump based on equation-fit models."""
    @property
    def heat_pump_air_to_water_fuel_fired_heatings(self) -> IDFCollection[HeatPumpAirToWaterFuelFiredHeating]:
        """All ``HeatPump:AirToWater:FuelFired:Heating`` objects in the document. The object defines a fuel-fired absorption heat pump based on equation-fit models."""
    @property
    def heat_pump_air_to_waters(self) -> IDFCollection[HeatPumpAirToWater]:
        """All ``HeatPump:AirToWater`` objects in the document. air-to-water heat pump system which provides either chilled or hot water with single- or variable speed compressors."""
    @property
    def heat_pump_plant_loop_eir_coolings(self) -> IDFCollection[HeatPumpPlantLoopEIRCooling]:
        """All ``HeatPump:PlantLoop:EIR:Cooling`` objects in the document. An EIR formulated water to water heat pump model, cooling operation."""
    @property
    def heat_pump_plant_loop_eir_heatings(self) -> IDFCollection[HeatPumpPlantLoopEIRHeating]:
        """All ``HeatPump:PlantLoop:EIR:Heating`` objects in the document. An EIR formulated water to water heat pump model, heating operation"""
    @property
    def heat_pump_water_to_water_equation_fit_coolings(self) -> IDFCollection[HeatPumpWaterToWaterEquationFitCooling]:
        """All ``HeatPump:WaterToWater:EquationFit:Cooling`` objects in the document. simple water-water heat pump curve-fit model"""
    @property
    def heat_pump_water_to_water_equation_fit_heatings(self) -> IDFCollection[HeatPumpWaterToWaterEquationFitHeating]:
        """All ``HeatPump:WaterToWater:EquationFit:Heating`` objects in the document. simple water-water hp curve-fit model"""
    @property
    def heat_pump_water_to_water_parameter_estimation_coolings(
        self,
    ) -> IDFCollection[HeatPumpWaterToWaterParameterEstimationCooling]:
        """All ``HeatPump:WaterToWater:ParameterEstimation:Cooling`` objects in the document. OSU parameter estimation model"""
    @property
    def heat_pump_water_to_water_parameter_estimation_heatings(
        self,
    ) -> IDFCollection[HeatPumpWaterToWaterParameterEstimationHeating]:
        """All ``HeatPump:WaterToWater:ParameterEstimation:Heating`` objects in the document. OSU parameter estimation model"""
    @property
    def hot_water_equipment(self) -> IDFCollection[HotWaterEquipment]:
        """All ``HotWaterEquipment`` objects in the document. Sets internal gains for hot water equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and..."""
    @property
    def hot_water_equipment_definitions(self) -> IDFCollection[HotWaterEquipmentDefinition]:
        """All ``HotWaterEquipment:Definition`` objects in the document. Defines the physical characteristics (design level and heat gain fractions) for hot water equipment. Referenced by one or more HotWaterEquipment:Instance objects."""
    @property
    def hot_water_equipment_instances(self) -> IDFCollection[HotWaterEquipmentInstance]:
        """All ``HotWaterEquipment:Instance`` objects in the document. Sets internal gains for hot water equipment in the zone. The physical characteristics are given by the referenced HotWaterEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised ..."""
    @property
    def hot_water_equipments(self) -> IDFCollection[HotWaterEquipment]:
        """All ``HotWaterEquipment`` objects in the document. Sets internal gains for hot water equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and..."""
    @property
    def humidifier_steam_electrics(self) -> IDFCollection[HumidifierSteamElectric]:
        """All ``Humidifier:Steam:Electric`` objects in the document. Electrically heated steam humidifier with fan."""
    @property
    def humidifier_steam_gases(self) -> IDFCollection[HumidifierSteamGas]:
        """All ``Humidifier:Steam:Gas`` objects in the document. Natural gas fired steam humidifier with optional blower fan."""
    @property
    def hvac_system_root_finding_algorithms(self) -> IDFCollection[HVACSystemRootFindingAlgorithm]:
        """All ``HVACSystemRootFindingAlgorithm`` objects in the document. Specifies a HVAC system solver algorithm to find a root"""
    @property
    def hvac_template_plant_boiler_object_references(self) -> IDFCollection[HVACTemplatePlantBoilerObjectReference]:
        """All ``HVACTemplate:Plant:Boiler:ObjectReference`` objects in the document. This object references a detailed boiler object and adds it to an HVACTemplate:Plant:HotWaterLoop or MixedWaterLoop. The user must create a complete detailed boiler object with all required curve o..."""
    @property
    def hvac_template_plant_boilers(self) -> IDFCollection[HVACTemplatePlantBoiler]:
        """All ``HVACTemplate:Plant:Boiler`` objects in the document. This object adds a boiler to an HVACTemplate:Plant:HotWaterLoop or MixedWaterLoop."""
    @property
    def hvac_template_plant_chilled_water_loops(self) -> IDFCollection[HVACTemplatePlantChilledWaterLoop]:
        """All ``HVACTemplate:Plant:ChilledWaterLoop`` objects in the document. Plant and condenser loops to serve all HVACTemplate chilled water coils, chillers, and towers."""
    @property
    def hvac_template_plant_chiller_object_references(self) -> IDFCollection[HVACTemplatePlantChillerObjectReference]:
        """All ``HVACTemplate:Plant:Chiller:ObjectReference`` objects in the document. This object references a detailed chiller object and adds it to an HVACTemplate:Plant:ChilledWaterLoop. The user must create a complete detailed chiller object with all required curve or performanc..."""
    @property
    def hvac_template_plant_chillers(self) -> IDFCollection[HVACTemplatePlantChiller]:
        """All ``HVACTemplate:Plant:Chiller`` objects in the document. This object adds a chiller to an HVACTemplate:Plant:ChilledWaterLoop."""
    @property
    def hvac_template_plant_hot_water_loops(self) -> IDFCollection[HVACTemplatePlantHotWaterLoop]:
        """All ``HVACTemplate:Plant:HotWaterLoop`` objects in the document. Plant loop to serve all HVACTemplate hot water coils and boilers."""
    @property
    def hvac_template_plant_mixed_water_loops(self) -> IDFCollection[HVACTemplatePlantMixedWaterLoop]:
        """All ``HVACTemplate:Plant:MixedWaterLoop`` objects in the document. Central plant loop portion of a water source heat pump system."""
    @property
    def hvac_template_plant_tower_object_references(self) -> IDFCollection[HVACTemplatePlantTowerObjectReference]:
        """All ``HVACTemplate:Plant:Tower:ObjectReference`` objects in the document. This object references a detailed cooling tower object and adds it to an HVACTemplate:Plant:ChilledWaterLoop or MixedWaterLoop. The user must create a complete detailed cooling tower object with al..."""
    @property
    def hvac_template_plant_towers(self) -> IDFCollection[HVACTemplatePlantTower]:
        """All ``HVACTemplate:Plant:Tower`` objects in the document. This object adds a cooling tower to an HVACTemplate:Plant:ChilledWaterLoop or MixedWaterLoop."""
    @property
    def hvac_template_system_constant_volumes(self) -> IDFCollection[HVACTemplateSystemConstantVolume]:
        """All ``HVACTemplate:System:ConstantVolume`` objects in the document. Constant Air Volume air loop with optional chilled water cooling coil, optional heating coil and optional preheat."""
    @property
    def hvac_template_system_dedicated_outdoor_airs(self) -> IDFCollection[HVACTemplateSystemDedicatedOutdoorAir]:
        """All ``HVACTemplate:System:DedicatedOutdoorAir`` objects in the document. This object creates a dedicated outdoor air system that must be used with HVACTemplate:Zone:* objects for BaseboardHeat FanCoil PTAC PTHP WaterToAirHeatPump and VRF. Does not support HVACTemplate:Z..."""
    @property
    def hvac_template_system_dual_ducts(self) -> IDFCollection[HVACTemplateSystemDualDuct]:
        """All ``HVACTemplate:System:DualDuct`` objects in the document. Dual-duct constant volume or variable volume air loop"""
    @property
    def hvac_template_system_packaged_vavs(self) -> IDFCollection[HVACTemplateSystemPackagedVAV]:
        """All ``HVACTemplate:System:PackagedVAV`` objects in the document. Packaged Variable Air Volume (PVAV) air loop with optional heating coil and optional preheat."""
    @property
    def hvac_template_system_unitaries(self) -> IDFCollection[HVACTemplateSystemUnitary]:
        """All ``HVACTemplate:System:Unitary`` objects in the document. Unitary furnace with air conditioner"""
    @property
    def hvac_template_system_unitary_heat_pump_air_to_airs(
        self,
    ) -> IDFCollection[HVACTemplateSystemUnitaryHeatPumpAirToAir]:
        """All ``HVACTemplate:System:UnitaryHeatPump:AirToAir`` objects in the document. Unitary furnace with electric air-to-air heat pump"""
    @property
    def hvac_template_system_unitary_systems(self) -> IDFCollection[HVACTemplateSystemUnitarySystem]:
        """All ``HVACTemplate:System:UnitarySystem`` objects in the document. Unitary HVAC system with optional cooling and heating. Supports DX and chilled water, cooling, gas, electric, and hot water heating, air-to-air and water-to-air heat pumps."""
    @property
    def hvac_template_system_vavs(self) -> IDFCollection[HVACTemplateSystemVAV]:
        """All ``HVACTemplate:System:VAV`` objects in the document. Variable Air Volume (VAV) air loop with optional heating coil and optional preheat."""
    @property
    def hvac_template_system_vrfs(self) -> IDFCollection[HVACTemplateSystemVRF]:
        """All ``HVACTemplate:System:VRF`` objects in the document. Variable refrigerant flow (VRF) heat pump condensing unit. Serves one or more VRF zone terminal units (HVACTemplate:Zone:VRF)."""
    @property
    def hvac_template_thermostats(self) -> IDFCollection[HVACTemplateThermostat]:
        """All ``HVACTemplate:Thermostat`` objects in the document. Zone thermostat control. Referenced schedules must be defined elsewhere in the idf. Thermostat control type is dual setpoint with deadband. It is not necessary to create a thermostat object for eve..."""
    @property
    def hvac_template_zone_baseboard_heats(self) -> IDFCollection[HVACTemplateZoneBaseboardHeat]:
        """All ``HVACTemplate:Zone:BaseboardHeat`` objects in the document. Zone baseboard heating system."""
    @property
    def hvac_template_zone_constant_volumes(self) -> IDFCollection[HVACTemplateZoneConstantVolume]:
        """All ``HVACTemplate:Zone:ConstantVolume`` objects in the document. Zone terminal unit, constant volume, reheat optional. Referenced schedules must be defined elsewhere in the idf."""
    @property
    def hvac_template_zone_dual_ducts(self) -> IDFCollection[HVACTemplateZoneDualDuct]:
        """All ``HVACTemplate:Zone:DualDuct`` objects in the document. Zone terminal unit, dual-duct, constant or variable volume."""
    @property
    def hvac_template_zone_fan_coils(self) -> IDFCollection[HVACTemplateZoneFanCoil]:
        """All ``HVACTemplate:Zone:FanCoil`` objects in the document. 4 pipe fan coil unit with optional outdoor air."""
    @property
    def hvac_template_zone_ideal_loads_air_systems(self) -> IDFCollection[HVACTemplateZoneIdealLoadsAirSystem]:
        """All ``HVACTemplate:Zone:IdealLoadsAirSystem`` objects in the document. Zone with ideal air system that meets heating or cooling loads"""
    @property
    def hvac_template_zone_ptacs(self) -> IDFCollection[HVACTemplateZonePTAC]:
        """All ``HVACTemplate:Zone:PTAC`` objects in the document. Packaged Terminal Air Conditioner"""
    @property
    def hvac_template_zone_pthps(self) -> IDFCollection[HVACTemplateZonePTHP]:
        """All ``HVACTemplate:Zone:PTHP`` objects in the document. Packaged Terminal Heat Pump"""
    @property
    def hvac_template_zone_unitaries(self) -> IDFCollection[HVACTemplateZoneUnitary]:
        """All ``HVACTemplate:Zone:Unitary`` objects in the document. Zone terminal unit, constant volume, no controls."""
    @property
    def hvac_template_zone_vav_fan_powereds(self) -> IDFCollection[HVACTemplateZoneVAVFanPowered]:
        """All ``HVACTemplate:Zone:VAV:FanPowered`` objects in the document. Zone terminal unit, fan powered variable volume, reheat optional. Referenced schedules must be defined elsewhere in the idf."""
    @property
    def hvac_template_zone_vav_heat_and_cools(self) -> IDFCollection[HVACTemplateZoneVAVHeatAndCool]:
        """All ``HVACTemplate:Zone:VAV:HeatAndCool`` objects in the document. VAV system with VAV for both heating and cooling and optional reheat coil. For heating, this unit increases airflow first, then activates reheat coil."""
    @property
    def hvac_template_zone_vavs(self) -> IDFCollection[HVACTemplateZoneVAV]:
        """All ``HVACTemplate:Zone:VAV`` objects in the document. Zone terminal unit, variable volume, reheat optional. For heating, this unit activates reheat coil first, then increases airflow (if reverse action specified)."""
    @property
    def hvac_template_zone_vrfs(self) -> IDFCollection[HVACTemplateZoneVRF]:
        """All ``HVACTemplate:Zone:VRF`` objects in the document. Zone terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air or water-to-air heat pump). The VRF terminal units are served by an HVACTemplate:System:VRF system."""
    @property
    def hvac_template_zone_water_to_air_heat_pumps(self) -> IDFCollection[HVACTemplateZoneWaterToAirHeatPump]:
        """All ``HVACTemplate:Zone:WaterToAirHeatPump`` objects in the document. Water to Air Heat Pump to be used with HVACTemplate:Plant:MixedWaterLoop"""
    @property
    def hvac_templates(self) -> IDFCollection[HVACTemplateZoneIdealLoadsAirSystem]:
        """All ``HVACTemplate:Zone:IdealLoadsAirSystem`` objects in the document. Zone with ideal air system that meets heating or cooling loads"""
    @property
    def hybrid_model_zones(self) -> IDFCollection[HybridModelZone]:
        """All ``HybridModel:Zone`` objects in the document. Zones with measured air temperature data and a range of dates. If the range of temperature measurement dates includes a leap day, the weather data should include a leap day."""
    @property
    def ideal_loads(self) -> IDFCollection[ZoneHVACIdealLoadsAirSystem]:
        """All ``ZoneHVAC:IdealLoadsAirSystem`` objects in the document. Ideal system used to calculate loads without modeling a full HVAC system. All that is required for the ideal system are zone controls, zone equipment configurations, and the ideal loads system comp..."""
    @property
    def indoor_living_walls(self) -> IDFCollection[IndoorLivingWall]:
        """All ``IndoorLivingWall`` objects in the document. Indoor greenery systems such as indoor living walls are panels of plants, which grow hydroponically or from substrates. The living wall structures can be either free-standing or attached to walls. ..."""
    @property
    def infiltration(self) -> IDFCollection[ZoneInfiltrationDesignFlowRate]:
        """All ``ZoneInfiltration:DesignFlowRate`` objects in the document. Infiltration is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Infiltration=Idesign * FSchedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D..."""
    @property
    def internal_mass(self) -> IDFCollection[InternalMass]:
        """All ``InternalMass`` objects in the document. Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zo..."""
    @property
    def internal_masses(self) -> IDFCollection[InternalMass]:
        """All ``InternalMass`` objects in the document. Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zo..."""
    @property
    def life_cycle_cost_nonrecurring_costs(self) -> IDFCollection[LifeCycleCostNonrecurringCost]:
        """All ``LifeCycleCost:NonrecurringCost`` objects in the document. A non-recurring cost happens only once during the study period. For costs that occur more than once during the study period on a regular schedule, use the LifeCycleCost:RecurringCost object."""
    @property
    def life_cycle_cost_parameters(self) -> IDFCollection[LifeCycleCostParameters]:
        """All ``LifeCycleCost:Parameters`` objects in the document. Provides inputs related to the overall life-cycle analysis. It establishes many of the assumptions used in computing the present value. It is important that when comparing the results of multiple s..."""
    @property
    def life_cycle_cost_recurring_costs(self) -> IDFCollection[LifeCycleCostRecurringCosts]:
        """All ``LifeCycleCost:RecurringCosts`` objects in the document. Recurring costs are costs that repeat over time on a regular schedule during the study period. If costs associated with equipment do repeat but not on a regular schedule, use LifeCycleCost:Nonrecur..."""
    @property
    def life_cycle_cost_use_adjustments(self) -> IDFCollection[LifeCycleCostUseAdjustment]:
        """All ``LifeCycleCost:UseAdjustment`` objects in the document. Used by advanced users to adjust the energy or water use costs for future years. This should not be used for compensating for inflation but should only be used to increase the costs of energy or wa..."""
    @property
    def life_cycle_cost_use_price_escalations(self) -> IDFCollection[LifeCycleCostUsePriceEscalation]:
        """All ``LifeCycleCost:UsePriceEscalation`` objects in the document. Life cycle cost escalation factors. The values for this object may be found in the annual supplement to NIST Handbook 135 in Tables Ca-1 to Ca-5 and are included in an EnergyPlus dataset file."""
    @property
    def lights(self) -> IDFCollection[Lights]:
        """All ``Lights`` objects in the document. Sets internal gains for lights in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instanc..."""
    @property
    def lights_definitions(self) -> IDFCollection[LightsDefinition]:
        """All ``Lights:Definition`` objects in the document. Defines the physical characteristics (design level and heat gain fractions) for lights. Referenced by one or more Lights:Instance objects."""
    @property
    def lights_instances(self) -> IDFCollection[LightsInstance]:
        """All ``Lights:Instance`` objects in the document. Sets internal gains for lights in the zone. The physical characteristics are given by the referenced Lights:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space i..."""
    @property
    def load_profile_plants(self) -> IDFCollection[LoadProfilePlant]:
        """All ``LoadProfile:Plant`` objects in the document. Used to simulate a scheduled plant loop demand profile. Load and flow rate are specified using schedules. Positive values are heating loads, and negative values are cooling loads. The actual load m..."""
    @property
    def material_air_gaps(self) -> IDFCollection[MaterialAirGap]:
        """All ``Material:AirGap`` objects in the document. Air Space in Opaque Construction"""
    @property
    def material_airgap(self) -> IDFCollection[MaterialAirGap]:
        """All ``Material:AirGap`` objects in the document. Air Space in Opaque Construction"""
    @property
    def material_infrared_transparents(self) -> IDFCollection[MaterialInfraredTransparent]:
        """All ``Material:InfraredTransparent`` objects in the document. Special infrared transparent material. Similar to a Material:Nomass with low thermal resistance. High absorptance in both wavelengths. Area will be doubled internally to make internal radiant excha..."""
    @property
    def material_no_masses(self) -> IDFCollection[MaterialNoMass]:
        """All ``Material:NoMass`` objects in the document. Regular materials properties described whose principal description is R (Thermal Resistance)"""
    @property
    def material_nomass(self) -> IDFCollection[MaterialNoMass]:
        """All ``Material:NoMass`` objects in the document. Regular materials properties described whose principal description is R (Thermal Resistance)"""
    @property
    def material_property_glazing_spectral_datas(self) -> IDFCollection[MaterialPropertyGlazingSpectralData]:
        """All ``MaterialProperty:GlazingSpectralData`` objects in the document. Name is followed by up to 800 sets of normal-incidence measured values of [wavelength, transmittance, front reflectance, back reflectance] for wavelengths covering the solar spectrum (from about 0...."""
    @property
    def material_property_heat_and_moisture_transfer_diffusions(
        self,
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferDiffusion]:
        """All ``MaterialProperty:HeatAndMoistureTransfer:Diffusion`` objects in the document. HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between water vapor diffusion and relative humidity fraction Has no effect with other HeatBalanceAl..."""
    @property
    def material_property_heat_and_moisture_transfer_redistributions(
        self,
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferRedistribution]:
        """All ``MaterialProperty:HeatAndMoistureTransfer:Redistribution`` objects in the document. HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid transport coefficient and moisture content Has no effect with other HeatBalanceAlgor..."""
    @property
    def material_property_heat_and_moisture_transfer_settings(
        self,
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferSettings]:
        """All ``MaterialProperty:HeatAndMoistureTransfer:Settings`` objects in the document. HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Additional material properties for surfaces. Has no effect with other HeatBalanceAlgorithm solution algorithms"""
    @property
    def material_property_heat_and_moisture_transfer_sorption_isotherms(
        self,
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferSorptionIsotherm]:
        """All ``MaterialProperty:HeatAndMoistureTransfer:SorptionIsotherm`` objects in the document. HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between moisture content and relative humidity fraction. Has no effect with other HeatBalanceAlgori..."""
    @property
    def material_property_heat_and_moisture_transfer_suctions(
        self,
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferSuction]:
        """All ``MaterialProperty:HeatAndMoistureTransfer:Suction`` objects in the document. HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid suction transport coefficient and moisture content Has no effect with other HeatBala..."""
    @property
    def material_property_heat_and_moisture_transfer_thermal_conductivities(
        self,
    ) -> IDFCollection[MaterialPropertyHeatAndMoistureTransferThermalConductivity]:
        """All ``MaterialProperty:HeatAndMoistureTransfer:ThermalConductivity`` objects in the document. HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between thermal conductivity and moisture content Has no effect with other HeatBalanceAlgorithm sol..."""
    @property
    def material_property_moisture_penetration_depth_settings(
        self,
    ) -> IDFCollection[MaterialPropertyMoisturePenetrationDepthSettings]:
        """All ``MaterialProperty:MoisturePenetrationDepth:Settings`` objects in the document. Additional properties for moisture using EMPD procedure HeatBalanceAlgorithm choice=MoisturePenetrationDepthConductionTransferFunction only Has no effect with other HeatBalanceAlgorithm solution al..."""
    @property
    def material_property_phase_change_hystereses(self) -> IDFCollection[MaterialPropertyPhaseChangeHysteresis]:
        """All ``MaterialProperty:PhaseChangeHysteresis`` objects in the document. Additional properties for temperature dependent thermal conductivity and enthalpy for Phase Change Materials (PCM) with separate melting and freezing curves. HeatBalanceAlgorithm = CondFD (Conducti..."""
    @property
    def material_property_phase_changes(self) -> IDFCollection[MaterialPropertyPhaseChange]:
        """All ``MaterialProperty:PhaseChange`` objects in the document. Additional properties for temperature dependent thermal conductivity and enthalpy for Phase Change Materials (PCM) Name and temperature coefficient are followed by up to 100 sets of temperature-ent..."""
    @property
    def material_property_variable_absorptances(self) -> IDFCollection[MaterialPropertyVariableAbsorptance]:
        """All ``MaterialProperty:VariableAbsorptance`` objects in the document."""
    @property
    def material_property_variable_thermal_conductivities(
        self,
    ) -> IDFCollection[MaterialPropertyVariableThermalConductivity]:
        """All ``MaterialProperty:VariableThermalConductivity`` objects in the document. Additional properties for temperature dependent thermal conductivity using piecewise linear temperature-conductivity function. Name is followed by up to 100 sets of temperature-conductivity pairs. ..."""
    @property
    def material_roof_vegetations(self) -> IDFCollection[MaterialRoofVegetation]:
        """All ``Material:RoofVegetation`` objects in the document. EcoRoof model, plant layer plus soil layer Implemented by Portland State University (Sailor et al., January, 2007) only one material must be referenced per simulation though the same EcoRoof materi..."""
    @property
    def materials(self) -> IDFCollection[Material]:
        """All ``Material`` objects in the document. Regular materials described with full set of thermal properties"""
    @property
    def matrix_two_dimensions(self) -> IDFCollection[MatrixTwoDimension]:
        """All ``Matrix:TwoDimension`` objects in the document. matrix data in row-major order list each row keeping the columns in order number of values must equal N1 x N2"""
    @property
    def meter_custom_decrements(self) -> IDFCollection[MeterCustomDecrement]:
        """All ``Meter:CustomDecrement`` objects in the document. Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and..."""
    @property
    def meter_customs(self) -> IDFCollection[MeterCustom]:
        """All ``Meter:Custom`` objects in the document. Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and..."""
    @property
    def node_lists(self) -> IDFCollection[NodeList]:
        """All ``NodeList`` objects in the document. This object is used in places where lists of nodes may be needed, e.g. ZoneHVAC:EquipmentConnections field Zone Air Inlet Node or NodeList Name"""
    @property
    def other_equipment_definitions(self) -> IDFCollection[OtherEquipmentDefinition]:
        """All ``OtherEquipment:Definition`` objects in the document. Defines the physical characteristics (design level and heat gain fractions) for 'other' equipment. Referenced by one or more OtherEquipment:Instance objects."""
    @property
    def other_equipment_instances(self) -> IDFCollection[OtherEquipmentInstance]:
        """All ``OtherEquipment:Instance`` objects in the document. Sets internal gains or losses for 'other' equipment in the zone. The physical characteristics are given by the referenced OtherEquipment:Definition object. If a ZoneList, SpaceList, or a Zone compr..."""
    @property
    def other_equipments(self) -> IDFCollection[OtherEquipment]:
        """All ``OtherEquipment`` objects in the document. Sets internal gains or losses for 'other' equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spa..."""
    @property
    def outdoor_air_mixers(self) -> IDFCollection[OutdoorAirMixer]:
        """All ``OutdoorAir:Mixer`` objects in the document. Outdoor air mixer. Node names cannot be duplicated within a single OutdoorAir:Mixer object or across all outdoor air mixers."""
    @property
    def outdoor_air_node_lists(self) -> IDFCollection[OutdoorAirNodeList]:
        """All ``OutdoorAir:NodeList`` objects in the document. This object sets the temperature and humidity conditions for an outdoor air node using the weather data values. to vary outdoor air node conditions with height above ground use OutdoorAir:Node inst..."""
    @property
    def outdoor_air_nodes(self) -> IDFCollection[OutdoorAirNode]:
        """All ``OutdoorAir:Node`` objects in the document. This object sets the temperature and humidity conditions for an outdoor air node. It allows the height above ground to be specified. This object may be used more than once. The same node name may n..."""
    @property
    def output_constructions(self) -> IDFCollection[OutputConstructions]:
        """All ``Output:Constructions`` objects in the document. Adds a report to the eio output file which shows details for each construction, including overall properties, a list of material layers, and calculated results related to conduction transfer functi..."""
    @property
    def output_control_files(self) -> IDFCollection[OutputControlFiles]:
        """All ``OutputControl:Files`` objects in the document. Conditionally turn on/off output from EnergyPlus."""
    @property
    def output_control_illuminance_map_styles(self) -> IDFCollection[OutputControlIlluminanceMapStyle]:
        """All ``OutputControl:IlluminanceMap:Style`` objects in the document. default style for the Daylighting Illuminance Map is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may..."""
    @property
    def output_control_reporting_tolerances(self) -> IDFCollection[OutputControlReportingTolerances]:
        """All ``OutputControl:ReportingTolerances`` objects in the document. Calculations of the time that setpoints are not met use a tolerance of 0.2C. This object allows changing the tolerance used to determine when setpoints are being met."""
    @property
    def output_control_resilience_summaries(self) -> IDFCollection[OutputControlResilienceSummaries]:
        """All ``OutputControl:ResilienceSummaries`` objects in the document. Specifies methods for resilience reporting variables"""
    @property
    def output_control_sizing_styles(self) -> IDFCollection[OutputControlSizingStyle]:
        """All ``OutputControl:Sizing:Style`` objects in the document. Default style for the Sizing output files is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may be a be..."""
    @property
    def output_control_surface_color_schemes(self) -> IDFCollection[OutputControlSurfaceColorScheme]:
        """All ``OutputControl:SurfaceColorScheme`` objects in the document. This object is used to set colors for reporting on various building elements particularly for the DXF reports. We know the user can enter 0 to 255 and the color map is available in DXF output. Ther..."""
    @property
    def output_control_table_styles(self) -> IDFCollection[OutputControlTableStyle]:
        """All ``OutputControl:Table:Style`` objects in the document. default style for the OutputControl:Table:Style is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may b..."""
    @property
    def output_control_timestamps(self) -> IDFCollection[OutputControlTimestamp]:
        """All ``OutputControl:Timestamp`` objects in the document. Control timestamp format, currently applies only to JSON and native CSV (not CSV via ReadVars)"""
    @property
    def output_daylight_factors(self) -> IDFCollection[OutputDaylightFactors]:
        """All ``Output:DaylightFactors`` objects in the document. Reports hourly daylight factors for each exterior window for four sky types (clear, turbid clear, intermediate, and overcast)."""
    @property
    def output_debugging_datas(self) -> IDFCollection[OutputDebuggingData]:
        """All ``Output:DebuggingData`` objects in the document. switch eplusout.dbg file on or off"""
    @property
    def output_diagnostics(self) -> IDFCollection[OutputDiagnostics]:
        """All ``Output:Diagnostics`` objects in the document. Special keys to produce certain warning messages or effect certain simulation characteristics."""
    @property
    def output_energy_management_systems(self) -> IDFCollection[OutputEnergyManagementSystem]:
        """All ``Output:EnergyManagementSystem`` objects in the document. This object is used to control the output produced by the Energy Management System"""
    @property
    def output_environmental_impact_factors(self) -> IDFCollection[OutputEnvironmentalImpactFactors]:
        """All ``Output:EnvironmentalImpactFactors`` objects in the document. This is used to Automatically report the facility meters and turn on the Environmental Impact Report calculations for all of the Environmental Factors."""
    @property
    def output_illuminance_maps(self) -> IDFCollection[OutputIlluminanceMap]:
        """All ``Output:IlluminanceMap`` objects in the document. reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field"""
    @property
    def output_jsons(self) -> IDFCollection[OutputJSON]:
        """All ``Output:JSON`` objects in the document. Output from EnergyPlus can be written to JSON format files."""
    @property
    def output_meter_cumulative_meter_file_onlies(self) -> IDFCollection[OutputMeterCumulativeMeterFileOnly]:
        """All ``Output:Meter:Cumulative:MeterFileOnly`` objects in the document. Each Output:Meter:Cumulative:MeterFileOnly command picks meters to be reported cumulatively onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulati..."""
    @property
    def output_meter_cumulatives(self) -> IDFCollection[OutputMeterCumulative]:
        """All ``Output:Meter:Cumulative`` objects in the document. Each Output:Meter:Cumulative command picks meters to be reported cumulatively onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. a list of ..."""
    @property
    def output_meter_meter_file_onlies(self) -> IDFCollection[OutputMeterMeterFileOnly]:
        """All ``Output:Meter:MeterFileOnly`` objects in the document. Each Output:Meter:MeterFileOnly command picks meters to be put only onto meter file (.mtr). Not all meters are reported in every simulation. A list of meters that can be reported a list of meters t..."""
    @property
    def output_meters(self) -> IDFCollection[OutputMeter]:
        """All ``Output:Meter`` objects in the document. Each Output:Meter command picks meters to be put onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. A list of meters that can be reported a..."""
    @property
    def output_preprocessor_messages(self) -> IDFCollection[OutputPreprocessorMessage]:
        """All ``Output:PreprocessorMessage`` objects in the document. This object does not come from a user input. This is generated by a pre-processor so that various conditions can be gracefully passed on by the InputProcessor."""
    @property
    def output_schedules(self) -> IDFCollection[OutputSchedules]:
        """All ``Output:Schedules`` objects in the document. Produces a condensed reporting that illustrates the full range of schedule values in the eio output file. In the style of input: DaySchedule, WeekSchedule, and Annual Schedule."""
    @property
    def output_sqlites(self) -> IDFCollection[OutputSQLite]:
        """All ``Output:SQLite`` objects in the document. Output from EnergyPlus can be written to an SQLite format file."""
    @property
    def output_surfaces_drawings(self) -> IDFCollection[OutputSurfacesDrawing]:
        """All ``Output:Surfaces:Drawing`` objects in the document. Produces reports/files that are capable of rendering graphically or being imported into other programs. Rendering does not alter the actual inputs/surfaces."""
    @property
    def output_surfaces_lists(self) -> IDFCollection[OutputSurfacesList]:
        """All ``Output:Surfaces:List`` objects in the document. Produces a report summarizing the details of surfaces in the eio output file."""
    @property
    def output_table_annuals(self) -> IDFCollection[OutputTableAnnual]:
        """All ``Output:Table:Annual`` objects in the document. Provides a generic method of setting up tables of annual results with one row per object. The report has multiple columns that are each defined using a repeated group of fields for any number of co..."""
    @property
    def output_table_monthlies(self) -> IDFCollection[OutputTableMonthly]:
        """All ``Output:Table:Monthly`` objects in the document. Provides a generic method of setting up tables of monthly results. The report has multiple columns that are each defined using a repeated group of fields for any number of columns. A single Output:..."""
    @property
    def output_table_report_periods(self) -> IDFCollection[OutputTableReportPeriod]:
        """All ``Output:Table:ReportPeriod`` objects in the document. This object allows the user to generate the resilience tabular reports over a subset of a run period. When it is defined, a series of reporting-period-specific resilience summary tables will be gen..."""
    @property
    def output_table_summary(self) -> IDFCollection[OutputTableSummaryReports]:
        """All ``Output:Table:SummaryReports`` objects in the document. This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object a..."""
    @property
    def output_table_summary_reports(self) -> IDFCollection[OutputTableSummaryReports]:
        """All ``Output:Table:SummaryReports`` objects in the document. This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object a..."""
    @property
    def output_table_time_bins(self) -> IDFCollection[OutputTableTimeBins]:
        """All ``Output:Table:TimeBins`` objects in the document. Produces a bin report in the table output file which shows the amount of time in hours that occurs in different bins for a single specific output variable or meter. Two different types of binning a..."""
    @property
    def output_variable_dictionaries(self) -> IDFCollection[OutputVariableDictionary]:
        """All ``Output:VariableDictionary`` objects in the document. Produces a list summarizing the output variables and meters that are available for reporting for the model being simulated (rdd output file). The list varies depending on the types of objects prese..."""
    @property
    def output_variables(self) -> IDFCollection[OutputVariable]:
        """All ``Output:Variable`` objects in the document. each Output:Variable command picks variables to be put onto the standard output file (.eso) some variables may not be reported for every simulation. a list of variables that can be reported are ava..."""
    @property
    def parametric_file_name_suffixes(self) -> IDFCollection[ParametricFileNameSuffix]:
        """All ``Parametric:FileNameSuffix`` objects in the document. Defines the suffixes to be appended to the idf and output file names for each parametric run. If this object is omitted, the suffix will default to the run number."""
    @property
    def parametric_logics(self) -> IDFCollection[ParametricLogic]:
        """All ``Parametric:Logic`` objects in the document. This object allows some types of objects to be included for some parametric cases and not for others. For example, you might want an overhang on a window in some parametric runs and not others. A s..."""
    @property
    def parametric_run_controls(self) -> IDFCollection[ParametricRunControl]:
        """All ``Parametric:RunControl`` objects in the document. Controls which parametric runs are simulated. This object is optional. If it is not included, then all parametric runs are performed."""
    @property
    def parametric_set_value_for_runs(self) -> IDFCollection[ParametricSetValueForRun]:
        """All ``Parametric:SetValueForRun`` objects in the document. Parametric objects allow a set of multiple simulations to be defined in a single idf file. The parametric preprocessor scans the idf for Parametric:* objects then creates and runs multiple idf file..."""
    @property
    def people(self) -> IDFCollection[People]:
        """All ``People`` objects in the document. Sets internal gains and contaminant rates for occupants in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable..."""
    @property
    def people_definitions(self) -> IDFCollection[PeopleDefinition]:
        """All ``People:Definition`` objects in the document. Defines the physical characteristics (number of people, heat gain fractions, CO2 generation rate and thermal comfort model selections) for occupants. Referenced by one or more People:Instance objects."""
    @property
    def people_instances(self) -> IDFCollection[PeopleInstance]:
        """All ``People:Instance`` objects in the document. Sets internal gains and contaminant rates for occupants in the zone. The physical characteristics are given by the referenced People:Definition object. If a ZoneList, SpaceList, or a Zone comprised..."""
    @property
    def performance_precision_tradeoffs(self) -> IDFCollection[PerformancePrecisionTradeoffs]:
        """All ``PerformancePrecisionTradeoffs`` objects in the document. This object enables users to choose certain options that speed up EnergyPlus simulation, but may lead to small decreases in accuracy of results."""
    @property
    def photovoltaic_performance_equivalent_one_diodes(
        self,
    ) -> IDFCollection[PhotovoltaicPerformanceEquivalentOneDiode]:
        """All ``PhotovoltaicPerformance:EquivalentOne-Diode`` objects in the document. Describes the performance characteristics of Photovoltaic (PV) modules to be modeled using an equivalent one-diode circuit. This model is also known as the 4- or 5-parameter TRNSYS model for photov..."""
    @property
    def photovoltaic_performance_sandias(self) -> IDFCollection[PhotovoltaicPerformanceSandia]:
        """All ``PhotovoltaicPerformance:Sandia`` objects in the document. Describes performance input data needed for specific makes and models of production PV panels using the empirical coefficients assembled by Sandia National Laboratory."""
    @property
    def photovoltaic_performance_simples(self) -> IDFCollection[PhotovoltaicPerformanceSimple]:
        """All ``PhotovoltaicPerformance:Simple`` objects in the document. Describes a simple model of photovoltaics that may be useful for early phase design analysis. In this model the user has direct access to the efficiency with which surfaces convert incident solar r..."""
    @property
    def pipe_adiabatic_steams(self) -> IDFCollection[PipeAdiabaticSteam]:
        """All ``Pipe:Adiabatic:Steam`` objects in the document. Passes Inlet Node state variables to Outlet Node state variables"""
    @property
    def pipe_adiabatics(self) -> IDFCollection[PipeAdiabatic]:
        """All ``Pipe:Adiabatic`` objects in the document. Passes Inlet Node state variables to Outlet Node state variables"""
    @property
    def pipe_indoors(self) -> IDFCollection[PipeIndoor]:
        """All ``Pipe:Indoor`` objects in the document. Pipe model with transport delay and heat transfer to the environment."""
    @property
    def pipe_outdoors(self) -> IDFCollection[PipeOutdoor]:
        """All ``Pipe:Outdoor`` objects in the document. Pipe model with transport delay and heat transfer to the environment."""
    @property
    def pipe_undergrounds(self) -> IDFCollection[PipeUnderground]:
        """All ``Pipe:Underground`` objects in the document. Buried Pipe model: For pipes buried at a depth less than one meter, this is an alternative object to: HeatExchanger:Surface"""
    @property
    def piping_system_underground_domains(self) -> IDFCollection[PipingSystemUndergroundDomain]:
        """All ``PipingSystem:Underground:Domain`` objects in the document. The ground domain object for underground piping system simulation."""
    @property
    def piping_system_underground_pipe_circuits(self) -> IDFCollection[PipingSystemUndergroundPipeCircuit]:
        """All ``PipingSystem:Underground:PipeCircuit`` objects in the document. The pipe circuit object in an underground piping system. This object is simulated within an underground piping domain object and connected on a branch on a plant loop."""
    @property
    def piping_system_underground_pipe_segments(self) -> IDFCollection[PipingSystemUndergroundPipeSegment]:
        """All ``PipingSystem:Underground:PipeSegment`` objects in the document. The pipe segment to be used in an underground piping system This object represents a single pipe leg positioned axially in the local z-direction, at a given x, y location in the domain"""
    @property
    def plant_component_temperature_sources(self) -> IDFCollection[PlantComponentTemperatureSource]:
        """All ``PlantComponent:TemperatureSource`` objects in the document. Simulates an object of pre-determined (constant or scheduled) source temperature The object introduces fluid into the plant loop at the specified temperature and at the same flow rate as the fluid ..."""
    @property
    def plant_component_user_defineds(self) -> IDFCollection[PlantComponentUserDefined]:
        """All ``PlantComponent:UserDefined`` objects in the document. Defines a generic plant component for custom modeling using Energy Management System or External Interface"""
    @property
    def plant_equipment_lists(self) -> IDFCollection[PlantEquipmentList]:
        """All ``PlantEquipmentList`` objects in the document. List plant equipment in order of operating priority, 1st in list will be used 1st, etc Use only plant equipment in this list. If no equipment object types and equipment names are specified, then th..."""
    @property
    def plant_equipment_operation_chiller_heater_changeovers(
        self,
    ) -> IDFCollection[PlantEquipmentOperationChillerHeaterChangeover]:
        """All ``PlantEquipmentOperation:ChillerHeaterChangeover`` objects in the document. Plant equipment operation object to control switchover between chiller and heater operation of chiller heater heat pump serving 2 plant loops. Poll zone loads and determine if plant should be in he..."""
    @property
    def plant_equipment_operation_component_setpoints(self) -> IDFCollection[PlantEquipmentOperationComponentSetpoint]:
        """All ``PlantEquipmentOperation:ComponentSetpoint`` objects in the document. Plant equipment operation scheme for component setpoint operation. Specifies one or pieces of equipment which are controlled to meet the temperature setpoint at the component outlet node."""
    @property
    def plant_equipment_operation_cooling_loads(self) -> IDFCollection[PlantEquipmentOperationCoolingLoad]:
        """All ``PlantEquipmentOperation:CoolingLoad`` objects in the document. Plant equipment operation scheme for cooling load range operation. Specifies one or more groups of equipment which are available to operate for successive cooling load ranges."""
    @property
    def plant_equipment_operation_heating_loads(self) -> IDFCollection[PlantEquipmentOperationHeatingLoad]:
        """All ``PlantEquipmentOperation:HeatingLoad`` objects in the document. Plant equipment operation scheme for heating load range operation. Specifies one or more groups of equipment which are available to operate for successive heating load ranges."""
    @property
    def plant_equipment_operation_outdoor_dewpoint_differences(
        self,
    ) -> IDFCollection[PlantEquipmentOperationOutdoorDewpointDifference]:
        """All ``PlantEquipmentOperation:OutdoorDewpointDifference`` objects in the document. Plant equipment operation scheme for outdoor dewpoint temperature difference operation. Specifies one or more groups of equipment which are available to operate for successive ranges based the diff..."""
    @property
    def plant_equipment_operation_outdoor_dewpoints(self) -> IDFCollection[PlantEquipmentOperationOutdoorDewpoint]:
        """All ``PlantEquipmentOperation:OutdoorDewpoint`` objects in the document. Plant equipment operation scheme for outdoor dewpoint temperature range operation. Specifies one or more groups of equipment which are available to operate for successive outdoor dewpoint temperatu..."""
    @property
    def plant_equipment_operation_outdoor_dry_bulb_differences(
        self,
    ) -> IDFCollection[PlantEquipmentOperationOutdoorDryBulbDifference]:
        """All ``PlantEquipmentOperation:OutdoorDryBulbDifference`` objects in the document. Plant equipment operation scheme for outdoor dry-bulb temperature difference operation. Specifies one or more groups of equipment which are available to operate for successive ranges based the diff..."""
    @property
    def plant_equipment_operation_outdoor_dry_bulbs(self) -> IDFCollection[PlantEquipmentOperationOutdoorDryBulb]:
        """All ``PlantEquipmentOperation:OutdoorDryBulb`` objects in the document. Plant equipment operation scheme for outdoor dry-bulb temperature range operation. Specifies one or more groups of equipment which are available to operate for successive outdoor dry-bulb temperatu..."""
    @property
    def plant_equipment_operation_outdoor_relative_humidities(
        self,
    ) -> IDFCollection[PlantEquipmentOperationOutdoorRelativeHumidity]:
        """All ``PlantEquipmentOperation:OutdoorRelativeHumidity`` objects in the document. Plant equipment operation scheme for outdoor relative humidity range operation. Specifies one or more groups of equipment which are available to operate for successive outdoor relative humidity ran..."""
    @property
    def plant_equipment_operation_outdoor_wet_bulb_differences(
        self,
    ) -> IDFCollection[PlantEquipmentOperationOutdoorWetBulbDifference]:
        """All ``PlantEquipmentOperation:OutdoorWetBulbDifference`` objects in the document. Plant equipment operation scheme for outdoor wet-bulb temperature difference operation. Specifies one or more groups of equipment which are available to operate for successive ranges based the diff..."""
    @property
    def plant_equipment_operation_outdoor_wet_bulbs(self) -> IDFCollection[PlantEquipmentOperationOutdoorWetBulb]:
        """All ``PlantEquipmentOperation:OutdoorWetBulb`` objects in the document. Plant equipment operation scheme for outdoor wet-bulb temperature range operation. Specifies one or more groups of equipment which are available to operate for successive outdoor wet-bulb temperatu..."""
    @property
    def plant_equipment_operation_schemes(self) -> IDFCollection[PlantEquipmentOperationSchemes]:
        """All ``PlantEquipmentOperationSchemes`` objects in the document. Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first th..."""
    @property
    def plant_equipment_operation_thermal_energy_storages(
        self,
    ) -> IDFCollection[PlantEquipmentOperationThermalEnergyStorage]:
        """All ``PlantEquipmentOperation:ThermalEnergyStorage`` objects in the document. Plant equipment operation scheme for simpler input to control thermal (ice) energy storage systems. It replaces a host of setpoint managers with simple, single input values. For more complex contro..."""
    @property
    def plant_equipment_operation_uncontrolleds(self) -> IDFCollection[PlantEquipmentOperationUncontrolled]:
        """All ``PlantEquipmentOperation:Uncontrolled`` objects in the document. Plant equipment operation scheme for uncontrolled operation. Specifies a group of equipment that runs if the loop is active, unless turned off by the loop flow resolver to maintain continuity in th..."""
    @property
    def plant_equipment_operation_user_defineds(self) -> IDFCollection[PlantEquipmentOperationUserDefined]:
        """All ``PlantEquipmentOperation:UserDefined`` objects in the document. Defines a generic plant operation scheme for custom supervisory control using Energy Management System or External Interface to dispatch loads"""
    @property
    def plant_loops(self) -> IDFCollection[PlantLoop]:
        """All ``PlantLoop`` objects in the document. Defines a central plant loop."""
    @property
    def pump_constant_speeds(self) -> IDFCollection[PumpConstantSpeed]:
        """All ``Pump:ConstantSpeed`` objects in the document. This pump model is described in the ASHRAE secondary HVAC toolkit."""
    @property
    def pump_variable_speed_condensates(self) -> IDFCollection[PumpVariableSpeedCondensate]:
        """All ``Pump:VariableSpeed:Condensate`` objects in the document. This pump model is described in the ASHRAE secondary HVAC toolkit. Variable Speed Condensate pump for Steam Systems"""
    @property
    def pump_variable_speeds(self) -> IDFCollection[PumpVariableSpeed]:
        """All ``Pump:VariableSpeed`` objects in the document. This pump model is described in the ASHRAE secondary HVAC toolkit."""
    @property
    def python_plugin_instances(self) -> IDFCollection[PythonPluginInstance]:
        """All ``PythonPlugin:Instance`` objects in the document. A single plugin to be executed during the simulation, which can contain multiple calling points for the same class instance by overriding multiple calling point methods."""
    @property
    def python_plugin_output_variables(self) -> IDFCollection[PythonPluginOutputVariable]:
        """All ``PythonPlugin:OutputVariable`` objects in the document. This object sets up an EnergyPlus output variable from a Python Plugin variable"""
    @property
    def python_plugin_search_paths(self) -> IDFCollection[PythonPluginSearchPaths]:
        """All ``PythonPlugin:SearchPaths`` objects in the document. Add directories to the search path for Python plugin modules The directory containing the EnergyPlus executable file is automatically added so that the Python interpreter can find the packaged up p..."""
    @property
    def python_plugin_trend_variables(self) -> IDFCollection[PythonPluginTrendVariable]:
        """All ``PythonPlugin:TrendVariable`` objects in the document. This object sets up a Python plugin trend variable from an Python plugin variable A trend variable logs values across timesteps"""
    @property
    def python_plugin_variables(self) -> IDFCollection[PythonPluginVariables]:
        """All ``PythonPlugin:Variables`` objects in the document. This object defines name identifiers for custom Python Plugin variable data that should be shared among all running Python Plugins."""
    @property
    def refrigeration_air_chillers(self) -> IDFCollection[RefrigerationAirChiller]:
        """All ``Refrigeration:AirChiller`` objects in the document. Works in conjunction with a refrigeration chiller set, compressor rack, a refrigeration system, or a refrigeration secondary system to simulate the performance of an air chiller, similar to one fou..."""
    @property
    def refrigeration_case_and_walk_in_lists(self) -> IDFCollection[RefrigerationCaseAndWalkInList]:
        """All ``Refrigeration:CaseAndWalkInList`` objects in the document. Provides a list of all the refrigerated cases, walk in coolers, or air chillers cooled by a single refrigeration system. Note that the names of all cases, walk-ins ,air chillers, and CaseAndWalkInL..."""
    @property
    def refrigeration_cases(self) -> IDFCollection[RefrigerationCase]:
        """All ``Refrigeration:Case`` objects in the document. The Refrigeration Case object works in conjunction with a compressor rack, a refrigeration system, or a secondary loop to simulate the performance of a refrigerated case system. The object calculat..."""
    @property
    def refrigeration_compressor_lists(self) -> IDFCollection[RefrigerationCompressorList]:
        """All ``Refrigeration:CompressorList`` objects in the document. List of all the compressors included within a single refrigeration system (Refrigeration:System). Each list must contain at least one compressor. The order in which the individual compressors are l..."""
    @property
    def refrigeration_compressor_racks(self) -> IDFCollection[RefrigerationCompressorRack]:
        """All ``Refrigeration:CompressorRack`` objects in the document. Works in conjunction with the refrigeration case and walk-in objects to simulate the performance of a refrigerated case system. This object models the electric consumption of the rack compressors a..."""
    @property
    def refrigeration_compressors(self) -> IDFCollection[RefrigerationCompressor]:
        """All ``Refrigeration:Compressor`` objects in the document. Refrigeration system compressor. Data is available for many compressors in the RefrigerationCompressor.idf dataset"""
    @property
    def refrigeration_condenser_air_cooleds(self) -> IDFCollection[RefrigerationCondenserAirCooled]:
        """All ``Refrigeration:Condenser:AirCooled`` objects in the document. Air cooled condenser for a refrigeration system (Refrigeration:System)."""
    @property
    def refrigeration_condenser_cascades(self) -> IDFCollection[RefrigerationCondenserCascade]:
        """All ``Refrigeration:Condenser:Cascade`` objects in the document. Cascade condenser for a refrigeration system (Refrigeration:System). The cascade condenser is unlike the other condenser options because it rejects heat to another, higher-temperature, refrigeratio..."""
    @property
    def refrigeration_condenser_evaporative_cooleds(self) -> IDFCollection[RefrigerationCondenserEvaporativeCooled]:
        """All ``Refrigeration:Condenser:EvaporativeCooled`` objects in the document. Evaporative-cooled condenser for a refrigeration system (Refrigeration:System)."""
    @property
    def refrigeration_condenser_water_cooleds(self) -> IDFCollection[RefrigerationCondenserWaterCooled]:
        """All ``Refrigeration:Condenser:WaterCooled`` objects in the document. Water cooled condenser for a refrigeration system (Refrigeration:System)."""
    @property
    def refrigeration_gas_cooler_air_cooleds(self) -> IDFCollection[RefrigerationGasCoolerAirCooled]:
        """All ``Refrigeration:GasCooler:AirCooled`` objects in the document. The transcritical refrigeration system requires a single gas cooler to reject the system heat."""
    @property
    def refrigeration_secondary_systems(self) -> IDFCollection[RefrigerationSecondarySystem]:
        """All ``Refrigeration:SecondarySystem`` objects in the document. Works in conjunction with refrigerated cases and walkins to simulate the performance of a secondary loop supermarket refrigeration system. Heat from the refrigeration loads served by the secondary ..."""
    @property
    def refrigeration_subcoolers(self) -> IDFCollection[RefrigerationSubcooler]:
        """All ``Refrigeration:Subcooler`` objects in the document. Two types of subcoolers are modeled by the detailed refrigeration system. The liquid suction heat exchanger uses cool suction gas to subcool the hot condensate after it leaves the condenser and bef..."""
    @property
    def refrigeration_systems(self) -> IDFCollection[RefrigerationSystem]:
        """All ``Refrigeration:System`` objects in the document. Simulates the performance of a supermarket refrigeration system when used along with other objects to define the refrigeration load(s), the compressor(s), and the condenser."""
    @property
    def refrigeration_transcritical_systems(self) -> IDFCollection[RefrigerationTranscriticalSystem]:
        """All ``Refrigeration:TranscriticalSystem`` objects in the document. Detailed transcritical carbon dioxide (CO2) booster refrigeration systems used in supermarkets. The object allows for modeling either a single stage system with medium-temperature loads or a two st..."""
    @property
    def refrigeration_transfer_load_lists(self) -> IDFCollection[RefrigerationTransferLoadList]:
        """All ``Refrigeration:TransferLoadList`` objects in the document. A refrigeration system may provide cooling to other, secondary, systems through either a secondary loop or a cascade condenser. If multiple transfer loads are served by a single primary system, use..."""
    @property
    def refrigeration_walk_ins(self) -> IDFCollection[RefrigerationWalkIn]:
        """All ``Refrigeration:WalkIn`` objects in the document. Works in conjunction with a compressor rack, a refrigeration system, or a refrigeration secondary system to simulate the performance of a walk-in cooler. The walk-in cooler model uses information a..."""
    @property
    def roof_ceiling_detaileds(self) -> IDFCollection[RoofCeilingDetailed]:
        """All ``RoofCeiling:Detailed`` objects in the document. Allows for detailed entry of roof/ceiling heat transfer surfaces."""
    @property
    def roof_irrigations(self) -> IDFCollection[RoofIrrigation]:
        """All ``RoofIrrigation`` objects in the document. Used to describe the amount of irrigation on the ecoroof surface over the course of the simulation runperiod."""
    @property
    def roofs(self) -> IDFCollection[Roof]:
        """All ``Roof`` objects in the document. Allows for simplified entry of roofs (exterior). View Factor to Ground is automatically calculated."""
    @property
    def room_air_model_types(self) -> IDFCollection[RoomAirModelType]:
        """All ``RoomAirModelType`` objects in the document. Selects the type of room air model to be used in a given zone. If no RoomAirModelType object is specified then the default Mixing model (all zone air at the same temperature) will be used."""
    @property
    def room_air_node_airflow_network_adjacent_surface_lists(
        self,
    ) -> IDFCollection[RoomAirNodeAirflowNetworkAdjacentSurfaceList]:
        """All ``RoomAir:Node:AirflowNetwork:AdjacentSurfaceList`` objects in the document."""
    @property
    def room_air_node_airflow_network_hvac_equipments(self) -> IDFCollection[RoomAirNodeAirflowNetworkHVACEquipment]:
        """All ``RoomAir:Node:AirflowNetwork:HVACEquipment`` objects in the document. define the zone equipment associated with one particular RoomAir:Node"""
    @property
    def room_air_node_airflow_network_internal_gains(self) -> IDFCollection[RoomAirNodeAirflowNetworkInternalGains]:
        """All ``RoomAir:Node:AirflowNetwork:InternalGains`` objects in the document. define the internal gains that are associated with one particular RoomAir:Node"""
    @property
    def room_air_node_airflow_networks(self) -> IDFCollection[RoomAirNodeAirflowNetwork]:
        """All ``RoomAir:Node:AirflowNetwork`` objects in the document. define an air node for some types of nodal air models"""
    @property
    def room_air_nodes(self) -> IDFCollection[RoomAirNode]:
        """All ``RoomAir:Node`` objects in the document. Define an air node for some types of nodal room air models"""
    @property
    def room_air_settings_airflow_networks(self) -> IDFCollection[RoomAirSettingsAirflowNetwork]:
        """All ``RoomAirSettings:AirflowNetwork`` objects in the document. RoomAir modeling using Airflow pressure network solver"""
    @property
    def room_air_settings_cross_ventilations(self) -> IDFCollection[RoomAirSettingsCrossVentilation]:
        """All ``RoomAirSettings:CrossVentilation`` objects in the document. This UCSD Cross Ventilation Room Air Model provides a simple model for heat transfer and vertical temperature profile prediction in cross ventilated rooms. The model distinguishes two regions in th..."""
    @property
    def room_air_settings_one_node_displacement_ventilations(
        self,
    ) -> IDFCollection[RoomAirSettingsOneNodeDisplacementVentilation]:
        """All ``RoomAirSettings:OneNodeDisplacementVentilation`` objects in the document. The Mundt model for displacement ventilation"""
    @property
    def room_air_settings_three_node_displacement_ventilations(
        self,
    ) -> IDFCollection[RoomAirSettingsThreeNodeDisplacementVentilation]:
        """All ``RoomAirSettings:ThreeNodeDisplacementVentilation`` objects in the document. The UCSD model for Displacement Ventilation"""
    @property
    def room_air_settings_under_floor_air_distribution_exteriors(
        self,
    ) -> IDFCollection[RoomAirSettingsUnderFloorAirDistributionExterior]:
        """All ``RoomAirSettings:UnderFloorAirDistributionExterior`` objects in the document. Applicable to exterior spaces that are served by an underfloor air distribution system. The dominant sources of heat gain should be from people, equipment, and other localized sources located in th..."""
    @property
    def room_air_settings_under_floor_air_distribution_interiors(
        self,
    ) -> IDFCollection[RoomAirSettingsUnderFloorAirDistributionInterior]:
        """All ``RoomAirSettings:UnderFloorAirDistributionInterior`` objects in the document. This Room Air Model is applicable to interior spaces that are served by an underfloor air distribution system. The dominant sources of heat gain should be from people, equipment, and other localize..."""
    @property
    def room_air_temperature_pattern_constant_gradients(
        self,
    ) -> IDFCollection[RoomAirTemperaturePatternConstantGradient]:
        """All ``RoomAir:TemperaturePattern:ConstantGradient`` objects in the document. Used to model room air with a fixed temperature gradient in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined."""
    @property
    def room_air_temperature_pattern_nondimensional_heights(
        self,
    ) -> IDFCollection[RoomAirTemperaturePatternNondimensionalHeight]:
        """All ``RoomAir:TemperaturePattern:NondimensionalHeight`` objects in the document. Defines a distribution pattern for air temperatures relative to the current mean air temperature as a function of height. The height, referred to as Zeta, is nondimensional by normalizing with the ..."""
    @property
    def room_air_temperature_pattern_surface_mappings(self) -> IDFCollection[RoomAirTemperaturePatternSurfaceMapping]:
        """All ``RoomAir:TemperaturePattern:SurfaceMapping`` objects in the document. Defines a distribution pattern for the air temperatures adjacent to individual surfaces. This allows controlling the adjacent air temperature on a surface-by-surface basis rather than by height. Th..."""
    @property
    def room_air_temperature_pattern_two_gradients(self) -> IDFCollection[RoomAirTemperaturePatternTwoGradient]:
        """All ``RoomAir:TemperaturePattern:TwoGradient`` objects in the document. Used to model room air with two temperature gradients in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined."""
    @property
    def room_air_temperature_pattern_user_defineds(self) -> IDFCollection[RoomAirTemperaturePatternUserDefined]:
        """All ``RoomAir:TemperaturePattern:UserDefined`` objects in the document. Used to explicitly define temperature patterns that are to be applied to the mean air temperature within a thermal zone. Used with RoomAirModelType = UserDefined."""
    @property
    def run_period(self) -> IDFCollection[RunPeriod]:
        """All ``RunPeriod`` objects in the document. Specify a range of dates and other parameters for a simulation. Multiple run periods may be input, but they may not overlap."""
    @property
    def run_period_control_daylight_saving_times(self) -> IDFCollection[RunPeriodControlDaylightSavingTime]:
        """All ``RunPeriodControl:DaylightSavingTime`` objects in the document. This object sets up the daylight saving time period for any RunPeriod. Ignores any daylight saving time period on the weather file and uses this definition. These are not used with SizingPeriod:Des..."""
    @property
    def run_period_control_special_days(self) -> IDFCollection[RunPeriodControlSpecialDays]:
        """All ``RunPeriodControl:SpecialDays`` objects in the document. This object sets up holidays/special days to be used during weather file run periods. (These are not used with SizingPeriod:* objects.) Depending on the value in the run period, days on the weather..."""
    @property
    def run_periods(self) -> IDFCollection[RunPeriod]:
        """All ``RunPeriod`` objects in the document. Specify a range of dates and other parameters for a simulation. Multiple run periods may be input, but they may not overlap."""
    @property
    def schedule_compacts(self) -> IDFCollection[ScheduleCompact]:
        """All ``Schedule:Compact`` objects in the document. Irregular object. Does not follow the usual definition for fields. Fields A3... are: Through: Date For: Applicable days (ref: Schedule:Week:Compact) Interpolate: Average/Linear/No (ref: Schedule:Da..."""
    @property
    def schedule_constants(self) -> IDFCollection[ScheduleConstant]:
        """All ``Schedule:Constant`` objects in the document. Constant hourly value for entire year."""
    @property
    def schedule_day_hourlies(self) -> IDFCollection[ScheduleDayHourly]:
        """All ``Schedule:Day:Hourly`` objects in the document. A Schedule:Day:Hourly contains 24 values for each hour of the day."""
    @property
    def schedule_day_intervals(self) -> IDFCollection[ScheduleDayInterval]:
        """All ``Schedule:Day:Interval`` objects in the document. A Schedule:Day:Interval contains a full day of values with specified end times for each value Currently, is set up to allow for 10 minute intervals for an entire day."""
    @property
    def schedule_day_lists(self) -> IDFCollection[ScheduleDayList]:
        """All ``Schedule:Day:List`` objects in the document. Schedule:Day:List will allow the user to list 24 hours worth of values, which can be sub-hourly in nature."""
    @property
    def schedule_file_shadings(self) -> IDFCollection[ScheduleFileShading]:
        """All ``Schedule:File:Shading`` objects in the document. A Schedule:File:Shading points to a CSV file that has 8760-8784 hours of sunlit fraction data for all or some of the exterior surfaces."""
    @property
    def schedule_files(self) -> IDFCollection[ScheduleFile]:
        """All ``Schedule:File`` objects in the document. A Schedule:File points to a text computer file that has 8760-8784 hours of data."""
    @property
    def schedule_type_limits(self) -> IDFCollection[ScheduleTypeLimits]:
        """All ``ScheduleTypeLimits`` objects in the document. ScheduleTypeLimits specifies the data types and limits for the values contained in schedules"""
    @property
    def schedule_week_compacts(self) -> IDFCollection[ScheduleWeekCompact]:
        """All ``Schedule:Week:Compact`` objects in the document. Compact definition for Schedule:Day:List"""
    @property
    def schedule_week_dailies(self) -> IDFCollection[ScheduleWeekDaily]:
        """All ``Schedule:Week:Daily`` objects in the document. A Schedule:Week:Daily contains 12 Schedule:Day:Hourly objects, one for each day type."""
    @property
    def schedule_week_rules(self) -> IDFCollection[ScheduleWeekRule]:
        """All ``Schedule:Week:Rule`` objects in the document. A Schedule:Week:Rule defines one override rule for a Schedule:Year:Rules. Rules are evaluated in ascending Rule Priority Order; the first matching rule wins. A rule matches a day if: (a) the day fa..."""
    @property
    def schedule_year_rules(self) -> IDFCollection[ScheduleYearRules]:
        """All ``Schedule:Year:Rules`` objects in the document. A Schedule:Year:Rules defines a yearly schedule using a default day profile and a prioritized list of override rules (Schedule:Week:Rule objects). Rules are evaluated in ascending Rule Priority Ord..."""
    @property
    def schedule_years(self) -> IDFCollection[ScheduleYear]:
        """All ``Schedule:Year`` objects in the document. A Schedule:Year contains from 1 to 52 week schedules"""
    @property
    def schedules_compact(self) -> IDFCollection[ScheduleCompact]:
        """All ``Schedule:Compact`` objects in the document. Irregular object. Does not follow the usual definition for fields. Fields A3... are: Through: Date For: Applicable days (ref: Schedule:Week:Compact) Interpolate: Average/Linear/No (ref: Schedule:Da..."""
    @property
    def schedules_constant(self) -> IDFCollection[ScheduleConstant]:
        """All ``Schedule:Constant`` objects in the document. Constant hourly value for entire year."""
    @property
    def schedules_day_hourly(self) -> IDFCollection[ScheduleDayHourly]:
        """All ``Schedule:Day:Hourly`` objects in the document. A Schedule:Day:Hourly contains 24 values for each hour of the day."""
    @property
    def schedules_day_interval(self) -> IDFCollection[ScheduleDayInterval]:
        """All ``Schedule:Day:Interval`` objects in the document. A Schedule:Day:Interval contains a full day of values with specified end times for each value Currently, is set up to allow for 10 minute intervals for an entire day."""
    @property
    def schedules_day_list(self) -> IDFCollection[ScheduleDayList]:
        """All ``Schedule:Day:List`` objects in the document. Schedule:Day:List will allow the user to list 24 hours worth of values, which can be sub-hourly in nature."""
    @property
    def schedules_file(self) -> IDFCollection[ScheduleFile]:
        """All ``Schedule:File`` objects in the document. A Schedule:File points to a text computer file that has 8760-8784 hours of data."""
    @property
    def schedules_week_daily(self) -> IDFCollection[ScheduleWeekDaily]:
        """All ``Schedule:Week:Daily`` objects in the document. A Schedule:Week:Daily contains 12 Schedule:Day:Hourly objects, one for each day type."""
    @property
    def schedules_year(self) -> IDFCollection[ScheduleYear]:
        """All ``Schedule:Year`` objects in the document. A Schedule:Year contains from 1 to 52 week schedules"""
    @property
    def setpoint_manager_coldests(self) -> IDFCollection[SetpointManagerColdest]:
        """All ``SetpointManager:Coldest`` objects in the document. This SetpointManager is used in dual duct systems to reset the setpoint temperature of the air in the heating supply duct. Usually it is used in conjunction with a SetpointManager:Warmest resetting..."""
    @property
    def setpoint_manager_condenser_entering_reset_ideals(
        self,
    ) -> IDFCollection[SetpointManagerCondenserEnteringResetIdeal]:
        """All ``SetpointManager:CondenserEnteringReset:Ideal`` objects in the document. This setpoint manager determine the ideal optimum condenser entering water temperature setpoint for a given timestep."""
    @property
    def setpoint_manager_condenser_entering_resets(self) -> IDFCollection[SetpointManagerCondenserEnteringReset]:
        """All ``SetpointManager:CondenserEnteringReset`` objects in the document. This setpoint manager uses one curve to determine the optimum condenser entering water temperature for a given timestep and two other curves to place boundary conditions on the setpoint value."""
    @property
    def setpoint_manager_follow_ground_temperatures(self) -> IDFCollection[SetpointManagerFollowGroundTemperature]:
        """All ``SetpointManager:FollowGroundTemperature`` objects in the document. This setpoint manager is used to place a temperature setpoint on a system node that is derived from a current ground temperature. The ground temperatures are specified in different Site:GroundTempe..."""
    @property
    def setpoint_manager_follow_outdoor_air_temperatures(
        self,
    ) -> IDFCollection[SetpointManagerFollowOutdoorAirTemperature]:
        """All ``SetpointManager:FollowOutdoorAirTemperature`` objects in the document. This setpoint manager is used to place a temperature setpoint on a system node that is derived from the current outdoor air environmental conditions. The outdoor air conditions are obtained from th..."""
    @property
    def setpoint_manager_follow_system_node_temperatures(
        self,
    ) -> IDFCollection[SetpointManagerFollowSystemNodeTemperature]:
        """All ``SetpointManager:FollowSystemNodeTemperature`` objects in the document. This setpoint manager is used to place a temperature setpoint on a system node that is derived from the current temperatures at a separate system node. The current value of the temperature at a ref..."""
    @property
    def setpoint_manager_mixed_airs(self) -> IDFCollection[SetpointManagerMixedAir]:
        """All ``SetpointManager:MixedAir`` objects in the document. The Mixed Air Setpoint Manager is meant to be used in conjunction with a Controller:OutdoorAir object. This setpoint manager is used to establish a temperature setpoint at the mixed air node."""
    @property
    def setpoint_manager_multi_zone_cooling_averages(self) -> IDFCollection[SetpointManagerMultiZoneCoolingAverage]:
        """All ``SetpointManager:MultiZone:Cooling:Average`` objects in the document. This setpoint manager sets the average supply air temperature based on the cooling load requirements of all controlled zones in an air loop served by a central air-conditioner."""
    @property
    def setpoint_manager_multi_zone_heating_averages(self) -> IDFCollection[SetpointManagerMultiZoneHeatingAverage]:
        """All ``SetpointManager:MultiZone:Heating:Average`` objects in the document. This setpoint manager sets the average supply air temperature based on the heating load requirements of all controlled zones in an air loop served by a central air-conditioner."""
    @property
    def setpoint_manager_multi_zone_humidity_maximums(self) -> IDFCollection[SetpointManagerMultiZoneHumidityMaximum]:
        """All ``SetpointManager:MultiZone:Humidity:Maximum`` objects in the document. This setpoint manager sets the maximum supply air humidity ratio based on dehumidification requirements of a controlled zone with critical humidity ratio setpoint (i.e., a zone with the lowest humi..."""
    @property
    def setpoint_manager_multi_zone_humidity_minimums(self) -> IDFCollection[SetpointManagerMultiZoneHumidityMinimum]:
        """All ``SetpointManager:MultiZone:Humidity:Minimum`` objects in the document. This setpoint manager sets the minimum supply air humidity ratio based on humidification requirements of a controlled zone with critical humidity ratio setpoint (i.e., a zone with the highest humid..."""
    @property
    def setpoint_manager_multi_zone_maximum_humidity_averages(
        self,
    ) -> IDFCollection[SetpointManagerMultiZoneMaximumHumidityAverage]:
        """All ``SetpointManager:MultiZone:MaximumHumidity:Average`` objects in the document. This setpoint manager sets the average supply air maximum humidity ratio based on moisture load requirements of all controlled zones in an air loop served by a central air-conditioner."""
    @property
    def setpoint_manager_multi_zone_minimum_humidity_averages(
        self,
    ) -> IDFCollection[SetpointManagerMultiZoneMinimumHumidityAverage]:
        """All ``SetpointManager:MultiZone:MinimumHumidity:Average`` objects in the document. This setpoint manager sets the average supply air minimum humidity ratio based on moisture load requirements of all controlled zones in an air loop served by a central air-conditioner."""
    @property
    def setpoint_manager_outdoor_air_pretreats(self) -> IDFCollection[SetpointManagerOutdoorAirPretreat]:
        """All ``SetpointManager:OutdoorAirPretreat`` objects in the document. This setpoint manager determines the required conditions at the outdoor air stream node which will produce the reference setpoint condition at the mixed air node when mixed with the return air stream"""
    @property
    def setpoint_manager_outdoor_air_resets(self) -> IDFCollection[SetpointManagerOutdoorAirReset]:
        """All ``SetpointManager:OutdoorAirReset`` objects in the document. This Setpoint Manager is used to place a setpoint temperature on system node according to the outdoor air temperature using a reset rule. The outdoor air temperature is obtained from the weather in..."""
    @property
    def setpoint_manager_return_air_bypass_flows(self) -> IDFCollection[SetpointManagerReturnAirBypassFlow]:
        """All ``SetpointManager:ReturnAirBypassFlow`` objects in the document. This setpoint manager determines the required mass flow rate through a return air bypass duct to meet the specified temperature setpoint"""
    @property
    def setpoint_manager_return_temperature_chilled_waters(
        self,
    ) -> IDFCollection[SetpointManagerReturnTemperatureChilledWater]:
        """All ``SetpointManager:ReturnTemperature:ChilledWater`` objects in the document. This setpoint manager is used to place a temperature setpoint on a plant supply outlet node based on a target return water setpoint. The setpoint manager attempts to achieve the desired return wate..."""
    @property
    def setpoint_manager_return_temperature_hot_waters(self) -> IDFCollection[SetpointManagerReturnTemperatureHotWater]:
        """All ``SetpointManager:ReturnTemperature:HotWater`` objects in the document. This setpoint manager is used to place a temperature setpoint on a plant supply outlet node based on a target return water setpoint. The setpoint manager attempts to achieve the desired return wate..."""
    @property
    def setpoint_manager_scheduled_dual_setpoints(self) -> IDFCollection[SetpointManagerScheduledDualSetpoint]:
        """All ``SetpointManager:Scheduled:DualSetpoint`` objects in the document. This setpoint manager places a high and low schedule value on one or more nodes."""
    @property
    def setpoint_manager_scheduleds(self) -> IDFCollection[SetpointManagerScheduled]:
        """All ``SetpointManager:Scheduled`` objects in the document. The simplest Setpoint Manager simply uses a schedule to determine one or more setpoints. Values of the nodes are not used as input."""
    @property
    def setpoint_manager_single_zone_coolings(self) -> IDFCollection[SetpointManagerSingleZoneCooling]:
        """All ``SetpointManager:SingleZone:Cooling`` objects in the document. This setpoint manager detects the control zone load to meet the current cooling setpoint, zone inlet node flow rate, and zone node temperature, and calculates a setpoint temperature for the supply ..."""
    @property
    def setpoint_manager_single_zone_heatings(self) -> IDFCollection[SetpointManagerSingleZoneHeating]:
        """All ``SetpointManager:SingleZone:Heating`` objects in the document. This setpoint manager detects the control zone load to meet the current heating setpoint, zone inlet node flow rate, and zone node temperature, and calculates a setpoint temperature for the supply ..."""
    @property
    def setpoint_manager_single_zone_humidity_maximums(self) -> IDFCollection[SetpointManagerSingleZoneHumidityMaximum]:
        """All ``SetpointManager:SingleZone:Humidity:Maximum`` objects in the document. The Single Zone Maximum Humidity Setpoint Manager allows the control of a single zone maximum humidity level. This setpoint manager can be used in conjunction with object ZoneControl:Humidistat to ..."""
    @property
    def setpoint_manager_single_zone_humidity_minimums(self) -> IDFCollection[SetpointManagerSingleZoneHumidityMinimum]:
        """All ``SetpointManager:SingleZone:Humidity:Minimum`` objects in the document. The Single Zone Minimum Humidity Setpoint Manager allows the control of a single zone minimum humidity level. This setpoint manager can be used in conjunction with object ZoneControl:Humidistat to ..."""
    @property
    def setpoint_manager_single_zone_one_stage_coolings(
        self,
    ) -> IDFCollection[SetpointManagerSingleZoneOneStageCooling]:
        """All ``SetpointManager:SingleZone:OneStageCooling`` objects in the document. This object can be used with CoilSystem:Cooling:DX to model on/off cycling control of single stage air systems. Setpoints are modulated to run coil full on or full off depending on zone conditions...."""
    @property
    def setpoint_manager_single_zone_one_stage_heatings(
        self,
    ) -> IDFCollection[SetpointManagerSingleZoneOneStageHeating]:
        """All ``SetpointManager:SingleZone:OneStageHeating`` objects in the document. This object can be used with CoilSystem:Heating:DX, Coil:Heating:Fuel, Coil:Heating:Electric to model on/off cycling control of single stage air systems. Setpoints are modulated to run coil full on..."""
    @property
    def setpoint_manager_single_zone_reheats(self) -> IDFCollection[SetpointManagerSingleZoneReheat]:
        """All ``SetpointManager:SingleZone:Reheat`` objects in the document. This setpoint manager detects the control zone load, zone inlet node flow rate, and zone node temperature and calculates a setpoint temperature for the supply air that will satisfy the zone load (h..."""
    @property
    def setpoint_manager_system_node_reset_humidities(self) -> IDFCollection[SetpointManagerSystemNodeResetHumidity]:
        """All ``SetpointManager:SystemNodeReset:Humidity`` objects in the document. This Setpoint Manager is used to place a humidity ratio setpoint on a system node according to the reference (e.g., return) humidity ratio using a reset rule. The humidity ratio setpoint is obtaine..."""
    @property
    def setpoint_manager_system_node_reset_temperatures(
        self,
    ) -> IDFCollection[SetpointManagerSystemNodeResetTemperature]:
        """All ``SetpointManager:SystemNodeReset:Temperature`` objects in the document. This Setpoint Manager is used to place a temperature setpoint on a system node according to the reference (e.g., return) temperature using a reset rule. The temperature setpoint is obtained by retr..."""
    @property
    def setpoint_manager_warmest_temperature_flows(self) -> IDFCollection[SetpointManagerWarmestTemperatureFlow]:
        """All ``SetpointManager:WarmestTemperatureFlow`` objects in the document. This setpoint manager sets both the supply air temperature and the supply air flow rate."""
    @property
    def setpoint_manager_warmests(self) -> IDFCollection[SetpointManagerWarmest]:
        """All ``SetpointManager:Warmest`` objects in the document. This SetpointManager resets the cooling supply air temperature of a central forced air HVAC system according to the cooling demand of the warmest zone."""
    @property
    def shading_building(self) -> IDFCollection[ShadingBuildingDetailed]:
        """All ``Shading:Building:Detailed`` objects in the document. used for shading elements such as trees, other buildings, parts of this building not being modeled these items are relative to the current building and would move with relative geometry"""
    @property
    def shading_building_detaileds(self) -> IDFCollection[ShadingBuildingDetailed]:
        """All ``Shading:Building:Detailed`` objects in the document. used for shading elements such as trees, other buildings, parts of this building not being modeled these items are relative to the current building and would move with relative geometry"""
    @property
    def shading_buildings(self) -> IDFCollection[ShadingBuilding]:
        """All ``Shading:Building`` objects in the document. used for shading elements such as trees, other buildings, parts of this building not being modeled these items are relative to the current building and would move with relative geometry"""
    @property
    def shading_fin_projections(self) -> IDFCollection[ShadingFinProjection]:
        """All ``Shading:Fin:Projection`` objects in the document. Fins are usually shading surfaces that are perpendicular to a window or door."""
    @property
    def shading_fins(self) -> IDFCollection[ShadingFin]:
        """All ``Shading:Fin`` objects in the document. Fins are usually shading surfaces that are perpendicular to a window or door."""
    @property
    def shading_overhang_projections(self) -> IDFCollection[ShadingOverhangProjection]:
        """All ``Shading:Overhang:Projection`` objects in the document. Overhangs are typically flat shading surfaces that reference a window or door."""
    @property
    def shading_overhangs(self) -> IDFCollection[ShadingOverhang]:
        """All ``Shading:Overhang`` objects in the document. Overhangs are usually flat shading surfaces that reference a window or door."""
    @property
    def shading_property_reflectances(self) -> IDFCollection[ShadingPropertyReflectance]:
        """All ``ShadingProperty:Reflectance`` objects in the document. If this object is not defined for a shading surface the default values listed in following fields will be used in the solar reflection calculation."""
    @property
    def shading_site_detaileds(self) -> IDFCollection[ShadingSiteDetailed]:
        """All ``Shading:Site:Detailed`` objects in the document. used for shading elements such as trees these items are fixed in space and would not move with relative geometry"""
    @property
    def shading_sites(self) -> IDFCollection[ShadingSite]:
        """All ``Shading:Site`` objects in the document. used for shading elements such as trees these items are fixed in space and would not move with relative geometry"""
    @property
    def shading_surfaces(self) -> IDFCollection[ShadingSiteDetailed]:
        """All ``Shading:Site:Detailed`` objects in the document. used for shading elements such as trees these items are fixed in space and would not move with relative geometry"""
    @property
    def shading_zone(self) -> IDFCollection[ShadingZoneDetailed]:
        """All ``Shading:Zone:Detailed`` objects in the document. used For fins, overhangs, elements that shade the building, are attached to the building but are not part of the heat transfer calculations"""
    @property
    def shading_zone_detaileds(self) -> IDFCollection[ShadingZoneDetailed]:
        """All ``Shading:Zone:Detailed`` objects in the document. used For fins, overhangs, elements that shade the building, are attached to the building but are not part of the heat transfer calculations"""
    @property
    def shadow_calculations(self) -> IDFCollection[ShadowCalculation]:
        """All ``ShadowCalculation`` objects in the document. This object is used to control details of the solar, shading, and daylighting models"""
    @property
    def simulation_control(self) -> IDFCollection[SimulationControl]:
        """All ``SimulationControl`` objects in the document. Note that the following 3 fields are related to the Sizing:Zone, Sizing:System, and Sizing:Plant objects. Having these fields set to Yes but no corresponding Sizing object will not cause the sizing..."""
    @property
    def simulation_controls(self) -> IDFCollection[SimulationControl]:
        """All ``SimulationControl`` objects in the document. Note that the following 3 fields are related to the Sizing:Zone, Sizing:System, and Sizing:Plant objects. Having these fields set to Yes but no corresponding Sizing object will not cause the sizing..."""
    @property
    def site_ground_domain_basements(self) -> IDFCollection[SiteGroundDomainBasement]:
        """All ``Site:GroundDomain:Basement`` objects in the document. Ground-coupled basement model for simulating basements or other underground zones."""
    @property
    def site_ground_domain_slabs(self) -> IDFCollection[SiteGroundDomainSlab]:
        """All ``Site:GroundDomain:Slab`` objects in the document. Ground-coupled slab model for on-grade and in-grade cases with or without insulation."""
    @property
    def site_ground_reflectance_snow_modifiers(self) -> IDFCollection[SiteGroundReflectanceSnowModifier]:
        """All ``Site:GroundReflectance:SnowModifier`` objects in the document. Specifies ground reflectance multipliers when snow resident on the ground. These multipliers are applied to the 'normal' ground reflectances specified in Site:GroundReflectance."""
    @property
    def site_ground_reflectances(self) -> IDFCollection[SiteGroundReflectance]:
        """All ``Site:GroundReflectance`` objects in the document. Specifies the ground reflectance values used to calculate ground reflected solar. The ground reflectance can be further modified when snow is on the ground by Site:GroundReflectance:SnowModifier."""
    @property
    def site_ground_temperature_building_surfaces(self) -> IDFCollection[SiteGroundTemperatureBuildingSurface]:
        """All ``Site:GroundTemperature:BuildingSurface`` objects in the document. These temperatures are specifically for those surfaces that have the outside environment of 'Ground'. Documentation about what values these should be is located in the Auxiliary programs document (..."""
    @property
    def site_ground_temperature_deeps(self) -> IDFCollection[SiteGroundTemperatureDeep]:
        """All ``Site:GroundTemperature:Deep`` objects in the document. These temperatures are specifically for the ground heat exchangers that would use 'deep' (3-4 m depth) ground temperatures for their heat source. They are not used in other models."""
    @property
    def site_ground_temperature_fcfactor_methods(self) -> IDFCollection[SiteGroundTemperatureFCfactorMethod]:
        """All ``Site:GroundTemperature:FCfactorMethod`` objects in the document. These temperatures are specifically for underground walls and ground floors defined with the C-factor and F-factor methods, and should be close to the monthly average outdoor air temperature delaye..."""
    @property
    def site_ground_temperature_shallows(self) -> IDFCollection[SiteGroundTemperatureShallow]:
        """All ``Site:GroundTemperature:Shallow`` objects in the document. These temperatures are specifically for the Surface Ground Heat Exchanger and should probably be close to the average outdoor air temperature for the location. They are not used in other models."""
    @property
    def site_ground_temperature_undisturbed_finite_differences(
        self,
    ) -> IDFCollection[SiteGroundTemperatureUndisturbedFiniteDifference]:
        """All ``Site:GroundTemperature:Undisturbed:FiniteDifference`` objects in the document. Undisturbed ground temperature object using a detailed finite difference 1-D model"""
    @property
    def site_ground_temperature_undisturbed_kusuda_achenbaches(
        self,
    ) -> IDFCollection[SiteGroundTemperatureUndisturbedKusudaAchenbach]:
        """All ``Site:GroundTemperature:Undisturbed:KusudaAchenbach`` objects in the document. Undisturbed ground temperature object using the Kusuda-Achenbach 1965 correlation."""
    @property
    def site_ground_temperature_undisturbed_xings(self) -> IDFCollection[SiteGroundTemperatureUndisturbedXing]:
        """All ``Site:GroundTemperature:Undisturbed:Xing`` objects in the document. Undisturbed ground temperature object using the Xing 2014 2 harmonic parameter model."""
    @property
    def site_height_variations(self) -> IDFCollection[SiteHeightVariation]:
        """All ``Site:HeightVariation`` objects in the document. This object is used if the user requires advanced control over height-dependent variations in wind speed and temperature. When this object is not present, the default model for temperature dependen..."""
    @property
    def site_location(self) -> IDFCollection[SiteLocation]:
        """All ``Site:Location`` objects in the document. Specifies the building's location. Only one location is allowed. Weather data file location, if it exists, will override this object."""
    @property
    def site_locations(self) -> IDFCollection[SiteLocation]:
        """All ``Site:Location`` objects in the document. Specifies the building's location. Only one location is allowed. Weather data file location, if it exists, will override this object."""
    @property
    def site_precipitations(self) -> IDFCollection[SitePrecipitation]:
        """All ``Site:Precipitation`` objects in the document. Used to describe the amount of water precipitation at the building site. Precipitation includes both rain and the equivalent water content of snow."""
    @property
    def site_solar_and_visible_spectrums(self) -> IDFCollection[SiteSolarAndVisibleSpectrum]:
        """All ``Site:SolarAndVisibleSpectrum`` objects in the document. If this object is omitted, the default solar and visible spectrum data will be used."""
    @property
    def site_spectrum_datas(self) -> IDFCollection[SiteSpectrumData]:
        """All ``Site:SpectrumData`` objects in the document. Spectrum Data Type is followed by up to 107 sets of normal-incidence measured values of [wavelength, spectrum] for wavelengths covering the solar (0.25 to 2.5 microns) or visible spectrum (0.38 to ..."""
    @property
    def site_variable_locations(self) -> IDFCollection[SiteVariableLocation]:
        """All ``Site:VariableLocation`` objects in the document. Captures the scheduling of a moving/reorienting building, or more likely a vessel"""
    @property
    def site_water_mains_temperatures(self) -> IDFCollection[SiteWaterMainsTemperature]:
        """All ``Site:WaterMainsTemperature`` objects in the document. Used to calculate water mains temperatures delivered by underground water main pipes. Water mains temperatures are a function of outdoor climate conditions and vary with time of year."""
    @property
    def site_weather_stations(self) -> IDFCollection[SiteWeatherStation]:
        """All ``Site:WeatherStation`` objects in the document. This object should only be used for non-standard weather data. Standard weather data such as TMY2, IWEC, and ASHRAE design day data are all measured at the default conditions and do not require thi..."""
    @property
    def sizing_parameters(self) -> IDFCollection[SizingParameters]:
        """All ``Sizing:Parameters`` objects in the document. Specifies global heating and cooling sizing factors/ratios. These ratios are applied at the zone level to all of the zone heating and cooling loads and air flow rates. Then these new loads and air ..."""
    @property
    def sizing_period_design_days(self) -> IDFCollection[SizingPeriodDesignDay]:
        """All ``SizingPeriod:DesignDay`` objects in the document. The design day object creates the parameters for the program to create the 24 hour weather profile that can be used for sizing as well as running to test the other simulation parameters. Parameters..."""
    @property
    def sizing_period_weather_file_condition_types(self) -> IDFCollection[SizingPeriodWeatherFileConditionType]:
        """All ``SizingPeriod:WeatherFileConditionType`` objects in the document. Use a weather file period for design sizing calculations. EPW weather files are created with typical and extreme periods created heuristically from the weather file data. For more details on these ..."""
    @property
    def sizing_period_weather_file_days(self) -> IDFCollection[SizingPeriodWeatherFileDays]:
        """All ``SizingPeriod:WeatherFileDays`` objects in the document. Use a weather file period for design sizing calculations."""
    @property
    def sizing_plants(self) -> IDFCollection[SizingPlant]:
        """All ``Sizing:Plant`` objects in the document. Specifies the input needed to autosize plant loop flow rates and equipment capacities. This information is initially used by components that use water for heating or cooling such as hot or chilled ..."""
    @property
    def sizing_system(self) -> IDFCollection[SizingSystem]:
        """All ``Sizing:System`` objects in the document. Specifies the input needed to perform sizing calculations for a central forced air system. System design air flow, heating capacity, and cooling capacity will be calculated using this input data."""
    @property
    def sizing_systems(self) -> IDFCollection[SizingSystem]:
        """All ``Sizing:System`` objects in the document. Specifies the input needed to perform sizing calculations for a central forced air system. System design air flow, heating capacity, and cooling capacity will be calculated using this input data."""
    @property
    def sizing_zone(self) -> IDFCollection[SizingZone]:
        """All ``Sizing:Zone`` objects in the document. Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, hea..."""
    @property
    def sizing_zones(self) -> IDFCollection[SizingZone]:
        """All ``Sizing:Zone`` objects in the document. Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, hea..."""
    @property
    def solar_collector_flat_plate_photovoltaic_thermals(
        self,
    ) -> IDFCollection[SolarCollectorFlatPlatePhotovoltaicThermal]:
        """All ``SolarCollector:FlatPlate:PhotovoltaicThermal`` objects in the document. Models hybrid photovoltaic-thermal (PVT) solar collectors that convert incident solar energy into both electricity and useful thermal energy by heating air or water."""
    @property
    def solar_collector_flat_plate_waters(self) -> IDFCollection[SolarCollectorFlatPlateWater]:
        """All ``SolarCollector:FlatPlate:Water`` objects in the document. Flat plate water solar collector (single glazed, unglazed, or evacuated tube). Thermal and optical properties are taken from the referenced SolarCollectorPerformance:FlatPlate object. Collector til..."""
    @property
    def solar_collector_integral_collector_storages(self) -> IDFCollection[SolarCollectorIntegralCollectorStorage]:
        """All ``SolarCollector:IntegralCollectorStorage`` objects in the document. Glazed solar collector with integral storage unit. Thermal and optical properties are taken from the referenced SolarCollectorPerformance:IntegralCollectorStorage object. Collector tilt, azimuth, a..."""
    @property
    def solar_collector_performance_flat_plates(self) -> IDFCollection[SolarCollectorPerformanceFlatPlate]:
        """All ``SolarCollectorPerformance:FlatPlate`` objects in the document. Thermal and optical performance parameters for a single flat plate solar collector module. These parameters are based on the testing methodologies described in ASHRAE Standards 93 and 96 which are ..."""
    @property
    def solar_collector_performance_integral_collector_storages(
        self,
    ) -> IDFCollection[SolarCollectorPerformanceIntegralCollectorStorage]:
        """All ``SolarCollectorPerformance:IntegralCollectorStorage`` objects in the document. Thermal and optical performance parameters for a single glazed solar collector with integral storage unit."""
    @property
    def solar_collector_performance_photovoltaic_thermal_bipvts(
        self,
    ) -> IDFCollection[SolarCollectorPerformancePhotovoltaicThermalBIPVT]:
        """All ``SolarCollectorPerformance:PhotovoltaicThermal:BIPVT`` objects in the document. Thermal performance parameters for Building-Integrated Photovoltaic-Thermal (BIPVT) solar collector."""
    @property
    def solar_collector_performance_photovoltaic_thermal_simples(
        self,
    ) -> IDFCollection[SolarCollectorPerformancePhotovoltaicThermalSimple]:
        """All ``SolarCollectorPerformance:PhotovoltaicThermal:Simple`` objects in the document. Thermal performance parameters for a hybrid photovoltaic-thermal (PVT) solar collector."""
    @property
    def solar_collector_unglazed_transpired_multisystems(
        self,
    ) -> IDFCollection[SolarCollectorUnglazedTranspiredMultisystem]:
        """All ``SolarCollector:UnglazedTranspired:Multisystem`` objects in the document. quad-tuples of inlet, outlet, control, and zone nodes for multiple different outdoor air systems attached to same collector"""
    @property
    def solar_collector_unglazed_transpireds(self) -> IDFCollection[SolarCollectorUnglazedTranspired]:
        """All ``SolarCollector:UnglazedTranspired`` objects in the document. Unglazed transpired solar collector (UTSC) used to condition outdoor air. This type of collector is generally used to heat air drawn through perforated absorbers and also recover heat conducted out..."""
    @property
    def space_hvac_equipment_connections(self) -> IDFCollection[SpaceHVACEquipmentConnections]:
        """All ``SpaceHVAC:EquipmentConnections`` objects in the document. Specifies the HVAC equipment connections for a space. Node names are specified for the space air node, air inlet nodes, air exhaust nodes, and the air return node. If any space in a zone has a Spac..."""
    @property
    def space_hvac_zone_equipment_mixers(self) -> IDFCollection[SpaceHVACZoneEquipmentMixer]:
        """All ``SpaceHVAC:ZoneEquipmentMixer`` objects in the document. Mixes the airflow from one or more Spaces into a piece of zone equipment. All spaces in the zone must also have a SpaceHVAC:EquipmentConnections object. Used only when ZoneAirHeatBalanceAlgorithm '..."""
    @property
    def space_hvac_zone_equipment_splitters(self) -> IDFCollection[SpaceHVACZoneEquipmentSplitter]:
        """All ``SpaceHVAC:ZoneEquipmentSplitter`` objects in the document. Distributes the output from a piece of zone equipment to one or more Spaces in the Zone. If any equipment in a zone has a SpaceHVAC:ZoneEquipmentSplitter, then all equipment in the zone must have o..."""
    @property
    def space_hvac_zone_return_mixers(self) -> IDFCollection[SpaceHVACZoneReturnMixer]:
        """All ``SpaceHVAC:ZoneReturnMixer`` objects in the document. Mixes the return airflow from one or more Spaces into a zone return node. All spaces in the zone must also have a SpaceHVAC:EquipmentConnections object. Used only when ZoneAirHeatBalanceAlgorithm '..."""
    @property
    def space_lists(self) -> IDFCollection[SpaceList]:
        """All ``SpaceList`` objects in the document. Defines a list of Spaces which can be referenced as a group. The SpaceList name may be used elsewhere in the input to apply a parameter to all Spaces in the list. SpaceLists can be used effectively..."""
    @property
    def spaces(self) -> IDFCollection[Space]:
        """All ``Space`` objects in the document. Defines a space (room) in the building. All Spaces are part of a Zone. Every Zone contains one or more spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a defaul..."""
    @property
    def steam_equipment_definitions(self) -> IDFCollection[SteamEquipmentDefinition]:
        """All ``SteamEquipment:Definition`` objects in the document. Defines the physical characteristics (design level and heat gain fractions) for steam equipment. Referenced by one or more SteamEquipment:Instance objects."""
    @property
    def steam_equipment_instances(self) -> IDFCollection[SteamEquipmentInstance]:
        """All ``SteamEquipment:Instance`` objects in the document. Sets internal gains for steam equipment in the zone. The physical characteristics are given by the referenced SteamEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more..."""
    @property
    def steam_equipments(self) -> IDFCollection[SteamEquipment]:
        """All ``SteamEquipment`` objects in the document. Sets internal gains for steam equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and eac..."""
    @property
    def sub_surface_construction_assignments(self) -> IDFCollection[SubSurfaceConstructionAssignments]:
        """All ``SubSurfaceConstructionAssignments`` objects in the document. Defines construction assignments for each sub-surface type for a single boundary-condition category (exterior or interior). The generic Window type (kept for backward compatibility) resolves via th..."""
    @property
    def surface_construction_assignments(self) -> IDFCollection[SurfaceConstructionAssignments]:
        """All ``SurfaceConstructionAssignments`` objects in the document. Defines construction assignments for the three opaque surface types (Floor, Wall, Roof/Ceiling) for a single boundary-condition category (exterior, interior, or ground-contact)."""
    @property
    def surface_contaminant_source_and_sink_generic_boundary_layer_diffusions(
        self,
    ) -> IDFCollection[SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion]:
        """All ``SurfaceContaminantSourceAndSink:Generic:BoundaryLayerDiffusion`` objects in the document. Simulate generic contaminant source driven by the boundary layer diffusion controlled model."""
    @property
    def surface_contaminant_source_and_sink_generic_deposition_velocity_sinks(
        self,
    ) -> IDFCollection[SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink]:
        """All ``SurfaceContaminantSourceAndSink:Generic:DepositionVelocitySink`` objects in the document. Simulate generic contaminant source driven by the boundary layer diffusion controlled model."""
    @property
    def surface_contaminant_source_and_sink_generic_pressure_drivens(
        self,
    ) -> IDFCollection[SurfaceContaminantSourceAndSinkGenericPressureDriven]:
        """All ``SurfaceContaminantSourceAndSink:Generic:PressureDriven`` objects in the document. Simulate generic contaminant source driven by the pressure difference across a surface."""
    @property
    def surface_control_movable_insulations(self) -> IDFCollection[SurfaceControlMovableInsulation]:
        """All ``SurfaceControl:MovableInsulation`` objects in the document. Exterior or Interior Insulation on opaque surfaces"""
    @property
    def surface_convection_algorithm_inside_adaptive_model_selections(
        self,
    ) -> IDFCollection[SurfaceConvectionAlgorithmInsideAdaptiveModelSelections]:
        """All ``SurfaceConvectionAlgorithm:Inside:AdaptiveModelSelections`` objects in the document. Options to change the individual convection model equations for dynamic selection when using AdaptiveConvectiongAlgorithm This object is only needed to make changes to the default model selections ..."""
    @property
    def surface_convection_algorithm_inside_user_curves(
        self,
    ) -> IDFCollection[SurfaceConvectionAlgorithmInsideUserCurve]:
        """All ``SurfaceConvectionAlgorithm:Inside:UserCurve`` objects in the document. Used to describe a custom model equation for surface convection heat transfer coefficient If more than one curve is referenced they are all used and added together."""
    @property
    def surface_convection_algorithm_insides(self) -> IDFCollection[SurfaceConvectionAlgorithmInside]:
        """All ``SurfaceConvectionAlgorithm:Inside`` objects in the document. Default indoor surface heat transfer convection algorithm to be used for all zones"""
    @property
    def surface_convection_algorithm_outside_adaptive_model_selections(
        self,
    ) -> IDFCollection[SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections]:
        """All ``SurfaceConvectionAlgorithm:Outside:AdaptiveModelSelections`` objects in the document. Options to change the individual convection model equations for dynamic selection when using AdaptiveConvectiongAlgorithm This object is only needed to make changes to the default model selections ..."""
    @property
    def surface_convection_algorithm_outside_user_curves(
        self,
    ) -> IDFCollection[SurfaceConvectionAlgorithmOutsideUserCurve]:
        """All ``SurfaceConvectionAlgorithm:Outside:UserCurve`` objects in the document. Used to describe a custom model equation for surface convection heat transfer coefficient If more than one curve is referenced they are all used and added together."""
    @property
    def surface_convection_algorithm_outsides(self) -> IDFCollection[SurfaceConvectionAlgorithmOutside]:
        """All ``SurfaceConvectionAlgorithm:Outside`` objects in the document. Default outside surface heat transfer convection algorithm to be used for all zones"""
    @property
    def surface_properties_vapor_coefficients(self) -> IDFCollection[SurfacePropertiesVaporCoefficients]:
        """All ``SurfaceProperties:VaporCoefficients`` objects in the document. The interior and external vapor transfer coefficients. Normally these value are calculated using the heat convection coefficient values. Use this object to used fixed constant values. Units are kg/..."""
    @property
    def surface_property_convection_coefficients(self) -> IDFCollection[SurfacePropertyConvectionCoefficients]:
        """All ``SurfaceProperty:ConvectionCoefficients`` objects in the document. Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coeffici..."""
    @property
    def surface_property_convection_coefficients_multiple_surfaces(
        self,
    ) -> IDFCollection[SurfacePropertyConvectionCoefficientsMultipleSurface]:
        """All ``SurfaceProperty:ConvectionCoefficients:MultipleSurface`` objects in the document. Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coeffici..."""
    @property
    def surface_property_exposed_foundation_perimeters(
        self,
    ) -> IDFCollection[SurfacePropertyExposedFoundationPerimeter]:
        """All ``SurfaceProperty:ExposedFoundationPerimeter`` objects in the document. Defines the perimeter of a foundation floor that is exposed to the exterior environment through the floor. User may either define the total exposed perimeter, fraction of perimeter exposed or indiv..."""
    @property
    def surface_property_exterior_natural_vented_cavities(
        self,
    ) -> IDFCollection[SurfacePropertyExteriorNaturalVentedCavity]:
        """All ``SurfaceProperty:ExteriorNaturalVentedCavity`` objects in the document. Used to describe the decoupled layer, or baffle, and the characteristics of the cavity and openings for naturally ventilated exterior surfaces. This object is also used in conjunction with the Othe..."""
    @property
    def surface_property_ground_surfaces(self) -> IDFCollection[SurfacePropertyGroundSurfaces]:
        """All ``SurfaceProperty:GroundSurfaces`` objects in the document. This object defines a list of ground surfaces for use with an exterior surface."""
    @property
    def surface_property_heat_balance_source_terms(self) -> IDFCollection[SurfacePropertyHeatBalanceSourceTerm]:
        """All ``SurfaceProperty:HeatBalanceSourceTerm`` objects in the document. Allows an additional heat source term to be added to the inside or outside surface boundary. A heat source can be added to either or both the inside and outside of the same surface."""
    @property
    def surface_property_heat_transfer_algorithm_constructions(
        self,
    ) -> IDFCollection[SurfacePropertyHeatTransferAlgorithmConstruction]:
        """All ``SurfaceProperty:HeatTransferAlgorithm:Construction`` objects in the document. Determines which Heat Balance Algorithm will be used for surfaces that have a specific type of construction Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction ..."""
    @property
    def surface_property_heat_transfer_algorithm_multiple_surfaces(
        self,
    ) -> IDFCollection[SurfacePropertyHeatTransferAlgorithmMultipleSurface]:
        """All ``SurfaceProperty:HeatTransferAlgorithm:MultipleSurface`` objects in the document. Determines which Heat Balance Algorithm will be used for a group of surface types Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD ..."""
    @property
    def surface_property_heat_transfer_algorithm_surface_lists(
        self,
    ) -> IDFCollection[SurfacePropertyHeatTransferAlgorithmSurfaceList]:
        """All ``SurfaceProperty:HeatTransferAlgorithm:SurfaceList`` objects in the document. Determines which Heat Balance Algorithm will be used for a list of surfaces Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effec..."""
    @property
    def surface_property_heat_transfer_algorithms(self) -> IDFCollection[SurfacePropertyHeatTransferAlgorithm]:
        """All ``SurfaceProperty:HeatTransferAlgorithm`` objects in the document. Determines which Heat Balance Algorithm will be used for a specific surface Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effec..."""
    @property
    def surface_property_incident_solar_multipliers(self) -> IDFCollection[SurfacePropertyIncidentSolarMultiplier]:
        """All ``SurfaceProperty:IncidentSolarMultiplier`` objects in the document."""
    @property
    def surface_property_local_environments(self) -> IDFCollection[SurfacePropertyLocalEnvironment]:
        """All ``SurfaceProperty:LocalEnvironment`` objects in the document. This object defines the local environment properties of an exterior surface. One or more environment properties have to be defined and linked to the exterior surface."""
    @property
    def surface_property_other_side_coefficients(self) -> IDFCollection[SurfacePropertyOtherSideCoefficients]:
        """All ``SurfaceProperty:OtherSideCoefficients`` objects in the document. This object sets the other side conditions for a surface in a variety of ways."""
    @property
    def surface_property_other_side_conditions_models(self) -> IDFCollection[SurfacePropertyOtherSideConditionsModel]:
        """All ``SurfaceProperty:OtherSideConditionsModel`` objects in the document. This object sets up modifying the other side conditions for a surface from other model results."""
    @property
    def surface_property_solar_incident_insides(self) -> IDFCollection[SurfacePropertySolarIncidentInside]:
        """All ``SurfaceProperty:SolarIncidentInside`` objects in the document. Used to provide incident solar radiation on the inside of the surface. Reference surface-construction pair and if that pair is used in a simulation, then program will use value provided in schedule..."""
    @property
    def surface_property_surrounding_surfaces(self) -> IDFCollection[SurfacePropertySurroundingSurfaces]:
        """All ``SurfaceProperty:SurroundingSurfaces`` objects in the document. This object defines a list of surrounding surfaces for an exterior surface."""
    @property
    def surface_property_underwaters(self) -> IDFCollection[SurfacePropertyUnderwater]:
        """All ``SurfaceProperty:Underwater`` objects in the document. This object sets up a convective water boundary condition for a surface The free stream temperature and velocity are scheduled. If the free stream velocity is zero, the surface will naturally conve..."""
    @property
    def swimming_pool_indoors(self) -> IDFCollection[SwimmingPoolIndoor]:
        """All ``SwimmingPool:Indoor`` objects in the document. Specifies an indoor swimming pools linked to a floor surface. The pool is assumed to cover the entire floor to which it is linked."""
    @property
    def table_independent_variable_lists(self) -> IDFCollection[TableIndependentVariableList]:
        """All ``Table:IndependentVariableList`` objects in the document. A sorted list of independent variables used by one or more Table:Lookup objects."""
    @property
    def table_independent_variables(self) -> IDFCollection[TableIndependentVariable]:
        """All ``Table:IndependentVariable`` objects in the document. An independent variable representing a single dimension of a Table:Lookup object."""
    @property
    def table_lookups(self) -> IDFCollection[TableLookup]:
        """All ``Table:Lookup`` objects in the document. Lookup tables are used in place of curves and can represent any number of independent variables (defined as Table:IndependentVariable objects in a Table:IndependentVariableList). Output values are ..."""
    @property
    def tempering_valves(self) -> IDFCollection[TemperingValve]:
        """All ``TemperingValve`` objects in the document. Temperature-controlled diversion valve used to divert flow around one or more plant components such as a hot water heater. It can only be used on one of two branches between a Splitter and a Mixer."""
    @property
    def thermal_storage_chilled_water_mixeds(self) -> IDFCollection[ThermalStorageChilledWaterMixed]:
        """All ``ThermalStorage:ChilledWater:Mixed`` objects in the document. Chilled water storage with a well-mixed, single-node tank. The chilled water is 'used' by drawing from the 'Use Side' of the water tank. The tank is indirectly charged by circulating cold water thr..."""
    @property
    def thermal_storage_chilled_water_stratifieds(self) -> IDFCollection[ThermalStorageChilledWaterStratified]:
        """All ``ThermalStorage:ChilledWater:Stratified`` objects in the document. Chilled water storage with a stratified, multi-node tank. The chilled water is 'used' by drawing from the 'Use Side' of the water tank. The tank is indirectly charged by circulating cold water thro..."""
    @property
    def thermal_storage_hot_water_stratifieds(self) -> IDFCollection[ThermalStorageHotWaterStratified]:
        """All ``ThermalStorage:HotWater:Stratified`` objects in the document."""
    @property
    def thermal_storage_ice_detaileds(self) -> IDFCollection[ThermalStorageIceDetailed]:
        """All ``ThermalStorage:Ice:Detailed`` objects in the document. This input syntax is intended to describe a thermal storage system that includes smaller containers filled with water that are placed in a larger tank or series of tanks. The model uses polynomial ..."""
    @property
    def thermal_storage_ice_simples(self) -> IDFCollection[ThermalStorageIceSimple]:
        """All ``ThermalStorage:Ice:Simple`` objects in the document. This ice storage model is a simplified model It requires a setpoint placed on the Chilled Water Side Outlet Node It should be placed in the chilled water supply side outlet branch followed by a pip..."""
    @property
    def thermal_storage_pcms(self) -> IDFCollection[ThermalStoragePCM]:
        """All ``ThermalStorage:PCM`` objects in the document. This thermal storage model is PCM-based It requires PCM material property connection In addition to the object linking, this object needs PCM Latent heat storage capacity and Heat Loss Rate This mo..."""
    @property
    def thermal_storage_sizings(self) -> IDFCollection[ThermalStorageSizing]:
        """All ``ThermalStorage:Sizing`` objects in the document. Sizing information for thermal energy stoarge capacity."""
    @property
    def thermostat_setpoint_dual_setpoints(self) -> IDFCollection[ThermostatSetpointDualSetpoint]:
        """All ``ThermostatSetpoint:DualSetpoint`` objects in the document. Used for a heating and cooling thermostat with dual setpoints. The setpoints can be scheduled and varied throughout the simulation for both heating and cooling."""
    @property
    def thermostat_setpoint_single_coolings(self) -> IDFCollection[ThermostatSetpointSingleCooling]:
        """All ``ThermostatSetpoint:SingleCooling`` objects in the document. Used for a cooling only thermostat. The setpoint can be scheduled and varied throughout the simulation but only cooling is allowed."""
    @property
    def thermostat_setpoint_single_heating_or_coolings(self) -> IDFCollection[ThermostatSetpointSingleHeatingOrCooling]:
        """All ``ThermostatSetpoint:SingleHeatingOrCooling`` objects in the document. Used for a heating and cooling thermostat with a single setpoint. The setpoint can be scheduled and varied throughout the simulation for both heating and cooling."""
    @property
    def thermostat_setpoint_single_heatings(self) -> IDFCollection[ThermostatSetpointSingleHeating]:
        """All ``ThermostatSetpoint:SingleHeating`` objects in the document. Used for a heating only thermostat. The setpoint can be scheduled and varied throughout the simulation but only heating is allowed with this control type."""
    @property
    def thermostat_setpoint_thermal_comfort_fanger_dual_setpoints(
        self,
    ) -> IDFCollection[ThermostatSetpointThermalComfortFangerDualSetpoint]:
        """All ``ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint`` objects in the document. Used for heating and cooling thermal comfort control with dual setpoints. The PMV setpoints can be scheduled and varied throughout the simulation for both heating and cooling."""
    @property
    def thermostat_setpoint_thermal_comfort_fanger_single_coolings(
        self,
    ) -> IDFCollection[ThermostatSetpointThermalComfortFangerSingleCooling]:
        """All ``ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling`` objects in the document. Used for cooling only thermal comfort control. The PMV setpoint can be scheduled and varied throughout the simulation but only cooling is allowed with this control type."""
    @property
    def thermostat_setpoint_thermal_comfort_fanger_single_heating_or_coolings(
        self,
    ) -> IDFCollection[ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling]:
        """All ``ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling`` objects in the document. Used for heating and cooling thermal comfort control with a single setpoint. The PMV setpoint can be scheduled and varied throughout the simulation for both heating and cooling."""
    @property
    def thermostat_setpoint_thermal_comfort_fanger_single_heatings(
        self,
    ) -> IDFCollection[ThermostatSetpointThermalComfortFangerSingleHeating]:
        """All ``ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating`` objects in the document. Used for heating only thermal comfort control. The PMV setpoint can be scheduled and varied throughout the simulation but only heating is allowed with this control type."""
    @property
    def thermostats(self) -> IDFCollection[ThermostatSetpointDualSetpoint]:
        """All ``ThermostatSetpoint:DualSetpoint`` objects in the document. Used for a heating and cooling thermostat with dual setpoints. The setpoints can be scheduled and varied throughout the simulation for both heating and cooling."""
    @property
    def timestep(self) -> IDFCollection[Timestep]:
        """All ``Timestep`` objects in the document. Specifies the 'basic' timestep for the simulation. The value entered here is also known as the Zone Timestep. This is used in the Zone Heat Balance Model calculation as the driving timestep for hea..."""
    @property
    def timesteps(self) -> IDFCollection[Timestep]:
        """All ``Timestep`` objects in the document. Specifies the 'basic' timestep for the simulation. The value entered here is also known as the Zone Timestep. This is used in the Zone Heat Balance Model calculation as the driving timestep for hea..."""
    @property
    def unitary_system_performance_multispeeds(self) -> IDFCollection[UnitarySystemPerformanceMultispeed]:
        """All ``UnitarySystemPerformance:Multispeed`` objects in the document. The UnitarySystemPerformance object is used to specify the air flow ratio at each operating speed. This object is primarily used for multispeed DX and water coils to allow operation at alternate fl..."""
    @property
    def utility_cost_charge_blocks(self) -> IDFCollection[UtilityCostChargeBlock]:
        """All ``UtilityCost:Charge:Block`` objects in the document. Used to compute energy and demand charges (or any other charges) that are structured in blocks of charges. Multiple UtilityCost:Charge:Block objects may be defined for a single tariff and they will..."""
    @property
    def utility_cost_charge_simples(self) -> IDFCollection[UtilityCostChargeSimple]:
        """All ``UtilityCost:Charge:Simple`` objects in the document. UtilityCost:Charge:Simple is one of the most often used objects for tariff calculation. It is used to compute energy and demand charges that are very simple. It may also be used for taxes, surcharg..."""
    @property
    def utility_cost_computations(self) -> IDFCollection[UtilityCostComputation]:
        """All ``UtilityCost:Computation`` objects in the document. The object lists a series of computations that are used to perform the utility bill calculation. The object is only used for complex tariffs that cannot be modeled any other way. For most utility t..."""
    @property
    def utility_cost_qualifies(self) -> IDFCollection[UtilityCostQualify]:
        """All ``UtilityCost:Qualify`` objects in the document. The qualify object allows only tariffs to be selected based on limits which may apply such as maximum or minimum demand requirements. If the results of the simulation fall outside of the range of q..."""
    @property
    def utility_cost_ratchets(self) -> IDFCollection[UtilityCostRatchet]:
        """All ``UtilityCost:Ratchet`` objects in the document. Allows the modeling of tariffs that include some type of seasonal ratcheting. Ratchets are most common when used with electric demand charges. A ratchet is when a utility requires that the demand c..."""
    @property
    def utility_cost_tariffs(self) -> IDFCollection[UtilityCostTariff]:
        """All ``UtilityCost:Tariff`` objects in the document. Defines the name of a utility cost tariff, the type of tariff, and other details about the overall tariff. Each other object that is part of the tariff model references the tariff name. See Utility..."""
    @property
    def utility_cost_variables(self) -> IDFCollection[UtilityCostVariable]:
        """All ``UtilityCost:Variable`` objects in the document. Allows for the direct entry of monthly values into a utility tariff variable."""
    @property
    def ventilation(self) -> IDFCollection[ZoneVentilationDesignFlowRate]:
        """All ``ZoneVentilation:DesignFlowRate`` objects in the document. Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D *..."""
    @property
    def versions(self) -> IDFCollection[Version]:
        """All ``Version`` objects in the document. Specifies the EnergyPlus version of the IDF file."""
    @property
    def wall_adiabatics(self) -> IDFCollection[WallAdiabatic]:
        """All ``Wall:Adiabatic`` objects in the document. Allows for simplified entry of interior walls."""
    @property
    def wall_detaileds(self) -> IDFCollection[WallDetailed]:
        """All ``Wall:Detailed`` objects in the document. Allows for detailed entry of wall heat transfer surfaces."""
    @property
    def wall_exteriors(self) -> IDFCollection[WallExterior]:
        """All ``Wall:Exterior`` objects in the document. Allows for simplified entry of exterior walls. View Factor to Ground is automatically calculated."""
    @property
    def wall_interzones(self) -> IDFCollection[WallInterzone]:
        """All ``Wall:Interzone`` objects in the document. Allows for simplified entry of interzone walls (walls between zones)."""
    @property
    def wall_undergrounds(self) -> IDFCollection[WallUnderground]:
        """All ``Wall:Underground`` objects in the document. Allows for simplified entry of underground walls."""
    @property
    def water_heater_heat_pump_pumped_condensers(self) -> IDFCollection[WaterHeaterHeatPumpPumpedCondenser]:
        """All ``WaterHeater:HeatPump:PumpedCondenser`` objects in the document. This object models an air-source heat pump for water heating where the water is pumped out of the tank, through a heating coil and returned to the tank. For wrapped condenser HPWHs, see WaterHeater..."""
    @property
    def water_heater_heat_pump_wrapped_condensers(self) -> IDFCollection[WaterHeaterHeatPumpWrappedCondenser]:
        """All ``WaterHeater:HeatPump:WrappedCondenser`` objects in the document. This object models an air-source heat pump for water heating where the heating coil is wrapped around the tank, which is typical of residential HPWHs. For pumped condenser HPWHs, see WaterHeater:He..."""
    @property
    def water_heater_mixeds(self) -> IDFCollection[WaterHeaterMixed]:
        """All ``WaterHeater:Mixed`` objects in the document. Water heater with well-mixed, single-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater ..."""
    @property
    def water_heater_sizings(self) -> IDFCollection[WaterHeaterSizing]:
        """All ``WaterHeater:Sizing`` objects in the document. This input object is used with WaterHeater:Mixed or with WaterHeater:Stratified to autosize tank volume and heater capacity This object is not needed if water heaters are not autosized."""
    @property
    def water_heater_stratifieds(self) -> IDFCollection[WaterHeaterStratified]:
        """All ``WaterHeater:Stratified`` objects in the document. Water heater with stratified, multi-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (..."""
    @property
    def water_use_connections(self) -> IDFCollection[WaterUseConnections]:
        """All ``WaterUse:Connections`` objects in the document. A subsystem that groups together multiple WaterUse:Equipment components. As its name suggests, the object provides connections that are shared by these components, including: 1. Inlet node and outl..."""
    @property
    def water_use_equipments(self) -> IDFCollection[WaterUseEquipment]:
        """All ``WaterUse:Equipment`` objects in the document. A generalized object for simulating all water end uses. Hot and cold water uses are included, as well as controlled mixing of hot and cold water at the tap. The WaterUse:Equipment object can be use..."""
    @property
    def water_use_rain_collectors(self) -> IDFCollection[WaterUseRainCollector]:
        """All ``WaterUse:RainCollector`` objects in the document. Used for harvesting rainwater falling on building surfaces. The rainwater is sent to a WaterUse:Storage object. In versions up till Version 9.6, it is necessary to also include a Site:Precipitation..."""
    @property
    def water_use_storages(self) -> IDFCollection[WaterUseStorage]:
        """All ``WaterUse:Storage`` objects in the document. A water storage tank. If the building model is to include any on-site water collection, wells, or storing and reuse of graywater, then a WaterUse:Storage object is needed. Each WaterUse:Storage can..."""
    @property
    def water_use_wells(self) -> IDFCollection[WaterUseWell]:
        """All ``WaterUse:Well`` objects in the document. Simulates on-site water supply from a well. Well water is pumped out of the ground into a WaterUse:Storage. The operation of the ground water well is controlled by the associated WaterUse:Storage w..."""
    @property
    def weather_property_sky_temperatures(self) -> IDFCollection[WeatherPropertySkyTemperature]:
        """All ``WeatherProperty:SkyTemperature`` objects in the document. This object is used to override internal sky temperature calculations."""
    @property
    def window_gap_deflection_states(self) -> IDFCollection[WindowGapDeflectionState]:
        """All ``WindowGap:DeflectionState`` objects in the document. Used to enter data describing deflection state of the gap. It is referenced from WindowMaterial:Gap object only and it is used only when deflection model is set to MeasuredDeflection, otherwise it ..."""
    @property
    def window_gap_support_pillars(self) -> IDFCollection[WindowGapSupportPillar]:
        """All ``WindowGap:SupportPillar`` objects in the document. used to define pillar geometry for support pillars"""
    @property
    def window_interzones(self) -> IDFCollection[WindowInterzone]:
        """All ``Window:Interzone`` objects in the document. Allows for simplified entry of interzone windows (adjacent to other zones)."""
    @property
    def window_material_blind_equivalent_layers(self) -> IDFCollection[WindowMaterialBlindEquivalentLayer]:
        """All ``WindowMaterial:Blind:EquivalentLayer`` objects in the document. Window equivalent layer blind slat optical and thermal properties. The model assumes that slats are thin and flat, applies correction empirical correlation to account for curvature effect. Slats ar..."""
    @property
    def window_material_blinds(self) -> IDFCollection[WindowMaterialBlind]:
        """All ``WindowMaterial:Blind`` objects in the document. Window blind thermal properties"""
    @property
    def window_material_complex_shades(self) -> IDFCollection[WindowMaterialComplexShade]:
        """All ``WindowMaterial:ComplexShade`` objects in the document. Complex window shading layer thermal properties"""
    @property
    def window_material_drape_equivalent_layers(self) -> IDFCollection[WindowMaterialDrapeEquivalentLayer]:
        """All ``WindowMaterial:Drape:EquivalentLayer`` objects in the document. Specifies the properties of equivalent layer drape fabric materials. Shades are considered to be perfect diffusers (all transmitted and reflected radiation is hemispherically-diffuse) independent o..."""
    @property
    def window_material_gap_equivalent_layers(self) -> IDFCollection[WindowMaterialGapEquivalentLayer]:
        """All ``WindowMaterial:Gap:EquivalentLayer`` objects in the document. Gas material properties that are used in Windows Equivalent Layer References only WindowMaterial:Gas properties"""
    @property
    def window_material_gaps(self) -> IDFCollection[WindowMaterialGap]:
        """All ``WindowMaterial:Gap`` objects in the document. Used to define the gap between two layers in a complex fenestration system, where the Construction:ComplexFenestrationState object is used. It is referenced as a layer in the Construction:ComplexFe..."""
    @property
    def window_material_gas(self) -> IDFCollection[WindowMaterialGas]:
        """All ``WindowMaterial:Gas`` objects in the document. Gas material properties that are used in Windows or Glass Doors"""
    @property
    def window_material_gas_mixtures(self) -> IDFCollection[WindowMaterialGasMixture]:
        """All ``WindowMaterial:GasMixture`` objects in the document. Gas mixtures that are used in Windows or Glass Doors"""
    @property
    def window_material_gases(self) -> IDFCollection[WindowMaterialGas]:
        """All ``WindowMaterial:Gas`` objects in the document. Gas material properties that are used in Windows or Glass Doors"""
    @property
    def window_material_glazing(self) -> IDFCollection[WindowMaterialGlazing]:
        """All ``WindowMaterial:Glazing`` objects in the document. Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method."""
    @property
    def window_material_glazing_equivalent_layers(self) -> IDFCollection[WindowMaterialGlazingEquivalentLayer]:
        """All ``WindowMaterial:Glazing:EquivalentLayer`` objects in the document. Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method."""
    @property
    def window_material_glazing_group_thermochromics(self) -> IDFCollection[WindowMaterialGlazingGroupThermochromic]:
        """All ``WindowMaterial:GlazingGroup:Thermochromic`` objects in the document. thermochromic glass at different temperatures"""
    @property
    def window_material_glazing_refraction_extinction_methods(
        self,
    ) -> IDFCollection[WindowMaterialGlazingRefractionExtinctionMethod]:
        """All ``WindowMaterial:Glazing:RefractionExtinctionMethod`` objects in the document. Glass material properties for Windows or Glass Doors Index of Refraction/Extinction Coefficient input method Not to be used for coated glass"""
    @property
    def window_material_glazings(self) -> IDFCollection[WindowMaterialGlazing]:
        """All ``WindowMaterial:Glazing`` objects in the document. Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method."""
    @property
    def window_material_screen_equivalent_layers(self) -> IDFCollection[WindowMaterialScreenEquivalentLayer]:
        """All ``WindowMaterial:Screen:EquivalentLayer`` objects in the document. Equivalent layer window screen physical properties. Can only be located on the exterior side of a window construction."""
    @property
    def window_material_screens(self) -> IDFCollection[WindowMaterialScreen]:
        """All ``WindowMaterial:Screen`` objects in the document. Window screen physical properties. Can only be located on the exterior side of a window construction."""
    @property
    def window_material_shade_equivalent_layers(self) -> IDFCollection[WindowMaterialShadeEquivalentLayer]:
        """All ``WindowMaterial:Shade:EquivalentLayer`` objects in the document. Specifies the properties of equivalent layer window shade material Shades are considered to be perfect diffusers (all transmitted and reflected radiation is hemispherically-diffuse) independent of ..."""
    @property
    def window_material_shades(self) -> IDFCollection[WindowMaterialShade]:
        """All ``WindowMaterial:Shade`` objects in the document. Specifies the properties of window shade materials. Reflectance and emissivity properties are assumed to be the same on both sides of the shade. Shades are considered to be perfect diffusers (all t..."""
    @property
    def window_material_simple(self) -> IDFCollection[WindowMaterialSimpleGlazingSystem]:
        """All ``WindowMaterial:SimpleGlazingSystem`` objects in the document. Alternate method of describing windows This window material object is used to define an entire glazing system using simple performance parameters."""
    @property
    def window_material_simple_glazing_systems(self) -> IDFCollection[WindowMaterialSimpleGlazingSystem]:
        """All ``WindowMaterial:SimpleGlazingSystem`` objects in the document. Alternate method of describing windows This window material object is used to define an entire glazing system using simple performance parameters."""
    @property
    def window_property_airflow_controls(self) -> IDFCollection[WindowPropertyAirflowControl]:
        """All ``WindowProperty:AirflowControl`` objects in the document. Used to control forced airflow through a gap between glass layers"""
    @property
    def window_property_frame_and_dividers(self) -> IDFCollection[WindowPropertyFrameAndDivider]:
        """All ``WindowProperty:FrameAndDivider`` objects in the document. Specifies the dimensions of a window frame, dividers, and inside reveal surfaces. Referenced by the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, ..."""
    @property
    def window_property_storm_windows(self) -> IDFCollection[WindowPropertyStormWindow]:
        """All ``WindowProperty:StormWindow`` objects in the document. This is a movable exterior glass layer that is usually applied in the winter and removed in the summer."""
    @property
    def window_shading_controls(self) -> IDFCollection[WindowShadingControl]:
        """All ``WindowShadingControl`` objects in the document. Specifies the type, location, and controls for window shades, window blinds, and switchable glazing. Referencing the surface objects for exterior windows and glass doors (ref: FenestrationSurface:D..."""
    @property
    def window_thermal_model_params(self) -> IDFCollection[WindowThermalModelParams]:
        """All ``WindowThermalModel:Params`` objects in the document. object is used to select which thermal model should be used in tarcog simulations"""
    @property
    def windows(self) -> IDFCollection[Window]:
        """All ``Window`` objects in the document. Allows for simplified entry of Windows."""
    @property
    def windows_calculation_engines(self) -> IDFCollection[WindowsCalculationEngine]:
        """All ``WindowsCalculationEngine`` objects in the document. Describes which window model will be used in calculations. Built in windows model will use algorithms that are part of EnergyPlus, while ExternalWindowsModel will use Windows-CalcEngine library to ..."""
    @property
    def zone_air_balance_outdoor_airs(self) -> IDFCollection[ZoneAirBalanceOutdoorAir]:
        """All ``ZoneAirBalance:OutdoorAir`` objects in the document. Provide a combined zone outdoor air flow by including interactions between mechanical ventilation, infiltration and duct leakage. This object will combine outdoor flows from all ZoneInfiltration an..."""
    @property
    def zone_air_contaminant_balances(self) -> IDFCollection[ZoneAirContaminantBalance]:
        """All ``ZoneAirContaminantBalance`` objects in the document. Determines which contaminant concentration will be simulates."""
    @property
    def zone_air_heat_balance_algorithms(self) -> IDFCollection[ZoneAirHeatBalanceAlgorithm]:
        """All ``ZoneAirHeatBalanceAlgorithm`` objects in the document. Controls the zone/space air heat balance."""
    @property
    def zone_air_mass_flow_conservations(self) -> IDFCollection[ZoneAirMassFlowConservation]:
        """All ``ZoneAirMassFlowConservation`` objects in the document. Enforces the zone air mass flow balance by either adjusting zone mixing object flow only, adjusting zone total return flow only, zone mixing and the zone total return flows, or adjusting the zone t..."""
    @property
    def zone_baseboard_outdoor_temperature_controlleds(
        self,
    ) -> IDFCollection[ZoneBaseboardOutdoorTemperatureControlled]:
        """All ``ZoneBaseboard:OutdoorTemperatureControlled`` objects in the document. Specifies outside temperature-controlled electric baseboard heating. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable..."""
    @property
    def zone_capacitance_multiplier_research_specials(self) -> IDFCollection[ZoneCapacitanceMultiplierResearchSpecial]:
        """All ``ZoneCapacitanceMultiplier:ResearchSpecial`` objects in the document. Multiplier altering the relative capacitance of the air compared to an empty zone"""
    @property
    def zone_contaminant_source_and_sink_carbon_dioxides(
        self,
    ) -> IDFCollection[ZoneContaminantSourceAndSinkCarbonDioxide]:
        """All ``ZoneContaminantSourceAndSink:CarbonDioxide`` objects in the document. Represents internal CO2 gains and sinks in the zone."""
    @property
    def zone_contaminant_source_and_sink_generic_constants(
        self,
    ) -> IDFCollection[ZoneContaminantSourceAndSinkGenericConstant]:
        """All ``ZoneContaminantSourceAndSink:Generic:Constant`` objects in the document. Sets internal generic contaminant gains and sinks in a zone with constant values."""
    @property
    def zone_contaminant_source_and_sink_generic_cutoff_models(
        self,
    ) -> IDFCollection[ZoneContaminantSourceAndSinkGenericCutoffModel]:
        """All ``ZoneContaminantSourceAndSink:Generic:CutoffModel`` objects in the document. Simulate generic contaminant source driven by the cutoff concentration model."""
    @property
    def zone_contaminant_source_and_sink_generic_decay_sources(
        self,
    ) -> IDFCollection[ZoneContaminantSourceAndSinkGenericDecaySource]:
        """All ``ZoneContaminantSourceAndSink:Generic:DecaySource`` objects in the document. Simulate generic contaminant source driven by the cutoff concentration model."""
    @property
    def zone_contaminant_source_and_sink_generic_deposition_rate_sinks(
        self,
    ) -> IDFCollection[ZoneContaminantSourceAndSinkGenericDepositionRateSink]:
        """All ``ZoneContaminantSourceAndSink:Generic:DepositionRateSink`` objects in the document. Simulate generic contaminant source driven by the boundary layer diffusion controlled model."""
    @property
    def zone_control_contaminant_controllers(self) -> IDFCollection[ZoneControlContaminantController]:
        """All ``ZoneControl:ContaminantController`` objects in the document. Used to control a zone to a specified indoor level of CO2 or generic contaminants, or to specify minimum CO2 concentration schedule name for a zone."""
    @property
    def zone_control_humidistats(self) -> IDFCollection[ZoneControlHumidistat]:
        """All ``ZoneControl:Humidistat`` objects in the document. Specifies zone relative humidity setpoint schedules for humidifying and dehumidifying."""
    @property
    def zone_control_thermostat_operative_temperatures(
        self,
    ) -> IDFCollection[ZoneControlThermostatOperativeTemperature]:
        """All ``ZoneControl:Thermostat:OperativeTemperature`` objects in the document. This object can be used with the ZoneList option on a thermostat or with one of the zones on that list (but you won't be able to use the object list to pick only one of those zones. Thermostat name..."""
    @property
    def zone_control_thermostat_staged_dual_setpoints(self) -> IDFCollection[ZoneControlThermostatStagedDualSetpoint]:
        """All ``ZoneControl:Thermostat:StagedDualSetpoint`` objects in the document. Define the Thermostat StagedDualSetpoint settings for a zone or list of zones. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList."""
    @property
    def zone_control_thermostat_temperature_and_humidities(
        self,
    ) -> IDFCollection[ZoneControlThermostatTemperatureAndHumidity]:
        """All ``ZoneControl:Thermostat:TemperatureAndHumidity`` objects in the document. This object modifies a ZoneControl:Thermostat object to effect temperature control based on zone air humidity conditions."""
    @property
    def zone_control_thermostat_thermal_comforts(self) -> IDFCollection[ZoneControlThermostatThermalComfort]:
        """All ``ZoneControl:Thermostat:ThermalComfort`` objects in the document. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList."""
    @property
    def zone_control_thermostats(self) -> IDFCollection[ZoneControlThermostat]:
        """All ``ZoneControl:Thermostat`` objects in the document. Define the Thermostat settings for a zone or list of zones. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList."""
    @property
    def zone_cool_tower_showers(self) -> IDFCollection[ZoneCoolTowerShower]:
        """All ``ZoneCoolTower:Shower`` objects in the document. A cooltower (sometimes referred to as a wind tower or a shower cooling tower) models passive downdraught evaporative cooling (PDEC) that is designed to capture the wind at the top of a tower and co..."""
    @property
    def zone_cross_mixings(self) -> IDFCollection[ZoneCrossMixing]:
        """All ``ZoneCrossMixing`` objects in the document. ZoneCrossMixing exchanges an equal amount of air between two zones or spaces. Note that this statement affects the energy balance of both zones or spaces."""
    @property
    def zone_earthtube_parameters(self) -> IDFCollection[ZoneEarthtubeParameters]:
        """All ``ZoneEarthtube:Parameters`` objects in the document. Parameters that apply to the vertical model for an earth tube"""
    @property
    def zone_earthtubes(self) -> IDFCollection[ZoneEarthtube]:
        """All ``ZoneEarthtube`` objects in the document. Earth Tube is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Earthtube=Edesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * Wi..."""
    @property
    def zone_groups(self) -> IDFCollection[ZoneGroup]:
        """All ``ZoneGroup`` objects in the document. Adds a multiplier to a ZoneList. This can be used to reduce the amount of input necessary for simulating repetitive structures, such as the identical floors of a multi-story building."""
    @property
    def zone_hvac_air_distribution_units(self) -> IDFCollection[ZoneHVACAirDistributionUnit]:
        """All ``ZoneHVAC:AirDistributionUnit`` objects in the document. Central air system air distribution unit, serves as a wrapper for a specific type of air terminal unit. This object is referenced in a ZoneHVAC:EquipmentList."""
    @property
    def zone_hvac_baseboard_convective_electrics(self) -> IDFCollection[ZoneHVACBaseboardConvectiveElectric]:
        """All ``ZoneHVAC:Baseboard:Convective:Electric`` objects in the document. Electric baseboard heater, convection-only. Natural convection electric heating unit."""
    @property
    def zone_hvac_baseboard_convective_waters(self) -> IDFCollection[ZoneHVACBaseboardConvectiveWater]:
        """All ``ZoneHVAC:Baseboard:Convective:Water`` objects in the document. Hot water baseboard heater, convection-only. Natural convection hydronic heating unit."""
    @property
    def zone_hvac_baseboard_radiant_convective_electrics(
        self,
    ) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveElectric]:
        """All ``ZoneHVAC:Baseboard:RadiantConvective:Electric`` objects in the document. The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list"""
    @property
    def zone_hvac_baseboard_radiant_convective_steam_designs(
        self,
    ) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveSteamDesign]:
        """All ``ZoneHVAC:Baseboard:RadiantConvective:Steam:Design`` objects in the document."""
    @property
    def zone_hvac_baseboard_radiant_convective_steams(self) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveSteam]:
        """All ``ZoneHVAC:Baseboard:RadiantConvective:Steam`` objects in the document. The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list."""
    @property
    def zone_hvac_baseboard_radiant_convective_water_designs(
        self,
    ) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveWaterDesign]:
        """All ``ZoneHVAC:Baseboard:RadiantConvective:Water:Design`` objects in the document."""
    @property
    def zone_hvac_baseboard_radiant_convective_waters(self) -> IDFCollection[ZoneHVACBaseboardRadiantConvectiveWater]:
        """All ``ZoneHVAC:Baseboard:RadiantConvective:Water`` objects in the document. The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list"""
    @property
    def zone_hvac_cooling_panel_radiant_convective_waters(
        self,
    ) -> IDFCollection[ZoneHVACCoolingPanelRadiantConvectiveWater]:
        """All ``ZoneHVAC:CoolingPanel:RadiantConvective:Water`` objects in the document. The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list"""
    @property
    def zone_hvac_dehumidifier_dxes(self) -> IDFCollection[ZoneHVACDehumidifierDX]:
        """All ``ZoneHVAC:Dehumidifier:DX`` objects in the document. This object calculates the performance of zone (room) air dehumidifiers. Meant to model conventional direct expansion (DX) cooling-based room air dehumidifiers (reject 100% of condenser heat to the..."""
    @property
    def zone_hvac_energy_recovery_ventilator_controllers(
        self,
    ) -> IDFCollection[ZoneHVACEnergyRecoveryVentilatorController]:
        """All ``ZoneHVAC:EnergyRecoveryVentilator:Controller`` objects in the document. This controller is used exclusively by the ZoneHVAC:EnergyRecoveryVentilator object to allow economizer (free cooling) operation when possible."""
    @property
    def zone_hvac_energy_recovery_ventilators(self) -> IDFCollection[ZoneHVACEnergyRecoveryVentilator]:
        """All ``ZoneHVAC:EnergyRecoveryVentilator`` objects in the document. This compound component models a stand-alone energy recovery ventilator (ERV) that conditions outdoor ventilation air and supplies that air directly to a zone. The ERV unit is modeled as a collecti..."""
    @property
    def zone_hvac_equipment_connections(self) -> IDFCollection[ZoneHVACEquipmentConnections]:
        """All ``ZoneHVAC:EquipmentConnections`` objects in the document. Specifies the HVAC equipment connections for a zone. Node names are specified for the zone air node, air inlet nodes, air exhaust nodes, and the air return node. A zone equipment list is referenced..."""
    @property
    def zone_hvac_equipment_lists(self) -> IDFCollection[ZoneHVACEquipmentList]:
        """All ``ZoneHVAC:EquipmentList`` objects in the document. List equipment in simulation order. Note that an ZoneHVAC:AirDistributionUnit object must be listed in this statement if there is a forced air system serving the zone from the air loop. Equipment i..."""
    @property
    def zone_hvac_evaporative_cooler_units(self) -> IDFCollection[ZoneHVACEvaporativeCoolerUnit]:
        """All ``ZoneHVAC:EvaporativeCoolerUnit`` objects in the document. Zone evaporative cooler. Forced-convection cooling-only unit with supply fan, 100% outdoor air supply. Optional relief exhaust node"""
    @property
    def zone_hvac_exhaust_controls(self) -> IDFCollection[ZoneHVACExhaustControl]:
        """All ``ZoneHVAC:ExhaustControl`` objects in the document. Defines a controlled exhaust flow from a zone which finally feeds into one of AirLoopHVAC:ZoneMixer's inlets, which are part of an AirLoopHVAC:ExhaustSystem."""
    @property
    def zone_hvac_forced_air_user_defineds(self) -> IDFCollection[ZoneHVACForcedAirUserDefined]:
        """All ``ZoneHVAC:ForcedAir:UserDefined`` objects in the document. Defines a generic zone air unit for custom modeling using Energy Management System or External Interface"""
    @property
    def zone_hvac_four_pipe_fan_coils(self) -> IDFCollection[ZoneHVACFourPipeFanCoil]:
        """All ``ZoneHVAC:FourPipeFanCoil`` objects in the document. Four pipe fan coil system. Forced-convection hydronic heating-cooling unit with supply fan, hot water heating coil, chilled water cooling coil, and fixed-position outdoor air mixer."""
    @property
    def zone_hvac_high_temperature_radiants(self) -> IDFCollection[ZoneHVACHighTemperatureRadiant]:
        """All ``ZoneHVAC:HighTemperatureRadiant`` objects in the document. The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list"""
    @property
    def zone_hvac_hybrid_unitary_hvacs(self) -> IDFCollection[ZoneHVACHybridUnitaryHVAC]:
        """All ``ZoneHVAC:HybridUnitaryHVAC`` objects in the document. Hybrid Unitary HVAC. A black box model for multi-mode packaged forced air equipment. Independent variables include outdoor air conditions and indoor air conditions. Controlled inputs include operat..."""
    @property
    def zone_hvac_ideal_loads_air_systems(self) -> IDFCollection[ZoneHVACIdealLoadsAirSystem]:
        """All ``ZoneHVAC:IdealLoadsAirSystem`` objects in the document. Ideal system used to calculate loads without modeling a full HVAC system. All that is required for the ideal system are zone controls, zone equipment configurations, and the ideal loads system comp..."""
    @property
    def zone_hvac_low_temperature_radiant_constant_flow_designs(
        self,
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantConstantFlowDesign]:
        """All ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design`` objects in the document."""
    @property
    def zone_hvac_low_temperature_radiant_constant_flows(
        self,
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantConstantFlow]:
        """All ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow`` objects in the document. Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water temperature circulating throu..."""
    @property
    def zone_hvac_low_temperature_radiant_electrics(self) -> IDFCollection[ZoneHVACLowTemperatureRadiantElectric]:
        """All ``ZoneHVAC:LowTemperatureRadiant:Electric`` objects in the document. Electric resistance low temperature radiant system"""
    @property
    def zone_hvac_low_temperature_radiant_surface_groups(
        self,
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantSurfaceGroup]:
        """All ``ZoneHVAC:LowTemperatureRadiant:SurfaceGroup`` objects in the document. This is used to allow the coordinate control of several radiant system surfaces. Note that the following flow fractions must sum up to 1.0 The number of surfaces can be expanded beyond 100, if nece..."""
    @property
    def zone_hvac_low_temperature_radiant_variable_flow_designs(
        self,
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantVariableFlowDesign]:
        """All ``ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design`` objects in the document."""
    @property
    def zone_hvac_low_temperature_radiant_variable_flows(
        self,
    ) -> IDFCollection[ZoneHVACLowTemperatureRadiantVariableFlow]:
        """All ``ZoneHVAC:LowTemperatureRadiant:VariableFlow`` objects in the document. Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water flow to the unit."""
    @property
    def zone_hvac_outdoor_air_unit_equipment_lists(self) -> IDFCollection[ZoneHVACOutdoorAirUnitEquipmentList]:
        """All ``ZoneHVAC:OutdoorAirUnit:EquipmentList`` objects in the document. Equipment list for components in a ZoneHVAC:OutdoorAirUnit. Components are simulated sequentially in the order given in the equipment list."""
    @property
    def zone_hvac_outdoor_air_units(self) -> IDFCollection[ZoneHVACOutdoorAirUnit]:
        """All ``ZoneHVAC:OutdoorAirUnit`` objects in the document. The zone outdoor air unit models a single-zone dedicated outdoor air system (DOAS). Forced-convection 100% outdoor air unit with supply fan and optional equipment including exhaust fan, heating coi..."""
    @property
    def zone_hvac_packaged_terminal_air_conditioners(self) -> IDFCollection[ZoneHVACPackagedTerminalAirConditioner]:
        """All ``ZoneHVAC:PackagedTerminalAirConditioner`` objects in the document. Packaged terminal air conditioner (PTAC). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam) and fixed-pos..."""
    @property
    def zone_hvac_packaged_terminal_heat_pumps(self) -> IDFCollection[ZoneHVACPackagedTerminalHeatPump]:
        """All ``ZoneHVAC:PackagedTerminalHeatPump`` objects in the document. Packaged terminal heat pump (PTHP). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), supplemental heating coil (ga..."""
    @property
    def zone_hvac_refrigeration_chiller_sets(self) -> IDFCollection[ZoneHVACRefrigerationChillerSet]:
        """All ``ZoneHVAC:RefrigerationChillerSet`` objects in the document. Works in conjunction with one or multiple air chillers, compressor racks, refrigeration systems, or refrigeration secondary system objects to simulate the performance of a group of air chillers coo..."""
    @property
    def zone_hvac_terminal_unit_variable_refrigerant_flows(
        self,
    ) -> IDFCollection[ZoneHVACTerminalUnitVariableRefrigerantFlow]:
        """All ``ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`` objects in the document. A terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air heat pump). The VRF terminal units are served by an AirConditioner:VariableRefrigerantFlow or AirCondit..."""
    @property
    def zone_hvac_unit_heaters(self) -> IDFCollection[ZoneHVACUnitHeater]:
        """All ``ZoneHVAC:UnitHeater`` objects in the document. Unit heater. Forced-convection heating-only unit with supply fan, heating coil (gas, electric, hot water, or steam) and fixed-position outdoor air mixer."""
    @property
    def zone_hvac_unit_ventilators(self) -> IDFCollection[ZoneHVACUnitVentilator]:
        """All ``ZoneHVAC:UnitVentilator`` objects in the document. Unit ventilator. Forced-convection ventilation unit with supply fan (constant-volume or variable-volume), optional chilled water cooling coil, optional heating coil (gas, electric, hot water, or st..."""
    @property
    def zone_hvac_ventilated_slab_slab_groups(self) -> IDFCollection[ZoneHVACVentilatedSlabSlabGroup]:
        """All ``ZoneHVAC:VentilatedSlab:SlabGroup`` objects in the document. This is used to allow the coordinate control of several ventilated slab system surfaces. Note that the flow fractions must sum up to 1.0. The number of surfaces can be expanded beyond 10, if necess..."""
    @property
    def zone_hvac_ventilated_slabs(self) -> IDFCollection[ZoneHVACVentilatedSlab]:
        """All ``ZoneHVAC:VentilatedSlab`` objects in the document. Ventilated slab system where outdoor air flows through hollow cores in a building surface (wall, ceiling, or floor)."""
    @property
    def zone_hvac_water_to_air_heat_pumps(self) -> IDFCollection[ZoneHVACWaterToAirHeatPump]:
        """All ``ZoneHVAC:WaterToAirHeatPump`` objects in the document. Water-to-air heat pump. Forced-convection heating-cooling unit with supply fan, water-to-air cooling and heating coils, supplemental heating coil (gas, electric, hot water, or steam), and fixed-pos..."""
    @property
    def zone_hvac_window_air_conditioners(self) -> IDFCollection[ZoneHVACWindowAirConditioner]:
        """All ``ZoneHVAC:WindowAirConditioner`` objects in the document. Window air conditioner. Forced-convection cooling-only unit with supply fan, direct expansion (DX) cooling coil, and fixed-position outdoor air mixer."""
    @property
    def zone_infiltration_design_flow_rates(self) -> IDFCollection[ZoneInfiltrationDesignFlowRate]:
        """All ``ZoneInfiltration:DesignFlowRate`` objects in the document. Infiltration is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Infiltration=Idesign * FSchedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D..."""
    @property
    def zone_infiltration_effective_leakage_areas(self) -> IDFCollection[ZoneInfiltrationEffectiveLeakageArea]:
        """All ``ZoneInfiltration:EffectiveLeakageArea`` objects in the document. Infiltration is specified as effective leakage area at 4 Pa, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * (AL..."""
    @property
    def zone_infiltration_flow_coefficients(self) -> IDFCollection[ZoneInfiltrationFlowCoefficient]:
        """All ``ZoneInfiltration:FlowCoefficient`` objects in the document. Infiltration is specified as flow coefficient, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * SQRT( (c * Cs*|(T..."""
    @property
    def zone_lists(self) -> IDFCollection[ZoneList]:
        """All ``ZoneList`` objects in the document. Defines a list of thermal zones which can be referenced as a group. The ZoneList name may be used elsewhere in the input to apply a parameter to all zones in the list. ZoneLists can be used effecti..."""
    @property
    def zone_mixings(self) -> IDFCollection[ZoneMixing]:
        """All ``ZoneMixing`` objects in the document. ZoneMixing is a simple air exchange from one zone or space to another. Note that this statement only affects the energy balance of the 'receiving' zone or space and will not produce any effect on t..."""
    @property
    def zone_mrt_calculations(self) -> IDFCollection[ZoneMRTCalculation]:
        """All ``ZoneMRTCalculation`` objects in the document. Blends MRT values calculated for People instances into one Zone MRT. The weighting factors must sum to a value from 0.0 through 1.0. Only one ZoneMRTCalculation object is allowed for each Zone. All..."""
    @property
    def zone_property_local_environments(self) -> IDFCollection[ZonePropertyLocalEnvironment]:
        """All ``ZoneProperty:LocalEnvironment`` objects in the document. This object defines the local environment properties of a zone object. A corresponding outdoor air node should be defined and linked to the zone object."""
    @property
    def zone_property_user_view_factors_by_surface_names(
        self,
    ) -> IDFCollection[ZonePropertyUserViewFactorsBySurfaceName]:
        """All ``ZoneProperty:UserViewFactors:BySurfaceName`` objects in the document. View factors for Surface to Surface in a zone. (Number of Surfaces)**2 are expected. Any omitted surface pairs will be assumed to have a view factor of zero."""
    @property
    def zone_refrigeration_door_mixings(self) -> IDFCollection[ZoneRefrigerationDoorMixing]:
        """All ``ZoneRefrigerationDoorMixing`` objects in the document. Refrigeration Door Mixing is used for an opening between two zones (or spaces) that are at the same elevation but have different air temperatures. In this case, the mixing air flow between the two ..."""
    @property
    def zone_terminal_unit_lists(self) -> IDFCollection[ZoneTerminalUnitList]:
        """All ``ZoneTerminalUnitList`` objects in the document. List of variable refrigerant flow (VRF) terminal units served by a given VRF condensing unit. See ZoneHVAC:TerminalUnit:VariableRefrigerantFlow and AirConditioner:VariableRefrigerantFlow."""
    @property
    def zone_thermal_chimneys(self) -> IDFCollection[ZoneThermalChimney]:
        """All ``ZoneThermalChimney`` objects in the document. A thermal chimney is a vertical shaft utilizing solar radiation to enhance natural ventilation. It consists of an absorber wall, air gap and glass cover with high solar transmissivity."""
    @property
    def zone_ventilation_design_flow_rates(self) -> IDFCollection[ZoneVentilationDesignFlowRate]:
        """All ``ZoneVentilation:DesignFlowRate`` objects in the document. Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D *..."""
    @property
    def zone_ventilation_windand_stack_open_areas(self) -> IDFCollection[ZoneVentilationWindandStackOpenArea]:
        """All ``ZoneVentilation:WindandStackOpenArea`` objects in the document. This object is specified as natural ventilation driven by wind and stack effect only: Ventilation Wind = Cw * Opening Area * Schedule * WindSpd Ventilation Stack = Cd * Opening Area * Schedule * SQ..."""
    @property
    def zones(self) -> IDFCollection[Zone]:
        """All ``Zone`` objects in the document. Defines a thermal zone of the building. Every zone contains one or more Spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will ..."""
