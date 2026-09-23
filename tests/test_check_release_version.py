"""Guard the release version gate (idfkit#212).

The gate lives in ``scripts/check_release_version.py`` and is loaded by path, as a maintainer
script rather than part of the distributed package. It compares the release tag against the
version ``pyproject.toml`` declares, and it exists because the workflow used to write the tag into
that field instead: tags carry the ``v`` prefix, so ``version = "v1.0.0-rc.5"`` reached the wheel's
metadata and the generator header came out as ``!-Generator idfkit vv1.0.0-rc.5``.

The comparison is by PEP 440 equality rather than by string, which is the part worth guarding: the
tag format and the manifest form differ on the prefix and on punctuation for every release in the
candidate series, and none of those differences is a disagreement.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "check_release_version.py"


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gate = _load("check_release_version", _SCRIPT)


class TestAgreement:
    """Forms that differ as strings and agree as versions."""

    @pytest.mark.parametrize(
        ("declared", "tag"),
        [
            ("1.0.0rc5", "v1.0.0-rc.5"),
            ("1.0.0rc5", "1.0.0rc5"),
            ("1.0.0rc5", "v1.0.0rc5"),
            ("1.0.0", "v1.0.0"),
            ("0.15.0", "v0.15.0"),
        ],
    )
    def test_agrees(self, declared: str, tag: str, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(gate, "declared_version", lambda: declared)
        assert gate.main(["--tag", tag]) == 0

    def test_the_repository_agrees_with_itself(self) -> None:
        """The committed manifest against its own version, spelled as a tag."""
        declared = gate.declared_version()
        assert gate.main(["--tag", f"v{declared}"]) == 0


class TestDisagreement:
    @pytest.mark.parametrize(
        ("declared", "tag"),
        [
            ("1.0.0rc5", "v1.0.0-rc.6"),
            ("1.0.0rc5", "v1.0.0"),
            ("1.0.0", "v1.0.1"),
        ],
    )
    def test_fails(self, declared: str, tag: str, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(gate, "declared_version", lambda: declared)
        assert gate.main(["--tag", tag]) == 1


class TestWhatThisGateDoesNotCatch:
    def test_a_manifest_already_carrying_the_prefix_passes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The exact shape of idfkit#212: the tag, prefix and all, as the declared version."""
        monkeypatch.setattr(gate, "declared_version", lambda: "v1.0.0-rc.5")
        # It passes, because PEP 440 tolerates the prefix and the two are then the same version.
        # This gate is not what makes idfkit#212 impossible; removing the patch step is. Recorded
        # so that anyone reintroducing a patch has to change this test before claiming otherwise.
        assert gate.main(["--tag", "v1.0.0-rc.5"]) == 0


class TestRefusals:
    def test_no_tag_and_no_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("GITHUB_REF_NAME", raising=False)
        assert gate.main([]) == 2

    def test_reads_the_environment_when_no_tag_is_given(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(gate, "declared_version", lambda: "1.0.0rc5")
        monkeypatch.setenv("GITHUB_REF_NAME", "v1.0.0-rc.5")
        assert gate.main([]) == 0

    def test_a_tag_that_is_not_a_version_refuses(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(gate, "declared_version", lambda: "1.0.0rc5")
        with pytest.raises(SystemExit) as raised:
            gate.main(["--tag", "not-a-release"])
        assert str(raised.value).startswith("2:")
