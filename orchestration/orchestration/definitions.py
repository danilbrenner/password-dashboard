import os
import shutil

from dagster import (
    Definitions,
    ScheduleDefinition,
    asset,
    AssetSelection,
    define_asset_job,
    get_dagster_logger,
    file_relative_path,
)
from .assets import dbt_resource, dbt_project_assets

# Paths for your DuckDB file
SOURCE_PATH = "../../passwords_etl/passwords.duckdb"
TARGET_PATH = "/warehouse/analytics.duckdb"


# This asset runs *after* all dbt assets and copies the DuckDB file
@asset(deps=[dbt_project_assets])
def copy_duckdb_file_asset():
    logger = get_dagster_logger()

    source_full_path = file_relative_path(__file__, SOURCE_PATH)
    target_full_path = file_relative_path(__file__, TARGET_PATH)

    os.makedirs(os.path.dirname(target_full_path), exist_ok=True)

    # Copy to a temp file first, then atomically move it to avoid file locking/corruption issues
    temp_target_path = target_full_path + ".tmp"
    shutil.copy2(source_full_path, temp_target_path)
    os.replace(temp_target_path, target_full_path)

    logger.info(f"Copied {SOURCE_PATH} -> {TARGET_PATH}")


# Job that materializes all assets: dbt models + copy_duckdb_file_asset
materialize_dbt_and_copy = define_asset_job(
    name="materialize_dbt_and_copy",
    selection=AssetSelection.all(),  # or narrow it later if you like
)

defs = Definitions(
    assets=[dbt_project_assets, copy_duckdb_file_asset],
    resources={
        "dbt": dbt_resource,
    },
    schedules=[
        ScheduleDefinition(
            name="nightly_materialization",
            cron_schedule="0 */4 * * *",
            job=materialize_dbt_and_copy,
        )
    ],
)
