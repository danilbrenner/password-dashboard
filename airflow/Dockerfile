FROM apache/airflow:2.8.0-python3.10

USER airflow
RUN pip install yoyo-migrations azure-storage-blob pandas sqlalchemy psycopg2-binary

USER airflow