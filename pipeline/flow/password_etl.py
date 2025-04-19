

def my_etl():
    from db_migrations import run_db_migrations
    from db_backup_loader import download_backup
    from additional_data_loader import download_additional_data
    from additional_data_loader import load_additional_data
    from data_transfromation import transform_data
    from db_backup_loader import load_backup
    from datetime import datetime

    print(f"{datetime.now()}: Running DB migrations...")
    run_db_migrations()

    print(f"{datetime.now()}: Downloading backup...")
    download_backup()

    print(f"{datetime.now()}:Loading backup...")
    load_backup()

    print(f"{datetime.now()}:Downloading additional data...")
    download_additional_data()

    print(f"{datetime.now()}: Loading additional data...")
    load_additional_data()

    print(f"{datetime.now()}: Transforming data...")
    transform_data()

    print(f"{datetime.now()}: Pipeline completed successfully.")

if __name__ == "__main__":
    my_etl()