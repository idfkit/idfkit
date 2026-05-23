"""Static validator for fenced ``python`` blocks in agent reference docs.

Catches the kinds of API drift that have bitten us before:

- imports that name idfkit symbols which no longer exist,
- attribute access on imported names (classes, modules, enums) that
  doesn't resolve — typo'd enum members, deleted classmethods, etc.,
- calls with keyword arguments that aren't in the target signature.

What this does NOT check:

- Types of argument values (e.g. ``set_wwr(wwr={...})`` looks fine to
  this validator because ``wwr`` is a valid kwarg name).
- Methods on instances whose type cannot be inferred. We handle the
  two common patterns ``x = Class(...)`` and
  ``x = Class.classmethod(...)`` (when the classmethod's return
  annotation names the class). Anything else (``x = func(...)``,
  ``x = obj.method(...)``) is left alone.
- Blocks that need optional dependencies absent from the dev env.

Add ``<!-- skip-check -->`` on the line before a fence to opt that
block out of validation.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import re
from pathlib import Path

import pytest

_REFS_DIR = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "idfkit"
    / ".agents"
    / "skills"
    / "developing-with-idfkit"
    / "references"
)
_FENCE_RE = re.compile(r"^```python\n(.*?)^```", re.DOTALL | re.MULTILINE)
_SKIP_MARKER = "<!-- skip-check -->"
_IDFKIT_PREFIX = "idfkit"


def _discover_blocks() -> list[tuple[str, str]]:
    if not _REFS_DIR.is_dir():
        return []
    blocks: list[tuple[str, str]] = []
    for md in sorted(_REFS_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        for match in _FENCE_RE.finditer(text):
            window = text[max(0, match.start() - 80) : match.start()]
            if _SKIP_MARKER in window:
                continue
            line_no = text[: match.start()].count("\n") + 1
            blocks.append((f"{md.name}:{line_no}", match.group(1)))
    return blocks


_BLOCKS = _discover_blocks()


def _resolve_imports(tree: ast.AST) -> tuple[dict[str, object], list[str]]:  # noqa: C901
    """Build a name → object map from ``Import`` / ``ImportFrom`` nodes.

    Returns the namespace and a list of import errors. Only failures
    that touch ``idfkit`` (its absence would be a real bug) are
    reported; missing optional third-party libraries are silently
    skipped.
    """
    namespace: dict[str, object] = {}
    errors: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            try:
                module = importlib.import_module(node.module)
            except ImportError as exc:
                if node.module.startswith(_IDFKIT_PREFIX):
                    errors.append(f"import {node.module}: {exc}")
                continue
            for alias in node.names:
                if alias.name == "*":
                    continue
                if not hasattr(module, alias.name):
                    if node.module.startswith(_IDFKIT_PREFIX):
                        errors.append(f"{node.module}: no attribute {alias.name!r}")
                    continue
                namespace[alias.asname or alias.name] = getattr(module, alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                try:
                    module = importlib.import_module(alias.name)
                except ImportError as exc:
                    if alias.name.startswith(_IDFKIT_PREFIX):
                        errors.append(f"import {alias.name}: {exc}")
                    continue
                namespace[alias.asname or alias.name.partition(".")[0]] = module
    return namespace, errors


def _propagate_assignments(tree: ast.AST, namespace: dict[str, object]) -> None:  # noqa: C901
    """Extend the namespace with ``x = Class(...)`` and ``x = Class.cm(...)``.

    The latter only fires when the classmethod's return annotation names
    the owner class — covering the common ``from_*`` factory pattern.
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or not isinstance(node.value, ast.Call):
            continue
        rhs = node.value
        cls: object | None = None
        if isinstance(rhs.func, ast.Name) and rhs.func.id in namespace:
            candidate = namespace[rhs.func.id]
            if inspect.isclass(candidate):
                cls = candidate
        elif (
            isinstance(rhs.func, ast.Attribute)
            and isinstance(rhs.func.value, ast.Name)
            and rhs.func.value.id in namespace
        ):
            owner = namespace[rhs.func.value.id]
            if inspect.isclass(owner):
                method = getattr(owner, rhs.func.attr, None)
                if method is not None:
                    try:
                        ret = inspect.signature(method).return_annotation
                    except (TypeError, ValueError):
                        ret = inspect.Parameter.empty
                    if ret is owner or (isinstance(ret, str) and ret == owner.__name__):
                        cls = owner
        if cls is not None:
            namespace[target.id] = cls


def _kwarg_errors(callable_obj: object, call: ast.Call) -> list[str]:
    if any(kw.arg is None for kw in call.keywords):
        return []  # **dict unpacking; skip
    try:
        sig = inspect.signature(callable_obj)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return []
    if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()):
        return []
    valid = {p.name for p in sig.parameters.values()} - {"self", "cls"}
    return [f"unknown kwarg {kw.arg!r}; valid: {sorted(valid)}" for kw in call.keywords if kw.arg not in valid]


def _validate(tree: ast.AST, namespace: dict[str, object]) -> list[str]:
    errors: list[str] = []
    call_func_ids = {id(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)}

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            target, label = _resolve(node.func, namespace)
            if label and target is _MISSING:
                errors.append(f"{label}: attribute does not exist")
                continue
            if target is None or target is _MISSING:
                continue
            errors.extend(f"{label}: {e}" for e in _kwarg_errors(target, node))
        elif (
            isinstance(node, ast.Attribute)
            and id(node) not in call_func_ids
            and isinstance(node.value, ast.Name)
            and node.value.id in namespace
        ):
            owner = namespace[node.value.id]
            if not hasattr(owner, node.attr):
                errors.append(f"{node.value.id}.{node.attr}: attribute does not exist")
    return errors


_MISSING: object = object()


def _resolve(func: ast.AST, namespace: dict[str, object]) -> tuple[object | None, str]:
    """Resolve a callable expression to (object_or_None_or_MISSING, label)."""
    if isinstance(func, ast.Name) and func.id in namespace:
        return namespace[func.id], func.id
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id in namespace:
        owner = namespace[func.value.id]
        label = f"{func.value.id}.{func.attr}"
        if not hasattr(owner, func.attr):
            return _MISSING, label
        return getattr(owner, func.attr), label
    return None, ""


@pytest.mark.skipif(not _BLOCKS, reason="no reference docs found in source tree")
@pytest.mark.parametrize(("block_id", "code"), _BLOCKS, ids=[b[0] for b in _BLOCKS])
def test_reference_block(block_id: str, code: str) -> None:
    """Each ```python block must syntactically parse and reference real APIs."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        pytest.fail(f"{block_id} syntax error: {exc}\n--- snippet ---\n{code}")

    namespace, import_errors = _resolve_imports(tree)
    _propagate_assignments(tree, namespace)
    errors = import_errors + _validate(tree, namespace)
    if errors:
        bullets = "\n  - ".join(errors)
        pytest.fail(f"{block_id}:\n  - {bullets}\n--- snippet ---\n{code}")
