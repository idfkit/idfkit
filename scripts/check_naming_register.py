#!/usr/bin/env python3
"""Check the idfkit public surface against the pinned naming register.

The register, ``governance/naming.toml`` in the idfkit-conformance repository, is the single public
record of every concept the Python and TypeScript libraries share. This script is the Python half of
the gate pair described in ``contracts/naming-register.md``: it reads the register at the governance
tag pinned in ``pyproject.toml`` and holds the Python public surface against it.

Inputs, exactly the ones the contract names:

* ``idfkit.__all__``, plus every public attribute bound on the ``idfkit`` module. The second half is
  what a reader actually meets on ``idfkit.`` completion, and it is where assembly artefacts show up
  (FR-008).
* ``src/idfkit/document.pyi``, the IDFDocument stub that ``make check-stubs`` regenerates and diffs.
  The generated per-object-type accessors are recognised through the same machinery that emits them,
  ``idfkit.document._PYTHON_TO_IDF`` minus ``generate_stubs._RESERVED_ATTRS``, rather than being
  re-derived here. Run ``make check-stubs`` first: this gate reads the stub, it does not refresh it.

What it enforces:

* FR-003, FR-008: every public name resolves to a register entry, and a name that does not is named
  along with the file it is exported from.
* FR-005: one public name per concept per language.
* FR-006: an ``excluded`` entry that gains a counterpart in the other language fails.
* FR-079: no name reaches a second rename. A name whose Python rename budget is already spent is
  frozen at its registered spelling.
* FR-082: a side that is behind the pinned register stays blocked, and the report says which side is
  behind rather than only that the two disagree.

Exit codes:

* 0 every public name resolves, against a register read at the pinned governance tag.
* 1 at least one blocking finding.
* 2 the gate could not run: no pin declared, or the pinned register could not be read (FR-084).
* 3 every check passed, but the register was read through the local path override rather than from
  the pinned tag. That is not a green pinned run, so it is deliberately not 0.

Usage::

    uv run python scripts/check_naming_register.py
    uv run python scripts/check_naming_register.py --register ../idfkit-conformance/governance/naming.toml
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, NoReturn

try:
    import tomllib as _toml
except ModuleNotFoundError:  # Python 3.10
    try:
        import tomli as _toml  # type: ignore[no-redef]
    except ModuleNotFoundError:
        _toml = None  # type: ignore[assignment]

EXIT_OK = 0
EXIT_BLOCKED = 1
EXIT_CANNOT_RUN = 2
EXIT_UNPINNED = 3

REGISTER_PATH_IN_REPO = "governance/naming.toml"
GOVERNANCE_TAG_RE = re.compile(r"^governance-\d{4}\.\d+$")
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
DOTTED_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+$")
TRAILING_CALL_RE = re.compile(r"\(.*\)$")

VALID_KINDS = frozenset({"aligned", "divergent", "excluded"})
REASON_REQUIRED_KINDS = frozenset({"divergent", "excluded"})

# Files that carry no library surface of their own. `_generated_types.pyi` is one register entry
# ("generated object types"), not a thousand of them, so its classes are not indexed as names.
INDEX_SKIP_NAMES = frozenset({"_generated_types.pyi"})
INDEX_SKIP_DIRS = frozenset({"schemas", "data", ".agents", "__pycache__"})


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


class Severity(Enum):
    """Whether a finding blocks the merge."""

    BLOCKING = "blocking"
    INFO = "info"


@dataclass(frozen=True)
class Finding:
    """One thing the gate has to say about the surface or the register."""

    code: str
    severity: Severity
    headline: str
    details: tuple[str, ...] = ()

    def render(self) -> list[str]:
        lines = [f"  [{self.code}] {self.headline}"]
        lines.extend(f"      {detail}" for detail in self.details)
        return lines


# ---------------------------------------------------------------------------
# The register
# ---------------------------------------------------------------------------


class Shape(Enum):
    """What a register name value looks like, once read as text."""

    IDENTIFIER = "identifier"
    DOTTED_MODULE = "dotted-module"
    DOTTED_MEMBER = "dotted-member"
    EXPRESSION = "expression"


@dataclass(frozen=True)
class NameToken:
    """One name read out of a register entry's ``python`` or ``typescript`` field.

    A field may list several names, comma separated, which is how the register records a whole
    excluded surface under one concept.
    """

    raw: str
    symbol: str
    qualified: str | None
    shape: Shape

    @property
    def is_code_name(self) -> bool:
        """True when the token is a name a library could define, rather than an expression."""
        return self.shape is not Shape.EXPRESSION


@dataclass(frozen=True)
class RegisterEntry:
    """One ``[[entry]]`` of the register."""

    concept: str
    python: str
    typescript: str
    kind: str
    divergence_reason: str
    canonical_form: str
    notes: str
    rename_count_python: int | None
    rename_count_typescript: int | None
    python_names: tuple[NameToken, ...]
    typescript_names: tuple[NameToken, ...]
    position: int

    @property
    def python_code_names(self) -> tuple[NameToken, ...]:
        return tuple(token for token in self.python_names if token.is_code_name)


@dataclass(frozen=True)
class RegisterSource:
    """Where the register text came from, and whether that source was the pinned one."""

    text: str
    pinned: bool
    tag: str
    origin: str


@dataclass
class Register:
    """The parsed register, plus the lookup tables the checks need."""

    entries: tuple[RegisterEntry, ...]
    source: RegisterSource
    by_qualified: dict[str, RegisterEntry] = field(default_factory=dict)
    by_symbol: dict[str, RegisterEntry] = field(default_factory=dict)

    def build_index(self) -> None:
        """Index every Python name in the register, qualified first, bare name second.

        A module path deeper than ``idfkit.<name>`` is indexed by its full path only. Those entries
        say in so many words that Python reaches the name inside a submodule rather than through the
        top-level ``__all__``, so letting the last segment stand alone would have
        ``idfkit.schedules.values`` silently cover ``IDFDocument.values``, which is a different
        thing with the same last word.
        """
        for entry in self.entries:
            for token in entry.python_code_names:
                if token.qualified is not None:
                    self.by_qualified.setdefault(token.qualified, entry)
                if token.shape is Shape.DOTTED_MODULE and (token.qualified or "").count(".") > 1:
                    continue
                self.by_symbol.setdefault(token.symbol, entry)

    def lookup(self, qualified: str, symbol: str) -> RegisterEntry | None:
        """Resolve a public name to its entry: exact qualified match, then bare name."""
        return self.by_qualified.get(qualified) or self.by_symbol.get(symbol)


def classify_name(raw: str) -> NameToken | None:
    """Read one register name value as a token.

    ``col.get(name)`` becomes the member ``get``; ``doc["Zone"]`` is an expression and names no
    symbol; ``idfkit.validation.Severity`` is a module path whose last segment is the symbol.
    """
    text = raw.strip()
    if not text:
        return None
    text = TRAILING_CALL_RE.sub("", text).strip()
    if not text:
        return None
    if IDENTIFIER_RE.match(text):
        return NameToken(raw=raw.strip(), symbol=text, qualified=None, shape=Shape.IDENTIFIER)
    if DOTTED_RE.match(text):
        shape = Shape.DOTTED_MODULE if text.startswith("idfkit.") else Shape.DOTTED_MEMBER
        return NameToken(raw=raw.strip(), symbol=text.rsplit(".", 1)[1], qualified=text, shape=shape)
    return NameToken(raw=raw.strip(), symbol=text, qualified=None, shape=Shape.EXPRESSION)


def split_names(value: str) -> tuple[NameToken, ...]:
    """Split one register name field into tokens. A comma separates names, never one name."""
    tokens: list[NameToken] = []
    for part in value.split(","):
        token = classify_name(part)
        if token is not None:
            tokens.append(token)
    return tuple(tokens)


def _read_rename_count(raw: Any, language: str) -> int | None:
    if not isinstance(raw, dict):
        return None
    value = raw.get(language)
    return value if isinstance(value, int) else None


def parse_register(source: RegisterSource) -> Register:
    """Parse the register text into entries. Field validation is a check, not a parse error."""
    data = _toml.loads(source.text)
    raw_entries = data.get("entry", [])
    if not isinstance(raw_entries, list):
        fail_to_run("The register has no [[entry]] array. This is not a naming register.")
    entries: list[RegisterEntry] = []
    for position, raw in enumerate(raw_entries, start=1):
        rename_count = raw.get("rename_count")
        python = str(raw.get("python", ""))
        typescript = str(raw.get("typescript", ""))
        entries.append(
            RegisterEntry(
                concept=str(raw.get("concept", "")),
                python=python,
                typescript=typescript,
                kind=str(raw.get("kind", "")),
                divergence_reason=str(raw.get("divergence_reason", "")).strip(),
                canonical_form=str(raw.get("canonical_form", "")).strip(),
                notes=str(raw.get("notes", "")).strip(),
                rename_count_python=_read_rename_count(rename_count, "python"),
                rename_count_typescript=_read_rename_count(rename_count, "typescript"),
                python_names=split_names(python),
                typescript_names=split_names(typescript),
                position=position,
            )
        )
    register = Register(entries=tuple(entries), source=source)
    register.build_index()
    return register


# ---------------------------------------------------------------------------
# Reading the register at the pinned governance tag (FR-081, FR-084)
# ---------------------------------------------------------------------------


def fail_to_run(message: str, *details: str) -> NoReturn:
    """Refuse to run. The gate never falls back to an unpinned or absent register."""
    print("naming register gate: CANNOT RUN")
    print(f"  {message}")
    for detail in details:
        print(f"  {detail}")
    raise SystemExit(EXIT_CANNOT_RUN)


def read_pinned_level(repo: Path) -> str:
    """Read ``[tool.idfkit.governance] level`` from pyproject.toml, or refuse to run."""
    pyproject = repo / "pyproject.toml"
    if not pyproject.is_file():
        fail_to_run(f"No pyproject.toml at {pyproject}.")
    data = _toml.loads(pyproject.read_text(encoding="utf-8"))
    level = data.get("tool", {}).get("idfkit", {}).get("governance", {}).get("level")
    if not isinstance(level, str) or not level.strip():
        fail_to_run(
            "No governance level is declared in pyproject.toml.",
            'Add [tool.idfkit.governance] level = "governance-YYYY.N".',
            "FR-084: a gate that finds no pin refuses to run rather than falling back to a default.",
        )
    level = level.strip()
    if not GOVERNANCE_TAG_RE.match(level):
        fail_to_run(
            f"The declared governance level {level!r} is not an immutable governance-YYYY.N tag.",
            "FR-081: reading the register from a branch is prohibited, so a branch name is refused here.",
        )
    return level


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        ["git", "-C", str(repo), *args],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )


def resolve_conformance_repo(explicit: str | None, library_repo: Path) -> Path:
    """Find the idfkit-conformance checkout that carries the governance tags."""
    candidate = explicit or os.environ.get("IDFKIT_CONFORMANCE_REPO")
    path = Path(candidate).expanduser() if candidate else library_repo.parent / "idfkit-conformance"
    if not (path / ".git").exists():
        fail_to_run(
            f"No idfkit-conformance git checkout at {path}.",
            "Pass --conformance-repo PATH, or set IDFKIT_CONFORMANCE_REPO.",
        )
    return path


def load_register_from_tag(conformance_repo: Path, tag: str) -> RegisterSource:
    """Read the register out of the pinned tag. A missing tag refuses to run (FR-084)."""
    resolved = _git(conformance_repo, "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}^{{commit}}")
    if resolved.returncode != 0:
        fail_to_run(
            f"The pinned governance tag {tag} does not exist in {conformance_repo}.",
            "FR-084: the artefact is published and versioned before it is pinned, and a missing one",
            "fails the build rather than falling back to the default branch.",
            "For local development before the tag is published, pass",
            f"  --register {conformance_repo / REGISTER_PATH_IN_REPO}",
            "which is reported as an unpinned run and exits 3 rather than 0.",
        )
    shown = _git(conformance_repo, "show", f"{tag}:{REGISTER_PATH_IN_REPO}")
    if shown.returncode != 0:
        fail_to_run(f"{REGISTER_PATH_IN_REPO} is not present at {tag} in {conformance_repo}.")
    return RegisterSource(
        text=shown.stdout,
        pinned=True,
        tag=tag,
        origin=f"{conformance_repo}@{tag}:{REGISTER_PATH_IN_REPO}",
    )


def load_register_from_path(path: Path, tag: str) -> RegisterSource:
    """Read the register from a local working copy. Development only, never a green pinned run."""
    if not path.is_file():
        fail_to_run(f"No register file at {path}.")
    return RegisterSource(text=path.read_text(encoding="utf-8"), pinned=False, tag=tag, origin=str(path))


# ---------------------------------------------------------------------------
# The public surface
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PublicName:
    """One name on the Python public surface, and where a reader meets it."""

    symbol: str
    qualified: str
    origin: str
    source_file: str


@dataclass(frozen=True)
class Surface:
    """The Python public surface the register has to cover."""

    exported: tuple[PublicName, ...]
    document_members: tuple[PublicName, ...]
    leaked: tuple[PublicName, ...]
    generated_accessors: int

    @property
    def checked(self) -> tuple[PublicName, ...]:
        return self.exported + self.document_members


def _module_import_map(init_path: Path, package_root: Path) -> dict[str, str]:
    """Map each name imported by ``__init__.py`` to the file it is exported from."""
    tree = ast.parse(init_path.read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.level == 1:
            module_file = _module_file(package_root, node.module)
            for alias in node.names:
                mapping[alias.asname or alias.name] = module_file
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            mapping.setdefault(node.name, str(init_path))
    return mapping


def _module_file(package_root: Path, dotted: str) -> str:
    parts = dotted.split(".")
    as_module = package_root.joinpath(*parts).with_suffix(".py")
    if as_module.is_file():
        return str(as_module)
    as_package = package_root.joinpath(*parts) / "__init__.py"
    if as_package.is_file():
        return str(as_package)
    return f"{package_root.joinpath(*parts)} (unresolved)"


def _document_stub_members(stub_path: Path) -> list[tuple[str, int]]:
    """Read the public members of IDFDocument out of the generated stub."""
    tree = ast.parse(stub_path.read_text(encoding="utf-8"))
    members: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef) or node.name != "IDFDocument":
            continue
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("_"):
                members.append((item.name, item.lineno))
            elif (
                isinstance(item, ast.AnnAssign)
                and isinstance(item.target, ast.Name)
                and not item.target.id.startswith("_")
            ):
                members.append((item.target.id, item.lineno))
    return members


def collect_surface(repo: Path) -> Surface:
    """Collect the surface from the live module and from the stubs check-stubs already diffed."""
    package_root = repo / "src" / "idfkit"
    stub_path = package_root / "document.pyi"
    generated_types = package_root / "_generated_types.pyi"
    for required in (stub_path, generated_types):
        if not required.is_file():
            fail_to_run(f"Missing {required}. Run `make check-stubs` before this gate.")

    sys.path.insert(0, str(repo / "src"))
    try:
        import idfkit
        from idfkit.codegen.generate_stubs import _RESERVED_ATTRS
        from idfkit.document import _PYTHON_TO_IDF
    except ImportError as exc:
        fail_to_run(f"Could not import idfkit from {repo / 'src'}: {exc}")

    exported_names = tuple(idfkit.__all__)
    import_map = _module_import_map(package_root / "__init__.py", package_root)

    exported = tuple(
        PublicName(
            symbol=name,
            qualified=f"idfkit.{name}",
            origin="idfkit.__all__",
            source_file=import_map.get(name, str(package_root / "__init__.py")),
        )
        for name in exported_names
        if not name.startswith("__")
    )

    # Assembly artefacts: bound on the module, public, and not declared in __all__ (FR-008).
    # Submodules of the package itself are structure rather than leakage.
    declared = set(exported_names)
    leaked: list[PublicName] = []
    for name, value in sorted(vars(idfkit).items()):
        if name.startswith("_") or name in declared:
            continue
        module_name = getattr(value, "__name__", "") if isinstance(value, type(idfkit)) else ""
        if module_name.startswith("idfkit"):
            continue
        leaked.append(
            PublicName(
                symbol=name,
                qualified=f"idfkit.{name}",
                origin="module attribute, absent from __all__",
                source_file=str(package_root / "__init__.py"),
            )
        )

    # The per-object-type accessors are the Python half of "generated object types". They are
    # recognised through the machinery that emits them rather than re-derived here.
    generated = {name for name in _PYTHON_TO_IDF if name not in _RESERVED_ATTRS}
    document_members = tuple(
        PublicName(
            symbol=name,
            qualified=f"IDFDocument.{name}",
            origin="IDFDocument, from the generated stub",
            source_file=f"{stub_path}:{lineno}",
        )
        for name, lineno in _document_stub_members(stub_path)
        if name not in generated
    )

    return Surface(
        exported=exported,
        document_members=document_members,
        leaked=tuple(leaked),
        generated_accessors=len(generated),
    )


# ---------------------------------------------------------------------------
# What the library actually defines, for the "which side is behind" report
# ---------------------------------------------------------------------------


@dataclass
class DefinitionIndex:
    """Every public name the library defines anywhere, so a register name can be resolved."""

    qualified: dict[str, str] = field(default_factory=dict)
    symbols: dict[str, str] = field(default_factory=dict)
    parameters: set[str] = field(default_factory=set)
    console_scripts: set[str] = field(default_factory=set)

    def resolve(self, token: NameToken) -> str | None:
        """Where the library defines this register name, or None when it defines it nowhere."""
        if token.shape is Shape.DOTTED_MODULE:
            # A module path is precise: an unrelated method of the same bare name is not a match.
            return self.qualified.get(token.qualified or "")
        if token.shape is Shape.DOTTED_MEMBER:
            found = self.qualified.get(token.qualified or "")
            return found or self.symbols.get(token.symbol)
        if token.symbol in self.symbols:
            return self.symbols[token.symbol]
        if token.symbol in self.console_scripts:
            return "pyproject.toml [project.scripts]"
        if token.symbol in self.parameters:
            return "a keyword parameter of a public function"
        return None


def _record_class(index: DefinitionIndex, node: ast.ClassDef, module: str, path: Path) -> None:
    for item in node.body:
        name: str | None = None
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = item.name
        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            name = item.target.id
        if name is None or name.startswith("_"):
            continue
        index.qualified.setdefault(f"{node.name}.{name}", str(path))
        index.qualified.setdefault(f"{module}.{node.name}.{name}", str(path))
        index.symbols.setdefault(name, str(path))


def _record_function(index: DefinitionIndex, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
    args = node.args
    for arg in [*args.posonlyargs, *args.args, *args.kwonlyargs]:
        index.parameters.add(arg.arg)


def build_definition_index(repo: Path) -> DefinitionIndex:
    """Walk the package with ast. No imports, so optional dependencies cannot make it fail."""
    package_root = repo / "src" / "idfkit"
    index = DefinitionIndex()
    for path in sorted(package_root.rglob("*.py*")):
        if path.suffix not in {".py", ".pyi"}:
            continue
        if INDEX_SKIP_DIRS.intersection(path.relative_to(package_root).parts[:-1]):
            continue
        module = _dotted_module(package_root, path)
        # A module is itself a name the register can carry, `idfkit._generated_types` among them.
        index.qualified.setdefault(module, str(path))
        if path.name in INDEX_SKIP_NAMES:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        _index_module(index, tree, module, path)
    index.console_scripts = _console_scripts(repo)
    return index


def _index_module(index: DefinitionIndex, tree: ast.Module, module: str, path: Path) -> None:
    """Record every public top-level name one module binds."""
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            _record_top_level(index, node.name, module, path)
            _record_class(index, node, module, path)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _record_top_level(index, node.name, module, path)
            _record_function(index, node)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            _record_top_level(index, node.target.id, module, path)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    _record_top_level(index, target.id, module, path)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            _record_reexports(index, node, module, path)


def _record_reexports(index: DefinitionIndex, node: ast.Import | ast.ImportFrom, module: str, path: Path) -> None:
    """Record a re-export, module qualified only.

    ``idfkit.schedules.evaluate`` is defined in ``schedules/evaluate.py`` and reached through the
    subpackage, which is the name the register carries. The bare name is deliberately NOT recorded:
    every stdlib import would otherwise answer for a register name of the same word.
    """
    for alias in node.names:
        name = alias.asname or alias.name.split(".")[0]
        if not name.startswith("_"):
            index.qualified.setdefault(f"{module}.{name}", str(path))


def _record_top_level(index: DefinitionIndex, name: str, module: str, path: Path) -> None:
    if name.startswith("_"):
        return
    index.qualified.setdefault(f"{module}.{name}", str(path))
    index.symbols.setdefault(name, str(path))


def _dotted_module(package_root: Path, path: Path) -> str:
    parts = list(path.relative_to(package_root).parts)
    parts[-1] = parts[-1].removesuffix(".pyi").removesuffix(".py")
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(["idfkit", *parts])


def _console_scripts(repo: Path) -> set[str]:
    data = _toml.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    return set(scripts) if isinstance(scripts, dict) else set()


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_register_schema(register: Register) -> list[Finding]:
    """The register's own field contract, including the rename count FR-079 requires."""
    findings: list[Finding] = []
    seen: dict[str, int] = {}
    for entry in register.entries:
        label = entry.concept or f"entry #{entry.position}"
        if not entry.concept:
            findings.append(Finding("register-schema", Severity.BLOCKING, f"Entry #{entry.position} has no concept."))
        elif entry.concept in seen:
            findings.append(
                Finding(
                    "register-schema",
                    Severity.BLOCKING,
                    f"The concept {entry.concept!r} appears twice, at entries #{seen[entry.concept]} "
                    f"and #{entry.position}. A concept is unique across the register.",
                )
            )
        else:
            seen[entry.concept] = entry.position
        if entry.kind not in VALID_KINDS:
            findings.append(
                Finding(
                    "register-schema",
                    Severity.BLOCKING,
                    f"{label}: kind {entry.kind!r} is not one of aligned, divergent, excluded.",
                )
            )
        if entry.kind in REASON_REQUIRED_KINDS and not entry.divergence_reason:
            findings.append(
                Finding(
                    "divergence-reason",
                    Severity.BLOCKING,
                    f"{label}: a {entry.kind} entry has no divergence_reason.",
                    ("It must state why each side is correct in its own ecosystem.",),
                )
            )
        findings.extend(_check_rename_count_present(entry, label))
    return findings


