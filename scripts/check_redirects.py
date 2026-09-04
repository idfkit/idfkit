#!/usr/bin/env python3
"""Confirm every previously published address still resolves after the cutover.

Implements FR-056 and SC-020, and the "Cutover and redirects" clause of
``contracts/documentation-site.md``: both retired sites stop publishing, every address they ever
published resolves on ``developers.idfkit.com``, and dead links number zero.

THE INVENTORY

``old-sitemaps/`` holds the sitemaps of both retired sites, captured while they still published
because they are unrecoverable afterwards (FR-086): 89 addresses for ``py.idfkit.com``, 28 for
``js.idfkit.com``. Read its README before touching those files. Regenerating them after the cutover
would capture the redirect-only build and make this gate vacuous.

THE MAP

``redirects/path-map.json``, whose format is stated in ``redirects/README.md``. This gate is one of
its three readers, alongside ``scripts/build_redirect_site.py``, which writes the redirect pages,
and the ``404.html`` table that same script emits for addresses no page was written for. All three
apply the same three-step resolution, so the gate cannot pass on a rule the deployment would not
follow.

Resolution, in order, for an incoming path on a retired host:

1. an exact entry in that host's ``routes``;
2. otherwise the *longest* matching prefix in ``prefix_fallbacks``, which lands on a section page
   rather than carrying the rest of the path across;
3. otherwise the host's ``fallback``.

``notes`` carries caveats and routes nothing, so this gate reads it only to print it.

TWO MODES, AND WHY BOTH

**Offline** is the default and the mode CI runs on every pull request. It resolves each captured
address through the map and confirms the target exists, either in a built site under ``site/`` or in
the captured address inventory lists. It needs no network, so it runs on a pull request opened
months before the cutover and fails the day a page the map points at is renamed or removed.

**Live** (``--live``) is run once, after the cutover. It requests each old address for real and
requires a redirect chain ending in 200 on the unified host. A 200 with no redirect is a failure
rather than a success: it means the retired site is still publishing, which FR-056 forbids more
firmly than it forbids a broken link, because a stale copy outranks the real page in search.

WHAT COUNTS AS EXISTING, OFFLINE

A target exists when a built site under ``site/`` publishes it, or when the captured inventory lists
it. Both are consulted and the report says which answered, because a stale ``site/`` would otherwise
vouch for a page that no longer has a source file, and a navigation entry vouches for a page that
has not been built yet. With neither available there is nothing to check against, and the gate
refuses to run rather than passing on an empty set.

WHAT IS CHECKED

* Every captured address has an exact ``routes`` entry. Falling through to a prefix is a working
  redirect and not a broken link, but the map claims one entry per published address, and
  ``build_redirect_site.py`` writes a page per ``routes`` entry, so an address that is not there
  gets the 404 table rather than a page of its own.
* Every target the map declares exists on the unified site: every ``routes`` value, every
  ``prefix_fallbacks`` value, and each host's ``fallback``. Declared rather than merely exercised,
  so a rule that is broken before anything uses it fails on the day it is written.
* Every captured address is on the host whose inventory it appears in.
* Every host with an inventory is declared in the map.

EXIT CODES

  0  every address in the inventory resolves to a page the unified site publishes
  1  at least one address does not, or a rule points at a page that does not exist
  2  the gate could not run: no map, an unreadable or future-versioned map, no sitemap,
     or nothing to resolve targets against

Usage:

    python scripts/check_redirects.py
    python scripts/check_redirects.py --from py.idfkit.com
    python scripts/check_redirects.py --sitemap old-sitemaps/js.idfkit.com.sitemap.xml
    python scripts/check_redirects.py --live            # once, after the cutover
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ElementTree
from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_REFUSED = 2

DEFAULT_MAP = Path("redirects") / "path-map.json"
DEFAULT_SITE_DIR = "site"
DEFAULT_INVENTORY = "old-sitemaps/developers.idfkit.com.txt"

# The captured inventory is named after the host it came from. build_redirect_site.py reads the same
# convention, and old-sitemaps/README.md is why neither file may be regenerated.
SITEMAP_DIR = "old-sitemaps"
SITEMAP_SUFFIX = ".sitemap.xml"

# The only map format this gate understands. A map that declares a later version is read by a later
# gate, so this one stops rather than guessing, which is what redirects/README.md asks of a reader.
SUPPORTED_MAP_VERSION = 1

LIVE_TIMEOUT_SECONDS = 20
MAX_DETAIL_LINES = 8

NO_MAP = (
    "no redirect map at {path}. Every previously published address has to resolve somewhere "
    "(FR-056), and nothing states where without this file. Write it, or pass --map."
)
UNREADABLE_MAP = "the redirect map at {path} is not readable JSON: {reason}"
MALFORMED_MAP = "the redirect map at {path} is malformed: {reason}"
UNSUPPORTED_VERSION = (
    "the redirect map at {path} declares map_version {found}; this gate reads version {supported} "
    "and stops rather than guessing at a format it does not know."
)
NO_SITEMAP = "no sitemap at {path}. old-sitemaps/README.md says why it must not be regenerated."
EMPTY_SITEMAP = "{path} lists no addresses, so it cannot be the captured inventory of a published site."
UNPARSEABLE_SITEMAP = "{path} is not parseable XML: {reason}"
NOTHING_TO_RESOLVE_AGAINST = (
    "offline mode has nothing to resolve targets against: no built site at {site} and no readable "
    "navigation at {config}. Run `mkdocs build`, or pass --site-dir, or pass --config."
)
NO_HOSTS_SELECTED = "no retired host selected. The map declares: {hosts}."


class Refusal(Exception):
    """The gate cannot run at all. Distinct from a gate failure."""


class Via(Enum):
    """Which of the map's three steps sent an address to its target."""

    ROUTE = "exact route"
    PREFIX = "prefix fallback"
    FALLBACK = "host fallback"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    """One line of the map: where an address or a family of addresses goes."""

    source: str
    target: str
    via: Via

    @property
    def label(self) -> str:
        table = {Via.ROUTE: "routes", Via.PREFIX: "prefix_fallbacks", Via.FALLBACK: "fallback"}[self.via]
        return f'{table}["{self.source}"]' if self.via is not Via.FALLBACK else "fallback"


