import unittest #nose2 package to be able to run all tests simultaneously
import os
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from models import Content, User, Questions, Answers, Announcement, FlaskUsage

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, func, and_

from datetime import datetime

import os


class TestBase(TestCase):

    def create_app(self):
        # pass in test configurations
        #config_name = 'testing'
        os.environ['FLASK_SETTINGS'] = 'config.TestingConfig'
        app = create_app()

        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()


    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()


class TestModels(TestBase):

    """
    Write database test methods here
    """

    def test_user_add_model(self):
        """
        Test that a user can be successfully added to database and queried
        """
        user = User(email="test@test.com", password="test")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.filter_by(email="test@test.com").count(), 1)

    def test_user_delete_model(self):
        """
        Test that the user is successfully deleted from the database
        """
        db.session.delete(User.query.filter_by(email="test@test.com").first())
        db.session.commit()
        self.assertEqual(User.query.filter_by(email="test@test.com").count(), 0)

    def test_content_add_model(self):
        """
        Test that the content of the page is successfully added to the database
        """
        content = Content(header = "Test_Header", content = "Test_Content")
        db.session.add(content)
        db.session.commit()
        self.assertEqual(Content.query.filter_by(header = "Test_Header", content = "Test_Content").count(), 1)

    def test_content_delete_model(self):
        """
        Test that the content of the page is successfully deleted from the database
        """
        db.session.delete(Content.query.filter_by(header = "Test_Header", content = "Test_Content").first())
        db.session.commit()
        self.assertEqual(Content.query.filter_by(header = "Test_Header", content = "Test_Content").count(), 0)


    def test_announcments_add_model(self):
        """
        Test that the announcement is successfully added to the database
        """
        announcement = Announcement(title = "Title", description = "Description", date = datetime(2015, 6, 5, 8, 10, 10, 10))
        db.session.add(announcement)
        db.session.commit()
        self.assertEqual(Announcement.query.filter_by(title = "Title", description = "Description", date = datetime(2015, 6, 5, 8, 10, 10, 10)).count(), 1)

    def test_announcments_delete_model(self):
        """
        Test that the announcement is successfully deleted from the database
        """
        db.session.delete(Announcement.query.filter_by(title = "Title", description = "Description", date = datetime(2015, 6, 5, 8, 10, 10, 10)).first())
        db.session.commit()
        self.assertEqual(Announcement.query.filter_by(title = "Title", description = "Description", date = datetime(2015, 6, 5, 8, 10, 10, 10)).count(), 0)

    def test_questions_answers_add_model(self):
        """
        Test that the question and then answer is successfully added to the database
        """
        content = Content(header = "Test_Header", content = "Test_Content")
        question = Questions(question_text = "Test_Question?", content = content)
        answer = Answers(answer_text = "Answer_Test", correct = 0, question = question)
        db.session.add(content)
        db.session.add(question)
        db.session.add(answer)
        db.session.commit()
        self.assertEqual(Questions.query.filter_by(question_text = "Test_Question?").count(), 1)
        self.assertEqual(Answers.query.filter_by(answer_text = "Answer_Test", correct = 0, question = question).count(), 1)

    def test_questions_answers_delete_model(self):
        """
        Test that the question and then answer is successfully deleted from the database
        """
        db.session.delete(Answers.query.filter_by(answer_text = "Answer_Test", correct = 0).first())
        db.session.delete(Questions.query.filter_by(question_text="Test_Question?").first())
        db.session.delete(Content.query.filter_by(header = "Test_Header", content = "Test_Content").first())
        db.session.commit()
        self.assertEqual(Questions.query.filter_by(question_text="Test_Question?").count(), 0)
        self.assertEqual(Answers.query.filter_by(answer_text = "Answer_Test").count(), 0)

    def test_flask_usage_request(self):
        """
        Test that a record is succesfully stored in database table after a request.
        """
        beforeRequestCount = FlaskUsage.query.filter_by(path="/index").count()
        response = self.client.get(url_for('main.index'))
        self.assertEqual(FlaskUsage.query.filter_by(path="/index").count(), (beforeRequestCount+1))

    def test_flask_usage_status_code(self):
        """
        Test that shows flask usage stores the correct status code from a request.
        """
        response = self.client.get(url_for("main.faq"))
        flaskUsageCode = FlaskUsage.query.filter_by(path="/faq").order_by("datetime").first()
        if flaskUsageCode is not None:
            self.assertEqual(flaskUsageCode.status, response.status_code)



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

    def test_faq_view(self):
        """
        Test that faq page is accessible
        """
        response = self.client.get(url_for('main.faq'))
        self.assertEqual(response.status_code, 200)

    def test_announcement_view(self):
        """
        Test that announcement page is accessible
        """
        response = self.client.get(url_for('main.announcements'))
        self.assertEqual(response.status_code, 200)

    def test_drug_chart_view(self):
        """
        Test that the drug chart page is accessible
        """
        response = self.client.get(url_for('drug_chart.medication'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        """
        Test that about page is accessible
        """
        response = self.client.get(url_for('main.about'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible
        """
        response = self.client.get(url_for('users.login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('dashboard.dashboard_panel')
        redirect_url = url_for('users.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TestErrorPages(TestBase):
    """
    Write tests for erroneous pages...
    """

    def test_404_not_found(self):
        """
        Test an imaginary page in order to get a 404 status code.
        """
        response = self.client.get('/testPage404')
        self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
