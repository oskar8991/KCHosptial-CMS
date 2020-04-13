
import unittest #nose2 package to be able to run all tests simultaneously
import urllib
import time, os

from flask import url_for

from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#import chromedriver_binary

from app import create_app, db, bcrypt
from models import User, Questions, Answers, Announcement, FlaskUsage, FAQQuestions, About, Content


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

test_edit_question_question = "and where? "

test_add_title = "Test title."
test_add_description = "Test description."
test_add_links = "Test links"

test_question = "Test question?"
test_answer = "Test answer"

test_title = "Test title"
test_header = "Test header"
test_subject = "Test Subject"
test_content = "Testing content text"


class TestBase(LiveServerTestCase):

    def create_app(self):
        #config_name = 'testing'
        os.environ['FLASK_SETTINGS'] = 'config.TestingConfig'
        app = create_app()

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
        time.sleep(3)
        self.driver.find_element_by_id("readMoreHome").click()
        time.sleep(2)
        assert url_for('main.index') in self.driver.current_url

        # Click on login icon
        time.sleep(2)
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
        time.sleep(3)
        self.driver.find_element_by_id("readMoreHome").click()
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
        time.sleep(3)
        self.driver.find_element_by_id("readMoreHome").click()
        time.sleep(3)
        assert url_for('main.index') in self.driver.current_url
        time.sleep(3)
        # Click on login icon
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)

        # Click on login button
        self.driver.find_element_by_id("loginButton").click()
        time.sleep(2)
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
        time.sleep(3)
        self.driver.find_element_by_id("readMoreHome").click()
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
        time.sleep(5)
        self.driver.find_element_by_id("readMoreHome").click()
        time.sleep(3)
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(2)
        self.driver.find_element_by_id("loginButton").click()
        time.sleep(2)
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

        # Click Users to see the actions availiable
        self.driver.find_element_by_id("users").click()
        time.sleep(1)

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
        time.sleep(3)
        # Click Users to see the actions availiable
        self.driver.find_element_by_id("users").click()
        time.sleep(3)

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

        # Click Users to see the actions availiable
        self.driver.find_element_by_id("users").click()
        time.sleep(1)

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



#This section is not done because the adding quiz question is not fully implemented

