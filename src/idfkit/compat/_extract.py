"""AST-based extraction of idfkit-relevant string literals from Python source."""

from __future__ import annotations

import ast
import re
from functools import lru_cache
from typing import Literal

from ._models import ExtractedLiteral, LiteralKind
from ._narrow import ALL_RELEASES, DocumentRef, Guard, Narrower, Releases, Scope, ScopeTable, escapes, rebinds


def extract_literals(
    source: str,
    filename: str = "<unknown>",
    *,
    package: str | None = None,
    version: tuple[int, int, int] | None = None,
) -> list[ExtractedLiteral]:
    """Parse *source* as Python and extract high-confidence idfkit literals.

    Detected patterns (constant string literals only):

    * ``something.add("ObjectType", ...)`` -- first positional arg is an object type.
    * ``something.add("ObjectType", field="value")`` -- keyword string values are
      potential choice values for that object type.
    * ``something.add("ObjectType", "Name", {"field": "value"})`` -- string values
      in a dict literal third argument are potential choice values.
    * ``something.get_collection("ObjectType")`` -- the argument (positional or
      ``obj_type=``) is an object type (only when the file imports from ``idfkit``:
      other libraries, pymongo among them, have a ``get_collection`` too).
    * ``something["ObjectType"]`` -- subscript access (only when the file imports
      from ``idfkit``).

    Dynamic strings, f-strings, and variable references are ignored.

    Each literal records the releases its code can run against when the code around it narrows
    the document (an ``as_version`` receiver, or an enclosing ``if doc.version >= (9, 4, 0):``);
    :mod:`idfkit.compat._narrow` lists exactly what is recognised.

    Args:
        source: Python source code to analyse.
        filename: File path used in extracted literal records.
        package: The dotted package the file belongs to (``"idfkit.simulation"`` for
            ``src/idfkit/simulation/expand.py``), used to resolve relative imports: inside idfkit's
            own source, ``from .document import ...`` is an idfkit import. ``None`` treats every
            relative import as foreign.
        version: The release whose schema names object types and document accessors when the
            receiver of an ``add()`` call is classified (``doc.zones`` is a collection). ``None``
            uses the latest supported release; ``check_compatibility`` passes its newest target,
            whose schema it has loaded already.

    Returns:
        List of :class:`ExtractedLiteral` instances.
    """
    tree = ast.parse(source, filename)
    has_import = _has_idfkit_import(tree, package)
    visitor = _LiteralVisitor(source, tree, has_idfkit_import=has_import, version=version)
    visitor.visit(tree)
    return visitor.literals


def _is_idfkit_module(name: str) -> bool:
    return name == "idfkit" or name.startswith("idfkit.")


def _resolve_relative(node: ast.ImportFrom, package: str | None) -> str | None:
    """The absolute module a relative ``from . import`` names, or ``None`` when it cannot be known."""
    if package is None:
        return None
    parts = package.split(".")
    if node.level - 1 >= len(parts):
        return None
    base = parts[: len(parts) - (node.level - 1)]
    return ".".join([*base, node.module] if node.module else base)


