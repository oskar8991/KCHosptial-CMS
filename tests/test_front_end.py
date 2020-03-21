'''
import unittest #nose2 package to be able to run all tests simultaneously
import urllib

from flask_testing import LiveServerTestCase
from selenium import webdriver

from app import create_app
from models import User, Announcement, Questions, Answers

"""
Set test variables (such as login information) below:
"""


class TestBase(LiveServerTestCase):

    def create_app(self):
        #config_name = 'testing'
        app = create_app()
        app.config.update(
            # Specify the test database
            SQLALCHEMY_DATABASE_URI='sqlite:///data.db',
            #Set the port that the live server will listen on below:
            #LIVESERVER_PORT=5000
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        """
        Setup the test driver and create test users
        In this test we are using Chrome as our test browser
        install selenium using "pip install selenium" (pip3)
        and then install ChromeDriver using "brew install chromedriver"
        if on windows, download chromedriver binary and add to PATH
        """
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())


    def tearDown(self):
        """
        Will be called after every test
        """
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
'''
