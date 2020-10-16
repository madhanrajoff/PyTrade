from . import *


class Logger:

    logger: LoggerConfig = LoggerConfig.initialize()

    @classmethod
    def info(cls, msg):
        cls.logger.info(msg)

    @classmethod
    def debug(cls, msg):
        cls.logger.debug(msg)

    @classmethod
    def warning(cls, msg):
        cls.logger.warning(msg)

    @classmethod
    def error(cls, msg):
        cls.logger.error(msg)

    @classmethod
    def critical(cls, msg):
        cls.logger.critical(msg)
