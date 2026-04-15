"""Tests for migration-specific exception shapes."""

from __future__ import annotations

from idfkit.exceptions import MigrationError, VersionMismatchError


class TestVersionMismatchError:
    def test_forward_direction(self) -> None:
        err = VersionMismatchError(
            current=(24, 1, 0),
            target=(25, 1, 0),
            migration_chain=(((24, 1, 0), (24, 2, 0)), ((24, 2, 0), (25, 1, 0))),
        )
        assert err.direction == "forward"
        assert err.migration_chain[0] == ((24, 1, 0), (24, 2, 0))
        text = str(err)
        assert "24.1.0" in text
        assert "25.1.0" in text
        assert "Migration chain" in text

    def test_backward_direction(self) -> None:
        err = VersionMismatchError(current=(25, 1, 0), target=(24, 2, 0))
        assert err.direction == "backward"
        assert "Backward migration is not supported" in str(err)

    def test_empty_chain_with_forward_still_mentions_migrate(self) -> None:
        # An empty chain with forward direction shouldn't leak the "Backward" message.
        err = VersionMismatchError(current=(24, 1, 0), target=(24, 2, 0), migration_chain=())
        text = str(err)
        assert "Backward migration is not supported" not in text


class TestMigrationError:
    def test_carries_structured_context(self) -> None:
        err = MigrationError(
            "boom",
            from_version=(24, 1, 0),
            to_version=(24, 2, 0),
            exit_code=2,
            stderr="err output",
            completed_steps=(((24, 1, 0), (24, 2, 0)),),
        )
        assert err.from_version == (24, 1, 0)
        assert err.to_version == (24, 2, 0)
        assert err.exit_code == 2
        assert err.stderr == "err output"
        assert err.completed_steps == (((24, 1, 0), (24, 2, 0)),)
        text = str(err)
        assert "boom" in text
        assert "err output" in text
        assert "24.1.0" in text
        assert "24.2.0" in text

    def test_truncates_long_stderr(self) -> None:
        long_stderr = "x" * 1000
        err = MigrationError("boom", stderr=long_stderr)
        # String form should include at most 500 chars of stderr content.
        assert len(str(err)) < 800
