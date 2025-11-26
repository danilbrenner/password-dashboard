import os
import shutil
from pipes import SOURCE

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
    shutil.copy2(source_full_path, target_full_path)
    
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
            cron_schedule="0 19 * * *", 
            job=materialize_dbt_and_copy,
        )
    ],
)