def _has_idfkit_import(tree: ast.Module, package: str | None = None) -> bool:
    """Return True if the AST imports from idfkit, absolutely or relatively from inside it."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(_is_idfkit_module(alias.name) for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.level == 0 else _resolve_relative(node, package)
            if module and _is_idfkit_module(module):
                return True
    return False


_LINE_RE = re.compile(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+\Z")


def _splitlines_no_ff(source: str) -> list[str]:
    """Split *source* into lines as the tokenizer does (form feeds do not end a line), keeping ends."""
    return _LINE_RE.findall(source)


def _end_col(node: ast.expr) -> int:
    """Best-effort end column offset for a node."""
    if node.end_col_offset is not None:
        return node.end_col_offset
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        # +2 for the surrounding quotes (rough fallback)
        return node.col_offset + len(node.value) + 2
    return node.col_offset


# Calls whose result is a document with a schema: a name bound once to one, or a parameter annotated
# with a document type, is a document receiver (see _LiteralVisitor._receiver). IDFDocument() is not
# one: constructed without a schema, it accepts any type name.
_DOCUMENT_FACTORIES = frozenset({
    "new_document",
    "load_idf",
    "load_epjson",
    "parse_idf",
    "parse_epjson",
    "as_version",
})

# Annotations and constructors of a mapping: a subscript of one is a value, not a collection.
_MAPPING_HEADS = frozenset({
    "dict",
    "Dict",
    "Mapping",
    "MutableMapping",
    "defaultdict",
    "DefaultDict",
    "OrderedDict",
    "ChainMap",
})

_ReceiverKind = Literal["document", "collection", "unknown"]


def _latest() -> tuple[int, int, int]:
    from ..versions import LATEST_VERSION

    return LATEST_VERSION


@lru_cache(maxsize=4096)
def _accessor_type(attr: str, version: tuple[int, int, int], *, exact: bool) -> str | None:
    """The object type a document attribute names in *version*'s schema, or ``None``.

    With *exact*, only the typed accessors count (``zones``, ``building_surfaces``, ``building``):
    the case-insensitive raw spelling (``zone`` for ``Zone``) is a common variable name too.
    """
    if attr.startswith("_"):
        return None
    from ..document import _build_resolver  # pyright: ignore[reportPrivateUsage]
    from ..schema import get_schema

    resolver = get_schema(version).accessor_resolver(_build_resolver)
    if exact:
        return resolver.accessors().get(attr)
    return resolver.resolve(attr)


@lru_cache(maxsize=4096)
def _is_singleton(obj_type: str, version: tuple[int, int, int]) -> bool:
    """Whether a model holds at most one object of *obj_type* (``Building``, ``Version``, ...)."""
    from ..schema import get_schema

    schema = get_schema(version).get_object_schema(obj_type)
    return schema is not None and schema.get("maxProperties") == 1


@lru_cache(maxsize=4096)
def _is_object_type(key: str, version: tuple[int, int, int]) -> bool:
    """Whether *key* names an object type of *version*'s schema, in any case."""
    from ..schema import get_schema

    return get_schema(version).resolve_type_name(key) is not None


def _call_name(node: ast.Call) -> str | None:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _head(expr: ast.expr) -> str:
    """The unqualified name an annotation member starts with: ``IDFCollection`` for ``ok.IDFCollection[Zone]``."""
    while isinstance(expr, ast.Subscript):
        expr = expr.value
    if isinstance(expr, ast.Attribute):
        return expr.attr
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Constant) and expr.value is None:
        return "None"
    return ""


def _union_members(expr: ast.expr) -> list[ast.expr]:
    """The members of ``A | B``, ``Union[A, B]`` and ``Optional[A]``; ``[expr]`` for anything else."""
    if isinstance(expr, ast.BinOp) and isinstance(expr.op, ast.BitOr):
        return [*_union_members(expr.left), *_union_members(expr.right)]
    if isinstance(expr, ast.Subscript) and _head(expr.value) in ("Union", "Optional"):
        inner = expr.slice
        members = list(inner.elts) if isinstance(inner, ast.Tuple) else [inner]
        return [m for e in members for m in _union_members(e)]
    return [expr]


def _annotation_expr(annotation: ast.expr | None) -> ast.expr | None:
    """*annotation*, with a string annotation parsed."""
    if isinstance(annotation, ast.Constant) and isinstance(annotation.value, str):
        try:
            return ast.parse(annotation.value, mode="eval").body
        except SyntaxError:
            return None
    return annotation


def _annotation_kind(annotation: ast.expr | None) -> _ReceiverKind:
    """What a parameter annotated *annotation* is: a document, ``IDFCollection[...]``, or unknown.

    A union counts only when every member but ``None`` is of one kind: ``IDFDocument | None`` is a
    document, ``IDFDocument | IDFCollection[Zone]`` unknown.
    """
    expr = _annotation_expr(annotation)
    if expr is None:
        return "unknown"
    kinds: set[_ReceiverKind] = set()
    for member in _union_members(expr):
        head = _head(member)
        if head == "None":
            continue
        if head == "IDFCollection":
            kinds.add("collection")
        elif "IDFDocument" in head:
            kinds.add("document")
        else:
            kinds.add("unknown")
    return kinds.pop() if len(kinds) == 1 else "unknown"


def _annotation_is_mapping(annotation: ast.expr | None) -> bool:
    expr = _annotation_expr(annotation)
    return expr is not None and any(_head(m) in _MAPPING_HEADS for m in _union_members(expr))


