#!/usr/bin/env python3
"""
Gate the parity ledger against the Python public surface.

Implements the exit contract in ``contracts/parity-ledger.md`` (FR-034, FR-046 to FR-050, FR-081,
FR-084, SC-017, Constitution Principle III).

WHAT THIS GATE IS FOR

Once both packages are called ``idfkit``, an undocumented behavioural difference reads as a bug.
``idfkit-conformance/governance/parity.toml`` is what converts an absence into documentation. This
script fails the build when the ledger and the shipped Python surface disagree, so a capability
cannot land or be withdrawn without the ledger moving in the same change.

HOW THE LEDGER IS READ (FR-081, FR-084)

The ledger and the naming register are read at the governance tag pinned in
``pyproject.toml`` under ``[tool.idfkit.governance] level``, never from a default branch. A gate
that followed a branch would change its verdict without any change landing in the repository it is
gating. A copy of this package that declares no level does not get a default: the gate refuses to
run and exits 2.

For development there is an obvious local override, ``--governance-dir`` or the
``IDFKIT_GOVERNANCE_DIR`` environment variable, which reads a working tree instead of a tag. It
prints a loud banner every time, because a green run under the override is not evidence about the
pinned tag.

HOW A CAPABILITY SET IS DERIVED FROM THE PYTHON SURFACE

This is the substance of the gate, so it is stated plainly.

A *capability unit* is a public module or subpackage of ``idfkit`` that exports at least one public
name: ``idfkit`` itself, ``idfkit.geometry``, ``idfkit.weather``, and so on. Deeper modules
(``idfkit.simulation.plotting``) are not units of their own; they belong to their subpackage. The
unit is the granularity at which capabilities actually land and are withdrawn. A new capability
arrives as a new module or subpackage; adding one more helper to ``idfkit.geometry`` is not a new
capability and must not trip a parity gate.

The surface is derived statically, with ``ast``, from the ``.py`` and ``.pyi`` files under
``src/idfkit``. The generated stubs are included because they ship, and because they are the input
the naming gate takes alongside ``idfkit.__all__``. Nothing is imported, so the gate needs no
optional dependency and cannot be fooled by an import side effect. A module's exports are its
``__all__`` when it declares one, and its public top-level definitions and assignments otherwise.

A ledger capability *claims* units through two sources, which are deliberately not equal:

  1. The naming register, which is NORMATIVE. Each concept in a capability's ``names`` resolves to a
     register entry, whose ``python`` field names the Python side of that concept. Those names are
     resolved against the surface. This is the path the contract specifies: "the exported capability
     set ... mapped to ledger ids through the ``names`` field". Every presence and absence failure
     below is decided from these names alone.
  2. The ``# Python:`` provenance comment above each ``[[capability]]`` entry, which is ADVISORY. It
     is mined for identifiers and module paths that resolve on the surface; anything that does not
     resolve is prose and is dropped. These only widen a capability's claim, so they can turn a
     coverage failure into a pass but can never create one.

Resolution answers two different questions and uses two different strictnesses, which matters
enough to name. OWNERSHIP, which decides the units a capability covers, counts only module-level
exports and explicit module references. PRESENCE, which decides whether a capability still exists
at all, also counts class members and keyword arguments, because the register legitimately records
concepts whose Python name is a method (``StationIndex.search``) or an argument
(``preserve_formatting``). Letting members feed ownership would be fatal to the coverage check:
``add``, ``get``, ``remove`` and ``version`` are ambient across the package, so one capability
would claim most of the surface and an unregistered module would never be reported.

The register is coarser than the surface on purpose: it registers concepts, not every symbol. So the
coverage check asks whether a *unit* is claimed, never whether a *symbol* is registered. Whether
every public name has a register entry is the naming gate's question (FR-008), not this one.

EXIT CODES

  0  the ledger and the exported surface agree
  1  a gate failure from the exit contract in contracts/parity-ledger.md
  2  the gate refused to run: no pinned level, no readable governance source, no TOML reader

Usage:

    python scripts/check_parity_ledger.py
    python scripts/check_parity_ledger.py --conformance-repo ../idfkit-conformance
    python scripts/check_parity_ledger.py --governance-dir ../idfkit-conformance/governance
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

PACKAGE = "idfkit"
GOVERNANCE_TABLE = ("tool", "idfkit", "governance")
PARITY_RELATIVE = "governance/parity.toml"
NAMING_RELATIVE = "governance/naming.toml"

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_REFUSED = 2

TIERS = frozenset({"tier-1", "tier-2", "tier-3", "never"})
AVAILABILITY = frozenset({"complete", "partial", "absent"})
ABSENCE_KINDS = frozenset({"not-yet", "never"})

# Directories under src/idfkit that hold data or vendored content rather than public API.
EXCLUDED_PARTS = frozenset({"__pycache__", "schemas", "data", ".agents", "tests"})

_DOTTED = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")
_MODULE_PATH = re.compile(r"idfkit/[A-Za-z0-9_/]+\.py")
_COMMENT_LABEL = re.compile(r"^#\s*([A-Z][A-Za-z ]*):")
_CAPABILITY_HEADER = re.compile(r"^\[\[capability\]\]\s*$")
# The governance series is `governance-YYYY.N`. A level of any other shape is a branch name or a
# typo, and either way it is not the immutable pin FR-081 requires.
_GOVERNANCE_TAG = re.compile(r"^governance-\d{4}\.\d+$")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GovernanceSource:
    """Where the ledger and the register were read from, and whether that was the pinned tag."""

    level: str
    origin: str
    pinned: bool
    parity_text: str
    naming_text: str

    def banner(self) -> str:
        if self.pinned:
            return f"Governance level {self.level}, read from {self.origin}."
        return (
            f"LOCAL OVERRIDE: reading {self.origin} instead of the pinned tag {self.level}.\n"
            "  A green run here says nothing about the pinned tag. CI must read the tag."
        )


@dataclass(frozen=True)
class RegisterEntry:
    """One `[[entry]]` of governance/naming.toml."""

    concept: str
    python: str
    typescript: str
    kind: str


@dataclass(frozen=True)
class LedgerEntry:
    """One `[[capability]]` of governance/parity.toml, plus where it sits in the file."""

    id: str
    title: str
    tier: str
    python: str
    typescript: str
    names: tuple[str, ...]
    absence_kind: str | None
    differences: str | None
    issue: str | None
    note: str | None
    line: int
    provenance: str
    raw: dict[str, Any]

    @property
    def location(self) -> str:
        return f"{PARITY_RELATIVE}:{self.line}"


@dataclass(frozen=True)
class ModuleSurface:
    """One module of the shipped package, as read statically from its source."""

    module: str
    path: Path
    exports: frozenset[str]
    public: bool

    @property
    def is_unit(self) -> bool:
        """A capability unit: a public top-level module or subpackage that exports something."""
        return self.public and self.module.count(".") <= 1 and bool(self.exports)


@dataclass
class PublicSurface:
    """
    The statically derived Python surface, indexed for name and module lookup.

    Three indexes, consulted in order of authority. The naming register records concepts, and a
    concept's Python name is not always a module-level export: it can be a method (`StationIndex`
    `.search`), an attribute (`IDFParseError.diagnostics`), or a keyword argument
    (`preserve_formatting`). Resolving only top-level names would report those capabilities as
    withdrawn, which is the opposite of true.
    """

    modules: dict[str, ModuleSurface] = field(default_factory=lambda: {})
    symbol_modules: dict[str, set[str]] = field(default_factory=lambda: {})
    member_modules: dict[str, set[str]] = field(default_factory=lambda: {})
    parameter_modules: dict[str, set[str]] = field(default_factory=lambda: {})

    @property
    def units(self) -> dict[str, ModuleSurface]:
        return {name: surface for name, surface in self.modules.items() if surface.is_unit}

    def unit_for(self, module: str) -> str | None:
        """The capability unit a module belongs to, or None when it is outside the public surface."""
        parts = module.split(".")
        for depth in (2, 1):
            candidate = ".".join(parts[:depth])
            surface = self.modules.get(candidate)
            if surface is not None and surface.is_unit:
                return candidate
        return None

    def _units(self, index: dict[str, set[str]], name: str) -> set[str]:
        return {unit for module in index.get(name, ()) if (unit := self.unit_for(module)) is not None}

    def owns(self, name: str) -> set[str]:
        """
        The units that export *name* at module level. Claim-grade resolution.

        Deliberately narrow. Ownership decides which units a capability covers, and a method name
        is not evidence of ownership: `add`, `get`, `version` and `remove` are ambient across the
        package, so admitting members here would let one capability claim most of the surface and
        the coverage check would never fire.
        """
        return self._units(self.symbol_modules, name)

    def locates(self, name: str) -> set[str]:
        """
        The units where *name* exists at all: a module-level export, a class member, or a keyword
        argument. Presence-grade resolution, used only to answer whether a capability still exists.
        """
        for index in (self.symbol_modules, self.member_modules, self.parameter_modules):
            found = self._units(index, name)
            if found:
                return found
        return set()

    def resolve_module(self, module: str) -> set[str]:
        if module not in self.modules:
            return set()
        unit = self.unit_for(module)
        return {unit} if unit is not None else set()


@dataclass
class CapabilityClaim:
    """What one ledger capability claims of the Python surface, and how well it resolved."""

    capability_id: str
    registered_tokens: tuple[str, ...] = ()
    owned_units: set[str] = field(default_factory=lambda: set())
    resolved_tokens: set[str] = field(default_factory=lambda: set())
    located_units: set[str] = field(default_factory=lambda: set())
    unresolved_tokens: set[str] = field(default_factory=lambda: set())
    advisory_units: set[str] = field(default_factory=lambda: set())

    @property
    def claimed_units(self) -> set[str]:
        return self.owned_units | self.advisory_units

    @property
    def has_registered_python_names(self) -> bool:
        return bool(self.registered_tokens)

    @property
    def resolves_in_python(self) -> bool:
        return bool(self.resolved_tokens)


@dataclass(frozen=True)
class Finding:
    """One gate failure, in the vocabulary of the exit contract."""

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

    source: GovernanceSource
    entries: tuple[LedgerEntry, ...]
    surface: PublicSurface
    claims: dict[str, CapabilityClaim]
    findings: list[Finding] = field(default_factory=lambda: [])
    warnings: list[str] = field(default_factory=lambda: [])

    @property
    def ok(self) -> bool:
        return not self.findings


class Refusal(Exception):
    """The gate cannot run at all. Distinct from a gate failure."""


class _TomlReader(Protocol):
    def loads(self, s: str, /) -> dict[str, Any]: ...


def _toml_reader() -> _TomlReader | None:
    """tomllib on 3.11+, tomli on 3.10, None when neither is installed."""
    try:  # Python 3.11+
        import tomllib  # pyright: ignore[reportMissingTypeStubs]
    except ModuleNotFoundError:  # pragma: no cover - exercised only on 3.10
        try:
            import tomli  # pyright: ignore[reportMissingImports]
        except ModuleNotFoundError:  # pragma: no cover
            return None
        return tomli  # pyright: ignore[reportReturnType, reportUnknownVariableType]
    return tomllib


def _load_toml(text: str) -> dict[str, Any]:
    """Parse TOML with whatever reader this interpreter has, or refuse to run."""
    reader = _toml_reader()
    if reader is None:
        raise Refusal(NO_TOML_READER)
    return reader.loads(text)


# ---------------------------------------------------------------------------
# Reading the governance source at the pinned tag
# ---------------------------------------------------------------------------


UNPINNED = (
    "declares no [tool.idfkit.governance] level. FR-084 forbids a default: a gate that guesses "
    "which governance artifacts it is checking against is not a gate. Add:\n\n"
    '    [tool.idfkit.governance]\n    level = "governance-YYYY.N"\n'
)
NO_TOML_READER = (
    "no TOML reader available. Python 3.11+ provides tomllib; on 3.10 install tomli (`uv add --dev tomli`)."
)


def read_pinned_level(pyproject: Path) -> str:
    """The governance tag this package is checked against. FR-084: no default, ever."""
    if not pyproject.is_file():
        message = f"no {pyproject} to read the pinned governance level from"
        raise Refusal(message)
    node: Any = _load_toml(pyproject.read_text(encoding="utf-8"))
    for key in GOVERNANCE_TABLE:
        if not isinstance(node, dict) or key not in node:
            message = f"{pyproject} {UNPINNED}"
            raise Refusal(message)
        node = node[key]  # pyright: ignore[reportUnknownVariableType]
    if not isinstance(node, dict):
        message = f"{pyproject}: [tool.idfkit.governance] is not a table"
        raise Refusal(message)
    table: dict[str, Any] = dict(node)  # pyright: ignore[reportUnknownArgumentType]
    level = table.get("level")
    if not isinstance(level, str) or not level.strip():
        message = f"{pyproject}: [tool.idfkit.governance] level is empty. FR-084 forbids a default."
        raise Refusal(message)
    pinned = level.strip()
    if not _GOVERNANCE_TAG.match(pinned):
        message = (
            f"{pyproject}: [tool.idfkit.governance] level is {pinned!r}, which is not an immutable "
            "governance-YYYY.N tag. FR-081 forbids reading governance from a branch: a moving ref "
            "changes this gate's verdict without any change landing in the repository it gates."
        )
        raise Refusal(message)
    return pinned


def _git_show(repo: Path, ref: str, relative: str) -> str:
    # `git` from PATH with a fully argument-quoted command line: the ref comes from pyproject.toml
    # in this same checkout, and no shell is involved.
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(repo), "show", f"{ref}:{relative}"],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = (
            f"cannot read {relative} at {ref} from {repo}:\n    {result.stderr.strip()}\n"
            "  The governance tag must exist and must be fetched. In CI, check the conformance "
            "repository out at the pinned ref. Locally, use --governance-dir to read a working "
            "tree instead, and understand that this is an override."
        )
        raise Refusal(message)
    return result.stdout


def _candidate_repos(explicit: str | None, package_root: Path) -> list[Path]:
    if explicit:
        return [Path(explicit).expanduser().resolve()]
    from_env = os.environ.get("IDFKIT_CONFORMANCE_REPO")
    if from_env:
        return [Path(from_env).expanduser().resolve()]
    return [
        package_root / "conformance",  # the path the CI workflow checks the corpus out to
        package_root.parent / "idfkit-conformance",  # the sibling clone in a workspace checkout
    ]


def load_governance(
    level: str,
    package_root: Path,
    conformance_repo: str | None,
    governance_dir: str | None,
) -> GovernanceSource:
    """Read parity.toml and naming.toml, at the pinned tag unless a local override says otherwise."""
    override = governance_dir or os.environ.get("IDFKIT_GOVERNANCE_DIR")
    if override:
        directory = Path(override).expanduser().resolve()
        parity = directory / "parity.toml"
        naming = directory / "naming.toml"
        missing = [str(p) for p in (parity, naming) if not p.is_file()]
        if missing:
            message = "governance override directory is missing " + ", ".join(missing)
            raise Refusal(message)
        return GovernanceSource(
            level=level,
            origin=str(directory),
            pinned=False,
            parity_text=parity.read_text(encoding="utf-8"),
            naming_text=naming.read_text(encoding="utf-8"),
        )

    tried: list[Path] = []
    for repo in _candidate_repos(conformance_repo, package_root):
        tried.append(repo)
        if not (repo / ".git").exists():
            continue
        return GovernanceSource(
            level=level,
            origin=f"{repo} at {level}",
            pinned=True,
            parity_text=_git_show(repo, level, PARITY_RELATIVE),
            naming_text=_git_show(repo, level, NAMING_RELATIVE),
        )

    message = (
        "no idfkit-conformance checkout found. Looked at: "
        + ", ".join(str(path) for path in tried)
        + "\n  Pass --conformance-repo, set IDFKIT_CONFORMANCE_REPO, or use --governance-dir for a "
        "local working tree."
    )
    raise Refusal(message)


# ---------------------------------------------------------------------------
# Parsing the ledger and the register
# ---------------------------------------------------------------------------


def _capability_lines(text: str) -> list[int]:
    return [index + 1 for index, line in enumerate(text.splitlines()) if _CAPABILITY_HEADER.match(line)]


def _python_provenance(text: str, header_line: int) -> str:
    """The `# Python:` section of the comment block immediately above a `[[capability]]` header."""
    lines = text.splitlines()
    block: list[str] = []
    index = header_line - 2  # zero-based index of the line above the header
    while index >= 0 and lines[index].startswith("#"):
        block.append(lines[index])
        index -= 1
    block.reverse()

    collected: list[str] = []
    inside = False
    for line in block:
        stripped = line.rstrip()
        if stripped == "#":  # a blank comment line ends the labelled section
            if inside:
                break
            continue
        label = _COMMENT_LABEL.match(stripped)
        if label is not None:
            if label.group(1).strip() == "Python":
                inside = True
                collected.append(stripped.split(":", 1)[1])
                continue
            if inside:
                break
            inside = False
            continue
        if inside:
            collected.append(stripped.lstrip("#"))
    return " ".join(part.strip() for part in collected)


def _tables(value: Any, where: str) -> list[dict[str, Any]]:
    """The array-of-tables at *value*, refusing when it is missing, empty, or malformed."""
    if not isinstance(value, list) or not value:
        message = f"{where} declares no entries"
        raise Refusal(message)
    items: list[Any] = list(value)  # pyright: ignore[reportUnknownArgumentType]
    tables: list[dict[str, Any]] = []
    for position, item in enumerate(items):
        if not isinstance(item, dict):
            message = f"{where}: entry {position} is not a table"
            raise Refusal(message)
        table: dict[str, Any] = dict(item)  # pyright: ignore[reportUnknownArgumentType]
        tables.append(table)
    return tables


def _strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    items: list[Any] = list(value)  # pyright: ignore[reportUnknownArgumentType]
    return tuple(str(item) for item in items)


def _as_str(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def parse_ledger(text: str) -> tuple[LedgerEntry, ...]:
    raw_entries = _tables(_load_toml(text).get("capability"), PARITY_RELATIVE)
    lines = _capability_lines(text)
    entries: list[LedgerEntry] = []
    for position, raw in enumerate(raw_entries):
        line = lines[position] if position < len(lines) else 0
        entries.append(
            LedgerEntry(
                id=str(raw.get("id", "")).strip(),
                title=str(raw.get("title", "")).strip(),
                tier=str(raw.get("tier", "")).strip(),
                python=str(raw.get("python", "")).strip(),
                typescript=str(raw.get("typescript", "")).strip(),
                names=_strings(raw.get("names")),
                absence_kind=_as_str(raw.get("absence_kind")),
                differences=_as_str(raw.get("differences")),
                issue=_as_str(raw.get("issue")),
                note=_as_str(raw.get("note")),
                line=line,
                provenance=_python_provenance(text, line) if line else "",
                raw=raw,
            )
        )
    return tuple(entries)


def parse_register(text: str) -> dict[str, RegisterEntry]:
    raw_entries = _tables(_load_toml(text).get("entry"), NAMING_RELATIVE)
    register: dict[str, RegisterEntry] = {}
    for raw in raw_entries:
        concept = str(raw.get("concept", "")).strip()
        if not concept:
            continue
        register[concept] = RegisterEntry(
            concept=concept,
            python=str(raw.get("python", "")).strip(),
            typescript=str(raw.get("typescript", "")).strip(),
            kind=str(raw.get("kind", "")).strip(),
        )
    return register


# ---------------------------------------------------------------------------
# Deriving the Python surface, statically
# ---------------------------------------------------------------------------


def _module_name(path: Path, src_root: Path) -> str:
    relative = path.relative_to(src_root.parent)
    parts = list(relative.parts)
    if path.stem == "__init__":
        parts = parts[:-1]
    else:
        parts[-1] = path.stem
    return ".".join(parts)


def _is_public_module(module: str) -> bool:
    return all(not part.startswith("_") for part in module.split("."))


def _string_list(node: ast.AST) -> list[str]:
    if not isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return []
    return [
        element.value for element in node.elts if isinstance(element, ast.Constant) and isinstance(element.value, str)
    ]


@dataclass
class ModuleScan:
    """Everything one source file contributes to the surface indexes."""

    exports: frozenset[str] = frozenset()
    origins: dict[str, str] = field(default_factory=lambda: {})
    members: set[str] = field(default_factory=lambda: set())
    parameters: set[str] = field(default_factory=lambda: set())


def _parameters(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    args = node.args
    names = [a.arg for a in (*args.posonlyargs, *args.args, *args.kwonlyargs)]
    return {name for name in names if name not in {"self", "cls"} and not name.startswith("_")}


def _class_scan(node: ast.ClassDef) -> tuple[set[str], set[str]]:
    """The public members of a class and the parameter names of its methods."""
    members: set[str] = set()
    parameters: set[str] = set()
    for child in node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not child.name.startswith("_"):
                members.add(child.name)
            parameters |= _parameters(child)
        elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            if not child.target.id.startswith("_"):
                members.add(child.target.id)
        elif isinstance(child, ast.Assign):
            members |= {t.id for t in child.targets if isinstance(t, ast.Name) and not t.id.startswith("_")}
    return members, parameters


def _assigned_names(node: ast.Assign | ast.AnnAssign) -> set[str]:
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    return {t.id for t in targets if isinstance(t, ast.Name) and not t.id.startswith("_")}


def _import_bindings(node: ast.ImportFrom) -> dict[str, str]:
    """Names bound by one `from ... import ...`, mapped to the module they came from."""
    # Keep the leading dots: `from .geometry import set_wwr` is relative and must be resolved
    # against the importing module's package, not read as a top-level module.
    origin = "." * node.level + (node.module or "")
    return {alias.asname or alias.name: origin for alias in node.names if alias.name != "*"}


def _module_scan(tree: ast.Module) -> ModuleScan:
    """The names a module exports, where each imported name came from, its members and parameters."""
    declared: list[str] | None = None
    scan = ModuleScan()
    defined: set[str] = set()

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            scan.parameters |= _parameters(node)
            if not node.name.startswith("_"):
                defined.add(node.name)
        elif isinstance(node, ast.ClassDef):
            members, parameters = _class_scan(node)
            scan.members |= members
            scan.parameters |= parameters
            if not node.name.startswith("_"):
                defined.add(node.name)
        elif isinstance(node, ast.Assign) and _declares_all(node):
            declared = _string_list(node.value)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            defined |= _assigned_names(node)
        elif isinstance(node, ast.ImportFrom):
            bindings = _import_bindings(node)
            scan.origins.update(bindings)
            defined |= {name for name in bindings if not name.startswith("_")}

    scan.exports = frozenset(declared) if declared is not None else frozenset(defined)
    return scan


def _declares_all(node: ast.Assign) -> bool:
    return any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)


def _resolve_origin(module: str, is_package: bool, origin: str) -> str | None:
    """The absolute module an import binding came from, or None when it leaves the package."""
    if not origin:
        return None
    if not origin.startswith("."):
        return origin if origin == PACKAGE or origin.startswith(PACKAGE + ".") else None
    level = len(origin) - len(origin.lstrip("."))
    tail = origin.lstrip(".")
    base = module if is_package else module.rsplit(".", 1)[0]
    parts = base.split(".")
    if level > 1:
        parts = parts[: -(level - 1)]
    if not parts:
        return None
    absolute = ".".join(parts)
    return f"{absolute}.{tail}" if tail else absolute


def derive_surface(src_root: Path) -> PublicSurface:
    """Read every module under src/idfkit and build the capability-unit view of the surface."""
    if not src_root.is_dir():
        message = f"no package source at {src_root}"
        raise Refusal(message)

    surface = PublicSurface()
    # `.pyi` as well as `.py`: the generated stub set is part of the shipped public surface, and it
    # is the input the naming gate takes alongside `idfkit.__all__`.
    sources = sorted({*src_root.rglob("*.py"), *src_root.rglob("*.pyi")})
    for path in sources:
        relative = path.relative_to(src_root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError):  # pragma: no cover - defensive
            continue
        module = _module_name(path, src_root)
        scan = _module_scan(tree)
        # A `.pyi` alongside a `.py` describes the same module: merge rather than replace.
        existing = surface.modules.get(module)
        previous: frozenset[str] = existing.exports if existing is not None else frozenset()
        merged: frozenset[str] = scan.exports | previous
        surface.modules[module] = ModuleSurface(
            module=module,
            path=existing.path if existing is not None else path,
            exports=merged,
            public=_is_public_module(module),
        )
        is_package = path.stem == "__init__"
        for name in scan.exports:
            # Attribute a re-exported name to the module that defines it as well as to the module
            # that exports it, so `idfkit.set_wwr` counts as evidence for idfkit.geometry rather
            # than only for the package facade.
            surface.symbol_modules.setdefault(name, set()).add(module)
            defining = _resolve_origin(module, is_package, scan.origins.get(name, ""))
            if defining is not None:
                surface.symbol_modules[name].add(defining)
        for name in scan.members:
            surface.member_modules.setdefault(name, set()).add(module)
        for name in scan.parameters:
            surface.parameter_modules.setdefault(name, set()).add(module)

    return surface


# ---------------------------------------------------------------------------
# Mapping the surface onto ledger capabilities
# ---------------------------------------------------------------------------

# Identifiers that appear in the register as expression placeholders rather than as exported names.
PLACEHOLDER_HEADS = frozenset({"doc", "col", "obj", "model", "self"})


def _tokens(value: str) -> list[str]:
    """Split a register `python` value into candidate name tokens."""
    return [token.strip() for token in re.split(r"[,;]", value) if token.strip()]


def _candidates(token: str) -> tuple[list[str], list[str]]:
    """Turn one token into (module candidates, symbol candidates)."""
    module_paths = _MODULE_PATH.findall(token)
    modules = [path[: -len(".py")].replace("/", ".") for path in module_paths]

    match = _DOTTED.match(token)
    if match is None:
        return modules, []
    dotted = match.group(0)
    parts = dotted.split(".")
    if parts[0] == PACKAGE:
        modules.append(dotted)
        # `idfkit.introspection.describe_object_type` also names a symbol.
        if len(parts) > 1:
            return modules, [parts[-1]]
        return modules, []
    symbols = [parts[0]] if parts[0] not in PLACEHOLDER_HEADS else []
    if len(parts) > 1:
        symbols.append(parts[-1])
    return modules, symbols


def _advisory_units(provenance: str, surface: PublicSurface) -> set[str]:
    """Units named by the `# Python:` comment. Anything that does not resolve is prose."""
    units: set[str] = set()
    for path in _MODULE_PATH.findall(provenance):
        units |= surface.resolve_module(path[: -len(".py")].replace("/", "."))
    for dotted in _DOTTED.findall(provenance):
        parts = dotted.split(".")
        if parts[0] == PACKAGE:
            units |= surface.resolve_module(dotted)
            if len(parts) > 1:
                units |= surface.owns(parts[-1])
            continue
        if parts[0] not in PLACEHOLDER_HEADS:
            units |= surface.owns(parts[0])
        if len(parts) > 1:
            units |= surface.owns(parts[-1])
    return units


def build_claims(
    entries: Sequence[LedgerEntry],
    register: dict[str, RegisterEntry],
    surface: PublicSurface,
) -> dict[str, CapabilityClaim]:
    claims: dict[str, CapabilityClaim] = {}
    for entry in entries:
        claim = CapabilityClaim(capability_id=entry.id)
        registered: list[str] = []
        for concept in entry.names:
            register_entry = register.get(concept)
            if register_entry is None or not register_entry.python:
                continue
            for token in _tokens(register_entry.python):
                registered.append(token)
                modules, symbols = _candidates(token)
                owned: set[str] = set()
                for module in modules:
                    owned |= surface.resolve_module(module)
                for symbol in symbols:
                    owned |= surface.owns(symbol)
                claim.owned_units |= owned
                # Ownership is claim-grade and narrow; presence is a weaker question, so a token
                # that names only a method or a keyword argument still counts as present.
                located = owned or {unit for symbol in symbols for unit in surface.locates(symbol)}
                if located:
                    claim.resolved_tokens.add(token)
                    claim.located_units |= located
                else:
                    claim.unresolved_tokens.add(token)
        claim.registered_tokens = tuple(registered)
        claim.advisory_units = _advisory_units(entry.provenance, surface)
        claims[entry.id] = claim
    return claims


# ---------------------------------------------------------------------------
# The checks
# ---------------------------------------------------------------------------


def _check_required_fields(entry: LedgerEntry) -> list[Finding]:
    """Presence and enum membership of the always-required fields."""
    where = entry.location
    findings: list[Finding] = []
    if not entry.title:
        findings.append(Finding("schema", entry.id, f"no title ({where})"))
    if entry.tier not in TIERS:
        findings.append(
            Finding("schema", entry.id, f"tier is {entry.tier!r}, expected one of {sorted(TIERS)} ({where})")
        )
    for side in ("python", "typescript"):
        value: str = getattr(entry, side)
        if value not in AVAILABILITY:
            findings.append(
                Finding("schema", entry.id, f"{side} is {value!r}, expected one of {sorted(AVAILABILITY)} ({where})")
            )
    if "names" not in entry.raw:
        findings.append(Finding("schema", entry.id, f"no names field ({where})"))
    return findings


def _check_conditional_fields(entry: LedgerEntry) -> list[Finding]:
    """
    The fields whose requirement depends on the availability states.

    This is T130: `partial` must state its differences (FR-049), a deferred absence must name a
    tracking issue (FR-050), and a permanent absence must justify the permanence.
    """
    where = entry.location
    absent = "absent" in (entry.python, entry.typescript)
    partial = "partial" in (entry.python, entry.typescript)
    findings: list[Finding] = []

    if absent and entry.absence_kind is None:
        findings.append(
            Finding(
                "schema",
                entry.id,
                f"one side is absent but absence_kind is missing ({where})",
                ("FR-050: an absence is either deferred (not-yet) or permanent (never), never unstated.",),
            )
        )
    if entry.absence_kind is not None and entry.absence_kind not in ABSENCE_KINDS:
        findings.append(
            Finding("schema", entry.id, f"absence_kind is {entry.absence_kind!r}, expected not-yet or never ({where})")
        )
    if entry.absence_kind is not None and not absent:
        findings.append(Finding("schema", entry.id, f"absence_kind is set but neither side is absent ({where})"))

    # FR-049: partial without a stated difference is indistinguishable from complete.
    if partial and not entry.differences:
        findings.append(
            Finding(
                "partial-without-differences",
                entry.id,
                f"python={entry.python}, typescript={entry.typescript}, differences is empty or missing ({where})",
                (
                    "FR-049: a partial capability with no differences reads as complete, which is the",
                    "single claim this ledger exists to prevent. State what differs and why.",
                ),
            )
        )
    if entry.differences and not partial:
        findings.append(Finding("schema", entry.id, f"differences is set but neither side is partial ({where})"))

    # FR-050: a deferred absence must be tracked somewhere a reader can follow.
    problem = _issue_problem(entry.issue) if entry.absence_kind == "not-yet" else None
    if problem is not None:
        findings.append(
            Finding(
                "not-yet-without-issue",
                entry.id,
                f"absence_kind is not-yet and {problem} ({where})",
                (
                    "FR-050: a deferred absence without a tracking issue is a promise with no address.",
                    "Open the issue in idfkit-js and record its URL before the governance tag is cut.",
                ),
            )
        )

    # `never` is the permanent-versus-deferred distinction the ledger rests on: it must say why.
    if entry.absence_kind == "never" and not entry.note:
        findings.append(
            Finding(
                "never-without-note",
                entry.id,
                f"absence_kind is never and note is empty or missing ({where})",
                (
                    "A `never` entry is a permanent claim, and moving it needs a constitutional amendment.",
                    "The note is the only place the permanence is justified. Without it the entry is a",
                    "deferral wearing a permanent label.",
                ),
            )
        )
    if entry.note and entry.absence_kind != "never":
        findings.append(Finding("schema", entry.id, f"note is set but absence_kind is not never ({where})"))
    if entry.issue and entry.absence_kind != "not-yet":
        findings.append(Finding("schema", entry.id, f"issue is set but absence_kind is not not-yet ({where})"))
    return findings


def check_schema(entries: Sequence[LedgerEntry]) -> list[Finding]:
    """Field contract from contracts/parity-ledger.md, including T130's two rules."""
    findings: list[Finding] = []
    seen: dict[str, LedgerEntry] = {}

    for entry in entries:
        if not entry.id:
            findings.append(Finding("schema", entry.location, "capability has no id"))
            continue
        if entry.id in seen:
            findings.append(
                Finding(
                    "duplicate-id",
                    entry.id,
                    f"declared twice, at {seen[entry.id].location} and {entry.location}",
                )
            )
        seen[entry.id] = entry
        findings += _check_required_fields(entry)
        findings += _check_conditional_fields(entry)

    return findings


