import os
import datetime as dt
from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator

load_dotenv()

# CoinGecko API key
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

# MinIO connection
MINIO_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
MINIO_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

# Database connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# API connection
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")

default_args = {
    "owner": "josh",
    "start_date": dt.datetime(2024, 11, 13),
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=3),
    # Add other default args like retries, etc.
}

with DAG(
    default_args=default_args,
    dag_id="dag_run_scraper_and_model_docker_operator_v01",
    description="Run crypto_scraper and crypto_model using Docker operator in Airflow locally",
    # Set your desired schedule interval or use None for manual triggering
    # schedule_interval="0 */2 * * *", # every 2 hours
    catchup=False, # avoid running previous schedules
) as dag:
    
    crypto_scraper_task = DockerOperator(
        task_id="docker_crypto_scraper_task",
        docker_url="unix://var/run/docker.sock",  # Use the default Docker socket
        api_version="auto",  # Use "auto" to let Docker select the appropriate API version
        auto_remove=False,  # Remove the container when the task completes
        image="cryptoscraper",  # Replace with your Docker image and tag
        # container_name="test",
        # Set environment variables inside the contain
        environment={
            "COINGECKO_API_KEY": COINGECKO_API_KEY,
            "DB_HOST": DB_HOST,
            "DB_USER": DB_USER,
            "DB_PASS": DB_PASS,
            "DB_PORT": DB_PORT,
            "DB_NAME": DB_NAME,
        },
        command=["python", "main.py", "market_chart"],  # Replace with the command you want to run inside the container
        # network_mode="bridge",  # Specify the network mode if needed
        # volumes=["/host/path:/container/path"],  # Mount volumes if needed
        # dag=dag,
    )

    crypto_model_task = DockerOperator(
        task_id="docker_crypto_model_task",
        docker_url="unix://var/run/docker.sock",  # Use the default Docker socket
        api_version="auto",  # Use "auto" to let Docker select the appropriate API version
        auto_remove=False,  # Remove the container when the task completes
        image="cryptomodel",  # Replace with your Docker image and tag
        # container_name="test",
        # Set environment variables inside the contain
        environment={
            "DB_HOST": DB_HOST,
            "DB_USER": DB_USER,
            "DB_PASS": DB_PASS,
            "DB_PORT": DB_PORT,
            "DB_NAME": DB_NAME,
            "MINIO_ACCESS_KEY_ID": MINIO_ACCESS_KEY_ID,
            "MINIO_SECRET_ACCESS_KEY": MINIO_SECRET_ACCESS_KEY,
            "MINIO_ENDPOINT": MINIO_ENDPOINT,
            "MINIO_BUCKET_NAME": MINIO_BUCKET_NAME,
        },
        command=["python", "main.py"],  # Replace with the command you want to run inside the container
        # network_mode="bridge",  # Specify the network mode if needed
        # volumes=["/host/path:/container/path"],  # Mount volumes if needed
        dag=dag,
    )

    crypto_api_refresh_model = BashOperator(
        task_id="crypto_api_refresh_model_task",
        bash_command=f"""
            curl -X POST http://{API_HOST}:{API_PORT}/get_latest_model
        """,
        dag=dag
    )

    crypto_scraper_task >> crypto_model_task >> crypto_api_refresh_model