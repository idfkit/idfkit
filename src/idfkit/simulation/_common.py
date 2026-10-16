"""Shared helpers for sync and async simulation runners.

Internal module — not part of the public API.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from .config import EnergyPlusConfig, find_energyplus

PREPROCESSOR_TIMEOUT_ENV = "IDFKIT_PREPROCESSOR_TIMEOUT"
DEFAULT_PREPROCESSOR_TIMEOUT = 120.0


def resolve_preprocessor_timeout(explicit: float | None) -> float:
    """Resolve the preprocessor timeout for a single subprocess invocation.

    Resolution order:

    1. *explicit* if not ``None`` (caller-supplied value).
    2. ``IDFKIT_PREPROCESSOR_TIMEOUT`` environment variable, parsed as
       a float.
    3. ``DEFAULT_PREPROCESSOR_TIMEOUT`` (120 seconds).

    Args:
        explicit: Caller-supplied value, or ``None`` to defer to the
            environment / default.

    Returns:
        The timeout in seconds applied to each preprocessor subprocess
        (ExpandObjects, Slab, Basement). The value is per-invocation, not
        a shared budget across the pipeline.

    Raises:
        ValueError: If ``IDFKIT_PREPROCESSOR_TIMEOUT`` is set but cannot
            be parsed as a positive float.
    """
    if explicit is not None:
        return explicit

    env_value = os.environ.get(PREPROCESSOR_TIMEOUT_ENV)
    if env_value is None or env_value == "":
        return DEFAULT_PREPROCESSOR_TIMEOUT

    try:
        parsed = float(env_value)
    except ValueError as exc:
        msg = f"{PREPROCESSOR_TIMEOUT_ENV} must be a positive number of seconds, got {env_value!r}"
        raise ValueError(msg) from exc

    if parsed <= 0:
        msg = f"{PREPROCESSOR_TIMEOUT_ENV} must be a positive number of seconds, got {parsed}"
        raise ValueError(msg)

    return parsed


if TYPE_CHECKING:
    from ..document import IDFDocument
    from ..migration.report import MigrationReport
    from .fs import AsyncFileSystem, FileSystem


def resolve_version_mismatch(
    *,
    model: IDFDocument,
    config: EnergyPlusConfig,
    auto_migrate: bool,
) -> tuple[IDFDocument, MigrationReport | None]:
    """Reconcile a model's version with the installed EnergyPlus version.

    Returns a ``(model_to_simulate, migration_report)`` pair. If the versions
    already match, the report is ``None`` and the caller's model is returned
    unchanged. If they differ and *auto_migrate* is ``True``, the model is
    forward-migrated and the resulting
    [MigrationReport][idfkit.migration.report.MigrationReport] is returned.

    Raises:
        VersionMismatchError: If versions differ and *auto_migrate* is
            ``False``, or if the model is newer than the installed EP
            (backward migration is never attempted).
        SimulationError: If migration completes without producing a migrated
            model (should not happen in practice).
    """
    from ..exceptions import SimulationError, VersionMismatchError
    from ..migration.chain import plan_migration_chain

    if model.version == config.version:
        return model, None

    if model.version > config.version:
        raise VersionMismatchError(current=model.version, target=config.version)

    chain = plan_migration_chain(model.version, config.version)
    if not auto_migrate:
        raise VersionMismatchError(
            current=model.version,
            target=config.version,
            migration_chain=chain,
        )

    from ..migration.runner import migrate

    report = migrate(model, target_version=config.version, energyplus=config)
    migrated = report.migrated_model
    if migrated is None:  # pragma: no cover -- chain is non-empty, so migrate() returns a model
        msg = "Migration completed without producing a migrated model"
        raise SimulationError(msg)
    return migrated, report


async def async_resolve_version_mismatch(
    *,
    model: IDFDocument,
    config: EnergyPlusConfig,
    auto_migrate: bool,
) -> tuple[IDFDocument, MigrationReport | None]:
    """Async counterpart to [resolve_version_mismatch][idfkit.simulation._common.resolve_version_mismatch].

    Differs only in that the migration step is dispatched through
    [async_migrate()][idfkit.migration.async_runner.async_migrate] so it does
    not block the event loop.
    """
    from ..exceptions import SimulationError, VersionMismatchError
    from ..migration.async_runner import async_migrate
    from ..migration.chain import plan_migration_chain

    if model.version == config.version:
        return model, None

    if model.version > config.version:
        raise VersionMismatchError(current=model.version, target=config.version)

    chain = plan_migration_chain(model.version, config.version)
    if not auto_migrate:
        raise VersionMismatchError(
            current=model.version,
            target=config.version,
            migration_chain=chain,
        )

    report = await async_migrate(model, target_version=config.version, energyplus=config)
    migrated = report.migrated_model
    if migrated is None:  # pragma: no cover -- chain is non-empty, so async_migrate() returns a model
        msg = "Migration completed without producing a migrated model"
        raise SimulationError(msg)
    return migrated, report


WEATHER_EMPTY_STRING_MESSAGE = (
    "weather is an empty string, which does not identify a weather file. "
    "Pass weather=None to run design days without a weather file."
)
WEATHER_REQUIRED_MESSAGE = (
    "A weather file is required unless the run is design-day-only (design_day=True, annual=False). "
    "Pass the path of an EPW file as weather."
)
WEATHER_GROUND_HEAT_MESSAGE = (
    "The model contains {types} objects, and GroundHeatTransfer:Control enables their preprocessor. "
    "The Slab and Basement preprocessors derive ground temperatures from the weather file, so this "
    "model cannot be simulated without one. Pass the path of an EPW file as weather."
)
WEATHER_DEFAULT_FILE_MESSAGE = (
    "The run directory {run_dir} contains in.epw, which EnergyPlus reads when no weather file is given. "
    "Remove it, choose another output_dir, or pass it explicitly as weather."
)


def admit_weather(
    weather: str | Path | None,
    *,
    model: IDFDocument,
    design_day: bool,
    annual: bool,
    expand_objects: bool,
    run_dir: str | Path | None = None,
) -> Path | None:
    """Decide whether a simulation request may proceed with the given weather argument.

    The rules are evaluated in order, and the first that applies decides:

    1. An empty string is refused, because it would resolve to the working
       directory.
    2. A path that does not resolve to a file is refused with the
       ``Weather file not found`` message.
    3. A path that resolves to a file is returned, resolved.
    4. ``None`` is refused unless the run is design-day-only
       (``design_day=True`` and ``annual=False``).
    5. ``None`` is refused when *expand_objects* is true and *model* contains
       ``GroundHeatTransfer:Slab:*`` objects with ``run_slab_preprocessor``
       set to ``Yes``, or ``GroundHeatTransfer:Basement:*`` objects with
       ``run_basement_preprocessor`` set to ``Yes``, in
       ``GroundHeatTransfer:Control``. Those preprocessors read the weather
       file; a preprocessor that the control object leaves at ``No``, or a
       model without the control object, runs no solver.
    6. ``None`` is refused when *run_dir* is given and already contains
       ``in.epw``, as decided by
       [refuse_default_weather][idfkit.simulation._common.refuse_default_weather].
    7. Otherwise ``None`` is returned, and the run proceeds without a
       weather file.

    Rule 6 is applied here, before version migration and the cache lookup,
    so that no subprocess runs for a request that will be refused.
    [prepare_run_directory][idfkit.simulation._common.prepare_run_directory]
    applies it again to the directory it prepares.

    Args:
        weather: The caller's weather argument.
        model: The model to be simulated, before version migration.
        design_day: Whether the run is design-day-only (``-D``).
        annual: Whether the run is annual (``-a``).
        expand_objects: Whether idfkit runs the preprocessors.
        run_dir: The local run directory requested by the caller, or
            ``None`` when the run will use a fresh temporary directory.

    Returns:
        The resolved weather file path, or ``None`` for a run without a
        weather file.

    Raises:
        SimulationError: If any of rules 1, 2, 4, 5 or 6 refuses the request.
    """
    from ..exceptions import SimulationError

    if isinstance(weather, str) and weather == "":
        raise SimulationError(WEATHER_EMPTY_STRING_MESSAGE)

    if weather is not None:
        weather_path = Path(weather).resolve()
        if not weather_path.is_file():
            msg = f"Weather file not found: {weather_path}"
            raise SimulationError(msg)
        return weather_path

    if not (design_day and not annual):
        raise SimulationError(WEATHER_REQUIRED_MESSAGE)

    if expand_objects:
        from .expand import enabled_ground_heat_object_types

        types = enabled_ground_heat_object_types(model)
        if types:
            raise SimulationError(WEATHER_GROUND_HEAT_MESSAGE.format(types=", ".join(types)))

    if run_dir is not None:
        refuse_default_weather(Path(run_dir).resolve())

    return None


def refuse_default_weather(run_dir: Path) -> None:
    """Refuse a run without a weather file whose run directory already holds ``in.epw``.

    EnergyPlus reads ``in.epw`` from its working directory when no weather
    file is given, so such a run would silently use that file.

    Args:
        run_dir: The prepared run directory.

    Raises:
        SimulationError: If ``run_dir / "in.epw"`` exists.
    """
    from ..exceptions import SimulationError

    if (run_dir / "in.epw").exists():
        raise SimulationError(WEATHER_DEFAULT_FILE_MESSAGE.format(run_dir=run_dir))


def resolve_config(energyplus: EnergyPlusConfig | None) -> EnergyPlusConfig:
    """Resolve EnergyPlus config, auto-discovering if needed.

    Args:
        energyplus: Optional pre-configured config.

    Returns:
        Validated EnergyPlusConfig.
    """
    if energyplus is not None:
        return energyplus
    return find_energyplus()


def ensure_sql_output(model: IDFDocument) -> None:
    """Add Output:SQLite to the model if not already present.

    Args:
        model: The model to modify in place.
    """
    if "Output:SQLite" not in model:
        model.add("Output:SQLite", "", option_type="SimpleAndTabular", validate=False)


def prep_outputs(model: IDFDocument) -> None:
    """Add standard output objects to the model if not already present.

    Ensures the model includes:

    - ``Output:SQLite`` (SimpleAndTabular) — for SQL-based result queries
    - ``Output:Table:SummaryReports`` (AllSummary) — for tabular reports
    - ``Output:VariableDictionary`` (Regular) — for ``.rdd`` / ``.mdd`` generation

    This is a superset of `ensure_sql_output`.

    Args:
        model: The model to modify in place.
    """
    ensure_sql_output(model)

    if "Output:Table:SummaryReports" not in model:
        model.add("Output:Table:SummaryReports", "", report_1="AllSummary", validate=False)

    if "Output:VariableDictionary" not in model:
        model.add("Output:VariableDictionary", "", key_field="Regular", validate=False)


def maybe_preprocess(
    original: IDFDocument,
    sim_model: IDFDocument,
    config: EnergyPlusConfig,
    weather_path: Path | None,
    expand_objects: bool,
    preprocessor_timeout: float | None = None,
) -> tuple[IDFDocument, bool]:
    """Run ground heat-transfer preprocessing if needed.

    The EnergyPlus CLI's ``-x`` flag runs ExpandObjects for HVACTemplate
    expansion, but does **not** invoke the Slab or Basement Fortran
    solvers.  When GHT objects are present we run the full preprocessing
    pipeline (ExpandObjects + Slab/Basement) ourselves and disable the
    ``-x`` flag.

    Args:
        original: The original (unmutated) model, used for GHT detection.
        sim_model: The working copy of the model.
        config: EnergyPlus configuration.
        weather_path: Resolved path to the weather file, or ``None`` when
            the run has no weather file. Weather admission guarantees that
            ``None`` reaches this function only for a model whose Slab and
            Basement preprocessors ``GroundHeatTransfer:Control`` leaves
            disabled, so that only ExpandObjects runs.
        expand_objects: Whether the caller requested expansion.
        preprocessor_timeout: Per-subprocess timeout (seconds) applied to
            ExpandObjects, Slab, and Basement individually. ``None`` defers
            to [resolve_preprocessor_timeout][idfkit.simulation._common.resolve_preprocessor_timeout]
            (env var ``IDFKIT_PREPROCESSOR_TIMEOUT`` or 120 s default).

    Returns:
        A ``(model, ep_expand)`` tuple where *model* is either the
        preprocessed model or the original *sim_model*, and *ep_expand*
        indicates whether EnergyPlus should still run ExpandObjects
        via the ``-x`` flag.
    """
    if not expand_objects:
        return sim_model, False

    from .expand import needs_ground_heat_preprocessing, run_preprocessing

    if needs_ground_heat_preprocessing(original):
        preprocessed = run_preprocessing(
            sim_model,
            energyplus=config,
            weather=weather_path,
            timeout=resolve_preprocessor_timeout(preprocessor_timeout),
        )
        return preprocessed, False  # Already expanded by preprocessing

    return sim_model, True  # Let EnergyPlus handle ExpandObjects via -x


def upload_results(local_dir: Path, remote_dir: Path, fs: FileSystem) -> None:
    """Upload all output files from a local directory to a remote file system.

    Args:
        local_dir: Local directory containing simulation outputs.
        remote_dir: Remote directory path for the file system.
        fs: File system backend to upload to.
    """
    for p in local_dir.iterdir():
        if p.is_file():
            remote_path = str(remote_dir / p.name)
            fs.write_bytes(remote_path, p.read_bytes())


async def async_upload_results(local_dir: Path, remote_dir: Path, fs: AsyncFileSystem) -> None:
    """Upload all output files from a local directory to a remote async file system.

    Local file reads are delegated to a thread via [asyncio.to_thread][]
    to avoid blocking the event loop.  Remote writes are dispatched
    concurrently via [asyncio.gather][].

    Args:
        local_dir: Local directory containing simulation outputs.
        remote_dir: Remote directory path for the file system.
        fs: Async file system backend to upload to.
    """
    import asyncio

    async def _upload_one(p: Path) -> None:
        remote_path = str(remote_dir / p.name)
        data = await asyncio.to_thread(p.read_bytes)
        await fs.write_bytes(remote_path, data)

    tasks = [asyncio.create_task(_upload_one(p)) for p in local_dir.iterdir() if p.is_file()]
    if tasks:
        await asyncio.gather(*tasks)


def prepare_run_directory(output_dir: str | Path | None, weather_path: Path | None) -> Path:
    """Create and populate the simulation run directory.

    Args:
        output_dir: Explicit output directory, or None for a temp dir.
        weather_path: Path to the weather file to copy, or ``None`` when the
            run has no weather file, in which case nothing is copied and the
            directory is checked by
            [refuse_default_weather][idfkit.simulation._common.refuse_default_weather].

    Returns:
        Path to the run directory.

    Raises:
        SimulationError: If *weather_path* is ``None`` and the run directory
            already contains ``in.epw``.
    """
    if output_dir is not None:
        run_dir = Path(output_dir).resolve()
        run_dir.mkdir(parents=True, exist_ok=True)
    else:
        run_dir = Path(tempfile.mkdtemp(prefix="idfkit_sim_"))

    if weather_path is None:
        refuse_default_weather(run_dir)
        return run_dir

    # Copy weather file into run dir
    dest = run_dir / weather_path.name
    if not dest.exists():
        shutil.copy2(weather_path, dest)

    return run_dir


def build_command(
    *,
    config: EnergyPlusConfig,
    idf_path: Path,
    weather_path: Path | None,
    output_dir: Path,
    output_prefix: str,
    output_suffix: Literal["C", "L", "D"],
    expand_objects: bool,
    annual: bool,
    design_day: bool,
    readvars: bool,
    extra_args: list[str] | None,
) -> list[str]:
    """Build the EnergyPlus command-line invocation.

    Args:
        config: EnergyPlus configuration.
        idf_path: Path to the IDF file.
        weather_path: Path to the weather file in the run dir, or ``None``
            to omit the ``-w`` argument.
        output_dir: Output directory path.
        output_prefix: Output file prefix.
        output_suffix: Output file naming suffix ("C", "L", or "D").
        expand_objects: Whether to run ExpandObjects.
        annual: Whether to run annual simulation.
        design_day: Whether to run design-day-only simulation.
        readvars: Whether to run ReadVarsESO.
        extra_args: Additional arguments.

    Returns:
        Command as a list of strings.
    """
    cmd: list[str] = [str(config.executable)]
    if weather_path is not None:
        cmd.extend(["-w", str(weather_path)])
    cmd += [
        "-d",
        str(output_dir),
        "-p",
        output_prefix,
        "-s",
        output_suffix,
        "-i",
        str(config.idd_path),
    ]

    if expand_objects:
        cmd.append("-x")
    if annual:
        cmd.append("-a")
    if design_day:
        cmd.append("-D")
    if readvars:
        cmd.append("-r")
    if extra_args:
        cmd.extend(extra_args)

    cmd.append(str(idf_path))

    return cmd
