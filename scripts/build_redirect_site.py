"""Build the redirect-only site published to a retired documentation host.

``py.idfkit.com`` and ``js.idfkit.com`` are retired by FR-056: both stop publishing and both
redirect permanently to ``developers.idfkit.com``, and no previously published deep link may
break. Both are GitHub Pages, which has no server-side rewrite, so a redirect is an HTML page:
a ``<meta http-equiv="refresh">``, a ``<link rel="canonical">`` at the new address, and a visible
sentence for a reader whose browser does not follow the refresh.

This script writes one such page per published address, from the path map at
``redirects/path-map.json``. It is the only generator: the workflow in this repository and the
one in ``idfkit-js`` both run it, so the two retired hosts cannot drift apart. It uses the
standard library only, so a runner needs no environment beyond ``python3``.

Addresses that were never published are handled too. A reader can arrive at anything, and FR-056
says an unmapped path lands on a section landing page rather than on an error, so the script also
writes a ``404.html`` that carries the host's prefix table and resolves the address in the
browser. That page is what GitHub Pages serves for every path the map does not name.

Usage::

    uv run python scripts/build_redirect_site.py --host py.idfkit.com --out site
    uv run python scripts/build_redirect_site.py --host js.idfkit.com --out site --no-verify

By default the generated pages are verified against the address inventory captured in
``old-sitemaps/`` while both sites still published (FR-086): every address in the sitemap must
have a route, or the build fails. Pass ``--sitemap`` to point elsewhere, or ``--no-verify`` to
skip the check when the inventory is not available.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn, cast

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP_PATH = REPO_ROOT / "redirects" / "path-map.json"
DEFAULT_SITEMAP_DIR = REPO_ROOT / "old-sitemaps"

SUPPORTED_MAP_VERSION = 1


def fail(message: str) -> NoReturn:
    """Report a fatal problem and stop with exit code 2."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


@dataclass(frozen=True)
class Note:
    """A caveat attached to one address in the map, carried through to the report."""

    host: str
    path: str
    note: str


@dataclass(frozen=True)
class HostMap:
    """The map for one retired host.

    ``routes`` is the exact table: every address the host published, and where it goes on the
    unified site. ``prefix_fallbacks`` catches everything else, longest prefix first, and
    ``fallback`` catches what no prefix does.
    """

    host: str
    fallback: str
    prefix_fallbacks: dict[str, str]
    routes: dict[str, str]

    def resolve(self, path: str) -> str:
        """Resolve one incoming path to its target path on the unified site.

        Exact match wins; then the longest matching prefix; then the host fallback. The result
        is a path, never ``None``: FR-056 forbids a dead end.
        """
        exact = self.routes.get(path)
        if exact is not None:
            return exact
        best_prefix = ""
        best_target = self.fallback
        for prefix, target in self.prefix_fallbacks.items():
            if path.startswith(prefix) and len(prefix) > len(best_prefix):
                best_prefix = prefix
                best_target = target
        return best_target


@dataclass(frozen=True)
class PathMap:
    """The whole map: both retired hosts, the unified site they point at, and the caveats."""

    map_version: int
    unified_site: str
    hosts: dict[str, HostMap]
    notes: tuple[Note, ...]

    def host(self, name: str) -> HostMap:
        host_map = self.hosts.get(name)
        if host_map is None:
            known = ", ".join(sorted(self.hosts)) or "none"
            fail(f"{name} is not a retired host in the map (known hosts: {known})")
        return host_map

    def notes_for(self, host: str) -> tuple[Note, ...]:
        return tuple(note for note in self.notes if note.host == host)


