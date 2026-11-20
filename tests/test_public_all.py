"""Every public module declares its public API in ``__all__``.

Without ``__all__``, ``from idfkit.geometry import *``, IDE autocompletion and API
documentation tools offer a module's imports and internals (``Any``, ``cast``, ``math``,
``logger``) alongside its real API.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import pkgutil
import re
import sys
from types import ModuleType

import pytest

import idfkit


def _public_module_names() -> list[str]:
    """Every module of ``idfkit`` whose dotted path has no underscore-prefixed part."""
    names = ["idfkit"]
    for info in pkgutil.walk_packages(idfkit.__path__, prefix="idfkit."):
        if any(part.startswith("_") for part in info.name.split(".")):
            continue
        names.append(info.name)
    return sorted(names)


PUBLIC_MODULES = _public_module_names()


def _import(name: str) -> ModuleType:
    """Import *name*, skipping the maintainer tools that need ``tomllib`` on Python 3.10.

    ``idfkit.codegen.generate_conformance`` and ``generate_epw_sentinels`` are documented as
    needing Python 3.11. Any other import failure, and this one on 3.11+, still fails the test.
    """
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as error:
        if sys.version_info < (3, 11) and error.name == "tomllib":
            pytest.skip(f"{name} needs tomllib, which is Python 3.11+ (maintainer tooling)")
        raise


def test_walk_finds_the_public_modules() -> None:
    # A guard against the walk silently finding nothing (a packaging change, a renamed package).
    for expected in ("idfkit.geometry", "idfkit.document", "idfkit.simulation.parsers.sql", "idfkit.weather.station"):
        assert expected in PUBLIC_MODULES


@pytest.mark.parametrize("module_name", PUBLIC_MODULES)
def test_public_module_declares_all(module_name: str) -> None:
    module = _import(module_name)
    assert "__all__" in vars(module), f"{module_name} has no __all__"
    exported = module.__all__
    assert isinstance(exported, (list, tuple)), f"{module_name}.__all__ is a {type(exported).__name__}"
    assert all(isinstance(name, str) for name in exported), f"{module_name}.__all__ holds a non-string"
    duplicates = sorted({name for name in exported if exported.count(name) > 1})
    assert not duplicates, f"{module_name}.__all__ lists {duplicates} more than once"


@pytest.mark.parametrize("module_name", PUBLIC_MODULES)
def test_all_names_exist(module_name: str) -> None:
    module = _import(module_name)
    missing = [name for name in getattr(module, "__all__", ()) if not hasattr(module, name)]
    assert not missing, f"{module_name}.__all__ lists names the module does not have: {missing}"


@pytest.mark.parametrize("module_name", PUBLIC_MODULES)
def test_all_lists_no_private_names(module_name: str) -> None:
    module = _import(module_name)
    private = [name for name in getattr(module, "__all__", ()) if name.startswith("_") and not name.startswith("__")]
    assert not private, f"{module_name}.__all__ lists private names: {private}"


@pytest.mark.parametrize("module_name", PUBLIC_MODULES)
def test_star_import_hides_imports(module_name: str) -> None:
    """``from module import *`` brings in no stdlib helper the module merely imported."""
    _import(module_name)
    namespace: dict[str, object] = {}
    exec(f"from {module_name} import *", namespace)  # noqa: S102
    leaked = sorted({"Any", "cast", "math", "logging", "logger", "dataclass"} & namespace.keys())
    assert not leaked, f"from {module_name} import * leaks {leaked}"


def _relative_imports(package: ModuleType) -> dict[str, str]:
    """``{name: defining module}`` for each ``from .module import name`` in a package's ``__init__``.

    Read from the source rather than from ``__module__``, so constants and type aliases count as
    well as classes and functions.
    """
    source = inspect.getsource(package)
    found: dict[str, str] = {}
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.ImportFrom) or node.level != 1 or node.module is None:
            continue
        home = f"{package.__name__}.{node.module}"
        for alias in node.names:
            found[alias.asname or alias.name] = home
    return found


@pytest.mark.parametrize("module_name", PUBLIC_MODULES)
def test_reexports_are_public_where_defined(module_name: str) -> None:
    """A name a package re-exports is also in the ``__all__`` of the module it is imported from.

    So ``from idfkit.versions import LATEST_VERSION`` is as public as ``from idfkit import LATEST_VERSION``.
    """
    module = _import(module_name)
    if not hasattr(module, "__path__"):
        return
    imported_from = _relative_imports(module)
    problems: list[str] = []
    for name in getattr(module, "__all__", ()):
        home = imported_from.get(name)
        if home is None or home not in PUBLIC_MODULES:
            continue
        if name not in getattr(_import(home), "__all__", ()):
            problems.append(f"{name} (imported from {home})")
    assert not problems, f"{module_name} re-exports names missing from their module's __all__: {problems}"


_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _annotations_of(obj: object) -> list[str]:
    """The annotations a caller of *obj* sees: its signature, or a class's public fields and methods."""
    raw: list[object] = []
    if inspect.isfunction(obj):
        raw.extend(obj.__annotations__.values())
    elif inspect.isclass(obj):
        for klass in obj.__mro__:
            if klass.__module__ != obj.__module__:
                continue
            raw.extend(v for k, v in vars(klass).get("__annotations__", {}).items() if not k.startswith("_"))
            for attr, value in vars(klass).items():
                if attr.startswith("_") and attr != "__init__":
                    continue
                func = value.fget if isinstance(value, property) else getattr(value, "__func__", value)
                if inspect.isfunction(func):
                    raw.extend(func.__annotations__.values())
    return [a if isinstance(a, str) else repr(a) for a in raw]


@pytest.mark.parametrize("module_name", PUBLIC_MODULES)
def test_public_api_types_are_exported(module_name: str) -> None:
    """A class a public name takes, returns or exposes as a field is public where it is defined.

    ``monthly_means()`` returns ``list[MonthlyMean]`` and ``WeatherFile.location`` is an
    ``EpwLocation``, so both belong in ``idfkit.weather.epw.__all__``.
    """
    module = _import(module_name)
    exported = set(getattr(module, "__all__", ()))
    local_classes = {
        name
        for name, value in vars(module).items()
        if inspect.isclass(value) and value.__module__ == module_name and not name.startswith("_")
    }
    unexported = local_classes - exported
    problems: list[str] = []
    for name in sorted(exported):
        obj = getattr(module, name, None)
        if getattr(obj, "__module__", None) != module_name:
            continue
        used = {ident for text in _annotations_of(obj) for ident in _IDENTIFIER.findall(text)} & unexported
        problems.extend(f"{name} uses {hidden}" for hidden in sorted(used))
    assert not problems, f"{module_name}.__all__ leaves out types its public API uses: {problems}"


def test_geometry_dir_example() -> None:
    """The motivating case: geometry's star import is its API, not its imports."""
    import idfkit.geometry as geometry

    namespace: dict[str, object] = {}
    exec("from idfkit.geometry import *", namespace)  # noqa: S102
    assert "Vector3D" in namespace
    assert "calculate_surface_area" in namespace
    for leaked in ("Any", "Callable", "Sequence", "cast", "dataclass", "logging", "math", "pairwise", "logger"):
        assert leaked not in geometry.__all__
        assert leaked not in namespace
