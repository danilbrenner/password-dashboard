from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

from db_migrations import run_db_migrations

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

    task1 = BashOperator(
        task_id='print_date',
        bash_command='date'
    )

    run_db_migrations_task >> task1