@dataclass(frozen=True)
class RetiredHost:
    """The map for one retired host."""

    host: str
    fallback: str
    routes: tuple[Rule, ...]
    prefixes: tuple[Rule, ...]

    @property
    def by_path(self) -> dict[str, Rule]:
        return {rule.source: rule for rule in self.routes}

    @property
    def longest_first(self) -> tuple[Rule, ...]:
        """Prefixes most specific first, which is the order redirects/README.md specifies."""
        return tuple(sorted(self.prefixes, key=lambda rule: -len(rule.source)))

    @property
    def fallback_rule(self) -> Rule:
        return Rule(source="", target=self.fallback, via=Via.FALLBACK)

    @property
    def declared(self) -> tuple[Rule, ...]:
        """Every rule the map declares, used or not."""
        return (*self.routes, *self.prefixes, self.fallback_rule)


@dataclass(frozen=True)
class Note:
    """One entry of the map's `notes` list. Carries a caveat; routes nothing."""

    host: str
    path: str
    text: str


@dataclass(frozen=True)
class RedirectMap:
    """The whole map, as read from one file."""

    path: Path
    version: int
    unified_site: str
    hosts: tuple[RetiredHost, ...]
    notes: tuple[Note, ...]

    def host(self, name: str) -> RetiredHost | None:
        return next((entry for entry in self.hosts if entry.host == name), None)

    @property
    def host_names(self) -> tuple[str, ...]:
        return tuple(entry.host for entry in self.hosts)


@dataclass(frozen=True)
class Inventory:
    """One captured sitemap: a host, the file it came from, and every address in it."""

    host: str
    path: Path
    addresses: tuple[str, ...]


