"""Run-time stand-ins for the per-version document types.

For a type checker, ``AnyIDFDocument`` (``document.pyi``) and each ``IDFDocumentV<major>_<minor>``
(``versioned.pyi``) are distinct classes: each carries the object types and fields of its
EnergyPlus version. At run time there is one document class, :class:`~idfkit.document.IDFDocument`,
and its version is a value read from the file. The stand-ins here connect the two: ``isinstance``
against one holds exactly for a document of its version, which is what
:func:`as_version` checks before it hands a document back under that type.

That ``isinstance`` is this module's mechanism, not the public way to check a release. The
latest release's type has no stand-in: it is ``IDFDocument``, which every document is an
instance of, so ``isinstance(doc, IDFDocument)`` holds for a document of any release while a type
checker then types it as the latest one. :func:`as_version` is the check.

A document's version is matched to a release the way its schema is chosen,
by :func:`~idfkit.versions.find_closest_version`: a file states its version with two components
(``Version, 9.0;``), so a document read from one carries patch ``0`` even where the release's is
not (9.0.1).
"""

from __future__ import annotations

import functools
import operator
import types
from functools import lru_cache
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

from .versions import (
    ENERGYPLUS_VERSIONS,
    LATEST_VERSION,
    find_closest_version,
    find_release,
    releases_between,
    version_string,
)

if TYPE_CHECKING:
    from typing import TypeAlias

    from typing_extensions import TypeIs

    from .document import AnyIDFDocument

    # What since= and before= take: a release's document type, its number, or its version tuple.
    _Bound: TypeAlias = "type[AnyIDFDocument] | str | tuple[int, int] | tuple[int, int, int]"

_D = TypeVar("_D", bound="AnyIDFDocument")