def _passes_validate_false(node: ast.Call) -> bool:
    """Whether an ``add()`` call passes ``validate=False``, which stores values unchecked."""
    return any(
        kw.arg == "validate" and isinstance(kw.value, ast.Constant) and kw.value.value is False for kw in node.keywords
    )


class _LiteralVisitor(ast.NodeVisitor):
    """AST visitor that collects idfkit-relevant string literals."""

    def __init__(
        self,
        source: str,
        tree: ast.Module,
        *,
        has_idfkit_import: bool,
        version: tuple[int, int, int] | None = None,
    ) -> None:
        self.literals: list[ExtractedLiteral] = []
        self._version = version or _latest()
        self._source = source
        self._has_idfkit_import = has_idfkit_import
        # Narrowing only applies to a file that imports idfkit; skip the scope walk otherwise.
        self._table = ScopeTable(tree if has_idfkit_import else ast.Module(body=[], type_ignores=[]))
        self._narrower = Narrower(self._table)
        self._scope: Scope = self._table.module
        self._guards: list[Guard] = []
        self._lines: list[str] | None = None
        # Whether a statement rebinds a document, keyed by (statement, document bases): an elif
        # chain asks this of every tail of the chain, which would otherwise be quadratic.
        self._rebinds_memo: dict[tuple[int, frozenset[str]], bool] = {}
        # Parameter annotations of each function scope, by id(scope), read by _receiver.
        self._annotations: dict[int, dict[str, ast.expr | None]] = {}

    # ------------------------------------------------------------------
    # Scopes and version guards
    # ------------------------------------------------------------------
    def _visit_scope(self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda | ast.ClassDef) -> None:
        """Visit a function, lambda or class body in its own scope, outside every enclosing guard.

        Decorators, argument defaults, annotations, class bases and keywords are evaluated where
        the definition runs, so they are visited first, in the enclosing scope and under its guards.
        """
        outer: list[ast.AST]
        inner: list[ast.AST]
        if isinstance(node, ast.ClassDef):
            outer = [*node.decorator_list, *node.bases, *node.keywords]
            inner = list(node.body)
        else:
            args = node.args
            all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs, args.vararg, args.kwarg]
            outer = [*args.defaults, *(d for d in args.kw_defaults if d is not None)]
            if isinstance(node, ast.Lambda):
                inner = [node.body]
            else:
                outer[:0] = node.decorator_list
                outer += [a.annotation for a in all_args if a is not None and a.annotation is not None]
                if node.returns is not None:
                    outer.append(node.returns)
                inner = list(node.body)
        for child in outer:
            self.visit(child)
        saved_scope, saved_guards = self._scope, self._guards
        self._scope, self._guards = self._table.scope_for(node, saved_scope), []
        if not isinstance(node, ast.ClassDef):
            params = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
            self._annotations[id(self._scope)] = {a.arg: a.annotation for a in params}
        try:
            for child in inner:
                self.visit(child)
        finally:
            self._scope, self._guards = saved_scope, saved_guards

    visit_FunctionDef = _visit_scope
    visit_AsyncFunctionDef = _visit_scope
    visit_Lambda = _visit_scope
    visit_ClassDef = _visit_scope

    def visit_If(self, node: ast.If) -> None:
        # An elif chain is an If nested in the orelse of the one before. It is walked in a loop,
        # not by recursion, so a long chain neither overflows the stack nor costs quadratic time.
        saved = self._guards
        current: ast.If | None = node
        try:
            while current is not None:
                self.visit(current.test)
                if not self._has_idfkit_import:
                    conjuncts: list[Guard] = []
                    negated: list[Guard] = []
                else:
                    conjuncts = [
                        g
                        for g in self._narrower.guard_conjuncts(current.test, self._scope)
                        if not self._unsound(g.document, current.body)
                    ]
                    whole = self._narrower.guard(current.test, self._scope)
                    negated = []
                    if whole is not None and not self._unsound(whole.document, current.orelse):
                        negated = [whole.negated()]
                self._visit_block(current.body, conjuncts)
                orelse = current.orelse
                if len(orelse) == 1 and isinstance(orelse[0], ast.If):
                    self._guards = [*self._guards, *negated]
                    current = orelse[0]
                else:
                    self._visit_block(orelse, negated)
                    current = None
        finally:
            self._guards = saved

    def _unsound(self, document: DocumentRef, body: list[ast.stmt]) -> bool:
        """Whether a guard on *document* cannot be trusted inside *body*."""
        return escapes(document, self._table) or any(self._stmt_rebinds(stmt, document) for stmt in body)

    def _stmt_rebinds(self, stmt: ast.stmt, document: DocumentRef) -> bool:
        """``rebinds([stmt], document)``, computed once per elif-chain link, bottom-up."""
        chain: list[ast.stmt] = [stmt]
        while True:
            last = chain[-1]
            if not (isinstance(last, ast.If) and len(last.orelse) == 1 and isinstance(last.orelse[0], ast.If)):
                break
            if (id(last.orelse[0]), document.bases) in self._rebinds_memo:
                break
            chain.append(last.orelse[0])
        for link in reversed(chain):
            key = (id(link), document.bases)
            if key in self._rebinds_memo:
                continue
            if isinstance(link, ast.If):
                tail = link.orelse
                if len(tail) == 1 and isinstance(tail[0], ast.If):
                    tail_rebinds = self._rebinds_memo[(id(tail[0]), document.bases)]
                else:
                    tail_rebinds = rebinds(tail, document)
                result = rebinds([ast.Expr(value=link.test)], document) or rebinds(link.body, document) or tail_rebinds
            else:
                result = rebinds([link], document)
            self._rebinds_memo[key] = result
        return self._rebinds_memo[(id(stmt), document.bases)]

    def _visit_comprehension(self, node: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp) -> None:
        """Visit a comprehension in the scope it runs in.

        Only its first iterable is evaluated in the enclosing scope. The rest runs in the
        comprehension's own scope, which, like a function's, does not see the names of an
        enclosing class body. A generator also runs when it is consumed, perhaps after the guard
        around it stopped holding, so its body is visited outside every guard.
        """
        first = node.generators[0]
        self.visit(first.iter)
        saved_scope, saved_guards = self._scope, self._guards
        if self._scope.is_class and self._scope.parent is not None:
            self._scope = self._scope.parent
        if isinstance(node, ast.GeneratorExp):
            self._guards = []
        body: list[ast.AST] = [first.target, *first.ifs, *node.generators[1:]]
        body += [node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]
        try:
            for child in body:
                self.visit(child)
        finally:
            self._scope, self._guards = saved_scope, saved_guards

    visit_ListComp = _visit_comprehension
    visit_SetComp = _visit_comprehension
    visit_DictComp = _visit_comprehension
    visit_GeneratorExp = _visit_comprehension

    def _visit_block(self, body: list[ast.stmt], guards: list[Guard]) -> None:
        saved = self._guards
        self._guards = [*saved, *guards]
        try:
            for stmt in body:
                self.visit(stmt)
        finally:
            self._guards = saved

    def _releases(self, receiver: ast.expr | None) -> Releases | None:
        """The releases a lookup on *receiver* can run against here, or ``None`` for all of them."""
        if receiver is None or not self._has_idfkit_import:
            return None
        document = self._narrower.document(receiver, self._scope)
        releases = document.releases
        for guard in self._guards:
            if guard.document.bases & document.bases:
                releases = guard.narrow(releases if releases is not None else ALL_RELEASES)
        return None if releases == ALL_RELEASES else releases

    def _receiver_text(self, receiver: ast.expr) -> str:
        """The receiver as the author wrote it, so a suggested fix reads like their code.

        A receiver spread over several lines is normalised, so a diagnostic stays on one line, and
        one that is not a primary (``a or b``, ``await load()``) is parenthesised, so appending
        ``["Zone"]`` or ``.get_collection(...)`` to it keeps its meaning.
        """
        segment = self._segment(receiver) if receiver.lineno == receiver.end_lineno else None
        text = segment or ast.unparse(receiver)
        if not isinstance(receiver, (ast.Name, ast.Attribute, ast.Call, ast.Subscript)):
            text = f"({text})"
        return text

    def _segment(self, node: ast.expr) -> str | None:
        """``ast.get_source_segment`` over lines split once per file, not once per call."""
        if node.end_lineno is None or node.end_col_offset is None:
            return None
        if self._lines is None:
            self._lines = _splitlines_no_ff(self._source)
        lines = self._lines
        first, last = node.lineno - 1, node.end_lineno - 1
        if last >= len(lines):
            return None
        if first == last:
            return lines[first].encode()[node.col_offset : node.end_col_offset].decode()
        head = lines[first].encode()[node.col_offset :].decode()
        tail = lines[last].encode()[: node.end_col_offset].decode()
        return "".join([head, *lines[first + 1 : last], tail])

    # ------------------------------------------------------------------
    # Pattern: something.add("ObjectType", ...)
    # ------------------------------------------------------------------
    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Attribute) and node.func.attr == "add":
            self._handle_add_call(node, node.func)
        elif self._has_idfkit_import and isinstance(node.func, ast.Attribute) and node.func.attr == "get_collection":
            self._handle_get_collection_call(node, node.func)
        self.generic_visit(node)

    # ------------------------------------------------------------------
    # Pattern: something.get_collection("ObjectType")
    # ------------------------------------------------------------------
    def _handle_get_collection_call(self, node: ast.Call, func: ast.Attribute) -> None:
        arg: ast.expr | None = node.args[0] if node.args else None
        if arg is None:
            arg = next((kw.value for kw in node.keywords if kw.arg == "obj_type"), None)
        if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
            return
        self.literals.append(
            ExtractedLiteral(
                value=arg.value,
                kind=LiteralKind.OBJECT_TYPE,
                line=arg.lineno,
                col=arg.col_offset,
                end_col=_end_col(arg),
                call="get_collection",
                receiver=self._receiver_text(func.value),
                releases=self._releases(func.value),
            )
        )

    def _receiver(
        self, expr: ast.expr, scope: Scope, depth: int = 0
    ) -> tuple[_ReceiverKind, str | None, ast.expr | None, Scope | None]:
        """What the receiver of an ``add()`` call is known to be.

        ``doc.add("Zone", "Office")`` takes an object type first, and a collection's
        ``doc.zones.add("Office")`` a name, so the two must not be confused. A receiver is a
        collection when it is ``doc["Zone"]`` (a key that names an object type, or any key on a
        receiver known to be a document: ``docs["base"]`` may be a document held in a dict), a
        document accessor (``doc.zones``), ``doc.get_collection("Zone")``, a name bound once to one
        of those, or a parameter annotated ``IDFCollection[...]``; the object type is returned when
        it can be read. It is a document when it is a call that returns one (``new_document()``,
        ``load_idf(...)``, ``as_version(...)``), a name bound once to one, or a parameter annotated
        with a document type. Anything else is unknown. The third item is the document expression a
        collection was read from, when it means the same in *scope*, for narrowing.
        """
        if depth > 8:
            return "unknown", None, None, None
        if isinstance(expr, ast.Subscript):
            return self._receiver_of_subscript(expr, scope, depth)
        if isinstance(expr, ast.Attribute):
            return self._receiver_of_attribute(expr, scope, depth)
        if isinstance(expr, ast.Call):
            return self._receiver_of_call(expr, scope, depth)
        if isinstance(expr, ast.Name):
            return self._receiver_of_name(expr, scope, depth)
        return "unknown", None, None, None

    def _receiver_of_subscript(
        self, expr: ast.Subscript, scope: Scope, depth: int
    ) -> tuple[_ReceiverKind, str | None, ast.expr | None, Scope | None]:
        """``doc["Zone"]``: a collection when the key names an object type and the base can be a document.

        On a base known to be a document, any string key is a collection (``doc["zone"]``). On a
        base known to be a mapping (a name bound to a dict, or annotated ``dict[...]``), the item is
        a value, which may be a document held under a key such as ``"Window"``.
        """
        key = expr.slice
        if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
            return "unknown", None, None, None
        base = self._receiver(expr.value, scope, depth + 1)[0]
        if base == "document" or (
            _is_object_type(key.value, self._version) and not self._is_mapping(expr.value, scope)
        ):
            return "collection", key.value, expr.value, None
        return "unknown", None, None, None

    def _receiver_of_attribute(
        self, expr: ast.Attribute, scope: Scope, depth: int
    ) -> tuple[_ReceiverKind, str | None, ast.expr | None, Scope | None]:
        """``doc.zones``: a collection when the attribute is a document accessor and the base can be a document.

        On a base known to be a document every accessor spelling counts. On any other base only the
        typed accessors do, and not one of a type a model holds at most one of: ``self.building``
        or ``app.version`` is as likely to hold a document or a value as the ``Building`` collection.
        """
        if self._receiver(expr.value, scope, depth + 1)[0] == "document":
            obj_type = _accessor_type(expr.attr, self._version, exact=False)
        else:
            obj_type = _accessor_type(expr.attr, self._version, exact=True)
            if obj_type is not None and _is_singleton(obj_type, self._version):
                obj_type = None
        if obj_type is not None:
            return "collection", obj_type, expr.value, None
        return "unknown", None, None, None

    def _is_mapping(self, expr: ast.expr, scope: Scope) -> bool:
        """Whether *expr* is known to be a mapping: a name bound once to a dict, or annotated as one."""
        if not isinstance(expr, ast.Name):
            return False
        bound = self._table.value_of(expr.id, scope)
        if bound is not None:
            value = bound[0]
            return isinstance(value, (ast.Dict, ast.DictComp)) or (
                isinstance(value, ast.Call) and _call_name(value) in _MAPPING_HEADS
            )
        owner = self._table.lookup(expr.id, scope)
        return owner is not None and _annotation_is_mapping(self._annotations.get(id(owner), {}).get(expr.id))

    def _receiver_of_call(
        self, expr: ast.Call, scope: Scope, depth: int
    ) -> tuple[_ReceiverKind, str | None, ast.expr | None, Scope | None]:
        name = _call_name(expr)
        if name == "get_collection" and isinstance(expr.func, ast.Attribute):
            arg = expr.args[0] if expr.args else next((kw.value for kw in expr.keywords if kw.arg == "obj_type"), None)
            obj_type = arg.value if isinstance(arg, ast.Constant) and isinstance(arg.value, str) else None
            return "collection", obj_type, expr.func.value, None
        if name in _DOCUMENT_FACTORIES:
            return "document", None, None, None
        if name == "copy" and isinstance(expr.func, ast.Attribute):
            inner, _, _, _ = self._receiver(expr.func.value, scope, depth + 1)
            if inner == "document":
                return "document", None, None, None
        return "unknown", None, None, None

    def _receiver_of_name(
        self, expr: ast.Name, scope: Scope, depth: int
    ) -> tuple[_ReceiverKind, str | None, ast.expr | None, Scope | None]:
        bound = self._table.value_of(expr.id, scope)
        if bound is not None:
            kind, obj_type, document, owner = self._receiver(bound[0], bound[1], depth + 1)
            # The document expression is read in the scope it was written in.
            return kind, obj_type, document, owner or bound[1]
        owner = self._table.lookup(expr.id, scope)
        if owner is not None and len(owner.bindings.get(expr.id, [])) == 1:
            return _annotation_kind(self._annotations.get(id(owner), {}).get(expr.id)), None, None, None
        return "unknown", None, None, None

    def _handle_collection_add(
        self,
        node: ast.Call,
        receiver: ast.expr,
        obj_type: str | None,
        document: ast.expr | None,
        owner: Scope | None,
    ) -> None:
        """A collection's ``add(name, **fields)``: the first argument is a name, the keywords its fields."""
        if obj_type is None:
            return
        releases = self._collection_releases(document, owner)
        self._keyword_choice_literals(node, obj_type, self._receiver_text(receiver), releases, in_idfkit_add=True)

    def _collection_releases(self, document: ast.expr | None, owner: Scope | None) -> Releases | None:
        """The releases a collection read from *document* (written in *owner*) can run against here.

        A narrowing in the expression itself (``as_version(doc, since=...)["Zone"]``) holds wherever
        the collection is used. A version guard around the use (``if doc.version >= ...``) narrows
        it only when the document's names mean the same single bindings here as where it was read.
        """
        if document is None:
            return None
        if owner is None or owner is self._scope or self._narrower.same_meaning(document, owner, self._scope):
            return self._releases(document)
        releases = self._narrower.document(document, owner).releases
        return None if releases == ALL_RELEASES else releases

    def _keyword_choice_literals(
        self,
        node: ast.Call,
        obj_type: str,
        receiver_text: str,
        releases: Releases | None,
        *,
        in_idfkit_add: bool,
    ) -> None:
        """Choice values passed by keyword: ``add(..., field="value")``."""
        for kw in node.keywords:
            if kw.arg is not None and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                self.literals.append(
                    ExtractedLiteral(
                        value=kw.value.value,
                        kind=LiteralKind.CHOICE_VALUE,
                        line=kw.value.lineno,
                        col=kw.value.col_offset,
                        end_col=_end_col(kw.value),
                        obj_type=obj_type,
                        field_name=kw.arg,
                        receiver=receiver_text,
                        releases=releases,
                        in_idfkit_add=in_idfkit_add,
                    )
                )

    def _handle_add_call(self, node: ast.Call, func: ast.Attribute) -> None:
        receiver = func.value
        kind: _ReceiverKind = "unknown"
        if self._has_idfkit_import:
            kind, collection_type, document, owner = self._receiver(receiver, self._scope)
            if kind == "collection":
                self._handle_collection_add(node, receiver, collection_type, document, owner)
                return
        if not node.args:
            return
        first_arg = node.args[0]
        if not (isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str)):
            return

        obj_type_value: str = first_arg.value
        receiver_text = self._receiver_text(receiver)
        releases = self._releases(receiver)
        # idfkit's add() is called with a name, fields or both; set.add and its kin take one argument.
        in_idfkit_add = self._has_idfkit_import and len(node.args) + len(node.keywords) > 1
        # A type name no release has is reported (C006) only on a receiver known to be a document,
        # whatever the arity (doc.add("Timestep") is legal): a collection's add() takes a name
        # first, and an unknown receiver may be one.
        type_in_idfkit_add = self._has_idfkit_import and kind == "document"

        self.literals.append(
            ExtractedLiteral(
                value=obj_type_value,
                kind=LiteralKind.OBJECT_TYPE,
                line=first_arg.lineno,
                col=first_arg.col_offset,
                end_col=_end_col(first_arg),
                call="add",
                receiver=receiver_text,
                releases=releases,
                in_idfkit_add=type_in_idfkit_add,
            )
        )

        # With validate=False, add() stores a value outside the choices rather than raising.
        choice_in_idfkit_add = in_idfkit_add and not _passes_validate_false(node)
        self._keyword_choice_literals(node, obj_type_value, receiver_text, releases, in_idfkit_add=choice_in_idfkit_add)
        self._dict_choice_literals(node, obj_type_value, receiver_text, releases, choice_in_idfkit_add)

    def _dict_choice_literals(
        self,
        node: ast.Call,
        obj_type_value: str,
        receiver_text: str | None,
        releases: frozenset[tuple[int, int, int]] | None,
        in_idfkit_add: bool,
    ) -> None:
        """Choice values in a dict literal of ``doc.add("Type", "Name", {"field": "value"})``."""
        # Pattern: doc.add("Type", "Name", {"field": "value", ...})
        dict_arg: ast.Dict | None = None
        if len(node.args) >= 3 and isinstance(node.args[2], ast.Dict):
            dict_arg = node.args[2]
        elif len(node.args) == 2 and isinstance(node.args[1], ast.Dict):
            # Pattern: doc.add("Type", {"field": "value", ...})  (no name)
            dict_arg = node.args[1]

        if dict_arg is not None:
            for key_node, val_node in zip(dict_arg.keys, dict_arg.values, strict=True):
                if (
                    key_node is not None
                    and isinstance(key_node, ast.Constant)
                    and isinstance(key_node.value, str)
                    and isinstance(val_node, ast.Constant)
                    and isinstance(val_node.value, str)
                ):
                    self.literals.append(
                        ExtractedLiteral(
                            value=val_node.value,
                            kind=LiteralKind.CHOICE_VALUE,
                            line=val_node.lineno,
                            col=val_node.col_offset,
                            end_col=_end_col(val_node),
                            obj_type=obj_type_value,
                            field_name=key_node.value,
                            receiver=receiver_text,
                            releases=releases,
                            in_idfkit_add=in_idfkit_add,
                        )
                    )

    # ------------------------------------------------------------------
    # Pattern: doc["ObjectType"]  (only with idfkit import)
    # ------------------------------------------------------------------
    def visit_Subscript(self, node: ast.Subscript) -> None:
        if self._has_idfkit_import and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
            self.literals.append(
                ExtractedLiteral(
                    value=node.slice.value,
                    kind=LiteralKind.OBJECT_TYPE,
                    line=node.slice.lineno,
                    col=node.slice.col_offset,
                    end_col=_end_col(node.slice),
                    receiver=self._receiver_text(node.value),
                    releases=self._releases(node.value),
                )
            )
        self.generic_visit(node)
