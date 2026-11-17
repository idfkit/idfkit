"""Static narrowing of the EnergyPlus releases a line of code can run against.

``idfkit check`` reports a literal against every target release unless the code around it
already restricts the document to some of them. This module recognises a small, sound subset of
the ways code does that, and nothing cleverer:

* **as_version receivers.** A lookup made directly on ``as_version(doc, ...)``, or on a name
  bound exactly once in its scope to such a call (``legacy = as_version(doc, IDFDocumentV9_4)``),
  runs only against the releases ``as_version`` accepts. Recognised arguments: one document type
  (``IDFDocumentV9_4``, ``IDFDocument`` for the latest release, ``versioned.IDFDocumentV9_4``,
  ``IDFDocumentV9_4[bool]``), a tuple, ``|`` union or ``Union[...]`` of them, and the
  ``since=``/``before=`` keywords (``since`` inclusive, ``before`` exclusive) given a release
  string (``"9.4"``), a version tuple or a document type. A name bound exactly once to one of
  those (``_SINCE_9_4 = (IDFDocumentV9_4, ...)``) is followed.
* **version guards.** Inside ``if X.version <op> (9, 4, 0):``, where ``X`` is a name or a dotted
  attribute of one, the lookups on ``X`` (or on an ``as_version`` of ``X``) run only against the
  releases that satisfy the comparison, and inside its ``else`` against the others. ``<``,
  ``<=``, ``>``, ``>=``, ``==``, ``!=`` and chained comparisons against tuples of integers are
  read, combined with ``and``, ``or`` and ``not``. A conjunct that is not a version comparison
  (``and "Space" in doc``) is skipped, which is sound for ``and``; an ``else`` is narrowed only
  when its whole test was read. A release is kept when the comparison can hold for any version
  number a document of that release carries: ``doc.version`` is the number the model declared, so
  a ``Version, 9.0;`` model is ``(9, 0, 0)`` on the 9.0.1 schema, and a model newer than every
  release keeps its own number on the latest schema.

Anything else gives no narrowing, which can only produce a warning that suppression handles,
never hide one: early returns (``if doc.version < (9, 4, 0): return``), ``assert``, conditional
expressions, ``match``, ``isinstance``, annotations, and names bound more than once. A guard stops
applying inside a nested function or class, and is dropped for a block that rebinds the document
it tests.
"""

from __future__ import annotations

import ast
import operator
import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

from ..versions import ENERGYPLUS_VERSIONS, LATEST_VERSION

Release = tuple[int, int, int]
Releases = frozenset[Release]
Predicate = Callable[[Release], bool]

ALL_RELEASES: Releases = frozenset(ENERGYPLUS_VERSIONS)

_MAX_DEPTH = 8
_DOC_TYPE_RE = re.compile(r"^IDFDocumentV(\d+)_(\d+)$")
_ROOT_RE = re.compile(r"^[A-Za-z_]\w*")
_COMPARE_OPS: dict[type[ast.cmpop], Callable[[Any, Any], bool]] = {
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
}


def release_for_line(major: int, minor: int) -> Release | None:
    """The supported release of the ``major.minor`` line (``9.0`` is 9.0.1), or ``None``."""
    return next((v for v in ENERGYPLUS_VERSIONS if v[:2] == (major, minor)), None)


# ---------------------------------------------------------------------------
# Scopes: which names are bound exactly once, and to what
# ---------------------------------------------------------------------------


@dataclass
class Scope:
    """The bindings of one Python scope (module, function, lambda or class body)."""

    parent: Scope | None
    is_class: bool = False
    bindings: dict[str, list[ast.expr | None]] = field(default_factory=lambda: {})
    star_import: bool = False