@dataclass(frozen=True)
class TargetIndex:
    """Every path the unified site publishes, and where that knowledge came from."""

    built: frozenset[str]
    navigated: frozenset[str]
    site_dir: Path | None
    config_path: Path | None

    def source_of(self, path: str) -> str | None:
        """Which source vouches for a path, or None when neither does."""
        if path in self.built:
            return "built site"
        if path in self.navigated:
            return "navigation"
        return None

    @property
    def description(self) -> str:
        parts: list[str] = []
        if self.site_dir is not None:
            parts.append(f"built site {self.site_dir} ({len(self.built)} published paths)")
        if self.config_path is not None:
            parts.append(f"inventory {self.config_path} ({len(self.navigated)} addresses)")
        return " and ".join(parts) if parts else "nothing"


@dataclass(frozen=True)
class Resolution:
    """One captured address, and what became of it."""

    host: str
    address: str
    old_path: str
    rule: Rule
    exists_in: str | None

    @property
    def target(self) -> str:
        return self.rule.target

    @property
    def via(self) -> Via:
        return self.rule.via

    @property
    def resolved(self) -> bool:
        return self.exists_in is not None


@dataclass(frozen=True)
class LiveResult:
    """One old address, requested for real."""

    address: str
    status: int | None
    chain: tuple[str, ...]
    error: str | None

    @property
    def final(self) -> str:
        return self.chain[-1] if self.chain else self.address


@dataclass(frozen=True)
class Finding:
    """One gate failure."""

    code: str
    subject: str
    message: str
    detail: tuple[str, ...] = ()

    def render(self) -> str:
        head = f"  [{self.code}] {self.subject}: {self.message}"
        if not self.detail:
            return head
        body = "\n".join(f"      {line}" for line in self.detail)
        return f"{head}\n{body}"


@dataclass
class Report:
    """Everything one run of the gate produced."""

    redirect_map: RedirectMap
    mode: str
    inventories: tuple[Inventory, ...]
    index: TargetIndex | None = None
    resolutions: tuple[Resolution, ...] = ()
    live: tuple[LiveResult, ...] = ()
    findings: list[Finding] = field(default_factory=lambda: [])
    warnings: list[str] = field(default_factory=lambda: [])

    @property
    def ok(self) -> bool:
        return not self.findings

    @property
    def total(self) -> int:
        return sum(len(inventory.addresses) for inventory in self.inventories)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------


def normalize_path(value: str) -> str:
    """Fold a URL path to the form MkDocs publishes: leading slash, trailing slash on a page."""
    path = value.split("#", 1)[0].split("?", 1)[0]
    if not path.startswith("/"):
        path = f"/{path}"
    if path.endswith("/"):
        return path
    if "." in path.rsplit("/", 1)[-1]:
        return path
    return f"{path}/"


def _nav_url(relative: str) -> str:
    """The address MkDocs publishes a docs-relative source file at, under directory URLs."""
    stem = relative.rsplit(".", 1)[0]
    if stem == "index":
        return "/"
    if stem.endswith("/index"):
        stem = stem[: -len("/index")]
    return f"/{stem}/"


# ---------------------------------------------------------------------------
# Reading the map
# ---------------------------------------------------------------------------


def _table(value: object, key: str, where: Path) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise Refusal(MALFORMED_MAP.format(path=where, reason=f"`{key}` must be an object of path to path"))
    table: dict[str, str] = {}
    for source, target in cast("dict[str, object]", value).items():
        if not isinstance(target, str):
            raise Refusal(MALFORMED_MAP.format(path=where, reason=f"`{key}.{source}` must be a string"))
        table[normalize_path(str(source))] = normalize_path(target)
    return table


