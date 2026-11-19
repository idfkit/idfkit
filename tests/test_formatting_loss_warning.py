"""Saving a document over the commented IDF file it was read from, without its formatting, warns."""

from __future__ import annotations

import pickle
import warnings
from pathlib import Path

import pytest

from idfkit import load_idf, save_idf
from idfkit.exceptions import FormattingLossWarning
from idfkit.writers import OutputType

COMMENTED = """\
! Hand-curated model: keep these notes.
Version,24.1;

! Office zones
Zone,
  Office,                  !- Name
  0;                       !- Direction of Relative North {deg}
Building,
  B,                       !- Name
  0,                       !- North Axis {deg}
  City,                    !- Terrain
  0.04,                    !- Loads Convergence Tolerance Value {W}
  0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
  FullExterior,            !- Solar Distribution
  25,                      !- Maximum Number of Warmup Days
  6;                       ! tuned by hand
"""

FIELD_LABELS_ONLY = """\
Version,24.1;
Zone,
  Office,                  !- Name
  0;                       !- Direction of Relative North {deg}
"""


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "model.idf"
    path.write_text(text, encoding="latin-1")
    return path


def test_save_over_commented_source_warns(tmp_path: Path) -> None:
    path = _write(tmp_path, COMMENTED)
    model = load_idf(path)
    model["Zone"]["Office"].direction_of_relative_north = 10.0
    with pytest.warns(FormattingLossWarning, match=r"which has 3 comment lines") as record:
        model.save()
    # Points at the caller, not into idfkit's compatibility layer.
    assert record[0].filename == __file__


def test_save_idf_over_commented_source_warns(tmp_path: Path) -> None:
    path = _write(tmp_path, COMMENTED)
    model = load_idf(path)
    with pytest.warns(FormattingLossWarning, match="preserve_formatting=True") as record:
        save_idf(model, path)
    assert record[0].filename == __file__


def test_preserved_formatting_does_not_warn_and_keeps_comments(tmp_path: Path) -> None:
    path = _write(tmp_path, COMMENTED)
    model = load_idf(path, preserve_formatting=True)
    model["Zone"]["Office"].direction_of_relative_north = 10.0
    with warnings.catch_warnings():
        warnings.simplefilter("error", FormattingLossWarning)
        model.save()
    assert "! Hand-curated model: keep these notes." in path.read_text(encoding="latin-1")


@pytest.mark.parametrize("output_type", ["nocomment", "compressed"])
def test_reformatting_a_preserving_document_does_not_warn(tmp_path: Path, output_type: OutputType) -> None:
    """A document loaded with preserve_formatting=True and written in another layout was reformatted on request."""
    path = _write(tmp_path, COMMENTED)
    model = load_idf(path, preserve_formatting=True)
    with warnings.catch_warnings():
        warnings.simplefilter("error", FormattingLossWarning)
        model.save(output_type=output_type)


@pytest.mark.parametrize("explicit", [True, False])
def test_explicit_preserve_formatting_does_not_warn(tmp_path: Path, explicit: bool) -> None:
    path = _write(tmp_path, COMMENTED)
    model = load_idf(path, preserve_formatting=explicit)
    with warnings.catch_warnings():
        warnings.simplefilter("error", FormattingLossWarning)
        save_idf(model, path, preserve_formatting=False)


def test_saving_elsewhere_does_not_warn(tmp_path: Path) -> None:
    path = _write(tmp_path, COMMENTED)
    model = load_idf(path)
    with warnings.catch_warnings():
        warnings.simplefilter("error", FormattingLossWarning)
        model.saveas(tmp_path / "copy.idf")
        # The copy idfkit wrote has only field labels, so saving over it again loses nothing.
        model.save()


def test_field_labels_alone_do_not_warn(tmp_path: Path) -> None:
    path = _write(tmp_path, FIELD_LABELS_ONLY)
    model = load_idf(path)
    with warnings.catch_warnings():
        warnings.simplefilter("error", FormattingLossWarning)
        model.save()


def test_warning_pickles() -> None:
    warning = FormattingLossWarning("model.idf", 1)
    clone = pickle.loads(pickle.dumps(warning))  # noqa: S301
    assert str(clone) == str(warning)
    assert "1 comment line," in str(clone)
