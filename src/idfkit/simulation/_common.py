"""Shared helpers for sync and async simulation runners.

Internal module — not part of the public API.
"""

from __future__ import annotations

import dataclasses
import filecmp
import os
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from ._run_dir import RunDirLease, register_temp_run_dir
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
    from ..document import AnyIDFDocument
    from ..migration.report import MigrationReport
    from .fs import AsyncFileSystem, FileSystem
    from .result import SimulationResult


def _migration_target(
    *,
    model: AnyIDFDocument,
    config: EnergyPlusConfig,
    auto_migrate: bool,
) -> tuple[int, int, int] | None:
    """Decide whether *model* must be migrated to run on *config*, shared by both resolvers.

    Both versions are matched to their release line first, the way schema selection
    and ``as_version`` match a document's version: a file headed ``Version, 9.0;``
    loads as ``(9, 0, 0)``, and the 9.0 release (and its install) is 9.0.1. A version
    with no supported release line is compared as it is, so a model newer than the
    installed EnergyPlus still raises ``VersionMismatchError`` and an unsupported one
    still raises ``UnsupportedVersionError`` from the chain planner.

    Returns:
        ``None`` when the model already matches the installed release, else the
        release to migrate it to.

    Raises:
        VersionMismatchError: If the model is newer than the installed EnergyPlus, or
            a migration is needed and *auto_migrate* is ``False``.
        UnsupportedVersionError: If a migration is needed from or to a version with
            no supported release.
    """
    from ..exceptions import VersionMismatchError
    from ..migration.chain import plan_migration_chain
    from ..versions import find_release

    source = find_release(model.version) or model.version
    target = find_release(config.version) or config.version

    if source == target:
        return None

    if source > target:
        raise VersionMismatchError(current=source, target=target)

    chain = plan_migration_chain(source, target)
    if not auto_migrate:
        raise VersionMismatchError(current=source, target=target, migration_chain=chain)
    return target


