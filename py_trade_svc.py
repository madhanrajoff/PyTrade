import pprint

from app.services.get_data_cf import GetDataCf
from app.models.entities import Quote
from library.pandas.dataframe_helper import DFHelper as Df


class PyTradeSvc:

    @classmethod
    def start(cls):
        GetDataCf.daily_equity_quotes()
        # if get_data_cf.daily_equity_quotes():
        # quote = Quote()
        # df = Df.read_sql(quote())
        # pprint.pprint(df)
