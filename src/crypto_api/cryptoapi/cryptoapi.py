import datetime as dt
import pandas as pd
import joblib
from loguru import logger
from sqlalchemy import Engine
from minio import Minio

def get_latest_model(minio_client: Minio, minio_bucket_name: str) -> str:
    try:
        models = list(minio_client.list_objects(minio_bucket_name, prefix="models/"))
        latest_model = models[-1]
        minio_client.fget_object(minio_bucket_name, latest_model.object_name, "regression_model.pkl")
        object_name = latest_model.object_name
        logger.info(f"{object_name} has been downloaded")
        return object_name
    except Exception as e:
        logger.error(e)
        raise e 

def load_model():
    return joblib.load("regression_model.pkl")

def feature_prep_past_n_records(df: pd.DataFrame, n_features: int=5, n_response: int=1) -> pd.DataFrame:
    features = []
    responses = []

    try:
    
        # Iterate over the DataFrame to create features and responses
        for i in range(len(df) - n_features - n_response + 1):
            feature_set = df["price"].iloc[i:i+n_features].values
            response_set = df["price"].iloc[i+n_features:i+n_features+n_response].values[0]
            features.append(feature_set)
            responses.append(response_set)

        df_reshaped = pd.DataFrame(features, columns=[f"feature_{i+1}" for i in range(n_features)])
        df_reshaped["response"] = responses

        return df_reshaped
    
    except Exception as e:
        logger.error(e)
        raise e

def generate_predictions(n: int, coin_id: str, engine: Engine, model) -> pd.DataFrame:
    # Get latest data
    sql = f"SELECT timestamp, price FROM market_chart WHERE coin_id='{coin_id}' ORDER BY timestamp DESC LIMIT {n}" 
    df = pd.read_sql(sql, engine).sort_values("timestamp")
    
    # Create placeholder for the results 
    df_results = df.copy()
    df_results["tagging"] = "actual"

    for _ in range(n):
        # Get the next timestamp 
        last_timestamp = df_results["timestamp"].max()
        next_timestamp = last_timestamp + dt.timedelta(minutes=5)

        # Get the last 6 records for feature engineering
        x = df_results.tail(6)
        x_reshape = feature_prep_past_n_records(x)

        # Further preprocessing to adjust the sample set
        x_reshape.drop("feature_1", axis=1, inplace=True)
        x_reshape.columns = [f"feature_{i}" for i in range(1,6)]

        prediction = model.predict(x_reshape)
        new_values = pd.DataFrame(
            {
                "timestamp": next_timestamp,
                "price": prediction,
                "tagging": "prediction"
            }, index=[0]
        )
        df_results = pd.concat([df_results, new_values], ignore_index=True)

    return df_results