def _check_rename_count_present(entry: RegisterEntry, label: str) -> list[Finding]:
    findings: list[Finding] = []
    for language, count in (("python", entry.rename_count_python), ("typescript", entry.rename_count_typescript)):
        if count is None:
            findings.append(
                Finding(
                    "rename-count",
                    Severity.BLOCKING,
                    f"{label}: rename_count.{language} is missing or is not an integer.",
                    ("FR-079 requires a rename count per name, so the budget can be enforced at merge.",),
                )
            )
        elif count < 0:
            findings.append(
                Finding("rename-count", Severity.BLOCKING, f"{label}: rename_count.{language} is negative ({count}).")
            )
    return findings


def check_rename_budget(register: Register) -> list[Finding]:
    """FR-079: one rename is the budget, and the block is not waivable by the gate."""
    findings: list[Finding] = []
    for entry in register.entries:
        for language, count, names in (
            ("python", entry.rename_count_python, entry.python),
            ("typescript", entry.rename_count_typescript, entry.typescript),
        ):
            if count is not None and count >= 2:
                findings.append(
                    Finding(
                        "rename-budget",
                        Severity.BLOCKING,
                        f"{entry.concept}: {language} name {names!r} is at rename_count {count}.",
                        (
                            "One rename is the budget (FR-079, SC-003). A second rename requires an",
                            "amendment to the register, reviewed by both languages, stating why the",
                            "first rename was wrong. The gate does not waive it.",
                        ),
                    )
                )
    return findings


