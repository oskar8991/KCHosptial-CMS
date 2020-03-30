
import unittest #nose2 package to be able to run all tests simultaneously
import urllib
import time, os

from flask import url_for

from flask_testing import LiveServerTestCase
from selenium import webdriver

from app import create_app, db, bcrypt
from models import User, Questions, Answers, Announcement, FlaskUsage


"""
Set test variables (such as login information) below:
"""
test_email = "test@admin.com"
test_password = "admin"
test_wrong_email = "wrong@admin.com"



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

        SECRET_KEY = os.urandom(32)
        app.config['SECRET_KEY'] = SECRET_KEY


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
        hashed_password = bcrypt.generate_password_hash(test_password).decode('utf-8')
        self.admin = User (email = test_email, password = hashed_password)

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
        self.driver.find_element_by_id("readMore").click()
        assert url_for('main.index') in self.driver.current_url

        # Click on login icon
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)

        # Click on login button
        self.driver.find_element_by_id("loginButton").click()
        assert url_for('users.login') in self.driver.current_url
        time.sleep(1)

        #Send keys inside placeholders
        self.driver.find_element_by_id("email").send_keys(test_email)
        self.driver.find_element_by_id("password").send_keys(test_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)

        #Checks if the user has been redirected to dashboard_
        assert url_for('dashboard.dashboard_panel') in self.driver.current_url




    def test_login_wrong_email(self):
        """
        Test that a user can't login with wrong email and that the error will display
        """
        #Click on Read More on spash page
        self.driver.find_element_by_id("splashHomeId").click()
        time.sleep(1)
        self.driver.find_element_by_id("readMore").click()
        assert url_for('main.index') in self.driver.current_url

        # Click on login icon
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)

        # Click on login button
        self.driver.find_element_by_id("loginButton").click()
        assert url_for('users.login') in self.driver.current_url
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys(test_wrong_email)
        self.driver.find_element_by_id("password").send_keys(test_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)

        # Assert that error message is shown
        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Invalid credentials." in error_message



    def test_login_invalid_email_format(self):
        """
        Test that a user cannot login using an invalid email format and that error will display
        """

        #Click on Read More on spash page
        self.driver.find_element_by_id("splashHomeId").click()
        time.sleep(1)
        self.driver.find_element_by_id("readMore").click()
        assert url_for('main.index') in self.driver.current_url

        # Click on login icon
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)

        # Click on login button
        self.driver.find_element_by_id("loginButton").click()
        assert url_for('users.login') in self.driver.current_url
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys("wrong_format")
        self.driver.find_element_by_id("password").send_keys(test_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)

        # Assert that error message is shown
        error_message = self.driver.find_element_by_class_name("invalid-feedback").text
        assert "Invalid email address." in error_message


    def test_login_wrong_password(self):
        """
        Test that a user can't login with wrong password and that the error will display
        """
        #Click on Read More on spash page
        self.driver.find_element_by_id("splashHomeId").click()
        time.sleep(1)
        self.driver.find_element_by_id("readMore").click()
        assert url_for('main.index') in self.driver.current_url

        # Click on login icon
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)

        # Click on login button
        self.driver.find_element_by_id("loginButton").click()
        assert url_for('users.login') in self.driver.current_url
        time.sleep(1)

        # Fill in login form
        self.driver.find_element_by_id("email").send_keys(test_email)
        self.driver.find_element_by_id("password").send_keys("wrong_password")
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)

        # Assert that error message is shown
        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Invalid credentials." in error_message



class CreateObjects(object):

    """
    If we need to be logged in in the futher test, these method should
    be called, for simplifiyng the process
    """

    def login_admin(self):
        #Log in as an admin
        self.driver.find_element_by_id("splashHomeId").click()
        time.sleep(1)
        self.driver.find_element_by_id("readMore").click()
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)
        self.driver.find_element_by_id("loginButton").click()
        time.sleep(1)
        self.driver.find_element_by_id("email").send_keys(test_email)
        self.driver.find_element_by_id("password").send_keys(test_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)

        


if __name__ == '__main__':
    unittest.main()