def _read_host(name: str, value: object, where: Path) -> RetiredHost:
    if not isinstance(value, dict):
        raise Refusal(MALFORMED_MAP.format(path=where, reason=f"`retired_hosts.{name}` must be an object"))
    entry = cast("dict[str, object]", value)
    fallback = entry.get("fallback")
    if not isinstance(fallback, str) or not fallback:
        reason = f"`retired_hosts.{name}.fallback` is required and must be a non-empty string"
        raise Refusal(MALFORMED_MAP.format(path=where, reason=reason))
    routes = _table(entry.get("routes"), f"retired_hosts.{name}.routes", where)
    prefixes = _table(entry.get("prefix_fallbacks"), f"retired_hosts.{name}.prefix_fallbacks", where)
    return RetiredHost(
        host=name,
        fallback=normalize_path(fallback),
        routes=tuple(Rule(source=source, target=target, via=Via.ROUTE) for source, target in sorted(routes.items())),
        prefixes=tuple(
            Rule(source=source, target=target, via=Via.PREFIX) for source, target in sorted(prefixes.items())
        ),
    )


def _read_notes(value: object) -> tuple[Note, ...]:
    if not isinstance(value, list):
        return ()
    notes: list[Note] = []
    for item in cast("list[object]", value):
        if not isinstance(item, dict):
            continue
        entry = cast("dict[str, object]", item)
        notes.append(
            Note(
                host=str(entry.get("host", "")),
                path=str(entry.get("path", "")),
                text=str(entry.get("note", "")),
            )
        )
    return tuple(notes)


