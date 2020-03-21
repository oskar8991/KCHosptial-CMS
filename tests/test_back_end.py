import unittest #nose2 package to be able to run all tests simultaneously

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from models import Content, User

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData

import os


class TestBase(TestCase):

    def create_app(self):
        # pass in test configurations
        #config_name = 'testing'
        app = create_app()
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///data.db'
        )

        SECRET_KEY = os.urandom(32)
        app.config['SECRET_KEY'] = SECRET_KEY

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

    def test_user_add_model(self):
        """
        Test that a user can be successfully added to database and queried
        Then Test that the user is successfully deleted from the database
        """
        user = User(email="ivan@test.com", password="test")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.filter_by(email="ivan@test.com").count(), 1)

    def test_user_delete_model(self):
        db.session.delete(User.query.filter_by(email="ivan@test.com").first())
        db.session.commit()
        self.assertEqual(User.query.filter_by(email="ivan@test.com").count(), 0)


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
        response = self.client.get('/testPage404')
        self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