def _as_object(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{where} must be a JSON object")
    return cast("dict[str, Any]", value)


def _as_str_map(value: Any, where: str) -> dict[str, str]:
    obj = _as_object(value, where)
    out: dict[str, str] = {}
    for key, item in obj.items():
        if not isinstance(item, str):
            fail(f"{where}[{key!r}] must be a string")
        out[key] = item
    return out


def _require(obj: dict[str, Any], key: str, where: str) -> Any:
    if key not in obj:
        fail(f"{where} is missing the required key {key!r}")
    return obj[key]


def _require_str(obj: dict[str, Any], key: str, where: str) -> str:
    value = _require(obj, key, where)
    if not isinstance(value, str):
        fail(f"{where}.{key} must be a string")
    return value


def load_path_map(path: Path) -> PathMap:
    """Read and validate the path map. Any structural problem is fatal."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"path map not found at {path}")
    except json.JSONDecodeError as exc:
        fail(f"path map at {path} is not valid JSON: {exc}")

    doc = _as_object(raw, str(path))
    version = _require(doc, "map_version", str(path))
    if version != SUPPORTED_MAP_VERSION:
        fail(f"path map version {version!r} is not supported (this script reads {SUPPORTED_MAP_VERSION})")

    unified_site = _require_str(doc, "unified_site", str(path)).rstrip("/")

    hosts: dict[str, HostMap] = {}
    for name, value in _as_object(_require(doc, "retired_hosts", str(path)), "retired_hosts").items():
        where = f"retired_hosts[{name!r}]"
        host_obj = _as_object(value, where)
        hosts[name] = HostMap(
            host=name,
            fallback=_require_str(host_obj, "fallback", where),
            prefix_fallbacks=_as_str_map(_require(host_obj, "prefix_fallbacks", where), f"{where}.prefix_fallbacks"),
            routes=_as_str_map(_require(host_obj, "routes", where), f"{where}.routes"),
        )

    raw_notes = doc.get("notes", [])
    if not isinstance(raw_notes, list):
        fail("notes must be a JSON array")
    notes: list[Note] = []
    for index, entry in enumerate(cast("list[Any]", raw_notes)):
        where = f"notes[{index}]"
        note_obj = _as_object(entry, where)
        notes.append(
            Note(
                host=_require_str(note_obj, "host", where),
                path=_require_str(note_obj, "path", where),
                note=_require_str(note_obj, "note", where),
            )
        )

    return PathMap(map_version=SUPPORTED_MAP_VERSION, unified_site=unified_site, hosts=hosts, notes=tuple(notes))


def read_sitemap_paths(path: Path, host: str) -> list[str]:
    """Return every path the retired host published, from the captured sitemap."""
    try:
        xml = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"sitemap not found at {path}")
    locations = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    paths: list[str] = []
    for location in locations:
        marker = f"//{host}"
        if marker not in location:
            fail(f"{path} contains {location}, which is not an address of {host}")
        paths.append(location.split(marker, 1)[1] or "/")
    if not paths:
        fail(f"{path} lists no addresses")
    return paths


def redirect_page(target_url: str) -> str:
    """The HTML of one redirect page: refresh, canonical, and a sentence a human can act on."""
    escaped = html.escape(target_url, quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved to developers.idfkit.com</title>
<link rel="canonical" href="{escaped}">
<meta http-equiv="refresh" content="0; url={escaped}">
</head>
<body>
<h1>This page has moved</h1>
<p>The idfkit documentation for Python and TypeScript is now one site.
This page is at <a href="{escaped}">{escaped}</a>.</p>
<p>If your browser does not take you there, follow the link above.</p>
</body>
</html>
"""


def not_found_page(host_map: HostMap, unified_site: str) -> str:
    """The HTML of ``404.html``: resolve an unmapped address in the browser, never a dead end.

    GitHub Pages serves this file for every address the map does not name, and it is the only
    place the incoming path is known, so the prefix table travels with it. A reader without
    JavaScript still gets the unified site rather than an error.
    """
    table = {
        "site": unified_site,
        "fallback": host_map.fallback,
        "routes": host_map.routes,
        "prefixes": host_map.prefix_fallbacks,
    }
    payload = json.dumps(table, indent=2, sort_keys=True).replace("</", "<\\/")
    home = html.escape(f"{unified_site}/", quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved to developers.idfkit.com</title>
<link rel="canonical" href="{home}">
</head>
<body>
<h1>This page has moved</h1>
<p>The idfkit documentation for Python and TypeScript is now one site, at
<a href="{home}">{home}</a>. Taking you to the closest page.</p>
<noscript><p>Your browser is not running the redirect. Start from
<a href="{home}">{home}</a>.</p></noscript>
<script id="idfkit-redirect-map" type="application/json">
{payload}
</script>
<script>
(function () {{
  var element = document.getElementById('idfkit-redirect-map');
  if (!element) return;
  var map = JSON.parse(element.textContent || '{{}}');
  var path = window.location.pathname;
  if (path.charAt(path.length - 1) !== '/' && path.indexOf('.') === -1) path += '/';
  var target = map.routes[path];
  if (!target) {{
    var best = '';
    target = map.fallback;
    for (var prefix in map.prefixes) {{
      if (path.indexOf(prefix) === 0 && prefix.length > best.length) {{
        best = prefix;
        target = map.prefixes[prefix];
      }}
    }}
  }}
  window.location.replace(map.site + target + window.location.search + window.location.hash);
}})();
</script>
</body>
</html>
"""


@dataclass(frozen=True)
class BuildResult:
    """What one build wrote, for the workflow log and for the human running the cutover."""

    host: str
    pages: int
    output_dir: Path


def build(host_map: HostMap, unified_site: str, out_dir: Path) -> BuildResult:
    """Write the redirect pages, the fallback page, and the CNAME into ``out_dir``."""
    out_dir.mkdir(parents=True, exist_ok=True)

    for path, target in sorted(host_map.routes.items()):
        page_dir = out_dir / path.strip("/")
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(redirect_page(f"{unified_site}{target}"), encoding="utf-8")

    (out_dir / "404.html").write_text(not_found_page(host_map, unified_site), encoding="utf-8")
    (out_dir / "CNAME").write_text(f"{host_map.host}\n", encoding="utf-8")

    # The sentinel archive-retired-site.yml looks for. A tree carrying it is a redirect build,
    # not the last full build, and archiving it instead would be a silent loss (FR-090).
    (out_dir / "REDIRECTS_ONLY").write_text(
        f"{host_map.host} serves redirects to {unified_site} only. See redirects/README.md.\n", encoding="utf-8"
    )

    return BuildResult(host=host_map.host, pages=len(host_map.routes), output_dir=out_dir)


def verify(host_map: HostMap, sitemap_path: Path) -> tuple[str, ...]:
    """Return the published addresses the map does not name. Empty means SC-020 can hold."""
    published = read_sitemap_paths(sitemap_path, host_map.host)
    return tuple(path for path in sorted(published) if path not in host_map.routes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", required=True, help="the retired host to build, as named in the path map")
    parser.add_argument("--out", required=True, type=Path, help="directory to write the redirect site into")
    parser.add_argument("--map", dest="map_path", type=Path, default=DEFAULT_MAP_PATH, help="path map to read")
    parser.add_argument("--sitemap", type=Path, default=None, help="captured sitemap to verify coverage against")
    parser.add_argument("--no-verify", action="store_true", help="skip the sitemap coverage check")
    args = parser.parse_args(argv)

    host_name = cast("str", args.host)
    out_dir = cast("Path", args.out)
    map_path = cast("Path", args.map_path)
    sitemap_arg = cast("Path | None", args.sitemap)
    skip_verify = cast("bool", args.no_verify)

    path_map = load_path_map(map_path)
    host_map = path_map.host(host_name)

    if not skip_verify:
        sitemap_path = sitemap_arg or DEFAULT_SITEMAP_DIR / f"{host_name}.sitemap.xml"
        missing = verify(host_map, sitemap_path)
        if missing:
            listed = "\n  ".join(missing)
            fail(f"{len(missing)} published address(es) of {host_name} have no route in the map:\n  {listed}")
        print(f"verified {host_name} against {sitemap_path}: every published address has a route")

    result = build(host_map, path_map.unified_site, out_dir)
    print(f"wrote {result.pages} redirect pages plus 404.html and CNAME for {result.host} into {result.output_dir}")

    for note in path_map.notes_for(host_name):
        print(f"note: {note.host}{note.path} -> {host_map.resolve(note.path)}: {note.note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