class ScopeTable:
    """Every scope of a module, and the names whose binding cannot be followed statically."""

    def __init__(self, tree: ast.Module) -> None:
        self.module = Scope(parent=None)
        self.children: dict[int, Scope] = {}
        self.escaped: set[str] = set()
        self._collect_body(tree.body, self.module)

    def scope_for(self, node: ast.AST, current: Scope) -> Scope:
        """The scope a function, lambda or class *node* opens (``current`` for any other node)."""
        return self.children.get(id(node), current)

    def lookup(self, name: str, scope: Scope) -> Scope | None:
        """The scope whose binding *name* refers to from *scope*, or ``None`` when it cannot be known.

        Follows Python's lexical rule: a class body is visible only from itself, not from the
        functions nested in it. A ``global``/``nonlocal`` name or a ``from x import *`` on the way
        makes the answer unknown.
        """
        if name in self.escaped:
            return None
        current: Scope | None = scope
        first = True
        while current is not None:
            if current.star_import:
                return None
            if (first or not current.is_class) and name in current.bindings:
                return current
            first = False
            current = current.parent
        return None

    def value_of(self, name: str, scope: Scope) -> tuple[ast.expr, Scope] | None:
        """The expression *name* is bound to, and the scope it is bound in, if it is bound exactly once."""
        owner = self.lookup(name, scope)
        if owner is None:
            return None
        values = owner.bindings[name]
        value = values[0] if len(values) == 1 else None
        return (value, owner) if value is not None else None

    def is_stable(self, name: str, scope: Scope, other: Scope) -> bool:
        """Whether *name* means the same single binding from *scope* and from *other*."""
        owner = self.lookup(name, scope)
        return owner is not None and owner is self.lookup(name, other) and len(owner.bindings[name]) == 1

    # -- collection ---------------------------------------------------------

    def _bind(self, scope: Scope, name: str, value: ast.expr | None) -> None:
        scope.bindings.setdefault(name, []).append(value)

    def _bind_target(self, scope: Scope, target: ast.expr, value: ast.expr | None) -> None:
        if isinstance(target, ast.Name):
            self._bind(scope, target.id, value)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                self._bind_target(scope, elt, None)
        elif isinstance(target, ast.Starred):
            self._bind_target(scope, target.value, None)
        # Attribute and subscript targets bind no name; their sub-expressions are collected below.

    def _collect_body(self, body: list[ast.stmt], scope: Scope) -> None:
        for stmt in body:
            self._collect(stmt, scope)

    def _open(self, node: ast.AST, scope: Scope, *, is_class: bool) -> Scope:
        child = Scope(parent=scope, is_class=is_class)
        self.children[id(node)] = child
        return child

    def _collect_arguments(self, args: ast.arguments, scope: Scope, child: Scope) -> None:
        for default in [*args.defaults, *(d for d in args.kw_defaults if d is not None)]:
            self._collect(default, scope)
        params = [*args.posonlyargs, *args.args, *args.kwonlyargs]
        params += [a for a in (args.vararg, args.kwarg) if a is not None]
        for param in params:
            self._bind(child, param.arg, None)

    def _collect(self, node: ast.AST, scope: Scope) -> None:  # noqa: C901
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self._bind(scope, node.name, None)
            for decorator in node.decorator_list:
                self._collect(decorator, scope)
            child = self._open(node, scope, is_class=False)
            self._collect_arguments(node.args, scope, child)
            self._collect_body(node.body, child)
            return
        if isinstance(node, ast.Lambda):
            child = self._open(node, scope, is_class=False)
            self._collect_arguments(node.args, scope, child)
            self._collect(node.body, child)
            return
        if isinstance(node, ast.ClassDef):
            self._bind(scope, node.name, None)
            for expr in [*node.decorator_list, *node.bases, *(k.value for k in node.keywords)]:
                self._collect(expr, scope)
            self._collect_body(node.body, self._open(node, scope, is_class=True))
            return
        if isinstance(node, ast.Assign):
            single = len(node.targets) == 1
            for target in node.targets:
                self._bind_target(scope, target, node.value if single else None)
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            self._bind_target(scope, node.target, node.value)
        elif isinstance(node, ast.AugAssign):
            self._bind_target(scope, node.target, None)
        elif isinstance(node, ast.NamedExpr):
            self._bind_target(scope, node.target, node.value)
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            self._bind_target(scope, node.target, None)
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            self._bind_target(scope, node.optional_vars, None)
        elif isinstance(node, ast.Delete):
            for target in node.targets:
                self._bind_target(scope, target, None)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.name == "*":
                    scope.star_import = True
                else:
                    self._bind(scope, alias.asname or alias.name.split(".")[0], None)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            self._bind(scope, node.name, None)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            self.escaped.update(node.names)
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name:
            self._bind(scope, node.name, None)
        elif isinstance(node, ast.MatchMapping) and node.rest:
            self._bind(scope, node.rest, None)
        for child_node in ast.iter_child_nodes(node):
            self._collect(child_node, scope)