class TestQuiz(CreateObjects, TestBase):

    def test_correct_question_answer(self):
        """
        Test that an admin user can add a question to a quiz
        Checks if it's added to databse
        """
        # Login as admin user
        self.login_admin()

        #Click on edit page in the dahsboard
        self.driver.find_element_by_id("editPage").click()
        time.sleep(1)

        #Click on add a new section
        self.driver.find_element_by_id("add_section").click()
        time.sleep(1)

        #Input new section
        self.driver.find_element_by_id("input_header").send_keys(test_header, Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_id("new_input_title").send_keys(test_title, Keys.ENTER)
        time.sleep(1)

        #Save changes
        self.driver.find_element_by_id("create_section").click()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        # clicks 'OK' button
        ale.accept()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        ale.accept()

        #Go back to dashboard
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)
        self.driver.find_element_by_id("dashboard").click()
        time.sleep(1)

        # Click Quiz to see the actions availiable
        self.driver.find_element_by_id("quiz").click()
        time.sleep(1)

        #Click on add quiz in the dahsboard
        self.driver.find_element_by_id("addQuiz").click()
        time.sleep(1)

        #Click on add question
        self.driver.find_element_by_id("addQuestion").click()
        time.sleep(3)

        # Fill in the question form
        self.driver.find_element_by_id("test_add_question_question").send_keys(test_add_question_question)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer1").send_keys(test_add_question_answer1)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer2").send_keys(test_add_question_answer2)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer3").send_keys(test_add_question_answer3)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answerCorrect").send_keys(test_add_question_answerCorrect)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that there is still only 1 question in the database
        self.assertEqual(Questions.query.count(), 1)
        self.driver.find_element_by_id("home_top").click()
        time.sleep(2)
        self.driver.find_element_by_id("open_quiz").click()
        time.sleep(4)
        self.driver.find_element_by_id("quiz-start-btn1").click()
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, 570)")
        time.sleep(2)
        self.driver.find_element_by_id("op3").click()
        time.sleep(2)
        self.driver.find_element_by_id("quiz-finish-btn1").click()
        time.sleep(2)

        updatescore = Questions.query.filter_by(question_text='What is the liver located in? ').first()

        #Check that it redirects to the all announcement page
        self.assertEqual(updatescore.stat_right, 1);

    def test_wrong_question_answer(self):
        """
        Test that an admin user can add a question to a quiz
        Checks if it's added to databse
        """
        # Login as admin user
        self.login_admin()

        #Click on edit page in the dahsboard
        self.driver.find_element_by_id("editPage").click()
        time.sleep(1)

        #Click on add a new section
        self.driver.find_element_by_id("add_section").click()
        time.sleep(1)

        #Input new section
        self.driver.find_element_by_id("input_header").send_keys(test_header, Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_id("new_input_title").send_keys(test_title, Keys.ENTER)
        time.sleep(1)

        #Save changes
        self.driver.find_element_by_id("create_section").click()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        # clicks 'OK' button
        ale.accept()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        ale.accept()

        #Go back to dashboard
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)
        self.driver.find_element_by_id("dashboard").click()
        time.sleep(1)

        # Click Quiz to see the actions availiable
        self.driver.find_element_by_id("quiz").click()
        time.sleep(1)

        #Click on add quiz in the dahsboard
        self.driver.find_element_by_id("addQuiz").click()
        time.sleep(1)

        #Click on add question
        self.driver.find_element_by_id("addQuestion").click()
        time.sleep(3)

        # Fill in the question form
        self.driver.find_element_by_id("test_add_question_question").send_keys(test_add_question_question)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer1").send_keys(test_add_question_answer1)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer2").send_keys(test_add_question_answer2)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer3").send_keys(test_add_question_answer3)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answerCorrect").send_keys(test_add_question_answerCorrect)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that there is still only 1 question in the database
        self.assertEqual(Questions.query.count(), 1)
        self.driver.find_element_by_id("home_top").click()
        time.sleep(2)
        self.driver.find_element_by_id("open_quiz").click()
        time.sleep(4)
        self.driver.find_element_by_id("quiz-start-btn1").click()
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, 570)")
        time.sleep(2)
        self.driver.find_element_by_id("op1").click()
        time.sleep(2)
        self.driver.find_element_by_id("quiz-finish-btn1").click()
        time.sleep(2)

        updatescore = Questions.query.filter_by(question_text='What is the liver located in? ').first()

        #Check that it redirects to the all announcement page
        self.assertEqual(updatescore.stat_wrong, 1);


    def test_add_question(self):
        """
        Test that an admin user can add a question to a quiz
        Checks if it's added to databse
        """

        # Login as admin user
        self.login_admin()

        #Click on edit page in the dahsboard
        self.driver.find_element_by_id("editPage").click()
        time.sleep(1)

        #Click on add a new section
        self.driver.find_element_by_id("add_section").click()
        time.sleep(1)

        #Input new section
        self.driver.find_element_by_id("input_header").send_keys(test_header, Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_id("new_input_title").send_keys(test_title, Keys.ENTER)
        time.sleep(1)

        #Save changes
        self.driver.find_element_by_id("create_section").click()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        # clicks 'OK' button
        ale.accept()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        ale.accept()

        #Go back to dashboard
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)
        self.driver.find_element_by_id("dashboard").click()
        time.sleep(1)

        # Click Quiz to see the actions availiable
        self.driver.find_element_by_id("quiz").click()
        time.sleep(1)

        #Click on add quiz in the dahsboard
        self.driver.find_element_by_id("addQuiz").click()
        time.sleep(1)

        #Click on add question
        self.driver.find_element_by_id("addQuestion").click()
        time.sleep(3)

        # Fill in the question form
        self.driver.find_element_by_id("test_add_question_question").send_keys(test_add_question_question)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer1").send_keys(test_add_question_answer1)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer2").send_keys(test_add_question_answer2)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer3").send_keys(test_add_question_answer3)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answerCorrect").send_keys(test_add_question_answerCorrect)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert that there is still only 1 question in the database
        self.assertEqual(Questions.query.count(), 1)


    def test_edit_question(self):
        """
        Checks that question is added to the page and then you can
        edit it and it updates in the database
        """
        # Login as admin user
        self.login_admin()

        #Click on edit page in the dahsboard
        self.driver.find_element_by_id("editPage").click()
        time.sleep(1)

        #Click on add a new section
        self.driver.find_element_by_id("add_section").click()
        time.sleep(1)

        #Input new section
        self.driver.find_element_by_id("input_header").send_keys(test_header, Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_id("new_input_title").send_keys(test_title, Keys.ENTER)
        time.sleep(1)

        #Save changes
        self.driver.find_element_by_id("create_section").click()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        # clicks 'OK' button
        ale.accept()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        ale.accept()

        #Go back to dashboard
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)
        self.driver.find_element_by_id("dashboard").click()
        time.sleep(1)

        # Click Quiz to see the actions availiable
        self.driver.find_element_by_id("quiz").click()
        time.sleep(1)

        #Click on add quiz
        self.driver.find_element_by_id("addQuiz").click()
        time.sleep(1)

        #Click on add question
        self.driver.find_element_by_id("addQuestion").click()
        time.sleep(1)

        # Fill in add question form
        self.driver.find_element_by_id("test_add_question_question").send_keys(test_add_question_question)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer1").send_keys(test_add_question_answer1)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer2").send_keys(test_add_question_answer2)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer3").send_keys(test_add_question_answer3)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answerCorrect").send_keys(test_add_question_answerCorrect)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check that it redirects to the all quiz page
        assert url_for('quiz.questions') in self.driver.current_url

        #Click on edit button
        self.driver.find_element_by_id("editQuestion").click()
        time.sleep(2)

        #Add a new title and submit
        self.driver.find_element_by_id("new_question").send_keys(test_edit_question_question)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        updatedQuestion = Questions.query.filter_by(question_text='What is the liver located in? and where? ').first()

        #Check that it redirects to the all announcement page
        assert url_for('quiz.questions') in self.driver.current_url
        #Checks that the content has been updated in the database
        assert "What is the liver located in? and where? " in updatedQuestion.question_text


    def test_delete_question(self):
        """
        Test that an admin user can delete a question from a quiz
        Checks if it's delted from databse
        """

        # Login as admin user
        self.login_admin()

        #Click on edit page in the dahsboard
        self.driver.find_element_by_id("editPage").click()
        time.sleep(1)

        #Click on add a new section
        self.driver.find_element_by_id("add_section").click()
        time.sleep(1)

        #Input new section
        self.driver.find_element_by_id("input_header").send_keys(test_header, Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_id("new_input_title").send_keys(test_title, Keys.ENTER)
        time.sleep(1)

        #Save changes
        self.driver.find_element_by_id("create_section").click()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        # clicks 'OK' button
        ale.accept()
        time.sleep(1)
        ale = self.driver.switch_to_alert()
        ale.accept()

        #Go back to dashboard
        self.driver.find_element_by_id("navbarLogin").click()
        time.sleep(1)
        self.driver.find_element_by_id("dashboard").click()
        time.sleep(1)

        # Click Quiz to see the actions availiable
        self.driver.find_element_by_id("quiz").click()
        time.sleep(1)

        #Click on add quizin dahsboard
        self.driver.find_element_by_id("addQuiz").click()
        time.sleep(1)

        #Click on add question
        self.driver.find_element_by_id("addQuestion").click()
        time.sleep(3)

        # Add the questions input
        self.driver.find_element_by_id("test_add_question_question").send_keys(test_add_question_question)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer1").send_keys(test_add_question_answer1)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer2").send_keys(test_add_question_answer2)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answer3").send_keys(test_add_question_answer3)
        time.sleep(1)
        self.driver.find_element_by_id("test_add_question_answerCorrect").send_keys(test_add_question_answerCorrect)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check that it redirects to the all questions page
        assert url_for('quiz.questions') in self.driver.current_url

        #Click on delete question button
        self.driver.find_element_by_id("deleteQuestion").click()
        time.sleep(2)

        #Check that it is deleted from the database
        self.assertEqual(Questions.query.count(), 0)



