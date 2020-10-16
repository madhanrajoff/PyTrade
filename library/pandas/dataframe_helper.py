import pandas as pd

from library.object_broker import ob


class DFHelper:
    sql_engine = ob.engine

    @classmethod
    def to_sql_with_index(cls, df, table_name, if_exists="replace", index_label="pid"):
        df.to_sql(f"{table_name}", cls.sql_engine, if_exists=if_exists, index_label=index_label, index=True)

    @classmethod
    def to_sql_without_index(cls, df, table_name, if_exists="replace"):
        df.to_sql(f"{table_name}", cls.sql_engine, if_exists=if_exists, index=False)

    @classmethod
    def read_sql(cls, sql_q):
        return pd.read_sql(sql_q, cls.sql_engine)
