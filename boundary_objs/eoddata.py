import requests

from enum import Enum

from library.object_broker import ob


class Stocks(Enum):
    NYSE = 1  # United States
    NASDAQ = 2  # United States
    JPX = 3  # Japan
    LSE = 4  # United Kingdom, Italy
    SSE = 5  # China
    SEHK = 6  # Hong Kong
    Euronext = 7  # European Union
    TSX = 8  # Canada
    SZSE = 9  # China
    BSE = 10  # India
    NSE = 11  # India


class EodDataAPI:

    def __init__(self):
        # eoddata config
        ydict = ob.config.yaml_config.path_get("EodData")
        self.base_url = ob.config.yaml_config.path_get("BASE-URL", ydict)

    def stocklist(self, each):
        stocklist_url = f"{self.base_url}/{Stocks.NYSE.name}/{each}.htm"
        resp = requests.get(stocklist_url)
        return resp.content