def resolve_version_mismatch(
    *,
    model: AnyIDFDocument,
    config: EnergyPlusConfig,
    auto_migrate: bool,
) -> tuple[AnyIDFDocument, MigrationReport | None]:
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
    """
    target = _migration_target(model=model, config=config, auto_migrate=auto_migrate)
    if target is None:
        return model, None

    from ..migration.runner import migrate

    report = migrate(model, target_version=target, energyplus=config)
    return report.migrated_model, report


async def async_resolve_version_mismatch(
    *,
    model: AnyIDFDocument,
    config: EnergyPlusConfig,
    auto_migrate: bool,
) -> tuple[AnyIDFDocument, MigrationReport | None]:
    """Async counterpart to [resolve_version_mismatch][idfkit.simulation._common.resolve_version_mismatch].

    Differs only in that the migration step is dispatched through
    [async_migrate()][idfkit.migration.async_runner.async_migrate] so it does
    not block the event loop.
    """
    from ..migration.async_runner import async_migrate

    target = _migration_target(model=model, config=config, auto_migrate=auto_migrate)
    if target is None:
        return model, None

    report = await async_migrate(model, target_version=target, energyplus=config)
    return report.migrated_model, report


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


def admit_model(model: object, func: str = "simulate") -> None:
    """Refuse a *model* that is not a document, before it reaches an attribute it lacks.

    ``migrate(doc, ...).migrated_model`` was ``None`` for a model already at the target, and
    passing that on failed deep in the run with ``'NoneType' object has no attribute 'version'``.

    Raises:
        TypeError: If *model* is not an [IDFDocument][idfkit.document.IDFDocument] of any release.
    """
    from ..document import IDFDocument

    if isinstance(model, IDFDocument):
        return
    msg = f"{func}(model, ...): model must be an IDFDocument, got {type(model).__name__} {model!r}"
    if isinstance(model, (str, Path)):
        msg += "; load it first with load_idf(path) or load_epjson(path)"
    raise TypeError(msg)


def admit_weather(
    weather: str | Path | None,
    *,
    model: AnyIDFDocument,
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


ANNUAL_WITHOUT_RUN_PERIOD_MESSAGE = (
    "annual=True, but the model has no RunPeriod. EnergyPlus would warn that it is adding one and then "
    "simulate no environment, reporting success with empty results. Add a run period first, e.g. "
    'model.add("RunPeriod", "Annual", begin_month=1, begin_day_of_month=1, end_month=12, end_day_of_month=31), '
    "or run without annual=True."
)


def admit_annual(model: AnyIDFDocument, *, annual: bool) -> None:
    """Refuse an annual run (``-a``) of a model that has no ``RunPeriod``.

    Given ``-a`` and no run period, EnergyPlus warns that it is adding a full-year run period, then
    simulates no environment at all (not even the design days) and exits with success, so every
    result is empty. ``RunPeriod:CustomRange`` (EnergyPlus 8.9) counts as a run period.

    Args:
        model: The model to be simulated, before version migration.
        annual: Whether the run is annual (``-a``).

    Raises:
        SimulationError: If *annual* is true and *model* has no run period.
    """
    if annual and "RunPeriod" not in model and "RunPeriod:CustomRange" not in model:
        from ..exceptions import SimulationError

        raise SimulationError(ANNUAL_WITHOUT_RUN_PERIOD_MESSAGE)


DESIGN_DAY_WITHOUT_DESIGN_DAYS_MESSAGE = (
    "design_day=True, but the model has no SizingPeriod:DesignDay. EnergyPlus would stop with "
    "'Errors found in Weather Data Input', although the weather file is not at fault. Add design days "
    "first, e.g. DesignDayManager(ddy_path).apply_to_model(model) or apply_ashrae_sizing(model, station) "
    "from idfkit.weather, or run without design_day=True."
)


def admit_design_day(model: AnyIDFDocument, *, design_day: bool) -> None:
    """Refuse a design-day-only run (``-D``) of a model that has no ``SizingPeriod:DesignDay``.

    Given ``-D`` and no design day, EnergyPlus reports "Requested Design Days only ... but no Design
    Days specified" and terminates with "Errors found in Weather Data Input", which points at the
    weather file rather than the model. ``SizingPeriod:WeatherFileDays`` and
    ``SizingPeriod:WeatherFileConditionType`` do not count: EnergyPlus counts only
    ``SizingPeriod:DesignDay`` objects for this check.

    Args:
        model: The model to be simulated, before version migration.
        design_day: Whether the run is design-day-only (``-D``).

    Raises:
        SimulationError: If *design_day* is true and *model* has no ``SizingPeriod:DesignDay``.
    """
    if design_day and "SizingPeriod:DesignDay" not in model:
        from ..exceptions import SimulationError

        raise SimulationError(DESIGN_DAY_WITHOUT_DESIGN_DAYS_MESSAGE)


NO_ENVIRONMENT_MESSAGE = (
    "The model gives EnergyPlus nothing to simulate: {reasons}. EnergyPlus would warn and report "
    "success with empty results. Add a run period, e.g. "
    'model.add("RunPeriod", "Annual", begin_month=1, begin_day_of_month=1, end_month=12, end_day_of_month=31), '
    "or design days, e.g. DesignDayManager(ddy_path).apply_to_model(model) from idfkit.weather, "
    "or set SimulationControl's run_simulation_for_* fields to Yes."
)

_SIZING_PERIOD_TYPES = (
    "SizingPeriod:DesignDay",
    "SizingPeriod:WeatherFileDays",
    "SizingPeriod:WeatherFileConditionType",
)
_SIZING_CALCULATION_FIELDS = (
    "do_zone_sizing_calculation",
    "do_system_sizing_calculation",
    "do_plant_sizing_calculation",
)


def _simulation_control_flag(model: AnyIDFDocument, field_name: str, *, default: bool) -> bool:
    """A ``SimulationControl`` Yes/No field, or its schema default when blank or the object is absent."""
    control = model["SimulationControl"].first()
    value = control.get(field_name) if control is not None else None
    if not isinstance(value, str) or not value.strip():
        return default
    return value.strip().lower() == "yes"


def admit_environments(model: AnyIDFDocument, *, annual: bool, design_day: bool) -> None:
    """Refuse a default-mode run (no ``-a``, no ``-D``) in which EnergyPlus would simulate nothing.

    Without either flag, ``SimulationControl`` decides what runs: weather-file run periods
    (``RunPeriod``) and sizing periods (``SizingPeriod:*``), both on by default. A model with
    neither, as ``new_document()`` makes, runs no environment, and EnergyPlus warns and exits with
    success, so every result is empty. Sizing periods also count when only a sizing calculation
    (``do_zone_sizing_calculation`` and its siblings) is on. *annual* and *design_day* runs are
    checked by [admit_annual][idfkit.simulation._common.admit_annual] and
    [admit_design_day][idfkit.simulation._common.admit_design_day].

    Args:
        model: The model to be simulated, before version migration.
        annual: Whether the run is annual (``-a``).
        design_day: Whether the run is design-day-only (``-D``).

    Raises:
        SimulationError: If neither flag is set and the model has no environment that runs.
    """
    if annual or design_day:
        return
    has_run_period = "RunPeriod" in model or "RunPeriod:CustomRange" in model
    has_sizing_period = any(t in model for t in _SIZING_PERIOD_TYPES)
    run_weather = _simulation_control_flag(model, "run_simulation_for_weather_file_run_periods", default=True)
    run_sizing = _simulation_control_flag(model, "run_simulation_for_sizing_periods", default=True)
    do_sizing = any(_simulation_control_flag(model, f, default=False) for f in _SIZING_CALCULATION_FIELDS)
    if (has_run_period and run_weather) or (has_sizing_period and (run_sizing or do_sizing)):
        return

    reasons: list[str] = []
    if not has_run_period:
        reasons.append("it has no RunPeriod")
    elif not run_weather:
        reasons.append("SimulationControl turns off weather-file run periods")
    if not has_sizing_period:
        reasons.append("no SizingPeriod:DesignDay or other sizing period")
    else:
        reasons.append("SimulationControl turns off sizing periods and every sizing calculation")
    from ..exceptions import SimulationError

    raise SimulationError(NO_ENVIRONMENT_MESSAGE.format(reasons=" and ".join(reasons)))


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


def ensure_sql_output(model: AnyIDFDocument) -> None:
    """Add Output:SQLite to the model if not already present.

    Args:
        model: The model to modify in place.
    """
    if "Output:SQLite" not in model:
        model["Output:SQLite"].add(option_type="SimpleAndTabular", validate=False)


def prep_outputs(model: AnyIDFDocument) -> None:
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
        model["Output:Table:SummaryReports"].add(reports=[{"report_name": "AllSummary"}], validate=False)

    if "Output:VariableDictionary" not in model:
        model.add("Output:VariableDictionary", "", key_field="Regular", validate=False)


def maybe_preprocess(
    sim_model: AnyIDFDocument,
    config: EnergyPlusConfig,
    weather_path: Path | None,
    expand_objects: bool,
    preprocessor_timeout: float | None = None,
) -> tuple[AnyIDFDocument, bool]:
    """Run ground heat-transfer preprocessing if needed.

    The EnergyPlus CLI's ``-x`` flag runs ExpandObjects for HVACTemplate
    expansion, but does **not** invoke the Slab or Basement Fortran
    solvers.  When GHT objects are present we run the full preprocessing
    pipeline (ExpandObjects + Slab/Basement) ourselves and disable the
    ``-x`` flag.

    Args:
        sim_model: The working copy of the model, used both to detect ground heat-transfer
            objects and as the preprocessing input.
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

    if needs_ground_heat_preprocessing(sim_model):
        preprocessed = run_preprocessing(
            sim_model,
            energyplus=config,
            weather=weather_path,
            timeout=resolve_preprocessor_timeout(preprocessor_timeout),
        )
        return preprocessed, False  # Already expanded by preprocessing

    return sim_model, True  # Let EnergyPlus handle ExpandObjects via -x


