"""CLI subcommand for TMYx weather data from climate.onebuilding.org.

Registered under ``idfkit tmy``. Provides search, download, and an
interactive map browser over the bundled station index.
"""

from __future__ import annotations

import argparse
import enum
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.error import HTTPError, URLError

from .geocode import GeocodingError, detect_location, geocode
from .index import StationIndex, default_cache_dir

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .station import WeatherStation


# ---------------------------------------------------------------------------
# Exit codes (documented contract)
# ---------------------------------------------------------------------------

EXIT_OK = 0
EXIT_NO_MATCHES = 1
EXIT_USAGE = 2
EXIT_NETWORK = 3

# Sentinel used for ``--download`` without an explicit DIR argument.
_DOWNLOAD_CACHE_SENTINEL = "__cache__"


# ---------------------------------------------------------------------------
# Typed configuration
# ---------------------------------------------------------------------------


class TmyAction(enum.Enum):
    """The action to take after filters are applied."""

    LIST = "list"
    DOWNLOAD = "download"
    BROWSE = "browse"
    REFRESH = "refresh"


@dataclass(frozen=True, slots=True)
class TmyFilters:
    """Station filter criteria assembled from CLI arguments."""

    query: str | None = None
    wmo: str | None = None
    filename: str | None = None
    near: str | None = None
    lat: float | None = None
    lon: float | None = None
    max_km: float | None = None
    country: str | None = None
    state: str | None = None
    variant: str | None = None
    nearby: bool = False

    @property
    def has_spatial(self) -> bool:
        return self.near is not None or (self.lat is not None and self.lon is not None) or self.nearby

    @property
    def has_any(self) -> bool:
        return self.nearby or any(
            v is not None
            for v in (
                self.query,
                self.wmo,
                self.filename,
                self.near,
                self.lat,
                self.country,
                self.state,
                self.variant,
            )
        )


@dataclass(frozen=True, slots=True)
class TmyOutputConfig:
    """Output and UX settings."""

    first: bool = False
    limit: int = 10
    json_output: bool = False
    quiet: bool = False


@dataclass(frozen=True, slots=True)
class TmyDownloadConfig:
    """Download target; ``None`` means no download (list mode)."""

    dir: Path | None = None
    use_cache: bool = False


@dataclass(frozen=True, slots=True)
class TmyBrowserConfig:
    """Settings for the web browser UI."""

    host: str = "127.0.0.1"
    port: int = 0
    open_browser: bool = True


@dataclass(frozen=True, slots=True)
class TmyMatch:
    """A resolved station with optional ranking metadata.

    ``score`` is populated by text search; ``distance_km`` by spatial
    search. Both may be ``None`` for exact/metadata lookups.
    """

    station: WeatherStation
    score: float | None = None
    distance_km: float | None = None
    match_field: str = ""


@dataclass(frozen=True, slots=True)
class TmyRunConfig:
    """Fully resolved configuration for a single ``idfkit tmy`` invocation."""

    action: TmyAction
    filters: TmyFilters
    output: TmyOutputConfig
    download: TmyDownloadConfig
    browser: TmyBrowserConfig
    cache_dir: Path | None = None
    errors: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Argparse registration
# ---------------------------------------------------------------------------

_EPILOG = """\
examples:
  idfkit tmy "chicago ohare"
  idfkit tmy --near "350 Fifth Ave, NYC" --max-km 25
  idfkit tmy --nearby --max-km 50 --first --download
  idfkit tmy --wmo 725300 --variant 2009-2023 --download ./weather/
  idfkit tmy "london" --first --download
  idfkit tmy --browse
  idfkit tmy --refresh

behavior:
  - TTY + multiple matches + --download  interactive picker
  - non-TTY + multiple matches + --download  error; use --first or narrow filters
  - progress  stderr   results  stdout
  - exit 0 ok / 1 no matches / 2 usage / 3 network

Data source: TMYx typical meteorological year datasets from
climate.onebuilding.org. Each ZIP ships EPW (8760 hourly values), DDY
(ASHRAE design days), and STAT (climate summary). These are synthetic
typical years, not historical measurements or live observations.
"""


