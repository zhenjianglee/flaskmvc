import unittest
from flask import render_template,redirect,url_for,abort,flash
from app import create_app, db
from app.models import User, Role
from app.auth.forms import LoginForm
import re
class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        User.init_users()

        self.client = self.app.test_client(use_cookies=True)
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Stranger' in response.get_data(as_text=True))

        # login with the new account

        response = self.client.post(url_for('auth.login'), data={
            'user_id': '001',
            'password': '001'
        }, follow_redirects=True)

        data = response.get_data(as_text=True)

        self.assertTrue('Enquery' in data)
