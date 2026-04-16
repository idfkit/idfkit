"""Default migration backend: invoke EnergyPlus's ``Transition-VX-to-VY`` binaries.

The binaries live in ``PreProcess/IDFVersionUpdater`` inside an EnergyPlus
installation. Each binary takes a single IDF file as its command-line argument,
reads the sibling ``V{from}-Energy+.idd`` file, and writes the migrated IDF
back to the same path (moving the original to ``<name>.idfold``).

The binary must be run with ``cwd`` set to the ``IDFVersionUpdater`` directory
so it can locate its ``VX-Y-Z-Energy+.idd`` companion; we therefore stage the
input IDF inside a temporary subdirectory and invoke the binary from there
using an absolute path to the binary (matching how ``IDFVersionUpdater.app``
launches them).
"""

from __future__ import annotations

import logging
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ..exceptions import MigrationError
from .protocol import MigrationStepResult

logger = logging.getLogger(__name__)

DEFAULT_STEP_TIMEOUT: float = 600.0


@dataclass(frozen=True, slots=True)
class SubprocessMigrator:
    """Migrator backend that shells out to EnergyPlus's transition binaries.

    Attributes:
        version_updater_dir: Path to ``PreProcess/IDFVersionUpdater``. Must contain
            the ``Transition-V*-to-V*`` binaries and matching
            ``V*-Energy+.idd`` files.
        step_timeout: Maximum wall-clock seconds for a single transition step.
    """

    version_updater_dir: Path
    step_timeout: float = DEFAULT_STEP_TIMEOUT

    def migrate_step(
        self,
        idf_text: str,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
        *,
        work_dir: Path,
    ) -> MigrationStepResult:
        """Run a single ``Transition-VX-to-VY`` binary on *idf_text*."""
        binary = self.locate_binary(from_version, to_version)

        work_dir.mkdir(parents=True, exist_ok=True)
        input_idf = work_dir / "in.idf"
        input_idf.write_text(idf_text, encoding="latin-1")

        try:
            proc = subprocess.run(  # noqa: S603
                [str(binary), str(input_idf)],
                capture_output=True,
                text=True,
                timeout=self.step_timeout,
                cwd=str(self.version_updater_dir),
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            msg = f"Transition timed out after {self.step_timeout} seconds"
            raise MigrationError(
                msg,
                from_version=from_version,
                to_version=to_version,
                stderr=str(exc.stderr) if exc.stderr else None,
            ) from exc
        except OSError as exc:
            msg = f"Failed to start transition binary: {exc}"
            raise MigrationError(
                msg,
                from_version=from_version,
                to_version=to_version,
            ) from exc

        if proc.returncode != 0:
            msg = "Transition binary exited with non-zero status"
            raise MigrationError(
                msg,
                from_version=from_version,
                to_version=to_version,
                exit_code=proc.returncode,
                stderr=proc.stderr,
            )

        if not input_idf.is_file():
            msg = f"Transition binary produced no output at {input_idf}"
            raise MigrationError(
                msg,
                from_version=from_version,
                to_version=to_version,
                exit_code=proc.returncode,
                stderr=proc.stderr,
            )

        migrated_text = input_idf.read_text(encoding="latin-1")
        return MigrationStepResult(
            idf_text=migrated_text,
            stdout=proc.stdout,
            stderr=proc.stderr,
            audit_text=collect_audit_text(work_dir),
        )

    def locate_binary(
        self,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
    ) -> Path:
        """Return the absolute path to the transition binary for a single step.

        Tries the registry-exact name first, then falls back to ``(major, minor, 0)``
        for either side -- EnergyPlus's transition binaries are always named with
        ``patch=0`` (notably, v9.0.1 uses the ``V9-0-0`` binary name).
        """
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


def binary_candidates(
    from_version: tuple[int, int, int],
    to_version: tuple[int, int, int],
) -> list[str]:
    """Return the candidate transition-binary file names, in probe order.

    EnergyPlus's transition binaries are always named with ``patch=0``, but
    the ``ENERGYPLUS_VERSIONS`` registry includes non-zero patch entries
    (notably ``(9, 0, 1)``). Try the registry-exact name first, then fall
    back to the ``patch=0`` form, for each side.
    """
    suffix = ".exe" if platform.system() == "Windows" else ""
    a = from_version
    b = to_version
    ordered = [
        f"Transition-V{a[0]}-{a[1]}-{a[2]}-to-V{b[0]}-{b[1]}-{b[2]}{suffix}",
        f"Transition-V{a[0]}-{a[1]}-0-to-V{b[0]}-{b[1]}-0{suffix}",
        f"Transition-V{a[0]}-{a[1]}-{a[2]}-to-V{b[0]}-{b[1]}-0{suffix}",
        f"Transition-V{a[0]}-{a[1]}-0-to-V{b[0]}-{b[1]}-{b[2]}{suffix}",
    ]
    seen: set[str] = set()
    out: list[str] = []
    for n in ordered:
        if n in seen:
            continue
        seen.add(n)
        out.append(n)
    return out


def collect_audit_text(work_dir: Path) -> str | None:
    """Return the contents of any ``*.audit`` file the transition binary emitted."""
    for child in sorted(work_dir.iterdir()):
        if child.suffix == ".audit":
            try:
                return child.read_text(encoding="latin-1")
            except OSError:  # pragma: no cover -- best-effort read
                return None
    return None
