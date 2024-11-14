import os, sys, json
from datetime import datetime as dt
from loguru import logger
from cryptoscraper.utils import get_conn
from cryptoscraper.coinetl import CoinGeckoETL

if __name__=="__main__":

    # Logging configuration
    log_date = dt.now().strftime("%Y%m%d")
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time}: {level} - {message}")
    logger.add(sys.stderr, level="ERROR", format="{time}: {level} - {message}")

    API_KEY = os.getenv("COINGECKO_API_KEY")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    # Initialize CoinGeckoETL class and Engine for db connection
    cg = CoinGeckoETL(api_key=API_KEY)
    engine = get_conn("postgresql+psycopg2", db_host=DB_HOST, db_name=DB_NAME, db_user=DB_USER, db_pass=DB_PASS, db_port=DB_PORT)

    logger.info("App has started")

    try:

        # Check parameter
        argv = sys.argv
        logger.info(argv)

        if "market_chart" in argv:
            # Load coins configuration
            with open("config.json") as fp:
                coins = json.load(fp)

            for coin in coins:
                cg.run(
                    **coin,
                    engine=engine,
                    schema_name="public",
                    table_name="market_chart"
                )

        elif "coins_list" in argv:
            cg.refresh_coins_list(engine, "public", "coins_list")

        logger.info("App has ended")

    except Exception as e:
        logger.error(f"Missing parameter {e}")
        raise e