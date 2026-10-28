"""Run-time stand-ins for the per-version document types.

For a type checker, ``AnyIDFDocument`` (``document.pyi``) and each ``IDFDocumentV<major>_<minor>``
(``versioned.pyi``) are distinct classes: each carries the object types and fields of its
EnergyPlus version. At run time there is one document class, :class:`~idfkit.document.IDFDocument`,
and its version is a value read from the file. The stand-ins here connect the two: ``isinstance``
against one holds exactly for a document of its version, which is what
:func:`as_version` checks before it hands a document back under that type.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NoReturn, TypeVar, cast

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
        return cls._energyplus_version is None or version == cls._energyplus_version

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
    """Create the run-time stand-in for the document type of *version*."""
    from .document import IDFDocument

    return DocumentTypeMeta(name, (IDFDocument,), {"_energyplus_version": version, "__module__": "idfkit.versioned"})


def _required_version(document_type: type) -> tuple[int, int, int] | None:
    from .document import IDFDocument
    from .versions import LATEST_VERSION

    if document_type is IDFDocument:
        # IDFDocument is typed for the latest release, while isinstance holds for every document.
        return LATEST_VERSION
    if isinstance(document_type, DocumentTypeMeta):
        return document_type.energyplus_version
    msg = f"{document_type!r} is not a document type of idfkit.versioned or idfkit.document"
    raise TypeError(msg)


def as_version(doc: AnyIDFDocument, document_type: type[_D]) -> _D:
    """Type *doc* as a document of the EnergyPlus version *document_type* stands for.

    The stub in ``versioned.pyi`` documents this function; this is its run-time check.
    """
    required = _required_version(document_type)
    if required is not None and doc.version != required:
        have = ".".join(map(str, doc.version))
        want = ".".join(map(str, required))
        msg = f"The document is EnergyPlus {have}, not {want}, so it cannot be typed as {document_type.__name__}"
        raise TypeError(msg)
    return cast("_D", doc)
