import pandas as pd
import alpaca_trade_api as tradeapi

from library.object_broker import ob
from library.pandas.dataframe_helper import DFHelper as Df


class AlpacaAPI:

    def __init__(self):

        # tdameritrade config
        ydict = ob.config.yaml_config.path_get("Alpaca")
        base_url = ob.config.yaml_config.path_get("Base-Url", ydict)
        key_id = ob.config.yaml_config.path_get("API-Key-ID", ydict)
        secret_key = ob.config.yaml_config.path_get("Secret-Key", ydict)

        # Initialize the alpaca api
        self.client_sdk = tradeapi.REST(
                key_id,
                secret_key,
                base_url,
                'v2'
                )

    def list_positions(self):
        return self.client_sdk.list_positions()

    def check_if_the_market_is_open_now(self):
        return self.client_sdk.get_clock().is_open

    def submit_order(self, symbol, qty, side, type, time_in_force):

        order = self.client_sdk.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type,
            time_in_force=time_in_force
        )

        df = pd.DataFrame.from_dict([order.__dict__["_raw"]])

        # Add to MySql
        Df.to_sql_without_index(df=df, table_name="Order", if_exists="append")