# ---------------------------------------------------------------------------
# Documents: what an expression is, and which releases it is narrowed to
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DocumentRef:
    """What a receiver expression is known to be.

    Attributes:
        bases: Source texts (normalised with ``ast.unparse``) of every expression known to be this
            same document: the receiver itself, the first argument of an ``as_version`` call, and
            each name bound once to one of those.
        releases: The releases the document is narrowed to, or ``None`` for no narrowing.
    """

    bases: frozenset[str]
    releases: Releases | None


def _intersect(a: Releases | None, b: Releases | None) -> Releases | None:
    if a is None:
        return b
    if b is None:
        return a
    return a & b


def is_as_version_call(node: ast.expr) -> bool:
    """Whether *node* calls a function named ``as_version``."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (isinstance(func, ast.Name) and func.id == "as_version") or (
        isinstance(func, ast.Attribute) and func.attr == "as_version"
    )


class Narrower:
    """Resolve receivers and guards against one module's scopes."""

    def __init__(self, table: ScopeTable) -> None:
        self.table = table

    # -- documents ------------------------------------------------------------

    def document(self, expr: ast.expr, scope: Scope, depth: int = 0) -> DocumentRef:
        """What *expr*, used as a document, is known to be in *scope*."""
        text = ast.unparse(expr)
        if depth > _MAX_DEPTH:
            return DocumentRef(frozenset({text}), None)
        if isinstance(expr, ast.Call) and is_as_version_call(expr) and expr.args:
            inner = self.document(expr.args[0], scope, depth + 1)
            narrowed = self.as_version_releases(expr, scope)
            return DocumentRef(inner.bases | {text}, _intersect(inner.releases, narrowed))
        if isinstance(expr, ast.Name):
            bound = self.table.value_of(expr.id, scope)
            if bound is not None and (isinstance(bound[0], ast.Name) or is_as_version_call(bound[0])):
                value, owner = bound
                inner = self.document(value, owner, depth + 1)
                # The value's names were read where it was bound. They name the same document here
                # only if they resolve to the same single binding from both places: a parameter
                # of the same name, or a later rebinding, would make a guard on one apply to the
                # other.
                kept = {b for b in inner.bases if self._stable_text(b, owner, scope)}
                return DocumentRef(frozenset(kept | {text}), inner.releases)
        return DocumentRef(frozenset({text}), None)

    def _stable_text(self, text: str, owner: Scope, scope: Scope) -> bool:
        """Whether every name in the expression *text* means one fixed binding from both scopes."""
        try:
            names = [n.id for n in ast.walk(ast.parse(text, mode="eval")) if isinstance(n, ast.Name)]
        except SyntaxError:
            return False
        return all(self.table.is_stable(name, owner, scope) for name in names)

    def as_version_releases(self, call: ast.Call, scope: Scope) -> Releases | None:
        """The releases an ``as_version(doc, ...)`` call accepts, or ``None`` when not read."""
        keywords = {kw.arg: kw.value for kw in call.keywords if kw.arg is not None}
        type_arg = call.args[1] if len(call.args) > 1 else keywords.get("document_type")
        since = keywords.get("since")
        before = keywords.get("before")
        if type_arg is not None:
            # A type together with a range is refused at run time; nothing to narrow.
            return None if since is not None or before is not None else self.document_types(type_arg, scope)
        lower = self._bound(since, scope) if since is not None else None
        upper = self._bound(before, scope) if before is not None else None
        if lower is None and upper is None:
            return None
        return frozenset(
            v for v in ENERGYPLUS_VERSIONS if (lower is None or v >= lower) and (upper is None or v < upper)
        )

    def document_types(self, expr: ast.expr, scope: Scope, depth: int = 0) -> Releases | None:  # noqa: C901
        """The releases a document-type expression names (a type, tuple or union), or ``None``."""
        if depth > _MAX_DEPTH:
            return None
        if isinstance(expr, (ast.Tuple, ast.List)):
            members = [self.document_types(e, scope, depth + 1) for e in expr.elts]
            return _union(members)
        if isinstance(expr, ast.BinOp) and isinstance(expr.op, ast.BitOr):
            return _union([
                self.document_types(expr.left, scope, depth + 1),
                self.document_types(expr.right, scope, depth + 1),
            ])
        if isinstance(expr, ast.Subscript):
            head = _name_of(expr.value)
            if head == "Union":
                return self.document_types(expr.slice, scope, depth + 1)
            return self.document_types(expr.value, scope, depth + 1)
        name = _name_of(expr)
        if name is None:
            return None
        if name == "IDFDocument":
            return frozenset({LATEST_VERSION})
        match = _DOC_TYPE_RE.match(name)
        if match:
            release = release_for_line(int(match.group(1)), int(match.group(2)))
            return frozenset({release}) if release is not None else None
        if isinstance(expr, ast.Name):
            bound = self.table.value_of(expr.id, scope)
            if bound is not None:
                return self.document_types(bound[0], bound[1], depth + 1)
        return None

    def _bound(self, expr: ast.expr, scope: Scope, depth: int = 0) -> Release | None:
        """The release a ``since=``/``before=`` bound names, or ``None`` when it is not read."""
        if depth > _MAX_DEPTH:
            return None
        if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
            parts = expr.value.strip().split(".")
            if len(parts) in {2, 3} and all(p.isdigit() for p in parts):
                return release_for_line(int(parts[0]), int(parts[1]))
            return None
        numbers = _int_tuple(expr)
        if numbers is not None:
            return release_for_line(numbers[0], numbers[1]) if len(numbers) >= 2 else None
        types = self.document_types(expr, scope, depth + 1)
        if types is not None and len(types) == 1:
            return next(iter(types))
        if isinstance(expr, ast.Name):
            bound = self.table.value_of(expr.id, scope)
            if bound is not None:
                return self._bound(bound[0], bound[1], depth + 1)
        return None

    # -- guards ---------------------------------------------------------------

    def guard_conjuncts(self, test: ast.expr, scope: Scope) -> list[Guard]:
        """Every version comparison that must hold for *test* to be true (sound for ``and``)."""
        if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.And):
            return [g for value in test.values for g in self.guard_conjuncts(value, scope)]
        guard = self.guard(test, scope)
        return [guard] if guard is not None else []

    def guard(self, test: ast.expr, scope: Scope) -> Guard | None:  # noqa: C901
        """*test* read completely as a version predicate on one document, or ``None``."""
        if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
            inner = self.guard(test.operand, scope)
            if inner is None:
                return None
            return inner.negated()
        if isinstance(test, ast.BoolOp):
            parts = [self.guard(v, scope) for v in test.values]
            if any(p is None for p in parts):
                return None
            guards = [p for p in parts if p is not None]
            if len({g.document.bases for g in guards}) != 1:
                return None
            preds = [g.predicate for g in guards]
            combine = all if isinstance(test.op, ast.And) else any
            points = frozenset(point for g in guards for point in g.points)
            return Guard(guards[0].document, lambda v: combine(p(v) for p in preds), points)
        if not isinstance(test, ast.Compare):
            return None
        operands = [test.left, *test.comparators]
        receiver: ast.expr | None = None
        terms: list[tuple[int, ...] | None] = []
        for operand in operands:
            if isinstance(operand, ast.Attribute) and operand.attr == "version":
                if not _is_dotted(operand.value):
                    # ``docs[i].version``: the index can change between the test and the lookup.
                    return None
                if receiver is not None and ast.unparse(receiver) != ast.unparse(operand.value):
                    return None
                receiver = operand.value
                terms.append(None)
                continue
            numbers = _int_tuple(operand)
            if numbers is None:
                return None
            terms.append(numbers)
        if receiver is None:
            return None
        ops: list[Callable[[Any, Any], bool]] = []
        for op in test.ops:
            fn = _COMPARE_OPS.get(type(op))
            if fn is None:
                return None
            ops.append(fn)
        frozen_terms = tuple(terms)

        def predicate(version: Release) -> bool:
            values = [version if t is None else t for t in frozen_terms]
            return all(fn(values[i], values[i + 1]) for i, fn in enumerate(ops))

        points = frozenset(t for t in frozen_terms if t is not None)
        return Guard(self.document(receiver, scope), predicate, points)