def publish_exclude(weather_path: Path | None) -> frozenset[str]:
    """Names in a local run directory that an upload to a file system leaves out.

    The run's copy of the weather file is an input the caller already has, and
    the cache's metadata file is not a simulation output.

    Args:
        weather_path: The weather file as [admit_weather][idfkit.simulation._common.admit_weather]
            resolved it (the name the run directory holds it under), or ``None``.

    Returns:
        The file names [upload_results][idfkit.simulation._common.upload_results] skips.
    """
    from .cache import CACHE_META_FILE

    names = {CACHE_META_FILE}
    if weather_path is not None:
        names.add(weather_path.name)
    return frozenset(names)


def upload_results(local_dir: Path, remote_dir: Path, fs: FileSystem, *, exclude: frozenset[str] = frozenset()) -> None:
    """Upload all output files from a local directory to a remote file system.

    Args:
        local_dir: Local directory containing simulation outputs.
        remote_dir: Remote directory path for the file system.
        fs: File system backend to upload to.
        exclude: File names in *local_dir* not to upload (a cache entry's
            metadata file, for example).
    """
    fs.makedirs(remote_dir, exist_ok=True)
    for p in local_dir.iterdir():
        if p.is_file() and p.name not in exclude:
            remote_path = str(remote_dir / p.name)
            fs.write_bytes(remote_path, p.read_bytes())


