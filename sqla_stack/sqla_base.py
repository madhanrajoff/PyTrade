from . import *

Base = automap_base()
Base.prepare(ob.engine, reflect=True)


class Model(Base):
    __abstract__ = True

    # noinspection PyMethodParameters
    @decl.declared_attr
    def __tablename__(cls):
        return cls.__name__