_HUGE = 10**6


@dataclass(frozen=True)
class Guard:
    """A version predicate that holds for one document inside a guarded block.

    Attributes:
        document: The document the predicate tests.
        predicate: The test, applied to a ``doc.version`` value.
        points: The version tuples the test compares against, which decide the values
            :meth:`narrow` tries for each release.
    """

    document: DocumentRef
    predicate: Predicate
    points: frozenset[tuple[int, ...]] = frozenset()

    def negated(self) -> Guard:
        """The guard of the opposite branch."""
        predicate = self.predicate
        return Guard(self.document, lambda v: not predicate(v), self.points)

    def narrow(self, releases: Releases) -> Releases:
        """The members of *releases* a document could satisfy the guard on.

        ``doc.version`` is the number the model declared, not the release whose schema reads it:
        any patch of the release's line, and for the latest release any newer number. A release
        is kept when the predicate holds for at least one such value, so narrowing never drops a
        release the guarded code can run on.
        """
        return frozenset(r for r in releases if any(self.predicate(v) for v in self._candidates(r)))

    def _candidates(self, release: Release) -> set[Release]:
        major, minor = release[0], release[1]
        values: set[Release] = {release, (major, minor, 0), (major, minor, _HUGE)}
        for point in self.points:
            filled = (*point, 0, 0, 0)
            padded: Release = (filled[0], filled[1], filled[2])
            if padded[:2] == (major, minor):
                values.update((major, minor, max(padded[2] + d, 0)) for d in (-1, 0, 1))
            elif release == LATEST_VERSION and padded > release:
                values.update({padded, (padded[0], padded[1], padded[2] + 1)})
        if release == LATEST_VERSION:
            values.add((_HUGE, 0, 0))
        return values


