import os
import shutil
import json
import duckdb
from kafka import KafkaProducer

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


@asset(deps=[copy_duckdb_file_asset])
def query_analytics_db_asset():
    logger = get_dagster_logger()
    target_full_path = file_relative_path(__file__, TARGET_PATH)

    conn = duckdb.connect(target_full_path, read_only=True)
    try:
        q1 = """
             select datediff('days', latest_export_ts, current_date) as sync_age
             from fact_master_passwords
             order by latest_export_ts desc limit 1; \
             """
        res1 = conn.execute(q1).fetchall()

        q2 = """
             with latest_session as (select session_type,
                                            max(cast(export_ts as date)) as last_sync
                                     from fact_exchange_sessions
                                     group by session_type)
             select datediff('day', last_sync, current_date) as sync_age,
                    session_type                             as export_type
             from latest_session
             order by session_type; \
             """

        res2 = conn.execute(q2).fetchall()

        results = {
            "type": "PasswordDashboardAnalytics",
            "master_passwords_sync_age": res1[0][0] if res1 else None,
            "session_sync_ages": [
                {"sync_age": row[0], "export_type": row[1]}
                for row in res2
            ]
        }

        json_str = json.dumps(results, indent=2, default=str)
        logger.info(f"Analytics Query Results:\n{json_str}")

        kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "orb_weather_kafka:9092")
        kafka_topic = os.getenv("KAFKA_TOPIC", "password_dashboard_analytics")

        try:
            producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
            producer.send(kafka_topic, json_str.encode("utf-8"))
            producer.flush()
            logger.info(f"Sent results to Kafka topic '{kafka_topic}' at {kafka_bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to send to Kafka: {e}")

        return results
    finally:
        conn.close()


# Job that materializes all assets: dbt models + copy_duckdb_file_asset
materialize_dbt_and_copy = define_asset_job(
    name="materialize_dbt_and_copy",
    selection=AssetSelection.all(),  # or narrow it later if you like
)

defs = Definitions(
    assets=[dbt_project_assets, copy_duckdb_file_asset, query_analytics_db_asset],
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