def _issue_problem(issue: str | None) -> str | None:
    """Why an `issue` value is not a tracking URL, or None when it is one."""
    if issue is None:
        return "issue is missing"
    value = issue.strip()
    if not value:
        return "issue is empty"
    if value.startswith("http://") or value.startswith("https://"):
        return None
    return f"issue is not a URL but the placeholder {value!r}"


def check_names_resolve(entries: Sequence[LedgerEntry], register: dict[str, RegisterEntry]) -> list[Finding]:
    findings: list[Finding] = []
    for entry in entries:
        for concept in entry.names:
            if concept not in register:
                findings.append(
                    Finding(
                        "unknown-concept",
                        entry.id,
                        f"names entry {concept!r} does not resolve in the naming register ({entry.location})",
                        ("Every names entry must exist as a [[entry]] concept in governance/naming.toml.",),
                    )
                )
    return findings


def check_capability_diff(
    entries: Sequence[LedgerEntry],
    claims: dict[str, CapabilityClaim],
    surface: PublicSurface,
) -> tuple[list[Finding], list[str]]:
    """The FR-048 diff: the exported capability set against what the ledger claims."""
    findings: list[Finding] = []
    warnings: list[str] = []

    claimed_units: set[str] = set()
    for entry in entries:
        claim = claims[entry.id]
        claimed_units |= claim.claimed_units

        if entry.python == "absent":
            if claim.resolves_in_python:
                findings.append(
                    Finding(
                        "capability-present-but-declared-absent",
                        entry.id,
                        "the ledger records python = absent, but its registered names are exported by "
                        + ", ".join(sorted(claim.located_units)),
                        (
                            "Resolved names: " + ", ".join(sorted(claim.resolved_tokens)),
                            "FR-048: a capability that lands updates the ledger in the same change.",
                        ),
                    )
                )
            continue

        if not claim.has_registered_python_names:
            warnings.append(
                f"{entry.id}: python = {entry.python}, but no names entry carries a Python name, so the "
                "ledger's claim about Python cannot be checked against the surface."
            )
            continue

        if not claim.resolves_in_python:
            findings.append(
                Finding(
                    "capability-removed-while-claimed",
                    entry.id,
                    f"the ledger records python = {entry.python}, but not one of its registered Python "
                    "names is exported by this package",
                    (
                        "Names looked for: " + ", ".join(sorted(claim.unresolved_tokens)),
                        "Either the capability was withdrawn and the ledger still claims it, or the",
                        "naming register points at names this package no longer exports.",
                    ),
                )
            )

    for name, unit in sorted(surface.units.items()):
        if name in claimed_units:
            continue
        sample = ", ".join(sorted(unit.exports)[:8])
        if len(unit.exports) > 8:
            sample += f", and {len(unit.exports) - 8} more"
        findings.append(
            Finding(
                "capability-added-without-entry",
                name,
                f"exports {len(unit.exports)} public name(s) and no ledger capability claims it",
                (
                    f"Exported from: {unit.path}",
                    f"Exports: {sample}",
                    "FR-048: a capability that lands updates the ledger in the same change. Either add a",
                    "[[capability]] entry whose names cover this module, or make the module private.",
                ),
            )
        )

    return findings, warnings


