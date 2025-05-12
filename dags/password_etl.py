from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from db_migrations import run_db_migrations
from db_backup_loader import load_backup, download_backup
from additional_data_loader import load_additional_data, download_additional_data
from data_transfromation import transform_data

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

    download_backup = PythonOperator(
        task_id='download_backup',
        python_callable=download_backup,
        op_kwargs={'name': 'Airflow'}
    )

    load_backup_data = PythonOperator(
        task_id='load_backup_data',
        python_callable=load_backup,
        op_kwargs={'name': 'Airflow'}
    )

    download_additional_data = PythonOperator(
        task_id='download_additional_data',
        python_callable=download_additional_data,
        op_kwargs={'name': 'Airflow'}
    )

    load_additional_data = PythonOperator(
        task_id='load_additional_data',
        python_callable=load_additional_data,
        op_kwargs={'name': 'Airflow'}
    )

    transform_data_step = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={'name': 'Airflow'}
    )

    (
            run_db_migrations_task
            >> download_additional_data
            >> load_additional_data
            >> download_backup
            >> load_backup_data
            >> transform_data_step
    )

