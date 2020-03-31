
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
test_wrong_password = "aaadminn"
test_add_email = "added@admin.com"
test_add_password = "adminadd"
test_add_question_question = "What is the liver located in? "
test_add_question_answer1 = "Head"
test_add_question_answer2 = "Pancreas"
test_add_question_answer3 = "Aspectic"
test_add_question_answerCorrect = "Human Body"




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
        self.driver.find_element_by_id("password").send_keys(test_wrong_password)
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




class TestUser(CreateObjects, TestBase):

    def test_add_user(self):
        """
        Test that an admin user can add a user and checks that it is in database
        """

        # Login as admin user
        self.login_admin()

        # Click departments menu link
        self.driver.find_element_by_id("addUser").click()
        time.sleep(1)


        # Fill in add department form
        self.driver.find_element_by_id("input_email").send_keys(test_add_email)
        time.sleep(1)
        self.driver.find_element_by_id("input_password1").send_keys(test_add_password)
        time.sleep(1)
        self.driver.find_element_by_id("input_password2").send_keys(test_add_password)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that there are now 2 users in the database
        self.assertEqual(User.query.count(), 2)




    def test_delete_user(self):
        """
        Tests that admin can delete a user and that databaes is updated
        """

        # Login as admin user
        self.login_admin()

        #Click on user list in the dahsboard
        self.driver.find_element_by_id("seeUser").click()
        time.sleep(1)


        #Click on delete user button
        self.driver.find_element_by_class_name("btn").click()
        time.sleep(2)


        # Assert that there are now 2 users in the database
        self.assertEqual(User.query.count(), 0)


    def test_add_existing_user(self):
        """
        Test that an admin user cannot add another user with the same email.
        Checks if the error message is valid and that it didn't add it to database.
        """

        # Login as admin user
        self.login_admin()

        #Click on user list in the dahsboard
        self.driver.find_element_by_id("addUser").click()
        time.sleep(1)

        # Fill in add department form
        self.driver.find_element_by_id("input_email").send_keys(test_email)
        time.sleep(1)
        self.driver.find_element_by_id("input_password1").send_keys(test_add_password)
        time.sleep(1)
        self.driver.find_element_by_id("input_password2").send_keys(test_add_password)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name("invalid-feedback").text
        assert "That email is taken. Please choose a different one." in error_message

        # Assert that there is still only 1 department in the database
        self.assertEqual(User.query.count(), 1)



class TestQuiz(CreateObjects, TestBase):

    def test_add_question(self):
        """
        Test that an admin user can add a question to a quiz
        Checks if it's added to databse
        """

        # Login as admin user
        self.login_admin()

        #Click on user list in the dahsboard
        self.driver.find_element_by_id("addQuiz").click()
        time.sleep(1)

        self.driver.find_element_by_id("addQuestion").click()
        time.sleep(3)

        # Fill in add department form
        self.driver.find_element_by_id("questionInput").send_keys(test_add_question_question)
        time.sleep(1)
        self.driver.find_element_by_id("questionAnswer1").send_keys(test_add_question_answer1)
        time.sleep(1)
        self.driver.find_element_by_id("questionAnswer2").send_keys(test_add_question_answer2)
        time.sleep(1)
        self.driver.find_element_by_id("questionAnswer3").send_keys(test_add_question_answer3)
        time.sleep(1)
        self.driver.find_element_by_id("questionAnswerCorrect").send_keys(test_add_question_answerCorrect)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that there is still only 1 department in the database
        self.assertEqual(Questions.query.count(), 2)







if __name__ == '__main__':
    unittest.main()
