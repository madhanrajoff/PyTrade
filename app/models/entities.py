from library.object_broker import ob
from sqla_stack import sqla_base as sa


class _Entity(sa.Model):
    __abstract__ = True

    def query(self, table, field_select):
        return ob.session.query(table).with_entities(*field_select)


class Quote(_Entity):

    def __init__(self):
        self.table = super().classes.Quote

    def my_qfields(self):
        qf = [self.table.symbol.label('symbol'), self.table.bidPrice.label('bidPrice'),
              self.table.closePrice.label('closePrice'), self.table.date.label('date')]
        return qf

    def __call__(self):
        return super().query(self.table, self.my_qfields()).statement


class RAWSql:
    connection = ob.engine

    @classmethod
    def add_primary_key(cls, table_name):
        with cls.connection.connect() as con:
            con.execute(
                f"ALTER TABLE {table_name} "
                f"CHANGE COLUMN `pid` `pid` BIGINT NOT NULL, "
                f"ADD PRIMARY KEY (`pid`), "
                f"ADD UNIQUE INDEX `pid_UNIQUE` (`pid` ASC) VISIBLE"
            )


class RAWSqlQuote:

    @classmethod
    def add_primary_key(cls, table_name="Quote"):
        RAWSql.add_primary_key(table_name=table_name)
