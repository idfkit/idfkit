"""Async migration backend: invoke ``Transition-VX-to-VY`` via asyncio subprocesses.

Non-blocking counterpart to
[SubprocessMigrator][idfkit.migration.subprocess_backend.SubprocessMigrator].
Uses [asyncio.create_subprocess_exec][] instead of [subprocess.run][] so that
migration chains can run concurrently with other coroutines.

The cancellation/cleanup pattern mirrors
[idfkit.simulation.async_runner][]: on timeout or cancellation, the subprocess
is killed and awaited to avoid leaked processes.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from dataclasses import dataclass
from pathlib import Path

from ..exceptions import MigrationError
from .protocol import MigrationStepResult
from .subprocess_backend import DEFAULT_STEP_TIMEOUT, binary_candidates, collect_audit_text, stage_idd_symlinks

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class AsyncSubprocessMigrator:
    """Async migrator backend built on [asyncio.create_subprocess_exec][].

    Attributes:
        version_updater_dir: Path to ``PreProcess/IDFVersionUpdater``.
        step_timeout: Maximum wall-clock seconds for a single transition step.
    """

    version_updater_dir: Path
    step_timeout: float = DEFAULT_STEP_TIMEOUT

    async def migrate_step(
        self,
        idf_text: str,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
        *,
        work_dir: Path,
    ) -> MigrationStepResult:
        """Run a single ``Transition-VX-to-VY`` binary without blocking."""
        binary = self.locate_binary(from_version, to_version)

        await asyncio.to_thread(work_dir.mkdir, parents=True, exist_ok=True)
        await asyncio.to_thread(stage_idd_symlinks, self.version_updater_dir, work_dir)
        input_idf = work_dir / "in.idf"
        await asyncio.to_thread(input_idf.write_text, idf_text, "latin-1")

        try:
            proc = await asyncio.create_subprocess_exec(
                str(binary),
                str(input_idf),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(work_dir),
            )
        except OSError as exc:
            msg = f"Failed to start transition binary: {exc}"
            raise MigrationError(
                msg,
                from_version=from_version,
                to_version=to_version,
            ) from exc

        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.step_timeout,
            )
        except asyncio.TimeoutError as exc:
            proc.kill()
            with contextlib.suppress(ProcessLookupError):
                await proc.wait()
            msg = f"Transition timed out after {self.step_timeout} seconds"
            raise MigrationError(
                msg,
                from_version=from_version,
                to_version=to_version,
            ) from exc
        except asyncio.CancelledError:
            proc.kill()
            with contextlib.suppress(ProcessLookupError):
                await proc.wait()
            raise

        stdout = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
        stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
        returncode = proc.returncode if proc.returncode is not None else -1

        if returncode != 0:
            msg = "Transition binary exited with non-zero status"
            raise MigrationError(
                msg,
                from_version=from_version,
                to_version=to_version,
                exit_code=returncode,
                stderr=stderr,
            )

        if not input_idf.is_file():
            msg = f"Transition binary produced no output at {input_idf}"
            raise MigrationError(
                msg,
                from_version=from_version,
                to_version=to_version,
                exit_code=returncode,
                stderr=stderr,
            )

        migrated_text = await asyncio.to_thread(input_idf.read_text, "latin-1")
        audit_text = await asyncio.to_thread(collect_audit_text, work_dir)
        return MigrationStepResult(
            idf_text=migrated_text,
            stdout=stdout,
            stderr=stderr,
            audit_text=audit_text,
        )

    def locate_binary(
        self,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
    ) -> Path:
        """Return the absolute path to the transition binary for a single step."""
        candidates = binary_candidates(from_version, to_version)
        for name in candidates:
            p = self.version_updater_dir / name
            if p.is_file():
                return p
        if not self.version_updater_dir.is_dir():
            msg = f"IDFVersionUpdater directory not found: {self.version_updater_dir}"
            raise MigrationError(msg, from_version=from_version, to_version=to_version)
        msg = f"No transition binary found. Tried: {', '.join(candidates)}"
        raise MigrationError(msg, from_version=from_version, to_version=to_version)