# ---------------------------------------------------------------------------
# Running and reporting
# ---------------------------------------------------------------------------


def run(package_root: Path, conformance_repo: str | None, governance_dir: str | None) -> Report:
    level = read_pinned_level(package_root / "pyproject.toml")
    source = load_governance(level, package_root, conformance_repo, governance_dir)
    entries = parse_ledger(source.parity_text)
    register = parse_register(source.naming_text)
    surface = derive_surface(package_root / "src" / PACKAGE)
    claims = build_claims(entries, register, surface)

    findings = check_schema(entries)
    findings += check_names_resolve(entries, register)
    diff_findings, warnings = check_capability_diff(entries, claims, surface)
    findings += diff_findings

    return Report(source=source, entries=entries, surface=surface, claims=claims, findings=findings, warnings=warnings)


def _state_counts(entries: Sequence[LedgerEntry]) -> str:
    def tally(side: str) -> str:
        counts = {state: sum(1 for e in entries if getattr(e, side) == state) for state in sorted(AVAILABILITY)}
        return ", ".join(f"{state} {count}" for state, count in counts.items())

    tiers = {tier: sum(1 for e in entries if e.tier == tier) for tier in sorted(TIERS)}
    tier_line = ", ".join(f"{tier} {count}" for tier, count in tiers.items())
    return f"  python:     {tally('python')}\n  typescript: {tally('typescript')}\n  tiers:      {tier_line}"


