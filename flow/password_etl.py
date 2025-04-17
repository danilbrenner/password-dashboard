

def my_etl():
    from db_migrations import run_db_migrations
    from db_backup_loader import download_backup
    from additional_data_loader import download_additional_data
    from additional_data_loader import load_additional_data
    from data_transfromation import transform_data
    from db_backup_loader import load_backup

    print("Running DB migrations...")
    run_db_migrations()

    print("Downloading backup...")
    download_backup()

    print("Loading backup...")
    load_backup()

    print("Downloading additional data...")
    download_additional_data()

    print("Loading additional data...")
    load_additional_data()

    print("Transforming data...")
    transform_data()

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    my_etl()