"""Run-time stand-ins for the per-version document types.

For a type checker, ``AnyIDFDocument`` (``document.pyi``) and each ``IDFDocumentV<major>_<minor>``
(``versioned.pyi``) are distinct classes: each carries the object types and fields of its
EnergyPlus version. At run time there is one document class, :class:`~idfkit.document.IDFDocument`,
and its version is a value read from the file. The stand-ins here connect the two: ``isinstance``
against one holds exactly for a document of its version, which is what
:func:`as_version` checks before it hands a document back under that type.

A document's version is matched to a release the way its schema is chosen,
by :func:`~idfkit.versions.find_closest_version`: a file states its version with two components
(``Version, 9.0;``), so a document read from one carries patch ``0`` even where the release's is
not (9.0.1).
"""

from __future__ import annotations

import types
from typing import TYPE_CHECKING, Any, NoReturn, TypeVar, cast, get_origin

from .versions import LATEST_VERSION, find_closest_version, version_string

if TYPE_CHECKING:
    from .document import AnyIDFDocument

_D = TypeVar("_D", bound="AnyIDFDocument")


class DocumentTypeMeta(type):
    """Metaclass of the stand-ins: instance checks compare versions, and construction is refused."""

    _energyplus_version: tuple[int, int, int] | None

    def __instancecheck__(cls, instance: object) -> bool:
        from .document import IDFDocument

        # IDFDocument is a TypedDict-backed class to a type checker, which isinstance refuses.
        if not isinstance(instance, cast("type", IDFDocument)):
            return False
        version = cast("IDFDocument", instance).version
        return cls._energyplus_version is None or find_closest_version(version) == cls._energyplus_version

    def __call__(cls, *args: Any, **kwargs: Any) -> NoReturn:
        msg = (
            f"{cls.__name__} is a type for type checkers and is not instantiated; "
            "create a document with idfkit.new_document(version=...) or load one"
        )
        raise TypeError(msg)

    @property
    def energyplus_version(cls) -> tuple[int, int, int] | None:
        """The version this stand-in stands for; ``None`` for ``AnyIDFDocument``."""
        return cls._energyplus_version


def document_type(name: str, version: tuple[int, int, int]) -> type:
    """Create the run-time stand-in for the document type of *version*.

    Generic in ``Strict``, as the stub's class is, so ``IDFDocumentV9_4[bool]`` evaluates at run time.
    """
    from .document import IDFDocument, Strict

    def fill(namespace: dict[str, Any]) -> None:
        namespace.update({"_energyplus_version": version, "__module__": "idfkit.versioned"})

    # The base is IDFDocument[Strict]. Spelled through Any, because outside a class statement the
    # type variable means nothing to a type checker; the class only has to exist at run time.
    generic: Any = IDFDocument
    return types.new_class(name, (generic[Strict],), {"metaclass": DocumentTypeMeta}, fill)


def _resolve(document_type: Any) -> tuple[type, tuple[int, int, int] | None]:
    """The class *document_type* names, with or without type arguments, and the release it requires."""
    from .document import IDFDocument

    origin = get_origin(document_type) or document_type
    if origin is IDFDocument:
        # IDFDocument is typed for the latest release, while isinstance holds for every document.
        return origin, LATEST_VERSION
    if isinstance(origin, DocumentTypeMeta):
        return origin, origin.energyplus_version
    msg = f"{document_type!r} is not a document type of idfkit.versioned or idfkit.document"
    raise TypeError(msg)


def as_version(doc: AnyIDFDocument, document_type: type[_D]) -> _D:
    """Type *doc* as a document of the EnergyPlus version *document_type* stands for.

    The stub in ``versioned.pyi`` documents this function; this is its run-time check.
    """
    origin, required = _resolve(document_type)
    if required is not None and find_closest_version(doc.version) != required:
        msg = (
            f"The document is EnergyPlus {version_string(doc.version)}, not {version_string(required)}, "
            f"so it cannot be typed as {origin.__name__}"
        )
        raise TypeError(msg)
    return cast("_D", doc)