def add_subparser(
    sub: argparse._SubParsersAction[argparse.ArgumentParser],  # pyright: ignore[reportPrivateUsage]
) -> None:
    """Register the ``tmy`` subcommand on the top-level CLI parser."""
    p = sub.add_parser(
        "tmy",
        help="Search and download TMYx typical meteorological year data",
        description=(
            "Search and download TMYx typical meteorological year data from "
            "climate.onebuilding.org. Each station ships EPW (8760h), DDY "
            "(ASHRAE design days), and STAT (climate summary). These are "
            "synthetic typical years, not historical measurements."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_EPILOG,
    )

    p.add_argument("query", nargs="?", metavar="QUERY", help="Free-text search query")

    p.add_argument("--wmo", metavar="WMO", help="Exact WMO station number (e.g. 725300)")
    p.add_argument("--filename", metavar="NAME", help="Exact EPW filename or stem")

    p.add_argument("--near", metavar="ADDRESS", help="Geocode address, then find nearest stations")
    p.add_argument(
        "--nearby",
        action="store_true",
        help=(
            "Auto-detect coordinates from your public IP "
            "(sent over HTTPS to ipapi.co; cached locally for 1h) "
            "and find nearest stations"
        ),
    )
    p.add_argument("--lat", type=float, metavar="LAT", help="Latitude (decimal degrees, N positive)")
    p.add_argument("--lon", type=float, metavar="LON", help="Longitude (decimal degrees, E positive)")
    p.add_argument("--max-km", dest="max_km", type=float, metavar="KM", help="Maximum distance in km")

    p.add_argument("--country", metavar="CC", help="ISO country code (e.g. USA, FRA, GBR)")
    p.add_argument("--state", metavar="ST", help="State/province code")
    p.add_argument(
        "--variant",
        metavar="STR",
        help='Substring match on dataset variant (e.g. "TMYx", "TMYx.2009-2023", "2009-2023")',
    )

    actions = p.add_mutually_exclusive_group()
    actions.add_argument(
        "-d",
        "--download",
        dest="download",
        nargs="?",
        const=_DOWNLOAD_CACHE_SENTINEL,
        default=None,
        metavar="DIR",
        help="Download the match; DIR defaults to the platform cache",
    )
    actions.add_argument("--browse", action="store_true", help="Launch the interactive web UI")
    actions.add_argument(
        "--refresh",
        action="store_true",
        help="Rebuild the station index from upstream (requires [weather] extra)",
    )

    p.add_argument("--first", action="store_true", help="Non-interactive: pick top-scored match")
    p.add_argument(
        "--limit",
        type=int,
        default=10,
        metavar="N",
        help="Maximum results when listing (default: 10)",
    )
    p.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Machine-readable JSON output (auto-enabled when piped if --first)",
    )
    p.add_argument("-q", "--quiet", action="store_true", help="Suppress progress messages on stderr")

    p.add_argument("--host", default="127.0.0.1", help="Browser bind host (default: 127.0.0.1)")
    p.add_argument("--port", type=int, default=0, metavar="N", help="Browser port (default: random free)")
    p.add_argument("--no-open", dest="no_open", action="store_true", help="Do not auto-open the web browser")

    p.add_argument(
        "--cache-dir",
        dest="cache_dir",
        default=None,
        metavar="DIR",
        help="Override the station cache directory",
    )


# ---------------------------------------------------------------------------
# Namespace → typed config
# ---------------------------------------------------------------------------


def _resolve_action(ns: argparse.Namespace) -> TmyAction:
    if bool(getattr(ns, "refresh", False)):
        return TmyAction.REFRESH
    if bool(getattr(ns, "browse", False)):
        return TmyAction.BROWSE
    if getattr(ns, "download", None) is not None:
        return TmyAction.DOWNLOAD
    return TmyAction.LIST


