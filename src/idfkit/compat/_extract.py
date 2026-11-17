"""AST-based extraction of idfkit-relevant string literals from Python source."""

from __future__ import annotations

import ast

from ._models import ExtractedLiteral, LiteralKind
from ._narrow import ALL_RELEASES, Guard, Narrower, Releases, Scope, ScopeTable, rebinds


def extract_literals(source: str, filename: str = "<unknown>", *, package: str | None = None) -> list[ExtractedLiteral]:
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

    Returns:
        List of :class:`ExtractedLiteral` instances.
    """
    tree = ast.parse(source, filename)
    has_import = _has_idfkit_import(tree, package)
    visitor = _LiteralVisitor(source, tree, has_idfkit_import=has_import)
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


def _end_col(node: ast.expr) -> int:
    """Best-effort end column offset for a node."""
    if node.end_col_offset is not None:
        return node.end_col_offset
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        # +2 for the surrounding quotes (rough fallback)
        return node.col_offset + len(node.value) + 2
    return node.col_offset


class _LiteralVisitor(ast.NodeVisitor):
    """AST visitor that collects idfkit-relevant string literals."""

    def __init__(self, source: str, tree: ast.Module, *, has_idfkit_import: bool) -> None:
        self.literals: list[ExtractedLiteral] = []
        self._source = source
        self._has_idfkit_import = has_idfkit_import
        # Narrowing only applies to a file that imports idfkit; skip the scope walk otherwise.
        self._table = ScopeTable(tree if has_idfkit_import else ast.Module(body=[], type_ignores=[]))
        self._narrower = Narrower(self._table)
        self._scope: Scope = self._table.module
        self._guards: list[Guard] = []

    # ------------------------------------------------------------------
    # Scopes and version guards
    # ------------------------------------------------------------------
    def _visit_scope(self, node: ast.AST) -> None:
        """Visit a function, lambda or class body in its own scope, outside every enclosing guard."""
        saved_scope, saved_guards = self._scope, self._guards
        self._scope, self._guards = self._table.scope_for(node, saved_scope), []
        try:
            self.generic_visit(node)
        finally:
            self._scope, self._guards = saved_scope, saved_guards

    visit_FunctionDef = _visit_scope
    visit_AsyncFunctionDef = _visit_scope
    visit_Lambda = _visit_scope
    visit_ClassDef = _visit_scope

    def visit_If(self, node: ast.If) -> None:
        self.visit(node.test)
        if not self._has_idfkit_import:
            self._visit_block(node.body, [])
            self._visit_block(node.orelse, [])
            return
        conjuncts = [
            g for g in self._narrower.guard_conjuncts(node.test, self._scope) if not rebinds(node.body, g.document)
        ]
        self._visit_block(node.body, conjuncts)
        whole = self._narrower.guard(node.test, self._scope)
        negated: list[Guard] = []
        if whole is not None and not rebinds(node.orelse, whole.document):
            negated = [whole.negated()]
        self._visit_block(node.orelse, negated)

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
        """The receiver as the author wrote it, so a suggested fix reads like their code."""
        return ast.get_source_segment(self._source, receiver) or ast.unparse(receiver)

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

    def _handle_add_call(self, node: ast.Call, func: ast.Attribute) -> None:
        receiver = func.value
        if not node.args:
            return
        first_arg = node.args[0]
        if not (isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str)):
            return

        obj_type_value: str = first_arg.value
        receiver_text = self._receiver_text(receiver)
        releases = self._releases(receiver)

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
            )
        )

        # Extract choice values from keyword arguments
        for kw in node.keywords:
            if kw.arg is not None and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                self.literals.append(
                    ExtractedLiteral(
                        value=kw.value.value,
                        kind=LiteralKind.CHOICE_VALUE,
                        line=kw.value.lineno,
                        col=kw.value.col_offset,
                        end_col=_end_col(kw.value),
                        obj_type=obj_type_value,
                        field_name=kw.arg,
                        receiver=receiver_text,
                        releases=releases,
                    )
                )

        # Extract choice values from a dict-literal third positional arg.
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