def render(report: Report, verbose: bool) -> str:
    lines = [report.source.banner(), ""]
    lines.append(f"Ledger: {len(report.entries)} capabilities. Surface: {len(report.surface.units)} capability units.")
    lines.append(_state_counts(report.entries))

    if verbose:
        lines.append("")
        lines.append("Capability units and the entries claiming them:")
        claimed: dict[str, list[str]] = {}
        for capability_id, claim in report.claims.items():
            for unit in claim.claimed_units:
                claimed.setdefault(unit, []).append(capability_id)
        for name in sorted(report.surface.units):
            owners = ", ".join(sorted(claimed.get(name, []))) or "UNCLAIMED"
            lines.append(f"  {name:<28} {owners}")

    if report.warnings:
        lines.append("")
        lines.append("Not checkable against the surface:")
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
        lines.append("OK: the ledger and the exported capability set agree.")

    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check governance/parity.toml against the idfkit Python public surface.",
    )
    parser.add_argument(
        "--package-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Root of the idfkit package checkout (default: the parent of this script's directory).",
    )
    parser.add_argument(
        "--conformance-repo",
        default=None,
        help=(
            "Path to an idfkit-conformance clone. The ledger is read from it at the pinned governance "
            "tag with `git show`. Defaults to ./conformance then ../idfkit-conformance, or "
            "IDFKIT_CONFORMANCE_REPO."
        ),
    )
    parser.add_argument(
        "--governance-dir",
        default=None,
        help=(
            "LOCAL OVERRIDE for development: read parity.toml and naming.toml from this working-tree "
            "directory instead of the pinned tag. Also settable as IDFKIT_GOVERNANCE_DIR. Never use "
            "this in CI."
        ),
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="List every capability unit and its claimants.")
    args = parser.parse_args(argv)

    try:
        report = run(Path(args.package_root).resolve(), args.conformance_repo, args.governance_dir)
    except Refusal as refusal:
        print(f"check_parity_ledger: refusing to run.\n  {refusal}", file=sys.stderr)
        return EXIT_REFUSED

    print(render(report, args.verbose))
    return EXIT_OK if report.ok else EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