def rebinds(body: list[ast.stmt], document: DocumentRef) -> bool:
    """Whether *body* assigns to the guarded document, or to the name it is reached through."""
    roots = {m.group(0) for m in (_ROOT_RE.match(b) for b in document.bases) if m}
    for target in _assigned_targets(body):
        if isinstance(target, ast.Name) and target.id in roots:
            return True
        if ast.unparse(target) in document.bases:
            return True
    return False


def _assigned_targets(body: list[ast.stmt]) -> Iterator[ast.expr]:
    """Every target *body* binds, in any form, including comprehension and ``except`` names."""
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Assign):
                yield from _flatten(node.targets)
            elif isinstance(
                node, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr, ast.For, ast.AsyncFor, ast.comprehension)
            ):
                yield from _flatten([node.target])
            elif isinstance(node, ast.withitem) and node.optional_vars is not None:
                yield from _flatten([node.optional_vars])
            elif isinstance(node, ast.Delete):
                yield from _flatten(node.targets)
            else:
                yield from (ast.Name(id=name) for name in _bound_names(node))


def _bound_names(node: ast.AST) -> list[str]:
    """The names a statement or pattern binds other than by assignment (``except as``, ``import``, ``def``)."""
    names: list[str | None] = []
    if isinstance(node, ast.ExceptHandler):
        names = [node.name]
    elif isinstance(node, (ast.Import, ast.ImportFrom)):
        names = [a.asname or a.name.split(".")[0] for a in node.names]
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.MatchAs, ast.MatchStar)):
        names = [node.name]
    elif isinstance(node, ast.MatchMapping):
        names = [node.rest]
    elif isinstance(node, (ast.Global, ast.Nonlocal)):
        names = list(node.names)
    return [n for n in names if n]


def _flatten(targets: list[ast.expr]) -> Iterator[ast.expr]:
    for target in targets:
        if isinstance(target, (ast.Tuple, ast.List)):
            yield from _flatten(target.elts)
        elif isinstance(target, ast.Starred):
            yield from _flatten([target.value])
        else:
            yield target


def _union(members: list[Releases | None]) -> Releases | None:
    if not members or any(m is None for m in members):
        return None
    out: set[Release] = set()
    for m in members:
        if m is not None:
            out |= m
    return frozenset(out)


def _name_of(expr: ast.expr) -> str | None:
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return expr.attr
    return None


def _int_tuple(expr: ast.expr) -> tuple[int, ...] | None:
    if not isinstance(expr, ast.Tuple) or not expr.elts:
        return None
    numbers: list[int] = []
    for elt in expr.elts:
        if not (isinstance(elt, ast.Constant) and type(elt.value) is int):
            return None
        numbers.append(elt.value)
    return tuple(numbers)


def _is_dotted(expr: ast.expr) -> bool:
    """Whether *expr* is a name or a chain of attributes on one (``doc``, ``self.model``)."""
    while isinstance(expr, ast.Attribute):
        expr = expr.value
    return isinstance(expr, ast.Name)
