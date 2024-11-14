import requests
from loguru import logger

class CoinGeckoAPI:

    def __init__(self, api_key: str):
        self.base_url = "https://api.coingecko.com/api/v3/"
        self.api_key = api_key
        self.header = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.api_key
        }

    def ping(self):
        url = self.base_url + "ping"
        response = requests.get(url, headers=self.header)
        
        try:
            response.raise_for_status()
            logger.info(response.json())
            print(response.json())

        except Exception as e:
            # logger.error(e)
            raise e

    def coins_list(self) -> dict:
        url = self.base_url + f"coins/list"
        response = requests.get(url, headers=self.header)
        try:
            response.raise_for_status()
            logger.info(f"{response.status_code} GET request {url}")
            return response.json()
        
        except Exception as e:
            # logger.error(e)
            raise e

    def coin_historical_chart_data_by_id(self, coin_id: str, vs_currency: str, days: int, interval: str = None, precision: int = 4) -> dict:
        url = self.base_url + f"coins/{coin_id}/market_chart"

        # Configure parameters
        params = {
            "vs_currency": vs_currency,
            "days": days,
            "precision": precision
        }

        # Add only interval if specified 
        if interval:
            params["interval"] = interval

        response = requests.get(url, headers=self.header, params=params)
        try:
            response.raise_for_status()
            logger.info(f"{response.status_code} GET request {url}")
            return response.json()
        
        except Exception as e:
            # logger.error(e)
            raise e