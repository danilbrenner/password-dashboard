from dagster import Definitions, ScheduleDefinition, job
from .assets import dbt_resource, dbt_project_assets

# Define a job to materialize the dbt assets
@job
def materialize_dbt_assets():
    dbt_project_assets()

defs = Definitions(
    assets=[dbt_project_assets],
    resources={
        "dbt": dbt_resource,
    },
    schedules=[
        ScheduleDefinition(
            name="nightly_materialization",
            cron_schedule="0 1 * * *",  # Every day at 1 AM
            job=materialize_dbt_assets,
        )
    ],
)
