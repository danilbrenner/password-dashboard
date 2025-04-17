

def transform_data():
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    import os

    pg_conn_string = os.environ.get("PASSWORD_DASHBOARD_DB")
    pg_engine = create_engine(pg_conn_string)
    session_delegate = sessionmaker(bind=pg_engine)
    session = session_delegate()

    try:
        session.execute(text("call mart.sync_dim_logins()"))
        session.execute(text("call mart.sync_snapshots()"))
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Transaction rolled back due to error: {e}")
        raise
    finally:
        session.close()