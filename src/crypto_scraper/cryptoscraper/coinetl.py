import pandas as pd
from datetime import datetime as dt
from loguru import logger
from sqlalchemy import Engine
from .utils import timestamp_to_datetime, run_query
from .coingecko import CoinGeckoAPI

class CoinGeckoETL(CoinGeckoAPI):

    def refresh_coins_list(self, engine: Engine, schema_name: str, table_name: str):
        # Scrape updated coins_list and transform to dataframe
        data = self.coins_list()
        df = pd.DataFrame(data)
        df["insertion_date"] = dt.now()

        # Truncate table 
        sql = f"delete from {schema_name}.{table_name}"
        run_query(engine, sql)

        # Load to database
        self.load(df, engine, schema_name, table_name)

    def extract(self, coin_id: str, vs_currency: str, days: int, interval: str = None, precision: int = 4) -> dict:

        # Store the parameters for reference
        self.coin_id = coin_id
        self.vs_currency = vs_currency

        # Get historical chart data 
        return self.coin_historical_chart_data_by_id(
            coin_id=coin_id, 
            vs_currency=vs_currency, 
            days=days, 
            interval=interval, 
            precision=precision
        )

    def transform(self, hist: dict, last_timestamp: dt):

        try:
        
            # Fetch the market historical prices
            hist_prices = pd.DataFrame(hist["prices"], columns=["timestamp","price"])
            hist_market_caps = pd.DataFrame(hist["market_caps"], columns=["timestamp","market_cap"])
            hist_total_volumes = pd.DataFrame(hist["total_volumes"], columns=["timestamp","total_volume"])

            # Consolidate sources into a single dataframe
            df_hist = hist_prices.merge(
                hist_market_caps,how="left", on="timestamp"
            ).merge(
                hist_total_volumes, how="left", on="timestamp"
            )

            # Convert timestamp to datetime and get only latest records based on timestamp
            df_hist["timestamp"] = df_hist["timestamp"].map(timestamp_to_datetime)
            df_hist_filtered = df_hist[df_hist["timestamp"]>last_timestamp].copy()

            # Add columns 
            df_hist_filtered["coin_id"] = self.coin_id
            df_hist_filtered["vs_currency"] = self.vs_currency
            df_hist_filtered["insertion_date"] = dt.now()

            return df_hist_filtered

        except Exception as e:
            # logger.error(e)
            raise e
        
    def load(self, df: pd.DataFrame, engine: Engine, schema_name: str, table_name: str):
        try:
            df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists="append", index=False)
            n_rows = df.shape[0]
            logger.info(f"{n_rows} records have been loaded to the database")
            engine.dispose()
        except Exception as e:
            # logger.error(e)
            raise e
        
    def run(self, coin_id: str, vs_currency: str, days: int, engine: Engine, schema_name: str, table_name: str, interval: str = None, precision: int = 4):

        sql = f"select coalesce(max(timestamp),'1900-01-01') from {schema_name}.{table_name} where coin_id='{coin_id}'"
        last_timestamp = run_query(engine, sql).fetchone()[0]

        hist = self.extract(coin_id, vs_currency, days, interval, precision)
        df = self.transform(hist, last_timestamp)
        self.load(df, engine, schema_name=schema_name, table_name=table_name)