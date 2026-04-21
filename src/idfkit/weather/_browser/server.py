"""Stdlib HTTP server for the ``idfkit tmy --browse`` interactive map.

Endpoints:

* ``GET  /``                   index.html
* ``GET  /app.js``             client application
* ``GET  /style.css``          styles
* ``GET  /stations.json.gz``   bundled station index (content-encoded gzip)
* ``GET  /api/config``         initial filter state from CLI flags
* ``GET  /api/zip``            stream a station's ZIP to the user's browser
"""

from __future__ import annotations

import json
import logging
import sys
import threading
import webbrowser
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import parse_qs, urlparse

from ..index import (
    _BUNDLED_INDEX,  # pyright: ignore[reportPrivateUsage]
    _CACHED_INDEX,  # pyright: ignore[reportPrivateUsage]
    default_cache_dir,
)

if TYPE_CHECKING:
    from .._cli import TmyBrowserConfig, TmyFilters  # pyright: ignore[reportPrivateUsage]
    from ..index import StationIndex

logger = logging.getLogger(__name__)

_ASSETS_DIR = Path(__file__).parent / "assets"

_MIME_TYPES: dict[str, str] = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
}


# ---------------------------------------------------------------------------
# Server-side state (shared across handlers)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BrowserState:
    """Immutable server state; shared via a class attribute on the handler."""

    index: StationIndex
    filters: TmyFilters
    cache_dir: Path | None
    quiet: bool


# ---------------------------------------------------------------------------
# Handler
# ---------------------------------------------------------------------------


def _send_plain(handler: BaseHTTPRequestHandler, status: HTTPStatus, message: str) -> None:
    body = message.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/plain; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _send_json(
    handler: BaseHTTPRequestHandler,
    status: HTTPStatus,
    payload: dict[str, object],
) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _serve_asset(handler: BaseHTTPRequestHandler, name: str) -> None:
    asset_path = _ASSETS_DIR / name
    if not asset_path.is_file():
        _send_plain(handler, HTTPStatus.NOT_FOUND, f"asset not found: {name}")
        return
    body = asset_path.read_bytes()
    ctype = _MIME_TYPES.get(asset_path.suffix.lower(), "application/octet-stream")
    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", ctype)
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-cache")
    handler.end_headers()
    handler.wfile.write(body)


def _serve_stations_gz(handler: BaseHTTPRequestHandler, state: BrowserState) -> None:
    cache_source = (state.cache_dir or default_cache_dir()) / _CACHED_INDEX
    source = cache_source if cache_source.is_file() else _BUNDLED_INDEX
    if not source.is_file():
        _send_plain(handler, HTTPStatus.NOT_FOUND, "station index missing; run --refresh")
        return
    body = source.read_bytes()
    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Encoding", "gzip")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-cache")
    handler.end_headers()
    handler.wfile.write(body)


def _serve_config(handler: BaseHTTPRequestHandler, state: BrowserState) -> None:
    f = state.filters
    payload: dict[str, object] = {
        "query": f.query,
        "wmo": f.wmo,
        "filename": f.filename,
        "near": f.near,
        "lat": f.lat,
        "lon": f.lon,
        "max_km": f.max_km,
        "country": f.country,
        "state": f.state,
        "variant": f.variant,
        "cache_dir": str(state.cache_dir) if state.cache_dir else str(default_cache_dir()),
    }
    _send_json(handler, HTTPStatus.OK, payload)


def _serve_zip(handler: BaseHTTPRequestHandler, state: BrowserState) -> None:
    """Stream a station's ZIP to the client as a browser file download.

    The ZIP is fetched (or served from cache) via ``WeatherDownloader``
    server-side, then written back with ``Content-Disposition: attachment``
    so the browser saves it to the user's Downloads folder.
    """
    params = parse_qs(urlparse(handler.path).query)
    wmo = (params.get("wmo", [""])[0] or "").strip()
    filename = (params.get("filename", [""])[0] or "").strip()
    if not wmo and not filename:
        _send_plain(handler, HTTPStatus.BAD_REQUEST, "wmo or filename query parameter required")
        return

    stations = state.index.get_by_filename(filename) if filename else state.index.get_by_wmo(wmo)
    if not stations:
        _send_plain(handler, HTTPStatus.NOT_FOUND, "no station found")
        return
    station = stations[0]

    from ..download import WeatherDownloader

    downloader = WeatherDownloader(cache_dir=state.cache_dir)
    try:
        files = downloader.download(station)
    except RuntimeError as exc:
        _send_plain(handler, HTTPStatus.BAD_GATEWAY, f"fetch failed: {exc}")
        return

    zip_path = files.zip_path
    if not zip_path.is_file():  # pragma: no cover - defensive; download() creates the file
        _send_plain(handler, HTTPStatus.INTERNAL_SERVER_ERROR, "zip missing after fetch")
        return
    body = zip_path.read_bytes()

    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", "application/zip")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Content-Disposition", f'attachment; filename="{zip_path.name}"')
    handler.send_header("Cache-Control", "no-cache")
    handler.end_headers()
    handler.wfile.write(body)


_GET_ROUTES: dict[str, str] = {
    "/": "index.html",
    "/app.js": "app.js",
    "/style.css": "style.css",
}


def _make_handler(state: BrowserState) -> type[BaseHTTPRequestHandler]:
    """Build a handler class closed over shared server state."""

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            if not state.quiet:
                sys.stderr.write(f"[tmy browser] {format % args}\n")

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            asset = _GET_ROUTES.get(path)
            if asset is not None:
                _serve_asset(self, asset)
                return
            if path == "/stations.json.gz":
                _serve_stations_gz(self, state)
                return
            if path == "/api/config":
                _serve_config(self, state)
                return
            if path == "/api/zip":
                _serve_zip(self, state)
                return
            _send_plain(self, HTTPStatus.NOT_FOUND, "not found")

    return Handler


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def launch_browser(
    *,
    index: StationIndex,
    filters: TmyFilters,
    browser: TmyBrowserConfig,
    cache_dir: Path | None,
    quiet: bool,
) -> int:
    """Start the HTTP server, optionally open a browser, and block until Ctrl+C.

    Returns the process exit code suitable for ``sys.exit``.
    """
    state = BrowserState(index=index, filters=filters, cache_dir=cache_dir, quiet=quiet)
    handler_cls = _make_handler(state)

    try:
        server = ThreadingHTTPServer((browser.host, browser.port), handler_cls)
    except OSError as exc:
        print(f"error: cannot bind to {browser.host}:{browser.port}: {exc}", file=sys.stderr)
        return 2

    host, port = server.server_address[0], server.server_address[1]
    # Prefer an addressable URL when the server is bound to a wildcard.
    display_host = "localhost" if host in {"0.0.0.0", ""} else host  # noqa: S104 - just for display
    url = f"http://{display_host}:{port}/"

    if not quiet:
        print(f"[tmy browser] Serving {len(index)} stations at {url}", file=sys.stderr)
        print("[tmy browser] Press Ctrl+C to stop.", file=sys.stderr)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    if browser.open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            if not quiet:
                print(f"[tmy browser] Open {url} manually.", file=sys.stderr)

    try:
        thread.join()
    except KeyboardInterrupt:
        if not quiet:
            print("\n[tmy browser] Shutting down...", file=sys.stderr)
        server.shutdown()
        server.server_close()
        return 0
    return 0
