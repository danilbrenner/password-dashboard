import os
from yoyo import read_migrations, get_backend

def run_db_migrations():
    database_url = os.environ.get("PASSWORD_DASHBOARD_DB")
    backend = get_backend(database_url)

    migrations = read_migrations("migrations")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
