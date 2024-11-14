import os
from loguru import logger
from fastapi import FastAPI
from cryptoapi import utils 
from cryptoapi import cryptoapi as c

app = FastAPI()

# MinIO Credentials 
MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
MINIO_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

# Database Credentials 
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = utils.get_dbconn("postgresql+psycopg2", db_host=DB_HOST, db_name=DB_NAME, db_user=DB_USER, db_pass=DB_PASS, db_port=DB_PORT)
minio_client = utils.get_minio(MINIO_ENDPOINT, MINIO_ACCESS_KEY_ID, MINIO_SECRET_ACCESS_KEY)

c.get_latest_model(minio_client, MINIO_BUCKET_NAME)
logger.info("The latest model has been downloaded.")

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Welcome to Crypto Forecaster v0.1!"
    }

@app.post("/get_latest_model")
async def get_latest_model():
    try:
        model_name = c.get_latest_model(minio_client, MINIO_BUCKET_NAME)
        return {
            "status": "success",
            "message": f"Successfully fetched latest model {model_name}."
        }
    except Exception as e:
        logger.error(e)
        return {
            "status": "error",
            "message": e
        }

@app.get("/get_predictions")
async def get_predictions(n: int, coin_id: str):
    try:
        model = c.load_model()
        df_predictions = c.generate_predictions(n, coin_id, engine, model)
        return {
            "status": "success",
            "data": df_predictions.to_dict(orient="records")
        }
    
    except Exception as e:
        logger.error(e)
        return {
            "status": "error",
            "message": e
        }