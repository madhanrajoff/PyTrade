import unittest


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        from app import AppFactory
        AppFactory.create_app()

    def tearDown(self):
        pass
