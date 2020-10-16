from sqlalchemy.orm import Session

# noinspection PyUnresolvedReferences
from sqlalchemy.ext.automap import automap_base

# noinspection PyUnresolvedReferences
from sqlalchemy.ext import declarative as decl

# noinspection PyUnresolvedReferences
from sqlalchemy import Table, Column, types, JSON, ForeignKey, event, func, sql, \
    schema, inspect, create_engine, distinct

from library.object_broker import ob


class SQLADBConn:

    ydict = ob.config.yaml_config.path_get("Database-Connections/MySQL/PyTrade")
    db_conn = ob.config.yaml_config.path_get(f"URLs/{ob.config.config_mode}", ydict)

    @classmethod
    def initialize(cls):
        engine = create_engine(cls.db_conn)
        ob['engine'] = engine

        session = Session(engine)
        ob['session'] = session
