"""Derived-view cache on an :class:`~idfkit.document.IDFDocument`.

A derived view (the HVAC topology, the results index) is computed from a document and is valid for
exactly one document revision. The cache lives on the document itself, in its ``_derived`` slot, so
it dies with the document: there is no global registry and no ``id(doc)`` keying that a recycled
id could confuse (research R-06, R-21).

Every mutation path of the document moves :attr:`IDFDocument.revision
<idfkit.document.IDFDocument.revision>` forward (an extensible-list assignment by one per group;
a write into ``obj.data`` not at all). A view stored at revision *r* is returned while
the document is still at *r* and rebuilt on the first ask after any change. Rebuilding costs a few
percent of loading the model, which is why the views are rebuilt instead of maintained
incrementally.

This module is private. Callers inside idfkit reach the slots through it so that the rest of the
package never touches ``_revision`` or ``_derived`` directly.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable
from typing import TYPE_CHECKING, TypeVar, cast

if TYPE_CHECKING:
    from idfkit.document import IDFDocument

T = TypeVar("T")


def bump_revision(doc: IDFDocument) -> None:
    """Record one mutation of *doc*.

    Called once per mutation by the object write paths that do not pass through a document
    ``notify_*`` hook which already bumps.
    """
    revision = cast("int", object.__getattribute__(doc, "_revision"))
    object.__setattr__(doc, "_revision", revision + 1)


def get_or_build(doc: IDFDocument, view_name: str, build: Callable[[], T]) -> T:
    """Return the view *view_name* of *doc*, rebuilding it if the document changed since it was built.

    Args:
        doc: The document the view is derived from.
        view_name: The cache slot, for example ``"hvac"``.
        build: Called with no arguments to compute the view when the cached one is missing or stale.

    Returns:
        The cached view when its stored revision equals ``doc.revision``, otherwise the result of
        ``build()``, which is then stored with the current revision.
    """
    cache = cast("dict[str, tuple[int, object]]", object.__getattribute__(doc, "_derived"))
    revision = doc.revision
    entry = cache.get(view_name)
    if entry is not None and entry[0] == revision:
        return cast("T", entry[1])
    view = build()
    cache[view_name] = (revision, view)
    return view


def get_or_build_stamped(doc: IDFDocument, view_name: str, stamp: Hashable, build: Callable[[], T]) -> T:
    """Return the view *view_name* of *doc* built for *stamp*, building it on the first ask for that stamp.

    Unlike :func:`get_or_build`, the view is not tied to the document's revision. A results index
    belongs to one simulation run: an edit after the run makes it stale, which callers report, but
    the run's results do not change, so the index is kept until a different run asks for the slot.

    Args:
        doc: The document the view is attached to.
        view_name: The cache slot, for example ``"results"``.
        stamp: What identifies the source the view was built from, such as the run directory,
            revision and model hash.
        build: Called with no arguments to compute the view when the slot holds another stamp.

    Returns:
        The cached view when it was built for an equal *stamp*, otherwise the result of ``build()``.
    """
    cache = cast("dict[str, tuple[int, object]]", object.__getattribute__(doc, "_derived"))
    entry = cache.get(view_name)
    if entry is not None:
        held_stamp, view = cast("tuple[Hashable, T]", entry[1])
        if held_stamp == stamp:
            return view
    view = build()
    cache[view_name] = (-1, (stamp, view))
    return view