class TestAnnouncement(CreateObjects, TestBase):
    def test_add_announcement(self):
        """
        Checks that announcement is added to the page and checks that it is in database
        """
        # Login as admin user
        self.login_admin()
        time.sleep(2)
        #Click on announcements in the navbar
        self.driver.find_element_by_id("announcement").click()
        time.sleep(1)

        #Click on add announcement
        self.driver.find_element_by_id("addAnnouncement").click()
        time.sleep(1)

        #Input the announcement
        self.driver.find_element_by_id("title").send_keys(test_add_title)
        time.sleep(1)
        self.driver.find_element_by_id("description").send_keys(test_add_description)
        time.sleep(1)
        self.driver.find_element_by_id("links").send_keys(test_add_links)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check if the announcement is in database
        self.assertEqual(Announcement.query.count(), 1)


    def test_edit_announcement(self):

        """
        Checks that announcement is added to the page and then you can
        edit it and it updates in the database
        """
        # Login as admin user
        self.login_admin()

        #Click on announcements in the navbar
        self.driver.find_element_by_id("announcement").click()
        time.sleep(1)

        #Click on add announcement
        self.driver.find_element_by_id("addAnnouncement").click()
        time.sleep(1)

        #Input the announcement
        self.driver.find_element_by_id("title").send_keys(test_add_title)
        time.sleep(1)
        self.driver.find_element_by_id("description").send_keys(test_add_description)
        time.sleep(1)
        self.driver.find_element_by_id("links").send_keys(test_add_links)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check that it redirects to the all announcement page
        assert url_for('main.announcements') in self.driver.current_url

        #Click on edit button
        self.driver.find_element_by_id("edit").click()
        time.sleep(2)

        #Add a new title and submit
        self.driver.find_element_by_id("newTitle").send_keys(test_add_title)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        updatedTitle = Announcement.query.filter_by(title='Test title.Test title.').first()

        #Check that it redirects to the all announcement page
        assert url_for('main.announcements') in self.driver.current_url
        #Checks that the content has been updated in the database
        assert "Test title.Test title." in updatedTitle.title


    def test_delete_announcement(self):
        """
        Checks that announcement is added to the page and then you can
        delete it and it updates in the database
        """
        # Login as admin user
        self.login_admin()

        #Click on announcements in the navbar
        self.driver.find_element_by_id("announcement").click()
        time.sleep(1)

        #Click on add announcement
        self.driver.find_element_by_id("addAnnouncement").click()
        time.sleep(1)

        #Input the announcement
        self.driver.find_element_by_id("title").send_keys(test_add_title)
        time.sleep(1)
        self.driver.find_element_by_id("description").send_keys(test_add_description)
        time.sleep(1)
        self.driver.find_element_by_id("links").send_keys(test_add_links)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check that it redirects to the all announcement page
        assert url_for('main.announcements') in self.driver.current_url

        #Click on delete button and confirm the deletion
        self.driver.find_element_by_id("delete").click()
        time.sleep(2)
        #Click on edit button
        self.driver.find_element_by_id("deleteConfirm").click()
        time.sleep(2)

        #Check that it redirects to the all announcement page
        assert url_for('main.announcements') in self.driver.current_url

        #Check if the announcement was deleted from the database
        self.assertEqual(Announcement.query.count(), 0)

    def test_click_announcement_scroll(self):
        """
        Checks that announcement is added to the page and checks that it is in database
        """
        # Login as admin user
        self.login_admin()
        time.sleep(2)
        #Click on announcements in the navbar
        self.driver.find_element_by_id("announcement").click()
        time.sleep(1)

        #Click on add announcement
        self.driver.find_element_by_id("addAnnouncement").click()
        time.sleep(1)

        #Input the announcement
        self.driver.find_element_by_id("title").send_keys(test_add_title)
        time.sleep(1)
        self.driver.find_element_by_id("description").send_keys(test_add_description)
        time.sleep(1)
        self.driver.find_element_by_id("links").send_keys(test_add_links)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check if the announcement is in database
        self.assertEqual(Announcement.query.count(), 1)
        time.sleep(2)
        self.driver.find_element_by_id("home_top").click()
        time.sleep(2)
        assert url_for('main.index') in self.driver.current_url
        time.sleep(5)
        self.driver.find_element_by_id("rollinglink").click()
        time.sleep(5)
        assert url_for('main.announcements') in self.driver.current_url


