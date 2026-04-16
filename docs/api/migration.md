# Migration API

Forward-migrate IDF models across EnergyPlus versions by orchestrating the
`Transition-VX-to-VY` binaries shipped in `PreProcess/IDFVersionUpdater`.

## migrate

::: idfkit.migration.runner.migrate
    options:
      show_root_heading: true
      show_source: true

## async_migrate

::: idfkit.migration.async_runner.async_migrate
    options:
      show_root_heading: true
      show_source: true

## MigrationReport

::: idfkit.migration.report.MigrationReport
    options:
      show_root_heading: true
      show_source: true
      members:
        - migrated_model
        - source_version
        - target_version
        - requested_target
        - steps
        - diff
        - success
        - completed_steps
        - failed_step
        - summary

## MigrationStep

::: idfkit.migration.report.MigrationStep
    options:
      show_root_heading: true
      show_source: true

## MigrationDiff

::: idfkit.migration.report.MigrationDiff
    options:
      show_root_heading: true
      show_source: true
      members:
        - added_object_types
        - removed_object_types
        - object_count_delta
        - field_changes
        - is_empty

## FieldDelta

::: idfkit.migration.report.FieldDelta
    options:
      show_root_heading: true
      show_source: true

## MigrationProgress

::: idfkit.migration.progress.MigrationProgress
    options:
      show_root_heading: true
      show_source: true

## Migrator

::: idfkit.migration.protocol.Migrator
    options:
      show_root_heading: true
      show_source: true

## AsyncMigrator

::: idfkit.migration.protocol.AsyncMigrator
    options:
      show_root_heading: true
      show_source: true

## MigrationStepResult

::: idfkit.migration.protocol.MigrationStepResult
    options:
      show_root_heading: true
      show_source: true

## SubprocessMigrator

::: idfkit.migration.subprocess_backend.SubprocessMigrator
    options:
      show_root_heading: true
      show_source: true

## AsyncSubprocessMigrator

::: idfkit.migration.async_subprocess_backend.AsyncSubprocessMigrator
    options:
      show_root_heading: true
      show_source: true

## plan_migration_chain

::: idfkit.migration.chain.plan_migration_chain
    options:
      show_root_heading: true
      show_source: true

## document_diff

::: idfkit.migration.diff.document_diff
    options:
      show_root_heading: true
      show_source: true
