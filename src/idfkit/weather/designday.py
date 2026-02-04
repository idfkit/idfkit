"""Design day parsing and injection into EnergyPlus models.

Parses DDY files (which use standard IDF syntax) via :func:`idfkit.load_idf`
and classifies the ``SizingPeriod:DesignDay`` objects they contain into
ASHRAE design-condition categories.
"""

from __future__ import annotations

import re
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from ..versions import LATEST_VERSION

if TYPE_CHECKING:
    from ..document import IDFDocument
    from ..objects import IDFObject
    from .station import WeatherStation


class DesignDayType(Enum):
    """Classification of ASHRAE annual design day conditions.

    Values encode the condition type and annual percentile.
    """

    HEATING_99_6 = "heating_99.6"
    HEATING_99 = "heating_99"
    COOLING_DB_0_4 = "cooling_db_0.4"
    COOLING_DB_1 = "cooling_db_1"
    COOLING_DB_2 = "cooling_db_2"
    COOLING_WB_0_4 = "cooling_wb_0.4"
    COOLING_WB_1 = "cooling_wb_1"
    COOLING_WB_2 = "cooling_wb_2"
    COOLING_ENTH_0_4 = "cooling_enth_0.4"
    COOLING_ENTH_1 = "cooling_enth_1"
    COOLING_ENTH_2 = "cooling_enth_2"
    DEHUMID_0_4 = "dehumid_0.4"
    DEHUMID_1 = "dehumid_1"
    DEHUMID_2 = "dehumid_2"
    HUMIDIFICATION_99_6 = "humidif_99.6"
    HUMIDIFICATION_99 = "humidif_99"
    HTG_WIND_99_6 = "htg_wind_99.6"
    HTG_WIND_99 = "htg_wind_99"
    WIND_0_4 = "wind_0.4"
    WIND_1 = "wind_1"


# Regex patterns for classifying annual design day names.
# The names in DDY files follow ASHRAE conventions, e.g.:
#   "Chicago Ohare Intl AP Ann Htg 99.6% Condns DB"
#   "Chicago Ohare Intl AP Ann Clg .4% Condns DB=>MWB"
#   "Chicago Ohare Intl AP Ann Hum_n 99.6% Condns DP=>MCDB"
#   "Chicago Ohare Intl AP Ann Htg Wind 99.6% Condns WS=>MCDB"
#
# Monthly design days use a different naming scheme and are not classified
# into the DesignDayType enum; use the ``monthly`` property instead.
_CLASSIFY_PATTERNS: list[tuple[re.Pattern[str], DesignDayType]] = [
    # Heating dry-bulb
    (re.compile(r"Htg\s+99\.6%\s+Condns\s+DB", re.IGNORECASE), DesignDayType.HEATING_99_6),
    (re.compile(r"Htg\s+99%\s+Condns\s+DB", re.IGNORECASE), DesignDayType.HEATING_99),
    # Humidification dew-point: "Hum_n 99.6% Condns DP=>MCDB"
    (re.compile(r"Hum_n\s+99\.6%", re.IGNORECASE), DesignDayType.HUMIDIFICATION_99_6),
    (re.compile(r"Hum_n\s+99%", re.IGNORECASE), DesignDayType.HUMIDIFICATION_99),
    # Heating wind speed: "Htg Wind 99.6% Condns WS=>MCDB"
    (re.compile(r"Htg\s+Wind\s+99\.6%", re.IGNORECASE), DesignDayType.HTG_WIND_99_6),
    (re.compile(r"Htg\s+Wind\s+99%", re.IGNORECASE), DesignDayType.HTG_WIND_99),
    # Cooling dry-bulb: "Clg .4% Condns DB=>MWB" or "Clg 0.4% Condns DB=>MWB"
    (re.compile(r"Clg\s+0?\.4%\s+Condns\s+DB", re.IGNORECASE), DesignDayType.COOLING_DB_0_4),
    (re.compile(r"Clg\s+1%\s+Condns\s+DB", re.IGNORECASE), DesignDayType.COOLING_DB_1),
    (re.compile(r"Clg\s+2%\s+Condns\s+DB", re.IGNORECASE), DesignDayType.COOLING_DB_2),
    # Cooling wet-bulb: "Clg .4% Condns WB=>MDB"
    (re.compile(r"Clg\s+0?\.4%\s+Condns\s+WB", re.IGNORECASE), DesignDayType.COOLING_WB_0_4),
    (re.compile(r"Clg\s+1%\s+Condns\s+WB", re.IGNORECASE), DesignDayType.COOLING_WB_1),
    (re.compile(r"Clg\s+2%\s+Condns\s+WB", re.IGNORECASE), DesignDayType.COOLING_WB_2),
    # Cooling enthalpy: "Clg .4% Condns Enth=>MDB"
    (re.compile(r"Clg\s+0?\.4%\s+Condns\s+Enth", re.IGNORECASE), DesignDayType.COOLING_ENTH_0_4),
    (re.compile(r"Clg\s+1%\s+Condns\s+Enth", re.IGNORECASE), DesignDayType.COOLING_ENTH_1),
    (re.compile(r"Clg\s+2%\s+Condns\s+Enth", re.IGNORECASE), DesignDayType.COOLING_ENTH_2),
    # Dehumidification: "Clg .4% Condns DP=>MDB"
    (re.compile(r"Clg\s+0?\.4%\s+Condns\s+DP", re.IGNORECASE), DesignDayType.DEHUMID_0_4),
    (re.compile(r"Clg\s+1%\s+Condns\s+DP", re.IGNORECASE), DesignDayType.DEHUMID_1),
    (re.compile(r"Clg\s+2%\s+Condns\s+DP", re.IGNORECASE), DesignDayType.DEHUMID_2),
    # Wind speed (EnergyPlus-native DDY format): "Coldest Month WS/MDB 0.4%"
    (re.compile(r"Coldest\s+Month\s+WS.*0?\.4%", re.IGNORECASE), DesignDayType.WIND_0_4),
    (re.compile(r"Coldest\s+Month\s+WS.*1%", re.IGNORECASE), DesignDayType.WIND_1),
]