class TestFAQ(CreateObjects, TestBase):

    def test_add_faq(self):
        """
        Checks that faq is added to the page and checks that it is in database
        """
        # Login as admin user
        self.login_admin()

        #Click on faq in the navbar
        self.driver.find_element_by_id("faq").click()
        time.sleep(2)

        #Click on add faq
        self.driver.find_element_by_id("addFaq").click()
        time.sleep(2)

        #Input the faq
        self.driver.find_element_by_id("question").send_keys(test_question)
        time.sleep(2)
        self.driver.find_element_by_id("answer").send_keys(test_answer)
        time.sleep(2)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check if the faq is in database
        self.assertEqual(FAQQuestions.query.count(), 1)

    def test_delete_faq(self):
        """
        Checks that faq is added to the page and then you can
        delete it and it updates in the database
        """
        # Login as admin user
        self.login_admin()

        #Click on faq in the navbar
        self.driver.find_element_by_id("faq").click()
        time.sleep(1)

        #Click on add faq
        self.driver.find_element_by_id("addFaq").click()
        time.sleep(1)

        #Input the faq
        self.driver.find_element_by_id("question").send_keys(test_question)
        time.sleep(1)
        self.driver.find_element_by_id("answer").send_keys(test_answer)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)
        self.driver.find_element_by_id("faqBtn").click()
        time.sleep(2)
        self.driver.find_element_by_id("deleteButton").click()
        time.sleep(2)

        #click on faq
        self.driver.find_element_by_id("delete_Button").click()
        time.sleep(2)

        #Check if the faq is not in database
        self.assertEqual(FAQQuestions.query.count(), 0)

    def test_edit_faq(self):

        # Login as admin user
        self.login_admin()

        #Click on faq in the navbar
        self.driver.find_element_by_id("faq").click()
        time.sleep(2)

        #Click on add faq
        self.driver.find_element_by_id("addFaq").click()
        time.sleep(2)

        #Input the faq
        self.driver.find_element_by_id("question").send_keys(test_question)
        time.sleep(2)
        self.driver.find_element_by_id("answer").send_keys(test_answer)
        time.sleep(2)
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)

        #Check that it redirects to the all announcement page
        assert url_for('main.faq') in self.driver.current_url

        time.sleep(2)
        self.driver.find_element_by_id("faqBtn").click()
        time.sleep(2)


        #Click on edit button
        self.driver.find_element_by_id("editButton").click()
        time.sleep(2)

        #Add a new title and submit
        self.driver.find_element_by_id("newQuestion").send_keys(test_question)
        time.sleep(3)
        self.driver.find_element_by_id("update").click()
        time.sleep(3)

        updatedQuestion = FAQQuestions.query.filter_by(question='Test question?Test question?').first()
        #Check that it redirects to the all announcement page
        assert url_for('main.faq') in self.driver.current_url
        #Checks that the content has been updated in the database
        assert "Test question?Test question?" in updatedQuestion.question


