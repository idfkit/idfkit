"""AST-based extraction of idfkit-relevant string literals from Python source."""

from __future__ import annotations

import ast

from ._models import ExtractedLiteral, LiteralKind


def extract_literals(source: str, filename: str = "<unknown>") -> list[ExtractedLiteral]:
    """Parse *source* as Python and extract high-confidence idfkit literals.

    Detected patterns (constant string literals only):

    * ``something.add("ObjectType", ...)`` -- first positional arg is an object type.
    * ``something.add("ObjectType", field="value")`` -- keyword string values are
      potential choice values for that object type.
    * ``something.add("ObjectType", "Name", {"field": "value"})`` -- string values
      in a dict literal third argument are potential choice values.
    * ``something["ObjectType"]`` -- subscript access (only when the file imports
      from ``idfkit``).

    Dynamic strings, f-strings, and variable references are ignored.

    Args:
        source: Python source code to analyse.
        filename: File path used in extracted literal records.

    Returns:
        List of :class:`ExtractedLiteral` instances.
    """
    tree = ast.parse(source, filename)
    has_import = _has_idfkit_import(tree)
    visitor = _LiteralVisitor(has_idfkit_import=has_import)
    visitor.visit(tree)
    return visitor.literals


def _has_idfkit_import(tree: ast.Module) -> bool:
    """Return True if the AST contains any ``import idfkit`` or ``from idfkit import ...``."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "idfkit" or alias.name.startswith("idfkit."):
                    return True
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module
            and (node.module == "idfkit" or node.module.startswith("idfkit."))
        ):
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

    def __init__(self, *, has_idfkit_import: bool) -> None:
        self.literals: list[ExtractedLiteral] = []
        self._has_idfkit_import = has_idfkit_import

    # ------------------------------------------------------------------
    # Pattern: something.add("ObjectType", ...)
    # ------------------------------------------------------------------
    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Attribute) and node.func.attr == "add":
            self._handle_add_call(node)
        self.generic_visit(node)

    def _handle_add_call(self, node: ast.Call) -> None:
        if not node.args:
            return
        first_arg = node.args[0]
        if not (isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str)):
            return

        obj_type_value: str = first_arg.value

        self.literals.append(
            ExtractedLiteral(
                value=obj_type_value,
                kind=LiteralKind.OBJECT_TYPE,
                line=first_arg.lineno,
                col=first_arg.col_offset,
                end_col=_end_col(first_arg),
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
                )
            )
        self.generic_visit(node)
