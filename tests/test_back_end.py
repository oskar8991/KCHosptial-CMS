import unittest #nose2 package to be able to run all tests simultaneously

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app
from models import Content


class TestBase(TestCase):

    def create_app(self):
        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///data.db'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """


    def tearDown(self):
        """
        Will be called after every test
        """


class TestModels(TestBase):

    """
    Write test methods here
    """


class TestViews(TestBase):

    """
    Write tests for each web page view
    """


class TestErrorPages(TestBase):

    """
    Write tests for erroneous pages...
    """


if __name__ == '__main__':
    unittest.main()