class TestAbout(CreateObjects, TestBase):

    def test_add_about(self):
        """
        Checks that about card is added to the page and checks that it is in database
        """
        # Login as admin user
        self.login_admin()
        time.sleep(2)
        #Click on about in the navbar
        self.driver.find_element_by_id("about").click()
        time.sleep(1)

        #Click on add card
        self.driver.find_element_by_id("addCard").click()
        time.sleep(1)

        #Input the card
        self.driver.find_element_by_id("subject").send_keys(test_subject)
        time.sleep(1)
        self.driver.find_element_by_id("content").send_keys(test_content)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check if the card is in database
        self.assertEqual(About.query.count(), 1)

    def test_edit_about(self):
        """
        Checks that about card is added to the page and checks that it is in database
        """
        # Login as admin user
        self.login_admin()
        time.sleep(2)
        #Click on about in the navbar
        self.driver.find_element_by_id("about").click()
        time.sleep(3)

        #Click on add about
        self.driver.find_element_by_id("addCard").click()
        time.sleep(2)

          #Input the card
        self.driver.find_element_by_id("subject").send_keys(test_subject)
        time.sleep(1)
        self.driver.find_element_by_id("content").send_keys(test_content)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check that it redirects to the about page
        assert url_for('main.about') in self.driver.current_url
        time.sleep(2)
        #Click on edit button
        self.driver.find_element_by_id("editButton").click()
        time.sleep(2)

        #Add a new title and submit
        self.driver.find_element_by_id("newSubject").send_keys(test_add_title)
        time.sleep(3)
        self.driver.find_element_by_id("newContent").send_keys(test_add_title)
        time.sleep(3)
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)

        updatedtitle = About.query.filter_by(title='Test SubjectTest title.').first()
        updatedcontent = About.query.filter_by(content='Testing content textTest title.').first()
        time.sleep(2)
        #Check that it redirects to the all announcement page
        assert url_for('main.about') in self.driver.current_url
        #Checks that the content has been updated in the database
        assert "Test SubjectTest title." in updatedtitle.title
        assert "Testing content textTest title." in updatedcontent.content


    def test_delete_about(self):
        self.login_admin()
        #Click on about in the navbar
        self.driver.find_element_by_id("about").click()
        time.sleep(1)

        #Click on add card
        self.driver.find_element_by_id("addCard").click()
        time.sleep(1)

        #Input the card
        self.driver.find_element_by_id("subject").send_keys(test_question)
        time.sleep(1)
        self.driver.find_element_by_id("content").send_keys(test_answer)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        assert url_for('main.about') in self.driver.current_url
        time.sleep(2)
        #click on delete
        self.driver.find_element_by_id("deleteButton").click()
        time.sleep(2)
        #confirm the deletion
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        #Check if the card is not in database
        self.assertEqual(About.query.count(), 0)



