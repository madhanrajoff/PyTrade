"""
APPLICATION FACTORY - Application Package Constructor

Delays the creation of the application by moving it into a factory function that can be explicitly invoked
from the script.
 - This allows for applying configuration changes dynamically. This is particularly important for unit tests.
It is sometimes necessary to run the application under different configuration settings.
 - This also provides the ability to create multiple application instances
"""


class AppFactory:

    @classmethod
    def create_app(cls, config=None):

        try:
            from library.object_broker import ob

            if config is None:
                from config import Config
                config = Config()

            ob['config'] = config
            Config.initialize(config)

            return True

        except Exception as e:
            raise e
