
import unittest #nose2 package to be able to run all tests simultaneously
import urllib
import time

from flask import url_for

from flask_testing import LiveServerTestCase
from selenium import webdriver

from app import create_app, db
from models import User, Announcement, Questions, Answers

"""
Set test variables (such as login information) below:
"""
test_email = "test@admin.com"
test_password = "admin"

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
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        #create a test user
        self.admin = User (email = test_email, password = test_password)

        db.session.add(self.admin)
        db.session.commit()


    def tearDown(self):
        """
        Will be called after every test
        """
        self.driver.quit()

    def test_server_is_up_and_running(self):
        """
        Tests if the server is up and running
        """
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


class TestLogin(TestBase):

    def test_login(self):
        """
        Test that a user can login and that they will be redirected to
        the dashboard
        """
        #Click on Read More on spash page
        self.driver.find_element_by_id("splashHomeId").click()
        time.sleep(1)
        assert url_for('main.index') in self.driver.current_url

        # Click on login icon
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(2)

        # Click on login button
        self.driver.find_element_by_id("loginButton").click()
        assert url_for('users.login') in self.driver.current_url



if __name__ == '__main__':
    unittest.main()
