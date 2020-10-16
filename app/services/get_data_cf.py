import uuid
import pandas as pd
import numpy as np
import string
import time
import pprint

from bs4 import BeautifulSoup

from library.datetime_helper import DatetimeHelper as DTH
from library.generator.with_uuid import UUID
from library.logger.logger import Logger
from boundary_objs.td_ameritrade import TDAmeritradeAPI
from boundary_objs.eoddata import EodDataAPI
from library.pandas.dataframe_helper import DFHelper as Df
from app.models.entities import RAWSqlQuote


class GetDataCf:

    @classmethod
    def daily_equity_quotes(cls):
        
        # Initialize the tdameritrade api
        tdameritrade = TDAmeritradeAPI()

        # Initialize the edodata api
        edodata = EodDataAPI()

        # Check if the market was open today.
        # eastern so I convert the timezone
        today = DTH.now_new_york()
        today_fmt = today.strftime("%Y-%m-%d")

        # Call the td ameritrade hours endpoint for equities to see if it is open
        reqt = tdameritrade.daily_equity_quotes(today_fmt=today_fmt)

        Logger.info(f"Equity: {reqt}")

        try:
            if reqt["equity"]["EQ"]["isOpen"] is True:
                # Get a current list of all the stock symbols for the NYSE
                # Create a list of every letter in the alphabet
                # Each page has a letter for all those symbols
                # i.e. http://eoddata.com/stocklist/NYSE/A.htm"
                alpha = list(string.ascii_uppercase)

                symbols = []

                # Loop through the letters in the alphabet to get the stocks on each page
                # from the table and store them in a list
                for each in alpha:
                    site = edodata.stocklist(each)
                    soup = BeautifulSoup(site, "html.parser")
                    table = soup.find("table", {"class": "quotes"})
                    for row in table.findAll("tr")[1:]:
                        symbols.append(row.findAll("td")[0].text.rstrip())

                # Remove the extra letters on the end
                symbols_clean = []

                for each in symbols:
                    each = each.replace(".", "-")
                    symbols_clean.append((each.split("-")[0]))

                # The TD Ameritrade api has a limit to the number of symbols you can get data for
                # in a single call so we chunk the list into 200 symbols at a time
                def chunks(l, n):
                    """
                    Takes in a list and how long you want
                    each chunk to be
                    """
                    n = max(1, n)
                    return (l[i:i + n] for i in range(0, len(l), n))

                symbols_chunked = list(chunks(list(set(symbols_clean)), 200))

                # Function for the api request to get the data from td ameritrade
                def quotes_request(stocks):
                    """
                    Makes an api call for a list of stock symbols
                    and returns a dataframe
                    """
                    reqt = tdameritrade.quotes_request(stocks)

                    for k, v in reqt.items():
                        v['pid'] = UUID.random_int(length=10)

                    time.sleep(1)

                    return pd.DataFrame.from_dict(
                        reqt,
                        orient="index"
                    ).reset_index(drop=True)

                # Loop through the chunked list of symnbols
                # and call the api. Append all the resulting dataframes into one
                df = pd.concat([quotes_request(each) for each in symbols_chunked])

                # Add the date and fmt the dates for BQ
                df["date"] = pd.to_datetime(today_fmt)
                df["date"] = df["date"].dt.date
                df["divDate"] = pd.to_datetime(df["divDate"])
                df["divDate"] = df["divDate"].dt.date
                df["divDate"] = df["divDate"].fillna(np.nan)

                # Remove anything without a price
                df = df.loc[df["bidPrice"] > 0]

                # Rename columns and format for sql (can"t start with a number)
                df = df.rename(columns={
                    "52WkHigh": "_52WkHigh",
                    "52WkLow": "_52WkLow"
                })

                df.set_index('pid', inplace=True)

                Logger.info(f"Quotes: {df.head().to_dict('index')}")

                # Add to MySql
                Df.to_sql_with_index(df=df, table_name="Quote")

                # Alter Quote Table
                RAWSqlQuote.add_primary_key()

                return True

            else:
                Logger.warning("Market Not Open Today")

        except KeyError:
            Logger.warning("Not a weekday")