_MONTH_PATTERN = re.compile(
    r"(?:January|February|March|April|May|June"
    r"|July|August|September|October|November|December)"
    r"\s+\.?\d",
    re.IGNORECASE,
)


def _classify_design_day(name: str) -> DesignDayType | None:
    """Classify a design day by its ASHRAE name.

    Returns ``None`` if the name does not match any known pattern.
    """
    for pattern, dd_type in _CLASSIFY_PATTERNS:
        if pattern.search(name):
            return dd_type
    return None


class DesignDayManager:
    """Parse DDY files and inject design day conditions into IDF models.

    A DDY file is a valid IDF-syntax file containing ``Site:Location`` and
    ``SizingPeriod:DesignDay`` objects.  This class uses :func:`idfkit.load_idf`
    to parse the file and classifies each design day by its ASHRAE condition
    type.

    Args:
        ddy_path: Path to a ``.ddy`` file.
        version: EnergyPlus version to use for schema resolution.  Defaults
            to the latest supported version (design day fields are stable
            across versions).
    """

    __slots__ = ("_all_objects", "_design_days", "_doc", "_location", "_path")

    def __init__(
        self,
        ddy_path: Path | str,
        version: tuple[int, int, int] | None = None,
    ) -> None:
        from ..idf_parser import parse_idf

        self._path = Path(ddy_path)
        self._doc = parse_idf(self._path, version=version or LATEST_VERSION)
        self._design_days: dict[DesignDayType, IDFObject] = {}
        self._all_objects: list[IDFObject] = []
        self._location: IDFObject | None = None
        self._parse()

    def _parse(self) -> None:
        """Parse and classify the design days in the document."""
        # Extract Site:Location
        if "Site:Location" in self._doc:
            collection = self._doc["Site:Location"]
            if len(collection) > 0:
                self._location = next(iter(collection))

        # Store all SizingPeriod:DesignDay objects and classify annual ones
        if "SizingPeriod:DesignDay" in self._doc:
            for dd in self._doc["SizingPeriod:DesignDay"]:
                self._all_objects.append(dd)
                dd_type = _classify_design_day(dd.name)
                if dd_type is not None:
                    self._design_days[dd_type] = dd

    @classmethod
    def from_station(
        cls,
        station: WeatherStation,
        *,
        dataset: str | None = None,
        version: tuple[int, int, int] | None = None,
    ) -> DesignDayManager:
        """Download the DDY file for a station and parse it.

        Args:
            station: The weather station.
            dataset: TMYx variant to download.  Defaults to the most recent.
            version: EnergyPlus version for schema resolution.
        """
        from .download import WeatherDownloader

        # If a specific dataset is requested we need to find the matching
        # station entry (same WMO, matching URL).  For now, download whatever
        # the station's URL points to.
        _ = dataset  # reserved for future dataset selection
        downloader = WeatherDownloader()
        ddy_path = downloader.get_ddy(station)
        return cls(ddy_path, version=version)

    # --- Accessors ----------------------------------------------------------

    @property
    def all_design_days(self) -> list[IDFObject]:
        """All ``SizingPeriod:DesignDay`` objects from the DDY file."""
        return list(self._all_objects)

    @property
    def annual(self) -> list[IDFObject]:
        """All classified annual design day objects."""
        return list(self._design_days.values())

    @property
    def monthly(self) -> list[IDFObject]:
        """All monthly design day objects.

        Monthly design days follow the naming pattern
        ``{Location} {Month} {pct}% Condns {type}`` and are not classified
        into the :class:`DesignDayType` enum.
        """
        return [dd for dd in self._all_objects if _MONTH_PATTERN.search(dd.name)]

    def get(self, dd_type: DesignDayType) -> IDFObject | None:
        """Get a specific design day by type."""
        return self._design_days.get(dd_type)

    @property
    def heating(self) -> list[IDFObject]:
        """All heating design days."""
        return [dd for t, dd in self._design_days.items() if t.value.startswith("heating")]

    @property
    def cooling(self) -> list[IDFObject]:
        """All cooling dry-bulb, wet-bulb, enthalpy, and dehumidification design days."""
        return [dd for t, dd in self._design_days.items() if t.value.startswith(("cooling", "dehumid"))]

    @property
    def location(self) -> IDFObject | None:
        """The ``Site:Location`` object from the DDY file, if present."""
        return self._location

    # --- Injection ----------------------------------------------------------

    @staticmethod
    def _select_types(
        *,
        heating: str,
        cooling: str,
        include_wet_bulb: bool,
        include_enthalpy: bool,
        include_dehumidification: bool,
        include_wind: bool,
    ) -> list[DesignDayType]:
        """Build the list of design day types to inject."""
        _P = DesignDayType
        selected: list[DesignDayType] = []

        # Heating
        if heating in ("99.6%", "both"):
            selected.append(_P.HEATING_99_6)
        if heating in ("99%", "both"):
            selected.append(_P.HEATING_99)

        # Cooling dry-bulb
        _cooling_db = {"0.4%": [_P.COOLING_DB_0_4], "1%": [_P.COOLING_DB_1], "2%": [_P.COOLING_DB_2]}
        _cooling_db["all"] = [_P.COOLING_DB_0_4, _P.COOLING_DB_1, _P.COOLING_DB_2]
        selected.extend(_cooling_db.get(cooling, []))

        # Cooling wet-bulb
        if include_wet_bulb:
            _wb = {"0.4%": [_P.COOLING_WB_0_4], "1%": [_P.COOLING_WB_1], "2%": [_P.COOLING_WB_2]}
            _wb["all"] = [_P.COOLING_WB_0_4, _P.COOLING_WB_1, _P.COOLING_WB_2]
            selected.extend(_wb.get(cooling, []))

        # Cooling enthalpy
        if include_enthalpy:
            _e = {"0.4%": [_P.COOLING_ENTH_0_4], "1%": [_P.COOLING_ENTH_1], "2%": [_P.COOLING_ENTH_2]}
            _e["all"] = [_P.COOLING_ENTH_0_4, _P.COOLING_ENTH_1, _P.COOLING_ENTH_2]
            selected.extend(_e.get(cooling, []))

        # Dehumidification
        if include_dehumidification:
            _d = {"0.4%": [_P.DEHUMID_0_4], "1%": [_P.DEHUMID_1], "2%": [_P.DEHUMID_2]}
            _d["all"] = [_P.DEHUMID_0_4, _P.DEHUMID_1, _P.DEHUMID_2]
            selected.extend(_d.get(cooling, []))

        # Wind (both OneBuilding "Htg Wind" and EnergyPlus "Coldest Month WS" formats)
        if include_wind:
            selected.extend([_P.HTG_WIND_99_6, _P.HTG_WIND_99, _P.WIND_0_4, _P.WIND_1])

        return selected

    def apply_to_model(
        self,
        model: IDFDocument,
        *,
        heating: Literal["99.6%", "99%", "both"] = "99.6%",
        cooling: Literal["0.4%", "1%", "2%", "all"] = "1%",
        include_wet_bulb: bool = False,
        include_enthalpy: bool = False,
        include_dehumidification: bool = False,
        include_wind: bool = False,
        update_location: bool = True,
        replace_existing: bool = True,
    ) -> list[str]:
        """Inject design day objects into an IDF model.

        Selects the appropriate design days based on common ASHRAE sizing
        practices and adds them as ``SizingPeriod:DesignDay`` objects.

        Args:
            model: The target :class:`~idfkit.document.IDFDocument`.
            heating: Which heating percentile to include.
            cooling: Which cooling dry-bulb percentile to include.
            include_wet_bulb: Also include cooling wet-bulb design days.
            include_enthalpy: Also include cooling enthalpy design days.
            include_dehumidification: Also include dehumidification design days.
            include_wind: Also include heating wind-speed design days.
            update_location: Update the ``Site:Location`` object to match the
                DDY file metadata.
            replace_existing: Remove existing ``SizingPeriod:DesignDay`` objects
                before adding new ones.

        Returns:
            List of design day names that were added.
        """
        selected_types = self._select_types(
            heating=heating,
            cooling=cooling,
            include_wet_bulb=include_wet_bulb,
            include_enthalpy=include_enthalpy,
            include_dehumidification=include_dehumidification,
            include_wind=include_wind,
        )

        # Remove existing design days if requested
        if replace_existing and "SizingPeriod:DesignDay" in model:
            existing = list(model["SizingPeriod:DesignDay"])
            model.removeidfobjects(existing)

        # Add selected design days (as copies so the DDY document is not mutated)
        added_names: list[str] = []
        for dd_type in selected_types:
            dd = self._design_days.get(dd_type)
            if dd is not None:
                model.copyidfobject(dd)
                added_names.append(dd.name)

        # Update Site:Location if requested
        if update_location and self._location is not None:
            if "Site:Location" in model:
                existing_locs = list(model["Site:Location"])
                model.removeidfobjects(existing_locs)
            model.copyidfobject(self._location)

        return added_names

    def summary(self) -> str:
        """Human-readable summary of all design days in the DDY file."""
        monthly_count = len(self.monthly)
        lines = [f"Design days from: {self._path.name}", ""]
        if self._location:
            lines.append(f"  Location: {self._location.name}")
        lines.append(f"  Design days found: {len(self._all_objects)}")
        lines.append(f"  Annual (classified): {len(self._design_days)}")
        if monthly_count:
            lines.append(f"  Monthly: {monthly_count}")
        lines.append("")
        for dd_type, dd in sorted(self._design_days.items(), key=lambda x: x[0].value):
            lines.append(f"  [{dd_type.value}] {dd.name}")
        return "\n".join(lines)


def apply_ashrae_sizing(
    model: IDFDocument,
    station: WeatherStation,
    *,
    standard: Literal["90.1", "general"] = "general",
    version: tuple[int, int, int] | None = None,
) -> list[str]:
    """Apply standard ASHRAE sizing design days to a model.

    This is the one-line convenience function for the most common use case.

    Presets:
        - ``"90.1"``: Heating 99.6% + Cooling 1% DB + Cooling 1% WB
          (per ASHRAE Standard 90.1 requirements).
        - ``"general"``: Heating 99.6% + Cooling 0.4% DB
          (conservative general practice).

    Args:
        model: The :class:`~idfkit.document.IDFDocument` to modify.
        station: Weather station whose DDY file to use.
        standard: ASHRAE preset to apply.
        version: EnergyPlus version for schema resolution.

    Returns:
        List of design day names that were added.
    """
    ddm = DesignDayManager.from_station(station, version=version)
    if standard == "90.1":
        return ddm.apply_to_model(model, heating="99.6%", cooling="1%", include_wet_bulb=True)
    return ddm.apply_to_model(model, heating="99.6%", cooling="0.4%")
