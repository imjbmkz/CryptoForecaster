import pandas as pd
import joblib
from datetime import datetime as dt
from loguru import logger
from sqlalchemy import Engine
from minio import Minio
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

class CryptoML:

    def __init__(self) -> None:
        pass

    def read_data(self, sql: str, engine: Engine) -> pd.DataFrame:
        try:
            df = pd.read_sql(sql, engine)
            n_rows = df.shape[0]
            logger.info(f"{n_rows} records have been read from the database")
            return df
        
        except Exception as e:
            logger.error(e)
            raise e
        
    def data_prep_select_columns(self, df: pd.DataFrame, columns_to_retain: list) -> pd.DataFrame:
        return df[columns_to_retain].copy()
    
    def data_prep_get_xy(self, df: pd.DataFrame, X_columns: list, y_column: str) -> tuple:
        x = df[X_columns]
        y = df[y_column]
        return (x, y)
    
    def data_prep_train_test_split(self, X_variables: pd.DataFrame, y_variable: pd.Series, train_size: float = 0.7) -> list:
        return train_test_split(X_variables, y_variable, train_size=train_size)
    
    def feature_prep_past_n_records(self, df: pd.DataFrame, n_features: int=5, n_response: int=1) -> pd.DataFrame:
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
            logger.info(f"Dataframe has been processed to shape {df.shape}")

            return df_reshaped
        
        except Exception as e:
            logger.error(e)
            raise e
    
    def model_pipeline(self, X_variables: pd.DataFrame, y_variable: pd.Series) -> Pipeline:
        pipe = Pipeline(
            [
                ("Regressor", LinearRegression())
            ]
        )

        params = [
            {
                'Regressor' : [RandomForestRegressor(random_state=123)],
                'Regressor__criterion': ['friedman_mse'],
                'Regressor__n_estimators': [50, 100, 500],
            },
            {
                'Regressor' : [DecisionTreeRegressor(random_state=123)],
                'Regressor__criterion' : ['friedman_mse'],
                'Regressor__max_depth' : [1, 5, 10, 15],
            },
            {
                'Regressor' : [GradientBoostingRegressor(random_state=123)],
                'Regressor__learning_rate' : [0.01, 0.1, 0.2, 0.5],
            }
        ]

        try:
            logger.info("Model training has been initialized")
            grid_search = GridSearchCV(pipe, params, cv = 6, scoring = 'neg_mean_absolute_error', verbose = 2, n_jobs= -1)
            grid_search.fit(X_variables, y_variable)

            logger.info(f"Optimal model: {grid_search.best_estimator_}")
            logger.info(f"Optimal model parameters: {grid_search.best_params_}")
            logger.info(f"Optimal model yielded score: {grid_search.best_score_}")

            return grid_search.best_estimator_[0]
        
        except Exception as e:
            logger.error(e)
            raise e
    
    def model_to_pickle(self, model: Pipeline) -> str:
        ts = dt.now().strftime("%Y%m%d%H%M%S")
        file_name = f"regression_model_{ts}.pkl"
        try: 
            joblib.dump(model, file_name)
            logger.info(f"Model has been saved in pickle file {file_name}")
            return file_name
        except Exception as e:
            logger.error(e)
            raise e
        
    def model_to_minio(self, modelpath: str, minio_client: Minio, minio_bucket: str, minio_path: str):
        try:
            minio_client.fput_object(minio_bucket, minio_path, modelpath)
            logger.info(f"Model uploaded to MinIO: s3://{minio_bucket}/{minio_path}")
        except Exception as e:
            logger.error(e)
            raise e
        
    def run(
            self,
            sql: str,
            engine: Engine,
            columns_to_retain: list,
            X_columns: list,
            y_column: str,
            minio_client: Minio,
            minio_bucket: str,
            n_features: int=5,
            n_response: int=1
    ):
        df = self.read_data(sql, engine)
        df_subset = self.data_prep_select_columns(df, columns_to_retain)
        df_reshape = self.feature_prep_past_n_records(df_subset, n_features, n_response)
        X, y = self.data_prep_get_xy(df_reshape, X_columns, y_column)
        model = self.model_pipeline(X, y)
        file_name = self.model_to_pickle(model)
        self.model_to_minio(file_name, minio_client, minio_bucket, f"models/{file_name}")