async def async_upload_results(
    local_dir: Path, remote_dir: Path, fs: AsyncFileSystem, *, exclude: frozenset[str] = frozenset()
) -> None:
    """Upload all output files from a local directory to a remote async file system.

    Local file reads are delegated to a thread via [asyncio.to_thread][]
    to avoid blocking the event loop.  Remote writes are dispatched
    concurrently via [asyncio.gather][].

    Args:
        local_dir: Local directory containing simulation outputs.
        remote_dir: Remote directory path for the file system.
        fs: Async file system backend to upload to.
        exclude: File names in *local_dir* not to upload.
    """
    import asyncio

    async def _upload_one(p: Path) -> None:
        remote_path = str(remote_dir / p.name)
        data = await asyncio.to_thread(p.read_bytes)
        await fs.write_bytes(remote_path, data)

    await fs.makedirs(remote_dir, exist_ok=True)
    tasks = [asyncio.create_task(_upload_one(p)) for p in local_dir.iterdir() if p.is_file() and p.name not in exclude]
    if tasks:
        await asyncio.gather(*tasks)


def restore_cached_result(
    entry: SimulationResult, output_dir: str | Path | None, weather_path: Path | None = None
) -> SimulationResult:
    """Copy a cache hit's files into *output_dir* and return a result that reads the copy.

    The copy lands in *output_dir* (created when missing), where a fresh run
    would have written, with the weather file, which the cache entry does not
    hold, copied in as a fresh run copies it. Without an *output_dir* nothing
    is copied: *entry* is returned as is, so a hit costs no disk and its
    ``run_dir`` is the cache entry itself, to be treated as read-only.

    Args:
        entry: The result [SimulationCache.get][idfkit.simulation.cache.SimulationCache.get]
            returned, whose ``run_dir`` is the cache entry.
        output_dir: The run's requested local output directory, or ``None``.
        weather_path: The run's weather file, or ``None`` for a run without one.

    Returns:
        A result with ``cached=True`` whose ``run_dir`` holds the copied files,
        or *entry* itself when *output_dir* is ``None``.
    """
    from .cache import CACHE_META_FILE

    if output_dir is None:
        return entry
    run_dir = Path(output_dir).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(entry.run_dir, run_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns(CACHE_META_FILE))
    if weather_path is not None:
        prepare_run_directory(run_dir, weather_path)
    # replace() carries every field of the cache entry, so one added to SimulationResult later
    # reaches the restored result without this function naming it.
    return dataclasses.replace(entry, run_dir=run_dir, cached=True, owns_run_dir=False, fs=None, async_fs=None)


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
    return _populate_run_directory(run_dir, weather_path)


def _populate_run_directory(run_dir: Path, weather_path: Path | None) -> Path:
    """Copy *weather_path* into *run_dir*, or check it has no stale ``in.epw`` when there is none."""
    if weather_path is None:
        refuse_default_weather(run_dir)
        return run_dir

    # Copy weather file into run dir, replacing a stale copy left by an earlier
    # run with a different weather file of the same name. A file that already
    # is the caller's weather file, or has identical content, is left alone.
    dest = run_dir / weather_path.name
    if not dest.exists() or (
        not os.path.samefile(weather_path, dest) and not filecmp.cmp(weather_path, dest, shallow=False)
    ):
        shutil.copy2(weather_path, dest)

    return run_dir


class RunDirectoryGuard:
    """Create the run directory, and delete it again if idfkit made it and the run then raises.

    ``simulate()`` without an ``output_dir`` runs in a new temporary directory, which the
    returned result owns and deletes on cleanup. A run that raises returns no result, so
    nothing could reach that directory afterwards: leaving the ``with`` block with an
    exception deletes it. A caller's ``output_dir`` is never deleted.
    """

    def __init__(self) -> None:
        self._owned: Path | None = None
        self._lease: RunDirLease | None = None

    def prepare(self, output_dir: str | Path | None, weather_path: Path | None) -> Path:
        """Create and populate the run directory, as [prepare_run_directory][idfkit.simulation._common.prepare_run_directory]."""
        if output_dir is not None:
            return prepare_run_directory(output_dir, weather_path)
        self._owned = Path(tempfile.mkdtemp(prefix="idfkit_sim_"))
        # Registered before anything else can fail, so the result built for it finds the lease; this guard
        # holds it until then, and the result (with its copies) from then on.
        self._lease = register_temp_run_dir(self._owned)
        return _populate_run_directory(self._owned, weather_path)

    def __enter__(self) -> RunDirectoryGuard:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, *exc: object) -> None:
        if exc_type is not None and self._owned is not None:
            if self._lease is not None:
                self._lease.release()  # deleted here, without the warning meant for a missing cleanup
            shutil.rmtree(self._owned, ignore_errors=True)


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
