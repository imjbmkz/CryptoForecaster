from datetime import datetime as dt
from loguru import logger
from sqlalchemy import create_engine, URL, Engine, text, CursorResult

def timestamp_to_datetime(ts: int) -> dt:
    return dt.fromtimestamp(ts / 1000)

def get_conn(db_driver: str, db_host: str, db_user: str, db_pass: str, db_port: int, db_name: str) -> Engine:
    try:
        connection_string = URL.create(
            db_driver,
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name
        )
        return create_engine(connection_string)
    
    except Exception as e:
        # logger.error(e)
        raise e

def run_query(engine: Engine, sql: str) -> CursorResult:
    try:
        with engine.connect() as con:
            response = con.execute(text(sql))
            con.commit()
            return response
    
    except Exception as e:
        # logger.error(e)
        raise e