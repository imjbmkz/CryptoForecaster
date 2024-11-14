import os, sys
from datetime import datetime as dt
from loguru import logger
from cryptomodel.utils import get_dbconn, get_minio
from cryptomodel.cryptoml import CryptoML

if __name__=="__main__":

    # Logging configuration
    log_date = dt.now().strftime("%Y%m%d")
    logger.remove()
    logger.add(f"logs/std_out_{log_date}.log", level="INFO", format="{time}: {level} - {message}")
    logger.add(f"logs/std_err_{log_date}.log", level="ERROR", format="{time}: {level} - {message}")
    logger.add(sys.stdout, level="INFO", format="{time}: {level} - {message}")
    logger.add(sys.stderr, level="ERROR", format="{time}: {level} - {message}")
    logger.info("App has started")

    # Get database credentials
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    # MinIO Credentials 
    MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
    MINIO_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

    # Initialize CryptoML class, database connection engine, and Minio client
    crypto_ml = CryptoML()
    engine = get_dbconn("postgresql+psycopg2", db_host=DB_HOST, db_name=DB_NAME, db_user=DB_USER, db_pass=DB_PASS, db_port=DB_PORT)
    minio_client = get_minio(
        minio_endpoint=MINIO_ENDPOINT,
        minio_access_key_id=MINIO_ACCESS_KEY_ID,
        minio_secret_access_key=MINIO_SECRET_ACCESS_KEY
    )

    crypto_ml.run(
        "SELECT * FROM market_chart WHERE coin_id='ethereum' ORDER BY timestamp",
        engine, 
        ["timestamp","price"],
        ["feature_1", "feature_2", "feature_3", "feature_4", "feature_5"],
        "response",
        minio_client,
        MINIO_BUCKET_NAME
    )