class DocumentTypeMeta(type):
    """Metaclass of the stand-ins: instance checks compare versions, and construction is refused."""

    _energyplus_version: tuple[int, int, int] | None

    def __instancecheck__(cls, instance: object) -> bool:
        from .document import IDFDocument

        if not isinstance(instance, IDFDocument):
            return False
        version = instance.version
        return cls._energyplus_version is None or find_closest_version(version) == cls._energyplus_version

    def __call__(cls, *args: Any, **kwargs: Any) -> NoReturn:
        # AnyIDFDocument stands for no single release, so new_document refuses it: point to the tuple form.
        # new_document also refuses a subclass of a release's type, so name the release's type it derives from.
        stand_in = next((base for base in cls.__mro__ if "_energyplus_version" in vars(base)), cls)
        create = (
            "idfkit.new_document(version=...)"
            if cls._energyplus_version is None
            else f"idfkit.new_document({stand_in.__name__})"
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


def release_type_var(name: str, *releases: type) -> Any:
    """Create the run-time ``ReleaseDocumentT``: a type variable constrained to the release types.

    Spelled through ``Any`` for the reason ``document_type`` is: the stand-ins are values here, not
    classes a type checker can see, and the type variable only has to exist at run time.
    """
    factory: Any = TypeVar
    return factory(name, *releases)


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


def is_type_form(value: object) -> TypeIs[type[Any]]:
    """Whether *value* names a type (a class, a parametrized one such as ``IDFDocumentV9_4[bool]``, or a union)
    rather than a version value, for the functions that take either: :func:`idfkit.new_document` and ``migrate``.

    A union is not itself a class; the narrowing serves the other branch, where the value is a version.
    """
    return isinstance(value, (type, types.UnionType)) or get_origin(value) is not None


def release_for_new_document(document_type: object, strict: bool) -> tuple[tuple[int, int, int], bool]:
    """The release and strictness of the document :func:`idfkit.new_document` creates for *document_type*.

    The release is the one :func:`release_of` resolves; the strictness the one the type argument states
    (``IDFDocumentV9_4[Literal[False]]``), else *strict*. On top of :func:`release_of`, ``IDFDocument`` is
    refused: it is the run-time class of every document, so ``new_document(type(doc))`` would create a
    latest-release document typed as ``doc``'s release. So is a subclass of a release type, which
    ``new_document`` would type as the subclass while returning an ``IDFDocument``.

    Raises:
        TypeError: As :func:`release_of` does, for ``IDFDocument`` or a subclass of a release type, and for a
            strictness that contradicts *strict*.
    """
    from .document import IDFDocument

    release = release_of(document_type)
    origin, _ = _resolve(document_type)
    if origin is IDFDocument:
        latest_type = f"IDFDocumentV{LATEST_VERSION[0]}_{LATEST_VERSION[1]}"
        msg = (
            "new_document does not take IDFDocument, nor the latest release's type, "
            f"{latest_type}, which is IDFDocument: it is the run-time class of every document, so it names "
            "no release here (new_document(type(doc)) would create a latest-release document whatever doc's "
            "release). Call new_document() for the latest release, or pass an older release's type from "
            "idfkit.versioned"
        )
        raise TypeError(msg)
    if "_energyplus_version" not in vars(origin):
        msg = f"{origin.__name__} is a subclass of a release type; pass a release's type from idfkit.versioned"
        raise TypeError(msg)
    stated = _stated_strictness(document_type)
    if stated is None:
        return release, strict
    if stated and not strict:
        msg = f"strict=False contradicts the document type {document_type!r}; pass the type alone"
        raise TypeError(msg)
    return release, stated


def _stated_strictness(document_type: object) -> bool | None:
    """The strictness a parametrized document type states, as in ``IDFDocumentV9_4[Literal[False]]``, if any.

    ``Annotated`` and type aliases (``type Lax = Literal[False]``, or ``TypeAliasType``) are looked through,
    as a type checker looks through them. A type argument that is not one literal ``bool`` (``bool``,
    ``Any``, ``Literal[True, False]``) states none.

    Raises:
        TypeError: If the type argument is a string, which is not evaluated at run time.
    """
    args = get_args(document_type)
    if len(args) != 1:
        return None
    argument = args[0]
    # Bounded, as `type A = A` is its own value.
    for _ in range(32):
        if get_origin(argument) is Annotated:
            argument = get_args(argument)[0]
        elif type(argument).__name__ == "TypeAliasType" and hasattr(argument, "__value__"):
            # typing.TypeAliasType (3.12+) or typing_extensions'; matched by name, which needs neither.
            argument = argument.__value__
        else:
            break
    if isinstance(argument, (str, ForwardRef)):
        msg = f"{document_type!r}: write the strictness unquoted, as Literal[False]; a string is not read at run time"
        raise TypeError(msg)
    values = get_args(argument) if get_origin(argument) is Literal else ()
    return values[0] if len(values) == 1 and isinstance(values[0], bool) else None


def release_of(document_type: object) -> tuple[int, int, int]:
    """The one release *document_type* stands for, as :func:`as_version` resolves it.

    Raises:
        TypeError: If *document_type* is not a document type, or names no single release:
            ``AnyIDFDocument``, or a union of several types.
    """
    candidates = _candidates(document_type)
    if len(candidates) != 1:
        msg = f"{document_type!r} names {len(candidates)} releases; name one, such as IDFDocumentV9_4"
        raise TypeError(msg)
    origin, release = _resolve(candidates[0])
    if release is None:
        msg = f"{origin.__name__} stands for no single EnergyPlus release; name one, such as IDFDocumentV9_4"
        raise TypeError(msg)
    return release


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


def _release(bound: object, keyword: str) -> tuple[int, int, int]:
    """The supported release *bound* names, for ``since=`` or ``before=``.

    A document type names the release it stands for (``IDFDocument`` the latest). A string
    (``"9.6"``, ``"9.6.0"``) or a version tuple (``(9, 6, 0)``, as ``doc.version`` is) names one by
    number, and is matched to its release line by :func:`~idfkit.versions.find_release`; a number
    newer than every supported release, which a file may degrade to the latest, names no release.
    """
    if isinstance(bound, str):
        parts = bound.split(".")
        if not 2 <= len(parts) <= 3 or not all(part.isdecimal() for part in parts):
            msg = f"{keyword}={bound!r} is not a release: give {_BOUND_FORMS}"
            raise ValueError(msg)
        numbers = tuple(int(part) for part in parts)
    elif isinstance(bound, tuple):
        numbers = cast("tuple[object, ...]", bound)
        if not 2 <= len(numbers) <= 3 or not all(type(n) is int for n in numbers):
            msg = f"{keyword}={bound!r} is not a release: give {_BOUND_FORMS}"
            raise ValueError(msg)
    else:
        try:
            _, required = _resolve(bound)
        except TypeError:
            msg = f"{keyword}={bound!r} is not a release: give {_BOUND_FORMS}"
            raise TypeError(msg) from None
        if required is None:
            msg = f"{keyword}= needs a release, and AnyIDFDocument names none"
            raise TypeError(msg)
        return required
    version = cast("tuple[int, int, int]", (*numbers, 0)[:3])
    release = find_release(version)
    if release is None:
        supported = ", ".join(version_string(v) for v in ENERGYPLUS_VERSIONS)
        msg = f"{keyword}={bound!r}: idfkit supports no such EnergyPlus release (it supports {supported})"
        raise ValueError(msg)
    return release


_BOUND_FORMS = '"major.minor" ("9.6"), a version tuple ((9, 6, 0)) or a document type (IDFDocumentV9_6)'


def _describe_range(low: tuple[int, int, int] | None, high: tuple[int, int, int] | None) -> str:
    """``9.6.0 or later``, ``a release before 9.6.0`` or ``from 9.6.0 to before 23.2.0``."""
    if high is None:
        return f"{version_string(cast('tuple[int, int, int]', low))} or later"
    if low is None:
        return f"a release before {version_string(high)}"
    return f"from {version_string(low)} to before {version_string(high)}"


def _check_range(doc: AnyIDFDocument, since: object, before: object) -> None:
    """Raise unless *doc* is of a supported release from *since* (inclusive) to *before* (exclusive)."""
    low = None if since is None else _release(since, "since")
    high = None if before is None else _release(before, "before")
    members = releases_between(low, high)
    if members and find_closest_version(doc.version) in members:
        return
    # Only a refusal pays for the description.
    described = _describe_range(low, high)
    if not members:
        msg = f"No supported EnergyPlus release is {described}"
        raise ValueError(msg)
    releases = ", ".join(version_string(v) for v in members)
    msg = f"The document is EnergyPlus {version_string(doc.version)}, not {described} ({releases})"
    raise TypeError(msg)


@overload
def as_version(doc: AnyIDFDocument, document_type: type[_D]) -> _D: ...
@overload
def as_version(doc: AnyIDFDocument, document_type: tuple[type[_D], ...]) -> _D: ...
@overload
def as_version(
    doc: AnyIDFDocument,
    *,
    since: _Bound | None = None,
    before: _Bound | None = None,
) -> AnyIDFDocument: ...
def as_version(
    doc: AnyIDFDocument,
    document_type: type[_D] | tuple[type[_D], ...] | None = None,
    *,
    since: _Bound | None = None,
    before: _Bound | None = None,
) -> _D | AnyIDFDocument:
    """Type *doc* as a document of the EnergyPlus version *document_type* stands for, or one of several.

    Or, given *since* and/or *before* instead, as a document of any supported release from *since*
    on and before *before*.

    The stub in ``versioned.pyi`` documents this function; this is its run-time check.
    """
    ranged = since is not None or before is not None
    if document_type is not None and ranged:
        msg = "as_version takes a document type or since=/before=, not both"
        raise TypeError(msg)
    if ranged:
        _check_range(doc, since, before)
        return doc
    if document_type is None:
        msg = "as_version needs a document type, or since= or before="
        raise TypeError(msg)
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


def check_target(document_type: object, since: object, before: object) -> None:
    """Refuse, before a file is read, a release target no document could meet.

    What the loaders (``load_idf(path, as_type=...)``, ``since=``, ``before=``) check up front, so a
    misspelt bound fails at once rather than after a parse. Whether the document meets the target
    is :func:`as_version`'s check, made once it is read.

    Raises:
        TypeError: If both a document type and a range are given, or the document type is not one.
        ValueError: If a bound names no supported release, or the range holds none.
    """
    if document_type is not None and (since is not None or before is not None):
        msg = "pass as_type= or since=/before=, not both"
        raise TypeError(msg)
    if document_type is not None:
        candidates = _candidates(document_type)
        if not candidates:
            msg = "as_type= needs at least one document type"
            raise TypeError(msg)
        for candidate in candidates:
            _resolve(candidate)
        return
    if since is None and before is None:
        return
    low = None if since is None else _release(since, "since")
    high = None if before is None else _release(before, "before")
    if not releases_between(low, high):
        msg = f"No supported EnergyPlus release is {_describe_range(low, high)}"
        raise ValueError(msg)


def release_union(*members: type) -> Any:
    """The run-time value of a generated range alias, such as ``IDFDocumentSince9_6``: the union of *members*.

    A type checker reads the alias from ``versioned.pyi``; this only has to exist when imported.
    One member is that member.

    ``IDFDocument`` stands for the latest release, but every document is an instance of it, so it
    is replaced by a stand-in for the latest release: ``isinstance(doc, IDFDocumentSince9_4)``
    then holds only for a document of 9.4 or later, as ``as_version`` reads the alias.
    """
    from .document import IDFDocument

    # Joined with ``|`` rather than ``Union[...]``: a ``typing.Union`` checks ``isinstance`` by the
    # instance's class, which skips the stand-ins' version check, while ``types.UnionType`` asks each
    # member, so ``isinstance(doc, IDFDocumentBefore9_4)`` holds for a 9.1 document.
    return functools.reduce(operator.or_, (_latest_release_type() if m is IDFDocument else m for m in members))


@lru_cache(maxsize=1)
def _latest_release_type() -> type:
    """A stand-in for the latest release that, unlike ``IDFDocument``, an older document is not an instance of."""
    major, minor, _ = LATEST_VERSION
    return document_type(f"IDFDocumentV{major}_{minor}", LATEST_VERSION)
