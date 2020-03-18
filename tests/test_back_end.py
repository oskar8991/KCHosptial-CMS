import unittest #nose2 package to be able to run all tests simultaneously

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app
from models import Content


class TestBase(TestCase):

    def create_app(self):
        # pass in test configurations
        #config_name = 'testing'
        app = create_app()
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
    Write database test methods here
    """


class TestViews(TestBase):

    """
    Write tests for each web page view
    """

    def test_index_view(self):
        """
        Test that index page is accessible
        """
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible
        """
        response = self.client.get(url_for('users.login'))
        self.assertEqual(response.status_code, 200)


class TestErrorPages(TestBase):

    """
    Write tests for erroneous pages...
    """

    def test_404_not_found(self):
        response = self.client.get('/testPage404')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

if __name__ == '__main__':
    unittest.main()
