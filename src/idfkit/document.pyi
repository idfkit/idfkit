"""Auto-generated type stub for IDFDocument (EnergyPlus 26.1.0).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs 26.1.0
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any, Generic, TypeVar

from ._compat import EppyDocumentMixin
from ._generated_types import *  # noqa: F403
from ._generated_types import _ObjectTypeMap
from .cst import DocumentCST
from .introspection import ObjectDescription
from .objects import IDFCollection, IDFObject
from .references import ReferenceGraph
from .schema import EpJSONSchema
from .simulation.config import EnergyPlusConfig

Strict = TypeVar("Strict", bound=bool, default=bool, covariant=True)

_PYTHON_TO_IDF: dict[str, str]
_IDF_TO_PYTHON: dict[str, str]

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

    def get_collection(self, obj_type: str) -> IDFCollection[IDFObject]:
        """Get collection by type name (typed for dynamic string keys)."""
    def __getattr__(self, name: str) -> IDFCollection[IDFObject]:
        """Get collection by Python-style attribute name.

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
    def __contains__(self, obj_type: str) -> bool:  # type: ignore[override]
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
        the original.  Strict mode is preserved.

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
    def zones(self) -> IDFCollection[Zone]:
        """All ``Zone`` objects in the document. Defines a thermal zone of the building. Every zone contains one or more Spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will ..."""
    @property
    def materials(self) -> IDFCollection[Material]:
        """All ``Material`` objects in the document. Regular materials described with full set of thermal properties"""
    @property
    def material_nomass(self) -> IDFCollection[MaterialNoMass]:
        """All ``Material:NoMass`` objects in the document. Regular materials properties described whose principal description is R (Thermal Resistance)"""
    @property
    def material_airgap(self) -> IDFCollection[MaterialAirGap]:
        """All ``Material:AirGap`` objects in the document. Air Space in Opaque Construction"""
    @property
    def constructions(self) -> IDFCollection[Construction]:
        """All ``Construction`` objects in the document. Start with outside layer and work your way to the inside layer Up to 10 layers total, 8 for windows Enter the material name for each layer"""
    @property
    def building_surfaces(self) -> IDFCollection[BuildingSurfaceDetailed]:
        """All ``BuildingSurface:Detailed`` objects in the document. Allows for detailed entry of building heat transfer surfaces. Does not include subsurfaces such as windows or doors."""
    @property
    def fenestration_surfaces(self) -> IDFCollection[FenestrationSurfaceDetailed]:
        """All ``FenestrationSurface:Detailed`` objects in the document. Allows for detailed entry of subsurfaces (windows, doors, glass doors, tubular daylighting devices)."""
    @property
    def internal_mass(self) -> IDFCollection[InternalMass]:
        """All ``InternalMass`` objects in the document. Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zo..."""
    @property
    def shading_surfaces(self) -> IDFCollection[ShadingSiteDetailed]:
        """All ``Shading:Site:Detailed`` objects in the document. used for shading elements such as trees these items are fixed in space and would not move with relative geometry"""
    @property
    def shading_building(self) -> IDFCollection[ShadingBuildingDetailed]:
        """All ``Shading:Building:Detailed`` objects in the document. used for shading elements such as trees, other buildings, parts of this building not being modeled these items are relative to the current building and would move with relative geometry"""
    @property
    def shading_zone(self) -> IDFCollection[ShadingZoneDetailed]:
        """All ``Shading:Zone:Detailed`` objects in the document. used For fins, overhangs, elements that shade the building, are attached to the building but are not part of the heat transfer calculations"""
    @property
    def schedules_compact(self) -> IDFCollection[ScheduleCompact]:
        """All ``Schedule:Compact`` objects in the document. Irregular object. Does not follow the usual definition for fields. Fields A3... are: Through: Date For: Applicable days (ref: Schedule:Week:Compact) Interpolate: Average/Linear/No (ref: Schedule:Da..."""
    @property
    def schedules_constant(self) -> IDFCollection[ScheduleConstant]:
        """All ``Schedule:Constant`` objects in the document. Constant hourly value for entire year."""
    @property
    def schedules_file(self) -> IDFCollection[ScheduleFile]:
        """All ``Schedule:File`` objects in the document. A Schedule:File points to a text computer file that has 8760-8784 hours of data."""
    @property
    def schedules_year(self) -> IDFCollection[ScheduleYear]:
        """All ``Schedule:Year`` objects in the document. A Schedule:Year contains from 1 to 52 week schedules"""
    @property
    def schedules_week_daily(self) -> IDFCollection[ScheduleWeekDaily]:
        """All ``Schedule:Week:Daily`` objects in the document. A Schedule:Week:Daily contains 12 Schedule:Day:Hourly objects, one for each day type."""
    @property
    def schedules_day_interval(self) -> IDFCollection[ScheduleDayInterval]:
        """All ``Schedule:Day:Interval`` objects in the document. A Schedule:Day:Interval contains a full day of values with specified end times for each value Currently, is set up to allow for 10 minute intervals for an entire day."""
    @property
    def schedules_day_hourly(self) -> IDFCollection[ScheduleDayHourly]:
        """All ``Schedule:Day:Hourly`` objects in the document. A Schedule:Day:Hourly contains 24 values for each hour of the day."""
    @property
    def schedules_day_list(self) -> IDFCollection[ScheduleDayList]:
        """All ``Schedule:Day:List`` objects in the document. Schedule:Day:List will allow the user to list 24 hours worth of values, which can be sub-hourly in nature."""
    @property
    def schedule_type_limits(self) -> IDFCollection[ScheduleTypeLimits]:
        """All ``ScheduleTypeLimits`` objects in the document. ScheduleTypeLimits specifies the data types and limits for the values contained in schedules"""
    @property
    def people(self) -> IDFCollection[People]:
        """All ``People`` objects in the document. Sets internal gains and contaminant rates for occupants in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable..."""
    @property
    def lights(self) -> IDFCollection[Lights]:
        """All ``Lights`` objects in the document. Sets internal gains for lights in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instanc..."""
    @property
    def electric_equipment(self) -> IDFCollection[ElectricEquipment]:
        """All ``ElectricEquipment`` objects in the document. Sets internal gains for electric equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and ..."""
    @property
    def gas_equipment(self) -> IDFCollection[GasEquipment]:
        """All ``GasEquipment`` objects in the document. Sets internal gains and contaminant rates for gas equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applic..."""
    @property
    def hot_water_equipment(self) -> IDFCollection[HotWaterEquipment]:
        """All ``HotWaterEquipment`` objects in the document. Sets internal gains for hot water equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and..."""
    @property
    def infiltration(self) -> IDFCollection[ZoneInfiltrationDesignFlowRate]:
        """All ``ZoneInfiltration:DesignFlowRate`` objects in the document. Infiltration is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Infiltration=Idesign * FSchedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D..."""
    @property
    def ventilation(self) -> IDFCollection[ZoneVentilationDesignFlowRate]:
        """All ``ZoneVentilation:DesignFlowRate`` objects in the document. Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D *..."""
    @property
    def thermostats(self) -> IDFCollection[ThermostatSetpointDualSetpoint]:
        """All ``ThermostatSetpoint:DualSetpoint`` objects in the document. Used for a heating and cooling thermostat with dual setpoints. The setpoints can be scheduled and varied throughout the simulation for both heating and cooling."""
    @property
    def hvac_templates(self) -> IDFCollection[HVACTemplateZoneIdealLoadsAirSystem]:
        """All ``HVACTemplate:Zone:IdealLoadsAirSystem`` objects in the document. Zone with ideal air system that meets heating or cooling loads"""
    @property
    def ideal_loads(self) -> IDFCollection[ZoneHVACIdealLoadsAirSystem]:
        """All ``ZoneHVAC:IdealLoadsAirSystem`` objects in the document. Ideal system used to calculate loads without modeling a full HVAC system. All that is required for the ideal system are zone controls, zone equipment configurations, and the ideal loads system comp..."""
    @property
    def sizing_zone(self) -> IDFCollection[SizingZone]:
        """All ``Sizing:Zone`` objects in the document. Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, hea..."""
    @property
    def sizing_system(self) -> IDFCollection[SizingSystem]:
        """All ``Sizing:System`` objects in the document. Specifies the input needed to perform sizing calculations for a central forced air system. System design air flow, heating capacity, and cooling capacity will be calculated using this input data."""
    @property
    def output_variables(self) -> IDFCollection[OutputVariable]:
        """All ``Output:Variable`` objects in the document. each Output:Variable command picks variables to be put onto the standard output file (.eso) some variables may not be reported for every simulation. a list of variables that can be reported are ava..."""
    @property
    def output_meters(self) -> IDFCollection[OutputMeter]:
        """All ``Output:Meter`` objects in the document. Each Output:Meter command picks meters to be put onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. A list of meters that can be reported a..."""
    @property
    def output_table_summary(self) -> IDFCollection[OutputTableSummaryReports]:
        """All ``Output:Table:SummaryReports`` objects in the document. This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object a..."""
    @property
    def simulation_control(self) -> IDFCollection[SimulationControl]:
        """All ``SimulationControl`` objects in the document. Note that the following 3 fields are related to the Sizing:Zone, Sizing:System, and Sizing:Plant objects. Having these fields set to Yes but no corresponding Sizing object will not cause the sizing..."""
    @property
    def run_period(self) -> IDFCollection[RunPeriod]:
        """All ``RunPeriod`` objects in the document. Specify a range of dates and other parameters for a simulation. Multiple run periods may be input, but they may not overlap."""
    @property
    def building(self) -> IDFCollection[Building]:
        """All ``Building`` objects in the document. Describes parameters that are used during the simulation of the building. There are necessary correlations between the entries for this object and some entries in the Site:WeatherStation and Site:H..."""
    @property
    def global_geometry_rules(self) -> IDFCollection[GlobalGeometryRules]:
        """All ``GlobalGeometryRules`` objects in the document. Specifies the geometric rules used to describe the input of surface vertices and daylighting reference points."""
    @property
    def site_location(self) -> IDFCollection[SiteLocation]:
        """All ``Site:Location`` objects in the document. Specifies the building's location. Only one location is allowed. Weather data file location, if it exists, will override this object."""
    @property
    def sizing_parameters(self) -> IDFCollection[SizingParameters]:
        """All ``Sizing:Parameters`` objects in the document. Specifies global heating and cooling sizing factors/ratios. These ratios are applied at the zone level to all of the zone heating and cooling loads and air flow rates. Then these new loads and air ..."""
    @property
    def timestep(self) -> IDFCollection[Timestep]:
        """All ``Timestep`` objects in the document. Specifies the 'basic' timestep for the simulation. The value entered here is also known as the Zone Timestep. This is used in the Zone Heat Balance Model calculation as the driving timestep for hea..."""
    @property
    def window_material_simple(self) -> IDFCollection[WindowMaterialSimpleGlazingSystem]:
        """All ``WindowMaterial:SimpleGlazingSystem`` objects in the document. Alternate method of describing windows This window material object is used to define an entire glazing system using simple performance parameters."""
    @property
    def window_material_glazing(self) -> IDFCollection[WindowMaterialGlazing]:
        """All ``WindowMaterial:Glazing`` objects in the document. Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method."""
    @property
    def window_material_gas(self) -> IDFCollection[WindowMaterialGas]:
        """All ``WindowMaterial:Gas`` objects in the document. Gas material properties that are used in Windows or Glass Doors"""
    @property
    def construction_window(self) -> IDFCollection[Construction]:
        """All ``Construction`` objects in the document. Start with outside layer and work your way to the inside layer Up to 10 layers total, 8 for windows Enter the material name for each layer"""
