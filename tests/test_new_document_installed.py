"""``new_document(EnergyPlusConfig)``: a model at the release of an installed EnergyPlus (prototype)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest

from idfkit import new_document
from idfkit.exceptions import UnsupportedVersionError
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.versioned import IDFDocumentV9_4, IDFDocumentV25_1


def _install(version: tuple[int, int, int]) -> EnergyPlusConfig:
    """A config for an installation that need not exist: new_document reads only its version."""
    root = Path("/opt/EnergyPlus")
    return EnergyPlusConfig(
        executable=root / "energyplus", version=version, install_dir=root, idd_path=root / "Energy+.idd"
    )


class TestNewDocumentForAnInstallation:
    def test_creates_the_model_at_the_installed_release(self) -> None:
        doc = new_document(_install((25, 1, 0)))
        assert doc.version == (25, 1, 0)
        assert [v.version_identifier for v in doc["Version"]] == ["25.1"]

    def test_matches_the_release_line_not_the_patch(self) -> None:
        assert new_document(_install((9, 0, 0))).version == (9, 0, 1)

    def test_keeps_strict_and_normalize_choices(self) -> None:
        doc = new_document(_install((24, 1, 0)), strict=False, normalize_choices=False)
        assert (doc.strict, doc.normalize_choices) == (False, False)

    @pytest.mark.parametrize("version", [(27, 1, 0), (8, 8, 0)])
    def test_refuses_a_release_without_a_bundled_schema(self, version: tuple[int, int, int]) -> None:
        with pytest.raises(UnsupportedVersionError):
            new_document(_install(version))

    def test_as_type_names_the_expected_release(self) -> None:
        doc = new_document(_install((25, 1, 0)), as_type=IDFDocumentV25_1)
        assert doc.version == (25, 1, 0)

    def test_as_type_refuses_another_release(self) -> None:
        with pytest.raises(TypeError, match=r"9\.4"):
            new_document(_install((25, 1, 0)), as_type=IDFDocumentV9_4)

    def test_as_type_states_the_strictness(self) -> None:
        doc = new_document(_install((25, 1, 0)), as_type=IDFDocumentV25_1[Literal[False]])
        assert doc.strict is False

    def test_as_type_is_refused_without_an_installation(self) -> None:
        with pytest.raises(TypeError, match="only with an EnergyPlusConfig"):
            new_document((25, 1, 0), as_type=IDFDocumentV25_1)  # pyright: ignore[reportCallIssue, reportArgumentType]


class TestSimulateAcceptsIt:
    """The model's release is the one simulate() resolves the installation to, so it runs without migrating."""

    @pytest.mark.parametrize("version", [(25, 1, 0), (9, 0, 0), (9, 0, 1), (26, 2, 0)])
    def test_no_version_mismatch(self, version: tuple[int, int, int]) -> None:
        from idfkit.simulation._common import resolve_version_mismatch  # pyright: ignore[reportPrivateUsage]

        config = _install(version)
        doc = new_document(config)
        model, report = resolve_version_mismatch(model=doc, config=config, auto_migrate=False)
        assert model is doc
        assert report is None
