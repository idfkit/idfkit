"""Read the pinned TypeDoc artifact, and bridge it to griffe-typedoc's model of it.

TWO JOBS, AND THE FIRST ONE IS WHY THIS LIVES HERE RATHER THAN IN idfkit-js

The unified site renders the TypeScript reference and must build with no Node toolchain and no
checkout of idfkit-js (FR-058). `mkdocstrings-typescript` does the opposite: it calls
`griffe_typedoc.load(["typedoc"])`, which shells out to a `typedoc` executable and regenerates the
JSON on every build. There is no option to hand it a file.

So the first patch replaces that call with a read of the artifact this repository pins:
`docs/typedoc/typedoc.json`, vendored from the `docs-YYYY.N` release of idfkit-js by
`scripts/sync_js_artifacts.py` and compared against that release by a blocking CI job. The
reference is still generated from source and never written (Principle V); it is generated in the
repository that owns the source, which is the only place it can be.

The second job is the original one, kept verbatim below.

BRIDGING TypeDoc 0.28's JSON TO griffe-typedoc's MODEL OF IT

`mkdocstrings-typescript` reads TypeDoc's JSON output through `griffe-typedoc`,
which its author labels "still in prototyping phase". Its dataclasses were
written against an earlier TypeDoc, and it decodes strictly: every key becomes a
constructor keyword and every type node's kind must be in a closed enum. TypeDoc
has moved on, so an unpatched build dies on the first mismatch with a
`TypeError` or a `ValueError` and produces no reference at all.

Two kinds of mismatch show up here, and neither is exotic:

1.  **Unmodelled type kinds.** `indexedAccess` and `conditional` are missing from
    `TypeKind`. Both come from `typemap.ts`, where `ObjectOf`, `TypeNameOf`, and
    `ValuesOf` are exactly an indexed access into a generated map guarded by a
    conditional -- the mechanism that makes `doc.all('Zone')` return a typed
    object. Excluding those aliases to appease the decoder would cut the most
    load-bearing types out of the reference, so they are coerced into a plain
    named reference instead: the signature renders as `M[K]` or
    `A extends B ? C : D` rather than a cross-linked structure.

2.  **Keys with no field.** TypeDoc 0.28 emits `schemaVersion` on the project and
    `elementSummaries` on tuples, among others. Nothing renders them. Rather
    than pin TypeDoc (and with it TypeScript, which the packages track closely),
    unknown keys are dropped on the way in.

The alternative to both is pinning TypeDoc to whatever release griffe-typedoc
last tracked, which would hold the whole toolchain back for the sake of fields
that are never displayed.

Delete this hook, and its `hooks:` entry in `mkdocs.yml`, once griffe-typedoc
models current TypeDoc output. If the reference starts losing detail, that is the
signal to check whether it already does.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from griffe_typedoc._internal import decoder as _decoder
from griffe_typedoc._internal import models as _models
from griffe_typedoc._internal.models import BlockTagContentKind, Type, TypeKind

# --------------------------------------------------------------------------
# Reading the pinned artifact instead of running TypeDoc
# --------------------------------------------------------------------------

#: Where the vendored artifact sits, relative to this file. Under docs/ deliberately: the
#: documentation tree has to build from a directory this repository is not in, so nothing here may
#: compute a path out of its own location. The portability job in .github/workflows/docs.yml
#: enforces exactly that and would fail on a `parents[2]`.
_ARTIFACT = Path(__file__).resolve().parent.parent / "typedoc" / "typedoc.json"

#: An escape hatch for a maintainer trying an unreleased reference, and it announces itself.
#: Never set in CI: a build under it says nothing about the pinned level.
_OVERRIDE = "IDFKIT_TYPEDOC_JSON"


def _load_pinned(*_args: object, **_kwargs: object) -> Any:
    """Decode the pinned TypeDoc JSON, in place of shelling out to `typedoc`."""
    override = os.environ.get(_OVERRIDE)
    path = Path(override) if override else _ARTIFACT
    if override:
        print(f"!! Reading {path} instead of the pinned TypeDoc artifact. This is an override.")
    if not path.is_file():
        raise FileNotFoundError(
            f"No TypeDoc artifact at {path}. The TypeScript reference is rendered from the "
            f"artifact pinned in pyproject.toml, not by running TypeDoc: this build has no Node "
            f"toolchain and must not acquire one (FR-058). Run "
            f"`uv run python scripts/sync_js_artifacts.py --from-release` from the repository root."
        )
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, cls=_decoder.TypedocDecoder)


_KNOWN_TYPE_KINDS = {kind.value for kind in TypeKind}

# "Project.__init__() got an unexpected keyword argument 'schema_version'"
_UNEXPECTED_KWARG = re.compile(r"unexpected keyword argument '([^']+)'")


def _render(node: Any) -> str:
    """Best-effort source-like text for an already-decoded type node."""
    if node is None:
        return "unknown"
    name = getattr(node, "name", None)
    if name:
        return str(name)
    value = getattr(node, "value", None)
    if value is not None:
        return repr(value)
    return "unknown"


def _name_for(kind: str, obj_dict: dict[str, Any]) -> str:
    # Keys are still camelCase at this point: griffe-typedoc snake-cases them
    # inside its `_loader` wrapper, which has not run yet.
    if kind == "indexedAccess":
        return f"{_render(obj_dict.get('objectType'))}[{_render(obj_dict.get('indexType'))}]"
    if kind == "conditional":
        return (
            f"{_render(obj_dict.get('checkType'))} extends "
            f"{_render(obj_dict.get('extendsType'))} ? "
            f"{_render(obj_dict.get('trueType'))} : "
            f"{_render(obj_dict.get('falseType'))}"
        )
    return kind


def _snake_to_camel(key: str) -> str:
    head, *tail = key.split("_")
    return head + "".join(word.title() for word in tail)


Loader = Callable[[dict[str, Any], dict[int, Any]], Any]


def _tolerant(loader: Loader) -> Loader:
    """Retry a loader, shedding one unmodelled key per attempt.

    The loaders mutate `obj_dict` on the way through -- snake-casing keys in
    place, popping `type` -- and some of that happens before the constructor
    raises, so each attempt starts from a fresh copy of the original. The failing
    keyword comes back snake-cased while the copy may still hold the camelCase
    spelling, so both are dropped. Retries are bounded by the key count, and
    anything that is not an unexpected-keyword `TypeError` propagates untouched.
    """

    def load(obj_dict: dict[str, Any], symbol_map: dict[int, Any]) -> Any:
        original = dict(obj_dict)
        dropped: set[str] = set()
        for _ in range(len(original) + 1):
            attempt = {key: value for key, value in original.items() if key not in dropped}
            try:
                return loader(attempt, symbol_map)
            except TypeError as error:
                match = _UNEXPECTED_KWARG.search(str(error))
                if match is None:
                    raise
                snake = match.group(1)
                dropped.update({snake, _snake_to_camel(snake)})
        raise RuntimeError(f"Could not decode TypeDoc object: {sorted(original)}")

    return load


_undecorated_load_type = _decoder._load_type


def _load_type(obj_dict: dict[str, Any], symbol_map: dict[int, Any]) -> Type:
    kind = obj_dict.get("type")
    if isinstance(kind, str) and kind not in _KNOWN_TYPE_KINDS:
        # Drop the payload keys along with the kind: `Type` has no fields for
        # them, so passing them through would fail the same way the enum did.
        return Type(type=TypeKind.REFERENCE, name=_name_for(kind, obj_dict))
    return _undecorated_load_type(obj_dict, symbol_map)


_decoder._load_type = _tolerant(_load_type)
_decoder._loader_map = {kind: _tolerant(loader) for kind, loader in _decoder._loader_map.items()}


# --------------------------------------------------------------------------
# Comment content kinds
# --------------------------------------------------------------------------
#
# A doc comment is decoded as a list of content parts, each tagged with a kind
# that must be one of `text`, `code`, or `inline-tag`. TypeDoc 0.28 also emits
# `relative-link` for a relative markdown link inside a comment, and the
# resulting `ValueError` is not caught where it is raised: the decoder falls
# through to a reflection-kind lookup that fails with a bare
# `KeyError: 'relative-link'`, and MkDocs reports it as an unreadable page.
#
# An unrecognised part is still text, so treat it as such. Its extra keys are
# then shed by the tolerant loaders above.


class _ContentKind:
    """Stand-in for `BlockTagContentKind` that degrades unknown kinds to text.

    The decoder uses the name both as a constructor and for member access
    (`BlockTagContentKind.CODE`), so everything but the call is delegated.
    """

    def __getattr__(self, name: str) -> Any:
        return getattr(BlockTagContentKind, name)

    def __call__(self, value: Any) -> BlockTagContentKind:
        try:
            return BlockTagContentKind(value)
        except ValueError:
            # Only strings are content kinds. Integers are reflection kinds, and
            # the decoder needs its own `ValueError` to fall through to them.
            if not isinstance(value, str):
                raise
            return BlockTagContentKind.TEXT


_decoder.BlockTagContentKind = _ContentKind()


# --------------------------------------------------------------------------
# Reading the source line behind a symbol
# --------------------------------------------------------------------------
#
# Templates print `source_contents` to show a declaration as it is written. To
# get it, `Source.contents` opens the file registry entry for the symbol's root
# module and reads one line out of it -- which is wrong twice over in a
# `entryPointStrategy: "packages"` build like this one:
#
#   * the root module of anything under `@idfkit/core` registers as the package
#     directory `packages/core`, and opening a directory raises;
#   * the fallback is `Path(filepath).with_name(source.file_name)`, and
#     `with_name` rejects any name containing a separator -- every one of ours
#     looks like `core/src/collection.ts`, because TypeDoc roots each
#     sub-project's paths at the packages directory rather than at the repo.
#
# So it raises `ValueError` and the build dies. Worse, when the first open does
# happen to succeed, the line number belongs to a different file and the wrong
# line is displayed with no error at all.
#
# Resolve against the file registry instead, which holds correct repo-relative
# paths, and fall back to reading nothing rather than reading something false.


def _registry_paths(source: Any) -> list[str]:
    try:
        entries = source.parent.root.files.entries
    except AttributeError:
        return []
    return list(entries.values())


def _contents(self: Any) -> str:
    name = self.file_name
    candidates = [name, *(path for path in _registry_paths(self) if path.endswith(f"/{name}"))]
    for candidate in candidates:
        try:
            with Path(candidate).open(encoding="utf8") as handle:
                return handle.readlines()[self.line - 1]
        except (OSError, IndexError):
            continue
    return ""


_models.Source.contents = property(_contents)


# Applied last, so the decoder patches above are all in place before anything decodes. The handler
# module binds `load_typedoc` at import time, so patching `griffe_typedoc.load` alone would not
# reach it; both are replaced.
def _install_pinned_loader() -> None:
    import griffe_typedoc
    from mkdocstrings_handlers.typescript._internal import handler as _handler

    griffe_typedoc.load = _load_pinned
    _handler.load_typedoc = _load_pinned


_install_pinned_loader()
