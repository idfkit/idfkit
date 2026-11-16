"""Run-time stand-ins for the per-version document types.

For a type checker, ``AnyIDFDocument`` (``document.pyi``) and each ``IDFDocumentV<major>_<minor>``
(``versioned.pyi``) are distinct classes: each carries the object types and fields of its
EnergyPlus version. At run time there is one document class, :class:`~idfkit.document.IDFDocument`,
and its version is a value read from the file. The stand-ins here connect the two: ``isinstance``
against one holds exactly for a document of its version, which is what
:func:`as_version` checks before it hands a document back under that type.

That ``isinstance`` is this module's mechanism, not the public way to check a release. Pyright
rejects ``isinstance`` against a document type, and the latest release's type has no stand-in:
it is ``IDFDocument``, which every document is an instance of. :func:`as_version` is the check.

A document's version is matched to a release the way its schema is chosen,
by :func:`~idfkit.versions.find_closest_version`: a file states its version with two components
(``Version, 9.0;``), so a document read from one carries patch ``0`` even where the release's is
not (9.0.1).
"""

from __future__ import annotations

import types
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    ForwardRef,
    Literal,
    NoReturn,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    overload,
)

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
        # AnyIDFDocument stands for no single release, so new_document refuses it: point to the tuple form.
        create = (
            "idfkit.new_document(version=...)"
            if cls._energyplus_version is None
            else f"idfkit.new_document({cls.__name__})"
        )
        msg = f"{cls.__name__} is a type for type checkers and is not instantiated; create a document with {create} or load one"
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


def release_for_new_document(version: object, strict: bool) -> tuple[tuple[int, int, int], bool]:
    """The release and strictness of the document :func:`idfkit.new_document` creates for *version*.

    *version* is a release's document type, such as ``IDFDocumentV9_4`` or ``IDFDocumentV9_4[Literal[False]]``:
    the release is the one the type stands for, and the strictness the one its type argument states, else
    *strict*. Anything that is not a class or a parametrized one is handed back as it is, for
    ``new_document`` to report as an unsupported version the way it always has.

    Raises:
        TypeError: If *version* names several releases (a union), no single release (``AnyIDFDocument``),
            ``IDFDocument``, a class that is not one of the release types, or a strictness that contradicts
            *strict*.
    """
    from .document import IDFDocument

    if not isinstance(version, type) and get_origin(version) is None:
        return cast("tuple[int, int, int]", version), strict
    candidates = _candidates(version)
    if len(candidates) != 1:
        msg = f"new_document creates a document of one release, and {version!r} names {len(candidates)}"
        raise TypeError(msg)
    origin, release = _resolve(version)
    if origin is IDFDocument:
        # IDFDocument is also the run-time class of every document, so new_document(type(doc)) would pass
        # it and create a latest-release document typed as doc's release, whatever that release is.
        msg = (
            "new_document does not take IDFDocument: it is the run-time class of every document, so it names "
            "no release here (new_document(type(doc)) would create a latest-release document whatever doc's "
            "release). Call new_document() for the latest release, or pass a release's type from idfkit.versioned"
        )
        raise TypeError(msg)
    if release is None or "_energyplus_version" not in vars(origin):
        what = "stands for no single EnergyPlus release" if release is None else "is a subclass of a release type"
        msg = f"{origin.__name__} {what}; pass a release's type from idfkit.versioned, such as IDFDocumentV9_4"
        raise TypeError(msg)
    stated = _stated_strictness(version)
    if stated is None:
        return release, strict
    if stated and not strict:
        msg = f"strict=False contradicts the document type {version!r}; pass the type alone"
        raise TypeError(msg)
    return release, stated


def _stated_strictness(document_type: object) -> bool | None:
    """The strictness a parametrized document type states, as in ``IDFDocumentV9_4[Literal[False]]``, if any.

    ``Annotated`` is looked through. A type argument that is not one literal ``bool`` (``bool``, ``Any``,
    ``Literal[True, False]``) states none.

    Raises:
        TypeError: If the type argument is a string, which is not evaluated at run time.
    """
    args = get_args(document_type)
    if len(args) != 1:
        return None
    argument = args[0]
    if get_origin(argument) is Annotated:
        argument = get_args(argument)[0]
    if isinstance(argument, (str, ForwardRef)):
        msg = f"{document_type!r}: write the strictness unquoted, as Literal[False]; a string is not read at run time"
        raise TypeError(msg)
    values = get_args(argument) if get_origin(argument) is Literal else ()
    return values[0] if len(values) == 1 and isinstance(values[0], bool) else None


def _candidates(document_type: object) -> tuple[object, ...]:
    """The document types *document_type* names: itself, a tuple's members, or a union's.

    A union is taken as ``isinstance`` takes one, because pyright accepts
    ``as_version(doc, IDFDocumentV9_6 | IDFDocument)`` (it reads ``A | B`` as ``type[A] | type[B]``),
    so that call has to work when it runs.
    """
    if isinstance(document_type, tuple):
        return cast("tuple[object, ...]", document_type)
    if isinstance(document_type, types.UnionType) or get_origin(document_type) is Union:
        return get_args(document_type)
    return (document_type,)


@overload
def as_version(doc: AnyIDFDocument, document_type: type[_D]) -> _D: ...
@overload
def as_version(doc: AnyIDFDocument, document_type: tuple[type[_D], ...]) -> _D: ...
def as_version(doc: AnyIDFDocument, document_type: type[_D] | tuple[type[_D], ...]) -> _D:
    """Type *doc* as a document of the EnergyPlus version *document_type* stands for, or one of several.

    The stub in ``versioned.pyi`` documents this function; this is its run-time check.
    """
    candidates = _candidates(document_type)
    if not candidates:
        msg = "as_version needs at least one document type"
        raise TypeError(msg)
    resolved = [_resolve(candidate) for candidate in candidates]
    release = find_closest_version(doc.version)
    if any(required is None or required == release for _, required in resolved):
        return cast("_D", doc)
    if len(resolved) == 1:
        origin, required = resolved[0]
        expected = f"not {version_string(cast('tuple[int, int, int]', required))}"
        typed_as = origin.__name__
    else:
        releases = ", ".join(version_string(cast("tuple[int, int, int]", required)) for _, required in resolved)
        expected = f"not one of {releases}"
        typed_as = " | ".join(origin.__name__ for origin, _ in resolved)
    msg = f"The document is EnergyPlus {version_string(doc.version)}, {expected}, so it cannot be typed as {typed_as}"
    raise TypeError(msg)
