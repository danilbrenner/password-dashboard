from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from db_migrations import run_db_migrations
from get_latest_backup import get_latest_backup
from load_data import load_data

with DAG(
    dag_id='password_dashboard_etl',
    start_date=datetime(2025, 1, 1),
    schedule_interval="0 6 * * *",
    catchup=False
) as dag:

    run_db_migrations_task = PythonOperator(
        task_id='run_db_migrations',
        python_callable=run_db_migrations,
        op_kwargs={'name': 'Airflow'}
    )

    get_latest_backup = PythonOperator(
        task_id='get_latest_backup',
        python_callable=get_latest_backup,
        op_kwargs={'name': 'Airflow'}
    )

    copy_data = PythonOperator(
        task_id='copy_data',
        python_callable=load_data,
        op_kwargs={'name': 'Airflow'}
    )

    run_db_migrations_task >> get_latest_backup >> copy_data
