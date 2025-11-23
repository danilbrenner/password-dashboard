from dagster import file_relative_path
from dagster_dbt import DbtCliResource, dbt_assets

DBT_PROJECT_DIR = file_relative_path(__file__, "../../passwords_etl")

dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)

@dbt_assets(manifest=DBT_PROJECT_DIR + "/target/manifest.json")
def dbt_project_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


