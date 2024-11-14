from loguru import logger
from sqlalchemy import create_engine, URL, Engine, text, CursorResult
from minio import Minio

def get_dbconn(db_driver: str, db_host: str, db_user: str, db_pass: str, db_port: int, db_name: str) -> Engine:
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
        logger.error(e)
        raise e
    
def get_minio(minio_endpoint: str, minio_access_key_id: str, minio_secret_access_key: str):
    # Configure the MinIO client with your MinIO server details
    try:
        return Minio(
            minio_endpoint,  
            access_key=minio_access_key_id,
            secret_key=minio_secret_access_key,
            secure=False,  # Set to True if using HTTPS
        )
    
    except Exception as e:
        logger.error(e)
        raise e

def run_query(engine: Engine, sql: str) -> CursorResult:
    try:
        with engine.connect() as con:
            result = con.execute(text(sql))
            con.commit()
            return result
    
    except Exception as e:
        logger.error(e)
        raise e