def check_excluded_counterparts(register: Register) -> list[Finding]:
    """FR-006: excluded is terminal. A counterpart on the other side fails the gate."""
    findings: list[Finding] = []
    for entry in register.entries:
        if entry.kind != "excluded":
            continue
        has_python = bool(entry.python.strip())
        has_typescript = bool(entry.typescript.strip())
        if has_python and has_typescript:
            present, counterpart = ("Python", entry.typescript) if entry.python else ("TypeScript", entry.python)
            findings.append(
                Finding(
                    "excluded-counterpart",
                    Severity.BLOCKING,
                    f"{entry.concept}: an excluded entry has a counterpart in the other language.",
                    (
                        f"Excluded surface, {present} side: {entry.python or entry.typescript}",
                        f"Offending counterpart: {counterpart}",
                        "Adding one requires amending this entry, reviewed by both languages.",
                    ),
                )
            )
        elif not has_python and not has_typescript:
            findings.append(
                Finding(
                    "excluded-counterpart",
                    Severity.BLOCKING,
                    f"{entry.concept}: an excluded entry names nothing on either side.",
                )
            )
    return findings


def check_coverage(surface: Surface, register: Register) -> tuple[list[Finding], dict[str, list[PublicName]]]:
    """FR-003 and FR-008: every public name resolves, and leakage is deleted rather than registered."""
    findings: list[Finding] = []
    grouped: dict[str, list[PublicName]] = {}
    for name in surface.checked:
        entry = register.lookup(name.qualified, name.symbol)
        if entry is None:
            findings.append(
                Finding(
                    "uncovered-name",
                    Severity.BLOCKING,
                    f"{name.qualified} has no register entry.",
                    (
                        f"library: idfkit (Python), exported from {name.source_file}",
                        f"surface: {name.origin}",
                        "The REGISTER is behind the LIBRARY. The register entry lands first (FR-003),",
                        "so either register this name or withdraw it from the public surface.",
                    ),
                )
            )
            continue
        grouped.setdefault(entry.concept, []).append(name)
    findings.extend(_leak_findings(surface))
    return findings, grouped


