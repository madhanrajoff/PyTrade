import requests

from enum import Enum

from library.object_broker import ob


class MarketType(Enum):
    BOND = 1
    EQUITY = 2
    ETF = 3
    FOREX = 4
    FUTURE = 5
    FUTURE_OPTION = 6
    INDEX = 7
    INDICATOR = 8
    MUTUAL_FUND = 9
    OPTION = 10
    UNKNOWN = 11


class TDAmeritradeAPI:

    def __init__(self):
        # tdameritrade config
        ydict = ob.config.yaml_config.path_get("TD-Ameritrade")
        self.base_url = ob.config.yaml_config.path_get("Base-Url", ydict)
        self.consumer_key = ob.config.yaml_config.path_get("Consumer-Key", ydict)

    def daily_equity_quotes(self, today_fmt):
        market_url = f"{self.base_url}/marketdata/{MarketType.EQUITY.name}/hours"
        params = {
            'apikey': self.consumer_key,
            'date': today_fmt
        }
        reqt = requests.get(
            url=market_url,
            params=params
        ).json()
        return reqt

    def quotes_request(self, stocks):
        quotes_url = f"{self.base_url}/marketdata/quotes"
        params = {
            'apikey': self.consumer_key,
            'symbol': stocks
        }
        reqt = requests.get(
            url=quotes_url,
            params=params
        ).json()
        return reqt
