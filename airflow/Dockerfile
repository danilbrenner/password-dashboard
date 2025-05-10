FROM apache/airflow:2.8.0-python3.10

USER airflow

COPY pipeline/requirements.txt .
RUN pip install -r requirements.txt

USER airflow