def _leak_findings(surface: Surface) -> list[Finding]:
    if not surface.leaked:
        return []
    return [
        Finding(
            "assembly-artefact",
            Severity.BLOCKING,
            f"{name.qualified} is public on the module but is not in __all__.",
            (
                f"library: idfkit (Python), bound in {name.source_file}",
                "FR-008: a name that was never intended as public is deleted from the surface,",
                "not registered. Import-leakage shows up in completion on `idfkit.`.",
            ),
        )
        for name in surface.leaked
    ]


def check_one_name_per_concept(
    register: Register,
    grouped: dict[str, list[PublicName]],
) -> list[Finding]:
    """FR-005: one public name per concept per language.

    Two arms. The surface arm catches a concept that two distinct public spellings resolve to. The
    register arm catches an entry that lists two names for one concept. Excluded entries are exempt
    from the register arm by construction: one entry stands for a whole non-portable surface there.
    """
    findings: list[Finding] = []
    by_concept = {entry.concept: entry for entry in register.entries}
    for concept, names in sorted(grouped.items()):
        entry = by_concept.get(concept)
        if entry is not None and entry.kind == "excluded":
            continue
        spellings = sorted({name.symbol for name in names})
        if len(spellings) > 1:
            findings.append(
                Finding(
                    "second-public-name",
                    Severity.BLOCKING,
                    f"{concept}: {len(spellings)} public Python names for one concept.",
                    tuple([f"names: {', '.join(spellings)}"] + [f"  {n.qualified} in {n.source_file}" for n in names]),
                )
            )
    findings.extend(_register_side_duplicates(register))
    return findings