class TestSplashPage(TestBase):

    def test_home_read_more(self):
        """
        Test that the user is redirected to the Home page
        """
        #Click on the splash home box
        self.driver.find_element_by_id("splashHomeId").click()
        time.sleep(3)
        #Click on the read more button
        self.driver.find_element_by_id("readMoreHome").click()
        time.sleep(3)
        #Check that the redirect is correct
        assert url_for('main.index') in self.driver.current_url

    def test_drugchart_read_more(self):
        """
        Test that the user is redirected to the Drugchart page
        """
        #Click on the splash drugchart box
        self.driver.find_element_by_id("splashDrugchartId").click()
        time.sleep(3)
        #Click on the read more button
        self.driver.find_element_by_id("readMoreDrugchart").click()
        time.sleep(3)
        assert url_for('drug_chart.medication') in self.driver.current_url


    def test_faq_read_more(self):
        """
        Test that the user is redirected to the FAQ page
        """
        #Click on the splash faq box
        self.driver.find_element_by_id("splashFaqtId").click()
        time.sleep(3)
        #Click on the read more button
        self.driver.find_element_by_id("readMoreFaq").click()
        time.sleep(3)
        #Check that the redirect is correct
        assert url_for('main.faq') in self.driver.current_url

    def test_about_read_more(self):
        """
        Test that the user is redirected to the About page
        """
        #Click on the splash about box
        self.driver.find_element_by_id("splashAboutId").click()
        time.sleep(3)
        #Click on the read more button
        self.driver.find_element_by_id("readMoreAbout").click()
        time.sleep(3)
        #Check that the redirect is correct
        assert url_for('main.about') in self.driver.current_url


class TestDrugChart(TestBase):

    def test_generate_chart(self):
        """
        Test that the user is redirected to the generated drug chart
        """
        #Click on the splash drugchart box
        self.driver.find_element_by_id("splashDrugchartId").click()
        time.sleep(3)
        #Click on the read more button
        self.driver.find_element_by_id("readMoreDrugchart").click()
        time.sleep(3)
        #Click on the generate button
        self.driver.find_element_by_id("generate").click()
        time.sleep(3)
        self.assertTrue("Patient Name" in self.driver.page_source)


class TestVisuals(TestBase):

    def test_dark_mode_activate(self):
        """
        Test that the dark mode theme is activated
        """
        #Click on the splash home box
        self.driver.find_element_by_id("splashHomeId").click()
        time.sleep(3)
        #Click on the read more button
        self.driver.find_element_by_id("readMoreHome").click()
        time.sleep(3)
        #Click on the dark mode checkbox
        self.driver.find_element_by_id("darkModeBtn").click()
        time.sleep(2)
        #Obtain the background color of the new dark mode checkbox button
        elem_colour = self.driver.find_element_by_id("darkModeBtn").value_of_css_property('background')
        #Check that this colour is correct
        self.assertTrue("rgb(31, 66, 97)" in elem_colour)

    def test_dark_mode_deactivate(self):
        """
        Test that the dark mode theme is deactivated
        """
        #Click on the splash home box
        self.driver.find_element_by_id("splashHomeId").click()
        time.sleep(3)
        #Click on the read more button
        self.driver.find_element_by_id("readMoreHome").click()
        time.sleep(3)
        #Click on the dark mode checkbox to turn on dark mode
        self.driver.find_element_by_id("darkModeBtn").click()
        time.sleep(3)
        #Click on the dark mode checkbox to turn off dark mode
        self.driver.find_element_by_id("darkModeBtn").click()
        time.sleep(3)
        #Obtain the background color of the dark mode checkbox button
        elem_colour = self.driver.find_element_by_id("darkModeBtn").value_of_css_property('background')
        #Check that this colour is correct
        self.assertTrue("rgb(255, 255, 255)" in elem_colour)


if __name__ == '__main__':
    unittest.main()
