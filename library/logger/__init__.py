import logging

from library.object_broker import ob


class LoggerConfig:

    @classmethod
    def initialize(cls):

        # log file config
        ydict = ob.config.yaml_config.path_get("Logger")

        fname = ob.config.yaml_config.path_get("File-Name", ydict)

        # Create and configure logger
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', filename=fname, filemode='w')

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)

        return logger