def _register_side_duplicates(register: Register) -> list[Finding]:
    findings: list[Finding] = []
    for entry in register.entries:
        if entry.kind == "excluded":
            continue
        spellings = sorted({token.symbol for token in entry.python_code_names})
        if len(spellings) > 1:
            findings.append(
                Finding(
                    "second-public-name",
                    Severity.BLOCKING,
                    f"{entry.concept}: the register itself lists {len(spellings)} Python names for one concept.",
                    (f"names: {', '.join(spellings)}", "Exactly one must remain public (FR-005)."),
                )
            )
    return findings


def check_library_behind(register: Register, index: DefinitionIndex) -> list[Finding]:
    """FR-003 and FR-082: say which side is behind, and keep a reverted side blocked.

    A registered name the library does not define is not automatically a failure: FR-007 requires
    names to be registered before the capability is written. It IS a failure when the name's Python
    rename budget is already spent, because that spelling is frozen: the absence then means either
    the rename has not landed or the side was reverted, and FR-082 keeps it blocked without the
    register entry being withdrawn.
    """
    findings: list[Finding] = []
    for entry in register.entries:
        for token in entry.python_code_names:
            if index.resolve(token) is not None:
                continue
            spent = (entry.rename_count_python or 0) >= 1
            findings.append(_behind_finding(entry, token, spent=spent))
    return findings