def _namespace_to_config(ns: argparse.Namespace) -> TmyRunConfig:
    """Translate an argparse Namespace into a validated :class:`TmyRunConfig`.

    Collected errors are attached to ``_errors`` on the returned config so
    the caller can print them and exit cleanly.
    """
    errors: list[str] = []

    filters = TmyFilters(
        query=getattr(ns, "query", None),
        wmo=getattr(ns, "wmo", None),
        filename=getattr(ns, "filename", None),
        near=getattr(ns, "near", None),
        lat=getattr(ns, "lat", None),
        lon=getattr(ns, "lon", None),
        max_km=getattr(ns, "max_km", None),
        country=getattr(ns, "country", None),
        state=getattr(ns, "state", None),
        variant=getattr(ns, "variant", None),
        nearby=bool(getattr(ns, "nearby", False)),
    )

    # Cross-flag validation
    if filters.near is not None and (filters.lat is not None or filters.lon is not None):
        errors.append("--near cannot be combined with --lat/--lon")
    if filters.nearby and filters.near is not None:
        errors.append("--nearby cannot be combined with --near")
    if filters.nearby and (filters.lat is not None or filters.lon is not None):
        errors.append("--nearby cannot be combined with --lat/--lon")
    if (filters.lat is None) != (filters.lon is None):
        errors.append("--lat and --lon must be specified together")
    if filters.max_km is not None and not filters.has_spatial:
        errors.append("--max-km requires --near, --nearby, or --lat/--lon")

    action = _resolve_action(ns)

    download_raw = getattr(ns, "download", None)
    if download_raw == _DOWNLOAD_CACHE_SENTINEL:
        download = TmyDownloadConfig(dir=None, use_cache=True)
    elif download_raw is not None:
        download = TmyDownloadConfig(dir=Path(download_raw), use_cache=False)
    else:
        download = TmyDownloadConfig()

    output = TmyOutputConfig(
        first=bool(getattr(ns, "first", False)),
        limit=int(getattr(ns, "limit", 10)),
        json_output=bool(getattr(ns, "json_output", False)),
        quiet=bool(getattr(ns, "quiet", False)),
    )

    browser = TmyBrowserConfig(
        host=str(getattr(ns, "host", "127.0.0.1")),
        port=int(getattr(ns, "port", 0)),
        open_browser=not bool(getattr(ns, "no_open", False)),
    )

    cache_dir_raw = getattr(ns, "cache_dir", None)
    cache_dir = Path(cache_dir_raw) if cache_dir_raw else None

    return TmyRunConfig(
        action=action,
        filters=filters,
        output=output,
        download=download,
        browser=browser,
        cache_dir=cache_dir,
        errors=tuple(errors),
    )


# ---------------------------------------------------------------------------
# TTY / output helpers
# ---------------------------------------------------------------------------


def _stdout_is_tty() -> bool:
    return sys.stdout.isatty()


def _stderr_is_tty() -> bool:
    return sys.stderr.isatty()


def _info(msg: str, *, quiet: bool = False) -> None:
    """Emit a progress/status line on stderr unless quiet."""
    if not quiet:
        print(msg, file=sys.stderr)


