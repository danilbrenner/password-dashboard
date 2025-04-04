
def load_data(**kwargs):
    import os
    import sqlite3
    import pandas as pd
    from sqlalchemy import create_engine

    ti = kwargs['ti']
    sqlite_path = ti.xcom_pull(task_ids='get_latest_backup')
    pg_conn_string = os.environ.get("PASSWORD_DASHBOARD_DB")
    pg_schema = "raw"
    tables = [ "sync_events", "logins" ]

    sqlite_conn = sqlite3.connect(sqlite_path)
    pg_engine = create_engine(pg_conn_string)

    for table in tables:
        print(f"Copying table: {table}")
        df = pd.read_sql_query(f"SELECT * FROM {table}", sqlite_conn)
        df.to_sql(table, pg_engine, schema=pg_schema, if_exists='replace', index=False)