def _behind_finding(entry: RegisterEntry, token: NameToken, *, spent: bool) -> Finding:
    shared = (
        f"concept: {entry.concept}",
        f"registered Python name: {token.raw}",
        "The LIBRARY is behind the REGISTER: the register carries a name idfkit does not define.",
    )
    if spent:
        return Finding(
            "library-behind",
            Severity.BLOCKING,
            f"{token.raw} is registered with its rename budget spent, and idfkit does not define it.",
            (
                *shared,
                f"rename_count.python = {entry.rename_count_python}, so this spelling is frozen (FR-079).",
                "The side stays blocked until it catches up, and the register entry is not withdrawn (FR-082).",
            ),
        )
    return Finding(
        "library-behind",
        Severity.INFO,
        f"{token.raw} is registered but idfkit does not define it.",
        (
            *shared,
            "rename_count.python = 0, so this is a name registered ahead of its implementation",
            "(FR-007), or an entry that records a property rather than a symbol.",
        ),
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_header(register: Register, surface: Surface) -> None:
    print("idfkit naming register gate")
    print(f"  register: {register.source.origin}")
    if register.source.pinned:
        print(f"  read at the pinned governance tag {register.source.tag}")
    else:
        print("")
        print("  !! UNPINNED LOCAL REGISTER, DEVELOPMENT ONLY !!")
        print(f"  !! pyproject.toml pins {register.source.tag}; this run read a working copy instead.")
        print("  !! A pass here is NOT a green pinned run. It exits 3, never 0 (FR-081, FR-084).")
        print("")
    print(f"  entries: {len(register.entries)}")
    print(
        f"  surface: {len(surface.exported)} from idfkit.__all__, "
        f"{len(surface.document_members)} from IDFDocument (document.pyi), "
        f"{len(surface.checked)} names checked"
    )
    print(
        f"  not checked: {surface.generated_accessors} generated per-object-type accessors, covered "
        "by the 'generated object types' entry"
    )
    print("")


def print_findings(findings: list[Finding]) -> tuple[int, int]:
    blocking = [f for f in findings if f.severity is Severity.BLOCKING]
    info = [f for f in findings if f.severity is Severity.INFO]
    if blocking:
        print(f"BLOCKING ({len(blocking)})")
        for finding in blocking:
            for line in finding.render():
                print(line)
        print("")
    if info:
        print(f"INFORMATION ({len(info)})")
        for finding in info:
            for line in finding.render():
                print(line)
        print("")
    return len(blocking), len(info)


def print_summary(register: Register, surface: Surface, blocking: int, info: int) -> int:
    if blocking:
        print(f"FAILED: {blocking} blocking finding(s), {info} informational.")
        return EXIT_BLOCKED
    if not register.source.pinned:
        print(f"PASSED against an UNPINNED local register: {len(surface.checked)} public names, {info} informational.")
        print(f"This is not a green pinned run. Publish {register.source.tag} and rerun without --register.")
        return EXIT_UNPINNED
    print(
        f"PASSED: {len(surface.checked)} public names resolve to entries in {register.source.tag}. {info} informational."
    )
    return EXIT_OK


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check the idfkit public surface against the pinned naming register.")
    parser.add_argument(
        "--repo",
        default=str(Path(__file__).resolve().parent.parent),
        help="Path to the idfkit repository (default: the repository this script lives in).",
    )
    parser.add_argument(
        "--conformance-repo",
        default=None,
        help="Path to the idfkit-conformance checkout carrying the governance tags.",
    )
    parser.add_argument(
        "--register",
        default=None,
        help=(
            "Read the register from this path instead of the pinned tag. Development only, for use "
            "before the governance tag is published. A clean run exits 3, not 0."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if _toml is None:
        fail_to_run("No TOML reader available. Python 3.11+ ships tomllib; on 3.10 install tomli.")
    repo = Path(args.repo).expanduser().resolve()
    tag = read_pinned_level(repo)

    if args.register:
        source = load_register_from_path(Path(args.register).expanduser().resolve(), tag)
    else:
        source = load_register_from_tag(resolve_conformance_repo(args.conformance_repo, repo), tag)

    register = parse_register(source)
    surface = collect_surface(repo)
    index = build_definition_index(repo)

    findings: list[Finding] = []
    findings.extend(check_register_schema(register))
    findings.extend(check_rename_budget(register))
    findings.extend(check_excluded_counterparts(register))
    coverage_findings, grouped = check_coverage(surface, register)
    findings.extend(coverage_findings)
    findings.extend(check_one_name_per_concept(register, grouped))
    findings.extend(check_library_behind(register, index))

    print_header(register, surface)
    blocking, info = print_findings(findings)
    return print_summary(register, surface, blocking, info)


if __name__ == "__main__":
    raise SystemExit(main())