def _error(msg: str) -> None:
    """Emit an error line on stderr."""
    print(f"error: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Filter resolution
# ---------------------------------------------------------------------------


def _variant_matches(station: WeatherStation, pattern: str) -> bool:
    return pattern.lower() in station.dataset_variant.lower()


def _post_filter(matches: Sequence[TmyMatch], filters: TmyFilters) -> list[TmyMatch]:
    """Apply country/state/variant filters to already-resolved matches."""
    result: list[TmyMatch] = []
    for m in matches:
        s = m.station
        if filters.country and s.country.upper() != filters.country.upper():
            continue
        if filters.state and s.state.upper() != filters.state.upper():
            continue
        if filters.variant and not _variant_matches(s, filters.variant):
            continue
        result.append(m)
    return result


def _resolve_coords(filters: TmyFilters, *, quiet: bool) -> tuple[float, float] | None:
    """Resolve the spatial anchor from ``--nearby``, ``--near``, or ``--lat/--lon``.

    Returns ``None`` when no spatial filter is active. Raises
    :class:`GeocodingError` on geocoding / IP-detection failure.
    """
    if filters.lat is not None and filters.lon is not None:
        return filters.lat, filters.lon
    if filters.nearby:
        _info("Detecting location from IP via ipapi.co...", quiet=quiet)
        lat, lon = detect_location()
        _info(f"Detected approximate location: {lat:.4f}, {lon:.4f}", quiet=quiet)
        return lat, lon
    if filters.near is not None:
        _info(f"Geocoding '{filters.near}' via Nominatim...", quiet=quiet)
        return geocode(filters.near)
    return None


def _resolve_matches(
    index: StationIndex,
    filters: TmyFilters,
    *,
    limit: int,
    quiet: bool,
) -> list[TmyMatch]:
    """Apply filters to the index in priority order and return matches."""
    # 1. Exact WMO
    if filters.wmo is not None:
        stations = index.get_by_wmo(filters.wmo)
        matches = [TmyMatch(station=s, match_field="wmo") for s in stations]
        return _post_filter(matches, filters)

    # 2. Exact filename
    if filters.filename is not None:
        stations = index.get_by_filename(filters.filename)
        matches = [TmyMatch(station=s, match_field="filename") for s in stations]
        return _post_filter(matches, filters)

    # 3. Spatial (optionally with query as text sub-filter)
    if filters.has_spatial:
        coords = _resolve_coords(filters, quiet=quiet)
        if coords is None:  # pragma: no cover - guarded by has_spatial
            return []
        lat, lon = coords
        # Pull a generous window so post-filters can narrow it.
        spatial_limit = max(limit * 10, 50)
        spatial = index.nearest(
            lat,
            lon,
            limit=spatial_limit,
            max_distance_km=filters.max_km,
            country=filters.country,
        )
        matches = [TmyMatch(station=r.station, distance_km=r.distance_km) for r in spatial]
        if filters.query:
            q = filters.query.lower()
            matches = [m for m in matches if q in m.station.display_name.lower()]
        return _post_filter(matches, filters)

    # 4. Text search
    if filters.query:
        search_limit = max(limit * 4, 40)
        search = index.search(filters.query, limit=search_limit, country=filters.country)
        matches = [TmyMatch(station=r.station, score=r.score, match_field=r.match_field) for r in search]
        return _post_filter(matches, filters)

    # 5. Metadata-only
    if filters.country or filters.state or filters.variant:
        matches = [TmyMatch(station=s) for s in index.stations]
        return _post_filter(matches, filters)

    return []


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------


def _match_to_dict(m: TmyMatch) -> dict[str, object]:
    return {
        "station": m.station.to_dict(),
        "display_name": m.station.display_name,
        "dataset_variant": m.station.dataset_variant,
        "filename_stem": m.station.filename_stem,
        "score": m.score,
        "distance_km": m.distance_km,
        "match_field": m.match_field or None,
    }


def _format_json(matches: Sequence[TmyMatch]) -> str:
    return json.dumps([_match_to_dict(m) for m in matches], indent=2)


def _format_tsv(matches: Sequence[TmyMatch]) -> str:
    """Tab-delimited output for non-TTY piping without ``--json``."""
    lines: list[str] = ["country\tstate\tcity\twmo\tvariant\tlat\tlon\tscore\tdistance_km\turl"]
    for m in matches:
        s = m.station
        score = f"{m.score:.2f}" if m.score is not None else ""
        dist = f"{m.distance_km:.1f}" if m.distance_km is not None else ""
        lines.append(
            "\t".join([
                s.country,
                s.state,
                s.city,
                s.wmo,
                s.dataset_variant,
                f"{s.latitude:.4f}",
                f"{s.longitude:.4f}",
                score,
                dist,
                s.url,
            ])
        )
    return "\n".join(lines)


# Minimal ANSI styling — only applied when stdout is a TTY.
_ANSI_RESET = "\x1b[0m"
_ANSI_BOLD = "\x1b[1m"
_ANSI_DIM = "\x1b[2m"
_ANSI_CYAN = "\x1b[36m"
_ANSI_GREEN = "\x1b[32m"


def _style(text: str, *codes: str, enabled: bool) -> str:
    if not enabled or not codes:
        return text
    return f"{''.join(codes)}{text}{_ANSI_RESET}"


def _format_table(matches: Sequence[TmyMatch], *, color: bool) -> str:
    if not matches:
        return "No stations match the given filters."

    # Column widths
    name_w = max(len(m.station.display_name) for m in matches)
    name_w = min(max(name_w, 20), 48)
    variant_w = max(len(m.station.dataset_variant) for m in matches)
    variant_w = min(max(variant_w, 8), 20)

    has_dist = any(m.distance_km is not None for m in matches)

    lines: list[str] = []
    for i, m in enumerate(matches):
        s = m.station
        marker = "*" if i == 0 else " "
        name = s.display_name
        if len(name) > name_w:
            name = name[: name_w - 1] + "…"
        variant = s.dataset_variant
        if len(variant) > variant_w:
            variant = variant[: variant_w - 1] + "…"

        parts: list[str] = []
        parts.append(_style(marker, _ANSI_GREEN, _ANSI_BOLD, enabled=color) if i == 0 else marker)
        parts.append(_style(f"{name:<{name_w}}", _ANSI_BOLD, enabled=color))
        parts.append(_style(f"WMO {s.wmo:<7}", _ANSI_CYAN, enabled=color))
        parts.append(f"{variant:<{variant_w}}")
        if has_dist:
            dist_str = f"{m.distance_km:6.1f} km" if m.distance_km is not None else " " * 9
            parts.append(dist_str)
        lines.append(" ".join(parts))

    return "\n".join(lines)


def _spatial_anchor_bit(filters: TmyFilters) -> str | None:
    """One-line description of the spatial anchor, or ``None`` if absent."""
    if filters.near:
        return f'near="{filters.near}"'
    if filters.lat is not None and filters.lon is not None:
        return f"coords={filters.lat:.4f},{filters.lon:.4f}"
    if filters.nearby:
        return "nearby=ip"
    return None


def _format_header(filters: TmyFilters, matches: Sequence[TmyMatch], *, color: bool) -> str:
    bits: list[str] = []
    if filters.query:
        bits.append(f'query="{filters.query}"')
    if filters.wmo:
        bits.append(f"wmo={filters.wmo}")
    if filters.filename:
        bits.append(f"filename={filters.filename}")
    spatial = _spatial_anchor_bit(filters)
    if spatial is not None:
        bits.append(spatial)
    if filters.max_km is not None:
        bits.append(f"max_km={filters.max_km}")
    if filters.country:
        bits.append(f"country={filters.country}")
    if filters.state:
        bits.append(f"state={filters.state}")
    if filters.variant:
        bits.append(f"variant={filters.variant}")

    descriptor = ", ".join(bits) if bits else "all stations"
    summary = f"Found {len(matches)} match" + ("" if len(matches) == 1 else "es")
    return _style(f"{summary} — {descriptor}", _ANSI_DIM, enabled=color)


def _next_action_hint(matches: Sequence[TmyMatch], *, color: bool) -> str:
    if not matches:
        return ""
    top = matches[0].station
    cmd = f"idfkit tmy --wmo {top.wmo} --variant {top.dataset_variant} --download"
    return _style(f"\n→ {cmd}   to fetch the top match", _ANSI_DIM, enabled=color)


# ---------------------------------------------------------------------------
# Interactive picker
# ---------------------------------------------------------------------------


def _prompt_pick(matches: Sequence[TmyMatch]) -> TmyMatch | None:
    """Show an indexed list on stderr and prompt for a selection.

    Returns the chosen match, or ``None`` if the user cancels.
    """
    color = _stderr_is_tty()
    print("Multiple matches — pick one:\n", file=sys.stderr)
    for i, m in enumerate(matches, start=1):
        s = m.station
        marker = _style("*", _ANSI_GREEN, _ANSI_BOLD, enabled=color) if i == 1 else " "
        name = _style(s.display_name, _ANSI_BOLD, enabled=color)
        wmo = _style(f"WMO {s.wmo}", _ANSI_CYAN, enabled=color)
        dist = ""
        if m.distance_km is not None:
            dist = f"   {m.distance_km:.1f} km"
        print(f" [{i:>2}] {marker} {name}   {wmo}   {s.dataset_variant}{dist}", file=sys.stderr)
    print("", file=sys.stderr)

    prompt = f"Select 1-{len(matches)} [1], or 'q' to cancel: "
    try:
        raw = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("", file=sys.stderr)
        return None

    if raw.lower() in {"q", "quit", "exit"}:
        return None
    if not raw:
        return matches[0]
    try:
        idx = int(raw)
    except ValueError:
        _error(f"not a number: {raw!r}")
        return None
    if idx < 1 or idx > len(matches):
        _error(f"selection out of range: {idx}")
        return None
    return matches[idx - 1]


# ---------------------------------------------------------------------------
# Action handlers
# ---------------------------------------------------------------------------


def _run_refresh(cfg: TmyRunConfig) -> int:
    try:
        index = StationIndex.refresh(cache_dir=cfg.cache_dir)
    except ImportError as exc:
        _error(str(exc))
        return EXIT_USAGE
    except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as exc:
        _error(f"refresh failed: {exc}")
        return EXIT_NETWORK

    cache = cfg.cache_dir or default_cache_dir()
    msg = f"Refreshed index: {len(index)} station entries → {cache}/stations.json.gz"
    if cfg.output.json_output:
        print(
            json.dumps(
                {"stations": len(index), "cache_dir": str(cache), "status": "ok"},
                indent=2,
            )
        )
    else:
        print(msg)
    return EXIT_OK


def _run_browse(cfg: TmyRunConfig) -> int:
    # Imported lazily so that the main path doesn't pay the cost
    # and so that a broken browser module doesn't break search/download.
    from ._browser.server import launch_browser

    try:
        index = StationIndex.load(cache_dir=cfg.cache_dir)
    except FileNotFoundError as exc:
        _error(str(exc))
        return EXIT_USAGE

    return launch_browser(
        index=index,
        filters=cfg.filters,
        browser=cfg.browser,
        cache_dir=cfg.cache_dir,
        quiet=cfg.output.quiet,
    )


def _run_list(cfg: TmyRunConfig, matches: Sequence[TmyMatch]) -> int:
    if not matches:
        if cfg.output.json_output:
            print("[]")
        else:
            _error("no stations match the given filters")
        return EXIT_NO_MATCHES

    limited = list(matches[: cfg.output.limit])

    if cfg.output.json_output:
        print(_format_json(limited))
        return EXIT_OK

    color = _stdout_is_tty()
    if not color and not cfg.output.json_output:
        # Piped without --json → TSV (data-pipe friendly)
        print(_format_tsv(limited))
        return EXIT_OK

    # TTY: header on stderr (so stdout stays clean-ish), table on stdout, hint on stderr.
    if not cfg.output.quiet:
        print(_format_header(cfg.filters, matches, color=_stderr_is_tty()), file=sys.stderr)
    print(_format_table(limited, color=color))
    if len(matches) > cfg.output.limit and not cfg.output.quiet:
        remaining = len(matches) - cfg.output.limit
        print(
            _style(
                f"… {remaining} more match(es) hidden — raise with --limit N",
                _ANSI_DIM,
                enabled=_stderr_is_tty(),
            ),
            file=sys.stderr,
        )
    if not cfg.output.quiet:
        print(_next_action_hint(limited, color=_stderr_is_tty()), file=sys.stderr)
    return EXIT_OK


def _pick_download_station(
    cfg: TmyRunConfig,
    matches: Sequence[TmyMatch],
) -> tuple[TmyMatch | None, int | None]:
    """Choose a single match for download.

    Returns ``(match, None)`` on a successful pick, ``(None, exit_code)``
    when the caller should abort with the given code, or
    ``(None, EXIT_OK)`` for a clean user cancellation.
    """
    if len(matches) == 1 or cfg.output.first:
        return matches[0], None

    if _stdout_is_tty() and _stderr_is_tty():
        picked = _prompt_pick(matches[: cfg.output.limit])
        if picked is None:
            _info("Cancelled.", quiet=cfg.output.quiet)
            return None, EXIT_OK
        return picked, None

    # Non-TTY: refuse to pick silently.
    _error(
        f"{len(matches)} matches; non-interactive session. "
        "Use --first to pick the top match, or narrow with --wmo / --variant / --country."
    )
    preview = matches[: min(5, cfg.output.limit)]
    for m in preview:
        s = m.station
        print(f"  WMO {s.wmo}  {s.display_name}  [{s.dataset_variant}]", file=sys.stderr)
    return None, EXIT_USAGE


def _emit_download_result(
    cfg: TmyRunConfig,
    chosen: TmyMatch,
    files: object,
) -> None:
    # ``files`` is a WeatherFiles; typed loosely to avoid a runtime import on this path.
    epw = getattr(files, "epw")  # noqa: B009
    ddy = getattr(files, "ddy")  # noqa: B009
    stat = getattr(files, "stat", None)
    zip_path = getattr(files, "zip_path")  # noqa: B009

    if cfg.output.json_output:
        print(
            json.dumps(
                {
                    "station": chosen.station.to_dict(),
                    "epw": str(epw),
                    "ddy": str(ddy),
                    "stat": str(stat) if stat else None,
                    "zip": str(zip_path),
                },
                indent=2,
            )
        )
        return

    color = _stdout_is_tty()
    print(_style(f"EPW : {epw}", _ANSI_BOLD, enabled=color))
    print(f"DDY : {ddy}")
    if stat is not None:
        print(f"STAT: {stat}")
    print(_style(f"ZIP : {zip_path}", _ANSI_DIM, enabled=color))


def _run_download(cfg: TmyRunConfig, matches: Sequence[TmyMatch]) -> int:
    from .download import WeatherDownloader

    if not matches:
        _error("no stations match the given filters; nothing to download")
        return EXIT_NO_MATCHES

    chosen, exit_code = _pick_download_station(cfg, matches)
    if chosen is None:
        return exit_code if exit_code is not None else EXIT_USAGE

    if cfg.download.use_cache:
        downloader = WeatherDownloader(cache_dir=cfg.cache_dir)
        target = cfg.cache_dir or default_cache_dir()
        _info(
            f"Downloading {chosen.station.display_name} [WMO {chosen.station.wmo}] to cache...",
            quiet=cfg.output.quiet,
        )
    elif cfg.download.dir is not None:
        downloader = WeatherDownloader(cache_dir=cfg.download.dir)
        target = cfg.download.dir
        target.mkdir(parents=True, exist_ok=True)
        _info(
            f"Downloading {chosen.station.display_name} [WMO {chosen.station.wmo}] to {target}...",
            quiet=cfg.output.quiet,
        )
    else:  # pragma: no cover - download action without download config is a logic bug
        _error("internal error: download action without download config")
        return EXIT_USAGE

    try:
        files = downloader.download(chosen.station)
    except RuntimeError as exc:
        _error(f"download failed: {exc}")
        return EXIT_NETWORK

    _emit_download_result(cfg, chosen, files)
    return EXIT_OK


# ---------------------------------------------------------------------------
# Top-level entry
# ---------------------------------------------------------------------------


def run_tmy(ns: argparse.Namespace) -> int:
    """Entry point called from the top-level ``idfkit`` CLI dispatcher."""
    cfg = _namespace_to_config(ns)

    if cfg.errors:
        for msg in cfg.errors:
            _error(msg)
        return EXIT_USAGE

    if cfg.action is TmyAction.REFRESH:
        return _run_refresh(cfg)

    if cfg.action is TmyAction.BROWSE:
        return _run_browse(cfg)

    # list / download need at least one filter
    if not cfg.filters.has_any:
        _error(
            "no filters given. Provide a QUERY, --wmo, --filename, --near/--lat/--lon, "
            "or a metadata filter (--country/--state/--variant). Use --browse for interactive."
        )
        return EXIT_USAGE

    try:
        index = StationIndex.load(cache_dir=cfg.cache_dir)
    except FileNotFoundError as exc:
        _error(str(exc))
        return EXIT_USAGE

    try:
        matches = _resolve_matches(
            index,
            cfg.filters,
            limit=cfg.output.limit,
            quiet=cfg.output.quiet,
        )
    except GeocodingError as exc:
        _error(f"geocoding failed: {exc}")
        return EXIT_NETWORK

    if cfg.action is TmyAction.DOWNLOAD:
        return _run_download(cfg, matches)
    return _run_list(cfg, matches)
