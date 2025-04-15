import os
import tempfile

tmp_dir = tempfile.gettempdir()
files = [ "important_logins.csv" ]

def download_additional_data():
    from azure.storage.blob import ContainerClient, BlobClient

    conn_str = os.environ.get("BACKUP_AZURE_STORAGE_CONNECTION_STRING")
    # container_name = os.environ.get("BACKUP_AZURE_STORAGE_CONTAINER")

    if conn_str is None: # or container_name is None:
        raise ValueError("Backup azure storage must be set")

    # container_client = ContainerClient.from_connection_string(conn_str, container_name)

    for file_name in files:
        blob_client = BlobClient.from_connection_string(
            conn_str=conn_str,
            container_name="data",
            blob_name=file_name
        )
        print(f"Loading file {file_name}")
        with open(os.path.join(tmp_dir, file_name), "wb") as file:
            download_stream = blob_client.download_blob()
            file.write(download_stream.readall())

def load_additional_data():
    import pandas as pd
    from sqlalchemy import create_engine

    pg_conn_string = os.environ.get("PASSWORD_DASHBOARD_DB")
    pg_schema = "raw"

    pg_engine = create_engine(pg_conn_string)

    for file_name in files:
        table = file_name.split(".")[0]
        print(f"Loading {file_name} into {table}...")
        df = pd.read_csv(os.path.join(tmp_dir, file_name))
        df.to_sql(table, pg_engine, schema=pg_schema, if_exists='replace', index=False)