def read_map(map_path: Path) -> RedirectMap:
    """Read redirects/path-map.json, or refuse to run."""
    if not map_path.is_file():
        raise Refusal(NO_MAP.format(path=map_path))
    try:
        loaded: object = json.loads(map_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Refusal(UNREADABLE_MAP.format(path=map_path, reason=exc)) from exc
    if not isinstance(loaded, dict):
        raise Refusal(MALFORMED_MAP.format(path=map_path, reason="the map must be a JSON object"))
    document = cast("dict[str, object]", loaded)

    version = document.get("map_version")
    if version != SUPPORTED_MAP_VERSION:
        raise Refusal(UNSUPPORTED_VERSION.format(path=map_path, found=version, supported=SUPPORTED_MAP_VERSION))
    unified = document.get("unified_site")
    if not isinstance(unified, str) or not unified:
        raise Refusal(MALFORMED_MAP.format(path=map_path, reason="`unified_site` is required"))
    raw_hosts = document.get("retired_hosts")
    if not isinstance(raw_hosts, dict) or not raw_hosts:
        raise Refusal(MALFORMED_MAP.format(path=map_path, reason="`retired_hosts` must name at least one host"))

    hosts = tuple(
        _read_host(str(name), value, map_path) for name, value in sorted(cast("dict[str, object]", raw_hosts).items())
    )
    return RedirectMap(
        path=map_path,
        version=SUPPORTED_MAP_VERSION,
        unified_site=unified.rstrip("/"),
        hosts=hosts,
        notes=_read_notes(document.get("notes")),
    )


# ---------------------------------------------------------------------------
# Reading the inventory
# ---------------------------------------------------------------------------


def read_sitemap(path: Path) -> tuple[str, ...]:
    """Every ``<loc>`` in one captured sitemap, in file order."""
    if not path.is_file():
        raise Refusal(NO_SITEMAP.format(path=path))
    try:
        # A committed file from old-sitemaps/, never a network fetch: the input is under review.
        root = ElementTree.fromstring(path.read_text(encoding="utf-8"))  # noqa: S314
    except ElementTree.ParseError as exc:
        raise Refusal(UNPARSEABLE_SITEMAP.format(path=path, reason=exc)) from exc
    found = [element.text.strip() for element in root.iter() if element.tag.endswith("loc") and element.text]
    if not found:
        raise Refusal(EMPTY_SITEMAP.format(path=path))
    return tuple(found)


def _majority_host(addresses: Sequence[str]) -> str:
    """The host a sitemap is the inventory of, taken from its first address."""
    return urlsplit(addresses[0]).netloc


def gather_inventories(
    redirect_map: RedirectMap, package_root: Path, hosts: Sequence[str], sitemaps: Sequence[Path]
) -> tuple[Inventory, ...]:
    """The captured sitemaps this run covers: the ones named, or one per host in the map."""
    if sitemaps:
        return tuple(
            Inventory(host=_majority_host(addresses), path=path, addresses=addresses)
            for path, addresses in ((path, read_sitemap(path)) for path in sitemaps)
        )
    selected = [entry.host for entry in redirect_map.hosts if not hosts or entry.host in hosts]
    if not selected:
        raise Refusal(NO_HOSTS_SELECTED.format(hosts=", ".join(redirect_map.host_names)))
    gathered: list[Inventory] = []
    for host in selected:
        path = package_root / SITEMAP_DIR / f"{host}{SITEMAP_SUFFIX}"
        gathered.append(Inventory(host=host, path=path, addresses=read_sitemap(path)))
    return tuple(gathered)


# ---------------------------------------------------------------------------
# What the unified site publishes
# ---------------------------------------------------------------------------


def built_paths(site_dir: Path) -> frozenset[str]:
    """Every address a built MkDocs site under ``site/`` serves."""
    found: set[str] = set()
    for html in site_dir.rglob("*.html"):
        relative = html.relative_to(site_dir).as_posix()
        if relative == "index.html":
            found.add("/")
        elif relative.endswith("/index.html"):
            found.add(f"/{relative[: -len('index.html')]}")
        else:
            found.add(f"/{relative}")
    return frozenset(found)


def navigated_paths(inventory_path: Path) -> frozenset[str]:
    """Every address the unified site serves, read from the inventory captured before the move.

    This used to parse the navigation out of mkdocs.yml through check_page_kinds. Feature 003
    moved both of those to idfkit/idfkit-developers, so neither is here to read, and this file
    stayed because it answers for the retired host rather than for the site.

    The inventory is a better authority than the navigation ever was. A navigation tree lists what
    the site MEANS to publish; old-sitemaps/developers.idfkit.com.txt is a listing of what a build
    actually produced, captured immediately before the site left this repository, which is the same
    kind of evidence as the two retired hosts' sitemaps beside it. A redirect target that resolves
    against the inventory is one a reader can actually reach.

    One line per address, as `find site -name '*.html'` emits them, relative to the site root.
    """
    found: set[str] = set()
    for line in inventory_path.read_text(encoding="utf-8").splitlines():
        relative = line.strip()
        if not relative or relative.startswith("#"):
            continue
        if relative == "index.html":
            found.add("/")
        elif relative.endswith("/index.html"):
            found.add(f"/{relative[: -len('index.html')]}")
        else:
            found.add(f"/{relative}")
    return frozenset(found)


def build_index(site_dir: Path | None, config_path: Path | None) -> TargetIndex:
    """Consult both sources, and refuse to run when neither answers."""
    built: frozenset[str] = built_paths(site_dir) if site_dir is not None and site_dir.is_dir() else frozenset()
    navigated: frozenset[str] = frozenset()
    if config_path is not None and config_path.is_file():
        try:
            navigated = navigated_paths(config_path)
        except (OSError, ValueError, Refusal):
            navigated = frozenset()
    if not built and not navigated:
        raise Refusal(NOTHING_TO_RESOLVE_AGAINST.format(site=site_dir, config=config_path))
    return TargetIndex(
        built=built,
        navigated=navigated,
        site_dir=site_dir if built else None,
        config_path=config_path if navigated else None,
    )


# ---------------------------------------------------------------------------
# Resolving
# ---------------------------------------------------------------------------


def rule_for(host: RetiredHost, old_path: str) -> Rule:
    """The map's three steps, in the order redirects/README.md states them."""
    route = host.by_path.get(old_path)
    if route is not None:
        return route
    for prefix in host.longest_first:
        if old_path.startswith(prefix.source):
            return prefix
    return host.fallback_rule


def resolve(host: RetiredHost, address: str, index: TargetIndex) -> Resolution:
    """Send one captured address through the map, and say whether it lands on a real page."""
    old_path = normalize_path(urlsplit(address).path)
    rule = rule_for(host, old_path)
    return Resolution(
        host=host.host,
        address=address,
        old_path=old_path,
        rule=rule,
        exists_in=index.source_of(rule.target),
    )


def _capped(lines: Sequence[str]) -> tuple[str, ...]:
    if len(lines) <= MAX_DETAIL_LINES:
        return tuple(lines)
    return (*lines[:MAX_DETAIL_LINES], f"... and {len(lines) - MAX_DETAIL_LINES} more")


def check_declared_targets(host: RetiredHost, index: TargetIndex) -> list[Finding]:
    """Every target the map declares exists, whether or not an address currently uses it."""
    missing: dict[str, list[Rule]] = {}
    for rule in host.declared:
        if index.source_of(rule.target) is None:
            missing.setdefault(rule.target, []).append(rule)
    return [
        Finding(
            code="route-target-missing",
            subject=f"{host.host} -> {target}",
            message=f"{len(rules)} rule(s) point at a page the unified site does not publish",
            detail=_capped([rule.label for rule in rules]),
        )
        for target, rules in sorted(missing.items())
    ]


def check_addresses(
    host: RetiredHost, inventory: Inventory, index: TargetIndex
) -> tuple[list[Resolution], list[Finding]]:
    """Every captured address has an exact route, and lands on a page that exists."""
    resolutions = [resolve(host, address, index) for address in inventory.addresses]
    unrouted = [item.old_path for item in resolutions if item.via is not Via.ROUTE]
    findings: list[Finding] = []
    if unrouted:
        findings.append(
            Finding(
                code="unrouted-address",
                subject=host.host,
                message=(
                    f"{len(unrouted)} captured address(es) have no exact `routes` entry, so the redirect "
                    "build writes no page for them and they reach the 404 table instead"
                ),
                detail=_capped(sorted(unrouted)),
            )
        )
    dead = [f"{item.old_path} -> {item.target}" for item in resolutions if not item.resolved]
    if dead:
        findings.append(
            Finding(
                code="dead-address",
                subject=host.host,
                message=f"{len(dead)} captured address(es) resolve to a page the unified site does not publish",
                detail=_capped(sorted(dead)),
            )
        )
    return resolutions, findings


def check_hosts(redirect_map: RedirectMap, inventories: Sequence[Inventory]) -> list[Finding]:
    """Every inventory belongs to a declared host, and every address in it is on that host."""
    findings: list[Finding] = []
    for inventory in inventories:
        if redirect_map.host(inventory.host) is None:
            findings.append(
                Finding(
                    code="unmapped-host",
                    subject=inventory.host,
                    message=f"has a captured inventory at {inventory.path} but no entry in the map",
                    detail=(f"the map declares: {', '.join(redirect_map.host_names)}",),
                )
            )
        stray = [address for address in inventory.addresses if urlsplit(address).netloc not in ("", inventory.host)]
        if stray:
            findings.append(
                Finding(
                    code="host-mismatch",
                    subject=str(inventory.path),
                    message=f"{len(stray)} address(es) are not on {inventory.host}",
                    detail=_capped(stray),
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Live mode
# ---------------------------------------------------------------------------


class _ChainRecorder(urllib.request.HTTPRedirectHandler):
    """A redirect handler that remembers where it was sent."""

    def __init__(self) -> None:
        super().__init__()
        self.chain: list[str] = []

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> urllib.request.Request | None:
        self.chain.append(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def request_live(address: str) -> LiveResult:
    """Request one old address for real, and record the chain it took."""
    if urlsplit(address).scheme not in ("http", "https"):
        return LiveResult(address=address, status=None, chain=(), error="not an http(s) address")
    recorder = _ChainRecorder()
    opener = urllib.request.build_opener(recorder)
    request = urllib.request.Request(address, headers={"User-Agent": "idfkit-check-redirects"})  # noqa: S310
    try:
        with opener.open(request, timeout=LIVE_TIMEOUT_SECONDS) as response:
            status = int(response.status)
    except urllib.error.HTTPError as exc:
        return LiveResult(address=address, status=int(exc.code), chain=tuple(recorder.chain), error=None)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return LiveResult(address=address, status=None, chain=tuple(recorder.chain), error=str(exc))
    return LiveResult(address=address, status=status, chain=tuple(recorder.chain), error=None)


def check_live(host: str, addresses: Sequence[str], unified_site: str) -> tuple[list[LiveResult], list[Finding]]:
    """Every old address returns a redirect chain ending in 200 on the unified host."""
    unified_host = urlsplit(unified_site).netloc
    results = [request_live(address) for address in addresses]
    findings: list[Finding] = []
    for result in results:
        if result.error is not None:
            findings.append(Finding(code="live-unreachable", subject=result.address, message=result.error))
        elif result.status != 200:
            findings.append(
                Finding(code="live-not-ok", subject=result.address, message=f"ended in {result.status}, not 200")
            )
        elif not result.chain:
            findings.append(
                Finding(
                    code="still-publishing",
                    subject=result.address,
                    message=f"returned 200 without redirecting, so {host} is still publishing (FR-056)",
                )
            )
        elif urlsplit(result.final).netloc != unified_host:
            findings.append(
                Finding(
                    code="live-off-site",
                    subject=result.address,
                    message=f"redirected to {result.final}, which is not on {unified_host}",
                )
            )
    return results, findings


# ---------------------------------------------------------------------------
# Running and reporting
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Options:
    """One run's inputs, resolved to absolute paths."""

    map_path: Path
    package_root: Path
    site_dir: Path | None
    config_path: Path | None
    hosts: tuple[str, ...]
    sitemaps: tuple[Path, ...]
    live: bool


def run(options: Options) -> Report:
    redirect_map = read_map(options.map_path)
    inventories = gather_inventories(redirect_map, options.package_root, options.hosts, options.sitemaps)
    index = None if options.live else build_index(options.site_dir, options.config_path)

    findings = check_hosts(redirect_map, inventories)
    resolutions: list[Resolution] = []
    live: list[LiveResult] = []

    for inventory in inventories:
        host = redirect_map.host(inventory.host)
        if host is None:
            continue
        if index is not None:
            findings += check_declared_targets(host, index)
            host_resolutions, host_findings = check_addresses(host, inventory, index)
            resolutions += host_resolutions
            findings += host_findings
        else:
            host_live, host_findings = check_live(host.host, inventory.addresses, redirect_map.unified_site)
            live += host_live
            findings += host_findings

    # An exact route to a different address is a page that moved, which is the whole point of the
    # map. It is worth naming, because it is where a reader's bookmark changes meaning, but it is
    # not a failure. An address with no exact route is already a finding above.
    warnings = [
        f"{item.host}{item.old_path} moved to {item.target}"
        for item in resolutions
        if item.via is Via.ROUTE and item.target != item.old_path
    ]

    return Report(
        redirect_map=redirect_map,
        mode="live" if options.live else "offline",
        inventories=inventories,
        index=index,
        resolutions=tuple(resolutions),
        live=tuple(live),
        findings=findings,
        warnings=warnings,
    )


def _via_counts(resolutions: Sequence[Resolution]) -> str:
    tally: dict[str, int] = {}
    for resolution in resolutions:
        tally[resolution.via.value] = tally.get(resolution.via.value, 0) + 1
    return ", ".join(f"{label} {count}" for label, count in sorted(tally.items()))


def _header(report: Report) -> list[str]:
    inventories = ", ".join(f"{item.host} {len(item.addresses)}" for item in report.inventories)
    lines = [
        f"Redirect map: {report.redirect_map.path} (map_version {report.redirect_map.version})",
        f"Unified site: {report.redirect_map.unified_site}",
        f"Mode:         {report.mode}",
        f"Inventory:    {report.total} previously published addresses ({inventories})",
    ]
    if report.index is not None:
        lines.append(f"Resolved against: {report.index.description}")
        lines.append(f"Resolution:   {_via_counts(report.resolutions)}")
    if report.redirect_map.notes:
        lines.append(f"Notes:        {len(report.redirect_map.notes)} recorded caveats, which route nothing")
    return lines


def render(report: Report, verbose: bool) -> str:
    lines = _header(report)

    if verbose:
        if report.resolutions:
            lines.append("")
            lines.append("Every address and where it lands:")
            lines.extend(
                f"  {item.host}{item.old_path:<44} -> {item.target}  [{item.via.value}, {item.exists_in or 'MISSING'}]"
                for item in report.resolutions
            )
        if report.redirect_map.notes:
            lines.append("")
            lines.append("Recorded caveats:")
            lines.extend(f"  {note.host}{note.path}: {note.text}" for note in report.redirect_map.notes)

    if report.warnings:
        lines.append("")
        lines.append(f"Addresses that moved rather than survived ({len(report.warnings)}):")
        lines.extend(f"  {warning}" for warning in report.warnings)

    if report.findings:
        by_code: dict[str, list[Finding]] = {}
        for finding in report.findings:
            by_code.setdefault(finding.code, []).append(finding)
        lines.append("")
        lines.append(f"FAILED: {len(report.findings)} finding(s).")
        for code in sorted(by_code):
            group = by_code[code]
            lines.append("")
            lines.append(f"{code} ({len(group)}):")
            lines.extend(finding.render() for finding in group)
    else:
        lines.append("")
        lines.append(f"OK: all {report.total} previously published addresses resolve.")

    return "\n".join(lines)


def _options(args: argparse.Namespace, package_root: Path) -> Options:
    return Options(
        map_path=Path(str(args.map)).resolve() if args.map else package_root / DEFAULT_MAP,
        package_root=package_root,
        site_dir=Path(str(args.site_dir)).resolve() if args.site_dir else package_root / DEFAULT_SITE_DIR,
        config_path=Path(str(args.inventory)).resolve() if args.inventory else package_root / DEFAULT_INVENTORY,
        hosts=tuple(str(host) for host in cast("list[Any]", args.from_host)),
        sitemaps=tuple(Path(str(path)).resolve() for path in cast("list[Any]", args.sitemap)),
        live=bool(args.live),
    )


def main(argv: Sequence[str] | None = None) -> int:
    package_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Check that every previously published address resolves after the cutover (FR-056, SC-020).",
    )
    parser.add_argument("--map", default=None, help=f"Redirect map (default: {DEFAULT_MAP.as_posix()}).")
    parser.add_argument(
        "--from",
        dest="from_host",
        action="append",
        default=[],
        metavar="HOST",
        help="Check only this retired host. Repeatable. Default: every host the map declares.",
    )
    parser.add_argument(
        "--sitemap",
        action="append",
        default=[],
        metavar="PATH",
        help=f"Check these sitemap files instead of {SITEMAP_DIR}/<host>{SITEMAP_SUFFIX}. Repeatable.",
    )
    parser.add_argument(
        "--site-dir", default=None, help=f"Built site to resolve against (default: {DEFAULT_SITE_DIR})."
    )
    parser.add_argument(
        "--inventory",
        default=None,
        help=f"Captured address inventory to resolve against (default: {DEFAULT_INVENTORY}).",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Request every old address for real. Needs the network, and is for after the cutover.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="List every address and where it lands.")
    args = parser.parse_args(argv)

    try:
        report = run(_options(args, package_root))
    except Refusal as refusal:
        print(f"check_redirects: refusing to run.\n  {refusal}", file=sys.stderr)
        return EXIT_REFUSED

    print(render(report, args.verbose))
    return EXIT_OK if report.ok else EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
