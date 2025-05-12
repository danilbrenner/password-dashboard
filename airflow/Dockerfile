FROM apache/airflow:2.8.1-python3.10

USER airflow

COPY airflow/requirements.txt .
RUN pip install -r requirements.txt

USER airflow