"""Tests for the migration chain planner."""

from __future__ import annotations

import pytest

from idfkit import IDFDocument
from idfkit.exceptions import UnsupportedVersionError
from idfkit.migration.chain import normalize_target, plan_migration_chain
from idfkit.versioned import IDFDocumentV9_0, IDFDocumentV24_1
from idfkit.versions import LATEST_VERSION


class TestNormalizeTarget:
    def test_document_type_is_its_release(self) -> None:
        assert normalize_target(IDFDocumentV24_1) == (24, 1, 0)
        # 9.0's release is 9.0.1, the version its schema and as_version use.
        assert normalize_target(IDFDocumentV9_0) == (9, 0, 1)
        assert normalize_target(IDFDocument) == LATEST_VERSION


class TestPlanMigrationChain:
    def test_no_op_when_source_equals_target(self) -> None:
        assert plan_migration_chain((24, 1, 0), (24, 1, 0)) == ()

    def test_single_step(self) -> None:
        chain = plan_migration_chain((24, 1, 0), (24, 2, 0))
        assert chain == (((24, 1, 0), (24, 2, 0)),)

    def test_multi_step_is_contiguous(self) -> None:
        chain = plan_migration_chain((23, 1, 0), (24, 2, 0))
        # Steps walk the registry in order: (23,1,0)->(23,2,0)->(24,1,0)->(24,2,0)
        assert chain == (
            ((23, 1, 0), (23, 2, 0)),
            ((23, 2, 0), (24, 1, 0)),
            ((24, 1, 0), (24, 2, 0)),
        )

    def test_spans_major_versions(self) -> None:
        from itertools import pairwise

        chain = plan_migration_chain((9, 6, 0), (22, 2, 0))
        assert chain[0][0] == (9, 6, 0)
        assert chain[-1][1] == (22, 2, 0)
        for (_, a_to), (b_from, _) in pairwise(chain):
            assert a_to == b_from

    def test_backward_raises(self) -> None:
        with pytest.raises(ValueError, match="Backward migration"):
            plan_migration_chain((24, 1, 0), (23, 1, 0))

    def test_unsupported_source_raises(self) -> None:
        with pytest.raises(UnsupportedVersionError):
            plan_migration_chain((7, 0, 0), (24, 1, 0))

    def test_unsupported_target_raises(self) -> None:
        with pytest.raises(UnsupportedVersionError):
            plan_migration_chain((24, 1, 0), (99, 0, 0))
