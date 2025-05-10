import os
import tempfile

tmp_dir = tempfile.gettempdir()
sqlite_file_name = "current_backup.sqlite"

def download_backup():
    from azure.storage.blob import ContainerClient, BlobClient

    conn_str = os.environ.get("BACKUP_AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.environ.get("BACKUP_AZURE_STORAGE_CONTAINER")

    if conn_str is None or container_name is None:
        raise ValueError("Backup azure storage must be set")

    container_client = ContainerClient.from_connection_string(conn_str, container_name)
    blobs = [
        blob for blob in container_client.list_blobs(name_starts_with='vaultbot/')
        if blob.name.endswith('.bcp')
    ]

    if not blobs:
        return None

    latest_blob = max(blobs, key=lambda b: b.last_modified)

    blob_client = BlobClient.from_connection_string(
        conn_str=conn_str,
        container_name=container_name,
        blob_name=latest_blob.name
    )

    download_file_path = os.path.join(tmp_dir, sqlite_file_name)

    with open(download_file_path, "wb") as file:
        download_stream = blob_client.download_blob()
        file.write(download_stream.readall())

    print(f"Downloaded latest backup: {latest_blob.name} to {download_file_path}")
    return download_file_path

def load_backup():
    import sqlite3
    import pandas as pd
    from sqlalchemy import create_engine, text

    sqlite_path = os.path.join(tmp_dir, sqlite_file_name)
    pg_conn_string = os.environ.get("PASSWORD_DASHBOARD_DB")
    pg_schema = "raw"
    tables = [ "sync_events", "logins" ]

    sqlite_conn = sqlite3.connect(sqlite_path)
    pg_engine = create_engine(pg_conn_string)

    with pg_engine.begin() as conn:
        for table in list(reversed(tables)):
            conn.execute(text(f"TRUNCATE TABLE {pg_schema}.{table};"))

    for table in tables:
        print(f"Copying table: {table}")
        df = pd.read_sql_query(f"SELECT * FROM {table}", sqlite_conn)
        df.to_sql(table, pg_engine, schema=pg_schema, if_exists='append', index=False)

