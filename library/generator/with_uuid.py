import uuid


class UUID:
    """
    Universal Unique Identifier

    """

    @classmethod
    def generate_int(cls):
        return uuid.uuid4().int

    @classmethod
    def random_str_int(cls):
        return str(cls.generate_int())

    @classmethod
    def random_int(cls, length: int = 10):
        return int(cls.random_str_int()[:length])
