
def get_latest_backup():
    from azure.storage.blob import ContainerClient, BlobClient
    import os

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

    download_file_path = "./current_backup.sqlite"

    if os.path.exists(download_file_path):
        os.remove(download_file_path)

    with open(download_file_path, "wb") as file:
        download_stream = blob_client.download_blob()
        file.write(download_stream.readall())

    print(f"✅ Downloaded latest backup: {latest_blob.name} to {download_file_path}")
    return download_file_path
